# Review round 3: the five recorded rulings, Codex

Third-round review under the A1.7 discipline: the author passed the updated
elicitation document (rulings §6) through Codex before allowing the rulings
to feed pre-registration.

## Reproducibility record

- **Reviewer:** Codex, reported by the author as **ChatGPT-4.6 Sol**.
  **Unresolved model-identity note:** the local Codex CLI config default
  observed 2026-07-19 was `gpt-5.6-sol`; the author dispatched directly, so
  the author's report is primary. Both recorded; discrepancy flagged, not
  resolved.
- **Reviewed input:** `docs/exploration-2026-07-19-service-layer-elicitation.md`
  with rulings §6, at content commit `e915a20`.
- **Dispatch prompt (author, verbatim — capture practice now established):**

  > I have worked with Claude to update
  > docs/exploration-2026-07-19-service-layer-elicitation.md with a set of
  > decisions. This is still an exploration note, so I request that you
  > review it - take your time, make sure to surface any issues that you
  > think we need to address. I've done my best to make correct decisions
  > here, but this is a complex field and I am relying upon my companions
  > to assist me in making the decisions. Ultimately, I own these
  > decisions. I know this.

- **Prior-transcript visibility:** yes (cites file line anchors and prior
  amendments).
- **Reviewer-reported repo changes:** none.

## Verbatim review

