"""Verifier following spec §5 (inputs, decision procedure (a)-(j), output) with §2.3 trust
configuration and §2.4 strict/degraded modes. THROWAWAY PROTOTYPE.

Pure function of (bundle, trust configuration, declared policy). No I/O, no network.

`Mutations` re-creates the two deliberately broken companions so the attack replays have a
red/green pair:
  * drop_frame_pin_and_mh  -- C-C2's companion: the in-bytes key-fingerprint pin (V17 `=fp(kX)`)
                              and the manifest-hash check (V18 `mh = h(t)`) are removed.
  * unbind_signature_bytes -- C-C5's companion: `let (=BYTES, anyb) = checksign(sg, k)`; the
                              signature is checked over whatever bytes it carries (an attached
                              message), never equated to the presented frame.
`dsks` is the TEST-ONLY DSKS emulation hook (crypto.DSKSOracle); it models an adversary
capability, so it is passed to BOTH correct and mutated verifiers.
"""
from __future__ import annotations

import binascii
from dataclasses import dataclass, field

from . import anchor_stub, frame, jcs, objects
from .crypto import (ALGS_KNOWN_UNSUPPORTED, ALGS_SUPPORTED, DSKSOracle, b64d, fingerprint, sha256_hex,
                     verify as sig_verify)

PASS, FAIL, UNPERF = "pass", "fail", "unperformable"
VALID_STRICT, VALID_DEGRADED, INVALID, UNVERIFIABLE = "VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"


@dataclass
class TrustConfig:
    channel_keys: dict[str, bytes]          # authority channel public keys (R-5.8, modelled)
    k: int = 6
    delta: int = 72 * 3600
    epsilon: int = 24 * 3600
    header_store: dict[int, str] = field(default_factory=dict)  # verifier-distributed header store (R-2.19)
    # GUESS G-27: revocation input. R-5.21 needs "no revocation effective at or before anchor_time"
    # but no bundle member or trust-config member carries revocation facts. Put here: fp -> time.
    revocations: dict[str, int] = field(default_factory=dict)
    channel_alg: str = "Ed25519"
    # PHASE 3: V38 policy for real headers (real/anchor.py). Unused by the stub anchor.
    header_policy: str = "pin-every-header"
    # G-17 EXPERIMENT (tests/test_g17.py, G17-REPORT.md). Two independent switches:
    #   binding_ids:   what the signed `binding_forms` identifiers name.
    #                  "forms"    -- statement forms STMT_DIGEST/STMT_DIRECT (spec l.792, R-4.30): the
    #                                spec-literal vocabulary; channels are all of channel_keys (V23).
    #                  "channels" -- authority-channel names (the reading TRIAGE finding 1 feared);
    #                                every evidence uses STMT_DIGEST.
    #   required_from: where strict's required set comes from.
    #                  "bundle"   -- the bundle's signed set (R-3.37 / V21 read literally).
    #                  "policy"   -- the verifier: channels = channel_keys; forms = policy_forms if
    #                                given, else the bundle's. V21 then only checks well-formedness.
    binding_ids: str = "forms"
    required_from: str = "bundle"
    policy_forms: frozenset | None = None


@dataclass
class Policy:
    name: str = "strict"
    waive_channels: frozenset = frozenset()   # P10: fewer than all external evidences
    waive_slots: frozenset = frozenset()      # P2: subset of the issue-time signature set
    delta: int | None = None                  # stricter-only overrides (R-2.20)
    epsilon: int | None = None


@dataclass
class Mutations:
    drop_frame_pin_and_mh: bool = False
    unbind_signature_bytes: bool = False


class PolicyError(ValueError):
    pass


class Checks:
    def __init__(self):
        self.m: dict[str, dict] = {}

    def add(self, cid: str, status: str, reason: str = "", group: str | None = None, **obs):
        # A check id may be recorded more than once; the worst outcome sticks (fail > unperf > pass).
        rank = {PASS: 0, UNPERF: 1, FAIL: 2}
        cur = self.m.get(cid)
        if cur is None or rank[status] > rank[cur["status"]]:
            self.m[cid] = {"status": status, "reason": reason, "group": group, **obs}

    def ok(self, cid: str) -> bool:
        return self.m.get(cid, {}).get("status") == PASS


