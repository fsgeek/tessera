"""Consumer 3: the 2106 EXAMINER (THROWAWAY).

No Tessera service, no live DNS, no live repository, no third-party log (R-5.10). It holds only:
  * the bundle (a JSON file),
  * the archived trust-anchor store (R-5.8: channel keys by validity period) plus the archived
    header store (R-2.19), as some verifier distribution once shipped them,
  * whatever the bundle embeds (spec, conformance vectors, standards-dependency manifest, preamble).

This module deliberately does NOT import the prototype's verifier, objects, frame or standing code:
an examiner in 2106 has no Tessera code. It reconstructs what it can from the bundle and from
standards, and records for every step where the needed rule or fact came from:

  BUNDLE      carried in the bundle
  STORE       the archived trust-anchor / header store
  EMBEDDED    the bundle's embedded spec / vectors / dependency manifest
  LISTED_STD  an external standard the dependency manifest names
  UNLISTED    an external standard the examiner needed but the manifest does not name
  RECONSTRUCTED  inferred by inspection or trial; plausible, not given
  SUPPLEMENT  a rule a complete embedded spec would have to state (second run only)
  MISSING     nowhere

Two runs are offered: `examine(bundle, store)` with the prototype bundle as it is, and
`examine(bundle, store, supplement=...)` as if the embedded spec were complete -- every rule the
spec says it will fix (O-01, O-79, K-2, §8 values) handed over. What still blocks in the second run
is what the BUNDLE (not the spec) fails to carry.
"""
from __future__ import annotations

import base64
import hashlib
import json
import struct
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .log import BLOCKED, CONFUSED, NOTE, WORKED, ConsumerLog

DONE, RECON, BLOCK = "done", "reconstructed", "blocked"


def _b64(s: str) -> bytes:
    return base64.b64decode(s, validate=True)


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _jcs(v) -> bytes:
    """Minimal RFC 8785 for what these payloads hold (strings, integers, arrays, objects); key order
    by code point equals UTF-16 order for the ASCII keys seen here. Written by the examiner."""
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _ed25519_ok(pub: bytes, sig: bytes, msg: bytes) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg)
        return True
    except (InvalidSignature, ValueError):
        return False


def _sig_ok(alg: str, pub: bytes, sig: bytes, msg: bytes, sup: dict) -> bool:
    """PHASE 3: the examiner knows Ed25519 (the dependency manifest names RFC 8032). Any other
    algorithm id needs a verifier handed over in the supplement (OpenPGP, ECDSA: unlisted)."""
    if alg == "Ed25519":
        return _ed25519_ok(pub, sig, msg)
    f = sup.get("signature_verify")
    return bool(f and f(alg, pub, sig, msg))


def _sha256d(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


@dataclass
class Step:
    name: str
    status: str
    sources: list[str]
    note: str = ""
    spec: str = ""
    required: bool = True      # does a verdict need this step?


@dataclass
class Exam:
    unlisted: list = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)
    needed_standards: set[str] = field(default_factory=set)
    log: ConsumerLog = field(default_factory=lambda: ConsumerLog("2106 examiner"))
    verdict: str = ""
    verdict_if_trusting_reconstructions: str = ""

    def add(self, *a, **kw) -> Step:
        s = Step(*a, **kw)
        self.steps.append(s)
        return s

    def blocked(self) -> list[Step]:
        return [s for s in self.steps if s.status == BLOCK and s.required]

    def table(self) -> list[tuple]:
        return [(s.name, s.status, "+".join(s.sources), s.note, s.spec) for s in self.steps]


# ------------------------------------------------------------------ reconstruction helpers

def infer_frame(fb: bytes) -> dict | None:
    """Reverse-engineer the frame: the JSON payload starts at the first '{'; test whether the 8 bytes
    before it are its big-endian length, the 2 before those a version, and byte 0 a tag length."""
    i = fb.find(b"{")
    if i < 11:
        return None
    (plen,) = struct.unpack(">Q", fb[i - 8:i])
    (cv,) = struct.unpack(">H", fb[i - 10:i - 8])
    tl = fb[0]
    if plen != len(fb) - i or tl != i - 11:
        return None
    try:
        tag = fb[1:1 + tl].decode("ascii")
    except UnicodeDecodeError:
        return None
    return {"tag": tag, "cv": cv, "payload": fb[i:], "layout": "u8 taglen | tag | u16 cv | u64 len | payload"}


