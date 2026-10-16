# THROWAWAY INSTRUMENT SPIKE - never ships. PREPARED 2026-10-14, NOT YET RUN (needs AWS and GCP credentials).
# A9.6 pass-condition re-capture: real signatures over GENUINE V1 hybrid frames. The 2026-10-13 KMS capture signed
# V1-SHAPED frames under the tag tessera-v1/receipt, which is not in T (ENCODING-V1 §2), so they cannot sit in A_sig.
# This builds, from the two real spike keys (AWS KMS ML-DSA-65 alias/tessera-pq-spike; GCP HSM P-256 slot2-spike),
# the hybrid manifest and two attestation pairs under the pair id (formal/p8/HYBRID-SUPPLEMENT-DRAFT.md):
#   small pair (frame <= 4096 bytes): kms signs with MessageType RAW;
#   big pair   (frame  > 4096 bytes): kms signs with MessageType EXTERNAL_MU, mu computed here from the KMS key;
#   manifest possession: kms RAW, gpg rule O.
# NOTE (2026-10-14, after owner decision 6 / review HS-05): the selected issuer path is EXTERNAL_MU ALWAYS. The RAW
# calls here (small frame, possession) are COMPARATIVE captures; they do not test the selected one-path policy.
# The gpg slot is signed through the GCP HSM exactly as spike_gcp.py does (rule O, one v4 type-0x00 packet).
# Then it builds both A_sig preimages and verifies OFFLINE: P8 implementation A (gen.py) and implementation B
# (check.py) receipt and possession checks, plus cryptography/OpenSSL and dilithium-py for every ML-DSA signature.
# Run from the repo root:  prototype/.venv/bin/python prototype/spike-pq/spike_v1_hybrid.py [verify]
#   (prototype/.venv has rfc8785 for gen.py, cryptography and dilithium-py; spike-pq/.venv lacks rfc8785)
#   (needs `aws login --profile tessera` and gcloud auth, as the two spikes did; `verify` is offline only)
import base64, datetime, hashlib, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "formal", "p8", "vectors")); sys.path.insert(0, HERE)
import gen, check                    # P8 implementations A and B
import spike_kms as K                # aws(), key_id(), kms_sign()
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from dilithium_py.ml_dsa import ML_DSA_65 as DPY

OUT = os.path.join(HERE, "out-v1-hybrid")
GCLOUD = os.path.expanduser("~/.local/bin/gcloud")
GKEY = ["--project=tessera-slot2", "--location=us-east1", "--keyring=tessera-v1", "--key=slot2-spike", "--version=1"]
D = "wamason.com"

def frames(kms_spki, gpg_fp):
    fm = gen.encode_manifest(gen.ALG_HYBRID, D, gen.fp_spki(kms_spki), gpg_fp)
    def common(content):
        return {"alg": gen.ALG_HYBRID, "binding_forms": ["STMT_DIRECT"], "content": content,
                "declared_issue_time": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "issuer": D, "manifest_sha256": hashlib.sha256(fm).hexdigest(),
                "preamble_sha256": hashlib.sha256(b"ILLUSTRATIVE: purpose preamble bytes\n").hexdigest(),
                "profile": gen.PROFILE,
                "spec": {"id": "tessera-v1-strict/verification-spec/1",
                         "sha256": hashlib.sha256(b"ILLUSTRATIVE: tessera-v1-strict verification specification bytes\n").hexdigest()},
                "vectors_sha256": hashlib.sha256(b"ILLUSTRATIVE: tessera-v1-strict conformance vector bytes\n").hexdigest()}
    cs = common({"statement": "pq-spike-v1", "note": "small"})
    cb = common({"statement": "pq-spike-v1", "blob": "a" * 6000})
    out = {"manifest": fm}
    for name, c in (("small", cs), ("big", cb)):
        out[name] = (gen.encode_attest(c, gen.fp_spki(kms_spki)), gen.encode_attest(c, gpg_fp))
    assert len(out["small"][0]) <= 4096 < len(out["big"][0])
    return out

def gcp_rule_o(doc, pt, created):
    """One rule-O packet over doc, signed by the GCP HSM key (same construction as spike_gcp.py)."""
    body = gen.openpgp_v4_body(pt, created)
    fpr = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).digest()
    when = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    hashed = gen._subpacket(33, b"\x04" + fpr) + gen._subpacket(2, when.to_bytes(4, "big"))
    head = bytes([4, 0x00, 19, 8]) + len(hashed).to_bytes(2, "big") + hashed
    pre = doc + head + b"\x04\xff" + len(head).to_bytes(4, "big")
    with tempfile.TemporaryDirectory() as d:
        inp, sigf = os.path.join(d, "in"), os.path.join(d, "sig")
        open(inp, "wb").write(pre)
        r = subprocess.run([GCLOUD, "kms", "asymmetric-sign", *GKEY, "--digest-algorithm=sha256",
                            f"--input-file={inp}", f"--signature-file={sigf}"], capture_output=True, text=True)
        if r.returncode: raise RuntimeError(r.stderr.strip())
        rr, ss = utils.decode_dss_signature(open(sigf, "rb").read())
    return gen.openpgp_v4_sig_packet(hashed, gen._subpacket(16, fpr[-8:]), gen.openpgp_v4_sig_digest(doc, hashed)[:2], rr, ss)

