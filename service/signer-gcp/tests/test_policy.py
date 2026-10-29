"""Every policy refusal, through a whole signer run on fake queues: the response is REFUSED with the reason, and the
HSM is never asked to sign."""
import base64
import json

import pytest
from tessera_verify.codec import frame, isotime, jcs

from tessera_signer.policy import EPS, MAX_BODY

from conftest import SIGN_UNTIL, T0, attest, manifest


def refused(env, reason):
    r = env.one()
    assert r["status"] == "REFUSED", r
    assert r["reason"] == reason, r
    assert "sig_b64" not in r
    assert env.kms.signed == []                         # nothing reached the HSM
    assert env.sqs.bodies("https://sqs.test/gpg-requests") == []   # the request is answered and deleted
    return r


# ------------------------------------------------------------------------------------------ malformed requests
@pytest.mark.parametrize("body", ["not json", "[1, 2]", "\"text\"", "null"])
def test_body_not_a_json_object(env, body):
    env.enqueue(body)
    assert refused(env, "BAD_REQUEST")["request_id"] is None


def test_body_over_the_sqs_maximum():
    """SQS itself rejects such a message; the signer checks anyway, before parsing."""
    from tessera_signer.policy import Refuse, load
    with pytest.raises(Refuse) as e:
        load(json.dumps({"request_id": "req-1", "pad": "x" * MAX_BODY}))
    assert e.value.code == "BAD_REQUEST"


@pytest.mark.parametrize("rid", [None, 7, "", "has space", "x" * 129, "req/1"])
def test_bad_request_id(env, rid):
    msg = {"frame_b64": base64.b64encode(attest(env.fp, T0)).decode(), "sign_by": isotime(SIGN_UNTIL)}
    if rid is not None:
        msg["request_id"] = rid
    env.enqueue(msg)
    assert refused(env, "BAD_REQUEST")["request_id"] is None


def _inline(env, **kw):
    msg = {"request_id": "req-1", "frame_b64": base64.b64encode(attest(env.fp, T0)).decode(),
           "sign_by": isotime(SIGN_UNTIL)}
    for k, v in kw.items():
        if v is None:
            msg.pop(k)
        else:
            msg[k] = v
    return msg


@pytest.mark.parametrize("change", [
    {"sign_by": None},                                   # sign_by is required
    {"sign_by": "2026-11-10 12:00:00"},
    {"sign_by": "2026-02-30T00:00:00Z"},
    {"sign_by": 1793000000},
    {"extra": 1},                                        # no other member
    {"frame_ref": "frames/r/" + "0" * 64},               # both shapes at once
    {"frame_b64": "not base64!"},
    {"frame_b64": "YWI"},                                # missing padding
    {"frame_b64": "YWJ="},                               # non-canonical: nonzero pad bits (decodes to b"ab")
    {"frame_b64": 5},
])
def test_bad_inline_request(env, change):
    env.enqueue(_inline(env, **change))
    r = refused(env, "BAD_REQUEST")
    assert r["request_id"] == "req-1"                    # a valid id is echoed, so the issuer can match it


@pytest.mark.parametrize("ref,digest", [
    ("result/r/" + "0" * 64, "0" * 64),                  # only frames/ may be named
    ("frames/r/" + "0" * 63, "0" * 64),
    ("frames/a/b/" + "0" * 64, "0" * 64),
    ("frames/r/" + "0" * 64, "0" * 63),
    ("frames/r/" + "0" * 64, "A" * 64),
])
def test_bad_frame_reference(env, ref, digest):
    env.enqueue({"request_id": "req-1", "frame_ref": ref, "frame_sha256": digest, "sign_by": isotime(SIGN_UNTIL)})
    refused(env, "BAD_REQUEST")
    assert env.s3.calls == []                            # nothing was read


# ------------------------------------------------------------------------------------------ the frame
def test_wrong_tag_receipt_anchor(env):
    env.inline(frame("tessera-v1/receipt-anchor-sig", jcs({"x": "y"})))
    refused(env, "TAG_MISMATCH")


def test_unknown_tag(env):
    env.inline(frame("tessera-v2/attest", jcs({"x": "y"})))
    refused(env, "TAG_UNKNOWN")


def test_truncated_frame(env):
    env.inline(attest(env.fp, T0)[:-1])
    refused(env, "TRUNCATED")


def test_empty_frame(env):
    env.inline(b"")
    refused(env, "TRUNCATED")


def test_trailing_bytes(env):
    env.inline(attest(env.fp, T0) + b"\x00")
    refused(env, "TRAILING")


def test_schema_violation(env):
    env.inline(frame("tessera-v1/attest", jcs({"common": {}, "signer": {"key_fp": env.fp}})))
    refused(env, "SCHEMA")


def test_noncanonical_payload(env):
    good = attest(env.fp, T0)
    payload = good[1 + good[0] + 6:]
    spaced = json.dumps(json.loads(payload), indent=1).encode()     # same value, not its RFC 8785 form
    env.inline(frame("tessera-v1/attest", spaced))
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"].startswith("JSON") and env.kms.signed == []


def test_attest_with_another_alg(env):
    env.inline(attest(env.fp, T0, alg="OPENPGP4-ECDSA-P256-SHA256"))
    refused(env, "ALG_NOT_ALLOWED")


def test_manifest_with_another_alg(env):
    env.inline(manifest(env.fp, alg="OPENPGP4-ECDSA-P256-SHA256"))
    refused(env, "ALG_NOT_ALLOWED")


