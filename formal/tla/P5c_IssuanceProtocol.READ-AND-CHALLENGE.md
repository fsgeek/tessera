# P5c — read-and-challenge annotation

**Status: author-side, NON-DISCHARGING. Not a review.**

This file is a *teaching artifact*, not a verification artifact. It was
produced with AI assistance (Claude) against a model that was itself written
with AI assistance. That is precisely the correlated-blind-spot configuration
the project's non-author falsification gate (A1.7) exists to defeat. Nothing
here discharges anything, upgrades any status in `PROPERTIES.md`, or counts as
independent review. If a claim in here and the model ever disagree, that is a
question to *investigate*, not a verdict.

Its only purpose: to demonstrate the *shape* of the questions a skeptic asks
of a formal model, on a model whose system you already understand — so the
read-and-challenge muscle is yours, not borrowed. The questions are the
product. The answers are yours to reach.

A model can only ever be wrong in three places. Every question below is an
instance of one of them:

1. **The abstraction lies** — the model omits or simplifies something whose
   omission is load-bearing for the property.
2. **The property is too weak** — the invariant passes but doesn't actually
   say what the English claim says.
3. **The seam is unguarded** — the model proves its half, another artifact
   proves the other half, and the join between them is asserted, not checked.

Read each question and ask yourself: *which of the three is this, and do I
believe the model's answer?*

---

## A. Does the abstraction lie? (the single-clock collapse)

The module header is admirably explicit that block timestamps equal real time
and blocks arrive one per tick. That honesty is exactly what makes the next
question askable.

**Q1. The consequence you were told, made concrete.** The header says the
single-clock abstraction means "issuance-side anchors never precede
declaration, so the epsilon side does not appear." Walk it yourself: `Anchor`
sets `anchorAt' = now`, and `now` only ever increases from `declared`'s value.
So `anchorAt >= declared` is true *by construction of the clock*, not because
the protocol enforces it. **Ask:** in the real system, is there any path where
a block timestamp is *earlier* than your declared issue time? (Bitcoin block
timestamps are not monotonic and can legitimately move backward by up to ~2
hours under the median-time-past rule.) If yes — is that path supposed to be
caught here, or is it explicitly handed to epsilon on the verifier side? Find
the sentence in A1.6 that catches it. If you can't find it, you've found a
seam (§C), not a bug — but you need to *know* it's handed off, not assume it.

**Q2. One tick, one block, one confirmation.** `Tick` both advances the clock
*and* deepens the anchor by exactly one. So in this model, time and
confirmation-depth are the same quantity. **Ask:** in reality, can time pass
*without* a confirmation arriving (a slow block, a mining lull)? If it can,
then real `now <= declared + Delta` and real `depth >= k` are two independent
race conditions, and this model has fused them into one. Does that fusion
*help* the attacker or the defender? Work out which — a fused model that
happens to be conservative is fine; a fused model that hides an adversarial
interleaving is not. Convince yourself which one this is. (Hint: ask what the
`Ship` guard would have to check if `Tick` could advance `now` while leaving
`depth` unchanged.)

---

## B. Is the property too weak? (what the invariants actually say)

**Q3. `NoShippedOrphan` and the reorg bound.** `Reorg` has the guard
`reorgs < 2` and the header calls this a "reachability witness" bound. But
look at what it does to the *harm* claim: the invariant `NoShippedOrphan` only
gets to fail if a reorg can *reach* a shipped-but-shallow receipt. **Ask:** is
`NoShippedOrphan` holding because the *depth-k rule* genuinely prevents the
harm, or partly because `reorgs < 2` caps the adversary before it can dig
deep? These are different reasons. The broken companion is the control that
answers this — it holds `reorgs < 2` fixed and *only* weakens `Ship` to
`depth >= 1`, and the harm becomes reachable. So the difference *is* isolated
to the ship rule. Good. **But now ask the follow-up:** does `reorgs < 2` bound
the *depth* a reorg can reach, or only the *number* of reorgs? Re-read
`Reorg`: it only fires when `depth < DepthK`. So a reorg can never orphan a
depth-k anchor *by construction of the guard*, not by the number 2. Is that
guard the A1.6 assumption ("depth >= k is permanent") wearing a disguise? If
so, `NoShippedOrphan` is partly *assuming* what it looks like it's proving.
That's not necessarily wrong — the header says depth-k permanence is a
precondition, not a result — but you should be able to say out loud: **"the
model proves the ship rule respects the permanence assumption; it does not
prove the permanence assumption."** Can you?

