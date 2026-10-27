import json
import subprocess
from pathlib import Path

from tessera_issue import api, stand_in
from tessera_issue.testkeys import P256Key
from tessera_issue.util import rfc3339

from conftest import VERIFIER_CLI


def submit(loc, key, content=b"TEST content", cred="cred-A"):
    r = api.submit(loc.iss, cred, key, content)
    return r, api.record_id(cred, key)


def fetch_receipt(loc, key, cred="cred-A"):
    """The client's retrieval: one GET (303 to a short-lived URL), then the URL. -> (bytes, SHA-256 header)."""
    r = api.receipt(loc.iss, cred, key)
    assert r.status == 303, r
    return loc.iss.results.fetch_url(r.headers["Location"], loc.clock()), r.headers["Tessera-Receipt-SHA256"]


def verify_with_cli(loc, bundle, out_dir, headers_from_chain=True):
    """The relying party's run: TEST trust (window entries + pins of the bundle's headers taken from the stand-in
    chain), a TEST release over it and the frozen catalog, then the service verifier's CLI in --mode test."""
    out = Path(out_dir)
    hd = json.loads(bundle)["layers"][0]["headers"]
    hdrs = {int(h): loc.world.chain.header(int(h)) for h in hd}
    trust = stand_in.relying_party_trust(loc.iss.window, hdrs, rfc3339(loc.clock()))
    rel, key = stand_in.make_test_release(trust, loc.iss.frozen.catalog, P256Key("issuer-tests release key"))
    for name, data in (("bundle.json", bundle), ("trust.json", trust), ("release.json", rel), ("release-key.json", key)):
        (out / name).write_bytes(data)
    p = subprocess.run([str(VERIFIER_CLI), "--mode", "test", "--test-release", str(out / "release.json"),
                        "--test-release-key", str(out / "release-key.json"), "--trust", str(out / "trust.json"),
                        "--bundle", str(out / "bundle.json")], capture_output=True, text=True, timeout=600)
    return p.returncode, json.loads(p.stdout) if p.stdout.strip() else None, p.stderr
