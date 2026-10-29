"""The stage pipeline and the scheduled poller (DESIGN.md "Pipeline"). Each poll first drains every signer response
queue (E-02), then advances each ACCEPTED request by at most one stage, then works off cleanup obligations:

  upload    the API owns the record before it stores the content (IS-05); an upload never finished within
            UPLOAD_GRACE_S is FAILED (CONTENT_UNAVAILABLE)
  frames    fix the manifest and common metadata (declared_issue_time = now), build both frames, enqueue the four
            signing jobs (attestation and possession, both slots) with request ids derived from (request, frame)
  signing   wait for all four; re-send unanswered jobs with the same id; then verify each on its exact bytes,
            freeze them, build A_sig and check it with the verifier's decoders           (profile 4 steps 2-6)
  stamp     after the git assertion's proof has k = 6 (tip >= h_git + 5): one stamp of SHA-256(A_sig); capture,
            validate (verifier DNSSEC code, now) and stamp the DNSSEC snapshot envelope
  confirm   upgrade both proofs until each has k = 6 at the tip
  headers   fetch headers h..h+5 for the lowest attestation of each of the three proofs
  assemble  build the canonical container and run the pre-ship checks (verifier library); VALID_STRICT ships,
            a snapshot-rule failure re-captures the snapshot, anything else is FAILED

Ending rules: 24 h after acceptance without COMPLETE -> FAILED; frames or signing after the signing stop (96 h
before not-after) -> FAILED. A request is never shipped late or incomplete: the deadline is checked again, on a fresh
clock, in the terminal transition itself (IS-02), and every policy signer refuses after the signing stop (IS-03).

Cleanup (IS-07): ending a request first records a cleanup obligation, then commits the state, then deletes. Each poll
retries outstanding obligations: content, work files and frames once the request has ended; the receipt (and
anything left) 30 days after the end. An obligation is dropped only when the listing shows nothing left, and not
before the late writers' lease (WRITE_LEASE_S, CF-02) has run out.

Completion (CF-01, CF2-01): COMPLETE is committed unconfirmed and then settled (api.settle). It is confirmed when a
clock reading taken after the commit is at least the writer lease before the deadline, left unconfirmed inside the
last lease, and FAILED at or after the deadline."""
import json

from tessera_verify.anchors import parse_ots, select
from tessera_verify.codec import Fault, read_anchor, read_frame, registered_codecs
from tessera_verify.dnssec import parse_snapshot, txt_value, validate_snapshot

from . import ots
from .api import confirmed, content_name, settle
from .chain import pin_of
from .encode import common_metadata, encode_anchor, encode_attest, encode_manifest, encode_snapshot_envelope
from .preship import PreShipUnavailable, check_config
from .service import DEADLINE_S, RETENTION_S, WRITE_LEASE_S
from .signers import request_id
from .util import ALG, POLICY_VERSION, b64d, b64e, jcs, rfc3339, sha256, sha256hex, PROFILE

JOBS = (("s_kms", "kms", "f_kms"), ("p_kms", "kms", "manifest"), ("s_gpg", "gpg", "f_gpg"), ("p_gpg", "gpg", "manifest"))
UPLOAD_GRACE_S = 15 * 60          # IS-05: an API call lasts at most 29 s; an upload not finished by then was abandoned
MERGE_ATTEMPTS = 5                # IS-08: compare-and-set retries when recording a verified signature
SNAPSHOT_REASONS = {"SNAPSHOT_TIME", "SNAPSHOT_NOT_ANCHORED", "SNAPSHOT_STAMP_MISMATCH", "DNS_WILDCARD",
                    "RRSIG_NOT_VALID_AT_EVAL_TIME", "DNS_EVIDENCE_MISSING", "TRUST_HORIZON"}


class StageError(Exception):
    pass


