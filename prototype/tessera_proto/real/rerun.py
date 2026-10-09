"""Item 5: the phase-2 consumers on the de-stubbed path, plus the cases only real mechanisms create.
THROWAWAY. Used by run_phase3.py and tests/test_phase3.py.

New cases (real mode only):
  m1  the honest complete receipt, after a mirror rewrote the UNHASHED subpacket area of slot B's
      OpenPGP signature (added a notation). Every signature still verifies.
  m2  the same receipt with slot A's ECDSA signature replaced by (r, n - s). Still verifies.
  m3  the same receipt with a possession proof's unhashed area rewritten.
In all three the bytes the issuer signed are unchanged, but the attempt core contains the signature
bytes (aid = h(t, ppf, sg, decl), R-3.25), so the derived attempt identity changes and the TLR no
longer names it.
"""
from __future__ import annotations

import copy

from .. import attacks
from ..crypto import b64d, b64e
from ..verifier import Mutations, Policy, verify_bundle
from . import openpgp as P
from .kms import P256_N

DEGRADED = attacks.DEGRADED_SOLE_DNS


def _rewrite_unhashed(sig_b64: str) -> str:
    s = P.parse_signature(b64d(sig_b64))
    note = b"\x80\x00\x00\x00" + (7).to_bytes(2, "big") + (6).to_bytes(2, "big") + b"seen-at" + b"mirror"
    return b64e(s.with_unhashed(s.unhashed_area + P.subpacket(20, note)).raw)


def _flip_s(sig_b64: str) -> str:
    s = P.parse_signature(b64d(sig_b64))
    return b64e(s.with_mpis([s.mpis[0], P256_N - s.mpis[1]]).raw)


def malleated(bundle: dict) -> dict[str, dict]:
    out = {}
    m1 = copy.deepcopy(bundle)
    sB = [x for x in m1["layers"][0]["slots"] if x["slot"] == "B"][0]
    sB["sig_b64"] = _rewrite_unhashed(sB["sig_b64"])
    out["m1"] = m1
    m2 = copy.deepcopy(bundle)
    sA = [x for x in m2["layers"][0]["slots"] if x["slot"] == "A"][0]
    sA["sig_b64"] = _flip_s(sA["sig_b64"])
    out["m2"] = m2
    m3 = copy.deepcopy(bundle)
    p0 = m3["layers"][0]["manifest"]["possession"][0]
    p0["sig_b64"] = _rewrite_unhashed(p0["sig_b64"])
    out["m3"] = m3
    return out


def extra_cases(sc):
    from consumers.scenarios import Case
    full = sc.cases["a"].bundle
    titles = {"m1": "honest receipt; slot-B OpenPGP unhashed area rewritten by a mirror",
              "m2": "honest receipt; slot-A ECDSA signature s -> n - s",
              "m3": "honest receipt; possession proof's unhashed area rewritten"}
    return {k: Case(k, titles[k], b, sc.honest_release, True,
                    "VALID_STRICT; standing ESTABLISHED by the TLR the issuer actually wrote")
            for k, b in malleated(full).items()}


def replay_pairs(sc) -> dict:
    """C-C2 and C-C5 against correct and mutated verifiers on the de-stubbed world."""
    w, full = sc.world, sc.cases["a"].bundle
    from ..world import T0
    out = {}
    from .gpg import KmsOpenPGPSlotKey
    # the attacker uses keys of the honest frame's algorithm (OpenPGP over P-256), held locally
    r2 = attacks.replay_cc02(w, full, T0 + 3 * 3600, keygen=KmsOpenPGPSlotKey.generate)
    tr = w.trust()
    ok = verify_bundle(r2.bundle, tr, DEGRADED)
    bad = verify_bundle(r2.bundle, tr, DEGRADED, Mutations(drop_frame_pin_and_mh=True))
    out["C-C2"] = (ok["layers"][0]["verification"], ok["layers"][0]["failed"],
                   bad["layers"][0]["verification"], attacks.judge_reattributed(bad, r2))
    r5 = attacks.replay_cc05(w, full, T0 + 3 * 3600)
    tr = w.trust()   # fresh header store: the replay mined new blocks
    ok = verify_bundle(r5.bundle, tr, DEGRADED, dsks=r5.dsks)
    bad = verify_bundle(r5.bundle, tr, DEGRADED, Mutations(unbind_signature_bytes=True), dsks=r5.dsks)
    out["C-C5"] = (ok["layers"][1]["verification"], ok["layers"][1]["failed"],
                   bad["layers"][1]["verification"], attacks.judge_inner_sig_transplanted(bad, r5))
    return out


def submitter_self_checks(sc) -> dict:
    """The at-ship receipt checked with the release the submitter held before submitting (stale header
    store), under the two V38 policies, and with a fresh release."""
    out = {}
    s = sc.submitter
    for pol in ("pin-every-header", "checkpoint+pow"):
        stale = s.trust
        old = stale.header_policy
        stale.header_policy = pol
        try:
            rep = verify_bundle(sc.cases["g"].bundle, stale)
        finally:
            stale.header_policy = old
        L0 = rep["layers"][0]
        out[f"stale/{pol}"] = (L0["verification"], L0["unperformable"], L0["checks"].get("V38", {}).get("reason"))
    rep = verify_bundle(sc.cases["g"].bundle, sc.trust())
    out["fresh/pin-every-header"] = (rep["layers"][0]["verification"], rep["layers"][0]["unperformable"], "")
    return out
