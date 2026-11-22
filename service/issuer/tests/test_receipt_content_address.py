"""A12-R2-03 / A12 r5 change 5: receipts are content-addressed (result/<rid>/<sha256>.json). A stale worker's late
put cannot change what the API serves; a fixed-key object is never served; tools/migrate_receipts.py copies pre-change
receipts to their digest names only when they hash to the record's digest; cleanup deletes both naming forms."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import migrate_receipts  # noqa: E402
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


def test_tampered_addressed_object_is_caught_by_the_clients_digest_check(key):
    """The API does not re-read the body (a check before the fetch cannot cover the fetch); S2's client check does."""
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    loc.iss.results.put("result", rid, rec["receipt_sha256"] + ".json", b"different bytes")
    r = api.receipt(loc.iss, "cred-A", key)
    assert r.status == 303 and r.headers["Tessera-Receipt-SHA256"] == rec["receipt_sha256"]
    served = loc.iss.results.get("result", rid, rec["receipt_sha256"] + ".json")
    assert sha256hex(served) != r.headers["Tessera-Receipt-SHA256"]     # the client rejects it


def test_a_fixed_key_object_is_never_served(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    good = loc.iss.results.get("result", rid, rec["receipt_sha256"] + ".json")
    loc.iss.results.delete("result", rid)
    loc.iss.results.put("result", rid, LEGACY, good)
    assert api.receipt(loc.iss, "cred-A", key).status == 410


def test_migration_copies_matching_legacy_receipts_and_reports_the_rest(key):
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    good = loc.iss.results.get("result", rid, rec["receipt_sha256"] + ".json")
    loc.iss.results.delete("result", rid)
    loc.iss.results.put("result", rid, LEGACY, good)
    assert migrate_receipts.migrate(loc.iss.requests, loc.iss.results, [rid]) == [(rid[:12], "would-copy")]
    assert api.receipt(loc.iss, "cred-A", key).status == 410                       # dry run changed nothing
    assert migrate_receipts.migrate(loc.iss.requests, loc.iss.results, [rid], apply=True) == [(rid[:12], "copied")]
    served, digest = fetch_receipt(loc, key)
    assert served == good and sha256hex(served) == digest == rec["receipt_sha256"]
    assert migrate_receipts.migrate(loc.iss.requests, loc.iss.results, [rid], apply=True) == [(rid[:12], "present")]
    loc.iss.results.put("result", rid, LEGACY, b"not the receipt")
    loc.iss.results.delete("result", rid)
    loc.iss.results.put("result", rid, LEGACY, b"not the receipt")
    assert migrate_receipts.migrate(loc.iss.requests, loc.iss.results, [rid], apply=True) == [(rid[:12], "mismatch")]
    assert api.receipt(loc.iss, "cred-A", key).status == 410


def test_missing_object_under_list_permission_is_410_not_an_error(key):
    """With ListBucket on result/*, S3 answers a missing key with 404; the adapter maps it to None and the API to 410."""
    loc = local.build(FROZEN)
    rid, rec = complete(loc, key)
    loc.iss.results.delete("result", rid)
    assert api.receipt(loc.iss, "cred-A", key).status == 410


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
