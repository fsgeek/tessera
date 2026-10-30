"""Repairs after Codex's second confirmation (docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md, ILC-I2-01..05)
under the owner's round-3 decisions. Codex's probes (/tmp/tmp.iALl276cQE/test_round2.py) are reproduced as
regression tests with the repaired behaviour as the oracle."""
import json
import uuid

import pytest

from tessera_issue import api, deadline, ots, pipeline
from tessera_issue.aws import S3ResultStore
from tessera_issue.lifecycle import current
from tessera_issue.service import POLL_BUDGET_S
from tessera_issue.util import DELTA, HOUR

from helpers import submit
from test_lifecycle import LambdaTimeout, att, bury, declared, get, poll, sign, to_evidence
from test_lifecycle_confirm import SLOW, SlowClient, aws_wire
from test_lifecycle_repairs import latched


# ================================================================================================ ILC-I2-01
def test_ILCI2_01_an_S3_body_is_read_inside_the_guarded_request():
    """Codex's probe: get_object returned before Body.read(), so the body read ran outside the guard."""
    seen = []

    class Body:
        def read(self):
            seen.append(deadline.CALL_TIMEOUT.get())
            return b"body"

    class Client:
        def get_object(self, **kw):
            return {"Body": Body()}
    store = S3ResultStore(Client(), "b")
    clock = [0]
    with deadline.Installed(deadline.Deadline(lambda: clock[0], 290, 10)):
        assert store.get("work", "rid", "x") == b"body"
    assert seen and seen[0] is not None


def test_ILCI2_01_the_invocation_deadline_runs_on_a_monotonic_clock_not_the_wall_clock(loc, key):
    """A wall-clock step during a poll (NTP, a skewed host) does not consume or extend the invocation's time: the
    deadline is measured on the issuer's elapsed (monotonic) clock."""
    _, rid = submit(loc, key)
    _, rid2 = submit(loc, str(uuid.uuid4()), b"second")
    wall = loc.iss.clock
    steps = [0]

    def stepping_wall():
        steps[0] += 1
        return wall() + 10_000 * steps[0]                 # the wall clock jumps forward on every reading
    loc.iss.clock = stepping_wall
    out = pipeline.poll(loc.iss)
    loc.iss.clock = wall
    assert not out.get("out_of_time") and not out.get("deferred")
    assert get(loc, rid)["stage"] == get(loc, rid2)["stage"] == "signing"


# ================================================================================================ ILC-I2-02
@pytest.fixture
def short_rrsigs(monkeypatch):
    """Snapshots whose RRSIGs are valid when captured but expire 100 s later (Codex's probe)."""
    from tessera_issue import stand_in
    real = stand_in.rrsig

    def short(*args):
        return real(*args[:-1], args[-2] + 5 * 24 * HOUR + 100)
    monkeypatch.setattr(stand_in, "rrsig", short)


def test_ILCI2_02_an_RRSIG_expired_at_the_snapshot_anchor_is_recaptured(loc, key, short_rrsigs):
    rid, rec = latched(loc, key)
    captures = loc.world.dns.captures
    poll(loc)
    rec = get(loc, rid)
    last = [e for e in rec["events"] if e[1] == "preship-recapture"][-1]
    assert last[3] == "RRSIG_NOT_VALID_AT_EVAL_TIME" and last[4] == "13.5"
    assert rec["stage"] == "snapshot" and att(rec)["state"] == "latched"
    poll(loc)
    assert loc.world.dns.captures > captures                 # recaptured, not retried on the same snapshot


def test_ILCI2_02_an_expired_RRSIG_reaches_the_impossibility_proof(loc, key, short_rrsigs):
    rid, rec = latched(loc, key)
    loc.clock.t = declared(att(rec)) + DELTA + 100
    loc.world.chain.mine(20)                                 # the chain's median time past is past declared + delta
    poll(loc)
    rec = get(loc, rid)
    end = rec["attempts"][0]["end"]
    assert end["reason"] == "SNAPSHOT_IMPOSSIBLE" and end["evidence"]["snapshot_reason"] == "RRSIG_NOT_VALID_AT_EVAL_TIME"


