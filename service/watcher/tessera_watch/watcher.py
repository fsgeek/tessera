"""One watcher run (docs/V1-DETECTION-CONTRACT.md, the Arariwa item 0(b); D5, D6, D7 IAM, D8; trace records 0(a)).

Order of a run:
  1. load the durable state (its ETag is the commit guard); on the very first run, create it at once, so the trail
     coverage start survives a crash of that run (review M2);
  2. read new CloudTrail files from the trail cursor (D6 Sign events, AccessDenied on the key, D7 IAM writes);
  3. scan the issuer table: new SIGLOG# entries (D5; the kms signatures the issuer verified and used, for D6) and
     newly terminal REQ# records;
  4. reconcile kms:Sign events against those signatures (D6), finalizing a match only past the delivery horizon;
  5. for each pending terminal request (oldest attempt first, bounded per run): re-verify a COMPLETE receipt and bind
     it to its record (D8), then write its trace record (0(a)) once its kms signatures are final;
  6. publish every finding waiting in the outbox (each was written there when it was found); 7. commit the state;
  8. publish the heartbeat (D9), unless a source could not be read, a trail file, trail record or SIGLOG# entry
     failed or was not reached (D6 is then not finalized), a finding could not be published, or the verifier's own
     startup check fails. A finding that could be neither written to the outbox nor published stops
     the run before 7 (no commit: the next run reads the same sources and finds it again).

Failure isolation (review H1): a failure while checking one trail file, one SIGLOG# entry or one request becomes a
`W` finding (detection, item id or rid prefix, exception class name only) and the run goes on; that item stays
unchecked and is retried next run (a trail record whose classification raises is not retried: its file is marked
read). A trail file or SIGLOG# entry that failed, or a trail file left unread for lack of time, also means no D6
outcome is finalized and no heartbeat is sent in that run (final pass). A failure of a whole source (the scan, the
trail listing) is a `W` finding and
withholds the heartbeat. Anything else (the state cannot be loaded or committed) is a failure of the run: the handler
reports WATCHER_ERROR with the class name and no heartbeat is sent, so D9 fires if it persists.

Cursors (review H2, M2): no cursor moves by an issuer-supplied time. Issuer items are new while their key is not in the
seen set; a seen key is forgotten only when the item is no longer in the (complete, strongly consistent) scan. The
trail cursor advances only to the watcher's own clock minus TRAIL_LAG_S, and never past a file it has not read (keys
are read in key-time order). D6 outcomes are finalized only in a run that read the trail, the scan and every SIGLOG#
entry in full. An issuer time more than FUTURE_S ahead of the watcher's clock is a finding and never counts.

Nothing here imports issuer code. The request id formula is the issuer's documented one, restated."""
import calendar
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field

from . import cloudtrail, receipts
from . import sanitize as S

STATE_VERSION = 2
TERMINAL = ("COMPLETE", "REFUSED", "FAILED")
RUN_S = 600                   # the schedule: one run every 10 minutes
FUTURE_S = 300                # an issuer time more than this ahead of the watcher's clock is a finding
MATCH_WINDOW_S = 40 * 60      # D6: a Sign at t is accounted for by a used kms signature first logged in [t - SKEW, t + this]
SKEW_S = 120                  # D6: clock difference between CloudTrail eventTime and the issuer's Lambda clock
CT_LAG_S = 45 * 60            # D6: CloudTrail delivers a Sign within this (platform; typically 15 min)
SIG_HORIZON_S = SKEW_S + CT_LAG_S                 # a signature's match is final this long after it was logged
SIGN_HORIZON_S = max(MATCH_WINDOW_S, CT_LAG_S)    # a Sign with no signature this long after it is unmatched
LOOKBACK_S = 24 * 3600        # the first run's trail coverage; a trail file failing this long is abandoned (reported)
TRAIL_LAG_S = 3600            # the trail cursor trails the watcher's clock by this (a file listed late is still read)
D8_GIVE_UP_S = 6 * 3600       # D8: a receipt that cannot be checked for this long is reported UNCHECKED (bounded)
UNLOGGED_S = 1800             # a job signature with no SIGLOG# entry this long after the request ended is a finding
RETAIN_S = 45 * 24 * 3600     # D6 reconciliation memory: final signatures and Signs kept this long, then pruned
REPORTED_RETAIN_S = 30 * 24 * 3600
TRACE_WAIT_S = SIG_HORIZON_S + 2 * RUN_S          # a trace waits at most this for its kms signatures to be final
MAX_VERIFY_PER_RUN = 10       # D8 per run (review M4); the rest carry over, least recently tried first
FINISH_RESERVE_S = 90         # left for publication, the commit and the heartbeat
MIN_VERIFY_S = 60             # no verification is started with less than this to spend on it
TRAIL_RESERVE_S = 150         # no trail file is read with less than this left

