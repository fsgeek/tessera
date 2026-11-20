"""G1 (docs/V1-DETECTION-CONTRACT.md): structured log lines from the API and the poller (LOGGING.md)."""
import base64
import json
import uuid
from types import SimpleNamespace

import pytest

from tessera_issue import api, lambda_app, logs, pipeline
from tessera_issue.util import MIB, sha256hex

from helpers import submit

SECRET_CONTENT = b"SECRET-CONTENT-MARKER-0123456789"


def lines(capsys):
    out = capsys.readouterr().out
    return [json.loads(x) for x in out.splitlines() if x.startswith("{")]


def event(key, body, cred="cred-A", method="POST", resource="/v1/requests", path_key=None):
    ev = {"httpMethod": method, "resource": resource, "headers": {"Tessera-Request-Key": key} if key else {},
          "requestContext": {"identity": {"apiKeyId": cred}}, "body": base64.b64encode(body).decode()
          if body is not None else None, "isBase64Encoded": True}
    if path_key:
        ev["pathParameters"] = {"key": path_key}
    return ev


def test_api_accepted_request_logs_one_line_without_content_or_key(loc, key, capsys):
    out = lambda_app.handle_api_event(loc.iss, event(key, SECRET_CONTENT))
    assert out["statusCode"] == 202
    raw = capsys.readouterr().out
    assert key not in raw and "cred-A" not in raw and SECRET_CONTENT.decode() not in raw
    (ln,) = [json.loads(x) for x in raw.splitlines() if x.startswith("{")]
    assert ln["event"] == "api" and ln["v"] == 1 and ln["status"] == 202 and ln["state"] == "ACCEPTED"
    assert ln["method"] == "POST" and ln["route"] == "/v1/requests" and ln["content_len"] == len(SECRET_CONTENT)
    assert ln["cred"] == api.cred_digest("cred-A") and ln["rid"] == api.record_id("cred-A", key)
    assert sha256hex(SECRET_CONTENT) not in raw          # not even the content digest


def test_api_too_large_refusal_names_the_reason(loc, key, capsys):
    out = lambda_app.handle_api_event(loc.iss, event(key, b"x" * (MIB + 1)))
    assert out["statusCode"] == 413
    (ln,) = lines(capsys)
    assert ln["status"] == 413 and ln["reason"] == "TOO_LARGE" and ln["content_len"] == MIB + 1


def test_api_key_content_mismatch_and_status_lookup(loc, key, capsys):
    lambda_app.handle_api_event(loc.iss, event(key, b"one"))
    lambda_app.handle_api_event(loc.iss, event(key, b"two"))
    lambda_app.handle_api_event(loc.iss, event(None, None, method="GET", resource="/v1/requests/{key}", path_key=key))
    a, b, c = lines(capsys)
    assert b["status"] == 409 and b["reason"] == "KEY_CONTENT_MISMATCH"
    assert c["method"] == "GET" and c["status"] == 200 and c["content_len"] is None
    assert c["rid"] == a["rid"]


def test_api_exception_logs_one_line_and_still_raises(loc, key, capsys):
    loc.iss.requests.get = lambda rid: (_ for _ in ()).throw(RuntimeError("store down"))
    with pytest.raises(RuntimeError):
        lambda_app.handle_api_event(loc.iss, event(key, b"x"))
    (ln,) = lines(capsys)
    assert ln["event"] == "api" and ln["status"] == 500 and ln["reason"] == "EXCEPTION" and ln["error"] == "RuntimeError"


def test_poller_logs_transitions_siglog_dispositions_and_summary(loc, key, capsys):
    _, rid = submit(loc, key, SECRET_CONTENT)
    capsys.readouterr()
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    out = capsys.readouterr().out
    assert key not in out and SECRET_CONTENT.decode() not in out and "cred-A" not in out
    ls = [json.loads(x) for x in out.splitlines() if x.startswith("{")]
    assert all(x["v"] == 1 and "event" in x for x in ls)
    stages = [x for x in ls if x["event"] == "request_stage" and x["rid"] == rid]
    assert ("frames", "signing") in [(x["from_stage"], x["to_stage"]) for x in stages]
    tr = [x for x in ls if x["event"] == "request_transition" and x["rid"] == rid]
    assert tr[0]["from_state"] == "ACCEPTED" and tr[0]["to_attempt"] == "a1" and tr[0]["from_attempt"] == ""
    assert tr[-1]["from_state"] == "ACCEPTED" and tr[-1]["to_state"] == "COMPLETE"
    sr = [x for x in ls if x["event"] == "signer_response"]
    assert sr and {x["disposition"] for x in sr} == {"used"} and all(x["request_id"] and x["slot"] for x in sr)
    assert any(x["signature_sha256"] and x["frame_sha256"] and x["attempt"] == "a1" for x in sr)
    summ = [x for x in ls if x["event"] == "poll_summary"]
    assert summ and {"drained", "advanced", "cleaned"} <= set(summ[0])


def test_unrequested_signer_response_is_logged(loc, key, capsys):
    kms = loc.workers["kms"]
    kms.responses.send(json.dumps({"request_id": "req-from-an-earlier-run", "status": "SIGNED", "sig_b64": "AAAA"}))
    capsys.readouterr()
    pipeline.drain(loc.iss)
    (ln,) = [x for x in lines(capsys) if x["event"] == "signer_response"]
    assert ln["disposition"] == "unrequested" and ln["slot"] == "kms" and ln["request_id"].startswith("invalid:")
    assert ln["status"] == "SIGNED" and ln["signature_sha256"] == sha256hex(b"\x00\x00\x00") and ln["frame_sha256"] is None


def test_notes_are_emitted(loc, capsys):
    loc.iss.note("poll out of time:", "budget")
    (ln,) = lines(capsys)
    assert ln == {"event": "poller_note", "v": 1, "msg": "poll out of time: budget"}


def test_logging_failure_never_changes_behaviour(loc, key, monkeypatch):
    class Broken:
        def write(self, *_):
            raise OSError("stdout closed")

        def flush(self):
            raise OSError("stdout closed")
    monkeypatch.setattr(logs.sys, "stdout", Broken())
    def boom(*a, **k):
        raise ValueError("boom")
    monkeypatch.setattr(logs, "json", SimpleNamespace(dumps=boom))
    out = lambda_app.handle_api_event(loc.iss, event(key, b"hello"))
    assert out["statusCode"] == 202
    _, rid = submit(loc, str(uuid.uuid4()), b"again")
    assert loc.run_until_done(rid)["state"] == "COMPLETE"
