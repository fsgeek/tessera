"""The registered issuance lifecycle (docs/decisions/2026-10-29-issuance-lifecycle.md, revision 5.3.1, and the checked
protocol formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla). One test group per item of the implementation brief:

  1  attempts 1..N with isolated material; responses routed by attempt
  2  one lifecycle writer: the API is read-only
  3  the fence before every evidence fetch; every lifecycle write guarded on (state, attempt id, version)
  4  eligibility (three conjuncts, k = 6, the attempt's own evidence) and the latch with its preserved presentation
  5  expiry / discard only on complete negative evidence; anything else leaves the attempt open (step 5 is GATED)
  6  after the latch: transient failures retried, incurable ones discarded with a reason, presentation never swapped
  7  atomic end-and-allocate; REFUSED ATTEMPTS_EXHAUSTED / SIGNING_CLOSED; closed signing never ends a latched or
     signed-and-stamped attempt
  8  the public view
  9  storage lifetime: no age rule on live objects; cleanup tags cleanup-due, then deletes

Evidence is driven with the stand-in chain and calendar on the fake clock: a stamp stays pending until a block is
mined, the block's time is the clock, and k = 6 needs five more blocks. Races are driven by hooks on the stores, as in
test_confirm_fixes.py; nothing sleeps. Model action names (Start, Fence, Fetch, Send, Commit, Kill, Resend) are used
where a test mirrors one of the model's interleavings."""
import copy
import json

import pytest

from tessera_issue import api, ots, pipeline
from tessera_issue.aws import DynamoRequestStore, S3ResultStore
from tessera_issue.chain import pin_of
from tessera_issue.lifecycle import B_of, current
from tessera_issue.service import N_ATTEMPTS, POLL_INTERVAL_S, RETENTION_S, SLACK_S
from tessera_issue.stand_in import StandInCalendar
from tessera_issue.stores import InMemoryRequestStore, lifecycle_guard
from tessera_issue.util import DAY, DELTA, EPS, HOUR, b64d, rfc3339, sha256, ts
from tessera_verify.anchors import parse_ots, select

from fakes import FakeDynamo, FakeS3
from helpers import submit


class LambdaTimeout(BaseException):
    """The invocation is killed: nothing in the issuer can catch it."""


# ------------------------------------------------------------------------------------------------ helpers
def get(loc, rid):
    return loc.iss.requests.get(rid)


def att(rec, n=None):
    return rec["attempts"][(n or rec["cur"]) - 1]


def only_first_open(rec):
    """Attempt 1 is still the current attempt, still open, and nothing was allocated after it."""
    return rec["state"] == "ACCEPTED" and rec["cur"] == 1 and len(rec["attempts"]) == 1 \
        and rec["attempts"][0]["state"] == "open"


def declared(a):
    return ts(a["declared_issue_time"])


def poll(loc):
    return pipeline.poll(loc.iss)


def sign(loc):
    for w in loc.workers.values():
        w.process()


def to_evidence(loc, rid):
    """Frames, signatures and the stamps of the current attempt, with no block mined: the stamps stay pending."""
    for _ in range(12):
        rec = get(loc, rid)
        if rec["state"] == "ACCEPTED" and rec["stage"] == "evidence":
            return rec
        sign(loc)
        poll(loc)
    raise AssertionError(("evidence stage not reached", rec["state"], rec["stage"], loc.iss.log[-3:]))


def bury(loc, at, confirmed_at=None):
    """Mine the block holding every pending commitment at wall time `at`, then five more; the sixth (h + 5) gets
    time `confirmed_at` (default: at + 5). -> h."""
    chain = loc.world.chain
    loc.clock.t = at
    h = chain.mine(1)
    loc.clock.t = (confirmed_at - 4) if confirmed_at is not None else at
    chain.mine(5)
    assert confirmed_at is None or chain.blocks[h + 5]["time"] == confirmed_at
    return h


def run(loc, rid, max_polls=12):
    """Poll (signers answering) until the request ends. -> record."""
    for _ in range(max_polls):
        rec = get(loc, rid)
        if rec["state"] != "ACCEPTED":
            return rec
        sign(loc)
        poll(loc)
    return get(loc, rid)


def saves(loc):
    """Record every committed record version (deep copies), in order."""
    store, seen = loc.iss.requests, []
    real = store.save

    def rec_save(rec, expect=None):
        ok = real(rec, expect)
        if ok:
            seen.append(copy.deepcopy(rec))
        return ok
    store.save = rec_save
    return seen


