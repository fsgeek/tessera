# Slot-2 policy signer test client (instrument code under A9.2; never ships). It plays the AWS-side issuer:
# it holds only the tessera AWS profile, enqueues frames on SQS tessera-slot2-requests and waits for the
# response on tessera-slot2-responses. It holds no GCP credential and never calls the GCP key.
#
# Run from the repo root with prototype/.venv (rfc8785, cryptography, dilithium-py):
#   prototype/.venv/bin/python prototype/policy-signer/client.py send FRAME_FILE     # any bytes; prints the response
#   prototype/.venv/bin/python prototype/policy-signer/client.py evidence [a|b|c|all] # DESIGN.md evidence (a)-(c)
#   prototype/.venv/bin/python prototype/policy-signer/client.py verify-a            # offline re-check of (a)
#
# (a) builds genuine V1 hybrid frames the way prototype/spike-pq/spike_v1_hybrid.py does (declared time = now):
# the manifest and one attestation pair under the pair id. Slot kms is signed by AWS KMS ML-DSA-65
# (alias/tessera-pq-spike, EXTERNAL_MU, owner decision 6); slot gpg and the gpg manifest-possession signature come
# ONLY from the policy signer, through the queue. Then it builds A_sig and verifies offline in P8 implementation A
# (gen.py) and implementation B (check.py).
import base64, datetime, hashlib, json, os, subprocess, sys, tempfile, time, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "formal", "p8", "vectors"))
import gen, check                                   # P8 implementations A and B
from cryptography.hazmat.primitives import serialization
from dilithium_py.ml_dsa import ML_DSA_65 as DPY

AWS = [os.path.expanduser("~/.local/bin/aws"), "--profile", "tessera", "--region", "us-east-2", "--output", "json"]
Q = "https://sqs.us-east-2.amazonaws.com/477139661040/"
REQ, RESP = Q + "tessera-slot2-requests", Q + "tessera-slot2-responses"
KMS_ALIAS = "alias/tessera-pq-spike"
OUT = os.path.join(HERE, "out")
D = "wamason.com"
GCP_CAPTURE = os.path.join(ROOT, "prototype", "spike-pq", "out-gcp", "capture.json")   # slot-2 public key (public data)

def aws(*args):
    r = subprocess.run([*AWS, *args], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout) if r.stdout.strip() else {}

# ---- queue path -----------------------------------------------------------------------------------------------
def enqueue(frame, request_id=None):
    rid = request_id or "req-" + uuid.uuid4().hex
    body = json.dumps({"request_id": rid, "frame_b64": base64.b64encode(frame).decode()})
    with tempfile.NamedTemporaryFile("w", delete=False) as f: f.write(body); p = f.name
    try: mid = aws("sqs", "send-message", "--queue-url", REQ, "--message-body", f"file://{p}")["MessageId"]
    finally: os.unlink(p)
    return rid, mid

def wait(rid, timeout=240):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for m in aws("sqs", "receive-message", "--queue-url", RESP, "--max-number-of-messages", "10",
                     "--wait-time-seconds", "20", "--visibility-timeout", "5").get("Messages", []):
            r = json.loads(m["Body"])
            if r.get("request_id") == rid:
                aws("sqs", "delete-message", "--queue-url", RESP, "--receipt-handle", m["ReceiptHandle"])
                r["_waited_s"] = round(time.time() - t0, 1)
                return r
    raise TimeoutError(f"no response for {rid} in {timeout} s")

def submit(frame, label):
    rid, mid = enqueue(frame)
    print(f"[{label}] enqueued {rid} (sqs {mid}), frame {len(frame)} B sha256 {hashlib.sha256(frame).hexdigest()[:16]}...",
          flush=True)
    r = wait(rid)
    print(f"[{label}] {r['status']} {r.get('reason') or ''} after {r['_waited_s']} s; signer clock {r['signer']['clock']}",
          flush=True)
    return rid, mid, r

# ---- genuine V1 hybrid frames (as spike_v1_hybrid.frames) -----------------------------------------------------
def kms_key():
    kid = aws("kms", "describe-key", "--key-id", KMS_ALIAS)["KeyMetadata"]["KeyId"]   # never creates
    return kid, base64.b64decode(aws("kms", "get-public-key", "--key-id", kid)["PublicKey"])

def gpg_key():
    g = json.load(open(GCP_CAPTURE))
    n = serialization.load_pem_public_key(g["spki_pem"].encode()).public_numbers()
    assert gen.fp_gpg(gen._point(n.x, n.y), g["key_created"]) == g["key_fp"]
    return (n.x, n.y, g["key_created"]), g["key_fp"]

