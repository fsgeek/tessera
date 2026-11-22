"""In-memory stand-ins for the boto3 clients the watcher uses, and builders of realistic issuer items and CloudTrail
log files. No network."""
import gzip
import hashlib
import io
import json
import time
import uuid

ACCOUNT = "111122223333"
REGION = "us-east-2"
KEY_ID = "2c9ba2cf-0000-4000-8000-000000000001"
KEY_ARN = f"arn:aws:kms:{REGION}:{ACCOUNT}:key/{KEY_ID}"
ALIAS = "alias/tessera-v1-kms"
SIGNER_ROLE = f"arn:aws:iam::{ACCOUNT}:role/tessera-v1-signer-kms-role"
OTHER_ROLE = f"arn:aws:iam::{ACCOUNT}:role/admin"


class ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class Body:
    def __init__(self, data):
        self.data = data

    def read(self, n=-1):
        return self.data


class FakeS3:
    def __init__(self):
        self.objects = {}          # (bucket, key) -> {"body", "etag", "kw"}
        self.versions = []         # every put, in order: (bucket, key, kw)
        self.fail_put = None       # a callable(bucket, key) -> exception or None
        self.gets = []

    def put(self, bucket, key, data):
        self.objects[(bucket, key)] = {"body": data, "etag": '"%s"' % hashlib.md5(data).hexdigest(), "kw": {}}

    def put_object(self, Bucket, Key, Body, **kw):
        if self.fail_put and (e := self.fail_put(Bucket, Key)):
            raise e
        cur = self.objects.get((Bucket, Key))
        if "IfNoneMatch" in kw and cur is not None:
            raise ClientError("PreconditionFailed")
        if "IfMatch" in kw and (cur is None or cur["etag"] != kw["IfMatch"]):
            raise ClientError("PreconditionFailed")
        self.objects[(Bucket, Key)] = {"body": bytes(Body), "etag": '"%s"' % uuid.uuid4().hex, "kw": kw}
        self.versions.append((Bucket, Key, kw))
        return {"ETag": self.objects[(Bucket, Key)]["etag"]}

    def get_object(self, Bucket, Key):
        self.gets.append((Bucket, Key))
        o = self.objects.get((Bucket, Key))
        if o is None:
            raise ClientError("NoSuchKey")
        return {"Body": Body(o["body"]), "ETag": o["etag"]}

    def delete_object(self, Bucket, Key):
        self.objects.pop((Bucket, Key), None)
        self.deletes = getattr(self, "deletes", []) + [(Bucket, Key)]

    def head_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            raise ClientError("404")
        return {"ContentLength": len(self.objects[(Bucket, Key)]["body"])}

    def list_objects_v2(self, Bucket, Prefix="", Delimiter=None, ContinuationToken=None, MaxKeys=2):
        keys = sorted(k for b, k in self.objects if b == Bucket and k.startswith(Prefix))
        if Delimiter:
            prefixes = sorted({Prefix + k[len(Prefix):].split(Delimiter, 1)[0] + Delimiter for k in keys
                               if Delimiter in k[len(Prefix):]})
            return {"CommonPrefixes": [{"Prefix": p} for p in prefixes]}
        start = int(ContinuationToken or 0)                      # paginate in pages of 2 to exercise the loop
        page = keys[start:start + MaxKeys]
        out = {"Contents": [{"Key": k} for k in page]}
        if start + MaxKeys < len(keys):
            out["NextContinuationToken"] = str(start + MaxKeys)
        return out


class FakeDynamo:
    """Holds items as the issuer writes them; the watcher may only scan."""

    def __init__(self):
        self.items = {}
        self.calls = []

    def put(self, pk, doc):
        self.items[pk] = {"pk": {"S": pk}, "doc": {"S": json.dumps(doc, sort_keys=True)}}

    def scan(self, **kw):
        self.calls.append(("scan", kw))
        assert kw["FilterExpression"] == "begins_with(pk, :r) OR begins_with(pk, :s)"
        pks = sorted(p for p in self.items if p.startswith(("REQ#", "SIGLOG#")))
        start = int((kw.get("ExclusiveStartKey") or {}).get("i", 0))
        page = pks[start:start + 3]
        out = {"Items": [self.items[p] for p in page]}
        if start + 3 < len(pks):
            out["LastEvaluatedKey"] = {"i": start + 3}
        return out

    def __getattr__(self, name):                                # any other call is a write or a read we never make
        raise AssertionError(f"watcher called dynamodb.{name}")


class FakeSNS:
    def __init__(self):
        self.sent = []
        self.fail = False

    def publish(self, TopicArn, Subject, Message):
        if self.fail:
            raise ClientError("InternalError")
        self.sent.append({"TopicArn": TopicArn, "Subject": Subject, "Message": Message})