def negative_then_next(loc, rid, at):
    """Bury the current attempt's stamp late (T > declared + delta), poll once at `at` (>= the burial). -> record."""
    rec = to_evidence(loc, rid)
    a = att(rec)
    bury(loc, declared(a) + DELTA + HOUR)
    loc.clock.t = max(at, loc.clock())
    poll(loc)
    return get(loc, rid)


class HeldCalendar(StandInCalendar):
    """A second calendar whose commitments are mined only once released."""

    def __init__(self, chain):
        super().__init__(chain, uri="https://stand-in-calendar-b.invalid")
        self.held = True

    def include(self, h):
        return [] if self.held else super().include(h)


class GappedHeaders:
    """The header source, failing for chosen heights (a header store or explorer that cannot serve them)."""

    def __init__(self, real, blocked=None):
        self.real, self.blocked = real, None if blocked is None else set(blocked)   # None: every height

    def tip(self):
        return self.real.tip()

    def headers(self, heights):
        if self.blocked is None or self.blocked & set(heights):
            raise OSError("explorers unavailable for " + str(sorted(heights)))
        return self.real.headers(heights)


# ================================================================================================ 1 isolation
def test_1_attempts_have_their_own_declared_time_frames_jobs_stamp_and_evidence(loc, key):
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    a1 = att(rec)
    assert rec["cur"] == 1 and a1["id"] == "a1" and a1["state"] == "open"
    loc.clock.advance(HOUR)
    rec = negative_then_next(loc, rid, declared(a1) + DELTA + 2 * HOUR)
    assert att(rec, 1)["state"] == "discarded" and rec["cur"] == 2
    rec = to_evidence(loc, rid)
    a1, a2 = att(rec, 1), att(rec, 2)
    assert a2["id"] == "a2" and declared(a2) > declared(a1)
    names = loc.iss.results.names("work", rid)
    n1, n2 = {n for n in names if n.startswith("a1/")}, {n for n in names if n.startswith("a2/")}
    assert n1 and n2 and not [n for n in names if not n.startswith(("a1/", "a2/"))]
    for name in ("manifest", "f_kms", "f_gpg", "a_sig", "receipt.ots", "snapshot.ots"):
        assert loc.iss.results.get("work", rid, "a1/" + name) != loc.iss.results.get("work", rid, "a2/" + name) \
            or name == "manifest"
    assert {j["request_id"] for j in a1["jobs"].values()}.isdisjoint(j["request_id"] for j in a2["jobs"].values())
    for n, a in ((1, a1), (2, a2)):                       # each stamp is a fresh stamp of that attempt's own A_sig
        proof = parse_ots(loc.iss.results.get("work", rid, f"a{n}/receipt.ots"))
        assert proof.digest == sha256(loc.iss.results.get("work", rid, f"a{n}/a_sig"))
    assert a1["receipt_id"] != a2["receipt_id"]


def test_1_a_late_response_for_another_attempt_is_logged_and_ignored(loc, key):
    _, rid = submit(loc, key)
    kms, gpg = loc.workers["kms"], loc.workers["gpg"]
    poll(loc)                                            # attempt 1: frames sent
    skew = gpg.clock
    gpg.clock = lambda: loc.clock() + 2 * DAY            # attempt 1's gpg attestation is refused (epsilon)
    gpg.process()
    gpg.clock = skew
    poll(loc)                                            # the refusal discards attempt 1; attempt 2 is allocated
    rec = get(loc, rid)
    assert att(rec, 1)["state"] == "discarded" and att(rec, 1)["end"]["reason"].startswith("SIGNER_REFUSED:")
    assert rec["cur"] == 2
    poll(loc)                                            # attempt 2's frames are sent
    a1_ids = {j["request_id"] for j in att(get(loc, rid), 1)["jobs"].values()}
    sign(loc)                                            # kms now answers attempt 1's requests late, and attempt 2's
    poll(loc)
    rec = get(loc, rid)
    log = loc.iss.requests.siglog()
    late = [e for e in log if e["request_id"] in a1_ids and e["status"] == "SIGNED"]
    assert late and all(e["disposition"] == "other-attempt" for e in late)
    a2 = att(rec, 2)
    used = {(e["request_id"], e["signature_sha256"]) for e in log if e["disposition"] == "used"}
    for j in a2["jobs"].values():
        assert j["request_id"] not in a1_ids
        assert j["sig_sha256"] is None or (j["request_id"], j["sig_sha256"]) in used
    assert rec["stage"] in ("stamp", "evidence")


