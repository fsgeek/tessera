"""The AWS implementations (DynamoDB request store, S3 result store, SQS queues, SNS wake, the Lambda entry points)
against in-memory fakes of the boto3 clients: the same contract the in-memory stores meet, then a whole issuance
through API Gateway proxy events and the poller handler, ending in a VALID_STRICT bundle. No AWS call is made."""
import base64
import json
import uuid

import pytest

from tessera_issue import api, lambda_app, local, pipeline
from tessera_issue.aws import DynamoRequestStore, S3ResultStore, SnsWake
from tessera_issue.queues import InMemoryQueue, SqsQueue
from tessera_issue.signers import SlotSigner, StandInSigner
from tessera_issue.stores import InMemoryRequestStore, InMemoryResultStore

from conftest import FROZEN
from fakes import FakeDynamo, FakeS3, FakeSession, FakeSns, FakeSqs
from helpers import verify_with_cli


def rec(rid, state="ACCEPTED"):
    return {"rid": rid, "state": state, "stage": "frames", "expires_at": None, "x": 1}


@pytest.fixture(params=["memory", "dynamo"])
def store(request):
    return InMemoryRequestStore() if request.param == "memory" else DynamoRequestStore(FakeDynamo(), "t")


@pytest.fixture(params=["memory", "s3"])
def results(request):
    return InMemoryResultStore() if request.param == "memory" else S3ResultStore(FakeS3(), "b")


def test_request_store_contract(store):
    a = rec("a")
    assert store.create(a) and a["version"] == 1
    assert not store.create(rec("a"))
    stale = store.get("a")
    a["x"] = 2
    assert store.save(a) and a["version"] == 2
    assert not store.save(stale) and stale["version"] == 1        # compare-and-set
    assert store.get("a")["x"] == 2
    for i in range(5):
        store.create(rec(f"p{i}"))
    done = store.get("p0")
    done["state"] = "COMPLETE"
    store.save(done)
    assert sorted(r["rid"] for r in store.active()) == ["a", "p1", "p2", "p3", "p4"]
    assert store.get("missing") is None and store.tombstone_get("a") is None
    store.tombstone_put("a", 100)
    store.tombstone_put("a", 999)                                  # first write wins
    assert store.tombstone_get("a")["keep_until"] == 100
    store.sigreq_put("req-1", {"rid": "a", "job": "s_kms", "slot": "kms", "frame_sha256": "f"}, 50)
    assert store.sigreq_get("req-1")["job"] == "s_kms" and store.sigreq_get("req-2") is None
    store.siglog_add({"request_id": "req-1", "disposition": "used"})
    store.siglog_add({"request_id": "req-9", "disposition": "unrequested"})
    assert sorted(e["request_id"] for e in store.siglog()) == ["req-1", "req-9"]


def test_dynamo_items_carry_ttl_and_sparse_index():
    ddb = FakeDynamo()
    s = DynamoRequestStore(ddb, "t")
    r = rec("a")
    s.create(r)
    assert ddb.tables["t"]["REQ#a"]["pending_shard"] == {"S": "1"} and "expires_at" not in ddb.tables["t"]["REQ#a"]
    r.update(state="COMPLETE", expires_at=1234)
    s.save(r)
    item = ddb.tables["t"]["REQ#a"]
    assert "pending_shard" not in item and item["expires_at"] == {"N": "1234"}
    s.tombstone_put("a", 5000)
    ddb.ttl_sweep("t", 2000)
    assert s.get("a") is None and s.tombstone_get("a") is not None


def test_result_store_contract(results):
    results.put("work", "r1", "a", b"1")
    results.put("work", "r1", "b", b"2")
    results.put("work", "r1", "c", b"3")
    results.put("work", "r1", "d", b"4")
    results.put("result", "r1", "receipt.json", b"R")
    assert results.get("work", "r1", "b") == b"2" and results.get("work", "r2", "b") is None
    results.delete("work", "r1")
    assert results.get("work", "r1", "a") is None and results.get("result", "r1", "receipt.json") == b"R"


def test_s3_layout_encryption_and_presign():
    s3 = FakeS3()
    st = S3ResultStore(s3, "bucket")
    st.put("result", "r1", "receipt.json", b"RECEIPT")
    assert ("bucket", "result/r1/receipt.json") in s3.objects and s3.put_args == ["AES256"]
    assert st.size("result", "r1", "receipt.json") == 7 and st.size("result", "r1", "x") is None
    url = st.presign("result", "r1", "receipt.json", 300, 0)
    assert s3.presigned == [("bucket", "result/r1/receipt.json", 300)] and "X-Amz-Expires=300" in url
    st.put("frames", "r1", "ab", b"F")
    assert st.get_ref(st.ref("frames", "r1", "ab")) == b"F" and st.names("frames", "r1") == ["ab"]
    with pytest.raises(ValueError):
        st.put("elsewhere", "r1", "x", b"")


def test_sqs_queue_and_sns_wake():
    from tessera_issue.util import FakeClock
    sqs = FakeSqs(FakeClock(0))
    q = SqsQueue(sqs, "https://sqs.invalid/q")
    q.send("hello")
    (m,) = q.receive()
    assert m.body == "hello" and q.receive() == []
    q.delete(m.handle)
    assert len(sqs.q("https://sqs.invalid/q")) == 0
    sns = FakeSns()
    SnsWake(sns, {"kms": "arn:kms-wake", "gpg": None})("kms")
    SnsWake(sns, {"kms": "arn:kms-wake", "gpg": None})("gpg")
    assert [t for t, _ in sns.published] == ["arn:kms-wake"]


