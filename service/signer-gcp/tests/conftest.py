import base64
import hashlib
import json
import time

import pytest
from tessera_verify.codec import (frame, isotime, jcs, parse_signature, public_key, registered_codecs, sig_policy,
                                  signature_verifies, utc)

from tessera_signer import openpgp
from tessera_signer.main import Config
from tessera_signer.policy import ALG
from tessera_signer.signer import Signer

from fakes import Clock, FakeKms, FakeS3, FakeSqs

T0 = utc("2026-11-10T12:00:00Z")
SIGN_UNTIL = T0 + 10 * 86400
KEY_VERSION = "projects/tessera-slot2/locations/us-east1/keyRings/tessera-v1/cryptoKeys/slot2/cryptoKeyVersions/1"
KEY_CREATED = 1791946553
REQ, RESP, BUCKET = "https://sqs.test/gpg-requests", "https://sqs.test/gpg-responses", "issuer-results"
VERIFIER_CLI = (__import__("pathlib").Path(__file__).resolve().parents[3] / "service" / "verifier" / ".venv" / "bin"
                / "tessera-verify")                                # read by service/issuer/tests/helpers.py


def attest(key_fp, declared, alg=ALG, content=None):
    common = {"alg": alg, "binding_forms": ["STMT_DIRECT"], "content": content or {"statement": "test"},
              "declared_issue_time": isotime(declared), "issuer": "wamason.com", "manifest_sha256": "a" * 64,
              "preamble_sha256": "b" * 64, "profile": "tessera-v1-strict",
              "spec": {"id": "tessera-v1-strict/verification-spec/1", "sha256": "c" * 64}, "vectors_sha256": "d" * 64}
    return frame("tessera-v1/attest", jcs({"common": common, "signer": {"key_fp": key_fp}}))


def manifest(gpg_fp, alg=ALG):
    return frame("tessera-v1/manifest", jcs({"alg": alg, "issuer": "wamason.com", "key_fp": "spki-sha256:" + "e" * 64,
                                             "sset": [gpg_fp], "ver": "map-v1"}))


class Env:
    def __init__(self):
        self.clock = Clock(T0)
        self.sqs, self.s3, self.kms = FakeSqs(self.clock), FakeS3(), FakeKms(KEY_VERSION)
        self.key_body = openpgp.key_body(openpgp.point65(self.kms.key.public_key()), KEY_CREATED)
        self.fp = openpgp.fp_gpg(self.key_body)
        self.logs = []
        self.cfg = self.config()
        self.signer = self.make_signer()

    def config(self, **kw):
        base = dict(request_queue_url=REQ, response_queue_url=RESP, frame_bucket=BUCKET, key_version=KEY_VERSION,
                    key_created=KEY_CREATED, key_fp=self.fp, sign_until=SIGN_UNTIL, aws_role_arn="arn:aws:iam::1:role/r",
                    aws_audience="aud", image="test", budget_s=40, wait_s=0, visibility_s=120)
        base.update(kw)
        return Config(**base)

    def make_signer(self, cfg=None, kms=None):
        s = Signer(cfg or self.cfg, kms or self.kms, self.sqs, self.s3, self.clock, time.monotonic,
                   lambda **f: self.logs.append(f))
        s.load_key()
        return s

    def enqueue(self, msg):
        body = msg if isinstance(msg, str) else json.dumps(msg, sort_keys=True)
        return self.sqs.send_message(QueueUrl=REQ, MessageBody=body)["MessageId"]

    def inline(self, data, rid="req-1", sign_by=None):
        return self.enqueue({"request_id": rid, "frame_b64": base64.b64encode(data).decode(),
                             "sign_by": isotime(SIGN_UNTIL if sign_by is None else sign_by)})

    def by_ref(self, data, rid="req-1", sign_by=None, stored=None, digest=None):
        digest = digest or hashlib.sha256(data).hexdigest()
        ref = f"frames/rid-1/{digest}"
        if stored is not False:
            self.s3.put(BUCKET, ref, data if stored is None else stored)
        return self.enqueue({"request_id": rid, "frame_ref": ref, "frame_sha256": digest,
                             "sign_by": isotime(SIGN_UNTIL if sign_by is None else sign_by)})

    def run(self):
        return self.signer.run()

    def responses(self):
        return self.sqs.take(RESP)

    def one(self):
        self.run()
        out = self.responses()
        assert len(out) == 1, out
        return out[0]

    def verifies(self, data, sig_b64):
        sig = base64.b64decode(sig_b64)
        parsed = parse_signature(sig, ALG, "gpg", registered_codecs(ALG))
        sig_policy(parsed)
        return signature_verifies(data, parsed, public_key(self.key_body, "gpg", ALG))

    def events(self, name):
        return [e for e in self.logs if e.get("event") == name]


@pytest.fixture
def env():
    return Env()
