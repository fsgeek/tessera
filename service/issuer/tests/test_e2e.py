"""Local end-to-end (DESIGN.md test group 2): stand-in signers, chain and calendar drive a request to COMPLETE, and
the issued bundle is verified by the service verifier's CLI in --mode test as VALID_STRICT. The relying party's
trust configuration pins the headers taken from the stand-in chain, not from the bundle."""
import base64
import json
import os

import pytest
from tessera_verify.codec import read_anchor, registered_codecs

from tessera_issue import api, local
from tessera_issue.util import ALG, MIB, sha256hex

from conftest import FROZEN
from helpers import fetch_receipt, submit, verify_with_cli


@pytest.mark.parametrize("wire,content", [(False, b"Tessera V1 issuer end-to-end TEST content\n"),
                                          (True, os.urandom(MIB))], ids=["direct", "wire-protocols-1MiB"])
def test_request_to_complete_and_verified_valid_strict(tmp_path, key, wire, content):
    loc = local.build(FROZEN, wire=wire)
    r, rid = submit(loc, key, content)
    assert r.status == 202
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE", (rec["state"], rec["reason"], loc.iss.log[-3:])
    bundle, digest = fetch_receipt(loc, key)
    assert sha256hex(bundle) == digest
    rc, out, err = verify_with_cli(loc, bundle, tmp_path)
    assert rc == 0, err
    assert out["stable"]["verdict"] == "VALID_STRICT" and out["stable"]["reason"] == "OK", out
    assert out["stable"]["T"] == rec["T"]
    assert out["utc_assessment"]["assumption_id"] == "A-UTC-7200-6" and out["utc_assessment"]["utc_upper_bound"]
    # S1: decoding common.content recovers exactly the submitted bytes, and those bytes are what is signed.
    layer = json.loads(bundle)["layers"][0]
    frames = read_anchor(base64.b64decode(layer["a_sig"]), registered_codecs(ALG))
    assert base64.b64decode(frames[0][1]["common"]["content"]) == content
    assert frames[0][1]["common"]["spec"]["sha256"] == loc.iss.frozen.catalog["spec_sha256"]


def test_tampered_bundle_is_not_valid(tmp_path, key):
    loc = local.build(FROZEN)
    _, rid = submit(loc, key, b"tamper control")
    assert loc.run_until_done(rid)["state"] == "COMPLETE"
    bundle = fetch_receipt(loc, key)[0]
    obj = json.loads(bundle)
    sig = bytearray(base64.b64decode(obj["layers"][0]["a_sig"]))
    sig[-10] ^= 1                                             # one bit of the gpg-slot signature
    obj["layers"][0]["a_sig"] = base64.b64encode(bytes(sig)).decode()
    from tessera_issue.util import jcs
    rc, out, err = verify_with_cli(loc, jcs(obj), tmp_path)
    assert rc == 0 and out["stable"]["verdict"] == "INVALID", out


def test_several_requests_in_flight_share_blocks_and_all_verify(tmp_path):
    import uuid
    loc = local.build(FROZEN)
    keys = [str(uuid.uuid4()) for _ in range(4)]
    rids = [submit(loc, k, f"request {i}".encode())[1] for i, k in enumerate(keys)]
    for _ in range(40):
        loc.tick()
        if all(loc.iss.requests.get(r)["state"] != "ACCEPTED" for r in rids):
            break
    recs = [loc.iss.requests.get(r) for r in rids]
    assert [r["state"] for r in recs] == ["COMPLETE"] * 4
    assert len({r["attempts"][-1]["latch"]["height"] for r in recs}) == 1    # one block, several transactions
    assert len({r["receipt_sha256"] for r in recs}) == 4
    rc, out, _ = verify_with_cli(loc, fetch_receipt(loc, keys[-1])[0], tmp_path)
    assert rc == 0 and out["stable"]["verdict"] == "VALID_STRICT"
