"""Offline unit tests for built-in safety guards, rate limiting, ledger, and parser.

Runs without AWS credentials, without network access, and without boto3 installed.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ledger import RunLedger
from observer import parse_sns_sqs_message
from safety import (
    ALLOWED_REGION,
    ISSUER_MAX_BODY_BYTES,
    OVERSIZED_PAYLOAD_BYTES,
    RateLimiter,
    SafetyViolation,
    SmokeTestQuotaTracker,
    assert_env_region_safe,
    assert_post_was_refused,
    assert_region,
    assert_safe_api_request,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    make_throwaway_name,
    sanitize_value,
)


def test_region_lock() -> None:
    assert assert_region(ALLOWED_REGION) == "us-east-2"
    for bad in ("us-east-1", "us-west-2", "eu-west-1", "", None):
        with pytest.raises(SafetyViolation):
            assert_region(bad)


def test_env_region_check(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    assert_env_region_safe()

    monkeypatch.setenv("AWS_REGION", "us-east-2")
    assert_env_region_safe()

    monkeypatch.setenv("AWS_REGION", "us-east-1")
    with pytest.raises(SafetyViolation):
        assert_env_region_safe()


def test_throwaway_name_guard_accepts_only_dtest() -> None:
    name = make_throwaway_name("1123abc1", "kms")
    assert name == "tessera-dtest-1123abc1-kms"
    assert_throwaway_name(name)
    assert_throwaway_name(f"alias/{name}", allow_alias_prefix=True)
    assert_throwaway_name(f"arn:aws:sns:us-east-2:123456789012:{name}")
    assert_throwaway_name(f"arn:aws:iam::123456789012:role/{name}")
    assert_throwaway_name(f"https://sqs.us-east-2.amazonaws.com/123456789012/{name}")

    forbidden = [
        "tessera-v1-alarms",
        "alias/tessera-v1-kms",
        "tessera-v1-requests",
        "tessera-dtest-1123abc1-tessera-v1-sneaky",
        "arn:aws:sns:us-east-2:123456789012:tessera-v1-alarms",
        "arn:aws:sns:us-east-1:123456789012:tessera-dtest-1123abc1-topic",
        "https://sqs.us-east-1.amazonaws.com/123456789012/tessera-dtest-1123abc1-q",
        "my-random-bucket",
        "",
    ]
    for bad in forbidden:
        with pytest.raises(SafetyViolation):
            assert_throwaway_name(bad, allow_alias_prefix=True)


def test_registered_id_guard() -> None:
    owned = {"key-123"}
    assert assert_throwaway_id_registered("key-123", owned, "kms:DisableKey") == "key-123"
    with pytest.raises(SafetyViolation):
        assert_throwaway_id_registered("prod-key-999", owned, "kms:DisableKey")


def test_api_request_safety_rules() -> None:
    valid_uuid = str(uuid.uuid4())
    # Allowed read-only GET on /v1/requests/{uuid}
    assert_safe_api_request(
        "GET",
        f"/v1/requests/{valid_uuid}",
        headers={},
        body=None,
        using_smoke_key=False,
    )
    # Disallowed unknown route (Rule 3 narrow exception covers status route only)
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "GET",
            "/v1/unknown-route",
            headers={},
            body=None,
            using_smoke_key=False,
        )
    # Disallowed receipt retrieval or DELETE
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "GET",
            f"/v1/requests/{valid_uuid}/receipt",
            headers={},
            body=None,
            using_smoke_key=True,
        )
    # Allowed malformed POST (non-UUID Tessera-Request-Key)
    assert_safe_api_request(
        "POST",
        "/v1/requests",
        headers={"Tessera-Request-Key": "not-a-uuid"},
        body=b"small",
        using_smoke_key=True,
        post_refusal_mode="malformed_400",
    )
    # CRITICAL: malformed_400 with a VALID UUID would be accepted for issuance! Must refuse.
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "POST",
            "/v1/requests",
            headers={"Tessera-Request-Key": valid_uuid},
            body=b"small",
            using_smoke_key=True,
            post_refusal_mode="malformed_400",
        )
    # Allowed oversized POST (> 1 MiB)
    assert_safe_api_request(
        "POST",
        "/v1/requests",
        headers={"Tessera-Request-Key": valid_uuid},
        body=b"X" * OVERSIZED_PAYLOAD_BYTES,
        using_smoke_key=True,
        post_refusal_mode="oversized_413",
    )
    # Oversized POST with <= 1 MiB body must be refused before sending!
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "POST",
            "/v1/requests",
            headers={"Tessera-Request-Key": valid_uuid},
            body=b"X" * ISSUER_MAX_BODY_BYTES,
            using_smoke_key=True,
            post_refusal_mode="oversized_413",
        )
    # Any 2xx response to POST must abort immediately
    assert_post_was_refused(400, "d3a")
    assert_post_was_refused(413, "d3b")
    with pytest.raises(SafetyViolation):
        assert_post_was_refused(202, "d3a")


def test_rate_limiter_and_quota_tracker() -> None:
    with pytest.raises(SafetyViolation):
        RateLimiter(rps=5.0)  # Must stay strictly below 5 rps
    with pytest.raises(SafetyViolation):
        RateLimiter(rps=0.0)

    now = [100.0]
    slept: list[float] = []

    def fake_clock() -> float:
        return now[0]

    def fake_sleep(dt: float) -> None:
        slept.append(dt)
        now[0] += dt

    rl = RateLimiter(rps=2.0, _clock=fake_clock, _sleeper=fake_sleep)
    rl.wait()
    rl.wait()
    assert len(slept) == 1 and abs(slept[0] - 0.5) < 1e-6

    qt = SmokeTestQuotaTracker(max_requests=2)
    assert qt.consume() == 1
    assert qt.consume() == 2
    with pytest.raises(SafetyViolation):
        qt.consume()


def test_redaction_and_ledger(tmp_path: Path) -> None:
    secrets = ["https://secret.execute-api.us-east-2.amazonaws.com/v1", "my-super-secret-smoke-key"]
    ledger_file = tmp_path / "ledger-test.json"
    ledger = RunLedger(run_id="1123abcd", path=ledger_file, secrets=secrets)
    ledger.record_created("kms_key", "key-uuid-1", "tessera-dtest-1123abcd-kms")
    ledger.record_kms_scheduled_deletion("key-uuid-1", "2026-11-30")
    ledger.add_note(
        "url=https://secret.execute-api.us-east-2.amazonaws.com/v1 "
        "key=my-super-secret-smoke-key aws=AKIAIOSFODNN7EXAMPLE"
    )
    raw = ledger_file.read_text(encoding="utf-8")
    assert "secret.execute-api" not in raw
    assert "my-super-secret-smoke-key" not in raw
    assert "AKIAIOSFODNN7EXAMPLE" not in raw
    assert "scheduled, deletes on 2026-11-30" in raw
    assert not ledger.has_uncleaned_resources()

    clean_dict = sanitize_value({"SecretAccessKey": "s3cr3t", "ok": "hello"}, secrets)
    assert clean_dict["SecretAccessKey"] == "[REDACTED]"
    assert clean_dict["ok"] == "hello"


def test_sns_sqs_parser_extracts_identifiers() -> None:
    inner = json.dumps(
        {
            "detail": {
                "eventID": "ev-12345",
                "eventName": "PutKeyPolicy",
                "eventTime": "2026-11-23T14:00:00Z",
                "eventSource": "kms.amazonaws.com",
            }
        }
    )
    envelope = json.dumps(
        {
            "MessageId": "sns-msg-1",
            "Timestamp": "2026-11-23T14:00:03.000Z",
            "Subject": "Tessera D7",
            "Message": inner,
        }
    )
    parsed = parse_sns_sqs_message(
        body=envelope,
        sent_timestamp_ms="1795442404000",
        received_at_utc="2026-11-23T14:00:05.000000Z",
    )
    assert parsed["sns_message_id"] == "sns-msg-1"
    assert parsed["identifiers"]["cloudtrail_event_id"] == "ev-12345"
    assert parsed["identifiers"]["event_name"] == "PutKeyPolicy"