class FakeCW:
    def __init__(self):
        self.beats = []

    def put_metric_data(self, Namespace, MetricData):
        self.beats.append((Namespace, MetricData))


# ------------------------------------------------------------------------------------------- CloudTrail builders
def rfc(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(t)))


def ident(role):
    return {"type": "AssumedRole", "principalId": "AROAEXAMPLE:session", "arn": role.replace(":role/", ":assumed-role/")
            .replace("arn:aws:iam::", "arn:aws:sts::") + "/session", "accountId": ACCOUNT,
            "sessionContext": {"sessionIssuer": {"type": "Role", "arn": role, "accountId": ACCOUNT,
                                                 "userName": role.rsplit("/", 1)[-1]},
                               "attributes": {"creationDate": "2026-11-22T00:00:00Z", "mfaAuthenticated": "false"}}}


def sign_event(t, role=SIGNER_ROLE, key=KEY_ARN, error=None, key_param=None, eid=None, name="Sign"):
    e = {"eventVersion": "1.10", "userIdentity": ident(role), "eventTime": rfc(t), "eventSource": "kms.amazonaws.com",
         "eventName": name, "awsRegion": REGION, "sourceIPAddress": "lambda.amazonaws.com", "userAgent": "Boto3/1.40",
         "requestParameters": {"keyId": key_param or key, "messageType": "EXTERNAL_MU",
                               "signingAlgorithm": "ML_DSA_SHAKE_256"},
         "responseElements": None, "requestID": str(uuid.uuid4()), "eventID": eid or str(uuid.uuid4()),
         "readOnly": True, "resources": [{"accountId": ACCOUNT, "type": "AWS::KMS::Key", "ARN": key}],
         "eventType": "AwsApiCall", "managementEvent": True, "recipientAccountId": ACCOUNT,
         "eventCategory": "Management"}
    if error:
        e["errorCode"] = error
        e["errorMessage"] = "User is not authorized to perform: kms:Sign"
    return e


def iam_event(t, name="CreateAccessKey", read_only=False, role=OTHER_ROLE):
    return {"eventVersion": "1.10", "userIdentity": ident(role), "eventTime": rfc(t),
            "eventSource": "iam.amazonaws.com", "eventName": name, "awsRegion": "us-east-1",
            "requestParameters": {"userName": "someone"}, "responseElements": None, "eventID": str(uuid.uuid4()),
            "readOnly": read_only, "eventType": "AwsApiCall", "managementEvent": True,
            "recipientAccountId": ACCOUNT, "eventCategory": "Management"}


def trail_key(t, region=REGION):
    stamp = time.strftime("%Y%m%dT%H%MZ", time.gmtime(int(t)))
    day = time.strftime("%Y/%m/%d", time.gmtime(int(t)))
    return (f"AWSLogs/{ACCOUNT}/CloudTrail/{region}/{day}/{ACCOUNT}_CloudTrail_{region}_{stamp}_"
            f"{uuid.uuid4().hex[:16]}.json.gz")


def trail_file(records):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(json.dumps({"Records": records}).encode())
    return buf.getvalue()


# ------------------------------------------------------------------------------------------- issuer item builders
def sha(b):
    return hashlib.sha256(b).hexdigest()


def siglog(at, slot="kms", status="SIGNED", disposition="used", reason=None, request_id=None, sig=None, attempt="a1"):
    return {"at": rfc(at), "slot": slot, "request_id": request_id or "r-" + uuid.uuid4().hex[:20], "status": status,
            "reason": reason, "frame_sha256": sha(b"frame" + str(at).encode()),
            "signature_sha256": (sig or sha(uuid.uuid4().bytes)) if status == "SIGNED" else None,
            "disposition": disposition, "attempt": attempt}


def request(rid, state, ended_at, created_at=None, jobs=None, receipt_sha256=None, cred="c" * 64, key=None,
            reason=None):
    a = {"n": 1, "id": "a1", "state": "shipped" if state == "COMPLETE" else "discarded",
         "declared_issue_time": rfc(created_at or ended_at - 600), "jobs": jobs or {},
         "end": {"outcome": "SHIPPED" if state == "COMPLETE" else "DISCARDED", "reason": reason, "at": ended_at}}
    return {"rid": rid, "cred": cred, "key": key or str(uuid.uuid4()), "state": state, "reason": reason,
            "stage": None, "content_sha256": sha(b"content"), "content_len": 7,
            "created_at": created_at or ended_at - 600, "ended_at": ended_at, "expires_at": ended_at + 30 * 86400,
            "cur": 1, "attempts": [a], "receipt_sha256": receipt_sha256, "events": []}


def job(slot, request_id, sig_sha256):
    return {"slot": slot, "frame": "f_" + slot, "frame_sha256": sha(request_id.encode()), "request_id": request_id,
            "sent_at": 0, "attempts": 1, "sig_sha256": sig_sha256}
