"""Both production signers behind the issuer's real pipeline (ISI-01, docs/reviews/issuer-signer-interface/).

test_issuer_protocol.py builds its own frames and frame references, so a change on the issuer's side (2026-10-30: an
attempt-prefixed frame name that both signers refuse) could pass it. Here the issuer's own pipeline produces every
frame, reference and request, and the slot-2 signer and the KMS signer answer, with fake provider clients only.
Test-only use of service/issuer and service/signer-kms; the signer does not import either."""
import io
import json
import sys
import time
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "service" / "signer-kms"))
sys.path.insert(0, str(ROOT / "service" / "issuer" / "tests"))

from tessera_issue import api, local                                   # noqa: E402
from tessera_sign_kms.signer import KmsSigner                           # noqa: E402

from tessera_signer.main import Config                                 # noqa: E402
from tessera_signer.signer import Signer                               # noqa: E402

from conftest import VERIFIER_CLI                                       # noqa: E402
from fakes import ClientError, Clock, FakeKms, FakeSqs, QueueView      # noqa: E402

FROZEN = ROOT / "formal" / "freeze-v1" / "objects"


def _kms_fakes():
    import importlib.util
    spec = importlib.util.spec_from_file_location("kms_fakes", ROOT / "service" / "signer-kms" / "tests" / "fakes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class IssuerQueues:
    """The SQS calls the slot-2 signer makes, over the issuer's own in-memory slot queues."""

    def __init__(self, requests, responses):
        self.q = {"req": requests, "resp": responses}

    def receive_message(self, QueueUrl, MaxNumberOfMessages=10, **kw):
        return {"Messages": [{"MessageId": m.id, "Body": m.body, "ReceiptHandle": m.handle,
                              "Attributes": {"ApproximateReceiveCount": str(m.receives)}}
                             for m in self.q[QueueUrl].receive(MaxNumberOfMessages)]}

    def send_message(self, QueueUrl, MessageBody):
        return {"MessageId": self.q[QueueUrl].send(MessageBody)}

    def delete_message(self, QueueUrl, ReceiptHandle):
        self.q[QueueUrl].delete(ReceiptHandle)


class IssuerResults:
    """S3 get_object over the issuer's result store, where the pipeline stashes large frames."""

    def __init__(self, store):
        self.store = store

    def get_object(self, Bucket, Key):
        assert Bucket == "results"
        data = self.store.get_ref(Key)
        if data is None:
            raise ClientError("NoSuchKey")
        return {"Body": io.BytesIO(data), "ContentLength": len(data)}


class Slot2Worker:
    def __init__(self, signer):
        self.signer = signer

    def process(self):
        return self.signer.run()


class KmsWorker:
    def __init__(self, signer, slot):
        self.signer, self.slot = signer, slot

    def process(self):
        n = 0
        for m in self.slot.requests.receive(10):
            self.slot.responses.send(json.dumps(self.signer.handle(m.body, m.receives, m.id)))
            self.slot.requests.delete(m.handle)
            n += 1
        return n


@pytest.mark.parametrize("size", [20, 1 << 20], ids=["inline", "by-reference-1MiB"])
def test_both_production_signers_complete_a_pipeline_issuance(tmp_path, size):
    loc = local.build(FROZEN)
    iss, gpg_key = loc.iss, loc.world.gpg_key
    gpg_slot, kms_slot = iss.signers["gpg"], iss.signers["kms"]
    hsm = FakeKms("test-version", key=gpg_key._priv)
    cfg = Config("req", "resp", "results", "test-version", gpg_key.created, gpg_key.fp_gpg, iss.window.sign_until,
                 "test", "test", wait_s=0)
    slot2 = Signer(cfg, hsm, IssuerQueues(gpg_slot.requests, gpg_slot.responses), IssuerResults(iss.results),
                   loc.clock, time.monotonic, lambda **kw: None)
    slot2.load_key()
    kms = KmsSigner(_kms_fakes().FakeKms(loc.world.kms_key), "test", loc.world.kms_key.fp_kms,
                    iss.window.sign_until, iss.results.get_ref, loc.clock, lambda entry: None)
    loc.workers = {"gpg": Slot2Worker(slot2), "kms": KmsWorker(kms, kms_slot)}

    key = str(uuid.uuid4())
    api.submit(iss, "cred-A", key, b"x" * size)
    rec = loc.run_until_done(api.record_id("cred-A", key))
    assert rec["state"] == "COMPLETE", (rec["state"], rec.get("reason"))
    assert len(hsm.signed) == 2                                          # slot 2's attestation and the manifest
    if VERIFIER_CLI.exists():
        from helpers import fetch_receipt, verify_with_cli
        bundle, _ = fetch_receipt(loc, key)
        rc, report, err = verify_with_cli(loc, bundle, tmp_path)
        assert rc == 0 and report["stable"]["verdict"] == "VALID_STRICT", (rc, report, err[-2000:])


def test_queue_view_reports_the_actual_redelivery_count():
    clock = Clock(10)
    view = QueueView(FakeSqs(clock), "resp")
    view.send("{}")
    assert view.receive()[0].receives == 1
    clock.advance(61)                                                     # not acknowledged; visibility lapses
    assert view.receive()[0].receives == 2
