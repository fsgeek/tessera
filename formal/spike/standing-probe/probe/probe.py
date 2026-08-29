"""
PROBE — NON-DISCHARGING. Design probe under docs/reviews/2026-08-29-design-probe-ruling.md.

Minimal issuer / authority-channel / chain / verifier fixture for the
A3.7.1 standing-evidence question. Nothing here is intended for use in
the Tessera service. Every external thing is a stub and says so.

Declared in ../PROBE.md before this file existed.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import eddsa

# ---------------------------------------------------------------- stubs --
# STUB canonicalization. This is NOT P8. It exists so two dicts with the
# same content sign identically inside this probe; nothing about it is
# claimed.
def canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def h(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# Domain-separation tags. One per signed object kind, per the first-link
# decision's rule that forms must be tag-distinct.
STMT_DIRECT = "STMT_DIRECT"   # authority channel evidence over the tuple
POSS = "POSS"                 # manifest self-signature (A1.5 item 3: over the MANIFEST, not the fingerprint)
BYTES = "BYTES"               # attestation signature over framed bytes
TLR = "TLR"                   # terminal lineage record (candidate standing evidence)


class Key:
    """Ed25519 key. fp() is the fingerprint the authority tuple carries."""

    def __init__(self) -> None:
        self._k = ECC.generate(curve="ed25519")
        # DER-encoded SubjectPublicKeyInfo: pycryptodome 3.23 imports DER but not raw Ed25519 points.
        # (Probe run 1 failed on exactly this — every verify() returned False. Fixture bug, not a finding.)
        self.pub: str = self._k.public_key().export_key(format="DER").hex()

    @staticmethod
    def fp(pub_hex: str) -> str:
        # STUB fingerprint: hash of the DER encoding. What a real fingerprint hashes is P8's business.
        return h(bytes.fromhex(pub_hex))

    def sign(self, tag: str, body: Any) -> str:
        return eddsa.new(self._k, "rfc8032").sign(canon({"tag": tag, "body": body})).hex()

    @staticmethod
    def verify(pub_hex: str, tag: str, body: Any, sig_hex: str) -> bool:
        try:
            k = ECC.import_key(bytes.fromhex(pub_hex))
            eddsa.new(k, "rfc8032").verify(canon({"tag": tag, "body": body}), bytes.fromhex(sig_hex))
            return True
        except (ValueError, TypeError):
            return False


class ChannelStub:
    """STUB authority channel (DNS or repository). Publishes a signed statement over the tuple."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.key = Key()

    def publish(self, tup: dict) -> dict:
        return {"channel": self.name, "tuple": tup, "sig": self.key.sign(STMT_DIRECT, tup)}


class ChainStub:
    """STUB chain: blocks with heights and timestamps. Time is chain time (ts)."""

    def __init__(self) -> None:
        self.blocks: list[dict] = [{"height": 0, "ts": 0, "anchors": []}]

    @property
    def tip(self) -> dict:
        return self.blocks[-1]

    def mine(self, dt: int = 10) -> dict:
        b = {"height": self.tip["height"] + 1, "ts": self.tip["ts"] + dt, "anchors": []}
        self.blocks.append(b)
        return b

    def anchor(self, handle: str, dt: int = 10) -> dict:
        b = self.mine(dt)
        b["anchors"].append(handle)
        return {"height": b["height"]}

    def view(self) -> list[dict]:
        """Archived headers — what a bundle carries. A copy, so the verifier cannot reach the live chain."""
        return json.loads(json.dumps(self.blocks))

    @staticmethod
    def confirmed_at(view: list[dict], ref: dict, k: int) -> int | None:
        """A2.1 convention: timestamp of block h+k-1, or None if not buried that deep."""
        target = ref["height"] + k - 1
        for b in view:
            if b["height"] == target:
                return b["ts"]
        return None


