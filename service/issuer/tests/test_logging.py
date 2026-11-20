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


# ------------------------------------------------------------------------------------------------ G1 review fixes
FAKE_URL = "https://bucket.s3.amazonaws.com/obj?X-Amz-Signature=PRESIGNED-SIG-9f8e7d&X-Amz-Credential=AKIAFAKE"
FAKE_SECRET = "hunter2-SECRET-TOKEN-777"
LEAK = f"boom {FAKE_URL} {FAKE_SECRET}"


def all_lines(capsys):
    return capsys.readouterr().out


def test_notes_never_carry_exception_text(loc, key, capsys, monkeypatch):
    _, rid = submit(loc, key, SECRET_CONTENT)
    capsys.readouterr()
    loc.iss.note("direct:", RuntimeError(LEAK))                       # an exception passed to note()

    def stage_fault(iss, rec, now):
        raise RuntimeError(LEAK)
    monkeypatch.setitem(pipeline.STAGES, "frames", stage_fault)        # the poller's per-request handler
    loc.tick()
    def take_fault(*a, **k):
        raise ConnectionError(LEAK)
    loc.iss.signers["kms"].responses.send(json.dumps({"request_id": "req-" + "0" * 40, "status": "SIGNED"}))
    monkeypatch.setattr(pipeline, "_take", take_fault)                 # drain's "not taken" path
    for _ in range(6):
        pipeline.drain(loc.iss)
    out = all_lines(capsys)
    assert FAKE_URL not in out and FAKE_SECRET not in out and "PRESIGNED" not in out and "boom" not in out
    notes = [json.loads(x) for x in out.splitlines() if x.startswith("{") and '"poller_note"' in x]
    assert any("RuntimeError" in n["msg"] and rid[:12] in n["msg"] for n in notes)
    assert any("ConnectionError" in n["msg"] for n in notes)


def test_stdout_failures_never_change_api_behaviour(loc, key, monkeypatch):
    for exc in (OSError("stdout closed"), SystemExit(3)):
        class Broken:
            def write(self, *_):
                raise exc
        monkeypatch.setattr(logs.sys, "stdout", Broken())
        k = str(uuid.uuid4())
        assert lambda_app.handle_api_event(loc.iss, event(k, b"hello"))["statusCode"] == 202     # return kept
        loc.iss.requests.get = lambda rid: (_ for _ in ()).throw(RuntimeError("store down"))
        with pytest.raises(RuntimeError, match="store down"):                                      # original kept
            lambda_app.handle_api_event(loc.iss, event(k, b"x"))
        del loc.iss.requests.get


def test_stdout_failures_never_change_poll_return_or_exception(loc, key, monkeypatch):
    _, rid = submit(loc, key)

    class Broken:
        def write(self, *_):
            raise SystemExit(9)
    monkeypatch.setattr(logs.sys, "stdout", Broken())
    out = pipeline.poll(loc.iss)                                       # a successful return survives
    assert "advanced" in out
    monkeypatch.setattr(pipeline, "_poll", lambda *a: (_ for _ in ()).throw(KeyError("original")))
    with pytest.raises(KeyError, match="original"):                    # an in-flight exception survives
        pipeline.poll(loc.iss)


def _refusal_setup(loc, key):
    _, rid = submit(loc, key, SECRET_CONTENT)
    loc.tick(run_signers=False)
    rec = loc.iss.requests.get(rid)
    return rid, rec["attempts"][0]["jobs"]["s_gpg"]["request_id"], loc.iss.signers["gpg"].responses


def _drain_all(loc):
    for _ in range(8):
        pipeline.drain(loc.iss)


def test_unknown_but_valid_reason_is_not_logged_and_maps_to_unrecognized(loc, key, capsys):
    rid, srid, q = _refusal_setup(loc, key)
    capsys.readouterr()
    q.send(json.dumps({"request_id": srid, "status": "REFUSED", "reason": "SECRET_CONTENT_123"}))
    _drain_all(loc)
    out = all_lines(capsys)
    assert "SECRET_CONTENT_123" not in out
    sr = [json.loads(x) for x in out.splitlines() if '"signer_response"' in x]
    assert [(x["disposition"], x["reason"]) for x in sr] == [("refused", "UNRECOGNIZED_REASON")]
    tr = [json.loads(x) for x in out.splitlines() if '"request_transition"' in x]
    assert tr and tr[0]["reason"] == "SIGNER_REFUSED:UNRECOGNIZED_REASON"
    assert "SECRET_CONTENT_123" not in json.dumps(loc.iss.requests.get(rid), default=str)


def test_known_refusal_reasons_pass_through(loc, key, capsys):
    rid, srid, q = _refusal_setup(loc, key)
    capsys.readouterr()
    q.send(json.dumps({"request_id": srid, "status": "REFUSED", "reason": "SIGNING_STOPPED"}))
    _drain_all(loc)
    (ln,) = [x for x in lines(capsys) if x["event"] == "signer_response"]
    assert ln["reason"] == "SIGNING_STOPPED" and ln["disposition"] == "refused"


def test_malformed_and_bad_signature_dispositions_are_logged(loc, key, capsys):
    rid, srid, q = _refusal_setup(loc, key)
    capsys.readouterr()
    q.send(json.dumps({"request_id": srid, "status": "SIGNED", "sig_b64": "!!not base64!!"}))
    _drain_all(loc)
    (ln,) = [x for x in lines(capsys) if x["event"] == "signer_response"]
    assert ln["disposition"] == "malformed" and ln["status"] == "SIGNED" and ln["signature_sha256"] is None
    q.send(json.dumps({"request_id": srid, "status": "SIGNED", "sig_b64": base64.b64encode(b"not a signature").decode()}))
    _drain_all(loc)
    (ln,) = [x for x in lines(capsys) if x["event"] == "signer_response"]
    assert ln["disposition"] == "bad-signature" and ln["frame_sha256"] and ln["signature_sha256"]


def test_failed_guarded_save_emits_no_transition_or_stage_and_is_not_counted(loc, key, capsys, monkeypatch):
    _, rid = submit(loc, key)
    capsys.readouterr()
    monkeypatch.setattr(loc.iss.requests, "save", lambda rec, expect=None: False)
    out = loc.tick()
    ls = lines(capsys)
    assert not [x for x in ls if x["event"] in ("request_transition", "request_stage")]
    assert out["advanced"][rid][0] == out["advanced"][rid][1] and out["committed"] == 0
    assert loc.iss.requests.get(rid)["stage"] == "frames"             # and nothing was stored


def test_committed_stage_change_is_logged_even_if_the_stage_then_raises(loc, key, capsys, monkeypatch):
    _, rid = submit(loc, key)
    capsys.readouterr()

    def send_fault(*a, **k):
        raise RuntimeError("signer queue down")
    monkeypatch.setattr(pipeline, "_send", send_fault)
    out = loc.tick()
    ls = lines(capsys)
    st = [(x["from_stage"], x["to_stage"]) for x in ls if x["event"] == "request_stage" and x["rid"] == rid]
    assert st == [("frames", "signing")]
    assert out["advanced"][rid] == ["frames", "signing"] or out["advanced"][rid] == ("frames", "signing")
    assert out["committed"] == 1 and loc.iss.requests.get(rid)["stage"] == "signing"
