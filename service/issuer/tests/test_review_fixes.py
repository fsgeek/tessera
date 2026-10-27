"""Regression tests for the Codex review of the V1 issuer (docs/reviews/issuer/CODEX-REVIEW.md, IS-01..IS-11). Each
test reproduces the review's failing scenario; docs/reviews/issuer/DISPOSITION.md maps findings to tests."""
import json
import re
import struct
import uuid
from pathlib import Path

import pytest

from tessera_issue import api, dns, local, pipeline
from tessera_issue.aws import DynamoRequestStore, S3ResultStore
from tessera_issue.service import DEADLINE_S, RETENTION_S
from tessera_issue.util import MIB, sha256hex

from conftest import FROZEN
from fakes import FakeDynamo, FakeS3
from helpers import submit

SQS_MAX = 1048576                         # SendMessage maximum message size, bytes


def held(worker):
    real = worker.process
    worker.process = lambda limit=None: 0
    return real


def blobs(loc, rid, ns=None):
    return [k for k in loc.iss.results.blobs if k[1] == rid and (ns is None or k[0] == ns)]


def until_stage(loc, rid, stage, max_ticks=100):
    for _ in range(max_ticks):
        rec = loc.iss.requests.get(rid)
        if rec["stage"] == stage:
            return rec
        loc.tick()
    raise AssertionError("stage not reached: " + stage)


# ------------------------------------------------------------------------------------------------ IS-01
def test_IS01_signature_is_not_eligible_before_its_log_record_is_durable(loc, key):
    _, rid = submit(loc, key)
    store = loc.iss.requests
    real_add, failed = store.siglog_add, []

    def flaky(entry):
        if entry.get("disposition") == "used" and entry["slot"] == "gpg" and not failed:
            failed.append(entry["request_id"])
            raise OSError("log write failed")
        return real_add(entry)
    store.siglog_add = flaky
    pipeline.poll(loc.iss)                               # frames built and sent
    for w in loc.workers.values():
        w.process()
    try:
        pipeline.poll(loc.iss)
    except OSError:
        pass
    assert failed
    store.siglog_add = real_add
    logged = {e["signature_sha256"] for e in store.siglog() if e["disposition"] == "used"}
    rec = store.get(rid)
    for j in rec["jobs"].values():                       # every signature the record relies on is logged
        assert j["sig_sha256"] is None or j["sig_sha256"] in logged
    loc.workers["gpg"].responses.msgs.clear()            # the unacknowledged response is never seen again
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    used = {(e["request_id"], e["signature_sha256"]) for e in store.siglog() if e["disposition"] == "used"}
    for j in rec["jobs"].values():
        assert (j["request_id"], j["sig_sha256"]) in used


