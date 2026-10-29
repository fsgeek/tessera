"""One run of the slot-2 policy signer over injected clients: drain the request queue for a time budget and, for each
request, either sign the frame with the HSM key (one rule-O packet) or refuse it with a reason. Queue content and the
referenced frame objects are untrusted input.

Clients (boto3-style for AWS, so main.py passes boto3 clients straight in; tests pass fakes):
  sqs  receive_message / send_message / delete_message
  s3   get_object(Bucket, Key) -> {"Body": readable, "ContentLength": int}; a missing object raises an error whose
       response Error Code is NoSuchKey, 404 or NotFound
  kms  public_key() -> Cloud KMS PublicKey resource (dict); sign_digest(sha256 digest) -> DER ECDSA signature
  clock() -> integer seconds; monotonic() -> float seconds; log(**fields)

Response (the issuer reads request_id, status, sig_b64, reason; everything else is for the logs and the operator):
  {"v": 1, "request_id", "sqs_message_id", "status": "SIGNED" | "REFUSED", "kind"?, "sig_b64"?, "sig_sha256"?,
   "frame_sha256"?, "reason"?, "detail"?, "signer": {"slot": "gpg", "clock", ...}}

E-02 on this side: every signature is logged (request id, frame SHA-256, signature SHA-256) before its response is
sent. A request delivered twice in one run gets the same signature again, not a second one. Across runs there is no
memory: a request redelivered after its response was sent (a failed delete) is signed again, and the issuer records
the second response as a duplicate. sign_by bounds how late that can happen."""
import base64
import hashlib
import json
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from tessera_verify.codec import (Fault, parse_signature, public_key, registered_codecs, sig_policy,
                                  signature_verifies, isotime)

from . import openpgp, policy
from .policy import ALG, EPS, Refuse

SLOT = "gpg"
MAX_RECEIVES = 3                      # transient errors (KMS, S3, network): leave the message, then refuse
KMS_ALGORITHM = "EC_SIGN_P256_SHA256"
REGISTRY = registered_codecs(ALG)


def code_sha256():
    here = os.path.dirname(os.path.abspath(__file__))
    h = hashlib.sha256()
    for name in sorted(f for f in os.listdir(here) if f.endswith(".py")):
        with open(os.path.join(here, name), "rb") as f:
            h.update(name.encode() + b"\0" + f.read() + b"\0")
    return h.hexdigest()


