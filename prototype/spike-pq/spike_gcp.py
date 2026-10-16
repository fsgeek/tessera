# THROWAWAY INSTRUMENT SPIKE - never ships. Slot-2 half of the PQ spike (A9.6 pass condition, slot-2 custody =
# GCP Cloud KMS HSM P-256): a real HSM signature over a V1 attest frame, serialized as rule O (one OpenPGP v4
# type-0x00 packet, ENCODING-V1 §5.2) using the P8 reference encoder, verified offline by the P8 decoder plus two
# independent ECDSA implementations (P8 gen.py pure-Python, and `cryptography`/OpenSSL).
# Run from the repo root: prototype/.venv/bin/python prototype/spike-pq/spike_gcp.py [verify]
import json, os, subprocess, sys, tempfile, datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "formal", "p8", "vectors"))
import gen  # P8 reference encoder/decoder (implementation A)

GCLOUD = os.path.expanduser("~/.local/bin/gcloud")
KEY = ["--project=tessera-slot2", "--location=us-east1", "--keyring=tessera-v1", "--key=slot2-spike", "--version=1"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out-gcp")

def gc(*args):
    r = subprocess.run([GCLOUD, *args], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return r.stdout

def golden(vid):
    for v in json.load(open(os.path.join(ROOT, "formal/p8/vectors/golden.json")))["vectors"]:
        if v["id"] == vid: return v
    raise KeyError(vid)

def capture():
    os.makedirs(OUT, exist_ok=True)
    KV = [k for k in KEY if not k.startswith("--version")]   # key-version commands take the version positionally
    pem = gc("kms", "keys", "versions", "get-public-key", "1", *KV)
    pub = serialization.load_pem_public_key(pem.encode())
    nums = pub.public_numbers(); pt = gen._point(nums.x, nums.y)   # 65-byte uncompressed point (gen's key form)
    desc = json.loads(gc("kms", "keys", "versions", "describe", "1", *KV, "--format=json"))
    created = int(datetime.datetime.fromisoformat(desc["createTime"].replace("Z", "+00:00")).timestamp())
    key_fp = gen.fp_gpg(pt, created)                      # "gpg-sha256:<hex>" over the v4 key-packet body
    # A real V1 attest frame: golden F-01's common block, signer bound to this HSM key's slot fingerprint.
    f01 = bytes.fromhex(golden("F-01")["bytes_hex"])                    # the encoded golden frame itself
    common = json.loads(f01[f01.index(b"{"):])["common"]                 # its JCS payload (ASCII-safe in F-01)
    frame = gen.encode_attest(common, key_fp)
    fpr = __import__("hashlib").sha1(b"\x99" + len(gen.openpgp_v4_body(pt, created)).to_bytes(2, "big")
                                     + gen.openpgp_v4_body(pt, created)).digest()
    sig_created = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    hashed = gen._subpacket(33, b"\x04" + fpr) + gen._subpacket(2, sig_created.to_bytes(4, "big"))
    unhashed = gen._subpacket(16, fpr[-8:])
    head = bytes([4, 0x00, 19, 8]) + len(hashed).to_bytes(2, "big") + hashed
    preimage = frame + head + b"\x04\xff" + len(head).to_bytes(4, "big")   # SHA-256 of this = OpenPGP v4 digest
    assert __import__("hashlib").sha256(preimage).digest() == gen.openpgp_v4_sig_digest(frame, hashed)
    with tempfile.TemporaryDirectory() as d:
        inp, sigf = os.path.join(d, "in"), os.path.join(d, "sig")
        open(inp, "wb").write(preimage)
        gc("kms", "asymmetric-sign", *KEY, "--digest-algorithm=sha256", f"--input-file={inp}", f"--signature-file={sigf}")
        der = open(sigf, "rb").read()
    r, s = utils.decode_dss_signature(der)
    packet = gen.openpgp_v4_sig_packet(hashed, unhashed, gen.openpgp_v4_sig_digest(frame, hashed)[:2], r, s)
    rec = {"key": "/".join(KEY), "protection": desc.get("protectionLevel"), "algorithm": desc.get("algorithm"),
           "attestation_format": (desc.get("attestation") or {}).get("format"), "key_created": created,
           "spki_pem": pem, "key_fp": key_fp, "frame_hex": frame.hex(), "sig_hex": packet.hex()}
    json.dump(rec, open(os.path.join(OUT, "capture.json"), "w"), indent=1)
    print("captured", rec["protection"], rec["algorithm"], rec["attestation_format"])

def verify():
    r = json.load(open(os.path.join(OUT, "capture.json")))
    frame, sig = bytes.fromhex(r["frame_hex"]), bytes.fromhex(r["sig_hex"])
    pub = serialization.load_pem_public_key(r["spki_pem"].encode()); n = pub.public_numbers()
    pt, q = gen._point(n.x, n.y), (n.x, n.y)        # bytes for fingerprints, (x, y) for gen ECDSA
    gen.decode_sig(sig, gen.ALG_V1, 1)                              # rule O codec gate (P8 decoder); raises on reject
    hashed, rr, ss = gen.decode_sig_openpgp4(sig)
    digest = gen.openpgp_v4_sig_digest(frame, hashed)
    def openssl_ok(fr):
        try:
            pub.verify(utils.encode_dss_signature(rr, ss), gen.openpgp_v4_sig_digest(fr, hashed),
                       ec.ECDSA(utils.Prehashed(hashes.SHA256()))); return True
        except Exception: return False
    tampered = frame[:-1] + bytes([frame[-1] ^ 1])
    res = {
        "HSM / algorithm / attestation": (r["protection"], r["algorithm"], r["attestation_format"]),
        "frame signer.key_fp == fp_gpg(HSM point, created)": r["key_fp"] == gen.fp_gpg(pt, r["key_created"])
            and r["key_fp"].encode() in frame,
        "rule O codec accepts packet (P8 decoder)": True,
        "verify: P8 gen.py pure-Python ECDSA": gen.verify_openpgp4(frame, sig, q),
        "verify: cryptography/OpenSSL": openssl_ok(frame),
        "tamper rejected by both": (not gen.verify_openpgp4(tampered, sig, q)) and not openssl_ok(tampered),
        "sig packet length": len(sig),
    }
    for k, v in res.items(): print(f"{k}: {v}")
    ok = all(v for k, v in res.items() if isinstance(v, bool))
    print("PASS" if ok else "FAIL"); return ok

if __name__ == "__main__":
    if "verify" not in sys.argv[1:]: capture()
    sys.exit(0 if verify() else 1)
