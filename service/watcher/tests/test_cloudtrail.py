"""CloudTrail log files: parsing realistic gzipped files, key timestamps, listing across regions and days, and the
classification of the events the watcher acts on."""
import gzip

import pytest

import fakes
from conftest import T0
from tessera_watch import cloudtrail as ct

KEY = ct.KeyRefs(fakes.KEY_ARN, (fakes.ALIAS,))


def kinds(rec):
    return [k for k, _ in ct.classify(rec, KEY, fakes.SIGNER_ROLE)]


def test_parse_gzipped_file_round_trip():
    recs = [fakes.sign_event(T0), fakes.iam_event(T0)]
    assert ct.parse(fakes.trail_file(recs)) == recs


@pytest.mark.parametrize("raw", [b"not gzip", gzip.compress(b"{not json"), gzip.compress(b'{"x": 1}'),
                                 gzip.compress(b"[1, 2]"), fakes.trail_file([])[:-4]])
def test_unreadable_files_raise_valueerror(raw):
    with pytest.raises(ValueError):
        ct.parse(raw)


def test_empty_records_list_is_a_valid_file():
    assert ct.parse(fakes.trail_file([])) == []


def test_key_time_from_cloudtrail_key():
    k = fakes.trail_key(T0)
    assert ct.key_time(k) == T0 - T0 % 60
    assert ct.key_time(f"AWSLogs/{fakes.ACCOUNT}/CloudTrail-Digest/us-east-2/2026/11/17/x.json.gz") is None


def test_sign_by_signer_role_on_key_arn_alias_and_id():
    assert kinds(fakes.sign_event(T0)) == ["sign"]
    e = fakes.sign_event(T0, key_param=fakes.ALIAS)
    e["resources"] = []
    assert kinds(e) == ["sign"]
    e = fakes.sign_event(T0, key_param=fakes.KEY_ID)
    e["resources"] = []
    assert kinds(e) == ["sign"]
    e = fakes.sign_event(T0, key_param=f"arn:aws:kms:{fakes.REGION}:{fakes.ACCOUNT}:{fakes.ALIAS}")
    e["resources"] = []
    assert kinds(e) == ["sign"]


def test_sign_by_other_principal_is_foreign():
    assert kinds(fakes.sign_event(T0, role=fakes.OTHER_ROLE)) == ["foreign_sign"]
    e = fakes.sign_event(T0)
    e["userIdentity"] = {"type": "Root", "arn": f"arn:aws:iam::{fakes.ACCOUNT}:root"}
    assert kinds(e) == ["foreign_sign"]


def test_access_denied_on_the_key_any_operation():
    assert kinds(fakes.sign_event(T0, role=fakes.OTHER_ROLE, error="AccessDenied")) == ["access_denied"]
    assert kinds(fakes.sign_event(T0, error="AccessDeniedException", name="GetPublicKey")) == ["access_denied"]


def test_other_keys_and_other_errors_are_ignored():
    other = f"arn:aws:kms:{fakes.REGION}:{fakes.ACCOUNT}:key/other"
    assert kinds(fakes.sign_event(T0, key=other)) == []
    assert kinds(fakes.sign_event(T0, error="ThrottlingException")) == []
    assert kinds(fakes.sign_event(T0, name="GetPublicKey")) == []


def test_iam_writes_and_reads():
    assert kinds(fakes.iam_event(T0)) == ["iam_write"]
    assert kinds(fakes.iam_event(T0, name="GetRole", read_only=True)) == []
    e = fakes.iam_event(T0, name="PutRolePolicy")
    e["readOnly"] = "false"
    assert kinds(e) == ["iam_write"]
    e = fakes.iam_event(T0, name="AttachRolePolicy")
    e["errorCode"] = "AccessDenied"                     # an attempted write is still reported
    assert kinds(e) == ["iam_write"]


def test_candidate_keys_all_regions_days_and_window():
    s3 = fakes.FakeS3()
    base = ct.base_prefix("", fakes.ACCOUNT)
    inside = [fakes.trail_key(T0 - 3600, "us-east-2"), fakes.trail_key(T0 - 90000, "us-east-1"),
              fakes.trail_key(T0, "eu-west-1")]
    outside = [fakes.trail_key(T0 - 3 * 86400, "us-east-2")]
    for k in inside + outside:
        s3.put("trail", k, b"x")
    s3.put("trail", f"AWSLogs/{fakes.ACCOUNT}/CloudTrail-Digest/us-east-2/x.json.gz", b"x")
    got = ct.candidate_keys(s3, "trail", base, T0 - 2 * 86400, T0)
    assert got == sorted(inside, key=lambda k: (ct.key_time(k), k))         # key-time order, across regions


def test_base_prefix_with_trail_prefix():
    assert ct.base_prefix("", "1") == "AWSLogs/1/CloudTrail/"
    assert ct.base_prefix("/p/q/", "1") == "p/q/AWSLogs/1/CloudTrail/"
