"""Issuer following spec §4 steps 1-9 as literally as the prototype can (THROWAWAY).

In-process keys (no KMS, no GPG), stub channels, stub anchor chain (anchor_stub.py), simulated
clock. Steps not built are marked NOT BUILT.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import frame, jcs, objects
from .anchor_stub import StubChain
from .crypto import KeyPair, b64e

HOUR = 3600


@dataclass
class Params:
    delta: int = 72 * HOUR     # δ strict default (§8)
    epsilon: int = 24 * HOUR   # ε strict default
    k: int = 6                 # confirmation depth
    N: int = 3                 # MaxAttempts
    S: int = 24 * HOUR         # operational slack


@dataclass
class Channel:
    """STUB authority channel (stands in for DNSSEC snapshot / anchored git publication)."""
    name: str
    key: KeyPair

    def evidence(self, form: str, t: dict) -> dict:
        fb = objects.evidence_frame(form, t)
        return {"channel": self.name, "form": form, "frame_b64": b64e(fb), "sig_b64": b64e(self.key.sign(fb))}


@dataclass
class ChainSchedule:
    """How the stub chain behaves for one attempt: seconds from declared time to inclusion,
    and seconds between subsequent blocks."""
    inclusion_delay: int = 600
    block_interval: int = 600


@dataclass
class AttemptRecord:
    attempt: int
    declared: int
    bundle: dict
    aid: str
    predicate_ok: bool
    why: str


@dataclass
class IssuanceResult:
    disposition: str                     # "SHIPPED" | "REFUSED"
    attempts: list[AttemptRecord] = field(default_factory=list)
    shipped: dict | None = None
    tlr: dict | None = None
    refusal_record: dict | None = None


def build_attest_layer(*, object_type: str, content, declared: int, issuer_id: str, slot_keys: list[KeyPair],
                       channels: list[Channel], binding_forms=("STMT_DIGEST",), extra_common=None,
                       alg: str = "Ed25519", attach_signed_bytes: dict | None = None,
                       declared_set=None) -> dict:
    """Steps 2-4: canonicalize, frame per signer slot (reading (a)), sign, manifest + evidence."""
    t = objects.authority_tuple(issuer_id, slot_keys[0].fp, [k.fp for k in slot_keys[1:]], alg)
    mh = objects.manifest_hash(t)
    # declared_set (G-17 experiment): what goes into the signed `binding_forms`, when it is not the
    # statement forms themselves (e.g. channel names). Evidence is still minted per `binding_forms`.
    common = objects.attest_common(issuer_id, alg, mh, declared, content,
                                   binding_forms if declared_set is None else declared_set,
                                   objects.spec_hash(), extra_common)
    slots = []
    for i, kp in enumerate(slot_keys):
        fb = frame.encode(object_type, frame.CANON_V1, objects.attest_payload(common, kp.fp))
        slots.append({"slot": "AB"[i] if i < 2 else f"S{i}", "alg": alg, "pubkey_b64": b64e(kp.pub_raw),
                      "frame_b64": b64e(fb), "sig_b64": b64e(kp.sign(fb))})
    pf = objects.possession_frame(t)
    manifest = {
        "tuple": t,
        "evidences": [ch.evidence(form, t) for ch in channels for form in sorted(binding_forms)],
        "possession": [{"key_fp": kp.fp, "sig_b64": b64e(kp.sign(pf))} for kp in slot_keys],
    }
    return {"object_type": object_type, "slots": slots, "manifest": manifest}


def anchor_layer(layer: dict, chain: StubChain, declared: int, sched: ChainSchedule, k: int,
                 frames_b64: list[str] | None = None) -> dict:
    """Step 5 against the STUB chain: submit the receipt digest, mine k blocks."""
    from .crypto import b64d
    fbs = [b64d(x) for x in (frames_b64 or [s["frame_b64"] for s in layer["slots"]])]
    if hasattr(chain, "anchor_receipt"):   # PHASE 3: real-format OTS on the regtest chain (real/ots.py)
        return chain.anchor_receipt(fbs, declared, sched, k)
    digest = objects.receipt_digest(fbs)
    txid = chain.submit(digest)
    t = declared + sched.inclusion_delay
    chain.mine(t)
    for _ in range(k - 1):
        t += sched.block_interval
        chain.mine(t)
    proof = chain.proof(digest)
    headers = chain.segment(proof["height"], k)
    return {"proof": proof, "txid": txid, "headers": headers}


class Issuer:
    def __init__(self, issuer_id: str, slot_keys: list[KeyPair], channels: list[Channel], chain: StubChain,
                 params: Params | None = None, binding_forms=("STMT_DIGEST",), declared_set=None):
        self.issuer_id = issuer_id
        self.slot_keys = slot_keys
        self.channels = channels
        self.chain = chain
        self.p = params or Params()
        self.binding_forms = binding_forms
        self.declared_set = declared_set

    # Step 1
    def ingest(self, submitted: bytes):
        return jcs.parse_strict(submitted)  # raises CanonicalizationRejected (explicit rejection)

    def _predicate(self, declared: int, anchor: dict) -> tuple[bool, str]:
        hs = anchor["headers"]
        if hs is None or len(hs) < self.p.k:
            return False, "depth<k"
        anchor_time = hs[0]["time"]
        confirmed_at = hs[self.p.k - 1]["time"]
        c1 = declared - self.p.epsilon <= anchor_time
        c2 = anchor_time <= declared + self.p.delta
        c3 = confirmed_at <= declared + self.p.delta
        return (c1 and c2 and c3), f"c1={c1} c2={c2} c3={c3}"

    def issue(self, submitted: bytes, now: int, schedules: list[ChainSchedule] | None = None) -> IssuanceResult:
        content = self.ingest(submitted)
        schedules = schedules or [ChainSchedule()]
        res = IssuanceResult(disposition="REFUSED")
        clock = now
        for n in range(1, self.p.N + 1):
            sched = schedules[min(n - 1, len(schedules) - 1)]
            declared = clock  # R-4.49 fresh declared time per attempt
            layer = build_attest_layer(object_type="OT_ATTEST", content=content, declared=declared,
                                       issuer_id=self.issuer_id, slot_keys=self.slot_keys,
                                       channels=self.channels, binding_forms=self.binding_forms,
                                       declared_set=self.declared_set,
                                       alg=self.slot_keys[0].alg)
            layer["anchor"] = anchor_layer(layer, self.chain, declared, sched, self.p.k)
            ok, why = self._predicate(declared, layer["anchor"])
            bundle = self._bundle(layer, declared)
            core = self._core(layer, declared)
            rec = AttemptRecord(n, declared, bundle, objects.attempt_id(core), ok, why)
            res.attempts.append(rec)
            if ok:  # Step 7: ship on the three conjuncts + depth; no envelope re-verification (R-4.77a)
                res.disposition = "SHIPPED"
                res.shipped = bundle
                clock = layer["anchor"]["headers"][-1]["time"]
                break
            # discarded; the attempt's window expires at declared + δ + S (R-4.45)
            clock = max(layer["anchor"]["headers"][-1]["time"], declared + self.p.delta + self.p.S) + 1
        # Step 8: terminal lineage record at terminal disposition, anchored (SC-1)
        res.tlr = self._tlr(res, clock)
        for a in res.attempts:
            a.bundle["standing"] = res.tlr
        if res.disposition == "REFUSED":
            # NOT BUILT beyond a stub: portable refusal record + commitment + PENDING states (R-4.61).
            res.refusal_record = {"status": "NOT BUILT (stub)", "delivery": "PENDING", "publication": "PENDING"}
        return res

    def _core(self, layer: dict, declared: int) -> dict:
        return objects.attempt_core(layer["manifest"]["tuple"],
                                    [p["sig_b64"] for p in layer["manifest"]["possession"]],
                                    [s["sig_b64"] for s in layer["slots"]], objects.ts(declared))

    def _bundle(self, layer: dict, declared: int) -> dict:
        a = layer["anchor"]
        return {
            "bundle_format": "tessera-proto-bundle/0",
            "layers": [layer],
            "embedded": objects.embedded_objects(),
            # Outside the signed bytes: R-3.46's "observed anchor delay" cannot be inside them.
            "issuance_record": {"issue_policy_version": objects.POLICY_VERSION,
                                "observed_anchor_delay_s": a["headers"][0]["time"] - declared},
        }

    def _tlr(self, res: IssuanceResult, clock: int) -> dict:
        lineage = [{"aid": a.aid, "disposition": "DISP_SHIPPED" if a.predicate_ok else "DISP_DISCARDED"}
                   for a in res.attempts]
        if res.disposition == "SHIPPED":
            terminal = {"kind": "TERM_SHIPPED", "aid": res.attempts[-1].aid}
        else:
            terminal = {"kind": "TERM_REFUSED"}
        body = {"tag": "TLR", "lineage": lineage, "terminal": terminal, "declared_terminal_time": objects.ts(clock)}
        fb = frame.encode("OT_TLR", frame.CANON_V1, jcs.canonicalize(body))
        entitled = self.slot_keys[0]  # GUESS G-25: the "entitled key" is the slot-A (primary) key
        anchor = anchor_layer({"slots": [{"frame_b64": b64e(fb)}]}, self.chain, clock, ChainSchedule(), self.p.k)
        return {"tlr": {"key_fp": entitled.fp, "alg": entitled.alg, "pubkey_b64": b64e(entitled.pub_raw),
                        "frame_b64": b64e(fb), "sig_b64": b64e(entitled.sign(fb))},
                "anchor": anchor}