# D5: signer reasons only an attacker or a fault produces, and the poller dispositions (contract table, row D5).
D5_REASONS = frozenset({"KEY_FP_MISMATCH", "FRAME_DIGEST_MISMATCH", "ALG_NOT_ALLOWED", "DECLARED_TIME_OUTSIDE_EPSILON",
                        "BAD_REQUEST", "TRUNCATED", "UNRECOGNIZED_REASON",
                        # the verifier codec's Fault codes, forwarded by both signers: the issuer builds every frame,
                        # so a codec fault on one is a fault or an attacker (steward, 2026-11-22)
                        "ANCHOR_COUNT", "CONTAINER_SCHEMA", "CV_UNKNOWN", "JSON_DEPTH", "JSON_DUPLICATE_NAME",
                        "JSON_ENCODING", "JSON_NONCANONICAL", "JSON_NUMBER", "JSON_SYNTAX", "KEY_FORMAT", "LENGTH_CAP",
                        "SCHEMA", "SIG_EMPTY", "SIG_FORMAT", "SIG_PACKET", "SIG_POLICY", "TAG_MISMATCH", "TAG_UNKNOWN",
                        "TRAILING"})
D5_DISPOSITIONS = frozenset({"unrequested", "malformed", "bad-signature"})
NOT_A_JOB = D5_DISPOSITIONS
COUNTED = "used"              # D6 counts only signatures the issuer verified and used (review H3)
JOB_NAMES = ("s_kms", "s_gpg", "p_kms", "p_gpg")

SUBJECTS = {
    "D5": "Tessera D5: signer response only an attacker or a fault produces",
    "D6": "Tessera D6: a kms:Sign no used signature accounts for",
    "D7": "Tessera D7: IAM change in the issuing account",
    "D8": "Tessera D8: a receipt does not verify or is not its request's",
    "W": "Tessera watcher: a check could not be made",
}


@dataclass
class Finding:
    detection: str                 # D5, D6, D7, D8, or W (the watcher's own fault, or an inconsistent issuer record)
    code: str                      # a bounded code naming what was seen
    detail: dict = field(default_factory=dict)

    def line(self):
        """The finding as emitted: every field through its validator (sanitize.RULES)."""
        return {"event": "finding", "v": 1, "detection": S.clean("detection", self.detection),
                "code": S.code(self.code), **S.clean_fields(self.detail)}

    def subject(self):
        det = self.detection if self.detection in SUBJECTS else "W"
        return f"{SUBJECTS[det]} ({S.code(self.code)})"

    def fid(self):
        return hashlib.sha256(json.dumps(self.line(), sort_keys=True).encode()).hexdigest()[:32]

    @classmethod
    def from_line(cls, d):
        """A finding read back from the outbox: rebuilt and validated again on the way out."""
        d = {k: v for k, v in d.items() if k in S.RULES} if isinstance(d, dict) else {}   # no unknown names (H4)
        det, code = d.pop("detection", "W"), d.pop("code", "OUTBOX_UNREADABLE")
        d.pop("event", None)
        d.pop("v", None)
        return cls(det, code, d)


def log(obj, out=None):
    """One JSON object per line. Callers pass only finding lines (validated) and summaries of counts and codes."""
    try:
        (out or sys.stdout).write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
    except BaseException:  # noqa: BLE001  logging never changes behaviour
        pass


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def cred_digest(api_key_id):
    """The issuer's credential digest of an API key id (service/issuer/tessera_issue/api.py, restated)."""
    return sha256hex(("tessera-v1-credential\n" + api_key_id).encode())


def item_id(pk):
    """A stable id for an issuer item key (its SHA-256, 24 hex): what the state and findings hold, never the key."""
    return sha256hex(pk.encode() if isinstance(pk, str) else repr(pk).encode())[:24]


def rfc3339(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(t)))


def parse_time(s):
    try:
        return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError, OverflowError):
        return None