def build(kms_spki, gpg_fp, when, label):
    fm = gen.encode_manifest(gen.ALG_HYBRID, D, gen.fp_spki(kms_spki), gpg_fp)
    common = {"alg": gen.ALG_HYBRID, "binding_forms": ["STMT_DIRECT"],
              "content": {"statement": "slot2-policy-signer-evidence", "case": label},
              "declared_issue_time": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
              "issuer": D, "manifest_sha256": hashlib.sha256(fm).hexdigest(),
              "preamble_sha256": hashlib.sha256(b"ILLUSTRATIVE: purpose preamble bytes\n").hexdigest(),
              "profile": gen.PROFILE,
              "spec": {"id": "tessera-v1-strict/verification-spec/1",
                       "sha256": hashlib.sha256(b"ILLUSTRATIVE: tessera-v1-strict verification specification bytes\n").hexdigest()},
              "vectors_sha256": hashlib.sha256(b"ILLUSTRATIVE: tessera-v1-strict conformance vector bytes\n").hexdigest()}
    return fm, gen.encode_attest(common, gen.fp_spki(kms_spki)), gen.encode_attest(common, gpg_fp)

def kms_sign_mu(kid, pk, frame):
    mu = gen.mldsa65_external_mu(pk, frame)
    with tempfile.NamedTemporaryFile(delete=False) as f: f.write(mu); p = f.name
    try:
        return base64.b64decode(aws("kms", "sign", "--key-id", kid, "--message", f"fileb://{p}", "--message-type",
                                    "EXTERNAL_MU", "--signing-algorithm", "ML_DSA_SHAKE_256")["Signature"])
    finally: os.unlink(p)

def now():
    return datetime.datetime.now(datetime.timezone.utc)

# ---- evidence -----------------------------------------------------------------------------------------------
def evidence_a():
    kid, spki = kms_key(); pk = gen.decode_spki_mldsa65(spki)
    gq, gfp = gpg_key()
    fm, f0, f1 = build(spki, gfp, now(), "a-valid")
    s0 = kms_sign_mu(kid, pk, f0)
    rid, mid, r = submit(f1, "a: attest frame, declared time now")
    assert r["status"] == "SIGNED", r
    s1 = base64.b64decode(r["sig_b64"])
    pid, pmid, pr = submit(fm, "a: manifest (possession)")
    assert pr["status"] == "SIGNED", pr
    rec = {"captured": now().strftime("%Y-%m-%dT%H:%M:%SZ"), "kms_key_id": kid,
           "spki_b64": base64.b64encode(spki).decode(),
           "gpg": {"x": f"{gq[0]:064x}", "y": f"{gq[1]:064x}", "created": gq[2], "key_fp": gfp},
           "manifest_hex": fm.hex(), "f0_hex": f0.hex(), "s0_hex": s0.hex(), "f1_hex": f1.hex(), "s1_hex": s1.hex(),
           "anchor_hex": gen.encode_anchor(f0, s0, f1, s1).hex(),
           "possession_kms_hex": kms_sign_mu(kid, pk, fm).hex(), "possession_gpg_hex": base64.b64decode(pr["sig_b64"]).hex(),
           "attest_request": {"request_id": rid, "sqs_message_id": mid}, "attest_response": r,
           "manifest_request": {"request_id": pid, "sqs_message_id": pmid}, "manifest_response": pr}
    os.makedirs(OUT, exist_ok=True)
    json.dump(rec, open(os.path.join(OUT, "evidence-a.json"), "w"), indent=1)
    return verify_a()

