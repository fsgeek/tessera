# Pre-registered predictions — P5c refusal-state bench work

**Status: author-side calibration artifact, NON-DISCHARGING.** Written
2026-07-20 by the session's Claude instance AFTER designing the refusal
extension on paper but BEFORE any TLC run. Genre precedent:
`2026-07-19-claude-predictions-for-codex-elicitation-review.md` (where the
assistant's predictions missed the serious findings — prior to update).
Scored in place after the runs; scoring appended, predictions unedited.

Task under prediction: extend `formal/tla/P5c_IssuanceProtocol.tla` with
the round-3 ruling-4 refusal construction — atomic entry (final failed
attempt enters `refused` in the same transition), safety-only, claim
narrowed to "refusal durably recorded and available for retrieval" — plus
vacuity witnesses and a `_BrokenSilent` companion (the review's warned
construction: separately enabled `Refuse` action) that must go red on
exactly the silent-deadlock invariant.

## Predictions

1. **Vacuity at the old bound (design-time find, TLC-confirmable).**
   At the previously checked constants (MaxTime=8, Delta=3, MaxAttempts=3)
   refusal is unreachable: the earliest the third window can expire is
   t=12 (expiries at 4, 8, 12), so `NoSilentDeadlock` would pass
   *vacuously* at MaxTime=8 and the `RefusalUnreachable` sanity witness
   would NOT fire. Caught while designing, before running the tool —
   this is my doorway prediction ("a vacuity witness will be harder than
   expected, and the difficulty will be a finding") landing at design
   time rather than run time. Prediction for the record: at MaxTime=12
   all three refusal witnesses fire; at MaxTime=8 none would.

2. **Clean discrimination, revising my doorway hedge.** `_BrokenSilent`
   goes red on `NoSilentDeadlock` on the first run, with a shortest
   trace ending in the Tick that crosses the final deadline (~13 states),
   and the companion green cfg (all other invariants, minus the deadlock
   invariant) completes green — i.e., red on *exactly* the specified
   invariant, no repair iteration needed. In the doorway I bet the
   discrimination test would be where the first surprise lived; having
   now actually designed the construction, I downgrade that. Noted per
   the change-notification commitment: the hedge was priced before
   design.

3. **Residual surprise slot (low confidence).** If anything unexpected
   goes red, my bet is `ExpiredCannotShip` — it is stated via
   `ENABLED Ship` (the Q5 coupling in the READ-AND-CHALLENGE) and is the
   invariant most exposed to a guard change. I estimate this at <20%.

## Scoring (appended 2026-07-20 after the runs; predictions unedited)

1. **CONFIRMED, both halves.** At MaxTime=8 TLC violates only the three
   ship witnesses — all three refusal witnesses survive, i.e. refusal is
   unreachable and every refusal invariant would have passed vacuously.
   At MaxTime=12 all six witnesses fire. (Run at 8 done from a scratch
   cfg for scoring only; the repository cfgs are the 12 runs.)

2. **CONFIRMED on substance, miss on detail.** `_BrokenSilent` went red
   on exactly `NoSilentDeadlock` on its first run, and the `_Green`
   isolation control (all other invariants + the latch property)
   completed green on its first run — clean discrimination, no repair
   iteration. Detail miss: predicted a ~13-state trace; actual is 15
   states (I forgot the two Reissue steps don't advance the clock).

3. **The surprise slot fired — not where I bet.** `ExpiredCannotShip`
   never went red (the <20% was priced about right). The actual first-run
   failure was in the MAIN model: a TLA+ operator-precedence error. `=`
   binds tighter than `\/`, so the atomic entry
   `refused' = refused \/ (trigger)` parsed as
   `(refused' = refused) \/ (trigger)` — whenever the trigger held, the
   disjunction was satisfied without constraining `refused'` to TRUE,
   TLC kept `refused' = refused`, and refusal never entered. Fix:
   parenthesize the right-hand side.

   Two things worth the record. (a) The miss location is consistent with
   my standing calibration result: the serious finding lands where the
   assistant is not looking — I predicted semantic surprises and got a
   syntactic one. (b) The invariant did real work on its own author:
   the buggy main model was behaviorally a *worse* `_BrokenSilent`
   (refusal never recorded at all, not merely late), and
   `NoSilentDeadlock` flagged it on the first run with a minimal trace.
   The deadlock invariant caught an implementation error of the very
   construction it was designed to protect — evidence it isolates the
   property and not just the designed-broken companion.

Standing note for the next instance: this is now two calibration
exercises in which the found-thing was in a category the predictions did
not cover (design-level flaws on 07-19, parse-level flaw today). The
lesson is not "predict harder" — it is that the tool run / non-author
review is the load-bearing check, and the predictions' value is exactly
in making that visible.
