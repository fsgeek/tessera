# Codex non-author review — P5c refusal state (atomic entry)

**Date:** 2026-07-20. **Reviewer:** Codex (GPT-5.5 ~~— CORRECTED
2026-07-21: the CLI's configured model has been `gpt-5.6-sol` since
2026-07-19 13:06, so this review ran on GPT-5.6; the 5.5 label was the
session assistant carrying a stale handoff note~~), dispatched by the
author. **Scope:** the refusal-state bench work
(`formal/tla/P5c_IssuanceProtocol.tla` and companions, tracker bullet,
READ-AND-CHALLENGE postscript 2). **Verdict:** "accept the atomic-entry
safety construction" — no transition-system defect; three evidence/prose
overclaims. Dispositions below; repairs folded same day by the session's
Claude instance, TLC re-run after folding (all runs green/red as
specified). Calibration companion:
`2026-07-20-claude-predictions-p5c-refusal-bench.md`.

## Review prompt (captured verbatim)

> Non-author falsification review, Tessera P5c refusal state. Files:
> `formal/tla/P5c_IssuanceProtocol.tla` (+.cfg, `_Sanity.cfg`),
> `P5c_IssuanceProtocol_BrokenSilent.tla` (+.cfg, `_Green.cfg`),
> `P5c_IssuanceProtocol_Broken.tla` (parity edit only), tracker bullet in
> `formal/PROPERTIES.md`, context in round-3 review ruling 4. The
> construction claims: atomic entry of `refused` on the final
> window-expiring Tick; safety-only; discharged claim "refusal durably
> recorded and available for retrieval," NOT "reported." Attack, in
> order: (1) boundary correctness of the trigger
> `now + 1 > declared + Delta` against Ship's `now <= declared + Delta` —
> exhibit any tick where both or neither hold; (2) whether
> `NoSilentDeadlock` is equivalent to the atomicity claim at this model's
> granularity, or a weaker shadow — construct the simplest model
> satisfying it without atomic entry if one exists; (3) whether
> shipped/refused mutual exclusion should be a checked invariant instead
> of a comment-corollary; (4) soundness of the red-plus-green-control
> isolation demonstration for `_BrokenSilent`; (5) the off-happy-path
> trace: late anchor → depth k−1 → window expiry → post-refusal burial to
> depth k — anything re-enable Ship?; (6) any surviving prose that
> overclaims "reported" or "termination by construction." Do not repair;
> report findings with traces or line references. Verdict per finding:
> defect / overclaim / sound.

## Findings and dispositions

### 1. Boundary — SOUND, with an explicit race. ACCEPT, comment folded.

Reviewer: since `now` is integral, the refusal trigger `now + 1 > D` is
`now >= D` and Ship's guard is `now <= D`, so **both are enabled at
exactly `now = D`** (never neither) — TLC reached the full overlap
(declared=8, now=11, depth=DepthK, both actions enabled). Sound iff the
deadline governs completion: boundary eligibility does not oblige the
scheduler to Ship. Reviewer asked that the overlap be named as
intentional boundary semantics.

**Disposition:** correct in every particular. The race is real and
intentional — it is the model's honest image of the physical race
between burial and clock at the deadline, both branches are safe, and
the outcomes are mutually exclusive (`RefusedOnlyWhenExhausted`).
Folded: a BOUNDARY RACE comment block at Ship.

### 2. NoSilentDeadlock is a shadow, closed by the suite. ACCURATE, NO CHANGE.

Reviewer: the invariant alone is not equivalent to atomic entry — a
countermodel could stall Tick at the deadline until a separate action
records refusal, or make expiration unreachable (vacuity). In this
suite, `RefusedOnlyWhenExhausted`, the sanity witnesses, and inspection
of Tick close those loopholes; the module's own "state-level shadow"
description is accurate.

**Disposition:** no repair needed — the reviewer confirms the existing
comment says exactly what is true. Recorded here because the
countermodel construction is the sharpest available statement of WHY the
invariant is only a shadow; the semantic atomicity claim rests on the
combined suite plus inspection of Tick, and any future edit to Tick must
re-earn it.

### 3. Mutual exclusion — already checked. NO CHANGE (redundant invariant declined).

Reviewer: `RefusedOnlyWhenExhausted` directly contains
`refused => ~shipped`; Ship's missing `~refused` guard is harmless
(refusal implies the window is expired forever). A separately named
`~(shipped /\ refused)` would be redundant evidence.

