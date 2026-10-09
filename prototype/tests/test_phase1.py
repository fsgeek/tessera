"""Phase 1 tests: honest flow, both attack pairs (correct rejects / mutated accepts), and a few
spec-derived negative cases. THROWAWAY."""
import copy

import pytest

from tessera_proto import attacks, frame, jcs, objects
from tessera_proto.crypto import KeyPair, b64d, b64e
from tessera_proto.issuer import ChainSchedule, Params, anchor_layer, build_attest_layer
from tessera_proto.verifier import Mutations, Policy, PolicyError, verify_bundle
from tessera_proto.world import T0, make_world

HOUR = 3600


@pytest.fixture
def honest():
    w = make_world()
    r = w.issuer.issue(b'{"claim": "the minutes of 2026-10-06", "pages": 3}', T0)
    assert r.disposition == "SHIPPED"
    return w, r


def L(rep, i=0):
    return rep["layers"][i]


# ---------------------------------------------------------------- honest flow

def test_honest_issue_verify_valid_strict_and_established(honest):
    w, r = honest
    rep = verify_bundle(r.shipped, w.trust())
    assert L(rep)["verification"] == "VALID_STRICT", L(rep)["failed"] + L(rep)["unperformable"]
    assert L(rep)["protocol_standing"]["value"] == "ESTABLISHED"
    assert L(rep)["protocol_standing"]["reason"] == "TERMINAL_DISPOSITION_SHOWN"
    # same bundle twice, same verdict (P9 vector shape)
    assert verify_bundle(r.shipped, w.trust()) == rep


def test_honest_degraded_policy_records_waiver_observation(honest):
    w, r = honest
    rep = verify_bundle(r.shipped, w.trust(), attacks.DEGRADED_SOLE_DNS)
    assert L(rep)["verification"] == "VALID_DEGRADED(policy=degraded-waive-repo)"
    assert L(rep)["waivers"]["channel:repo"]["observation"] == "would-pass"


def test_honest_wrapper_both_layers_valid(honest):
    w, r = honest
    skW = KeyPair.generate("skW")
    inner = r.shipped["layers"][0]
    emb = [{"slot": s["slot"], "frame_b64": s["frame_b64"], "sig_b64": s["sig_b64"]} for s in inner["slots"]]
    now = T0 + 10 * HOUR
    outer = build_attest_layer(object_type="OT_WRAPPER", content={"renewal": 1}, declared=now, issuer_id="wamason.com",
                               slot_keys=[skW], channels=[w.dns, w.repo],
                               extra_common={"inner": {"cv": 1, "slots": emb}, "outer_cv": 1})
    outer["anchor"] = anchor_layer(outer, w.chain, now, ChainSchedule(), w.params.k)
    inner_entry = {"object_type": "OT_ATTEST", "manifest": inner["manifest"], "anchor": inner["anchor"],
                   "slots": [{k: s[k] for k in ("slot", "alg", "pubkey_b64")} for s in inner["slots"]]}
    b = {"layers": [outer, inner_entry], "embedded": objects.embedded_objects()}
    rep = verify_bundle(b, w.trust())
    assert [x["verification"] for x in rep["layers"]] == ["VALID_STRICT", "VALID_STRICT"]


# ---------------------------------------------------------------- C-C2 pair

def test_cc02_correct_verifier_rejects(honest):
    w, r = honest
    rp = attacks.replay_cc02(w, r.shipped, T0 + 2 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS)
    assert L(rep)["verification"] == "INVALID"
    assert {"V17[A]", "V18[A]"} <= set(L(rep)["failed"])
    assert not attacks.judge_reattributed(rep, rp)


def test_cc02_mutated_verifier_accepts(honest):
    w, r = honest
    rp = attacks.replay_cc02(w, r.shipped, T0 + 2 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, Mutations(drop_frame_pin_and_mh=True))
    assert L(rep)["verification"].startswith("VALID_DEGRADED")
    assert attacks.judge_reattributed(rep, rp)  # ReattributedA fires


def test_cc02_mutated_strict_mode_not_valid(honest):
    w, r = honest
    rp = attacks.replay_cc02(w, r.shipped, T0 + 2 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), Policy(), Mutations(drop_frame_pin_and_mh=True))
    assert L(rep)["verification"] == "UNVERIFIABLE"  # repo evidence absent; attacker holds only skS


