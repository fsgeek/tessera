# THROWAWAY INSTRUMENT SPIKE - never ships. KMS half of the PQ spike (A9 pass condition):
# a real AWS KMS ML-DSA-65 signature over a V1-shaped frame, RAW (<= 4096 B) and EXTERNAL_MU (> 4096 B),
# verified offline in two independent implementations (cryptography, dilithium-py).
# Run: cd prototype/spike-pq && uv run python spike_kms.py   (needs `aws login --profile tessera`)
# Phase "capture" talks to KMS and writes out-kms/; phase "verify" is offline and reads only out-kms/.
import base64, hashlib, json, os, struct, subprocess, sys, tempfile
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import mldsa as C
from dilithium_py.ml_dsa import ML_DSA_65 as D

AWS = os.path.expanduser("~/.local/bin/aws")
PROFILE, REGION, ALIAS = "tessera", "us-east-2", "alias/tessera-pq-spike"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out-kms")

def jcs(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
def header(t): t = t.encode(); return bytes([len(t)]) + t
def frame(t, payload): return header(t) + struct.pack(">HI", 1, len(payload)) + payload
def make_frame(content_len):
    return frame("tessera-v1/receipt", jcs({"content": "a" * content_len, "issuer": "wamason.com", "slot": "kms"}))
def mu_of(pk_raw, msg):  # FIPS 204 external mu, pure mode, empty context
    return hashlib.shake_256(hashlib.shake_256(pk_raw).digest(64) + b"\x00\x00" + msg).digest(64)

def aws(*args):
    r = subprocess.run([AWS, *args, "--profile", PROFILE, "--region", REGION, "--output", "json"],
                       capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout) if r.stdout.strip() else {}

def key_id():
    try: return aws("kms", "describe-key", "--key-id", ALIAS)["KeyMetadata"]["KeyId"]
    except RuntimeError as e:
        if "NotFoundException" not in str(e): raise
    k = aws("kms", "create-key", "--key-spec", "ML_DSA_65", "--key-usage", "SIGN_VERIFY",
            "--description", "Tessera PQ spike (throwaway; delete after spike)",
            "--tags", "TagKey=project,TagValue=tessera", "TagKey=purpose,TagValue=pq-spike")["KeyMetadata"]["KeyId"]
    aws("kms", "create-alias", "--alias-name", ALIAS, "--target-key-id", k)
    return k

def kms_sign(kid, msg, mtype):
    with tempfile.NamedTemporaryFile(delete=False) as f: f.write(msg); p = f.name
    try:
        return base64.b64decode(aws("kms", "sign", "--key-id", kid, "--message", f"fileb://{p}",
                                    "--message-type", mtype, "--signing-algorithm", "ML_DSA_SHAKE_256")["Signature"])
    finally: os.unlink(p)

def capture():
    os.makedirs(OUT, exist_ok=True)
    kid = key_id()
    meta = aws("kms", "describe-key", "--key-id", kid)["KeyMetadata"]
    spki = base64.b64decode(aws("kms", "get-public-key", "--key-id", kid)["PublicKey"])
    pk_raw = serialization.load_der_public_key(spki).public_bytes_raw()
    small, big = make_frame(2048), make_frame(6000)
    assert len(small) <= 4096 < len(big)
    rec = {"key_id": kid, "key_spec": meta.get("KeySpec"), "origin": meta.get("Origin"), "region": REGION,
           "spki_b64": base64.b64encode(spki).decode(),
           "small_frame_b64": base64.b64encode(small).decode(), "big_frame_b64": base64.b64encode(big).decode(),
           "sig_raw_small_b64": base64.b64encode(kms_sign(kid, small, "RAW")).decode(),
           "sig_mu_big_b64": base64.b64encode(kms_sign(kid, mu_of(pk_raw, big), "EXTERNAL_MU")).decode()}
    try: kms_sign(kid, big, "RAW"); rec["raw_over_4096"] = "ACCEPTED (unexpected)"
    except RuntimeError as e: rec["raw_over_4096"] = "REJECTED: " + str(e)[-160:]
    json.dump(rec, open(os.path.join(OUT, "capture.json"), "w"), indent=1)
    print("captured", kid, meta.get("KeySpec"), meta.get("Origin"))

def verify():  # offline: reads only out-kms/capture.json
    r = json.load(open(os.path.join(OUT, "capture.json")))
    b = lambda k: base64.b64decode(r[k])
    pub = serialization.load_der_public_key(b("spki_b64")); assert isinstance(pub, C.MLDSA65PublicKey)
    pk_raw = pub.public_bytes_raw()
    def crypto_ok(sig, msg):
        try: pub.verify(sig, msg); return True
        except Exception: return False
    small, big = b("small_frame_b64"), b("big_frame_b64")
    res = {
        "key_spec/origin": (r["key_spec"], r["origin"]),
        "pk/sig sizes": (len(pk_raw), len(b("sig_raw_small_b64")), len(b("sig_mu_big_b64"))),
        "RAW small: cryptography": crypto_ok(b("sig_raw_small_b64"), small),
        "RAW small: dilithium-py": D.verify(pk_raw, small, b("sig_raw_small_b64"), ctx=b""),
        "MU big (full msg): cryptography": crypto_ok(b("sig_mu_big_b64"), big),
        "MU big (full msg): dilithium-py": D.verify(pk_raw, big, b("sig_mu_big_b64"), ctx=b""),
        "tamper small rejected (both)": not crypto_ok(b("sig_raw_small_b64"), small[:-1] + b"\x00")
            and not D.verify(pk_raw, small[:-1] + b"\x00", b("sig_raw_small_b64"), ctx=b""),
        "tamper big rejected (both)": not crypto_ok(b("sig_mu_big_b64"), big[:-1] + b"\x00")
            and not D.verify(pk_raw, big[:-1] + b"\x00", b("sig_mu_big_b64"), ctx=b""),
        "RAW > 4096 at KMS": r["raw_over_4096"],
    }
    for k, v in res.items(): print(f"{k}: {v}")
    checks = [v for k, v in res.items() if isinstance(v, bool)]
    print("PASS" if all(checks) else "FAIL")
    return all(checks)

if __name__ == "__main__":
    if "verify" not in sys.argv[1:]: capture()
    sys.exit(0 if verify() else 1)
