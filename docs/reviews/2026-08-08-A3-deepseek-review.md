Thank you for the invitation to provide a cold read of Amendment 3. I've carefully reviewed the document, along with the original preregistration and Amendments 1-2 for context.

## Executive Assessment

**No fatal errors detected.** The design is intellectually rigorous, internally consistent, and the amendment pattern itself demonstrates the discipline the project preaches. The document's primary strength is its honesty about irreducible residual risks—the pre-handoff death interval, the custody dependency, the exposed Layer 2 assumptions that no proof can discharge.

## Critical Observations

### 1. The "cold read" paradox is correctly flagged

Your author note in §A3.11 is the most honest part of the document. The 800-line amendment is a product of extended dialogue—you *cannot* cold-read it in the sense the pre-registration's epistemology requires. You've done the right thing by flagging this rather than pretending otherwise. The remedy (fresh external panel eyes) is appropriate.

### 2. The reliance-party story requirement (§A3.1.4) is the right addition

The "one page" artifact that opens with "Tessera can establish / does not establish" is precisely what bridges formal verification to real-world use. I'd suggest ensuring this page is drafted *before* Band 0 exit, not merely listed as an artifact—it will expose framing assumptions that the formal models might silently assume.

### 3. The first-link invariant (§A3.2.1) is well-stated but carries execution risk

The boundary invariant is sound. The mechanism spike will need to demonstrate that two manifests differing in authority-relevant facts cannot share the same evidence. This is straightforward to specify; less straightforward to test in a symbolic protocol model where equivalence queries may blow up. Consider whether the spike's timebox (unspecified in the amendment) should be explicitly noted in the review artifacts.

### 4. The unknown-algorithm verdict boundary (§A3.6) is a model-theater trap I'd watch for

You've correctly placed `UNVERIFIABLE` for unknown algorithms and `INVALID` for missing/malformed identifiers. The broken companion must fail-open—this is testable. But the permanent canary (one unrecognized identifier forever reserved) is clever: it prevents the code from atrophying the `UNVERIFIABLE` path. Ensure the canary is in the *formal model's* transition set, not just the test suite.

### 5. The tending obligations (§A3.5) introduce a new trust dimension

You're right that tending health never enters a receipt verdict. But the conditional visibility ("any holder of a current custodial record may observe the condition") is operationally weaker than it appears: a party holding an old receipt but no current custodial record has no visibility into custodian health. This is correctly exposed as a custodial dependency, not a Tessera guarantee. I'd suggest the dead-project demonstration explicitly test that an old bundle's verdict remains stable when custodial records are unavailable—that is, the `UNVERIFIABLE` path for the tending check (if any) is triggered, and `VALID_STRICT` is unaffected.

### 6. The refusal-record decomposition (§A3.7.2) names an honest impossibility

The pre-handoff death interval is a real residual. You've stated it rather than disguising it. The consequence is sharp: if the authority dies after local refusal but before handoff/publication, no surviving observer holds evidence. I'd consider whether the public commitment value could be *pre-computed* and revealed only on refusal—this moves the publishing moment earlier without requiring the refusal event to be externally witnessed. Not a flaw; a possible improvement.

### 7. The assessment-scope boundary (§A3.8) is appropriate

Making the base result unsigned but including a separate attested verification report as an optional typed wrapper is the correct separation. The unsigned result can be stripped by a non-conforming relay, but that's a conformance failure, not a cryptographic one—and you've flagged it as such.

### 8. The A2.1 bridge finding (A3.7.3) needs the non-author review it's pending

You've registered that the bridge finding's non-author review is part of this amendment's panel scope. Good. The prose repair ("issuer ships on full VALID_STRICT") resolves the ambiguity, but the bridge model already checked it. The review should confirm the model and prose now match.

## Suggestions for Strengthening

These are non-fatal; the design is sound as drafted.

1. **§A3.3 (capstone gate):** The "mechanism spike precedes suite scaffold" is sound. I'd add that the spike's three named outcomes—query violation, timeout, termination—each have a *predicted probability* registered before running. This is the H0 discipline applied at the tool-selection layer. "We expect timeouts on queries of complexity X" is testable; "we'll see what happens" is not.

2. **§A3.5 (tending):** The four-outcome record is good. I'd add that `ACTION_DUE` and `FAILED` are visible states with **deadlines**—a custodian can observe that a trigger fired 90 days ago with no renewal. The amendment says the last two outcomes "make the gap visible," but doesn't specify visible *to whom* and *when*. The "conditional visibility" section addresses this somewhat; I'd make the visibility boundary explicit: a holder of a current custodial record sees staleness; a holder of an old bundle does not, and that's intended.

3. **§A3.7.1 (standing):** The orthogonal assessment dimension is right. I'd ensure the dead-project demonstration tests standing on an abandoned artifact presented *alone*—this is the hard case. The amendment says it's testable, but the exact test harness isn't specified. The demonstration's evaluation conditions should record whether the abandoned artifact was presented with or without lineage context.

4. **§A3.2 (linked floors):** The two-worlds attack is a real threat. The amendment's linked-chain requirement closes it. I'd ensure the formal model's adversary capability set includes "control any subset of authority channels but not all"—this is in A1.3 but should be explicitly connected to the floor's proof obligation in the capstone ledger.

5. **The read timing (2026-08-08 vs your sign-off):** You're signing an amendment that cites review artifacts from 2026-07-28 and 2026-08-07. The timeline is tight but credible. I'd ensure the author cold-read note (§A3.11) is carried forward into the final signed document—it's an honest disclosure that strengthens, not weakens, the amendment's credibility.

## Summary