def test_cc02_mutated_but_too_late_is_temporally_invalid(honest):
    """Concrete-only defence: the honest frame carries its declared time, so a replay
    anchored after declared + δ fails V34/V35 even in the mutant. The model has no time."""
    w, r = honest
    rp = attacks.replay_cc02(w, r.shipped, T0 + 80 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, Mutations(drop_frame_pin_and_mh=True))
    assert L(rep)["verification"] == "INVALID"
    assert "V34" in L(rep)["failed"]


# ---------------------------------------------------------------- C-C5 pair

def test_cc05_correct_verifier_rejects_inner(honest):
    w, r = honest
    rp = attacks.replay_cc05(w, r.shipped, T0 + 2 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, dsks=rp.dsks)
    assert L(rep, 1)["verification"] == "INVALID"
    assert L(rep, 1)["failed"] == ["V19[A]"]
    # registered degraded cost: the attacker's OWN wrapper layer verifies, degraded
    assert L(rep, 0)["verification"].startswith("VALID_DEGRADED")
    assert not attacks.judge_inner_sig_transplanted(rep, rp)


def test_cc05_mutated_verifier_accepts_with_emulated_dsks(honest):
    w, r = honest
    rp = attacks.replay_cc05(w, r.shipped, T0 + 2 * HOUR)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS,
                        Mutations(unbind_signature_bytes=True), dsks=rp.dsks)
    assert L(rep, 1)["verification"].startswith("VALID_DEGRADED")
    assert attacks.judge_inner_sig_transplanted(rep, rp)  # InnerSigTransplanted fires
    assert ("dsks-accepted", True) in rp.dsks.uses


def test_cc05_mutated_without_dsks_rejects(honest):
    w, r = honest
    rp = attacks.replay_cc05(w, r.shipped, T0 + 2 * HOUR, use_dsks=False)
    rep = verify_bundle(rp.bundle, w.trust(), attacks.DEGRADED_SOLE_DNS, Mutations(unbind_signature_bytes=True))
    assert L(rep, 1)["verification"] == "INVALID"


# ---------------------------------------------------------------- standing S2/S3/S4

def test_standing_superseded_and_refused():
    w = make_world()
    late = ChainSchedule(inclusion_delay=70 * HOUR, block_interval=HOUR)   # in-window anchor, late burial
    r = w.issuer.issue(b'{"x":"y"}', T0, [late, ChainSchedule()])
    assert [a.predicate_ok for a in r.attempts] == [False, True]
    rep = verify_bundle(r.attempts[0].bundle, w.trust())
    assert L(rep)["verification"] == "INVALID" and "V35" in L(rep)["failed"]
    assert L(rep)["protocol_standing"]["reason"] == "SUPERSEDED"
    alone = copy.deepcopy(r.attempts[0].bundle)
    alone.pop("standing")
    assert L(verify_bundle(alone, w.trust()))["protocol_standing"]["reason"] == "NO_TERMINAL_DISPOSITION_EVIDENCE"

    w2 = make_world()
    r2 = w2.issuer.issue(b'{"x":"y"}', T0, [late])
    assert r2.disposition == "REFUSED"
    rep = verify_bundle(r2.attempts[-1].bundle, w2.trust())
    assert L(rep)["protocol_standing"]["reason"] == "ISSUANCE_REFUSED"


# ---------------------------------------------------------------- spec negative cases

@pytest.mark.parametrize("raw,code", [
    (b'{"a":1,"a":2}', "P8_DUPLICATE_NAME"),
    (b'{"a":NaN}', "P8_NAN_INFINITY"),
    (b'{"a":0.1}', "P8_NUMBER_NOT_DOUBLE"),
    (b'{"a":-0}', "P8_NEGATIVE_ZERO"),
    (b'{"a":9007199254740993}', "P8_NUMBER_NOT_DOUBLE"),
    (b'{"a":"\\ud800"}', "P8_NON_IJSON_STRING"),
    (b'{"a":"e\xcc\x81"}', "P8_UNICODE_NORMALIZATION"),
    (b'{"a":1} x', "P8_TRAILING_BYTES"),
])
def test_ingestion_rejects(raw, code):
    w = make_world()
    with pytest.raises(jcs.CanonicalizationRejected) as e:
        w.issuer.issue(raw, T0)
    assert e.value.code == code


