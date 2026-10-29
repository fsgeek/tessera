"""The slot-2 signing policy: request parsing and the checks a frame must pass before any signature is requested.
Pure functions over bytes, strings and integer clocks; nothing here signs, reads a queue or reads an object.

Request (the issuer's format, service/issuer/tessera_issue/signers.py SlotSigner.send; authoritative):
  inline:    {"request_id", "sign_by", "frame_b64"}
  reference: {"request_id", "sign_by", "frame_ref", "frame_sha256"}       (IS-09)
No other member is accepted. `sign_by` is required here (the issuer always sends it; a request without a deadline is
refused rather than signed at any later time).

Policy (A9.6; service/issuer/DESIGN.md IS-03, IS-09; V1-OPERATIONS-RUNBOOK §3), every check before signing:
  - the frame decodes under the service verifier's codec as tessera-v1/attest or tessera-v1/manifest, within schema;
  - its alg (attest: common.alg; manifest: alg) is the registered pair id ALG;
  - attest: signer.key_fp is this key's gpg-sha256 fingerprint; manifest: sset[0] is;
  - attest: |declared_issue_time - signer clock| <= EPS (24 h, A9.2);
  - immediately before the HSM call: the clock is not past the configured signing stop, nor past the request's sign_by.
EPS, ALG and the policy are code, not configuration. Nothing in a request can change them."""
import json
import re
from dataclasses import dataclass

from tessera_verify.codec import HEX, HYBRID_ALG, Fault, b64, read_frame, utc

ALG = HYBRID_ALG                     # KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256, the catalog's registered pair id
EPS = 24 * 3600                      # A9.2: refuse iff |declared - clock| > EPS
MAX_BODY = 1 << 20                   # one SQS message, bytes (the SQS maximum)
MAX_FRAME = 1 + 255 + 2 + 4 + (1 << 24)   # the largest frame the codec can accept (ENCODING-V1 §2)
T_ATTEST, T_MANIFEST = "tessera-v1/attest", "tessera-v1/manifest"
RE_REQID = re.compile(r"[A-Za-z0-9._:-]{1,128}")
RE_REF = re.compile(r"frames/[A-Za-z0-9._-]{1,128}/[0-9a-f]{64}")
INLINE_KEYS = frozenset(("request_id", "sign_by", "frame_b64"))
REF_KEYS = frozenset(("request_id", "sign_by", "frame_ref", "frame_sha256"))


class Refuse(Exception):
    """A refusal: the signer answers REFUSED with this reason and signs nothing."""

    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


@dataclass(frozen=True)
class Request:
    request_id: str
    sign_by: int
    frame_b64: str | None = None
    frame_ref: str | None = None
    frame_sha256: str | None = None


def load(body):
    """Message body -> JSON object. BAD_REQUEST for anything else."""
    if not isinstance(body, str):
        raise Refuse("BAD_REQUEST", "body is not text")
    if len(body.encode("utf-8", "surrogatepass")) > MAX_BODY:
        raise Refuse("BAD_REQUEST", f"body of {len(body)} characters exceeds {MAX_BODY} bytes")
    try:
        obj = json.loads(body)
    except ValueError as e:
        raise Refuse("BAD_REQUEST", f"not JSON: {e}") from None
    if not isinstance(obj, dict):
        raise Refuse("BAD_REQUEST", "not a JSON object")
    return obj


def request_id(obj):
    rid = obj.get("request_id")
    if not (isinstance(rid, str) and RE_REQID.fullmatch(rid)):
        raise Refuse("BAD_REQUEST", "bad request_id")
    return rid


def parse(obj):
    """JSON object -> Request. Exactly one of the two shapes; strict values."""
    rid = request_id(obj)
    keys = set(obj)
    if keys not in (INLINE_KEYS, REF_KEYS):
        raise Refuse("BAD_REQUEST", f"members {sorted(keys)}; want {sorted(INLINE_KEYS)} or {sorted(REF_KEYS)}")
    try:
        sign_by = utc(obj["sign_by"])
    except Fault:
        raise Refuse("BAD_REQUEST", "sign_by is not an RFC 3339 UTC second") from None
    if keys == INLINE_KEYS:
        if not isinstance(obj["frame_b64"], str):
            raise Refuse("BAD_REQUEST", "frame_b64 is not a string")
        return Request(rid, sign_by, frame_b64=obj["frame_b64"])
    ref, digest = obj["frame_ref"], obj["frame_sha256"]
    if not (isinstance(ref, str) and RE_REF.fullmatch(ref)):
        raise Refuse("BAD_REQUEST", "frame_ref is not frames/<rid>/<sha256>")
    if not (isinstance(digest, str) and HEX.fullmatch(digest)):
        raise Refuse("BAD_REQUEST", "frame_sha256 is not 64 lowercase hex digits")
    return Request(rid, sign_by, frame_ref=ref, frame_sha256=digest)


def inline_frame(req):
    """Strict, canonical base64 (the issuer's b64e) -> bytes."""
    try:
        frame = b64(req.frame_b64)
    except Fault:
        raise Refuse("BAD_REQUEST", "frame_b64 is not canonical base64") from None
    if len(frame) > MAX_FRAME:
        raise Refuse("BAD_REQUEST", "frame too large")
    return frame


def check_frame(frame, key_fp, clock):
    """-> (kind, alg), or raises Refuse. `clock` is the signer's own clock, integer seconds."""
    if len(frame) < 1 or len(frame) < 1 + frame[0]:
        raise Refuse("TRUNCATED", "no complete tag")
    expected = T_MANIFEST if frame[1:1 + frame[0]] == T_MANIFEST.encode() else T_ATTEST   # else TAG_UNKNOWN/MISMATCH
    try:
        obj = read_frame(frame, expected)
    except Fault as e:
        raise Refuse(e.code, f"frame does not decode as {expected}") from None
    if expected == T_ATTEST:
        alg, fp = obj["common"]["alg"], obj["signer"]["key_fp"]
    else:
        alg, fp = obj["alg"], obj["sset"][0]
    if alg != ALG:
        raise Refuse("ALG_NOT_ALLOWED", alg)
    if fp != key_fp:
        raise Refuse("KEY_FP_MISMATCH", fp)
    if expected == T_ATTEST:
        declared = utc(obj["common"]["declared_issue_time"])
        if abs(declared - clock) > EPS:
            raise Refuse("DECLARED_TIME_OUTSIDE_EPSILON",
                         f"declared {obj['common']['declared_issue_time']}, difference {declared - clock} s, "
                         f"epsilon {EPS} s")
    return ("attest" if expected == T_ATTEST else "manifest"), alg


def check_stop(now, sign_until, sign_by):
    """IS-03, called immediately before the HSM call: refuse past the configured stop or the request's sign_by."""
    if now > sign_until:
        raise Refuse("SIGNING_STOPPED", f"signer clock {now} past the configured signing stop {sign_until}")
    if now > sign_by:
        raise Refuse("SIGNING_STOPPED", f"signer clock {now} past the request's sign_by {sign_by}")
