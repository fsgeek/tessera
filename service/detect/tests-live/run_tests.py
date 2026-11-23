#!/usr/bin/env python3
"""CLI runner for Tessera V1 live detection tests.

Safety & fidelity guarantees (BRIEF-gemini.md r5):
- Never writes credentials, API keys, SQS URLs, HTTP URLs, or raw exception text
  to stdout, stderr, or disk (Rule 5).
- D3b (oversized 413 POST) is REMOVED and NOT COVERED (Rule 3 r5: no recorded POSTs).
- Rejects incompatible flags (e.g., --dry-run with --cleanup-ledger).
- Refuses to start if a ledger or any AWS resource with run_id already exists.
- Uses ONE process-wide RateLimiter for all API traffic and checks prior daily
  smoke-test usage before running smoke-key tests.
- Enforces opt-in flags on deduplicated selection AND again at final dispatch,
  and enforces D4c strictly last.
- Keeps the observer SQS queue subscribed before stimuli and polling long enough
  for each executed row's contract latency (up to 1 h for watcher IAM rows).
- Joins every executed row's stimulus with CloudTrail events, CloudWatch alarm
  history, read-only access logs, and observed SNS messages by exact identifiers,
  producing per-row evidence and a steward mailbox handoff block.
- Crash recovery (--cleanup-ledger) verifies every target live, persists results,
  and exits non-zero on any refused, failed, or residual resource.
"""

from __future__ import annotations

