"""Successful signing, E-02 duplicate and late requests, startup checks and configuration."""
import base64
import hashlib

import pytest
from tessera_verify.codec import isotime, parse_signature, registered_codecs

from tessera_signer import openpgp
from tessera_signer.main import config_from_env, main
from tessera_signer.policy import ALG
from tessera_signer.signer import StartupError

from conftest import KEY_CREATED, KEY_VERSION, REQ, SIGN_UNTIL, T0, attest, manifest
from fakes import FakeKms


# ------------------------------------------------------------------------------------------ signing
def test_attest_inline_signed_and_verifies(env):
    data = attest(env.fp, T0)
    env.inline(data, rid="req-abc")
    r = env.one()
    assert r["status"] == "SIGNED" and r["request_id"] == "req-abc" and r["kind"] == "attest"
    assert env.verifies(data, r["sig_b64"])
    sig = base64.b64decode(r["sig_b64"])
    assert r["sig_sha256"] == hashlib.sha256(sig).hexdigest()
    assert r["frame_sha256"] == hashlib.sha256(data).hexdigest()
    assert r["signer"]["slot"] == "gpg" and r["signer"]["key_fp"] == env.fp
    assert len(env.kms.signed) == 1
    assert env.sqs.bodies(REQ) == []


def test_manifest_possession_signed(env):
    data = manifest(env.fp)
    env.inline(data)
    r = env.one()
    assert r["status"] == "SIGNED" and r["kind"] == "manifest" and env.verifies(data, r["sig_b64"])


def test_frame_ref_signed_over_the_referenced_bytes(env):
    data = attest(env.fp, T0, content={"statement": "x" * 400_000})     # too large for an inline message
    env.by_ref(data)
    r = env.one()
    assert r["status"] == "SIGNED" and env.verifies(data, r["sig_b64"])
    assert r["frame_sha256"] == hashlib.sha256(data).hexdigest()


def test_signature_does_not_verify_on_other_bytes(env):
    data = attest(env.fp, T0)
    env.inline(data)
    r = env.one()
    assert not env.verifies(data + b"x", r["sig_b64"])
    assert not env.verifies(attest(env.fp, T0 + 1), r["sig_b64"])


def test_signature_packet_layout(env):
    """Hashed {33 issuer fingerprint, 2 creation time = the clock read before signing}, unhashed {16 key id}."""
    env.clock.t = T0 + 77
    env.inline(attest(env.fp, T0))
    sig = parse_signature(base64.b64decode(env.one()["sig_b64"]), ALG, "gpg", registered_codecs(ALG))
    fpr = openpgp.v4_fingerprint(env.key_body)
    assert [(t, d) for t, _, d in sig.hashed] == [(33, b"\x04" + fpr), (2, (T0 + 77).to_bytes(4, "big"))]
    assert [(t, d) for t, _, d in sig.unhashed] == [(16, fpr[-8:])]


def test_every_signature_is_logged_before_its_response(env):
    data = attest(env.fp, T0)
    env.inline(data)
    env.run()
    events = [e["event"] for e in env.logs]
    assert events.index("signed") < events.index("response")
    (s,) = env.events("signed")
    (r,) = env.responses()
    assert s["sig_sha256"] == r["sig_sha256"] and s["frame_sha256"] == hashlib.sha256(data).hexdigest()


def test_a_run_answers_every_queued_request(env):
    for i in range(23):
        env.inline(attest(env.fp, T0 + i), rid=f"req-{i}")
    assert env.run() == 23
    out = env.responses()
    assert sorted(r["request_id"] for r in out) == sorted(f"req-{i}" for i in range(23))
    assert all(r["status"] == "SIGNED" for r in out)


# ------------------------------------------------------------------------------------------ E-02
def test_duplicate_request_in_one_run_gets_the_same_signature(env):
    """The issuer's retry reuses the request id; the second delivery is answered without a second signature."""
    data = attest(env.fp, T0)
    env.inline(data, rid="req-dup")
    env.inline(data, rid="req-dup")
    env.run()
    a, b = env.responses()
    assert a["status"] == b["status"] == "SIGNED" and a["sig_b64"] == b["sig_b64"]
    assert len(env.kms.signed) == 1
    assert len(env.events("signed")) == 1 and len(env.events("resent")) == 1


def test_same_request_id_with_other_frame_is_signed_separately(env):
    env.inline(attest(env.fp, T0), rid="req-x")
    env.inline(attest(env.fp, T0 + 1), rid="req-x")
    env.run()
    a, b = env.responses()
    assert a["sig_b64"] != b["sig_b64"] and len(env.kms.signed) == 2


def test_redelivery_after_a_failed_delete_signs_again_in_a_later_run(env):
    """No memory across runs: the response was sent but the request not deleted, so the next run answers again. Both
    signatures verify, carry the same request id, and are both logged; the issuer records the second as a
    duplicate."""
    data = attest(env.fp, T0)
    env.inline(data, rid="req-late")
    env.sqs.fail_delete = True
    env.run()
    env.sqs.fail_delete = False
    assert len(env.events("handle_error")) == 1
    env.clock.advance(env.cfg.visibility_s)
    env.signer = env.make_signer()                       # a new job execution
    env.run()
    a, b = env.responses()
    assert a["request_id"] == b["request_id"] == "req-late"
    assert env.verifies(data, a["sig_b64"]) and env.verifies(data, b["sig_b64"])
    assert len(env.events("signed")) == 2
    assert env.sqs.bodies(REQ) == []