def rebuild_frame(tag: str, cv: int, payload: bytes) -> bytes:
    t = tag.encode("ascii")
    return struct.pack(">B", len(t)) + t + struct.pack(">H", cv) + struct.pack(">Q", len(payload)) + payload


FP_CANDIDATES = {
    "fp1:sha256(alg|00|pub)": lambda alg, pub: "fp1:" + _sha(alg.encode() + b"\x00" + pub),
    "sha256(pub)": lambda alg, pub: _sha(pub),
    "fp1:sha256(pub)": lambda alg, pub: "fp1:" + _sha(pub),
    "fp1:sha256(alg|pub)": lambda alg, pub: "fp1:" + _sha(alg.encode() + pub),
}


def guess_fp(alg: str, pub: bytes, target: str) -> str | None:
    for name, f in FP_CANDIDATES.items():
        if f(alg, pub) == target:
            return name
    return None


# ------------------------------------------------------------------ the examination

def examine(bundle: dict, store: dict, supplement: dict | None = None) -> Exam:
    ex = Exam()
    L = ex.log
    sup = supplement or {}
    emb = bundle.get("embedded") or {}

    # 0. The container
    ex.add("read the bundle container", DONE if "bundle_format" in sup else RECON,
           ["BUNDLE", "UNLISTED:RFC 8259 JSON", "UNLISTED:RFC 4648 base64"] + (["SUPPLEMENT"] if sup else []),
           f"format label {bundle.get('bundle_format')!r} names no embedded definition; member names read as English",
           "R-5.4, GUESSES G-26")
    ex.needed_standards |= {"RFC 8259 (JSON)", "RFC 4648 (base64)"}

    # 1. Preamble
    pre = emb.get("purpose_preamble")
    ex.add("purpose preamble", DONE if pre else BLOCK, ["EMBEDDED"], (pre or "")[:80], "R-3.50", required=False)

    # 2. Embedded spec and its hash
    spec = emb.get("spec") or {}
    spec_bytes = _b64(spec["bytes_b64"]) if spec.get("bytes_b64") else b""
    ex.needed_standards.add("FIPS 180-4 (SHA-256)")
    spec_hash_ok = spec_bytes and "sha256:" + _sha(spec_bytes) == spec.get("hash")
    ex.add("embedded spec matches its own content address", DONE if spec_hash_ok else BLOCK,
           ["EMBEDDED", "UNLISTED:FIPS 180-4"], "", "R-3.50, R-7.3")
    procedure_given = len(spec_bytes) > 2000 or bool(sup)
    ex.add("verification procedure from the embedded spec", DONE if sup else BLOCK,
           ["SUPPLEMENT"] if sup else ["EMBEDDED"],
           "complete spec handed over (second run)" if sup else
           f"embedded spec is {len(spec_bytes)} bytes of prose pointing at a repository that no longer exists; "
           "even the full 2026 spec leaves the byte layouts open (O-01, O-79) and 50 builder guesses",
           "R-7.4, R-7.9, R-7.11, GUESSES.md")
    if not procedure_given:
        L.add(BLOCKED, "The embedded specification cannot be executed or even read as a procedure; everything below "
                       "is reverse-engineered from the bytes", "R-7.4 Designated Community claim, R-7.11 (candidate)")

    deps = [d.get("standard") for d in emb.get("standards_dependencies", [])]

    # 3. Layers (outermost only; the honest bundles examined here are single-layer)
    lay = bundle["layers"][0]
    slots = lay["slots"]
    t = lay["manifest"]["tuple"]
    commons, frames = [], []
    sig_ok = True
    for s in slots:
        fb = _b64(s["frame_b64"])
        fr = infer_frame(fb)
        if fr is None:
            ex.add(f"frame layout, slot {s['slot']}", BLOCK, ["MISSING"], "cannot locate the payload", "R-4.9, O-01")
            return _finish(ex, deps)
        frames.append(fb)
        payload = json.loads(fr["payload"])
        canon = _jcs(payload) == fr["payload"]
        commons.append(payload)
        ok = _sig_ok(s["alg"], _b64(s["pubkey_b64"]), _b64(s["sig_b64"]), fb, sup)
        sig_ok &= ok and canon
        ex.add(f"slot {s['slot']}: frame layout", DONE if "frame_layout" in sup else RECON,
               ["SUPPLEMENT"] if "frame_layout" in sup else ["RECONSTRUCTED"],
               f"{'given' if 'frame_layout' in sup else 'inferred'} {fr['layout']}, tag {fr['tag']!r}; reconstruction byte-identical: {rebuild_frame(fr['tag'], fr['cv'], fr['payload']) == fb}",
               "R-4.8, R-4.9 (O-01)")
        ex.add(f"slot {s['slot']}: payload canonical + signature over the frame", DONE if ok and canon else BLOCK,
               ["BUNDLE", "LISTED_STD:RFC 8785", "LISTED_STD:RFC 8032" if s["alg"] == "Ed25519" else
                f"UNLISTED:{s['alg']}"] + (["SUPPLEMENT"] if s["alg"] != "Ed25519" and sup else []),
               f"canonical={canon} signature={ok} alg={s['alg']}", "V6, V19")
    ex.needed_standards |= {"RFC 8785 (JCS)", "RFC 8032 (Ed25519)"}
    common = commons[0]["common"]
    same = len({_jcs(c["common"]) for c in commons}) == 1
    ex.add("payload equal across signer slots", DONE if "encoding_map" in sup else RECON,
           ["SUPPLEMENT" if "encoding_map" in sup else "RECONSTRUCTED"],
           f"read 'common' as the shared part (G-15); equal={same}", "R-3.12a (O-79), V30")

    # 4. Governing spec bound in the signed bytes
    bound = common.get("spec", {}).get("hash") == spec.get("hash")
    ex.add("signed bytes name the embedded spec", DONE if bound else BLOCK, ["BUNDLE", "EMBEDDED"],
           "the spec that says how to parse the frame is named only inside the frame", "R-3.50")
    L.add(CONFUSED, "Chicken and egg: the identifier of the governing specification sits inside the signed payload, "
                    "so the examiner must already know how to parse the frame before it can learn which procedure "
                    "governs the parse", "R-3.50, R-4.8")

    # 5. Key binding: fingerprint function
    fp_ok = True
    fp_rule = None
    for s, c in zip(slots, commons):
        pub = _b64(s["pubkey_b64"])
        if "fingerprint" in sup:
            name = "supplied" if sup["fingerprint"](s["alg"], pub) == c["signer"]["key_fp"] else None
        else:
            name = guess_fp(s["alg"], pub, c["signer"]["key_fp"])
        fp_rule = fp_rule or name
        fp_ok &= name is not None
    fps = [c["signer"]["key_fp"] for c in commons]
    ex.add("key fingerprint function (pubkey -> tuple key_fp / sset)", (DONE if "fingerprint" in sup else RECON) if fp_ok else BLOCK,
           ["SUPPLEMENT"] if "fingerprint" in sup else ["RECONSTRUCTED"],
           f"by trial over {len(FP_CANDIDATES)} candidates: {fp_rule}; tuple matches slots: {fps == [t['key_fp'], *t['sset']]}",
           "R-3.11, V16 ('fp is a free constructor'), GUESSES G-10")

    # 6. Manifest hash and possession
    mh_rule = None
    for name, f in {"sha256:sha256(JCS(tuple))": lambda: "sha256:" + _sha(_jcs(t)),
                    "sha256(JCS(tuple))": lambda: _sha(_jcs(t)),
                    "sha256:sha256(JCS(manifest))": lambda: "sha256:" + _sha(_jcs(lay["manifest"]))}.items():
        if f() == common.get("manifest_hash"):
            mh_rule = name
    if "manifest_hash" in sup:
        mh_rule = "supplied" if sup["manifest_hash"](t) == common.get("manifest_hash") else None
    ex.add("manifest hash", (DONE if "manifest_hash" in sup else RECON) if mh_rule else BLOCK,
           ["SUPPLEMENT" if "manifest_hash" in sup else "RECONSTRUCTED"], f"by trial: {mh_rule}",
           "R-3.11, V18, GUESSES G-14, K-5")
    poss_rule = None
    pos = {p["key_fp"]: _b64(p["sig_b64"]) for p in lay["manifest"]["possession"]}
    cands = [("supplied", sup["possession_msg"](t))] if "possession_msg" in sup else \
        [(tag, rebuild_frame(tag, 1, _jcs(t))) for tag in
         ("tessera/v0/OT_MANIFEST", "tessera/v0/OT_ISSUER_KEY_MANIFEST", "tessera/v0/OT_POSS")]
    for tag, msg in cands:
        if all(_sig_ok(s["alg"], _b64(s["pubkey_b64"]), pos.get(fp, b""), msg, sup) for s, fp in zip(slots, fps)):
            poss_rule = f"frame({tag!r}, JCS(tuple))"
            break
    ex.add("possession proofs", (DONE if "possession_msg" in sup else RECON) if poss_rule else BLOCK,
           ["SUPPLEMENT" if "possession_msg" in sup else "RECONSTRUCTED"],
           f"by trial over guessed type tags: {poss_rule}", "R-3.38 vs V24 (K-5), GUESSES G-22")

    # 7. Authority evidence against the archived store
    declared = common.get("declared_issue_time")
    ev_ok = {}
    for e in lay["manifest"]["evidences"]:
        ch = e["channel"]
        entry = store.get("channel_keys", {}).get(ch)
        efr = infer_frame(_b64(e["frame_b64"]))
        if not entry or efr is None:
            ev_ok[ch] = False
            continue
        good = _ed25519_ok(_b64(entry["pub_b64"]), _b64(e["sig_b64"]), _b64(e["frame_b64"]))
        binds = json.loads(efr["payload"]).get("digest") == common.get("manifest_hash")
        ev_ok[ch] = good and binds
    ex.add("authority evidence, per channel, against the archived store",
           DONE if ev_ok and all(ev_ok.values()) else BLOCK, ["BUNDLE", "STORE"],
           f"{ev_ok}; key chosen by the receipt's own declared time {declared}, because the stub evidence "
           "carries no anchor of its own", "R-3.31, R-5.4 'time-anchored', R-5.8, GUESSES G-21")
    L.add(CONFUSED, "The archived store lists channel keys 'by validity period', but the authority evidence carries no "
                    "time of its own (stub) -- the examiner picks the store entry by the issuer's declared time, which "
                    "is the very party the evidence is meant to vouch for", "R-5.8, R-3.31, R-2.18")
    L.add(CONFUSED, "The bundle names no trust-anchor store (no identifier, no digest, no version), so the examiner "
                    "must take on faith that the store in its hands is the one a 2026 verifier shipped. Whoever "
                    "curates the archived store decides every channel check and every header check",
          "R-5.8, R-2.18, R-2.19, R-7.12 (candidate)")
    ex.needed_standards |= {"RFC 4033-4035 (DNSSEC) [hidden by stub]", "git object format + OpenPGP [hidden by stub]"}

    # 8. Anchor: what was anchored, and the chain
    a = lay["anchor"]
    proof = a.get("proof") or {}
    if a.get("format") == "ots-bitcoin":
        pass
    elif "receipt_digest" in sup:
        rd_ok = sup["receipt_digest"](frames) == proof["digest"]
        ex.add("receipt-to-anchor binding (what digest was anchored)", DONE if rd_ok else BLOCK, ["SUPPLEMENT"],
               f"matches: {rd_ok}", "R-3.42, V33a, K-2")
    else:
        trials = [_sha(frames[0]), _sha(b"".join(frames)),
                  _sha(b"".join(struct.pack(">I", len(f)) + f for f in frames))]
        hit = proof["digest"] in trials
        ex.add("receipt-to-anchor binding (what digest was anchored)", RECON if hit else BLOCK,
               ["RECONSTRUCTED" if hit else "MISSING"],
               "a two-frame receipt has no defined 'its canonical bytes'; obvious constructions tried, none match"
               if not hit else "by trial", "R-3.42, V33a, K-2, GUESSES G-19")
    if a.get("format") == "ots-bitcoin":
        _examine_ots(ex, a, frames, store, sup)
        ex.add("revocation time-relativity (R-5.21)", BLOCK, ["MISSING"],
               "neither the bundle, the archived store nor any embedded object carries revocation facts",
               "R-5.21, R-5.4, R-5.8, GUESSES G-27")
        return _finish_standing(ex, bundle, lay, common, t, sup, deps)
    if "anchor_format" in sup:
        f = sup["anchor_format"]
        chain_ok = f["txid"](proof["digest"]) == proof["txid"] and \
            f["root"](proof["txid"], proof["path"]) == {h["height"]: h for h in a["headers"]}[proof["height"]]["merkle_root"]
        ex.add("anchor proof path to the block", DONE if chain_ok else BLOCK, ["SUPPLEMENT", "UNLISTED:OpenTimestamps"],
               "stub format supplied", "R-4.74, V33a")
    else:
        ex.add("anchor proof path to the block", BLOCK, ["UNLISTED:OpenTimestamps + Bitcoin"],
               "proof format is neither embedded nor named in the dependency manifest (stub: 'STUB-TX'/'STUB-LEAF' prefixes)",
               "R-3.51, R-7.7, GUESSES G-20")
    ex.needed_standards |= {"OpenTimestamps proof format [hidden by stub]", "Bitcoin block header + PoW rules [hidden by stub]"}
    hh = store.get("header_hashes", {})
    hdr_rule = None
    if hh:
        hf = sup.get("header_hash") or (lambda h: _sha(_jcs(h)))
        if all(hh.get(h["height"]) == hf(h) for h in a["headers"]):
            hdr_rule = "supplied" if "header_hash" in sup else "sha256(JCS(header))"
    ex.add("block headers authenticated against the archived header store",
           (DONE if "header_hash" in sup else RECON) if hdr_rule else BLOCK,
           ["BUNDLE", "STORE", "SUPPLEMENT" if "header_hash" in sup else "RECONSTRUCTED"], f"header hash rule by trial: {hdr_rule}; store pins every height",
           "R-2.19, V37, V38 'not specified' (O-22), GUESSES G-31")
    params = sup.get("params")
    ex.add("temporal predicate (needs k, delta, epsilon)", DONE if params else BLOCK,
           ["SUPPLEMENT"] if params else ["MISSING"],
           f"params {params}" if params else
           "the bundle records a policy-version label and an observed delay, not the values; the embedded stub has no §8",
           "R-2.20, R-5.9, §8, R-3.46")

    # 9. Revocation
    ex.add("revocation time-relativity (R-5.21)", BLOCK, ["MISSING"],
           "neither the bundle, the archived store (channel keys only) nor any embedded object carries issuer-key "
           "revocation facts or their effective times", "R-5.21, R-5.4, R-5.8, GUESSES G-27")
    L.add(BLOCKED, "Revocation: no input in 2106 says whether either issuer key was revoked inside (declared, anchor]. "
                   "The 2026 relying party could not learn it either; in 2106 there is also nobody left to ask",
          "R-5.21, R-5.10, GUESSES G-27")

    return _finish_standing(ex, bundle, lay, common, t, sup, deps)


