"""Copy receipts issued before content addressing (`result/<rid>/receipt.json`) to their digest names
(`result/<rid>/<receipt_sha256>.json`), so the API, which serves only digest names (A12 change 5), can still serve them
for their 30-day retention (S5). A steward tool, run with the author's session before and after the deployment.

Copies only when the request record is COMPLETE, unexpired, and the fixed-key bytes hash to its `receipt_sha256`;
writes create-only (S3 IfNoneMatch="*"), never deletes or overwrites; an existing digest object with wrong bytes is
reported, not replaced. Dry run unless --apply. Exit 1 on any mismatch or not-complete row. Run once before the
deployment and once after the poller's maximum invocation time has passed since it, so no old-code invocation can
still be writing a fixed-key receipt or its COMPLETE.

  python tools/migrate_receipts.py --table tessera-v1-issuer-requests --bucket <results bucket> [--apply]
"""
import argparse
import sys

LEGACY = "receipt.json"


def migrate(requests, results, rids, apply=False, now=None, create_only=None):
    """-> list of (rid prefix, outcome). Outcomes: copied, would-copy, present, present-mismatch, exists-raced,
    not-complete, expired, mismatch, missing. `create_only(rid, name, data)` writes only if the object does not exist
    and returns False if it did (S3: PutObject IfNoneMatch="*"); without it, a check-then-put for single-process tests."""
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
        if now is not None and rec.get("expires_at") is not None and now >= rec["expires_at"]:
            out.append((rid[:12], "expired"))          # never recreate an object for a record past retention
            continue
        digest = rec["receipt_sha256"]
        if sha256hex(bytes(data)) != digest:
            out.append((rid[:12], "mismatch"))
            continue
        name = f"{digest}.json"
        if results.size("result", rid, name) is not None:
            have = results.get("result", rid, name)
            ok = have is not None and sha256hex(bytes(have)) == digest
            out.append((rid[:12], "present" if ok else "present-mismatch"))   # never overwritten; reported
            continue
        if not apply:
            out.append((rid[:12], "would-copy"))
            continue
        if create_only is not None:
            wrote = create_only(rid, name, bytes(data))
        else:
            wrote = results.size("result", rid, name) is None
            if wrote:
                results.put("result", rid, name, bytes(data))
        out.append((rid[:12], "copied" if wrote else "exists-raced"))
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
    import time
    sess = boto3.session.Session(profile_name=a.profile, region_name=a.region)
    s3 = sess.client("s3")
    store = S3ResultStore(s3, a.bucket)

    def create_only(rid, name, data):
        try:
            s3.put_object(Bucket=a.bucket, Key=store.key("result", rid, name), Body=data, IfNoneMatch="*")
            return True
        except s3.exceptions.ClientError as e:
            if e.response.get("Error", {}).get("Code") in ("PreconditionFailed", "ConditionalRequestConflict"):
                return False
            raise

    rows = migrate(DynamoRequestStore(sess.client("dynamodb"), a.table), store, legacy_rids(s3, a.bucket),
                   apply=a.apply, now=time.time(), create_only=create_only)
    for rid, outcome in rows:
        print(rid, outcome)
    print(f"{len(rows)} fixed-key receipt(s); {'applied' if a.apply else 'dry run'}")
    return 1 if any(o in ("mismatch", "present-mismatch", "not-complete") for _, o in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
