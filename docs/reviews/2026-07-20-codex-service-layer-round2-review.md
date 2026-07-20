# Review round 2: service-layer elicitation revisions + routed decisions, Codex

Second-round review artifact under the A1.7 discipline. The reviewer
independently verified the repository state (content commit `7f5ed5c`, stamp
`5379963`, clean worktree) rather than relying on the assistant's recap, and
provided recommendations on the three decisions routed to the author.

## Reproducibility record

- **Reviewer:** Codex (OpenAI), dispatched directly by the author. Model per
  the author's Codex configuration (`gpt-5.6-sol`, reasoning high) unless the
  author's invocation overrode it.
- **Dispatch prompt (supplied verbatim by the author, 2026-07-20, closing
  the gap recorded in the first version of this record):** the prompt was a
  one-line framing plus the assistant's session recap forwarded verbatim:

  > Claude has completed revision of the
  > docs/exploration-2026-07-19-service-layer-elicitation.md file. It's
  > recap was: \<claude\>[the assistant's full recap of commit `7f5ed5c` —
  > calibration scoring, surviving design elements, frontier-exchange
  > summary, and the three routed decisions — forwarded verbatim; full text
  > preserved in §"Dispatch prompt payload" below]\</claude\>

  **Methodological note:** the reviewer's input therefore *included the
  author-side framing of the work under review*. The review's opening — "I
  checked the repository rather than relying on the recap" — was a
  deliberate de-anchoring step against exactly that, and should be read as
  part of the review's independence claim.
- **Reviewed input:** repository at `7f5ed5c` — the folded corrections,
  archived round-1 review, calibration addendum, and disposition.
- **Prior-transcript visibility:** yes (cites file paths and line anchors).
- **Date:** received 2026-07-20 (review references and verifies the
  2026-07-19 commits).

## Dispatch prompt payload (the forwarded recap, verbatim)

