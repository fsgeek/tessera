# Review round 4: reword resolutions + DSL boundary, Codex

Fourth-round pass: the author sent the round-3 resolutions (including his
rejection of finding 7's removal and his DFA/Turing-complete DSL proposal)
back through Codex.

## Reproducibility record

- **Reviewer:** Codex, per the author's dispatch (model as round 3;
  identity note there applies).
- **Reviewed input:** `docs/exploration-2026-07-19-service-layer-elicitation.md`
  at content commit `22737d6`.
- **Dispatch prompt (author, verbatim):**

  > Claude revised, I accepted one; I agreed to language change to one
  > where I used FLP as an _example_ of a system that is technically
  > "live" but practially speaking useless. I'm not wedded to FLP, I was
  > just trying to use it as an illustrative example. I rejected one. The
  > CH hypothesis is neither provable nor disprovable in ZFC and that is
  > to my mind "ambiguous". The _statement_ of CH is not ambiguous, but
  > that's just evidence a non-ambiguous statment can still not be
  > answerable given a specific model. I don't think we can eliminate
  > those ambiguities in Turing complete DSLs but we might be able to
  > contstruct a DFA DSL that doesn't admit ambiguity. For the former, we
  > just accept there are always going to be unanswerables and leave it to
  > future ayllu members to pick a fork when necessary. For the latter,
  > the question will be if it restricts the expressability more than is
  > acceptable for the project. The document has been updated again.

## Verbatim review

> Your rejection is justified, provided "ambiguity" is explicitly used as
> an umbrella term. The revised three-way distinction is much better:
>
> - interpretive ambiguity: the statement has multiple readings;
> - axiomatic underdetermination: the statement is precise, but the
>   governing theory does not decide it;
> - algorithmic undecidability: no general decision procedure exists.
>
> CH belongs in the second category. I would prefer the technical label
> "axiomatic underdetermination" while acknowledging it as a kind of
> ambiguity in Tessera's broader vocabulary.
>
> Your DFA/Turing-complete distinction is also sound. A deliberately
> finite-state DSL can make syntax, status transitions, reachability,
> equivalence, and completeness of transition coverage decidable—assuming
> finite domains, total transitions, and mutually exclusive guards. A
> Turing-complete DSL cannot offer comparable general guarantees. But the
> DFA cannot establish that the ayllu selected the right states,
> transitions, or relationship to reality. It eliminates machine-level
> uncertainty within the encoded system, not stakeholder incompleteness
> or mistaken modeling.
>
> That suggests a useful architectural boundary:
>
> > Keep the normative manifest/status core finite-state and deliberately
> > non-Turing-complete. Permit richer specifications outside that core,
> > but require their undecidable or unresolved obligations to be named
> > and handed to future review.
>
> The expressiveness tradeoff then becomes explicit rather than
> accidental.
>
> A few issues remain in the updated text.
>
> 1. The FLP analogy still needs one technical adjustment.
>
> The gloss says FLP's adversary wins by "forever deferring the deciding
> message" docs/exploration-2026-07-19-service-layer-elicitation.md:561.
> More exactly, the adversarial scheduler chooses an admissible ordering
> of events that keeps the system bivalent and indefinitely postpones a
> decision; it need not withhold one fixed "deciding message."
>
> Also, such an execution is not technically live with respect to
> consensus termination. Processes continue taking steps, but the useful
> liveness property fails. Your practical point survives:
>
> > FLP provides the analogy: a system may remain operationally active
> > while an admissible schedule indefinitely postpones the useful
> > outcome. MaxAttempts does not solve or avoid FLP; it changes
> > Tessera's contract from guaranteed successful issuance to bounded
> > termination in either success or explicit refusal.
>
> That states precisely what you meant.
>
> 2. The CH paragraph needs a relative-consistency qualification.
>
> The statement that models of ZFC exist in which CH holds and others in
> which it fails should say assuming ZFC is consistent, or use the
> standard formulation that CH and ¬CH are each consistent relative to
> ZFC's consistency.
> docs/exploration-2026-07-19-service-layer-elicitation.md:468 otherwise
> asserts model existence unconditionally.
>
> For consistency within the paragraph, I would also change ZF+CH and
> ZF+¬CH to ZFC+CH and ZFC+¬CH.
>
> 3. The status banner still contains two stale statements.
>
> docs/exploration-2026-07-19-service-layer-elicitation.md:357 say
> ratification occurs when a hash appears in the manifest, but the
> accepted correction properly says hash inclusion alone is insufficient:
> the manifest must assign the appropriate role and registration state.
>
> The same banner says findings 6–7 remain pending author confirmation,
> although both have now been resolved. Those should be updated.
>
> 4. The closing status is also stale.
>
> docs/exploration-2026-07-19-service-layer-elicitation.md:607 say the
> author "will pass" the rulings through Codex. That review has now
> happened. It should record this pass and whichever gate follows it.
>
> The substantive revisions are otherwise good. In particular, the
> document now preserves your mathematical intuition without conflating
> precise-but-independent propositions with vague statements. That is a
> genuine synthesis rather than either side merely yielding.
>
> The enduring limitation is now stated in the right place: a finite DSL
> may decide every question expressible within its bounded formal world,
> while the ayllu must still decide whether that world is adequate—and
> must preserve unresolved forks when it cannot.

## Disposition (AI collaborator, 2026-07-20 — all items accepted, none routed)

1. **FLP precision: ACCEPT** — Codex's replacement paragraph adopted
   verbatim; it states exactly what the author meant (bivalence-preserving
   admissible schedules; operationally active while the useful liveness
   property fails; MaxAttempts changes the contract, not the theorem).
2. **CH relative-consistency: ACCEPT** — "assuming ZFC is consistent"
   added; ZF+CH/ZF+¬CH corrected to ZFC+CH/ZFC+¬CH.
3. **Stale banner statements: ACCEPT** — ratification wording upgraded to
   role+state assignment (hash inclusion insufficient); findings 6–7
   marked resolved.
4. **Stale closing status: ACCEPT** — updated to record rounds 3–4
   complete and the standing gate.
5. **Terminology: ACCEPT** — "axiomatic underdetermination" adopted as
   the technical label, with "ambiguity" explicitly an umbrella term in
   Tessera's vocabulary (preserving the author's usage).
6. **Architectural boundary: ADOPT into the DSL note** — finite-state,
   deliberately non-Turing-complete normative manifest/status core
   (decidability conditional on finite domains, total transitions,
   mutually exclusive guards); richer specifications live outside the
   core and must name their undecidable or unresolved obligations for
   future review. Credit: the DFA/Turing split originated in the author's
   dispatch prompt; the reviewer supplied the validity conditions and the
   limitation (machine-level certainty within the encoded world only —
   the ayllu still decides whether the world is adequate).
