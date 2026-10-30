"""The stage pipeline and the scheduled poller (DESIGN.md "Pipeline"), implementing the registered issuance lifecycle
(A2.1-A2.3, A9.2, A9.5; docs/decisions/2026-10-29-issuance-lifecycle.md revision 5.3.1, "What the issuer does" and
"Implementation boundary until the author decides"). The checked protocol is
formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla; code paths are named after its actions where natural.

ONE LIFECYCLE WRITER (step 1). Only this poller (reserved concurrency 1) starts, latches, discards, expires, ships or
refuses. The API is read-only for the lifecycle. Every lifecycle write is guarded on (request state, current attempt
id, current attempt state) and the record version (stores.lifecycle_guard), so a write meant for an ended attempt, or
decided on a version it did not read, fails its guard (the model's GuardOK).

Each poll first drains every signer response queue (E-02), then advances each ACCEPTED request by at most one stage,
then works off cleanup obligations. Stages of the current attempt (attempt material lives under work/<rid>/<attempt>/):

  upload    the API owns the record before it stores the content (IS-05); an upload never finished within
            UPLOAD_GRACE_S is FAILED (CONTENT_UNAVAILABLE) - no attempt exists yet
  frames    Start (attempt 1 only; later attempts are allocated by the write that ends their predecessor): the
            attempt's declared issue time is its allocation time. Build both frames, enqueue the four signing jobs
            with request ids derived from (request, attempt, frame)
  signing   wait for all four; re-send unanswered jobs with the same id; then verify each on its exact bytes, freeze
            them, build A_sig and check it with the verifier's decoders                (profile 4 steps 2-6; A9.5)
  stamp     after the git assertion's proof has k = 6: one fresh stamp of SHA-256(A_sig) for this attempt; capture,
            validate and stamp the DNSSEC snapshot envelope
  evidence  the attempt is OPEN. Fence, Fetch, Send (below): latch on eligibility; discard (at or before B) or expire
            (after B) only on COMPLETE negative evidence; anything else leaves it open
  finalize  the attempt is LATCHED. Fence; complete the snapshot's confirmation and the headers; assemble with the
            PRESERVED presentation; pre-ship checks (verifier library); ship, or recapture the snapshot, or retry, or
            discard only for a failure the frozen attempt cannot cure (step 7: classify_preship, by the failing
            verifier row's dependency; or SNAPSHOT_IMPOSSIBLE, proven from the chain's median time past)
  snapshot  latched, re-capturing the DNSSEC snapshot after a snapshot-rule pre-ship failure

DEADLINE (ILI-05, ILC-I-02). One poll runs under one deadline (deadline.py): every client request (DynamoDB, S3, SQS,
SNS, calendars, explorers, DNS) and the pre-ship check is admitted only if its worst case fits the time left, with its
timeout capped to that. Units of work (a header height, a tip) are pre-checked against the clients' computed worst
cases; fetched headers and calendar answers are checkpointed; requests are served round-robin from a durable cursor;
running out of time never ends an attempt.

EVIDENCE (steps 3-5). Fence: a guarded write that bumps the version, committed before anything is fetched; a write
left pending by a killed earlier invocation then fails its guard (R5-F3). Fetch: the wall reading is taken before the
fetch starts (R5-F1); the attempt's proof is upgraded from its calendars and the full pinned, linked h..h+5 segment is
fetched for every Bitcoin attestation; the verifier's own `select` picks the lowest qualifying height. Eligible: that
presentation satisfies the three A2.2 conjuncts (declared - eps <= T, T <= declared + delta, confirmed_at <= declared +
delta). Complete: every calendar the attempt was stamped to has attested, and every attestation's segment was
obtained. Send: eligible -> latch (any time while open, however late); complete and failing -> discard / expire;
otherwise no lifecycle transition: stale, pending, partial or failed evidence never ends an attempt.

GATED (design step 5, until a signed amendment decides it): an attempt whose evidence never completes stays open.
Nothing here commits EVIDENCE_UNAVAILABLE, ends or allocates because of unavailability, or derives a refusal, cleanup
or terminal status from it, and no timeout or age rule ends an attempt indirectly. `unavailable_since` and
`failed_intervals` are recorded for diagnosis only; no decision reads them.

END AND ALLOCATE (step 8): ending attempt i and allocating i + 1 (fresh declared time; its frames, signatures and
stamp follow) is one guarded write; ending attempt N records REFUSED ATTEMPTS_EXHAUSTED in the same write, listing each
attempt's reason. If the next attempt would need signing after the signing stop, the request is REFUSED SIGNING_CLOSED
instead. A closed signing window never ends a latched or signed-and-stamped attempt; it ends only an attempt that still
needs signing.

Cleanup (IS-07, revision 5.3.1): ending a request first records a cleanup obligation, then commits the end, then
deletes. Each poll retries outstanding obligations: content, work files and frames once the request has ended; the
receipt (and anything left) 30 days after the end. Before deleting, the obligation tags the objects cleanup-due (the
S3 lifecycle backstop expires only tagged objects). An obligation is dropped only when the listing shows nothing
left, and not before the late writers' lease (WRITE_LEASE_S, CF-02) has run out."""
import json
import re
from dataclasses import dataclass, field
from types import SimpleNamespace

from tessera_verify.anchors import parse_ots, select
from tessera_verify.codec import Fault, read_anchor, read_frame, registered_codecs
from tessera_verify.dnssec import parse_snapshot, txt_value, validate_snapshot
from tessera_verify.verify import ROWS

from . import deadline, ots
from .api import content_name
from .deadline import OutOfBudget
from .chain import check_links, pin_of
from .encode import common_metadata, encode_anchor, encode_attest, encode_manifest, encode_snapshot_envelope
from .lifecycle import DISCARDED, ENDED, EXPIRED, LATCHED, OPEN, OUTCOME, SHIPPED, B_of, current, new_attempt
from .preship import PreShipUnavailable, check_config
from .service import N_ATTEMPTS, POLL_INTERVAL_S, POLL_RESERVE_S, RETENTION_S, WRITE_LEASE_S
from .signers import request_id
from .stores import lifecycle_guard
from .util import (ALG, DELTA, EPS, K, POLICY_VERSION, PROFILE, b64d, b64e, jcs, rfc3339, sha256, sha256hex, ts)

JOBS = (("s_kms", "kms", "f_kms"), ("p_kms", "kms", "manifest"), ("s_gpg", "gpg", "f_gpg"), ("p_gpg", "gpg", "manifest"))
UPLOAD_GRACE_S = 15 * 60          # IS-05: an API call lasts at most 29 s; an upload not finished by then was abandoned
MERGE_ATTEMPTS = 5                # IS-08: compare-and-set retries when recording a verified signature
FAILED_INTERVAL_RUNS = 256        # diagnostic failure history: at most this many runs of consecutive intervals kept
# ILI-01: post-latch pre-ship failures are classified by what the failing verifier check depends on (rows of the
# service verifier's ledger, tessera_verify.verify.ROWS), not by a reason-code list alone:
#   FROZEN      the attempt's committed bytes (frames, frozen signatures, A_sig, manifest, the window's keys), the
#               PRESERVED receipt presentation (pruned proof and its segment), or the window's frozen git material.
#               Recovering evidence cannot change them: an INVALID result here discards the attempt (step 7).
#   SNAPSHOT    the DNSSEC snapshot (rows 13.x) and what is read from it (15.x): replaceable by recapture, unless no
#               lawful snapshot can be obtained for this frozen attempt any more (ILI-02, proven from evidence).
#   anything else (pins and headers 10.x, container 1.x-2.x, catalog/config 7.1, 8.1, 8.3, 8.4, 17.x, the trust
#               configuration's repository-key intervals 14.7, every UNVERIFIABLE result): the issuer's or the
#               operator's to repair; retried, never a reason to discard.
FROZEN_ROWS = {"3.1", "4.1", "4.2", "5.1", "5.2", "6.1", "6.2", "6.3", "8.2", "8.5", "9.1", "9.2", "9.3", "9.4", "9.5",
               "11.1", "11.2", "11.3", "11.4", "11.5", "12.1", "12.2", "12.3",
               "14.1", "14.2", "14.3", "14.4", "14.5", "14.6", "14.8", "16.1"}
