# Archive record for the genuine V1 hybrid capture (supplement HS-01). OFFLINE: reads only capture.json here.
# Writes evidence.json (the exact objects, keys, signatures, lengths, mu, hashes, tool versions) and verify-ab.log
# (implementation A and implementation B, each on its own, plus cryptography and dilithium-py).
# Run from the repo root: prototype/.venv/bin/python formal/p8/evidence/v1-hybrid-2026-10-14/derive.py
# evidence.json as archived records capture_instrument_sha256 = c06cae46...c6da, the instrument AS RUN (03:23Z).
# A comment was added to the instrument afterwards (HS-05 labelling), so a rerun records the newer file hash.
import base64, hashlib, importlib.metadata as md, json, os, platform, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "formal", "p8", "vectors"))
import gen, check
from cryptography.hazmat.primitives import serialization
from dilithium_py.ml_dsa import ML_DSA_65 as DPY

raw = open(os.path.join(HERE, "capture.json"), "rb").read()
cap = json.loads(raw)
hx, sha = bytes.fromhex, (lambda b: hashlib.sha256(b).hexdigest())
spki = base64.b64decode(cap["spki_b64"])
pk = gen.decode_spki_mldsa65(spki)
gk = (int(cap["gpg"]["x"], 16), int(cap["gpg"]["y"], 16), cap["gpg"]["created"])
fm = hx(cap["manifest_hex"])
log = []

def rec(label, ok):
    log.append(f"{label}: {'PASS' if ok else 'FAIL'}")
    return ok

def run(label, fn):
    try:
        fn(); return rec(label, True)
    except Exception as e:                       # gen.Reject / check.Bad carry the reason code
        log.append(f"{label}: FAIL {getattr(e, 'code', e)!r}"); return False

pub = serialization.load_der_public_key(spki)
def libs(msg, sig):
    try: pub.verify(sig, msg); c = True
    except Exception: c = False
    return c and DPY.verify(pk, msg, sig, ctx=b"")

ev = {"source": "prototype/spike-pq/out-v1-hybrid/capture.json (owner run of spike_v1_hybrid.py, 2026-10-14 ~03:23Z)",
      "capture_sha256": sha(raw), "alg": cap["alg"], "kms_key_id": cap["kms_key_id"],
      "keys": {"kms_spki_der_hex": spki.hex(), "kms_key_fp": gen.fp_spki(spki),
               "gpg": cap["gpg"], "gpg_key_fp": gen.fp_gpg(gen._point(*gk[:2]), gk[2])},
      "manifest": {"hex": fm.hex(), "length": len(fm), "sha256": sha(fm)}, "pairs": {}, "possession": {}}
ok = run("A manifest decodes", lambda: gen.decode_frame(fm, gen.T_MANIFEST))
ok &= run("B manifest decodes", lambda: check.frame_decode(fm, "manifest"))
for name in ("small", "big"):
    x = cap[name]
    f0, s0, f1, s1, a = (hx(x[k]) for k in ("f0_hex", "s0_hex", "f1_hex", "s1_hex", "anchor_hex"))
    p = {"kms_mode_at_capture": x["mode"] + (" (comparative; selected issuer path is EXTERNAL_MU)" if x["mode"] == "RAW" else " (selected issuer path)"),
         "f_kms": {"hex": f0.hex(), "length": len(f0), "sha256": sha(f0)}, "s_kms": {"hex": s0.hex(), "length": len(s0)},
         "f_gpg": {"hex": f1.hex(), "length": len(f1), "sha256": sha(f1)}, "s_gpg": {"hex": s1.hex(), "length": len(s1)},
         "a_sig": {"length": len(a), "sha256": sha(a)},
         "mu_external_hex": gen.mldsa65_external_mu(pk, f0).hex()}
    ev["pairs"][name] = p
    for lbl, f in (("kms", f0), ("gpg", f1)):
        ok &= run(f"A {name} {lbl} frame decodes as attest ({len(f)} B)", lambda f=f: gen.decode_frame(f, gen.T_ATTEST))
        ok &= run(f"B {name} {lbl} frame decodes as attest ({len(f)} B)", lambda f=f: check.frame_decode(f, "attest"))
    ok &= rec(f"A {name} kms ML-DSA-65 verifies over its exact frame", gen.mldsa65_verify(pk, f0, s0))
    ok &= rec(f"B {name} kms ML-DSA-65 verifies over its exact frame", check.mldsa65_ok(check.mldsa_spki(spki), f0, s0))
    ok &= rec(f"cryptography + dilithium-py {name} kms", libs(f0, s0))
    ok &= rec(f"A {name} mu equals SHAKE256(SHAKE256(pk,64)||00 00||F,64) recomputed by B-style hashing",
              hashlib.shake_256(hashlib.shake_256(pk).digest(64) + b"\x00\x00" + f0).digest(64).hex() == p["mu_external_hex"])
    ok &= run(f"A {name} receipt (codec + both signatures)", lambda: gen.check_receipt(fm, f0, s0, f1, s1, a, (spki, gk)))
    ok &= run(f"B {name} receipt (codec + both signatures)", lambda: check.receipt(fm, f0, s0, f1, s1, a, (spki, gk[:2], gk[2])))
for slot, key in ((0, "kms_hex"), (1, "gpg_hex")):
    sg = hx(cap["possession"][key])
    ev["possession"][["kms", "gpg"][slot]] = {"hex": sg.hex(), "length": len(sg),
                                             "note": "KMS RAW: comparative" if slot == 0 else "GCP HSM, instrument-direct"}
    k = spki if slot == 0 else gk
    ok &= run(f"A possession {['kms', 'gpg'][slot]}", lambda: gen.check_possession(fm, slot, sg, k))
    ok &= run(f"B possession {['kms', 'gpg'][slot]}", lambda: check.possession(fm, slot, sg, k))
ok &= rec("cryptography + dilithium-py possession kms", libs(fm, hx(cap["possession"]["kms_hex"])))
ev["tools"] = {"python": platform.python_version(), "cryptography": md.version("cryptography"),
               "dilithium-py": md.version("dilithium-py"), "rfc8785": md.version("rfc8785"),
               "gen.py_sha256": sha(open(gen.__file__, "rb").read()), "check.py_sha256": sha(open(check.__file__, "rb").read()),
               "capture_instrument_sha256": sha(open(os.path.join(ROOT, "prototype/spike-pq/spike_v1_hybrid.py"), "rb").read())}
ev["result"] = "PASS" if ok else "FAIL"
json.dump(ev, open(os.path.join(HERE, "evidence.json"), "w"), indent=1)
open(os.path.join(HERE, "verify-ab.log"), "w").write("\n".join(log + [ev["result"]]) + "\n")
print("\n".join(log + [ev["result"]]))
sys.exit(0 if ok else 1)