# ------------------------------------------------------------------------------------------------ the poller
def poll(iss):
    """One scheduled tick. -> summary dict."""
    out = {"drained": drain(iss), "advanced": {}, "cleaned": 0}
    for rec in iss.requests.active():
        before = rec["stage"]
        try:
            advance(iss, rec)
        except PreShipUnavailable as e:
            iss.note("pre-ship unavailable, request kept:", rec["rid"][:12], e)
        except Exception as e:  # noqa: BLE001  one request's fault never stops the others; retried next tick
            iss.note("stage", before, "error, request kept:", rec["rid"][:12], type(e).__name__, e)
        out["advanced"][rec["rid"]] = (before, rec["stage"] or rec["state"])
    out["cleaned"] = cleanup(iss)
    return out


def _save(iss, rec):
    if not iss.requests.save(rec):
        raise StageError("record changed concurrently; retried next tick")


def _event(rec, now, *what):
    rec["events"] = (rec.get("events") or [])[-40:] + [[now, *what]]


def _end(iss, rec, state, reason, now):
    iss.requests.cleanup_put(rec["rid"], {"rid": rec["rid"], "end_done": False})   # IS-07: before the commit
    now = max(now, iss.clock())                        # CF-01: read after the obligation is durable (IS-02)
    if state == "COMPLETE" and now >= rec["created_at"] + DEADLINE_S:
        state, reason = "FAILED", "NOT_COMPLETE_WITHIN_24H"
    rec.update(state=state, reason=reason, stage=None, ended_at=now, expires_at=now + RETENTION_S)
    _event(rec, now, state, reason)
    _save(iss, rec)
    if state == "COMPLETE":
        settle(iss, rec)                               # CF-01: confirmed only if the commit preceded the deadline
    try:
        _cleanup_one(iss, rec["rid"], {"rid": rec["rid"], "end_done": False}, now)
    except Exception as e:  # noqa: BLE001  the obligation stays; the next poll retries it
        iss.note("cleanup deferred:", rec["rid"][:12], type(e).__name__, e)


# ------------------------------------------------------------------------------------------------ cleanup (IS-07)
END_NS = ("content", "work", "frames")


def _cleanup_one(iss, rid, doc, now=None):
    """-> True when the obligation is discharged. Content, work files and frames go when the request has ended;
    the receipt goes 30 days after the end (or at once if the request did not complete).

    CF-02: a writer that read the request while it was ACCEPTED (an upload retry, a response consumer, a stale
    poller) may still store an object after the end. Each such writer runs inside one Lambda invocation, so it is
    gone WRITE_LEASE_S after the end was first seen here. Until then the obligation is kept and every poll deletes
    again; only a listing taken after the lease discharges it."""
    rec = iss.requests.get(rid)
    if rec is not None and not confirmed(rec):
        settle(iss, rec)                               # CF-01: an unconfirmed COMPLETE left by an interrupted end
    if rec is not None and (rec["state"] == "ACCEPTED" or not confirmed(rec)):
        return False                                   # not ended (an obligation written before a lost commit), or
                                                       # CF2-01: COMPLETE inside the last lease, settled at the deadline
    seen = iss.clock()                                 # read after the record: no earlier than the end's commit
    expired = rec is None or seen >= rec["ended_at"] + RETENTION_S
    namespaces = END_NS + ("result",) if (expired or rec["state"] != "COMPLETE") else END_NS
    if doc.get("end_done") and not expired:
        return False
    if doc.get("fence_until") is None:                 # CF-02: start the writers' lease, durably
        doc = dict(doc, rid=rid, fence_until=seen + WRITE_LEASE_S)
        iss.requests.cleanup_put(rid, doc)
    for ns in namespaces:
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
        except Exception as e:  # noqa: BLE001
            iss.note("cleanup", rid[:12], "error, kept:", type(e).__name__, e)
    return n


def advance(iss, rec):
    now = iss.clock()
    if now >= rec["created_at"] + DEADLINE_S:
        return _end(iss, rec, "FAILED", "NOT_COMPLETE_WITHIN_24H", now)
    try:
        STAGES[rec["stage"]](iss, rec, now)
    except StageError as e:
        iss.note("stage", rec["stage"], "deferred:", e)


