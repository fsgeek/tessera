#!/usr/bin/env python3
"""CLI runner for Tessera V1 live detection tests.

Never writes credentials, API keys, or endpoint URLs to stdout or disk (Rule 5).
Supports --dry-run (no AWS or API calls), scoped suites, opt-in risky/costly
tests (--include-cloudtrail, --include-iam-access-key, --include-quota-exhaustion),
and crash-recovery cleanup (--cleanup-ledger <path>).
"""

from __future__ import annotations

import argparse
import os
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from api_tests import (
    ApiConfig,
    run_d2a_missing_key,
    run_d2b_invalid_key,
    run_d3a_malformed_post,
    run_d3b_oversized_post,
    run_d4a_smoke_volume,
    run_d4c_quota_exceeded,
)
from d7_tests import (
    cleanup_from_ledger_file,
    run_d7_apigw,
    run_d7_cloudtrail,
    run_d7_iam_access_key,
    run_d7_iam_role,
    run_d7_kms,
    run_d7_lambda,
    run_d7_s3,
    run_d7_sns,
    run_d7_sup_cw,
    run_d7_sup_ddb,
    run_d7_sup_eb,
    run_d7_sup_logs,
    run_d7_sup_sqs,
)
from ledger import RunLedger
from observer import AlarmObserver, describe_recent_alarm_transitions
from safety import (
    ALLOWED_REGION,
    SmokeTestQuotaTracker,
    assert_env_region_safe,
    validate_run_id,
)

ALL_TESTS = [
    # D7 EventBridge (promised)
    "d7-kms",
    "d7-s3",
    "d7-sns",
    "d7-apigw",
    "d7-lambda",
    "d7-cloudtrail",  # opt-in
    # D7 IAM via watcher (promised)
    "d7-iam-role",
    "d7-iam-access-key",  # opt-in
    # D7 EventBridge supplementary checks
    "d7-sup-sqs",
    "d7-sup-ddb",
    "d7-sup-cw",
    "d7-sup-logs",
    "d7-sup-eb",
    # D1-D4 production API Gateway path
    "d2a",
    "d2b",
    "d3a",
    "d3b",
    "d4a",
    "d4c",  # opt-in
]

SUITES: dict[str, list[str]] = {
    "d7": ["d7-kms", "d7-s3", "d7-sns", "d7-apigw", "d7-lambda", "d7-cloudtrail"],
    "d7-iam": ["d7-iam-role", "d7-iam-access-key"],
    "d7-sup": ["d7-sup-sqs", "d7-sup-ddb", "d7-sup-cw", "d7-sup-logs", "d7-sup-eb"],
    "api": ["d2a", "d2b", "d3a", "d3b", "d4a", "d4c"],
    "d2": ["d2a", "d2b"],
    "d3": ["d3a", "d3b"],
    "d4": ["d4a", "d4c"],
    "all": ALL_TESTS,
}


def _default_run_id() -> str:
    day = datetime.now(timezone.utc).strftime("%m%d")
    return f"{day}{secrets.token_hex(3)}"