def _expected_slot_names(n: int) -> list[str]:
    return ["A", "B"][:n] + [f"S{i}" for i in range(2, n)]


def _validate_policy(policy: Policy, trust: TrustConfig, n_slots_required: int):
    chans = set(trust.channel_keys)
    if not policy.waive_channels <= chans:
        raise PolicyError("waiver names an unknown channel")
    if chans and policy.waive_channels == chans:
        raise PolicyError("P10 waiver may be fewer, never zero (R-2.29)")
    if policy.delta is not None and policy.delta > trust.delta:
        raise PolicyError("no policy may enlarge δ (R-2.20)")
    if policy.epsilon is not None and policy.epsilon > trust.epsilon:
        raise PolicyError("no policy may enlarge ε (R-2.20)")


def _decode_payload(fb_payload: bytes, cks: Checks, sid: str, group: str):
    try:
        ok = jcs.is_canonical(fb_payload)
        cks.add(f"V6[{sid}]", PASS if ok else FAIL, "" if ok else "P8_NOT_CANONICAL", group)
        if not ok:
            return None
        v = jcs.parse_strict(fb_payload)
    except jcs.CanonicalizationRejected as e:
        cks.add(f"V6[{sid}]", FAIL, e.code, group)
        return None
    # GUESS G-28: payload schema failure is recorded under V6 (P8 domain) as INVALID.
    if not (isinstance(v, dict) and set(v) == {"common", "signer"} and isinstance(v["common"], dict)
            and isinstance(v["signer"], dict) and isinstance(v["signer"].get("key_fp"), str)):
        cks.add(f"V6[{sid}]", FAIL, "P8_PAYLOAD_SCHEMA", group)
        return None
    return v


def _tuple_ok(t) -> bool:
    return (isinstance(t, dict) and set(t) == {"issuer_id", "key_fp", "sset", "alg", "ver"}
            and all(isinstance(t[x], str) for x in ("issuer_id", "key_fp", "alg", "ver"))
            and isinstance(t["sset"], list) and all(isinstance(x, str) for x in t["sset"])
            and len(set([t["key_fp"], *t["sset"]])) == 1 + len(t["sset"]))


