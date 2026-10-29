"""The policy signer on fake KMS and S3 clients: a successful signature, every policy refusal (none of which calls
KMS), the digest-bound frame reference (IS-09), the signing stop (IS-03), transient errors, and the start-up key
pin. Every signature and refusal must leave one structured log line."""
import base64
import json

import pytest

from tessera_issue.signers import verify_slot_signature
from tessera_issue.util import sha256hex, rfc3339
from tessera_sign_kms.signer import EPS, MAX_RECEIVES, KeyMismatch, KmsSigner, Retry, external_mu

from conftest import NOW, STOP
from fakes import ClientError, FakeKms


def answer(ctx, body, count=1):
    return ctx.signer.handle(body, count, "m-1")


def refused(ctx, body, reason, count=1):
    r = answer(ctx, body, count)
    assert r["status"] == "REFUSED" and r["reason"] == reason, r
    assert ctx.log[-1]["event"] == "refused" and ctx.log[-1]["reason"] == reason
    return r


# ------------------------------------------------------------------------------------------- success
@pytest.mark.parametrize("kind", ["attest", "manifest"])
def test_signs_a_frame_and_the_issuer_verifies_it(ctx, kind):
    frame = ctx.attest() if kind == "attest" else ctx.manifest()
    r = answer(ctx, ctx.body(frame, rid="req-abc"))
    assert r["status"] == "SIGNED" and r["request_id"] == "req-abc" and r["frame_sha256"] == sha256hex(frame)
    sig = base64.b64decode(r["sig_b64"])
    assert verify_slot_signature("kms", ctx.key.spki, frame, sig)          # the issuer's own check
    assert ctx.kms.signs == [external_mu(ctx.key.spki[22:], frame)]       # KMS saw mu, never the frame
    line = ctx.log[-1]
    assert line["event"] == "signed" and line["kind"] == kind and line["request_id"] == "req-abc"
    assert line["frame_sha256"] == sha256hex(frame) and line["signature_sha256"] == sha256hex(sig)
    assert line["message_id"] == "m-1" and r["signer"]["key_fp"] == ctx.key.fp_kms


def test_log_lines_are_json_serialisable(ctx):
    answer(ctx, ctx.body(ctx.attest()))
    answer(ctx, "not json")
    for line in ctx.log:
        json.dumps(line)


# ------------------------------------------------------------------------------------------- request shape
@pytest.mark.parametrize("body,rid", [
    ("not json", None),
    ("[1, 2]", None),
    (json.dumps({"request_id": "req-1", "frame_b64": "AAAA"}), "req-1"),                         # no sign_by (IS-03)
    (json.dumps({"request_id": "req-1", "frame_b64": "AAAA", "sign_by": "tomorrow"}), "req-1"),
    (json.dumps({"request_id": "req-1", "frame_b64": "AAB=", "sign_by": "2026-11-11T00:00:00Z"}), "req-1"),
    (json.dumps({"request_id": "bad id!", "frame_b64": "AAAA", "sign_by": "2026-11-11T00:00:00Z"}), None),
    (json.dumps({"request_id": "req-1", "frame_b64": "AAAA", "sign_by": "2026-11-11T00:00:00Z", "x": 1}), "req-1"),
    (json.dumps({"request_id": "req-1", "frame_b64": "AAAA", "frame_ref": "frames/r/" + "0" * 64,
                 "frame_sha256": "0" * 64, "sign_by": "2026-11-11T00:00:00Z"}), "req-1"),
])
def test_malformed_requests_are_refused_bad_request(ctx, body, rid):
    r = refused(ctx, body, "BAD_REQUEST")
    assert r["request_id"] == rid and ctx.kms.signs == []


def test_oversized_message_is_refused(ctx):
    refused(ctx, ctx.body(b"\x00" * (800 * 1024)), "BAD_REQUEST")
    assert ctx.kms.signs == []


