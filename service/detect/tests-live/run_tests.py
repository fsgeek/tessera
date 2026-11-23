#!/usr/bin/env python3
"""CLI runner for Tessera V1 live detection tests.

Steward removal pass (2026-11-23):
- No production alarm-topic subscription, no IAM, S3, CloudTrail or Lambda tests.
  Delivery evidence is read-only CloudWatch alarm history (API rows) plus the
  steward's mailbox read; D7 rows carry CloudTrail stimulus proof only.
- TESSERA_API must be exactly the deployed API host (safety.PINNED_API_HOST) and /v1.
- The run ID is generated here (uuid4 hex, 12 chars); it cannot be supplied.
- Preflight (caller identity + tag search for the new run ID) runs BEFORE any ledger
  file exists; if preflight refuses, no ledger is written.
- ONE RUN AT A TIME: an exclusive lock file (O_CREAT|O_EXCL) in the fixed run-output
  directory is held for the whole run or recovery and released in `finally`. Pacing
  and the smoke-key quota guard are per process, so concurrent runs are unsupported.
  If a crash leaves the lock, confirm no run is active, then remove run-output/.lock.
- Recovery (--cleanup-ledger) uses tag search only, persists results, and exits
  non-zero on any refused, failed, or residual resource. All output is redacted to
  resource names and class names.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import uuid
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
    run_d7_kms,
    run_d7_sns,
    run_d7_sup_cw,
    run_d7_sup_ddb,
    run_d7_sup_eb,
    run_d7_sup_logs,
    run_d7_sup_sqs,
)
from ledger import RunLedger
from observer import (
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

RUN_OUTPUT_DIR = Path(__file__).resolve().parent / "run-output"
LOCK_NAME = ".lock"

# Removed in the steward pass (NOT COVERED): d3b, d7-s3, d7-lambda, d7-cloudtrail,
# d7-iam-role, d7-iam-access-key, and the production-topic observer.
ALL_TESTS = [
    "d7-kms",
    "d7-sns",
    "d7-apigw",
    "d7-sup-sqs",
    "d7-sup-ddb",
    "d7-sup-cw",
    "d7-sup-logs",
    "d7-sup-eb",
    "d2a",
    "d2b",
    "d3a",
    "d4a",
    "d4c",  # opt-in, ALWAYS enforced last
]

OPT_IN_TESTS = {"d4c": "include_quota_exhaustion"}

SUITES: dict[str, list[str]] = {
    "d7": ["d7-kms", "d7-sns", "d7-apigw"],
    "d7-sup": ["d7-sup-sqs", "d7-sup-ddb", "d7-sup-cw", "d7-sup-logs", "d7-sup-eb"],
    "api": ["d2a", "d2b", "d3a", "d4a", "d4c"],
    "d2": ["d2a", "d2b"],
    "d3": ["d3a"],
    "d4": ["d4a", "d4c"],
    "all": ALL_TESTS,
}

TEST_CONTRACT_LATENCY_S: dict[str, int] = {t: 600 for t in ALL_TESTS}
TEST_CONTRACT_LATENCY_S.update({"d3a": 900, "d4a": 900, "d4c": 900})

API_TESTS = ("d2a", "d2b", "d3a", "d4a", "d4c")
SMOKE_KEY_TESTS = ("d3a", "d4a", "d4c")

API_BASELINE_ALARMS: dict[str, list[str]] = {
    "d2a": ["tessera-v1-d2-bad-keys", "tessera-v1-api-4xx"],
    "d2b": ["tessera-v1-d2-bad-keys", "tessera-v1-api-4xx"],
    "d3a": ["tessera-v1-d3-smoke-test"],
    "d4a": ["tessera-v1-d4-volume-smoke-test"],
    "d4c": ["tessera-v1-d4-quota"],
}


def generate_run_id() -> str:
    return validate_run_id(uuid.uuid4().hex[:12])


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


class RunLock:
    """Exclusive lock file; refuses if it already exists. Release only what we created."""

    def __init__(self, directory: Path) -> None:
        self.path = Path(directory) / LOCK_NAME
        self._held = False

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise SafetyViolation("Another run holds the run-output lock; only one run at a time is supported.") from exc
        try:
            os.write(fd, f"{os.getpid()}\n".encode())
        finally:
            os.close(fd)
        self._held = True

    def release(self) -> None:
        if self._held:
            self._held = False
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def _select_tests(args: argparse.Namespace) -> list[str]:
    if args.only:
        raw_items = [t.strip() for t in args.only.split(",") if t.strip()]
        unknown = [t for t in raw_items if t not in ALL_TESTS]
        if unknown:
            raise SystemExit("Unknown or removed test name(s) in --only.")
        selected = list(dict.fromkeys(raw_items))
    else:
        selected = list(SUITES[args.suite])
    selected = [t for t in selected if t not in OPT_IN_TESTS or bool(getattr(args, OPT_IN_TESTS[t], False))]
    if "d4c" in selected:
        selected = [t for t in selected if t != "d4c"] + ["d4c"]
    return selected


def _assert_opt_in_allowed(test_name: str, args: argparse.Namespace) -> None:
    flag = OPT_IN_TESTS.get(test_name)
    if flag and not bool(getattr(args, flag, False)):
        raise SafetyViolation("Refusing to dispatch an opt-in test without its flag.")


def compute_required_wait_seconds(selected: list[str]) -> int:
    """Wait before reading CloudTrail and alarm history: max contract latency of selected rows."""
    return max((TEST_CONTRACT_LATENCY_S.get(t, 600) for t in selected), default=0)


def correlate_row_results(
    stimuli: list[dict[str, Any]],
    alarm_transitions: list[dict[str, Any]],
    *,
    ct_events_by_row: dict[str, list[dict[str, Any]]] | None = None,
    access_logs_by_row: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Join each stimulus with CloudTrail (D7) or alarm history + access logs (API) by identifiers."""
    ct_map = ct_events_by_row or {}
    log_map = access_logs_by_row or {}
    row_results: list[dict[str, Any]] = []
    handoff: list[dict[str, Any]] = []

    for stim in stimuli:
        row_id = stim["row_id"]
        kind = stim["kind"]
        trigger = stim.get("trigger_timestamp_utc") or stim.get("started_at_utc")
        started_dt = _parse_iso(trigger)
        latency_s = int(stim.get("contract_latency_s", 600))
        deadline_iso = (
            (started_dt + timedelta(seconds=latency_s)).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if started_dt else None
        )
        matched_ct = ct_map.get(row_id, [])
        matched_logs = log_map.get(row_id, [])
        matched_alarms: list[dict[str, Any]] = []
        corr: dict[str, Any] = {"resource_name": stim.get("resource_name")}

        if kind == "d7_eventbridge":
            ok_ids = sorted({ev["event_id"] for ev in matched_ct if ev.get("succeeded") and ev.get("event_id")})
            corr["cloudtrail_event_ids"] = ok_ids
            corr["expected_event_names"] = stim.get("expected_event_names", [])
            status = (
                "STIMULUS_CONFIRMED_PENDING_EMAIL"
                if ok_ids and stim.get("api_call_succeeded", False)
                else "OPEN_MISSING_STIMULUS_EVIDENCE"
            )
        else:
            expected = set(stim.get("expected_alarm_names", []))
            window_start = _parse_iso(stim.get("started_at_utc"))
            for tr in alarm_transitions:
                if tr.get("alarm_name") not in expected or tr.get("new_state") != "ALARM":
                    continue
                tr_dt = _parse_iso(tr.get("state_updated_timestamp"))
                if window_start and tr_dt and tr_dt < window_start - timedelta(seconds=5):
                    continue
                matched_alarms.append(tr)
            corr["expected_alarm_names"] = sorted(expected)
            corr["request_ids_count"] = len(stim.get("request_ids", []))
            corr["access_log_matched_count"] = len(matched_logs)
            corr["alarm_state_changes"] = [
                {"alarm_name": tr["alarm_name"], "state_updated_timestamp": tr["state_updated_timestamp"]}
                for tr in matched_alarms
            ]
            required_err = stim.get("require_access_log_error")
            log_ok = (not required_err) or any(m.get("error") == required_err for m in matched_logs)
            corr["access_log_error_verified"] = log_ok
            status = "ALARM_FIRED_PENDING_EMAIL" if matched_alarms and log_ok else "OPEN_MISSING_ALARM_EVIDENCE"

        row_results.append(
            {
                "row_id": row_id,
                "action": stim["action"],
                "kind": kind,
                "resource_name": stim.get("resource_name"),
                "started_at_utc": stim.get("started_at_utc"),
                "ended_at_utc": stim.get("ended_at_utc"),
                "trigger_timestamp_utc": trigger,
                "contract_latency_s": latency_s,
                "mailbox_deadline_utc": deadline_iso,
                "overall_status": status,
                "cloudtrail_events": matched_ct,
                "cloudwatch_alarm_transitions": matched_alarms,
                "email_evidence": {"status": "PENDING_STEWARD_MAILBOX_READ", "deadline_utc": deadline_iso},
            }
        )
        handoff.append(
            {
                "row_id": row_id,
                "action": stim["action"],
                "event_time_utc": trigger,
                "deadline_utc": deadline_iso,
                "correlating_identifiers": corr,
            }
        )
    return row_results, handoff


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Tessera V1 live detection tests (us-east-2, tessera-dtest-* only, one run at a time)."
    )
    p.add_argument("--suite", choices=sorted(SUITES.keys()), default="all")
    p.add_argument("--only", help="Comma-separated test names (overrides --suite)")
    p.add_argument("--dry-run", action="store_true", help="Print plan and verify guards; no network/AWS calls, no files")
    p.add_argument("--include-quota-exhaustion", action="store_true", help="Opt-in: run D4c last (exhausts smoke-test daily quota)")
    p.add_argument("--wait-seconds", type=int, default=None, help="Override evidence wait before reading CloudTrail/alarm history")
    p.add_argument("--baseline-wait-seconds", type=int, default=900, help="Max wait for alarms to reach OK before API rows")
    p.add_argument("--prior-smoke-count", type=int, default=0, help="Known prior same-day smoke-test requests")
    p.add_argument("--cleanup-ledger", help="Recovery: ledger file name or path inside run-output/")
    return p


