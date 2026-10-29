"""Round trips with the issuer's own code (tessera_issue, imported by the tests only): SlotSigner.send -> the Lambda
handler -> SlotSigner.receive/verify, inline and by reference (IS-09); and a whole local issuance in which the kms
slot is answered by this signer (fake KMS over the window's TEST key) instead of the issuer's StandInSigner, driven
to COMPLETE and verified VALID_STRICT by the service verifier's CLI."""
import base64
import json
import os
import uuid

import pytest

from tessera_issue import api, local
from tessera_issue.queues import InMemoryQueue
from tessera_issue.signers import SlotSigner, request_id
from tessera_issue.stores import InMemoryResultStore
from tessera_sign_kms import lambda_app
from tessera_sign_kms.signer import KmsSigner

from conftest import FROZEN, STOP, VERIFIER_CLI
from fakes import FakeKms, Log


class EventSourceMapping:
    """What the SQS event source mapping does: receive a batch, invoke the handler, delete what did not fail."""

    def __init__(self, signer, requests, responses):
        self.signer, self.requests, self.responses, self.counts = signer, requests, responses, {}

    def process(self, limit=None):
        n = 0
        while True:
            msgs = self.requests.receive(10)
            if not msgs:
                return n
            recs = []
            for m in msgs:
                self.counts[m.id] = self.counts.get(m.id, 0) + 1
                recs.append({"messageId": m.id, "body": m.body,
                             "attributes": {"ApproximateReceiveCount": str(self.counts[m.id])}})
            out = lambda_app.handle_event(self.signer, self.responses, {"Records": recs})
            failed = {f["itemIdentifier"] for f in out["batchItemFailures"]}
            for m in msgs:
                if m.id not in failed:
                    self.requests.delete(m.handle)
                    n += 1


def test_slot_signer_round_trip_inline_and_by_reference(ctx):
    req, resp = InMemoryQueue(ctx.clock), InMemoryQueue(ctx.clock)
    issuer_side = SlotSigner("kms", ctx.key.spki, req, resp)
    results = InMemoryResultStore()
    ctx.signer.fetch = results.get_ref
    small, big = ctx.attest(), ctx.attest(content=b"z" * 400_000)

    def stash(data):
        from tessera_issue.util import sha256hex
        results.put("frames", "a" * 64, sha256hex(data), data)
        return results.ref("frames", "a" * 64, sha256hex(data))
    ids = {request_id("a" * 64, "kms", f): f for f in (small, big)}
    for rid, f in ids.items():
        issuer_side.send(rid, f, sign_by=STOP, stash=stash)
    assert "frame_ref" in json.loads(req.msgs["m2"]["body"])                 # the large frame went by reference
    assert EventSourceMapping(ctx.signer, req, resp).process() == 2
    got = issuer_side.receive(10)
    assert len(got) == 2
    for handle, body in got:
        assert body["status"] == "SIGNED"
        assert issuer_side.verify(ids[body["request_id"]], base64.b64decode(body["sig_b64"]))
        issuer_side.ack(handle)
    assert len(resp) == 0 and len(req) == 0


@pytest.mark.skipif(not VERIFIER_CLI.exists(), reason="service verifier CLI not installed")
@pytest.mark.parametrize("content", [b"TEST content signed through the KMS-slot policy signer", os.urandom(1 << 20)],
                         ids=["inline", "by-reference-1MiB"])
def test_local_issuance_with_this_signer_completes_and_verifies_valid_strict(tmp_path, content):
    import sys
    sys.path.insert(0, str(FROZEN.parents[2] / "service" / "issuer" / "tests"))
    from helpers import fetch_receipt, verify_with_cli
    loc = local.build(FROZEN)
    kms_slot = loc.iss.signers["kms"]
    log = Log()
    signer = KmsSigner(FakeKms(loc.world.kms_key), "alias/test", loc.world.kms_key.fp_kms, loc.iss.window.sign_until,
                       loc.iss.results.get_ref, loc.clock, log)
    loc.workers["kms"] = EventSourceMapping(signer, kms_slot.requests, kms_slot.responses)
    key = str(uuid.uuid4())
    api.submit(loc.iss, "cred-A", key, content)
    rec = loc.run_until_done(api.record_id("cred-A", key))
    assert rec["state"] == "COMPLETE", rec
    assert [e["event"] for e in log] == ["signed", "signed"]                  # f_kms and the manifest
    bundle, _ = fetch_receipt(loc, key)
    rc, report, err = verify_with_cli(loc, bundle, tmp_path)
    assert rc == 0 and report["stable"]["verdict"] == "VALID_STRICT", (rc, report, err[-2000:])