import argparse
import os
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from api_tests import (
    ApiConfig,
    run_d2a_missing_key,
    run_d2b_invalid_key,
    run_d3a_malformed_post,
    run_d4a_smoke_volume,
    run_d4c_quota_exceeded,
)
from d7_tests import (
    assert_no_existing_run_resources,
    cleanup_from_ledger_file,
    get_caller_identity,
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
from observer import (
    AlarmObserver,
    correlate_access_logs,
    count_today_smoke_requests,
    describe_recent_alarm_transitions,
    lookup_cloudtrail_events,
    wait_for_alarms_ok,
)
from safety import (
    ALLOWED_REGION,
    RateLimiter,
    SafetyViolation,
    SmokeTestQuotaTracker,
    assert_aws_env_safe,
    safe_error_label,
    sanitize_value,
    validate_run_id,
)

# NOTE: d3b is intentionally REMOVED (NOT COVERED under BRIEF-gemini.md r5 Rule 3).
ALL_TESTS = [
    # D7 EventBridge (promised)
    "d7-kms",
    "d7-s3",
    "d7-sns",
    "d7-apigw",
    "d7-lambda",
    "d7-cloudtrail",  # opt-in
    # D7 IAM via watcher (promised, contract latency up to 1 h)
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
    "d4a",
    "d4c",  # opt-in, ALWAYS enforced last
]

OPT_IN_TESTS = {
    "d7-cloudtrail": "include_cloudtrail",
    "d7-iam-access-key": "include_iam_access_key",
    "d4c": "include_quota_exhaustion",
}

SUITES: dict[str, list[str]] = {
    "d7": ["d7-kms", "d7-s3", "d7-sns", "d7-apigw", "d7-lambda", "d7-cloudtrail"],
    "d7-iam": ["d7-iam-role", "d7-iam-access-key"],
    "d7-sup": ["d7-sup-sqs", "d7-sup-ddb", "d7-sup-cw", "d7-sup-logs", "d7-sup-eb"],
    "api": ["d2a", "d2b", "d3a", "d4a", "d4c"],
    "d2": ["d2a", "d2b"],
    "d3": ["d3a"],
    "d4": ["d4a", "d4c"],
    "all": ALL_TESTS,
}

# Contract latency (seconds) per test suite item, used for default observer retention.
TEST_CONTRACT_LATENCY_S: dict[str, int] = {
    "d7-kms": 600,
    "d7-s3": 600,
    "d7-sns": 600,
    "d7-apigw": 600,
    "d7-lambda": 600,
    "d7-cloudtrail": 600,
    "d7-iam-role": 3600,
    "d7-iam-access-key": 3600,
    "d7-sup-sqs": 600,
    "d7-sup-ddb": 600,
    "d7-sup-cw": 600,
    "d7-sup-logs": 600,
    "d7-sup-eb": 600,
    "d2a": 600,
    "d2b": 600,
    "d3a": 900,
    "d4a": 900,
    "d4c": 900,
}

API_BASELINE_ALARMS: dict[str, list[str]] = {
    "d2a": ["tessera-v1-d2-bad-keys", "tessera-v1-api-4xx"],
    "d2b": ["tessera-v1-d2-bad-keys", "tessera-v1-api-4xx"],
    "d3a": ["tessera-v1-d3-smoke-test"],
    "d4a": ["tessera-v1-d4-volume-smoke-test"],
    "d4c": ["tessera-v1-d4-quota"],
}


def _default_run_id() -> str:
    day = datetime.now(timezone.utc).strftime("%m%d")
    return f"{day}{secrets.token_hex(3)}"


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    raw = ts.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _select_tests(args: argparse.Namespace) -> list[str]:
    if args.only:
        raw_items = [t.strip() for t in args.only.split(",") if t.strip()]
        unknown = [t for t in raw_items if t not in ALL_TESTS]
        if unknown:
            raise SystemExit(f"Unknown or removed test(s): {unknown}. Valid: {ALL_TESTS}")
        # Deduplicate preserving order (Finding 10).
        selected = list(dict.fromkeys(raw_items))
    else:
        selected = list(SUITES[args.suite])

    # Filter out opt-in tests with list comprehension so duplicates can never survive.
    selected = [
        t
        for t in selected
        if t not in OPT_IN_TESTS or bool(getattr(args, OPT_IN_TESTS[t], False))
    ]

    # Always enforce d4c strictly LAST so quota exhaustion never impairs earlier tests.
    if "d4c" in selected:
        selected = [t for t in selected if t != "d4c"] + ["d4c"]
    return selected


def _assert_opt_in_allowed(test_name: str, args: argparse.Namespace) -> None:
    flag = OPT_IN_TESTS.get(test_name)
    if flag and not bool(getattr(args, flag, False)):
        raise SafetyViolation(f"Refusing to dispatch opt-in test {test_name!r} without --{flag.replace('_', '-')}.")


def compute_required_wait_seconds(selected: list[str], *, observer_enabled: bool) -> int:
    """Compute required SNS observation window from selected rows' contract latencies (Finding 14)."""
    latencies = [TEST_CONTRACT_LATENCY_S.get(t, 600) for t in selected]
    if observer_enabled:
        latencies.append(600)  # D7-sns-sub-subscribe
    return max(latencies) if latencies else 0


def correlate_row_results(
    stimuli: list[dict[str, Any]],
    sns_messages: list[dict[str, Any]],
    alarm_transitions: list[dict[str, Any]],
    *,
    ct_events_by_row: dict[str, list[dict[str, Any]]] | None = None,
    access_logs_by_row: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Join each executed stimulus with CloudTrail, CloudWatch, access logs, and SNS by IDs (Findings 13 & 17)."""
    ct_map = ct_events_by_row or {}
    log_map = access_logs_by_row or {}
    row_results: list[dict[str, Any]] = []
    mailbox_handoff: list[dict[str, Any]] = []

    for stim in stimuli:
        row_id = stim["row_id"]
        kind = stim["kind"]
        started_dt = _parse_iso(stim.get("trigger_timestamp_utc") or stim.get("started_at_utc"))
        latency_s = int(stim.get("contract_latency_s", 600))
        deadline_iso = (
            (started_dt + timedelta(seconds=latency_s)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            if started_dt
            else None
        )

        matched_sns: list[dict[str, Any]] = []
        matched_alarms: list[dict[str, Any]] = []
        matched_ct = ct_map.get(row_id, [])
        matched_logs = log_map.get(row_id, [])
        corr_ids: dict[str, Any] = {"resource_name": stim.get("resource_name")}

        if kind in ("d7_eventbridge", "d7_watcher_iam"):
            # Require exact CloudTrail eventID join AND successful action (no errorCode) where claimed.
            succeeded_ct_ids = {
                ev["event_id"] for ev in matched_ct if ev.get("succeeded") and ev.get("event_id")
            }
            all_ct_ids = {ev["event_id"] for ev in matched_ct if ev.get("event_id")}
            corr_ids["cloudtrail_event_ids"] = sorted(succeeded_ct_ids or all_ct_ids)
            corr_ids["expected_event_names"] = stim.get("expected_event_names", [])

            for msg in sns_messages:
                ids = msg.get("identifiers", {})
                msg_ev_id = ids.get("cloudtrail_event_id")
                if msg_ev_id and msg_ev_id in succeeded_ct_ids:
                    matched_sns.append(msg)
        elif kind == "api_alarm":
            expected_alarms = set(stim.get("expected_alarm_names", []))
            corr_ids["expected_alarm_names"] = sorted(expected_alarms)
            corr_ids["request_ids_count"] = len(stim.get("request_ids", []))
            corr_ids["access_log_matched_count"] = len(matched_logs)

            # Match CloudWatch OK -> ALARM transitions occurring at/after stimulus start.
            window_start = _parse_iso(stim.get("started_at_utc"))
            for tr in alarm_transitions:
                if tr.get("alarm_name") not in expected_alarms:
                    continue
                if tr.get("new_state") != "ALARM":
                    continue
                tr_dt = _parse_iso(tr.get("state_updated_timestamp"))
                if window_start and tr_dt and tr_dt < window_start - timedelta(seconds=5):
                    continue
                matched_alarms.append(tr)

            corr_ids["alarm_state_changes"] = [
                {
                    "alarm_name": tr["alarm_name"],
                    "state_updated_timestamp": tr["state_updated_timestamp"],
                }
                for tr in matched_alarms
            ]

            for msg in sns_messages:
                ids = msg.get("identifiers", {})
                if ids.get("alarm_name") in expected_alarms and ids.get("new_state") == "ALARM":
                    msg_ts = _parse_iso(ids.get("state_change_time") or msg.get("sns_timestamp_utc"))
                    if window_start and msg_ts and msg_ts < window_start - timedelta(seconds=5):
                        continue
                    matched_sns.append(msg)

        # Extra check for D4c: must have logged error == QUOTA_EXCEEDED in access logs.
        required_log_err = stim.get("require_access_log_error")
        log_err_verified = True
        if required_log_err:
            log_err_verified = any(m.get("error") == required_log_err for m in matched_logs)

        if not stim.get("sns_observable", True):
            overall_status = "PENDING_EMAIL_ONLY"
        elif kind == "api_alarm":
            if matched_alarms and matched_sns and log_err_verified:
                overall_status = "OBSERVED_ALARM_AND_SNS_PENDING_EMAIL"
            else:
                overall_status = "OPEN_MISSING_CORRELATED_EVIDENCE"
        else:
            if matched_sns and stim.get("api_call_succeeded", False):
                overall_status = "OBSERVED_SNS_PENDING_EMAIL"
            else:
                overall_status = "OPEN_MISSING_CORRELATED_EVIDENCE"

        sns_summary = [
            {
                "sns_message_id": m.get("sns_message_id"),
                "sns_timestamp_utc": m.get("sns_timestamp_utc"),
                "sqs_sent_at_utc": m.get("sqs_sent_at_utc"),
                "received_at_utc": m.get("received_at_utc"),
                "message_format": m.get("message_format"),
                "identifiers": m.get("identifiers", {}),
            }
            for m in matched_sns
        ]

        row_results.append(
            {
                "row_id": row_id,
                "action": stim["action"],
                "kind": kind,
                "resource_name": stim.get("resource_name"),
                "started_at_utc": stim.get("started_at_utc"),
                "ended_at_utc": stim.get("ended_at_utc"),
                "trigger_timestamp_utc": stim.get("trigger_timestamp_utc") or stim.get("started_at_utc"),
                "contract_latency_s": latency_s,
                "mailbox_deadline_utc": deadline_iso,
                "overall_status": overall_status,
                "cloudtrail_events": matched_ct,
                "cloudwatch_alarm_transitions": matched_alarms,
                "access_log_error_verified": log_err_verified,
                "sns_evidence": sns_summary,
                "email_evidence": {
                    "status": "PENDING_STEWARD_MAILBOX_READ",
                    "deadline_utc": deadline_iso,
                    "correlating_identifiers": corr_ids,
                },
            }
        )
        mailbox_handoff.append(
            {
                "row_id": row_id,
                "action": stim["action"],
                "event_time_utc": stim.get("trigger_timestamp_utc") or stim.get("started_at_utc"),
                "deadline_utc": deadline_iso,
                "correlating_identifiers": corr_ids,
            }
        )

    return row_results, mailbox_handoff


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
    p.add_argument("--include-quota-exhaustion", action="store_true", help="Opt-in: run D4c QUOTA_EXCEEDED last (exhausts smoke-test daily quota)")
    p.add_argument(
        "--wait-sns-seconds",
        type=int,
        default=None,
        help="Override observer SNS poll duration in seconds (default: auto from max contract latency, up to 3600s for IAM)",
    )
    p.add_argument(
        "--baseline-wait-seconds",
        type=int,
        default=900,
        help="Max seconds to wait for CloudWatch alarms to reach clean OK baseline before API rows (default: 900)",
    )
    p.add_argument(
        "--prior-smoke-count",
        type=int,
        default=0,
        help="Known prior same-day smoke-test requests (combined with read-only access-log count)",
    )
    p.add_argument("--cleanup-ledger", help="Crash-recovery mode: verify live and clean up lingering resources from a ledger JSON")
    return p


def _print_sanitized(text: str, secrets_list: list[str] | None = None, *, stream: Any = None) -> None:
    out = sanitize_value(text, secrets_list or [])
    print(out, file=stream or sys.stdout)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    assert_aws_env_safe()

    # Reject incompatible flags (Finding 7).
    if args.dry_run and args.cleanup_ledger:
        _print_sanitized(
            "[ERROR] --dry-run and --cleanup-ledger are mutually exclusive.",
            stream=sys.stderr,
        )
        return 2

    if args.cleanup_ledger:
        _print_sanitized(f"[cleanup] Verifying live and sweeping resources for ledger: {Path(args.cleanup_ledger).name}")
        try:
            result = cleanup_from_ledger_file(args.cleanup_ledger)
        except Exception as exc:
            _print_sanitized(f"[ERROR] Recovery aborted: {safe_error_label(exc)}", stream=sys.stderr)
            return 1
        for line in result["actions"]:
            _print_sanitized(f"  {line}")
        if result["refused"]:
            _print_sanitized(f"[cleanup] REFUSED {len(result['refused'])} unverified resource(s).", stream=sys.stderr)
        if result["residuals"]:
            _print_sanitized(f"[cleanup] RESIDUAL resources still exist: {result['residuals']}", stream=sys.stderr)
        return 0 if result["ok"] else 1

    run_id = validate_run_id(args.run_id or _default_run_id())
    selected = _select_tests(args)
    needs_api = any(t in ("d2a", "d2b", "d3a", "d4a", "d4c") for t in selected)
    needs_smoke_key = any(t in ("d3a", "d4a", "d4c") for t in selected)
    required_wait_s = compute_required_wait_seconds(selected, observer_enabled=not args.skip_observer)
    effective_wait_s = required_wait_s if args.wait_sns_seconds is None else args.wait_sns_seconds

    _print_sanitized(f"Tessera V1 Detection Tests | run_id={run_id} | region={ALLOWED_REGION}")
    _print_sanitized(f"Selected tests ({len(selected)}): {', '.join(selected) if selected else '(none)'}")
    _print_sanitized(f"Observer SNS wait window: {effective_wait_s}s (contract requirement: {required_wait_s}s)")

    if args.dry_run:
        _print_sanitized("DRY RUN: No AWS or API calls will be made.")
        _print_sanitized(f"  TESSERA_API set: {bool(os.environ.get('TESSERA_API'))}")
        _print_sanitized(f"  TESSERA_SMOKE_KEY set: {bool(os.environ.get('TESSERA_SMOKE_KEY'))}")
        _print_sanitized(f"  Observer SQS on tessera-v1-alarms: {'disabled' if args.skip_observer else 'enabled'}")
        _print_sanitized(f"  Resource naming prefix: tessera-dtest-{run_id}-*")
        return 0

    api_config: ApiConfig | None = None
    secrets_to_redact: list[str] = []
    try:
        if needs_api:
            api_config = ApiConfig.from_env(require_smoke_key=needs_smoke_key)
            secrets_to_redact = api_config.secrets
    except Exception as exc:
        _print_sanitized(f"[ERROR] API config validation failed: {safe_error_label(exc)}", stream=sys.stderr)
        return 1

    ledger_path = Path(args.output_dir) / f"ledger-{run_id}.json"
    try:
        ledger = RunLedger(
            run_id=run_id,
            path=ledger_path,
            secrets=secrets_to_redact,
            exclusive_create=True,
        )
    except Exception as exc:
        _print_sanitized(f"[ERROR] Ledger init refused: {safe_error_label(exc)}", secrets_to_redact, stream=sys.stderr)
        return 1

    run_start_utc = datetime.now(timezone.utc)
    # Single process-wide limiter for ALL API traffic (Finding 8).
    shared_limiter = RateLimiter(rps=2.0)

    observer: AlarmObserver | None = None
    stimuli: list[dict[str, Any]] = []
    ct_events_by_row: dict[str, list[dict[str, Any]]] = {}
    access_logs_by_row: dict[str, list[dict[str, Any]]] = {}
    exit_code = 0
    try:
        account_id, _ = get_caller_identity()
        ledger.set_account_id(account_id)
        # Refuse to start if any resource with this run_id already exists (Finding 5).
        assert_no_existing_run_resources(run_id, account_id)

        prior_smoke = max(0, int(args.prior_smoke_count))
        if needs_smoke_key:
            try:
                logged_today = count_today_smoke_requests()
                prior_smoke = max(prior_smoke, logged_today)
                ledger.add_note(f"Pre-flight smoke-test daily count from access logs: {logged_today}")
            except Exception as exc:
                ledger.add_note(f"Could not read prior smoke-test access logs: {safe_error_label(exc)}")
        quota = SmokeTestQuotaTracker(max_requests=60, prior_count=prior_smoke)

        if not args.skip_observer:
            observer = AlarmObserver(run_id, ledger, account_id)
            obs_info = observer.start()
            stimuli.append(obs_info["stimulus"])
            _print_sanitized(
                f"[observer] Subscribed throwaway SQS {obs_info['queue_name']} to {obs_info['topic_name']}",
                secrets_to_redact,
            )

        dispatch: dict[str, Callable[[], list[dict[str, Any]]]] = {
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
            "d2a": lambda: run_d2a_missing_key(api_config, ledger, shared_limiter),  # type: ignore[arg-type]
            "d2b": lambda: run_d2b_invalid_key(api_config, ledger, shared_limiter),  # type: ignore[arg-type]
            "d3a": lambda: run_d3a_malformed_post(api_config, ledger, shared_limiter, quota),  # type: ignore[arg-type]
            "d4a": lambda: run_d4a_smoke_volume(api_config, ledger, shared_limiter, quota),  # type: ignore[arg-type]
            "d4c": lambda: run_d4c_quota_exceeded(api_config, ledger, shared_limiter, quota),  # type: ignore[arg-type]
        }

        for test_name in selected:
            _assert_opt_in_allowed(test_name, args)
            baseline_alarms = API_BASELINE_ALARMS.get(test_name)
            if baseline_alarms:
                _print_sanitized(f"[baseline] Waiting for OK baseline on {baseline_alarms} ...", secrets_to_redact)
                wait_for_alarms_ok(baseline_alarms, timeout_s=args.baseline_wait_seconds)
            _print_sanitized(f"[run] Starting {test_name} ...", secrets_to_redact)
            row_stims = dispatch[test_name]()
            stimuli.extend(row_stims)
            _print_sanitized(f"[run] Completed {test_name} ({len(row_stims)} row stimulus record(s))", secrets_to_redact)

        if observer and effective_wait_s > 0:
            if effective_wait_s < required_wait_s:
                ledger.add_note(
                    f"Observer wait ({effective_wait_s}s) was overridden below contract latency ({required_wait_s}s)."
                )
            _print_sanitized(
                f"[observer] Polling throwaway SQS for up to {effective_wait_s}s ...",
                secrets_to_redact,
            )
            msgs = observer.poll(duration_s=effective_wait_s)
            _print_sanitized(f"[observer] Received {len(msgs)} structured SNS message(s).", secrets_to_redact)

        # Read-only correlation passes (CloudTrail for D7, CloudWatch + access logs for API).
        for stim in stimuli:
            st_dt = _parse_iso(stim.get("started_at_utc")) or run_start_utc
            en_dt = _parse_iso(stim.get("ended_at_utc")) or datetime.now(timezone.utc)
            if stim["kind"] in ("d7_eventbridge", "d7_watcher_iam"):
                ct_matches = lookup_cloudtrail_events(
                    event_names=stim.get("expected_event_names", []),
                    start_utc=st_dt,
                    end_utc=en_dt,
                    target_ids=stim.get("target_ids", []),
                    expected_event_source=stim.get("expected_event_source"),
                )
                ct_events_by_row[stim["row_id"]] = ct_matches
            elif stim["kind"] == "api_alarm" and stim.get("request_ids"):
                log_matches = correlate_access_logs(st_dt, en_dt, stim["request_ids"])
                access_logs_by_row[stim["row_id"]] = log_matches
                ledger.record_access_log_matches(log_matches)

        transitions: list[dict[str, Any]] = []
        if needs_api:
            transitions = describe_recent_alarm_transitions(run_start_utc)
            for tr in transitions:
                ledger.record_alarm_transition(tr)
            _print_sanitized(
                f"[alarms] Recorded {len(transitions)} CloudWatch alarm state transition(s).",
                secrets_to_redact,
            )

        row_results, handoff = correlate_row_results(
            stimuli,
            ledger.data.get("sns_messages", []),
            transitions,
            ct_events_by_row=ct_events_by_row,
            access_logs_by_row=access_logs_by_row,
        )
        ledger.set_row_results(row_results)
        ledger.set_steward_mailbox_handoff(handoff)
    except Exception as exc:
        exit_code = 1
        err_label = safe_error_label(exc)
        ledger.add_note(f"Run aborted with error: {err_label}", safe=True)
        _print_sanitized(f"[ERROR] {err_label}", secrets_to_redact, stream=sys.stderr)
    finally:
        unsub_stim: dict[str, Any] | None = None
        if observer:
            unsub_stim = observer.close()
        if unsub_stim:
            stimuli.append(unsub_stim)
            row_results, handoff = correlate_row_results(
                stimuli,
                ledger.data.get("sns_messages", []),
                ledger.data.get("alarm_transitions", []),
                ct_events_by_row=ct_events_by_row,
                access_logs_by_row=access_logs_by_row,
            )
            try:
                ledger.set_row_results(row_results)
                ledger.set_steward_mailbox_handoff(handoff)
            except OSError:
                pass
        ledger.finish()
        _print_sanitized("\n=== Cleanup Ledger Summary ===", secrets_to_redact)
        for line in ledger.cleanup_summary_lines():
            _print_sanitized(line, secrets_to_redact)
        _print_sanitized("\n=== Per-Row Observation Status ===", secrets_to_redact)
        for rr in ledger.data.get("row_results", []):
            _print_sanitized(
                f"- {rr['row_id']}: {rr['overall_status']} (sns={len(rr['sns_evidence'])}, email=PENDING_STEWARD_MAILBOX_READ)",
                secrets_to_redact,
            )
        if ledger.has_uncleaned_resources():
            _print_sanitized(
                f"WARNING: Residual resources need recovery! Run: "
                f"python3 run_tests.py --cleanup-ledger {ledger_path.name}",
                secrets_to_redact,
                stream=sys.stderr,
            )
            exit_code = 1
        _print_sanitized(f"\nSanitized ledger written to: {ledger_path.name}", secrets_to_redact)
        _print_sanitized(
            "Reminder: exit 0 proves only scripted completion + cleanup; hand steward_mailbox_handoff to steward for email correlation.",
            secrets_to_redact,
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
