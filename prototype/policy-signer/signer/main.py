# Slot-2 policy signer (instrument code under A9.2; never ships). Design: prototype/policy-signer/DESIGN.md.
#
# One run of the Cloud Run job: obtain AWS credentials by web identity federation (a Google-issued OIDC token
# for this job's service account; no static credential), drain the SQS request queue for a short time budget,
# and for each request either sign the frame with the GCP HSM key slot2-spike (rule O: one OpenPGP v4 type-0x00
# packet, ENCODING-V1 §5.2) or refuse it with a reason. Queue content is untrusted input.
#
# Policy (A9.6, DESIGN.md decision 4), enforced here, before any signature is requested:
#   - the frame decodes, under the vendored P8 reference decoder (p8_codec.py, verbatim from gen.py), as
#     tessera-v1/attest or tessera-v1/manifest, within schema;
#   - common.alg (manifest: alg) is one of ALLOWED_ALGS;
#   - attest: signer.key_fp equals this key's gpg-sha256 fingerprint; manifest: sset[0] equals it;
#   - attest: |declared_issue_time - this container's clock| <= EPSILON (24 h, A9.2), clock = time.time().
# EPSILON and the policy are code, not configuration. Nothing in a request can change them.
import base64
import calendar
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import boto3
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

import p8_codec as P8

EPSILON = 24 * 3600                     # A9.2: ε = 24 h. Refuse iff |declared - clock| > ε.
MAX_BODY = 1 << 20                      # request message cap (bytes of JSON text)
MAX_RECEIVES = 3                        # transient signing errors: retry, then refuse
RE_REQID = re.compile(r"[A-Za-z0-9._:-]{1,128}")

ENV = os.environ
REQ_URL, RESP_URL = ENV["REQUEST_QUEUE_URL"], ENV["RESPONSE_QUEUE_URL"]
ROLE_ARN, AUDIENCE, REGION = ENV["AWS_ROLE_ARN"], ENV["AWS_AUDIENCE"], ENV.get("AWS_REGION_QUEUES", "us-east-2")
KEY_VERSION = ENV["KMS_KEY_VERSION"]    # projects/.../cryptoKeys/slot2-spike/cryptoKeyVersions/1
KEY_CREATED = int(ENV["KEY_CREATED"])   # OpenPGP key creation time bound into the fingerprint
KEY_FP = ENV["KEY_FP"]                  # expected gpg-sha256 fingerprint; checked against the HSM public key
ALLOWED_ALGS = tuple(a for a in ENV["ALLOWED_ALGS"].split(",") if a)
IMAGE = ENV.get("SIGNER_IMAGE", "unknown")
BUDGET = int(ENV.get("RUN_SECONDS", "40"))

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_SHA256 = hashlib.sha256(b"".join(open(os.path.join(HERE, f), "rb").read()
                                      for f in ("main.py", "p8_codec.py"))).hexdigest()

def log(**kw):
    print(json.dumps(kw, sort_keys=True), flush=True)

def utcnow():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---- Google metadata server and Cloud KMS REST ---------------------------------------------------------------
MD = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/"

def metadata(path):
    req = urllib.request.Request(MD + path, headers={"Metadata-Flavor": "Google"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"metadata {path.split('?')[0]}: HTTP {e.code} {e.read()[:300]!r}") from None

def gcp_token():
    return json.loads(metadata("token"))["access_token"]

def kms(method, suffix, body=None):
    req = urllib.request.Request(f"https://cloudkms.googleapis.com/v1/{KEY_VERSION}{suffix}", method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + gcp_token(),
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"KMS {suffix}: HTTP {e.code} {e.read()[:300]!r}") from None

def _crc32c(data):
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 & -(crc & 1))
    return crc ^ 0xFFFFFFFF

def hsm_sign_digest(digest):
    out = kms("POST", ":asymmetricSign", {"digest": {"sha256": base64.b64encode(digest).decode()},
                                          "digestCrc32c": str(_crc32c(digest))})
    if out.get("name") != KEY_VERSION or not out.get("verifiedDigestCrc32c"):
        raise RuntimeError(f"KMS response integrity: name={out.get('name')} verified={out.get('verifiedDigestCrc32c')}")
    der = base64.b64decode(out["signature"])
    if int(out["signatureCrc32c"]) != _crc32c(der):
        raise RuntimeError("KMS signature CRC32C mismatch")
    return der