def test_tampered_payload_invalid(honest):
    w, r = honest
    b = copy.deepcopy(r.shipped)
    s = b["layers"][0]["slots"][0]
    fb = bytearray(b64d(s["frame_b64"]))
    fb[-3] ^= 1
    s["frame_b64"] = b64e(bytes(fb))
    assert L(verify_bundle(b, w.trust()))["verification"] == "INVALID"


def test_missing_headers_unverifiable(honest):
    w, r = honest
    b = copy.deepcopy(r.shipped)
    b["layers"][0]["anchor"]["headers"] = b["layers"][0]["anchor"]["headers"][:2]
    rep = verify_bundle(b, w.trust())
    assert L(rep)["verification"] == "UNVERIFIABLE" and "V37" in L(rep)["unperformable"]


def test_canary_unknown_algorithm_unverifiable():
    w = make_world()
    k = KeyPair.generate("canary")
    k.alg = "TESSERA-RESERVED-UNRECOGNIZED-0"
    lay = build_attest_layer(object_type="OT_ATTEST", content={"c": 1}, declared=T0, issuer_id="wamason.com",
                             slot_keys=[k], channels=[w.dns, w.repo], alg="TESSERA-RESERVED-UNRECOGNIZED-0")
    for s in lay["slots"]:
        s["alg"] = "TESSERA-RESERVED-UNRECOGNIZED-0"
    lay["anchor"] = anchor_layer(lay, w.chain, T0, ChainSchedule(), w.params.k)
    rep = verify_bundle({"layers": [lay]}, w.trust(), evaluate_standing=False)
    # Fingerprint, signature and possession checks are unperformable -> UNVERIFIABLE (G-10b).
    assert L(rep)["verification"] == "UNVERIFIABLE", L(rep)["failed"]


def test_policy_cannot_waive_all_channels(honest):
    w, r = honest
    with pytest.raises(PolicyError):
        verify_bundle(r.shipped, w.trust(), Policy(name="x", waive_channels=frozenset({"dns", "repo"})))


def test_revocation_in_window_invalid(honest):
    w, r = honest
    rep = verify_bundle(r.shipped, w.trust(revocations={w.skB2.fp: T0 + 60}))
    assert L(rep)["verification"] == "INVALID" and "REV[B]" in L(rep)["failed"]


def test_degraded_cost_content_copy_under_leaked_channel_is_valid_degraded(honest):
    """Not an attack replay: the REGISTERED degraded cost (R-1.11, R-5.32). With the sole required
    channel's key leaked, an attacker frames the honest CONTENT under its own key and the honest
    issuer id. The correct verifier says VALID_DEGRADED and records repo evidence `absent`.
    Strict mode says UNVERIFIABLE. Kept here because phase 2's relying party must read this."""
    w, r = honest
    a = KeyPair.generate("attacker")
    content = jcs.parse_strict(frame.decode(b64d(r.shipped["layers"][0]["slots"][0]["frame_b64"]))[0].payload)["common"]["content"]
    from tessera_proto.issuer import Channel
    lay = build_attest_layer(object_type="OT_ATTEST", content=content, declared=T0 + HOUR, issuer_id="wamason.com",
                             slot_keys=[a], channels=[Channel("dns", w.dns.key)])
    lay["anchor"] = anchor_layer(lay, w.chain, T0 + HOUR, ChainSchedule(), w.params.k)
    b = {"layers": [lay]}
    rep = verify_bundle(b, w.trust(), attacks.DEGRADED_SOLE_DNS)
    assert L(rep)["verification"].startswith("VALID_DEGRADED")
    assert L(rep)["waivers"]["channel:repo"]["observation"] == "absent"
    assert L(rep)["protocol_standing"]["reason"] == "NO_TERMINAL_DISPOSITION_EVIDENCE"
    assert L(verify_bundle(b, w.trust()))["verification"] == "UNVERIFIABLE"
