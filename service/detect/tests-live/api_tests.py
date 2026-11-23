"""Live API Gateway detection tests (D1c, D2a, D2b, D3a, D4a, opt-in D4c).

NOTE (BRIEF-gemini.md r5, Hard Safety Rule 3):
- D3b (oversized 413 POST) is REMOVED and NOT COVERED because the issuer writes a
  durable REFUSED/TOO_LARGE record + tombstone to the production DynamoDB table and
  the watcher locks a 400-day trace for it.
- D3a sends POST /v1/requests with a provably non-UUID Tessera-Request-Key header,
  which service/issuer/tessera_issue/api.py:118-120 rejects with HTTP 400 before
  any DynamoDB read or write.

Transport & safety guarantees:
- TESSERA_API is pinned strictly to an https://<id>.execute-api.us-east-2.amazonaws.com/v1
  origin and stage.
- Custom opener disables HTTP proxies and refuses ALL redirects (SafetyViolation).
- TESSERA_SMOKE_KEY is sent ONLY to the exact pinned host.
- One process-wide RateLimiter paces ALL API traffic (< 5 rps, burst 1).
- POST refusal (non-2xx) is asserted immediately on HTTP status before reading the body.
- Per-attempt evidence (UUID, timestamp, status, x-amzn-requestid, error_type) is
  preserved even if a batch fails mid-way; no raw response bodies or URLs are logged.
"""

from __future__ import annotations

import os
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any

