"""Offline unit tests for safety guards, transport pinning, live-verified recovery,
rate limiting, redaction, and evidence correlation.

Runs without AWS credentials, without network access, and without boto3 installed.
"""

from __future__ import annotations

import json
import sys
import types
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import api_tests
import d7_tests
import run_tests
from api_tests import ApiConfig, NoRedirectHandler, _send_http
from ledger import RunLedger, load_ledger
from observer import parse_sns_sqs_message
from safety import (
    ALLOWED_REGION,
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    RUN_ID_TAG_KEY,
    RateLimiter,
    SafetyViolation,
    SmokeTestQuotaTracker,
    assert_aws_env_safe,
    assert_ownership_tags,
    assert_post_was_refused,
    assert_region,
    assert_safe_api_request,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
    safe_error_label,
    sanitize_value,
    validate_tessera_api_url,
)


def test_region_lock_and_env_endpoint_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    assert assert_region(ALLOWED_REGION) == "us-east-2"
    for bad in ("us-east-1", "us-west-2", "eu-west-1", "", None):
        with pytest.raises(SafetyViolation):
            assert_region(bad)

    for var in (
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
        "AWS_ENDPOINT_URL",
        "AWS_ENDPOINT_URL_KMS",
        "AWS_USE_FIPS_ENDPOINT",
        "AWS_USE_DUALSTACK_ENDPOINT",
        "AWS_STS_REGIONAL_ENDPOINTS",
    ):
        monkeypatch.delenv(var, raising=False)
    assert_aws_env_safe()

    monkeypatch.setenv("AWS_REGION", "us-east-2")
    assert_aws_env_safe()

    for var, bad_val in (
        ("AWS_REGION", "us-east-1"),
        ("AWS_DEFAULT_REGION", "us-west-2"),
        ("AWS_ENDPOINT_URL", "https://evil.example.com"),
        ("AWS_ENDPOINT_URL_KMS", "https://kms.us-east-1.amazonaws.com"),
        ("AWS_USE_FIPS_ENDPOINT", "true"),
        ("AWS_USE_DUALSTACK_ENDPOINT", "true"),
        ("AWS_STS_REGIONAL_ENDPOINTS", "legacy"),
    ):
        monkeypatch.setenv(var, bad_val)
        with pytest.raises(SafetyViolation):
            assert_aws_env_safe()
        monkeypatch.delenv(var, raising=False)