def test_attest_naming_another_key(env):
    env.inline(attest("gpg-sha256:" + "1" * 64, T0))
    refused(env, "KEY_FP_MISMATCH")


def test_attest_naming_a_kms_key(env):
    env.inline(attest("spki-sha256:" + "1" * 64, T0))
    refused(env, "KEY_FP_MISMATCH")


def test_manifest_naming_another_key(env):
    env.inline(manifest("gpg-sha256:" + "1" * 64))
    refused(env, "KEY_FP_MISMATCH")


@pytest.mark.parametrize("offset", [EPS + 1, -(EPS + 1), 25 * 3600, -30 * 86400])
def test_declared_time_outside_epsilon(env, offset):
    env.inline(attest(env.fp, T0 + offset))
    r = refused(env, "DECLARED_TIME_OUTSIDE_EPSILON")
    assert r["signer"]["clock"] == isotime(T0)


@pytest.mark.parametrize("offset", [EPS, -EPS, 0])
def test_declared_time_at_epsilon_is_signed(env, offset):
    env.inline(attest(env.fp, T0 + offset))
    assert env.one()["status"] == "SIGNED"


# ------------------------------------------------------------------------------------------ IS-03 signing stop
def test_past_the_configured_signing_stop(env):
    env.clock.t = SIGN_UNTIL + 1
    env.inline(attest(env.fp, SIGN_UNTIL + 1), sign_by=SIGN_UNTIL + 3600)
    assert "configured signing stop" in refused(env, "SIGNING_STOPPED")["detail"]


def test_at_the_configured_signing_stop_is_signed(env):
    env.clock.t = SIGN_UNTIL
    env.inline(attest(env.fp, SIGN_UNTIL))
    assert env.one()["status"] == "SIGNED"


def test_past_the_requests_sign_by(env):
    env.inline(attest(env.fp, T0), sign_by=T0 - 1)
    assert "sign_by" in refused(env, "SIGNING_STOPPED")["detail"]


def test_at_sign_by_is_signed(env):
    env.inline(attest(env.fp, T0), sign_by=T0)
    assert env.one()["status"] == "SIGNED"


def test_stop_is_read_after_the_policy_checks(env):
    """The clock is read again immediately before the HSM call: a stop that passes while the request is checked
    still refuses."""
    ticks = iter([T0, T0 + 10])                         # handle() start, then the pre-sign read
    env.signer.clock = lambda: next(ticks, T0 + 10)
    env.inline(attest(env.fp, T0), sign_by=T0 + 5)
    refused(env, "SIGNING_STOPPED")


def test_manifest_has_no_declared_time_but_the_stop_still_applies(env):
    env.inline(manifest(env.fp), sign_by=T0 - 1)
    refused(env, "SIGNING_STOPPED")


# ------------------------------------------------------------------------------------------ IS-09 frame reference
def test_frame_ref_tampered_object(env):
    good = attest(env.fp, T0)
    tampered = attest(env.fp, T0, content={"statement": "something else"})
    env.by_ref(good, stored=tampered)
    r = refused(env, "FRAME_DIGEST_MISMATCH")
    assert "frame_sha256" not in r                      # the bytes it read are not named as the frame


def test_frame_ref_object_with_one_flipped_byte(env):
    good = attest(env.fp, T0)
    env.by_ref(good, stored=good[:-2] + bytes([good[-2] ^ 1]) + good[-1:])
    refused(env, "FRAME_DIGEST_MISMATCH")


def test_frame_ref_missing_object(env):
    env.by_ref(attest(env.fp, T0), stored=False)
    refused(env, "FRAME_UNAVAILABLE")


def test_frame_ref_read_from_the_configured_bucket_only(env):
    env.by_ref(attest(env.fp, T0))
    assert env.one()["status"] == "SIGNED"
    assert [b for b, _ in env.s3.calls] == ["issuer-results"]


def test_frame_ref_transient_error_retried_then_refused(env):
    env.s3.transient = 10
    env.by_ref(attest(env.fp, T0))
    for _ in range(2):                                  # deliveries 1 and 2: left on the queue, no response
        env.run()
        assert env.responses() == []
        env.clock.advance(env.cfg.visibility_s)
    refused(env, "FRAME_UNAVAILABLE")                   # delivery 3


def test_frame_ref_transient_error_then_success(env):
    env.s3.transient = 1
    data = attest(env.fp, T0)
    env.by_ref(data)
    env.run()
    assert env.responses() == []
    env.clock.advance(env.cfg.visibility_s)
    r = env.one()
    assert r["status"] == "SIGNED" and env.verifies(data, r["sig_b64"])


# ------------------------------------------------------------------------------------------ signer errors
def test_kms_error_retried_then_refused(env):
    env.kms.fail = 10
    env.inline(attest(env.fp, T0))
    for _ in range(2):
        env.run()
        assert env.responses() == []
        env.clock.advance(env.cfg.visibility_s)
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"] == "SIGNER_ERROR"


def test_bad_hsm_output_is_never_returned(env):
    env.kms.corrupt = True
    env.inline(attest(env.fp, T0))
    for _ in range(2):
        env.run()
        assert env.responses() == []
        env.clock.advance(env.cfg.visibility_s)
    r = env.one()
    assert r["status"] == "REFUSED" and r["reason"] == "SIGNER_ERROR" and "sig_b64" not in r


def test_unexpected_exception_refuses(env, monkeypatch):
    import tessera_signer.policy as policy

    def boom(*a):
        raise TypeError("decoder bug")
    monkeypatch.setattr(policy, "check_frame", boom)
    env.inline(attest(env.fp, T0))
    refused(env, "INTERNAL")
