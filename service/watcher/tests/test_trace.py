"""Trace records (contract item 0(a)): fields, reconciliation of kms jobs, Object Lock parameters, write-once, and
that a record never carries request content, the plaintext request key, an API key value or a URL."""
import json

import fakes
from conftest import T0
from tessera_watch import watcher as W

SECRET_KEY_VALUE = "tEsTaPiKeYvAlUe0123456789abcdefghijklmn"      # what an API key VALUE looks like; never stored
CONTENT = b"the requester's private content"


def setup_complete(env, request_key="ca33cc04-6032-4da0-8a7a-7fffd0373dd3"):
    k1, k2 = "kms-s-1", "kms-p-1"
    h1, h2 = fakes.sha(b"s1"), fakes.sha(b"s2")
    jobs = {"s_kms": fakes.job("kms", k1, h1), "p_kms": fakes.job("kms", k2, h2),
            "s_gpg": fakes.job("gpg", "gpg-s-1", fakes.sha(b"g1")), "p_gpg": fakes.job("gpg", "gpg-p-1", fakes.sha(b"g2"))}
    rec = fakes.request("rid1", "COMPLETE", T0 - 300, created_at=T0 - 4000, jobs=jobs,
                        receipt_sha256=fakes.sha(b"bundle"), cred=W.cred_digest("abc123key"), key=request_key)
    rec["content_sha256"] = fakes.sha(CONTENT)
    rec["content_len"] = len(CONTENT)
    rec["diag"] = SECRET_KEY_VALUE                      # even if a record carried other text, it is not copied
    env.ddb.put("REQ#rid1", rec)
    env.s3.put("results", f"result/rid1/{fakes.sha(b'bundle')}.json", b"bundle")
    env.ddb.put("SIGLOG#USED#a", fakes.siglog(T0 - 3000, request_id=k1, sig=h1))
    env.ddb.put("SIGLOG#USED#b", fakes.siglog(T0 - 2990, request_id=k2, sig=h2))
    env.ddb.put("SIGLOG#g", fakes.siglog(T0 - 2990, slot="gpg", request_id="gpg-s-1", sig=fakes.sha(b"g1")))
    e1, e2 = "11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3100, eid=e1), fakes.sign_event(T0 - 3050, eid=e2)])
    return rec, (e1, e2), (h1, h2)


def test_trace_record_fields(env):
    rec, (e1, e2), (h1, h2) = setup_complete(env)
    env.run()
    assert env.sns.sent == []
    t = env.traces()["trace/rid1.json"]
    assert t["format"] == "tessera-v1-trace/1"
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
    assert jobs["s_kms"]["signer_request_id"] == "kms-s-1" and jobs["s_kms"]["frame_sha256"]


def test_trace_record_has_no_secret_content_key_or_url(env):
    rec, _, _ = setup_complete(env)
    env.run()
    raw = env.s3.objects[("trace", "trace/rid1.json")]["body"].decode()
    assert rec["key"] not in raw and rec["key"].replace("-", "") not in raw
    assert CONTENT.decode() not in raw and SECRET_KEY_VALUE not in raw
    assert "http" not in raw and "X-Amz" not in raw and "://" not in raw
    allowed = {"format", "written_at", "watcher_version", "credential_digest", "api_key_id", "client", "rid",
               "request_key_sha256", "content_sha256", "content_len", "state", "reason", "created_at", "ended_at",
               "attempts", "receipt_sha256", "anchor_heights", "T", "verification", "slot2_reconciliation"}
    assert set(json.loads(raw)) == allowed


def test_finding_lines_carry_no_content_digest_or_key(env):
    import io
    env.out = io.StringIO()
    rec, _, _ = setup_complete(env)
    env.ddb.put("REQ#rid1", dict(rec, receipt_sha256="f" * 64))         # its object is missing: a D8 finding
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
    env.ddb.put("REQ#rid1", dict(rec, ended_at=T0 - 2100))
    env.run()
    assert env.traces() == {} and "rid1" in env.state()["pending"]
    env.clock.t = T0 - 2990 + W.CT_LAG_S + 1            # both declared missing (D6), then the record is written
    env.run()
    t = env.traces()["trace/rid1.json"]
    assert t["attempts"][0]["jobs"]["s_kms"]["kms_signs"][0]["reconciled"] == "unmatched"
    assert env.codes().count("SIGNATURE_WITHOUT_SIGN_EVENT") == 2


def test_refused_at_submission_trace(env):
    env.ddb.put("REQ#r", dict(fakes.request("r", "REFUSED", T0 - 10, reason="TOO_LARGE"), attempts=[], cur=0))
    env.run()
    t = env.traces()["trace/r.json"]
    assert t["state"] == "REFUSED" and t["reason"] == "TOO_LARGE" and t["attempts"] == []
    assert t["verification"] is None and t["api_key_id"] is None


def test_trace_is_write_once_even_if_rerun(env):
    setup_complete(env)
    env.run()
    del env.s3.objects[("state", "state/watcher.json")]   # the state is lost: everything is seen as new again
    env.run()
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 1