def _verify_layer(li: int, layer: dict, slot_material: list[dict], expected_type: str, trust: TrustConfig,
                  policy: Policy, mut: Mutations, dsks: DSKSOracle | None, cks: Checks) -> dict:
    """Stages (a)-(i) for one layer. Returns facts the standing path / wrapper handling need."""
    facts: dict = {"commons": {}}
    man = layer.get("manifest") or {}
    t = man.get("tuple")
    # (e) V22 manifest destructuring
    if not _tuple_ok(t):
        cks.add("V22", FAIL, "P10_TUPLE_MALFORMED")
        return facts
    cks.add("V22", PASS)
    facts["tuple"] = t
    req_fps = objects.slot_fps(t)
    names = _expected_slot_names(len(req_fps))
    _validate_policy(policy, trust, len(req_fps))
    if not set(policy.waive_slots) <= set(names) or set(policy.waive_slots) == set(names):
        raise PolicyError("P2 waiver must name a proper subset of the required slots")
    mh = objects.manifest_hash(t)

    # (f) V28 / V31 arity read from the signed tuple, never from what is presented
    presented = {s.get("slot"): s for s in slot_material}
    extra = [x for x in presented if x not in names]
    cks.add("V28", FAIL if extra or len(presented) != len(slot_material) else PASS,
            "P2_SIGNATURE_SET_EXTRA_OR_DUPLICATE" if extra else "")
    for name in names:
        if name not in presented:
            cks.add(f"V31[{name}]", FAIL, "P2_SIGNATURE_MISSING", f"slot:{name}", observation="absent")
        else:
            cks.add(f"V31[{name}]", PASS, "", f"slot:{name}")

    # binding forms (V21) are read from slot A's common after parse; collected below
    pf = objects.possession_frame(t)
    for i, name in enumerate(names):
        s = presented.get(name)
        g = f"slot:{name}"
        if s is None:
            continue
        try:
            fb = b64d(s["frame_b64"]); sig = b64d(s["sig_b64"]); pub = b64d(s["pubkey_b64"])
        except (KeyError, binascii.Error, ValueError):
            cks.add(f"V2[{name}]", FAIL, "P8_ENCODING", g)
            continue
        # (a) parse and P8 rejection
        try:
            fr, ffails = frame.decode(fb)
        except frame.FrameError as e:
            cks.add(f"V2[{name}]", FAIL, e.code, g)
            continue
        for cid, code in ffails:
            cks.add(f"{cid}[{name}]", FAIL, code, g)
        for cid in ("V1", "V2", "V3", "V5", "V8"):
            cks.add(f"{cid}[{name}]", PASS, "", g)
        # (b) V4 type tag = the tag the caller verifies against
        cks.add(f"V4[{name}]", PASS if fr.object_type == expected_type else FAIL,
                "" if fr.object_type == expected_type else "P7_TYPE_TAG_MISMATCH", g)
        pl = _decode_payload(fr.payload, cks, name, g)
        if pl is None:
            continue
        common, signer = pl["common"], pl["signer"]
        facts["commons"][name] = (fr, common, fb)

        # (c) algorithm identifier, inside the canonical payload (R-3.41)
        alg = common.get("alg")
        if not isinstance(alg, str) or not alg:
            cks.add(f"V15[{name}]", FAIL, "ALG_MISSING_OR_MALFORMED", g)
            continue
        if alg != t["alg"] or s.get("alg") != alg:
            cks.add(f"V13[{name}]", FAIL, "ALG_SUBSTITUTED", g)
        else:
            cks.add(f"V13[{name}]", PASS, "", g)
        alg_usable = alg in ALGS_SUPPORTED
        if alg in ALGS_KNOWN_UNSUPPORTED:
            cks.add(f"V14[{name}]", UNPERF, "ALG_KNOWN_UNSUPPORTED", g)
        elif not alg_usable:
            cks.add(f"V14[{name}]", UNPERF, "ALG_UNKNOWN", g)
        else:
            cks.add(f"V14[{name}]", PASS, "", g)

        # (d) key binding
        kfp = fingerprint(alg, pub)
        pins = [common.get("issuer_id") == t["issuer_id"], common.get("alg") == t["alg"]]
        if alg_usable:
            cks.add(f"V16[{name}]", PASS if kfp == req_fps[i] else FAIL,
                    "" if kfp == req_fps[i] else "KEY_FINGERPRINT_MISMATCH", g)
            if not mut.drop_frame_pin_and_mh:
                pins.append(signer.get("key_fp") == kfp)            # =fp(kX)
        else:
            # GUESS G-10b: the fingerprint function is algorithm-specific (G-10), so for an
            # algorithm the verifier does not know, fp(kX) cannot be computed: V16 and the
            # in-bytes =fp(kX) pin are unperformable, not failed.
            cks.add(f"V16[{name}]", UNPERF, "FINGERPRINT_UNDEFINED_FOR_ALG", g)
        cks.add(f"V17[{name}]", PASS if all(pins) else FAIL, "" if all(pins) else "P3_FRAME_BINDING_MISMATCH", g)
        if not mut.drop_frame_pin_and_mh:
            ok = common.get("manifest_hash") == mh                  # mh = h(t)
            cks.add(f"V18[{name}]", PASS if ok else FAIL, "" if ok else "P3_MANIFEST_HASH_MISMATCH", g)
        if alg_usable:
            if mut.unbind_signature_bytes and "signed_bytes_b64" in s:
                signed = b64d(s["signed_bytes_b64"])   # MUTANT: bytes never equated to fb
            else:
                signed = fb
            ok = sig_verify(alg, pub, sig, signed, dsks)
            cks.add(f"V19[{name}]", PASS if ok else FAIL, "" if ok else "P1_SIGNATURE_INVALID", g)
            # (e) V24 possession by the same key whose signature is accepted
            poss = {p.get("key_fp"): p.get("sig_b64") for p in man.get("possession", [])}
            psig = poss.get(kfp)
            if psig is None:
                cks.add(f"V24[{name}]", FAIL, "P10_POSSESSION_MISSING", g, observation="absent")
            else:
                ok = sig_verify(alg, pub, b64d(psig), pf, dsks)
                cks.add(f"V24[{name}]", PASS if ok else FAIL, "" if ok else "P10_POSSESSION_INVALID", g)
        else:
            for cid in ("V19", "V24"):
                cks.add(f"{cid}[{name}]", UNPERF, "ALG_NOT_SUPPORTED_BY_VERIFIER", g)

        # (i) revocation time-relativity (input source is GUESS G-27)
        facts.setdefault("slot_fps", {})[name] = kfp

    # (f) V30 common attested content across slots (reading (a))
    cs = [jcs.canonicalize(c) for (_, c, _) in facts["commons"].values()]
    cvs = {fr.canon_version for (fr, _, _) in facts["commons"].values()}
    ots = {fr.object_type for (fr, _, _) in facts["commons"].values()}
    same = len(set(cs)) <= 1 and len(cvs) <= 1 and len(ots) <= 1
    cks.add("V30", PASS if same else FAIL, "" if same else "P2_SPLICED_SLOTS")
    if not facts["commons"]:
        cks.add("V30", FAIL, "P2_NO_PARSEABLE_SLOT")
        return facts
    first = next(iter(facts["commons"].values()))
    common = first[1]
    facts["common"] = common
    facts["frames"] = [facts["commons"][n][2] for n in names if n in facts["commons"]]

    # (e) V21 binding-form required set
    bf = common.get("binding_forms")
    vocab_channels = trust.binding_ids == "channels"
    if vocab_channels:
        known_sup, known_unsup = set(trust.channel_keys), set()
    else:
        known_sup, known_unsup = objects.BINDING_FORMS_KNOWN_SUPPORTED, objects.BINDING_FORMS_KNOWN_UNSUPPORTED
    if not isinstance(bf, list) or not bf or not all(isinstance(x, str) for x in bf) \
            or len(set(bf)) != len(bf) or bf != sorted(bf):
        cks.add("V21", FAIL, "BINDING_FORM_SET_MALFORMED")
        bf = []
    else:
        unknown = [x for x in bf if x not in known_sup | known_unsup]
        unsupported = [x for x in bf if x in known_unsup]
        if unknown:
            cks.add("V21", UNPERF, "BINDING_FORM_UNKNOWN")
        elif unsupported:
            cks.add("V21", UNPERF, "BINDING_FORM_KNOWN_UNSUPPORTED")
        else:
            cks.add("V21", PASS)
    # Which (channel, form) pairs strict requires (G-17 experiment switches, see TrustConfig).
    if vocab_channels:
        forms = ["STMT_DIGEST"]
        chans = sorted(trust.channel_keys) if trust.required_from == "policy" \
            else [x for x in bf if x in trust.channel_keys]
    else:
        chans = list(trust.channel_keys)
        if trust.required_from == "policy" and trust.policy_forms is not None:
            forms = sorted(trust.policy_forms)
        else:
            forms = [x for x in bf if x in objects.BINDING_FORMS_KNOWN_SUPPORTED]
    facts["required_channels"], facts["required_forms"] = list(chans), list(forms)

    # (e) V20/V23 authority evidence per channel per required form
    evs = man.get("evidences", [])
    for ch in chans:
        chkey = trust.channel_keys[ch]
        g = f"channel:{ch}"
        for form in forms:
            cid = f"V20[{ch}:{form}]"
            mine = [e for e in evs if e.get("channel") == ch and e.get("form") == form]
            if not mine:
                # GUESS G-29: required evidence ABSENT is "cannot be performed" (UNVERIFIABLE),
                # not "performed and failed" (INVALID). R-2.37's "missing member -> INVALID"
                # is read as applying to the binding-form set only.
                cks.add(cid, UNPERF, "AUTHORITY_EVIDENCE_ABSENT", g, observation="absent")
                continue
            if len(mine) > 1:
                cks.add(cid, FAIL, "AUTHORITY_EVIDENCE_DUPLICATE", g, observation="invalid")
                continue
            e = mine[0]
            try:
                efb = b64d(e["frame_b64"]); esig = b64d(e["sig_b64"])
                efr, efails = frame.decode(efb)
            except (KeyError, binascii.Error, ValueError, frame.FrameError):
                cks.add(cid, FAIL, "AUTHORITY_EVIDENCE_MALFORMED", g, observation="invalid")
                continue
            if efails or efr.object_type != "OT_AUTHEVID":
                cks.add(cid, FAIL, "AUTHORITY_EVIDENCE_TYPE", g, observation="invalid")
                continue
            sig_ok = sig_verify(trust.channel_alg, chkey, esig, efb)
            binds = efr.payload == objects.evidence_payload(form, t)
            if sig_ok and binds:
                cks.add(cid, PASS, "", g, observation="would-pass")
            else:
                names_other = False
                try:
                    ev = jcs.parse_strict(efr.payload)
                    st = ev.get("statement") if isinstance(ev, dict) else None
                    names_other = isinstance(st, dict) and st.get("key_fp") != t["key_fp"]
                except jcs.CanonicalizationRejected:
                    pass
                cks.add(cid, FAIL, "AUTHORITY_EVIDENCE_INVALID" if not sig_ok else "AUTHORITY_EVIDENCE_BINDS_OTHER_STATEMENT",
                        g, observation="names-other-key" if names_other else "invalid")

    # (h) temporal, against the receipt's own anchor (non-waivable)
    _temporal(layer.get("anchor"), facts["frames"], common, trust, policy, cks, facts)

    # (i) revocation
    at = facts.get("anchor_time")
    try:
        declared = objects.parse_ts(common.get("declared_issue_time", ""))
    except ValueError:
        declared = None
    for name, kfp in facts.get("slot_fps", {}).items():
        rv = trust.revocations.get(kfp)
        if rv is None:
            cks.add(f"REV[{name}]", PASS, "", f"slot:{name}")
        elif at is None or declared is None:
            cks.add(f"REV[{name}]", UNPERF, "REVOCATION_WINDOW_UNEVALUABLE", f"slot:{name}")
        else:
            bad = rv <= at or rv <= declared
            cks.add(f"REV[{name}]", FAIL if bad else PASS, "P6_REVOKED_IN_WINDOW" if bad else "", f"slot:{name}")
    return facts