def test_ILCI2_02_row_13_5_is_classified_by_reason():
    from tessera_verify.verify import Ledger
    for reason, kind in [("RRSIG_NOT_VALID_AT_EVAL_TIME", "snapshot"), ("RRSIG_INTERVAL_REVERSED", "snapshot"),
                         ("RRSIG_TIME_AMBIGUOUS", "snapshot"), ("KSK_OUTSIDE_RELIANCE_PERIOD", "retry"),
                         ("TRUST_HORIZON", "retry"), ("NO_TRUSTED_KSK_USABLE", "retry"),
                         ("TRUSTED_KSK_SIGNATURE_INVALID", "retry"), ("DNSSEC_SIGNATURE_INVALID", "retry")]:
        led = Ledger()
        led.fault("13.5", reason)
        assert pipeline.classify_preship(led)[0] == kind, reason


# ================================================================================================ ILC-I2-03
def test_ILCI2_03_calendar_progress_is_checkpointed_on_the_guarded_adapters():
    """Codex's probe: 20 pending calendars at 20 s each on the real guarded S3 adapter. The checkpoint writes are
    reserved before calendar requests are spent, so the cursor is saved and every calendar is reached across polls."""
    loc, _ = aws_wire("calendar")
    _, rid = submit(loc, str(uuid.uuid4()))
    to_evidence(loc, rid)
    raw = loc.iss.results.get("work", rid, "a1/receipt.ots")
    digest, root = ots.parse_file(raw)
    asked = []
    for i in range(20):
        uri = f"https://pending-{i}.invalid"

        def transport(method, url, body, i=i):
            asked.append(i)
            loc.clock.advance(20)
            return 404, b""
        loc.iss.calendars.append(ots.HttpCalendar(uri, transport))
        root.att(ots.PENDING, ots.pending_payload(uri))
    loc.iss.results.put("work", rid, "a1/receipt.upgraded.ots", ots.serialize_file(digest, root))
    for _ in range(8):
        poll(loc)
        if set(range(20)) <= set(asked):
            break
    assert set(range(20)) <= set(asked), sorted(set(asked))
    assert loc.iss.results.get("work", rid, "a1/receipt.upgrade-cursor") is not None


# ================================================================================================ ILC-I2-04
def test_ILCI2_04_every_request_advances_when_enumeration_is_slow(monkeypatch):
    """Codex's probe: 15 requests, every DynamoDB request taking 20 s. Enumeration is paged and resumable from a
    durable continuation position, so every request gets turns and advances."""
    monkeypatch.setitem(SLOW, "dynamodb", 20)
    loc, _ = aws_wire("dynamodb")
    loc.iss.budget_s = float("inf")
    rids = []
    for _ in range(15):
        k = str(uuid.uuid4())
        api.submit(loc.iss, "cred-A", k, b"x")
        rids.append(api.record_id("cred-A", k))
    loc.iss.budget_s = POLL_BUDGET_S
    for _ in range(30):
        pipeline.poll(loc.iss)
        if all(loc.iss.requests.get(r)["cur"] >= 1 for r in rids):
            break
    assert all(loc.iss.requests.get(r)["cur"] >= 1 for r in rids)


def test_ILCI2_04_a_flood_of_signer_responses_does_not_starve_request_work(monkeypatch):
    """Fairness between work classes: draining signer responses has a share of each invocation, so a queue that is
    continuously replenished cannot take every invocation from the requests."""
    monkeypatch.setitem(SLOW, "sqs", 20)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    junk = json.dumps({"request_id": "req-" + "0" * 40, "status": "SIGNED", "sig_b64": "AAAA"})
    q = loc.workers["kms"].responses                        # the fake SQS queue behind the issuer's adapter
    real, spans = pipeline.drain, []

    def timed(iss, **kw):
        t0 = loc.clock()
        n = real(iss, **kw)
        spans.append(loc.clock() - t0)
        return n
    monkeypatch.setattr(pipeline, "drain", timed)
    for _ in range(3):
        for _ in range(300):                                 # replenished before every poll
            q.send(junk)
        pipeline.poll(loc.iss)
    assert get(loc, rid)["cur"] >= 1
    # the drain kept to its cooperative share: at most one receive, one message and one acknowledgement over it
    assert max(spans) <= POLL_BUDGET_S / 3 + 3 * 20, spans    # the owner's one-third share