# ================================================================================================ 2 one writer
def test_2_status_and_receipt_are_read_only_in_every_state(loc, key):
    _, rid = submit(loc, key)
    store = loc.iss.requests
    real_save, real_create = store.save, store.create

    def forbidden(*a, **k):
        raise AssertionError("the API made a write")
    for _ in range(20):
        store.save, store.create = forbidden, forbidden
        assert api.status(loc.iss, "cred-A", key).status == 200
        api.receipt(loc.iss, "cred-A", key)
        store.save, store.create = real_save, real_create
        if get(loc, rid)["state"] != "ACCEPTED":
            break
        loc.tick()
    assert get(loc, rid)["state"] == "COMPLETE"
    assert not hasattr(api, "settle") and not hasattr(api, "confirmed")


# ================================================================================================ 3 fence and guards
def test_3_the_fence_commits_before_any_evidence_is_fetched(loc, key):
    _, rid = submit(loc, key)
    to_evidence(loc, rid)
    order, store = [], loc.iss.requests
    real_save, real_tip, real_fetch = store.save, loc.iss.headers.tip, loc.iss.calendars[0].fetch
    store.save = lambda rec, expect=None: (order.append(("save", real_save(rec, expect))), order[-1][1])[1]
    loc.iss.headers.tip = lambda: (order.append(("tip",)), real_tip())[1]
    loc.iss.calendars[0].fetch = lambda m: (order.append(("calendar",)), real_fetch(m))[1]
    poll(loc)
    assert order[0] == ("save", True) and ("calendar",) in order
    assert order.index(("save", True)) < order.index(("calendar",))


def test_3_no_fetch_happens_when_the_fence_fails(loc, key):
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    bury(loc, declared(att(rec)) + HOUR)
    fetched, store = [], loc.iss.requests
    real_save = store.save
    store.save = lambda rec, expect=None: False             # every guarded write fails (e.g. a concurrent writer)
    real_fetch = loc.iss.calendars[0].fetch
    loc.iss.calendars[0].fetch = lambda m: fetched.append(m) or real_fetch(m)
    poll(loc)
    store.save = real_save
    assert not fetched and only_first_open(get(loc, rid))


def _kill_on(loc, pred):
    """Kill the invocation when it sends a write matching pred; the write is left pending. -> list of (rec, expect)."""
    store, left = loc.iss.requests, []
    real = store.save

    def send(rec, expect=None):
        if not left and pred(rec):
            left.append((copy.deepcopy(rec), copy.deepcopy(expect)))
            store.save = real
            raise LambdaTimeout()
        return real(rec, expect)
    store.save = send
    return left


def _stale_calendar(loc):
    cal = loc.iss.calendars[0]
    real = cal.fetch
    cal.fetch = lambda m: None                              # up, but answering stale (pending)
    return lambda: setattr(cal, "fetch", real)


@pytest.mark.parametrize("fence", [True, False], ids=["fenced", "B5-no-fence"])
def test_3_a_leftover_write_of_a_killed_invocation_cannot_beat_a_live_latch(loc, key, fence, monkeypatch):
    """R5 path (c) and its companion B5. Invocation 1 reads past B, its fetch is stale, it sends its failure-history
    write and is killed; the write stays pending. Invocation 2 fences, fetches eligibility and latches; the leftover
    write resolves just before the latch. With the fence it fails its version guard and the latch commits. Without the
    fence (B5) the leftover commits and the live latch fails its guard: the race the fence closes."""
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    a = att(rec)
    bury(loc, declared(a) + HOUR)                          # timely
    loc.clock.t = B_of(a) + 600
    restore = _stale_calendar(loc)
    left = _kill_on(loc, lambda r: bool(current(r).get("failed_intervals")))
    with pytest.raises(LambdaTimeout):
        poll(loc)
    restore()
    assert left
    if not fence:
        monkeypatch.setattr(pipeline, "_fence", lambda iss, rec, now: None)
    store, outcome = loc.iss.requests, {}
    real = store.save

    def latch_after_leftover(rec, expect=None):
        if current(rec)["state"] == "latched" and "leftover" not in outcome:
            outcome["leftover"] = real(*left[0])
        return real(rec, expect)
    store.save = latch_after_leftover
    poll(loc)
    store.save = real
    rec = get(loc, rid)
    if fence:
        assert outcome["leftover"] is False and att(rec)["state"] == "latched"
        assert not att(rec)["failed_intervals"]
    else:
        assert outcome["leftover"] is True and only_first_open(rec)
    poll(loc)
    assert att(get(loc, rid))["state"] in ("latched", "shipped")   # either way it is not lost for good


