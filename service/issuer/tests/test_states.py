"""Unit tests for every client-visible state transition (DESIGN.md test group 1), including duplicate keys and
key/content mismatch. States: ACCEPTED -> COMPLETE | REFUSED (ATTEMPTS_EXHAUSTED, SIGNING_CLOSED) | FAILED (an upload
never finished, before any attempt); REFUSED at submission; any ended state -> EXPIRED 30 days after it ended
(V1-SERVICE-RESOLUTIONS S3-S6, L1; the attempt lifecycle of docs/decisions/2026-10-29-issuance-lifecycle.md)."""
import uuid

import pytest

from tessera_issue import api, pipeline
from tessera_issue.service import RETENTION_S
from tessera_issue.util import DAY, HOUR, MIB, sha256hex

from helpers import fetch_receipt, submit


def view(loc, key, cred="cred-A"):
    return api.status(loc.iss, cred, key)


# ------------------------------------------------------------------------------------------------ submission
def test_accept_creates_request_stores_content_and_tombstone(loc, key):
    r, rid = submit(loc, key, b"abc")
    assert r.status == 202 and r.body["state"] == "ACCEPTED" and r.body["request_key"] == key
    rec = loc.iss.requests.get(rid)
    assert rec["stage"] == "frames" and rec["content_sha256"] == sha256hex(b"abc")
    assert loc.iss.results.get("content", rid, api.content_name(sha256hex(b"abc"))) == b"abc"
    assert loc.iss.requests.tombstone_get(rid) is not None


def test_same_key_same_content_is_the_same_request(loc, key):
    r1, rid = submit(loc, key, b"abc")
    loc.clock.advance(60)
    r2, _ = submit(loc, key, b"abc")
    assert r2.status == 202 and r2.body == view(loc, key).body
    assert r2.body["accepted_at"] == r1.body["accepted_at"]
    assert len(loc.iss.requests.recs) == 1


def test_same_key_different_content_is_409(loc, key):
    submit(loc, key, b"abc")
    r, _ = submit(loc, key, b"abd")
    assert r.status == 409 and r.body["error"] == "KEY_CONTENT_MISMATCH"
    assert view(loc, key).body["state"] == "ACCEPTED"


def test_key_is_case_insensitive_uuid(loc, key):
    submit(loc, key, b"abc")
    r, _ = submit(loc, key.upper(), b"abc")
    assert r.status == 202 and r.body["request_key"] == key
    assert len(loc.iss.requests.recs) == 1


@pytest.mark.parametrize("bad", [None, "", "not-a-uuid", "1234", str(uuid.uuid4()) + "x"])
def test_bad_request_key_is_refused_and_not_stored(loc, bad):
    r = api.submit(loc.iss, "cred-A", bad, b"abc")
    assert r.status == 400 and r.body == {"state": "REFUSED", "reason": "BAD_REQUEST",
                                          "detail": "header Tessera-Request-Key must be a UUID"}
    assert not loc.iss.requests.recs and not loc.iss.results.blobs


def test_missing_credential_is_401(loc, key):
    assert api.submit(loc.iss, None, key, b"abc").status == 401
    assert api.status(loc.iss, "", key).status == 401


def test_too_large_is_refused_and_content_not_stored(loc, key):
    r, rid = submit(loc, key, b"x" * (MIB + 1))
    assert r.status == 413 and r.body["state"] == "REFUSED" and r.body["reason"] == "TOO_LARGE"
    assert not loc.iss.results.blobs
    r2, _ = submit(loc, str(uuid.uuid4()), b"x" * MIB)
    assert r2.status == 202


def test_outside_window_before_opening_and_after_acceptance_cutoff(loc):
    w = loc.iss.window
    loc.clock.t = w.nb - 1
    assert submit(loc, str(uuid.uuid4()))[0].body["reason"] == "OUTSIDE_WINDOW"
    loc.clock.t = w.nb
    assert submit(loc, str(uuid.uuid4()))[0].status == 202
    loc.clock.t = w.accept_until
    assert submit(loc, str(uuid.uuid4()))[0].status == 202
    loc.clock.t = w.accept_until + 1
    r = submit(loc, str(uuid.uuid4()))[0]
    assert r.status == 403 and r.body["reason"] == "OUTSIDE_WINDOW"
    # L1 (revised 2026-10-29, A11 c016): acceptance stops delta + S + 24 h before signing stops, so a first
    # attempt always has its full registered lifecycle before signing stops.
    from tessera_issue.util import DELTA
    from tessera_issue.service import SLACK_S
    assert w.na - w.sign_until == 96 * HOUR
    assert w.sign_until - w.accept_until == DELTA + SLACK_S + 24 * HOUR
    assert w.na - w.accept_until == 216 * HOUR