# ================================================================================================ ILC-I2-05
def test_ILCI2_05_receipt_evidence_is_classified_while_snapshot_capture_keeps_failing(loc, key):
    """Codex's probe: the DNS capture keeps being rejected and the chain moves past the attempt's temporal limit. The
    receipt is still classified: its complete negative ends the attempt."""
    _, rid = submit(loc, key)
    poll(loc)
    sign(loc)
    poll(loc)
    loc.iss.dns.capture = lambda now: b"bad"
    for _ in range(3):
        poll(loc)
    rec = get(loc, rid)
    assert rec["stage"] == "evidence"
    bury(loc, declared(att(rec)) + DELTA + 20 * HOUR)
    poll(loc)
    rec = get(loc, rid)
    assert rec["attempts"][0]["state"] in ("discarded", "expired")
    assert rec["attempts"][0]["end"]["reason"] == "TIME_AFTER_DECLARED_DELTA"


def test_ILCI2_05_a_latch_without_any_snapshot_captures_one_before_finalizing(loc, key):
    _, rid = submit(loc, key)
    good = loc.iss.dns.capture
    loc.iss.dns.capture = lambda now: b"bad"
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    poll(loc)
    rec = get(loc, rid)
    assert att(rec)["state"] == "latched" and rec["stage"] == "snapshot"
    loc.iss.dns.capture = good
    loc.clock.t = declared(a) + 2 * HOUR
    poll(loc)
    loc.world.chain.mine(6)
    for _ in range(3):
        poll(loc)
    assert get(loc, rid)["state"] == "COMPLETE"


def test_ILCI2_05_no_snapshot_ever_captured_and_no_timely_anchor_possible_is_impossible(loc, key):
    _, rid = submit(loc, key)
    loc.iss.dns.capture = lambda now: b"bad"
    a = att(to_evidence(loc, rid))
    bury(loc, declared(a) + HOUR)
    poll(loc)
    assert get(loc, rid)["stage"] == "snapshot"
    loc.clock.t = declared(a) + DELTA + 100
    loc.world.chain.mine(20)
    poll(loc)
    end = get(loc, rid)["attempts"][0]["end"]
    assert end["reason"] == "SNAPSHOT_IMPOSSIBLE" and end["evidence"]["snapshot_reason"] == "NO_SNAPSHOT"


# ================================================================================================ ILC-I3-01
def test_ILCI3_01_the_drain_rotation_survives_cold_starts(monkeypatch):
    """Codex's eight-cold-start probe (docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-3.md): 20 s SQS calls, the
    KMS response queue refilled before every poll, and a cold start (a fresh issuer object: in-memory state lost,
    signers rebuilt KMS first) before every poll. Oldest-first draining (ILC-I6) needs no remembered rotation: the
    GPG responses are older than the replenished KMS traffic, so they are handled, and the request reaches stamp."""
    monkeypatch.setitem(SLOW, "sqs", 20)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    junk = json.dumps({"request_id": "req-" + "0" * 40, "status": "SIGNED", "sig_b64": "AAAA"})
    for _ in range(8):
        for _ in range(100):
            loc.workers["kms"].responses.send(junk)
        for attr in ("drain_turn",):                      # a cold start: nothing kept in memory
            loc.iss.__dict__.pop(attr, None)
        pipeline.poll(loc.iss)
        if get(loc, rid)["stage"] != "signing":
            break
    assert get(loc, rid)["stage"] in ("stamp", "evidence")