def verify_a():     # offline: reads only out/evidence-a.json
    r = json.load(open(os.path.join(OUT, "evidence-a.json"))); hx = bytes.fromhex
    spki, fm = base64.b64decode(r["spki_b64"]), hx(r["manifest_hex"])
    f0, s0, f1, s1, an = (hx(r[k]) for k in ("f0_hex", "s0_hex", "f1_hex", "s1_hex", "anchor_hex"))
    pk = gen.decode_spki_mldsa65(spki)
    gx, gy, gc = int(r["gpg"]["x"], 16), int(r["gpg"]["y"], 16), r["gpg"]["created"]
    pg, pkms = hx(r["possession_gpg_hex"]), hx(r["possession_kms_hex"])
    pub = serialization.load_der_public_key(spki)
    def mldsa_libs(msg, sig):
        try: pub.verify(sig, msg); c = True
        except Exception: c = False
        return c and DPY.verify(pk, msg, sig, ctx=b"")
    def rejects(fn):
        try: fn(); return False
        except (gen.Reject, check.Bad): return True
    t1 = f1[:-2] + bytes([f1[-2] ^ 1]) + f1[-1:]
    res = {
        "slot-2 sig: P8 A rule-O codec (gen.decode_sig, slot gpg)": not rejects(lambda: gen.decode_sig(s1, gen.ALG_HYBRID, 1)),
        "slot-2 sig: P8 B rule-O codec (check.sig_check, slot gpg)": not rejects(lambda: check.sig_check(s1, check.HYB_ALG, 1)),
        "slot-2 sig: A ECDSA verify over its frame (gen.verify_openpgp4)": gen.verify_openpgp4(f1, s1, (gx, gy)),
        "slot-2 sig: B ECDSA verify over its frame (check.pgp4_verify)": check.pgp4_verify(f1, s1, (gx, gy)),
        "slot-2 sig: tampered frame rejected by A and B": not gen.verify_openpgp4(t1, s1, (gx, gy))
                                                           and not check.pgp4_verify(t1, s1, (gx, gy)),
        "receipt (manifest, both frames, both sigs, A_sig): A accepts with keys": gen.check_receipt(fm, f0, s0, f1, s1, an, (spki, (gx, gy, gc))) is not None,
        "receipt: B accepts with keys": check.receipt(fm, f0, s0, f1, s1, an, (spki, (gx, gy), gc)) is not None,
        "receipt with slot-2 sig swapped for the possession sig: A and B reject": rejects(lambda: gen.check_receipt(
            fm, f0, s0, f1, pg, gen.encode_anchor(f0, s0, f1, pg), (spki, (gx, gy, gc)))) and rejects(lambda: check.receipt(
            fm, f0, s0, f1, pg, gen.encode_anchor(f0, s0, f1, pg), (spki, (gx, gy), gc))),
        "kms sig (EXTERNAL_MU) verifies over the full frame: cryptography + dilithium-py": mldsa_libs(f0, s0),
        "possession gpg (via signer): A": gen.check_possession(fm, 1, pg, (gx, gy, gc)) is not None,
        "possession gpg (via signer): B": check.possession(fm, 1, pg, (gx, gy, gc)) is not None,
        "possession kms: A and B": gen.check_possession(fm, 0, pkms, spki) is not None
                                   and check.possession(fm, 0, pkms, spki) is not None,
        "declared_issue_time": gen.decode_frame(f1, gen.T_ATTEST)["common"]["declared_issue_time"],
        "signer clock at signing": r["attest_response"]["signer"]["clock"],
        "frame f1 length / sha256": f"{len(f1)} / {hashlib.sha256(f1).hexdigest()}",
        "slot-2 sig length / sha256": f"{len(s1)} / {hashlib.sha256(s1).hexdigest()}",
        "anchor sha256": hashlib.sha256(an).hexdigest(),
    }
    for k, v in res.items(): print(f"  {k}: {v}")
    ok = all(v for v in res.values() if isinstance(v, bool))
    print("  (a)", "PASS" if ok else "FAIL"); return ok

def refusal(label, frame, want):
    rid, mid, r = submit(frame, label)
    ok = r["status"] == "REFUSED" and r.get("reason") == want and "sig_b64" not in r
    print(f"  expected REFUSED/{want}: {'PASS' if ok else 'FAIL'}; detail: {r.get('detail')}")
    return ok, {"label": label, "request_id": rid, "sqs_message_id": mid, "frame_hex": frame.hex(), "response": r}

def evidence_b():
    _, spki = kms_key(); _, gfp = gpg_key()
    _, _, f1 = build(spki, gfp, now() - datetime.timedelta(hours=25), "b-stale-25h")
    ok, rec = refusal("b: declared time 25 h in the past", f1, "DECLARED_TIME_OUTSIDE_EPSILON")
    json.dump(rec, open(os.path.join(OUT, "evidence-b.json"), "w"), indent=1)
    print("  (b)", "PASS" if ok else "FAIL"); return ok

def evidence_c():
    _, spki = kms_key(); _, gfp = gpg_key()
    _, f0, f1 = build(spki, gfp, now(), "c-wrong")
    wrong_tag = gen.header(b"tessera-v1/receipt") + f1[1 + f1[0]:]   # the withdrawn toy tag, not in T
    anchor_tag = gen.header(gen.T_ANCHOR) + f1[1 + f1[0]:]           # in T, but not a slot-2 document
    recs, oks = [], []
    for label, fr, want in (("c1: wrong tag tessera-v1/receipt (not in T)", wrong_tag, "TAG_UNKNOWN"),
                            ("c2: tag tessera-v1/receipt-anchor-sig (in T, not signable)", anchor_tag, "TAG_MISMATCH"),
                            ("c3: wrong key_fp (the kms slot's fingerprint)", f0, "KEY_FP_MISMATCH")):
        ok, rec = refusal(label, fr, want); oks.append(ok); recs.append(rec)
    json.dump(recs, open(os.path.join(OUT, "evidence-c.json"), "w"), indent=1)
    print("  (c)", "PASS" if all(oks) else "FAIL"); return all(oks)

if __name__ == "__main__":
    a = sys.argv[1:] or ["evidence", "all"]
    os.makedirs(OUT, exist_ok=True)
    if a[0] == "send":
        rid, mid, r = submit(open(a[1], "rb").read(), "send"); print(json.dumps(r, indent=1)); sys.exit(0)
    if a[0] == "verify-a":
        sys.exit(0 if verify_a() else 1)
    which = (a[1] if len(a) > 1 else "all")
    steps = {"a": evidence_a, "b": evidence_b, "c": evidence_c}
    results = [steps[k]() for k in (steps if which == "all" else which)]
    sys.exit(0 if all(results) else 1)
