"""Copy receipts issued before content addressing (`result/<rid>/receipt.json`) to their digest names
(`result/<rid>/<receipt_sha256>.json`), so the API, which serves only digest names (A12 change 5), can still serve them
for their 30-day retention (S5). A steward tool, run with the author's session before and after the deployment.

Copies only when the request record is COMPLETE and the fixed-key bytes hash to its `receipt_sha256`; never deletes or
overwrites (an existing digest-named object is left as is); reports every case. Dry run unless --apply.

  python tools/migrate_receipts.py --table tessera-v1-issuer-requests --bucket <results bucket> [--apply]
"""
import argparse
import sys

LEGACY = "receipt.json"


def migrate(requests, results, rids, apply=False):
    """-> list of (rid prefix, outcome). Outcomes: copied, would-copy, present, not-complete, mismatch, missing."""
    from tessera_issue.util import sha256hex
    out = []
    for rid in rids:
        rec = requests.get(rid)
        data = results.get("result", rid, LEGACY)
        if data is None:
            out.append((rid[:12], "missing"))
            continue
        if rec is None or rec.get("state") != "COMPLETE" or not rec.get("receipt_sha256"):
            out.append((rid[:12], "not-complete"))
            continue
        digest = rec["receipt_sha256"]
        if sha256hex(bytes(data)) != digest:
            out.append((rid[:12], "mismatch"))
            continue
        name = f"{digest}.json"
        if results.size("result", rid, name) is not None:
            out.append((rid[:12], "present"))
            continue
        if apply:
            results.put("result", rid, name, bytes(data))
        out.append((rid[:12], "copied" if apply else "would-copy"))
    return out


def legacy_rids(s3, bucket):
    rids = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="result/"):
        for o in page.get("Contents", []):
            parts = o["Key"].split("/")
            if len(parts) == 3 and parts[2] == LEGACY:
                rids.append(parts[1])
    return rids


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--bucket", required=True)
    ap.add_argument("--region", default="us-east-2")
    ap.add_argument("--profile", default="tessera")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    import boto3
    from tessera_issue.aws import DynamoRequestStore, S3ResultStore
    sess = boto3.session.Session(profile_name=a.profile, region_name=a.region)
    s3 = sess.client("s3")
    rows = migrate(DynamoRequestStore(sess.client("dynamodb"), a.table), S3ResultStore(s3, a.bucket),
                   legacy_rids(s3, a.bucket), apply=a.apply)
    for rid, outcome in rows:
        print(rid, outcome)
    print(f"{len(rows)} fixed-key receipt(s); {'applied' if a.apply else 'dry run'}")
    return 1 if any(o == "mismatch" for _, o in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