**Q4. `ShippedIsSound` — is the conjunction complete?** It asserts
`anchorAt >= declared`, `anchorAt <= declared + Delta`, `depth >= DepthK`.
**Ask:** the English claim is "temporally sound and buried." Is "buried within
delta of *the declared time*" the same as "buried within delta of *when a
verifier will later evaluate it*"? The A2 resolution made issuer and verifier
share *one* predicate on chain-time. Does this invariant reference that shared
predicate, or a proxy for it that happens to coincide under the single clock?
(This is the same fusion as Q2, viewed from the invariant instead of the
action. If Q2's fusion is safe, this is too — but check them *separately*,
because a proxy that coincides in the model can diverge in the code.)

**Q5. `ExpiredCannotShip` uses `ENABLED Ship`.** This is a clever, honest way
to state "no expired attempt can ship." **Ask:** `ENABLED Ship` is evaluated
against *this module's* `Ship`. If you later change `Ship` (as the broken
companion does), this invariant's *meaning* changes with it silently. Is that
what you want? (It is defensible — the invariant is "whatever shipping means,
an expired attempt can't do it." But notice you've coupled a safety property
to an action definition. In the broken companion, is `ExpiredCannotShip` even
checked? Look at its cfg. If not — why is it safe to drop, and did you decide
that on purpose?)

---

## C. Is the seam unguarded? (where P5c hands off)

This is the highest-value section for the integrity headline (P1), because
P1's soundness lives in the *joins* between models, not inside any one.

**Q6. The verifier-permanence handoff.** The header's whole reason for
existing: "it discharges the obligation the verifier-side model's scope
boundary names: that the verifier may take `anchor` as an already-permanent
block time." So P5P6 (verifier) *assumes* permanence; P5c (issuer) is supposed
to *earn* it. **Ask the seam question:** does P5c earn *exactly* the thing
P5P6 assumes — same predicate, same depth convention, same delta? The A2.1
convention pin (`DepthK = k - 1`, block-after-inclusion vs Bitcoin's
count-the-including-block) is *precisely* the kind of off-by-one that lives in
a seam. Open `P5P6_TemporalRevocation.tla`, find its `confirmedAt`, and check
by hand that the two modules mean the identical block by "confirmed at depth
k." If they're off by one in *opposite* directions, both models pass and the
composed system is wrong. **This is the check no single model can perform on
itself.** It is the strongest argument for outsourced review (option 3) — not
because the models are hard, but because the *seam* is invisible to each side.

