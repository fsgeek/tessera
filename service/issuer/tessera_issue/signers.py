"""The two policy signers behind one interface (DESIGN.md "Signers"): the issuer enqueues a frame on the slot's
request queue and reads signed responses from the slot's response queue. The issuer holds no signing credential.

Wire protocol (the deployed slot-2 policy signer's): request {"request_id", "frame_b64"}; response {"request_id",
"status": "SIGNED" | "REFUSED", "sig_b64"?, "reason"?, "detail"?, "signer": {...}?}.
Additions after review (DESIGN.md "Changes after review"):
  IS-03  the request carries "sign_by" (RFC 3339): the signer refuses (SIGNING_STOPPED) when its clock is past it, or
         past its own configured signing stop, immediately before signing.
  IS-09  a frame whose inline message would exceed INLINE_MAX is sent as {"request_id", "frame_ref", "frame_sha256",
         "sign_by"}: the signer reads the object at frame_ref and refuses (FRAME_DIGEST_MISMATCH) unless its SHA-256 is
         frame_sha256, so it signs exactly the bytes the issuer named.

E-01: `wake()` starts a signer on demand (optional hook per slot, called once per enqueued batch).
E-02: request ids are derived from (request, frame hash), so a retry reuses the id and a late answer to the first
attempt satisfies it; the caller records every response with frame and signature hashes (pipeline.drain).

StandInSigner is the local signer process: it reads the same queues and signs with TEST keys."""
import json

from tessera_verify.codec import (Fault, parse_signature, public_key, registered_codecs, sig_policy,
                                  signature_verifies, read_frame)

from .encode import fp_gpg, fp_kms
from .util import ALG, EPS, b64d, b64e, rfc3339, sha256hex, ts

SLOTS = ("kms", "gpg")
INLINE_MAX = 256 * 1024          # bytes of one inline request message; SQS allows at most 1 MiB (IS-09)
REGISTRY = registered_codecs(ALG)


def request_id(request_id_scope, slot, frame):
    """E-02: one id per (request, slot, frame); a retry of the same frame for the same request reuses it. The slot is
    in the derivation because the manifest frame goes to both slots."""
    return "req-" + sha256hex(f"{request_id_scope}\n{slot}\n{sha256hex(frame)}".encode())[:40]


def verify_slot_signature(slot, key_bytes, frame, sig):
    """Rule R (kms) or rule O (gpg) codec and policy, then the signature over the exact frame bytes, with the
    service verifier's own functions."""
    try:
        parsed = parse_signature(sig, ALG, slot, REGISTRY)
        sig_policy(parsed)
        return signature_verifies(frame, parsed, public_key(key_bytes, slot, ALG))
    except Fault:
        return False


class SlotSigner:
    """Issuer side of one slot: its public key and its two queues."""

    def __init__(self, slot, key_bytes, requests, responses, wake=None):
        if slot not in SLOTS:
            raise ValueError(slot)
        public_key(key_bytes, slot, ALG)                 # KEY_FORMAT gate
        self.slot, self.key_bytes = slot, key_bytes
        self.fp = fp_kms(key_bytes) if slot == "kms" else fp_gpg(key_bytes)
        self.requests, self.responses, self._wake = requests, responses, wake

    def send(self, rid, frame, sign_by=None, stash=None):
        """stash(frame) -> object reference, used when the inline message would be too large (IS-09)."""
        msg = {"request_id": rid, "frame_b64": b64e(frame)}
        if sign_by is not None:
            msg["sign_by"] = rfc3339(sign_by)
        body = json.dumps(msg, sort_keys=True)
        if len(body.encode()) > INLINE_MAX:
            if stash is None:
                raise ValueError("frame too large for an inline signer request")
            del msg["frame_b64"]
            msg.update(frame_ref=stash(frame), frame_sha256=sha256hex(frame))
            body = json.dumps(msg, sort_keys=True)
        self.requests.send(body)

    def wake(self):
        if self._wake is not None:
            self._wake(self.slot)

    def receive(self, max_messages=10):
        out = []
        for m in self.responses.receive(max_messages):
            try:
                body = json.loads(m.body)
                if not isinstance(body, dict):
                    raise ValueError
            except ValueError:
                body = {"_unparseable": m.body[:200]}
            out.append((m.handle, body))
        return out

    def ack(self, handle):
        self.responses.delete(handle)

    def verify(self, frame, sig):
        return verify_slot_signature(self.slot, self.key_bytes, frame, sig)


