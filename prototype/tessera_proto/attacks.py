"""Concrete replays of two symbolic attack traces (THROWAWAY).

C-C2 reattribution  -- formal/suite/capstone/proverif/dev/slice_probe/out/cap_cc02_d__depth0.cone__cq3a.out:888-959
C-C5 inner-signature transplant -- .../codex/cap_cc05_d__depth1.cone__cq4s.out:1290-1376 (dsks route)

Both traces are against MUTATED companions in DEGRADED mode with the sole required channel's
key (skS) public. Here: the dns stub channel's key is the leaked skS; policy waives `repo`.

Translation notes (see PHASE1-REPORT.md §Predictions item 4):
  * Symbolic `checksign(s, k)` RETURNS the signed message. Ed25519 has no message recovery, so
    C-C5's mutated `let (=BYTES, anyb) = checksign(sg, k)` has a concrete counterpart only if the
    presented structure carries the signed bytes separately from the frame that gets pin-checked.
    We give signature entries an optional attached `signed_bytes_b64` (JWS/COSE-attached style).
    The correct verifier never reads it; the mutant verifies over it.
  * `dsks(s, r)` is EMULATED with crypto.DSKSOracle. Not a real Ed25519 attack.
  * "Anchor anything" (A1.3 item 5): the attacker submits its own receipt digest to the stub chain.
    The concrete temporal window then constrains WHEN the replay can be done (see report).
"""
from __future__ import annotations

from dataclasses import dataclass

from . import objects
from .crypto import DSKSOracle, KeyPair, b64d, b64e
from .issuer import Channel, ChainSchedule, anchor_layer, build_attest_layer
from .verifier import Policy

DEGRADED_SOLE_DNS = Policy(name="degraded-waive-repo", waive_channels=frozenset({"repo"}))


@dataclass
class Replay:
    bundle: dict
    honest_frame: bytes
    honest_sig: bytes
    honest_pub: bytes
    attacker_keys: dict
    dsks: DSKSOracle | None = None


def honest_slot_B(bundle: dict) -> tuple[bytes, bytes, bytes]:
    s = [x for x in bundle["layers"][0]["slots"] if x["slot"] == "B"][0]
    return b64d(s["frame_b64"]), b64d(s["sig_b64"]), b64d(s["pubkey_b64"])


def replay_cc02(world, honest_bundle: dict, now: int, keygen=KeyPair.generate) -> Replay:
    """C-C2: re-sign the honest skB2 frame bytes UNCHANGED under attacker key a_2, present them in
    slot A of a two-signer tuple (a_2, [a_5]) whose authority evidence is minted with leaked skS.
    PHASE 3: `keygen` lets the attacker use keys of the honest frame's algorithm (default unchanged)."""
    fbB, sB, pubB = honest_slot_B(honest_bundle)
    a2, a5 = keygen("a_2"), keygen("a_5")
    alg = a2.alg
    leaked_skS = Channel("dns", world.dns.key)   # out(c, skS) at {17}
    # the trace's tuple: authTuple(issuerId2, fp(pk(a_2)), signers1(fp(pk(a_5))), algH, a_6)
    t = objects.authority_tuple(world.issuer.issuer_id, a2.fp, [a5.fp], alg, "map-v1")
    pf = objects.possession_frame(t)
    layer = {
        "object_type": "OT_ATTEST",
        "slots": [
            {"slot": "A", "alg": alg, "pubkey_b64": b64e(a2.pub_raw), "frame_b64": b64e(fbB),
             "sig_b64": b64e(a2.sign(fbB))},                       # honest bytes, attacker signature
            {"slot": "B", "alg": alg, "pubkey_b64": b64e(a5.pub_raw), "frame_b64": b64e(fbB),
             "sig_b64": b64e(a5.sign(fbB))},                       # trace leaves slot B's kfp/mh free
        ],
        "manifest": {
            "tuple": t,
            "evidences": [leaked_skS.evidence("STMT_DIGEST", t)],
            "possession": [{"key_fp": a2.fp, "sig_b64": b64e(a2.sign(pf))},
                           {"key_fp": a5.fp, "sig_b64": b64e(a5.sign(pf))}],
        },
    }
    layer["anchor"] = anchor_layer(layer, world.chain, now, ChainSchedule(), world.params.k)
    bundle = {"bundle_format": "tessera-proto-bundle/0", "layers": [layer], "embedded": objects.embedded_objects()}
    return Replay(bundle, fbB, sB, pubB, {"a_2": a2, "a_5": a5})


