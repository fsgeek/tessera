# Pre-registered predictions — TLA+↔TLA+ bridge bench work

**Status: author-side calibration artifact, NON-DISCHARGING.** Written
2026-07-21 by the session's Claude instance AFTER designing the bridge
model on paper but BEFORE any TLC run. Genre precedent: the P5c refusal
bench predictions (scored same-day; the found thing was again in an
unpredicted category — parse-level). Scored in place after the runs;
predictions frozen.

Task under prediction: the tracker's TLA+↔TLA+ correspondence
obligation — a bridge model with block timestamps decoupled from the
tick clock, `confirmedAt` DERIVED from headers (not free, not latched),
issuer and verifier transcribed INDEPENDENTLY (P5c's depth convention
vs. A2.1/A2.2's height-h+k−1 convention), plus broken companions:
anchorAt-substitution (the obligated one), wall-clock ship, and an
off-by-one pin cfg.

## Design-time finding, registered before any run

While transcribing the issuer's Ship guard I hit a prose gap in A2.1
that the single-clock P5c could not expose: **A2.1's "The rule" sentence
states only the third conjunct** ("issuance is complete only if
confirmed_at ≤ declared + δ"). Under decoupled, non-monotonic
timestamps, conjunct 3 alone does NOT imply conjunct 2 — a
forward-skewed anchor timestamp near the boundary can give
`confirmed_at ≤ declared + δ` with `anchor_time > declared + δ`, so a
conjunct-3-only issuer would honestly ship a receipt the verifier
rejects on conjunct 2. A2.1's "by construction" sentence is *narrowly*
true (it claims only the confirmation conjunct), but the spirit —
honest ship never rejected — needs the issuer to evaluate the FULL
VALID_STRICT at Ship (which the P5c header's "identical predicate"
language already implies, but A2.1's rule sentence does not state).
The bridge's Ship is transcribed with the full three-conjunct guard,
and this question is routed to the A2 review rounds: should A2.1 state
explicitly that the issuer evaluates all three conjuncts before
shipping?

## Predictions

1. **The ε side reactivates.** P5c's header says the single clock makes
   the ε side invisible (anchors never precede declaration). I predict
   the bridge makes `anchor_time < declared` reachable (witness fires)
   and the first conjunct does real work for the first time in any
   TLA+ artifact of this project.

2. **My own transcription produces an off-by-one on the first run**
   (~40%, my highest-probability self-error): TLA+ sequences are
   1-based and the depth-vs-height conventions differ by exactly one —
   the precise seam Q6 warned about. If it happens, TLC catches it as
   either a designated-block disagreement or an out-of-bounds index.
   (Calibration note: after yesterday, I am deliberately betting ON a
   category-of-my-own-error rather than only on model semantics.)

3. **The broken companions discriminate as specified**: anchorAt
   substitution red on late-burial rejection AND designated-block
   correspondence (two faces of one defect — predicted, not a miss);
   wall-clock ship red on honest-ship-accepted via skew; pin cfg red on
   the pin invariant with a length-1 trace. Isolation greens all pass
   first try (~70%).

4. **Surprise slot:** if something unpredicted goes red, my bet is the
   non-monotonic-timestamp interaction — some invariant or witness
   turns out to silently assume `confirmedAt ≥ anchor_time`. (<25%.)

## Scoring (appended 2026-07-21 after the runs; predictions unedited)

1. **CONFIRMED.** `EpsilonSideUnreachable` fires: anchor timestamps
   before `declared` are reachable, and the first conjunct does real
   work. The fused clock's invisibility of the ε side is now a
   demonstrated model artifact, not a suspicion.

2. **DID NOT OCCUR.** The main bridge ran green on the first attempt —
   no off-by-one, no out-of-bounds (456,442 distinct states). The 40%
   bet on my own transcription error loses. Calibration note: after two
   sessions of "the error is where you aren't looking," deliberately
   looking there apparently helps — the 1-based-indexing hazard was
   handled correctly precisely because it was pre-named.

3. **CONFIRMED, one reporting-form miss.** `_BrokenAnchorSubst`: red on
   exactly the two predicted invariants (`ShippedDesignatedAgree`,
   `LateBurialRejected` — two faces of one defect, in disjoint states),
   isolation green passes first try. `_BrokenWallClock`: red on
   `HonestShipAccepted` (counterexample: declared=0, shipped at wall
   time 1, chain <<0,0,3>> — k-th confirmation forward-skewed out of
   window), isolation green passes first try. `_BrokenPin`: red on
   PinAgreement but NOT via a length-1 trace — TLC short-circuits
   constant-level invariants ("The invariant of PinAgreement is equal
   to FALSE") before exploring any state. Stronger than predicted,
   differently shaped than predicted.

4. **NO SURPRISE FIRED.** Nothing unpredicted went red; the
   non-monotonic witness fired with all invariants green, so no
   invariant silently assumes timestamp monotonicity. The session's
   largest yield remains the DESIGN-TIME finding above (A2.1's
   conjunct-3-only rule sentence), found before any tool ran — routed
   to the A2 review rounds.

Standing note: three calibration exercises now. The found-things were:
design-level (07-19), parse-level (07-20), and prose-level-found-at-
design-time (today, pre-run). Today is the first time the highest-value
finding preceded the tool run — and it was found BY the act of
transcription, which is an argument for the bridge-model method itself:
the transcription forced a precision the prose lacked, before TLC saw a
single state.
