**No fatal errors that would make the design incoherent, unimplementable under the registered constraints, or that would silently undermine H0 / the dual-signature + temporal-anchor construction.**

Amendment 3 is a careful, mostly strengthening document. It closes real residues from A2, tightens the waiver lattice in a way that preserves prior valid verdicts, makes the identity boundary and evidence floors explicit, and correctly refuses to claim more than the construction can support (especially on survivability and the pre-handoff death residual for refusals). The A1.1 falsifier is not triggered: no property is weakened, no adversary capability is excluded, and the construction remains dual-signature + temporal anchor. The mechanism-open posture is consistent with the project’s declared method.

That said, several design points are fragile enough that they could become de-facto fatal under realistic long-horizon or adversarial use if left unaddressed. Below I separate true show-stoppers (none found) from high-severity design risks and concrete strengthening suggestions.

### High-severity design risks (not fatal today, but likely to become so)

1. **Survivability Claim 1 vs. the Designated Community competence profile**
   The bundle now embeds the Tessera verification specification + conformance vectors and binds the verification-spec identity/hash into the signed bytes. This is good. However, the competence profile still assumes a member can “implement or execute the deterministic Tessera verification procedure” using only ordinary documented tools + the bundle.
   If the embedded specification is a prose + vector document rather than an executable (or formally executable) artifact, the “dead-project” demonstration becomes a human-skill test rather than a mechanical one. Over multi-decade horizons this is the classic OAIS Representation Information failure mode. The century-horizon language correctly labels this aspirational, but the Designated Community declaration itself still over-claims reconstructability.

2. **Refusal residual (A3.7.2)**
   The three-state-machine decomposition (local REFUSED + delivery + publication) is honest and correctly names the irreducible residual: if the generating authority dies after the local latch but before handoff *and* before publication, no surviving evidence of the refusal exists.
   This is the right call. The residual is, however, larger than the text acknowledges once you consider correlated failure modes (the same fee/congestion/calendar events that produce clusters of refusals also make the publication channel unavailable). The independence declaration required of the publication channel is necessary but currently untestable under the no-spend constraint.

3. **Standing evidence (A3.7.1)**
   The invariant is correct: cryptographic validity alone confers no protocol standing; standing evidence must be present and bind issuance identity + attempt lineage + terminal disposition.
   Leaving the mechanism open is fine, but the testability requirement (“must be testable on an abandoned artifact presented alone”) is strong. Any mechanism that relies on a later lineage record or external transparency log will fail that test by construction. This creates pressure toward a self-contained standing proof inside the shipped receipt, which then collides with the “exactly one shipped anchor” rule of A2.4.

4. **Evidence-floor first-link invariant (A3.2.1)**
   Declining both docketed options (digest publication vs. authorized tuple) in favor of a boundary invariant is defensible, but it defers the hardest part of the two-worlds attack to the spike. The spike must produce a concrete broken companion in which two authority-distinct manifests share evidence *and* the consuming linkage query fails. If the spike cannot find a clean encoding that satisfies the invariant without self-reference, Band 0 will stall exactly where the original H0 gate was meant to be decisive.

5. **Header authentication residual (carried forward from A2.1)**
   A2 already flagged that bundled headers are only a candidate chain segment. A3 does not strengthen the authentication rules. A privately-mined in-window fork presented in a bundle remains a live acceptance path under naive evaluation. This is still inside the “header provenance” residual, not closed.

### Strengthening suggestions (ordered by leverage)

**Immediate / low-cost (can be done before signing A3)**

- Make the embedded verification specification *executable in principle*. Require that the typed object in the bundle be either (a) a formal model fragment that a machine checker can re-verify or (b) a pure-function reference implementation in a language with a publicly frozen semantics (e.g., a restricted subset of Python or a small pure functional language). Prose + vectors alone is insufficient for the Designated Community claim.
- Explicitly register the standing-evidence mechanism as “must be self-contained in the shipped receipt or in a contemporaneous, independently anchored transparency record that the receipt itself commits to.” This forces the design space closed before the spike rather than after.
- Add a quantitative bound on the pre-handoff death residual for refusals: “The generating authority shall attempt delivery and publication with a declared maximum latency T; after T the residual is accepted and the attempt is marked DELIVERY_EXPIRED / PUBLICATION_EXPIRED.” Without a bound the residual is unbounded.

**Medium-term (Band 0 exit artifacts)**

- Capstone linkage query must include a two-worlds broken companion that actually exercises the first-link invariant, not merely cardinalities. Treat failure of the spike to produce such a companion as a trigger for a further amendment, not a soft “mechanism still open.”
- Header authentication: require the verifier policy to pin either (a) a set of checkpoint hashes or (b) a minimum cumulative-work threshold relative to a known-good tip, both of which travel with the trust configuration (same pattern as the historical trust-anchor store). Make the absence of such a pin an explicit UNVERIFIABLE case.
- Dead-project demonstration protocol: pre-register the evaluation conditions more tightly (verifier provenance must be a model or human who has never seen any Tessera source, challenge set generated after the bundle is sealed, etc.). Record the conditions as a first-class artifact.

