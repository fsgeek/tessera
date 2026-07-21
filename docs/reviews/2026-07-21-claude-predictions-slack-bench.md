# Calibration predictions — slack-parameter bridge extension (pre-run)

**Date:** 2026-07-21. **Instance:** Claude (session of the README
adoption / A2 readiness assessment). **Rule:** predictions written and
committed intent stated BEFORE any TLC run of the new module. Outcome
section appended after the runs; misses stay on the record.

**Bench item:** the slack-parameter analysis adopted as the path to the
clock-precedence ruling (round-2 blocker, GPT-5.6). Extend the bridge
with a wall-clock lifecycle guard carrying slack `S`, keep the
consensus-bounded timestamp skew (`MaxSkew`), and check whether the
chain-valid-but-discarded residue class is empty iff `S >= MaxSkew`.

## Design decisions (mine, registered)

1. **Companion module, not an edit.** `P5cP5P6_BridgeSlack.tla` copies
   the reviewed bridge and adds the lifecycle machinery. The committed
   bridge stays untouched mid-review; its header already registers that
   `Ship` gains a lifecycle guard *per the ruling* — this module is
   input to that ruling, not its implementation.
2. **The residue class is defined on opportunity, not outcome.** Under
   interleaving semantics a raw "expired AND unshipped AND chain-valid"
   state is reachable at ANY slack — scheduler laziness alone gets
   there (Tick is always enabled; nothing forces Ship). The checkable
   question is whether every chain-valid attempt HAD a live shipping
   opportunity: record `burialAtWall` (wall clock at the NewBlock that
   completes burial to the designated block) and check

       ChainValidBurialInLifecycle ==
         chain-valid  =>  burialAtWall <= declared + Delta + Slack

   The naive outcome-form residue is exhibited as a *sanity witness*
   instead (LifecycleBinds), so the scope narrowing is visible, not
   silent. Consequence for the ruling, stated now: even at sufficient
   slack, "no chain-valid attempt is discarded" is a CONTRACT statement
   (act on the opportunity), not a provable liveness property — same
   proof-vs-contract split as A2.3's refusal.
3. **Why the bound is MaxSkew.** A block arriving at wall time `w`
   carries `ts \in [w - MaxSkew, w + MaxSkew]`, so `w <= ts + MaxSkew`.
   Chain-valid requires `ts <= declared + Delta` on the designated
   block, hence `burialAtWall <= declared + Delta + MaxSkew`. The lag
   bound in this abstraction IS `MaxSkew`; the two-hour consensus
   future-bound is its real-world counterpart on the backdated side.

## Predictions (the bets)

- **P1 — Main cfg (`Slack = MaxSkew = 2`): all green**, including the
  four carried bridge invariants (PinAgreement, ShippedDesignatedAgree,
  HonestShipAccepted, LateBurialRejected — Ship's guard is strictly
  stronger, so nothing shipped-dependent can break) and the new
  `ChainValidBurialInLifecycle`. State count same order as the bridge's
  456k, modestly larger from the `burialAtWall` component (bet:
  under 2M distinct).
- **P2 — `_BrokenSlack` cfg (`Slack = 1 = MaxSkew - 1`): red on exactly
  `ChainValidBurialInLifecycle`** among the checked set. Predicted
  counterexample shape: Declare at now = 0; anchor block with in-window
  timestamp; wall clock runs ahead; burial block arrives at
  `now = declared + Delta + MaxSkew = 4` carrying a maximally backdated
  in-window timestamp `ts = 2`; burialAtWall = 4 > 3 = declared +
  Delta + Slack. Bet on trace length: 8–12 states.
- **P3 — Sanity cfg (`Slack = 2`), all four witnesses fire:**
  ship reachable; wall-clock divergence still live WITHIN the slack
  envelope (shipAtWall in `(declared+Delta, declared+Delta+Slack]` —
  the slack rule's point: chain governs inside a bounded wall
  envelope); LifecycleBinds (the laziness residue — chain-valid,
  unshipped, expired — reachable even at sufficient slack, per design
  decision 2); BurialAtCutoff (burial exactly at
  `declared + Delta + Slack`, chain-valid — tightness: the MaxSkew
  bound is achieved, so the iff is sharp, not slack).