def _examine_ots(ex: Exam, a: dict, frames: list[bytes], store: dict, sup: dict) -> None:
    """PHASE 3: a real-format OpenTimestamps proof. The examiner uses the OTS and Bitcoin standards
    (python-opentimestamps as a standard implementation, not Tessera code); neither is in the bundle's
    dependency manifest."""
    from opentimestamps.core.notary import BitcoinBlockHeaderAttestation
    from opentimestamps.core.serialize import BytesDeserializationContext
    from opentimestamps.core.timestamp import DetachedTimestampFile
    ex.needed_standards |= {"OpenTimestamps proof format", "Bitcoin block header + PoW rules"}
    dtf = DetachedTimestampFile.deserialize(BytesDeserializationContext(_b64(a["ots_b64"])))
    if "receipt_digest" in sup:
        rd_ok = sup["receipt_digest"](frames) == dtf.file_digest.hex()
        ex.add("receipt-to-anchor binding (what digest was anchored)", DONE if rd_ok else BLOCK, ["SUPPLEMENT"],
               f"matches: {rd_ok}", "R-3.42, V33a, K-2")
    else:
        trials = [_sha(frames[0]), _sha(b"".join(frames)),
                  _sha(b"".join(struct.pack(">I", len(f)) + f for f in frames))]
        hit = dtf.file_digest.hex() in trials
        ex.add("receipt-to-anchor binding (what digest was anchored)", RECON if hit else BLOCK,
               ["RECONSTRUCTED" if hit else "MISSING"],
               "the OTS file digest is sha256 of an undefined two-frame preimage; obvious constructions tried",
               "R-3.42, V33a, K-2, GUESSES G-19")
    atts = [(m, att.height) for m, att in dtf.timestamp.all_attestations() if isinstance(att, BitcoinBlockHeaderAttestation)]
    hdrs = {int(h): bytes.fromhex(x) for h, x in (a.get("headers_hex") or {}).items()}
    good = [(h, m) for m, h in atts if h in hdrs and hdrs[h][36:68] == m]
    ex.add("anchor proof path to the block", DONE if good else BLOCK, ["BUNDLE", "UNLISTED:OpenTimestamps", "UNLISTED:Bitcoin"],
           f"{len(atts)} Bitcoin attestation(s) at heights {sorted(h for _, h in atts)}; merkle root matches a bundled "
           f"header for {sorted(h for h, _ in good)}. Which one is 'the' anchor_time is not stated (R-3.42 says one proof)",
           "R-3.42, R-3.44, V33a")
    hh = store.get("header_hashes", {})
    pinned = all(hh.get(h) == _sha256d(x)[::-1].hex() for h, x in hdrs.items())
    ex.add("block headers authenticated against the archived header store", DONE if (hh and pinned) else BLOCK,
           ["BUNDLE", "STORE", "UNLISTED:Bitcoin header format (sha256d)"],
           f"store pins every bundled height: {pinned}; REGTEST difficulty here, so PoW proves nothing",
           "R-2.19, V37, V38 (O-22)")
    params = sup.get("params")
    ex.add("temporal predicate (needs k, delta, epsilon)", DONE if params else BLOCK,
           ["SUPPLEMENT"] if params else ["MISSING"], f"params {params}" if params else "not carried", "R-2.20, §8")