SNAPSHOT_ROWS = {"13.1", "13.2", "13.3", "13.4", "13.5", "13.6", "13.7", "15.1", "15.2"}
# ILC-I-01: snapshot checks whose INVALID result depends only on the snapshot's own bytes (body, proof, and the chain
# position its complete proof fixes) and frozen material - never on the trust configuration. Enumerated from the
# verifier (tessera_verify/verify.py, rows 13.x and 15.x):
#   13.1 LENGTH_CAP, 13.2 parse_snapshot, 13.3 DNS_WILDCARD, 13.6 owner and TXT grammar   - snapshot body
#   13.4 SNAPSHOT_STAMP_MISMATCH / OTS_FORMAT                 - snapshot body against its proof
#   13.7 SNAPSHOT_TIME                                        - the complete proof's anchor against declared time
#   15.1 DNS_KEY_MISMATCH, 15.2 CHANNEL_VALUE_MISMATCH        - snapshot TXT value against frozen keys / git blob
#   13.5 RRSIG_NOT_VALID_AT_EVAL_TIME, RRSIG_INTERVAL_REVERSED, RRSIG_TIME_AMBIGUOUS
#                                                             - ILC-I2-02: the snapshot's own RRSIG times against
#        its ANCHORED evaluation time (dnssec.rrsig_time; in the root group it runs only after a configured key has
#        verified the signature). Waiting cannot repair that interval; a new snapshot can.
# Configuration-dependent, so never a ground to recapture or discard (retried until the configuration or evidence is
# repaired): every other 13.5 outcome (validate_snapshot against the configured root KSKs, their reliance periods and
# the trust horizon - KSK_OUTSIDE_RELIANCE_PERIOD, NO_TRUSTED_KSK_USABLE, TRUSTED_KSK_SIGNATURE_INVALID,
# TRUST_HORIZON - and, conservatively, the chain of trust built on them: signature, key, DS and metadata outcomes),
# and 13.4's other outcomes (OTS_MERKLE_MISMATCH, SNAPSHOT_NOT_ANCHORED: the pinned headers).
SNAPSHOT_BYTES_ROWS = {"13.1", "13.2", "13.3", "13.6", "13.7", "15.1", "15.2"}
SNAPSHOT_BYTES_13_4 = {"SNAPSHOT_STAMP_MISMATCH", "OTS_FORMAT"}
SNAPSHOT_BYTES_13_5 = {"RRSIG_NOT_VALID_AT_EVAL_TIME", "RRSIG_INTERVAL_REVERSED", "RRSIG_TIME_AMBIGUOUS"}


def snapshot_bytes_only(check):
    return check.status == "invalid" and (check.row in SNAPSHOT_BYTES_ROWS
                                          or (check.row == "13.4" and check.reason in SNAPSHOT_BYTES_13_4)
                                          or (check.row == "13.5" and check.reason in SNAPSHOT_BYTES_13_5))
ROW_RANK = {r: i for i, r in enumerate(ROWS)}
REASON_RE = re.compile(r"[A-Z][A-Z0-9_]{0,63}\Z")             # ILI-07: a bounded reason code from outside
REQUEST_ID_RE = re.compile(r"req-[0-9a-f]{40}\Z")
DIAG_MAX = 1 << 20

# ILC-I-02: units of remote work are pre-checked against the clients' computed worst cases (defaults when a client
# does not say); the safety mechanism is deadline.py's per-request guard, these only avoid starting a unit that cannot
# finish. MIN_REQUEST_S: another request is started only with at least this much left.
MIN_REQUEST_S = 60
DRAIN_SHARE = 1 / 3              # ILC-I2-04: at most this share of an invocation drains signer responses
ENUM_PAGE = 10                   # ILC-I2-04: active requests read per page
MTP_SPAN = 11                                # median-time-past window (Bitcoin consensus)


class StageError(Exception):
    pass


class Superseded(StageError):
    """A guarded write failed: the record changed since this invocation read it (or fenced it)."""


def _deadline(iss):
    return deadline.CURRENT.get() or deadline.Deadline(iss.clock, float("inf"), 0)


def _tip_worst(iss):
    f = getattr(iss.headers, "tip_worst_s", None)
    return f() if f else 2 * deadline.HTTP_WORST_S


def _height_worst(iss):
    f = getattr(iss.headers, "height_worst_s", None)
    return f() if f else 4 * deadline.HTTP_WORST_S


def _tip(iss):
    deadline.ensure(_tip_worst(iss), "tip")
    return iss.headers.tip()


# ------------------------------------------------------------------------------------------------ the poller
def poll(iss, budget_s=None):
    """One scheduled tick under one deadline (ILC-I-02; its clock is monotonic, ILC-I2-01). Work classes share the
    invocation (ILC-I2-04): draining signer responses may use at most DRAIN_SHARE of it; requests then get the rest.
    Requests are enumerated in bounded pages from a DURABLE continuation position (RequestStore.active_page and the
    poller cursor), and the position is moved past a request BEFORE it is worked on, so neither a long active list
    nor a request that exhausts (or kills) an invocation takes the others' turns. -> summary dict."""
    d = deadline.Deadline(getattr(iss, "elapsed_clock", None) or iss.clock,          # ILC-I2-01: monotonic
                          iss.budget_s if budget_s is None else budget_s, POLL_RESERVE_S)
    out = {"drained": 0, "advanced": {}, "cleaned": 0}
    with deadline.Installed(d):
        try:
            out["drained"] = drain(iss, share_s=DRAIN_SHARE * d.limit)
            _serve_requests(iss, d, out)
            if d.available() >= MIN_REQUEST_S:
                out["cleaned"] = cleanup(iss)
        except OutOfBudget as e:                       # out of time outside a request's turn: resumed next poll
            iss.note("poll out of time:", e)
            out["out_of_time"] = True
    return out


def _serve_requests(iss, d, out):
    store = iss.requests
    position = _position(iss)
    keep = {k: v for k, v in position.items() if k not in ("token", "skip", "drain_turn")}   # drain_turn: obsolete

    def put(pos):
        store.cursor_put(dict(keep, **pos))
    cur = {"token": position.get("token"), "skip": position.get("skip", 0)}
    seen, served, wrapped = set(), 0, False
    while True:
        rids, nxt = store.active_page(cur["token"], ENUM_PAGE)
        if not rids and cur["token"] is not None and not wrapped:
            cur, wrapped = {"token": None, "skip": 0}, True            # end of the list: start again from the top
            continue
        for i in range(cur["skip"], len(rids)):
            rid = rids[i]
            if rid in seen:
                return                                 # a full lap in this invocation
            if served and d.available() < MIN_REQUEST_S:
                out["deferred"] = True
                return
            put({"token": cur["token"], "skip": i + 1})  # moved BEFORE the request is worked on
            seen.add(rid)
            served += 1
            rec = store.get(rid)
            if rec is None or rec["state"] != "ACCEPTED":
                continue                               # the index is eventually consistent
            before = rec["stage"]
            try:
                advance(iss, rec)
            except OutOfBudget as e:
                iss.note("out of time, request kept:", rid[:12], e)
            except PreShipUnavailable as e:
                iss.note("pre-ship unavailable, request kept:", rid[:12], e)
            except Exception as e:  # noqa: BLE001  one request's fault never stops the others; retried next tick
                iss.note("stage", before, "error, request kept:", rid[:12], type(e).__name__, e)
            out["advanced"][rid] = (before, rec["stage"] or rec["state"])
        if nxt is None:
            if wrapped or cur["token"] is None and not rids:
                put({"token": None, "skip": 0})
                return
            cur, wrapped = {"token": None, "skip": 0}, True
        else:
            cur = {"token": nxt, "skip": 0}
        put(cur)


def advance(iss, rec):
    now = iss.clock()
    try:
        STAGES[rec["stage"]](iss, rec, now)
    except StageError as e:
        iss.note("stage", rec["stage"], "deferred:", e)


def _commit(iss, rec, expect):
    """Commit: a write guarded on `expect` (the lifecycle guard as read) and the record version."""
    if not iss.requests.save(rec, expect):
        raise Superseded("record changed since it was read; re-read next tick")


def _event(rec, now, *what):
    rec["events"] = (rec.get("events") or [])[-40:] + [[now, *what]]


def _fence(iss, rec, now):
    """Fence (R5-F3): a guarded write that bumps the version, committed before this invocation fetches anything for
    the attempt. Any write a killed earlier invocation left pending carries an older version and now fails its guard.
    If the fence itself fails, Superseded ends this request's turn: nothing is fetched."""
    g = lifecycle_guard(rec)
    rec["fenced_at"] = now
    _commit(iss, rec, g)


def _end_request(iss, rec, expect, state, reason, now):
    """The request's terminal write (COMPLETE, REFUSED or FAILED), after its cleanup obligation is durable."""
    iss.requests.cleanup_put(rec["rid"], {"rid": rec["rid"], "end_done": False})   # IS-07: before the commit
    now = max(now, iss.clock())                        # ended_at read after the obligation is durable (IS-02)
    a = current(rec)
    if a is not None and a["state"] in (OPEN, LATCHED) and state != "COMPLETE":
        if a["state"] == LATCHED:                      # no path ends a latched attempt other than step 7's discard
            raise StageError("refusing to end a latched attempt with the request")
        a.update(state=DISCARDED, end={"outcome": OUTCOME[DISCARDED], "reason": reason, "at": now})
    rec.update(state=state, reason=reason, stage=None, ended_at=now, expires_at=now + RETENTION_S)
    _event(rec, now, state, reason)
    _commit(iss, rec, expect)
    try:
        _cleanup_one(iss, rec["rid"], {"rid": rec["rid"], "end_done": False}, now)
    except Exception as e:  # noqa: BLE001  the obligation stays; the next poll retries it
        iss.note("cleanup deferred:", rec["rid"][:12], type(e).__name__, e)