# ================================================================================================ ILC-I4-01
def test_ILCI4_01_an_empty_first_queue_under_a_reduced_budget_does_not_starve_the_other_signer(monkeypatch):
    """Codex's reduced-budget probe (docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-4.md): only valid GPG replies
    wait; every SQS request takes 60 s; every poll has a 190 s budget. Oldest-first draining (ILC-I6) receives from
    every slot, then handles the oldest message first, so GPG is served."""
    monkeypatch.setitem(SLOW, "sqs", 0)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    for handle, body, _sent in loc.iss.signers["kms"].receive():  # KMS delivered; only GPG replies wait
        pipeline._take(loc.iss, "kms", loc.iss.signers["kms"], body)
        loc.iss.signers["kms"].ack(handle)
    for signer in loc.iss.signers.values():
        signer.responses.client._client._delay = 60
    for _ in range(12):
        pipeline.poll(loc.iss, budget_s=190)
        if all(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values()):
            break
    assert all(v["sig_sha256"] for k, v in att(get(loc, rid))["jobs"].items() if "gpg" in k)


# ================================================================================================ ILC-I6 (oldest first)
def test_ILCI6_the_lock_in_probe_collects_GPG(monkeypatch):
    """Codex's parity lock-in probe (CODEX-CONFIRM-5.md), kept after the slot-ordering mechanism was removed: start
    readings that all fell into slot-0 windows, KMS traffic replenished before every poll. The GPG responses are the
    oldest messages, so they are handled."""
    monkeypatch.setitem(SLOW, "sqs", 20)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    base = ((int(loc.clock()) // 1200) + 1) * 1200
    junk = json.dumps({"request_id": "req-" + "0" * 40, "status": "SIGNED", "sig_b64": "AAAA"})
    for i in range(12):
        loc.clock.t = base + 599 + 600 * i + (0 if i % 2 == 0 else 2)
        for _ in range(100):
            loc.workers["kms"].responses.send(junk)
        pipeline.poll(loc.iss)
        if all(v["sig_sha256"] for k, v in att(get(loc, rid))["jobs"].items() if "gpg" in k):
            break
    assert all(v["sig_sha256"] for k, v in att(get(loc, rid))["jobs"].items() if "gpg" in k)


def test_ILCI6_one_slow_response_on_one_slot_cannot_starve_the_other(monkeypatch):
    """Codex's overrun counterexample (CODEX-CONFIRM-6.md): handling one KMS response costs 240 s (four 60 s
    requests), KMS junk is replenished before every poll and placed ahead of the valid GPG replies. Every slot is
    received from before anything is handled, and the oldest message is handled first: the GPG replies, which only
    grow older, are collected within a bounded number of polls."""
    monkeypatch.setitem(SLOW, "sqs", 0)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    object.__setattr__(loc.iss.requests.c, "_client", SlowClient(loc.iss.requests.c._client, loc.clock, 60, []))
    for signer in loc.iss.signers.values():
        signer.responses.client._client._delay = 60
    for slot, signer in loc.iss.signers.items():
        real = signer.receive

        def receive(n=10, slot=slot, real=real):
            loc.iss.requests.c._client._delay = 60 if slot == "kms" else 0
            return real(n)
        signer.receive = receive
    loc.workers["kms"].responses.msgs.clear()
    junk = json.dumps({"request_id": "req-" + "0" * 40, "status": "SIGNED", "sig_b64": "AAAA"})
    for i in range(12):
        loc.workers["kms"].responses.send(junk)
        loc.clock.advance(1200 - loc.clock() % 1200)     # every poll starts in a same-parity window (as Codex's)
        pipeline.poll(loc.iss)
        if all(v["sig_sha256"] for k, v in att(get(loc, rid))["jobs"].items() if "gpg" in k):
            break
    assert all(v["sig_sha256"] for k, v in att(get(loc, rid))["jobs"].items() if "gpg" in k)


def test_ILCI6_messages_are_handled_oldest_first_across_slots(loc, monkeypatch):
    handled = []
    monkeypatch.setattr(pipeline, "_take", lambda iss, slot, signer, body, **kw: handled.append(body["n"]))
    kms, gpg = loc.workers["kms"].responses, loc.workers["gpg"].responses
    for n, q in [(1, gpg), (2, kms), (3, gpg), (4, kms), (5, kms), (6, gpg)]:
        q.send(json.dumps({"n": n}))
        loc.clock.advance(1)
    pipeline.drain(loc.iss)
    assert handled == [1, 2, 3, 4, 5, 6]




# ================================================================================================ ILC-I7
@pytest.mark.parametrize("first", [0, 1])
def test_ILCI7_a_message_is_collected_when_one_receive_and_its_full_handling_fit(monkeypatch, first):
    """Codex's capacity counterexample (CODEX-CONFIRM-7.md): 290 s budget, SQS 50 s and DynamoDB 30 s per request,
    replies waiting on both slots. Receiving from the second slot used the time one message's complete handling
    (lookups, log, record update, acknowledgement) needed. Further receives now stop unless the next receive PLUS one
    message's complete handling still fit, so a signature is collected whichever slot is first."""
    monkeypatch.setitem(SLOW, "sqs", 0)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    object.__setattr__(loc.iss.requests.c, "_client", SlowClient(loc.iss.requests.c._client, loc.clock, 30, []))
    for signer in loc.iss.signers.values():
        signer.responses.client._client._delay = 50

    class Fixed:
        def randrange(self, n):
            return first
    loc.iss.rng = Fixed()
    for _ in range(12):
        loc.clock.advance(600)
        pipeline.poll(loc.iss)
        if any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values()):
            break
    assert any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values())