def test_closing_and_signing_unavailable(loc):
    loc.iss.signing_available = False
    r = submit(loc, str(uuid.uuid4()))[0]
    assert r.status == 403 and r.body["reason"] == "SIGNING_UNAVAILABLE"
    loc.iss.closing = True
    r = submit(loc, str(uuid.uuid4()))[0]
    assert r.status == 403 and r.body["reason"] == "CLOSING"


def test_refusal_is_final(loc, key):
    loc.iss.signing_available = False
    r1, rid = submit(loc, key, b"abc")
    loc.iss.signing_available = True                      # the condition clears; the request stays refused
    r2, _ = submit(loc, key, b"abc")
    assert r2.status == 403 and r2.body["state"] == "REFUSED" and r2.body["reason"] == "SIGNING_UNAVAILABLE"
    assert submit(loc, key, b"abd")[0].status == 409
    for _ in range(3):
        loc.tick()
    assert view(loc, key).body["state"] == "REFUSED"
    assert submit(loc, str(uuid.uuid4()), b"abc")[0].status == 202   # trying again means a new request


def test_requests_are_scoped_to_the_credential(loc, key):
    submit(loc, key, b"abc", cred="cred-A")
    assert api.status(loc.iss, "cred-B", key).status == 404
    assert api.receipt(loc.iss, "cred-B", key).status == 404
    r, _ = submit(loc, key, b"other", cred="cred-B")      # B's key space is its own
    assert r.status == 202 and view(loc, key, "cred-B").body["state"] == "ACCEPTED"


def test_unknown_and_malformed_lookups(loc, key):
    assert view(loc, key).status == 404
    assert api.status(loc.iss, "cred-A", "nope").status == 400


def test_receipt_before_completion_is_409(loc, key):
    submit(loc, key)
    r = api.receipt(loc.iss, "cred-A", key)
    assert r.status == 409 and r.body["state"] == "ACCEPTED"


# ------------------------------------------------------------------------------------------------ the pipeline
def test_accepted_to_complete_through_every_stage(loc, key):
    _, rid = submit(loc, key, b"stage walk")
    seen = []
    for _ in range(60):
        out = loc.tick()
        if rid in out["advanced"]:
            seen.append(out["advanced"][rid])
        if loc.iss.requests.get(rid)["state"] != "ACCEPTED":
            break
    moves = [(a, b) for a, b in seen if a != b]
    assert moves == [("frames", "signing"), ("signing", "stamp"), ("stamp", "evidence"), ("evidence", "finalize"),
                     ("finalize", "COMPLETE")]
    v = view(loc, key).body
    assert v["state"] == "COMPLETE" and "reason" not in v
    data, digest = fetch_receipt(loc, key)
    assert sha256hex(data) == v["receipt_sha256"] == digest
    assert loc.iss.results.get("content", rid, api.content_name(sha256hex(b"stage walk"))) is None
    assert not [k for k in loc.iss.results.blobs if k[0] == "work"]
    assert fetch_receipt(loc, key)[0] == data            # identical result every time


def test_accepted_to_refused_when_a_signer_refuses_every_attempt(loc, key):
    """Rewritten against the registered lifecycle (was FAILED SIGNER_REFUSED:...): a signer refusal discards that
    (unsigned, unstamped) attempt and the next one is allocated in the same write; after N refused attempts the request
    is REFUSED ATTEMPTS_EXHAUSTED, listing each attempt's reason."""
    _, rid = submit(loc, key)
    loc.workers["gpg"].clock = lambda: loc.clock() + 2 * DAY                 # its clock is off by more than epsilon
    rec = loc.run_until_done(rid, max_ticks=20)
    assert rec["state"] == "REFUSED" and rec["reason"] == "ATTEMPTS_EXHAUSTED"
    assert [a["end"]["reason"] for a in rec["attempts"]] == ["SIGNER_REFUSED:DECLARED_TIME_OUTSIDE_EPSILON"] * 3
    assert view(loc, key).body["attempts"] == [
        {"attempt": n, "outcome": "DISCARDED", "reason": "SIGNER_REFUSED:DECLARED_TIME_OUTSIDE_EPSILON"}
        for n in (1, 2, 3)]
    assert not [k for k in loc.iss.results.blobs if k[1] == rid and k[0] in ("content", "work")]


