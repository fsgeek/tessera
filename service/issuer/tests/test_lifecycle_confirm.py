"""Repairs after Codex's confirmation review (docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM.md, ILC-I-01..05;
ILC-I-06 is documentation). Codex's probes (/tmp/tmp.lgKk0SQtBY/test_confirmation.py) are reproduced as regression
tests with the repaired behaviour as the oracle; ILC-I-02 is tested for every client kind the poller uses."""
import copy
import uuid

import pytest

from tessera_issue import api, deadline, ots, pipeline
from tessera_issue.aws import DynamoRequestStore, S3ResultStore, SnsWake
from tessera_issue.chain import ExplorerHeaders
from tessera_issue.dns import LiveDns
from tessera_issue.ots import HttpCalendar
from tessera_issue.queues import SqsQueue
from tessera_issue.service import POLL_BUDGET_S, POLL_RESERVE_S
from tessera_issue.signers import SlotSigner, StandInSigner
from tessera_issue.util import DELTA, HOUR, rfc3339

from conftest import FROZEN
from fakes import FakeDynamo, FakeS3, FakeSns, FakeSqs
from helpers import submit
from test_lifecycle import att, bury, declared, get, poll, to_evidence
from test_lifecycle_repairs import SlowHeaders, latched


# ================================================================================================ ILC-I-01
def test_ILCI01_a_trust_configuration_failure_of_a_timely_snapshot_is_retried_and_ships_after_repair(loc, key):
    """Codex's KSK-interval probe: both proofs anchored on time, the chain far past the MTP threshold, and only the
    configured KSK interval broken. Row 13.5 depends on the trust configuration, so it is neither a recapture nor a
    SNAPSHOT_IMPOSSIBLE discard: the attempt and its snapshot are kept, and after the repair it ships."""
    rid, rec = latched(loc, key)
    a = att(rec)
    loc.clock.t = declared(a) + DELTA + 100
    loc.world.chain.mine(20)
    saved = copy.deepcopy(loc.iss.preship.trust_base["root_ksks"])
    loc.iss.preship.trust_base["root_ksks"][0]["signing_start"] = rfc3339(declared(a) + 2 * HOUR)
    body = loc.iss.results.get("work", rid, "a1/snapshot.body")
    for _ in range(3):
        poll(loc)
    rec = get(loc, rid)
    assert rec["cur"] == 1 and att(rec)["state"] == "latched" and rec["stage"] == "finalize"
    assert "KSK_OUTSIDE_RELIANCE_PERIOD" in [e for e in rec["events"] if e[1] == "preship-retry"][-1][3]
    assert not [e for e in rec["events"] if e[1] == "preship-recapture"]
    assert loc.iss.results.get("work", rid, "a1/snapshot.body") == body       # the timely snapshot is kept
    loc.iss.preship.trust_base["root_ksks"] = saved
    poll(loc)
    rec = get(loc, rid)
    assert rec["state"] == "COMPLETE" and len(rec["attempts"]) == 1


def test_ILCI01_the_snapshot_classification_keeps_configuration_rows_out_of_byte_only_rows():
    from tessera_verify.verify import Ledger
    # ("13.5", "RRSIG_NOT_VALID_AT_EVAL_TIME") moved to "snapshot" by the owner's ILC-I2-02 decision (the snapshot's
    # own RRSIG times at its anchored time); see test_lifecycle_round3.py
    for row, reason, kind in [("13.5", "KSK_OUTSIDE_RELIANCE_PERIOD", "retry"), ("13.5", "RRSIG_NOT_VALID_AT_EVAL_TIME",
                                                                                   "snapshot"),
                              ("13.4", "OTS_MERKLE_MISMATCH", "retry"), ("13.7", "SNAPSHOT_TIME", "snapshot"),
                              ("13.4", "SNAPSHOT_STAMP_MISMATCH", "snapshot"), ("15.1", "DNS_KEY_MISMATCH", "snapshot")]:
        led = Ledger()
        led.fault(row, reason)
        assert pipeline.classify_preship(led)[0] == kind, (row, reason)
    assert pipeline._snapshot_impossible(None, None, None, {"row": "13.5", "reason": "KSK_OUTSIDE_RELIANCE_PERIOD"}) \
        is None


# ================================================================================================ ILC-I-02
SLOW = {"dynamodb": 60, "s3": 60, "sqs": 60, "sns": 60, "calendar": 15, "explorer": 15, "dns": 15, "preship": 25}


class SlowClient:
    """A client (or transport) whose every request takes `delay` seconds of the issuer's clock, recording the
    timeout the deadline passed it (deadline.CALL_TIMEOUT) and the time left when it started."""

    def __init__(self, target, clock, delay, log):
        self._t, self._clock, self._delay, self._log = target, clock, delay, log

    def _slow(self, fn, *a, **kw):
        d = deadline.CURRENT.get()
        if d is not None:
            self._log.append((deadline.CALL_TIMEOUT.get(), d.remaining()))
        self._clock.advance(self._delay)
        return fn(*a, **kw)

    def __getattr__(self, name):
        attr = getattr(self._t, name)
        if not callable(attr) or name in ("q", "generate_presigned_url"):
            return attr
        return lambda *a, **kw: self._slow(attr, *a, **kw)

    def __call__(self, *a, **kw):
        return self._slow(self._t, *a, **kw)


