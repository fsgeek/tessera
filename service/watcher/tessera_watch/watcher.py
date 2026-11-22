"""One watcher run (docs/V1-DETECTION-CONTRACT.md, the Arariwa item 0(b); D5, D6, D7 IAM, D8; trace records 0(a)).

Order of a run, and why it never skips:
  1. load the durable state (its ETag is the commit guard);
  2. read new CloudTrail files (D6 Sign events, AccessDenied on the key, D7 IAM writes);
  3. scan the issuer table: new SIGLOG# entries (D5; kms signatures for D6) and newly terminal REQ# records;
  4. reconcile kms:Sign events against signed kms jobs (D6);
  5. for each terminal request: re-verify a COMPLETE receipt (D8), then write its trace record (0(a)) once its kms
     signatures are reconciled (or declared unmatched);
  6. publish every finding (SNS) and log it; 7. commit the state; 8. publish the heartbeat (D9).
A crash anywhere before step 7 leaves the old state, so the next run reads the same files and items again: findings
are at-least-once (a repeat is possible, a loss is not), and trace writes are write-once (an existing record is kept).
Every candidate a run sees is, in the state it commits, either done or pending; the watermarks only move past items
that are one or the other.

Nothing here imports issuer code. The request id formula is the issuer's documented one, restated."""
import calendar
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field

from . import cloudtrail, receipts

STATE_VERSION = 1
TERMINAL = ("COMPLETE", "REFUSED", "FAILED")
OVERLAP_S = 3600              # REQ#/SIGLOG# watermarks look back this far (a write commits seconds after its clock read)
MATCH_WINDOW_S = 40 * 60      # D6: a Sign at t is accounted for by a kms signature first logged in [t - SKEW, t + this]
SKEW_S = 120                  # D6: clock difference between CloudTrail eventTime and the issuer's Lambda clock
CT_LAG_S = 45 * 60            # D6: a logged signature with no Sign in the trail this long after it is unmatched
LOOKBACK_S = 24 * 3600        # CloudTrail files with a key timestamp older than this are not read
D8_GIVE_UP_S = 6 * 3600       # D8: a receipt that cannot be checked for this long is reported UNCHECKED (bounded)
RETAIN_S = 45 * 24 * 3600     # D6 reconciliation memory: signatures and Signs kept this long, then pruned
VERIFY_RESERVE_S = 120        # no new verification is started with less than this left in the invocation

# D5: signer reasons only an attacker or a fault produces, and the poller dispositions (contract table, row D5).
D5_REASONS = frozenset({"KEY_FP_MISMATCH", "FRAME_DIGEST_MISMATCH", "ALG_NOT_ALLOWED", "DECLARED_TIME_OUTSIDE_EPSILON",
                        "BAD_REQUEST", "TRUNCATED", "UNRECOGNIZED_REASON"})
D5_DISPOSITIONS = frozenset({"unrequested", "malformed", "bad-signature"})
NOT_A_JOB = D5_DISPOSITIONS                   # D6: such a response is not a signed job, whatever it carries

SUBJECTS = {
    "D5": "Tessera D5: signer response only an attacker or a fault produces",
    "D6": "Tessera D6: a kms signature no signed job accounts for",
    "D7": "Tessera D7: IAM change in the issuing account",
    "D8": "Tessera D8: a receipt does not verify VALID_STRICT",
    "W": "Tessera watcher: a check could not be made",
}


@dataclass
class Finding:
    detection: str                 # D5, D6, D7, D8, or W (the watcher's own fault)
    code: str                      # a bounded code naming what was seen
    detail: dict = field(default_factory=dict)

    def line(self):
        return {"event": "finding", "v": 1, "detection": self.detection, "code": self.code, **self.detail}

    def subject(self):
        return f"{SUBJECTS[self.detection]} ({self.code})"