def _end_attempt(iss, rec, outcome, reason, now, extra=None, no_successor=None):
    """End the current attempt (EXPIRED or DISCARDED, with its reason) and, in the SAME guarded write, allocate the
    next attempt, or refuse the request: ATTEMPTS_EXHAUSTED after attempt N, SIGNING_CLOSED when the next attempt
    would need signing after the stop (design step 8; the model's Commit of an ending write). no_successor names a
    reason no next attempt can be built at all (ILI-08: the content is lost); the request is then refused with it.
    extra: further fields of the attempt's end record (evidence, a diagnostic reference)."""
    assert outcome in ENDED
    expect = lifecycle_guard(rec)
    a, i = current(rec), rec["cur"]
    a.update(state=outcome, end={"outcome": OUTCOME[outcome], "reason": reason, "at": now, **(extra or {})},
             unavailable_since=None, failed_intervals=[])
    _event(rec, now, OUTCOME[outcome], a["id"], reason)
    if no_successor:
        return _end_request(iss, rec, expect, "REFUSED", no_successor, now)
    if i < N_ATTEMPTS and now <= iss.window.sign_until:
        rec["attempts"].append(new_attempt(i + 1, now))
        rec.update(cur=i + 1, stage="frames")
        _event(rec, now, "allocated", rec["attempts"][-1]["id"])
        return _commit(iss, rec, expect)
    _end_request(iss, rec, expect, "REFUSED", "ATTEMPTS_EXHAUSTED" if i >= N_ATTEMPTS else "SIGNING_CLOSED", now)


# ------------------------------------------------------------------------------------------------ cleanup (IS-07)
END_NS = ("content", "work", "frames")


def _cleanup_one(iss, rid, doc, now=None):
    """-> True when the obligation is discharged. Content, work files and frames go when the request has ended;
    the receipt goes 30 days after the end (or at once if the request did not complete). Deletion is keyed to the
    persisted end, never to an object's age; objects are tagged cleanup-due just before they are deleted (5.3.1).

    CF-02: a writer that read the request while it was ACCEPTED (an upload retry, a response consumer, a stale
    poller) may still store an object after the end. Each such writer runs inside one Lambda invocation, so it is
    gone WRITE_LEASE_S after the end was first seen here. Until then the obligation is kept and every poll deletes
    again; only a listing taken after the lease discharges it."""
    rec = iss.requests.get(rid)
    if rec is not None and rec["state"] == "ACCEPTED":
        return False                                   # not ended (an obligation written before a lost commit)
    seen = iss.clock()                                 # read after the record: no earlier than the end's commit
    expired = rec is None or seen >= rec["ended_at"] + RETENTION_S
    namespaces = END_NS + ("result",) if (expired or rec["state"] != "COMPLETE") else END_NS
    if doc.get("end_done") and not expired:
        return False
    if doc.get("fence_until") is None:                 # CF-02: start the writers' lease, durably
        doc = dict(doc, rid=rid, fence_until=seen + WRITE_LEASE_S)
        iss.requests.cleanup_put(rid, doc)
    for ns in namespaces:
        iss.results.mark_due(ns, rid)                  # due now: the lifecycle backstop may expire them from here on
        iss.results.delete(ns, rid)
    left = [ns for ns in namespaces if iss.results.names(ns, rid)]
    if left:
        raise StageError("objects left after deletion: " + ",".join(left))
    if seen < doc["fence_until"]:
        return False                                   # CF-02: a late writer may still store; delete again later
    if expired or "result" in namespaces:
        iss.requests.cleanup_done(rid)
        return True
    iss.requests.cleanup_put(rid, dict(doc, end_done=True))
    return False


def cleanup(iss):
    now, n = iss.clock(), 0
    for rid, doc in iss.requests.cleanup_list():
        try:
            n += bool(_cleanup_one(iss, rid, doc, now))
        except OutOfBudget:
            raise
        except Exception as e:  # noqa: BLE001
            iss.note("cleanup", rid[:12], "error, kept:", type(e).__name__, e)
    return n


# ------------------------------------------------------------------------------------------------ E-02 drain
def _position(iss):
    cur = iss.requests.cursor_get()
    return cur if isinstance(cur, dict) else {}


def _queue_worst(signer):
    return getattr(getattr(signer, "responses", None), "request_worst_s", 0)


def _handle_worst(iss, signer):
    """ILC-I7..I9: the worst case of one message's COMPLETE handling, from the adapters' per-request worst cases:
    every guarded request _take makes on its longest path (a redelivery that finds nothing done) - the signer-request
    index lookup, the record read, the used-log read, the used-log write and its append-only second write on a
    repeat, and the guarded record save (6 DynamoDB); the verified-object check, the frame read and the signature
    object write (3 S3) - and the acknowledgement (1 SQS). (A guarded save that loses a race re-reads and retries;
    not counted.)"""
    req = getattr(iss.requests, "request_worst_s", 0)
    res = getattr(iss.results, "request_worst_s", 0)
    return 6 * req + 3 * res + _queue_worst(signer)


def drain(iss, max_batches=50, share_s=float("inf")):
    """Read every slot's response queue. Every response is logged (request id, slot, status, frame hash when the
    id is known, signature hash) whether or not it is used, and then deleted from the queue.

    ILC-I6 (owner decision: OLDEST FIRST). Each round receives batches from the slots (each receive a guarded
    request; see below for when it stops), then handles the received messages across slots in order of their sent
    time (SQS SentTimestamp), oldest first. A message left unhandled becomes visible again and grows older. Handling is
    within the drain share (ILC-I2-04): a cooperative allocation checked between messages, never before a round's
    oldest message. Starvation-free with probability 1 only under the capacity condition stated below.

    Receiving goes on to the next slot only while that receive PLUS one message's complete worst-case handling
    (_handle_worst) still fit (ILC-I7); otherwise the round handles what it has, oldest first, the first message always
    (to completion, ack included, as far as the per-request guard admits each call). With the AWS adapters' worst
    cases that rule admits one receive per round, so the slot received from first is chosen at random each round
    (iss.rng): a fixed or schedule-derived first slot could keep receiving from the same (possibly empty) queue,
    while a random one reaches every slot with probability 1, with no remembered state. Residual: if an invocation
    cannot fit one receive plus one message's complete handling, progress waits for faster dependencies (the stated
    capacity limit, DESIGN.md)."""
    n, d = 0, _deadline(iss)
    start = d.clock()

    def over():
        return d.clock() - start >= share_s or d.available() < MIN_REQUEST_S
    slots = list(iss.signers.items())
    receive_worst = max((_queue_worst(s) for _, s in slots), default=0)
    handle_worst = max((_handle_worst(iss, s) for _, s in slots), default=0)
    for _ in range(max_batches):
        received = []
        first = iss.rng.randrange(len(slots)) if slots else 0       # see the docstring: no parity, no state
        for k_slot, (slot, signer) in enumerate(slots[first:] + slots[:first]):
            i = (first + k_slot) % len(slots)
            if k_slot and d.available() < receive_worst + handle_worst:
                break                              # ILC-I7: keep room for one message's COMPLETE handling
            try:
                batch = signer.receive(10)
            except OutOfBudget as e:
                iss.note("drain: no time for the next receive:", slot, e)
                break
            received += [(age, i, j, slot, signer, handle, body) for j, (handle, body, age) in enumerate(batch)]
        if not received:
            return n
        # oldest first across slots; equal sent times interleave the slots (each batch's own order, then slot), so a
        # tie never favours one slot
        received.sort(key=lambda r: (r[0][0], r[2], r[1]))
        for k, (age, _, _, slot, signer, handle, body) in enumerate(received):
            if k and over():
                return n                       # the rest become visible again after the visibility timeout
            try:
                _take(iss, slot, signer, body, receives=age[2])
                signer.ack(handle)
                n += 1
            except OutOfBudget as e:
                iss.note("drain out of time:", slot, e)
                return n
            except Exception as e:  # noqa: BLE001  not acknowledged: the queue delivers it again
                iss.note("response", slot, "not taken:", type(e).__name__, e)
        if over():
            return n
    return n


def _bounded(raw):
    """ILI-07: a signer-supplied reason as a bounded code. -> (code, diagnostic bytes or None)."""
    if raw is None:
        return None, None
    if isinstance(raw, str) and REASON_RE.match(raw):
        return raw, None
    data = raw.encode("utf-8", "replace") if isinstance(raw, str) else json.dumps(raw, sort_keys=True).encode()
    return "UNRECOGNIZED_REASON", data[:DIAG_MAX]


def _keep_diagnostic(iss, rid, aid, data):
    """Store an oversized or malformed external diagnostic by reference (deleted with the request's work files)."""
    digest = sha256hex(data)
    name = f"{aid}/diag-{digest}"
    iss.results.put("work", rid, name, data)
    return {"ref": name, "sha256": digest, "length": len(data)}


