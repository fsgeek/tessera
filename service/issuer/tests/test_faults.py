"""Fault tests (DESIGN.md test group 3): a signer timeout followed by a late answer (E-02); a lost API response
followed by lookup by key; stalls (formerly "the 24 h failure", rewritten against the registered lifecycle: there is
no request deadline); the stop margin."""
import json

from tessera_issue import api, pipeline
from tessera_issue.lifecycle import B_of, current
from tessera_issue.util import HOUR, rfc3339, sha256hex, ts

from helpers import fetch_receipt, submit


def held(worker):
    """Stop a stand-in signer from answering; returns the real process function."""
    real = worker.process
    worker.process = lambda limit=None: 0
    return real


# ------------------------------------------------------------------------------------------------ E-02
def test_signer_timeout_then_late_answer_is_logged_and_used_once(loc, key):
    _, rid = submit(loc, key, b"late answer")
    kms = loc.workers["kms"]
    real = held(kms)
    for _ in range(5):                                   # 50 min: past the 30 min re-send point
        loc.tick()
    rec = loc.iss.requests.get(rid)
    jobs = current(rec)["jobs"]
    assert rec["stage"] == "signing"
    assert jobs["s_kms"]["attempts"] == 2 and jobs["p_kms"]["attempts"] == 2
    assert len(kms.requests) == 4                        # two attempts per kms job, all with the same two ids
    ids = {json.loads(m["body"])["request_id"] for m in kms.requests.msgs.values()}
    assert ids == {jobs["s_kms"]["request_id"], jobs["p_kms"]["request_id"]}
    kms.process = real
    kms.process()                                        # the late first answers and the retries all arrive
    assert len(kms.signed) == 4 and len({s for _, _, s in kms.signed}) == 4   # ML-DSA signing is randomized
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    log = loc.iss.requests.siglog()
    kms_log = [e for e in log if e["slot"] == "kms"]
    assert sorted(e["disposition"] for e in kms_log) == ["duplicate", "duplicate", "used", "used"]
    for e in kms_log:                                    # recorded with frame and signature hashes, used or not
        assert e["frame_sha256"] and e["signature_sha256"]
    assert {s for _, _, s in kms.signed} <= {e["signature_sha256"] for e in log}   # no signature leaves unlogged
    assert len(kms.responses) == 0                        # recorded, then deleted
    used = {e["request_id"]: e["signature_sha256"] for e in kms_log if e["disposition"] == "used"}
    jobs = current(rec)["jobs"]
    assert used[jobs["s_kms"]["request_id"]] == jobs["s_kms"]["sig_sha256"]


def test_answer_after_the_request_moved_on_and_unrequested_answers_are_logged_then_deleted(loc, key):
    _, rid = submit(loc, key, b"stray answers")
    kms = loc.workers["kms"]
    real = held(kms)
    for _ in range(4):
        loc.tick()                                       # one re-send per kms job queued
    kms.process = real
    kms.process(limit=2)                                 # first attempts answered; the retries stay queued
    loc.workers["gpg"].process()
    rec = loc.run_until_done(rid, run_signers=False)
    assert rec["state"] == "COMPLETE"
    kms.responses.send(json.dumps({"request_id": "req-from-an-earlier-run", "status": "SIGNED",
                                   "sig_b64": "AAAA"}))  # like real-1's orphan: nobody here asked for it
    kms.process()                                        # the retries are answered after completion
    pipeline.drain(loc.iss)
    kms_log = [e for e in loc.iss.requests.siglog() if e["slot"] == "kms"]
    assert sorted(e["disposition"] for e in kms_log) == ["not-waiting", "not-waiting", "unrequested", "used", "used"]
    stray = [e for e in kms_log if e["disposition"] == "unrequested"][0]
    assert stray["signature_sha256"] == sha256hex(b"\x00\x00\x00") and stray["frame_sha256"] is None
    assert len(kms.responses) == 0


def test_a_failed_enqueue_is_resent_with_the_same_id(loc, key):
    _, rid = submit(loc, key)
    q = loc.iss.signers["gpg"].requests
    real_send, calls = q.send, []

    def flaky(body):
        calls.append(json.loads(body)["request_id"])
        if len(calls) <= 2:
            raise OSError("queue unavailable")
        return real_send(body)
    q.send = flaky
    loc.tick()                                           # the poller notes the error and carries on
    assert any("OSError" in n for n in loc.iss.log)
    rec = loc.iss.requests.get(rid)
    assert rec["stage"] == "signing"                     # durable before sending; nothing signed yet
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    assert calls[0] == current(rec)["jobs"]["s_gpg"]["request_id"] and calls[0] in calls[2:]


def test_complete_signature_set_is_reused_not_resigned(loc, key):
    _, rid = submit(loc, key)
    loc.tick()
    loc.tick()                                           # all four answered and A_sig built
    rec = loc.iss.requests.get(rid)
    assert rec["stage"] == "stamp"
    n = {s: len(w.signed) for s, w in loc.workers.items()}
    rec["stage"] = "signing"                             # e.g. a poller crash before the stage change was saved
    loc.iss.requests.save(rec)
    assert loc.run_until_done(rid)["state"] == "COMPLETE"
    assert {s: len(w.signed) for s, w in loc.workers.items()} == n


