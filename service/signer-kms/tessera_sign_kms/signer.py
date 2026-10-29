"""The KMS-slot policy signer (docs/decisions/2026-10-27-v1-signer-placement.md): the only principal that may ask
AWS KMS for an ML-DSA-65 signature with the window's kms key. It reads the issuer's requests (service/issuer,
tessera_issue/signers.py SlotSigner wire protocol), applies the policy below, signs, verifies locally, and answers.

Request (untrusted): {"request_id", "frame_b64", "sign_by"} or, for a large frame (IS-09), {"request_id",
"frame_ref", "frame_sha256", "sign_by"}. Response: {"request_id", "status": "SIGNED" | "REFUSED", "sig_b64"?,
"reason"?, "detail"?, "frame_sha256"?, "signer": {...}}.

Policy, all before KMS is called (as the slot-2 signer, prototype/policy-signer/signer/main.py, and the issuer's
StandInSigner):
  - the request is exactly one of the two shapes; sign_by is required (IS-03);
  - IS-09: a referenced frame is fetched from frames/<rid>/<sha256> and refused unless its SHA-256 is frame_sha256;
  - the frame decodes, under the service verifier's own decoder, as tessera-v1/attest or tessera-v1/manifest;
  - its alg is the hybrid pair (the kms slot exists only there);
  - attest: signer.key_fp is this key's fingerprint; manifest: key_fp is this key's fingerprint;
  - attest: |declared_issue_time - clock| <= EPS (24 h, A9.2);
  - IS-03: the clock, read immediately before the KMS call, is not past sign_by nor the configured signing stop.
After signing: the signature must pass the verifier's rule-R codec and verify over the full frame; and the clock is
read again, so a signature KMS returned after the stop is withheld (SIGNING_STOPPED), logged, never sent.

Transient failures (KMS or S3 errors, a failed self-check) raise Retry while the message has been received fewer
than MAX_RECEIVES times, so SQS delivers it again; after that they are refused (SIGNING_ERROR). Every refusal is a
response, never a silent drop. Every signature and every refusal is one structured log line. EPS and the policy are
code; nothing in a request changes them."""
import base64
import datetime as dt
import hashlib
import json
import re

from tessera_verify.codec import (HYBRID_ALG, Fault, parse_signature, public_key, read_frame, registered_codecs,
                                  sig_policy, signature_verifies)

EPS = 24 * 3600                       # A9.2: refuse iff |declared - clock| > EPS
MAX_BODY = 1 << 20                    # an SQS message is at most 1 MiB
MAX_FRAME = 1 << 25                   # a referenced frame: read_frame's payload cap (2^24) plus generous slack
MAX_RECEIVES = 3                      # transient errors: retried by redelivery, then refused
SPKI_MLDSA65_PREFIX = bytes.fromhex("308207b2300b0609608648016503040312038207a100")
T_MANIFEST = b"tessera-v1/manifest"
RE_RID = re.compile(r"[A-Za-z0-9._:-]{1,128}")
RE_HEX64 = re.compile(r"[0-9a-f]{64}")
RE_REF = re.compile(r"frames/[0-9a-f]{64}/([0-9a-f]{64})")        # the issuer's frames/<rid>/<sha256> (IS-09)
REGISTRY = registered_codecs(HYBRID_ALG)
SHAPES = (frozenset({"request_id", "frame_b64", "sign_by"}),
          frozenset({"request_id", "frame_ref", "frame_sha256", "sign_by"}))


class Refuse(Exception):
    def __init__(self, reason, detail=""):
        super().__init__(reason)
        self.reason, self.detail = reason, detail


class Retry(Exception):
    """Leave the message on the queue: SQS delivers it again."""


class KeyMismatch(RuntimeError):
    """The KMS key is not the pinned key: the signer does not start."""


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def b64e(b):
    return base64.b64encode(bytes(b)).decode("ascii")


def b64d(s):
    raw = base64.b64decode(s, validate=True)
    if base64.b64encode(raw).decode("ascii") != s:
        raise ValueError("non-canonical base64")
    return raw


def ts(s):
    """'YYYY-MM-DDTHH:MM:SSZ' -> integer seconds (no leap seconds), exactly the issuer's util.ts grammar."""
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", s):
        raise ValueError("not an RFC 3339 UTC second: " + repr(s))
    y, m, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    if not (1 <= m <= 12 and 1 <= d <= 31 and int(s[11:13]) < 24 and int(s[14:16]) < 60 and int(s[17:19]) < 60):
        raise ValueError("not an RFC 3339 UTC second: " + repr(s))
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doe = yoe * 365 + yoe // 4 - yoe // 100 + (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    return (era * 146097 + doe - 719468) * 86400 + int(s[11:13]) * 3600 + int(s[14:16]) * 60 + int(s[17:19])


