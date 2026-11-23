"""Live API Gateway detection tests (D1c, D2a, D2b, D3a, D3b, D4a, opt-in D4c).

Uses only Python standard library urllib.request (no external HTTP packages).
Reads TESSERA_API and TESSERA_SMOKE_KEY exclusively from environment variables
and never writes them to stdout, logs, or ledger files (Hard Safety Rule 5).

Every request is checked by safety.assert_safe_api_request, paced by
safety.RateLimiter (< 5 rps, burst 1), and counted against
safety.SmokeTestQuotaTracker whenever TESSERA_SMOKE_KEY is used. Any 2xx
response to a POST aborts the run immediately (Hard Safety Rule 3).
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any

from ledger import RunLedger, utc_now_iso
from safety import (
    OVERSIZED_PAYLOAD_BYTES,
    RateLimiter,
    SafetyViolation,
    SmokeTestQuotaTracker,
    assert_post_was_refused,
    assert_safe_api_request,
    sanitize_value,
)


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    smoke_key: str | None

    @classmethod
    def from_env(cls, *, require_smoke_key: bool = True) -> "ApiConfig":
        raw_url = os.environ.get("TESSERA_API", "").strip().rstrip("/")
        if not raw_url:
            raise RuntimeError(
                "Environment variable TESSERA_API is required (never hardcode or save it)."
            )
        if not raw_url.startswith("https://"):
            raise SafetyViolation("TESSERA_API must be an https:// URL.")
        smoke_key = os.environ.get("TESSERA_SMOKE_KEY", "").strip() or None
        if require_smoke_key and not smoke_key:
            raise RuntimeError(
                "Environment variable TESSERA_SMOKE_KEY is required for D3/D4 tests "
                "(never hardcode or save it)."
            )
        return cls(base_url=raw_url, smoke_key=smoke_key)

    @property
    def secrets(self) -> list[str]:
        return [s for s in (self.base_url, self.smoke_key) if s]


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
    quota: SmokeTestQuotaTracker | None,
    timeout_s: float = 15.0,
) -> dict[str, Any]:
    assert_safe_api_request(
        method,
        path,
        headers=headers,
        body=body,
        using_smoke_key=using_smoke_key,
        post_refusal_mode=post_refusal_mode,
    )
    if using_smoke_key:
        if quota is None:
            raise SafetyViolation("SmokeTestQuotaTracker is required for smoke-key calls.")
        quota.consume(1)

    limiter.wait()
    url = f"{config.base_url}{path}"
    req = urllib.request.Request(url=url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            snippet = resp.read(256).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        status = err.code
        resp_headers = {k.lower(): v for k, v in err.headers.items()} if err.headers else {}
        try:
            snippet = err.read(256).decode("utf-8", errors="replace")
        except Exception:
            snippet = ""

    if method.upper() == "POST":
        assert_post_was_refused(status, f"POST {path} ({post_refusal_mode})")

    return {
        "status": status,
        "request_id": resp_headers.get("x-amzn-requestid"),
        "error_type": resp_headers.get("x-amzn-errortype"),
        "body_excerpt": sanitize_value(snippet, config.secrets),
    }


def run_d2a_missing_key(
    config: ApiConfig,
    ledger: RunLedger,
    *,
    count: int = 55,
    rps: float = 2.0,
) -> dict[str, Any]:
    """D2a (missing API key) + D1c (50+ 4XX backstop): 55 GETs with no x-api-key."""
    limiter = RateLimiter(rps=rps)
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    error_types: dict[str, int] = {}
    request_ids: list[str] = []

    for _ in range(count):
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
            quota=None,
        )
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        et = res["error_type"] or "none"
        error_types[et] = error_types.get(et, 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])

    ended = utc_now_iso()
    summary = {
        "count": count,
        "rps": rps,
        "status_counts": statuses,
        "error_type_counts": error_types,
    }
    ledger.record_event(
        ["D2a", "D1c"],
        f"GET /v1/requests/<uuid> x{count} (missing API key)",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary


def run_d2b_invalid_key(
    config: ApiConfig,
    ledger: RunLedger,
    *,
    count: int = 55,
    rps: float = 2.0,
) -> dict[str, Any]:
    """D2b (invalid API key): 55 GETs with random invalid x-api-key values."""
    limiter = RateLimiter(rps=rps)
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    error_types: dict[str, int] = {}
    request_ids: list[str] = []

    for _ in range(count):
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
            quota=None,
        )
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        et = res["error_type"] or "none"
        error_types[et] = error_types.get(et, 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])

    ended = utc_now_iso()
    summary = {
        "count": count,
        "rps": rps,
        "status_counts": statuses,
        "error_type_counts": error_types,
    }
    ledger.record_event(
        ["D2b"],
        f"GET /v1/requests/<uuid> x{count} (invalid API key)",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary


def run_d3a_malformed_post(
    config: ApiConfig,
    ledger: RunLedger,
    quota: SmokeTestQuotaTracker,
    *,
    count: int = 6,
    rps: float = 0.5,
) -> dict[str, Any]:
    """D3a (malformed POST -> 400): 6 POST /v1/requests with non-UUID Tessera-Request-Key."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D3a.")
    limiter = RateLimiter(rps=rps)
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    request_ids: list[str] = []

    for i in range(count):
        res = _send_http(
            config,
            method="POST",
            path="/v1/requests",
            headers={
                "x-api-key": config.smoke_key,
                "Content-Type": "application/octet-stream",
                # Provably non-UUID -> issuer must refuse 400 BAD_REQUEST and never accept.
                "Tessera-Request-Key": f"tessera-dtest-malformed-not-a-uuid-{i}",
            },
            body=b"tessera-dtest-malformed-payload",
            using_smoke_key=True,
            post_refusal_mode="malformed_400",
            limiter=limiter,
            quota=quota,
        )
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])

    ended = utc_now_iso()
    summary = {
        "count": count,
        "rps": rps,
        "status_counts": statuses,
        "smoke_quota_used": quota.count,
    }
    ledger.record_event(
        ["D3a"],
        f"POST /v1/requests x{count} (malformed non-UUID Tessera-Request-Key, expect 400)",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary


def run_d3b_oversized_post(
    config: ApiConfig,
    ledger: RunLedger,
    quota: SmokeTestQuotaTracker,
    *,
    count: int = 6,
    rps: float = 0.5,
    payload_bytes: int = OVERSIZED_PAYLOAD_BYTES,
) -> dict[str, Any]:
    """D3b (oversized POST -> 413): 6 POST /v1/requests > 1 MiB (and < 6 MiB Lambda limit)."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D3b.")
    limiter = RateLimiter(rps=rps)
    payload = b"X" * payload_bytes
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    request_ids: list[str] = []

    for _ in range(count):
        res = _send_http(
            config,
            method="POST",
            path="/v1/requests",
            headers={
                "x-api-key": config.smoke_key,
                "Content-Type": "application/octet-stream",
                "Tessera-Request-Key": str(uuid.uuid4()),
            },
            body=payload,
            using_smoke_key=True,
            post_refusal_mode="oversized_413",
            limiter=limiter,
            quota=quota,
        )
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])

    ended = utc_now_iso()
    summary = {
        "count": count,
        "payload_bytes": payload_bytes,
        "rps": rps,
        "status_counts": statuses,
        "smoke_quota_used": quota.count,
    }
    ledger.record_event(
        ["D3b"],
        f"POST /v1/requests x{count} ({payload_bytes} bytes > 1 MiB, expect 413)",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary


def run_d4a_smoke_volume(
    config: ApiConfig,
    ledger: RunLedger,
    quota: SmokeTestQuotaTracker,
    *,
    target_total: int = 55,
    rps: float = 0.125,  # 1 req / 8s => <= 38 req per 5 min (does not trigger D1c 50+ 4XX/5min)
) -> dict[str, Any]:
    """D4a: bring smoke-test daily request count above 50 using read-only GETs, paced to avoid D1c."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D4a.")
    to_send = max(0, target_total - quota.count)
    limiter = RateLimiter(rps=rps)
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    request_ids: list[str] = []

    for _ in range(to_send):
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
            quota=quota,
        )
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])

    ended = utc_now_iso()
    summary = {
        "sent_this_step": to_send,
        "cumulative_smoke_requests": quota.count,
        "rps": rps,
        "status_counts": statuses,
    }
    ledger.record_event(
        ["D4a"],
        f"GET /v1/requests/<uuid> x{to_send} with smoke-test key (cumulative={quota.count} > 50)",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary


def run_d4c_quota_exceeded(
    config: ApiConfig,
    ledger: RunLedger,
    quota: SmokeTestQuotaTracker,
    *,
    rps: float = 0.125,
) -> dict[str, Any]:
    """D4c (opt-in final step): send paced read-only GETs until first 429 QUOTA_EXCEEDED."""
    if not config.smoke_key:
        raise RuntimeError("TESSERA_SMOKE_KEY is required for D4c.")
    limiter = RateLimiter(rps=rps)
    started = utc_now_iso()
    statuses: dict[int, int] = {}
    request_ids: list[str] = []
    quota_429_request_id: str | None = None
    sent = 0

    while quota.count < quota.max_requests:
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
            quota=quota,
        )
        sent += 1
        statuses[res["status"]] = statuses.get(res["status"], 0) + 1
        if res["request_id"]:
            request_ids.append(res["request_id"])
        if res["status"] == 429:
            quota_429_request_id = res["request_id"]
            break

    ended = utc_now_iso()
    summary = {
        "sent_this_step": sent,
        "cumulative_smoke_requests": quota.count,
        "observed_429": quota_429_request_id is not None or 429 in statuses,
        "quota_429_request_id": quota_429_request_id,
        "status_counts": statuses,
    }
    ledger.record_event(
        ["D4c"],
        f"GET /v1/requests/<uuid> with smoke-test key until 429 QUOTA_EXCEEDED (sent={sent})",
        resource_name="production-api-gateway",
        started_at_utc=started,
        ended_at_utc=ended,
        request_ids=request_ids,
        details=summary,
    )
    return summary
