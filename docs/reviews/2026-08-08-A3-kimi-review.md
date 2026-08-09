I have read Amendment 3 cold — no prior context from the 2026-08-07/08 authoring sessions, working only from the four committed documents.

**Fatal errors:** None. The amendment is internally consistent, consistent with the original preregistration and Amendments 1–2, and honest about its open mechanisms. It does not weaken any pre-registered property under the A1.1 falsifier.

**Near-fatal concerns:** None. The irreducible residuals (pre-handoff death interval in §A3.7.2, the model-to-code gap, the absence of human formal-methods review) are all named rather than concealed, which is exactly the discipline the project claims.

Below are suggestions for strengthening, ordered by leverage.

---

### 1. Formalize the standing-evidence mechanism in Band 0, not just as an implementation test (§A3.7.1)

§A3.7.1 introduces `protocol_standing` as an orthogonal assessment dimension that can be `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE` alongside the P4 verdict. This is load-bearing: a receipt can be `VALID_STRICT` yet have `ABSENT` standing, and the document correctly refuses to collapse this into a single checkmark.

**Gap:** The mechanism is left open ("A terminal lineage record, capability, transparency witness, or another construction may discharge the invariant"), with only a test criterion ("testable on an abandoned artifact presented alone").

**Suggestion:** Require that the chosen standing-evidence mechanism be modeled in the symbolic suite (ProVerif/TLA+) with the same adversarial rigor as P1–P10 before Band 0 exit. The adversary in A1.3 already includes replay, re-framing, and manifest crafting. A symbolic model should prove that an adversary cannot synthesize `ESTABLISHED` standing for an abandoned artifact without breaking the underlying hardness assumptions. This prevents standing from becoming a "test-only" property that the formal work does not actually cover.

---

### 2. Require an integrated end-to-end adversarial composition model (§A3.3)

§A3.3 mandates per-property ProVerif models and a capstone linkage query that discharges cross-model assumptions. This is strong.

**Gap:** The per-property decomposition may miss interaction faults between properties — e.g., whether a wrapper (P7) can be used to launder or override the standing evidence (§A3.7.1) of an inner artifact, or whether the refusal commitment (§A3.7.2) can be replayed into a different issuance context.

**Suggestion:** Add an explicit obligation for at least one integrated model in which the adversary drives the full protocol lifecycle: issuance → wrapping → supersession → refusal → verification → tending. The capstone linkage query checks compositional soundness; the integrated model checks for adversarial interactions that only appear when the adversary controls the full trace. This should include a broken companion where the adversary uses a wrapper to transplant standing from a valid inner artifact to a forged outer artifact.

---

### 3. Harden the exit criteria for the first-link mechanism spike (§A3.2.1)

The override in §A3.2.1 (boundary invariant replacing the digest-publication vs. authorized-tuple fork) is well-reasoned, but it leaves the design space very open.

**Gap:** The boundary invariant — "Two manifests that differ in any authority-relevant fact must not be supportable by the same evidence" — is only as strong as the definition of "authority-relevant." If the mechanism spike does not formally characterize this set, the broken companion ("two authority-distinct manifests share evidence; the consuming linkage query must fail") becomes a test of the implementation rather than a falsification of the property.

**Suggestion:** Require the mechanism spike to produce, as a Band 0 artifact, a formal *authority-relevance map*: an explicit enumeration of which manifest fields are authority-relevant (e.g., key fingerprints, issuer identity, algorithm identifiers) and which are non-authoritative (e.g., display labels, optional metadata). The broken companion must then demonstrate two manifests that differ *only* in an authority-relevant field and show that the same evidence cannot support both. This makes the boundary invariant checkable by inspection, not just by implementation testing.

---

### 4. Clarify whether standing is waivable under the A1.2.1 lattice (§A3.7.1)

§A3.2 tightens the waiver lattice to require a continuous evidentiary chain. §A3.7.1 says standing is orthogonal to P4.