def _take(iss, slot, signer, body, receives=1):
    """Route one signer response by (request, ATTEMPT, job). A response for an attempt that is not the request's
    current one is logged ("other-attempt") and ignored: it can never fill another attempt (step 2). Every field taken
    from the response is bounded before it is stored (ILI-07)."""
    now = iss.clock()
    raw_id = body.get("request_id")
    srid = raw_id if isinstance(raw_id, str) and REQUEST_ID_RE.match(raw_id) else None
    idx = iss.requests.sigreq_get(srid) if srid else None
    status = body.get("status") if body.get("status") in ("SIGNED", "REFUSED") else "OTHER"
    reason, diag = _bounded(body.get("reason"))
    sig = None
    if status == "SIGNED":
        try:
            sig = b64d(body.get("sig_b64", ""))
        except (ValueError, TypeError):
            sig = None
    entry = {"at": rfc3339(now), "slot": slot,
             "request_id": srid or "invalid:" + sha256hex(json.dumps(raw_id).encode())[:32], "status": status,
             "reason": reason, "frame_sha256": idx["frame_sha256"] if idx else None,
             "signature_sha256": sha256hex(sig) if sig is not None else None, "disposition": None,
             "attempt": idx.get("attempt") if idx else None}
    if diag is not None:
        entry.update(reason_sha256=sha256hex(diag), reason_length=len(diag))
    if idx is None or idx.get("slot") != slot:
        entry["disposition"] = "unrequested"
    else:
        rec = iss.requests.get(idx["rid"])
        a = current(rec) if rec else None
        job = a["jobs"].get(idx["job"]) if a else None
        if rec is None or rec["state"] != "ACCEPTED":
            entry["disposition"] = "not-waiting"
        elif a is None or a["id"] != idx.get("attempt"):
            entry["disposition"] = "other-attempt"
        elif rec["stage"] != "signing" or a["state"] != OPEN or job is None:
            entry["disposition"] = "not-waiting"
        elif job.get("sig_sha256"):
            if receives > 1 and sig is not None and job["sig_sha256"] == sha256hex(sig):
                return                                 # ILC-I9: our own handling's record update is done; only the
                                                       # acknowledgement remains (its "used" entry is logged)
            entry["disposition"] = "duplicate"
        elif status == "REFUSED":
            entry["disposition"] = "refused"
            extra = {"diagnostic": _keep_diagnostic(iss, rec["rid"], a["id"], diag)} if diag is not None else None
            iss.requests.siglog_add(entry)
            return _end_attempt(iss, rec, DISCARDED, "SIGNER_REFUSED:" + str(reason or "NO_REASON"), now, extra)
        elif sig is None:
            entry["disposition"] = "malformed"
        else:
            # ILC-I8, ILC-I9: resumable, and every completed step OBSERVABLE, so a later delivery skips it and never
            # repeats it: 1 index lookup and record read (above; a record that already holds this signature means
            # step 5 is done)   2 frame read and verification, THEN the signature object under its digest-named key
            # (only verified signatures are written there, so its existence means "verified")   3 the "used" log
            # entry (IS-01: before the signature can be used)   4 the guarded record update   5 the acknowledgement
            # (drain, last). A first delivery has done nothing yet; a redelivery (receives > 1) checks each
            # completion with one guarded read before doing the step: the log, then the verified object.
            h = entry["signature_sha256"]
            name = f"{a['id']}/" + sig_name(idx["job"], h)
            logged = receives > 1 and iss.requests.siglog_has(srid, h)
            stored = logged or (receives > 1 and iss.results.size("work", rec["rid"], name) is not None)
            if not stored:
                frame = iss.results.get("work", rec["rid"], f"{a['id']}/{job['frame']}")
                if frame is None or sha256hex(frame) != job["frame_sha256"] or not signer.verify(frame, sig):
                    entry["disposition"] = "bad-signature"
                    iss.requests.siglog_add(entry)
                    return
                iss.results.put("work", rec["rid"], name, sig)
            entry["disposition"] = "used"
            if not logged:
                iss.requests.siglog_add(entry)         # IS-01: durable in the log before it can be used
            outcome = _record_signature(iss, idx["rid"], a["id"], idx["job"], entry["signature_sha256"], srid,
                                        now, rec=rec)
            if outcome != "used":                      # IS-08: say what became of it
                iss.requests.siglog_add(dict(entry, disposition="superseded:" + outcome))
            return
    iss.requests.siglog_add(entry)


def sig_name(job, sig_sha256):
    """Each verified signature has its own object, so concurrent consumers never overwrite one another (IS-08)."""
    return f"sig-{job}-{sig_sha256}"


def _record_signature(iss, rid, aid, job, sig_sha256, srid, now, rec=None):
    """IS-08: merge one verified signature into its attempt, re-reading on a guarded-write conflict. `rec`: the record
    as already read by the caller (ILC-I8: saves a read; the guarded save still detects any change since)."""
    for k in range(MERGE_ATTEMPTS):
        rec = rec if (k == 0 and rec is not None) else iss.requests.get(rid)
        a = current(rec) if rec else None
        if (rec is None or rec["state"] != "ACCEPTED" or a is None or a["id"] != aid or a["state"] != OPEN
                or rec["stage"] != "signing" or job not in a["jobs"]):
            return "not-waiting"
        if a["jobs"][job]["sig_sha256"]:
            return "duplicate"
        g = lifecycle_guard(rec)
        a["jobs"][job]["sig_sha256"] = sig_sha256
        _event(rec, now, "signed", aid, job, srid)
        if iss.requests.save(rec, g):
            return "used"
    return "save-conflict"                             # left in storage and the log; reconciled before any resend


def _reconcile(iss, rec, a):
    """IS-08: adopt a stored signature (its digest-named object exists only once it was verified on the job's frame,
    ILC-I9) instead of asking the signer again. ILC-I8: a stored signature WITHOUT its log record (handling stopped
    between the object and the log) is logged here, then adopted (IS-01 order: logged before used), so an interrupted
    handling continues from durable state; the frame is not read again. (_seal verifies every signature on its exact
    bytes before A_sig is built.) -> True if a job was satisfied."""
    names, found, aid = iss.results.names("work", rec["rid"]), False, a["id"]
    for job, j in a["jobs"].items():
        if j["sig_sha256"]:
            continue
        for name in names:
            if not name.startswith(f"{aid}/sig-{job}-"):
                continue
            sig = iss.results.get("work", rec["rid"], name)
            h = sha256hex(sig) if sig is not None else None
            if not (h and name == f"{aid}/" + sig_name(job, h)):
                continue
            if not iss.requests.siglog_has(j["request_id"], h):
                iss.requests.siglog_add({"at": rfc3339(iss.clock()), "slot": j["slot"], "request_id": j["request_id"],
                                         "status": "SIGNED", "reason": None, "frame_sha256": j["frame_sha256"],
                                         "signature_sha256": h, "disposition": "used", "attempt": aid,
                                         "recovered": True})
            j["sig_sha256"], found = h, True
            break
    return found


def _send(iss, rec, a, job):
    j = a["jobs"][job]
    frame = iss.results.get("work", rec["rid"], f"{a['id']}/{j['frame']}")

    def stash(data):                                   # IS-09: immutable, digest-named, deleted with the request
        name = f"{a['id']}-{sha256hex(data)}"
        iss.results.put("frames", rec["rid"], name, data)
        return iss.results.ref("frames", rec["rid"], name)
    # IS-03: every signer refuses after the window's signing stop. The former per-request bound (acceptance + 24 h)
    # is withdrawn with the 24-hour rule; an attempt's own signing has no other deadline.
    iss.signers[j["slot"]].send(j["request_id"], frame, sign_by=iss.window.sign_until, stash=stash)


# ------------------------------------------------------------------------------------------------ stages
def st_upload(iss, rec, now):
    """IS-05: the API created the record before storing the content. Proceed once the content is there; an upload
    abandoned past the grace period fails the request (no attempt exists yet)."""
    content = iss.results.get("content", rec["rid"], content_name(rec["content_sha256"]))
    g = lifecycle_guard(rec)
    if content is not None and sha256hex(content) == rec["content_sha256"]:
        rec["stage"] = "frames"
        return _commit(iss, rec, g)
    if now - rec["created_at"] >= UPLOAD_GRACE_S:
        return _end_request(iss, rec, g, "FAILED", "CONTENT_UNAVAILABLE", now)


def _content(iss, rec):
    content = iss.results.get("content", rec["rid"], content_name(rec["content_sha256"]))
    return content if content is not None and sha256hex(content) == rec["content_sha256"] else None