def test_a_pre_ship_failure_that_the_frozen_attempt_can_outlive_is_retried_not_failed(loc, key):
    """Rewritten against the registered lifecycle (was FAILED PRESHIP:UNVERIFIABLE/GIT_SIGNER_NOT_CONFIGURED): a latched
    attempt is discarded only for a failure its committed bytes cannot cure (design step 7). A misconfigured trust
    base is the issuer's, not the attempt's: the attempt stays latched, the reason is recorded, and once the
    configuration is repaired it ships."""
    _, rid = submit(loc, key)
    import copy
    real = loc.iss.preship.trust_base
    tb = copy.deepcopy(real)
    from tessera_issue.testkeys import P256Key
    from tessera_issue.util import b64e
    tb["repository_keys"][0]["key"] = b64e(P256Key("not the repository key", 1790000000).pgp_body)
    loc.iss.preship.trust_base = tb
    for _ in range(15):
        loc.tick()
    rec = loc.iss.requests.get(rid)
    assert rec["state"] == "ACCEPTED" and rec["attempts"][0]["state"] == "latched" and len(rec["attempts"]) == 1
    assert [e for e in rec["events"] if e[1] == "preship-retry"][-1][3] == "UNVERIFIABLE/GIT_SIGNER_NOT_CONFIGURED"
    assert api.receipt(loc.iss, "cred-A", key).status == 409
    loc.iss.preship.trust_base = real
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and api.receipt(loc.iss, "cred-A", key).status == 303


def test_stamp_waits_for_the_git_proof_to_reach_k6(loc, key):
    class LowTip:
        def __init__(self, h):
            self.h = h

        def tip(self):
            return self.h

    _, rid = submit(loc, key)
    real = loc.iss.headers
    loc.iss.headers = LowTip(loc.iss.window.h_git + 4)
    for _ in range(4):
        loc.tick()
    assert loc.iss.requests.get(rid)["stage"] == "stamp"
    loc.iss.headers = real
    assert loc.run_until_done(rid)["state"] == "COMPLETE"


def test_snapshot_is_recaptured_when_it_does_not_validate(loc, key):
    good = loc.iss.dns

    class FirstBad:
        calls = 0

        def capture(self, now):
            FirstBad.calls += 1
            return good.capture(now - 30 * DAY) if FirstBad.calls == 1 else good.capture(now)   # RRSIGs expired

    loc.iss.dns = FirstBad()
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and FirstBad.calls == 2
    assert any(e[1] == "snapshot-rejected" for e in rec["events"])


# ------------------------------------------------------------------------------------------------ expiry
@pytest.mark.parametrize("ending", ["COMPLETE", "REFUSED", "FAILED"])
def test_every_ended_state_expires_after_30_days(loc, key, ending):
    """FAILED is reached by an abandoned upload (CONTENT_UNAVAILABLE); it was the 24 h rule, which is withdrawn."""
    if ending == "REFUSED":
        loc.iss.closing = True
    if ending == "FAILED":
        real = loc.iss.results.put
        loc.iss.results.put = lambda *a: (_ for _ in ()).throw(OSError("upload interrupted"))
        with pytest.raises(OSError):
            submit(loc, key, b"expiring")
        loc.iss.results.put = real
        rid = api.record_id("cred-A", key)
        loc.clock.advance(pipeline.UPLOAD_GRACE_S)
    else:
        _, rid = submit(loc, key, b"expiring")
    rec = loc.run_until_done(rid, max_ticks=300) if ending != "REFUSED" else loc.iss.requests.get(rid)
    assert rec["state"] == ending
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    assert view(loc, key).body["state"] == ending
    loc.clock.t = rec["ended_at"] + RETENTION_S
    assert view(loc, key).body == {"request_key": key, "state": "EXPIRED"}
    assert api.receipt(loc.iss, "cred-A", key).status == 410
    assert submit(loc, key, b"expiring")[0].status == 410
    loc.iss.requests.expire(loc.clock())                                       # the TTL deletes the record itself
    assert loc.iss.requests.get(rid) is None
    assert view(loc, key).body == {"request_key": key, "state": "EXPIRED"}  # the tombstone still answers
    r, _ = submit(loc, key, b"expiring")
    assert r.status == 410 and r.body["state"] == "EXPIRED"                  # an expired key cannot start again
    assert submit(loc, key, b"different")[0].status == 410