def test_locked_boto3_client_refuses_endpoint_override_and_unscoped_iam(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for var in (
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
        "AWS_ENDPOINT_URL",
        "AWS_USE_FIPS_ENDPOINT",
        "AWS_USE_DUALSTACK_ENDPOINT",
        "AWS_STS_REGIONAL_ENDPOINTS",
    ):
        monkeypatch.delenv(var, raising=False)

    class _FakeClient:
        def __init__(self, region: str, endpoint_url: str) -> None:
            self.meta = types.SimpleNamespace(region_name=region, endpoint_url=endpoint_url)

    class _HijackedSession:
        def client(self, service: str, **kwargs: Any) -> Any:
            return _FakeClient("us-east-2", "https://attacker.example.com")

    with pytest.raises(SafetyViolation):
        locked_boto3_client("kms", session=_HijackedSession())

    class _WrongRegionSession:
        def client(self, service: str, **kwargs: Any) -> Any:
            return _FakeClient("us-east-1", "https://kms.us-east-1.amazonaws.com")

    with pytest.raises(SafetyViolation):
        locked_boto3_client("kms", session=_WrongRegionSession())

    class _GoodSession:
        def client(self, service: str, region_name: str, endpoint_url: str) -> Any:
            return _FakeClient(region_name, endpoint_url)

    # IAM requires explicit allow_global_iam=True
    with pytest.raises(SafetyViolation):
        locked_boto3_client("iam", session=_GoodSession())
    iam_client = locked_boto3_client("iam", session=_GoodSession(), allow_global_iam=True)
    assert iam_client.meta.endpoint_url == "https://iam.amazonaws.com"

    kms_client = locked_boto3_client("kms", session=_GoodSession())
    assert kms_client.meta.endpoint_url == "https://kms.us-east-2.amazonaws.com"


def test_throwaway_name_and_sqs_url_strict_binding() -> None:
    run_id = "1123abc1"
    acct = "123456789012"
    name = make_throwaway_name(run_id, "kms")
    assert name == "tessera-dtest-1123abc1-kms"
    assert_throwaway_name(name, run_id=run_id)
    assert_throwaway_name(f"alias/{name}", allow_alias_prefix=True, run_id=run_id)
    assert_throwaway_name(f"arn:aws:sns:us-east-2:{acct}:{name}", run_id=run_id, account_id=acct)
    assert_throwaway_name(f"arn:aws:iam::{acct}:role/{name}", run_id=run_id, account_id=acct)
    assert_throwaway_name(
        f"https://sqs.us-east-2.amazonaws.com/{acct}/{name}",
        run_id=run_id,
        account_id=acct,
    )

    forbidden = [
        "tessera-v1-alarms",
        "alias/tessera-v1-kms",
        "tessera-dtest-1123abc1-tessera-v1-sneaky",
        "tessera-dtest-other999-kms",  # wrong run_id
        f"arn:aws:sns:us-east-2:999999999999:{name}",  # wrong account
        f"arn:aws:sns:us-east-1:{acct}:{name}",  # wrong region
        f"https://evil.us-east-2.example.com/{acct}/{name}",  # substring-spoofed SQS URL
        f"https://sqs.us-east-2.amazonaws.com/999999999999/{name}",  # wrong SQS account
        f"https://sqs.us-east-1.amazonaws.com/{acct}/{name}",
        "my-random-bucket",
        "",
    ]
    for bad in forbidden:
        with pytest.raises(SafetyViolation):
            assert_throwaway_name(bad, allow_alias_prefix=True, run_id=run_id, account_id=acct)

    assert_ownership_tags({PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id}, run_id, "test")
    with pytest.raises(SafetyViolation):
        assert_ownership_tags({PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: "other999"}, run_id, "test")
    with pytest.raises(SafetyViolation):
        assert_ownership_tags({RUN_ID_TAG_KEY: run_id}, run_id, "test")


def test_d3b_removed_and_http_destination_pinned() -> None:
    # D3b must not exist anywhere in dispatch or api_tests
    assert not hasattr(api_tests, "run_d3b_oversized_post")
    assert "d3b" not in run_tests.ALL_TESTS

    valid_host = "abcdefgh12.execute-api.us-east-2.amazonaws.com"
    valid_base = f"https://{valid_host}/v1"
    norm, host, base_path = validate_tessera_api_url(valid_base + "/")
    assert norm == valid_base
    assert host == valid_host
    assert base_path == "/v1"

    for bad_url in (
        "http://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1",
        "https://attacker.example.com/v1",
        "https://abcdefgh12.execute-api.us-east-1.amazonaws.com/v1",
        "https://abcdefgh12.execute-api.us-east-2.amazonaws.com/prod",
        "https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1?x=1",
        "https://user:pass@abcdefgh12.execute-api.us-east-2.amazonaws.com/v1",
        "https://abcdefgh12.execute-api.us-east-2.amazonaws.com:8443/v1",
    ):
        with pytest.raises(SafetyViolation):
            validate_tessera_api_url(bad_url)

    valid_uuid = str(uuid.uuid4())
    # Allowed read-only GET
    assert_safe_api_request(
        "GET",
        f"/v1/requests/{valid_uuid}",
        headers={},
        body=None,
        using_smoke_key=False,
        target_url=f"{valid_base}/v1/requests/{valid_uuid}",
        pinned_host=valid_host,
        base_path="/v1",
    )
    # Refused host mismatch
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "GET",
            f"/v1/requests/{valid_uuid}",
            headers={},
            body=None,
            using_smoke_key=False,
            target_url=f"https://otherhost1.execute-api.us-east-2.amazonaws.com/v1/v1/requests/{valid_uuid}",
            pinned_host=valid_host,
            base_path="/v1",
        )
    # Allowed malformed_400 POST (non-UUID header)
    assert_safe_api_request(
        "POST",
        "/v1/requests",
        headers={"Tessera-Request-Key": "not-a-uuid"},
        body=b"small",
        using_smoke_key=True,
        post_refusal_mode="malformed_400",
        target_url=f"{valid_base}/v1/requests",
        pinned_host=valid_host,
        base_path="/v1",
    )
    # Refused valid UUID in malformed_400
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "POST",
            "/v1/requests",
            headers={"Tessera-Request-Key": valid_uuid},
            body=b"small",
            using_smoke_key=True,
            post_refusal_mode="malformed_400",
            target_url=f"{valid_base}/v1/requests",
            pinned_host=valid_host,
            base_path="/v1",
        )
    # Refused oversized_413 (removed under r5 Rule 3!)
    with pytest.raises(SafetyViolation):
        assert_safe_api_request(
            "POST",
            "/v1/requests",
            headers={"Tessera-Request-Key": valid_uuid},
            body=b"X" * 1_100_000,
            using_smoke_key=True,
            post_refusal_mode="oversized_413",
            target_url=f"{valid_base}/v1/requests",
            pinned_host=valid_host,
            base_path="/v1",
        )