# ------------------------------------------------------------------------------------------- frame policy
def test_frame_grammar(ctx):
    """Anything the service verifier's decoder rejects is refused with the decoder's code."""
    refused(ctx, ctx.body(b"\x05junk!" + b"\x00" * 10), "TAG_UNKNOWN")
    f = bytearray(ctx.attest())
    f[-2] ^= 0x80                                                            # no longer UTF-8 / canonical JSON
    truncated = ctx.attest()[:-1]
    for frame in (bytes(f), truncated, b""):
        r = answer(ctx, ctx.body(frame))
        assert r["status"] == "REFUSED" and r["reason"] not in ("BAD_REQUEST", "KEY_FP_MISMATCH"), r
    assert ctx.kms.signs == []


def test_attestation_for_another_key_is_refused(ctx):
    refused(ctx, ctx.body(ctx.attest(key_fp=ctx.gpg.fp_gpg)), "KEY_FP_MISMATCH")
    refused(ctx, ctx.body(ctx.attest(key_fp="spki-sha256:" + "0" * 64)), "KEY_FP_MISMATCH")
    assert ctx.kms.signs == []


def test_manifest_naming_another_kms_key_is_refused(ctx):
    refused(ctx, ctx.body(ctx.manifest(kms_fp="spki-sha256:" + "1" * 64)), "KEY_FP_MISMATCH")
    assert ctx.kms.signs == []


def test_non_hybrid_alg_is_refused(ctx):
    refused(ctx, ctx.body(ctx.manifest(alg="OPENPGP4-ECDSA-P256-SHA256")), "ALG_NOT_ALLOWED")
    refused(ctx, ctx.body(ctx.attest(alg="OPENPGP4-ECDSA-P256-SHA256")), "ALG_NOT_ALLOWED")
    assert ctx.kms.signs == []


@pytest.mark.parametrize("offset,ok", [(-EPS, True), (EPS, True), (-EPS - 1, False), (EPS + 1, False)])
def test_declared_time_epsilon(ctx, offset, ok):
    r = answer(ctx, ctx.body(ctx.attest(declared=NOW + offset)))
    if ok:
        assert r["status"] == "SIGNED", r
    else:
        assert r["status"] == "REFUSED" and r["reason"] == "DECLARED_TIME_OUTSIDE_EPSILON" and ctx.kms.signs == []


# ------------------------------------------------------------------------------------------- IS-03 signing stop
def test_sign_by_passed_is_refused(ctx):
    refused(ctx, ctx.body(ctx.attest(), sign_by=NOW - 1), "SIGNING_STOPPED")
    assert answer(ctx, ctx.body(ctx.attest(), sign_by=NOW))["status"] == "SIGNED"      # at sign_by: still allowed
    assert len(ctx.kms.signs) == 1


def test_configured_signing_stop_overrides_a_later_sign_by(ctx):
    ctx.clock.t = STOP + 1
    frame = ctx.attest(declared=STOP)
    r = refused(ctx, ctx.body(frame, sign_by=STOP + 3600), "SIGNING_STOPPED")
    assert "signing stop" in r["detail"] and ctx.kms.signs == []


def test_signature_returned_after_the_stop_is_withheld(ctx):
    sign = ctx.kms.sign

    def slow_sign(**kw):                                  # KMS answers after sign_by has passed
        out = sign(**kw)
        ctx.clock.advance(10)
        return out
    ctx.kms.sign = slow_sign
    r = refused(ctx, ctx.body(ctx.attest(), sign_by=NOW + 5), "SIGNING_STOPPED")
    assert "withheld" in r["detail"] and "sig_b64" not in r
    assert len(ctx.kms.signs) == 1 and ctx.log[-1]["signature_sha256"]       # the signature exists and is logged


# ------------------------------------------------------------------------------------------- IS-09 frame_ref
def ref_body(ctx, frame, rid="req-big", digest=None, ref=None):
    digest = digest or sha256hex(frame)
    return json.dumps({"request_id": rid, "frame_ref": ref or f"frames/{'d' * 64}/{digest}", "frame_sha256": digest,
                       "sign_by": rfc3339(STOP)}, sort_keys=True)


def test_frame_by_reference_is_signed(ctx):
    frame = ctx.attest(content=b"x" * 300_000)
    ctx.objects[f"frames/{'d' * 64}/{sha256hex(frame)}"] = frame
    r = answer(ctx, ref_body(ctx, frame))
    assert r["status"] == "SIGNED" and verify_slot_signature("kms", ctx.key.spki, frame, base64.b64decode(r["sig_b64"]))


