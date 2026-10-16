"""THROWAWAY spike step 1: sign a small frame with real keys (KMS-style ECDSA P-256 OpenPGP slot + real gpg),
write the receipt bundle and the anchor preimage file. Network: none here (anchoring is a separate `ots stamp`)."""
import base64, hashlib, json, os, sys, time
from pathlib import Path
os.environ["TESSERA_PROTO_MODE"] = "real"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tessera_proto import jcs, objects
from tessera_proto.crypto import b64d
from tessera_proto.issuer import build_attest_layer
from tessera_proto.real import world as rw

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)
w = rw.make_world_real("wamason.com")
declared = int(time.time())
content = jcs.parse_strict(json.dumps({"spike": "tessera-v1-real-world-spike", "note": "test frame", "n": "1"}).encode())
layer = build_attest_layer(object_type="OT_ATTEST", content=content, declared=declared, issuer_id="wamason.com",
                           slot_keys=[w.skI, w.skB2], channels=[], binding_forms=("STMT_DIGEST",), alg=w.skI.alg)
fbs = [b64d(s["frame_b64"]) for s in layer["slots"]]
acc = b"".join(len(f).to_bytes(4, "big") + f for f in fbs)
pre = b"tessera/v0/receipt-digest\x00" + acc
assert hashlib.sha256(pre).hexdigest() == objects.receipt_digest(fbs)
(OUT / "receipt-preimage.bin").write_bytes(pre)
bundle = {"bundle_format": "tessera-spike-bundle/0", "declared": declared, "layer": layer,
          "receipt_digest": objects.receipt_digest(fbs), "preimage_file": "receipt-preimage.bin",
          "gpg_fpr_openpgp": w.skB2.fpr, "issuance_wall_clock": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
(OUT / "receipt.json").write_text(json.dumps(bundle, indent=1))
print("declared", declared, "digest", bundle["receipt_digest"], "preimage bytes", len(pre))
rw.close()