def test_http_redirect_refused_and_post_2xx_checked_before_body_read() -> None:
    handler = NoRedirectHandler()
    req = urllib.request.Request("https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1/v1/requests")
    with pytest.raises(SafetyViolation):
        handler.redirect_request(req, None, 302, "Found", {}, "https://evil.example.com/steal")

    cfg = ApiConfig(
        base_url="https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1",
        pinned_host="abcdefgh12.execute-api.us-east-2.amazonaws.com",
        base_path="/v1",
        smoke_key="secret-smoke-key",
    )
    limiter = RateLimiter(rps=4.0, _clock=lambda: 100.0, _sleeper=lambda _: None)
    quota = SmokeTestQuotaTracker(max_requests=10)

    class _Fake202Resp:
        status = 202
        headers: dict[str, str] = {}

        def __enter__(self) -> "_Fake202Resp":
            return self

        def __exit__(self, *args: Any) -> None:
            return None

        def read(self, n: int = -1) -> bytes:
            raise OSError("body read exploded")

    class _FakeOpener:
        def open(self, request: Any, timeout: float = 15.0) -> Any:
            return _Fake202Resp()

    # Must raise SafetyViolation (2xx POST) BEFORE read() raises OSError!
    with pytest.raises(SafetyViolation):
        _send_http(
            cfg,
            method="POST",
            path="/v1/requests",
            headers={"x-api-key": "secret-smoke-key", "Tessera-Request-Key": "not-a-uuid"},
            body=b"abc",
            using_smoke_key=True,
            post_refusal_mode="malformed_400",
            limiter=limiter,
            rps=1.0,
            quota=quota,
            opener=_FakeOpener(),  # type: ignore[arg-type]
        )

    assert_post_was_refused(400, "d3a")
    with pytest.raises(SafetyViolation):
        assert_post_was_refused(200, "d3a")


