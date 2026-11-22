"""Trace records (contract item 0(a)): fields, reconciliation of kms jobs, Object Lock parameters, write-once, and
that a record never carries request content, the plaintext request key, an API key value or a URL."""
import json

import fakes
from conftest import T0
from tessera_watch import watcher as W

SECRET_KEY_VALUE = "tEsTaPiKeYvAlUe0123456789abcdefghijklmn"      # what an API key VALUE looks like; never stored
CONTENT = b"the requester's private content"


RID = "d" * 64


def setup_complete(env, request_key="ca33cc04-6032-4da0-8a7a-7fffd0373dd3"):
    k1, k2 = "req-" + "1" * 40, "req-" + "2" * 40
    h1, h2 = fakes.sha(b"s1"), fakes.sha(b"s2")
    jobs = {"s_kms": fakes.job("kms", k1, h1), "p_kms": fakes.job("kms", k2, h2),
            "s_gpg": fakes.job("gpg", "req-" + "3" * 40, fakes.sha(b"g1")),
            "p_gpg": fakes.job("gpg", "req-" + "4" * 40, fakes.sha(b"g2"))}
    rec = fakes.request(RID, "COMPLETE", T0 - 300, created_at=T0 - 4000, jobs=jobs,
                        receipt_sha256=fakes.sha(b"bundle"), cred=W.cred_digest("abc123key"), key=request_key)
    rec["content_sha256"] = fakes.sha(CONTENT)
    rec["content_len"] = len(CONTENT)
    rec["diag"] = SECRET_KEY_VALUE                      # even if a record carried other text, it is not copied
    env.ddb.put("REQ#" + RID, rec)
    env.s3.put("results", f"result/{RID}/{fakes.sha(b'bundle')}.json", b"bundle")
    env.ddb.put("SIGLOG#USED#a", fakes.siglog(T0 - 3000, request_id=k1, sig=h1))
    env.ddb.put("SIGLOG#USED#b", fakes.siglog(T0 - 2990, request_id=k2, sig=h2))
    env.ddb.put("SIGLOG#g", fakes.siglog(T0 - 2990, slot="gpg", request_id="req-" + "3" * 40, sig=fakes.sha(b"g1")))
    e1, e2 = "11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3100, eid=e1), fakes.sign_event(T0 - 3050, eid=e2)])
    return rec, (e1, e2), (h1, h2)


def test_trace_record_fields(env):
    rec, (e1, e2), (h1, h2) = setup_complete(env)
    env.run()
    assert env.sns.sent == []
    t = env.traces()[f"trace/{RID}.json"]
    assert t["format"] == "tessera-v1-trace/1" and t["rid"] == RID and t["record_source"] == "issuer-record"
    assert t["credential_digest"] == rec["cred"] and t["api_key_id"] == "abc123key" and t["client"] == "smoke-test"
    assert t["request_key_sha256"] == fakes.sha(rec["key"].encode())
    assert t["content_sha256"] == fakes.sha(CONTENT) and t["content_len"] == len(CONTENT)
    assert t["state"] == "COMPLETE" and t["receipt_sha256"] == fakes.sha(b"bundle")
    assert t["verification"]["verdict"] == "VALID_STRICT" and t["anchor_heights"] == [1, 2]
    jobs = t["attempts"][0]["jobs"]
    assert jobs["s_kms"]["kms_signs"] == [{"signature_sha256": h1, "cloudtrail_sign_event_id": e1,
                                           "reconciled": "matched", "dispositions": ["used"]}]
    assert jobs["p_kms"]["kms_signs"][0]["cloudtrail_sign_event_id"] == e2
    assert jobs["s_gpg"]["gcp_use_to_sign"].startswith("TODO")
    assert jobs["s_kms"]["signer_request_id"] == "req-" + "1" * 40 and jobs["s_kms"]["frame_sha256"]
    assert t["verification"]["binding"] == "match"


def test_trace_record_has_no_secret_content_key_or_url(env):
    rec, _, _ = setup_complete(env)
    env.run()
    raw = env.s3.objects[("trace", f"trace/{RID}.json")]["body"].decode()
    assert rec["key"] not in raw and rec["key"].replace("-", "") not in raw
    assert CONTENT.decode() not in raw and SECRET_KEY_VALUE not in raw
    assert "http" not in raw and "X-Amz" not in raw and "://" not in raw
    allowed = {"format", "written_at", "watcher_version", "credential_digest", "api_key_id", "client", "rid",
               "request_key_sha256", "content_sha256", "content_len", "state", "reason", "reason_detail", "created_at",
               "ended_at", "attempts", "receipt_sha256", "anchor_heights", "T", "verification", "slot2_reconciliation",
               "record_source"}
    assert set(json.loads(raw)) == allowed


def test_finding_lines_carry_no_content_digest_or_key(env):
    import io
    env.out = io.StringIO()
    rec, _, _ = setup_complete(env)
    env.ddb.put("REQ#" + RID, dict(rec, receipt_sha256="f" * 64))         # its object is missing: a D8 finding
    env.run()
    out = env.out.getvalue() + "".join(m["Message"] for m in env.sns.sent)
    assert "RECEIPT_OBJECT_MISSING" in out
    assert rec["key"] not in out and fakes.sha(CONTENT) not in out and "http" not in out


