"""In-memory stand-ins for the clients the signer uses (boto3-style SQS and S3, the Cloud KMS adapter), implementing
exactly the calls the signer makes (no AWS, no GCP, no network)."""
import io
import itertools
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

SQS_MAX_BYTES = 1048576


class ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class Clock:
    def __init__(self, t):
        self.t = int(t)

    def __call__(self):
        return self.t

    def advance(self, s):
        self.t += int(s)


class FakeSqs:
    """At-least-once queues with visibility timeouts and receive counts, on the given clock."""

    def __init__(self, clock):
        self.clock, self.queues, self._ids = clock, {}, itertools.count(1)
        self.fail_delete = False
        self.fail_send = False

    def _q(self, url):
        return self.queues.setdefault(url, {})

    def send_message(self, QueueUrl, MessageBody):
        if self.fail_send:
            raise ClientError("ServiceUnavailable")
        if len(MessageBody.encode()) > SQS_MAX_BYTES:
            raise ClientError("InvalidParameterValue")
        mid = f"m{next(self._ids)}"
        self._q(QueueUrl)[mid] = {"body": MessageBody, "visible_at": 0, "receives": 0, "handle": None}
        return {"MessageId": mid}

    def receive_message(self, QueueUrl, MaxNumberOfMessages=1, WaitTimeSeconds=0, VisibilityTimeout=30,
                        MessageSystemAttributeNames=()):
        now, out = self.clock(), []
        for mid, m in self._q(QueueUrl).items():
            if len(out) >= MaxNumberOfMessages:
                break
            if m["visible_at"] <= now:
                m["visible_at"], m["receives"] = now + VisibilityTimeout, m["receives"] + 1
                m["handle"] = f"{mid}:{next(self._ids)}"
                msg = {"MessageId": mid, "ReceiptHandle": m["handle"], "Body": m["body"]}
                if "ApproximateReceiveCount" in MessageSystemAttributeNames:
                    msg["Attributes"] = {"ApproximateReceiveCount": str(m["receives"])}
                out.append(msg)
        return {"Messages": out} if out else {}

    def delete_message(self, QueueUrl, ReceiptHandle):
        if self.fail_delete:
            raise ClientError("ServiceUnavailable")
        mid = ReceiptHandle.split(":")[0]
        m = self._q(QueueUrl).get(mid)
        if m is not None and m["handle"] == ReceiptHandle:
            del self._q(QueueUrl)[mid]

    def bodies(self, url):
        return [json.loads(m["body"]) for m in self._q(url).values()]

    def take(self, url):
        """All messages on a queue as JSON, removing them (what a consumer that deletes would see)."""
        out = self.bodies(url)
        self._q(url).clear()
        return out


class QueueView:
    """The issuer's Queue interface (send / receive / delete) over one FakeSqs queue, so the issuer's own SlotSigner
    can drive the signer in the conformance tests."""

    def __init__(self, sqs, url):
        self.sqs, self.url = sqs, url

    def send(self, body):
        return self.sqs.send_message(QueueUrl=self.url, MessageBody=body)["MessageId"]

    def receive(self, max_messages=10, wait_s=0):
        from types import SimpleNamespace
        r = self.sqs.receive_message(QueueUrl=self.url, MaxNumberOfMessages=max_messages, VisibilityTimeout=60)
        return [SimpleNamespace(id=m["MessageId"], body=m["Body"], handle=m["ReceiptHandle"])
                for m in r.get("Messages", [])]

    def delete(self, handle):
        self.sqs.delete_message(QueueUrl=self.url, ReceiptHandle=handle)


class FakeS3:
    def __init__(self):
        self.objects, self.calls = {}, []
        self.transient = 0                     # this many get_object calls raise a non-404 error first

    def put(self, bucket, key, data):
        self.objects[(bucket, key)] = bytes(data)

    def get_object(self, Bucket, Key):
        self.calls.append((Bucket, Key))
        if self.transient:
            self.transient -= 1
            raise ClientError("SlowDown")
        data = self.objects.get((Bucket, Key))
        if data is None:
            raise ClientError("NoSuchKey")
        return {"Body": io.BytesIO(data), "ContentLength": len(data)}


class FakeKms:
    """A P-256 key standing in for the HSM key version. sign_digest signs the digest as Cloud KMS does."""

    def __init__(self, name, algorithm="EC_SIGN_P256_SHA256", protection="HSM", key=None):
        self.key = key or ec.generate_private_key(ec.SECP256R1())
        self.name, self.algorithm, self.protection = name, algorithm, protection
        self.signed = []                       # digests signed
        self.fail = 0                          # this many sign calls raise first
        self.corrupt = False                   # return a signature over a different digest

    def public_key(self):
        pem = self.key.public_key().public_bytes(serialization.Encoding.PEM,
                                                 serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        return {"name": self.name, "algorithm": self.algorithm, "protectionLevel": self.protection, "pem": pem}

    def sign_digest(self, digest):
        if self.fail:
            self.fail -= 1
            raise RuntimeError("KMS :asymmetricSign: HTTP 503")
        self.signed.append(digest)
        d = bytes(32) if self.corrupt else digest
        return self.key.sign(d, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