**Gap:** The document does not explicitly state whether `protocol_standing = ABSENT` can be overridden by a degraded verifier policy. If a relying party can waive the standing requirement, then the "orthogonal dimension" collapses into the waiver lattice in practice. If they cannot, then standing is effectively a non-waivable check for any verdict that claims protocol participation.

**Suggestion:** State explicitly in §A3.7.1 (or in the A1.2.1 mapping) whether standing evidence is waivable. My reading is that it should be **non-waivable** for any artifact claiming `ESTABLISHED` standing, but that a degraded policy may accept `ABSENT` standing with explicit recording — analogous to how `VALID_DEGRADED` records waived signature checks. This preserves the orthogonality while keeping the lattice monotonic.

---

### 5. Add a bundle-size governance rule for embedded specifications (§A3.4)

§A3.4 requires embedding "the Tessera verification specification and its conformance vectors" in every receipt bundle.

**Gap:** For a high-volume service, embedding a full specification in every bundle could create a significant size penalty. The document mentions content-addressed deduplication in aggregate preservation, but does not bound the per-bundle cost.

**Suggestion:** Add a hard invariant or a declared budget: e.g., "The embedded specification and conformance vectors shall not exceed N kilobytes per bundle; if the specification exceeds this bound, the bundle embeds a content-addressed reference (hash + retrieval identifier) and the full specification is published in a content-addressed store." This prevents an unbounded size obligation from becoming a covert denial-of-service vector against issuers or storage systems.

---

### 6. Require renderer conformance vectors (§A3.8)

§A3.8 states that "Every Tessera-controlled or conforming third-party surface that renders a result also renders its scope and the material independent dimensions" — the rendering red-bar.

**Gap:** This is a conformance rule, but the document does not specify how to test whether a renderer violates it. A non-conforming relay can strip scope and present a misleading checkmark; the document acknowledges this but does not make it mechanically detectable.

**Suggestion:** Add a requirement for **renderer conformance vectors**: a set of structured assessment outputs that a conforming renderer must display in full, and a set of malformed renderings (stripped scope, collapsed dimensions, missing `UNVERIFIABLE` context) that must fail a mechanical validation test. This makes the red-bar rule auditable in CI, not just a policy assertion.

---

### 7. Require a minimal tending policy skeleton for Band 0 exit (§A3.5)

§A3.5 correctly defers exact trigger expressions, cadence, and succession mechanisms to custodial practice.

**Gap:** Because no tending mechanism is required at Band 0, the survivability claim 3 ("long-horizon evidentiary continuity") is largely aspirational for the demonstration. The gap between "designed for renewal" and "renewal is possible" is not bridged by code.

**Suggestion:** Require that Band 0 exit include a **minimal tending policy artifact** — even if it declares `NO_ACTION_REQUIRED` for the PoC's expected lifetime, with triggers sized to the demonstration horizon (e.g., "assess algorithm viability annually; trigger if NIST post-quantum standard supersedes current algorithm"). This makes the tending machinery concrete and testable, and prevents the obligation from being silently punted to a future that never arrives.

---

### Summary

Amendment 3 is fit to sign. The architecture is coherent, the residuals are honest, and the additions (survivability, tending, standing, assessment scope) close real gaps without weakening prior commitments. The suggestions above are about raising the bar on *checkability* — making open mechanisms formally accountable, making renderer rules testable, and making the tending and standing machinery concrete before Band 0 closes — rather than correcting defects.


# Addendum

Prompt: Thanks. This is quite helpful. The one item that nobody has addressed yet but is required (A3.9) is the A3.7.3 bridge finding disposition needs to be in scope for validation.

## Follow-up Response

You are right to flag this — I did not explicitly validate the A3.7.3 disposition in my first pass. Reading it cold now:

**Fatal errors: none.** The disposition is logically sound and consistent with the decoupled-clock architecture of A2.1. But I see one precision risk and one checkability gap that are worth tightening before the amendment is signed.

