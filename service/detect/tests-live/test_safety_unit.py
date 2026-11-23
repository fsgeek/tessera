"""Offline unit tests for the detection-test safety guards (steward removal pass).

Runs without AWS credentials, without network access, and without boto3 installed.
"""

from __future__ import annotations

import json
import re
import sys
import types
import urllib.request
import uuid
from pathlib import Path
from typing import Any

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import api_tests  # noqa: E402
import d7_tests  # noqa: E402
import run_tests  # noqa: E402
from api_tests import ApiConfig, NoRedirectHandler, _send_http  # noqa: E402
from ledger import RunLedger, load_ledger  # noqa: E402
from safety import (  # noqa: E402
    ALLOWED_AWS_ENDPOINTS,
    ALLOWED_REGION,
    PINNED_API_HOST,
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
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
    safe_error_label,
    sanitize_value,
    validate_tessera_api_url,
)

ACCT = "123456789012"
PINNED_BASE = f"https://{PINNED_API_HOST}/v1"
ENV_VARS = (
    "AWS_REGION",
    "AWS_DEFAULT_REGION",
    "AWS_ENDPOINT_URL",
    "AWS_ENDPOINT_URL_KMS",
    "AWS_USE_FIPS_ENDPOINT",
    "AWS_USE_DUALSTACK_ENDPOINT",
    "AWS_STS_REGIONAL_ENDPOINTS",
    "TESSERA_API",
    "TESSERA_SMOKE_KEY",
)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ENV_VARS:
        monkeypatch.delenv(var, raising=False)


def _meta(service: str) -> Any:
    return types.SimpleNamespace(region_name="us-east-2", endpoint_url=f"https://{ALLOWED_AWS_ENDPOINTS[service]}")


class _Pag:
    def __init__(self, pages: list[dict[str, Any]]) -> None:
        self._pages = pages

    def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self._pages


class _Sts:
    meta = _meta("sts")

    def get_caller_identity(self) -> dict[str, str]:
        return {"Account": ACCT, "Arn": f"arn:aws:iam::{ACCT}:root"}


class _TagApi:
    meta = _meta("resourcegroupstaggingapi")

    def __init__(self, arns: list[str]) -> None:
        self.arns = arns
        self.calls: list[Any] = []

    def get_paginator(self, name: str) -> Any:
        api = self

        class _P:
            def paginate(self, **kwargs: Any) -> list[dict[str, Any]]:
                api.calls.append(kwargs)
                return [{"ResourceTagMappingList": [{"ResourceARN": a} for a in api.arns]}]

        return _P()


class _Session:
    def __init__(self, clients: dict[str, Any]) -> None:
        self.clients = clients
        self.requested: list[str] = []

    def client(self, service: str, **kwargs: Any) -> Any:
        self.requested.append(service)
        if service not in self.clients:
            raise AssertionError(f"unexpected client {service}")
        return self.clients[service]


# ---------------------------------------------------------------------------
# Region / endpoint / removed services
# ---------------------------------------------------------------------------

def test_region_lock_and_env_endpoint_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    assert assert_region(ALLOWED_REGION) == "us-east-2"
    for bad in ("us-east-1", "eu-west-1", "", None):
        with pytest.raises(SafetyViolation):
            assert_region(bad)
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


def test_locked_client_refuses_overrides_and_removed_services() -> None:
    class _Fake:
        def __init__(self, region: str, ep: str) -> None:
            self.meta = types.SimpleNamespace(region_name=region, endpoint_url=ep)

    class _Hijacked:
        def client(self, service: str, **kwargs: Any) -> Any:
            return _Fake("us-east-2", "https://attacker.example.com")

    with pytest.raises(SafetyViolation):
        locked_boto3_client("kms", session=_Hijacked())

    class _Good:
        def client(self, service: str, region_name: str, endpoint_url: str) -> Any:
            return _Fake(region_name, endpoint_url)

    assert locked_boto3_client("kms", session=_Good()).meta.endpoint_url == "https://kms.us-east-2.amazonaws.com"
    # IAM, S3 and Lambda clients no longer exist in this suite.
    for svc in ("iam", "s3", "lambda"):
        with pytest.raises(SafetyViolation):
            locked_boto3_client(svc, session=_Good())


