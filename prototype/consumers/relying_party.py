"""Consumer 2: the RELYING PARTY, today (THROWAWAY).

It holds: a downloaded tarball and SBOM, the bundle published next to them, the public reference
verifier, a trust configuration with exactly the members R-5.8 lists (channel keys, k, delta,
epsilon, header store -- no revocation member, because R-5.8 has none), and a declared policy. It
wants one decision: install Acme's release or not.

Two integrators are modelled, because the spec leaves the decision rule to "relying-party policy"
(R-1.16, R-5.42, R-5.56) and different readers will write different rules:

* NAIVE -- a reasonable non-expert who has read §1.5. Shows the headline verdict (the first entry
  in the per-layer list) and checks that the tarball's sha256 appears in what was attested.
  VALID_DEGRADED reads as "valid, with a caveat". Standing is "beside the verdict" and ignored.
* CAREFUL -- reads every field: every layer VALID_*, innermost issuer id = the service it expects,
  innermost standing ESTABLISHED, no waived evidence observed invalid / names-other-key, digest in
  the innermost layer's content.

Neither integrator is given anything the spec does not give it.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from tessera_proto import frame, jcs
from tessera_proto.crypto import b64d
from tessera_proto.verifier import FAIL, PASS, UNPERF, Policy, _ladder, verify_bundle

from .log import BLOCKED, CONFUSED, NOTE, WORKED, ConsumerLog

STRICT = Policy()
DEGRADED = Policy(name="degraded-waive-repo", waive_channels=frozenset({"repo"}))
POLICIES = {"strict": STRICT, "degraded": DEGRADED}
EXPECTED_ISSUER = "wamason.com"   # the Tessera service the integrator was told to trust


def layer_statements(bundle: dict) -> list[dict | None]:
    """Decode what each layer attests (slot A's common). Needs the frame layout (G-01) and the
    payload schema (G-15): the verifier report does not return content (R-5.44)."""
    out = []
    layers = bundle.get("layers") or []
    material = layers[0].get("slots", []) if layers else []
    for i, lay in enumerate(layers):
        try:
            fb = b64d(material[0]["frame_b64"])
            common = jcs.parse_strict(frame.decode(fb)[0].payload)["common"]
        except Exception:
            out.append(None)
            break
        out.append(common)
        inner = common.get("inner")
        if isinstance(inner, dict):
            material = inner.get("slots", [])
    return out


def digest_in(common: dict | None, digest: str) -> bool:
    if not common:
        return False
    arts = (common.get("content") or {}).get("artifacts") or []
    return any(a.get("sha256") == digest for a in arts if isinstance(a, dict))


@dataclass
class Decision:
    accept: bool
    why: str


@dataclass
class CaseResult:
    case: str
    policy: str
    layers: list[tuple[str, str | None, str | None]]   # (verification, standing value, standing reason)
    waivers: dict
    failed: list[str]
    unperformable: list[str]
    naive: Decision
    careful: Decision
    safe_accept: bool
    notes: list[str] = field(default_factory=list)

    def outcome(self, d: Decision) -> str:
        if d.accept == self.safe_accept:
            return "correct"
        return "UNSAFE ACCEPT" if d.accept else "false reject (safe, costly)"


class RelyingParty:
    def __init__(self, trust):
        self.trust = trust
        self.log = ConsumerLog("relying party")

    def verify(self, bundle: dict, policy: str, dsks=None) -> dict:
        return verify_bundle(bundle, self.trust, POLICIES[policy], dsks=dsks)

    def naive(self, rep: dict, bundle: dict, tar_sha: str) -> Decision:
        v = rep["layers"][0]["verification"]
        sts = layer_statements(bundle)
        found = any(digest_in(c, tar_sha) for c in sts)
        if v.startswith("VALID") and found:
            return Decision(True, f"headline {v}; tarball digest is in the attested statement")
        return Decision(False, f"headline {v}; digest {'found' if found else 'not found'}")

    def careful(self, rep: dict, bundle: dict, tar_sha: str) -> Decision:
        Ls = rep["layers"]
        bad = [x["verification"] for x in Ls if not x["verification"].startswith("VALID")]
        if bad:
            return Decision(False, f"a layer is {bad[0]}")
        sts = layer_statements(bundle)
        inner, innerL = sts[-1], Ls[-1]
        if (inner or {}).get("issuer_id") != EXPECTED_ISSUER:
            return Decision(False, f"innermost issuer is {(inner or {}).get('issuer_id')!r}")
        st = Ls[0].get("protocol_standing") if len(Ls) == 1 else innerL.get("protocol_standing")
        if not st or st.get("value") != "ESTABLISHED":
            return Decision(False, f"standing {st and st.get('value')}/{st and st.get('reason')}")
        for x in Ls:
            for g, w in x["waivers"].items():
                if w["observation"] in ("invalid", "names-other-key"):
                    return Decision(False, f"waived {g} observed {w['observation']}")
        if not digest_in(inner, tar_sha):
            return Decision(False, "digest not in innermost statement")
        return Decision(True, "all layers VALID_*, issuer as expected, standing ESTABLISHED, digest matches")

    def run(self, case, policy: str) -> CaseResult:
        tar_sha = hashlib.sha256(case.release.tarball).hexdigest()
        rep = self.verify(case.bundle, policy, case.world_facts.get("dsks"))
        Ls = rep["layers"]
        lay = [(x["verification"], (x.get("protocol_standing") or {}).get("value"),
                (x.get("protocol_standing") or {}).get("reason")) for x in Ls]
        return CaseResult(case.key, policy, lay, {i: x["waivers"] for i, x in enumerate(Ls) if x["waivers"]},
                          [f for x in Ls for f in x["failed"]], [f for x in Ls for f in x["unperformable"]],
                          self.naive(rep, case.bundle, tar_sha), self.careful(rep, case.bundle, tar_sha),
                          case.genuine)

    # ------------------------------------------------------------- revocation (case e)
    def revocation_view(self, bundle: dict, policy: str = "strict") -> dict:
        """What the relying party can and cannot learn about revocation from its inputs."""
        rep = self.verify(bundle, policy)
        L0 = rep["layers"][0]
        rev = {c: x for c, x in L0["checks"].items() if c.startswith("REV[")}
        members = sorted(bundle)
        carriers = [m for m in members if "revoc" in m.lower()]
        trust_members = sorted(vars(self.trust))
        common = layer_statements(bundle)[0] or {}
        t = bundle["layers"][0]["manifest"]["tuple"]
        a = bundle["layers"][0]["anchor"]
        anchor_time = a["headers"][0]["time"]
        from tessera_proto.objects import parse_ts
        declared = parse_ts(common.get("declared_issue_time", "1970-01-01T00:00:00Z"))
        # The verdict a spec-faithful verifier gives under the other reading of R-5.21 with no input:
        # the required revocation check cannot be performed -> UNVERIFIABLE, for EVERY bundle.
        from tessera_proto.verifier import Checks
        cks = Checks()
        for cid, x in L0["checks"].items():
            st = UNPERF if cid.startswith("REV[") else x["status"]
            cks.add(cid, st, "REVOCATION_FACTS_NOT_IN_ANY_INPUT" if cid.startswith("REV[") else x["reason"], x.get("group"))
        unperf_reading, _ = _ladder(cks, POLICIES[policy], set())
        view = {
            "bundle_members": members, "bundle_members_carrying_revocation": carriers,
            "trust_config_members_R-5.8": [m for m in trust_members if m != "revocations"],
            "reported_REV_checks": {c: x["status"] for c, x in rev.items()},
            "verdict_as_reported": L0["verification"],
            "verdict_if_REV_unperformable": unperf_reading,
            "learnable_window": {"declared": declared, "anchor_time": anchor_time,
                                 "signer_key_fps": [t["key_fp"], *t["sset"]]},
        }
        self.log.add(BLOCKED, "No bundle member and no R-5.8 trust-configuration member carries a revocation "
                              "fact, so R-5.21's check has no input; the relying party can compute the window "
                              f"(declared, anchor] = ({declared}, {anchor_time}] that matters, and nothing else",
                     "R-5.21, R-5.4, R-5.8, GUESSES G-27")
        if rev and all(x["status"] == PASS for x in rev.values()):
            self.log.add(CONFUSED, "The report lists REV[A]/REV[B] as 'pass' although nothing was checked: an "
                                   "empty revocation input reads as 'not revoked'. A required check reported as "
                                   "passed without being performed is the misreport R-5.33 forbids",
                         "R-5.33, R-2.32")
        self.log.add(NOTE, f"Under the opposite, fail-closed reading (the check is required and cannot be performed) "
                           f"the same honest bundle is {unperf_reading}, and so is every bundle ever issued",
                     "R-5.21, R-2.32, R-5.25")
        self.log.add(NOTE, "As adjudicator the relying party may use anything (R-1.22) -- but the spec defines no "
                           "revocation publication, no format, and no time-authenticated record of when a "
                           "revocation took effect, so there is nothing defined to fetch", "R-1.22, R-5.24")
        return view


def run_all(sc) -> tuple[RelyingParty, list[CaseResult], dict]:
    rp = RelyingParty(sc.trust())
    results = []
    for key in ("a", "g", "b", "c", "d1", "d2", "d3", "e", "f", "h"):
        case = sc.cases[key]
        for pol in case.policies:
            results.append(rp.run(case, pol))
    rev = rp.revocation_view(sc.cases["e"].bundle)
    # Variant of (e) with the prototype's G-27 extension: the facts are handed in out of band.
    e_ext = verify_bundle(sc.cases["e"].bundle, sc.trust(revocations=sc.cases["e"].world_facts["revoked"]))
    rev["verdict_with_G27_extension"] = e_ext["layers"][0]["verification"]
    rev["failed_with_G27_extension"] = e_ext["layers"][0]["failed"]
    _log_matrix(rp, results)
    return rp, results, rev


def shape(r: CaseResult) -> tuple:
    """Everything a relying party can see in a report, minus identifiers that differ per key."""
    return (tuple(r.layers), tuple(sorted((i, g, w["observation"]) for i, ws in r.waivers.items()
                                          for g, w in ws.items())), tuple(r.failed), tuple(r.unperformable))


def _log_matrix(rp: RelyingParty, results: list[CaseResult]) -> None:
    by = {(r.case, r.policy): r for r in results}
    L = rp.log
    c = by.get(("c", "degraded"))
    if c:
        L.add(CONFUSED, f"C-C5: the report's first entry says {c.layers[0][0]} and the second says {c.layers[1][0]}. "
                        "Nothing tells the integrator which layer answers 'is this release attested'; the spec "
                        "forbids an aggregate and leaves the rule to relying-party policy", "R-5.42, R-5.47, R-1.18, R-7.49")
    d2, d3 = by.get(("d2", "degraded")), by.get(("d3", "degraded"))
    if d2 and d3 and shape(d2) == shape(d3):
        L.add(CONFUSED, "An honest receipt whose repo evidence was lost (d2) and an attacker's receipt minted with "
                        "the leaked dns key under Tessera's issuer id, with its own TLR (d3), produce the same "
                        f"report: {d2.layers[0][0]}, standing {d2.layers[0][1]}, repo observation 'absent'. "
                        "Only the issuer key fingerprint differs, and the trust configuration holds no issuer "
                        "key to compare it with", "R-1.11, R-5.31, R-6.43, R-5.8")
    f = by.get(("f", "strict"))
    if f:
        L.add(CONFUSED, f"Impostor (f): {f.layers[0][0]} / {f.layers[0][1]} on a statement naming 'Acme Corp' "
                        "that Acme never made. Correct by the spec (bytes, not submitters) and fatal for the "
                        "integrator, who has no field that says who submitted", "R-1.1, R-1.4, §2.1, R-3.36 'bound, not validated'")
    g = by.get(("g", "strict"))
    if g:
        L.add(CONFUSED, f"Fresh receipt (g): {g.layers[0][0]} with standing {g.layers[0][1]}/{g.layers[0][2]}. "
                        "§1.5 says 'you may still use it, on your own judgement'; an integrator cannot tell a "
                        "too-early honest receipt from an abandoned artifact presented alone (both S3)", "R-6.30 S3, R-4.88(iv), §1.5")
    d2s = by.get(("d2", "strict"))
    if d2s and d2s.layers[0][1] is None:
        L.add(CONFUSED, f"Strict policy, repo evidence lost (d2): verification {d2s.layers[0][0]} and standing "
                        f"value None ({d2s.layers[0][2]}). The model emits no standing report when the authority "
                        "step cannot proceed, so the output has a hole the vocabulary does not name",
              "R-6.24 step 1, R-5.46, GUESSES G-34")
    h = by.get(("h", "strict"))
    if h:
        L.add(CONFUSED, f"Honest renewal wrapper (h): layers {[x[0] for x in h.layers]}, inner standing "
                        f"{h.layers[-1][1]}. The careful rule that rejects C-C5 (every layer VALID, inner standing "
                        f"ESTABLISHED) also rejects this honest wrap ({h.careful.why}): standing for a wrapped layer "
                        "is not defined", "R-6.44, R-7.49, R-1.18")
    b = by.get(("b", "strict"))
    if b:
        L.add(WORKED, f"C-C2: {b.layers[0][0]} under both policies; both integrators reject. Reason codes name "
                      "the binding checks (V17/V18)", "R-5.35, V17, V18")
    a = by.get(("a", "strict"))
    if a:
        L.add(WORKED, f"Honest complete receipt: {a.layers[0][0]} / {a.layers[0][1]}; both integrators accept", "§1.5")