def _recover_content(iss, rec):
    """ILI-08: the submitted bytes are inside every built attestation frame (common.content). Recover them from an
    earlier attempt's frame that decodes and hashes to the request's content digest, and store them again."""
    for a in rec["attempts"][:-1]:
        for name in ("f_kms", "f_gpg"):
            frame = iss.results.get("work", rec["rid"], f"{a['id']}/{name}")
            try:
                data = b64d(read_frame(frame, "tessera-v1/attest")["common"]["content"]) if frame else None
            except (Fault, KeyError, TypeError, ValueError):
                data = None
            if data is not None and sha256hex(data) == rec["content_sha256"]:
                iss.results.put("content", rec["rid"], content_name(rec["content_sha256"]), data)
                return data
    return None


def st_frames(iss, rec, now):
    w = iss.window
    if not rec.get("cur"):                           # Start: attempt 1 (a lifecycle transition; the poller's only)
        g = lifecycle_guard(rec)
        if now > w.sign_until:
            return _end_request(iss, rec, g, "REFUSED", "SIGNING_CLOSED", now)
        if _content(iss, rec) is None:               # ILI-08: checked BEFORE any attempt exists
            return _end_request(iss, rec, g, "FAILED", "CONTENT_UNAVAILABLE", now)
        rec.update(attempts=[new_attempt(1, now)], cur=1)
        _event(rec, now, "allocated", "a1")
        _commit(iss, rec, g)
    a = current(rec)
    if now > w.sign_until:                           # this attempt would be signed after the stop
        return _end_attempt(iss, rec, DISCARDED, "SIGNING_CLOSED", now)
    content = _content(iss, rec)
    if content is None:                              # ILI-08: lost after allocation: recover, or no attempt can be built
        content = _recover_content(iss, rec)
        if content is None:
            return _end_attempt(iss, rec, DISCARDED, "CONTENT_UNAVAILABLE", now, no_successor="CONTENT_UNAVAILABLE")
        _event(rec, now, "content-recovered", a["id"])
    aid, declared = a["id"], a["declared_issue_time"]
    manifest = encode_manifest(w.kms_fp, w.gpg_fp)
    common = common_metadata(b64e(content), declared, manifest, iss.frozen.catalog)
    frames = {"manifest": manifest, "f_kms": encode_attest(common, w.kms_fp), "f_gpg": encode_attest(common, w.gpg_fp)}
    for name, data in frames.items():
        iss.results.put("work", rec["rid"], f"{aid}/{name}", data)
    jobs = {}
    for job, slot, fname in JOBS:
        srid = request_id(f"{rec['rid']}/{aid}", slot, frames[fname])
        jobs[job] = {"slot": slot, "frame": fname, "frame_sha256": sha256hex(frames[fname]), "request_id": srid,
                     "sent_at": now, "attempts": 1, "sig_sha256": None}
        iss.requests.sigreq_put(srid, {"rid": rec["rid"], "attempt": aid, "job": job, "slot": slot,
                                       "frame_sha256": jobs[job]["frame_sha256"]}, now + RETENTION_S)
    g = lifecycle_guard(rec)
    a["jobs"] = jobs
    rec["stage"] = "signing"
    _event(rec, now, "frames", aid, declared)
    _commit(iss, rec, g)                             # durable before anything is sent
    for job, _, _ in JOBS:
        _send(iss, rec, a, job)
    for slot in iss.signers:
        iss.signers[slot].wake()                     # E-01: started on demand, once per batch


def st_signing(iss, rec, now):
    a = current(rec)
    jobs = a["jobs"]
    g = lifecycle_guard(rec)
    if not all(j["sig_sha256"] for j in jobs.values()) and _reconcile(iss, rec, a):
        _event(rec, now, "reconciled", a["id"])      # IS-08: verified and logged, but its record update was lost.
        _commit(iss, rec, g)                         # ILI-04: recovered BEFORE deciding that signing is still needed
    if all(j["sig_sha256"] for j in jobs.values()):
        return _seal(iss, rec, a, now)               # a complete set is sealed whatever the signing window
    if now > iss.window.sign_until:                  # still needs signing after the stop (never a stamped attempt)
        return _end_attempt(iss, rec, DISCARDED, "SIGNING_CLOSED", now)
    g = lifecycle_guard(rec)
    resend = [(k, j) for k, j in jobs.items() if not j["sig_sha256"] and now - j["sent_at"] >= iss.signer_retry_s]
    if not resend:
        return
    for k, j in resend:
        j.update(sent_at=now, attempts=j["attempts"] + 1)
        iss.requests.sigreq_put(j["request_id"], {"rid": rec["rid"], "attempt": a["id"], "job": k, "slot": j["slot"],
                                                  "frame_sha256": j["frame_sha256"]}, now + RETENTION_S)
    _event(rec, now, "resend", a["id"], [k for k, _ in resend])
    _commit(iss, rec, g)
    slots = set()
    for k, j in resend:                               # E-02: the same request id; a late first answer still counts
        _send(iss, rec, a, k)
        slots.add(j["slot"])
    for s in slots:
        iss.signers[s].wake()


def _seal(iss, rec, a, now):
    """Profile 4 steps 4-6: verify each signature on the exact bytes, freeze, build A_sig, check it (A9.5: the
    signatures are frozen before the attempt is stamped)."""
    rid, aid = rec["rid"], a["id"]
    get = lambda n: iss.results.get("work", rid, f"{aid}/{n}")  # noqa: E731
    sigs = {}
    for job, j in a["jobs"].items():
        s, f = get(sig_name(job, j["sig_sha256"])), get(j["frame"])
        if (s is None or sha256hex(s) != j["sig_sha256"] or not iss.signers[j["slot"]].verify(f, s)
                or not iss.requests.siglog_has(j["request_id"], j["sig_sha256"])):     # IS-01
            g = lifecycle_guard(rec)
            j["sig_sha256"] = None                     # lost or corrupt: ask again with the same id
            j["sent_at"] = 0
            return _commit(iss, rec, g)
        sigs[job] = s
    a_sig = encode_anchor(get("f_kms"), sigs["s_kms"], get("f_gpg"), sigs["s_gpg"])
    try:
        for (f, obj, s, _), slot in zip(read_anchor(a_sig, registered_codecs(ALG)), ("kms", "gpg")):
            if not iss.signers[slot].verify(f, s) or obj["common"]["manifest_sha256"] != sha256hex(get("manifest")):
                raise StageError("A_sig check")
        read_frame(get("manifest"), "tessera-v1/manifest")
    except Fault as e:
        raise StageError("A_sig decode: " + e.code) from None
    iss.results.put("work", rid, f"{aid}/a_sig", a_sig)
    g = lifecycle_guard(rec)
    a["receipt_id"] = sha256hex(a_sig)
    rec["stage"] = "stamp"
    _event(rec, now, "a_sig", aid, a["receipt_id"])
    _commit(iss, rec, g)


def _validate_snapshot_now(iss, body, now):
    """Issuer pre-stamp check with the verifier's DNSSEC code: wildcard-free, every chain group valid now, and the
    TXT value equal to the window's assertion."""
    try:
        snap = parse_snapshot(body)
        if snap.wildcard:
            return "DNS_WILDCARD"
        config = check_config(iss.window.trust_base, {}, rfc3339(now))
        bad = [a.reason or a.status for a in validate_snapshot(snap, config, now) if a.status != "pass"]
        if bad:
            return bad[0]
        if snap.txt is None or txt_value([r.data for r in snap.txt.rr])["_raw"] != iss.window.assertion:
            return "DNS_VALUE_DIFFERS"
    except Fault as e:
        return e.code
    return None


def _capture_snapshot(iss, rec, a, now):
    """Capture, validate and stamp the DNSSEC snapshot for attempt a. -> True when stored (proofs updated in rec,
    not yet committed); False after committing a 'snapshot-rejected' event (recapture next tick)."""
    body = iss.dns.capture(now)
    problem = _validate_snapshot_now(iss, body, now)
    if problem:
        g = lifecycle_guard(rec)
        _event(rec, now, "snapshot-rejected", a["id"], problem)
        _commit(iss, rec, g)
        return False
    env = encode_snapshot_envelope(body)
    raw = ots.stamp(sha256(env), iss.calendars, iss.nonce())
    iss.results.put("work", rec["rid"], f"{a['id']}/snapshot.body", body)
    iss.results.put("work", rec["rid"], f"{a['id']}/snapshot.ots", raw)
    a["proofs"]["snapshot"] = {"stamped_at": now}
    return True


def _try_snapshot(iss, rec, a, now):
    """Capture and stamp the attempt's DNSSEC snapshot if it has none. ILC-I2-05: a rejected or failed capture is
    recorded and retried later; it never holds up the receipt's evidence. -> True when a snapshot is now held."""
    if "snapshot" in a["proofs"]:
        return True
    g = lifecycle_guard(rec)
    try:
        if not _capture_snapshot(iss, rec, a, now):
            return False
    except (OutOfBudget, Superseded):
        raise
    except Exception as e:  # noqa: BLE001  a capture failure is retried; it is not a lifecycle event
        iss.note("snapshot capture failed, retried:", rec["rid"][:12], type(e).__name__, e)
        return False
    a.pop("snapshot_failure", None)
    _event(rec, now, "stamped", a["id"], "snapshot")
    _commit(iss, rec, g)
    return True