def test_source_never_touches_alarm_topic_subscriptions_or_iam() -> None:
    """Item 1 & 2: no subscribe/unsubscribe, no IAM/S3/Lambda calls anywhere in the code."""
    forbidden = [
        r"\.subscribe\(",
        r"\.unsubscribe\(",
        r"list_subscriptions",
        r"get_subscription_attributes",
        r"PRODUCTION_ALARM_TOPIC_NAME",
        r"allow_global_iam",
        r"locked_boto3_client\(\s*\"(iam|s3|lambda)\"",
        r"create_role|put_role_policy|create_user|create_access_key|assume_role",
        r"create_bucket|create_trail|stop_logging|create_function",
        r"create_grant|create_alias|create_usage_plan_key|create_rest_api",
    ]
    for src in ("run_tests.py", "d7_tests.py", "observer.py", "api_tests.py", "ledger.py"):
        text = (HERE / src).read_text(encoding="utf-8")
        for pat in forbidden:
            assert not re.search(pat, text), f"{src} matches forbidden pattern {pat}"


def test_throwaway_name_binding_and_tags() -> None:
    run_id = "a1b2c3d4e5f6"
    name = make_throwaway_name(run_id, "kms")
    assert name == "tessera-dtest-a1b2c3d4e5f6-kms"
    assert_throwaway_name(f"arn:aws:sns:us-east-2:{ACCT}:{name}", run_id=run_id, account_id=ACCT)
    for bad in (
        "tessera-v1-alarms",
        "tessera-dtest-a1b2c3d4e5f6-tessera-v1-sneaky",
        "tessera-dtest-000000000000-kms",
        f"arn:aws:sns:us-east-2:999999999999:{name}",
        f"arn:aws:sns:us-east-1:{ACCT}:{name}",
        f"https://sqs.us-east-2.amazonaws.com/999999999999/{name}",
    ):
        with pytest.raises(SafetyViolation):
            assert_throwaway_name(bad, run_id=run_id, account_id=ACCT)
    assert_ownership_tags({PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id}, run_id, "t")
    with pytest.raises(SafetyViolation):
        assert_ownership_tags({RUN_ID_TAG_KEY: run_id}, run_id, "t")


# ---------------------------------------------------------------------------
# Item 3: API host binding
# ---------------------------------------------------------------------------

def test_api_bound_to_deployed_host_only() -> None:
    norm, host, base = validate_tessera_api_url(PINNED_BASE + "/")
    assert (norm, host, base) == (PINNED_BASE, PINNED_API_HOST, "/v1")
    for bad in (
        "https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1",  # another valid-looking API ID
        "http://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1",
        "https://p4e0222jof.execute-api.us-east-1.amazonaws.com/v1",
        "https://p4e0222jof.execute-api.us-east-2.amazonaws.com/prod",
        "https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1/extra",
        "https://p4e0222jof.execute-api.us-east-2.amazonaws.com.evil.com/v1",
        "https://user:pw@p4e0222jof.execute-api.us-east-2.amazonaws.com/v1",
        "https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1?x=1",
    ):
        with pytest.raises(SafetyViolation):
            validate_tessera_api_url(bad)


