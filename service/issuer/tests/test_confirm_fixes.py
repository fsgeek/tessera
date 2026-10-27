"""Regression tests for the Codex confirmation review (docs/reviews/issuer/CODEX-CONFIRM.md, CF-01..CF-04; CF-05 is
the strengthened IS-05 test in test_review_fixes.py). Races are driven by a controllable clock and by hooks that
interleave a concurrent actor at a chosen point; nothing sleeps."""
import re
import uuid
from pathlib import Path

import pytest

from tessera_issue import api, local, pipeline
from tessera_issue.aws import S3ResultStore
from tessera_issue.service import DEADLINE_S, RETENTION_S, WRITE_LEASE_S

from conftest import FROZEN
from fakes import FakeS3
from helpers import submit


class LambdaTimeout(BaseException):
    """The invocation is killed: nothing in the issuer can catch it."""


def blobs(loc, rid, ns=None):
    res = loc.iss.results
    if isinstance(res, S3ResultStore):
        return [k for b, k in res.c.objects if k.split("/")[1] == rid and (ns is None or k.startswith(ns + "/"))]
    return [k for k in res.blobs if k[1] == rid and (ns is None or k[0] == ns)]


def s3_loc():
    loc = local.build(FROZEN)
    loc.iss.results = S3ResultStore(FakeS3(), "bucket")
    loc.workers["kms"].fetch = loc.workers["gpg"].fetch = loc.iss.results.get_ref
    return loc


def at_assemble(loc, key):
    """-> (rid, deadline) with the request about to be assembled, the clock one second before its deadline."""
    _, rid = submit(loc, key)
    for _ in range(100):
        rec = loc.iss.requests.get(rid)
        if rec["stage"] == "assemble":
            break
        loc.tick()
    assert rec["stage"] == "assemble"
    deadline = rec["created_at"] + DEADLINE_S
    loc.clock.t = deadline - 1
    return rid, deadline


def assert_failed_late(loc, key, rid, deadline):
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "FAILED" and rec["reason"] == "NOT_COMPLETE_WITHIN_24H", (rec["state"], rec["reason"])
    assert rec["ended_at"] >= deadline                       # never backdated
    assert api.status(loc.iss, "cred-A", key).body["state"] == "FAILED"
    assert api.receipt(loc.iss, "cred-A", key).status == 409
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid, "result")


# ------------------------------------------------------------------------------------------------ CF-01
def test_CF01_slow_cleanup_obligation_write_cannot_carry_completion_past_the_deadline(loc, key):
    rid, deadline = at_assemble(loc, key)
    store = loc.iss.requests
    real = store.cleanup_put

    def slow(r, doc):                                        # persisting the obligation takes two seconds
        loc.clock.advance(2)
        return real(r, doc)
    store.cleanup_put = slow
    pipeline.poll(loc.iss)
    store.cleanup_put = real
    assert_failed_late(loc, key, rid, deadline)


def test_CF01_slow_terminal_write_cannot_carry_completion_past_the_deadline(loc, key):
    rid, deadline = at_assemble(loc, key)
    store = loc.iss.requests
    real, delayed = store.save, []

    def slow(rec):                                           # the COMPLETE write lands two seconds later
        if rec["state"] == "COMPLETE" and not delayed:
            delayed.append(1)
            loc.clock.advance(2)
        return real(rec)
    store.save = slow
    pipeline.poll(loc.iss)
    store.save = real
    assert delayed
    assert_failed_late(loc, key, rid, deadline)


def test_CF01_completion_seen_before_the_deadline_never_turns_into_failed(loc, key):
    """The COMPLETE write lands before the deadline and a client sees it; the writer only gets the answer after
    the deadline. The client's view must stay COMPLETE (no flip), with ended_at no earlier than the commit."""
    rid, deadline = at_assemble(loc, key)
    store = loc.iss.requests
    real, seen = store.save, []

    def commit_then_slow(rec):
        ok = real(rec)
        if rec["state"] == "COMPLETE" and not seen:
            seen.append(None)
            seen[0] = api.status(loc.iss, "cred-A", key).body["state"]      # a client polls meanwhile
            loc.clock.advance(2)
        return ok
    store.save = commit_then_slow
    pipeline.poll(loc.iss)
    store.save = real
    rec = store.get(rid)
    assert seen == ["COMPLETE"] and rec["state"] == "COMPLETE"
    assert rec["ended_at"] == deadline - 1 and rec["confirmed_at"] == deadline - 1
    assert api.receipt(loc.iss, "cred-A", key).status == 303


def test_CF01_unconfirmed_completion_left_by_a_crash_is_settled(loc, key):
    rid, deadline = at_assemble(loc, key)
    store = loc.iss.requests
    real = store.save

    def crash(rec):                                          # the COMPLETE write lands; the invocation then dies
        ok = real(rec)
        if rec["state"] == "COMPLETE":
            store.save = real
            raise LambdaTimeout()
        return ok
    store.save = crash
    with pytest.raises(LambdaTimeout):
        pipeline.poll(loc.iss)
    rec = store.get(rid)
    assert rec["state"] == "COMPLETE" and rec.get("confirmed_at") is None
    assert api.view(rec, loc.clock())["state"] == "ACCEPTED"      # not reported COMPLETE while unconfirmed
    loc.clock.t = deadline                                       # nobody saw it before the deadline
    pipeline.poll(loc.iss)                                       # the cleanup obligation settles it
    assert_failed_late(loc, key, rid, deadline)