def _finish_standing(ex: Exam, bundle: dict, lay: dict, common: dict, t: dict, sup: dict, deps) -> Exam:
    # 10. Standing
    st = bundle.get("standing")
    if not st:
        ex.add("standing evidence", BLOCK, ["MISSING"], "no TLR in the bundle: S3 for ever", "R-6.30 S3, R-4.88(iv)", required=False)
    else:
        tl = st["tlr"]
        tfr = infer_frame(_b64(tl["frame_b64"]))
        tsig = _sig_ok(tl["alg"], _b64(tl["pubkey_b64"]), _b64(tl["sig_b64"]), _b64(tl["frame_b64"]), sup)
        entitled = (sup.get("fingerprint") or FP_CANDIDATES["fp1:sha256(alg|00|pub)"])(tl["alg"], _b64(tl["pubkey_b64"])) == t["key_fp"]
        ex.add("TLR signed by the entitled key", (DONE if sup else RECON) if tsig and entitled else BLOCK,
               ["BUNDLE", "SUPPLEMENT" if sup else "RECONSTRUCTED"],
               f"signature={tsig}; 'entitled key' read as slot A (G-25): {entitled}", "R-4.83, R-6.24 step 5, GUESSES G-25", required=False)
        body = json.loads(tfr["payload"]) if tfr else {}
        if "attempt_core" in sup:
            aid = sup["attempt_core"](lay, common)
            mine = [e for e in body.get("lineage", []) if e.get("aid") == aid]
            ex.add("which lineage entry is this receipt (aid = h(core))", DONE if mine else BLOCK, ["SUPPLEMENT"],
                   f"found: {bool(mine)}", "R-6.24 step 3, GUESSES G-24", required=False)
        else:
            ex.add("which lineage entry is this receipt (aid = h(core))", BLOCK, ["MISSING"],
                   f"attempt-core composition is modelled, not registered; lineage has {len(body.get('lineage', []))} "
                   "entr(y/ies): with one the examiner can only assume, with two S1 and S2 are indistinguishable",
                   "§5.1 table 'Attempt core' row, GUESSES G-24", required=False)
        ex.add("no contradictory TLR exists", BLOCK, ["MISSING"],
               "undecidable from one bundle; a third-party log is the only witness and R-5.10 excludes it",
               "R-5.59, R-6.38, R-7.23, R-5.10", required=False)
    return _finish(ex, deps)