# ------------------------------------------------------------------------------------------------ E-02 drain
def drain(iss, max_batches=50):
    """Read every slot's response queue. Every response is logged (request id, slot, status, frame hash when the
    id is known, signature hash) whether or not it is used, and then deleted from the queue."""
    n = 0
    for slot, signer in iss.signers.items():
        for _ in range(max_batches):
            batch = signer.receive(10)
            if not batch:
                break
            for handle, body in batch:
                try:
                    _take(iss, slot, signer, body)
                except Exception as e:  # noqa: BLE001  not acknowledged: the queue delivers it again
                    iss.note("response", slot, "not taken:", type(e).__name__, e)
                    continue
                signer.ack(handle)
                n += 1
    return n


def _take(iss, slot, signer, body):
    now = iss.clock()
    srid = body.get("request_id")
    idx = iss.requests.sigreq_get(srid) if isinstance(srid, str) else None
    sig = None
    if body.get("status") == "SIGNED":
        try:
            sig = b64d(body.get("sig_b64", ""))
        except (ValueError, TypeError):
            sig = None
    entry = {"at": rfc3339(now), "slot": slot, "request_id": srid, "status": body.get("status"),
             "reason": body.get("reason"), "frame_sha256": idx["frame_sha256"] if idx else None,
             "signature_sha256": sha256hex(sig) if sig is not None else None, "disposition": None}
    if idx is None or idx.get("slot") != slot:
        entry["disposition"] = "unrequested"
    else:
        rec = iss.requests.get(idx["rid"])
        job = rec["jobs"].get(idx["job"]) if rec else None
        if rec is None or rec["state"] != "ACCEPTED" or rec["stage"] != "signing" or job is None:
            entry["disposition"] = "not-waiting"
        elif job.get("sig_sha256"):
            entry["disposition"] = "duplicate"
        elif body.get("status") == "REFUSED":
            entry["disposition"] = "refused"
            iss.requests.siglog_add(entry)
            return _end(iss, rec, "FAILED", "SIGNER_REFUSED:" + str(body.get("reason")), now)
        elif sig is None:
            entry["disposition"] = "malformed"
        else:
            frame = iss.results.get("work", rec["rid"], job["frame"])
            if frame is None or sha256hex(frame) != job["frame_sha256"] or not signer.verify(frame, sig):
                entry["disposition"] = "bad-signature"
            else:
                entry["disposition"] = "used"
                iss.requests.siglog_add(entry)         # IS-01: durable in the log before it can be used
                iss.results.put("work", rec["rid"], sig_name(idx["job"], entry["signature_sha256"]), sig)
                outcome = _record_signature(iss, idx["rid"], idx["job"], entry["signature_sha256"], srid, now)
                if outcome != "used":                  # IS-08: say what became of it
                    iss.requests.siglog_add(dict(entry, disposition="superseded:" + outcome))
                return
    iss.requests.siglog_add(entry)


def sig_name(job, sig_sha256):
    """Each verified signature has its own object, so concurrent consumers never overwrite one another (IS-08)."""
    return f"sig-{job}-{sig_sha256}"


def _record_signature(iss, rid, job, sig_sha256, srid, now):
    """IS-08: merge one verified signature into the record, re-reading on a compare-and-set conflict."""
    for _ in range(MERGE_ATTEMPTS):
        rec = iss.requests.get(rid)
        if rec is None or rec["state"] != "ACCEPTED" or rec["stage"] != "signing" or job not in rec["jobs"]:
            return "not-waiting"
        if rec["jobs"][job]["sig_sha256"]:
            return "duplicate"
        rec["jobs"][job]["sig_sha256"] = sig_sha256
        _event(rec, now, "signed", job, srid)
        if iss.requests.save(rec):
            return "used"
    return "save-conflict"                             # left in storage and the log; reconciled before any resend


