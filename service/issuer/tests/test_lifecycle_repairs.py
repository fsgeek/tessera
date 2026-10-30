"""Repairs after Codex's implementation review (docs/reviews/issuer-lifecycle-impl/CODEX-REVIEW.md, ILI-01..ILI-08;
ILI-09 is documentation). Each group reproduces the review's scenario (its scratch probes) and checks the repair.
Post-latch classifications are checked against REAL verifier outcomes (the service verifier as a library, through the
pre-ship check), never against a stubbed verdict."""
import json
import uuid

import pytest
from tessera_verify.anchors import parse_ots, select

from tessera_issue import api, ots, pipeline
from tessera_issue.aws import DynamoRequestStore
from tessera_issue.chain import pin_of
from tessera_issue.lifecycle import B_of, current
from tessera_issue.stand_in import StandInCalendar
from tessera_issue.util import DELTA, HOUR, b64d, b64e, rfc3339, sha256, sha256hex

from fakes import DYNAMO_ITEM_LIMIT, FakeDynamo, dynamo_item_size
from helpers import submit
from test_lifecycle import (GappedHeaders, HeldCalendar, LambdaTimeout, att, bury, declared, get, only_first_open, poll,
                            run, sign, to_evidence)


def latched(loc, key, at=None):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, at if at is not None else declared(a) + HOUR)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched", (rec["stage"], loc.iss.log[-3:])
    return rid, rec


def preserved(loc, rid, rec):
    return json.loads(loc.iss.results.get("work", rid, att(rec)["latch"]["ref"]))


def replace_presentation(loc, rid, pres):
    """Point the latch at a different presentation object, as a latch written by an earlier issuer version would."""
    store = loc.iss.requests
    rec = store.get(rid)
    body = json.dumps(pres, sort_keys=True, separators=(",", ":")).encode()
    name = f"a1/presentation-{sha256hex(body)}"
    loc.iss.results.put("work", rid, name, body)
    current(rec)["latch"].update(ref=name, sha256=sha256hex(body))
    assert store.save(rec)


def add_contradicting_branch(raw, height):
    """A Bitcoin attestation at `height` directly on the root: its message (the digest) is not the block's merkle
    root, so the pinned header contradicts it (OTS_MERKLE_MISMATCH)."""
    digest, root = ots.parse_file(raw)
    root.att(ots.BTC, ots._varuint(height))
    return ots.serialize_file(digest, root)


def ended(rec, n=1):
    a = rec["attempts"][n - 1]
    return a["state"], (a["end"] or {}).get("reason")


# ================================================================================================ ILI-01
def test_ILI01_a_contradicted_branch_at_the_selected_height_is_not_part_of_the_latched_presentation(loc, key):
    """Codex's probe: the proof holds a qualifying branch and a contradicted branch at the same height. select's
    contradiction flag is honoured: the latched presentation contains only qualifying branches (and is verified
    contradiction-free), so the receipt ships VALID_STRICT instead of failing OTS_MERKLE_MISMATCH forever."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h = bury(loc, declared(a) + HOUR)
    raw, _ = ots.upgrade(loc.iss.results.get("work", rid, "a1/receipt.ots"), loc.iss.calendars)
    loc.iss.results.put("work", rid, "a1/receipt.upgraded.ots", add_contradicting_branch(raw, h))
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and att(rec)["latch"]["contradicted_pruned"] == 1
    pres = preserved(loc, rid, rec)
    hdrs = {int(k): bytes.fromhex(v) for k, v in pres["headers"].items()}
    sel, contradicted = select(parse_ots(b64d(pres["ots"])), hdrs, {k: pin_of(v) for k, v in hdrs.items()})
    assert sel.height == h and not contradicted
    assert run(loc, rid)["state"] == "COMPLETE"


def test_ILI01_a_contradicted_preserved_presentation_is_discarded_with_its_reason(loc, key):
    """A preserved presentation that is itself contradicted (as an earlier issuer version could latch) is definitively
    invalid: the real verifier says INVALID / OTS_MERKLE_MISMATCH (row 11.3), which depends only on the preserved
    presentation, so step 7 discards the attempt with that reason and allocates the next one."""
    rid, rec = latched(loc, key)
    pres = preserved(loc, rid, rec)
    pres["ots"] = b64e(add_contradicting_branch(b64d(pres["ots"]), pres["height"]))
    replace_presentation(loc, rid, pres)
    poll(loc)
    rec = get(loc, rid)
    assert ended(rec) == ("discarded", "PRESHIP:INVALID/OTS_MERKLE_MISMATCH@11.3")
    assert rec["cur"] == 2 and rec["state"] == "ACCEPTED"


class ShapelessCalendar(StandInCalendar):
    """A calendar whose transaction carries the commitment in a non-OP_RETURN output: the merkle path is sound, so
    the attestation qualifies, but the receipt's transaction-shape check (row 11.5) fails."""

    def __init__(self, chain):
        super().__init__(chain, uri="https://shapeless-calendar.invalid")

    def _tx(self, m):
        prefix, suffix = super()._tx(m)
        assert prefix.endswith(b"\x6a\x20")
        return prefix[:-2] + b"\x51\x20", suffix