**Structural / long-horizon**

- Survivability Claim 3 (long-horizon evidentiary continuity) currently relies on custodial renewal under an ERS-style policy. Add an explicit “renewal window” parameter that is itself attested and visible in the tending record. Without it, a custodian can always claim the trigger had not yet fired.
- Consider whether the optional signed verification report (A3.8) should be the *only* way a Tessera-controlled surface is allowed to emit a result that will be relayed. This would make the rendering red-bar mechanically enforceable rather than a conformance hope.

### Minor consistency / clarity notes (non-fatal)

- A3.7.3 correctly registers the bridge finding as a prose repair. The non-author review of that repair should be in scope for the A3 panel; otherwise the repair sits in a soft state.
- The category-(b) register at the end is useful for the author; for external readers it would be clearer if each item carried a one-line “status: ratified / pending cold read” marker.
- The Designated Community declaration still contains a slight tension between “can reconstruct \ldots without Tessera-specific institutional knowledge” and the later statement that horizons requiring Claims 2 and 3 make the Community a *custodian*. The custodial role is correctly named, but the reconstructability claim should be scoped more tightly to Claim 1 only.

### Bottom line

The design is sound enough to proceed to cold non-author review and, after that, signature. The most important residual risks are:

- reconstructability of the verification procedure itself over long horizons,
- the self-contained standing-evidence requirement colliding with A2.4,
- and the still-open first-link binding for the evidence floor.

None of these is a silent contradiction or an unprovable claim under the current wording. They are all visible, named, and open to mechanism choice or further amendment. That is exactly the discipline the pre-registration set out to enforce.

I am happy to do a second pass focused on any single section (especially A3.2 / A3.4 / A3.7) or to draft concrete text patches for the high-severity items if that would be useful before the formal panel.

# Addendum

Prompt: Thanks. This is quite helpful. The one item that nobody has addressed yet but is required (A3.9) is the A3.7.3 bridge finding disposition needs to be in scope for validation.

## Follow-up Response

**Validated.** The A3.7.3 bridge-finding disposition is correct, necessary, and already consistent with the adopted A2 text and the bridge model. No fatal error, no weakening, and no new residual introduced.

### What the finding actually is
A2.1’s “The rule” sentence originally stated only the third conjunct:

```
confirmed_at ≤ declared_issue_time + δ
```

Under the clock-roles ruling (chain time governs evidence, wall time governs attempt lifecycle), that single conjunct does **not** imply the second conjunct of the temporal predicate:

```
anchor_time ≤ declared_issue_time + δ
```

(Non-monotonic block timestamps make the implication false.) Shipping on the third conjunct alone can therefore produce a receipt that a verifier applying the full A2.2 predicate will reject. The bridge model (`P5cP5P6_Bridge.tla`) already evaluates the full three-conjunct set in its `Ship` action; the prose lagged the model.

### Disposition in A3.7.3
A3.7.3 correctly registers the repair:

- The issuer must evaluate the **full three-conjunct temporal predicate** (the P5 temporal test inside `VALID_STRICT`) before shipping.
- This is exactly what the bridge model already does.
- The repair is authoritative prose; the non-author review of the repair is placed in the A3 panel scope.

This is the right disposition. It does not change any registered property, does not demote anything to an assumption, and does not alter the construction. It simply makes the issuer-side obligation match the verifier-side obligation and the already-checked model.

### Residual checks I performed
- Consistency with A2.2: the three conjuncts are unchanged; only the issuer’s evaluation obligation is made explicit.
- Consistency with A2.1 clock roles: the repair respects the separation (chain observables for the predicate, wall time + slack for the attempt lifecycle).
- Interaction with A2.3 attempt bound / refusal: none. An attempt that fails any of the three conjuncts is still discarded and counted against N; the full-predicate check simply makes the discard decision accurate.
- Interaction with P9 (stateless verification) and the header-evidence obligation: none. The verifier still evaluates the same three observables; the issuer now does the same.
- Model correspondence (A1.4): the bridge already implements the stronger rule; the prose repair closes the last gap between model and registered text.

### Minor clarity suggestion (optional, non-blocking)
The current A3.7.3 wording is accurate but dense. A one-sentence clarifying addition would make the obligation impossible to miss:

> “Consequently, the issuer’s shipping decision is defined as evaluation of the complete three-conjunct temporal predicate of A2.2; evaluation of the third conjunct alone is insufficient and is forbidden.”

That sentence can sit inside A3.7.3 or be folded into the A2.1 prose repair that A3.9 already lists as a tracked obligation. It does not change semantics.

### Conclusion on A3.7.3
The disposition is sound and ready for the cold non-author panel. It should be treated as in-scope validation of a registered repair, not as an open design question. Once the panel has examined it (and the rest of A3), the item can be closed.

No other A3.9 obligation appears to have been left unaddressed in the same way. If you want a second pass on any of the other tracked items (especially the first-link invariant or the standing-evidence testability requirement), say which one.