def test_ledger_exclusive_create_and_recovery_refuses_production_targets(tmp_path: Path) -> None:
    ledger_path = tmp_path / "ledger-1123abcd.json"
    ledger = RunLedger(run_id="1123abcd", path=ledger_path, account_id="123456789012")
    # Reusing same run_id/path must be refused!
    with pytest.raises(SafetyViolation):
        RunLedger(run_id="1123abcd", path=ledger_path)

    # Tamper ledger to pair throwaway display names with LIVE PRODUCTION identifiers (Finding 2!)
    data = load_ledger(ledger_path)
    data["resources"] = [
        {
            "resource_type": "kms_key",
            "identifier": "prod-kms-key-id-999",
            "name": "tessera-dtest-1123abcd-kms",
            "status": "active",
        },
        {
            "resource_type": "apigw_rest_api",
            "identifier": "prodapi999",
            "name": "tessera-dtest-1123abcd-api",
            "status": "active",
        },
        {
            "resource_type": "sns_observer_subscription",
            "identifier": "arn:aws:sns:us-east-2:123456789012:tessera-v1-alarms:author-email-sub",
            "name": "tessera-dtest-1123abcd-obs-q->tessera-v1-alarms",
            "status": "active",
        },
    ]
    ledger_path.write_text(json.dumps(data), encoding="utf-8")

    destructive_calls: list[str] = []

    class _MockSts:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://sts.us-east-2.amazonaws.com")

        def get_caller_identity(self) -> dict[str, str]:
            return {"Account": "123456789012", "Arn": "arn:aws:iam::123456789012:root"}

    class _MockKms:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://kms.us-east-2.amazonaws.com")

        def describe_key(self, KeyId: str) -> dict[str, Any]:
            return {
                "KeyMetadata": {
                    "KeyId": KeyId,
                    "AWSAccountId": "123456789012",
                    "Arn": f"arn:aws:kms:us-east-2:123456789012:key/{KeyId}",
                    "Description": "Production Tessera V1 signing key",
                }
            }

        def list_resource_tags(self, KeyId: str) -> dict[str, Any]:
            return {"Tags": []}

        def schedule_key_deletion(self, **kwargs: Any) -> None:
            destructive_calls.append("kms:schedule_key_deletion")

    class _MockApiGw:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://apigateway.us-east-2.amazonaws.com")

        def get_rest_api(self, restApiId: str) -> dict[str, Any]:
            return {"id": restApiId, "name": "tessera-v1-issuer", "tags": {}}

        def delete_rest_api(self, **kwargs: Any) -> None:
            destructive_calls.append("apigw:delete_rest_api")

    class _MockSns:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://sns.us-east-2.amazonaws.com")

        def get_paginator(self, name: str) -> Any:
            class _P:
                def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                    return [{"Topics": [{"TopicArn": "arn:aws:sns:us-east-2:123456789012:tessera-v1-alarms"}]}]
            return _P()

        def get_subscription_attributes(self, SubscriptionArn: str) -> dict[str, Any]:
            return {
                "Attributes": {
                    "TopicArn": "arn:aws:sns:us-east-2:123456789012:tessera-v1-alarms",
                    "Protocol": "email",
                    "Endpoint": "author@example.com",
                }
            }

        def unsubscribe(self, **kwargs: Any) -> None:
            destructive_calls.append("sns:unsubscribe")

    class _MockSqs:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://sqs.us-east-2.amazonaws.com")

    class _MockSession:
        def client(self, service: str, **kwargs: Any) -> Any:
            return {
                "sts": _MockSts(),
                "kms": _MockKms(),
                "apigateway": _MockApiGw(),
                "sns": _MockSns(),
                "sqs": _MockSqs(),
            }[service]

    res = d7_tests.cleanup_from_ledger_file(ledger_path, session=_MockSession(), discover_live=False)
    assert destructive_calls == []
    assert res["ok"] is False
    assert len(res["refused"]) == 3

    persisted = load_ledger(ledger_path)
    assert all(r["status"] == "refused_unverified" for r in persisted["resources"])
    assert len(persisted["recovery_runs"]) == 1
    assert persisted["recovery_runs"][0]["ok"] is False


def test_s3_empty_checks_versions_delete_markers_and_errors() -> None:
    deleted_batches: list[list[dict[str, str]]] = []

    class _MockS3:
        def get_bucket_location(self, Bucket: str, ExpectedBucketOwner: str) -> dict[str, str]:
            return {"LocationConstraint": "us-east-2"}

        def get_bucket_tagging(self, Bucket: str, ExpectedBucketOwner: str) -> dict[str, Any]:
            return {
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": RUN_ID_TAG_KEY, "Value": "1123abcd"},
                ]
            }

        def get_paginator(self, name: str) -> Any:
            assert name == "list_object_versions"

            class _P:
                def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                    return [
                        {
                            "Versions": [{"Key": "a", "VersionId": "v1"}],
                            "DeleteMarkers": [{"Key": "b", "VersionId": "dm1"}],
                        }
                    ]
            return _P()

        def delete_objects(self, Bucket: str, Delete: dict[str, Any], ExpectedBucketOwner: str) -> dict[str, Any]:
            deleted_batches.append(Delete["Objects"])
            return {"Errors": [{"Key": "a", "Code": "AccessDenied"}]}

    with pytest.raises(RuntimeError):
        d7_tests._empty_throwaway_bucket(
            _MockS3(), "tessera-dtest-1123abcd-ct-bkt", "1123abcd", "123456789012"
        )
    assert deleted_batches == [[{"Key": "a", "VersionId": "v1"}, {"Key": "b", "VersionId": "dm1"}]]