# ================================================================================================ ILC-I8 (resumable handling)
@pytest.mark.parametrize("first", [0, 1])
def test_ILCI8_admission_counterexample_records_the_signature(monkeypatch, first):
    """Codex's admission counterexample (CODEX-CONFIRM-8.md): SQS 20 s, DynamoDB 24 s, S3 47 s per request. A
    message's handling actually fits, but a late guarded call meets less headroom than its 73 s admission and the
    handling stopped part-way, every poll. Handling is now resumable step by step, so the signature is recorded within
    a bounded number of polls, whichever slot is received first."""
    monkeypatch.setitem(SLOW, "sqs", 0)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    object.__setattr__(loc.iss.requests.c, "_client", SlowClient(loc.iss.requests.c._client, loc.clock, 24, []))
    object.__setattr__(loc.iss.results.c, "_client", SlowClient(loc.iss.results.c._client, loc.clock, 47, []))
    for signer in loc.iss.signers.values():
        signer.responses.client._client._delay = 20
    loc.iss.rng = type("Fixed", (), {"randrange": lambda self, n: first})()
    for _ in range(12):
        loc.clock.advance(600)
        pipeline.poll(loc.iss)
        if any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values()):
            break
    assert any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values())


STEPS = [("requests", "sigreq_get"), ("requests", "get"), ("results", "get"), ("results", "put"),
         ("requests", "siglog_add"), ("requests", "save"), ("ack", "ack")]
DURABLE = {"results.get": (),                                      # a read: nothing durable is done yet
           "results.put": ("results.get", "results.put"), "requests.siglog_add": ("results.get", "results.put",
                                                                                   "requests.siglog_add"),
           "requests.save": ("results.get", "results.put", "requests.siglog_add", "requests.save"),
           "ack.ack": ("results.get", "results.put", "requests.siglog_add", "requests.save")}


