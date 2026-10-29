"""The three client operations as plain functions (wrapped for Lambda in lambda_app.py).

  POST /v1/requests                 submit(iss, credential, request_key, body)
  GET  /v1/requests/{key}           status(iss, credential, key)
  GET  /v1/requests/{key}/receipt   receipt(iss, credential, key)   -> 303 + pre-signed URL

Requests are scoped to the submitting credential: the record id is SHA-256(credential digest, request key), so
another credential's lookup of the same key finds nothing (404). Behaviour: docs/V1-SERVICE-RESOLUTIONS.md."""
import re
from dataclasses import dataclass, field

from .service import DEADLINE_S, RETENTION_S, WRITE_LEASE_S
from .util import MIB, dumps, rfc3339, sha256hex

UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")
RECEIPT_URL_TTL_S = 300               # the longest a minted receipt URL may live (IS-06)
REFUSAL_STATUS = {"TOO_LARGE": 413, "BAD_REQUEST": 400, "OUTSIDE_WINDOW": 403, "CLOSING": 403,
                  "SIGNING_UNAVAILABLE": 403}


@dataclass
class Response:
    status: int
    body: object                       # dict (JSON) or bytes (a receipt)
    headers: dict = field(default_factory=dict)

    def json(self):
        return self.body if isinstance(self.body, dict) else None


def cred_digest(credential):
    return sha256hex(("tessera-v1-credential\n" + credential).encode())


def record_id(credential, key):
    return sha256hex(f"{cred_digest(credential)}\n{key}".encode())


def content_name(digest):
    return "content-" + digest


def _expired(rec, now):
    return rec["ended_at"] is not None and now >= rec["ended_at"] + RETENTION_S


def confirmed(rec):
    """CF-01: a COMPLETE record counts only once it is known to have been committed before the deadline."""
    return rec["state"] != "COMPLETE" or rec.get("confirmed_at") is not None


def settle(iss, rec, attempts=5):
    """CF-01: decide an unconfirmed COMPLETE, in place. The clock is read after the record was read, so the COMPLETE
    commit happened no later than that reading. The confirmation is itself a write, and status reports COMPLETE only
    once it is durable (S4: the end is the status becoming COMPLETE), so it must also commit before the deadline.
    A clock check cannot bound when a write commits; the writer lease can (CF2-01): every write runs inside one
    Lambda invocation, so it commits within WRITE_LEASE_S of the decision. Hence: decided at least WRITE_LEASE_S
    before the deadline, it is confirmed (ended_at = that reading, never earlier than the commit); inside the last
    lease it is left unconfirmed (it reads as ACCEPTED, with its fail_after); at or after the deadline it is FAILED
    (NOT_COMPLETE_WITHIN_24H). Both writes are compare-and-set, so a confirmation and a failure never both win.
    -> rec."""
    for _ in range(attempts):
        if rec is None or confirmed(rec):
            return rec
        now = iss.clock()
        deadline = rec["created_at"] + DEADLINE_S
        if deadline - WRITE_LEASE_S <= now < deadline:
            return rec                                   # CF2-01: too late to confirm, too early to fail
        if now < deadline:
            rec.update(confirmed_at=now, ended_at=now, expires_at=now + RETENTION_S)
            rec["events"] = rec["events"][-40:] + [[now, "confirmed"]]
        else:
            rec.update(state="FAILED", reason="NOT_COMPLETE_WITHIN_24H", ended_at=now, expires_at=now + RETENTION_S,
                       receipt_sha256=None)
            rec["events"] = rec["events"][-40:] + [[now, "FAILED", "NOT_COMPLETE_WITHIN_24H", "unconfirmed"]]
        if iss.requests.save(rec):
            return rec
        cur = iss.requests.get(rec["rid"])               # someone else settled (or changed) it: decide again
        rec.clear()
        if cur is not None:
            rec.update(cur)
        else:
            return None
    raise RuntimeError("completion could not be settled; retried later")


def view(rec, now):
    if not confirmed(rec):                               # CF-01: not COMPLETE until confirmed
        rec = dict(rec, state="ACCEPTED", ended_at=None, reason=None, receipt_sha256=None)
    if _expired(rec, now):
        return {"request_key": rec["key"], "state": "EXPIRED"}
    v = {"request_key": rec["key"], "state": rec["state"], "accepted_at": rfc3339(rec["created_at"])}
    if rec["state"] == "ACCEPTED":
        v["fail_after"] = rfc3339(rec["created_at"] + DEADLINE_S)
    if rec["reason"]:
        v["reason"] = rec["reason"]
    if rec["ended_at"] is not None:
        v["ended_at"] = rfc3339(rec["ended_at"])
        v["available_until"] = rfc3339(rec["ended_at"] + RETENTION_S)
    if rec.get("receipt_sha256"):
        v["receipt_sha256"] = rec["receipt_sha256"]
    return v


def _original_status(rec):
    return REFUSAL_STATUS.get(rec["reason"], 403) if rec["state"] == "REFUSED" else 202


def _new_record(rid, credential, key, digest, length, now):
    return {"rid": rid, "cred": cred_digest(credential), "key": key, "state": None, "reason": None, "stage": None,
            "content_sha256": digest, "content_len": length, "created_at": now, "ended_at": None,
            "expires_at": None, "jobs": {}, "proofs": {}, "receipt_sha256": None, "events": []}