def test_3_a_duplicate_end_and_allocate_write_fails_its_guard(loc, key):
    """Resend: an ending write retried after an ambiguous response applies once; the retry fails its guard."""
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    store, dup = loc.iss.requests, []
    real = store.save

    def twice(rec, expect=None):
        before = copy.deepcopy(rec)
        ok = real(rec, expect)
        if ok and rec["cur"] == 2 and not dup:
            dup.append(real(before, expect))
        return ok
    store.save = twice
    bury(loc, declared(att(rec)) + DELTA + HOUR)
    poll(loc)
    store.save = real
    rec = get(loc, rid)
    assert dup == [False] and len(rec["attempts"]) == 2 and rec["cur"] == 2


@pytest.mark.parametrize("kind", ["memory", "dynamo"])
def test_3_the_guard_is_state_attempt_id_and_version(kind):
    st = InMemoryRequestStore() if kind == "memory" else DynamoRequestStore(FakeDynamo(), "t")
    rec = {"rid": "r", "state": "ACCEPTED", "stage": "evidence", "expires_at": None, "cur": 1,
           "attempts": [{"n": 1, "id": "a1", "state": "open"}]}
    st.create(rec)
    rec = st.get("r")
    g = lifecycle_guard(rec)
    assert g == {"state": "ACCEPTED", "attempt": "a1", "astate": "open"}
    assert not st.save(copy.deepcopy(rec), dict(g, attempt="a2"))
    assert not st.save(copy.deepcopy(rec), dict(g, state="REFUSED"))
    assert not st.save(copy.deepcopy(rec), dict(g, astate="latched"))
    stale = copy.deepcopy(rec)
    assert st.save(rec, g)
    assert not st.save(stale, g)                         # same state and attempt, older version
    assert st.get("r")["version"] == rec["version"]


# ================================================================================================ 4 eligibility
def test_4_latch_on_k6_and_three_conjuncts_with_the_preserved_presentation(loc, key):
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    a = att(rec)
    h = bury(loc, declared(a) + HOUR)
    loc.clock.advance(60)
    poll(loc)
    rec = get(loc, rid)
    a = att(rec)
    assert a["state"] == "latched" and rec["stage"] == "finalize"
    lt = a["latch"]
    assert lt["observed_at"] == loc.clock() and lt["height"] == h
    assert lt["T"] == loc.world.chain.blocks[h]["time"] and lt["confirmed_at"] == loc.world.chain.blocks[h + 5]["time"]
    body = loc.iss.results.get("work", rid, lt["ref"])
    assert body is not None and lt["ref"].startswith("a1/presentation-")
    pres = json.loads(body)
    hdrs = {int(k): bytes.fromhex(v) for k, v in pres["headers"].items()}
    assert sorted(hdrs) == list(range(h, h + 6))
    proof = parse_ots(b64d(pres["ots"]))
    assert proof.digest == sha256(loc.iss.results.get("work", rid, "a1/a_sig")) and not proof.pending
    sel, _ = select(proof, hdrs, {k: pin_of(v) for k, v in hdrs.items()})
    assert (sel.height, sel.time, sel.confirmed) == (h, lt["T"], lt["confirmed_at"])


def test_4_five_confirmations_do_not_latch(loc, key):
    _, rid = submit(loc, key)
    rec = to_evidence(loc, rid)
    loc.clock.t = declared(att(rec)) + HOUR
    loc.world.chain.mine(5)                               # h .. h+4: k = 5
    poll(loc)
    assert only_first_open(get(loc, rid))
    loc.world.chain.mine(1)
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched"