def _not_found(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code")
    return code in ("NoSuchKey", "404", "NotFound") or type(exc).__name__ == "NoSuchKey"


class StartupError(Exception):
    """The signer refuses to run at all (wrong key, wrong configuration)."""


class Signer:
    def __init__(self, cfg, kms, sqs, s3, clock, monotonic, log):
        self.cfg, self.kms, self.sqs, self.s3 = cfg, kms, sqs, s3
        self.clock, self.monotonic, self.log = clock, monotonic, log
        self.code = code_sha256()
        self.issued = {}                  # (request_id, frame sha256) -> packet, this run only
        self.pub = self.key_bytes = self.fpr = None

    # ------------------------------------------------------------------------------------------ the key
    def load_key(self):
        """Fetch the HSM public key and check it against the pinned version, algorithm, protection level and
        fingerprint before anything is signed."""
        pk = self.kms.public_key()
        if pk.get("name") != self.cfg.key_version:
            raise StartupError(f"KMS returned key version {pk.get('name')!r}, not {self.cfg.key_version!r}")
        if pk.get("algorithm") != KMS_ALGORITHM:
            raise StartupError(f"key algorithm {pk.get('algorithm')!r}, not {KMS_ALGORITHM}")
        if pk.get("protectionLevel") != "HSM":
            raise StartupError(f"key protection level {pk.get('protectionLevel')!r}, not HSM")
        try:
            pub = serialization.load_pem_public_key(pk["pem"].encode())
        except (KeyError, ValueError, TypeError) as e:
            raise StartupError(f"KMS public key does not load: {e!r}") from None
        if not isinstance(pub, ec.EllipticCurvePublicKey) or pub.curve.name != "secp256r1":
            raise StartupError("KMS public key is not P-256")
        body = openpgp.key_body(openpgp.point65(pub), self.cfg.key_created)
        fp = openpgp.fp_gpg(body)
        if fp != self.cfg.key_fp:
            raise StartupError(f"HSM key fingerprint {fp} is not the pinned {self.cfg.key_fp}; refusing to run")
        self.pub, self.key_bytes, self.fpr = pub, body, openpgp.v4_fingerprint(body)
        self.verify_key = public_key(body, SLOT, ALG)      # the verifier's own key gate (KEY_FORMAT)

    # ------------------------------------------------------------------------------------------ signing
    def sign(self, frame, created):
        """One rule-O packet over the exact frame, created at `created`; checked with the service verifier's own
        functions (the checks the issuer runs) before it is returned."""
        hashed = openpgp.hashed_area(self.fpr, created)
        unhashed = openpgp.subpacket(16, self.fpr[-8:])
        digest = openpgp.sig_digest(frame, hashed)
        der = self.kms.sign_digest(digest)
        self.pub.verify(der, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))   # raises if the HSM output is bad
        r, s = utils.decode_dss_signature(der)
        packet = openpgp.sig_packet(hashed, unhashed, digest[:2], r, s)
        try:
            parsed = parse_signature(packet, ALG, SLOT, REGISTRY)
            sig_policy(parsed)
            ok = signature_verifies(frame, parsed, self.verify_key)
        except Fault as e:
            raise RuntimeError(f"self-check: {e.code}") from None
        if not ok:
            raise RuntimeError("self-check: the packet does not verify on the frame")
        return packet

    # ------------------------------------------------------------------------------------------ one message
    def _signer_info(self, clock):
        c = self.cfg
        return {"slot": SLOT, "clock": isotime(clock), "code_sha256": self.code, "image": c.image,
                "key_version": c.key_version, "key_fp": c.key_fp, "epsilon_s": EPS, "alg": ALG,
                "sign_until": isotime(c.sign_until)}

    def _receives(self, msg):
        try:
            return int(msg.get("Attributes", {}).get("ApproximateReceiveCount", "1"))
        except ValueError:
            return 1

    def _transient(self, msg, rid, reason, exc):
        """Leave the message for redelivery (None), or after MAX_RECEIVES deliveries refuse with `reason`."""
        if self._receives(msg) < MAX_RECEIVES:
            self.log(event="transient_retry", request_id=rid, reason=reason, error=repr(exc)[:500])
            return None
        raise Refuse(reason, repr(exc)[:500])

    def fetch(self, req, msg):
        """IS-09: the object at frame_ref, accepted only if its SHA-256 is frame_sha256. None: retry later."""
        try:
            obj = self.s3.get_object(Bucket=self.cfg.frame_bucket, Key=req.frame_ref)
        except Exception as e:  # noqa: BLE001
            if _not_found(e):
                raise Refuse("FRAME_UNAVAILABLE", req.frame_ref) from None
            return self._transient(msg, req.request_id, "FRAME_UNAVAILABLE", e)
        size = obj.get("ContentLength")
        if isinstance(size, int) and size > policy.MAX_FRAME:
            raise Refuse("FRAME_UNAVAILABLE", f"object of {size} bytes exceeds {policy.MAX_FRAME}")
        try:
            frame = obj["Body"].read(policy.MAX_FRAME + 1)
        except Exception as e:  # noqa: BLE001
            return self._transient(msg, req.request_id, "FRAME_UNAVAILABLE", e)
        if len(frame) > policy.MAX_FRAME:
            raise Refuse("FRAME_UNAVAILABLE", f"object exceeds {policy.MAX_FRAME} bytes")
        if hashlib.sha256(frame).hexdigest() != req.frame_sha256:
            raise Refuse("FRAME_DIGEST_MISMATCH", f"object at {req.frame_ref} is not {req.frame_sha256}")
        return frame

    def handle(self, msg):
        """Answer one request message and delete it, or leave it on the queue for a later delivery.
        -> the response sent, or None."""
        clock = self.clock()
        resp = {"v": 1, "sqs_message_id": msg.get("MessageId"), "request_id": None,
                "signer": self._signer_info(clock)}
        try:
            obj = policy.load(msg.get("Body"))
            resp["request_id"] = policy.request_id(obj)
            req = policy.parse(obj)
            frame = policy.inline_frame(req) if req.frame_b64 is not None else self.fetch(req, msg)
            if frame is None:
                return None
            fsha = resp["frame_sha256"] = hashlib.sha256(frame).hexdigest()
            now = self.clock()                           # SG-02: after the frame is in hand; IS-03: just before signing
            kind, _ = policy.check_frame(frame, self.cfg.key_fp, now)
            policy.check_stop(now, self.cfg.sign_until, req.sign_by)    # SG-01: for a resend as well
            packet = self.issued.get((req.request_id, fsha))
            if packet is None:
                try:
                    packet = self.sign(frame, now)
                except Exception as e:  # noqa: BLE001  KMS, network, or a failed self-check
                    return self._transient(msg, req.request_id, "SIGNER_ERROR", e)
                try:
                    policy.check_stop(self.clock(), self.cfg.sign_until, req.sign_by)
                except Refuse:                           # SG-01: the HSM signed after a cutoff: withheld, logged
                    self.log(event="withheld", request_id=req.request_id, frame_sha256=fsha,
                             sig_sha256=hashlib.sha256(packet).hexdigest(), created=isotime(now))
                    raise
                self.issued[(req.request_id, fsha)] = packet
                self.log(event="signed", request_id=req.request_id, frame_sha256=fsha,
                         sig_sha256=hashlib.sha256(packet).hexdigest(), created=isotime(now), kind=kind)
            else:
                self.log(event="resent", request_id=req.request_id, frame_sha256=fsha,
                         sig_sha256=hashlib.sha256(packet).hexdigest())
            resp.update(status="SIGNED", kind=kind, sig_b64=base64.b64encode(packet).decode("ascii"),
                        sig_sha256=hashlib.sha256(packet).hexdigest())
        except Refuse as r:
            resp.update(status="REFUSED", reason=r.code, detail=r.detail[:500])        # signed nothing
        except Exception as e:  # noqa: BLE001  a codec bug or unexpected input: refuse, never sign
            resp.update(status="REFUSED", reason="INTERNAL", detail=repr(e)[:500])
        self.sqs.send_message(QueueUrl=self.cfg.response_queue_url, MessageBody=_dumps(resp))
        self.sqs.delete_message(QueueUrl=self.cfg.request_queue_url, ReceiptHandle=msg["ReceiptHandle"])
        self.log(event="response", request_id=resp["request_id"], sqs_message_id=resp["sqs_message_id"],
                 status=resp["status"], reason=resp.get("reason"), detail=resp.get("detail"),
                 frame_sha256=resp.get("frame_sha256"), sig_sha256=resp.get("sig_sha256"),
                 clock=resp["signer"]["clock"])
        return resp

    # ------------------------------------------------------------------------------------------ one run
    def run(self):
        """Drain the request queue until it is empty or the budget is spent. -> number of messages answered."""
        t0, n = self.monotonic(), 0
        self.log(event="start", code_sha256=self.code, image=self.cfg.image, key_version=self.cfg.key_version,
                 key_fp=self.cfg.key_fp, alg=ALG, epsilon_s=EPS, sign_until=isotime(self.cfg.sign_until),
                 clock=isotime(self.clock()))
        while self.monotonic() - t0 < self.cfg.budget_s:
            msgs = self.sqs.receive_message(
                QueueUrl=self.cfg.request_queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=self.cfg.wait_s,
                VisibilityTimeout=self.cfg.visibility_s,
                MessageSystemAttributeNames=["ApproximateReceiveCount"]).get("Messages", [])
            if not msgs:
                break
            for m in msgs:
                try:
                    if self.handle(m) is not None:
                        n += 1
                except Exception as e:  # noqa: BLE001  send or delete failed: the queue delivers it again
                    self.log(event="handle_error", sqs_message_id=m.get("MessageId"), error=repr(e)[:500])
        self.log(event="done", answered=n, seconds=round(self.monotonic() - t0, 1))
        return n


def _dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))