def _finish(ex: Exam, deps: list[str]) -> Exam:
    blocked = ex.blocked()
    ex.verdict = "UNVERIFIABLE" if blocked else "VALID_STRICT"
    only_rev = [s for s in blocked if not s.name.startswith("revocation")]
    ex.verdict_if_trusting_reconstructions = "VALID_STRICT (revocation assumed absent)" if not only_rev else "UNVERIFIABLE"
    listed = {d for d in deps if d}
    unlisted = sorted(s for s in ex.needed_standards if not any(s.startswith(d) for d in listed if d))
    ex.log.add(NOTE, f"Standards the examiner needed but the dependency manifest does not name: {unlisted}",
               "R-3.51, R-7.7, R-7.8")
    ex.log.add(NOTE, f"Verdict reachable honestly: {ex.verdict} ({len(blocked)} required step(s) blocked: "
                     f"{[s.name for s in blocked]})", "R-2.32, R-5.25")
    ex.unlisted = unlisted
    return ex


# ---- experimenter-side helpers (NOT used by examine(); they build its inputs from the stub world)

def archived_store(world) -> dict:
    """What R-5.8 + R-2.19 put in the examiner's hands: channel keys by validity period, header hashes."""
    from tessera_proto.crypto import b64e
    return {
        "store_format": "unnamed (R-7.12: a standalone store object is only a candidate)",
        "channel_keys": {c.name: {"pub_b64": b64e(c.key.pub_raw), "valid_from": "2026-01-01", "valid_to": "2027-01-01"}
                         for c in (world.dns, world.repo)},
        "header_hashes": world.chain.header_store(),
    }


