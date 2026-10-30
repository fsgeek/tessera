"""Regression tests for the Codex confirmation review (docs/reviews/issuer/CODEX-CONFIRM.md, CF-01..CF-04; CF-05 is
the strengthened IS-05 test in test_review_fixes.py). Races are driven by a controllable clock and by hooks that
interleave a concurrent actor at a chosen point; nothing sleeps.

The CF-01 and CF2-01 tests encoded the withdrawn 24-hour rule (S4's FAILED NOT_COMPLETE_WITHIN_24H, settled by
api.settle). They are rewritten against the registered lifecycle (docs/decisions/2026-10-29-issuance-lifecycle.md):
CF-01 now checks that completion is one guarded terminal write with no deadline to cross and no unconfirmed state;
CF2-01's become latch and expiry serialization tests (A2.1: the boundary is inclusive and latch-winning; expiry only
on complete negative evidence strictly after B)."""
import re
import uuid
from pathlib import Path

import pytest

from tessera_issue import api, local, pipeline
from tessera_issue.aws import S3ResultStore
from tessera_issue.lifecycle import B_of, current
from tessera_issue.service import RETENTION_S, WRITE_LEASE_S
from tessera_issue.util import DELTA, HOUR, ts

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


def at_finalize(loc, key):
    """-> rid, with the request latched and about to be finalized (assembled, checked, shipped)."""
    _, rid = submit(loc, key)
    for _ in range(100):
        rec = loc.iss.requests.get(rid)
        if rec["stage"] == "finalize":
            return rid
        loc.tick()
    raise AssertionError("finalize not reached")


def assert_complete(loc, key, rid, not_before):
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "COMPLETE" and rec["reason"] is None, (rec["state"], rec["reason"])
    assert rec["ended_at"] >= not_before                     # never backdated
    assert api.status(loc.iss, "cred-A", key).body["state"] == "COMPLETE"
    assert api.receipt(loc.iss, "cred-A", key).status == 303


# ------------------------------------------------------------------------------------------------ CF-01
def test_CF01_a_slow_cleanup_obligation_write_delays_but_never_fails_a_completion(loc, key):
    """Rewritten (was: ..._cannot_carry_completion_past_the_deadline). No deadline exists; ended_at is read after the
    obligation is durable, so it is never earlier than the obligation write."""
    rid = at_finalize(loc, key)
    loc.clock.t = loc.iss.requests.get(rid)["created_at"] + 24 * HOUR - 1     # the withdrawn deadline is irrelevant
    store = loc.iss.requests
    real = store.cleanup_put

    def slow(r, doc):                                        # persisting the obligation takes two seconds
        loc.clock.advance(2)
        return real(r, doc)
    store.cleanup_put = slow
    t0 = loc.clock()
    pipeline.poll(loc.iss)
    store.cleanup_put = real
    assert_complete(loc, key, rid, t0 + 2)


def test_CF01_a_slow_terminal_write_still_completes(loc, key):
    """Rewritten (was: ..._slow_terminal_write_cannot_carry_completion_past_the_deadline)."""
    rid = at_finalize(loc, key)
    store = loc.iss.requests
    real, delayed = store.save, []

    def slow(rec, expect=None):                              # the COMPLETE write lands two seconds later
        if rec["state"] == "COMPLETE" and not delayed:
            delayed.append(1)
            loc.clock.advance(2)
        return real(rec, expect)
    store.save = slow
    t0 = loc.clock()
    pipeline.poll(loc.iss)
    store.save = real
    assert delayed
    assert_complete(loc, key, rid, t0)


def test_CF01_a_completion_a_client_saw_stays_complete(loc, key):
    """The COMPLETE write lands and a client sees it; the writer only gets its answer much later. The view stays
    COMPLETE (no flip), and there is no unconfirmed COMPLETE state to settle."""
    rid = at_finalize(loc, key)
    store = loc.iss.requests
    real, seen = store.save, []

    def commit_then_slow(rec, expect=None):
        ok = real(rec, expect)
        if rec["state"] == "COMPLETE" and not seen:
            seen.append(api.status(loc.iss, "cred-A", key).body["state"])      # a client polls meanwhile
            loc.clock.advance(2 * 24 * HOUR)
        return ok
    store.save = commit_then_slow
    t0 = loc.clock()
    pipeline.poll(loc.iss)
    store.save = real
    assert seen == ["COMPLETE"]
    assert_complete(loc, key, rid, t0)
    assert "confirmed_at" not in store.get(rid)