def _select_tests(args: argparse.Namespace) -> list[str]:
    if args.only:
        selected = [t.strip() for t in args.only.split(",") if t.strip()]
        unknown = [t for t in selected if t not in ALL_TESTS]
        if unknown:
            raise SystemExit(f"Unknown test(s): {unknown}. Valid: {ALL_TESTS}")
    else:
        selected = list(SUITES[args.suite])

    # Opt-in gates unless explicitly enabled
    if "d7-cloudtrail" in selected and not args.include_cloudtrail:
        selected.remove("d7-cloudtrail")
    if "d7-iam-access-key" in selected and not args.include_iam_access_key:
        selected.remove("d7-iam-access-key")
    if "d4c" in selected and not args.include_quota_exhaustion:
        selected.remove("d4c")
    return selected


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Tessera V1 live detection tests (locked to us-east-2, tessera-dtest-* only)."
    )
    p.add_argument("--suite", choices=sorted(SUITES.keys()), default="all")
    p.add_argument("--only", help="Comma-separated test names (overrides --suite)")
    p.add_argument("--run-id", help="Alphanumeric run ID (default: random 10-char)")
    p.add_argument("--output-dir", default="run-output", help="Directory for sanitized ledger JSON")
    p.add_argument("--dry-run", action="store_true", help="Print plan and verify guards; make no network/AWS calls")
    p.add_argument("--skip-observer", action="store_true", help="Do not create/subscribe throwaway SQS observer queue")
    p.add_argument("--include-cloudtrail", action="store_true", help="Opt-in: run D7 CloudTrail on a throwaway trail")
    p.add_argument("--include-iam-access-key", action="store_true", help="Opt-in: run D7 IAM CreateAccessKey on throwaway user")
    p.add_argument("--include-quota-exhaustion", action="store_true", help="Opt-in: run D4c QUOTA_EXCEEDED (exhausts smoke-test daily quota)")
    p.add_argument("--wait-sns-seconds", type=int, default=180, help="Seconds to poll observer SQS queue after tests (default: 180)")
    p.add_argument("--d2-gap-seconds", type=int, default=0, help="Optional pause between D2a and D2b for alarm reset (e.g., 600)")
    p.add_argument("--d3-gap-seconds", type=int, default=0, help="Optional pause between D3a and D3b for alarm reset")
    p.add_argument("--cleanup-ledger", help="Crash-recovery mode: clean up lingering resources from an existing ledger JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    assert_env_region_safe()

    if args.cleanup_ledger:
        print(f"[cleanup] Sweeping lingering tessera-dtest-* resources from {args.cleanup_ledger}")
        results = cleanup_from_ledger_file(args.cleanup_ledger)
        for line in results:
            print(f"  {line}")
        return 0

    run_id = validate_run_id(args.run_id or _default_run_id())
    selected = _select_tests(args)
    needs_api = any(t in ("d2a", "d2b", "d3a", "d3b", "d4a", "d4c") for t in selected)
    needs_smoke_key = any(t in ("d3a", "d3b", "d4a", "d4c") for t in selected)

    print(f"Tessera V1 Detection Tests | run_id={run_id} | region={ALLOWED_REGION}")
    print(f"Selected tests ({len(selected)}): {', '.join(selected) if selected else '(none)'}")

    if args.dry_run:
        print("DRY RUN: No AWS or API calls will be made.")
        print(f"  TESSERA_API set: {bool(os.environ.get('TESSERA_API'))}")
        print(f"  TESSERA_SMOKE_KEY set: {bool(os.environ.get('TESSERA_SMOKE_KEY'))}")
        print(f"  Observer SQS on tessera-v1-alarms: {'disabled' if args.skip_observer else 'enabled'}")
        print(f"  Resource naming prefix: tessera-dtest-{run_id}-*")
        return 0

    api_config: ApiConfig | None = None
    secrets_to_redact: list[str] = []
    if needs_api:
        api_config = ApiConfig.from_env(require_smoke_key=needs_smoke_key)
        secrets_to_redact = api_config.secrets

    quota = SmokeTestQuotaTracker(max_requests=120 if args.include_quota_exhaustion else 60)
    ledger_path = Path(args.output_dir) / f"ledger-{run_id}.json"
    ledger = RunLedger(run_id=run_id, path=ledger_path, secrets=secrets_to_redact)
    run_start_utc = datetime.now(timezone.utc)

    observer: AlarmObserver | None = None
    exit_code = 0
    try:
        if not args.skip_observer:
            observer = AlarmObserver(run_id, ledger)
            obs_info = observer.start()
            print(f"[observer] Subscribed throwaway SQS {observer.queue_name} to {obs_info['topic_arn']}")

        dispatch: dict[str, Callable[[], None]] = {
            "d7-kms": lambda: run_d7_kms(run_id, ledger),
            "d7-s3": lambda: run_d7_s3(run_id, ledger),
            "d7-sns": lambda: run_d7_sns(run_id, ledger),
            "d7-apigw": lambda: run_d7_apigw(run_id, ledger),
            "d7-lambda": lambda: run_d7_lambda(run_id, ledger),
            "d7-cloudtrail": lambda: run_d7_cloudtrail(run_id, ledger),
            "d7-iam-role": lambda: run_d7_iam_role(run_id, ledger),
            "d7-iam-access-key": lambda: run_d7_iam_access_key(run_id, ledger),
            "d7-sup-sqs": lambda: run_d7_sup_sqs(run_id, ledger),
            "d7-sup-ddb": lambda: run_d7_sup_ddb(run_id, ledger),
            "d7-sup-cw": lambda: run_d7_sup_cw(run_id, ledger),
            "d7-sup-logs": lambda: run_d7_sup_logs(run_id, ledger),
            "d7-sup-eb": lambda: run_d7_sup_eb(run_id, ledger),
            "d2a": lambda: run_d2a_missing_key(api_config, ledger),  # type: ignore[arg-type]
            "d2b": lambda: run_d2b_invalid_key(api_config, ledger),  # type: ignore[arg-type]
            "d3a": lambda: run_d3a_malformed_post(api_config, ledger, quota),  # type: ignore[arg-type]
            "d3b": lambda: run_d3b_oversized_post(api_config, ledger, quota),  # type: ignore[arg-type]
            "d4a": lambda: run_d4a_smoke_volume(api_config, ledger, quota),  # type: ignore[arg-type]
            "d4c": lambda: run_d4c_quota_exceeded(api_config, ledger, quota),  # type: ignore[arg-type]
        }

        for test_name in selected:
            print(f"[run] Starting {test_name} ...")
            dispatch[test_name]()
            print(f"[run] Completed {test_name}")
            if test_name == "d2a" and "d2b" in selected and args.d2_gap_seconds > 0:
                print(f"[wait] Sleeping {args.d2_gap_seconds}s between D2a and D2b for alarm reset...")
                time.sleep(args.d2_gap_seconds)
            if test_name == "d3a" and "d3b" in selected and args.d3_gap_seconds > 0:
                print(f"[wait] Sleeping {args.d3_gap_seconds}s between D3a and D3b for alarm reset...")
                time.sleep(args.d3_gap_seconds)

        if observer and args.wait_sns_seconds > 0:
            print(f"[observer] Polling throwaway SQS for {args.wait_sns_seconds}s ...")
            msgs = observer.poll(duration_s=args.wait_sns_seconds)
            print(f"[observer] Received {len(msgs)} SNS message(s).")

        if needs_api:
            transitions = describe_recent_alarm_transitions(run_start_utc)
            for tr in transitions:
                ledger.record_alarm_transition(tr)
            print(f"[alarms] Recorded {len(transitions)} CloudWatch alarm state transition(s).")
    except Exception as exc:
        exit_code = 1
        ledger.add_note(f"Run aborted with error: {type(exc).__name__}: {exc}")
        print(f"[ERROR] {type(exc).__name__}: {exc}", file=sys.stderr)
    finally:
        if observer:
            observer.close()
        ledger.finish()
        print("\n=== Cleanup Ledger Summary ===")
        for line in ledger.cleanup_summary_lines():
            print(line)
        if ledger.has_uncleaned_resources():
            print(
                f"WARNING: Some resources need manual/recovery cleanup! Run: "
                f"python3 run_tests.py --cleanup-ledger {ledger_path}",
                file=sys.stderr,
            )
            exit_code = 1
        print(f"\nSanitized ledger written to: {ledger_path}")
        print("Reminder: ask the steward for email arrival times + correlating IDs from the author's mailbox.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