# ---- the key: fetched from the HSM, checked against the pinned fingerprint before anything is signed ---------
def load_key():
    pk = kms("GET", "/publicKey")
    if pk.get("algorithm") != "EC_SIGN_P256_SHA256" or pk.get("name") != KEY_VERSION:
        raise SystemExit(f"unexpected key: {pk.get('name')} {pk.get('algorithm')}")
    pub = serialization.load_pem_public_key(pk["pem"].encode())
    n = pub.public_numbers()
    pt = P8._point(n.x, n.y)
    fp = P8.fp_gpg(pt, KEY_CREATED)
    if fp != KEY_FP:
        raise SystemExit(f"HSM key fingerprint {fp} is not the pinned {KEY_FP}; refusing to run")
    fpr = hashlib.sha1(b"\x99" + len(P8.openpgp_v4_body(pt, KEY_CREATED)).to_bytes(2, "big")
                       + P8.openpgp_v4_body(pt, KEY_CREATED)).digest()      # OpenPGP v4 fingerprint (interop only)
    return pub, fpr

# ---- policy -------------------------------------------------------------------------------------------------
class Refuse(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code)
        self.code, self.detail = code, detail

def check_policy(frame, clock):
    """Returns (kind, alg) or raises Refuse. Runs entirely before any signing request."""
    if len(frame) < 1 or len(frame) < 1 + frame[0]:
        raise Refuse("TRUNCATED", "no complete tag")
    tag = frame[1:1 + frame[0]]
    expected = P8.T_MANIFEST if tag == P8.T_MANIFEST else P8.T_ATTEST   # anything else: TAG_UNKNOWN/TAG_MISMATCH
    try:
        v = P8.decode_frame(frame, expected)
    except P8.Reject as e:
        raise Refuse(e.code, str(e))
    if expected == P8.T_ATTEST:
        alg, fp = v["common"]["alg"], v["signer"]["key_fp"]
    else:
        alg, fp = v["alg"], v["sset"][0]
    if alg not in ALLOWED_ALGS:
        raise Refuse("ALG_NOT_ALLOWED", alg)
    if fp != KEY_FP:
        raise Refuse("KEY_FP_MISMATCH", fp)
    if expected == P8.T_ATTEST:
        declared = calendar.timegm(time.strptime(v["common"]["declared_issue_time"], "%Y-%m-%dT%H:%M:%SZ"))
        if abs(declared - clock) > EPSILON:
            raise Refuse("DECLARED_TIME_OUTSIDE_EPSILON",
                         f"declared {v['common']['declared_issue_time']}, signer clock "
                         f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(clock))}, "
                         f"difference {declared - int(clock)} s, epsilon {EPSILON} s")
    return ("attest" if expected == P8.T_ATTEST else "manifest"), alg

def sign_rule_o(frame, alg, pub, fpr):
    """One rule-O packet, built exactly as prototype/spike-pq/spike_gcp.py builds it; self-checked before return."""
    when = int(time.time())
    hashed = P8._subpacket(33, b"\x04" + fpr) + P8._subpacket(2, when.to_bytes(4, "big"))
    unhashed = P8._subpacket(16, fpr[-8:])
    digest = P8.openpgp_v4_sig_digest(frame, hashed)
    der = hsm_sign_digest(digest)
    pub.verify(der, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))     # raises if the HSM output is bad
    r, s = utils.decode_dss_signature(der)
    packet = P8.openpgp_v4_sig_packet(hashed, unhashed, digest[:2], r, s)
    P8.decode_sig(packet, alg, 1)                                            # rule-O codec gate, slot gpg
    return packet