def log(obj, out=None):
    """One JSON object per line (same rules as service/issuer/LOGGING.md: ids, digests of signatures and frames, codes;
    never request content or its digest, the request key, an API key, a URL or exception text). Best effort."""
    try:
        (out or sys.stdout).write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
    except BaseException:  # noqa: BLE001  logging never changes behaviour
        pass


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def cred_digest(api_key_id):
    """The issuer's credential digest of an API key id (service/issuer/tessera_issue/api.py, restated)."""
    return sha256hex(("tessera-v1-credential\n" + api_key_id).encode())


def rfc3339(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(t)))


def parse_time(s):
    try:
        return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


def empty_state(now):
    return {"v": STATE_VERSION, "created_at": now, "coverage_start": now - LOOKBACK_S,
            "req": {"watermark": 0, "seen": {}}, "pending": {},
            "siglog": {"watermark": 0, "seen": {}},
            "sigs": {}, "signs": {}, "ct_files": {}, "last_ok": None}


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


class Watcher:
    def __init__(self, cfg, table, results, trail, state, trace, topic, heartbeat, clock=time.time,
                 verify=receipts.verify, remaining=lambda: 1e9, out=None):
        self.cfg, self.table, self.results, self.trail = cfg, table, results, trail
        self.state_store, self.trace, self.topic, self.hb = state, trace, topic, heartbeat
        self.clock, self.verify, self.remaining, self.out = clock, verify, remaining, out
        self.key = cloudtrail.KeyRefs(cfg.kms_key_arn, cfg.kms_aliases)
        self.by_digest = {cred_digest(v): (k, v) for k, v in (cfg.client_key_ids or {}).items()}
        self.findings = []

    # ------------------------------------------------------------------------------------------------ helpers
    def find(self, detection, code, **detail):
        self.findings.append(Finding(detection, code, detail))

    # ------------------------------------------------------------------------------------------------ the run
    def run(self):
        now = self.clock()
        st, etag = self.state_store.load()
        if st is None:
            st = empty_state(now)
        elif st.get("v") != STATE_VERSION:
            raise RuntimeError("watcher state version")
        stats = {"ct_files": 0, "ct_records": 0, "signs": 0, "siglog_new": 0, "terminal_new": 0, "traces": 0,
                 "verified": 0}
        self.read_trail(st, now, stats)
        reqs, siglog = self.table.scan()
        self.read_siglog(st, siglog, stats)
        self.reconcile(st, now)
        self.process_requests(st, reqs, now, stats)
        self.prune(st, now)
        for f in self.findings:                                   # 6: findings before the commit (at-least-once)
            log(f.line(), self.out)
            self.topic.publish(f.subject(), json.dumps(f.line(), sort_keys=True, indent=1))
        st["last_ok"] = now
        self.state_store.save(st, etag)                           # 7: the commit; a conflict raises (no heartbeat)
        self.hb.beat()                                            # 8: D9 heartbeat only after a committed run
        summary = dict(stats, event="watch_summary", v=1, findings=len(self.findings),
                       pending=len(st["pending"]), at=rfc3339(now))
        log(summary, self.out)
        return summary

    # ------------------------------------------------------------------------------------- 2: the trail
    def read_trail(self, st, now, stats):
        base = cloudtrail.base_prefix(self.cfg.trail_prefix, self.cfg.account)
        since = max(st["coverage_start"], now - LOOKBACK_S)
        for key in cloudtrail.candidate_keys(self.trail.c, self.trail.b, base, since, now):
            if key in st["ct_files"]:
                continue
            raw = self.trail.get(key)                             # a read error raises: retried next run
            try:
                records = cloudtrail.parse(raw)
            except ValueError as e:
                self.find("W", "TRAIL_FILE_UNREADABLE", file=key.rsplit("/", 1)[-1], error=str(e))
                records = []
            stats["ct_files"] += 1
            stats["ct_records"] += len(records)
            for rec in records:
                for kind, d in cloudtrail.classify(rec, self.key, self.cfg.signer_role_arn):
                    self.on_trail_event(st, kind, d, rec, stats)
            st["ct_files"][key] = cloudtrail.key_time(key)

    def on_trail_event(self, st, kind, d, rec, stats):
        if kind == "sign":
            eid = d["event_id"]
            if eid and eid not in st["signs"]:
                st["signs"][eid] = {"t": cloudtrail.event_time(rec), "principal": d["principal"], "sig": None,
                                    "reported": False}
                stats["signs"] += 1
        elif kind == "foreign_sign":                              # alarmed; never matched against a signed job
            self.find("D6", "SIGN_BY_OTHER_PRINCIPAL", **d)
        elif kind == "access_denied":
            self.find("D6", "ACCESS_DENIED_ON_KEY", **d)
        elif kind == "iam_write":
            self.find("D7", "IAM_WRITE", latency_note="read from the trail: CloudTrail delivery plus up to one "
                      "watcher interval", **d)

    # ----------------------------------------------------------------------------------- 3: SIGLOG# (D5)
    def read_siglog(self, st, siglog, stats):
        s = st["siglog"]
        floor = s["watermark"] - OVERLAP_S
        top = s["watermark"]
        bad = s.setdefault("unreadable", [])                     # kept for good: SIGLOG# items never expire
        for pk, e in siglog:
            if pk in s["seen"] or pk in bad:
                continue
            at = parse_time(e.get("at")) if isinstance(e, dict) else None
            if at is None:
                bad.append(pk)
                self.find("D5", "SIGLOG_UNREADABLE", item=pk[:80])
                continue
            if at < floor:
                continue
            stats["siglog_new"] += 1
            s["seen"][pk] = at
            top = max(top, at)
            ids = {k: e.get(k) for k in ("slot", "request_id", "status", "reason", "disposition", "attempt",
                                          "frame_sha256", "signature_sha256", "at")}
            if e.get("disposition") in D5_DISPOSITIONS:
                self.find("D5", "DISPOSITION_" + e["disposition"].upper().replace("-", "_"), **ids)
            if e.get("reason") in D5_REASONS:
                self.find("D5", "REASON_" + e["reason"], **ids)
            if (e.get("slot") == "kms" and e.get("status") == "SIGNED" and e.get("signature_sha256")
                    and e.get("disposition") not in NOT_A_JOB):
                h = e["signature_sha256"]
                cur = st["sigs"].get(h)
                if cur is None:
                    st["sigs"][h] = {"at": at, "request_id": e.get("request_id"), "event": None, "missing": False,
                                     "dispositions": [e.get("disposition")]}
                else:
                    cur["at"] = min(cur["at"], at)
                    if e.get("disposition") not in cur["dispositions"]:
                        cur["dispositions"].append(e.get("disposition"))
        s["watermark"] = top
        s["seen"] = {k: v for k, v in s["seen"].items() if v >= top - OVERLAP_S}

    # ------------------------------------------------------------------------------------------ 4: D6
    def reconcile(self, st, now):
        """One-to-one in time order: each kms signature (ordered by when the issuer first logged it) takes the earliest
        unmatched Sign in [at - MATCH_WINDOW_S, at + SKEW_S]. CloudTrail Sign records carry no message or signature, so
        this matches by time and count only; which Sign event id is attributed to which signature is the time-order
        rule, not evidence of content."""
        free = sorted((v["t"], eid) for eid, v in st["signs"].items() if v["sig"] is None and v["t"] is not None)
        for h, sg in sorted(st["sigs"].items(), key=lambda kv: (kv[1]["at"], kv[0])):
            if sg["event"] is not None:
                continue
            for i, (t, eid) in enumerate(free):
                if sg["at"] - MATCH_WINDOW_S <= t <= sg["at"] + SKEW_S:
                    sg["event"] = eid
                    st["signs"][eid]["sig"] = h
                    del free[i]
                    break
        for t, eid in free:
            s = st["signs"][eid]
            if not s["reported"] and now - t > MATCH_WINDOW_S:
                s["reported"] = True
                self.find("D6", "SIGN_WITHOUT_SIGNED_JOB", event_id=eid, event_time=rfc3339(t), principal=s["principal"])
        for h, sg in st["sigs"].items():
            if sg["event"] is None and not sg["missing"] and now - sg["at"] > CT_LAG_S:
                sg["missing"] = True
                if sg["at"] - MATCH_WINDOW_S < st["coverage_start"]:
                    sg["before_coverage"] = True              # its Sign may precede the first trail file read
                    continue
                self.find("D6", "SIGNATURE_WITHOUT_SIGN_EVENT", signature_sha256=h, request_id=sg["request_id"],
                          logged_at=rfc3339(sg["at"]))

    # ------------------------------------------------------------------------------- 5: REQ# (D8, 0(a))
    def process_requests(self, st, reqs, now, stats):
        r = st["req"]
        floor = r["watermark"] - OVERLAP_S
        top = r["watermark"]
        docs = {}
        for pk, rec in reqs:
            if not isinstance(rec, dict) or rec.get("state") not in TERMINAL:
                continue
            rid = rec.get("rid") or pk[4:]
            docs[rid] = rec
            ended = rec.get("ended_at")
            if not isinstance(ended, (int, float)):
                continue
            if rid in r["seen"] or rid in st["pending"] or ended < floor:
                continue
            stats["terminal_new"] += 1
            st["pending"][rid] = {"ended_at": ended, "first_seen": now, "verify": None, "reported": []}
            top = max(top, ended)
        r["watermark"] = top
        for rid in sorted(st["pending"], key=lambda k: st["pending"][k]["ended_at"]):
            p = st["pending"][rid]
            rec = docs.get(rid)
            if rec is None:                                        # gone (expired) while pending: record what we know
                self.find("W", "TRACE_RECORD_LOST", rid=rid)
                self.done(st, rid, p)
                continue
            if rec["state"] == "COMPLETE" and p["verify"] is None:
                if self.remaining() < VERIFY_RESERVE_S * 1000:
                    continue                                       # stays pending; the next run continues
                p["verify"] = self.check_receipt(rec, p, now)
                if p["verify"] is None:
                    continue
                stats["verified"] += 1
            trace = self.trace_record(st, rec, p, now)
            if trace is None:
                continue                                           # a kms signature not yet reconciled
            self.trace.put(rid, trace)
            stats["traces"] += 1
            self.done(st, rid, p)
        r["seen"] = {k: v for k, v in r["seen"].items() if v >= r["watermark"] - OVERLAP_S}

    def done(self, st, rid, p):
        st["req"]["seen"][rid] = p["ended_at"]
        st["pending"].pop(rid, None)

    def check_receipt(self, rec, p, now):
        """-> the verification outcome dict, or None to retry next run."""
        rid, digest = rec["rid"], rec.get("receipt_sha256")
        out = {"receipt_sha256": digest, "checked_at": rfc3339(now)}
        if not isinstance(digest, str) or len(digest) != 64:
            self.find("D8", "COMPLETE_WITHOUT_RECEIPT_DIGEST", rid=rid)
            return dict(out, verdict="NO_RECEIPT", reason="NO_DIGEST")
        data = self.results.receipt(rid, digest)
        if data is None:
            self.find("D8", "RECEIPT_OBJECT_MISSING", rid=rid, receipt_sha256=digest)
            return dict(out, verdict="NO_RECEIPT", reason="OBJECT_MISSING")
        if sha256hex(data) != digest:
            self.find("D8", "RECEIPT_BYTES_DIGEST_MISMATCH", rid=rid, receipt_sha256=digest,
                      stored_sha256=sha256hex(data))
            return dict(out, verdict="DIGEST_MISMATCH", reason="STORED_BYTES")
        try:
            v = self.verify(data, self.cfg.window, self.cfg.catalog, rfc3339(now), list(self.cfg.explorers))
        except receipts.Unavailable as e:
            if e.code not in p["reported"]:
                p["reported"].append(e.code)
                self.find("W", "RECEIPT_CHECK_UNAVAILABLE", rid=rid, reason=e.code)
            if now - p["first_seen"] > D8_GIVE_UP_S:
                self.find("D8", "RECEIPT_UNCHECKED", rid=rid, receipt_sha256=digest, reason=e.code,
                          bound_s=D8_GIVE_UP_S)
                return dict(out, verdict="UNCHECKED", reason=e.code)
            return None
        if v["verdict"] != receipts.PASS:
            self.find("D8", "VERDICT_" + v["verdict"].replace("/", "_"), rid=rid, receipt_sha256=digest,
                      reason=v["reason"])
        return dict(out, verdict=v["verdict"], reason=v["reason"], anchor_heights=v["heights"], T=v.get("T"))

    # ------------------------------------------------------------------------------------- 0(a) trace record
    def trace_record(self, st, rec, p, now):
        """The accounting record (contract item 0(a)). Fields: digests, ids, states, codes. Never the request content,
        the plaintext request key, an API key value, a URL. -> dict, or None while a kms signature is unreconciled."""
        by_rid = {}
        for h, sg in st["sigs"].items():
            by_rid.setdefault(sg.get("request_id"), []).append((h, sg))
        attempts, waiting = [], False
        for a in rec.get("attempts") or []:
            jobs = {}
            for job, j in sorted((a.get("jobs") or {}).items()):
                entry = {"slot": j.get("slot"), "signer_request_id": j.get("request_id"),
                         "frame_sha256": j.get("frame_sha256"), "signature_sha256": j.get("sig_sha256")}
                if j.get("slot") == "kms":
                    signs = []
                    for h, sg in sorted(by_rid.get(j.get("request_id"), []), key=lambda x: x[1]["at"]):
                        if sg["event"] is None and not sg["missing"]:
                            waiting = True
                        signs.append({"signature_sha256": h, "cloudtrail_sign_event_id": sg["event"],
                                      "reconciled": "matched" if sg["event"] else
                                      ("before-coverage" if sg.get("before_coverage") else
                                       "unmatched" if sg["missing"] else "pending"),
                                      "dispositions": sg["dispositions"]})
                    entry["kms_signs"] = signs
                else:
                    entry["gcp_use_to_sign"] = "TODO: slot 2 reconciliation not built (G4)"
                jobs[job] = entry
            attempts.append({"id": a.get("id"), "state": a.get("state"),
                             "declared_issue_time": a.get("declared_issue_time"),
                             "end": {k: (a.get("end") or {}).get(k) for k in ("outcome", "reason")},
                             "jobs": jobs})
        if waiting and now - p["first_seen"] < CT_LAG_S + MATCH_WINDOW_S:
            return None
        client = self.by_digest.get(rec.get("cred"))
        v = p.get("verify") or {}
        key = rec.get("key")
        return {
            "format": "tessera-v1-trace/1",
            "written_at": rfc3339(now), "watcher_version": self.cfg.watcher_version,
            "credential_digest": rec.get("cred"),
            "api_key_id": client[1] if client else None, "client": client[0] if client else None,
            "rid": rec.get("rid"),
            "request_key_sha256": sha256hex(key.encode()) if isinstance(key, str) else None,
            "content_sha256": rec.get("content_sha256"), "content_len": rec.get("content_len"),
            "state": rec.get("state"), "reason": rec.get("reason"),
            "created_at": rfc3339(rec["created_at"]) if isinstance(rec.get("created_at"), (int, float)) else None,
            "ended_at": rfc3339(rec["ended_at"]),
            "attempts": attempts,
            "receipt_sha256": rec.get("receipt_sha256"),
            "anchor_heights": v.get("anchor_heights"), "T": v.get("T"),
            "verification": {k: v.get(k) for k in ("verdict", "reason", "checked_at")} if v else None,
            "slot2_reconciliation": "TODO: GCP useToSign not read (G4 open)",
        }

    # ------------------------------------------------------------------------------------------- pruning
    def prune(self, st, now):
        cut = now - RETAIN_S
        st["sigs"] = {h: s for h, s in st["sigs"].items() if s["at"] >= cut}
        st["signs"] = {e: s for e, s in st["signs"].items() if (s["t"] or now) >= cut}
        old = now - LOOKBACK_S - 3600
        st["ct_files"] = {k: t for k, t in st["ct_files"].items() if t is not None and t >= old}