from ledger import RunLedger, utc_now_iso
from safety import (
    RateLimiter,
    SafetyViolation,
    SmokeTestQuotaTracker,
    assert_post_was_refused,
    assert_safe_api_request,
    validate_tessera_api_url,
)


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Fail closed on any HTTP 3xx redirect so keys and traffic never leave the pinned origin."""

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        raise SafetyViolation(
            f"HTTP {code} redirect refused: redirects are forbidden by Hard Safety Rule 3."
        )


def build_pinned_opener() -> urllib.request.OpenerDirector:
    """Build a urllib opener with proxies disabled and redirects forbidden."""
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        NoRedirectHandler(),
    )


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    pinned_host: str
    base_path: str
    smoke_key: str | None

    @classmethod
    def from_env(cls, *, require_smoke_key: bool = True) -> "ApiConfig":
        raw_url = os.environ.get("TESSERA_API", "").strip()
        if not raw_url:
            raise RuntimeError(
                "Environment variable TESSERA_API is required (never hardcode or save it)."
            )
        normalized, host, base_path = validate_tessera_api_url(raw_url)
        smoke_key = os.environ.get("TESSERA_SMOKE_KEY", "").strip() or None
        if require_smoke_key and not smoke_key:
            raise RuntimeError(
                "Environment variable TESSERA_SMOKE_KEY is required for D3a/D4 tests "
                "(never hardcode or save it)."
            )
        return cls(
            base_url=normalized,
            pinned_host=host,
            base_path=base_path,
            smoke_key=smoke_key,
        )

    @property
    def secrets(self) -> list[str]:
        return [s for s in (self.base_url, self.pinned_host, self.smoke_key) if s]


def _send_http(
    config: ApiConfig,
    *,
    method: str,
    path: str,
    headers: dict[str, str],
    body: bytes | None,
    using_smoke_key: bool,
    post_refusal_mode: str | None,
    limiter: RateLimiter,
    rps: float,
    quota: SmokeTestQuotaTracker | None,
    timeout_s: float = 15.0,
    opener: urllib.request.OpenerDirector | None = None,
) -> dict[str, Any]:
    url = f"{config.base_url}{path}"
    assert_safe_api_request(
        method,
        path,
        headers=headers,
        body=body,
        using_smoke_key=using_smoke_key,
        post_refusal_mode=post_refusal_mode,
        target_url=url,
        pinned_host=config.pinned_host,
        base_path=config.base_path,
    )

    # Ensure TESSERA_SMOKE_KEY is never sent unless explicitly authorized AND host-pinned.
    if config.smoke_key:
        sent_smoke = any(config.smoke_key in str(v) for v in headers.values())
        if sent_smoke and not using_smoke_key:
            raise SafetyViolation("TESSERA_SMOKE_KEY found in headers when using_smoke_key=False.")
        if using_smoke_key and urllib.parse.urlsplit(url).hostname != config.pinned_host:
            raise SafetyViolation("Refusing to send TESSERA_SMOKE_KEY to non-pinned host.")

    if using_smoke_key:
        if quota is None:
            raise SafetyViolation("SmokeTestQuotaTracker is required for smoke-key calls.")
        quota.consume(1)

    limiter.wait(rps=rps)
    sent_at = utc_now_iso()
    req = urllib.request.Request(url=url, data=body, headers=headers, method=method.upper())
    active_opener = opener or build_pinned_opener()

    try:
        with active_opener.open(req, timeout=timeout_s) as resp:
            status = int(resp.status)
            if method.upper() == "POST":
                assert_post_was_refused(status, f"POST {path} ({post_refusal_mode})")
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            # Drain without persisting raw body content (Rule 5).
            resp.read(256)
    except urllib.error.HTTPError as err:
        status = int(err.code)
        if method.upper() == "POST":
            assert_post_was_refused(status, f"POST {path} ({post_refusal_mode})")
        resp_headers = {k.lower(): v for k, v in err.headers.items()} if err.headers else {}
        try:
            err.read(256)
        except Exception:
            pass

    return {
        "sent_at_utc": sent_at,
        "status": status,
        "request_id": resp_headers.get("x-amzn-requestid"),
        "error_type": resp_headers.get("x-amzn-errortype"),
    }


def run_d2a_missing_key(
    config: ApiConfig,
    ledger: RunLedger,
    limiter: RateLimiter,
    *,
    count: int = 55,
    rps: float = 2.0,
    opener: urllib.request.OpenerDirector | None = None,
) -> list[dict[str, Any]]:
    """D2a (missing API key) + D1c (50+ 4XX backstop): 55 GETs with no x-api-key."""
    started = utc_now_iso()
    statuses: dict[str, int] = {}
    error_types: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    request_ids: list[str] = []
    threshold_crossed_at: str | None = None
    qualifying_403 = 0

    try:
        for i in range(count):
            req_uuid = str(uuid.uuid4())
            res = _send_http(
                config,
                method="GET",
                path=f"/v1/requests/{req_uuid}",
                headers={"Accept": "application/json"},
                body=None,
                using_smoke_key=False,
                post_refusal_mode=None,
                limiter=limiter,
                rps=rps,
                quota=None,
                opener=opener,
            )
            st_key = str(res["status"])
            statuses[st_key] = statuses.get(st_key, 0) + 1
            et = res["error_type"] or "none"
            error_types[et] = error_types.get(et, 0) + 1
            if res["request_id"]:
                request_ids.append(res["request_id"])
            if res["status"] == 403:
                qualifying_403 += 1
                if qualifying_403 == 50 and threshold_crossed_at is None:
                    threshold_crossed_at = res["sent_at_utc"]
            attempts.append(
                {
                    "seq": i + 1,
                    "client_uuid": req_uuid,
                    "sent_at_utc": res["sent_at_utc"],
                    "status": res["status"],
                    "request_id": res["request_id"],
                    "error_type": res["error_type"],
                }
            )
    finally:
        ended = utc_now_iso()
        summary = {
            "planned_count": count,
            "completed_count": len(attempts),
            "rps": rps,
            "status_counts": statuses,
            "error_type_counts": error_types,
            "threshold_crossed_at_utc": threshold_crossed_at,
            "attempts": attempts,
        }
        ledger.record_event(
            ["D2a", "D1c"],
            f"GET /v1/requests/<uuid> x{len(attempts)} (missing API key)",
            resource_name="production-api-gateway",
            started_at_utc=started,
            ended_at_utc=ended,
            request_ids=request_ids,
            details=summary,
            safe=True,
        )

    trigger_ts = threshold_crossed_at or ended
    return [
        {
            "row_id": "D2a",
            "action": f"GET /v1/requests/<uuid> x{len(attempts)} (missing API key)",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d2-bad-keys"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": trigger_ts,
            "request_ids": request_ids,
            "contract_latency_s": 600,
            "sns_observable": True,
            "details": {"completed_count": len(attempts), "status_counts": statuses, "error_type_counts": error_types},
        },
        {
            "row_id": "D1c",
            "action": f"GET /v1/requests/<uuid> x{len(attempts)} (4XX backstop via D2a)",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-api-4xx"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": trigger_ts,
            "request_ids": request_ids,
            "contract_latency_s": 600,
            "sns_observable": True,
            "details": {"completed_count": len(attempts), "status_counts": statuses},
        },
    ]


def run_d2b_invalid_key(
    config: ApiConfig,
    ledger: RunLedger,
    limiter: RateLimiter,
    *,
    count: int = 55,
    rps: float = 2.0,
    opener: urllib.request.OpenerDirector | None = None,
) -> list[dict[str, Any]]:
    """D2b (invalid API key): 55 GETs with random invalid x-api-key values."""
    started = utc_now_iso()
    statuses: dict[str, int] = {}
    error_types: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    request_ids: list[str] = []
    threshold_crossed_at: str | None = None
    qualifying_403 = 0

    try:
        for i in range(count):
            req_uuid = str(uuid.uuid4())
            bad_key = f"tessera-dtest-invalid-{uuid.uuid4().hex}"
            res = _send_http(
                config,
                method="GET",
                path=f"/v1/requests/{req_uuid}",
                headers={"Accept": "application/json", "x-api-key": bad_key},
                body=None,
                using_smoke_key=False,
                post_refusal_mode=None,
                limiter=limiter,
                rps=rps,
                quota=None,
                opener=opener,
            )
            st_key = str(res["status"])
            statuses[st_key] = statuses.get(st_key, 0) + 1
            et = res["error_type"] or "none"
            error_types[et] = error_types.get(et, 0) + 1
            if res["request_id"]:
                request_ids.append(res["request_id"])
            if res["status"] == 403:
                qualifying_403 += 1
                if qualifying_403 == 50 and threshold_crossed_at is None:
                    threshold_crossed_at = res["sent_at_utc"]
            attempts.append(
                {
                    "seq": i + 1,
                    "client_uuid": req_uuid,
                    "sent_at_utc": res["sent_at_utc"],
                    "status": res["status"],
                    "request_id": res["request_id"],
                    "error_type": res["error_type"],
                }
            )
    finally:
        ended = utc_now_iso()
        summary = {
            "planned_count": count,
            "completed_count": len(attempts),
            "rps": rps,
            "status_counts": statuses,
            "error_type_counts": error_types,
            "threshold_crossed_at_utc": threshold_crossed_at,
            "attempts": attempts,
        }
        ledger.record_event(
            ["D2b"],
            f"GET /v1/requests/<uuid> x{len(attempts)} (invalid API key)",
            resource_name="production-api-gateway",
            started_at_utc=started,
            ended_at_utc=ended,
            request_ids=request_ids,
            details=summary,
            safe=True,
        )

    return [
        {
            "row_id": "D2b",
            "action": f"GET /v1/requests/<uuid> x{len(attempts)} (invalid API key)",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d2-bad-keys"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": threshold_crossed_at or ended,
            "request_ids": request_ids,
            "contract_latency_s": 600,
            "sns_observable": True,
            "details": {"completed_count": len(attempts), "status_counts": statuses, "error_type_counts": error_types},
        }
    ]


def run_d3a_malformed_post(
    config: ApiConfig,
    ledger: RunLedger,
    limiter: RateLimiter,
    quota: SmokeTestQuotaTracker,
    *,
    count: int = 6,
    rps: float = 0.5,
    opener: urllib.request.OpenerDirector | None = None,
) -> list[dict[str, Any]]:
    """D3a (invalid Tessera-Request-Key header -> 400 before any DB write): 6 POSTs."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D3a.")
    quota.ensure_headroom(count, "D3a")
    started = utc_now_iso()
    statuses: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    request_ids: list[str] = []
    threshold_crossed_at: str | None = None
    qualifying_400 = 0

    try:
        for i in range(count):
            res = _send_http(
                config,
                method="POST",
                path="/v1/requests",
                headers={
                    "x-api-key": config.smoke_key,
                    "Content-Type": "application/octet-stream",
                    # Rejected at api.py:118-120 with 400 before any DynamoDB read or write.
                    "Tessera-Request-Key": f"tessera-dtest-malformed-not-a-uuid-{i}",
                },
                body=b"tessera-dtest-malformed-payload",
                using_smoke_key=True,
                post_refusal_mode="malformed_400",
                limiter=limiter,
                rps=rps,
                quota=quota,
                opener=opener,
            )
            st_key = str(res["status"])
            statuses[st_key] = statuses.get(st_key, 0) + 1
            if res["request_id"]:
                request_ids.append(res["request_id"])
            if res["status"] == 400:
                qualifying_400 += 1
                if qualifying_400 == 5 and threshold_crossed_at is None:
                    threshold_crossed_at = res["sent_at_utc"]
            attempts.append(
                {
                    "seq": i + 1,
                    "sent_at_utc": res["sent_at_utc"],
                    "status": res["status"],
                    "request_id": res["request_id"],
                    "error_type": res["error_type"],
                }
            )
    finally:
        ended = utc_now_iso()
        summary = {
            "planned_count": count,
            "completed_count": len(attempts),
            "rps": rps,
            "status_counts": statuses,
            "smoke_quota_used_run": quota.count,
            "smoke_quota_used_daily": quota.total_daily_count,
            "threshold_crossed_at_utc": threshold_crossed_at,
            "attempts": attempts,
        }
        ledger.record_event(
            ["D3a"],
            f"POST /v1/requests x{len(attempts)} (non-UUID Tessera-Request-Key header, expect 400, no DB write)",
            resource_name="production-api-gateway",
            started_at_utc=started,
            ended_at_utc=ended,
            request_ids=request_ids,
            details=summary,
            safe=True,
        )

    return [
        {
            "row_id": "D3a",
            "action": f"POST /v1/requests x{len(attempts)} (invalid non-UUID Tessera-Request-Key header -> 400)",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d3-smoke-test"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": threshold_crossed_at or ended,
            "request_ids": request_ids,
            "contract_latency_s": 900,
            "sns_observable": True,
            "details": {"completed_count": len(attempts), "status_counts": statuses},
        }
    ]