def _existing(iss, rec, digest, body=None):
    if iss.requests.tombstone_get(rec["rid"]) is None:              # IS-04: repair a missing tombstone
        iss.requests.tombstone_put(rec["rid"], iss.tombstone_until)
    if rec["content_sha256"] != digest:
        return Response(409, {"error": "KEY_CONTENT_MISMATCH", "request_key": rec["key"]})
    now = iss.clock()                                          # CF3-03: after the reads and the tombstone repair
    if _expired(rec, now):
        return Response(410, view(rec, now))
    if rec["state"] == "ACCEPTED" and rec["stage"] == "upload" and body is not None:
        rec = _finish_upload(iss, rec, body) or rec           # IS-05: a retry completes an interrupted upload
        now = iss.clock()
    return Response(_original_status(rec), view(rec, now))


def _finish_upload(iss, rec, body):
    """IS-05: content is stored only by a request that already owns its record (stage "upload"). -> record."""
    iss.results.put("content", rec["rid"], content_name(rec["content_sha256"]), body)
    rec["stage"] = "frames"
    if iss.requests.save(rec):
        return rec
    cur = iss.requests.get(rec["rid"])                         # moved on concurrently (another retry, the poller)
    if cur is not None and cur["state"] != "ACCEPTED":
        iss.results.delete("content", rec["rid"])              # ended meanwhile: nothing may keep the content
    return cur


def submit(iss, credential, request_key, body):
    if not credential:
        return Response(401, {"error": "UNAUTHENTICATED"})
    if not isinstance(request_key, str) or not UUID_RE.match(request_key):
        return Response(400, {"state": "REFUSED", "reason": "BAD_REQUEST",
                              "detail": "header Tessera-Request-Key must be a UUID"})
    key = request_key.lower()
    rid = record_id(credential, key)
    digest = sha256hex(body)
    rec = iss.requests.get(rid)
    if rec is not None:
        return _existing(iss, rec, digest, body)
    if iss.requests.tombstone_get(rid) is not None:          # the record is gone; the key is never reused
        rec = iss.requests.get(rid)                          # (or it was created concurrently: answer as a repeat)
        if rec is not None:
            return _existing(iss, rec, digest, body)
        return Response(410, {"request_key": key, "state": "EXPIRED"})
    now = iss.clock()                                        # CF3-02: after the reads (the create is the tolerance)
    reason = None
    if len(body) > MIB:
        reason = "TOO_LARGE"
    elif iss.closing:
        reason = "CLOSING"
    elif not iss.window.nb <= now <= iss.window.accept_until:
        reason = "OUTSIDE_WINDOW"
    elif not iss.signing_available:
        reason = "SIGNING_UNAVAILABLE"
    rec = _new_record(rid, credential, key, digest, len(body), now)
    if reason:                                               # S3: final; S6: refused content is not stored
        rec.update(state="REFUSED", reason=reason, ended_at=now, expires_at=now + RETENTION_S)
    else:
        rec.update(state="ACCEPTED", stage="upload")         # IS-05: own the key before storing any content
    rec["events"].append([now, "submitted", rec["state"], reason])
    if not iss.requests.create(rec, iss.tombstone_until):    # IS-04: record and tombstone in one atomic write
        return _existing(iss, iss.requests.get(rid), digest, body)        # lost a race with the same key
    if rec["state"] == "ACCEPTED":
        rec = _finish_upload(iss, rec, body) or rec
    return Response(_original_status(rec), view(rec, now))


def status(iss, credential, key):
    if not credential:
        return Response(401, {"error": "UNAUTHENTICATED"})
    if not isinstance(key, str) or not UUID_RE.match(key):
        return Response(400, {"error": "BAD_REQUEST"})
    rid = record_id(credential, key.lower())
    rec = iss.requests.get(rid)
    now = iss.clock()                                    # CF2-02: read after the record, as receipt() does
    if rec is None:
        if iss.requests.tombstone_get(rid) is not None:
            return Response(200, {"request_key": key.lower(), "state": "EXPIRED"})
        return Response(404, {"error": "NOT_FOUND"})
    if not confirmed(rec):
        settle(iss, rec)                                 # CF-01
        now = iss.clock()
    return Response(200, view(rec, now))


def receipt(iss, credential, key):
    """IS-06 (owner decision): one plain GET. After the credential check (the record id is scoped to the credential)
    and only for a COMPLETE, unexpired request, mint a fresh pre-signed URL valid for RECEIPT_URL_TTL_S and answer 303.
    Nothing is minted otherwise; minted URLs are never stored or reused."""
    r = status(iss, credential, key)
    if r.status != 200:
        return r
    v = r.body
    if v["state"] == "EXPIRED":
        return Response(410, v)
    if v["state"] != "COMPLETE":
        return Response(409, v)
    rid = record_id(credential, key.lower())
    if iss.results.size("result", rid, "receipt.json") is None:
        return Response(410, {"request_key": v["request_key"], "state": "EXPIRED"})
    rec = iss.requests.get(rid)
    now = iss.clock()                                    # CF-03, CF2-02: after every read, just before minting
    if rec is None or _expired(rec, now):
        return Response(410, {"request_key": v["request_key"], "state": "EXPIRED"})
    url = iss.results.presign("result", rid, "receipt.json", RECEIPT_URL_TTL_S, now)
    return Response(303, {}, {"Location": url, "Tessera-Receipt-SHA256": v["receipt_sha256"],
                              "Cache-Control": "no-store"})


def encode(resp):
    """-> (status, headers, body bytes)."""
    if isinstance(resp.body, (bytes, bytearray)):
        return resp.status, resp.headers, bytes(resp.body)
    return resp.status, {"Content-Type": "application/json", **resp.headers}, dumps(resp.body).encode()