The design is coherent, the residual risks are appropriately exposed, and the amendment pattern itself—amending visibly, with reasons on record—is the method working as intended. The amendments have tightened the system without weakening any registered property. The A1.1 falsifier is not triggered.

I would sign this after the pending non-author review of the A3.7.3 bridge finding has been completed and any issues resolved.

Would you like me to dig deeper into any specific section?

# Addendum

Prompt: Thanks. This is quite helpful. The one item that nobody has addressed yet but is required (A3.9) is the A3.7.3 bridge finding disposition needs to be in scope for validation.

## Follow-up Response

You're right to flag that—the A3.7.3 bridge finding is a live wire that shouldn't be swept into the "pending review" column and forgotten. Let me give it the focused attention it deserves.

### A3.7.3 Bridge Finding Analysis

**The problem, restated.** A2.1's decoupled clocks ruling established that:
- Chain time governs evidence (the three-conjunct temporal predicate)
- Wall time governs the attempt lifecycle (the operational slack S)

The bridge model (`formal/tla/P5cP5P6_Bridge.tla`) surfaced that under this decoupling, the prose statement "The rule" in A2.1—which described only the confirmation conjunct (`confirmed_at ≤ declared + δ`)—did *not* imply the anchor-time conjunct (`anchor_time ≤ declared + δ`). An issuer who shipped solely on the confirmation conjunct could ship a receipt the verifier would reject.

**The repair, as registered.** The amendment's prose repair states: "the issuer evaluates the full `VALID_STRICT` predicate at ship — as the bridge model's Ship action already does." This is the authoritative resolution: the issuer ships on all three conjuncts, not on the confirmation conjunct alone.

**Validation check (what I'd verify in the non-author review):**

1. **Model-prose correspondence.** The bridge model's `Ship` action must evaluate the complete three-conjunct predicate. Is the TLA+ model committed? A2.1 says it's in `P5cP5P6_Bridge.tla`; the amendment says the bridge model "checks" this. I'd verify that:
   - `Ship` includes the anchor-time conjunct (`anchor_time ≤ declared + δ`)
   - The model's invariant includes the proposition "No shipped receipt fails the verifier's temporal check under the declared tolerances"
   - A broken companion exists where an issuer ships on confirmation conjunct alone and the invariant fails

2. **Issuer behavior, not just model.** The prose repair says "the issuer evaluates the full `VALID_STRICT` predicate." The formal model can prove the state machine's safety; the implementation must implement the same predicate. The A1.7 conformance vectors should include a case where:
   - The confirmation conjunct passes
   - The anchor-time conjunct fails (e.g., `anchor_time = declared + δ + 1` while `confirmed_at = declared + δ - 1`)
   - The issuer correctly refuses to ship

3. **The "no shipped receipt fails verifier" invariant is what matters.** The bridge finding's real threat was a shipped receipt that fails verification. The repair closes that. The disposition is sound if:
   - The model proves the invariant (shipped → verifier-acceptance under the same tolerances)
   - The implementation's ship gate implements the same predicate

4. **The residual the bridge finding does NOT close.** The abandoned-anchor artifact remains: an operationally abandoned attempt whose anchor confirms in-window but was never shipped. A2.0 registered this as an open residue; A2.2 and A2.4 confined standing; A3.7.1 adds the standing-evidence invariant. The bridge finding and the abandoned-anchor residue are *separate*:
   - Bridge finding: shipped receipts that fail verification (closed)
   - Abandoned-anchor residue: chain-valid but never-shipped receipts (governed by standing rules, not verification)

**What I'd want to see in the non-author review report:**

1. A clear statement: "The bridge model's `Ship` action was inspected; it evaluates all three temporal conjuncts. The broken companion demonstrates that a ship-on-confirmation-only variant fails the invariant."

2. A cross-check against the conformance vectors: the reviewer should verify that the vector suite includes both:
   - A late-burial artifact → `INVALID` (A2.2's new conjunct)
   - An in-window anchor but out-of-window burial → the issuer refuses to ship (the bridge repair's implementation evidence)

3. A note on whether the bridge model's "Ship" action and the P5c model's "Ship" action are now synchronized. The amendment says the bridge model already had the correct `Ship`; the repair is to the prose that described it incorrectly. The reviewer should confirm the prose and model now match.

4. The bridge finding's disposition status in the property tracker (`formal/PROPERTIES.md`). The amendment says A3.9 includes this as an artifact obligation; I'd verify it's recorded as `RESOLVED` with the bridge model's commit hash, not `PENDING` or `DEFERRED`.

### The Broader Pattern

What's interesting about this review requirement is that it's testing the *amendment discipline itself*. A2.1's decoupled clock ruling was correct, but it surfaced a prose/model mismatch that needed repair. The repair is now in the amendment; the non-author review validates that the repair actually fixes the mismatch. This is the method working as intended: the formal model catches the problem, the amendment registers the fix, the review confirms it, and the commit anchors it.

The remaining validation work, as I see it:

| Item | Status | What's needed |
|------|--------|---------------|
| A3.7.3 bridge finding | Registered | Non-author review of model/prose correspondence |
| A2.0 abandoned-anchor residue | A3.7.1 adds standing-evidence invariant | The standing test on an abandoned artifact alone |
| A2.1 clock-roles ruling | Ratified in A2.5 | The slack companions (`_Latch` variant) have non-author review? |

**Recommendation:** The A3.7.3 review should be conducted by a reviewer who can read the TLA+ bridge model and confirm the `Ship` action's predicate. The panel should include at least one reviewer with formal-methods competence—not just the symbolic protocol focus of A3.3's capstone work. If the panel doesn't have that, it's a gap.

Would you like me to draft a review protocol for this specific finding—what the reviewer should inspect, what broken companions to ask for, what conformance vectors must exist?
