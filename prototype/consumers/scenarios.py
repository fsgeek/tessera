"""Build every bundle the phase-2 consumers are run against, in one stub world (THROWAWAY).

The builder is the *experimenter*, not a consumer: it may use attacker capabilities and the
issuer's internals. The consumers only ever see the bundles, files and trust configuration it hands
them.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field

from tessera_proto import attacks
from tessera_proto.crypto import KeyPair
from tessera_proto.issuer import ChainSchedule, Channel, Issuer, anchor_layer, build_attest_layer
from tessera_proto.world import T0, World, make_world

from .submitter import Release, Submitter, acme_release

HOUR = 3600
ORG = "Acme Corp"


@dataclass
class Case:
    key: str
    title: str
    bundle: dict
    release: Release            # the files the relying party downloaded next to the bundle
    genuine: bool               # ground truth: is this Acme's real release, properly attested?
    spec_says: str              # what the spec says the right envelope outcome is, in words
    world_facts: dict = field(default_factory=dict)   # facts true in the world but not in any input
    policies: tuple = ("strict", "degraded")


@dataclass
class Scenario:
    world: World
    submitter: Submitter
    honest_release: Release
    evil_release: Release
    honest_payload: bytes
    cases: dict[str, Case]

    def trust(self, **kw):
        """The relying party's trust configuration as R-5.8 lists it, fetched now (fresh header store)."""
        return self.world.trust(**kw)


def evil_statement(sub: Submitter, rel: Release) -> dict:
    """The statement an attacker wants believed: Acme's name and version, the attacker's tarball."""
    return json.loads(sub.statement_digests(rel))


