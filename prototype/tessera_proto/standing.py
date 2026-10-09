"""Standing path (spec §6.3 R-6.24 steps, with R-6.24a's SC-3 rule). THROWAWAY.

Runs on the same bundle as the envelope path and inherits nothing from it (R-6.23): it
re-checks the authority evidence and the entitled key itself.
"""
from __future__ import annotations

from . import anchor_stub, frame, jcs, objects
from .crypto import b64d, fingerprint, verify as sig_verify

EST, ABS, UNV = "ESTABLISHED", "ABSENT", "UNVERIFIABLE"


def _r(value, reason, **kw):
    return {"value": value, "reason": reason, **kw}


def standing_path(layer: dict, slot_material: list[dict], se: dict | None, trust, policy) -> dict:
    man = layer.get("manifest") or {}
    t = man.get("tuple")
    # step 1: authority evidence binds this exact tuple -- under the channels the policy requires
    # GUESS G-34: the model has one channel key; with two we require every non-waived channel's
    # STMT_DIGEST evidence. If the path cannot proceed, the model emits NO report; a real output
    # must say something, so we emit value None with an invented reason.
    try:
        req = [c for c in trust.channel_keys if c not in policy.waive_channels]
        for ch in req:
            ev = [e for e in man.get("evidences", []) if e.get("channel") == ch and e.get("form") == "STMT_DIGEST"]
            efb = b64d(ev[0]["frame_b64"])
            ok = sig_verify(trust.channel_alg, trust.channel_keys[ch], b64d(ev[0]["sig_b64"]), efb)
            fr, fails = frame.decode(efb)
            if not ok or fails or fr.payload != objects.evidence_payload("STMT_DIGEST", t):
                raise ValueError
    except Exception:
        return _r(None, "STANDING_NOT_EVALUATED_AUTHORITY_UNBOUND (prototype code, unregistered)")
    # step 2: tuple destructuring (done by evidence_payload above)
    # step 3: derive attempt identity from the core the verifier holds, never read from a label
    slots = {s.get("slot"): s for s in slot_material}
    try:
        common = jcs.parse_strict(frame.decode(b64d(slots["A"]["frame_b64"]))[0].payload)["common"]
        core = objects.attempt_core(t, [p["sig_b64"] for p in man.get("possession", [])],
                                    [slots[n]["sig_b64"] for n in sorted(slots)], common["declared_issue_time"])
    except Exception:
        return _r(UNV, "STANDING_EVIDENCE_MALFORMED", note="core underivable (prototype)")
    aid = objects.attempt_id(core)
    # step 4
    if not se:
        return _r(ABS, "NO_TERMINAL_DISPOSITION_EVIDENCE", aid=aid, presented_with_lineage=False)
    tlr = se.get("tlr") or {}
    try:
        kT = b64d(tlr["pubkey_b64"])
        kX = b64d(slots["A"]["pubkey_b64"])
    except Exception:
        return _r(UNV, "STANDING_EVIDENCE_MALFORMED", aid=aid)
    # step 5: entitled key, inside the standing path
    if fingerprint(tlr.get("alg", ""), kT) != t["key_fp"]:
        return _r(UNV, "STANDING_EVIDENCE_SIGNATURE_INVALID", aid=aid)
    # step 6: TLR key equals presented key (O-74: no outcome modelled; GUESS G-35)
    if kT != kX:
        return _r(UNV, "STANDING_EVIDENCE_SIGNATURE_INVALID", aid=aid, note="kT != kX (O-74 guess)")
    # step 7: TLR signature, tag TLR
    tfb = b64d(tlr["frame_b64"])
    tfr, tfails = frame.decode(tfb)
    if tfails or tfr.object_type != "OT_TLR" or not sig_verify(tlr.get("alg"), kT, b64d(tlr["sig_b64"]), tfb):
        return _r(UNV, "STANDING_EVIDENCE_SIGNATURE_INVALID", aid=aid)
    body = jcs.parse_strict(tfr.payload)
    if body.get("tag") != "TLR":
        return _r(UNV, "STANDING_EVIDENCE_SIGNATURE_INVALID", aid=aid)
    # step 8: anchor proof is over this TLR, and the A2.1 predicate against declared_terminal_time
    a = se.get("anchor") or {}
    if a.get("format") == "ots-bitcoin":   # PHASE 3: real OTS anchor for the TLR
        from .real import anchor as real_anchor
        try:
            ok = real_anchor.tlr_anchor_ok(a, tfb, objects.parse_ts(body["declared_terminal_time"]), trust)
        except Exception:
            ok = False
        if not ok:
            return _r(UNV, "STANDING_EVIDENCE_TEMPORAL_MISMATCH", aid=aid)
        a = None
    try:
        if a is None:
            raise StopIteration
        dterm = objects.parse_ts(body["declared_terminal_time"])
        hs = {x["height"]: x for x in a["headers"]}
        h = a["proof"]["height"]
        dig = objects.receipt_digest([tfb])
        ok = (a["proof"]["digest"] == dig
              and anchor_stub.merkle_root_from_path(a["proof"]["txid"], a["proof"]["path"]) == hs[h]["merkle_root"]
              and all(anchor_stub.header_hash(hs[x]) == trust.header_store.get(x) for x in range(h, h + trust.k)))
        at, ca = hs[h]["time"], hs[h + trust.k - 1]["time"]
        ok = ok and dterm - trust.epsilon <= at <= dterm + trust.delta and ca <= dterm + trust.delta
    except StopIteration:
        ok = True
    except Exception:
        ok = False
    if not ok:
        return _r(UNV, "STANDING_EVIDENCE_TEMPORAL_MISMATCH", aid=aid)
    # step 9: §A5.6 tuple pin -- the core is built from the presented tuple, so this is
    # structurally true here (see GUESSES G-24: the alias attack is not expressible).
    # step 10: lineage lookup
    lineage = body.get("lineage") or []
    entry = [e for e in lineage if e.get("aid") == aid]
    if not entry:
        return _r(ABS, "STANDING_EVIDENCE_MISMATCH", aid=aid)
    d = entry[0].get("disposition")
    term = body.get("terminal") or {}
    # R-6.24a, evaluated before step 11
    if term.get("kind") == "TERM_REFUSED" and d == "DISP_SHIPPED":
        return _r(UNV, "STANDING_EVIDENCE_MALFORMED", aid=aid)
    if d == "DISP_SHIPPED" and term.get("kind") == "TERM_SHIPPED" and term.get("aid") != aid:
        return _r(UNV, "STANDING_EVIDENCE_MALFORMED", aid=aid)
    # step 11
    if term.get("kind") == "TERM_REFUSED":
        return _r(ABS, "ISSUANCE_REFUSED", aid=aid, presented_with_lineage=True)
    if term.get("kind") != "TERM_SHIPPED":
        return _r(UNV, "STANDING_EVIDENCE_MALFORMED", aid=aid)
    if term.get("aid") != aid:
        return _r(ABS, "SUPERSEDED", aid=aid, presented_with_lineage=True)
    # step 12
    if d == "DISP_SHIPPED":
        return _r(EST, "TERMINAL_DISPOSITION_SHOWN", aid=aid, presented_with_lineage=True)
    return _r(UNV, "STANDING_EVIDENCE_MALFORMED", aid=aid)