def test_4_eligibility_observed_exactly_at_B_latches_and_never_expires(loc, key):
    """A2.1: the boundary is inclusive and latch-winning. confirmed_at = declared + delta exactly; first poll at B."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + DELTA - HOUR, confirmed_at=declared(a) + DELTA)
    loc.clock.t = B_of(a)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and att(rec)["latch"]["observed_at"] == B_of(a)
    loc.clock.t = B_of(a) + 1
    assert run(loc, rid)["state"] == "COMPLETE"


def test_4_timely_burial_first_observed_long_after_B_latches(loc, key):
    """The latch may be written at any time while the attempt is open; timeliness is the chain fact."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    loc.clock.t = B_of(a) + 10 * DAY                      # no poll ran in between (an outage of the poller)
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched"
    rec = run(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1


def test_4_a_killed_invocation_between_fetch_and_latch_loses_nothing_durable(loc, key):
    """Kill after an eligible Fetch, before the latch is written: the next poll fetches again and latches."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    left = _kill_on(loc, lambda r: current(r)["state"] == "latched")
    with pytest.raises(LambdaTimeout):
        poll(loc)
    assert left and only_first_open(get(loc, rid))
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched"


def test_4_the_presentation_object_is_written_before_the_latch_commits(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    res, store = loc.iss.results, loc.iss.requests
    real_put, real_save, seen = res.put, store.save, []

    def failing_put(ns, r, name, data):
        if "presentation-" in name:
            raise OSError("S3 put failed")
        return real_put(ns, r, name, data)
    res.put = failing_put
    poll(loc)
    assert only_first_open(get(loc, rid))                 # no latch without its object
    res.put = real_put

    def check(rec, expect=None):
        if current(rec)["state"] == "latched":
            seen.append(res.get("work", rid, current(rec)["latch"]["ref"]) is not None)
        return real_save(rec, expect)
    store.save = check
    poll(loc)
    store.save = real_save
    assert seen == [True] and att(get(loc, rid))["state"] == "latched"


def test_4_the_predicate_is_three_conjuncts_not_rows_12_2_and_12_3():
    from tessera_verify.anchors import Selected
    d = 10_000_000
    f = pipeline.conjunct_failed
    assert f(Selected(1, d - EPS, d, []), d) is None
    assert f(Selected(1, d - EPS - 1, d, []), d) == "TIME_BEFORE_DECLARED_EPSILON"   # rows 12.2/12.3 would pass
    assert f(Selected(1, d + DELTA, d + DELTA, []), d) is None
    assert f(Selected(1, d + DELTA + 1, d + DELTA + 2, []), d) == "TIME_AFTER_DECLARED_DELTA"
    assert f(Selected(1, d + DELTA, d + DELTA + 1, []), d) == "CONFIRMATION_LATE"


def test_4_evidence_for_another_digest_is_not_the_attempts_evidence(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    other = ots.stamp(sha256(b"some other object"), loc.iss.calendars, bytes(16))
    loc.iss.results.put("work", rid, "a1/receipt.ots", other)
    bury(loc, declared(a) + HOUR)
    loc.clock.t = B_of(a) + DAY
    poll(loc)
    rec = get(loc, rid)
    assert only_first_open(rec)


# ================================================================================================ 5 complete negatives
def test_5_complete_negative_before_B_discards_and_allocates_the_next_attempt(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + DELTA + HOUR)                 # T after declared + delta
    loc.clock.advance(60)
    decided = loc.clock()
    assert decided <= B_of(a)
    poll(loc)
    rec = get(loc, rid)
    a1, a2 = att(rec, 1), att(rec, 2)
    assert a1["state"] == "discarded" and a1["end"] == {"outcome": "DISCARDED", "reason": "TIME_AFTER_DECLARED_DELTA",
                                                         "at": decided}
    assert a2["state"] == "open" and declared(a2) == decided and rec["cur"] == 2 and rec["stage"] == "frames"
    assert rec["state"] == "ACCEPTED"


def test_5_complete_negative_after_B_expires(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, B_of(a) + 1)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec, 1)["state"] == "expired" and att(rec, 1)["end"]["outcome"] == "EXPIRED"
    assert att(rec, 1)["end"]["reason"] == "TIME_AFTER_DECLARED_DELTA" and rec["cur"] == 2


def test_5_a_late_confirmation_is_a_failing_conjunct(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + DELTA - HOUR, confirmed_at=declared(a) + DELTA + 1)
    poll(loc)
    assert att(get(loc, rid), 1)["end"]["reason"] == "CONFIRMATION_LATE"


def test_5_evidence_that_never_completes_never_ends_the_attempt(loc, key):
    """GATED (step 5): no burial ever. Polls continue for sixty days past B; the attempt stays open, with its failure
    history recorded for diagnosis only. No EVIDENCE_UNAVAILABLE, no successor, no refusal, no cleanup."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    b = B_of(a)
    for t in [b - 600, b, b + 1, b + 600, b + 1200, b + DAY, b + 30 * DAY, b + 60 * DAY]:
        loc.clock.t = t
        poll(loc)
    rec = get(loc, rid)
    a = att(rec)
    assert rec["state"] == "ACCEPTED" and rec["cur"] == 1 and len(rec["attempts"]) == 1 and a["state"] == "open"
    assert a["unavailable_since"] == b + 1                     # the first failed fetch that started after B
    assert a["failed_intervals"][0][0] == (b + 1) // POLL_INTERVAL_S
    assert (b + 60 * DAY) // POLL_INTERVAL_S in {i for lo, hi in a["failed_intervals"] for i in range(lo, hi + 1)}
    assert loc.iss.requests.cleanup_list() == []
    assert "EVIDENCE_UNAVAILABLE" not in json.dumps(rec)
    bury(loc, b + 61 * DAY)                                     # evidence finally completes: negative -> EXPIRED
    poll(loc)
    rec = get(loc, rid)
    assert att(rec, 1)["state"] == "expired" and att(rec, 1)["unavailable_since"] is None


def test_5_a_failed_fetch_after_B_never_expires(loc, key):
    """B3: a complete negative exists on chain, but the poller's fetch fails. It must not be read as negative."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h = bury(loc, B_of(a) + HOUR)
    real = loc.iss.headers
    loc.iss.headers = GappedHeaders(real, range(h, h + 6))
    for t in (B_of(a) + 2 * HOUR, B_of(a) + 3 * DAY):
        loc.clock.t = t
        poll(loc)
    rec = get(loc, rid)
    assert only_first_open(rec) and att(rec)["failed_intervals"]
    loc.iss.headers = real
    poll(loc)
    assert att(get(loc, rid), 1)["state"] == "expired"


def test_5_a_pending_calendar_blocks_the_negative(loc, key):
    """Every calendar the attempt was stamped to must have attested before a negative is conclusive."""
    held = HeldCalendar(loc.world.chain)
    loc.iss.calendars.append(held)
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, B_of(a) + HOUR)                             # calendar A attested late (fails); B still pending
    loc.clock.t = B_of(a) + DAY
    poll(loc)
    assert only_first_open(get(loc, rid))
    held.held = False
    bury(loc, B_of(a) + 2 * DAY)
    poll(loc)
    assert att(get(loc, rid), 1)["state"] == "expired"


def test_5_partial_header_recovery_lower_attestation_qualifies_later(loc, key):
    """ILC2-03 (the model's B1' companion): every calendar has attested; the higher attestation's segment is in hand
    and fails; the lower attestation's segment cannot yet be obtained. No discard or expiry; once the segment is
    recovered the lower attestation is the lowest qualifying one, and it latches."""
    held = HeldCalendar(loc.world.chain)
    loc.iss.calendars.append(held)
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h1 = bury(loc, declared(a) + HOUR)                     # calendar A: timely, at h1
    real = loc.iss.headers
    loc.iss.headers = GappedHeaders(real, range(h1, h1 + 6))
    poll(loc)
    assert only_first_open(get(loc, rid))
    held.held = False
    h2 = bury(loc, declared(a) + DELTA + HOUR)            # calendar B: late, at h2 > h1 + 5
    assert h2 > h1 + 5
    for t in (declared(a) + DELTA + 2 * HOUR, B_of(a) + DAY):   # before and after B
        loc.clock.t = t
        poll(loc)
        assert only_first_open(get(loc, rid))
    loc.iss.headers = real
    poll(loc)
    a = att(get(loc, rid))
    assert a["state"] == "latched" and a["latch"]["height"] == h1


# ================================================================================================ 6 after the latch
def _latched(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched"
    return rid, rec


def test_6_transient_failures_after_the_latch_are_retried(loc, key):
    from tessera_issue.preship import PreShipUnavailable
    rid, _ = _latched(loc, key)
    real_headers, real_check = loc.iss.headers, loc.iss.preship.check
    loc.iss.headers = GappedHeaders(real_headers)          # no explorer answers
    for _ in range(3):
        poll(loc)
    assert att(get(loc, rid))["state"] == "latched"
    loc.iss.headers = real_headers

    def unavailable(*a, **k):
        raise PreShipUnavailable("SHA1DC_UNAVAILABLE")
    loc.iss.preship.check = unavailable
    poll(loc)
    loc.clock.advance(40 * DAY)                           # a long outage changes nothing
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched"
    loc.iss.preship.check = real_check
    rec = run(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1


def test_6_a_verdict_without_per_check_evidence_is_never_a_discard(loc, key):
    """Rewritten after ILI-01 (was ..._from_committed_bytes_discards_with_its_reason, which stubbed the verdict): a
    discard needs the verifier's per-row result showing the failing check depends only on frozen material. A bare
    verdict, even INVALID/SIG_INVALID, is retried. The real-outcome discards are in test_lifecycle_repairs.py."""
    rid, _ = _latched(loc, key)
    real = loc.iss.preship.check
    loc.iss.preship.check = lambda *a, **k: ({"verdict": "INVALID", "reason": "SIG_INVALID", "T": None}, {})
    poll(loc)
    poll(loc)
    loc.iss.preship.check = real
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and rec["cur"] == 1
    assert run(loc, rid)["state"] == "COMPLETE"


def test_6_a_verifier_reason_that_does_not_depend_only_on_committed_bytes_is_retried(loc, key):
    rid, _ = _latched(loc, key)
    real = loc.iss.preship.check
    loc.iss.preship.check = lambda *a, **k: ({"verdict": "UNVERIFIABLE", "reason": "HEADERS_NOT_COVERED", "T": None},
                                             {})
    for _ in range(3):
        poll(loc)
    assert att(get(loc, rid))["state"] == "latched"
    loc.iss.preship.check = real
    assert run(loc, rid)["state"] == "COMPLETE"


def test_6_T_after_not_after_is_never_shipped(loc, key):
    """A9 issuer invariant. With honest margins T <= declared + delta < not-after, so the window is moved here."""
    rid, rec = _latched(loc, key)
    t = att(rec)["latch"]["T"]
    loc.iss.window.not_after = rfc3339(t - 1)             # signing then also stopped long ago
    poll(loc)
    rec = get(loc, rid)
    assert att(rec, 1)["state"] == "discarded" and att(rec, 1)["end"]["reason"] == "T_AFTER_NOT_AFTER"
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED"
    assert not loc.iss.results.names("result", rid)


def test_6_the_preserved_presentation_is_shipped_never_a_later_one(loc, key):
    rid, rec = _latched(loc, key)
    pres = json.loads(loc.iss.results.get("work", rid, att(rec)["latch"]["ref"]))
    loc.iss.results.put("work", rid, "a1/receipt.ots", b"overwritten working copy")
    loc.iss.results.put("work", rid, "a1/receipt.upgraded.ots", b"overwritten working copy")
    rec = run(loc, rid)
    assert rec["state"] == "COMPLETE"
    bundle = json.loads(loc.iss.results.get("result", rid, "receipt.json"))
    layer = bundle["layers"][0]
    assert layer["receipt_anchor"]["ots"] == pres["ots"]
    assert {k: v for k, v in layer["headers"].items() if k in pres["headers"]} == pres["headers"]


# ================================================================================================ 7 end, allocate, refuse
def test_7_end_and_allocate_is_one_guarded_write(loc, key):
    _, rid = submit(loc, key)
    seen = saves(loc)
    rec = negative_then_next(loc, rid, 0)
    assert rec["cur"] == 2
    for r in seen:                                        # never between attempts: no stored version has an ended
        assert r["state"] != "ACCEPTED" or current(r) is None or current(r)["state"] in ("open", "latched")
    ending = [r for r in seen if r["attempts"][0]["state"] == "discarded"][0]
    assert ending["cur"] == 2 and ending["attempts"][1]["state"] == "open"


def test_7_the_third_ending_refuses_attempts_exhausted_in_the_same_write(loc, key):
    _, rid = submit(loc, key)
    seen = saves(loc)
    for n in range(1, N_ATTEMPTS + 1):
        rec = negative_then_next(loc, rid, 0)
    assert rec["state"] == "REFUSED" and rec["reason"] == "ATTEMPTS_EXHAUSTED" and rec["ended_at"] is not None
    assert [x["state"] for x in rec["attempts"]] == ["discarded"] * N_ATTEMPTS
    final = [r for r in seen if r["attempts"][-1]["state"] == "discarded" and len(r["attempts"]) == N_ATTEMPTS][0]
    assert final["state"] == "REFUSED"                    # the transition ending attempt N records the refusal
    v = api.status(loc.iss, "cred-A", key).body
    assert v["state"] == "REFUSED" and v["reason"] == "ATTEMPTS_EXHAUSTED"
    assert v["attempts"] == [{"attempt": n, "outcome": "DISCARDED", "reason": "TIME_AFTER_DECLARED_DELTA"}
                             for n in range(1, N_ATTEMPTS + 1)]
    loc.clock.advance(15 * 60)
    poll(loc)
    poll(loc)
    assert not loc.iss.results.names("work", rid) and not loc.iss.results.names("content", rid)


def test_7_signing_closed_when_the_next_attempt_would_sign_after_the_stop(loc, key):
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, max(B_of(a), loc.iss.window.sign_until) + 1)
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED"
    assert att(rec, 1)["state"] == "expired" and len(rec["attempts"]) == 1


def test_7_a_closed_signing_window_never_ends_a_signed_and_stamped_or_latched_attempt(loc):
    import uuid
    w = loc.iss.window
    loc.clock.t = w.accept_until
    k_open, k_latch = str(uuid.uuid4()), str(uuid.uuid4())
    _, r_open = submit(loc, k_open, b"open")
    _, r_latch = submit(loc, k_latch, b"latched")
    a_open, a_latch = att(to_evidence(loc, r_open)), att(to_evidence(loc, r_latch))
    loc.clock.t = w.sign_until + DAY                      # signing has stopped; nothing is buried yet
    poll(loc)
    assert only_first_open(get(loc, r_open)) and only_first_open(get(loc, r_latch))
    on_time = w.accept_until + DELTA - HOUR                # both stamps are mined on time (within declared + delta;
    loc.clock.t = on_time                                  # L1 now leaves delta + S + 24 h before the signing stop)
    bury(loc, on_time)
    loc.clock.t = w.sign_until + 2 * DAY                  # ... and first observed after the stop
    poll(loc)
    assert att(get(loc, r_latch))["state"] == "latched"
    assert run(loc, r_latch)["state"] == "COMPLETE" and run(loc, r_open)["state"] == "COMPLETE"
    assert declared(a_open) <= w.sign_until and declared(a_latch) <= w.sign_until


# ================================================================================================ 8 public view
def test_8_the_public_view_shows_attempt_i_of_N_and_B_with_the_nominal_note(loc, key):
    _, rid = submit(loc, key)
    v = api.status(loc.iss, "cred-A", key).body
    assert "fail_after" not in v and v["attempt"]["of"] == N_ATTEMPTS
    rec = to_evidence(loc, rid)
    v = api.status(loc.iss, "cred-A", key).body
    a = att(rec)
    assert v["state"] == "ACCEPTED" and "fail_after" not in v
    assert v["attempt"]["number"] == 1 and v["attempt"]["of"] == N_ATTEMPTS and v["attempt"]["state"] == "open"
    assert v["attempt"]["expiry_boundary"] == rfc3339(declared(a) + DELTA + SLACK_S)
    assert "nominal" in v["attempt"]["note"] and "twelve days" in v["attempt"]["note"]
    bury(loc, declared(a) + HOUR)
    poll(loc)
    v = api.status(loc.iss, "cred-A", key).body
    assert v["attempt"]["state"] == "latched" and "expiry_boundary" not in v["attempt"]


# ================================================================================================ 9 storage lifetime
def test_9_live_objects_are_never_marked_and_cleanup_marks_before_deleting(key):
    from tessera_issue import local
    from conftest import FROZEN
    loc = local.build(FROZEN)
    loc.iss.results = S3ResultStore(FakeS3(), "bucket")
    loc.workers["kms"].fetch = loc.workers["gpg"].fetch = loc.iss.results.get_ref
    s3 = loc.iss.results.c
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    loc.clock.t = B_of(a) + 45 * DAY                      # far older than any former age rule
    poll(loc)
    live = [k for b, k in s3.objects if k.split("/")[1] == rid]
    assert live and not [k for k in live if s3.tags.get(("bucket", k))]
    order, real_delete = [], s3.delete_objects

    def delete(**kw):
        order.append(("delete", [o["Key"] for o in kw["Delete"]["Objects"]]))
        for o in kw["Delete"]["Objects"]:
            assert s3.tags.get(("bucket", o["Key"])) == {"cleanup-due": "true"}, o["Key"]
        return real_delete(**kw)
    s3.delete_objects = delete
    bury(loc, loc.clock() + 60)                           # complete negative after B and after the signing stop
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "REFUSED" and rec["reason"] == "SIGNING_CLOSED" and order
    assert not [k for b, k in s3.objects if k.split("/")[1] == rid]


def test_9_a_failed_deletion_leaves_the_objects_marked_for_the_backstop_and_the_receipt_waits_30_days(key):
    from tessera_issue import local
    from conftest import FROZEN
    loc = local.build(FROZEN)
    loc.iss.results = S3ResultStore(FakeS3(), "bucket")
    loc.workers["kms"].fetch = loc.workers["gpg"].fetch = loc.iss.results.get_ref
    s3 = loc.iss.results.c
    s3.fail_delete = lambda k: "InternalError" if k.startswith("work/") else None
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE"
    work = [k for b, k in s3.objects if k.startswith(f"work/{rid}/")]
    assert work and all(s3.tags.get(("bucket", k)) == {"cleanup-due": "true"} for k in work)
    receipt = ("bucket", f"result/{rid}/receipt.json")
    assert receipt in s3.objects and not s3.tags.get(receipt)
    s3.fail_delete = lambda k: None
    loc.clock.t = rec["ended_at"] + RETENTION_S - 1
    poll(loc)
    assert receipt in s3.objects and not s3.tags.get(receipt)
    loc.clock.t = rec["ended_at"] + RETENTION_S
    poll(loc)
    assert receipt not in s3.objects