def _temporal(anchor, frames, common, trust, policy, cks: Checks, facts: dict, prefix: str = ""):
    delta = policy.delta if policy.delta is not None else trust.delta
    eps = policy.epsilon if policy.epsilon is not None else trust.epsilon
    k = trust.k
    if isinstance(anchor, dict) and anchor.get("format") == "ots-bitcoin":   # PHASE 3: real OTS anchor
        from .real import anchor as real_anchor
        return real_anchor.temporal(anchor, frames, common, trust, policy, cks, facts, prefix)
    ids = {x: f"{prefix}{x}" for x in ("V33a", "V33", "V34", "V35", "V36", "V37", "V38", "TIME")}
    try:
        declared = objects.parse_ts(common.get("declared_issue_time", ""))
        cks.add(ids["TIME"], PASS)
    except ValueError:
        cks.add(ids["TIME"], FAIL, "DECLARED_TIME_MALFORMED")
        return
    if not anchor or "proof" not in anchor:
        cks.add(ids["V33a"], UNPERF, "ANCHOR_PROOF_ABSENT")
        return
    proof = anchor["proof"]
    digest = objects.receipt_digest(frames)
    bound = (proof.get("digest") == digest and proof.get("txid") == anchor_stub.txid_for(digest)
             and anchor.get("txid") == proof.get("txid"))
    h = proof.get("height")
    hs = anchor.get("headers") or []
    by_h = {x.get("height"): x for x in hs if isinstance(x, dict)}
    # V37 header availability: bundle or verifier-distributed store (store holds hashes only here)
    need = list(range(h, h + k)) if isinstance(h, int) else []
    missing = [x for x in need if x not in by_h]
    if not need or missing:
        cks.add(ids["V37"], UNPERF, "HEADERS_UNAVAILABLE")
        cks.add(ids["V33a"], PASS if bound else FAIL, "" if bound else "ANCHOR_NOT_OVER_THIS_RECEIPT")
        return
    cks.add(ids["V37"], PASS)
    # V38 header authentication (STUB): each bundled header must equal the store's pinned hash
    # and link to its predecessor. GUESS G-31: store absence -> UNVERIFIABLE (docket 6-7 reading).
    auth = PASS
    reason = ""
    for x in need:
        st = trust.header_store.get(x)
        if st is None:
            auth, reason = UNPERF, "HEADER_NOT_IN_TRUST_STORE"
            break
        if anchor_stub.header_hash(by_h[x]) != st:
            auth, reason = FAIL, "HEADER_STORE_CONFLICT"
            break
        if x > h and by_h[x].get("prev") != anchor_stub.header_hash(by_h[x - 1]):
            auth, reason = FAIL, "HEADER_CHAIN_BROKEN"
            break
    cks.add(ids["V38"], auth, reason)
    root_ok = anchor_stub.merkle_root_from_path(proof.get("txid", ""), proof.get("path", [])) == by_h[h].get("merkle_root") \
        if bound else False
    cks.add(ids["V33a"], PASS if (bound and root_ok) else FAIL, "" if (bound and root_ok) else "ANCHOR_NOT_OVER_THIS_RECEIPT")
    anchor_time = by_h[h]["time"]
    confirmed_at = by_h[h + k - 1]["time"]
    facts["anchor_time"], facts["confirmed_at"], facts["declared"] = anchor_time, confirmed_at, declared
    cks.add(ids["V33"], PASS if declared - eps <= anchor_time else FAIL, "" if declared - eps <= anchor_time else "P5_ANCHOR_BEFORE_WINDOW")
    cks.add(ids["V34"], PASS if anchor_time <= declared + delta else FAIL, "" if anchor_time <= declared + delta else "P5_ANCHOR_AFTER_WINDOW")
    cks.add(ids["V35"], PASS if confirmed_at <= declared + delta else FAIL, "" if confirmed_at <= declared + delta else "P5_CONFIRMATION_LATE")
    cks.add(ids["V36"], PASS)  # depth: k consecutive headers h..h+k-1 present and authenticated above


