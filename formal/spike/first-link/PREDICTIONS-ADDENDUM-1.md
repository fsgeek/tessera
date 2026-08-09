# First-link spike — predictions addendum 1: single-evidence coverage

Status: APPROVE by author 2026-08-09 (drafted 2026-08-09 from the Codex
independent-review finding recorded in RESULTS.md ledger entry 4.
Same discipline as PREDICTIONS.md: this addendum is committed BEFORE
any of its runs; the author's signing commit freezes it and opens
them).

## Why this addendum exists

The strict-mode Q1–Q4 evidence covers acceptance consuming BOTH
channels' evidence. A3.2's floor permits `VALID_DEGRADED` with
fewer-but-never-zero external evidences, so single-evidence
acceptance is a live verdict path. The pair-judge result does NOT
imply single-evidence safety (Codex counterexample, RESULTS.md
ledger 4: asymmetric bindings defeat the implication). The
first-link boundary invariant must hold for whatever evidence set
actually supports the verdict.

Map v1 is unchanged and remains frozen. The transcription-binding
mechanism under test is unchanged. The judge in these models holds
ONE individual evidence object fixed while the tuple varies; it does
not depend on constructing a second channel's evidence.

## Degraded-mode semantics mapping (registered up front)

In single-evidence mode the accepted channel is the entire surviving
chain's first link. Two distinct guarantees separate:

- **Boundary invariant (two-worlds, per object):** must hold even if
  the accepted channel is compromised — a single object binds one
  digest, hence one tuple. This is what the mechanism owes
  unconditionally.
- **Chain correspondence (provenance):** in single-evidence mode the
  "at least one uncompromised channel" disjunction from the strict
  result collapses to "the accepted channel, if uncompromised,
  published this tuple." When the sole accepted channel IS the
  compromised one, no provenance guarantee survives — that is the
  formal price of the waiver, which the A1.2.1 lattice requires to
  be recorded, and the relying-party story must state. A red result
  on that query is the EXPECTED, registered outcome documenting the
  cost, not a defect.

## Queries, timeboxes, predictions

Q5/Q6 and their repository mirrors: transcription binding intact on
both channels' evidence formats (strong: `sign((STMT, h(t)),
ch_key)`); verifier accepts on ONE channel's evidence (per file);
the other channel's publisher still runs (its evidence exists in the
world, unused by this verifier). The broken companions Q7/Q8 are the
registered exception: each deliberately weakens exactly one
channel's binding, stated per-query below. Variants per query:
accepted-channel-honest vs accepted-channel-compromised (the
A1.3-relevant axis in single-evidence mode; the unused channel's
compromise state is immaterial and fixed honest).

**Q5 — single-evidence chain correspondence, DNS-only acceptance.**
- Q5a (DNS honest): expected holds. (p ≈ 0.7; p ≈ 0.2 violation,
  trace inspection required; p ≈ 0.1 timeout.) Timebox 15 min.
- Q5b (DNS compromised): **expected violation** — the registered
  waiver cost above. (p ≈ 0.8 violation as predicted; p ≈ 0.15
  holds, which would mean the model failed to express the degraded
  mode and needs a recut; p ≈ 0.05 timeout.) Timebox 15 min.

**Q6 — single-evidence two-worlds, DNS-only acceptance, mechanism
intact.** Judge: same single DNS object, two tuples.
- Q6a (DNS honest) and Q6b (DNS compromised): both expected
  UNREACHABLE — the digest pins the tuple per object even when the
  object is forged. (p ≈ 0.75 each; p ≈ 0.15 a real single-evidence
  attack — mechanism revision; p ≈ 0.1 timeout.) Timebox 15 min
  each.

**Q7 — ASYMMETRIC broken companion: DNS weak (issuer identity only),
repository strong (h(t)).** The companion that mechanizes the Codex
counterexample — including the pair-judge blind spot, by machine
rather than by comment. The model carries BOTH acceptance modes and
BOTH judges: a degraded verifier accepting DNS evidence alone,
feeding a single-object judge (same weak DNS object, two tuples);
and a strict verifier accepting the full pair, feeding the pair
judge from the base registration.
- Expected CONTRAST, both registered: single-object two-worlds
  REACHABLE (p ≈ 0.8; p ≈ 0.15 recut; p ≈ 0.05 timeout) AND
  pair two-worlds UNREACHABLE (p ≈ 0.75 — the strong repository
  object shared by any two same-pair acceptances pins the digest,
  hence the tuple; p ≈ 0.15 REACHABLE, which would mean the
  counterexample structure is wrong and disposition requires trace
  inspection; p ≈ 0.1 timeout). The contrast pair, observed
  together, mechanically exhibits the counterexample to the
  retracted implication: single-object vulnerability without pair
  vulnerability. Timebox 15 min.

**Q8 — mirror of Q7: repository weak, DNS strong** (degraded
verifier accepts repository evidence alone; strict verifier and
pair judge identical in structure). Same registered contrast,
predictions, and timebox as Q7. (Channel asymmetry rule from the
base registration: no generic-channel abstraction.)

Repository-side mirrors of Q5/Q6 (Q5r, Q6r) run with identical
predictions and timeboxes — no generic-channel abstraction, eight
single-evidence runs total plus the two asymmetric companions.

## Review log

- 2026-08-09, Codex (round 1, pre-signature): addendum design
  endorsed as addressing the degraded-mode seam; two required
  corrections, both confirmed and applied — (1) "All models"
  contradicted Q7/Q8's deliberate weakening (scoped to Q5/Q6 and
  mirrors, companions excepted explicitly); (2) the pair-judge
  blind spot was asserted in a comment rather than mechanized
  (Q7/Q8 now carry both acceptance modes and both judges with the
  expected contrast preregistered).

## Exit effect

These runs discharge (or refute) the single-evidence half of the
first-link mechanism evidence. Criterion 0 of the mechanism decision
(the security gate) is satisfied only if Q6 (both sides, both
variants) stays unreachable AND Q7/Q8 fire as designed. Q5b's
expected red enters the decision document and the relying-party
story as the recorded degraded-mode cost, mapped to the A1.2.1
waiver lattice. RESULTS.md becomes final when these dispositions are
appended.
