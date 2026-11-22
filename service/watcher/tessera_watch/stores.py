"""The watcher's reads of the issuer's stores (read-only) and writes to its own (state, trace records, findings,
heartbeat), over injected boto3-style clients. Nothing here can write to an issuer store: the methods do not exist,
and the role (service/detect/infra) grants no such action.

Issuer item shapes read (service/issuer/tessera_issue/aws.py docstring): REQ#<rid> with "doc" (the request record as
JSON); SIGLOG#<uuid> and SIGLOG#USED#<signer request id>#<signature sha256> with "doc" (one signer response as
logged). Receipts: result/<rid>/<receipt sha256>.json in the results bucket."""
import json
import re

HEX64 = re.compile(r"[0-9a-f]{64}")


def _code(exc):
    return getattr(exc, "response", {}).get("Error", {}).get("Code") or type(exc).__name__


def _missing(exc):
    return _code(exc) in ("NoSuchKey", "404", "NotFound")


class IssuerTable:
    """Read-only scan of REQ# and SIGLOG# items. -> (requests, siglog) with siglog as [(pk, entry)]."""

    def __init__(self, client, table):
        self.c, self.t = client, table

    def scan(self):
        reqs, logs, start = [], [], None
        while True:
            kw = {"TableName": self.t, "ConsistentRead": True,
                  "FilterExpression": "begins_with(pk, :r) OR begins_with(pk, :s)",
                  "ExpressionAttributeValues": {":r": {"S": "REQ#"}, ":s": {"S": "SIGLOG#"}},
                  "ProjectionExpression": "pk, #d", "ExpressionAttributeNames": {"#d": "doc"}}
            if start:
                kw["ExclusiveStartKey"] = start
            r = self.c.scan(**kw)
            for it in r.get("Items", []):
                pk = it["pk"]["S"]
                try:
                    doc = json.loads(it["doc"]["S"])
                except (KeyError, ValueError, TypeError):
                    doc = None
                (reqs if pk.startswith("REQ#") else logs).append((pk, doc))
            start = r.get("LastEvaluatedKey")
            if not start:
                return reqs, logs


class Results:
    """GetObject on result/* only. The role also holds s3:ListBucket on the bucket (review H1), so an absent object
    answers 404 (None here), not 403; any other failure raises to the caller, which reports it per receipt. The key is
    built only from a validated 64-hex rid and digest, so an SDK error can never carry an issuer-supplied path."""

    def __init__(self, client, bucket):
        self.c, self.b = client, bucket

    def receipt(self, rid, digest):
        if not (isinstance(rid, str) and HEX64.fullmatch(rid) and isinstance(digest, str) and HEX64.fullmatch(digest)):
            raise ValueError("receipt key")
        try:
            return self.c.get_object(Bucket=self.b, Key=f"result/{rid}/{digest}.json")["Body"].read()
        except Exception as e:  # noqa: BLE001
            if _missing(e):
                return None
            raise


class TrailBucket:
    def __init__(self, client, bucket):
        self.c, self.b = client, bucket

    def get(self, key):
        return self.c.get_object(Bucket=self.b, Key=key)["Body"].read()


class StateObject:
    """The watcher's durable cursor: one JSON object in its own bucket, written with S3 conditional writes (If-Match on
    the ETag read, If-None-Match on the first write), so two runs can never both commit from the same state."""

    def __init__(self, client, bucket, key):
        self.c, self.b, self.k = client, bucket, key

    def load(self):
        try:
            r = self.c.get_object(Bucket=self.b, Key=self.k)
        except Exception as e:  # noqa: BLE001
            if _missing(e):
                return None, None
            raise
        return json.loads(r["Body"].read()), r["ETag"]

    def save(self, state, etag):
        body = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
        kw = {"IfMatch": etag} if etag else {"IfNoneMatch": "*"}
        r = self.c.put_object(Bucket=self.b, Key=self.k, Body=body, ContentType="application/json",
                              ServerSideEncryption="AES256", **kw)
        return (r or {}).get("ETag")


class Outbox:
    """Findings awaiting publication (review M3): findings/<id>.json in the watcher's state bucket. A finding is written
    here when it is found, before any trace write and before publication; it is deleted only after SNS accepted it, so
    one that fails to publish (or whose run dies) is published by a later run. The id is a digest of the finding, so a
    replayed run that finds the same thing again writes nothing new while it is still waiting."""

    PREFIX = "findings/"

    def __init__(self, client, bucket):
        self.c, self.b = client, bucket

    def put(self, fid, line):
        body = json.dumps(line, sort_keys=True, separators=(",", ":")).encode()
        try:
            self.c.put_object(Bucket=self.b, Key=f"{self.PREFIX}{fid}.json", Body=body,
                              ContentType="application/json", ServerSideEncryption="AES256", IfNoneMatch="*")
        except Exception as e:  # noqa: BLE001
            if _code(e) in ("PreconditionFailed", "ConditionalRequestConflict"):
                return                                  # already waiting
            raise

    def keys(self):
        out, token = [], None
        while True:
            kw = {"Bucket": self.b, "Prefix": self.PREFIX}
            if token:
                kw["ContinuationToken"] = token
            r = self.c.list_objects_v2(**kw)
            out += [o["Key"] for o in r.get("Contents", [])]
            token = r.get("NextContinuationToken")
            if not token:
                return sorted(out)

    def get(self, key):
        return json.loads(self.c.get_object(Bucket=self.b, Key=key)["Body"].read())

    def delete(self, key):
        self.c.delete_object(Bucket=self.b, Key=key)


class TraceBucket:
    """trace/<rid>.json under Object Lock COMPLIANCE until retain_until (computed in code from the packaged window record,
    lambda_app.retain_until). Written once under the current key: an existing record is kept, never replaced (a re-run
    after a crash finds it and writes nothing). The bucket policy refuses delete markers and version deletes to every
    principal, so the current key stays the first record written (an account administrator who rewrites the bucket
    policy is the stated residual)."""

    def __init__(self, client, bucket, retain_until):
        self.c, self.b, self.until = client, bucket, retain_until

    def exists(self, rid):
        try:
            self.c.head_object(Bucket=self.b, Key=f"trace/{rid}.json")
            return True
        except Exception as e:  # noqa: BLE001
            if _missing(e):
                return False
            raise

    def put(self, rid, record):
        if not (isinstance(rid, str) and HEX64.fullmatch(rid)):
            raise ValueError("trace key")
        if self.exists(rid):
            return False
        body = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        self.c.put_object(Bucket=self.b, Key=f"trace/{rid}.json", Body=body, ContentType="application/json",
                          ObjectLockMode="COMPLIANCE", ObjectLockRetainUntilDate=self.until,
                          ChecksumAlgorithm="SHA256", ServerSideEncryption="AES256", IfNoneMatch="*")
        return True


class Topic:
    def __init__(self, client, arn):
        self.c, self.arn = client, arn

    def publish(self, subject, message):
        self.c.publish(TopicArn=self.arn, Subject=subject[:100], Message=message)


class Heartbeat:
    NAMESPACE = "Tessera/Watcher"

    def __init__(self, client, name="Heartbeat"):
        self.c, self.name = client, name

    def beat(self):
        self.c.put_metric_data(Namespace=self.NAMESPACE, MetricData=[{"MetricName": self.name, "Value": 1.0,
                                                                      "Unit": "Count"}])