> The new rulings are coherent with the prior review, but two pressure
> points are already visible: several classifications conflate evidence
> state with authorization policy, and "the manifest wins" may make
> contradictory files formally resolvable while still operationally
> dangerous. I'm tracing those against the existing verifier vocabulary
> and Band 0 obligations before deciding severity. ... One decision needs
> stronger correction than wording: the proposed "by-construction"
> declared-time safeguard cannot make downstream priority ordering
> inexpressible, because the marketplace still possesses the receipt
> containing declared_issue_time. The verifier can refuse to emit a
> priority judgment, but it cannot prevent a caller from deriving one from
> the input. I'm checking the related formal-method claims now, especially
> whether the proposed refusal invariant proves reporting or only records
> a local state. ... The direction is sound, and Ruling 3 is fully earned.
> I would not let Rulings 1, 2, 4, or 5 enter pre-registration unchanged.
> None prevents continued exploration, but several become correctness
> problems if promoted into normative text.
>
> ## Decision disposition
>
> | Ruling | Disposition |
> |---|---|
> | 1 — revocation | Accept direction; revise state and verdict semantics |
> | 2 — registration structure | Accept architecture; repair lifecycle and consistency rules |
> | 3 — comparison exercise | Confirm |
> | 4 — refusal modeling | Accept objective; replace the FLP rationale and distinguish safety from liveness |
> | 5 — A2.4 discharge | Revise substantially; one "by-construction" claim is false |
>
> ## Findings
>
> 1. Continuity evidence, transition state, and verifier verdict are
> conflated.
>
> docs/exploration-2026-07-19-service-layer-elicitation.md:357 speaks of
> publishing VALID_STRICT, VALID_DEGRADED, UNVERIFIABLE, or INVALID as
> signals, followed by relying-party interpretation. But those are
> judgments computed under a policy, not raw evidence. Band 0 already uses
> the same vocabulary for historical receipt validity, creating the
> possibility that a receipt is simultaneously:
>
> - VALID_STRICT under its issue-time context; and
> - UNVERIFIABLE under a C3 continuity profile at the present evaluation.
>
> That is legitimate, but a single unqualified verdict cannot express it.
>
> Stage one should separate:
>
> - immutable evidence observations;
> - protocol transition state: ACTIVE, PENDING, SUSPENDED, RECOVERY,
>   TERMINAL;
> - ReceiptVerdict;
> - ContinuityVerdict(profile_id, evidence_snapshot_hash, evaluated_at).
>
> The existing waiver lattice also limits how far "relying-party risk
> tolerance" can go: an unperformable non-waivable check must remain
> UNVERIFIABLE; only enumerated redundancy requirements may produce
> VALID_DEGRADED. docs/phase-0-prereg-amendment-1.md:304
>
> Three transition details must also be pinned:
>
> - "Planned" versus "reactive" should be derived from trace evidence, not
>   trusted as an issuer-supplied label.
> - If the activation boundary arrives before every planned publication
>   converges, the path must enter SUSPENDED; "planned transitions: no
>   halt" is otherwise a fail-open statement.
> - An "observed revocation intent" must have an exact authentication
>   threshold. If one recognized but compromised path can suspend the key,
>   the resulting availability attack is acceptable only as an explicit
>   safety trade.
>
> RECOVERY may remain undesigned in stage one only if it is registered as
> unclaimed and SUSPENDED → TERMINAL is the complete current behavior. If
> the state machine contains a recovery transition, its authorization and
> entry/exit conditions cannot remain a list of candidates.
>
> 2. The manifest rule currently violates itself and combines orthogonal
> states.
>
> The document calls Ruling 2 "RATIFIED"
> docs/exploration-2026-07-19-service-layer-elicitation.md:390, while its
> banner says it is working material and the ruling itself prohibits
> calling material ratified before it appears appropriately in a signed,
> anchored manifest. It should presently say something like
> "AUTHOR-ADOPTED FOR STAGE-ONE DRAFTING; NOT YET RATIFIED."
>
> The proposed lifecycle also combines three different axes:
>
> - component role: normative, informative, candidate;
> - registration state: working, registered, superseded;
> - property discharge: open, modeled, checked, discharged.
>
> A registered document can contain undischarged obligations, a discharged
> registration can later be superseded, and one file can contain
> properties in different discharge states. Therefore WORKING → REGISTERED
> → DISCHARGED / SUPERSEDED should not be one enum.
>
> "The manifest wins" is appropriate for interpretation, but insufficient
> for validation. If a file banner contradicts the manifest, a conforming
> registration tool should reject the bundle or registration operation.
> Otherwise the redundancy becomes a known inconsistency that downstream
> readers can silently misinterpret. The stronger rule is:
>
> > The manifest is authoritative, and any duplicated status metadata must
> > agree with it; disagreement is a validation failure.
>
> The schema will also need to specify that mere hash inclusion is
> insufficient—the manifest must assign the appropriate role and state—and
> define canonical manifest encoding, detached signing or equivalent
> non-self-referential construction, manifest identity, and authenticated
> supersession.
>
> 3. Declared-time priority cannot be made inexpressible through the
> verifier's output type.
>
> The claim at docs/exploration-2026-07-19-service-layer-elicitation.md:453
> is false as written. Even if the verifier emits no priority-related
> field, the marketplace possesses the input receipt containing
> declared_issue_time and can order receipts itself.
>
> What can honestly be guaranteed is:
>
> - the reference verifier emits no priority judgment;
> - its API provides no endorsed priority interpretation;
> - the marketplace policy forbids declared-time ordering;
> - marketplace conformance tests exercise that prohibition;
> - a downstream implementation that directly inspects receipts can still
>   violate the rule.
>
> A vector can demonstrate representative output, but it cannot prove
> global absence of misuse. Schema/type inspection can establish that the
> verifier exposes no priority result; the row-5 handoff and marketplace
> tests address downstream behavior. The residual possibility of a
> nonconforming consumer must remain explicit.
>
> 4. A refused bit and invariant do not necessarily prove eventual or
> reported refusal.
>
> Ruling 4's objective is correct, but the planned proof needs sharper
> semantics. The current P5c model has neither refusal state nor
> transition, as the earlier review correctly records. Merely adding a
> separately enabled Refuse action does not show that it eventually fires:
> TLA+ requires a liveness property and, commonly, an appropriate fairness
> assumption when an enabled action could otherwise be postponed.
> Lamport's fairness explanation
> (https://lamport.azurewebsites.net/tla/tutorial/session11-2.html)
>
> Two honest constructions are available:
>
> - Make the last failed attempt atomically enter refused; reaching
>   refusal then becomes a transition-level safety fact.
> - Keep a distinct Refuse action, add the required fairness assumption,
>   and check an eventuality such as exhausted ~> refused.
>
> Neither proves that another process receives the report. If "reported
> refusal" is claimed, model an outbox/delivery/acknowledgment handoff or
> narrow the property to "refusal durably recorded and available for
> retrieval."
>
> The FLP rationale should also be removed unless a specific consensus
> problem and system model are mapped. FLP concerns guaranteed consensus
> termination in a fully asynchronous system with a possible crash; an
> explicit bounded refusal does not "avoid FLP"—it relinquishes a
> liveness/availability objective. The original FLP paper
> (https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)
>
> The clean rationale is simply: a bounded, explicit negative result is
> preferable to silent deadlock, while eventual successful issuance
> remains unclaimed.
>
> 5. Anchor standing deserves its own property, not a rider on P2.
>
> P2 is specifically signature-set completeness and anti-stripping.
> docs/phase-0-prereg-amendment-1.md:121 does not own anchor-proof
> coherence. Attaching "accepted ⇒ anchor-binding holds" as a rider risks
> recreating the composition-obligation hiding that this exploration is
> trying to eliminate.
>
> Give anchor standing a stable property identifier of its own, with
> dependencies on P7/P8 and explicit subclaims:
>
> - exactly one designated proof/transaction pair has standing;
> - the proof commits to the exact framed receipt bytes;
> - the txid identifies the transaction containing that commitment;
> - the proof and txid are mutually coherent;
> - discarded or unshipped anchors are ignored;
> - substitution yields either rejection or another valid proof of the
>   same exact bytes.
>
> A ProVerif correspondence can support the symbolic claim, but only for
> the primitives and events modeled; ProVerif establishes relations
> between modeled facts/events rather than concrete Bitcoin or OTS
> implementation correctness. Official ProVerif description
> (https://bblanche.gitlabpages.inria.fr/proverif/usage.html) The direct
> framing proof, symbolic correspondence, implementation vectors, and
> Bitcoin/cryptographic assumptions should therefore remain visibly
> separate evidence.
>
> 6. The standing principle in Ruling 3 moralizes accepted residual risk.
>
> The comparison exercise itself is excellent. But
> docs/exploration-2026-07-19-service-layer-elicitation.md:423 is too
> broad. Engineers routinely identify risks that cannot responsibly be
> eliminated because mitigation creates greater cost, harm, or fragility.
> A later occurrence is not necessarily dishonest if the risk was
> analyzed, disclosed, bounded, and explicitly accepted.
>
> I suggest:
>
> > Allowing a foreseen risk to remain without analysis, disclosure, and
> > an accountable acceptance decision is a breach of the representation
> > made to users. An explicitly accepted residual risk is not an
> > unanticipated failure, but neither is it concealment.
>
> Likewise, the anchored record does not enforce this distinction. It
> preserves evidence that makes the distinction auditable and supports
> accountability. That is still a substantial architectural contribution.
>
> 7. The DSL paragraph conflates ambiguity with independence and
> undecidability.
>
> Euclid's fifth postulate, the axiom of choice, and the continuum
> hypothesis concern independence or alternative axiom systems; the
> halting problem concerns undecidability. None establishes that a
> specification must be ambiguous. A formal system may be perfectly
> unambiguous while incomplete or unable to decide every proposition.
>
> The intended conclusion is good: the DSL should make syntax,
> identifiers, status, and references machine-decidable while forcing
> unresolved semantic choices to be named. I would state that directly and
> remove the mathematical analogy.
>
> ## What has been earned
>
> The planned/reactive distinction, issuer-side prohibition on degraded
> issuance during suspension, manifest-bound multi-file structure,
> inter-stage citation barrier, augmented comparison exercise, and
> commitment to model-to-claim correspondence are all genuine
> improvements.
>
> Most importantly, Ruling 3 responds correctly to the earlier calibration
> failure: no successor mechanism is selected until it is compared with
> the simpler construction and traced through operational consequences.
> That is exactly the discipline the record earned.
>
> I made no repository changes. My recommended gate is: continue stage-one
> skeleton drafting, run the comparison exercise, and repair the findings
> above before any service-layer manifest is signed or described as
> ratified.

## Disposition (AI collaborator draft, 2026-07-20; findings 6–7 routed to the author)

1. **Verdict/state/evidence separation + three transition pins: ACCEPT.**
   The trace-derived planned/reactive determination is the sharpest catch —
   an issuer-supplied label would let a thief mark takeover "planned."
   Planned-boundary-without-convergence → SUSPENDED accepted (the "no
   halt" statement was fail-open as written). Intent-authentication
   threshold and the RECOVERY unclaimed-or-designed dichotomy accepted
   into stage-one requirements. Folded as CORRECTED into ruling 1.
2. **Manifest self-violation + axis separation + validation rule:
   ACCEPT.** The "RATIFIED" label violated the ruling's own citation rule
   — corrected to AUTHOR-ADOPTED FOR STAGE-ONE DRAFTING across all
   rulings. Three orthogonal axes (role / registration state / discharge)
   and disagreement-is-a-validation-failure adopted; schema obligations
   (canonical encoding, detached signing, manifest identity, authenticated
   supersession) recorded for stage one.
3. **By-construction claim false: ACCEPT — the claim was the AI
   collaborator's own "strengthening" in the refined Ruling 5, and it is
   false as written.** Replaced with the honest five-part guarantee stack
   and the explicit nonconforming-consumer residual. Calibration note: this
   recurrence — a rhetorically attractive upgrade introduced during
   refinement and killed on review — is a third worked instance of the
   tempered hypothesis, arising even in a list already enriched under
   pushback.
4. **Refusal semantics: ACCEPT.** Preferred construction: **atomic entry**
   (the last failed attempt enters `refused` in the same transition),
   keeping P5c safety-only — no fairness machinery needed; claim narrowed
   to "refusal durably recorded and available for retrieval" unless/until
   an outbox handoff is modeled. FLP rationale replaced by the clean form
   (bounded explicit negative over silent deadlock; eventual issuance
   unclaimed) — routed to the author for confirmation since the FLP
   framing was his.
5. **Anchor standing as own property: ACCEPT.** Own stable identifier
   (allocated in A3), dependencies on P7/P8, the six subclaims, and
   visibly separate evidence classes (framing proof / symbolic
   correspondence / implementation vectors / external assumptions). The
   P2-rider idea is withdrawn as the seam-burial it was.
6. **Residual-risk sharpening: ROUTED TO AUTHOR** — it rewords his
   recorded principle. The AI collaborator endorses the reword: it
   preserves the intent (unanalyzed foreseen risk = breach) while making
   room for accountably-accepted residuals, and corrects "the architecture
   enforces" to "the record makes auditable."
7. **DSL paragraph: ROUTED TO AUTHOR** — it removes his mathematical
   analogy while keeping his conclusion. The AI collaborator endorses:
   independence and undecidability bound completeness and decidability,
   not ambiguity; the direct statement is stronger.

**Gate adopted:** stage-one skeleton drafting and the comparison exercise
proceed; findings repaired before any service-layer manifest is signed or
described as ratified.