def test_api_config_from_env_refuses_other_host(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TESSERA_API", "https://abcdefgh12.execute-api.us-east-2.amazonaws.com/v1")
    monkeypatch.setenv("TESSERA_SMOKE_KEY", "smk")
    with pytest.raises(SafetyViolation):
        ApiConfig.from_env()
    monkeypatch.setenv("TESSERA_API", PINNED_BASE)
    assert ApiConfig.from_env().pinned_host == PINNED_API_HOST


def test_smoke_key_never_sent_to_a_hand_built_other_host() -> None:
    other = "abcdefgh12.execute-api.us-east-2.amazonaws.com"
    cfg = ApiConfig(base_url=f"https://{other}/v1", pinned_host=other, base_path="/v1", smoke_key="smk")
    opened: list[Any] = []

    class _Opener:
        def open(self, req: Any, timeout: float = 15.0) -> Any:
            opened.append(req)
            raise AssertionError("must not open")

    limiter = RateLimiter(rps=4.0, _clock=lambda: 1.0, _sleeper=lambda _: None)
    with pytest.raises(SafetyViolation):
        _send_http(cfg, method="GET", path=f"/v1/requests/{uuid.uuid4()}", headers={"x-api-key": "smk"},
                   body=None, using_smoke_key=True, post_refusal_mode=None, limiter=limiter, rps=1.0,
                   quota=SmokeTestQuotaTracker(max_requests=10), opener=_Opener())  # type: ignore[arg-type]
    assert opened == []


def test_redirect_refused_post_2xx_checked_and_headers_allowlisted() -> None:
    handler = NoRedirectHandler()
    with pytest.raises(SafetyViolation):
        handler.redirect_request(urllib.request.Request(PINNED_BASE), None, 302, "Found", {}, "https://evil.example.com")

    cfg = ApiConfig(base_url=PINNED_BASE, pinned_host=PINNED_API_HOST, base_path="/v1", smoke_key="smk")
    limiter = RateLimiter(rps=4.0, _clock=lambda: 100.0, _sleeper=lambda _: None)

    class _Resp:
        def __init__(self, status: int, headers: dict[str, str]) -> None:
            self.status = status
            self.headers = headers

        def __enter__(self) -> "_Resp":
            return self

        def __exit__(self, *a: Any) -> None:
            return None

        def read(self, n: int = -1) -> bytes:
            raise OSError("body read must not happen first")

    class _Opener:
        def __init__(self, resp: _Resp) -> None:
            self.resp = resp

        def open(self, req: Any, timeout: float = 15.0) -> Any:
            return self.resp

    with pytest.raises(SafetyViolation):
        _send_http(cfg, method="POST", path="/v1/requests", headers={"x-api-key": "smk", "Tessera-Request-Key": "nope"},
                   body=b"x", using_smoke_key=True, post_refusal_mode="malformed_400", limiter=limiter, rps=1.0,
                   quota=SmokeTestQuotaTracker(max_requests=10), opener=_Opener(_Resp(202, {})))  # type: ignore[arg-type]

    class _OkResp(_Resp):
        def read(self, n: int = -1) -> bytes:
            return b""

    rid = str(uuid.uuid4())
    res = _send_http(cfg, method="GET", path=f"/v1/requests/{uuid.uuid4()}", headers={}, body=None,
                     using_smoke_key=False, post_refusal_mode=None, limiter=limiter, rps=1.0, quota=None,
                     opener=_Opener(_OkResp(404, {"x-amzn-RequestId": rid, "x-amzn-ErrorType": "NotFoundException:http://x"})))  # type: ignore[arg-type]
    assert res["request_id"] == rid and res["error_type"] == "NotFoundException"
    res2 = _send_http(cfg, method="GET", path=f"/v1/requests/{uuid.uuid4()}", headers={}, body=None,
                      using_smoke_key=False, post_refusal_mode=None, limiter=limiter, rps=1.0, quota=None,
                      opener=_Opener(_OkResp(404, {"x-amzn-RequestId": "smk-reflected", "x-amzn-ErrorType": "a b"})))  # type: ignore[arg-type]
    assert res2["request_id"] is None and res2["error_type"] is None

    assert_post_was_refused(400, "d3a")
    with pytest.raises(SafetyViolation):
        assert_post_was_refused(200, "d3a")
    with pytest.raises(SafetyViolation):
        assert_safe_api_request("POST", "/v1/requests", headers={"Tessera-Request-Key": str(uuid.uuid4())},
                                body=b"x", using_smoke_key=True, post_refusal_mode="malformed_400")


# ---------------------------------------------------------------------------
# Item 4: run identity and preflight-before-ledger
# ---------------------------------------------------------------------------

def test_run_id_is_generated_and_cannot_be_supplied() -> None:
    ids = {run_tests.generate_run_id() for _ in range(50)}
    assert len(ids) == 50
    assert all(re.fullmatch(r"[0-9a-f]{12}", i) for i in ids)
    with pytest.raises(SystemExit):
        run_tests.build_parser().parse_args(["--run-id", "abcd1234"])
    with pytest.raises(SystemExit):
        run_tests.build_parser().parse_args(["--output-dir", "/tmp/elsewhere"])


def test_preflight_refusal_writes_no_ledger_and_releases_lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = "abcdef123456"
    monkeypatch.setattr(run_tests, "generate_run_id", lambda: fixed)
    tag = _TagApi([f"arn:aws:sqs:us-east-2:{ACCT}:tessera-dtest-{fixed}-q"])
    sess = _Session({"sts": _Sts(), "resourcegroupstaggingapi": tag})
    rc = run_tests.main(["--only", "d7-sup-sqs"], output_dir=tmp_path, session=sess)
    assert rc == 1
    assert list(tmp_path.glob("ledger-*")) == []
    assert not (tmp_path / ".lock").exists()
    # Tag search used BOTH tags.
    keys = {f["Key"] for f in tag.calls[0]["TagFilters"]}
    assert keys == {PURPOSE_TAG_KEY, RUN_ID_TAG_KEY}


def test_access_log_failure_fails_closed_before_smoke_key_traffic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TESSERA_API", PINNED_BASE)
    monkeypatch.setenv("TESSERA_SMOKE_KEY", "smk")

    def _boom(*a: Any, **k: Any) -> Any:
        raise AssertionError("smoke-key traffic must not start")

    monkeypatch.setattr(run_tests, "run_d3a_malformed_post", _boom)

    class _Logs:
        meta = _meta("logs")

        def get_paginator(self, name: str) -> Any:
            raise RuntimeError("logs unavailable")

    sess = _Session({"sts": _Sts(), "resourcegroupstaggingapi": _TagApi([]), "logs": _Logs()})
    rc = run_tests.main(["--only", "d3a", "--wait-seconds", "0"], output_dir=tmp_path, session=sess)
    assert rc == 1
    ledgers = list(tmp_path.glob("ledger-*.json"))
    assert len(ledgers) == 1
    raw = ledgers[0].read_text(encoding="utf-8")
    assert "smk" not in raw and "logs unavailable" not in raw


# ---------------------------------------------------------------------------
# Item 5: one process at a time
# ---------------------------------------------------------------------------

def test_lock_refuses_second_run_and_is_left_alone(tmp_path: Path) -> None:
    lock = run_tests.RunLock(tmp_path)
    lock.acquire()
    with pytest.raises(SafetyViolation):
        run_tests.RunLock(tmp_path).acquire()

    sess = _Session({})  # any AWS client request would fail the test
    assert run_tests.main(["--only", "d7-kms"], output_dir=tmp_path, session=sess) == 1
    assert run_tests.main(["--cleanup-ledger", "ledger-abcdef123456.json"], output_dir=tmp_path, session=sess) == 1
    assert sess.requested == []
    assert (tmp_path / ".lock").exists()  # refusing process did not delete another's lock
    lock.release()
    assert not (tmp_path / ".lock").exists()
    lock.release()  # idempotent


def test_dry_run_makes_no_files_no_calls(tmp_path: Path) -> None:
    sess = _Session({})
    assert run_tests.main(["--dry-run", "--suite", "all"], output_dir=tmp_path, session=sess) == 0
    assert list(tmp_path.iterdir()) == []
    assert sess.requested == []
    assert run_tests.main(["--dry-run", "--cleanup-ledger", "x.json"], output_dir=tmp_path) == 2


# ---------------------------------------------------------------------------
# Items 6 & 7: tag-only recovery, never closing on a miss, redaction
# ---------------------------------------------------------------------------

def _ledger_with(tmp_path: Path, run_id: str, entries: list[dict[str, Any]]) -> Path:
    path = tmp_path / f"ledger-{run_id}.json"
    led = RunLedger(run_id=run_id, path=path, account_id=ACCT)
    led.data["resources"] = entries
    led._flush()
    return path


def test_recovery_refuses_ledger_identifiers_and_untargeted_types(tmp_path: Path) -> None:
    run_id = "abcdef123456"
    destructive: list[str] = []
    path = _ledger_with(tmp_path, run_id, [
        {"resource_type": "kms_key", "identifier": "prod-key", "name": f"tessera-dtest-{run_id}-kms", "status": "active"},
    ])

    class _Sqs:
        meta = _meta("sqs")

        def delete_queue(self, **k: Any) -> None:
            destructive.append("sqs")

    # Tag search returns nothing for the ledger's kms entry, but finds a queue with no intent.
    tag = _TagApi([f"arn:aws:sqs:us-east-2:{ACCT}:tessera-dtest-{run_id}-q"])
    sess = _Session({"sts": _Sts(), "resourcegroupstaggingapi": tag, "sqs": _Sqs(), "kms": object()})
    res = d7_tests.cleanup_from_ledger_file(path, session=sess)
    assert destructive == []
    assert res["ok"] is False
    assert any("refused_no_matching_intent" in r for r in res["refused"])
    # The ledger-only production identifier was never acted on and remains a residual.
    assert any(r.startswith("ledger:kms_key") for r in res["residuals"])
    assert load_ledger(path)["recovery_runs"][-1]["ok"] is False


def test_recovery_unresolved_intent_stays_open_on_tag_miss(tmp_path: Path) -> None:
    run_id = "abcdef123456"
    path = _ledger_with(tmp_path, run_id, [
        {"resource_type": "kms_key", "identifier": None, "name": f"tessera-dtest-{run_id}-kms", "status": "unresolved"},
    ])
    sess = _Session({"sts": _Sts(), "resourcegroupstaggingapi": _TagApi([])})
    res = d7_tests.cleanup_from_ledger_file(path, session=sess)
    assert res["ok"] is False
    assert load_ledger(path)["resources"][0]["status"] == "unresolved"


def test_recovery_deletes_tag_found_resource_after_service_verification(tmp_path: Path) -> None:
    run_id = "abcdef123456"
    q = f"tessera-dtest-{run_id}-q"
    state = {"exists": True}
    path = _ledger_with(tmp_path, run_id, [
        {"resource_type": "sqs_queue", "identifier": None, "name": q, "status": "creating"},
    ])

    class _Sqs:
        meta = _meta("sqs")

        def get_queue_url(self, QueueName: str, QueueOwnerAWSAccountId: str) -> dict[str, str]:
            return {"QueueUrl": f"https://sqs.us-east-2.amazonaws.com/{ACCT}/{QueueName}"}

        def list_queue_tags(self, QueueUrl: str) -> dict[str, Any]:
            return {"Tags": {PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id}}

        def delete_queue(self, QueueUrl: str) -> None:
            state["exists"] = False

    class _DynTag(_TagApi):
        def get_paginator(self, name: str) -> Any:
            self.arns = [f"arn:aws:sqs:us-east-2:{ACCT}:{q}"] if state["exists"] else []
            return super().get_paginator(name)

    sess = _Session({"sts": _Sts(), "resourcegroupstaggingapi": _DynTag([]), "sqs": _Sqs()})
    res = d7_tests.cleanup_from_ledger_file(path, session=sess)
    assert res["ok"] is True, res
    assert state["exists"] is False
    assert load_ledger(path)["resources"][0]["status"] == "deleted"
    out = json.dumps(res)
    assert ACCT not in out and "https://" not in out


def test_tag_arn_classification_is_region_and_account_bound() -> None:
    run_id = "abcdef123456"
    c = d7_tests._classify_tagged_arn
    assert c(f"arn:aws:sqs:us-east-2:{ACCT}:tessera-dtest-{run_id}-q", run_id, ACCT)["resource_type"] == "sqs_queue"
    assert c("arn:aws:apigateway:us-east-2::/apikeys/abc123", run_id, ACCT)["resource_type"] == "apigw_api_key"
    assert c(f"arn:aws:logs:us-east-2:{ACCT}:log-group:tessera-dtest-{run_id}-logs:*", run_id, ACCT)["identifier"] == f"tessera-dtest-{run_id}-logs"
    for bad in (
        f"arn:aws:sqs:us-east-1:{ACCT}:tessera-dtest-{run_id}-q",
        f"arn:aws:sqs:us-east-2:999999999999:tessera-dtest-{run_id}-q",
        f"arn:aws:sqs:us-east-2:{ACCT}:tessera-v1-queue",
        f"arn:aws:s3:::tessera-dtest-{run_id}-bkt",
        "arn:aws:apigateway:us-east-2::/restapis/abc",
    ):
        assert c(bad, run_id, ACCT)["resource_type"] == "unknown"


def test_create_failure_classification() -> None:
    class _E(Exception):
        def __init__(self, status: int | None) -> None:
            self.response = {"Error": {"Code": "X"}, "ResponseMetadata": {"HTTPStatusCode": status}} if status else None

    assert d7_tests._definitely_not_created(_E(400)) is True
    assert d7_tests._definitely_not_created(_E(500)) is False
    assert d7_tests._definitely_not_created(_E(None)) is False
    assert d7_tests._definitely_not_created(TimeoutError()) is False


def test_redaction_and_summary_lines(tmp_path: Path) -> None:
    secrets = [PINNED_BASE, "my-super-secret-smoke-key"]
    path = tmp_path / "ledger-abcdef123456.json"
    led = RunLedger(run_id="abcdef123456", path=path, secrets=secrets, account_id=ACCT)
    iid = led.record_intent("kms_key", "tessera-dtest-abcdef123456-kms")
    led.confirm_created(iid, "1234abcd-12ab-34cd-56ef-1234567890ab")
    led.add_note(
        f"arn=arn:aws:sns:us-east-2:{ACCT}:tessera-dtest-abcdef123456-topic "
        "other=https://unrelated.example.com/p key=my-super-secret-smoke-key aws=AKIAIOSFODNN7EXAMPLE"
    )
    raw = path.read_text(encoding="utf-8")
    assert "https://" not in raw and "my-super-secret-smoke-key" not in raw and "AKIAIOSFODNN7EXAMPLE" not in raw
    assert f":{ACCT}:" not in raw
    lines = led.cleanup_summary_lines()
    assert lines and "1234abcd-12ab" not in lines[0] and "name=tessera-dtest-abcdef123456-kms" in lines[0]
    assert led.has_uncleaned_resources()
    with pytest.raises(SafetyViolation):
        RunLedger(run_id="abcdef123456", path=path)
    assert safe_error_label(RuntimeError(f"contacting {PINNED_BASE}")) == "RuntimeError"
    clean = sanitize_value({"SecretAccessKey": "s", "queue_url": "q"}, [])
    assert clean == {"SecretAccessKey": "[REDACTED]", "queue_url": "[REDACTED]"}


# ---------------------------------------------------------------------------
# Selection, pacing, correlation
# ---------------------------------------------------------------------------

def test_cli_selection_opt_in_and_removed_tests() -> None:
    for removed in ("d3b", "d7-s3", "d7-lambda", "d7-cloudtrail", "d7-iam-role", "d7-iam-access-key"):
        assert removed not in run_tests.ALL_TESTS
    p = run_tests.build_parser()
    assert run_tests._select_tests(p.parse_args(["--only", "d4c,d4c,d7-kms,d7-kms"])) == ["d7-kms"]
    assert run_tests._select_tests(p.parse_args(["--only", "d4c,d3a,d4a", "--include-quota-exhaustion"])) == ["d3a", "d4a", "d4c"]
    with pytest.raises(SystemExit):
        run_tests._select_tests(p.parse_args(["--only", "d7-iam-role"]))
    assert run_tests.compute_required_wait_seconds(["d7-kms"]) == 600
    assert run_tests.compute_required_wait_seconds(["d7-kms", "d3a"]) == 900


def test_shared_rate_limiter_and_prior_quota() -> None:
    with pytest.raises(SafetyViolation):
        RateLimiter(rps=5.0)
    now = [100.0]
    slept: list[float] = []

    def sleep(dt: float) -> None:
        slept.append(dt)
        now[0] += dt

    rl = RateLimiter(rps=2.0, _clock=lambda: now[0], _sleeper=sleep)
    for r in (2.0, 2.0, 0.5, 4.0):
        rl.wait(rps=r)
    assert [round(s, 3) for s in slept] == [0.5, 2.0, 0.5]
    qt = SmokeTestQuotaTracker(max_requests=60, prior_count=59)
    assert qt.consume() == 60
    with pytest.raises(SafetyViolation):
        qt.consume()


def test_correlate_row_results_uses_cloudtrail_and_alarm_history_only() -> None:
    ev_ok = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    stimuli = [
        {"row_id": "D7-kms-policy", "action": "kms:PutKeyPolicy", "kind": "d7_eventbridge",
         "started_at_utc": "2026-11-23T14:00:00.000000Z", "ended_at_utc": "2026-11-23T14:00:01.000000Z",
         "api_call_succeeded": True, "contract_latency_s": 600},
        {"row_id": "D7-kms-disable", "action": "kms:DisableKey", "kind": "d7_eventbridge",
         "started_at_utc": "2026-11-23T14:00:02.000000Z", "ended_at_utc": "2026-11-23T14:00:03.000000Z",
         "api_call_succeeded": True, "contract_latency_s": 600},
        {"row_id": "D4c", "action": "GET", "kind": "api_alarm", "expected_alarm_names": ["tessera-v1-d4-quota"],
         "started_at_utc": "2026-11-23T14:05:00.000000Z", "ended_at_utc": "2026-11-23T14:06:00.000000Z",
         "request_ids": ["r"], "require_access_log_error": "QUOTA_EXCEEDED", "contract_latency_s": 900},
    ]
    transitions = [{"alarm_name": "tessera-v1-d4-quota", "state_updated_timestamp": "2026-11-23T14:08:00.000000Z",
                    "old_state": "OK", "new_state": "ALARM"}]
    ct = {"D7-kms-policy": [{"event_id": ev_ok, "succeeded": True}],
          "D7-kms-disable": [{"event_id": "x", "succeeded": False, "error_code": "AccessDenied"}]}
    rows, handoff = run_tests.correlate_row_results(stimuli, transitions, ct_events_by_row=ct,
                                                    access_logs_by_row={"D4c": [{"error": "THROTTLED"}]})
    by = {r["row_id"]: r for r in rows}
    assert by["D7-kms-policy"]["overall_status"] == "STIMULUS_CONFIRMED_PENDING_EMAIL"
    assert by["D7-kms-disable"]["overall_status"] == "OPEN_MISSING_STIMULUS_EVIDENCE"
    assert by["D4c"]["overall_status"] == "OPEN_MISSING_ALARM_EVIDENCE"
    assert len(handoff) == 3 and all("sns" not in json.dumps(r).lower() for r in rows)
    rows2, _ = run_tests.correlate_row_results(stimuli, transitions, ct_events_by_row=ct,
                                               access_logs_by_row={"D4c": [{"error": "QUOTA_EXCEEDED"}]})
    assert {r["row_id"]: r for r in rows2}["D4c"]["overall_status"] == "ALARM_FIRED_PENDING_EMAIL"
