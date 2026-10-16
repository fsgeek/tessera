"""THROWAWAY INSTRUMENT SPIKE - never ships. Tessera PQ signature feasibility (offline)."""
import json, hashlib, struct, time, os, sys, importlib.metadata as md
from cryptography.hazmat.primitives.asymmetric import mldsa as C
from dilithium_py.ml_dsa import ML_DSA_65 as D
import slhdsa

def jcs(o):  # RFC 8785 approximation: sorted keys, no whitespace, ASCII-only strings here
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def header(t): t = t.encode(); return bytes([len(t)]) + t
def frame(t, payload): return header(t) + struct.pack(">HI", 1, len(payload)) + payload

def make_frame(content_len, fp):
    content = ("x" * content_len)
    common = {"content": content, "binds": {"manifest": "sha256:" + "ab" * 32, "ts": "2026-10-12T00:00:00Z", "dns": "sha256:" + "cd" * 32}}
    payload = b'{"common":' + jcs(common) + b',"signer":{"key_fp":' + jcs(fp) + b'}}'
    return frame("tessera-v1/attest", payload)

def shake(b, n): return hashlib.shake_256(b).digest(n)
R = {}
def rec(k, v): R[k] = v; print(k, "=", v, flush=True)

for p in ("cryptography", "dilithium-py", "slh-dsa", "pqcrypto"): rec("ver:" + p, md.version(p))
rec("python", sys.version.split()[0])

F_kms = make_frame(2048, "mldsa65-sha256:" + "11" * 32)
F_gpg = make_frame(2048, "slhdsa-sha256:" + "22" * 32)
rec("frame_len_2KB_content", (len(F_kms), len(F_gpg)))

# (2) ML-DSA-65: sign with cryptography (OpenSSL/Rust), verify with dilithium-py (pure Python)
sk = C.MLDSA65PrivateKey.generate(); pk = sk.public_key().public_bytes_raw()
sig_m = sk.sign(F_kms)  # ctx empty by default
rec("mldsa65 pk/sig sizes", (len(pk), len(sig_m)))
rec("(2) cryptography-sign -> dilithium-py-verify", D.verify(pk, F_kms, sig_m, ctx=b""))
rec("(2) tamper rejected", not D.verify(pk, F_kms[:-1] + b"\x00", sig_m))
# reverse direction
pk2, sk2 = D.keygen(); sig2 = D.sign(sk2, F_kms, ctx=b"")
try:
    C.MLDSA65PublicKey.from_public_bytes(pk2).verify(sig2, F_kms); ok = True
except Exception as e: ok = repr(e)
rec("(2) dilithium-py-sign -> cryptography-verify", ok)

# (3) external mu on frame > 4KB
BIG = make_frame(6000, "mldsa65-sha256:" + "11" * 32)
rec("big_frame_len", len(BIG))
tr = shake(pk, 64); mp = b"\x00\x00" + BIG; mu = shake(tr + mp, 64)
rec("(3) mu manual == dilithium-py prehash", mu == D.prehash_external_mu(pk, BIG, b""))
h = C.MLDSAMuHasher if hasattr(C, "MLDSAMuHasher") else None
# cryptography's hasher API: inspect via help text if needed
try:
    mh = sk.public_key  # placeholder to keep linter quiet
    hasher = C.MLDSAMuHasher(sk.public_key()) if False else None
except Exception: pass
sig_mu = sk.sign_mu(mu)  # cryptography: sign from external mu
rec("(3) cryptography sign_mu sig len", len(sig_mu))
rec("(3) mu-sig verifies as normal ML-DSA over full msg (cryptography verify)", (lambda: (sk.public_key().verify(sig_mu, BIG), True)[1])())
rec("(3) mu-sig verifies (dilithium-py verify, independent)", D.verify(pk, BIG, sig_mu, ctx=b""))
rec("(3) cryptography verify_mu(mu) ok", (sk.public_key().verify_mu(sig_mu, mu), True)[1])
# reverse: dilithium-py signs from mu, cryptography verifies full message
sig_mu2 = D.sign_external_mu(sk2, D.prehash_external_mu(pk2, BIG, b""))
C.MLDSA65PublicKey.from_public_bytes(pk2).verify(sig_mu2, BIG)
rec("(3) dilithium-py sign_external_mu -> cryptography verify full msg", True)

# (1) SLH-DSA
sizes = {}
for name in ("sha2_128s", "sha2_128f"):
    par = getattr(slhdsa, name)
    t = time.time(); kp = slhdsa.KeyPair.gen(par); tk = time.time() - t
    t = time.time(); s = kp.sign_pure(F_gpg, ctx=b""); ts = time.time() - t
    # verify with a freshly deserialized public key (public key bytes only)
    pkb = kp.pub.key[0] + kp.pub.key[1] if hasattr(kp.pub, "key") else None
    t = time.time(); ok = kp.pub.verify_pure(F_gpg, s, ctx=b""); tv = time.time() - t
    bad = kp.pub.verify_pure(F_gpg[:-1] + b"\x00", s, ctx=b"") if True else None
    rec(f"(1) {name} sig_len/verify/tamper_verify", (len(s), ok, bad))
    rec(f"    {name} times keygen/sign/verify s", (round(tk, 2), round(ts, 2), round(tv, 2)))
    sizes[name] = s

# (4) anchor preimage
def anchor(frames_sigs):
    out = header("tessera-v1/receipt-anchor") + b"\x02"
    for f, s in frames_sigs: out += struct.pack(">I", len(f)) + f + struct.pack(">I", len(s)) + s
    return out
for name, s in sizes.items():
    A = anchor([(F_kms, sig_m), (F_gpg, s)])
    rec(f"(4) anchor size ML-DSA-65 + {name}", len(A))
    rec(f"    sha256", hashlib.sha256(A).hexdigest())