# ------------------------------------------------------------------------------------------------ CF-02
def test_CF02_upload_that_commits_after_the_end_is_still_deleted(loc, key):
    store, res = loc.iss.requests, loc.iss.results
    real = res.put
    res.put = lambda *a: (_ for _ in ()).throw(OSError("upload interrupted"))
    with pytest.raises(OSError):
        submit(loc, key, b"late upload")
    rid = api.record_id("cred-A", key)
    loc.clock.advance(pipeline.UPLOAD_GRACE_S)

    def late(ns, r, name, data):                             # the retry's S3 write overlaps the 15-minute failure
        res.put = real
        pipeline.poll(loc.iss)                               # the poller fails the upload and cleans up first
        real(ns, r, name, data)                              # then the write commits ...
        raise OSError("connection reset")                    # ... and its caller sees only an error
    res.put = late
    with pytest.raises(OSError):
        submit(loc, key, b"late upload")
    assert store.get(rid)["state"] == "FAILED" and blobs(loc, rid, "content")
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid)
    assert [r for r, _ in store.cleanup_list()] == [rid]     # kept while a writer may still be running
    loc.clock.advance(WRITE_LEASE_S)
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid) and store.cleanup_list() == []


def test_CF02_signature_written_after_termination_is_still_deleted(loc, key):
    store, res = loc.iss.requests, loc.iss.results
    _, rid = submit(loc, key)
    pipeline.poll(loc.iss)
    for w in loc.workers.values():
        w.process()
    real = res.put

    def late(ns, r, name, data):
        if name.startswith("sig-"):                          # the consumer has read the record as waiting
            res.put = real
            rec = store.get(r)
            loc.clock.t = rec["created_at"] + DEADLINE_S
            pipeline.advance(loc.iss, rec)                   # concurrently the request ends and is cleaned up
        return real(ns, r, name, data)
    res.put = late
    pipeline.drain(loc.iss)
    assert store.get(rid)["state"] == "FAILED"
    assert [n for n in res.names("work", rid) if n.startswith("sig-")]
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid)
    loc.clock.advance(WRITE_LEASE_S)
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid) and store.cleanup_list() == []


def test_CF02_write_lease_covers_every_lambda_timeout():
    tf = (Path(__file__).resolve().parents[1] / "infra" / "main.tf").read_text()
    timeouts = [int(t) for t in re.findall(r"^\s*timeout\s*=\s*(\d+)", tf, re.M)]
    assert timeouts and max(timeouts) <= WRITE_LEASE_S


# ------------------------------------------------------------------------------------------------ CF-03
def test_CF03_no_url_is_minted_after_expiry_even_if_the_object_check_is_slow(key):
    loc = s3_loc()
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    s3 = loc.iss.results.c
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    real = s3.head_object

    def slow(**kw):                                          # the object check takes two seconds
        loc.clock.advance(2)
        return real(**kw)
    s3.head_object = slow
    r = api.receipt(loc.iss, "cred-A", key)
    assert r.status == 410 and r.body["state"] == "EXPIRED"
    assert not getattr(s3, "presigned", [])
    assert api.status(loc.iss, "cred-A", key).body["state"] == "EXPIRED"


# ------------------------------------------------------------------------------------------------ CF-04
def bounded(s3, limit):
    """Each poll is one Lambda invocation: past `limit` DeleteObjects calls it is killed."""
    real, calls = s3.delete_objects, [0]

    def call(**kw):
        calls[0] += 1
        if calls[0] > limit:
            raise LambdaTimeout()
        return real(**kw)
    s3.delete_objects = call
    return calls


def test_CF04_s3_delete_reports_per_object_errors_and_is_bounded():
    s3 = FakeS3()
    st = S3ResultStore(s3, "b")
    st.put("content", "r", "a", b"1")
    st.put("content", "r", "b", b"2")
    s3.fail_delete = lambda k: "InternalError" if k.endswith("/a") else None
    calls = bounded(s3, 50)
    with pytest.raises(OSError, match="InternalError"):
        st.delete("content", "r")
    assert calls[0] == 1 and st.names("content", "r") == ["a"]
    s3.fail_delete = lambda k: None
    for i in range(5000):                                    # more pages than one call may work through
        s3.objects[("b", f"work/r/{i:05}")] = b""
    calls[0] = 0
    with pytest.raises(OSError, match="rounds"):
        st.delete("work", "r")
    assert calls[0] == S3ResultStore.DELETE_ROUNDS


def test_CF04_one_failing_deletion_does_not_starve_other_cleanups(key):
    loc = s3_loc()
    s3, store = loc.iss.results.c, loc.iss.requests
    _, r1 = submit(loc, key, b"one")
    _, r2 = submit(loc, str(uuid.uuid4()), b"two")
    s3.fail_delete = lambda k: "InternalError" if k.startswith(f"content/{r1}/") else None
    calls = bounded(s3, 50)
    for _ in range(100):                                     # both requests complete; r1's content will not delete
        calls[0] = 0
        loc.tick()
        if store.get(r1)["state"] != "ACCEPTED" and store.get(r2)["state"] != "ACCEPTED":
            break
    assert store.get(r1)["state"] == store.get(r2)["state"] == "COMPLETE"
    loc.clock.advance(WRITE_LEASE_S)
    calls[0] = 0
    pipeline.poll(loc.iss)
    assert blobs(loc, r1, "content") and not blobs(loc, r2, "content") and not blobs(loc, r2, "work")
    assert {r: d.get("end_done") for r, d in store.cleanup_list()} == {r1: False, r2: True}
    assert any("InternalError" in line for line in loc.iss.log)
    s3.fail_delete = lambda k: None                           # the fault clears: the kept obligation finishes
    calls[0] = 0
    pipeline.poll(loc.iss)
    assert not blobs(loc, r1, "content") and not blobs(loc, r1, "work")