def _ladder(cks: Checks, policy: Policy, waived_groups: set[str]) -> tuple[str, dict]:
    waived, required = {}, {}
    for cid, c in cks.m.items():
        (waived if c.get("group") in waived_groups else required)[cid] = c
    if any(c["status"] == FAIL for c in required.values()):
        v = INVALID
    elif any(c["status"] == UNPERF for c in required.values()):
        v = UNVERIFIABLE
    elif not waived_groups:
        v = VALID_STRICT
    else:
        v = VALID_DEGRADED
    obs = {}
    for g in sorted(waived_groups):
        mem = {cid: c for cid, c in waived.items() if c.get("group") == g}
        if not mem:
            o = "absent"
        elif any(c.get("observation") == "names-other-key" for c in mem.values()):
            o = "names-other-key"
        elif any(c["status"] == FAIL and c.get("observation") == "absent" for c in mem.values()) \
                or all(c.get("observation") == "absent" for c in mem.values()):
            o = "absent"
        elif any(c["status"] == FAIL for c in mem.values()):
            o = "invalid"
        elif any(c["status"] == UNPERF for c in mem.values()):
            o = "unperformable"
        else:
            o = "would-pass"
        obs[g] = {"authorized_by_policy": policy.name, "observation": o}
    return v, obs


