#!/usr/bin/env python3
"""The window's git key assertion (V1-PROFILE §6.3, §15.4), signed offline by the repository root (YubiKey A).

  build     NUC: the 255-byte value, blob, trees and the UNSIGNED commit (exactly the bytes the root signs).
  assemble  NUC: insert the detached signature as the commit's gpgsig header and check the result with the
            verifier's own code (path, rule-O signature, root key). Writes the signed commit and its id.

No git binary is used: objects are built byte for byte as git would, so the root signs on Tails with gpg alone
(docs/ceremony/sign-assertion.sh). The value is also written into the commit message, so the signer can read the
fingerprints and dates and the signing script can recompute the tree from them.

  python3 key_assertion.py build --not-before 2026-11-16T00:00:00Z --not-after 2027-02-01T00:00:00Z --out DIR
  python3 key_assertion.py assemble --out DIR --sig DIR/payload.sig.asc --root-pub ROOT.pub.asc
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))                  # tessera_issue
sys.path.insert(0, str(HERE.parents[2] / "verifier"))     # tessera_verify
from tessera_issue.encode import assertion_value          # noqa: E402

# The window's service keys (service/issuer/DEPLOY-RUN.md, 2026-10-30 production keys).
KMS_FP = "spki-sha256:a33c216e4151f7202b4863f9edebf060b374ee1bb91ff9ca5734b8e7ba75679f"
GPG_FP = "gpg-sha256:6a2d7e757b99b46e469dd81f293387b7cfdbe3a1cab2b614dd2d26ecc79dda59"
IDENT = b"Tessera repository root <tessera@wamason.com>"
ROOT_FPR = "6BDA21559F18D5DB8E1312C363210B5FF92AD30A"   # docs/ceremony/2026-11-10-operator-data.md (CA-02)


def oid(kind, body):
    return hashlib.sha1(kind.encode() + b" " + str(len(body)).encode() + b"\x00" + body).digest()


def objects(value):
    blob = value
    sub = b"100644 key-assertion\x00" + oid("blob", blob)
    root = b"40000 tessera-v1\x00" + oid("tree", sub)
    return blob, sub, root


def build(a):
    value = assertion_value(KMS_FP, GPG_FP, a.not_before, a.not_after)
    blob, sub, root = objects(value)
    when = int(datetime.now(timezone.utc).timestamp())
    payload = (b"tree " + oid("tree", root).hex().encode() + b"\n"
               + b"author " + IDENT + b" %d +0000\n" % when
               + b"committer " + IDENT + b" %d +0000\n" % when
               + b"\nTessera V1 key assertion\n\n" + value + b"\n")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for name, data in (("value.txt", value), ("blob.bin", blob), ("tree-sub.bin", sub), ("tree-root.bin", root),
                       ("payload.txt", payload)):
        (out / name).write_bytes(data)
    rec = {"kms_fp": KMS_FP, "gpg_fp": GPG_FP, "not_before": a.not_before, "not_after": a.not_after,
           "tree": oid("tree", root).hex(),
           "sha256": {n: hashlib.sha256((out / n).read_bytes()).hexdigest()
                      for n in ("value.txt", "blob.bin", "tree-sub.bin", "tree-root.bin", "payload.txt")}}
    (out / "build.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(payload.decode())
    print("payload.txt sha256", rec["sha256"]["payload.txt"])


def assemble(a):
    from tessera_verify.codec import public_key, signature_verifies
    from tessera_verify.git_channel import dearmor, object_id, parse_commit, verify_path
    from tessera_verify import sha1dc
    out = Path(a.out)
    payload = (out / "payload.txt").read_bytes()
    armor = Path(a.sig).read_bytes().replace(b"\r\n", b"\n").rstrip(b"\n").split(b"\n")
    head, _, message = payload.partition(b"\n\n")
    signed = head + b"\ngpgsig " + b"\n ".join(armor) + b"\n\n" + message
    tree, payload_back, armor_back = parse_commit(signed)
    if payload_back != payload:
        sys.exit("FAIL: the signed commit's payload is not the unsigned payload")
    sig = dearmor(armor_back)
    pub = Path(a.root_pub).read_bytes()
    import base64
    lines = [ln for ln in pub.decode().splitlines() if ln and not ln.startswith(("-----", "=")) and ":" not in ln]
    raw = base64.b64decode("".join(lines))
    if raw[0] != 0x98:
        sys.exit("FAIL: unexpected public-key packet header")
    body = raw[2:2 + raw[1]]
    if not signature_verifies(payload, sig, public_key(body, "gpg")):
        sys.exit("FAIL: the signature does not verify over the payload under the root key")
    fpr = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).hexdigest().upper()
    if fpr != ROOT_FPR:
        sys.exit(f"FAIL: the supplied key {fpr} is not the repository root {ROOT_FPR}")
    root, sub, blob = ((out / n).read_bytes() for n in ("tree-root.bin", "tree-sub.bin", "blob.bin"))
    verify_path(tree, (root, sub), blob)
    inst = json.loads((HERE.parents[2] / "verifier" / "install.json").read_text())
    sha1dc.configure(inst["sha1dc_binary"], inst["sha1dc_binary_sha256"])   # the verifier's pinned install
    if not sha1dc.available():            # CA-03: the profile's pinned SHA-1 collision detector (§15.4 "Ids")
        sys.exit("FAIL: SHA-1DC detector unavailable (service/verifier/install.sh)")
    for kind, obj in (("commit", signed), ("tree", root), ("tree", sub), ("blob", blob)):
        if sha1dc.collision(kind, obj):
            sys.exit(f"FAIL: SHA-1DC reports a collision pattern in the {kind} object")
    cid = object_id("commit", signed)
    (out / "commit.bin").write_bytes(signed)
    (out / "git-stamp.txt").write_bytes((cid + "\n").encode())
    print(f"PASS: commit {cid} signed by the repository root {fpr}; path and signature checked by the verifier's code")


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    b = s.add_parser("build"); b.add_argument("--not-before", required=True); b.add_argument("--not-after", required=True)
    b.add_argument("--out", required=True)
    m = s.add_parser("assemble"); m.add_argument("--out", required=True); m.add_argument("--sig", required=True)
    m.add_argument("--root-pub", required=True)
    a = p.parse_args()
    {"build": build, "assemble": assemble}[a.cmd](a)


if __name__ == "__main__":
    main()
