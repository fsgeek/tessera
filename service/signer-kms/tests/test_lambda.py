"""The Lambda adapter: SQS event in, responses on the response queue, partial batch failures for redelivery; the S3
frame fetch; and from_env against fake clients."""
import json

from tessera_issue.util import sha256hex
from tessera_sign_kms import lambda_app

from conftest import NOW, STOP
from fakes import ClientError, FakeS3, FakeSession, FakeSqs, Log
from tessera_issue.util import rfc3339

RESP = "https://sqs.test/kms-responses"


def event(*bodies, count=1):
    return {"Records": [{"messageId": f"m{i}", "body": b, "attributes": {"ApproximateReceiveCount": str(count)},
                         "eventSource": "aws:sqs"} for i, b in enumerate(bodies)]}


def env(ctx):
    return {"KMS_KEY_ID": "alias/tessera-kms", "KEY_FP": ctx.key.fp_kms, "SIGN_UNTIL": rfc3339(STOP),
            "RESPONSE_QUEUE_URL": RESP, "FRAMES_BUCKET": "results-bucket"}


def build(ctx, monkeypatch, **over):
    s3, sqs = FakeS3(), FakeSqs(ctx.clock)
    log = Log()
    monkeypatch.setattr(lambda_app, "log_line", log)
    signer, responses = lambda_app.from_env(dict(env(ctx), **over), FakeSession(kms=ctx.kms, s3=s3, sqs=sqs),
                                            clock=ctx.clock)
    return signer, responses, s3, sqs, log


def responses_of(sqs):
    return [json.loads(m.body) for m in sqs.q(RESP).receive(100)]


def test_event_answers_every_message_and_logs_each(ctx, monkeypatch):
    signer, responses, s3, sqs, log = build(ctx, monkeypatch)
    out = lambda_app.handle_event(signer, responses, event(ctx.body(ctx.attest(), rid="req-a"),
                                                           ctx.body(ctx.attest(), rid="req-b", sign_by=NOW - 1),
                                                           "garbage"))
    assert out == {"batchItemFailures": []}
    got = {r["request_id"]: r for r in responses_of(sqs)}
    assert got["req-a"]["status"] == "SIGNED" and got["req-b"]["reason"] == "SIGNING_STOPPED"
    assert got[None]["reason"] == "BAD_REQUEST"
    assert [e["event"] for e in log] == ["signed", "refused", "refused"]


def test_transient_failure_is_reported_for_redelivery_not_answered(ctx, monkeypatch):
    signer, responses, s3, sqs, log = build(ctx, monkeypatch)
    ctx.kms.fail = ClientError("ThrottlingException")
    out = lambda_app.handle_event(signer, responses, event(ctx.body(ctx.attest()), count=1))
    assert out == {"batchItemFailures": [{"itemIdentifier": "m0"}]} and responses_of(sqs) == []
    out = lambda_app.handle_event(signer, responses, event(ctx.body(ctx.attest()), count=3))
    assert out == {"batchItemFailures": []} and responses_of(sqs)[0]["reason"] == "SIGNING_ERROR"


def test_response_not_sent_is_redelivered(ctx, monkeypatch):
    signer, responses, s3, sqs, log = build(ctx, monkeypatch)
    sqs.fail = ClientError("AWS.SimpleQueueService.NonExistentQueue")
    out = lambda_app.handle_event(signer, responses, event(ctx.body(ctx.attest())))
    assert out == {"batchItemFailures": [{"itemIdentifier": "m0"}]}
    assert [e["event"] for e in log] == ["signed", "response-not-sent"]


def test_frames_are_fetched_from_the_configured_bucket(ctx, monkeypatch):
    signer, responses, s3, sqs, log = build(ctx, monkeypatch)
    frame = ctx.attest(content=b"y" * 300_000)
    key = f"frames/{'e' * 64}/{sha256hex(frame)}"
    s3.objects[("results-bucket", key)] = frame
    body = json.dumps({"request_id": "req-r", "frame_ref": key, "frame_sha256": sha256hex(frame),
                       "sign_by": rfc3339(STOP)})
    lambda_app.handle_event(signer, responses, event(body))
    assert responses_of(sqs)[0]["status"] == "SIGNED" and s3.gets == [("results-bucket", key)]
    assert lambda_app.s3_fetch(s3, "results-bucket")(f"frames/x/{'0' * 64}") is None


def test_from_env_refuses_to_start_without_the_pinned_key(ctx, monkeypatch):
    import pytest
    from tessera_sign_kms.signer import KeyMismatch
    for fp in ("", "spki-sha256:" + "f" * 64):
        with pytest.raises(KeyMismatch):
            build(ctx, monkeypatch, KEY_FP=fp)