**Q7. Liveness is explicitly not checked.** The header is honest: "eventually
ships" is not verified; termination is "by construction (A2.3)" via
`MaxAttempts`. **Ask:** "by construction" is a proof obligation, not a proof.
Is there anywhere — prose, another model — that actually argues N attempts
terminate in a *reported* refusal rather than a silent stall? The
`PROPERTIES.md` tracker still has "A2.2 conformance-vector cases" unchecked.
Is the refusal-is-reported claim discharged anywhere, or is it currently a
promise? (A silent stall on attempt N is exactly the fail-*open* the whole
project is against. Worth knowing if it's proven or asserted.)

---

## THE HEADLINE WEAKNESS (sharpened from Q6, after reading P5P6)

Not a general "check the seam" — a specific undischarged correspondence.
Still author-side, still non-discharging. Go falsify it; don't trust it.

The two temporal modules agree on the confirmation-time *formula* in prose —
both cite A2.1's `confirmedAt := timestamp(block h+k-1)`. Good: the off-by-one
convention is at least *named* on both sides, not silently divergent. But they
model the underlying quantity **incompatibly**, and nothing checks that the
prose agreement survives the modeling gap:

- **P5c models depth operationally.** `depth` is a state variable; `Tick`
  increments it; `Ship` guards on `depth >= DepthK` with `DepthK = k-1`. The
  `h+k-1` burial is *enacted*.
- **P5P6 does not model depth at all.** There is no `depth` variable. It has
  `confirmedAt \in 0..MaxTime` — a *free integer* — constrained only by
  `confirmedAt <= declared + polDelta`. The `h+k-1` provenance is a comment
  (line 37) and is then discarded; the verifier treats `confirmedAt` as an
  arbitrary number it is handed.

**The unguarded seam:** P5c's *output* is a shipped receipt anchored at a
specific block; P5P6's *input* is a bare `confirmedAt` integer. The join —
"the `confirmedAt` the verifier reads is the timestamp of the very block P5c
shipped on" — is **modeled nowhere.** It lives entirely in the shared comment.
A bug (or adversary) that made P5c ship on the wrong block would emit a
`confirmedAt` P5P6 still accepts, because P5P6 cannot see *which* block it is —
only that the number is `<= declared + polDelta`.

This is the tracker's `Cross-model correspondence mapping` line — except the
correspondence that bites first is **TLA+ ↔ TLA+**, between your own two
temporal modules, and it is *not* itemized on the tracker as distinct from the
TLA+↔symbolic mapping. That is the gap.

**Work-through exercise (this is the training aid):**

1. Take a P5c terminal state: `shipped = TRUE`, with `declared`, `anchorAt`,
   `depth = DepthK`. Ask: what value of `confirmedAt` does P5P6 receive for
   this receipt? P5c never computes a "timestamp of the h+k-1 block" as a
   quantity distinct from `anchorAt` — under its single clock, block-time *is*
   the tick. So the mapping forces the Q2 clock-fusion back into the open,
   now from the seam side.
2. Decide: does P5P6's `confirmedAt` correspond to P5c's `anchorAt`, or to
   `anchorAt + (k-1)`? Under the single clock they may coincide; in reality
   the k-1 burial ticks are real elapsed time. If P5P6 is implicitly treating
   `anchorAt` and `confirmedAt` as the same instant, **the entire h+k-1 burial
   delay has disappeared in the handoff** — the verifier would accept a receipt
   whose k-th confirmation actually landed *outside* the window.

If that last line is true, it is a real hole, found before Band-0 exit — the
method working. If it is false, you will have discharged a correspondence
obligation *by hand* and earned the read. Either way the next move is a signed
amendment (A1.1) — either adding the TLA+↔TLA+ correspondence obligation to the
tracker, or recording that you checked it and it holds. Do not edit the models
in place to "fix" it before deciding which.

I could not settle this myself, and you should not let me — a cross-model
correspondence blessed by the same AI that helped write the models is the
correlated-blind-spot case A1.7 exists for. This is the sharpest argument in
the whole file for outsourced human review (option 3): the seam is invisible
to each model *and* to the assistant that wrote both.

---

## How to use this

Pick **one** question — Q6 is the one I'd start with, it has the most teeth
and it's a hand-check, not a tool run. Answer it *without* trusting me: open
both modules, trace the block index, and decide for yourself whether the seam
holds. If you can do that and defend the answer cold, you have the
read-and-challenge skill for this model. Then the questions I *didn't* think to
ask are the ones that matter next — and those are yours to find.

If any of these turns out to point at a real gap, the fix is a signed amendment
(A1.1), not an edit to the model in place — and the *discovery* is the method
working, not a failure.

---

## Postscript (2026-07-19, appended before archiving)

The HEADLINE section above went through the non-author gate in the
2026-07-18/19 session: Codex checked the alarming form — "the burial delay
disappears in the handoff" — and it does **not** reproduce (384-state check,
invariant holds; the initial framing was wrong and the falsification gate
killed it). What survives is narrower: an undischarged **TLA+↔TLA+
correspondence obligation**, now itemized in `formal/PROPERTIES.md` and
destined for Amendment 3 disposition per the break-the-chain decision. See
`docs/exploration-2026-07-18-causal-dag-commons.md` (§0 finding 1, §8, §8b).

The questions remain a teaching artifact; the headline should no longer be
read as a live alarm. Original text above is unedited, per the
record-preservation rule.

## Postscript 2 (2026-07-20, appended after the refusal-state bench work)

Q7's question — "is the refusal-is-reported claim discharged anywhere, or
is it currently a promise?" — now has a precise partial answer. The model
carries a `refused` state entered by **atomic entry** (the Tick expiring
the final window records it in the same transition; round-3 ruling 4),
with `NoSilentDeadlock`, `RefusedOnlyWhenExhausted`, and the
`RefusalLatched` latch checked, and a `_BrokenSilent` companion
(separately enabled, postponable Refuse) red on exactly the deadlock
invariant among the checked set. What is discharged (wording narrowed
2026-07-20 by the Codex review of this work, which withdrew its own
earlier "durably recorded and available for retrieval" as too strong):
**the abstract refusal state is entered atomically and latches**.
Storage durability, retrievability, and reporting all remain promises —
the record→report gap is an Amendment 3 disposition item (A2.3's draft
text was aligned to this split on 2026-07-21). Q7's "silent stall on attempt N" is now unrepresentable *as a
state*: no reachable state has the final window expired without the
refusal recorded. It is not excluded *as a behavior* — without fairness,
Tick can be postponed indefinitely before the crossing, and a mid-loop
stall (Reissue postponed forever, attempts unexhausted) is likewise
representable; both are the explicitly-unclaimed liveness, named in the
module header. This work has passed one non-author falsification pass
(`docs/reviews/2026-07-20-codex-p5c-refusal-review.md`); discharge
status is the tracker's to say, not this file's.