def test_tampered_frame_ref_digest_is_refused(ctx):
    """The object at the reference is not the frame the issuer named: refused before KMS."""
    frame, other = ctx.attest(content=b"named"), ctx.attest(content=b"substituted")
    ctx.objects[f"frames/{'d' * 64}/{sha256hex(frame)}"] = other
    r = refused(ctx, ref_body(ctx, frame), "FRAME_DIGEST_MISMATCH")
    assert sha256hex(other) in r["detail"] and ctx.kms.signs == []


def test_frame_ref_must_name_its_digest_and_stay_in_frames(ctx):
    frame = ctx.attest()
    ctx.objects[f"frames/{'d' * 64}/{sha256hex(frame)}"] = frame
    refused(ctx, ref_body(ctx, frame, ref=f"frames/{'d' * 64}/{'0' * 64}"), "BAD_REQUEST")
    refused(ctx, ref_body(ctx, frame, ref=f"result/{'d' * 64}/{sha256hex(frame)}"), "BAD_REQUEST")
    refused(ctx, ref_body(ctx, frame, ref=f"frames/../{sha256hex(frame)}"), "BAD_REQUEST")
    refused(ctx, ref_body(ctx, frame, digest="A" * 64), "BAD_REQUEST")
    assert ctx.kms.signs == []


def test_missing_frame_object_is_refused(ctx):
    refused(ctx, ref_body(ctx, ctx.attest()), "FRAME_UNAVAILABLE")


def test_s3_error_is_retried_then_refused(ctx):
    def broken(ref):
        raise ClientError("SlowDown")
    ctx.signer.fetch = broken
    body = ref_body(ctx, ctx.attest())
    for n in range(1, MAX_RECEIVES):
        with pytest.raises(Retry):
            answer(ctx, body, n)
        assert ctx.log[-1]["event"] == "retry"
    refused(ctx, body, "SIGNING_ERROR", MAX_RECEIVES)


# ------------------------------------------------------------------------------------------- transient KMS errors
def test_kms_error_is_retried_then_refused(ctx):
    ctx.kms.fail = ClientError("KMSInternalException")
    body = ctx.body(ctx.attest())
    with pytest.raises(Retry):
        answer(ctx, body, 1)
    r = refused(ctx, body, "SIGNING_ERROR", MAX_RECEIVES)
    assert "KMSInternalException" in r["detail"]


def test_kms_signature_that_does_not_verify_is_never_sent(ctx):
    ctx.kms.tamper = lambda s: s[:-1] + bytes([s[-1] ^ 1])
    body = ctx.body(ctx.attest())
    with pytest.raises(Retry):
        answer(ctx, body, 1)
    assert ctx.log[-1]["event"] == "retry" and ctx.log[-1]["signature_sha256"]
    r = refused(ctx, body, "SIGNING_ERROR", MAX_RECEIVES)
    assert "sig_b64" not in r


def test_unexpected_error_does_not_drop_the_request(ctx):
    def boom(frame, now):
        raise KeyError("bug")
    ctx.signer.check_frame = boom
    with pytest.raises(Retry):
        answer(ctx, ctx.body(ctx.attest()), 1)
    refused(ctx, ctx.body(ctx.attest()), "INTERNAL_ERROR", MAX_RECEIVES)


# ------------------------------------------------------------------------------------------- start-up key pin
def test_signer_refuses_to_start_on_the_wrong_key(ctx):
    with pytest.raises(KeyMismatch):
        KmsSigner(ctx.kms, "k", "spki-sha256:" + "0" * 64, STOP, ctx.objects.get, ctx.clock, ctx.log)
    with pytest.raises(KeyMismatch):
        KmsSigner(ctx.kms, "k", "", STOP, ctx.objects.get, ctx.clock, ctx.log)
    with pytest.raises(KeyMismatch):
        KmsSigner(FakeKms(ctx.key, key_spec="ECC_NIST_P256"), "k", ctx.key.fp_kms, STOP, ctx.objects.get, ctx.clock,
                  ctx.log)