def st_stamp(iss, rec, now):
    tip = _tip(iss)
    if tip < iss.window.h_git + 5:                     # chain-order pre-commitment (profile 4, 6.3)
        return
    a = current(rec)
    proofs = a["proofs"]
    if "receipt" not in proofs:                        # A9.5: a fresh stamp of this attempt's own A_sig
        raw = ots.stamp(sha256(iss.results.get("work", rec["rid"], f"{a['id']}/a_sig")), iss.calendars, iss.nonce())
        iss.results.put("work", rec["rid"], f"{a['id']}/receipt.ots", raw)       # immutable once committed
        g = lifecycle_guard(rec)
        proofs["receipt"] = {"stamped_at": now, "tip": tip}
        _event(rec, now, "stamped", a["id"], "receipt")
        _commit(iss, rec, g)
    _try_snapshot(iss, rec, a, now)                   # ILC-I2-05: evidence does not wait for it
    g = lifecycle_guard(rec)
    rec["stage"] = "evidence"
    _commit(iss, rec, g)


# ------------------------------------------------------------------------------------------------ evidence (steps 3-5)
def conjunct_failed(sel, declared):
    """The three-conjunct temporal predicate of A2.1/A2.2 on a selected presentation (the verifier's rows 12.1-12.3,
    all three; rows 12.2 and 12.3 alone are not the predicate). -> the first failing conjunct's code, or None."""
    if not declared - EPS <= sel.time:
        return "TIME_BEFORE_DECLARED_EPSILON"
    if not sel.time <= declared + DELTA:
        return "TIME_AFTER_DECLARED_DELTA"
    if not sel.confirmed <= declared + DELTA:
        return "CONFIRMATION_LATE"
    return None


@dataclass
class Evidence:
    """One Fetch for one attempt. cls: "elig" (the lowest qualifying presentation in hand satisfies the predicate),
    "neg" (COMPLETE evidence and that presentation fails a conjunct), "err" (some part of the fetch failed) or
    "pending" (anything else: a calendar not yet attested, a segment not yet buried k = 6, nothing qualifying).
    Only "elig" and "neg" are successes; neither "err" nor "pending" is ever evidence of absence."""
    cls: str                                          # "elig" | "neg" | "invalid" | "err" | "pending"
    fetch_start: int
    sel: object = None
    failed: str = None
    presentation: dict = None
    detail: str = ""
    errors: list = field(default_factory=list)


def _headers(iss, rec, a, heights):
    """Headers at `heights`, checkpointed per height under the attempt (ILI-05): a header once fetched and checked is
    stored, so a later invocation resumes instead of fetching it again. A height not yet stored is fetched only if the
    explorers' worst case for one height fits the time left (else OutOfBudget, after keeping what was fetched).

    Consecutive heights must link. If stored headers do not (a stored header is stale: a reorganisation, or a bad
    store), every stored header of the set is invalidated DURABLY (an empty object), and the set is fetched again; the
    refresh then advances across invocations, each one keeping the heights it re-fetched (ILC-I-03), instead of
    restarting from the lowest height and never reaching the stale one. The checkpoint relies on the k-deep
    assumption: no reorganisation of 6 or more blocks (A1.6, V1 contract)."""
    rid, aid = rec["rid"], a["id"]
    hs = sorted(set(heights))
    seg_name = f"{aid}/seg/{hs[0]}-{hs[-1]}"
    seg = iss.results.get("work", rid, seg_name)           # a whole linked set, stored once checked: one read
    if seg and len(seg) == 80 * len(hs):
        out = {h: seg[80 * i:80 * (i + 1)] for i, h in enumerate(hs)}
        try:
            check_links(out)
            return out
        except Exception:  # noqa: BLE001  fall through to the per-height checkpoints
            pass
    out = {}
    for h in hs:
        name = f"{aid}/hdr/{h}"
        raw = iss.results.get("work", rid, name)
        if raw is None or len(raw) != 80:
            deadline.ensure(_height_worst(iss), f"header {h}")
            raw = iss.headers.headers([h])[h]
            if len(raw) != 80:
                raise ValueError(f"header {h} is not 80 bytes")
            iss.results.put("work", rid, name, raw)
        out[h] = raw
    try:
        check_links(out)
    except Exception as e:  # noqa: BLE001
        iss.results.put("work", rid, seg_name, b"")
        for h in hs:                                   # durable invalidation: the refresh survives the invocation
            iss.results.put("work", rid, f"{aid}/hdr/{h}", b"")
        raise StageError(f"stored headers {hs[0]}..{hs[-1]} did not link ({e}); invalidated, re-fetched next") \
            from None
    if seg != b"".join(out[h] for h in hs):
        iss.results.put("work", rid, seg_name, b"".join(out[h] for h in hs))
    return out


def _upgrade(iss, rec, a, name, cursor_name):
    """Upgrade one of the attempt's proofs from its calendars, within the deadline, resuming at the durable cursor
    (ILC-I-05). -> (proof bytes, finished)."""
    rid = rec["rid"]
    raw = iss.results.get("work", rid, name)
    cur = iss.results.get("work", rid, cursor_name)
    start = int(cur) if cur and cur.isdigit() else 0
    # ILC-I2-03: the checkpoint write is reserved BEFORE any calendar request: a request starts only if, after it,
    # one write still fits. If a calendar answered, the changed proof is that write (its resolved attestations leave
    # the pending list, so the next invocation asks the others); otherwise the cursor is. Either way the progress of
    # this invocation is durable.
    write = getattr(iss.results, "request_worst_s", 0)
    new, changed, finished, nxt = ots.upgrade_bounded(
        raw, iss.calendars, start=start,
        keep_going=lambda: _deadline(iss).available() >= deadline.HTTP_WORST_S + write)
    if changed:
        iss.results.put("work", rid, name, new)
    if nxt != start:
        try:
            iss.results.put("work", rid, cursor_name, str(nxt).encode())
        except OutOfBudget:
            if not changed:
                raise
    return new, finished


def _evaluate(iss, rec, a, new, proof, tip, a_sig, fetch_start):
    """Classify the evidence in `proof` (see fetch_evidence)."""
    aid = a["id"]
    hdrs, missing, errors = {}, [], []
    for h in sorted({x.height for x in proof.bitcoin}):
        if h + K - 1 > tip:
            missing.append(h)                          # not yet buried k deep: the segment does not exist yet
            continue
        try:
            hdrs.update(_headers(iss, rec, a, range(h, h + K)))
        except OutOfBudget:
            raise
        except Exception as e:  # noqa: BLE001
            errors.append(f"{h}: {type(e).__name__}: {e}")
    pins = {h: pin_of(v) for h, v in hdrs.items()}
    sel, _ = select(proof, hdrs, pins)
    complete = bool(proof.bitcoin) and not proof.pending and not missing and not errors
    declared = ts(a["declared_issue_time"])
    failed = conjunct_failed(sel, declared) if sel is not None else None
    if sel is not None and failed is None:
        root = hdrs[sel.height][36:68]
        pruned, dropped = ots.prune_to_height(new, sel.height, merkle_root=root)
        seg = {i: hdrs[i] for i in range(sel.height, sel.height + K)}
        check, contradicted = select(parse_ots(pruned), seg, {i: pin_of(v) for i, v in seg.items()})
        if (check is None or contradicted
                or (check.height, check.time, check.confirmed) != (sel.height, sel.time, sel.confirmed)):
            return Evidence("err", fetch_start, detail="pruned presentation does not reproduce the selection")
        pres = {"format": "tessera-v1-issuer-presentation/1", "attempt": aid, "a_sig_sha256": sha256hex(a_sig),
                "ots": b64e(pruned), "height": sel.height, "T": sel.time, "confirmed_at": sel.confirmed,
                "contradicted_pruned": dropped,
                "headers": {str(i): v.hex() for i, v in sorted(seg.items())}}
        return Evidence("elig", fetch_start, sel=sel, presentation=pres)
    if complete and sel is not None:
        return Evidence("neg", fetch_start, sel=sel, failed=failed)
    if complete and all(x.height in hdrs and hdrs[x.height][36:68] != x.message for x in proof.bitcoin):
        return Evidence("invalid", fetch_start, failed="EVIDENCE_CONTRADICTED",
                        detail=f"all {len(proof.bitcoin)} attestations contradicted by their pinned headers")
    detail = (f"pending calendars {len(proof.pending)}, unburied {missing}, "
              f"{'no qualifying height' if sel is None else 'selected fails ' + str(failed)}")
    return Evidence("err" if errors else "pending", fetch_start, sel=sel, failed=failed, detail=detail, errors=errors)