def complete_spec_supplement(world) -> dict:
    """Every rule a complete embedded spec would carry once O-01, O-79, K-2 and §8 are fixed. Taken
    from the prototype's own choices, which is exactly what a future spec would have to write down."""
    from tessera_proto import anchor_stub, objects
    from tessera_proto.crypto import fingerprint, verify
    from tessera_proto.objects import attempt_core, attempt_id

    def core_aid(lay, common):
        slots = sorted(lay["slots"], key=lambda s: s["slot"])
        return attempt_id(attempt_core(lay["manifest"]["tuple"], [p["sig_b64"] for p in lay["manifest"]["possession"]],
                                       [s["sig_b64"] for s in slots], common["declared_issue_time"]))
    return {
        "bundle_format": True, "frame_layout": True, "encoding_map": True,
        "manifest_hash": objects.manifest_hash, "possession_msg": objects.possession_frame,
        "header_hash": anchor_stub.header_hash,
        "fingerprint": fingerprint,
        "signature_verify": verify,   # PHASE 3: OpenPGP/ECDSA ids (Ed25519 never reaches it)
        "receipt_digest": lambda frames: objects.receipt_digest(frames),
        "anchor_format": {"txid": anchor_stub.txid_for, "root": anchor_stub.merkle_root_from_path},
        "params": {"k": world.params.k, "delta": world.params.delta, "epsilon": world.params.epsilon},
        "attempt_core": core_aid,
    }