def _out(text: str, secrets: list[str] | None = None, *, stream: Any = None) -> None:
    print(sanitize_value(text, secrets or []), file=stream or sys.stdout)


def _env_secrets() -> list[str]:
    return [v for v in (os.environ.get("TESSERA_SMOKE_KEY", "").strip(), os.environ.get("TESSERA_API", "").strip()) if v]


def _resolve_ledger_path(raw: str, output_dir: Path) -> Path:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = output_dir / candidate.name
    candidate = candidate.resolve()
    if candidate.parent != output_dir.resolve() or not candidate.name.startswith("ledger-") or candidate.suffix != ".json":
        raise SafetyViolation("Recovery ledger must be a ledger-<run_id>.json file inside run-output/.")
    return candidate


def run_recovery(ledger_arg: str, output_dir: Path, *, session: Any = None) -> int:
    secrets = _env_secrets()
    lock = RunLock(output_dir)
    try:
        lock.acquire()
    except SafetyViolation as exc:
        _out(f"[ERROR] {safe_error_label(exc)}: run-output lock is held.", stream=sys.stderr)
        return 1
    try:
        path = _resolve_ledger_path(ledger_arg, output_dir)
        _out(f"[cleanup] Tag-search recovery for ledger: {path.name}", secrets)
        result = cleanup_from_ledger_file(path, session=session, secrets=secrets)
    except Exception as exc:
        _out(f"[ERROR] Recovery aborted: {safe_error_label(exc)}", secrets, stream=sys.stderr)
        return 1
    finally:
        lock.release()
    for line in result["actions"]:
        _out(f"  {line}", secrets)
    for line in result["refused"] + result["failed"]:
        _out(f"  {line}", secrets, stream=sys.stderr)
    for line in result["residuals"]:
        _out(f"  RESIDUAL {line}", secrets, stream=sys.stderr)
    _out(f"[cleanup] ok={result['ok']} residuals={len(result['residuals'])}", secrets)
    return 0 if result["ok"] else 1