def test_ILI01_a_receipt_transaction_shape_failure_is_discarded(loc, key):
    loc.iss.calendars = [ShapelessCalendar(loc.world.chain)]
    rid, _ = latched(loc, key)
    poll(loc)
    rec = get(loc, rid)
    assert ended(rec) == ("discarded", "PRESHIP:INVALID/ANCHOR_TXID_MISMATCH@11.5")


def test_ILI01_a_failure_of_the_frozen_git_material_is_discarded(loc, key):
    rid, _ = latched(loc, key)
    loc.iss.window.git["trees"] = [loc.iss.window.git["trees"][0], loc.iss.window.git["trees"][0]]
    poll(loc)
    state, reason = ended(get(loc, rid))
    assert state == "discarded" and reason.startswith("PRESHIP:INVALID/") and reason.split("@")[1].startswith("14.")


def test_ILI01_a_failure_of_the_frozen_signature_bytes_is_discarded(loc, key):
    rid, rec = latched(loc, key)
    a = att(rec)
    name = "a1/" + pipeline.sig_name("p_kms", a["jobs"]["p_kms"]["sig_sha256"])
    other = loc.iss.results.get("work", rid, "a1/" + pipeline.sig_name("s_kms", a["jobs"]["s_kms"]["sig_sha256"]))
    loc.iss.results.put("work", rid, name, other)        # a valid-format signature over different bytes
    poll(loc)
    assert ended(get(loc, rid)) == ("discarded", "PRESHIP:INVALID/POSSESSION_INVALID@9.5")