def aws_wire(slow_kind):
    """A local issuer whose every client is the real adapter over a fake (DynamoDB, S3, SQS, SNS) or the real
    protocol client over a stand-in transport (calendar, explorers, resolver); one kind is slow."""
    from tessera_issue import local
    loc = local.build(FROZEN)
    clock, world, iss, log = loc.clock, loc.world, loc.iss, []

    def slow(kind, target):
        return SlowClient(target, clock, SLOW[kind], log) if kind == slow_kind else target
    ddb, s3, sqs, sns = FakeDynamo(), FakeS3(), FakeSqs(clock), FakeSns()
    iss.requests = DynamoRequestStore(slow("dynamodb", ddb), "t")
    iss.results = S3ResultStore(slow("s3", s3), "b")
    wake = SnsWake(slow("sns", sns), {"kms": "arn:kms", "gpg": "arn:gpg"})
    q = slow("sqs", sqs)
    iss.signers = {"kms": SlotSigner("kms", world.kms_key.spki, SqsQueue(q, "kms-req"), SqsQueue(q, "kms-resp"), wake),
                   "gpg": SlotSigner("gpg", world.gpg_key.pgp_body, SqsQueue(q, "gpg-req"), SqsQueue(q, "gpg-resp"),
                                     wake)}
    loc.workers = {s: StandInSigner(s, k, sqs.q(f"{s}-req"), sqs.q(f"{s}-resp"), clock,
                                    sign_until=iss.window.sign_until, fetch=iss.results.get_ref)
                   for s, k in (("kms", world.kms_key), ("gpg", world.gpg_key))}
    iss.calendars = [HttpCalendar(world.calendar.uri, slow("calendar", world.calendar.serve))]
    iss.headers = ExplorerHeaders(["https://explorer-a.invalid/api", "https://explorer-b.invalid/api"],
                                  slow("explorer", world.chain.serve_esplora))
    iss.dns = LiveDns(slow("dns", world.dns.serve(clock)))
    if slow_kind == "preship":
        real = iss.preship.check
        iss.preship.check = lambda *a, **kw: SlowClient(real, clock, SLOW["preship"], log)(*a, **kw)
    return loc, log


@pytest.mark.parametrize("kind", sorted(SLOW))
def test_ILCI02_no_poll_exceeds_its_budget_whichever_client_is_slow(kind):
    loc, log = aws_wire(kind)
    key = str(uuid.uuid4())
    loc.iss.budget_s = float("inf")
    r = api.submit(loc.iss, "cred-A", key, b"slow clients")                  # the API is not the poller
    assert r.status == 202, r.body
    loc.iss.budget_s = POLL_BUDGET_S
    rid = api.record_id("cred-A", key)
    spans = []
    for _ in range(40):
        for w in loc.workers.values():
            w.process()
        start = loc.clock()
        pipeline.poll(loc.iss)
        spans.append(loc.clock() - start)
        loc.clock.advance(600)
        loc.world.chain.mine(1)
        if loc.iss.requests.get(rid)["state"] != "ACCEPTED":
            break
    assert log, "the slow client was never called inside a poll"
    assert max(spans) <= POLL_BUDGET_S - POLL_RESERVE_S, (kind, max(spans))
    for timeout, remaining in log:                       # (b) each request's timeout is no larger than what remains
        # a request made outside the guard has no CALL_TIMEOUT: this detects a client kind that bypasses it
        assert timeout is not None and timeout <= remaining - POLL_RESERVE_S + 1e-9


def test_ILCI02_the_worst_case_counts_explorers_and_retry_attempts():
    from tessera_issue.service import AWS_CLIENT_CONFIG as c
    attempts = c["retries"]["total_max_attempts"]
    assert deadline.AWS_WORST_S == attempts * (c["connect_timeout"] + c["read_timeout"]) + (attempts - 1) * 20
    three = ExplorerHeaders(["https://a.invalid", "https://b.invalid", "https://c.invalid"], lambda *a: (200, b"0"))
    assert three.height_worst_s() == 2 * 3 * deadline.HTTP_WORST_S and three.tip_worst_s() == 3 * deadline.HTTP_WORST_S