def fetch_evidence(iss, rec, a):
    """Fetch: the attempt's own proof (it must stamp SHA-256 of this attempt's A_sig), the full pinned, linked h..h+5
    segment of every Bitcoin attestation, and the lowest qualifying height by the verifier's `select`. The wall
    reading `fetch_start` is taken before anything is fetched (R5-F1). Every request is under the poll's deadline;
    headers and calendar answers already obtained are kept, and OutOfBudget is raised (no classification, no
    lifecycle write) when the evidence could not be fetched in this invocation.

    ILC-I-05: the evidence already held is evaluated FIRST; if it already shows eligibility the attempt latches
    without spending time on pending calendars. Otherwise pending calendars are asked, in turn from a durable cursor
    (so a long list of slow calendars is served across invocations), and the evidence is evaluated again.

    Classes: "elig" - the lowest qualifying presentation satisfies the three conjuncts; it is pruned to the qualifying
    branches at its height (select's contradiction flag is honoured: contradicted branches are not part of it, and
    the pruned presentation is re-checked contradiction-free). "neg" - COMPLETE evidence and that presentation fails a
    conjunct. "invalid" - COMPLETE evidence in which EVERY Bitcoin attestation is contradicted by its pinned header
    (ILI-03: conclusive invalid evidence, profile 7.1; reason EVIDENCE_CONTRADICTED). "err" / "pending" - anything
    else; never evidence of absence."""
    fetch_start = iss.clock()
    rid, aid = rec["rid"], a["id"]
    name = aid + "/receipt.upgraded.ots"
    try:
        a_sig = iss.results.get("work", rid, aid + "/a_sig")
        held = iss.results.get("work", rid, name)
        if held is None:
            held = iss.results.get("work", rid, aid + "/receipt.ots")
            if held is not None:
                iss.results.put("work", rid, name, held)
        if held is None or a_sig is None:
            raise StageError("attempt material unavailable")
        proof = parse_ots(held)
        if proof.digest != sha256(a_sig):
            return Evidence("err", fetch_start, detail="proof does not stamp this attempt's A_sig")
        tip = _tip(iss)
        ev = _evaluate(iss, rec, a, held, proof, tip, a_sig, fetch_start)          # the evidence already held
        if ev.cls == "elig" or not proof.pending:
            return ev
        new, finished = _upgrade(iss, rec, a, name, aid + "/receipt.upgrade-cursor")
        if new != held:
            proof = parse_ots(new)
            if proof.digest != sha256(a_sig):
                return Evidence("err", fetch_start, detail="upgraded proof does not stamp this attempt's A_sig")
            ev = _evaluate(iss, rec, a, new, proof, tip, a_sig, fetch_start)
        if not finished and ev.cls != "elig":
            raise OutOfBudget("pending calendars left for the next poll")
        return ev
    except OutOfBudget:
        raise
    except Exception as e:  # noqa: BLE001  a failed fetch: never a negative
        return Evidence("err", fetch_start, detail=f"{type(e).__name__}: {e}")


def _add_interval(a, idx):
    """Diagnostic failure history (gated step 5: behind no behaviour). failed_intervals holds runs [first, last] of
    absolute interval indices (fetch_start // POLL_INTERVAL_S), each interval at most once. -> True if changed."""
    runs = [list(r) for r in a.get("failed_intervals") or []]
    if any(lo <= idx <= hi for lo, hi in runs):
        return False
    runs.append([idx, idx])
    runs.sort()
    merged = []
    for lo, hi in runs:
        if merged and lo <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    if len(merged) > FAILED_INTERVAL_RUNS:
        a["failed_intervals_dropped"] = a.get("failed_intervals_dropped", 0) + len(merged) - FAILED_INTERVAL_RUNS
        merged = merged[-FAILED_INTERVAL_RUNS:]
    a["failed_intervals"] = merged
    return True