def event(method, resource, cred, key=None, body=None, request_key=None):
    e = {"httpMethod": method, "resource": resource, "headers": {}, "pathParameters": {"key": key} if key else None,
         "requestContext": {"identity": {"apiKeyId": cred}}, "body": None, "isBase64Encoded": False}
    if body is not None:
        e["body"], e["isBase64Encoded"] = base64.b64encode(body).decode(), True
    if request_key:
        e["headers"]["Tessera-Request-Key"] = request_key
    return e


def test_whole_issuance_through_lambda_handlers_on_aws_adapters(tmp_path, monkeypatch):
    """from_env() wiring with fake clients; signers and chain are the stand-ins behind the same SQS queues."""
    loc = local.build(FROZEN)
    clock, world = loc.clock, loc.world
    ddb, s3, sqs, sns = FakeDynamo(), FakeS3(), FakeSqs(clock), FakeSns()
    s3.put_object(Bucket="results", Key="config/window.json", Body=world.window.to_json().encode())
    env = {"REQUEST_TABLE": "requests", "RESULT_BUCKET": "results", "FREEZE_DIR": str(FROZEN),
           "KMS_REQUEST_QUEUE_URL": "q/kms-req", "KMS_RESPONSE_QUEUE_URL": "q/kms-resp",
           "GPG_REQUEST_QUEUE_URL": "q/gpg-req", "GPG_RESPONSE_QUEUE_URL": "q/gpg-resp",
           "KMS_WAKE_TOPIC_ARN": "arn:wake-kms", "GPG_WAKE_TOPIC_ARN": "arn:wake-gpg",
           "OTS_CALENDARS": "https://cal.invalid", "EXPLORERS": "https://a.invalid,https://b.invalid"}
    iss = lambda_app.from_env(env, FakeSession(dynamodb=ddb, s3=s3, sqs=sqs, sns=sns))
    assert iss.window.assertion == world.window.assertion
    # Offline: the network clients built by from_env are replaced by the stand-ins; stores, queues and wake are AWS.
    iss.calendars, iss.headers, iss.dns, iss.clock = [world.calendar], world.chain, world.dns, clock
    monkeypatch.setattr(lambda_app, "_ISSUER", iss)
    workers = [StandInSigner("kms", world.kms_key, sqs.q("q/kms-req"), sqs.q("q/kms-resp"), clock),
               StandInSigner("gpg", world.gpg_key, sqs.q("q/gpg-req"), sqs.q("q/gpg-resp"), clock)]

    key = str(uuid.uuid4())
    r = lambda_app.api_handler(event("POST", "/v1/requests", "apikey-1", body=b"\x00\xffbinary\r\n",
                                     request_key=key), None)
    assert r["statusCode"] == 202 and json.loads(r["body"])["state"] == "ACCEPTED"
    assert lambda_app.api_handler(event("GET", "/v1/requests/{key}", "apikey-2", key=key), None)["statusCode"] == 404
    for _ in range(60):
        for w in workers:
            w.process()
        lambda_app.poller_handler({}, None)
        clock.advance(600)
        world.chain.mine(1)
        st = json.loads(lambda_app.api_handler(event("GET", "/v1/requests/{key}", "apikey-1", key=key), None)["body"])
        if st["state"] != "ACCEPTED":
            break
    assert st["state"] == "COMPLETE", st
    assert {t for t, _ in sns.published} == {"arn:wake-kms", "arn:wake-gpg"}          # E-01 wake on demand
    r = lambda_app.api_handler(event("GET", "/v1/requests/{key}/receipt", "apikey-1", key=key), None)
    assert r["statusCode"] == 303 and r["body"] == "{}"                      # IS-06: one GET, redirect to a short-lived URL
    assert r["headers"]["Location"].endswith("X-Amz-Expires=300") and "Range" not in r["headers"]
    rid = api.record_id("apikey-1", key)
    bundle = s3.objects[("results", f"result/{rid}/receipt.json")]
    assert r["headers"]["Tessera-Receipt-SHA256"] == st["receipt_sha256"]
    assert not [k for b, k in s3.objects if k.startswith(("content/", "work/"))]      # deleted at the end
    rc, out, err = verify_with_cli(loc, bundle, tmp_path)
    assert rc == 0 and out["stable"]["verdict"] == "VALID_STRICT", (out, err)


def test_lambda_api_handler_edge_cases(loc):
    k = str(uuid.uuid4())
    h = lambda e: lambda_app.handle_api_event(loc.iss, e)  # noqa: E731
    r = h(event("POST", "/v1/requests", "c", body=b"x"))
    assert r["statusCode"] == 400 and json.loads(r["body"])["reason"] == "BAD_REQUEST"
    bad = event("POST", "/v1/requests", "c", request_key=k)
    bad.update(body="!!notbase64", isBase64Encoded=True)
    assert h(bad)["statusCode"] == 400
    assert h(event("DELETE", "/v1/requests/{key}", "c", key=k))["statusCode"] == 404
    assert h(event("POST", "/v1/requests", None, body=b"x", request_key=k))["statusCode"] == 401
    plain = event("POST", "/v1/requests", "c", request_key=k)
    plain["body"] = "text body"
    assert h(plain)["statusCode"] == 202