def capture():
    os.makedirs(OUT, exist_ok=True)
    kid = K.key_id()
    spki = base64.b64decode(K.aws("kms", "get-public-key", "--key-id", kid)["PublicKey"])
    old = json.load(open(os.path.join(HERE, "out-kms", "capture.json")))
    assert spki == base64.b64decode(old["spki_b64"]), "KMS key changed since the 2026-10-13 capture"
    pk = gen.decode_spki_mldsa65(spki)                                  # KEY_FORMAT gate
    g = json.load(open(os.path.join(HERE, "out-gcp", "capture.json")))
    gpub = serialization.load_pem_public_key(g["spki_pem"].encode()).public_numbers()
    pt = gen._point(gpub.x, gpub.y)
    fr = frames(spki, g["key_fp"])
    rec = {"alg": gen.ALG_HYBRID, "kms_key_id": kid, "spki_b64": base64.b64encode(spki).decode(),
           "gpg": {"x": f"{gpub.x:064x}", "y": f"{gpub.y:064x}", "created": g["key_created"]},
           "manifest_hex": fr["manifest"].hex()}
    for name, mode in (("small", "RAW"), ("big", "EXTERNAL_MU")):
        f0, f1 = fr[name]
        msg = f0 if mode == "RAW" else gen.mldsa65_external_mu(pk, f0)
        s0, s1 = K.kms_sign(kid, msg, mode), gcp_rule_o(f1, pt, g["key_created"])
        rec[name] = {"mode": mode, "f0_hex": f0.hex(), "s0_hex": s0.hex(), "f1_hex": f1.hex(), "s1_hex": s1.hex(),
                     "anchor_hex": gen.encode_anchor(f0, s0, f1, s1).hex()}
    rec["possession"] = {"kms_hex": K.kms_sign(kid, fr["manifest"], "RAW").hex(),
                         "gpg_hex": gcp_rule_o(fr["manifest"], pt, g["key_created"]).hex()}
    json.dump(rec, open(os.path.join(OUT, "capture.json"), "w"), indent=1)
    print("captured", kid, "and", "/".join(GKEY))

def verify():  # offline: reads only out-v1-hybrid/capture.json
    r = json.load(open(os.path.join(OUT, "capture.json")))
    hx = bytes.fromhex
    spki, fm = base64.b64decode(r["spki_b64"]), hx(r["manifest_hex"])
    pk = gen.decode_spki_mldsa65(spki)
    gq = (int(r["gpg"]["x"], 16), int(r["gpg"]["y"], 16), r["gpg"]["created"])
    pub = serialization.load_der_public_key(spki)
    def lib_ok(msg, sig):
        try: pub.verify(sig, msg); c = True
        except Exception: c = False
        return c and DPY.verify(pk, msg, sig, ctx=b"")
    res = {}
    for name in ("small", "big"):
        x = r[name]; a = [hx(x[k]) for k in ("f0_hex", "s0_hex", "f1_hex", "s1_hex", "anchor_hex")]
        res[f"{name} ({x['mode']}): A receipt"] = gen.check_receipt(fm, *a, (spki, gq)) is not None
        res[f"{name} ({x['mode']}): B receipt"] = check.receipt(fm, *a, (spki, gq[:2], gq[2])) is not None
        res[f"{name} ({x['mode']}): kms sig, cryptography + dilithium-py"] = lib_ok(a[0], a[1])
        res[f"{name}: frame length"] = len(a[0])
        res[f"{name}: anchor sha256"] = hashlib.sha256(a[4]).hexdigest()
    pk_, pg_ = hx(r["possession"]["kms_hex"]), hx(r["possession"]["gpg_hex"])
    res["possession kms: A"] = gen.check_possession(fm, 0, pk_, spki) is not None
    res["possession gpg: A"] = gen.check_possession(fm, 1, pg_, gq) is not None
    res["possession kms: B"] = check.possession(fm, 0, pk_, spki) is not None
    res["possession gpg: B"] = check.possession(fm, 1, pg_, gq) is not None
    res["possession kms: cryptography + dilithium-py"] = lib_ok(fm, pk_)
    for k, v in res.items(): print(f"{k}: {v}")
    ok = all(v for v in res.values() if isinstance(v, bool))
    print("PASS" if ok else "FAIL"); return ok

if __name__ == "__main__":
    if "verify" not in sys.argv[1:]: capture()
    sys.exit(0 if verify() else 1)