def test_trace_object_lock_compliance_until_retention(env):
    setup_complete(env)
    env.run()
    (kw,) = [kw for b, k, kw in env.s3.versions if b == "trace"]
    assert kw["ObjectLockMode"] == "COMPLIANCE" and kw["ObjectLockRetainUntilDate"] == "2028-03-07T00:00:00Z"
    assert kw["IfNoneMatch"] == "*"


def test_trace_waits_for_kms_reconciliation_then_bounds_it(env):
    rec, _, _ = setup_complete(env)
    for k in list(env.s3.objects):
        if k[0] == "trail":
            del env.s3.objects[k]                       # the Sign events have not been delivered yet
    env.clock.t = T0 - 2000                             # SIGLOG entries are 1000 s old: not yet declared missing
    env.ddb.put("REQ#" + RID, dict(rec, ended_at=T0 - 2100))
    env.run()
    assert env.traces() == {} and RID in env.state()["pending"]
    env.clock.t = T0 - 2990 + W.SIG_HORIZON_S + 1       # both declared missing (D6), then the record is written
    env.run()
    t = env.traces()[f"trace/{RID}.json"]
    assert t["attempts"][0]["jobs"]["s_kms"]["kms_signs"][0]["reconciled"] == "unmatched"
    assert env.codes().count("SIGNATURE_WITHOUT_SIGN_EVENT") == 2


def test_refused_at_submission_trace(env):
    r = "e" * 64
    env.ddb.put("REQ#" + r, dict(fakes.request(r, "REFUSED", T0 - 10, reason="TOO_LARGE"), attempts=[], cur=0))
    env.run()
    t = env.traces()[f"trace/{r}.json"]
    assert t["state"] == "REFUSED" and t["reason"] == "TOO_LARGE" and t["attempts"] == []
    assert t["verification"] is None and t["api_key_id"] is None


def test_trace_is_write_once_even_if_rerun(env):
    setup_complete(env)
    env.run()
    del env.s3.objects[("state", "state/watcher.json")]   # the state is lost: everything is seen as new again
    env.run()
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 1


def test_a_signer_reason_with_a_sub_code_is_split(env):
    r = "e" * 64
    env.ddb.put("REQ#" + r, fakes.request(r, "FAILED", T0 - 10, reason="SIGNER_REFUSED:KEY_FP_MISMATCH"))
    env.run()
    t = env.traces()[f"trace/{r}.json"]
    assert t["reason"] == "SIGNER_REFUSED" and t["reason_detail"] == "KEY_FP_MISMATCH"


def test_a_record_that_expires_while_pending_is_traced_from_its_snapshot(env):
    """M5: the REQ# item is gone before its kms signatures were final; the trace is still written, once."""
    rec, _, _ = setup_complete(env)
    for k in list(env.s3.objects):
        if k[0] == "trail":
            del env.s3.objects[k]
    env.clock.t = T0 - 2000
    env.ddb.put("REQ#" + RID, dict(rec, ended_at=T0 - 2100))
    env.run()
    assert env.traces() == {}
    del env.ddb.items["REQ#" + RID]
    env.clock.t = T0 - 2990 + W.SIG_HORIZON_S + 1
    env.run()
    t = env.traces()[f"trace/{RID}.json"]
    assert t["record_source"] == "snapshot" and t["request_key_sha256"] == fakes.sha(rec["key"].encode())
    assert "TRACE_FROM_SNAPSHOT" in env.codes()


def test_a_job_signature_not_yet_in_siglog_holds_the_trace(env):
    """M5: the scan read the SIGLOG# partition before the issuer logged a signature and the REQ# page after COMPLETE.
    The trace waits for the entry instead of being locked without it."""
    rec, (e1, e2), (h1, h2) = setup_complete(env)
    del env.ddb.items["SIGLOG#USED#b"]
    env.ddb.put("REQ#" + RID, dict(rec, ended_at=T0 - 2900))
    env.clock.t = T0 - 2800
    env.run()
    assert env.traces() == {}
    env.ddb.put("SIGLOG#USED#b", fakes.siglog(T0 - 2990, request_id="req-" + "2" * 40, sig=h2))
    env.clock.t = T0 - 2200
    env.run()
    env.clock.t = T0
    env.run()
    t = env.traces()[f"trace/{RID}.json"]
    assert t["attempts"][0]["jobs"]["p_kms"]["kms_signs"][0]["cloudtrail_sign_event_id"] == e2
    assert env.sns.sent == []


def test_a_job_signature_never_logged_is_a_finding_and_the_trace_says_so(env):
    rec, _, (h1, h2) = setup_complete(env)
    del env.ddb.items["SIGLOG#USED#b"]
    env.run()
    env.clock.t += W.UNLOGGED_S + 1
    env.run()
    assert "JOB_SIGNATURE_NOT_LOGGED" in env.codes()
    t = env.traces()[f"trace/{RID}.json"]
    assert t["attempts"][0]["jobs"]["p_kms"]["kms_signs"] == [
        {"signature_sha256": h2, "reconciled": "not-logged", "cloudtrail_sign_event_id": None, "dispositions": []}]


def test_a_failed_trace_write_is_retried_until_written(env):
    setup_complete(env)
    env.s3.fail_put = lambda b, k: fakes.ClientError("SlowDown") if b == "trace" else None
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["TRACE_WRITE_FAILED"] and RID in env.state()["pending"] and len(env.cw.beats) == 2
    env.s3.fail_put = None
    env.clock.t += 600
    env.run()
    assert f"trace/{RID}.json" in env.traces() and env.state()["pending"] == {}