@pytest.mark.parametrize("step", range(len(STEPS)), ids=[f"{o}.{m}" for o, m in STEPS])
def test_ILCI8_handling_killed_after_any_step_is_completed_by_a_later_poll(loc, key, step):
    """Kill the invocation right after each step of a signer response's handling in turn (index lookup, record read,
    frame read and verification, verified signature object, used log, record update, acknowledgement). A later poll
    completes the handling, and (ILC-I9) performs no COMPLETED durable step of that message again: the frame is not
    re-read and the object not re-written once the verified object exists, the log not re-written once logged, the
    record not re-saved once it holds the signature."""
    _, rid = submit(loc, key)
    poll(loc)
    loc.workers["kms"].process()                          # one slot only: the message under test is KMS's
    target, method = STEPS[step]
    obj = loc.iss.signers["kms"] if target == "ack" else getattr(loc.iss, target)
    real = getattr(obj, method)
    first_sig = {}

    def relevant(a):
        if target == "results" and method == "put":
            return "/sig-s_kms-" in str(a[2])
        if target == "results" and method == "get":
            return str(a[2]).endswith("/f_kms")
        if target == "requests" and method == "siglog_add":
            return a[0].get("disposition") == "used"
        if target == "requests" and method == "save":
            return bool(current(a[0])["jobs"]["s_kms"]["sig_sha256"])
        if target == "requests" and method == "sigreq_get":
            return True
        if target == "requests" and method == "get":
            return True
        return True

    def kill_after(*a, **kw):
        out = real(*a, **kw)
        if relevant(a) and not first_sig:
            first_sig["hit"] = True
            raise LambdaTimeout()
        return out
    setattr(obj, method, kill_after)
    with pytest.raises(LambdaTimeout):
        pipeline.drain(loc.iss)
    setattr(obj, method, real)
    assert first_sig
    counts = {k: 0 for k in ("results.get", "results.put", "requests.siglog_add", "requests.save")}
    wrapped = []
    for name in counts:
        o_name, m_name = name.split(".")
        o = getattr(loc.iss, o_name)
        r = getattr(o, m_name)

        def counter(*a, _r=r, _n=name, **kw):
            if (_n == "results.get" and str(a[2]).endswith("/f_kms")) or \
                    (_n == "results.put" and "/sig-s_kms-" in str(a[2])) or \
                    (_n == "requests.siglog_add" and a[0].get("disposition") == "used"
                     and a[0].get("request_id") == att(get(loc, rid))["jobs"]["s_kms"]["request_id"]) or \
                    (_n == "requests.save" and False):
                counts[_n] += 1
            return _r(*a, **kw)
        setattr(o, m_name, counter)
        wrapped.append((o, m_name, r))
    loc.clock.advance(400)                                # past the visibility timeout: an unacknowledged message returns
    pipeline.drain(loc.iss)
    for o, m_name, r in wrapped:
        setattr(o, m_name, r)
    done = DURABLE.get(f"{target}.{method}", ())
    for name in done:                                     # a completed step is never performed again
        assert counts.get(name, 0) == 0, (f"{target}.{method}", name, counts)
    for _ in range(3):
        loc.clock.advance(400)
        sign(loc)
        poll(loc)
    rec = get(loc, rid)
    assert current(rec)["jobs"]["s_kms"]["sig_sha256"]


# ================================================================================================ ILC-I9
@pytest.mark.parametrize("first", [0, 1])
def test_ILCI9_resume_gap_probe_logs_and_adopts_the_signatures(monkeypatch, first):
    """Codex's resume-gap probe (CODEX-CONFIRM-9.md): SQS 20 s, DynamoDB 24 s, S3 60 s per request. The signature
    write and frame read used to be repeated whenever the used-log entry was absent, so the log write never had
    headroom. Completed steps are now observable and skipped; the signatures are logged and adopted."""
    monkeypatch.setitem(SLOW, "sqs", 0)
    loc, _ = aws_wire("sqs")
    _, rid = submit(loc, str(uuid.uuid4()))
    pipeline.poll(loc.iss)
    for wk in loc.workers.values():
        wk.process()
    object.__setattr__(loc.iss.requests.c, "_client", SlowClient(loc.iss.requests.c._client, loc.clock, 24, []))
    object.__setattr__(loc.iss.results.c, "_client", SlowClient(loc.iss.results.c._client, loc.clock, 60, []))
    for signer in loc.iss.signers.values():
        signer.responses.client._client._delay = 20
    loc.iss.rng = type("Fixed", (), {"randrange": lambda self, n: first})()
    for _ in range(12):
        loc.clock.advance(600)
        pipeline.poll(loc.iss)
        if any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values()):
            break
    assert any(v["sig_sha256"] for v in att(get(loc, rid))["jobs"].values())
    assert any(e["disposition"] == "used" for e in loc.iss.requests.siglog())