class StandInSigner:
    """A local policy signer with a TEST key. Policy as the deployed slot-2 signer: tag must be attest or manifest;
    an attestation must name this slot's key; the gpg slot refuses a declared_issue_time more than epsilon from
    its clock (A9:401-405). `process()` handles what is queued now; tests call it (or not) to model a signer that
    is slow, down or late."""

    def __init__(self, slot, key, requests, responses, clock, sign_until=None, fetch=None):
        self.slot, self.key, self.requests, self.responses, self.clock = slot, key, requests, responses, clock
        self.sign_until = sign_until           # IS-03: the window's signing stop, configured at the signer
        self.fetch = fetch                     # IS-09: frame reference -> bytes or None
        self.key_bytes = key.spki if slot == "kms" else key.pgp_body
        self.fp = key.fp_kms if slot == "kms" else key.fp_gpg
        self.signed = []                       # (request_id, frame sha256, signature sha256)

    def _refuse(self, rid, reason, detail=""):
        return {"request_id": rid, "status": "REFUSED", "reason": reason, "detail": detail,
                "signer": {"clock": rfc3339(self.clock()), "slot": self.slot}}

    def handle(self, req):
        rid = req.get("request_id")
        try:
            if "frame_ref" in req:
                if self.fetch is None:
                    return self._refuse(rid, "FRAME_UNAVAILABLE")
                frame = self.fetch(req["frame_ref"])
                if frame is None:
                    return self._refuse(rid, "FRAME_UNAVAILABLE")
                if sha256hex(frame) != req["frame_sha256"]:
                    return self._refuse(rid, "FRAME_DIGEST_MISMATCH")
            else:
                frame = b64d(req["frame_b64"])
            sign_by = ts(req["sign_by"]) if "sign_by" in req else None
        except (KeyError, ValueError, TypeError):
            return self._refuse(rid, "BAD_REQUEST")
        try:
            obj = read_frame(frame, "tessera-v1/attest")
            if obj["signer"]["key_fp"] != self.fp:
                return self._refuse(rid, "KEY_FP_MISMATCH")
            if self.slot == "gpg" and abs(ts(obj["common"]["declared_issue_time"]) - self.clock()) > EPS:
                return self._refuse(rid, "DECLARED_TIME_OUTSIDE_EPSILON")
        except Fault:
            try:
                read_frame(frame, "tessera-v1/manifest")
            except Fault as e:
                return self._refuse(rid, e.code)
        now = self.clock()                     # IS-03: checked immediately before the signing operation
        if (self.sign_until is not None and now > self.sign_until) or (sign_by is not None and now > sign_by):
            return self._refuse(rid, "SIGNING_STOPPED")
        if self.slot == "kms":
            sig = self.key.sign(frame)
        else:
            from .testkeys import pgp_sign
            sig = pgp_sign(frame, self.key, self.clock())
        self.signed.append((rid, sha256hex(frame), sha256hex(sig)))
        return {"request_id": rid, "status": "SIGNED", "sig_b64": b64e(sig),
                "signer": {"clock": rfc3339(self.clock()), "slot": self.slot}}

    def process(self, limit=None):
        n = 0
        while limit is None or n < limit:
            msgs = self.requests.receive(1)
            if not msgs:
                break
            m = msgs[0]
            try:
                req = json.loads(m.body)
            except ValueError:
                req = {}
            self.responses.send(json.dumps(self.handle(req), sort_keys=True))
            self.requests.delete(m.handle)
            n += 1
        return n