def st_evidence(iss, rec, now):
    """An OPEN attempt: Fence, Fetch, Send. Latch on eligibility; end only on complete negative evidence (discard at or
    before B, expire after B); otherwise stay open, recording the failure history after B for diagnosis only."""
    a = current(rec)
    _fence(iss, rec, now)                             # Fence: committed before any fetch
    _try_snapshot(iss, rec, a, now)                   # ILC-I2-05: early (its anchor must be timely), never blocking
    ev = fetch_evidence(iss, rec, a)                  # Fetch
    now = iss.clock()                                 # Send: the decision's reading
    if ev.cls == "elig":
        return _latch(iss, rec, a, ev, now)
    if ev.cls in ("neg", "invalid"):                  # complete negative, or complete authenticated contradiction
        return _end_attempt(iss, rec, DISCARDED if now <= B_of(a) else EXPIRED, ev.failed, now)
    if ev.fetch_start > B_of(a):                      # only fetches that STARTED after B count (R5-F1)
        g = lifecycle_guard(rec)
        changed = a.get("unavailable_since") is None
        if changed:
            a["unavailable_since"] = ev.fetch_start
        changed = _add_interval(a, ev.fetch_start // POLL_INTERVAL_S) or changed
        if changed:
            a["last_failed_fetch"] = {"at": ev.fetch_start, "class": ev.cls, "detail": ev.detail[:300]}
            _commit(iss, rec, g)                      # diagnostic only; no decision reads it while step 5 is gated


def _latch(iss, rec, a, ev, now):
    """Latch (A2.1; design step 3): written whenever eligibility is observed while the attempt is open, with
    observed_at and the qualifying presentation itself. The presentation is an immutable, digest-named object written
    BEFORE the latch commits its reference (no transaction spans DynamoDB and S3; the item limit is 400 KB)."""
    body = json.dumps(ev.presentation, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256hex(body)
    name = f"{a['id']}/presentation-{digest}"
    iss.results.put("work", rec["rid"], name, body)
    g = lifecycle_guard(rec)
    a.update(state=LATCHED, unavailable_since=None, failed_intervals=[],
             latch={"observed_at": now, "fetch_start": ev.fetch_start, "ref": name, "sha256": digest,
                    "height": ev.sel.height, "T": ev.sel.time, "confirmed_at": ev.sel.confirmed,
                    "contradicted_pruned": ev.presentation["contradicted_pruned"]})
    rec["stage"] = "finalize" if "snapshot" in a["proofs"] else "snapshot"   # ILC-I2-05: capture before finalizing
    _event(rec, now, "latched", a["id"], ev.sel.height, rfc3339(ev.sel.time))
    _commit(iss, rec, g)


# ------------------------------------------------------------------------------------------------ after the latch (step 7)
def _preserved(iss, rec, a):
    lt = a["latch"]
    body = iss.results.get("work", rec["rid"], lt["ref"])
    if body is None or sha256hex(body) != lt["sha256"]:
        raise StageError("preserved presentation unavailable; retried")
    return json.loads(body)


def classify_preship(ledger):
    """ILI-01, ILC-I-01: -> (kind, the deciding verifier check or None). Kinds, in preference order:
      "frozen"    an INVALID check on frozen material (FROZEN_ROWS) is preferred over any other failing check, whatever
                  its position: it can never pass, so the attempt is discarded with it;
      "snapshot"  else, an INVALID check depending only on the snapshot's bytes (snapshot_bytes_only): this snapshot
                  can never pass; recapture it, or discard if no lawful snapshot can be obtained (ILI-02);
      "retry"     anything else, including every configuration-dependent snapshot result (13.5 and 13.4's header
                  outcomes) and every UNVERIFIABLE result: retried, keeping the current snapshot.
    Without a ledger (no per-row result) nothing is frozen or snapshot: retry."""
    if ledger is None:
        return "retry", None
    bad = sorted((c for c in ledger.checks if c.status in ("invalid", "unknown") and c.reason),
                 key=lambda c: (ROW_RANK.get(c.row, len(ROW_RANK)), c.tie))
    snap = [c for c in bad if c.row in SNAPSHOT_ROWS]
    frozen = [c for c in bad if c.status == "invalid" and c.row in FROZEN_ROWS
              and not (c.row == "16.1" and snap)]      # 16.1 reads the window from the snapshot
    if frozen:
        return "frozen", frozen[0]
    snap_bytes = [c for c in snap if snapshot_bytes_only(c)]
    if snap_bytes:
        return "snapshot", snap_bytes[0]
    return "retry", bad[0] if bad else None


def _snapshot_impossible(iss, rec, a, failure):
    """ILI-02, ILC-I-01: evidence that NO lawful snapshot can be obtained for this frozen attempt any more. -> evidence
    dict, or None when that is not proven (the issuer then recaptures or retries; elapsed time alone never proves it).

    Proven only when BOTH
      (1) the current snapshot can never pass: its recorded failure (`failure`: row, reason) is an INVALID check that
          depends only on the snapshot's bytes (snapshot_bytes_only; never a configuration-dependent row such as
          13.5), and its proof is complete (no pending calendar: its lowest attestation is fixed); and
      (2) no NEW snapshot can be anchored in time: a new anchor would be mined above the current tip, and every such
          block's time exceeds the median time past (MTP) of the eleven authenticated, linked headers ending k - 1 = 5
          below the tip (Bitcoin consensus: a block's time exceeds the MTP of its eleven predecessors, and MTP never
          decreases along a chain). Those eleven blocks survive under the k-deep assumption: no reorganisation of 6 or
          more blocks (A1.6; the V1 contract's wording). If that MTP is later than declared + delta, no new anchor can
          satisfy row 13.7's T <= declared + delta."""
    if failure is not None and not snapshot_bytes_only(SimpleNamespace(status="invalid", **failure)):
        return None                                    # a configuration-dependent failure is never ground for it
    snap = iss.results.get("work", rec["rid"], f"{a['id']}/snapshot.ots")
    if snap is None and "snapshot" not in a["proofs"]:
        failure = {"row": "-", "reason": "NO_SNAPSHOT"}  # ILC-I2-05: none was ever captured; (1) holds vacuously
    elif failure is None or snap is None or parse_ots(snap).pending:
        return None
    hi = _tip(iss) - (K - 1)
    lo = hi - MTP_SPAN + 1
    if lo < 0:
        return None
    try:
        hdrs = _headers(iss, rec, a, range(lo, hi + 1))
    except OutOfBudget:
        raise
    except Exception:  # noqa: BLE001  headers not obtainable: impossibility is not proven
        return None
    times = sorted(int.from_bytes(h[68:72], "little") for h in hdrs.values())
    mtp, limit = times[MTP_SPAN // 2], ts(a["declared_issue_time"]) + DELTA
    if mtp <= limit:
        return None
    return {"snapshot_reason": failure["reason"], "snapshot_row": failure["row"], "mtp_heights": [lo, hi],
            "median_time_past": mtp, "declared_plus_delta": limit}


def st_finalize(iss, rec, now):
    """A LATCHED attempt (step 7). Transient failures (store, explorer, calendar, DNS, pre-ship engine,
    configuration) are retried; the attempt is discarded only for a failure the frozen attempt cannot cure, with the
    reason recorded: T of the preserved presentation > not-after (A9:422); an INVALID verifier check that depends only
    on frozen material (classify_preship); or proven impossibility of any lawful snapshot (ILI-02, ILC-I-01). The
    preserved presentation is used as is, never swapped. A closed signing window does not end it. Every request is
    under the poll's deadline (ILC-I-02)."""
    a = current(rec)
    rid, aid = rec["rid"], a["id"]
    _fence(iss, rec, now)
    if a["latch"]["T"] > iss.window.na:
        return _end_attempt(iss, rec, DISCARDED, "T_AFTER_NOT_AFTER", now)
    pres = _preserved(iss, rec, a)
    snap = iss.results.get("work", rid, f"{aid}/snapshot.ots")
    if snap is None:
        raise StageError("snapshot proof unavailable; retried")
    tip = _tip(iss)
    ok, hs = ots.k6_ready(snap, tip)
    if not ok:                                         # ILC-I-05: upgrade only when the held proof is not ready
        snap, finished = _upgrade(iss, rec, a, f"{aid}/snapshot.ots", f"{aid}/snapshot.upgrade-cursor")
        ok, hs = ots.k6_ready(snap, tip)
        if not ok:
            if not finished:
                raise OutOfBudget("snapshot calendars left for the next poll")
            return                                     # the snapshot's confirmations are still coming
    try:
        extra = {}
        for lo in sorted({hs, iss.window.h_git}):
            extra.update(_headers(iss, rec, a, range(lo, lo + K)))
    except OutOfBudget:
        raise
    except Exception as e:  # noqa: BLE001
        raise StageError(f"headers unavailable ({type(e).__name__}); retried") from None
    hdrs = {int(h): bytes.fromhex(v) for h, v in pres["headers"].items()}
    for h, v in extra.items():
        if h in hdrs and hdrs[h] != v:
            raise StageError(f"header {h} differs from the preserved presentation; retried")
        hdrs[h] = v
    bundle = assemble(iss, rec, a, hdrs, pres)
    result = deadline.guarded(deadline.PRESHIP_WORST_S, iss.preship.check, bundle, hdrs, iss.clock(),
                              diagnostics=True, what="pre-ship")
    stable, ledger = result[0], (result[2] if len(result) > 2 else None)
    if stable["verdict"] == "VALID_STRICT" and stable["reason"] == "OK":
        return _ship(iss, rec, a, bundle, stable, now)
    kind, check = classify_preship(ledger)
    if kind == "frozen":
        return _end_attempt(iss, rec, DISCARDED, f"PRESHIP:INVALID/{check.reason}@{check.row}", now)
    if kind == "snapshot":
        failure = {"row": check.row, "reason": check.reason}
        evidence = _snapshot_impossible(iss, rec, a, failure)
        if evidence is not None:
            return _end_attempt(iss, rec, DISCARDED, "SNAPSHOT_IMPOSSIBLE", now, {"evidence": evidence})
        g = lifecycle_guard(rec)                       # profile 4: re-capture the snapshot before shipping
        a["proofs"].pop("snapshot", None)
        a["snapshot_failure"] = failure                # what the snapshot being replaced failed on (ILC-I-04)
        rec["stage"] = "snapshot"
        _event(rec, now, "preship-recapture", aid, check.reason, check.row)
        return _commit(iss, rec, g)
    what = f"{stable['verdict']}/{check.reason if check else stable['reason']}"
    iss.note("pre-ship", what, "on a latched attempt; retried:", rid[:12])
    last = (rec.get("events") or [[None]])[-1]
    if last[1:] != ["preship-retry", aid, what]:
        g = lifecycle_guard(rec)
        _event(rec, now, "preship-retry", aid, what)
        _commit(iss, rec, g)


def st_snapshot(iss, rec, now):
    """Re-capture the latched attempt's snapshot. ILC-I-04: before capturing, the impossibility proof is evaluated on
    the snapshot being replaced (its recorded byte-only failure), so a recapture that keeps being rejected cannot hold
    the attempt here once no lawful snapshot can be obtained."""
    a = current(rec)
    _fence(iss, rec, now)
    evidence = _snapshot_impossible(iss, rec, a, a.get("snapshot_failure"))
    if evidence is not None:
        return _end_attempt(iss, rec, DISCARDED, "SNAPSHOT_IMPOSSIBLE", now, {"evidence": evidence})
    g = lifecycle_guard(rec)
    if _capture_snapshot(iss, rec, a, now):
        a.pop("snapshot_failure", None)                # the snapshot it described is replaced
        rec["stage"] = "finalize"
        _event(rec, now, "stamped", a["id"], "snapshot")
        _commit(iss, rec, g)


def _ship(iss, rec, a, bundle, stable, now):
    iss.results.put("result", rec["rid"], "receipt.json", bundle)
    g = lifecycle_guard(rec)
    a["state"] = SHIPPED
    rec["receipt_sha256"] = sha256hex(bundle)
    rec["T"] = stable["T"]
    _end_request(iss, rec, g, "COMPLETE", None, now)


def assemble(iss, rec, a, hdrs, pres):
    """The canonical JCS container of profile 15.1, with the attempt's frozen material and its preserved receipt
    presentation."""
    get, w, fz = (lambda n: iss.results.get("work", rec["rid"], f"{a['id']}/{n}")), iss.window, iss.frozen
    receipt_ots = b64d(pres["ots"])
    selected, _ = select(parse_ots(receipt_ots), hdrs, {h: pin_of(v) for h, v in hdrs.items()})
    if selected is None or selected.height != pres["height"]:
        raise StageError("preserved presentation does not qualify under the assembled headers")
    txid = ots.txid_of(selected.paths[0])
    delay = max(0, selected.time - ts(a["declared_issue_time"]))
    layer = {
        "a_sig": b64e(get("a_sig")),
        "dependency_manifest": b64e(fz.dependency_manifest),
        "dns": {"ots": b64e(get("snapshot.ots")), "snapshot_body": b64e(get("snapshot.body"))},
        "git": {"blob": b64e(w.git["blob"]), "commit": b64e(w.git["commit"]), "object_format": "sha1",
                "ots": b64e(w.git["ots"]), "trees": [b64e(t) for t in w.git["trees"]]},
        "headers": {str(h): v.hex() for h, v in sorted(hdrs.items())},
        "issuer_record": {"observed_anchor_delay_s": str(delay), "policy_version": POLICY_VERSION},
        "keys": {"gpg": b64e(w.gpg_key), "kms": b64e(w.kms_key)},
        "manifest": b64e(get("manifest")),
        "possession": {"gpg": b64e(get(sig_name("p_gpg", a["jobs"]["p_gpg"]["sig_sha256"]))),
                       "kms": b64e(get(sig_name("p_kms", a["jobs"]["p_kms"]["sig_sha256"])))},
        "preamble": b64e(fz.preamble),
        "receipt_anchor": {"ots": b64e(receipt_ots), "txid": txid},
        "spec": b64e(fz.spec),
        "vectors": b64e(fz.vectors),
    }
    return jcs({"layers": [layer], "profile": PROFILE})


STAGES = {"upload": st_upload, "frames": st_frames, "signing": st_signing, "stamp": st_stamp,
          "evidence": st_evidence, "finalize": st_finalize, "snapshot": st_snapshot}