def test_cli_flags_opt_in_dedup_d4c_last_and_wait_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("AWS_REGION", "AWS_DEFAULT_REGION", "AWS_ENDPOINT_URL"):
        monkeypatch.delenv(var, raising=False)

    # Incompatible --dry-run + --cleanup-ledger must exit non-zero (Finding 7)
    assert run_tests.main(["--dry-run", "--cleanup-ledger", "foo.json"]) == 2

    # Duplicate opt-ins in --only must ALL be removed without flags (Finding 10)
    args = run_tests.build_parser().parse_args(
        ["--only", "d4c,d4c,d7-cloudtrail,d7-cloudtrail,d7-kms,d7-kms"]
    )
    assert run_tests._select_tests(args) == ["d7-kms"]

    # d4c MUST be enforced strictly LAST even if listed first in --only
    args2 = run_tests.build_parser().parse_args(
        ["--only", "d4c,d3a,d4a", "--include-quota-exhaustion"]
    )
    assert run_tests._select_tests(args2) == ["d3a", "d4a", "d4c"]

    # Auto observer wait reflects contract latencies (up to 3600s for IAM)
    assert run_tests.compute_required_wait_seconds(["d7-kms"], observer_enabled=True) == 600
    assert run_tests.compute_required_wait_seconds(["d3a"], observer_enabled=True) == 900
    assert run_tests.compute_required_wait_seconds(["d7-iam-role"], observer_enabled=True) == 3600


def test_shared_rate_limiter_and_prior_quota() -> None:
    with pytest.raises(SafetyViolation):
        RateLimiter(rps=5.0)
    with pytest.raises(SafetyViolation):
        RateLimiter(rps=0.0)

    now = [100.0]
    slept: list[float] = []

    def fake_clock() -> float:
        return now[0]

    def fake_sleep(dt: float) -> None:
        slept.append(dt)
        now[0] += dt

    # Process-wide limiter spaces consecutive calls across different row rps settings
    rl = RateLimiter(rps=2.0, _clock=fake_clock, _sleeper=fake_sleep)
    rl.wait(rps=2.0)  # immediate first request
    rl.wait(rps=2.0)  # +0.5s
    rl.wait(rps=0.5)  # +2.0s (slower row honoured)
    rl.wait(rps=4.0)  # +0.5s (global 2.0 rps ceiling still enforced)
    assert [round(s, 3) for s in slept] == [0.5, 2.0, 0.5]

    qt = SmokeTestQuotaTracker(max_requests=60, prior_count=58)
    assert qt.consume() == 59
    assert qt.consume() == 60
    with pytest.raises(SafetyViolation):
        qt.consume()
    qt.raise_cap_for_d4c(120)
    assert qt.consume() == 61


def test_redaction_urls_exceptions_and_allowlisted_sns_parser(tmp_path: Path) -> None:
    secrets = ["https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1", "my-super-secret-smoke-key"]
    ledger_file = tmp_path / "ledger-redact.json"
    ledger = RunLedger(run_id="1123abcd", path=ledger_file, secrets=secrets)
    intent_id = ledger.record_intent("kms_key", "tessera-dtest-1123abcd-kms")
    ledger.confirm_created(intent_id, "key-uuid-1")
    ledger.record_kms_scheduled_deletion("key-uuid-1", "2026-11-30", intent_id=intent_id)
    ledger.add_note(
        "sqs=https://sqs.us-east-2.amazonaws.com/123456789012/tessera-dtest-1123abcd-obs-q "
        "other=https://unrelated.example.com/secret/path "
        "api=https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1 "
        "key=my-super-secret-smoke-key aws=AKIAIOSFODNN7EXAMPLE"
    )
    raw = ledger_file.read_text(encoding="utf-8")
    assert "https://" not in raw
    assert "abcdefgh12.execute-api" not in raw
    assert "unrelated.example.com" not in raw
    assert "my-super-secret-smoke-key" not in raw
    assert "AKIAIOSFODNN7EXAMPLE" not in raw
    assert "sqs-queue:tessera-dtest-1123abcd-obs-q" in raw
    assert "scheduled, deletes on 2026-11-30" in raw
    assert not ledger.has_uncleaned_resources()

    # Dict keys AND sensitive keys sanitized
    clean = sanitize_value(
        {"https://leak.example.com": "val", "SecretAccessKey": "s3cr3t", "queue_url": "https://sqs.x"},
        secrets,
    )
    assert "https://leak.example.com" not in clean
    assert clean["SecretAccessKey"] == "[REDACTED]"
    assert clean["queue_url"] == "[REDACTED]"

    # safe_error_label never emits raw exception message
    err = RuntimeError("failed contacting https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1")
    label = safe_error_label(err)
    assert label == "RuntimeError"
    assert "execute-api" not in label

    # EventBridge D7 plain-text sentence parsed cleanly into allowlisted identifiers (no raw excerpt!)
    ev_uuid = "11111111-2222-3333-4444-555555555555"
    eb_text = (
        "Tessera D7 (control-plane change): PutKeyPolicy on kms.amazonaws.com "
        "by arn:aws:iam::123456789012:user/admin at 2026-11-23T14:00:00Z; "
        f"error null; CloudTrail event {ev_uuid}. Expected only during a deployment."
    )
    envelope = json.dumps(
        {
            "MessageId": "sns-msg-eb-1",
            "Timestamp": "2026-11-23T14:00:03.000Z",
            "Message": eb_text,
        }
    )
    parsed = parse_sns_sqs_message(
        body=envelope,
        sent_timestamp_ms="1795442404000",
        received_at_utc="2026-11-23T14:00:05.000000Z",
    )
    assert "raw_message_excerpt" not in parsed
    assert parsed["message_format"] == "eventbridge_d7_text"
    assert parsed["identifiers"]["cloudtrail_event_id"] == ev_uuid
    assert parsed["identifiers"]["event_name"] == "PutKeyPolicy"
    assert parsed["identifiers"]["error_code"] is None