**Disposition:** matches the model as written; the review prompt's
question 3 is answered "not a hole." Declined the redundant invariant —
the tracker and this archive are the record that the exclusion is
checked, under its existing name.

### 4. Red/green isolation — SOUND within the checked set. ACCEPT, wording folded.

Reviewer: fresh TLC reproduces all five results, and the parity edit did
not erase `_Broken`'s intended break. "Exactly" must be read as "exactly
among the enumerated invariants and property" — which is what the green
control demonstrates — not absence of every conceivable semantic
difference.

**Disposition:** the scoping is right and the original wording
overreached by omission. Folded: `_BrokenSilent` header and cfg comments
now say "among the checked set."

### 5. Post-refusal burial — coverage OVERCLAIM; mechanism sound. ACCEPT, repaired by extension.

Reviewer: at MaxTime=12 the requested off-happy-path trace is
impossible — refusal lands exactly at the bound, so no post-refusal Tick
can deepen an anchor; the `RefusalWithLiveAnchorUnreachable` witness
establishes anchor-present-at-refusal, not burial-after-refusal, and the
Anchor comment overcredits it. At a temporarily extended horizon (14)
the trace exists and Ship stays disabled — nothing re-enables it.

**Disposition:** the strongest finding — a claimed-but-unexercised path,
exactly the class the calibration file predicts the author misses.
Repaired by extension rather than narration: MaxTime raised 12→14
(= MaxAttempts·(Delta+1) + DepthK) across ALL cfgs, new sanity witness
`RefusalBuriedAnchorUnreachable == ~(refused /\ depth >= DepthK)` added
and confirmed firing, Anchor comment rewritten to claim only what each
witness shows. The reviewer's temporary-horizon experiment is now the
committed configuration.

### 6a. "Available for retrieval" — OVERCLAIM. ACCEPT, claim narrowed.

Reviewer: the model contains a latched Boolean — no retrieval action,
reader, authorization, storage failure, or response path. It proves
logical state persistence, not accessibility. **The reviewer explicitly
withdrew its own round-3 recommended wording as too strong.** Defensible
claim: "the abstract refusal state is entered and latches."

**Disposition:** folded everywhere the wording lived (module header,
RefusalLatched comment, PROPERTIES.md bullet, READ-AND-CHALLENGE
postscript 2). The discharged claim is now: **atomic entry + in-model
latch**; durability-as-storage, retrievability, and reporting are all
implementation/handoff obligations for Amendment 3. Process note for the
record: this is the falsification gate correcting its own prior
output — the round-3 reviewer's recommended phrase, adopted verbatim,
was itself the overclaim. Language that enters through review still
needs review.

### 6b. "Silent stall unrepresentable" / "termination by construction" — OVERCLAIM. ACCEPT, folded + annotated.

Reviewer: without fairness, Tick may be postponed indefinitely (or the
behavior stutters) before the final crossing. Atomic entry proves only:
IF the crossing Tick occurs, the post-state contains the refusal. The
expired-unrefused STATE is unrepresentable; the never-crossing BEHAVIOR
is not excluded. Flagged sites: READ-AND-CHALLENGE postscript 2 and the
round-4 FLP-replacement passage in the 07-19 elicitation doc ("bounded
termination in either success or explicit refusal").

**Disposition:** folded in the postscript (state-level phrasing).
For the elicitation doc: the flagged sentence is round-4 ruling text
confirmed by the author, so it was NOT edited — a dated scope annotation
was added beneath it distinguishing the contract's termination promise
(an implementation obligation) from what the model proves (the safety
half only). **Author veto point:** if the annotation misstates the
contract's intent, strike the annotation, not the ruling text.

*Follow-up 2026-07-21 (Codex, on seeing the disposition):* "I favor
keeping the scope annotation. 'Bounded termination in either success or
explicit refusal' can remain the protocol contract, while the present
model proves only the conditional safety half: when the
expiration-crossing transition occurs, refusal is entered atomically.
Eventual execution remains an implementation obligation. That
distinction is substantive, not hedging." Reviewer endorsement recorded;
the veto remains the author's — the annotation stands by default unless
he strikes it.

## Net

All five TLC runs re-executed after folding at MaxTime=14: main green
(all invariants + latch), sanity all seven witnesses fire, `_Broken` red
on `NoShippedOrphan`, `_BrokenSilent` red on exactly `NoSilentDeadlock`
(checked set), `_Green` control green. The construction stands; the
claims now match it. Nothing here is discharged in the A1.7 sense until
the author rules on the dispositions.
