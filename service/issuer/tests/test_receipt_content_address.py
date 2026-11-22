"""A12-R2-03 / A12 r5 change 5: receipts are content-addressed (result/<rid>/<sha256>.json). A stale worker's late
put cannot change what the API serves; pre-change receipts at the fixed key are served only when they hash to the
record's digest; cleanup deletes both naming forms."""
from tessera_issue import api, local, pipeline
from tessera_issue.aws import S3ResultStore
from tessera_issue.service import RETENTION_S
from tessera_issue.util import sha256hex

from conftest import FROZEN
from fakes import FakeS3
from helpers import fetch_receipt, submit, verify_with_cli

LEGACY = "receipt.json"


def complete(loc, key):
    _, rid = submit(loc, key)
    rec = loc.run_until_done(rid)
    assert rec["state"] == "COMPLETE", (rec["state"], rec["reason"])
    return rid, rec


def test_receipt_is_stored_under_its_digest_and_verifies(tmp_path, key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    assert loc.iss.results.names("result", rid) == [rec["receipt_sha256"] + ".json"]
    bundle, digest = fetch_receipt(loc, key)
    assert sha256hex(bundle) == digest == rec["receipt_sha256"]
    rc, out, err = verify_with_cli(loc, bundle, tmp_path)
    assert rc == 0, err
    assert out["stable"]["verdict"] == "VALID_STRICT"


def test_stale_puts_after_complete_cannot_change_what_is_served(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    good, _ = fetch_receipt(loc, key)
    loc.iss.results.put("result", rid, LEGACY, b"stale writer, other bytes")
    loc.iss.results.put("result", rid, sha256hex(b"x") + ".json", b"x")
    served, digest = fetch_receipt(loc, key)
    assert served == good and sha256hex(served) == digest == rec["receipt_sha256"]
    r = api.receipt(loc.iss, "cred-A", key)
    assert r.headers["Location"].endswith(f"/{rid}/{rec['receipt_sha256']}.json" + r.headers["Location"].split(".json", 1)[1])


def test_tampered_addressed_object_is_refused_not_served(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    loc.iss.results.put("result", rid, rec["receipt_sha256"] + ".json", b"different bytes")
    # even a valid legacy copy must not rescue a corrupt addressed object
    assert api.receipt(loc.iss, "cred-A", key).status == 410


def test_legacy_fixed_key_receipt_is_served_when_its_hash_matches(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    good = loc.iss.results.get("result", rid, rec["receipt_sha256"] + ".json")
    loc.iss.results.delete("result", rid)
    loc.iss.results.put("result", rid, LEGACY, good)
    served, digest = fetch_receipt(loc, key)
    assert served == good and sha256hex(served) == digest


def test_legacy_fixed_key_receipt_with_wrong_hash_is_refused(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    loc.iss.results.delete("result", rid)
    loc.iss.results.put("result", rid, LEGACY, b"not the receipt")
    assert api.receipt(loc.iss, "cred-A", key).status == 410
    loc.iss.results.delete("result", rid)
    assert api.receipt(loc.iss, "cred-A", key).status == 410         # nothing stored: as before


def test_cleanup_deletes_both_naming_forms_on_s3(key):
    loc = local.build(FROZEN)
    loc.iss.results = S3ResultStore(FakeS3(), "bucket")
    loc.workers["kms"].fetch = loc.workers["gpg"].fetch = loc.iss.results.get_ref
    s3 = loc.iss.results.c
    rid, rec = complete(loc, key)
    loc.iss.results.put("result", rid, LEGACY, b"legacy form")
    assert len([k for b, k in s3.objects if k.startswith(f"result/{rid}/")]) == 2
    loc.clock.t = rec["ended_at"] + RETENTION_S
    for _ in range(4):
        loc.tick()
    assert not [k for b, k in s3.objects if k.startswith(f"result/{rid}/")]