def number(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and abs(v) < 1e11 else None


def empty_state(now):
    return {"v": STATE_VERSION, "created_at": now, "coverage_start": now - LOOKBACK_S,
            "trail": {"cursor": now - LOOKBACK_S, "files": {}, "failing": {}},
            "siglog": {"seen": {}}, "req": {"seen": {}}, "pending": {}, "unlogged": {},
            "sigs": {}, "signs": {}, "reported": {}, "last_ok": None}


@dataclass
class Config:
    account: str
    kms_key_arn: str
    kms_aliases: tuple
    signer_role_arn: str
    trail_prefix: str = ""
    explorers: tuple = ("https://blockstream.info/api", "https://mempool.space/api")
    client_key_ids: dict = field(default_factory=dict)     # client name -> API key id (identifiers, not key values)
    window: dict = None
    catalog: dict = None
    retain_until: str = ""
    watcher_version: str = ""


class SourceDown(Exception):
    pass


class Watcher:
    def __init__(self, cfg, table, results, trail, state, trace, topic, heartbeat, clock=time.time,
                 verify=receipts.verify, remaining=lambda: 1e9, out=None, outbox=None, selfcheck=lambda: None):
        self.cfg, self.table, self.results, self.trail = cfg, table, results, trail
        self.state_store, self.trace, self.topic, self.hb = state, trace, topic, heartbeat
        self.clock, self.verify, self.remaining, self.out = clock, verify, remaining, out
        self.outbox, self.selfcheck = outbox, selfcheck
        self.key = cloudtrail.KeyRefs(cfg.kms_key_arn, cfg.kms_aliases)
        self.by_digest = {cred_digest(v): (k, v) for k, v in (cfg.client_key_ids or {}).items()}
        self.findings, self.unsaved = [], []
        self.st = None

    # ------------------------------------------------------------------------------------------------ helpers
    def find(self, detection, code, **detail):
        """Record a finding: logged at once, and written to the outbox before anything else happens (review M3)."""
        f = Finding(detection, code, detail)
        self.findings.append(f)
        log(f.line(), self.out)
        if self.outbox is None:
            self.unsaved.append(f)
            return
        try:
            self.outbox.put(f.fid(), f.line())
        except Exception as e:  # noqa: BLE001  kept in memory and published directly at the end of this run
            self.unsaved.append(f)
            log({"event": "outbox_write_failed", "v": 1, "error_class": S.class_name(e)}, self.out)

    def find_once(self, key, detection, code, **detail):
        """A finding reported once per key (a repeated failure of the same item is not re-sent every run)."""
        rep = self.st["reported"]
        if key in rep:
            return
        rep[key] = self.clock()
        self.find(detection, code, **detail)

    def item_failed(self, source, ident, exc, **detail):
        cls = S.class_name(exc)
        self.find_once(f"fail:{source}:{ident}:{cls}", "W", "ITEM_CHECK_FAILED", source=source, error_class=cls,
                       **detail)

    def left_s(self):
        return self.remaining() / 1000.0

    # ------------------------------------------------------------------------------------------------ the run
    def run(self):
        now = self.clock()
        st, etag = self.state_store.load()
        if st is None:
            st = empty_state(now)
            etag = self.state_store.save(st, None)                # create-only: coverage start is durable (M2)
        elif st.get("v") != STATE_VERSION:
            raise RuntimeError("watcher state version")
        self.st = st
        healthy = True
        stats = {"ct_files": 0, "ct_records": 0, "signs": 0, "siglog_new": 0, "terminal_new": 0, "traces": 0,
                 "verified": 0}
        code = self.selfcheck()
        if code is not None:                                       # the verifier refuses to start: D8 is blind (M8)
            reason, detail = S.split_code(code)
            self.find_once(f"selfcheck:{code}", "W", "VERIFIER_SELF_CHECK_FAILED", reason=reason,
                           reason_detail=detail)
            healthy = False
        complete = True                                            # every D6 source read in full this run
        try:
            complete = self.read_trail(st, now, stats)
        except SourceDown as e:
            self.find("W", "SOURCE_UNAVAILABLE", source="trail", error_class=str(e))
            healthy = complete = False
        reqs = siglog = None
        try:
            reqs, siglog = self.table.scan()
        except Exception as e:  # noqa: BLE001
            self.find("W", "SOURCE_UNAVAILABLE", source="issuer_table", error_class=S.class_name(e))
            healthy = complete = False
        if siglog is not None:
            complete = self.read_siglog(st, siglog, now, stats) and complete
        if reqs is not None:
            self.note_job_signatures(st, reqs, now, complete)
        if complete:                                               # no D6 outcome from a partial read (final pass)
            self.reconcile(st, now)
        if reqs is not None:
            self.process_requests(st, reqs, now, stats)
        self.prune(st, now)
        delivered, lost = self.deliver()                           # 6: before the commit (at-least-once)
        if lost:                                                   # a finding neither in the outbox nor published:
            raise RuntimeError("finding not delivered")            # no commit, so the next run finds it again
        st["last_ok"] = now
        self.state_store.save(st, etag)                            # 7: the commit; a conflict raises (no heartbeat)
        beat = healthy and delivered and complete                  # D6 not finalized this run: D9 fires if it persists
        if beat:
            try:
                self.hb.beat()                                     # 8: D9 heartbeat only after a committed, sound run
            except Exception as e:  # noqa: BLE001  D9 then fires by silence
                beat = False
                log({"event": "heartbeat_failed", "v": 1, "error_class": S.class_name(e)}, self.out)
        summary = dict(stats, event="watch_summary", v=1, findings=len(self.findings), pending=len(st["pending"]),
                       heartbeat=beat, at=rfc3339(now))
        log(summary, self.out)
        return summary

    def deliver(self):
        """Publish every finding waiting in the outbox (this run's and any earlier run's), deleting each only after SNS
        accepted it; then any finding this run could not write to the outbox. -> (ok, lost): ok if nothing is left
        unpublished; lost if a finding that is not in the outbox could not be published."""
        ok, lost = True, False
        if self.outbox is not None:
            try:
                keys = self.outbox.keys()
            except Exception as e:  # noqa: BLE001
                log({"event": "outbox_unreadable", "v": 1, "error_class": S.class_name(e)}, self.out)
                keys, ok = [], False
            for k in keys:
                try:
                    f = Finding.from_line(self.outbox.get(k))
                    self.topic.publish(f.subject(), json.dumps(f.line(), sort_keys=True, indent=1))
                    self.outbox.delete(k)
                except Exception as e:  # noqa: BLE001  stays in the outbox; the next run publishes it
                    ok = False
                    log({"event": "publish_failed", "v": 1, "error_class": S.class_name(e)}, self.out)
        for f in self.unsaved:
            try:
                self.topic.publish(f.subject(), json.dumps(f.line(), sort_keys=True, indent=1))
            except Exception as e:  # noqa: BLE001
                ok, lost = False, True
                log({"event": "publish_failed", "v": 1, "error_class": S.class_name(e)}, self.out)
        return ok, lost

    # ------------------------------------------------------------------------------------- 2: the trail
    def read_trail(self, st, now, stats):
        t = st["trail"]
        base = cloudtrail.base_prefix(self.cfg.trail_prefix, self.cfg.account)
        try:
            keys = cloudtrail.candidate_keys(self.trail.c, self.trail.b, base, t["cursor"], now)
        except Exception as e:  # noqa: BLE001
            raise SourceDown(S.class_name(e)) from None
        first_unread, complete = None, True
        for key in keys:
            if key in t["files"]:
                continue
            kt = cloudtrail.key_time(key)
            if self.left_s() < TRAIL_RESERVE_S:                    # out of time: the cursor stops at this file
                first_unread = kt if first_unread is None else min(first_unread, kt)
                complete = False
                break                                              # keys are in time order: none later is earlier
            try:
                records = cloudtrail.parse(self.trail.get(key))
            except Exception as e:  # noqa: BLE001  this file only; retried until LOOKBACK_S after its time
                cls = S.class_name(e)
                where = cloudtrail.safe_parts(key)
                complete = False
                if now - kt > LOOKBACK_S:
                    self.find("W", "TRAIL_FILE_ABANDONED", error_class=cls, **where)
                    t["files"][key] = kt
                    t["failing"].pop(key, None)
                    continue
                if cls not in t["failing"].setdefault(key, []):
                    t["failing"][key].append(cls)
                    self.find("W", "TRAIL_FILE_UNREADABLE", error_class=cls, **where)
                first_unread = kt if first_unread is None else min(first_unread, kt)
                continue
            stats["ct_files"] += 1
            stats["ct_records"] += len(records)
            for i, rec in enumerate(records):
                try:
                    for kind, d in cloudtrail.classify(rec, self.key, self.cfg.signer_role_arn):
                        self.on_trail_event(st, kind, d, rec, stats)
                except Exception as e:  # noqa: BLE001  this record only; reported, not retried
                    complete = False
                    self.item_failed("trail", f"{item_id(key)}:{i}", e, **cloudtrail.safe_parts(key))
            t["files"][key] = kt
            t["failing"].pop(key, None)
        target = now - TRAIL_LAG_S
        if first_unread is not None:
            target = min(target, first_unread)
        t["cursor"] = max(t["cursor"], target)
        return complete

    def on_trail_event(self, st, kind, d, rec, stats):
        if kind == "sign":
            raw = d["event_id"]
            eid = raw if isinstance(raw, str) and S.UUID.fullmatch(raw) else "h" + item_id(json.dumps(raw))
            if eid in st["signs"]:
                return
            t = cloudtrail.event_time(rec)
            st["signs"][eid] = {"t": t, "seen": self.clock(), "principal": S.principal(d["principal"]), "sig": None,
                                "reported": False, "final": False}
            stats["signs"] += 1
            if t is None:                                          # a Sign that cannot be placed in time
                st["signs"][eid]["reported"] = True
                self.find("D6", "SIGN_TIME_UNREADABLE", event_id=raw, principal=d["principal"])
        elif kind == "foreign_sign":                               # alarmed; never matched against a signature
            self.find("D6", "SIGN_BY_OTHER_PRINCIPAL", **d)
        elif kind == "access_denied":
            self.find("D6", "ACCESS_DENIED_ON_KEY", **d)
        elif kind == "iam_write":
            self.find("D7", "IAM_WRITE", latency_note="read from the trail: CloudTrail delivery plus up to one "
                      "watcher interval", **d)

    # ----------------------------------------------------------------------------------- 3: SIGLOG# (D5)
    def read_siglog(self, st, siglog, now, stats):
        s = st["siglog"]
        present, complete = set(), True
        for pk, e in siglog:
            iid = item_id(pk)
            present.add(iid)
            if iid in s["seen"]:
                continue
            try:
                self.on_siglog(st, iid, e, now, stats)
            except Exception as ex:  # noqa: BLE001  this entry only; not marked seen, so retried next run
                self.item_failed("siglog", iid, ex, item=iid[:16])
                complete = False
                continue
            s["seen"][iid] = now
        s["seen"] = {k: v for k, v in s["seen"].items() if k in present}
        return complete

    def on_siglog(self, st, iid, e, now, stats):
        at = parse_time(e.get("at")) if isinstance(e, dict) else None
        if at is None:
            self.find("D5", "SIGLOG_UNREADABLE", item=iid[:16])
            return
        stats["siglog_new"] += 1
        future = at > now + FUTURE_S
        if future:
            self.find("W", "ISSUER_TIME_IN_FUTURE", source="siglog", item=iid[:16], at=e.get("at"))
        ids = {k: e.get(k) for k in ("slot", "request_id", "status", "reason", "disposition", "attempt",
                                      "frame_sha256", "signature_sha256", "at")}
        disp, reason = e.get("disposition"), e.get("reason")
        if disp in D5_DISPOSITIONS:
            self.find("D5", "DISPOSITION_" + disp.upper().replace("-", "_"), **ids)
        if reason in D5_REASONS:
            self.find("D5", "REASON_" + reason, **ids)
        h = e.get("signature_sha256")
        if (e.get("slot") == "kms" and e.get("status") == "SIGNED" and isinstance(h, str) and S.HEX64.fullmatch(h)
                and disp not in NOT_A_JOB):
            d = S.clean("disposition", disp)
            cur = st["sigs"].get(h)
            if cur is None:
                cur = st["sigs"][h] = {"at": at, "first_seen": now, "request_id": S.clean("request_id",
                                                                                         e.get("request_id")),
                                       "event": None, "final": None, "dispositions": [], "used": False,
                                       "future": False, "reported": False}
            elif not cur["final"]:
                cur["at"] = min(cur["at"], at)
            if d not in cur["dispositions"]:
                cur["dispositions"].append(d)
            cur["future"] = cur["future"] or future
            cur["used"] = cur["used"] or disp == COUNTED

    def note_job_signatures(self, st, reqs, now, complete=True):
        """A kms signature on a job with no SIGLOG# entry at all is tracked (M5) and, after UNLOGGED_S, reported, but
        only from a run whose SIGLOG# read was complete. A job signature does not count for D6 by itself: only a "used"
        SIGLOG# entry does (the issuer logs it before recording the job), so deleting that entry leaves the Sign
        unmatched (final pass)."""
        for pk, rec in reqs:
            try:
                for a in (rec.get("attempts") or []) if isinstance(rec, dict) else []:
                    for j in (a.get("jobs") or {}).values():
                        if not isinstance(j, dict) or j.get("slot") != "kms":
                            continue
                        h = j.get("sig_sha256")
                        if not (isinstance(h, str) and S.HEX64.fullmatch(h)):
                            continue
                        if h in st["sigs"]:
                            st["unlogged"].pop(h, None)
                        else:
                            st["unlogged"].setdefault(h, now)
            except Exception as e:  # noqa: BLE001
                self.item_failed("request", item_id(pk), e)
        for h, first in list(st["unlogged"].items()):
            if h in st["sigs"]:
                st["unlogged"].pop(h)
            elif complete and now - first > UNLOGGED_S:
                self.find_once(f"unlogged:{h}", "D6", "JOB_SIGNATURE_NOT_LOGGED", signature_sha256=h)

    # ------------------------------------------------------------------------------------------ 4: D6
    @staticmethod
    def counts(sg):
        return sg["used"] and not sg["future"]

    def reconcile(self, st, now):
        """Time order, one to one: each counted kms signature (one the issuer verified and used), ordered by when the
        issuer first logged it, takes the earliest free signer-role Sign in [at - MATCH_WINDOW_S, at + SKEW_S]. Signs
        carry no message or signature, so this matches by time and count only. The matching is recomputed every
        complete run (the caller skips a run with a partial read, final pass) over everything not yet final (review
        M1): a Sign delivered late can still take its place in the order. A
        signature's match (or its absence) becomes final SIG_HORIZON_S after it was logged, when every Sign it could
        take has been delivered; a Sign is declared unmatched SIGN_HORIZON_S after its time."""
        sigs, signs = st["sigs"], st["signs"]
        for sg in sigs.values():
            if not sg["final"]:
                sg["event"] = None
        for s in signs.values():
            if not s["final"]:
                s["sig"] = None
        free = sorted((s["t"], eid) for eid, s in signs.items() if not s["final"] and s["t"] is not None)
        for h, sg in sorted(sigs.items(), key=lambda kv: (kv[1]["at"], kv[0])):
            if sg["final"] or not self.counts(sg):
                continue
            for i, (t, eid) in enumerate(free):
                if sg["at"] - MATCH_WINDOW_S <= t <= sg["at"] + SKEW_S:
                    sg["event"], signs[eid]["sig"] = eid, h
                    del free[i]
                    break
        for h, sg in sigs.items():
            if sg["final"] or not self.counts(sg) or now - sg["at"] <= SIG_HORIZON_S:
                continue
            if sg["event"] is not None:
                sg["final"] = "matched"
                signs[sg["event"]]["final"] = True
            elif sg["at"] < st["coverage_start"]:
                sg["final"] = "before-coverage"                    # logged before the first trail window
            else:
                sg["final"] = "unmatched"
                self.find("D6", "SIGNATURE_WITHOUT_SIGN_EVENT", signature_sha256=h, request_id=sg["request_id"],
                          logged_at=rfc3339(sg["at"]))
        for eid, s in signs.items():
            if s["sig"] is None and not s["reported"] and s["t"] is not None and now - s["t"] > SIGN_HORIZON_S:
                s["reported"] = True
                self.find("D6", "SIGN_WITHOUT_SIGNED_JOB", event_id=eid, event_time=rfc3339(s["t"]),
                          principal=s["principal"])

    def sig_status(self, sg):
        if not self.counts(sg):
            return "not-counted"
        if sg["final"]:
            return sg["final"]
        return "pending"

    # ------------------------------------------------------------------------------- 5: REQ# (D8, 0(a))
    def process_requests(self, st, reqs, now, stats):
        r, pending = st["req"], st["pending"]
        present = {}
        for pk, rec in reqs:
            try:
                if not isinstance(rec, dict):
                    self.find_once(f"requnreadable:{item_id(pk)}", "W", "REQUEST_UNREADABLE", item=item_id(pk)[:16])
                    continue
                if rec.get("state") not in TERMINAL:
                    continue
                rid = rec.get("rid")
                if not (isinstance(rid, str) and S.HEX64.fullmatch(rid) and pk == "REQ#" + rid):
                    self.find_once(f"badrid:{item_id(pk)}", "W", "REQUEST_ID_INVALID", item=item_id(pk)[:16])
                    continue
                present[rid] = rec
                if rid in r["seen"] or rid in pending:
                    continue
                stats["terminal_new"] += 1
                ended = number(rec.get("ended_at"))
                if ended is None:
                    self.find("W", "TERMINAL_TIME_INVALID", rid=rid)
                elif ended > now + FUTURE_S:
                    self.find("W", "ISSUER_TIME_IN_FUTURE", source="request", rid=rid)
                pending[rid] = {"first_seen": now, "verify": None, "reported": [], "last_try": 0,
                                "snap": self.snapshot(rec)}
            except Exception as e:  # noqa: BLE001
                self.item_failed("request", item_id(pk), e)
        r["seen"] = {k: v for k, v in r["seen"].items() if k in present}
        verified = 0
        for rid in sorted(pending, key=lambda k: (pending[k]["last_try"], pending[k]["first_seen"], k)):
            p = pending[rid]
            try:
                rec = present.get(rid)
                if rec is not None:                                # the snapshot is the one taken when first seen
                    p["source"] = "issuer-record"                  # terminal: never refreshed (final pass, M9)
                else:                                              # gone (expired) while pending: trace what we hold
                    p["source"] = "snapshot"
                    self.find_once(f"gone:{rid}", "W", "TRACE_FROM_SNAPSHOT", rid=rid)
                snap = p["snap"]
                if snap["state"] == "COMPLETE" and p["verify"] is None:
                    if rec is None:
                        p["verify"] = self.unchecked(snap, p, now, "RECORD_GONE")
                    elif verified < MAX_VERIFY_PER_RUN and self.left_s() - FINISH_RESERVE_S >= MIN_VERIFY_S:
                        verified += 1
                        p["last_try"] = now
                        p["verify"] = self.check_receipt(snap, p, now)
                        if p["verify"] is not None:
                            stats["verified"] += 1
                    elif now - p["first_seen"] > D8_GIVE_UP_S:     # deferred behind a backlog too long (M4)
                        p["verify"] = self.unchecked(snap, p, now, "D8_BACKLOG")
                    if p["verify"] is None:
                        continue                                   # stays pending; a later run continues
                trace = self.trace_record(st, snap, p, now)
                if trace is None:
                    continue                                       # a kms signature not yet final
                try:
                    self.trace.put(rid, trace)
                except Exception as e:  # noqa: BLE001  retried every run until it is written (M5)
                    cls = S.class_name(e)
                    self.find_once(f"tracefail:{rid}:{cls}", "W", "TRACE_WRITE_FAILED", rid=rid, error_class=cls)
                    continue
                stats["traces"] += 1
                r["seen"][rid] = now
                pending.pop(rid)
            except Exception as e:  # noqa: BLE001  this request only; it stays pending
                self.item_failed("request", rid, e, rid=rid)

    def unchecked(self, snap, p, now, reason):
        self.find("D8", "RECEIPT_UNCHECKED", rid=snap["rid"], receipt_sha256=snap["receipt_sha256"], reason=reason,
                  bound_s=D8_GIVE_UP_S)
        return {"receipt_sha256": snap["receipt_sha256"], "checked_at": rfc3339(now), "verdict": "UNCHECKED",
                "reason": reason}

    def snapshot(self, rec):
        """The request fields a trace record holds, validated, taken while the REQ# item exists (M5). The plaintext
        request key is hashed here and never kept."""
        key = rec.get("key")
        attempts = []
        for a in rec.get("attempts") or []:
            if not isinstance(a, dict):
                continue
            end = a.get("end") if isinstance(a.get("end"), dict) else {}
            reason, detail = S.split_code(end.get("reason"))
            jobs = {}
            for name, j in sorted((a.get("jobs") or {}).items()):
                if not isinstance(j, dict) or not isinstance(name, str) or not S.JOB_NAME.fullmatch(name):
                    continue
                jobs[name] = {"slot": S.clean("slot", j.get("slot")),
                              "signer_request_id": S.clean("signer_request_id", j.get("request_id")),
                              "frame_sha256": S.clean("frame_sha256", j.get("frame_sha256")),
                              "signature_sha256": S.clean("signature_sha256", j.get("sig_sha256"))}
            attempts.append({"id": S.clean("id", a.get("id")), "state": S.clean("state", a.get("state")),
                             "declared_issue_time": S.clean("declared_issue_time", a.get("declared_issue_time")),
                             "receipt_id": S.clean("receipt_id", a.get("receipt_id")),
                             "end": {"outcome": S.clean("outcome", end.get("outcome")), "reason": reason,
                                     "reason_detail": detail},
                             "jobs": jobs})
        reason, detail = S.split_code(rec.get("reason"))
        created, ended = number(rec.get("created_at")), number(rec.get("ended_at"))
        return {"rid": rec["rid"], "cred": S.clean("credential_digest", rec.get("cred")),
                "request_key_sha256": sha256hex(key.encode()) if isinstance(key, str) else None,
                "content_sha256": S.clean("content_sha256", rec.get("content_sha256")),
                "content_len": S.clean("content_len", rec.get("content_len")),
                "state": S.clean("state", rec.get("state")), "reason": reason, "reason_detail": detail,
                "created_at": rfc3339(created) if created is not None else None,
                "ended_at": rfc3339(ended) if ended is not None else None,
                "receipt_sha256": S.clean("receipt_sha256", rec.get("receipt_sha256")), "attempts": attempts}

    def check_receipt(self, snap, p, now):
        """-> the verification outcome dict, or None to retry next run."""
        rid, digest = snap["rid"], snap["receipt_sha256"]
        out = {"receipt_sha256": digest, "checked_at": rfc3339(now)}
        if not (isinstance(digest, str) and S.HEX64.fullmatch(digest)):
            self.find("D8", "COMPLETE_WITHOUT_RECEIPT_DIGEST", rid=rid)
            return dict(out, receipt_sha256=None, verdict="NO_RECEIPT", reason="NO_DIGEST")
        try:
            data = self.results.receipt(rid, digest)
        except Exception as e:  # noqa: BLE001  unreadable (not absent): a D8 finding, retried until the bound (H1)
            cls = S.class_name(e)
            if f"unreadable:{cls}" not in p["reported"]:
                p["reported"].append(f"unreadable:{cls}")
                self.find("D8", "RECEIPT_OBJECT_UNREADABLE", rid=rid, receipt_sha256=digest, error_class=cls)
            if now - p["first_seen"] > D8_GIVE_UP_S:
                return dict(out, verdict="NO_RECEIPT", reason="OBJECT_UNREADABLE")
            return None
        if data is None:
            self.find("D8", "RECEIPT_OBJECT_MISSING", rid=rid, receipt_sha256=digest)
            return dict(out, verdict="NO_RECEIPT", reason="OBJECT_MISSING")
        if sha256hex(data) != digest:
            self.find("D8", "RECEIPT_BYTES_DIGEST_MISMATCH", rid=rid, receipt_sha256=digest,
                      stored_sha256=sha256hex(data))
            return dict(out, verdict="DIGEST_MISMATCH", reason="STORED_BYTES")
        budget = min(receipts.VERIFY_CAP_S + 60, self.left_s() - FINISH_RESERVE_S)
        try:
            v = self.verify(data, self.cfg.window, self.cfg.catalog, rfc3339(now), list(self.cfg.explorers),
                            budget_s=budget)
        except receipts.Uncheckable as e:
            self.find("D8", "RECEIPT_UNCHECKED", rid=rid, receipt_sha256=digest, reason=e.code, bound_s=0)
            return dict(out, verdict="UNCHECKED", reason=e.code)
        except receipts.Unavailable as e:
            if e.code not in p["reported"]:
                p["reported"].append(e.code)
                self.find("W", "RECEIPT_CHECK_UNAVAILABLE", rid=rid, reason=e.code)
            if now - p["first_seen"] > D8_GIVE_UP_S:
                self.find("D8", "RECEIPT_UNCHECKED", rid=rid, receipt_sha256=digest, reason=e.code,
                          bound_s=D8_GIVE_UP_S)
                return dict(out, verdict="UNCHECKED", reason=e.code)
            return None
        except Exception as e:  # noqa: BLE001  an unexpected failure of this check: bounded like Unavailable
            self.item_failed("request", rid, e, rid=rid)
            if now - p["first_seen"] > D8_GIVE_UP_S:
                self.find("D8", "RECEIPT_UNCHECKED", rid=rid, receipt_sha256=digest, reason="CHECK_FAILED",
                          bound_s=D8_GIVE_UP_S)
                return dict(out, verdict="UNCHECKED", reason="CHECK_FAILED")
            return None
        verdict = v.get("verdict")
        if verdict != receipts.PASS:
            self.find("D8", "VERDICT_" + str(verdict), rid=rid, receipt_sha256=digest, reason=v.get("reason"))
            return dict(out, verdict=verdict, reason=v.get("reason"), binding=None)
        bad = self.mismatch(snap, v.get("binding"))
        if bad is None:
            self.find("D8", "RECEIPT_NOT_BOUND", rid=rid, receipt_sha256=digest)
            return dict(out, verdict="NOT_BOUND", reason="BINDING_UNREADABLE", verifier_verdict=verdict,
                        binding="unreadable")
        if bad:
            self.find("D8", "RECEIPT_NOT_THIS_REQUEST", rid=rid, receipt_sha256=digest, mismatch=bad)
            return dict(out, verdict="NOT_BOUND", reason="RECEIPT_NOT_THIS_REQUEST", verifier_verdict=verdict,
                        binding="mismatch", mismatch=bad)
        return dict(out, verdict=verdict, reason=v.get("reason"), anchor_heights=v.get("heights"), T=v.get("T"),
                    binding="match")

    @staticmethod
    def mismatch(snap, b):
        """M9: the receipt's commitments against its record. -> None if unbound, else the list of fields that differ
        (content digest and length always; each job signature, the attempt's receipt_id and declared issue time where
        the shipped attempt records them)."""
        if not isinstance(b, dict):
            return None
        bad = [k for k in ("content_sha256", "content_len") if snap.get(k) != b.get(k)]
        shipped = [a for a in snap["attempts"] if a["state"] == "shipped"]
        if len(shipped) > 1:
            return bad + ["receipt_id"]
        if shipped:
            a = shipped[0]
            for name in JOB_NAMES:
                rec_h = (a["jobs"].get(name) or {}).get("signature_sha256")
                if rec_h is not None and rec_h != (b.get("sigs") or {}).get(name):
                    bad.append(name)
            if a.get("receipt_id") is not None and a["receipt_id"] != b.get("receipt_id"):
                bad.append("receipt_id")
            if a.get("declared_issue_time") is not None and a["declared_issue_time"] != b.get("declared_issue_time"):
                bad.append("declared_issue_time")
        return bad

    # ------------------------------------------------------------------------------------- 0(a) trace record
    def trace_record(self, st, snap, p, now):
        """The accounting record (contract item 0(a)), from the validated snapshot. Fields: digests, ids, states, codes.
        Never the request content, the plaintext request key, an API key value, a URL. -> dict, or None while a kms
        signature of the request is not final (or a job signature has not appeared in SIGLOG# yet)."""
        by_rid = {}
        for h, sg in st["sigs"].items():
            by_rid.setdefault(sg.get("request_id"), []).append((h, sg))
        attempts, waiting = [], False
        for a in snap["attempts"]:
            jobs = {}
            for name, j in a["jobs"].items():
                entry = dict(j)
                if j["slot"] == "kms":
                    signs, hashes = [], set()
                    srid = j["signer_request_id"]
                    joined = by_rid.get(srid, []) if srid not in (None, S.WITHHELD) else []
                    for h, sg in sorted(joined, key=lambda x: (x[1]["at"], x[0])):
                        status = self.sig_status(sg)
                        waiting = waiting or status == "pending"
                        hashes.add(h)
                        signs.append({"signature_sha256": h, "reconciled": status,
                                      "cloudtrail_sign_event_id": sg["event"] if status == "matched" else None,
                                      "dispositions": sg["dispositions"]})
                    h = j["signature_sha256"]
                    if h not in (None, S.WITHHELD) and h not in hashes:
                        sg = st["sigs"].get(h)
                        if sg is None:                             # on the job, not (yet) in SIGLOG# (M5)
                            waiting = waiting or h in st["unlogged"] and now - st["unlogged"][h] <= UNLOGGED_S
                            signs.append({"signature_sha256": h, "reconciled": "not-logged",
                                          "cloudtrail_sign_event_id": None, "dispositions": []})
                    entry["kms_signs"] = signs
                else:
                    entry["gcp_use_to_sign"] = "TODO: slot 2 reconciliation not built (G4)"
                jobs[name] = entry
            attempts.append(dict(a, jobs=jobs))
        if waiting and now - p["first_seen"] < TRACE_WAIT_S:
            return None
        client = self.by_digest.get(snap["cred"])
        v = p.get("verify") or {}
        verification = None
        if v:
            reason, detail = S.split_code(v.get("reason"))
            verification = {"verdict": S.clean("verdict", v.get("verdict")), "reason": reason, "reason_detail": detail,
                            "checked_at": v.get("checked_at"), "binding": S.clean("binding", v.get("binding")),
                            "verifier_verdict": S.clean("verifier_verdict", v.get("verifier_verdict")),
                            "mismatch": S.clean("mismatch", v["mismatch"]) if "mismatch" in v else None}
        bound = v.get("binding") == "match"
        return {
            "format": "tessera-v1-trace/1",
            "written_at": rfc3339(now), "watcher_version": S.clean("watcher_version", self.cfg.watcher_version),
            "record_source": p.get("source", "issuer-record"),
            "credential_digest": snap["cred"],
            "api_key_id": S.clean("api_key_id", client[1]) if client else None,
            "client": S.clean("client", client[0]) if client else None,
            "rid": snap["rid"], "request_key_sha256": snap["request_key_sha256"],
            "content_sha256": snap["content_sha256"], "content_len": snap["content_len"],
            "state": snap["state"], "reason": snap["reason"], "reason_detail": snap["reason_detail"],
            "created_at": snap["created_at"], "ended_at": snap["ended_at"],
            "attempts": attempts,
            "receipt_sha256": snap["receipt_sha256"],
            # anchors and T only for a receipt bound to this request (M9): another request's would misattribute them
            "anchor_heights": S.heights(v.get("anchor_heights")) if bound else None,
            "T": S.clean("T", v.get("T")) if bound else None,
            "verification": verification,
            "slot2_reconciliation": "TODO: GCP useToSign not read (G4 open)",
        }

    # ------------------------------------------------------------------------------------------- pruning
    def prune(self, st, now):
        cut = now - RETAIN_S
        st["sigs"] = {h: s for h, s in st["sigs"].items() if not (s["final"] and s["at"] < cut)
                      and not (not self.counts(s) and s["first_seen"] < cut)}
        st["signs"] = {e: s for e, s in st["signs"].items() if (s["t"] if s["t"] is not None else s["seen"]) >= cut
                       or not (s["final"] or s["reported"])}
        t = st["trail"]
        t["files"] = {k: kt for k, kt in t["files"].items() if kt is not None and kt >= t["cursor"] - 3600}
        t["failing"] = {k: v for k, v in t["failing"].items() if k not in t["files"]}
        st["unlogged"] = {h: v for h, v in st["unlogged"].items() if v >= cut}
        st["reported"] = {k: v for k, v in st["reported"].items() if v >= now - REPORTED_RETAIN_S}