def _reconcile(iss, rec):
    """IS-08: adopt a stored signature that verifies on the job's frame and has its "used" log record, instead of
    asking the signer again. -> True if a job was satisfied."""
    names, found = iss.results.names("work", rec["rid"]), False
    for job, j in rec["jobs"].items():
        if j["sig_sha256"]:
            continue
        frame = iss.results.get("work", rec["rid"], j["frame"])
        for name in names:
            if not name.startswith(f"sig-{job}-"):
                continue
            sig = iss.results.get("work", rec["rid"], name)
            h = sha256hex(sig) if sig is not None else None
            if (h and name == sig_name(job, h) and iss.requests.siglog_has(j["request_id"], h)
                    and iss.signers[j["slot"]].verify(frame, sig)):
                j["sig_sha256"], found = h, True
                break
    return found


def _sign_by(iss, rec):
    """IS-03: the latest moment a signer may sign for this request."""
    return min(iss.window.sign_until, rec["created_at"] + DEADLINE_S)


def _send(iss, rec, job):
    j = rec["jobs"][job]
    frame = iss.results.get("work", rec["rid"], j["frame"])

    def stash(data):                                   # IS-09: immutable, digest-named, deleted with the request
        iss.results.put("frames", rec["rid"], sha256hex(data), data)
        return iss.results.ref("frames", rec["rid"], sha256hex(data))
    iss.signers[j["slot"]].send(j["request_id"], frame, sign_by=_sign_by(iss, rec), stash=stash)


# ------------------------------------------------------------------------------------------------ stages
def st_upload(iss, rec, now):
    """IS-05: the API created the record before storing the content. Proceed once the content is there; an upload
    abandoned past the grace period fails the request."""
    content = iss.results.get("content", rec["rid"], content_name(rec["content_sha256"]))
    if content is not None and sha256hex(content) == rec["content_sha256"]:
        rec["stage"] = "frames"
        return _save(iss, rec)
    if now - rec["created_at"] >= UPLOAD_GRACE_S:
        return _end(iss, rec, "FAILED", "CONTENT_UNAVAILABLE", now)


def st_frames(iss, rec, now):
    w = iss.window
    if now > w.sign_until:
        return _end(iss, rec, "FAILED", "SIGNING_STOPPED", now)
    content = iss.results.get("content", rec["rid"], content_name(rec["content_sha256"]))
    if content is None or sha256hex(content) != rec["content_sha256"]:
        return _end(iss, rec, "FAILED", "CONTENT_UNAVAILABLE", now)
    declared = rfc3339(now)
    manifest = encode_manifest(w.kms_fp, w.gpg_fp)
    common = common_metadata(b64e(content), declared, manifest, iss.frozen.catalog)
    frames = {"manifest": manifest, "f_kms": encode_attest(common, w.kms_fp), "f_gpg": encode_attest(common, w.gpg_fp)}
    for name, data in frames.items():
        iss.results.put("work", rec["rid"], name, data)
    jobs = {}
    for job, slot, fname in JOBS:
        srid = request_id(rec["rid"], slot, frames[fname])
        jobs[job] = {"slot": slot, "frame": fname, "frame_sha256": sha256hex(frames[fname]), "request_id": srid,
                     "sent_at": now, "attempts": 1, "sig_sha256": None}
        iss.requests.sigreq_put(srid, {"rid": rec["rid"], "job": job, "slot": slot,
                                       "frame_sha256": jobs[job]["frame_sha256"]}, now + RETENTION_S)
    rec.update(stage="signing", jobs=jobs, declared_issue_time=declared)
    _event(rec, now, "frames", declared)
    _save(iss, rec)                                  # durable before anything is sent
    for job, _, _ in JOBS:
        _send(iss, rec, job)
    for slot in iss.signers:
        iss.signers[slot].wake()                     # E-01: started on demand, once per batch


