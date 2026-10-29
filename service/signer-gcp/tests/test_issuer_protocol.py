"""Conformance with the issuer's side of the protocol, which is authoritative: the issuer's own SlotSigner builds the
requests (inline and IS-09 by reference, with sign_by), reads the responses, and verifies the signatures with the
service verifier, exactly as pipeline.drain does. Test-only use of service/issuer; the signer does not import it."""
import pytest
from tessera_issue.signers import INLINE_MAX, SlotSigner, request_id
from tessera_issue.util import b64d

from conftest import BUCKET, REQ, RESP, SIGN_UNTIL, T0, attest, manifest
from fakes import QueueView


@pytest.fixture
def issuer(env):
    return SlotSigner("gpg", env.key_body, QueueView(env.sqs, REQ), QueueView(env.sqs, RESP))


def stash_into(env):
    def stash(data):                                     # as pipeline._send: frames/<rid>/<sha256>
        from tessera_issue.util import sha256hex
        ref = f"frames/rid-7/{sha256hex(data)}"
        env.s3.put(BUCKET, ref, data)
        return ref
    return stash


def answers(issuer):
    return {body["request_id"]: body for _, body in issuer.receive(10)}


def test_issuer_fingerprint_matches_the_signers(env, issuer):
    assert issuer.fp == env.fp


@pytest.mark.parametrize("make", [lambda fp: attest(fp, T0), lambda fp: manifest(fp)])
def test_inline_request_round_trip(env, issuer, make):
    data = make(env.fp)
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data, sign_by=SIGN_UNTIL)
    env.run()
    body = answers(issuer)[rid]
    assert body["status"] == "SIGNED" and issuer.verify(data, b64d(body["sig_b64"]))


def test_reference_request_round_trip(env, issuer):
    data = attest(env.fp, T0, content={"statement": "y" * (INLINE_MAX + 1000)})
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data, sign_by=SIGN_UNTIL, stash=stash_into(env))
    (msg,) = env.sqs.bodies(REQ)
    assert "frame_ref" in msg and "frame_b64" not in msg   # the issuer chose the reference shape
    env.run()
    body = answers(issuer)[rid]
    assert body["status"] == "SIGNED" and issuer.verify(data, b64d(body["sig_b64"]))


def test_reference_to_a_replaced_object_is_refused(env, issuer):
    data = attest(env.fp, T0, content={"statement": "y" * (INLINE_MAX + 1000)})
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data, sign_by=SIGN_UNTIL, stash=stash_into(env))
    (msg,) = env.sqs.bodies(REQ)
    env.s3.put(BUCKET, msg["frame_ref"], attest(env.fp, T0, content={"statement": "z" * (INLINE_MAX + 1000)}))
    env.run()
    body = answers(issuer)[rid]
    assert body["status"] == "REFUSED" and body["reason"] == "FRAME_DIGEST_MISMATCH"


def test_issuer_request_without_sign_by_is_refused(env, issuer):
    """The issuer's SlotSigner allows sign_by=None; its pipeline always sends one. This signer requires it."""
    data = attest(env.fp, T0)
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data)
    env.run()
    body = answers(issuer)[rid]
    assert body["status"] == "REFUSED" and body["reason"] == "BAD_REQUEST" and env.kms.signed == []


def test_issuer_retry_of_the_same_frame_reuses_the_id_and_the_signature(env, issuer):
    data = attest(env.fp, T0)
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data, sign_by=SIGN_UNTIL)
    issuer.send(rid, data, sign_by=SIGN_UNTIL)
    env.run()
    got = [body for _, body in issuer.receive(10)]
    assert [b["request_id"] for b in got] == [rid, rid]
    assert got[0]["sig_b64"] == got[1]["sig_b64"] and len(env.kms.signed) == 1


def test_refusal_reasons_reach_the_issuer(env, issuer):
    data = attest(env.fp, T0 + 2 * 86400)
    rid = request_id("rid-7", "gpg", data)
    issuer.send(rid, data, sign_by=SIGN_UNTIL)
    env.run()
    body = answers(issuer)[rid]
    assert (body["status"], body["reason"]) == ("REFUSED", "DECLARED_TIME_OUTSIDE_EPSILON")