- **P4 — The epsilon side contributes no second lag source.** The
  residue bound depends only on the designated block's timestamp;
  conjuncts 1–2 constrain the anchor block, not burial wall time. No
  epsilon-dependent violation appears at `Slack = MaxSkew`.

**Where I most expect to be wrong** (bet-and-expect-to-be-wrong): the
boundary arithmetic at the cutoff (off-by-one between `<=` in the guard
and the `BlockTimestamps` bound — exactly the class the DepthK pin
caught last time), and the possibility that `_BrokenSlack` goes red on
a SHORTER trace through the non-monotonic case than the shape I
predicted.

## Outcome (appended post-run, same day)

All four predictions held. Scored against the bets:

- **P1 — HIT.** Main cfg (Slack = 2 = MaxSkew): green on all five
  invariants; 810,082 generated / 602,219 distinct (bet "under 2M" —
  comfortably; the bridge's 456k grew ~32% from `burialAtWall`).
- **P2 — HIT, with one shape variance worth recording.** `_BrokenSlack`
  (Slack = 1): red on exactly `ChainValidBurialInLifecycle` — a full
  `-continue` sweep reports NO other invariant violated (the four
  carried bridge invariants stay green). Trace length 10, inside the
  8–12 bet. Shape variance: I predicted anchor-block-then-wall-advance;
  TLC found wall-advance-first (Tick to now = 4, then Declare's anchor
  and both burial blocks all arrive at now = 4 with maximally backdated
  in-window ts = 2, burialAtWall = 4 > 3 = declared + Delta + Slack).
  Same essential mechanism — maximally backdated in-window timestamps
  at wall time declared + Delta + MaxSkew — reached by a lazier
  schedule than my mental trace. Consistent with the round-2 lesson
  that the model finds the cheapest path, not the narrative one.
- **P3 — HIT.** Sanity: all four witnesses fire (ship reachable;
  wall-clock divergence live within the slack envelope; the
  outcome-form laziness residue live at sufficient slack;
  **BurialAtCutoff fires — the MaxSkew bound is achieved, the iff is
  sharp at this discretization**).
- **P4 — HIT** (implicitly, by the main cfg's green: no epsilon-side
  second lag source at Slack = MaxSkew).
- **Feared off-by-one at the cutoff: did not materialize.** The `<=`
  guard and the `BlockTimestamps` bound compose as intended; the
  tightness witness confirms the boundary is exercised, not merely
  admitted.

**Result, stated for the ruling (analysis, not recommendation — the
ruling is the author's):** under the two-clock candidate rule
(wall-governed lifecycle with slack S beyond the chain window,
chain-governed shipping inside it), the chain-valid-but-discarded
residue class — in its checkable opportunity form — is **empty iff
S >= the consensus lag bound** (MaxSkew in this abstraction; the
real-world counterpart of the backdated side is the median-time-past
allowance). Below the bound the residue is non-empty by a length-10
mechanical witness; at the bound it is empty and the bound is tight.
Two consequences the ruling should weigh: (1) at sufficient slack the
rule preserves BOTH A2.1's chain-governed shipping AND A2.3's
wall-clock refusal semantics, with the divergence confined to the
bounded envelope; (2) what sufficiency buys is *opportunity*, not
outcome — "no chain-valid attempt is discarded" remains a contract
obligation on the implementation (act on the live opportunity), the
same proof-vs-contract split as A2.3's refusal, and the two-receipts
residue closure (A3/row-2) should be argued from the opportunity form,
not from an assumed-empty outcome form.

---

## CORRECTION and extension (same day) — non-author bench contract, received after the run

Codex (GPT-5.6) supplied a bench contract for this experiment that
reached the author after the runs above. Scored against it honestly:

**CORRECTION 1 — "consensus lag bound" was an overclaim (Codex
constraint 2, a clean hit).** Bitcoin consensus gives median-time-past
(timestamp must exceed the median of the prior eleven) and the
two-hour future bound. Neither yields a fixed finite bound on the
BACKWARD lag `B − C` between a block's timestamp and the wall time it
is observed. The `MaxSkew` symmetric-skew abstraction (inherited from
the bridge) is STRONGER than Bitcoin's rules on exactly the difficult
half. `L` is hereby reclassified as a **declared
environment/operational-policy assumption**, not a consensus
derivation, and the result above must be read in the conditional form:

> Under a declared maximum backward timestamp-lag assumption L, slack
> S >= L makes every chain-timely attempt operationally timely at the
> moment eligibility is reached.

Whether L is an assumption Tessera is willing to register is now
explicitly PART of the clock-precedence ruling (Codex's stopping
outcome 2: if not registrable, slack has not solved the protocol
problem and precedence must be chosen without it).

**CORRECTION 2 — the iff's epistemic status.** TLC established the two
directions at bounded parameter instances (S = MaxSkew green,
S = MaxSkew − 1 red, cutoff witness). The general claim rides on the
accompanying arguments, now stated as such: (⇐) `w <= ts + MaxSkew`
gives `B <= declared + Delta + L` for any chain-valid designated block
— two lines, parameter-free; (⇒) the length-10 witness construction
(blocks at wall `declared + Delta + L` carrying maximally backdated
in-window timestamps) generalizes to any S < L. "Iff" is
argument-plus-bounded-check, not TLC-established generality.

**Scored, not corrected — constraint 1 (eligibility instant).** The
analysis invariant was already defined on B (`burialAtWall`), so no
scheduler-manufactured expiry contaminated the headline result — the
model's answer matches Codex's predicted implication exactly. But the
variant Ship guard checks `now` at EXECUTION time, not latched-at-B,
so the state space EXCLUDES shipped states that latch semantics would
allow (ship after the wall envelope when eligibility was timely). The
`_Latch` variant below closes that gap.

### Latch-variant predictions (pre-run, per the standing rule)

- **P5 — Latch main cfg (Slack = 2): green on all five invariants.**
  `ChainValidBurialInLifecycle` is untouched (defined on B). The four
  carried bridge invariants survive the ADDED late-shipped states
  because the chain predicate in Ship is unchanged. State count: bet
  0.7M–1.5M distinct (new shipped tail states over the 602k).
- **P6 — Latch sanity: the new PostEnvelopeShip witness fires**
  (shipped with `shipAtWall > declared + Delta + Slack` — the state
  execution-guard semantics forbade; under latch it is legal because
  eligibility was timely), alongside ship-reachable. Semantics note
  predicted with it: under latch, the outcome-form laziness residue
  changes meaning — an eligible-in-time unshipped attempt past the
  envelope is no longer "discarded," it remains shippable; discard
  semantics under latch are ruled by B alone.

### Latch-variant outcome (appended post-run)

- **P5 — HIT on the property, MISS on the state-count bet.** Latch main
  cfg: green on all five invariants, `ChainValidBurialInLifecycle`
  included. But 613,441 distinct states — BELOW my 0.7M–1.5M bet. The
  latch added only ~11k states over the base 602,219 (~2%), not the
  multiplied shipped tail I imagined: MaxTime = 6 bounds the
  post-envelope shipping window far tighter than my mental picture.
  The miss stays on the record.
- **P6 — HIT.** Latch sanity: both witnesses fire, including
  **PostEnvelopeShip** (shipped with `shipAtWall > declared + Delta +
  Slack` on timely eligibility) — the exact state the execution-time
  guard excluded. Codex constraint 1's scheduler artifact is
  eliminated under latch semantics, and the headline result is
  unchanged by the semantics choice — as expected, since the analysis
  invariant was always defined on B.

**Net for the ruling, both semantics now checked:** the conditional
result stands under execution-time AND latched lifecycle guards; the
latch variant is the semantics the contract recommends the protocol
adopt if slack is adopted (the scheduler cannot expire an eligible
attempt, and discard is ruled by B alone). The load-bearing open
choice is unchanged and is the author's: whether a maximum backward
timestamp-lag assumption L is registrable in A1.6-style Layer 2 terms
— if yes, two-clock-with-slack (S >= L, latched at eligibility) is
viable; if no, explicit precedence must be chosen without slack
(Codex's provisional preference: separate roles — chain time governs
the verifier predicate, wall time governs waiting-before-refusal,
refusal removes standing without touching cryptographic validity,
standing enforced by A3's lineage/equivocation mechanism — is
compatible with either answer).
