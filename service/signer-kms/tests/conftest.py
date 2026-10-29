import json
from pathlib import Path

import pytest

from tessera_issue.encode import common_metadata, encode_attest, encode_manifest
from tessera_issue.testkeys import MLDSA65Key, P256Key
from tessera_issue.util import FakeClock, b64e, rfc3339, ts
from tessera_sign_kms.signer import KmsSigner

from fakes import FakeKms, Log

ROOT = Path(__file__).resolve().parents[1]                 # service/signer-kms
REPO = ROOT.parents[1]
FROZEN = REPO / "formal" / "freeze-v1" / "objects"
VERIFIER_CLI = REPO / "service" / "verifier" / ".venv" / "bin" / "tessera-verify"

NOW = ts("2026-11-10T12:00:00Z")
STOP = ts("2026-11-28T00:00:00Z")                          # the configured signing stop
CATALOG = {"alg": "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256", "preamble_sha256": "a" * 64,
           "spec_sha256": "b" * 64, "vectors_sha256": "c" * 64}


class Ctx:
    def __init__(self):
        self.key, self.gpg = MLDSA65Key("signer-kms tests"), P256Key("signer-kms tests gpg")
        self.clock, self.kms, self.log, self.objects = FakeClock(NOW), FakeKms(self.key), Log(), {}
        self.signer = KmsSigner(self.kms, "alias/test", self.key.fp_kms, STOP, self.objects.get, self.clock, self.log)

    def manifest(self, kms_fp=None, **kw):
        return encode_manifest(kms_fp or self.key.fp_kms, self.gpg.fp_gpg, **kw)

    def attest(self, declared=None, key_fp=None, content=b"TEST content", alg=None):
        common = common_metadata(b64e(content), rfc3339(NOW if declared is None else declared), self.manifest(),
                                 dict(CATALOG, alg=alg) if alg else CATALOG)
        return encode_attest(common, key_fp or self.key.fp_kms)

    @staticmethod
    def body(frame, rid="req-0001", sign_by=STOP, **extra):
        msg = {"request_id": rid, "frame_b64": b64e(frame), "sign_by": rfc3339(sign_by), **extra}
        return json.dumps(msg, sort_keys=True)


@pytest.fixture
def ctx():
    return Ctx()