def test_ILI01_a_replaceable_snapshot_failure_is_recaptured_not_discarded(loc, key):
    rid, rec = latched(loc, key)
    body = loc.iss.dns.capture(loc.clock())               # a different, valid snapshot body: the stamp no longer fits
    loc.iss.results.put("work", rid, "a1/snapshot.body", body)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and rec["stage"] == "snapshot"
    assert [e for e in rec["events"] if e[1] == "preship-recapture"][-1][3] == "SNAPSHOT_STAMP_MISMATCH"
    rec = run(loc, rid, max_polls=4)
    if rec["state"] == "ACCEPTED":
        loc.world.chain.mine(6)
        rec = run(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1


# ================================================================================================ ILI-02
def _late_snapshot(loc, rid, rec):
    """Re-capture the latched attempt's snapshot after declared + delta (Codex's probe)."""
    a = att(rec)
    loc.clock.t = declared(a) + DELTA + 100
    pipeline.st_snapshot(loc.iss, get(loc, rid), loc.clock())
    assert get(loc, rid)["stage"] == "finalize"


def test_ILI02_snapshot_time_without_proof_of_impossibility_is_retried(loc, key):
    """SNAPSHOT_TIME on the current snapshot is not proof that no lawful snapshot exists: while the chain's
    median-time-past does not yet exclude a block with time <= declared + delta, the issuer recaptures."""
    rid, rec = latched(loc, key)
    _late_snapshot(loc, rid, rec)
    loc.world.chain.mine(6)                              # anchored late; median-time-past still early
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and rec["stage"] == "snapshot"
    assert [e for e in rec["events"] if e[1] == "preship-recapture"][-1][3] == "SNAPSHOT_TIME"


def test_ILI02_proven_snapshot_impossibility_discards_with_evidence(loc, key):
    """Evidence-based, not age-based: the current snapshot's evidence is complete and fails SNAPSHOT_TIME, and the
    median time past of the eleven authenticated headers ending six below the tip already exceeds declared + delta;
    every future block (and so every new snapshot anchor) has a later time (consensus rule), so no lawful snapshot
    can be obtained for this frozen attempt. Step 7 discards it with the reason and the evidence."""
    rid, rec = latched(loc, key)
    _late_snapshot(loc, rid, rec)
    loc.world.chain.mine(20)
    poll(loc)
    rec = get(loc, rid)
    state, reason = ended(rec)
    assert (state, reason) == ("discarded", "SNAPSHOT_IMPOSSIBLE")
    ev = rec["attempts"][0]["end"]["evidence"]
    assert ev["median_time_past"] > ev["declared_plus_delta"] and ev["snapshot_reason"] == "SNAPSHOT_TIME"
    assert ev["mtp_heights"][1] == loc.world.chain.tip() - 5


# ================================================================================================ ILI-03
def _contradicted_only(loc, rid):
    root = ots.Node()
    root.att(ots.BTC, ots._varuint(loc.iss.window.h_git))
    raw = ots.serialize_file(sha256(loc.iss.results.get("work", rid, "a1/a_sig")), root)
    loc.iss.results.put("work", rid, "a1/receipt.ots", raw)


@pytest.mark.parametrize("when", ["before-B", "after-B"])
def test_ILI03_complete_authenticated_contradiction_ends_the_attempt_with_its_reason(loc, key, when):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    _contradicted_only(loc, rid)
    if when == "after-B":
        loc.clock.t = B_of(a) + 1
    poll(loc)
    rec = get(loc, rid)
    assert ended(rec) == ("discarded" if when == "before-B" else "expired", "EVIDENCE_CONTRADICTED")
    assert rec["cur"] == 2


def test_ILI03_contradiction_with_a_pending_calendar_stays_open(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    raw = loc.iss.results.get("work", rid, "a1/receipt.ots")                 # pending at the calendar
    loc.iss.results.put("work", rid, "a1/receipt.ots", add_contradicting_branch(raw, loc.iss.window.h_git))
    loc.clock.t = B_of(a) + 1
    poll(loc)
    assert only_first_open(get(loc, rid))


# ================================================================================================ ILI-04
def test_ILI04_durable_signatures_are_recovered_before_signing_closure_is_decided(loc, key):
    """Codex's probe: all four signatures are in S3 and logged "used", but every record update was lost; then
    signing stops. Nothing more needs signing, so the recovered set is sealed and the attempt continues."""
    _, rid = submit(loc, key)
    poll(loc)
    sign(loc)
    store = loc.iss.requests
    real = store.save
    store.save = lambda rec, expect=None: False
    pipeline.drain(loc.iss)
    store.save = real
    rec = get(loc, rid)
    assert rec["stage"] == "signing" and not any(j["sig_sha256"] for j in att(rec)["jobs"].values())
    # signing stops one hour after the declaration (the window is moved, as an operator closure would)
    loc.iss.window.not_after = rfc3339(declared(att(rec)) + HOUR + 96 * HOUR)
    loc.clock.t = loc.iss.window.sign_until + 1
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "ACCEPTED" and rec["stage"] == "stamp" and att(rec)["receipt_id"]
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1


def test_ILI04_a_partly_recovered_set_still_needing_signing_closes(loc, key):
    _, rid = submit(loc, key)
    poll(loc)
    loc.workers["kms"].process()                          # gpg never answers
    store = loc.iss.requests
    real = store.save
    store.save = lambda rec, expect=None: False
    pipeline.drain(loc.iss)
    store.save = real
    loc.clock.t = loc.iss.window.sign_until + 1
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED"
    assert [bool(j["sig_sha256"]) for j in att(rec)["jobs"].values()] == [True, True, False, False]


# ================================================================================================ ILI-05
class SlowHeaders:
    """Two explorers at `per` seconds per HTTP request: tip() costs 2 requests, each header height 4."""

    def __init__(self, real, clock, per=12):
        self.real, self.clock, self.per, self.calls = real, clock, per, []

    def tip(self):
        self.clock.advance(2 * self.per)
        return self.real.tip()

    def headers(self, heights):
        self.calls += list(heights)
        self.clock.advance(4 * self.per * len(heights))
        return self.real.headers(heights)


def _timed_polls(loc, n):
    spans = []
    for _ in range(n):
        t0 = loc.clock()
        poll(loc)
        spans.append(loc.clock() - t0)
    return spans


def test_ILI05_slow_explorers_progress_across_invocations_within_the_budget(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h = bury(loc, declared(a) + HOUR)
    slow = SlowHeaders(loc.iss.headers, loc.clock)
    loc.iss.headers = slow
    spans = _timed_polls(loc, 8)
    assert max(spans) <= 300, spans                                        # every invocation fits the Lambda timeout
    rec = get(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1
    assert len(slow.calls) == len(set(slow.calls))                          # fetched once, resumed from checkpoints
    assert set(range(h, h + 6)) <= set(slow.calls)


def test_ILI05_a_killed_invocation_keeps_the_headers_it_fetched(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h = bury(loc, declared(a) + HOUR)
    slow = SlowHeaders(loc.iss.headers, loc.clock, per=0)
    real_headers = slow.headers

    def dies_on_the_fourth(heights):
        if len(slow.calls) == 3:
            raise LambdaTimeout()
        return real_headers(heights)
    slow.headers = dies_on_the_fourth
    loc.iss.headers = slow
    with pytest.raises(LambdaTimeout):
        poll(loc)
    slow.headers = real_headers
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched"
    assert sorted(slow.calls) == list(range(h, h + 6))                       # nothing fetched twice


def test_ILI05_requests_are_scheduled_fairly_across_invocations(loc, monkeypatch):
    rids = []
    for i in range(3):
        _, rid = submit(loc, str(uuid.uuid4()), f"fair {i}".encode())
        rids.append(rid)
    for rid in rids:
        to_evidence(loc, rid)
    first, real = [], pipeline.advance

    def record(iss, rec):
        first.append(rec["rid"])
        return real(iss, rec)
    monkeypatch.setattr(pipeline, "advance", record)
    starts = []
    for _ in range(3):
        first.clear()
        loc.iss.budget_s = 1                              # room for (at most) one request per invocation
        poll(loc)
        starts.append(first[0])
    assert sorted(starts) == sorted(rids)                 # each invocation starts where the previous one stopped


# ================================================================================================ ILI-06
def test_ILI06_pruning_holds_the_presentation_when_lower_evidence_arrives_with_the_snapshot_headers(loc, key):
    """Latch the higher passing attestation while the lower one's segment is unavailable. At finalization the lower
    segment arrives as part of the snapshot's header collection (the snapshot was stamped to the same calendars).
    The pruned presentation still selects the latched height and ships; without pruning the selection moves."""
    held = HeldCalendar(loc.world.chain)
    loc.iss.calendars.append(held)
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h1 = bury(loc, declared(a) + HOUR)                   # calendar A: lower
    held.held = False
    h2 = bury(loc, declared(a) + 2 * HOUR)               # calendar B: higher, also passing
    real = loc.iss.headers
    loc.iss.headers = GappedHeaders(real, range(h1, h1 + 6))
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and att(rec)["latch"]["height"] == h2
    loc.iss.headers = real                                # the lower segment is now obtainable
    rec = run(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1
    bundle = json.loads(loc.iss.results.get("result", rid, "receipt.json"))
    assert str(h1) in bundle["layers"][0]["headers"]     # the lower segment travelled with the snapshot
    assert rec["T"] == rfc3339(att(rec)["latch"]["T"])  # the latched height's T, not the lower one's


# ================================================================================================ ILI-07
def dynamo_loc(loc):
    ddb = FakeDynamo()
    loc.iss.requests = DynamoRequestStore(ddb, "t")
    return ddb


def test_ILI07_an_oversized_signer_reason_is_bounded_and_kept_by_reference(loc, key):
    ddb = dynamo_loc(loc)
    _, rid = submit(loc, key)
    poll(loc)
    q = loc.iss.signers["gpg"].responses
    srid = att(get(loc, rid))["jobs"]["s_gpg"]["request_id"]
    huge = "x" * 210_000
    q.send(json.dumps({"request_id": srid, "status": "REFUSED", "reason": huge}))
    q.send(json.dumps({"request_id": "y" * 300_000, "status": "S" * 100_000, "reason": huge}))
    for _ in range(8):                                    # ILC-I7: a round may receive from one (random) slot
        poll(loc)
        if get(loc, rid)["attempts"][0]["state"] != "open":
            break
    rec = get(loc, rid)
    a1 = rec["attempts"][0]
    assert a1["state"] == "discarded" and a1["end"]["reason"] == "SIGNER_REFUSED:UNRECOGNIZED_REASON"
    diag = a1["end"]["diagnostic"]
    assert diag["sha256"] == sha256hex(huge.encode()) and diag["length"] == len(huge)
    assert loc.iss.results.get("work", rid, diag["ref"]) == huge.encode()
    assert ddb.max_item <= DYNAMO_ITEM_LIMIT and ddb.max_item < 64 * 1024
    for e in loc.iss.requests.siglog():
        assert len(json.dumps(e)) < 2048


def test_ILI07_the_fake_rejects_items_over_400_KiB_as_DynamoDB_does():
    ddb = FakeDynamo()
    st = DynamoRequestStore(ddb, "t")
    rec = {"rid": "r", "state": "ACCEPTED", "stage": "frames", "expires_at": None, "blob": "x" * (400 * 1024)}
    with pytest.raises(Exception, match="ValidationException"):
        st.create(rec)
    item = st._item(dict(rec, version=1, blob="x"))
    assert dynamo_item_size(item) < 1024


def test_ILI07_a_three_attempt_refusal_stays_far_below_the_item_limit(loc, key):
    ddb = dynamo_loc(loc)
    loc.workers["gpg"].clock = lambda: loc.clock() + 3 * 86400                # every attestation refused (epsilon)
    _, rid = submit(loc, key)
    for _ in range(12):
        sign(loc)
        poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "ATTEMPTS_EXHAUSTED"
    assert ddb.max_item < 64 * 1024


# ================================================================================================ ILI-08
def test_ILI08_content_is_checked_before_attempt_1_is_allocated(loc, key):
    _, rid = submit(loc, key)
    loc.iss.results.delete("content", rid)
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "FAILED" and rec["reason"] == "CONTENT_UNAVAILABLE" and rec["attempts"] == []


def _to_attempt_2_frames(loc, rid):
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + DELTA + HOUR)                 # complete negative: attempt 1 discarded, 2 allocated
    poll(loc)
    rec = get(loc, rid)
    assert rec["cur"] == 2 and rec["stage"] == "frames"
    return rec


def test_ILI08_content_lost_after_allocation_is_recovered_from_an_earlier_frame(loc, key):
    _, rid = submit(loc, key, b"recoverable content")
    _to_attempt_2_frames(loc, rid)
    loc.iss.results.delete("content", rid)
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "ACCEPTED" and rec["stage"] == "signing" and rec["cur"] == 2
    assert loc.iss.results.get("content", rid, api.content_name(sha256hex(b"recoverable content"))) \
        == b"recoverable content"
    assert any(e[1] == "content-recovered" for e in rec["events"])


def test_ILI08_content_lost_beyond_recovery_refuses_in_the_ending_write(loc, key):
    _, rid = submit(loc, key)
    _to_attempt_2_frames(loc, rid)
    loc.iss.results.delete("content", rid)
    for name in ("f_kms", "f_gpg"):
        loc.iss.results.put("work", rid, "a1/" + name, b"lost")
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "CONTENT_UNAVAILABLE"
    assert ended(rec, 2) == ("discarded", "CONTENT_UNAVAILABLE") and len(rec["attempts"]) == 2


def test_ILI05_the_lambda_handler_budgets_by_the_time_the_invocation_has_left(monkeypatch):
    from tessera_issue import lambda_app
    from tessera_issue.service import POLL_BUDGET_S, POLLER_TIMEOUT_S
    seen = []
    monkeypatch.setattr(lambda_app, "_issuer", lambda: type("I", (), {"budget_s": POLL_BUDGET_S})())
    monkeypatch.setattr(lambda_app.pipeline, "poll", lambda iss, budget_s=None: seen.append(budget_s) or {})

    class Context:
        def __init__(self, ms):
            self.ms = ms

        def get_remaining_time_in_millis(self):
            return self.ms
    lambda_app.poller_handler({}, Context(POLLER_TIMEOUT_S * 1000))
    lambda_app.poller_handler({}, Context(100_000))       # a late start: 100 s left
    lambda_app.poller_handler({}, None)
    assert seen == [POLL_BUDGET_S, 100 - (POLLER_TIMEOUT_S - POLL_BUDGET_S), POLL_BUDGET_S]
