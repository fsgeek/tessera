#!/usr/bin/env python3
"""Build config/window.json for the issuer (DEPLOY.md step 9) and check it with the issuer's own loader.

Inputs: the signed key-assertion evidence (docs/ceremony/assertion/: commit.bin, tree-root.bin, tree-sub.bin,
blob.bin, git-stamp.txt.ots, value.txt), the two service public keys (KMS SPKI DER; the slot-2 P-256 PEM and its
createTime), the repository root's public key, and the DNS root KSK entries (config/root-ksks.json, exported as data
from the archived IANA sources in formal/trust-sources/).

  python3 build_window.py --kms-spki K.der --slot2-pem S.pem --slot2-created 1793390508 --out window.json
"""
import argparse
import base64
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(REPO / "service" / "verifier"))
sys.path.insert(0, str(REPO / "service" / "signer-gcp"))
from tessera_issue import window as window_mod                     # noqa: E402
from tessera_issue.util import sha256hex                           # noqa: E402
from tessera_signer import openpgp                                 # noqa: E402

A = REPO / "docs" / "ceremony" / "assertion"
ROOT_PUB = REPO / "docs" / "ceremony" / "keys" / "root-6BDA21559F18D5DB8E1312C363210B5FF92AD30A.pub.asc"
ROOT_CREATED = "2026-11-10T19:44:55Z"     # the root key's creation time (public-key packet, 1794337495)


def armored_body(path):
    lines = [ln for ln in path.read_text().splitlines() if ln and not ln.startswith(("-----", "=")) and ":" not in ln]
    raw = base64.b64decode("".join(lines))
    assert raw[0] == 0x98, "expected an old-format public-key packet"
    return raw[2:2 + raw[1]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kms-spki", required=True); p.add_argument("--slot2-pem", required=True)
    p.add_argument("--slot2-created", type=int, required=True); p.add_argument("--out", required=True)
    a = p.parse_args()
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    gpg_body = openpgp.key_body(openpgp.point65(load_pem_public_key(Path(a.slot2_pem).read_bytes())), a.slot2_created)
    root_body = armored_body(ROOT_PUB)
    b64 = lambda b: base64.b64encode(b).decode()
    value = (A / "value.txt").read_bytes()
    v = value.decode()
    nb = v.split("issuance-not-before=")[1].split(";")[0]
    na = v.split("issuance-not-after=")[1]
    trust_base = {
        "root_ksks": json.loads((HERE.parents[1] / "config" / "root-ksks.json").read_text()),
        "repository_keys": [{"domain": "wamason.com", "key": b64(root_body), "signing_end": None,
                             "signing_start": ROOT_CREATED,
                             "sources": [{"description": "Repository root, YubiKey A (serial 39975687), key ceremony "
                                                         "2026-11-10; fingerprint 6BDA21559F18D5DB8E1312C363210B5FF92AD30A",
                                          "sha256": sha256hex(root_body),
                                          "uri": "repo:docs/ceremony/keys/root-6BDA21559F18D5DB8E1312C363210B5FF92AD30A.pub.asc"}]}]}
    win = window_mod.Window(nb, na, Path(a.kms_spki).read_bytes(), gpg_body, value,
                            {"commit": (A / "commit.bin").read_bytes(),
                             "trees": [(A / "tree-root.bin").read_bytes(), (A / "tree-sub.bin").read_bytes()],
                             "blob": (A / "blob.bin").read_bytes(), "ots": (A / "git-stamp.txt.ots").read_bytes()},
                            trust_base).check()
    text = win.to_json()
    window_mod.load_json(text)                       # the issuer's own loader, exactly as the Lambda runs it
    Path(a.out).write_text(text)
    print(f"PASS: window {nb} .. {na}; kms {win.kms_fp}; gpg {win.gpg_fp}; git proof lowest height {win.h_git}")


if __name__ == "__main__":
    main()
