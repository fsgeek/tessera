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


def at_assemble(loc, key, before=1):
    """-> (rid, deadline) with the request about to be assembled, the clock `before` seconds before its deadline."""
    _, rid = submit(loc, key)
    for _ in range(100):
        rec = loc.iss.requests.get(rid)
        if rec["stage"] == "assemble":
            break
        loc.tick()
    assert rec["stage"] == "assemble"
    deadline = rec["created_at"] + DEADLINE_S
    loc.clock.t = deadline - before
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
    t0 = WRITE_LEASE_S + 1                                   # CF2-01: decided before the last lease
    rid, deadline = at_assemble(loc, key, before=t0)
    store = loc.iss.requests
    real, seen = store.save, []

    def commit_then_slow(rec):
        ok = real(rec)
        if rec["state"] == "COMPLETE" and not seen:
            seen.append(None)
            seen[0] = api.status(loc.iss, "cred-A", key).body["state"]      # a client polls meanwhile
            loc.clock.advance(t0 + 1)
        return ok
    store.save = commit_then_slow
    pipeline.poll(loc.iss)
    store.save = real
    rec = store.get(rid)
    assert seen == ["COMPLETE"] and rec["state"] == "COMPLETE"
    assert rec["ended_at"] == deadline - t0 and rec["confirmed_at"] == deadline - t0
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


# ------------------------------------------------------------------------------------------------ CF2-01
# docs/reviews/issuer/CODEX-CONFIRM-2.md. A clock check before a write does not bound when the write commits; the
# writer lease does. A confirmation decided at least WRITE_LEASE_S before the deadline commits before it.
def test_CF2_01_confirmation_that_commits_late_never_reads_as_complete(loc, key):
    """Codex's reproduction: decided at deadline - 1, the confirmation write lands at deadline + 1."""
    rid, deadline = at_assemble(loc, key)
    store = loc.iss.requests
    real = store.save

    def slow_confirm(rec):
        if rec.get("confirmed_at") is not None:
            loc.clock.advance(2)
        return real(rec)
    store.save = slow_confirm
    pipeline.poll(loc.iss)
    store.save = real
    rec = store.get(rid)
    assert rec.get("confirmed_at") is None                   # inside the last lease nothing is confirmed
    loc.clock.t = max(loc.clock(), deadline)
    pipeline.poll(loc.iss)
    assert_failed_late(loc, key, rid, deadline)


def test_CF2_01_inside_the_last_lease_reads_as_accepted_until_the_deadline(loc, key):
    rid, deadline = at_assemble(loc, key, before=WRITE_LEASE_S)
    pipeline.poll(loc.iss)
    body = api.status(loc.iss, "cred-A", key).body
    assert body["state"] == "ACCEPTED" and "ended_at" not in body
    assert api.receipt(loc.iss, "cred-A", key).status == 409
    loc.clock.t = deadline
    pipeline.poll(loc.iss)
    assert_failed_late(loc, key, rid, deadline)


def test_CF2_01_a_confirmation_decided_before_the_last_lease_commits_before_the_deadline(loc, key):
    """The slowest a write can be is the lease: decided at deadline - lease - 1, it commits at deadline - 1."""
    rid, deadline = at_assemble(loc, key, before=WRITE_LEASE_S + 1)
    store = loc.iss.requests
    real, committed = store.save, []

    def slowest_confirm(rec):
        if rec.get("confirmed_at") is not None and not committed:
            loc.clock.advance(WRITE_LEASE_S)
            committed.append(loc.clock())
        return real(rec)
    store.save = slowest_confirm
    pipeline.poll(loc.iss)
    store.save = real
    rec = store.get(rid)
    assert rec["state"] == "COMPLETE" and committed and committed[0] < deadline
    assert api.receipt(loc.iss, "cred-A", key).status == 303


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


# ------------------------------------------------------------------------------------------------ CF2-02
def test_CF2_02_no_url_is_minted_after_expiry_even_if_the_record_read_is_slow(key):
    """Codex's reproduction: the clock was read before the record, so a slow read carried minting past expiry."""
    loc = s3_loc()
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    expiry = rec["ended_at"] + RETENTION_S
    loc.clock.t = expiry - 1
    real, calls = loc.iss.requests.get, []

    def slow(r):
        calls.append(r)
        if len(calls) == 2:                                  # the read just before minting
            loc.clock.advance(2)
        return real(r)
    loc.iss.requests.get = slow
    minted, presign = [], loc.iss.results.presign
    loc.iss.results.presign = lambda *a: minted.append(a) or presign(*a)
    assert api.receipt(loc.iss, "cred-A", key).status == 410
    assert not minted


# ------------------------------------------------------------------------------------------------ CF3
# docs/reviews/issuer/CODEX-CONFIRM-3.md. Clock readings are taken after the reads they decide on (CF3-02 read half,
# CF3-03). What a client cannot bound, the remote commit time of a write, is the stated tolerance in
# docs/decisions/2026-10-27-service-clock-tolerance.md; the client's own time is bounded by the botocore config.
def test_CF3_02_a_slow_admission_read_cannot_admit_after_acceptance_closes(key):
    loc = local.build(FROZEN)
    loc.clock.t = loc.iss.window.accept_until - 1
    real = loc.iss.requests.get

    def slow(rid):
        loc.clock.advance(2)
        return real(rid)
    loc.iss.requests.get = slow
    r = api.submit(loc.iss, "cred-A", key, b"TEST content")
    assert r.body["state"] == "REFUSED" and r.body["reason"] == "OUTSIDE_WINDOW", r.body


def test_CF3_03_a_slow_repeat_read_cannot_report_an_expired_request_as_complete(key):
    loc = local.build(FROZEN)
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    real = loc.iss.requests.get

    def slow(r):
        loc.clock.advance(2)
        return real(r)
    loc.iss.requests.get = slow
    r = api.submit(loc.iss, "cred-A", key, b"TEST content")
    assert r.status == 410 and r.body["state"] == "EXPIRED", (r.status, r.body)


def test_CF3_01_aws_client_time_is_bounded_well_inside_the_writer_lease():
    from tessera_issue.lambda_app import AWS_CLIENT_CONFIG as c
    attempts = c["retries"]["total_max_attempts"]
    worst = attempts * (c["connect_timeout"] + c["read_timeout"]) + attempts * 20  # standard backoff caps at 20 s
    assert c["retries"]["mode"] == "standard" and worst < WRITE_LEASE_S / 3, worst