def build(mode: str | None = None) -> Scenario:
    """mode "stub" (phase 1-2 default) or "real" (phase 3: tessera_proto/real/world.py). Default comes
    from tessera_proto.real.MODE, i.e. the TESSERA_PROTO_MODE environment variable, else "stub"."""
    from tessera_proto import real
    mode = mode or real.MODE
    if mode == "real":
        from tessera_proto.real.world import make_world_real
        w = make_world_real()
    else:
        w = make_world()
    honest, evil = acme_release(), acme_release(evil=True)
    sub = Submitter(ORG, w.issuer, w.trust())
    out = sub.submit(honest, T0)
    at_ship = sub.receipt_at_ship(out)
    full = sub.complete_receipt(out)
    cases: dict[str, Case] = {}

    cases["a"] = Case("a", "honest receipt, complete (TLR appended)", full, honest, True,
                      "VALID_STRICT, standing ESTABLISHED")
    cases["g"] = Case("g", "honest receipt as shipped, before the TLR exists", at_ship, honest, True,
                      "VALID_STRICT, standing ABSENT (S3: NO_TERMINAL_DISPOSITION_EVIDENCE)")

    # (b) C-C2 reattribution of the honest slot-B frame (honest statement, attacker keys).
    rp2 = attacks.replay_cc02(w, full, T0 + 3 * HOUR)
    cases["b"] = Case("b", "C-C2 reattribution: Acme's genuine statement under attacker keys", rp2.bundle,
                      honest, False, "INVALID (V17/V18): the attribution is forged even though the files are genuine")

    # (c) C-C5 transplant. The attacker puts its own release statement in both layers.
    ev = evil_statement(sub, evil)
    rp5 = attacks.replay_cc05(w, full, T0 + 3 * HOUR, inner_content=ev, outer_content=ev)
    c5 = Case("c", "C-C5 wrapped inner-signature transplant (evil tarball)", rp5.bundle, evil, False,
              "outer layer VALID_DEGRADED (attacker's own wrapper, registered cost); inner layer INVALID (V19)")
    c5.world_facts["dsks"] = rp5.dsks   # adversary capability; passed to the verifier as phase 1 does
    cases["c"] = c5

    # (d1) honest receipt verified under a degraded policy, repo evidence present.
    cases["d1"] = Case("d1", "honest receipt, degraded policy (repo waived, evidence present)", full, honest, True,
                       "VALID_DEGRADED, repo observation would-pass", policies=("degraded",))
    # (d2) honest receipt whose repo evidence was lost in custody.
    lost = copy.deepcopy(full)
    lost["layers"][0]["manifest"]["evidences"] = [e for e in lost["layers"][0]["manifest"]["evidences"]
                                                  if e["channel"] != "repo"]
    cases["d2"] = Case("d2", "honest receipt, repo evidence lost in custody", lost, honest, True,
                       "strict: UNVERIFIABLE; degraded: VALID_DEGRADED, repo observation absent")
    # (d3) the registered degraded cost: an attacker holding the leaked dns channel key runs its own
    # copy of the issuer under Tessera's issuer id, with its own key, and mints its own TLR.
    clone = Issuer(w.issuer.issuer_id, [KeyPair.generate("attacker-clone")], [Channel("dns", w.dns.key)],
                   w.chain, w.params)
    r3 = clone.issue(json.dumps(ev).encode(), T0 + 4 * HOUR)
    cases["d3"] = Case("d3", "attacker clone issuer with leaked dns key (evil tarball, own TLR)", r3.shipped,
                       evil, False, "strict: UNVERIFIABLE; degraded: VALID_DEGRADED (registered cost R-1.11, R-6.43)")

    # (e) honest receipt; in the world, slot-B's key was revoked 60 s after the declared time,
    # i.e. inside (declared, anchor]. The bundle bytes are identical to (a).
    declared = full["layers"][0]["anchor"]["headers"][0]["time"] - full["issuance_record"]["observed_anchor_delay_s"]
    cases["e"] = Case("e", "honest receipt; slot-B key revoked inside (declared, anchor]", full, honest, False,
                      "INVALID (R-5.21): revocation effective at or before anchor_time",
                      {"revoked": {w.skB2.fp: declared + 60}})

    # (f) an impostor submits Acme's name with the evil tarball through the honest service.
    r6 = w.issuer.issue(json.dumps(ev).encode(), T0 + 5 * HOUR)
    cases["f"] = Case("f", "impostor submits 'Acme Corp' + evil tarball through the honest service",
                      r6.shipped, evil, False, "VALID_STRICT, ESTABLISHED: the spec attests bytes, not submitters")
    # (h) an honest renewal: a custodian wraps the complete honest receipt (R-7.46). The custodian's
    # channel evidence is minted by the same stub channels (the model's one-key-per-channel reading).
    skW = KeyPair.generate("custodian")
    inner = full["layers"][0]
    emb = [{"slot": s["slot"], "frame_b64": s["frame_b64"], "sig_b64": s["sig_b64"]} for s in inner["slots"]]
    now = T0 + 6 * HOUR
    outer = build_attest_layer(object_type="OT_WRAPPER", content={"renewal": "custodial wrap", "of": "acme-widget-1.4.2"},
                               declared=now, issuer_id="archive.example", slot_keys=[skW], channels=[w.dns, w.repo],
                               extra_common={"inner": {"cv": 1, "slots": emb}, "outer_cv": 1})
    outer["anchor"] = anchor_layer(outer, w.chain, now, ChainSchedule(), w.params.k)
    inner_entry = {"object_type": "OT_ATTEST", "manifest": inner["manifest"], "anchor": inner["anchor"],
                   "slots": [{k: s[k] for k in ("slot", "alg", "pubkey_b64")} for s in inner["slots"]]}
    wrapped = {"bundle_format": full["bundle_format"], "layers": [outer, inner_entry], "embedded": full["embedded"],
               "standing": full["standing"]}
    cases["h"] = Case("h", "honest custodial renewal wrapper around the complete honest receipt", wrapped, honest, True,
                      "both layers VALID_STRICT; standing for wrapped layers is routed to S-P7 (R-6.44)")
    return Scenario(w, sub, honest, evil, out.accepted_payload, cases)