def st_signing(iss, rec, now):
    jobs = rec["jobs"]
    if all(j["sig_sha256"] for j in jobs.values()):
        return _seal(iss, rec, now)
    if now > iss.window.sign_until:
        return _end(iss, rec, "FAILED", "SIGNING_STOPPED", now)
    if _reconcile(iss, rec):                         # IS-08: verified and logged, but its record update was lost
        _event(rec, now, "reconciled")
        return _save(iss, rec)
    resend = [(k, j) for k, j in jobs.items() if not j["sig_sha256"] and now - j["sent_at"] >= iss.signer_retry_s]
    if not resend:
        return
    for k, j in resend:
        j.update(sent_at=now, attempts=j["attempts"] + 1)
    _event(rec, now, "resend", [k for k, _ in resend])
    _save(iss, rec)
    slots = set()
    for k, j in resend:                               # E-02: the same request id; a late first answer still counts
        _send(iss, rec, k)
        slots.add(j["slot"])
    for s in slots:
        iss.signers[s].wake()


def _seal(iss, rec, now):
    """Profile 4 steps 4-6: verify each signature on the exact bytes, freeze, build A_sig, check it."""
    rid, get = rec["rid"], (lambda n: iss.results.get("work", rec["rid"], n))
    sigs = {}
    for job, j in rec["jobs"].items():
        s, f = get(sig_name(job, j["sig_sha256"])), get(j["frame"])
        if (s is None or sha256hex(s) != j["sig_sha256"] or not iss.signers[j["slot"]].verify(f, s)
                or not iss.requests.siglog_has(j["request_id"], j["sig_sha256"])):     # IS-01
            j["sig_sha256"] = None                     # lost or corrupt: ask again with the same id
            j["sent_at"] = 0
            _save(iss, rec)
            return
        sigs[job] = s
    a_sig = encode_anchor(get("f_kms"), sigs["s_kms"], get("f_gpg"), sigs["s_gpg"])
    try:
        for (f, obj, s, _), slot in zip(read_anchor(a_sig, registered_codecs(ALG)), ("kms", "gpg")):
            if not iss.signers[slot].verify(f, s) or obj["common"]["manifest_sha256"] != sha256hex(get("manifest")):
                raise StageError("A_sig check")
        read_frame(get("manifest"), "tessera-v1/manifest")
    except Fault as e:
        raise StageError("A_sig decode: " + e.code) from None
    iss.results.put("work", rid, "a_sig", a_sig)
    rec.update(stage="stamp", receipt_id=sha256hex(a_sig))
    _event(rec, now, "a_sig", rec["receipt_id"])
    _save(iss, rec)


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


def st_stamp(iss, rec, now):
    tip = iss.headers.tip()
    if tip < iss.window.h_git + 5:                     # chain-order pre-commitment (profile 4, 6.3)
        return
    proofs = rec["proofs"]
    if "receipt" not in proofs:
        raw = ots.stamp(sha256(iss.results.get("work", rec["rid"], "a_sig")), iss.calendars, iss.nonce())
        iss.results.put("work", rec["rid"], "receipt.ots", raw)
        proofs["receipt"] = {"stamped_at": now, "tip": tip}
        _event(rec, now, "stamped", "receipt")
        _save(iss, rec)
    if "snapshot" not in proofs:
        body = iss.dns.capture(now)
        problem = _validate_snapshot_now(iss, body, now)
        if problem:
            _event(rec, now, "snapshot-rejected", problem)
            _save(iss, rec)
            return                                     # recapture next tick
        env = encode_snapshot_envelope(body)
        raw = ots.stamp(sha256(env), iss.calendars, iss.nonce())
        iss.results.put("work", rec["rid"], "snapshot.body", body)
        iss.results.put("work", rec["rid"], "snapshot.ots", raw)
        proofs["snapshot"] = {"stamped_at": now, "tip": tip}
        _event(rec, now, "stamped", "snapshot")
    rec["stage"] = "confirm"
    _save(iss, rec)