STUB_HIDES = [
    ("Header authentication", "The stub pins every header hash in the store, so 'authenticated' means 'listed'. A real "
     "examiner needs Bitcoin's header format, proof-of-work and difficulty rules, and a checkpoint, and must decide "
     "which chain is canonical (V38 'not specified', O-22). A store frozen before issuance cannot pin later blocks."),
    ("Block time", "Stub blocks carry exactly the time the test chose. Real header timestamps are miner-set, may run "
     "about two hours fast and need not increase, yet V33-V35 compare them with the declared time to the second."),
    ("Proof format", "The stub's txid is a hash of the digest and the merkle path uses private prefixes. A real OTS "
     "proof is a chain of operations into a real transaction; the format is neither embedded nor named in the "
     "dependency manifest, and txid-to-transaction needs chain data (R-4.75)."),
    ("Authority evidence", "Each stub channel is one Ed25519 key. Real DNSSEC evidence needs the 2026 root KSK, every "
     "intermediate DNSKEY/DS, RRSIG validity windows evaluated at an authenticated time, and the DNSSEC algorithms of "
     "2026; the repository channel needs a git object format, a signing key and an OTS proof of its own."),
    ("Hash survival", "Everything bottoms out in SHA-256 (frame digest, merkle path, headers). The stub cannot show "
     "what happens to a 2026 bundle never renewed if SHA-256 weakens; claim 3 (R-7.1) puts that on custodians."),
]