# ------------------------------------------------------------------------------------------------ lost API response
def test_lost_api_response_then_lookup_by_key(loc, key):
    submit(loc, key, b"the response was lost in transit")      # the client never sees this answer
    r = api.status(loc.iss, "cred-A", key)
    assert r.status == 200 and r.body["state"] == "ACCEPTED"   # acceptance was durable
    r2, rid = submit(loc, key, b"the response was lost in transit")
    assert r2.status == 202 and len(loc.iss.requests.recs) == 1
    rec = loc.run_until_done(rid)
    first, again = fetch_receipt(loc, key)[0], fetch_receipt(loc, key)[0]
    assert first == again
    assert sha256hex(first) == api.status(loc.iss, "cred-A", key).body["receipt_sha256"] == rec["receipt_sha256"]


def test_lost_response_for_a_refusal_then_lookup(loc, key):
    loc.iss.closing = True
    submit(loc, key)
    loc.iss.closing = False
    assert api.status(loc.iss, "cred-A", key).body["state"] == "REFUSED"


# ------------------------------------------------------------------------------------------------ stalls
def test_stalled_signers_never_fail_the_request_by_age_only_the_signing_stop_ends_it(loc, key):
    """Rewritten against the registered lifecycle (formerly test_not_complete_within_24h_fails_and_is_never_shipped,
    stall "signers"): the 24-hour FAILED rule contradicted A2 and is withdrawn. An attempt that still needs signing
    stays open, however long; only the window's signing stop ends it, and then the request is REFUSED SIGNING_CLOSED
    (design step 8) - never shipped, nothing left behind."""
    _, rid = submit(loc, key)
    created = loc.iss.requests.get(rid)["created_at"]
    real = {s: held(w) for s, w in loc.workers.items()}
    while loc.clock() < created + 3 * 24 * HOUR:
        loc.tick()
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "ACCEPTED" and rec["stage"] == "signing" and rec["cur"] == 1
    loc.clock.t = loc.iss.window.sign_until + 1
    pipeline.poll(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED"
    assert current(rec)["state"] == "discarded" and current(rec)["end"]["reason"] == "SIGNING_CLOSED"
    for s, w in loc.workers.items():                     # late answers change nothing
        w.process = real[s]
        w.process()
    for _ in range(3):
        loc.tick()
    assert loc.iss.requests.get(rid)["state"] == "REFUSED"
    assert not [k for k in loc.iss.results.blobs if k[1] == rid]
    assert api.receipt(loc.iss, "cred-A", key).status == 409


def test_a_stalled_chain_never_fails_the_request_and_a_late_confirmation_still_ships(loc, key):
    """Rewritten against the registered lifecycle (formerly the 24 h test, stall "chain"): no block is mined for
    longer than B = declared + delta + S. Pending evidence is never a negative, so the attempt stays open (design
    step 4; step 5's ending is gated). When the stamp is finally mined, its T is late: complete negative evidence after
    B expires attempt 1 and allocates attempt 2, which then ships."""
    _, rid = submit(loc, key)
    for _ in range(4):
        loc.tick(mine=False)
    rec = loc.iss.requests.get(rid)
    a1 = current(rec)
    assert rec["stage"] == "evidence"
    loc.clock.t = B_of(a1) + 2 * 24 * HOUR
    for _ in range(3):
        loc.tick(mine=False)
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "ACCEPTED" and rec["cur"] == 1 and current(rec)["state"] == "open"
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and rec["cur"] == 2
    assert rec["attempts"][0]["state"] == "expired" and rec["attempts"][0]["end"]["reason"] == "TIME_AFTER_DECLARED_DELTA"
    assert rec["attempts"][1]["state"] == "shipped"
    assert api.receipt(loc.iss, "cred-A", key).status == 303


# ------------------------------------------------------------------------------------------------ stop margin
def test_acceptance_stops_120h_and_requests_accepted_at_the_cutoff_finish_before_signing_stops(loc):
    w = loc.iss.window
    loc.clock.t = w.accept_until
    import uuid
    k_in, k_late = str(uuid.uuid4()), str(uuid.uuid4())
    _, rid = submit(loc, k_in)
    loc.clock.t = w.accept_until + 1
    assert submit(loc, k_late)[0].body["reason"] == "OUTSIDE_WINDOW"
    loc.clock.t = w.accept_until
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    assert ts(current(rec)["declared_issue_time"]) <= w.sign_until and ts(rec["T"]) <= w.na


def test_a_request_accepted_at_the_cutoff_whose_signers_are_late_is_refused_at_the_signing_stop(loc, key):
    """Rewritten against the registered lifecycle (it accepted FAILED NOT_COMPLETE_WITHIN_24H or SIGNING_STOPPED):
    the attempt still needs signing when signing stops, so the request is REFUSED SIGNING_CLOSED (design step 8)."""
    w = loc.iss.window
    loc.clock.t = w.accept_until
    _, rid = submit(loc, key)
    held(loc.workers["gpg"])
    rec = loc.run_until_done(rid, max_ticks=1000)          # L1: the signing stop is now 120 h after acceptance stops
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED"
    assert w.sign_until < rec["ended_at"] <= w.sign_until + 600


def test_frames_after_the_signing_stop_refuse_signing_closed(loc, key):
    """Rewritten against the registered lifecycle (formerly FAILED SIGNING_STOPPED): a skewed clock can reach the
    signing stop before attempt 1 is started; a new attempt would need signing after the stop, so the request is
    REFUSED SIGNING_CLOSED and nothing is sent for signing."""
    _, rid = submit(loc, key)
    loc.clock.t = loc.iss.window.sign_until + 1
    pipeline.poll(loc.iss)
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED" and rec["attempts"] == []
    assert not loc.workers["kms"].requests.msgs                # nothing was sent for signing