def replay_cc05(world, honest_bundle: dict, now: int, use_dsks: bool = True,
                inner_content=None, outer_content=None) -> Replay:
    """C-C5: derive kD = dsks(sH, r) from the honest skB2 signature sH; build a NEW inner frame
    pinned to kD with a manifest for kD (evidence minted with leaked skS, possession by kD);
    carry sH unchanged with that frame; wrap the pair under attacker outer key a_5."""
    fbB, sH, pubB = honest_slot_B(honest_bundle)
    oracle = DSKSOracle()
    algB = [x for x in honest_bundle["layers"][0]["slots"] if x["slot"] == "B"][0]["alg"]
    kD = oracle.derive(pubB, sH, "kD=dsks(sH,a_11)", algB) if use_dsks else KeyPair.generate("kD-no-dsks")
    a5 = KeyPair.generate("a_5")
    leaked_skS = Channel("dns", world.dns.key)
    inner = build_attest_layer(object_type="OT_ATTEST", content=inner_content or {"a_13": "attacker-chosen inner content"},
                               declared=now, issuer_id="a_10.attacker.example", slot_keys=[kD],
                               channels=[leaked_skS])
    new_inner_frame = inner["slots"][0]["frame_b64"]
    embedded = {"slot": "A", "frame_b64": new_inner_frame, "sig_b64": b64e(sH),   # sH unchanged
                "signed_bytes_b64": b64e(fbB)}                                     # attached honest bytes
    inner["anchor"] = anchor_layer(inner, world.chain, now, ChainSchedule(), world.params.k)
    inner_entry = {"object_type": "OT_ATTEST",
                   "slots": [{"slot": "A", "alg": "Ed25519", "pubkey_b64": b64e(kD.pub_raw)}],
                   "manifest": inner["manifest"], "anchor": inner["anchor"]}
    outer = build_attest_layer(object_type="OT_WRAPPER", content=outer_content or {"a_7": "attacker wrapper content"},
                               declared=now, issuer_id="a_4.attacker.example", slot_keys=[a5],
                               channels=[leaked_skS],
                               extra_common={"inner": {"cv": 1, "slots": [embedded]}, "outer_cv": 1})
    outer["anchor"] = anchor_layer(outer, world.chain, now, ChainSchedule(), world.params.k)
    bundle = {"bundle_format": "tessera-proto-bundle/0", "layers": [outer, inner_entry],
              "embedded": objects.embedded_objects()}
    return Replay(bundle, fbB, sH, pubB, {"kD": kD, "a_5": a5}, oracle)


# --- judges: concrete counterparts of the trace's goal events ---------------------------------

def _accepted(layer_result: dict) -> bool:
    return layer_result["verification"].startswith("VALID")


def judge_reattributed(report: dict, rp: Replay) -> bool:
    """ReattributedA(kX, kH, fb): framed bytes the honest key signed are ACCEPTED in a layer
    under a different key kX."""
    L = report["layers"][0]
    if not _accepted(L):
        return False
    s = [x for x in rp.bundle["layers"][0]["slots"] if x["slot"] == "A"][0]
    return b64d(s["frame_b64"]) == rp.honest_frame and b64d(s["pubkey_b64"]) != rp.honest_pub


def judge_inner_sig_transplanted(report: dict, rp: Replay) -> bool:
    """InnerSigTransplanted(kX, s): the honest inner signature s is accepted, at wrapped depth,
    under a key other than its signer's."""
    if len(report["layers"]) < 2 or not _accepted(report["layers"][1]):
        return False
    emb = rp.bundle["layers"][0]["slots"][0]
    inner_sig = None
    from . import frame, jcs
    common = jcs.parse_strict(frame.decode(b64d(emb["frame_b64"]))[0].payload)["common"]
    inner_sig = b64d(common["inner"]["slots"][0]["sig_b64"])
    inner_pub = b64d(rp.bundle["layers"][1]["slots"][0]["pubkey_b64"])
    return inner_sig == rp.honest_sig and inner_pub != rp.honest_pub