# --------------------------------------------------------------- issuer --
@dataclass
class Issuer:
    key: Key = field(default_factory=Key)
    issuer_id: str = "issuer-A"

    def tuple(self) -> dict:
        kf = Key.fp(self.key.pub)
        return {"issuer_id": self.issuer_id, "kfpr": kf, "signer_set": [kf], "alg": "ed25519", "ver": 1}

    def attempt(self, framed_bytes: bytes, declared: int) -> dict:
        """One issuance attempt. The handle is the hash of the signed core: identity is DERIVED, not declared."""
        tup = self.tuple()
        core = {
            "tuple": tup,
            "manifest_sig": self.key.sign(POSS, tup),           # A1.5 item 3 encoding
            "content_hash": h(framed_bytes),
            "bytes_sig": self.key.sign(BYTES, h(framed_bytes)),
            "declared": declared,
            "pub": self.key.pub,
        }
        return {"handle": h(canon(core)), "core": core, "anchor_ref": None}

    def tlr(self, lineage: list[dict], terminal: dict, binding: str = "handle") -> dict:
        """Terminal lineage record — the candidate. binding='handle' names attempts by derived
        handle; binding='ordinal' (the BROKEN variant for Q3) names them by position only."""
        if binding == "ordinal":
            lineage = [{k: v for k, v in e.items() if k != "handle"} for e in lineage]
            terminal = {k: v for k, v in terminal.items() if k != "handle"}
        body = {"binding": binding, "lineage": lineage, "terminal": terminal}
        return {"body": body, "sig": self.key.sign(TLR, body), "pub": self.key.pub}


# ------------------------------------------------------------- verifier --
@dataclass
class TrustConfig:
    """What the verifier holds BEFORE seeing a bundle. This is A3.8's 'trust configuration' — an input, not a fetch."""
    channel_pubs: dict[str, str]
    k: int = 3
    delta: int = 60


@dataclass
class Verifier:
    trust: TrustConfig
    collapse_reasons: bool = False   # Q4 broken variant: one reason code for S2 and S3
    fields_read: list[str] = field(default_factory=list)
    external_fetches: int = 0        # Q6: the verifier has no way to fetch; this can only stay 0

    def _read(self, name: str) -> None:
        self.fields_read.append(name)

    # -- envelope verdict (simplified P4 partition; NOT the registered state machine) --
    def envelope(self, bundle: dict) -> tuple[str, list[str]]:
        reasons: list[str] = []
        core = bundle["artifact"]["core"]
        tup = core["tuple"]
        self._read("artifact.core.tuple")
        # authority evidence, both channels expected
        ev_ok = 0
        for ev in bundle.get("evidence", []):
            self._read(f"evidence[{ev['channel']}]")
            pub = self.trust.channel_pubs.get(ev["channel"])
            if pub and ev["tuple"] == tup and Key.verify(pub, STMT_DIRECT, tup, ev["sig"]):
                ev_ok += 1
            else:
                reasons.append(f"EVIDENCE_INVALID:{ev['channel']}")
        if ev_ok == 0:
            return "UNVERIFIABLE", reasons + ["NO_AUTHORITY_EVIDENCE"]
        # fingerprint, manifest self-signature (over the manifest), bytes signature
        self._read("artifact.core.pub"); self._read("artifact.core.manifest_sig"); self._read("artifact.core.bytes_sig")
        if Key.fp(core["pub"]) != tup["kfpr"]:
            return "INVALID", reasons + ["KEY_FINGERPRINT_MISMATCH"]
        if not Key.verify(core["pub"], POSS, tup, core["manifest_sig"]):
            return "INVALID", reasons + ["MANIFEST_SELF_SIGNATURE_INVALID"]
        if not Key.verify(core["pub"], BYTES, core["content_hash"], core["bytes_sig"]):
            return "INVALID", reasons + ["BYTES_SIGNATURE_INVALID"]
        # temporal: A2.2-shaped test on the archived chain view
        self._read("artifact.anchor_ref"); self._read("chain_view"); self._read("artifact.core.declared")
        ref = bundle["artifact"]["anchor_ref"]
        if ref is None or not any(bundle["artifact"]["handle"] in b["anchors"] for b in bundle["chain_view"] if b["height"] == ref["height"]):
            return "INVALID", reasons + ["ANCHOR_ABSENT"]
        ca = ChainStub.confirmed_at(bundle["chain_view"], ref, self.trust.k)
        if ca is None:
            return "UNVERIFIABLE", reasons + ["NOT_BURIED_TO_DEPTH_K"]
        if ca > core["declared"] + self.trust.delta:
            return "INVALID", reasons + ["LATE_BURIAL"]
        return ("VALID_STRICT" if ev_ok == 2 else "VALID_DEGRADED"), reasons

    # -- standing report (orthogonal; A3.7.1) --
    def standing(self, bundle: dict) -> tuple[str, str]:
        no_evidence = ("ABSENT", "NO_STANDING" if self.collapse_reasons else "NO_TERMINAL_DISPOSITION_EVIDENCE")
        superseded = ("ABSENT", "NO_STANDING" if self.collapse_reasons else "SUPERSEDED")
        self._read("standing_evidence")
        tlr = bundle.get("standing_evidence")
        if tlr is None:
            return no_evidence
        core = bundle["artifact"]["core"]
        # the TLR must be signed by the accepted key — the one the authority tuple names
        if tlr["pub"] != core["pub"] or not Key.verify(tlr["pub"], TLR, tlr["body"], tlr["sig"]):
            return "UNVERIFIABLE", "STANDING_EVIDENCE_SIGNATURE_INVALID"
        body = tlr["body"]
        # identity binding: how does this artifact find itself in the lineage?
        if body["binding"] == "handle":
            me = bundle["artifact"]["handle"]
            mine = [e for e in body["lineage"] if e["handle"] == me]
        else:  # ordinal (BROKEN): trust a label presented alongside the artifact
            self._read("artifact.claimed_ordinal")
            me = bundle["artifact"].get("claimed_ordinal")
            mine = [e for e in body["lineage"] if e["ordinal"] == me]
        if not mine:
            return "ABSENT", "STANDING_EVIDENCE_MISMATCH"
        term = body["terminal"]
        if term["disposition"] == "REFUSED":
            return "ABSENT", "ISSUANCE_REFUSED"
        key = "handle" if body["binding"] == "handle" else "ordinal"
        if term["disposition"] == "SHIPPED" and term[key] == me:
            return "ESTABLISHED", "TERMINAL_DISPOSITION_SHOWN"
        return superseded

    def assess(self, bundle: dict) -> dict:
        self.fields_read.clear()
        v, r = self.envelope(bundle)
        s, sr = self.standing(bundle)
        return {"verification": v, "reasons": r, "protocol_standing": s, "standing_reason": sr,
                "fields_read": list(self.fields_read), "external_fetches": self.external_fetches}