def test_correlate_row_results_joins_by_exact_identifiers() -> None:
    ev_ok = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    ev_denied = "99999999-bbbb-cccc-dddd-eeeeeeeeeeee"
    stimuli = [
        {
            "row_id": "D7-kms-policy",
            "action": "kms:PutKeyPolicy",
            "kind": "d7_eventbridge",
            "resource_name": "tessera-dtest-1123abcd-kms",
            "expected_event_names": ["PutKeyPolicy"],
            "started_at_utc": "2026-11-23T14:00:00.000000Z",
            "ended_at_utc": "2026-11-23T14:00:01.000000Z",
            "api_call_succeeded": True,
            "contract_latency_s": 600,
            "sns_observable": True,
        },
        {
            "row_id": "D7-kms-disable",
            "action": "kms:DisableKey",
            "kind": "d7_eventbridge",
            "resource_name": "tessera-dtest-1123abcd-kms",
            "expected_event_names": ["DisableKey"],
            "started_at_utc": "2026-11-23T14:00:02.000000Z",
            "ended_at_utc": "2026-11-23T14:00:03.000000Z",
            "api_call_succeeded": True,
            "contract_latency_s": 600,
            "sns_observable": True,
        },
        {
            "row_id": "D4c",
            "action": "GET until QUOTA_EXCEEDED",
            "kind": "api_alarm",
            "resource_name": "production-api-gateway",
            "expected_alarm_names": ["tessera-v1-d4-quota"],
            "started_at_utc": "2026-11-23T14:05:00.000000Z",
            "ended_at_utc": "2026-11-23T14:06:00.000000Z",
            "trigger_timestamp_utc": "2026-11-23T14:06:00.000000Z",
            "request_ids": ["req-1"],
            "require_access_log_error": "QUOTA_EXCEEDED",
            "contract_latency_s": 900,
            "sns_observable": True,
        },
    ]
    sns_messages = [
        {
            "sns_message_id": "m1",
            "sns_timestamp_utc": "2026-11-23T14:00:10Z",
            "sqs_sent_at_utc": "2026-11-23T14:00:11Z",
            "received_at_utc": "2026-11-23T14:00:12Z",
            "message_format": "eventbridge_d7_text",
            "identifiers": {"cloudtrail_event_id": ev_ok, "event_name": "PutKeyPolicy"},
        },
        {
            "sns_message_id": "m2",
            "sns_timestamp_utc": "2026-11-23T14:00:15Z",
            "sqs_sent_at_utc": "2026-11-23T14:00:16Z",
            "received_at_utc": "2026-11-23T14:00:17Z",
            "message_format": "eventbridge_d7_text",
            "identifiers": {"cloudtrail_event_id": ev_denied, "event_name": "DisableKey", "error_code": "AccessDenied"},
        },
        {
            "sns_message_id": "m3",
            "sns_timestamp_utc": "2026-11-23T14:08:00Z",
            "sqs_sent_at_utc": "2026-11-23T14:08:01Z",
            "received_at_utc": "2026-11-23T14:08:02Z",
            "message_format": "cloudwatch_alarm",
            "identifiers": {
                "alarm_name": "tessera-v1-d4-quota",
                "new_state": "ALARM",
                "state_change_time": "2026-11-23T14:08:00Z",
            },
        },
    ]
    alarm_transitions = [
        {
            "alarm_name": "tessera-v1-d4-quota",
            "state_updated_timestamp": "2026-11-23T14:08:00.000000Z",
            "old_state": "OK",
            "new_state": "ALARM",
        }
    ]
    ct_events_by_row = {
        "D7-kms-policy": [{"event_id": ev_ok, "succeeded": True, "error_code": None}],
        # AccessDenied event must NOT be credited as a successful tamper pass!
        "D7-kms-disable": [{"event_id": ev_denied, "succeeded": False, "error_code": "AccessDenied"}],
    }
    # Access log shows THROTTLED instead of QUOTA_EXCEEDED -> D4c must stay OPEN!
    access_logs_by_row = {
        "D4c": [{"request_id": "req-1", "status": "429", "error": "THROTTLED"}]
    }

    rows, handoff = run_tests.correlate_row_results(
        stimuli,
        sns_messages,
        alarm_transitions,
        ct_events_by_row=ct_events_by_row,
        access_logs_by_row=access_logs_by_row,
    )
    by_id = {r["row_id"]: r for r in rows}
    assert by_id["D7-kms-policy"]["overall_status"] == "OBSERVED_SNS_PENDING_EMAIL"
    assert by_id["D7-kms-disable"]["overall_status"] == "OPEN_MISSING_CORRELATED_EVIDENCE"
    assert by_id["D4c"]["overall_status"] == "OPEN_MISSING_CORRELATED_EVIDENCE"
    assert by_id["D4c"]["access_log_error_verified"] is False
    assert len(handoff) == 3

    # Once access log confirms QUOTA_EXCEEDED, D4c transitions to observed pending email
    rows2, _ = run_tests.correlate_row_results(
        stimuli,
        sns_messages,
        alarm_transitions,
        ct_events_by_row=ct_events_by_row,
        access_logs_by_row={"D4c": [{"request_id": "req-1", "status": "429", "error": "QUOTA_EXCEEDED"}]},
    )
    assert {r["row_id"]: r for r in rows2}["D4c"]["overall_status"] == "OBSERVED_ALARM_AND_SNS_PENDING_EMAIL"


