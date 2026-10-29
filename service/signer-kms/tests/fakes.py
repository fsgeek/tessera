"""In-memory stand-ins for the boto3 clients the signer uses (kms, s3, sqs), implementing exactly the calls it makes
(no AWS, no network). Mirrors service/issuer/tests/fakes.py."""
import io

from tessera_issue.queues import InMemoryQueue


class ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class FakeKms:
    """An ML-DSA-65 KMS key backed by a TEST key (tessera_issue.testkeys.MLDSA65Key). sign() accepts only what real
    KMS needs for the external-mu path, and signs the 64-byte mu with the key's sign_mu."""
    ARN = "arn:aws:kms:us-east-2:111122223333:key/0b0e7c6e-test-test-test-000000000001"

    def __init__(self, key, key_spec="ML_DSA_65"):
        self.key, self.key_spec = key, key_spec
        self.signs, self.fail = [], None              # fail: an exception to raise from sign()
        self.tamper = None                            # tamper(sig) -> sig, to model a bad KMS answer

    def get_public_key(self, KeyId):
        return {"KeyId": self.ARN, "PublicKey": self.key.spki, "KeySpec": self.key_spec, "KeyUsage": "SIGN_VERIFY",
                "SigningAlgorithms": ["ML_DSA_SHAKE_256"]}

    def sign(self, KeyId, Message, MessageType, SigningAlgorithm):
        assert MessageType == "EXTERNAL_MU" and SigningAlgorithm == "ML_DSA_SHAKE_256" and len(Message) == 64
        self.signs.append(bytes(Message))
        if self.fail is not None:
            raise self.fail
        sig = self.key._priv.sign_mu(bytes(Message))
        return {"KeyId": self.ARN, "Signature": self.tamper(sig) if self.tamper else sig,
                "SigningAlgorithm": SigningAlgorithm}


class FakeS3:
    def __init__(self):
        self.objects, self.fail, self.gets = {}, None, []

    def get_object(self, Bucket, Key):
        self.gets.append((Bucket, Key))
        if self.fail is not None:
            raise self.fail
        if (Bucket, Key) not in self.objects:
            raise ClientError("NoSuchKey")
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}


class FakeSqs:
    def __init__(self, clock):
        self.queues, self.clock, self.fail = {}, clock, None

    def q(self, url):
        return self.queues.setdefault(url, InMemoryQueue(self.clock))

    def send_message(self, QueueUrl, MessageBody):
        if self.fail is not None:
            raise self.fail
        return {"MessageId": self.q(QueueUrl).send(MessageBody)}


class FakeSession:
    def __init__(self, **clients):
        self.clients = clients

    def client(self, name, **kw):
        return self.clients[name]


class Log(list):
    def __call__(self, entry):
        self.append(entry)