---

### The finding, restated cold

A2.1’s formal rule sentence states issuance completion by **conjunct 3 alone**:

> `confirmed_at ≤ declared_issue_time + δ`

Under decoupled clocks, block timestamps are non-monotonic, so conjunct 3 does **not** imply conjunct 2 (`anchor_time ≤ declared_issue_time + δ`). An issuer that ships on conjunct 3 alone could produce an honestly-shipped receipt that the verifier rejects — a divergence between issuance and verification that violates the correspondence A1.4 demands.

A3.7.3’s repair is to register that the issuer evaluates the **full three-conjunct temporal predicate** before shipping, noting that the bridge model’s `Ship` action already does so. This is the correct fix.

---

### What keeps it from being fatal

The surrounding prose in A2.1 already gestures at the full predicate (“evaluates this conjunct **as part of** the full three-conjunct temporal predicate”), and the bridge model (`P5cP5P6_Bridge.tla`) is the ground truth. The gap is between the *adopted formal rule statement* and the *model behavior*, not between the model and the intended protocol. Since A2 is frozen, the repair living in A3.7.3 is the right archival pattern.

---

### Suggestions to strengthen the disposition

**1. Scope “full VALID_STRICT predicate” to the temporal conjuncts**

A3.7.3 says the issuer evaluates the **full `VALID_STRICT` predicate** at ship. In the verifier, `VALID_STRICT` includes P1 (integrity), P2 (signature-set completeness), P3 (key binding), etc. The issuer should not be verifying its own signatures or key bindings at ship time — that would confuse the issuance protocol with the verification protocol.

**Suggested edit:** Change to “the issuer evaluates the **full P5 temporal conjunct set** (all three conjuncts of A2.2) before shipping.” This preserves the repair while avoiding the implication that the issuer re-runs the entire verifier state machine.

**2. Add an explicit issuance conformance vector for the decoupled-clock divergence case**

The gap only manifests when block timestamps run backwards enough that `confirmed_at` is in-window but `anchor_time` is not. This is a real (if rare) Bitcoin phenomenon.

**Suggested addition to A3.9:** A conformance vector (model-derived or adversarially authored) in which:
- `declared_issue_time = T`
- `anchor_time = T + δ + 1` (fails conjunct 2)
- `confirmed_at = T + δ − 1` (passes conjunct 3)

The required issuer behavior is **refuse to ship** (discard and re-issue). The vector should be extracted from the bridge model and included in the H1a red-bar suite as a dedicated issuance-path test. Without this vector, the implementation could pass all verifier tests while still shipping divergent receipts.

**3. Require the bridge model review to explicitly confirm the three-conjunct check**

A3.7.3 notes that non-author review of the bridge finding is pending in this amendment’s panel scope. I suggest adding a **specific review prompt**: “Confirm that the bridge model’s `Ship` action evaluates all three A2.2 conjuncts atomically, and that no trace exists in which `Ship` fires while conjunct 2 is violated.” This makes the review falsification-style (A1.7 discipline) rather than a general pass/fail on the model.

**4. Forward-reference marker on A2.1**

Because A2 is ADOPTED and immutable, future readers may consult A2.1’s “The rule” paragraph in isolation and miss A3.7.3. The project already archives review artifacts; I suggest adding a **one-line marginal note** in the A2.1 archive (or in the PROPERTIES tracker) stating:

> *Formal rule statement incomplete under decoupled clocks; superseded by A3.7.3 — issuer must evaluate full P5 temporal conjunct set.*

This is a documentation hedge, not a normative change, and it prevents the frozen A2.1 text from being mistaken for the current rule.

---

### Bottom line

The A3.7.3 disposition is **correct and safe to sign**, but the four tightenings above would move it from “prose repair with model backup” to “mechanically checked and auditable” — consistent with the project’s ethos of making gaps visible and closing them with evidence rather than assertion.