# ---- queue loop ---------------------------------------------------------------------------------------------
def aws_session():
    token = metadata(f"identity?audience={urllib.request.quote(AUDIENCE)}&format=full")
    sts = boto3.client("sts", region_name=REGION)
    c = sts.assume_role_with_web_identity(RoleArn=ROLE_ARN, RoleSessionName="slot2-signer",
                                          WebIdentityToken=token, DurationSeconds=900)["Credentials"]
    return boto3.client("sqs", region_name=REGION, aws_access_key_id=c["AccessKeyId"],
                        aws_secret_access_key=c["SecretAccessKey"], aws_session_token=c["SessionToken"])

def handle(sqs, msg, pub, fpr):
    clock = time.time()
    resp = {"v": 1, "sqs_message_id": msg["MessageId"], "request_id": None,
            "signer": {"code_sha256": CODE_SHA256, "image": IMAGE, "key_version": KEY_VERSION, "key_fp": KEY_FP,
                       "epsilon_s": EPSILON, "allowed_algs": list(ALLOWED_ALGS),
                       "clock": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(clock))}}
    frame = b""
    try:
        body = msg.get("Body", "")
        if len(body) > MAX_BODY:
            raise Refuse("REQUEST_TOO_LARGE", str(len(body)))
        try:
            req = json.loads(body)
        except ValueError as e:
            raise Refuse("REQUEST_MALFORMED", f"not JSON: {e}")
        if not isinstance(req, dict) or set(req) != {"request_id", "frame_b64"}:
            raise Refuse("REQUEST_MALFORMED", "want exactly {request_id, frame_b64}")
        if isinstance(req["request_id"], str) and RE_REQID.fullmatch(req["request_id"]):
            resp["request_id"] = req["request_id"]
        else:
            raise Refuse("REQUEST_MALFORMED", "bad request_id")
        try:
            frame = base64.b64decode(req["frame_b64"], validate=True)
        except Exception:
            raise Refuse("REQUEST_MALFORMED", "frame_b64 is not strict base64")
        resp["frame_sha256"] = hashlib.sha256(frame).hexdigest()
        kind, alg = check_policy(frame, clock)
        try:
            packet = sign_rule_o(frame, alg, pub, fpr)
        except Exception as e:                                       # transient (KMS/network) or self-check fail
            if int(msg["Attributes"].get("ApproximateReceiveCount", "1")) < MAX_RECEIVES:
                log(event="sign_error_retry", request_id=resp["request_id"], error=repr(e))
                return                                               # leave it; visibility timeout re-delivers
            raise Refuse("SIGNER_ERROR", repr(e))
        resp.update(status="SIGNED", kind=kind, sig_b64=base64.b64encode(packet).decode())
    except Refuse as r:
        resp.update(status="REFUSED", reason=r.code, detail=r.detail[:500])     # signed nothing
    except Exception as e:                                           # decoder bug or unexpected input
        resp.update(status="REFUSED", reason="INTERNAL", detail=repr(e)[:500])
    sqs.send_message(QueueUrl=RESP_URL, MessageBody=json.dumps(resp, sort_keys=True))
    sqs.delete_message(QueueUrl=REQ_URL, ReceiptHandle=msg["ReceiptHandle"])
    log(event="response", request_id=resp["request_id"], sqs_message_id=msg["MessageId"],
        status=resp["status"], reason=resp.get("reason"), detail=resp.get("detail"),
        frame_sha256=resp.get("frame_sha256"), clock=resp["signer"]["clock"])

def main():
    t0 = time.time()
    pub, fpr = load_key()
    sqs = aws_session()
    log(event="start", code_sha256=CODE_SHA256, image=IMAGE, key_version=KEY_VERSION, key_fp=KEY_FP,
        allowed_algs=list(ALLOWED_ALGS), epsilon_s=EPSILON, clock=utcnow())
    n = 0
    while time.time() - t0 < BUDGET:
        msgs = sqs.receive_message(QueueUrl=REQ_URL, MaxNumberOfMessages=10, WaitTimeSeconds=5,
                                   VisibilityTimeout=60, MessageSystemAttributeNames=["ApproximateReceiveCount"]).get("Messages", [])
        if not msgs:
            break
        for m in msgs:
            m.setdefault("Attributes", {})
            handle(sqs, m, pub, fpr)
            n += 1
    log(event="done", handled=n, seconds=round(time.time() - t0, 1))

if __name__ == "__main__":
    main()