def run_d4a_smoke_volume(
    config: ApiConfig,
    ledger: RunLedger,
    limiter: RateLimiter,
    quota: SmokeTestQuotaTracker,
    *,
    target_total: int = 55,
    rps: float = 0.125,  # 1 req / 8s => <= 38 req per 5 min (avoids D1c 50+ 4XX/5min)
    opener: urllib.request.OpenerDirector | None = None,
) -> list[dict[str, Any]]:
    """D4a: bring smoke-test daily logged count above 50 using read-only GETs, paced to avoid D1c."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D4a.")
    to_send = max(0, target_total - quota.total_daily_count)
    quota.ensure_headroom(to_send, "D4a")
    started = utc_now_iso()
    statuses: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    request_ids: list[str] = []
    threshold_crossed_at: str | None = None

    try:
        for i in range(to_send):
            req_uuid = str(uuid.uuid4())
            res = _send_http(
                config,
                method="GET",
                path=f"/v1/requests/{req_uuid}",
                headers={"Accept": "application/json", "x-api-key": config.smoke_key},
                body=None,
                using_smoke_key=True,
                post_refusal_mode=None,
                limiter=limiter,
                rps=rps,
                quota=quota,
                opener=opener,
            )
            st_key = str(res["status"])
            statuses[st_key] = statuses.get(st_key, 0) + 1
            if res["request_id"]:
                request_ids.append(res["request_id"])
            if quota.total_daily_count >= 51 and threshold_crossed_at is None:
                threshold_crossed_at = res["sent_at_utc"]
            attempts.append(
                {
                    "seq": i + 1,
                    "client_uuid": req_uuid,
                    "sent_at_utc": res["sent_at_utc"],
                    "status": res["status"],
                    "request_id": res["request_id"],
                    "error_type": res["error_type"],
                    "daily_count_after": quota.total_daily_count,
                }
            )
    finally:
        ended = utc_now_iso()
        summary = {
            "planned_this_step": to_send,
            "completed_this_step": len(attempts),
            "prior_daily_count": quota.prior_count,
            "cumulative_smoke_requests_daily": quota.total_daily_count,
            "rps": rps,
            "status_counts": statuses,
            "threshold_crossed_at_utc": threshold_crossed_at,
            "attempts": attempts,
        }
        ledger.record_event(
            ["D4a"],
            f"GET /v1/requests/<uuid> x{len(attempts)} with smoke-test key (daily={quota.total_daily_count})",
            resource_name="production-api-gateway",
            started_at_utc=started,
            ended_at_utc=ended,
            request_ids=request_ids,
            details=summary,
            safe=True,
        )

    return [
        {
            "row_id": "D4a",
            "action": f"GET /v1/requests/<uuid> x{len(attempts)} with smoke-test key (daily > 50)",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d4-volume-smoke-test"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": threshold_crossed_at or ended,
            "request_ids": request_ids,
            "contract_latency_s": 900,
            "sns_observable": True,
            "details": {
                "completed_this_step": len(attempts),
                "cumulative_smoke_requests_daily": quota.total_daily_count,
                "status_counts": statuses,
            },
        }
    ]


def run_d4c_quota_exceeded(
    config: ApiConfig,
    ledger: RunLedger,
    limiter: RateLimiter,
    quota: SmokeTestQuotaTracker,
    *,
    rps: float = 0.125,
    opener: urllib.request.OpenerDirector | None = None,
) -> list[dict[str, Any]]:
    """D4c (opt-in final step): send paced read-only GETs until 429 QUOTA_EXCEEDED.

    Does NOT treat a generic 429 THROTTLED as a pass: stops only on a 429 whose
    error_type is QUOTA_EXCEEDED (or when the hard 120 daily cap is reached), and
    requires read-only access-log correlation for error=='QUOTA_EXCEEDED'.
    """
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D4c.")
    quota.raise_cap_for_d4c(120)
    started = utc_now_iso()
    statuses: dict[str, int] = {}
    error_types: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    request_ids: list[str] = []
    quota_429_request_id: str | None = None
    quota_429_at: str | None = None
    throttled_429_count = 0

    try:
        while quota.total_daily_count < quota.max_requests:
            req_uuid = str(uuid.uuid4())
            res = _send_http(
                config,
                method="GET",
                path=f"/v1/requests/{req_uuid}",
                headers={"Accept": "application/json", "x-api-key": config.smoke_key},
                body=None,
                using_smoke_key=True,
                post_refusal_mode=None,
                limiter=limiter,
                rps=rps,
                quota=quota,
                opener=opener,
            )
            st_key = str(res["status"])
            statuses[st_key] = statuses.get(st_key, 0) + 1
            et = res["error_type"] or "none"
            error_types[et] = error_types.get(et, 0) + 1
            if res["request_id"]:
                request_ids.append(res["request_id"])
            attempts.append(
                {
                    "seq": len(attempts) + 1,
                    "client_uuid": req_uuid,
                    "sent_at_utc": res["sent_at_utc"],
                    "status": res["status"],
                    "request_id": res["request_id"],
                    "error_type": res["error_type"],
                }
            )
            if res["status"] == 429:
                et_up = (res["error_type"] or "").upper()
                if "THROTTLED" in et_up or "TOOMANYREQUESTS" in et_up:
                    throttled_429_count += 1
                    continue
                if "QUOTA" in et_up or et_up == "":
                    # API Gateway returns x-amzn-errortype: LimitExceededException for quota exhaustion.
                    # Access-log correlation confirms exact error=="QUOTA_EXCEEDED".
                    quota_429_request_id = res["request_id"]
                    quota_429_at = res["sent_at_utc"]
                    break
                if "LIMITEXCEEDED" in et_up:
                    quota_429_request_id = res["request_id"]
                    quota_429_at = res["sent_at_utc"]
                    break
    finally:
        ended = utc_now_iso()
        summary = {
            "completed_this_step": len(attempts),
            "cumulative_smoke_requests_daily": quota.total_daily_count,
            "observed_quota_429": quota_429_request_id is not None,
            "quota_429_request_id": quota_429_request_id,
            "throttled_429_count": throttled_429_count,
            "status_counts": statuses,
            "error_type_counts": error_types,
            "attempts": attempts,
        }
        ledger.record_event(
            ["D4c"],
            f"GET /v1/requests/<uuid> with smoke-test key until 429 QUOTA_EXCEEDED (sent={len(attempts)})",
            resource_name="production-api-gateway",
            started_at_utc=started,
            ended_at_utc=ended,
            request_ids=request_ids,
            details=summary,
            safe=True,
        )

    return [
        {
            "row_id": "D4c",
            "action": f"GET /v1/requests/<uuid> with smoke-test key until 429 QUOTA_EXCEEDED (sent={len(attempts)})",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d4-quota"],
            "started_at_utc": started,
            "ended_at_utc": ended,
            "trigger_timestamp_utc": quota_429_at or ended,
            "request_ids": request_ids,
            "require_access_log_error": "QUOTA_EXCEEDED",
            "contract_latency_s": 900,
            "sns_observable": True,
            "details": {
                "completed_this_step": len(attempts),
                "observed_quota_429": quota_429_request_id is not None,
                "quota_429_request_id": quota_429_request_id,
                "throttled_429_count": throttled_429_count,
                "status_counts": statuses,
            },
        }
    ]
