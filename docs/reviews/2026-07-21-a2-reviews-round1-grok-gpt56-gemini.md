# A2 pre-signature review — round 1: Grok, GPT-5.6 (Codex CLI), Gemini

**Date:** 2026-07-21. **Dispatched by:** the author, using the preamble
in `2026-07-21-a2-review-preamble.md`. **Reviewers:** Grok ×1 (in place
of a second GPT round, author's choice), GPT-5.6 (`gpt-5.6-sol` via
Codex CLI), Gemini (anti-gravity harness). **Verdicts:** Grok — sign
with repairs; GPT-5.6 — not as written, sign with repairs; Gemini — not
as written, sign with repairs.

**Disposition status:** repairs folded into the A2 draft same day by the
session's Claude instance, all flagged for the author's signature-time
veto; two dispositions explicitly reserved for the author (marked
below). Reviews archived verbatim at the end of this file.

## Disposition matrix

Findings merged across reviewers where they converge. "G" = Grok,
"C" = GPT-5.6 (ChatGPT), "M" = Gemini.

1. **A2.1 issuer-guard completeness (G2; converges with the bridge
   model's design-time finding, preamble Q3a).** ACCEPT — "The rule"
   paragraph now states the issuer evaluates the full `VALID_STRICT`,
   with the bridge citation and the conjunct-3-does-not-imply-conjunct-2
   reason.

2. **A2.1 "identical predicate" false under verifier-owns-tolerances
   (C2; the round's sharpest new finding).** VERIFIED against
   `P5P6_TemporalRevocation.tla:80` ("verifier may choose stricter,
   never larger") — a stricter δ′ rejects honestly-shipped receipts.
   ACCEPT — the no-disagreement guarantee is now scoped to
   "under the issuance policy's δ".

3. **A2.1 "exact correspondence" overclaim (C3) + issuer-evaluates-a-
   stronger-local-condition (M2).** ACCEPT, merged — the paragraph now
   says "same intended statement under the declared abstractions,"
   cites the bridge as the mechanical check (non-author review
   pending), and names P5c's fused-clock guard as a locally stronger
   condition implying the chain predicate. (C3's quote of the tracker
   predates the bridge commit 85d7ed3; the tracker line it cites is
   now discharged-pending-review, which the new text reflects.)

4. **Boundary tie belongs in registered text (G3, C4, M3 —
   three-reviewer consensus, all arguing the same way).** ACCEPT —
   "Boundary tie, registered" sentence added to A2.1: both outcomes
   admissible at equality, no priority guarantee.

5. **A2.0 two temporal senses of "registered properties" (C1).**
   ACCEPT — "none of them" now reads "none of the pre-Amendment-2
   registered set; A2.2 below changes exactly that."

6. **A2.3 unconditional "terminates" vs model note (M1; Grok's
   no-consistency-defect verdict missed this).** ACCEPT — now
   "Exhausting them obligates the implementation to terminate…"
   (contract phrasing, matching the model note's split).

7. **Nine-days bound overclaim (C5).** ACCEPT — now "nominal window
   budget… not a proven wall-clock bound on the process."

8. **"Red on exactly" missing its qualifier (C6).** ACCEPT — "among
   the checked set" restored in the A2.3 model note. Process note:
   this was the session assistant reintroducing, in a document, the
   exact unqualified phrase it had itself qualified in the model files
   the day before. Wording discipline does not transfer automatically
   across artifacts; correspondence review catches what authors of
   both sides miss.

9. **"Registered separately (Amendment 3)" implies A3 is in force
   (C7), plus stale cross-artifact references.** ACCEPT — A2 now says
   "to be registered in Amendment 3" (twice, incl. "planned, not yet
   in force"); synchronized the three active artifacts still citing
   "A2.3's registered word 'reported'": `P5c_IssuanceProtocol.tla`
   header, `PROPERTIES.md` refusal bullet, READ-AND-CHALLENGE
   postscript 2. Historical review archives left unchanged, per the
   record-preservation rule.

10. **txid "retrieval handle" overclaim (C8).** ACCEPT — now "identity
    handle," with availability (node/index/archive) named as an
    implementation obligation joining A2.2's evidence discipline; the
    hash argument scoped to identity, not availability.

11. **"No standing in verification or dispute" over-broad (C9, M4;
    Grok G4 found no defect — outvoted, and C9's argument is
    technically right: a validity rule should not adjudicate
    evidentiary admissibility).** ACCEPT, C9's narrowing — "confers no
    validity, no priority, and no claimed anchor identity," with the
    explicit note that evidentiary use in dispute processes is not
    barred and the clause underdetermines A3's stand-alone property.
    **RESERVED FOR AUTHOR:** this is a protocol-semantics choice about
    what dispute processes may consider; the folded text is the
    recommendation, not a ruling.

12. **Header-provenance residual family (G5 false-acceptance via lying
    store; C11 store authority/P9 underspecification; M5 private
    k-block fork in bundled headers — three angles on one hole).**
    ACCEPT, merged — new "Header provenance" named residual in A2.1
    (candidate-segment-vs-canonicity, private forks, lying stores),
    plus header *authentication* rules named as part of the A2.2
    evidence obligation with full specification deferred to that
    obligation's discharge. C11's full pin (store identity/version in
    declared policy, conflict rules) is quoted in the residual as the
    obligation's content.

13. **confirmed_at is a proxy; backward skew (C10).** ACCEPT — new
    named residual: the observable is the chosen chain-time proxy for
    burial, median-time-past permits a post-deadline block to carry an
    in-window timestamp; wall-clock burial lateness is not what the
    predicate measures.

14. **A2.6 broader than its A1.1 conclusion (C12) + UNVERIFIABLE
    availability cost (M6; Grok G6 found no weakening — right on the
    A1.1 question, but the cost deserved naming).** ACCEPT, merged —
    A2.6 now states the exact A1.1 conclusions (no A1.2 property
    weakened, no proof demoted, no A1.3 capability excluded,
    construction unchanged), acknowledges in ordinary language what
    did change, and names the new UNVERIFIABLE path as an availability
    cost carried by the P4 partition.

15. **double-SHA-256 chain-binding (M7).** DECLINE, recommended — the
    Bitcoin binding is intentional: the anchor chain of record is
    Bitcoin via OTS, and the no-new-assumption argument depends on the
    concrete hash construction; abstracting it would weaken the
    argument, and a future chain migration is an amendment-scale event
    regardless. **RESERVED FOR AUTHOR:** if multi-chain neutrality is
    a design goal, this reverses.

Findings with no repair needed: G1/G6/G7 (clean passes, two overtaken
by other reviewers as noted), C "what has been earned" list, Gemini's
correspondence positives.

## Calibration notes

- Reviewer diversity earned its cost: C2 (polDelta) was found by
  exactly one of three reviewers, as were M1, M5's fork variant, C10.
  The union is much stronger than any single round.
- Grok's round was the most agreeable and found the least; its two
  "no defect" verdicts that other reviewers contradicted (consistency,
  A2.4 pre-emption) were both wrong. Worth remembering when weighing
  its future verdicts.
- Two of the fifteen dispositions repair text the session assistant
  wrote earlier the same day (items 8, 9-in-part). The gate works on
  its own operators.

---

## Verbatim: Grok

[Author-relayed 2026-07-21. Quoted verbatim below.]

> Review of docs/phase-0-prereg-amendment-2.md (A2 draft)
>
> I performed a falsification-style non-author review per the provided
> brief. I read the full A2 draft, the normative context
> (phase-0-prereg.md especially A1.1–A1.2/A1.6/A1.7, and
> phase-0-prereg-amendment-1.md), the discharging artifacts (TLA+
> modules + cfgs/outputs, PROPERTIES.md, and relevant prior review
> artifacts), and cross-checked the model correspondence without
> re-deriving internals.
>
> Findings (in brief attack-surface order)
>
> 1. Internal consistency — No defects. No sentence in A2 contradicts
> another sentence in A2 or the known deltas (1–4). The A2.3 updates
> explicitly incorporate the recorded-vs-reported split, the
> safety-only conditional, the atomic-entry modeling, and the
> implementation obligations for Amendment 3. The added 2026/07/21
> notes align perfectly with the deltas. The "reported refusal"
> phrasing was cleaned up. No finding.
>
> 2. Text↔model correspondence — Minor defect (overclaim in A2.1).
> A2.1's registered predicate (confirmed_at ≤ declared_issue_time + δ
> on the h + k − 1 block) matches P5c's Ship action under the module's
> single-clock abstraction and the DepthK = k − 1 pin (explicitly
> called out and now checked in the bridge). Good. A2.2's third
> conjunct matches P5P6's confirmedAt conjunct. Good. A2.3 accurately
> describes the refusal machinery (atomic entry, latching, safety-only,
> no fairness). Good. Defect: A2.1's "The rule" paragraph and the "Why
> chain time..." paragraph claim the issuer evaluates this predicate
> (the third conjunct alone) before shipping. The bridge model
> (P5cP5P6_Bridge.tla, checked 2026-07-21) and its findings show the
> issuer must evaluate the full VALID_STRICT (all three conjuncts)
> under decoupled clocks, because the third conjunct does not imply the
> second. The prose underclaims the issuer's obligation relative to
> what the model actually checks at Ship. Proposed disposition: Clarify
> in A2.1 that the issuer evaluates the full VALID_STRICT (or
> explicitly that conjunct 3 is evaluated in the context of the other
> two). This is a precision issue, not a substantive weakening.
>
> 3. Boundary question (open, wants a ruling) — Open-question. The tie
> at confirmed_at = declared_issue_time + δ (both outcomes admissible
> per the model note in P5c at Ship) is documented in the module but
> not acknowledged in registered A2.1 text. I argue the registered text
> should acknowledge it. Protocol text that is silent on a documented
> race leaves verifiers and downstream users to discover it in the
> model (or worse, in production). Explicitly stating "at exact
> equality both Ship and refusal are admissible; the model chooses
> non-deterministically" costs almost nothing, strengthens the "no
> honestly-shipped receipt can fail the verifier" claim (it remains
> true), and honors the project's falsification ethos. Model-level
> documentation alone is insufficient for a property this central to
> the strict rule. Proposed disposition: Add one sentence to A2.1
> acknowledging the tie.
>
> 4. A2.4 vs. Amendment 3 — Cleanly underdetermines (no defect).
> A2.4's "no standing" rule for unshipped anchors and the
> txid-as-retrieval-handle is compatible with a future standalone
> anchor-standing property. It does not pre-empt or conflict; A3 can
> refine the exact mechanics of standing, durability of the refusal
> record, and dispute resolution without contradicting A2.4's core
> commitment. No wording forces A3 into contradiction. No finding.
>
> 5. Named residuals completeness — Additional residual identified.
> A2.1 names adversarial timestamping and non-monotonic timestamps. An
> additional residual exists at the interaction of the new conjunct
> with the ε side and header-store trust (A2.2's evidence obligation):
> If headers for h … h+k−1 are supplied from a partially-trusted header
> store (the A1.5 pattern) and that store lies about confirmed_at
> (pushing it earlier into the window), a verifier could accept an
> abandoned-anchor artifact as VALID_STRICT even though the issuer's
> honest chain view would have rejected it. This is distinct from the
> named griefing (which only forces re-issue); it creates a
> false-positive acceptance under partial trust. The current A2.2
> waiver status and P4 partition handle unperformable cases but do not
> name this forgery vector on the new observable. (The bridge model
> scopes this out via abstractions, but it is a real residual once
> header stores are real.) Proposed disposition: Add this as a third
> named residual under A2.1 (or A2.2), with the usual "bounded by trust
> configuration" mitigation. This strengthens rather than weakens the
> amendment.
>
> 6. Hidden weakening — None found. I could not construct a plausible
> reading under which any A2 change weakens a registered A1.2 property,
> demotes a proof to assumption, excludes an adversary, or changes the
> construction. The abandoned-anchor clarification narrows a prior
> overclaim (A2.0 explicitly says the artifact violated none of the
> original properties). Strengthening P5 with a third conjunct, adding
> explicit obligations, and registering the refusal state all tighten
> or make explicit without retreat. A2.6's claim holds. No finding.
>
> 7. Parameter sanity — No defect. All references treat N, k, δ, ε as
> ratified symbols (with working defaults stated). No text quietly
> depends on a numeric literal instead of the symbol. The δ = 72h
> sizing rationale is carried forward correctly. No finding.
>
> Overall Verdict: I would sign with the listed repairs (the three
> items above: issuer full-predicate clarification, explicit
> boundary-tie acknowledgment, and the additional header-store
> residual). These are all precision/residual-naming issues of the type
> this project's review discipline is designed to catch. None
> invalidate the ratification of the strict rule, the refusal
> machinery, or the anchor/declared-time commitments. With these
> addressed, A2 would be a clean, strengthened registration that honors
> the known deltas, maintains model correspondence, and leaves no
> hidden weakening. The draft is already high-quality and reflects the
> iterative, falsification-oriented process well. Happy to discuss any
> finding or re-review a revised draft.

## Verbatim: GPT-5.6 (Codex CLI)

[Author-relayed 2026-07-21. Quoted verbatim below.]

> ## Signing verdict
>
> I would not sign A2 as written. I would sign with the listed repairs.
> The underlying construction survives; the blockers are
> correspondence, scope, and registration-language defects rather than
> a collapse of the design.
>
> ## Findings
>
> 1. Defect — A2.0 uses two temporal meanings of "registered
> properties." A2.0 says the abandoned-anchor artifact "violates none"
> of the registered properties at docs/phase-0-prereg-amendment-2.md:41,
> while A2.2 says it is "rejected outright" at
> docs/phase-0-prereg-amendment-2.md:119. The intended distinction is
> recoverable: it violated none of the pre-A2 properties; A2.2 changes
> that. Disposition: qualify the first statement explicitly as
> referring to the pre-Amendment-2 property set.
>
> 2. Defect — issuer and verifier do not necessarily evaluate an
> identical predicate. A2.1 says the verifier evaluates the "identical
> predicate" and that no honestly shipped receipt can fail it
> (docs/phase-0-prereg-amendment-2.md:72). But P5c uses one fixed
> issuer Delta (formal/tla/P5c_IssuanceProtocol.tla:190), while P5P6
> deliberately permits a verifier to choose any stricter polDelta
> (formal/tla/P5P6_TemporalRevocation.tla:80). Concrete counterexample:
> declared = 0, anchor = 1, confirmedAt = 3, issuer Delta = 3 → Ship
> permitted; verifier polDelta = 2 → confirmedAt <= 2 is false. The
> receipt is honestly shipped under the issuer's rule and rejected by a
> conforming stricter verifier. The formula schema and observable are
> shared; the instantiated predicate is not necessarily identical.
> Disposition: distinguish issuerDelta from verifierDelta. Limit the
> no-disagreement guarantee to verification under the issuance
> policy—or state explicitly that stricter verifier policies may reject
> honestly shipped receipts.
>
> 3. Overclaim — "exact correspondence" remains known to be unproved.
> A2.1 says P5c and P5P6 become "the same statement about the same
> observable—the exact correspondence A1.4 demands" at
> docs/phase-0-prereg-amendment-2.md:84. The ledger correctly says
> otherwise: P5c models operational depth and a single clock; P5P6
> receives a free confirmedAt integer, and the join remains asserted
> pending a bridge model (formal/PROPERTIES.md:40). This is the
> unresolved prior-review finding, not a rediscovery. Disposition: say
> "the same intended predicate under the declared abstraction."
> Identify the bridge as the evidence needed for exact model
> correspondence.
>
> 4. Open question — the boundary tie belongs in normative A2 text.
> Ruling: yes. At equality, a fully buried anchor may ship, or the next
> Tick may refuse. That affects externally visible conforming behavior,
> not merely model exposition. Without an A2 statement, one
> implementation may guarantee shipping when qualified by the boundary
> while another refuses, and both can plausibly claim conformance.
> Disposition: register that equality makes both outcomes admissible,
> with no priority guarantee. This preserves the safety-only
> construction and prevents later implementations from inventing
> incompatible semantics.
>
> 5. Overclaim — N × δ = nine days does not presently establish a
> wall-clock bound. A2.3 says that with N = 3 and δ = 72h, the issuance
> process is bounded at nine days
> (docs/phase-0-prereg-amendment-2.md:144). But: δ is now a
> block-header-time predicate, not elapsed wall-clock time; reissue and
> the final crossing may be postponed; no scheduling overhead or
> independent refusal deadline is specified. The model note correctly
> calls termination an implementation obligation, but that does not
> itself define the clock or deadline by which the implementation must
> act. Disposition: either call 216 hours the nominal window budget,
> not a proven process bound, or register an independent wall-clock
> termination requirement and its permitted overhead/skew.
>
> 6. Overclaim — BrokenSilent is not red "exactly" without
> qualification. A2.3 says the companion is red on "exactly the
> silent-deadlock invariant" at docs/phase-0-prereg-amendment-2.md:157.
> The prior review narrowed this to "exactly among the checked set."
> Disposition: carry that qualification into A2.
>
> 7. Defect — Amendment 3 is described as already registering
> obligations that it has not yet registered. A2 says reporting is
> "registered separately (Amendment 3)" at
> docs/phase-0-prereg-amendment-2.md:145, and similarly treats storage
> durability, retrievability, and reporting as registered there at
> docs/phase-0-prereg-amendment-2.md:164. A3 is planned, not signed and
> in force. Related artifacts also remain stale: the P5c header and
> ledger still refer to A2.3's registered word "reported," although the
> draft no longer contains that requirement. Disposition: use "reserved
> for" or "shall be registered in Amendment 3," and make that future
> registration an explicit prerequisite. Synchronize active
> model/tracker commentary before signing; historical review quotations
> can remain unchanged.
>
> 8. Overclaim — a txid is an identifier, not by itself a retrieval
> mechanism. A2.4 calls the txid a "retrieval handle back to the chain"
> and says this requires no new assumption
> (docs/phase-0-prereg-amendment-2.md:173). Hash resistance supports
> transaction identity and substitution detection. It does not provide
> txid → transaction availability, an archive, an index, or
> canonical-chain selection. The official OpenTimestamps client itself
> says verification requires access to a Bitcoin Core node, even for a
> completed timestamp. OpenTimestamps client documentation
> (https://github.com/opentimestamps/opentimestamps-client)
> Disposition: call the txid an identity/coherence handle. If retrieval
> is required, register the archival/index availability and
> P9-compatible source as assumptions or implementation obligations.
>
> 9. Defect — "no standing in … dispute" pre-empts A3 too broadly.
> A2.4 says an unshipped anchor has "no standing in verification or
> dispute" at docs/phase-0-prereg-amendment-2.md:177. It should confer
> no validity, priority, or ownership standing. But an unshipped or
> discarded anchor may still be relevant evidence of issuer conduct,
> equivocation, retry history, or policy violation. A3's planned
> "discarded/unshipped anchors are ignored" naturally concerns the
> validity computation; it should not be forced to declare such
> evidence inadmissible in every dispute. Disposition: narrow the
> prohibition to receipt validity, priority, and claimed anchor
> identity. Preserve possible evidentiary use without conferring
> protocol standing.
>
> 10. Overclaim/residual — chain timestamp is not the actual instant
> depth k was reached. The provenance describes the strict reading as
> depth k being reached by the deadline
> (docs/phase-0-prereg-amendment-2.md:17), but the registered
> observable is the k-th block's header timestamp. Bitcoin requires a
> header timestamp to exceed the median of the previous eleven blocks
> and rejects timestamps too far in the future; it does not require
> each timestamp to exceed its immediate predecessor. Bitcoin
> block-header reference
> (https://developer.bitcoin.org/reference/block_chain.html?highlight=bits)
> Therefore a block mined after a real-time deadline can carry a
> timestamp at or before that deadline, including a timestamp earlier
> than the anchor block as A2 already acknowledges. The conjunct can
> pass even though burial occurred late in wall-clock time.
> Disposition: name backward timestamp skew as a residual, not merely
> non-monotonicity. Describe confirmed_at as the chosen chain-time
> proxy rather than a literal measurement of when burial occurred.
>
> 11. Open question — header-store authority and P9 reproducibility
> remain underspecified. A2.2 permits headers from either the bundle or
> a verifier-distributed store
> (docs/phase-0-prereg-amendment-2.md:123). It does not yet specify:
> canonical-chain and cumulative-work validation; stale-fork treatment;
> bundle/store disagreement; store identity, version, or checkpoint;
> whether store contents form part of declared verifier policy. Without
> that pin, the verdict is a function of bundle + policy + implicit
> store state, rather than P9's bundle-and-declared-policy function.
> Disposition: register the header-store provenance and conflict rules,
> or require its identity/hash/version inside the verifier policy. The
> existing bridge-model obligation is the natural handoff.
>
> 12. Overclaim — A2.6's wording is broader than the A1.1 conclusion
> it needs. A2.6 says "no capability excluded, no construction changed"
> at docs/phase-0-prereg-amendment-2.md:225. Yet A2 intentionally:
> excludes verifier acceptance previously admitted by the permissive
> reading; adds refusal and an attempt bound; requires exactly one
> designated anchor; prohibits declared-time priority policy. Those are
> construction and capability changes in ordinary language. I did not
> find an A1.1 falsifier: no A1.2 property is weakened, no property is
> demoted to an assumption, no declared A1.3 adversary capability is
> excluded, and the design remains dual-signature plus temporal anchor.
> Disposition: state those exact A1.1 conclusions. Do not claim that
> nothing changed.
>
> ## What has been earned
>
> The DepthK = k − 1 convention matches the issuer model. A2.2's third
> conjunct matches P5P6's arithmetic. The revised A2.3
> proof-versus-contract split is honest, and no active A2 sentence
> claims that the model proves reporting or liveness. The depth-k reorg
> boundary remains an explicit inherited Layer 2 assumption rather than
> a hidden theorem. The amendment is therefore repairable without
> changing its central decisions. No repository files were changed
> during this review.

## Verbatim: Gemini (anti-gravity harness)

[Author-relayed 2026-07-21. Quoted verbatim below.]

> ### 1. Internal consistency
> Defect. Quote: "Amended: issuance makes at most N attempts.
> Exhausting them terminates issuance in an explicit refusal, durably
> recorded..." (A2.3). Reason: The main text asserts unconditional
> termination ("Exhausting them terminates issuance..."). This
> contradicts the known deltas and the explicit caveat in the A2.3
> Model Note, which states that termination is only a "conditional
> safety half" and that "termination is a contract obligation on the
> implementation, not a proven liveness property." Disposition: Remove
> the unconditional termination phrasing. Reword to reflect the
> contract obligation, e.g., "Exhausting them requires the
> implementation to terminate issuance..." or "Exhausting them must
> terminate issuance..."
>
> ### 2. Text↔model correspondence
> Defect. Quote: "The issuer evaluates this predicate before shipping;
> the verifier evaluates the identical predicate on the identical
> observable at verification (A2.2)." (A2.1). Reason: The registered
> predicate is confirmed_at ≤ declared_issue_time + δ (where
> confirmed_at is the time of block h + k - 1). However, the P5c
> model's Ship action evaluates now <= declared + Delta, where now is
> the time of the shipping action. If the issuer dawdles and ships late
> (when depth > DepthK), now will be strictly greater than
> confirmed_at. Therefore, the issuer evaluates a local, strictly
> stronger predicate than the verifier's chain-visible observable, not
> the "identical" one. Disposition: Correct the text to acknowledge
> that the issuer evaluates a local, strictly stronger condition (now ≤
> declared + δ) which guarantees the verifier's chain-visible check
> (confirmed_at ≤ declared + δ) by construction.
>
> ### 3. Boundary question
> Open-question. Quote: "If it fails at issuance time, the attempt is
> discarded and re-issued..." (A2.1). Reason: At exactly now = declared
> + δ when the k-th confirmation arrives, the P5c model permits an
> intentional race: both Ship (shipping the receipt) and Tick
> (advancing time to fail the window) are valid, mutually exclusive
> transitions. The registered text is silent on this boundary tie.
> Argument: The text should explicitly acknowledge the boundary tie. In
> distributed protocols, failing to document intentional boundary races
> often leads to divergent, incompatible implementations. Stating
> explicitly that "at exactly confirmed_at = declared + δ, both
> shipping and refusal are admissible protocol outcomes" gives
> implementers freedom and prevents spurious verification failures or
> consensus bugs at the boundary. Disposition: Add a sentence to A2.1
> acknowledging the boundary tie and explicitly permitting either
> outcome at exact equality.
>
> ### 4. A2.4 vs. Amendment 3
> Overclaim. Quote: "...an anchor not shipped inside a receipt has no
> standing in verification or dispute..." (A2.4). Reason: Per the known
> deltas, "Anchor standing" will become its own property with a stable
> identifier in Amendment 3. By declaring the definitive rule ("has no
> standing") in A2.4, this text pre-empts Amendment 3, forcing A3 to
> either blindly duplicate this wording or contradict it when
> formalizing the standalone property. Disposition: Soften the language
> to cleanly underdetermine the property (e.g., "Anchor standing is
> deferred to a dedicated property in Amendment 3, but
> operationally..."), or strike the normative "no standing" clause
> entirely until A3 is drafted.
>
> ### 5. Named residuals completeness
> Defect. Quote: "The verifier must evaluate confirmed_at statelessly
> (P9): block headers h … h + k − 1 are available either archived in
> the bundle or from the verifier-distributed header store..." (A2.2).
> Reason: This leaves a missing residual: Isolated valid PoW forks
> presented as evidence. If a verifier evaluates the conjunct
> statelessly using headers archived solely in the bundle, a malicious
> issuer could mine a private k-block fork containing the anchor. The
> stateless verifier would accept the receipt because confirmed_at ≤
> declared + δ holds on that isolated fork. The rule leaves open a
> false-verdict residual where the verifier trusts bundled headers
> without authenticating them against a canonical chain tip.
> Disposition: Add "Isolated PoW forks" to the "Named residuals" list
> in A2.1, or clarify in A2.2 that bundled headers must still be
> authenticated against the canonical chain view.
>
> ### 6. Hidden weakening
> Defect. Quote: "Nothing is weakened; the A1.1 falsifier is not
> triggered." (A2.0 / A2.6). Reason: A2.2 introduces a new evidence
> obligation (requiring k headers to evaluate statelessly).
> Consequently, an honest receipt that is missing headers in its bundle
> (when the external header store is down) now degrades from VALID to
> UNVERIFIABLE. Adding strict evidence obligations inherently weakens
> the liveness/availability of verification (P1). Disposition:
> Acknowledge in A2.6 that while safety properties (P5) are
> strengthened, the liveness of verification (P1) is technically
> weakened by the new evidence obligations causing a new UNVERIFIABLE
> path.
>
> ### 7. Parameter sanity
> Defect. Quote: "...a txid is the double-SHA-256 of the
> transaction..." (A2.4). Reason: This phrase quietly binds the
> overarching protocol definition to Bitcoin's specific hashing
> algorithm. If the target chain changes or upgrades its transaction
> hashing standard in the future, this text breaks. Disposition:
> Replace "double-SHA-256" with a chain-agnostic term like
> "chain-native transaction hash" or "cryptographic hash".
>
> Final Verdict: I would not sign as written, but I would sign with the
> listed repairs.