def test_CF01_a_completion_whose_invocation_dies_after_the_commit_is_complete_and_cleaned(loc, key):
    """Rewritten (was: ..._unconfirmed_completion_left_by_a_crash_is_settled): the commit IS the completion; the
    cleanup obligation, durable before it, finishes the deletion on the next poll."""
    rid = at_finalize(loc, key)
    store = loc.iss.requests
    real = store.save

    def crash(rec, expect=None):                             # the COMPLETE write lands; the invocation then dies
        ok = real(rec, expect)
        if rec["state"] == "COMPLETE":
            store.save = real
            raise LambdaTimeout()
        return ok
    store.save = crash
    t0 = loc.clock()
    with pytest.raises(LambdaTimeout):
        pipeline.poll(loc.iss)
    assert blobs(loc, rid, "work")                            # killed before its own cleanup
    assert_complete(loc, key, rid, t0)
    pipeline.poll(loc.iss)
    assert not blobs(loc, rid, "work") and not blobs(loc, rid, "content") and blobs(loc, rid, "result")


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
        if "/sig-" in name:                                  # the consumer has read the record as waiting
            res.put = real
            rec = store.get(r)
            loc.clock.t = loc.iss.window.sign_until + 1      # (was: the 24 h deadline) signing stops meanwhile:
            pipeline.advance(loc.iss, rec)                   # the request ends (SIGNING_CLOSED) and is cleaned up
        return real(ns, r, name, data)
    res.put = late
    pipeline.drain(loc.iss)
    assert store.get(rid)["state"] == "REFUSED"
    assert [n for n in res.names("work", rid) if "/sig-" in n]
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
# Rewritten against the registered lifecycle. CF2-01 confirmed a completion only if decided WRITE_LEASE_S before the
# 24 h deadline; that cutoff contradicted A2.1 (IL-02) and is withdrawn with the deadline. These are now latch and
# expiry serialization tests: eligibility observed at B is timely however late its latch commits, and nothing but
# complete negative evidence after B expires an attempt.
def _at_evidence(loc, key):
    _, rid = submit(loc, key)
    for _ in range(10):
        rec = loc.iss.requests.get(rid)
        if rec["stage"] == "evidence":
            return rid, current(rec)
        loc.tick(mine=False)
    raise AssertionError("evidence not reached")


def _bury_timely(loc, a):
    t = ts(a["declared_issue_time"]) + DELTA - HOUR
    loc.clock.t = t
    loc.world.chain.mine(6)


def test_CF2_01_a_latch_observed_at_B_whose_write_commits_after_B_holds(loc, key):
    rid, a = _at_evidence(loc, key)
    _bury_timely(loc, a)
    loc.clock.t = B_of(a)
    store = loc.iss.requests
    real = store.save

    def slow_latch(rec, expect=None):
        if current(rec)["state"] == "latched":
            loc.clock.advance(WRITE_LEASE_S + 60)            # the latch lands well after B
        return real(rec, expect)
    store.save = slow_latch
    pipeline.poll(loc.iss)
    store.save = real
    rec = store.get(rid)
    assert current(rec)["state"] == "latched" and current(rec)["latch"]["observed_at"] == B_of(a)
    pipeline.poll(loc.iss)
    assert store.get(rid)["state"] == "COMPLETE" and len(store.get(rid)["attempts"]) == 1


def test_CF2_01_a_stale_fetch_after_B_cannot_expire_a_timely_observation(loc, key):
    """ILC-01's decisive schedule: L observes eligibility at B and is killed before its latch; E reads the attempt
    after B and its fetch is stale (pending). E must not expire it; the next poll latches."""
    rid, a = _at_evidence(loc, key)
    _bury_timely(loc, a)
    loc.clock.t = B_of(a)
    store = loc.iss.requests
    real = store.save

    def killed_latch(rec, expect=None):
        if current(rec)["state"] == "latched":
            store.save = real
            raise LambdaTimeout()
        return real(rec, expect)
    store.save = killed_latch
    with pytest.raises(LambdaTimeout):
        pipeline.poll(loc.iss)                               # L
    cal = loc.iss.calendars[0]
    loc.iss.results.put("work", rid, "a1/receipt.upgraded.ots", loc.iss.results.get("work", rid, "a1/receipt.ots"))
    real_fetch, cal.fetch = cal.fetch, (lambda m: None)      # E's sources answer stale
    loc.clock.t = B_of(a) + 3600
    pipeline.poll(loc.iss)                                   # E
    rec = store.get(rid)
    assert current(rec)["state"] == "open" and rec["cur"] == 1 and current(rec)["failed_intervals"]
    cal.fetch = real_fetch
    pipeline.poll(loc.iss)
    assert current(store.get(rid))["state"] == "latched"


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
