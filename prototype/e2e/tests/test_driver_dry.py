"""The whole issuer driver in dry-run mode: TEST signers, stub OTS chain, stub DNS; real GnuPG and git. The bundle
must be VALID_STRICT under the independent verifier provisioned by a TEST-signed release; tampering must not be."""
import json

import pytest

import driver
from common import U, b64, b64d, jcs, read_json, write_atomic


@pytest.fixture(scope="module")
def dry(tmp_path_factory):
    from common import WORK
    import time
    d = WORK / "tests" / f"dry-module-{time.strftime('%Y%m%dT%H%M%S')}"
    driver.init(d, "dry")
    driver.run(d, until="frames")          # stop part-way: every stage resumes from disk
    r = driver.Run(d)
    assert "frames" in r.state and "sign" not in r.state
    driver.run(d)
    return driver.Run(d)


def test_dry_run_valid_strict(dry):
    v = dry.state["verify"]
    assert v["verdict"] == "VALID_STRICT" and v["reason"] == "OK"
    assert v["T"] == U.rfc3339(read_json(dry.p("preship.json"))["facts"]["receipt"]["T"])
    assert all(read_json(dry.p("preship.json"))["checks"].values())


def test_dry_run_utc_assessment(dry):
    # A10.1.1 / profile 7.4: reported beside the stable six, U = 7200 + max nTime(h*..h*+5) >= T + 7200.
    a = dry.state["verify"]["utc_assessment"]
    assert a["assumption_id"] == "A-UTC-7200-6"
    T = read_json(dry.p("preship.json"))["facts"]["receipt"]["T"]
    assert U.ts(a["utc_upper_bound"]) >= T + 7200


def test_chain_order_and_heights(dry):
    f = read_json(dry.p("preship.json"))["facts"]
    assert f["git"]["h"] + 5 < f["receipt"]["h"]
    assert dry.state["stamp-receipt"]["tip_at_stamp"] >= dry.state["wait-git"]["h_git_lowest"] + 5


def _verify(dry, bundle_bytes, tmp, release=None):
    b = tmp / "bundle.json"
    b.write_bytes(bundle_bytes)
    rc, out, err = driver.verify_with_indep(dry.p("trust.json"), b, release or dry.p("release.json"),
                                            dry.p("release-key.json"))
    return rc, (json.loads(out)["stable"] if rc == 0 else None), err


def test_tampered_content_rejected(dry, tmp_path):
    obj = json.loads(dry.p("bundle.json").read_bytes())
    L = obj["layers"][0]
    a = bytearray(b64d(L["a_sig"]))
    i = bytes(a).index(b'"TEST":"Tessera V1')
    a[i + 2] ^= 0x20                                           # one bit inside the signed content
    L["a_sig"] = b64(bytes(a))
    rc, v, _ = _verify(dry, jcs(obj), tmp_path)
    assert rc == 0 and v["verdict"] == "INVALID"


def test_txid_swap_rejected(dry, tmp_path):
    obj = json.loads(dry.p("bundle.json").read_bytes())
    obj["layers"][0]["receipt_anchor"]["txid"] = "00" * 32
    rc, v, _ = _verify(dry, jcs(obj), tmp_path)
    assert rc == 0 and (v["verdict"], v["reason"]) == ("INVALID", "ANCHOR_TXID_MISMATCH")


def test_foreign_signed_release_gives_no_verdict(dry, tmp_path):
    rel = json.loads(dry.p("release.json").read_bytes())
    k = U.Keys.p256("not the TEST release key")
    forged = U.make_release(dry.p("trust.json").read_bytes(), signer=k, catalog_obj=rel["release"]["catalog"])
    forged["signature"]["signer_spki_sha256"] = rel["signature"]["signer_spki_sha256"]
    write_atomic(tmp_path / "release.json", jcs(forged))
    rc, v, err = _verify(dry, dry.p("bundle.json").read_bytes(), tmp_path, tmp_path / "release.json")
    assert rc != 0 and v is None and "TRUST_CONFIG_UNAUTHENTICATED" in err


def test_receipt_stamp_refused_before_k6(dry):
    class Fake:
        state = {"wait-git": {"h_git_lowest": 10**9}}

        def tip(self):
            return 10**9 + 4
    with pytest.raises(driver.IssueRefused):
        driver.st_stamp_receipt(Fake())