def main(argv: list[str] | None = None, *, output_dir: Path | None = None, session: Any = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(output_dir) if output_dir is not None else RUN_OUTPUT_DIR
    try:
        assert_aws_env_safe()
    except SafetyViolation as exc:
        _out(f"[ERROR] {safe_error_label(exc)}: AWS environment refused.", stream=sys.stderr)
        return 1

    if args.dry_run and args.cleanup_ledger:
        _out("[ERROR] --dry-run and --cleanup-ledger are mutually exclusive.", stream=sys.stderr)
        return 2
    if args.cleanup_ledger:
        return run_recovery(args.cleanup_ledger, out_dir, session=session)

    run_id = generate_run_id()
    selected = _select_tests(args)
    needs_api = any(t in API_TESTS for t in selected)
    needs_smoke_key = any(t in SMOKE_KEY_TESTS for t in selected)
    required_wait_s = compute_required_wait_seconds(selected)
    wait_s = required_wait_s if args.wait_seconds is None else max(0, args.wait_seconds)

    _out(f"Tessera V1 Detection Tests | run_id={run_id} | region={ALLOWED_REGION}")
    _out(f"Selected tests ({len(selected)}): {', '.join(selected) if selected else '(none)'}")
    _out(f"Evidence wait: {wait_s}s (contract requirement: {required_wait_s}s)")

    api_config: ApiConfig | None = None
    secrets: list[str] = []
    api_refusal: str | None = None
    if needs_api:
        try:
            api_config = ApiConfig.from_env(require_smoke_key=needs_smoke_key)
            secrets = api_config.secrets
        except Exception as exc:
            api_refusal = safe_error_label(exc)
            if not args.dry_run:
                _out(f"[ERROR] API config refused: {api_refusal}", stream=sys.stderr)
                return 1

    if args.dry_run:
        _out("DRY RUN: no AWS or API calls, no ledger, no lock.")
        if needs_api:
            _out(f"  TESSERA_API/TESSERA_SMOKE_KEY accepted: {api_config is not None}"
                 + (f" (refused: {api_refusal}; a live run would stop here)" if api_refusal else ""))
        _out(f"  TESSERA_SMOKE_KEY set: {bool(os.environ.get('TESSERA_SMOKE_KEY'))}")
        _out("  Production alarm topic: never called (no observer subscription)")
        _out(f"  Resource naming prefix: tessera-dtest-{run_id}-*")
        return 0

    lock = RunLock(out_dir)
    try:
        lock.acquire()
    except SafetyViolation as exc:
        _out(f"[ERROR] {safe_error_label(exc)}: run-output lock is held; one run at a time.", stream=sys.stderr)
        return 1

    try:
        # Preflight BEFORE any ledger file exists.
        try:
            account_id, _ = get_caller_identity(session=session)
            assert_no_existing_run_resources(run_id, account_id, session=session)
        except Exception as exc:
            _out(f"[ERROR] Preflight refused: {safe_error_label(exc)} (no ledger written)", secrets, stream=sys.stderr)
            return 1
        return _run_with_ledger(args, run_id, account_id, selected, api_config, secrets, wait_s, out_dir, session)
    finally:
        lock.release()


def _run_with_ledger(
    args: argparse.Namespace,
    run_id: str,
    account_id: str,
    selected: list[str],
    api_config: ApiConfig | None,
    secrets: list[str],
    wait_s: int,
    out_dir: Path,
    session: Any,
) -> int:
    ledger_path = out_dir / f"ledger-{run_id}.json"
    try:
        ledger = RunLedger(run_id=run_id, path=ledger_path, secrets=secrets, exclusive_create=True, account_id=account_id)
    except Exception as exc:
        _out(f"[ERROR] Ledger init refused: {safe_error_label(exc)}", secrets, stream=sys.stderr)
        return 1

    run_start = datetime.now(timezone.utc)
    limiter = RateLimiter(rps=2.0)
    stimuli: list[dict[str, Any]] = []
    exit_code = 0
    needs_api = any(t in API_TESTS for t in selected)
    try:
        prior = max(0, int(args.prior_smoke_count))
        if any(t in SMOKE_KEY_TESTS for t in selected):
            # Fail closed: without a successful log read the prior count is unknown.
            logged_today = count_today_smoke_requests(session=session)
            prior = max(prior, logged_today)
            ledger.add_note(f"Pre-flight smoke-test daily count from access logs: {logged_today}")
        quota = SmokeTestQuotaTracker(max_requests=60, prior_count=prior)

        dispatch: dict[str, Callable[[], list[dict[str, Any]]]] = {
            "d7-kms": lambda: run_d7_kms(run_id, ledger, session=session),
            "d7-sns": lambda: run_d7_sns(run_id, ledger, session=session),
            "d7-apigw": lambda: run_d7_apigw(run_id, ledger, session=session),
            "d7-sup-sqs": lambda: run_d7_sup_sqs(run_id, ledger, session=session),
            "d7-sup-ddb": lambda: run_d7_sup_ddb(run_id, ledger, session=session),
            "d7-sup-cw": lambda: run_d7_sup_cw(run_id, ledger, session=session),
            "d7-sup-logs": lambda: run_d7_sup_logs(run_id, ledger, session=session),
            "d7-sup-eb": lambda: run_d7_sup_eb(run_id, ledger, session=session),
            "d2a": lambda: run_d2a_missing_key(api_config, ledger, limiter),  # type: ignore[arg-type]
            "d2b": lambda: run_d2b_invalid_key(api_config, ledger, limiter),  # type: ignore[arg-type]
            "d3a": lambda: run_d3a_malformed_post(api_config, ledger, limiter, quota),  # type: ignore[arg-type]
            "d4a": lambda: run_d4a_smoke_volume(api_config, ledger, limiter, quota),  # type: ignore[arg-type]
            "d4c": lambda: run_d4c_quota_exceeded(api_config, ledger, limiter, quota),  # type: ignore[arg-type]
        }
        for test_name in selected:
            _assert_opt_in_allowed(test_name, args)
            baseline = API_BASELINE_ALARMS.get(test_name)
            if baseline:
                _out(f"[baseline] Waiting for OK on {baseline} ...", secrets)
                wait_for_alarms_ok(baseline, timeout_s=args.baseline_wait_seconds, session=session)
            _out(f"[run] {test_name} ...", secrets)
            row_stims = dispatch[test_name]()
            stimuli.extend(row_stims)
            _out(f"[run] {test_name} done ({len(row_stims)} stimulus record(s))", secrets)

        if wait_s > 0:
            _out(f"[evidence] Waiting {wait_s}s for CloudTrail delivery and alarm evaluation ...", secrets)
            time.sleep(wait_s)

        ct_by_row: dict[str, list[dict[str, Any]]] = {}
        logs_by_row: dict[str, list[dict[str, Any]]] = {}
        for stim in stimuli:
            st = _parse_iso(stim.get("started_at_utc")) or run_start
            en = _parse_iso(stim.get("ended_at_utc")) or datetime.now(timezone.utc)
            if stim["kind"] == "d7_eventbridge":
                ct_by_row[stim["row_id"]] = lookup_cloudtrail_events(
                    event_names=stim.get("expected_event_names", []),
                    start_utc=st,
                    end_utc=en,
                    target_ids=stim.get("target_ids", []),
                    expected_event_source=stim.get("expected_event_source"),
                    session=session,
                )
            elif stim["kind"] == "api_alarm" and stim.get("request_ids"):
                logs_by_row[stim["row_id"]] = correlate_access_logs(st, en, stim["request_ids"], session=session)
                ledger.record_access_log_matches(logs_by_row[stim["row_id"]])

        transitions: list[dict[str, Any]] = []
        if needs_api:
            transitions = describe_recent_alarm_transitions(run_start, session=session)
            for tr in transitions:
                ledger.record_alarm_transition(tr)

        rows, handoff = correlate_row_results(stimuli, transitions, ct_events_by_row=ct_by_row, access_logs_by_row=logs_by_row)
        ledger.set_row_results(rows)
        ledger.set_steward_mailbox_handoff(handoff)
    except Exception as exc:
        exit_code = 1
        ledger.add_note(f"Run aborted with error: {safe_error_label(exc)}", safe=True)
        _out(f"[ERROR] {safe_error_label(exc)}", secrets, stream=sys.stderr)
    finally:
        ledger.finish()
        _out("\n=== Cleanup Ledger Summary ===", secrets)
        for line in ledger.cleanup_summary_lines():
            _out(line, secrets)
        _out("\n=== Per-Row Status ===", secrets)
        for rr in ledger.data.get("row_results", []):
            _out(f"- {rr['row_id']}: {rr['overall_status']} (email=PENDING_STEWARD_MAILBOX_READ)", secrets)
        if ledger.has_uncleaned_resources():
            _out(f"RESIDUAL resources: run recovery: run_tests.py --cleanup-ledger {ledger_path.name}", secrets, stream=sys.stderr)
            exit_code = 1
        _out(f"\nSanitized ledger: {ledger_path.name}", secrets)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