# ================================================================================================ ILC-I-03
def test_ILCI03_a_stale_stored_header_is_refreshed_across_invocations(loc, key):
    """Codex's six-poll probe: a stale stored header at h + 4, explorers at 12 s per request. The stored set is
    invalidated durably and refreshed across invocations; the attempt latches."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    h = bury(loc, declared(a) + HOUR)
    for i, raw in loc.iss.headers.headers(range(h, h + 6)).items():
        if i == h + 4:
            raw = raw[:76] + bytes(x ^ 1 for x in raw[76:])
        loc.iss.results.put("work", rid, f"a1/hdr/{i}", raw)
    slow = SlowHeaders(loc.iss.headers, loc.clock)
    loc.iss.headers = slow
    for _ in range(6):
        poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] in ("latched", "shipped") and h + 4 in slow.calls


# ================================================================================================ ILC-I-04
def test_ILCI04_persistent_snapshot_rejection_reaches_the_impossibility_proof(loc, key):
    """Codex's probe: a late, complete snapshot first causes a recapture (MTP not yet past); after further chain
    progress the captures keep being rejected. The snapshot stage evaluates the proof before capturing and discards
    the attempt SNAPSHOT_IMPOSSIBLE with its evidence."""
    rid, rec = latched(loc, key)
    a = att(rec)
    loc.clock.t = declared(a) + DELTA + 100
    pipeline.st_snapshot(loc.iss, rec, loc.clock())
    loc.world.chain.mine(6)
    poll(loc)
    assert get(loc, rid)["stage"] == "snapshot"
    loc.world.chain.mine(20)
    loc.iss.dns.capture = lambda now: b"invalid DNS snapshot"
    poll(loc)
    rec = get(loc, rid)
    end = rec["attempts"][0]["end"]
    assert end["reason"] == "SNAPSHOT_IMPOSSIBLE" and end["evidence"]["snapshot_reason"] == "SNAPSHOT_TIME"
    assert rec["cur"] == 2


# ================================================================================================ ILC-I-05
class PendingCalendar:
    def __init__(self, i, clock, asked):
        self.uri, self.clock, self.asked = f"https://pending-{i}.invalid", clock, asked

    def fetch(self, msg):
        self.asked.append(self.uri)
        self.clock.advance(20)
        return None


def _with_pending_calendars(loc, rid, n, base):
    asked = []
    digest, root = ots.parse_file(base)
    for i in range(n):
        cal = PendingCalendar(i, loc.clock, asked)
        loc.iss.calendars.append(cal)
        root.att(ots.PENDING, ots.pending_payload(cal.uri))
    loc.iss.results.put("work", rid, "a1/receipt.upgraded.ots", ots.serialize_file(digest, root))
    return asked


def test_ILCI05_qualifying_evidence_already_held_latches_before_pending_calendars_are_asked(loc, key):
    """Codex's twelve-pending-calendars probe: the held proof already qualifies; it latches in the first poll."""
    _, rid = submit(loc, key)
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    raw, _ = ots.upgrade(loc.iss.results.get("work", rid, "a1/receipt.ots"), loc.iss.calendars)
    asked = _with_pending_calendars(loc, rid, 12, raw)
    poll(loc)
    assert att(get(loc, rid))["state"] == "latched" and asked == []


def test_ILCI05_pending_calendars_are_served_in_turn_across_invocations(loc, key):
    _, rid = submit(loc, key)
    to_evidence(loc, rid)                                 # nothing mined: nothing qualifies yet
    asked = _with_pending_calendars(loc, rid, 20, loc.iss.results.get("work", rid, "a1/receipt.ots"))
    seen = []
    for _ in range(3):
        n = len(asked)
        poll(loc)
        seen.append(asked[n:])
    assert all(0 < len(p) < 20 for p in seen)             # no single invocation can serve them all
    first_round = [u for poll_asked in seen for u in poll_asked][:20]
    assert len(first_round) == 20 and len(set(first_round)) == 20   # each asked once before any is asked again


@pytest.mark.parametrize("kind,delay", [("dynamodb", 20), ("s3", 10), ("sqs", 60), ("sns", 60), ("calendar", 15),
                                        ("explorer", 15), ("dns", 15), ("preship", 25)])
def test_ILCI02_slow_clients_still_make_progress_within_the_budget(kind, delay, monkeypatch):
    """Progress, not only the bound: at these per-request latencies the request completes across invocations, and
    no invocation exceeds its budget. (Measured limit, not a guarantee: with every DynamoDB request taking 30 s or
    every S3 request 20 s, a stage needs more requests than one invocation admits, and the request stalls without
    any invocation overrunning; see DESIGN.md "Invocation budget".)"""
    monkeypatch.setitem(SLOW, kind, delay)
    loc, log = aws_wire(kind)
    key = str(uuid.uuid4())
    loc.iss.budget_s = float("inf")
    api.submit(loc.iss, "cred-A", key, b"slow clients")
    loc.iss.budget_s = POLL_BUDGET_S
    rid = api.record_id("cred-A", key)
    spans = []
    for _ in range(40):
        for w in loc.workers.values():
            w.process()
        start = loc.clock()
        pipeline.poll(loc.iss)
        spans.append(loc.clock() - start)
        loc.clock.advance(600)
        loc.world.chain.mine(1)
        if loc.iss.requests.get(rid)["state"] != "ACCEPTED":
            break
    assert loc.iss.requests.get(rid)["state"] == "COMPLETE" and log
    assert max(spans) <= POLL_BUDGET_S - POLL_RESERVE_S