def test_late_request_past_sign_by_is_refused_not_signed(env):
    """The issuer gave up on a request (sign_by passed); a signer that runs only afterwards refuses it."""
    data = attest(env.fp, T0)
    env.inline(data, rid="req-old", sign_by=T0 + 600)
    env.clock.advance(3600)
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"] == "SIGNING_STOPPED" and env.kms.signed == []


def test_failed_send_leaves_the_request_and_logs_the_signature(env):
    env.inline(attest(env.fp, T0))
    env.sqs.fail_send = True
    env.run()
    env.sqs.fail_send = False
    assert len(env.events("signed")) == 1 and env.responses() == []
    assert len(env.sqs.bodies(REQ)) == 1                 # redelivered after the visibility timeout


# ------------------------------------------------------------------------------------------ startup
@pytest.mark.parametrize("kw,match", [
    ({"name": KEY_VERSION.replace("/1", "/2")}, "key version"),
    ({"algorithm": "EC_SIGN_P384_SHA384"}, "algorithm"),
    ({"protection": "SOFTWARE"}, "protection level"),
])
def test_startup_refuses_a_different_key(env, kw, match):
    kms = FakeKms(kw.get("name", KEY_VERSION), kw.get("algorithm", "EC_SIGN_P256_SHA256"),
                  kw.get("protection", "HSM"), key=env.kms.key)
    with pytest.raises(StartupError, match=match):
        env.make_signer(kms=kms)


def test_startup_refuses_a_key_with_another_fingerprint(env):
    with pytest.raises(StartupError, match="fingerprint"):
        env.make_signer(kms=FakeKms(KEY_VERSION))        # a fresh key: the pinned fingerprint is not its own


def test_startup_refuses_a_wrong_creation_time(env):
    with pytest.raises(StartupError, match="fingerprint"):
        env.make_signer(cfg=env.config(key_created=KEY_CREATED + 1))


ENV = {"REQUEST_QUEUE_URL": REQ, "RESPONSE_QUEUE_URL": "https://sqs.test/r", "FRAME_BUCKET": "b",
       "KMS_KEY_VERSION": KEY_VERSION, "KEY_CREATED": str(KEY_CREATED), "KEY_FP": "gpg-sha256:" + "0" * 64,
       "SIGN_UNTIL": isotime(SIGN_UNTIL), "AWS_ROLE_ARN": "arn:aws:iam::1:role/r", "AWS_AUDIENCE": "aud"}


def test_config_from_env():
    c = config_from_env(ENV)
    assert c.sign_until == SIGN_UNTIL and c.key_created == KEY_CREATED and c.budget_s == 40
    assert c.aws_region == "us-east-2" and c.aws_chain_role_arn is None


@pytest.mark.parametrize("name", sorted(ENV))
def test_config_requires_every_variable(name):
    with pytest.raises(StartupError, match=name):
        config_from_env({k: v for k, v in ENV.items() if k != name})


@pytest.mark.parametrize("name,value", [
    ("SIGN_UNTIL", "2026-11-20"), ("SIGN_UNTIL", "2026-11-20T00:00:00+00:00"), ("KEY_FP", "spki-sha256:" + "0" * 64),
    ("KMS_KEY_VERSION", "projects/p/keyRings/r"), ("KEY_CREATED", "-1"), ("RUN_SECONDS", "0"),
])
def test_config_rejects_bad_values(name, value):
    with pytest.raises(StartupError, match=name):
        config_from_env({**ENV, name: value})


def test_main_exits_2_without_configuration(capsys):
    assert main({}) == 2
    assert "refuse_to_run" in capsys.readouterr().out


# ------------------------------------------------------------------------------------------ SG-01, SG-02
# docs/reviews/signers/CODEX-REVIEW.md. Every clock-dependent check runs on one reading taken after the frame is in
# hand and immediately before signing (or resending); a signature the HSM returns after a cutoff is withheld.
def test_SG01_signature_returned_after_sign_by_is_withheld(env):
    data = attest(env.fp, T0)
    env.inline(data, rid="req-slow", sign_by=env.clock() + 1)
    real = env.kms.sign_digest

    def slow(digest):
        env.clock.advance(2)
        return real(digest)
    env.kms.sign_digest = slow
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"] == "SIGNING_STOPPED" and "sig_b64" not in r
    assert len(env.events("withheld")) == 1                 # the HSM did sign: logged, never sent


def test_SG01_a_cached_signature_is_not_resent_after_sign_by(env):
    data = attest(env.fp, T0)
    env.inline(data, rid="req-dup", sign_by=env.clock() + 60)
    env.inline(data, rid="req-dup", sign_by=env.clock() + 60)
    first = env.signer.handle(env.sqs.receive_message(QueueUrl=REQ, MaxNumberOfMessages=1)["Messages"][0])
    assert first["status"] == "SIGNED"
    env.clock.advance(120)
    second = env.signer.handle(env.sqs.receive_message(QueueUrl=REQ, MaxNumberOfMessages=1)["Messages"][0])
    assert second["status"] == "REFUSED" and second["reason"] == "SIGNING_STOPPED"


def test_SG02_epsilon_is_checked_after_a_slow_frame_fetch(env):
    data = attest(env.fp, env.clock() - 86400)               # exactly at the edge when the request arrives
    env.by_ref(data)
    real = env.s3.get_object

    def slow(**kw):
        env.clock.advance(60)
        return real(**kw)
    env.s3.get_object = slow
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"] == "DECLARED_TIME_OUTSIDE_EPSILON", r
    assert env.kms.signed == []