def st_confirm(iss, rec, now):
    tip = iss.headers.tip()
    ready = True
    for name in ("receipt", "snapshot"):
        raw = iss.results.get("work", rec["rid"], name + ".ots")
        new, changed = ots.upgrade(raw, iss.calendars)
        if changed:
            iss.results.put("work", rec["rid"], name + ".ots", new)
        ok, h = ots.k6_ready(new, tip)
        rec["proofs"][name]["h"] = h
        ready = ready and ok
    if ready:
        if not rec["proofs"]["receipt"]["h"] > iss.window.h_git + 5:
            return _end(iss, rec, "FAILED", "GIT_NOT_PRECOMMITTED", now)
        rec["stage"] = "headers"
        _event(rec, now, "confirmed", rec["proofs"]["receipt"]["h"], rec["proofs"]["snapshot"]["h"])
    _save(iss, rec)


def st_headers(iss, rec, now):
    heights = set()
    for raw in (iss.results.get("work", rec["rid"], "receipt.ots"), iss.results.get("work", rec["rid"], "snapshot.ots"),
                iss.window.git["ots"]):
        h = ots.lowest_btc_height(raw)
        heights.update(range(h, h + 6))
    hdrs = iss.headers.headers(sorted(heights))
    iss.results.put("work", rec["rid"], "headers.json", json.dumps({str(h): v.hex() for h, v in hdrs.items()}).encode())
    rec["stage"] = "assemble"
    _save(iss, rec)


def assemble(iss, rec, hdrs):
    """The canonical JCS container of profile 15.1."""
    get, w, fz = (lambda n: iss.results.get("work", rec["rid"], n)), iss.window, iss.frozen
    receipt_ots = get("receipt.ots")
    selected, _ = select(parse_ots(receipt_ots), hdrs, {h: pin_of(v) for h, v in hdrs.items()})
    if selected is None:
        raise StageError("receipt proof does not qualify under the fetched headers")
    txid = ots.txid_of(selected.paths[0])
    from .util import ts
    delay = max(0, selected.time - ts(rec["declared_issue_time"]))
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
        "possession": {"gpg": b64e(get(sig_name("p_gpg", rec["jobs"]["p_gpg"]["sig_sha256"]))),
                       "kms": b64e(get(sig_name("p_kms", rec["jobs"]["p_kms"]["sig_sha256"])))},
        "preamble": b64e(fz.preamble),
        "receipt_anchor": {"ots": b64e(receipt_ots), "txid": txid},
        "spec": b64e(fz.spec),
        "vectors": b64e(fz.vectors),
    }
    return jcs({"layers": [layer], "profile": PROFILE})


def st_assemble(iss, rec, now):
    hdrs = {int(h): bytes.fromhex(v) for h, v in json.loads(iss.results.get("work", rec["rid"], "headers.json")).items()}
    bundle = assemble(iss, rec, hdrs)
    stable, _ = iss.preship.check(bundle, hdrs, now)
    if stable["verdict"] == "VALID_STRICT" and stable["reason"] == "OK":
        if iss.clock() >= rec["created_at"] + DEADLINE_S:          # IS-02: re-checked after the pre-ship checks
            return _end(iss, rec, "FAILED", "NOT_COMPLETE_WITHIN_24H", now)
        iss.results.put("result", rec["rid"], "receipt.json", bundle)
        rec["receipt_sha256"] = sha256hex(bundle)
        rec["T"] = stable["T"]
        return _end(iss, rec, "COMPLETE", None, now)
    if stable["reason"] in SNAPSHOT_REASONS:            # profile 4: re-capture the snapshot before shipping
        rec["proofs"].pop("snapshot", None)
        rec["stage"] = "stamp"
        _event(rec, now, "preship-recapture", stable["reason"])
        return _save(iss, rec)
    return _end(iss, rec, "FAILED", "PRESHIP:" + stable["verdict"] + "/" + stable["reason"], now)


STAGES = {"upload": st_upload, "frames": st_frames, "signing": st_signing, "stamp": st_stamp, "confirm": st_confirm,
          "headers": st_headers, "assemble": st_assemble}