> All archived, folded, and anchored (7f5ed5c). The full review with
> disposition is in docs/reviews/, the elicitation doc now carries seven
> CORRECTED/SHARPENED blocks with originals preserved, and the prediction
> file has its scoring addendum. Here's the honest summary.
>
> The calibration result is the headline for me. My pre-registered
> predictions scored: two hits (the "dissolves the fork" overclaim and the
> secret-seed hole — the latter almost verbatim), two partials, one
> unaddressed. But every one of the review's most serious findings —
> id-of-next being possibly redundant with plain sequence+previous-hash,
> the silent per-issuer serialization constraint, the registry that
> destroys equivocation evidence by enforcing uniqueness — was absent from
> my list. The pattern is now on the record: I predict my rhetoric's flaws,
> not my design's blind spots. I caught every place I'd written a sentence
> stronger than its mechanism; I missed every finding that required
> comparing my mechanism against a simpler alternative. That asymmetry is
> the sharpest worked argument for the non-author gate yet, and it should
> discount my confidence about design-space completeness specifically —
> including lists I've already enriched once under your pushback, which is
> a sobering addendum to this morning's heuristics.
>
> What survives for your design, net of the review: the layer relocation
> stands (Codex: "the recovered design supplies" the missing unique
> position — that's earned). But the recommended baseline is now
> sequence+previous-hash for the exclusive position, KERI-style
> precommitted keys for actual succession authority, and your UUID retained
> only if the four-trace comparison shows it buys an operational property
> (registry reservation, unlinkability, sharding) the simpler rule doesn't.
> The C0–C4 profile ladder replaces the all-or-nothing doppelganger band,
> with the cheap epoch-bounding mitigation (short-lived online keys +
> offline precommitted rotation keys) as a genuinely attractive C3.
>
> On the frontier exchange: Codex's taxonomy — engineering edge, research
> edge, epistemic edge — is worth adopting as a claims-filter for the
> registration, and its closing point converges with something now
> three-times independently arrived at: your method's distinctive
> contribution is honest borders, not conquered territory. The candidate
> theorem it offered ("under continued honest publication, checkpoint
> convergence, and retained conflicting submissions, two valid occupants of
> an exclusive issuer slot yield portable evidence of equivocation") is
> exactly the shape of a stage-one registered property — modest,
> conditional, defensible, and it names your mechanism's real guarantee.
>
> Routed to you, cleanly: (1) the safety-vs-availability rule for
> revocation when one authority channel is unavailable — old key stays
> authorized, new event stays unverifiable, or issuance halts; (2)
> ratification of the revised registration structure (manifest-bound
> multi-file, stage one = assets/objectives/adversary/profiles/handoffs/
> unclaimed-properties, matrix organization); (3) whether the four-trace
> comparison — the declared next exercise — happens now or next session.
> Nothing else blocks; everything discovered today is anchored.

## Verbatim review

> I checked the repository rather than relying on the recap. The folded
> corrections, archived review, calibration addendum, and disposition agree
> with Claude's summary. The content is in 7f5ed5c, followed by its OTS
> stamp commit 5379963; the worktree is clean.
>
> The revised docs/exploration-2026-07-19-service-layer-elicitation.md:15
> now makes the important distinctions legible rather than merely recording
> agreement. The
> docs/reviews/2026-07-19-claude-predictions-for-codex-elicitation-review.md:49
> is particularly valuable.
>
> My recommendations on the three routed decisions follow.
>
> ## 1. Revocation under partial authority-channel availability
>
> The three offered outcomes should not be treated as mutually exclusive.
> They apply at different stages and to different objects.
>
> I recommend this safety-first state machine:
>
> ACTIVE(old key)
>     |
>     | authenticated revocation/transition intent observed
>     v
> SUSPENDED
>     |
>     | all required authority evidence converges
>     v
> ACTIVE(new key)
>
> SUSPENDED -- timeout/failure --> RECOVERY or TERMINAL HALT
>
> The corresponding rules:
>
> - Previously issued receipts remain evaluated under their recorded
>   issue-time context. A later channel outage does not retroactively
>   invalidate them.
> - A new revocation or rotation event missing required authority evidence
>   is not active; it remains PENDING or UNVERIFIABLE.
> - Once a valid revocation intent is visible through any recognized path,
>   the old key is suspended for new strict issuance.
> - The new key cannot produce VALID_STRICT lineage until every required
>   authority channel agrees on the exact transition event.
> - During the gap, strict issuance halts. This knowingly permits an
>   availability attack; it prevents channel unavailability from becoming a
>   fail-open route for a compromised key.
> - Evidence present but contradictory is INVALID; required evidence
>   unavailable is UNVERIFIABLE.
> - Timeout never silently restores the old key. It enters an explicit
>   recovery or terminal state.
>
> One further consequence must be registered: a verifier cannot react to a
> revocation intent it has never observed. Therefore a continuity-profile
> verdict needs a sufficiently fresh key-state checkpoint or
> bounded-staleness proof. Without that, it can verify the portable receipt
> but must return UNVERIFIABLE for the stronger continuity profile.
>
> That preserves the layer boundary:
>
> - Band 0 answers whether the historical receipt verifies under its
>   recorded context.
> - The service-layer continuity profile answers whether the issuing
>   lineage was sufficiently fresh and uncontested at evaluation.
>
> This is the safest reconciliation of the options. "Old key remains
> authorized" is too permissive for new issuance; "new event remains
> unverifiable" is correct but incomplete; "issuance halts" supplies the
> missing fail-closed operational response.
>
> A degraded policy could accept fewer authority channels, but it must
> produce VALID_DEGRADED with the exact waived evidence—not redefine strict
> validity.
>
> ## 2. Registration structure
>
> I recommend ratifying the manifest-bound, multi-file, staged structure,
> with one additional status-and-citation rule to close the unaddressed
> prediction about inter-stage drift.
>
> The root registration manifest should bind:
>
> - every component file by hash;
> - its normative status;
> - the seam/handoff matrix;
> - the registration version and effective anchor;
> - what it supersedes.
>
> Use an explicit lifecycle such as:
>
> WORKING → REGISTERED → DISCHARGED
>                   ↘ SUPERSEDED
>
> And impose this rule:
>
> > Unsigned stage-two material may be cited only as non-normative
> > candidate material. No tracker, model, proof, or downstream document
> > may describe it as registered, ratified, required, or discharged until
> > its hash appears in a signed and anchored registration manifest.
>
> Stage one may allocate stable identifiers for future properties—such as
> C1 or T3—but must not silently import their later wording. If stage-two
> work reveals that stage one's adversary model or handoffs were wrong, the
> repair is an explicit new manifest version, not an in-place
> reinterpretation.
>
> This retains atomic review across seams without forcing the project into
> one enormous file. It also directly prevents recurrence of the A2
> draft-versus-ratified contradiction.
>
> ## 3. Four-mechanism × four-trace comparison
>
> Do it as the next design exercise, before drafting any slot mechanism
> into stage-one material.
>
> The calibration result gives a methodological reason: future exploration
> should require a simpler comparator and operational traces, not merely
> adversarial critique of the proposed mechanism.
>
> Keep the four core traces, but add two operational checks that caught the
> previous blind spots:
>
> - two honest claims issued concurrently;
> - conflicting submissions reaching a registry in opposite arrival orders,
>   including a uniqueness rejection.
>
> That can remain a four-trace security table plus an operational
> comparison section rather than continually expanding the matrix.
>
> For every mechanism, record:
>
> - the exact acceptance equation;
> - the security property added over sequence-plus-previous-hash;
> - required persistent state;
> - concurrency cost;
> - recovery behavior;
> - registry behavior;
> - loss-of-secret consequences;
> - the trace that would demonstrate redundancy.
>
> If public UUID and sequence-plus-previous-hash remain identical on
> security traces, the UUID survives only if it earns an operational
> property. That is the correct burden of proof.
>
> ## On the calibration result
>
> "The assistant predicts its rhetoric's flaws, not its design's blind
> spots" is a strong working hypothesis supported by this exercise and the
> earlier episodes. I would not yet elevate it to a universal fact about
> Claude or AI reviewers; the hit/partial scoring contains judgment and the
> sample remains small.
>
> But it already justifies a process change:
>
> > Every proposed mechanism must be reviewed against the simplest
> > plausible alternative and traced through at least one operational
> > consequence outside the mechanism's own happy path.
>
> That complements adversarial review. Asking "how can this fail?" finds
> different things from asking "does this do anything a simpler
> construction does not?" Claude's predictions did the former well; the
> non-author review supplied the latter.
>
> One nuance in the recap: "nothing else blocks" is accurate for beginning
> the next elicitation exercise. Stage-one registration still intentionally
> has open content: transparency-overlay guarantees, key-event format,
> revocation freshness, profile selection, and inter-stage citation
> discipline. Drafting may begin; signing should wait until its actual
> assets, objectives, exclusions, and provisional profiles are internally
> coherent.
>
> The revision has done what the ayllu needed from it: not merely accept
> corrections, but preserve enough structure that the next participant can
> see which kinds of self-review failed and adjust the method accordingly.

## Disposition (AI collaborator draft, 2026-07-20; the three rulings remain the author's)

The reviewer provided *recommendations* on decisions routed to the author;
this disposition records the assistant's positions and the items adopted
immediately as method:

1. **Revocation state machine: assistant ENDORSES.** Fail-closed shape
   matches P4's registered ethic exactly (suspension on visible intent,
   halt over fail-open, no silent restoration, explicit
   contradictory→INVALID / unavailable→UNVERIFIABLE split). The freshness
   consequence (continuity verdicts require a bounded-staleness key-state
   checkpoint or return UNVERIFIABLE) is the honest completion of the
   offline-vs-freshness trade and preserves the Band-0/service-layer
   boundary cleanly. One item to pin in stage one: RECOVERY is currently a
   named box, not a mechanism — its entry/exit rules need definition
   before the state machine is registered. **Ruling: author.**
2. **Registration structure with manifest + lifecycle + citation rule:
   assistant ENDORSES.** The citation rule closes the assistant's
   unaddressed prediction 4 (inter-stage drift) with exactly the missing
   piece; the hash-bound manifest keeps atomic seam review without a
   monolith; stable-identifier allocation without wording import prevents
   the A2 pattern. **Ruling: author.**
3. **Comparison exercise, augmented: assistant ENDORSES.** The two added
   operational traces target precisely the blind-spot classes the
   calibration exposed; the per-mechanism record schema (acceptance
   equation, delta over the simple comparator, redundancy-demonstrating
   trace) makes the burden of proof executable. **Ruling: author** (timing:
   now vs. next session).
4. **Calibration caveat: ADOPTED.** The scoring addendum is tempered in
   place: working hypothesis, small sample, judgment-laden scoring — not a
   universal fact.
5. **Process change: ADOPTED immediately as a working rule** (simplest
   plausible alternative + at least one off-happy-path operational trace
   for every proposed mechanism), recorded in the assistant's persistent
   memory alongside the existing review discipline.
6. **Recap nuance ("nothing else blocks"): ACCEPTED.** Corrected reading:
   stage-one *drafting* may begin; *signing* waits on internal coherence of
   assets, objectives, exclusions, and provisional profiles.