def verify_bundle(bundle: dict, trust: TrustConfig, policy: Policy | None = None,
                  mutations: Mutations | None = None, dsks: DSKSOracle | None = None,
                  evaluate_standing: bool = True) -> dict:
    policy = policy or Policy()
    mut = mutations or Mutations()
    layers = bundle.get("layers") or []
    results = []
    # The outermost layer's type comes from the bundle but is restricted (GUESS G-32).
    expected = layers[0].get("object_type") if layers else None
    slot_material = layers[0].get("slots", []) if layers else []
    for li, layer in enumerate(layers):
        cks = Checks()
        if expected not in ("OT_ATTEST", "OT_WRAPPER"):
            cks.add("V4", FAIL, "P7_LAYER_TYPE_NOT_VERIFIABLE")
            results.append(_layer_result(li, expected, cks, policy, set()))
            break
        try:
            facts = _verify_layer(li, layer, slot_material, expected, trust, policy, mut, dsks, cks)
        except PolicyError:
            raise
        waived_groups = {f"slot:{x}" for x in policy.waive_slots} | {f"channel:{x}" for x in policy.waive_channels}
        res = _layer_result(li, expected, cks, policy, waived_groups)
        if li == 0 and evaluate_standing and expected == "OT_ATTEST":
            from .standing import standing_path
            res["protocol_standing"] = standing_path(layer, slot_material, bundle.get("standing"), trust, policy)
        results.append(res)
        # (b) wrapper handling: the next layer's frames/signatures come from the wrapper's
        # authenticated payload (opaque base64), its keys/manifest/anchor from the bundle (O-70).
        if expected == "OT_WRAPPER":
            common = facts.get("common") or {}
            inner = common.get("inner")
            if li + 1 >= len(layers) or not isinstance(inner, dict):
                cks.add("V12", FAIL, "P7_INNER_PACKAGE_INCOMPLETE")
                res.update(_layer_result(li, expected, cks, policy, waived_groups))
                break
            nxt = layers[li + 1]
            mat = []
            ok9 = isinstance(inner.get("slots"), list)
            for es in inner.get("slots", []) if ok9 else []:
                bs = {b.get("slot"): b for b in nxt.get("slots", [])}.get(es.get("slot"), {})
                if not isinstance(es.get("frame_b64"), str):
                    ok9 = False
                mat.append({**{k: v for k, v in bs.items() if k in ("slot", "alg", "pubkey_b64")},
                            **{k: v for k, v in es.items() if k in ("slot", "frame_b64", "sig_b64", "signed_bytes_b64")}})
            cks.add("V9", PASS if ok9 else FAIL, "" if ok9 else "P7_INNER_NOT_OPAQUE")
            # V10: recorded inner canonicalization version vs the inner frame's own
            ok10 = True
            for m in mat:
                try:
                    ifr, _ = frame.decode(b64d(m["frame_b64"]))
                    ok10 &= ifr.canon_version == inner.get("cv")
                except Exception:
                    ok10 = False
            fr0 = next(iter(facts["commons"].values()))[0] if facts.get("commons") else None
            ok10 &= fr0 is not None and common.get("outer_cv") == fr0.canon_version
            cks.add("V10", PASS if ok10 else FAIL, "" if ok10 else "P7_INNER_VERSION_LIED")
            res.update(_layer_result(li, expected, cks, policy, waived_groups))
            res["protocol_standing"] = {"value": None, "reason": "NOT_EVALUATED_FOR_WRAPPER_LAYER (prototype)"}
            slot_material = mat
            expected = nxt.get("object_type")
        elif li + 1 < len(layers):
            # extra layers not referenced by any wrapper
            cks.add("V12", FAIL, "UNREFERENCED_LAYER")
            res.update(_layer_result(li, expected, cks, policy, waived_groups))
            break
    return {
        "report_format": "tessera-proto-base-assessment/0",
        "unsigned": True,  # R-5.43
        "layers": results,  # per layer, never aggregated (R-5.42, R-5.47)
        "governing": {
            "spec": (bundle.get("embedded") or {}).get("spec", {}).get("id"),
            "policy": {"name": policy.name, "waive_channels": sorted(policy.waive_channels),
                       "waive_slots": sorted(policy.waive_slots)},
            "trust_config_digest": sha256_hex(repr(sorted(trust.channel_keys.items())).encode() +
                                              f"{trust.k}/{trust.delta}/{trust.epsilon}".encode()),
            "mutations": {"drop_frame_pin_and_mh": mut.drop_frame_pin_and_mh,
                          "unbind_signature_bytes": mut.unbind_signature_bytes},
        },
        "scope": "envelope verification of framed bytes per layer; NOT payload truth, meaning, or intended use (R-1.1, R-5.55)",
    }


def _layer_result(li: int, ot, cks: Checks, policy: Policy, waived_groups: set[str]) -> dict:
    v, obs = _ladder(cks, policy, waived_groups)
    label = f"VALID_DEGRADED(policy={policy.name})" if v == VALID_DEGRADED else v
    return {
        "layer": li,
        "object_type": ot,
        "verification": label,
        "waivers": obs,
        "checks": cks.m,
        "failed": sorted(c for c, x in cks.m.items() if x["status"] == FAIL and x.get("group") not in waived_groups),
        "unperformable": sorted(c for c, x in cks.m.items() if x["status"] == UNPERF and x.get("group") not in waived_groups),
    }
