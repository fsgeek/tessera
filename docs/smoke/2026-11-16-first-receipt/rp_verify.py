"""Relying-party verification of the first production receipt (owner, 2026-11-16).
Trust: the production window's entries (DNS root KSKs, the repository root) plus pins of the bundle's Bitcoin
headers fetched from two explorers that must agree. Verifier: service/verifier CLI under a TEST release (the
production release, YubiKey B, does not exist yet)."""
import hashlib, json, subprocess, sys, urllib.request
from pathlib import Path
R = Path("/home/tony/projects/tessera")
sys.path.insert(0, str(R / "service/issuer")); sys.path.insert(0, str(R / "service/issuer/tests")); sys.path.insert(0, str(R / "service/verifier"))
from tessera_issue import stand_in, window as W, freeze
from tessera_issue.testkeys import P256Key
from tessera_issue.util import rfc3339
import time

S = Path(sys.argv[1]); bundle = (S / "receipt.json").read_bytes()
win = W.load_json((R / "service/issuer/config/window.json").read_text())
heights = [int(h) for h in json.loads(bundle)["layers"][0]["headers"]]
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "tessera-rp-check"}), timeout=30).read().decode().strip()
hdrs = {}
for h in heights:
    got = []
    for api in ("https://blockstream.info/api", "https://mempool.space/api"):
        bh = get(f"{api}/block-height/{h}"); got.append(bytes.fromhex(get(f"{api}/block/{bh}/header")))
    assert got[0] == got[1], f"explorers disagree at {h}"
    hdrs[h] = got[0]
print("headers", sorted(hdrs), "both explorers agree")
trust = stand_in.relying_party_trust(win, hdrs, rfc3339(int(time.time())))
frozen = freeze.load(R / "formal/freeze-v1/objects")
rel, key = stand_in.make_test_release(trust, frozen.catalog, P256Key("smoke-test relying-party release key"))
for n, d in (("trust.json", trust), ("release.json", rel), ("release-key.json", key)): (S / n).write_bytes(d)
cli = R / "service/verifier/.venv/bin/tessera-verify"
p = subprocess.run([str(cli), "--mode", "test", "--test-release", str(S / "release.json"), "--test-release-key",
                    str(S / "release-key.json"), "--trust", str(S / "trust.json"), "--bundle", str(S / "receipt.json")],
                   capture_output=True, text=True, timeout=600)
(S / "verify-report.json").write_text(p.stdout)
rep = json.loads(p.stdout) if p.stdout.strip() else {}
print("exit", p.returncode, "verdict", rep.get("stable", {}).get("verdict"), p.stderr[-500:])