def test_IS01_seal_requires_the_log_record(loc, key):
    _, rid = submit(loc, key)
    pipeline.poll(loc.iss)
    for w in loc.workers.values():
        w.process()
    pipeline.drain(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert all(j["sig_sha256"] for j in rec["jobs"].values())
    gone = rec["jobs"]["s_gpg"]["sig_sha256"]
    loc.iss.requests.log = [e for e in loc.iss.requests.log if e["signature_sha256"] != gone]
    pipeline.poll(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert rec["stage"] == "signing" and rec["jobs"]["s_gpg"]["sig_sha256"] is None


# ------------------------------------------------------------------------------------------------ IS-02
def test_IS02_completion_cannot_cross_the_24h_deadline(loc, key):
    _, rid = submit(loc, key)
    rec = until_stage(loc, rid, "assemble")
    created = rec["created_at"]
    loc.clock.t = created + DEADLINE_S - 1
    real = loc.iss.preship.check

    def slow(*a, **kw):
        out = real(*a, **kw)
        loc.clock.advance(2)                             # verification takes two seconds
        return out
    loc.iss.preship.check = slow
    pipeline.poll(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "FAILED" and rec["reason"] == "NOT_COMPLETE_WITHIN_24H"
    assert rec["ended_at"] == created + DEADLINE_S + 1   # the actual transition time
    assert not blobs(loc, rid, "result")


# ------------------------------------------------------------------------------------------------ IS-03
def test_IS03_signers_refuse_queued_work_after_the_signing_stop(loc, key):
    w = loc.iss.window
    loc.clock.t = w.accept_until
    _, rid = submit(loc, key)
    real = {s: held(wk) for s, wk in loc.workers.items()}
    while loc.clock() <= w.sign_until:
        loc.tick()
    assert loc.iss.requests.get(rid)["state"] == "FAILED"
    for s, wk in loc.workers.items():
        wk.process = real[s]
        n = len(wk.requests)
        assert n and wk.process() == n
        assert wk.signed == []                           # no signature made after the stop
        bodies = [json.loads(m["body"]) for m in wk.responses.msgs.values()]
        assert bodies and all(b["status"] == "REFUSED" for b in bodies)


# ------------------------------------------------------------------------------------------------ IS-04
def test_IS04_failed_tombstone_write_cannot_free_the_key():
    loc = local.build(FROZEN, window_days=90)
    key, store = str(uuid.uuid4()), loc.iss.requests
    real, fails = store.tombstone_put, []

    def once(rid, until):
        if not fails:
            fails.append(rid)
            raise OSError("tombstone write failed")
        return real(rid, until)
    store.tombstone_put = once
    loc.iss.closing = True
    try:
        submit(loc, key)
    except OSError:
        pass
    r, rid = submit(loc, key)                            # client retry after the error
    assert r.body["state"] == "REFUSED"
    loc.iss.closing = False
    loc.clock.t = store.get(rid)["ended_at"] + RETENTION_S
    store.expire(loc.clock())
    assert store.get(rid) is None
    r, _ = submit(loc, key)
    assert r.status == 410 and r.body["state"] == "EXPIRED"


def test_IS04_existing_record_repairs_a_missing_tombstone(loc, key):
    _, rid = submit(loc, key)
    loc.iss.requests.tombs.clear()                       # a record left without its tombstone (older code)
    submit(loc, key)
    assert loc.iss.requests.tombstone_get(rid) is not None


def test_IS04_dynamo_creates_record_and_tombstone_in_one_transaction():
    ddb = FakeDynamo()
    st = DynamoRequestStore(ddb, "t")
    rec = {"rid": "r", "state": "REFUSED", "stage": None, "expires_at": 5}
    assert st.create(rec, 99)
    assert "transact_write_items" in ddb.calls and "put_item" not in ddb.calls
    assert st.tombstone_get("r") == {"rid": "r", "keep_until": 99}
    assert not st.create(dict(rec), 99)


# ------------------------------------------------------------------------------------------------ IS-05
def test_IS05_racing_refusal_leaves_no_content(loc, key):
    store, results, content = loc.iss.requests, loc.iss.results, b"racing content"
    real_create, real_put, raced = store.create, results.put, []

    def race():                                          # B is refused after A's lookup, before A's next write
        if raced:
            return
        raced.append(1)
        store.create, results.put = real_create, real_put
        loc.iss.signing_available = False
        rb = api.submit(loc.iss, "cred-A", key, content)
        assert rb.body["state"] == "REFUSED"
        loc.iss.signing_available = True
    store.create = lambda *a: (race(), store.create(*a))[1]
    results.put = lambda *a: (race(), results.put(*a))[1]
    ra, rid = submit(loc, key, content)
    assert raced and ra.body["state"] == "REFUSED"
    assert not blobs(loc, rid)


def test_IS05_interrupted_upload_is_recovered_by_a_retry(loc, key):
    real, fails = loc.iss.results.put, []

    def once(ns, rid, name, data):
        if ns == "content" and not fails:
            fails.append(1)
            raise OSError("upload interrupted")
        return real(ns, rid, name, data)
    loc.iss.results.put = once
    with pytest.raises(OSError):
        submit(loc, key, b"retry me")
    rid = api.record_id("cred-A", key)
    first = loc.iss.requests.get(rid)                    # CF-05: ownership is durable before any content is stored
    assert first is not None and first["state"] == "ACCEPTED" and first["stage"] == "upload"
    assert not blobs(loc, rid, "content")
    r, _ = submit(loc, key, b"retry me")
    assert r.status == 202
    resumed = loc.iss.requests.get(rid)                  # the retry resumes that same record
    assert resumed["created_at"] == first["created_at"] and resumed["stage"] == "frames"
    assert [e for e in resumed["events"] if e[1] == "submitted"] == [e for e in first["events"] if e[1] == "submitted"]
    assert loc.run_until_done(rid)["state"] == "COMPLETE"


def test_IS05_abandoned_upload_fails_after_the_grace_period(loc, key):
    loc.iss.results.put = lambda *a: (_ for _ in ()).throw(OSError("upload interrupted"))
    with pytest.raises(OSError):
        submit(loc, key, b"abandoned")
    rid = api.record_id("cred-A", key)
    pipeline.poll(loc.iss)
    assert loc.iss.requests.get(rid)["state"] == "ACCEPTED"   # still within the grace period
    loc.clock.advance(pipeline.UPLOAD_GRACE_S)
    pipeline.poll(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "FAILED" and rec["reason"] == "CONTENT_UNAVAILABLE"


# ------------------------------------------------------------------------------------------------ IS-06
def s3_loc():
    loc = local.build(FROZEN)
    loc.iss.results = S3ResultStore(FakeS3(), "bucket")
    loc.workers["kms"].fetch = loc.workers["gpg"].fetch = getattr(loc.iss.results, "get_ref", None)
    return loc


def test_IS06_url_is_minted_only_after_the_credential_and_state_checks(key):
    loc = s3_loc()
    _, rid = submit(loc, key)
    s3 = loc.iss.results.c
    assert api.receipt(loc.iss, "cred-A", key).status == 409 and not getattr(s3, "presigned", [])   # not COMPLETE
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    assert api.receipt(loc.iss, "cred-B", key).status == 404 and not getattr(s3, "presigned", [])   # other credential
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    r = api.receipt(loc.iss, "cred-A", key)
    assert r.status == 303 and r.headers["Tessera-Receipt-SHA256"] == rec["receipt_sha256"]
    assert r.headers["Location"].startswith("https://s3.test/bucket/result/")
    assert len(s3.presigned) == 1 and s3.presigned[0][2] <= 300                                     # lifetime
    api.receipt(loc.iss, "cred-A", key)
    assert len(s3.presigned) == 2                              # a fresh mint each time; nothing is reused
    loc.clock.t = rec["ended_at"] + RETENTION_S
    n = len(s3.presigned)
    assert api.receipt(loc.iss, "cred-A", key).status == 410 and len(s3.presigned) == n             # expired


def test_IS06_url_dies_at_300_s_and_the_object_at_30_days(loc, key):
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert api.RECEIPT_URL_TTL_S == 300
    loc.clock.t = rec["ended_at"] + 1000
    url = api.receipt(loc.iss, "cred-A", key).headers["Location"]
    res = loc.iss.results
    assert sha256hex(res.fetch_url(url, loc.clock())) == rec["receipt_sha256"]
    assert res.fetch_url(url, loc.clock() + 300) is not None and res.fetch_url(url, loc.clock() + 301) is None
    loc.clock.t = rec["ended_at"] + RETENTION_S
    loc.tick()                                                  # the poller deletes the receipt at 30 days
    assert res.fetch_url(url, loc.clock()) is None
    assert api.receipt(loc.iss, "cred-A", key).status == 410


# ------------------------------------------------------------------------------------------------ IS-07
def test_IS07_failed_cleanup_at_the_end_is_retried(loc, key):
    _, rid = submit(loc, key)
    real, fails = loc.iss.results.delete, []

    def once(ns, r):
        if ns == "content" and not fails:
            fails.append(1)
            raise OSError("delete failed")
        return real(ns, r)
    loc.iss.results.delete = once
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and fails
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid, "content") and not blobs(loc, rid, "work")


def test_IS07_results_are_deleted_30_days_after_the_end(loc, key):
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert blobs(loc, rid, "result")
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    pipeline.poll(loc.iss)
    assert blobs(loc, rid, "result")
    loc.clock.t = rec["ended_at"] + RETENTION_S
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid)
    assert loc.iss.requests.cleanup_list() == []


# ------------------------------------------------------------------------------------------------ IS-08
def test_IS08_concurrent_metadata_update_does_not_lose_a_verified_signature(loc, key):
    _, rid = submit(loc, key)
    real, done = loc.iss.results.put, []

    def concurrent(ns, r, name, data):
        real(ns, r, name, data)
        if name.startswith("sig-s_kms") and not done:   # another consumer saves the record meanwhile
            done.append(1)
            other = loc.iss.requests.get(r)
            other["events"].append([loc.clock(), "other consumer"])
            assert loc.iss.requests.save(other)
    loc.iss.results.put = concurrent
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and done
    assert {s: len(w.signed) for s, w in loc.workers.items()} == {"kms": 2, "gpg": 2}


def test_IS08_stored_verified_signatures_are_reconciled_before_resending(loc, key):
    _, rid = submit(loc, key)
    store = loc.iss.requests
    real_save = store.save
    pipeline.poll(loc.iss)
    store.save = lambda rec: False                       # every metadata merge loses
    for w in loc.workers.values():
        w.process()
    pipeline.drain(loc.iss)
    store.save = real_save
    assert not any(j["sig_sha256"] for j in store.get(rid)["jobs"].values())
    loc.clock.advance(loc.iss.signer_retry_s)
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    assert {s: len(w.signed) for s, w in loc.workers.items()} == {"kms": 2, "gpg": 2}


# ------------------------------------------------------------------------------------------------ IS-09
def test_IS09_one_mib_content_fits_the_queue_limit(loc, key):
    sizes = []
    for s in loc.iss.signers.values():
        q, real = s.requests, s.requests.send
        q.send = (lambda real: lambda body: (sizes.append(len(body.encode())), real(body))[1])(real)
    _, rid = submit(loc, key, bytes(range(256)) * (MIB // 256))
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    assert sizes and max(sizes) <= SQS_MAX
    assert not blobs(loc, rid, "frames")                 # frame objects are deleted with the request


def test_IS09_queue_stand_in_enforces_the_sqs_limit(loc):
    with pytest.raises(ValueError):
        loc.iss.signers["kms"].requests.send("x" * (SQS_MAX + 1))


def test_IS09_frame_reference_is_digest_bound(loc, key):
    _, rid = submit(loc, key, b"x" * MIB)
    loc.tick(run_signers=False)
    rec = loc.iss.requests.get(rid)
    refs = [k for k in loc.iss.results.blobs if k[0] == "frames"]
    assert refs
    for ref in refs:
        loc.iss.results.blobs[ref] = b"tampered"
    wk = loc.workers["kms"]
    wk.process()
    bodies = [json.loads(m["body"]) for m in wk.responses.msgs.values()]
    assert any(b["status"] == "REFUSED" and b["reason"] == "FRAME_DIGEST_MISMATCH" for b in bodies)
    assert rec["stage"] == "signing"


# ------------------------------------------------------------------------------------------------ IS-10
MAIN_TF = (Path(__file__).resolve().parents[1] / "infra" / "main.tf").read_text()


def policy_statements(name):
    block = re.search(r'data "aws_iam_policy_document" "%s" \{(.*?)\n\}' % name, MAIN_TF, re.S).group(1)
    out = []
    for st in re.findall(r"statement \{(.*?)\n  \}", block, re.S):
        actions = re.findall(r'"([a-z0-9]+:[A-Za-z*]+)"', st)
        resources = re.findall(r"/([a-z]+)/\*", st)
        out.append((actions, resources))
    return out


def grants(name, action, prefix):
    return any(action in a and prefix in r for a, r in policy_statements(name))


def test_IS10_iam_grants_only_the_object_actions_each_role_uses():
    assert grants("api", "s3:PutObject", "content") and grants("api", "s3:GetObject", "result")
    assert not grants("api", "s3:PutObject", "result") and not grants("api", "s3:DeleteObject", "result")
    assert grants("poller", "s3:GetObject", "config")
    for act in ("s3:PutObject", "s3:DeleteObject"):
        assert not grants("poller", act, "config") and not grants("api", act, "config")
    assert grants("signer", "s3:GetObject", "frames")
    assert not any(r for a, r in policy_statements("signer") if r != ["frames"])


# ------------------------------------------------------------------------------------------------ IS-11
def test_IS11_truncated_udp_answer_falls_back_to_tcp(monkeypatch):
    q = dns.make_query("wamason.com.", dns.T_DNSKEY, qid=7)
    rd = b"\x01\x01\x03\x0d" + b"k" * 64
    answer = b"\xc0\x0c" + struct.pack(">HHIH", dns.T_DNSKEY, 1, 300, len(rd)) + rd
    full = struct.pack(">HHHHHH", 7, 0x8180, 1, 1, 0, 0) + q[12:12 + len(dns.name_wire("wamason.com.")) + 4] + answer
    cut = bytearray(full[:-20])
    cut[2:4] = struct.pack(">H", 0x8380)                 # TC set, answer ends inside RDATA
    tcp_calls = []

    class Udp:
        def __init__(self, *a): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def settimeout(self, t): pass
        def sendto(self, data, addr): pass
        def recvfrom(self, n): return bytes(cut), ("192.0.2.1", 53)

    class Tcp:
        def __init__(self): self.buf = struct.pack(">H", len(full)) + full
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def sendall(self, data): pass
        def recv(self, n):
            out, self.buf = self.buf[:n], self.buf[n:]
            return out

    def connect(addr, timeout=None):
        tcp_calls.append(addr)
        return Tcp()
    monkeypatch.setattr(dns.socket, "socket", Udp)
    monkeypatch.setattr(dns.socket, "create_connection", connect)
    got = dns.udp_tcp_transport("192.0.2.1")(q)
    assert got == full and len(tcp_calls) == 1
    assert dns.parse_answers(got)[1][0][3] == rd


# ------------------------------------------------------------------------------------------------ store contracts
@pytest.mark.parametrize("kind", ["memory", "dynamo"])
def test_IS01_IS07_store_contract_for_used_log_records_and_cleanup_obligations(kind):
    from tessera_issue.stores import InMemoryRequestStore
    st = InMemoryRequestStore() if kind == "memory" else DynamoRequestStore(FakeDynamo(), "t")
    e = {"request_id": "req-1", "signature_sha256": "ab", "disposition": "used", "slot": "kms"}
    assert not st.siglog_has("req-1", "ab")
    st.siglog_add(dict(e, disposition="duplicate"))
    assert not st.siglog_has("req-1", "ab")
    st.siglog_add(e)
    st.siglog_add(e)                                     # append-only: a repeat is kept as its own entry
    assert st.siglog_has("req-1", "ab") and not st.siglog_has("req-1", "cd")
    assert len(st.siglog()) == 3
    st.cleanup_put("r1", {"rid": "r1", "end_done": False})
    st.cleanup_put("r1", {"rid": "r1", "end_done": True})
    st.cleanup_put("r2", {"rid": "r2", "end_done": False})
    assert sorted(st.cleanup_list()) == [("r1", {"rid": "r1", "end_done": True}),
                                         ("r2", {"rid": "r2", "end_done": False})]
    st.cleanup_done("r1")
    assert [r for r, _ in st.cleanup_list()] == ["r2"]
    st.create({"rid": "a", "state": "ACCEPTED", "stage": "frames", "expires_at": None}, 9)
    assert [r["rid"] for r in st.active()] == ["a"]      # cleanup items never appear as active requests