def rfc3339(t):
    return dt.datetime.fromtimestamp(int(t), dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fp_kms(spki):
    return "spki-sha256:" + sha256hex(spki)


def external_mu(pk_raw, message):
    """FIPS 204 external mu for pure ML-DSA with an empty context: what KMS signs under MessageType EXTERNAL_MU."""
    return hashlib.shake_256(hashlib.shake_256(pk_raw).digest(64) + b"\x00\x00" + message).digest(64)


class KmsSigner:
    """kms: a boto3-style KMS client; fetch(ref) -> bytes | None (None: no such object; raises on other errors);
    log(dict) writes one structured line; clock() -> int seconds."""
    slot = "kms"

    def __init__(self, kms, key_id, key_fp, sign_until, fetch, clock, log):
        if not re.fullmatch(r"spki-sha256:[0-9a-f]{64}", key_fp or ""):
            raise KeyMismatch("no pinned key fingerprint (KEY_FP) configured")
        self.kms, self.key_id, self.sign_until, self.fetch, self.clock, self.log = (
            kms, key_id, int(sign_until), fetch, clock, log)
        pk = kms.get_public_key(KeyId=key_id)
        if pk.get("KeySpec") != "ML_DSA_65" or "ML_DSA_SHAKE_256" not in pk.get("SigningAlgorithms", []):
            raise KeyMismatch(f"key {key_id} is {pk.get('KeySpec')}, not an ML-DSA-65 signing key")
        spki = bytes(pk["PublicKey"])
        try:
            self.pub = public_key(spki, "kms", HYBRID_ALG)           # the verifier's KEY_FORMAT gate
        except Fault as e:
            raise KeyMismatch(f"key {key_id}: {e.code}") from None
        if fp_kms(spki) != key_fp:
            raise KeyMismatch(f"KMS key fingerprint {fp_kms(spki)} is not the pinned {key_fp}; refusing to run")
        self.spki, self.fp, self.pk_raw = spki, key_fp, spki[len(SPKI_MLDSA65_PREFIX):]
        self.key_arn = pk.get("KeyId", key_id)

    # ------------------------------------------------------------------------------------------- policy
    def _request(self, body):
        if not isinstance(body, str) or len(body.encode()) > MAX_BODY:
            raise Refuse("BAD_REQUEST", "message missing or larger than 1 MiB")
        try:
            req = json.loads(body)
        except ValueError:
            raise Refuse("BAD_REQUEST", "not JSON") from None
        if not isinstance(req, dict):
            raise Refuse("BAD_REQUEST", "not a JSON object")
        return req

    def _frame(self, req):
        """-> (frame, sign_by). IS-09: a referenced frame is the object whose SHA-256 the issuer named."""
        if frozenset(req) not in SHAPES:
            raise Refuse("BAD_REQUEST", "fields " + ",".join(sorted(req)))
        try:
            sign_by = ts(req["sign_by"])
        except ValueError:
            raise Refuse("BAD_REQUEST", "sign_by") from None
        if "frame_b64" in req:
            try:
                return b64d(req["frame_b64"]), sign_by
            except (ValueError, TypeError):
                raise Refuse("BAD_REQUEST", "frame_b64 is not canonical base64") from None
        ref, want = req["frame_ref"], req["frame_sha256"]
        m = RE_REF.fullmatch(ref) if isinstance(ref, str) else None
        if m is None or not isinstance(want, str) or not RE_HEX64.fullmatch(want) or m.group(1) != want:
            raise Refuse("BAD_REQUEST", "frame_ref must be frames/<rid>/<frame_sha256>")
        try:
            frame = self.fetch(ref)
        except Exception as e:  # noqa: BLE001  S3 error other than "no such object": transient
            raise Retry(f"fetch {ref}: {type(e).__name__}: {e}") from None
        if frame is None:
            raise Refuse("FRAME_UNAVAILABLE", ref)
        if len(frame) > MAX_FRAME:
            raise Refuse("FRAME_TOO_LARGE", str(len(frame)))
        if sha256hex(frame) != want:
            raise Refuse("FRAME_DIGEST_MISMATCH", f"object {sha256hex(frame)}, named {want}")
        return frame, sign_by

    def check_frame(self, frame, now):
        """Frame grammar and content policy. -> "attest" | "manifest"."""
        kind = "manifest" if frame[:1 + len(T_MANIFEST)] == bytes([len(T_MANIFEST)]) + T_MANIFEST else "attest"
        try:
            obj = read_frame(frame, "tessera-v1/" + kind)
        except Fault as e:
            raise Refuse(e.code, kind) from None
        alg, fp = (obj["alg"], obj["key_fp"]) if kind == "manifest" else (obj["common"]["alg"], obj["signer"]["key_fp"])
        if alg != HYBRID_ALG:
            raise Refuse("ALG_NOT_ALLOWED", alg)
        if fp != self.fp:
            raise Refuse("KEY_FP_MISMATCH", fp)
        if kind == "attest":
            declared = ts(obj["common"]["declared_issue_time"])
            if abs(declared - now) > EPS:
                raise Refuse("DECLARED_TIME_OUTSIDE_EPSILON",
                             f"declared {rfc3339(declared)}, signer clock {rfc3339(now)}, epsilon {EPS} s")
        return kind

    def _stopped(self, now, sign_by):
        if now > self.sign_until:
            return f"clock {rfc3339(now)} past the signing stop {rfc3339(self.sign_until)}"
        if now > sign_by:
            return f"clock {rfc3339(now)} past sign_by {rfc3339(sign_by)}"
        return None

    # ------------------------------------------------------------------------------------------- signing
    def verify(self, frame, sig):
        """The issuer's check (signers.verify_slot_signature): rule-R codec, then ML-DSA-65 over the exact frame."""
        try:
            parsed = parse_signature(sig, HYBRID_ALG, "kms", REGISTRY)
            sig_policy(parsed)
            return signature_verifies(frame, parsed, self.pub)
        except Fault:
            return False

    def _kms_sign(self, frame):
        try:
            sig = self.kms.sign(KeyId=self.key_id, Message=external_mu(self.pk_raw, frame), MessageType="EXTERNAL_MU",
                                SigningAlgorithm="ML_DSA_SHAKE_256")["Signature"]
        except Exception as e:  # noqa: BLE001  KMS or network: transient
            raise Retry(f"kms sign: {type(e).__name__}: {e}") from None
        return bytes(sig)

    # ------------------------------------------------------------------------------------------- one message
    def _signer_info(self, now):
        return {"clock": rfc3339(now), "slot": self.slot, "key_fp": self.fp, "epsilon_s": EPS,
                "sign_until": rfc3339(self.sign_until)}

    def handle(self, body, receive_count=1, message_id=None):
        """-> the response dict to send, or raises Retry (the message is left for redelivery)."""
        rid, frame_sha, sig_sha, now = None, None, None, self.clock()
        line = {"event": None, "message_id": message_id, "receive_count": receive_count, "slot": self.slot,
                "key_fp": self.fp}
        try:
            try:
                req = self._request(body)
                rid = req.get("request_id")
                if not isinstance(rid, str) or not RE_RID.fullmatch(rid):
                    rid = None
                    raise Refuse("BAD_REQUEST", "request_id")
                frame, sign_by = self._frame(req)
                frame_sha = sha256hex(frame)
                kind = self.check_frame(frame, self.clock())
                now = self.clock()                    # IS-03: immediately before the signing operation
                stopped = self._stopped(now, sign_by)
                if stopped:
                    raise Refuse("SIGNING_STOPPED", stopped)
                sig = self._kms_sign(frame)
                sig_sha = sha256hex(sig)
                if not self.verify(frame, sig):
                    raise Retry(f"KMS signature {sig_sha} does not verify over the full frame")
                now = self.clock()
                stopped = self._stopped(now, sign_by)
                if stopped:                           # signed, but returned after the stop: withheld
                    raise Refuse("SIGNING_STOPPED", "signature withheld: " + stopped)
            except Retry as e:
                if receive_count < MAX_RECEIVES:
                    self.log(dict(line, event="retry", request_id=rid, frame_sha256=frame_sha,
                                  signature_sha256=sig_sha, detail=str(e)))
                    raise
                raise Refuse("SIGNING_ERROR", f"after {receive_count} receives: {e}") from None
            except Refuse:
                raise
            except Exception as e:  # noqa: BLE001  a bug must not drop the request silently or loop forever
                if receive_count < MAX_RECEIVES:
                    self.log(dict(line, event="retry", request_id=rid, frame_sha256=frame_sha,
                                  signature_sha256=sig_sha, detail=f"{type(e).__name__}: {e}"))
                    raise Retry(str(e)) from None
                raise Refuse("INTERNAL_ERROR", f"{type(e).__name__}: {e}") from None
        except Refuse as r:
            resp = {"request_id": rid, "status": "REFUSED", "reason": r.reason, "detail": r.detail,
                    "signer": self._signer_info(now)}
            if frame_sha:
                resp["frame_sha256"] = frame_sha
            self.log(dict(line, event="refused", request_id=rid, frame_sha256=frame_sha, signature_sha256=sig_sha,
                          reason=r.reason, detail=r.detail, clock=rfc3339(now)))
            return resp
        self.log(dict(line, event="signed", request_id=rid, frame_sha256=frame_sha, signature_sha256=sig_sha,
                      kind=kind, clock=rfc3339(now)))
        return {"request_id": rid, "status": "SIGNED", "sig_b64": b64e(sig), "frame_sha256": frame_sha,
                "signer": self._signer_info(now)}