def test_preflight_refuses_existing_run_resources_and_reconciles_intents(tmp_path: Path) -> None:
    run_id = "1123beef"
    acct = "123456789012"
    q_name = f"tessera-dtest-{run_id}-q"
    q_url = f"https://sqs.us-east-2.amazonaws.com/{acct}/{q_name}"
    user_name = f"tessera-dtest-{run_id}-user"

    deleted_ops: list[str] = []
    live_state = {"queue_exists": True, "user_exists": True, "user_keys": ["AKIAFAKEKEY000000001"]}

    def _empty_pag(key: str) -> Any:
        class _P:
            def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                return [{key: []}]
        return _P()

    class _MockSts:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://sts.us-east-2.amazonaws.com")
        def get_caller_identity(self) -> dict[str, str]:
            return {"Account": acct, "Arn": f"arn:aws:iam::{acct}:root"}

    class _MockTagApi:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://tagging.us-east-2.amazonaws.com")
        def get_paginator(self, name: str) -> Any:
            class _P:
                def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                    items = []
                    if live_state["queue_exists"]:
                        items.append({"ResourceARN": f"arn:aws:sqs:us-east-2:{acct}:{q_name}"})
                    return [{"ResourceTagMappingList": items}]
            return _P()

    class _MockSqs:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://sqs.us-east-2.amazonaws.com")
        def list_queues(self, QueueNamePrefix: str) -> dict[str, Any]:
            return {"QueueUrls": [q_url] if live_state["queue_exists"] else []}
        def get_queue_url(self, QueueName: str, QueueOwnerAWSAccountId: str) -> dict[str, str]:
            return {"QueueUrl": q_url}
        def list_queue_tags(self, QueueUrl: str) -> dict[str, Any]:
            return {"Tags": {PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id}}
        def delete_queue(self, QueueUrl: str) -> None:
            deleted_ops.append("sqs:delete_queue")
            live_state["queue_exists"] = False

    class _MockIam:
        meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url="https://iam.amazonaws.com")
        def get_paginator(self, name: str) -> Any:
            if name == "list_users":
                class _P:
                    def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                        return [{"Users": [{"UserName": user_name}] if live_state["user_exists"] else []}]
                return _P()
            return _empty_pag("Roles")
        def get_user(self, UserName: str) -> dict[str, Any]:
            return {
                "User": {
                    "Arn": f"arn:aws:iam::{acct}:user/{UserName}",
                    "Tags": [
                        {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                        {"Key": RUN_ID_TAG_KEY, "Value": run_id},
                    ],
                }
            }
        def list_access_keys(self, UserName: str) -> dict[str, Any]:
            return {"AccessKeyMetadata": [{"AccessKeyId": k} for k in live_state["user_keys"]]}
        def delete_access_key(self, UserName: str, AccessKeyId: str) -> None:
            deleted_ops.append("iam:delete_access_key")
            live_state["user_keys"] = [k for k in live_state["user_keys"] if k != AccessKeyId]
        def delete_user(self, UserName: str) -> None:
            assert not live_state["user_keys"], "keys must be deleted before user"
            deleted_ops.append("iam:delete_user")
            live_state["user_exists"] = False

    class _EmptyService:
        def __init__(self, ep: str, key: str = "items") -> None:
            self.meta = types.SimpleNamespace(region_name="us-east-2", endpoint_url=ep)
            self._key = key
        def get_paginator(self, name: str) -> Any:
            return _empty_pag(self._key)
        def list_buckets(self) -> dict[str, Any]:
            return {"Buckets": []}
        def list_trails(self) -> dict[str, Any]:
            return {"Trails": []}

    class _Session:
        def client(self, service: str, **kwargs: Any) -> Any:
            table: dict[str, Any] = {
                "sts": _MockSts(),
                "resourcegroupstaggingapi": _MockTagApi(),
                "sqs": _MockSqs(),
                "iam": _MockIam(),
                "sns": _EmptyService("https://sns.us-east-2.amazonaws.com", "Topics"),
                "s3": _EmptyService("https://s3.us-east-2.amazonaws.com"),
                "kms": _EmptyService("https://kms.us-east-2.amazonaws.com", "Aliases"),
                "apigateway": _EmptyService("https://apigateway.us-east-2.amazonaws.com", "items"),
                "lambda": _EmptyService("https://lambda.us-east-2.amazonaws.com", "Functions"),
                "cloudtrail": _EmptyService("https://cloudtrail.us-east-2.amazonaws.com"),
                "dynamodb": _EmptyService("https://dynamodb.us-east-2.amazonaws.com", "TableNames"),
                "cloudwatch": _EmptyService("https://monitoring.us-east-2.amazonaws.com", "MetricAlarms"),
                "logs": _EmptyService("https://logs.us-east-2.amazonaws.com", "logGroups"),
                "events": _EmptyService("https://events.us-east-2.amazonaws.com", "Rules"),
            }
            return table[service]

    sess = _Session()
    # 1. Pre-flight MUST refuse to start because resources for run_id already exist!
    with pytest.raises(SafetyViolation):
        d7_tests.assert_no_existing_run_resources(run_id, acct, session=sess)

    # 2. Recovery reconciles 'creating' intents via live discovery and deletes verified resources cleanly
    ledger_path = tmp_path / f"ledger-{run_id}.json"
    ledger = RunLedger(run_id=run_id, path=ledger_path, account_id=acct)
    ledger.record_intent("sqs_queue", q_name)
    ledger.record_intent("iam_user", user_name)
    ledger.record_intent("iam_access_key", user_name)

    res = d7_tests.cleanup_from_ledger_file(ledger_path, session=sess, discover_live=True)
    assert res["ok"] is True
    assert res["residuals"] == []
    assert res["refused"] == []
    assert "sqs:delete_queue" in deleted_ops
    assert "iam:delete_access_key" in deleted_ops
    assert "iam:delete_user" in deleted_ops

    # Check registered ID helper still enforces membership
    assert assert_throwaway_id_registered("id-1", {"id-1"}, "test") == "id-1"
    with pytest.raises(SafetyViolation):
        assert_throwaway_id_registered("prod-id", {"id-1"}, "test")