# ----------------------------------------------------------- lifecycle --
def bundle(artifact: dict, evidence: list[dict], chain: ChainStub, tlr: dict | None = None) -> dict:
    return {"artifact": artifact, "evidence": evidence, "chain_view": chain.view(), "standing_evidence": tlr}


def issue_with_reissue(issuer: Issuer, chain: ChainStub, content: bytes, k: int, delta: int,
                       issuer_timeout: int) -> tuple[list[dict], dict | None]:
    """A2.2/A2.3-shaped issuance loop at probe fidelity.

    Attempt 1 is anchored, then the chain is SLOW: by the issuer's timeout it has not reached
    depth k, so the issuer abandons it and reissues. But attempt 1's block does eventually bury
    within delta of ITS declared time by chain time — so a verifier accepts it. That is the A2.4
    residue: two valid artifacts, one shipped. Returns (attempts, shipped_attempt_or_None).
    """
    attempts: list[dict] = []
    a1 = issuer.attempt(content, declared=chain.tip["ts"])
    a1["anchor_ref"] = chain.anchor(a1["handle"], dt=10)
    attempts.append(a1)
    # slow chain: one block in issuer_timeout seconds, not enough for depth k
    chain.mine(dt=issuer_timeout)
    if ChainStub.confirmed_at(chain.view(), a1["anchor_ref"], k) is None:
        a1["disposition"] = "ABANDONED_ISSUER_TIMEOUT"
        a2 = issuer.attempt(content, declared=chain.tip["ts"])
        a2["anchor_ref"] = chain.anchor(a2["handle"], dt=5)
        attempts.append(a2)
        for _ in range(k):
            chain.mine(dt=5)          # fast blocks now — both anchors bury
        a2["disposition"] = "SHIPPED"
        return attempts, a2
    a1["disposition"] = "SHIPPED"
    return attempts, a1


def refuse_all(issuer: Issuer, chain: ChainStub, content: bytes, k: int, n_attempts: int, issuer_timeout: int) -> list[dict]:
    attempts = []
    for _ in range(n_attempts):
        a = issuer.attempt(content, declared=chain.tip["ts"])
        a["anchor_ref"] = chain.anchor(a["handle"], dt=10)
        chain.mine(dt=issuer_timeout)
        a["disposition"] = "ABANDONED_ISSUER_TIMEOUT"
        attempts.append(a)
    return attempts


def lineage_of(attempts: list[dict]) -> list[dict]:
    return [{"ordinal": i + 1, "handle": a["handle"], "anchor_ref": a["anchor_ref"], "disposition": a["disposition"]}
            for i, a in enumerate(attempts)]
