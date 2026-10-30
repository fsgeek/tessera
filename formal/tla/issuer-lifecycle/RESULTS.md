# Issuer lifecycle model: results (2026-10-29)

This is the formal side of the issuer change in `docs/decisions/2026-10-29-issuance-lifecycle.md` (design step 10). It
models **revision 4**: steps 1, 2 and 7 to 9 of revision 3, plus steps 3 to 6 and 10 of revision 4, after
`docs/reviews/issuance-lifecycle/CODEX-CONFIRM-2.md`. The work started against revision 3. The revision-4 brief arrived
before any revision-3 model was finished, so no separate revision-3 module exists. What the revision-3 analysis found
is recorded under F8. The AI collaborator entered this model. It is PROPOSED, not adopted.

Files (all in `formal/tla/issuer-lifecycle/`):

| File | Role |
|---|---|
| `IssuerLifecycle.tla` | The module. One spec; `Variant` selects the correct design or a broken companion. |
| `IssuerLifecycle.cfg` / `.out` | Correct model, safety (P1–P3). |
| `IssuerLifecycle_B1.cfg` / `.out` | B1′: expiry or discard on incomplete evidence. |
| `IssuerLifecycle_B2.cfg` / `.out` | B2: a second concurrent writer. |
| `IssuerLifecycle_B3.cfg` / `.out` | B3: expiry on a failed or partial fetch. |
| `IssuerLifecycle_Live.cfg` / `.out` | P4 termination. |
| `IssuerLifecycle_LiveNoStep5.cfg` / `.out` | P4 control: step 5 disabled. Must be red. |
| `IssuerLifecycle_Sanity.cfg` / `.out` | Vacuity witnesses. |
| `IssuerLifecycle_Residual.cfg` / `.out` | Residual witnesses. Not checked properties; reachability reports. |
| `run-witnesses.sh` | Runs each witness of a witness cfg as its own TLC run, stopping at the first violation. |

TLC: `java -XX:+UseParallelGC -cp ~/.local/lib/tla2tools.jar tlc2.TLC -workers auto -deadlock -noGenerateSpecTE
-metadir $(mktemp -d) -config <cfg> IssuerLifecycle.tla`. Witness cfgs use `./run-witnesses.sh <cfg>`. `-deadlock`
is needed because terminal states (shipped, refused, MaxTime) are artifacts of the bounds. TLC 2026.07.31, 12 cores.

## 1. What is modelled, and how

**Timeliness is the registered fact, not the issuer's write.** `bur[i]` is attempt i's `burialAtWall`. `pass[i]` is
the chain verdict of the three-conjunct predicate on its lowest qualifying presentation. The attempt is
*timely-eligible* when `bur[i] # NoTime /\ bur[i] <= decl[i] + Delta + Slack /\ pass[i]`. That is the expression in
`P5cP5P6_BridgeSlack_Latch.tla:49`, inclusive. No fetch, observation or durable write appears in it (ILC2-01).

**Environment, per attempt:**

- **Burial.** Happens at any wall time: before B, after B, or never. `pass` is chosen at burial.
- **Two attestations.**
  - `a1` sits at the lower height and carries `pass`.
  - `a2` sits at a higher height and always fails a conjunct. It is the ILC2-03 decoy.
  - Each one's evidence moves through 0 (calendar pending), 1 (attested, but the pinned `h..h+5` segment cannot yet be
    obtained) and 2 (segment obtainable). It only goes up, and a segment becomes obtainable only after burial.
  - Partial header recovery is modelled as `e2 = 2` while `e1 = 1`, followed later by `e1 -> 2`.
- **Fetches.** Each fetch returns, per attestation, any value in `0..e_j` or `Err`. A fetch can therefore be stale,
  partial or failed at any time. This is more adversarial than "monotone except a bounded outage". A fetch never shows
  more than exists.

**Issuer:**

- **Invocations.** Each invocation runs Start (read state and attempt id), then Fetch, then Send (wall reading,
  decision, one guarded write), then Await. Time may pass between any two steps, which models the observation-to-send
  delay. An invocation lives at most `Timeout` ticks.
- **Concurrency.** With reserved concurrency 1 there is one poller instance at a time.
- **Kill.** An invocation can be killed at any step, which covers a crash before persistence. Its sent writes stay
  pending and may commit up to `Lease` after the send, so a commit can come after the send. A new invocation may start
  while they are pending.
- **Resend and Drop.** Resend sends the same transition again (a duplicate transition retry). Drop means the store
  rejects the write.
- **Fault budget.** Kill, Resend and Drop share `MaxFaults`.
- **Guards.** Every write is guarded on (state, attempt id), evaluated atomically at commit.
- **Ending an attempt.** It allocates the next attempt in the same write, or records REFUSED at N.

**Decisions, for an open attempt:**

- **Eligible snapshot.** If the snapshot shows eligibility, the poller latches, at any time.
- **Complete negative snapshot.** If both segments are in hand and the lowest presentation fails, the attempt ends
  DISCARDED (now ≤ B) or EXPIRED (now > B).
- **Anything else.** No write, unless now > B + OpPeriod. Then the attempt ends EVIDENCE_UNAVAILABLE.

For a latched attempt the decision is to ship.

**Constants (main cfg):**

- `N = 2`.
- `Delta + Slack = 1`, so B = declared + 1. Only the sum enters the model.
- `Lease = 1`, `Timeout = 1`, `OpPeriod = 1`.
- `MaxTime = 7`, `MaxFaults = 2`.

`TrackGhosts = FALSE` freezes the witness-only ghosts at Init. Issuer actions never read a ghost.

**What is not modelled:**

- More than one request, and more than two attestations.
- Reorganisations. k-deep burial is assumed permanent (A1.6).
- Evidence authentication.
- `SIGNING_CLOSED` and all signing and stamping work.
- Step 7's post-latch incurable discard.
- Clock error between invocations. There is one wall clock.
- Store durability.
- The declared time of attempt i+1, which is taken as its allocation instant.
- The environment's later evidence for attempts that have already ended. It is irrelevant: a negative end needs
  complete evidence, so burial has already happened.
- Assembly after the latch, which is reduced to one ship write.
- `obsKilled` and `obsAt` are per-attempt approximations. "A timely eligible fetch existed" and "some invocation was
  killed holding an eligible snapshot" are recorded separately.

## 2. Properties and results

| Run | Result | Distinct states | Generated | Depth | Time |
|---|---|---|---|---|---|
| Correct, P1–P3 (`IssuerLifecycle.cfg`) | **GREEN**: 12 invariants, 4 action properties | 20,932,180 | 82,762,154 | 38 | 3 min 15 s |
| P4 termination (`_Live`, MaxTime 11, MaxFaults 1) | **GREEN** | 6,988,497 | 21,986,330 | 55 | 4 min 58 s |
| P4 control, step 5 off (`_LiveNoStep5`) | **RED**, Termination (lasso back to state 50) | 1,409,692 | 5,048,583 | 68 | 37 s |
| B1′ incomplete-evidence expiry (`_B1`) | **RED**, NoTimelyExpiry, 9-state trace | 17,193 (stopped) | 46,189 | 14 | <1 s |
| B2 second concurrent writer (`_B2`, MaxFaults 0) | **GREEN** on the full safety set (see F4) | 29,649,190 | 140,070,613 | 33 | 5 min 04 s |
| B3 unavailable-as-false expiry (`_B3`) | **RED**, NoTimelyExpiry, 8-state trace | 4,983 (stopped) | 13,009 | 12 | <1 s |
| Sanity, 13 witnesses (`_Sanity`) | **all 13 reachable** (healthy) | n/a | n/a | 11–21 | n/a |
| Residual, 3 witnesses (`_Residual`) | **all 3 reachable** | n/a | n/a | 12–19 | n/a |

**P1. NoTimelyExpiry: GREEN.**

- **Claim.** A timely-eligible attempt (registered definition) is never ended EXPIRED or DISCARDED.
- **Stronger forms, also green.** `NegativeEndsAreTrue`: every negative end has a failing chain verdict.
  `LatchIsTrue`: every latch has a passing one. `ExpiryAfterB`: an EXPIRED decision is taken strictly after B, and a
  DISCARDED one at or before B.
- **What it assumes about outages: nothing.** Fetches may fail, go stale or be partial forever. P1 also assumes nothing
  about the lease, kills, delays or the number of writers.
- **What it does assume:**
  1. No fetch shows more evidence than exists (evidence soundness).
  2. Complete evidence (every calendar attested, every segment obtained) fixes the lowest presentation, so its verdict
     is the chain verdict.
- **Not claimed.** P1 does not say a timely-eligible attempt is never ended EVIDENCE_UNAVAILABLE. It can be (F1, F2).

**P2. Mutual exclusion and bounds: GREEN.**

- `TypeOK`: one state per attempt.
- `OneLive`, `AllocatedPrefix`, `PastAttemptsEnded`: at most N attempts, allocated in order, only the current one live.
- `CompleteIffShipped`: at most one shipped.
- Action properties:
  - `LatchProtects`: latched or shipped never becomes ended.
  - `ShipFromLatch`: ship only from latched.
  - `EndedFrozen`: no write to an ended attempt takes effect, including orphaned and duplicate writes.

**P3. Refusal is atomic with the final end: GREEN.**

- `NoSilentEnd`: all attempts ended implies REFUSED.
- `NeverBetweenAttempts`: an active request always has an open or latched current attempt.
- `RefusedOnlyWhenExhausted`.
- `TerminalLatched` (action property).

**P4. Termination: GREEN** (`<>(req # "active")`). It rests on these assumptions:

- weak fairness of the poller's Start, Fetch and Send, and of write commit;
- strong fairness of Tick, which is disabled while an invocation or a write must resolve first;
- the schedule assumption `PollEachTick`: at least one poller start per time unit (the EventBridge rate);
- MaxFaults = 1.

There is **no fairness on evidence**: burial may never happen and every fetch may fail forever. Termination comes from
step 5. The control proves this: with `OpPeriod > MaxTime` it goes red, with a lasso in which the poller defers
forever on evidence that never completes. In a bounded model that lasso sits at MaxTime. The underlying cause, no
evidence fairness, does not depend on the bound.

**Sanity witnesses (all reachable):**

- ship;
- ship on attempt 2;
- refusal;
- EXPIRED, DISCARDED and EVIDENCE_UNAVAILABLE ends;
- a latch whose burial was after B;
- a latch on a timely burial first observed after B;
- a latch after a fetch saw the partial-header state (the lower attestation qualifying later);
- an orphaned in-flight write;
- a send later than its fetch;
- a commit later than its send;
- a resolved duplicate.

## 3. Broken companions

**B1′. Expiry on incomplete evidence (revision-3 step 6, ILC2-03): RED on NoTimelyExpiry.**

1. Attempt 1 is buried at 0 with `pass`.
2. Both calendars attest. `a2`'s segment arrives (`e1 = 1, e2 = 2`).
3. The poller fetches the class "every calendar attested, lowest in-hand presentation fails".
4. It sends DISCARDED at now = 0 ≤ B, and the write commits.

A timely-eligible attempt has been discarded while its lower attestation's segment was still missing. With the full
invariant set, B1′ also violates `NegativeEndsAreTrue`.

**B3. Expiry on a failed or partial fetch: RED on NoTimelyExpiry.**

1. Attempt 1 is buried at 1 = B with `pass`.
2. At now = 2 > B the poller's fetch returns `Err`.
3. The fetch is treated as negative, and EXPIRED commits.

With the main cfg's full set, TLC reports `NegativeEndsAreTrue` first: the expiry of a never-buried attempt on a
failed fetch is a shorter path. For that reason the B1′ and B3 cfgs check only `NoTimelyExpiry`.

**B2. A second concurrent writer: GREEN; it did not go red.** The prediction, recorded in the cfg before the run, was
green. See F4. Constants differ from main in one place, MaxFaults = 0. Two live processes already overlap writes, and
MaxFaults = 2 did not finish within minutes (more than 15M distinct states and still growing after 3 minutes).

## 4. Design findings (revision 4)

**F1. P1 holds, and none of steps 1, 4(b) or the lease is needed for it.** P1 depends only on:

- evidence soundness;
- "complete evidence fixes the verdict".

It holds with fetches that fail forever, with kills, delayed commits and duplicates, and with two writers (B2). This
is what step 4 claims ("No lease timing is relied on"). **Step 10's text still says "expiry after `B + lease`".** That
is stale wording from revision 3 and contradicts step 4. The model does not use a lease in any expiry guard; the lease
only bounds how long writes stay pending.

**F2. EVIDENCE_UNAVAILABLE ends timely-eligible attempts by three distinct paths, not one.** Step 5 calls the named
residual "the one case where a refused attempt might have been observed eligible by B". The model reaches three paths:

- **(a) `ResidualKilledObserver`: the named residual.**
  1. Burial at 1 = B; evidence complete at 1.
  2. An invocation fetches eligibility at 1 and is killed at 2 before sending.
  3. The next invocation's fetch is stale. At now = 3 > B + OpPeriod it sends EVIDENCE_UNAVAILABLE, which commits.
- **(b) `ResidualUnobserved`: ILC2-01's path.**
  1. Burial at 1 = B.
  2. No invocation polls until 3.
  3. That one fetch fails, and EVIDENCE_UNAVAILABLE commits.

  No kill is involved, and no observation was ever made.
- **(c) `ResidualLiveObserver`: a path the design does not mention.**
  1. At now = 3, invocation 1's fetch is stale, so it sends EVIDENCE_UNAVAILABLE. Then it is killed and the write is
     orphaned.
  2. Invocation 2, never killed, fetches eligibility and sends the latch.
  3. The orphaned write commits first, and the live latch fails its guard.

  Reserved concurrency 1 serialises invocations, not writes (as CODEX-CONFIRM-2 notes). This happens within one tick,
  so no lease length prevents it.

In (a) and (c) the service did observe eligibility on time, so the observation lag was not greater than S. **A2.1's
permission ("an attempt whose lag exceeds S may be refused"), which step 5 cites, does not cover them.** Path (b) is
covered only under the prose reading in which B is the service's observation time (A2:115-124). It is not covered
under the model's `burialAtWall` reading. This is the refinement question ILC2-01 raised. The model exposes it; it
cannot settle it, and the owner must.

**F3. Step 5's rule is weaker than its stated residual.** The residual says "permanent loss of the evidence for the
whole operating period". The rule as written ("after an operating period past B, an unlatched attempt whose evidence
is still incomplete may be ended") is evaluated on one poll's fetch. In trace (a) the evidence was fully obtainable at
the moment of the decision, and a single stale or failed fetch after B + OpPeriod was enough.

To match the residual, the rule would need a condition over the period itself. Examples:

- no successful fetch of any source during the period;
- a bounded number of consecutive failures spread across it;
- re-checking a preserved observation record.

Which to use is an owner choice. As written, the residual is understated.

**F4. The single writer is not load-bearing for any checked safety property.** B2 is the same procedure and guards
with a concurrent API writer, and it is green on P1 to P3. (B2 runs with MaxFaults = 0, but the correct model's fault
paths already produce writer overlap: the orphaned writes in F2(c).)

The brief required B2 to go red. A faithful second writer cannot make it go red against these properties, and the
model does not force a red. What step 1 still buys lies outside this model:

- one fewer source of the F2(c) overlap;
- idempotent external work (signing and stamping jobs);
- removing the API's existing `settle` writer, which is real code (`api.py:194`) and must be removed regardless.

**F5. Step 5 is the only termination mechanism, and the only expiry path for an attempt that never confirms.** Under
revision 4, "pending" evidence (no burial, no attestation) is never a conclusive negative. So an attempt whose anchor
never confirms is never EXPIRED. It ends only through EVIDENCE_UNAVAILABLE after B + OpPeriod. The `_LiveNoStep5`
control shows that termination fails without that path.

As a result, the common lifecycle end that A2.3 calls expiry is implemented by the path that carries the F2 residuals.
EXPIRED is reserved for complete negatives after B. The registered refusal reason for exhausting N attempts is then
mostly `EVIDENCE_UNAVAILABLE`, not `ATTEMPTS_EXHAUSTED`. CL-03's reason set and the public status text should say so.

**F6. Underspecified: what EVIDENCE_UNAVAILABLE does to attempt i < N.** Step 5 says the attempt is "ended". Step 8
lists `EVIDENCE_UNAVAILABLE` as a *request refusal* reason. The model ends the attempt and allocates i+1. At i = N it
records REFUSED with reason EVIDENCE_UNAVAILABLE (and ATTEMPTS_EXHAUSTED when the final attempt was a negative end).
If the intent is that unavailability refuses the request at once, whatever i is, the design should say so.

**F7. Confirmed, and worth stating in the design.**

- A latch of a timely burial first observed after B is reachable and protected: the permissive "may".
- A late burial that passes the chain predicate also latches.
- Partial header recovery then latch is reachable, and a lower attestation qualifying later is honoured.
- The guards hold under duplicates and orphans (`EndedFrozen`).
- The latch evidence was chain-true in every reachable state (`LatchIsTrue`).

**F8. Revision 3 (not built as a module; analysis only).** In revision 3, outages made fetches *fail*; they did not
regress silently. Expiry required (a) not latched, (b) now > B + Lease and (c) a fetch that did not show eligibility.
With monotone evidence, (c) alone already prevented a timely *observed* attempt from expiring. If an earlier fetch had
shown eligibility, every later successful fetch would too.

So a B1 that drops only the lease wait could not go red unless silent regression was modelled. The lease mattered only
for silent regression, which revision 3 itself named in its residual (outage-induced regression), and for step 5's
unavailability end if OpPeriod < Lease. Revision 4 removes both dependencies.

---

## 5. Revision 5 (`IssuerLifecycleR5.tla`)

This section models design revision 5: steps 5, 8 and 10, rewritten after findings 1 to 6 above. The revision-4
files are left unchanged at 8793966, and every R5 file is new. The AI collaborator entered this model. It is
PROPOSED, not adopted.

### 5.1 What changed in the model

- **`us[i]` (`unavailable_since`) and `ver[i]` (record version).** Every applied write to attempt i bumps `ver[i]`.
- **Setting `us[i]`.** A poll after B whose fetch does not succeed, and which read `us[i] = NoTime`, writes
  `us[i] := t`. The write is guarded on state and attempt id. The design gives it no version guard.
- **Reset.** A fetch *succeeds* when it is complete or shows the predicate holding. Every successful fetch of an open
  attempt already sends a latch or an end write, and that write is the reset. No separate reset write exists. A
  success whose write is lost therefore resets nothing (R5-F2).
- **EVIDENCE_UNAVAILABLE.** It is decided only by a live invocation that:
  - read `us[i] # NoTime` with `now − us[i] ≥ OpPeriod`;
  - had its own fetch fail;
  - re-fetched in the same step as the write.

  If the re-fetch succeeds, the poller latches or ends on it instead. Otherwise it sends the ending write, guarded on
  state, attempt id and the version it read.
- **Allocation and refusal.** Ending any attempt i < N allocates i+1. Ending attempt N records REFUSED with
  `ATTEMPTS_EXHAUSTED`. The per-attempt reason is the attempt's state.
- **`USReading`.** This constant chooses which wall reading `unavailable_since` takes (R5-F1):
  - `"fetch"`: the poll's fetch time, and the fetch must be after B;
  - `"send"`: the decision time.

  The main cfg uses `"fetch"`.
- **P5, checked as `P5_UnavailablePeriod`.** An attempt ended EVIDENCE_UNAVAILABLE had a failed poll after B at or
  before (decision − OpPeriod). The decider's own fetch and re-fetch both failed. No successful poll's write took
  effect, because such a write latches or ends the attempt.
- **P5 literal (reported, not checked).** "No successful fetch at all during the final OpPeriod before the ending."
  This counts fetches whose write was lost. The commit is taken as the ending, over the closed window
  [commit − OpPeriod, commit].
- **B4.** EVIDENCE_UNAVAILABLE after a single failed poll: the revision-4 rule (now > B + OpPeriod), with no
  `unavailable_since` and no re-fetch.
- **Bounds.** MaxFaults = 1 and MaxTime = 6; revision 4 used 2 and 7. At revision 4's bounds this module passed 190M
  distinct states after 35 minutes without finishing. MaxTime = 6 still lets both attempts end EVIDENCE_UNAVAILABLE;
  the sanity witness `RefusalAfterUnavailUnreachable` confirms it. Other constants are as in revision 4: B = declared
  + 1, Lease = Timeout = OpPeriod = 1.

### 5.2 Results

| Run | Result | Distinct states | Depth | Time |
|---|---|---|---|---|
| Correct, P1–P3 + P5 (`IssuerLifecycleR5.cfg`, 13 invariants + 4 action properties) | **GREEN** | 13,453,877 | 42 | 2 min 20 s |
| P4 termination (`R5_Live`, MaxTime 10, MaxFaults 1) | **GREEN** | 100,977,268 | 63 | **3 h 01 min** |
| B1′ incomplete-evidence expiry (`R5_B1`) | **RED**, NoTimelyExpiry, 9 states | 16,537 | 14 | <1 s |
| B3 unavailable-as-false expiry (`R5_B3`) | **RED**, NoTimelyExpiry, 8 states | 4,592 | 11 | <1 s |
| B4 single-failed-poll EVIDENCE_UNAVAILABLE (`R5_B4`) | **RED**, P5_UnavailablePeriod, 9 states | 2,069 | 11 | <1 s |
| B2 second concurrent writer (`R5_B2`, MaxFaults 0) | **GREEN** on the full set, incl. P5 | 233,267,456 | 48 | **1 h 10 min** |
| `unavailable_since` at the decision (`R5_SendReading`) | **RED**, P5_UnavailablePeriod, 13 states | 67,708 | 15 | <1 s |
| Sanity, 10 witnesses (`R5_Sanity`) | all reachable (healthy) | n/a | 10–27 | n/a |
| Residual, 3 witnesses + P5 literal (`R5_Residual`) | all 4 reachable | n/a | 17–23 | n/a |

**B2 and Live.** Both are green, B2 as finding F4 predicted. At these bounds both are far outside the minutes budget.
If they are re-run routinely, their bounds need lowering. A smaller MaxTime for Live has not been checked for
vacuity.

**B4 trace.**

1. The attempt is buried at 3 and fails its predicate. B = 1.
2. The first poll ever is at 3 > B + OpPeriod, and its fetch fails.
3. EVIDENCE_UNAVAILABLE commits at 3. The first failed poll after B is the deciding poll itself.

**Sanity witnesses (all reachable):** `us` set; latch after `us` was set; attempt 1 EVIDENCE_UNAVAILABLE followed by
a ship on attempt 2; refusal with both attempts EVIDENCE_UNAVAILABLE; an orphaned in-flight write; EXPIRED;
DISCARDED; EVIDENCE_UNAVAILABLE; ship; refusal.

### 5.3 Residual paths under revision 5 (correct model, shortest traces)

All three are still **reachable**. In each trace the attempt is timely-eligible on the registered definition: buried
at 1 = B with the predicate passing.

**(a) Killed-before-write timely observation: REACHABLE** (18 states).

1. At 1, a poll fetches eligibility, which is timely. It holds the snapshot across the tick and is killed at 2
   before sending.
2. The poll at 2 gets a stale fetch. The evidence was obtainable throughout (`e1 = 2`); the source returned stale
   data, it was not down. That poll sets `unavailable_since = 2`.
3. The poll at 3 has its fetch and its immediate re-fetch fail. Since 3 − 2 ≥ OpPeriod, it commits
   EVIDENCE_UNAVAILABLE.

The trace needs:

- a kill between the timely fetch and its write;
- a failed poll after B that starts the period;
- the decider's fetch and re-fetch failing at least OpPeriod later;
- no poll in between whose success took effect.

It does **not** need the evidence to be down, only that every poll in the period fails to obtain it, and it does not
need any polls between the two ends. Under a real 10-minute schedule, "every poll in the period failed" amounts to
whole-period loss as the design says. The rule itself does not require intermediate polls to exist.

**(b) Timely burial never observed: REACHABLE** (13 states).

1. Burial at 1, while the calendars have not returned (`e1 = e2 = 0`).
2. The poll at 2 fails and sets `unavailable_since = 2`. Its fetch was at 2; its send was at 3.
3. The poll at 3 has its fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE commits.

The trace needs the attempt's evidence to be unobtainable to every poll from the first failed poll after B through
the decision. Here it was genuinely absent: the calendars were pending. Whether A2.1 covers (b) is the B-meaning
question; see F2.

**(c) Leftover ending write beats a live latch: REACHABLE** (20 states).

1. `unavailable_since = 2`.
2. At 3, invocation 1's fetch and re-fetch fail. It sends EVIDENCE_UNAVAILABLE, guarded on version 1, and is killed.
   The write is left over.
3. Invocation 2 starts, reads version 1, fetches eligibility and sends its latch. It is never killed.
4. The leftover write commits first. The version is still 1, so the guard holds. The live latch then fails its
   guard.

The trace needs:

- a kill after the ending write is sent;
- a successor's eligible fetch and latch inside that write's lease;
- the successor having made **no write** before the leftover commits.

The version guard narrows (c) only to that last condition. It does not remove it, because the successor's latch is
itself the first write after the read.

**P5 literal: REACHABLE** (19 states). The ending write is decided at 4 on a failed fetch and re-fetch. The deciding
invocation is killed, and a successor fetches eligibility at 4. The leftover ending write commits before the
successor sends. A successful fetch therefore lies inside [commit − OpPeriod, commit]. The same is reachable with a
lost success *before* the decision: a successful poll that is killed before its write resets nothing.

### 5.4 Design findings (revision 5)

**R5-F1. Which wall reading `unavailable_since` takes is unspecified, and one reading breaks P5.** "Set by the first
poll after B whose fetch cannot complete the evidence" does not say whether the poll's time and its "after B" are
judged at the fetch or at the decision. With the decision reading (`R5_SendReading`, RED on P5), the trace is:

1. A poll fetches at 1 = B, not after B.
2. The invocation is delayed across the tick and decides at 2. It records `unavailable_since = 2`.
3. One failed poll at 3 ends the attempt.

Only one failed fetch strictly after B exists, so the one-failed-poll protection is lost. This is the same shape as
the observation-to-send gap in ILC2-02. The size of the shortening is bounded by the invocation duration (300 s
against an operating period of hours), but it breaks the rule's own guarantee.

The fetch reading (main cfg) is green. The design should say: `unavailable_since` is a wall reading taken *before*
the fetch begins, and the fetch must begin after B.

**R5-F2. "Reset by any poll whose fetch succeeds" holds only for successes whose write takes effect. P5 literal is
not attainable by any implementation.**

- A successful poll that is killed before its write, or whose write the store rejects, leaves no durable trace, so
  nothing can reset on it.
- An ending write already sent can commit after a later successful fetch, as in path (c).

P5 as checked here is the attainable form: one failed poll is never enough, and no durable success intervenes. If
the author needs the literal form, it would require a durable record written *before* each fetch, for example a
per-invocation fence (R5-F3). That has not been modelled.

**R5-F3. The version guard does not close path (c).** The successor's first write is the latch itself, so the
version it read is still current when the leftover ending write commits. A candidate repair, **untested**: each
invocation durably bumps the attempt's version (a fence) before fetching, and waits for that write to commit. Any
write left over from a predecessor then fails its version guard. This is a candidate only. Revision 4's finding
still applies to any write path without a version guard.

**R5-F4. The residual statement in step 5 is accurate for (b), and needs one qualifier for (a).** (a) needs only
that every poll in the period *failed to obtain* the evidence. That includes stale or partial answers from sources
that are up, not only "evidence then stayed unobtainable" in the sense of an outage. (c) remains as stated, with the
condition in 5.3.

**R5-F5 (confirmed, no change needed).**

- Revision 5 is green on P1 to P5 under the fetch reading.
- B4 shows that the `unavailable_since` period is what P5 depends on.
- P1 is unaffected by the revision-5 changes. B1′ and B3 stay red.
- Termination: see the table.
- `USAfterB` holds: `unavailable_since` is only ever a failed poll's time strictly after B.

Files added (in `formal/tla/issuer-lifecycle/`):

- `IssuerLifecycleR5.tla`
- `IssuerLifecycleR5.cfg` / `.out`
- `IssuerLifecycleR5_B1`, `_B2`, `_B3`, `_B4`, `_SendReading`, `_Live`, `_Sanity`, `_Residual`, each as `.cfg` /
  `.out`
- `run-witnesses-r5.sh`

---

## 6. Revision 5.1 (`IssuerLifecycleR51.tla`)

This section models design revision 5.1, step 5, which applies R5-F1 to R5-F4. All files are new. Sections 1 to 5
and their files are unchanged. The AI collaborator entered this model. It is PROPOSED, not adopted.

### 6.1 What changed in the model (relative to `IssuerLifecycleR5.tla`)

- **Fence.** After reading the record, an invocation sends a fence write: guarded on (state, attempt id, version
  read), bumping the version. It continues only after the fence commits. If the fence fails its guard or is dropped,
  the invocation ends. Every later write of the invocation is guarded on its fenced version and bumps it.

  The design names the version guard only for the fence and the ending write. This model applies it to every write;
  see R51-F3.
- **The fetch's wall reading `fat` is taken as the fetch starts.**
  - Only a failed fetch with `fat > B` counts.
  - `unavailable_since` is the `fat` of the first counted failure.
- **Counting failures.**
  - Each counted failed poll sends a `fail` write that sets `unavailable_since` if it is unset and increments
    `failed_polls`.
  - A committed latch or end clears both. A success that never commits resets nothing.
- **When EVIDENCE_UNAVAILABLE is allowed.** It requires, on the values read:
  - `now − unavailable_since ≥ OpPeriod`;
  - `failed_polls ≥ Expected − Allowance`, where `Expected = OpPeriod ÷ PollInterval`;
  - the decider's fetch fails;
  - its immediate re-fetch fails.
- **Poll rate.** `MaxPollsPerTick` caps poller starts per time unit:
  - 1 is the EventBridge schedule taken as a hard rate;
  - 2 is a burst (redelivery, an asynchronous retry, a loop).

  The cap must be finite, because every fence bumps the version. With unlimited polls per tick the first run reached
  depth 90 and was still climbing.
- **P5 (restated).** An EVIDENCE_UNAVAILABLE end had:
  - its first committed failed poll after B, at or before (decision − OpPeriod);
  - at least `Expected − Allowance` committed failed polls;
  - a failed fetch and a failed re-fetch at the decision;
  - no committed success in between.
- **`P5_Spread` (new).** Those committed failed polls *started* in at least `Expected − Allowance` distinct time
  units before the decision. In other words, no scheduled tick was skipped with the count made up elsewhere.
- **B5.** Revision 5.1 without the fence: writes are guarded on the version read at Start.
- **Bounds.**
  - OpPeriod = 2 and PollInterval = 1, so Expected = 2. Allowance = 0.
  - B = declared + 1. Lease = Timeout = 1. MaxFaults = 1. One poll per tick, except where stated.
  - Main and companions: N = 2, MaxTime = 6.
  - Residual and (c) checks: N = 1, MaxTime = 5. B = 1; the failed polls fall at 2 and 3; the end is decided at 4;
    a leftover write can still resolve until 5.

### 6.2 Results

| Run | Result | Distinct states | Depth | Time |
|---|---|---|---|---|
| **(A)** (c) on the correct model, 2 polls/tick (`R51_C_Correct`: ResidualLiveObserver, LiveLatchLostToEnd) | **NOT violated: (c) UNREACHABLE** (exhaustive) | 6,042,359 | 78 | 50 s |
| (A) (c) on the correct model, 1 poll/tick (`R51_Residual`, ResidualLiveObserver) | **NOT violated: UNREACHABLE** (exhaustive) | 1,336,457 | 47 | n/a |
| (A) B5, no fence, same bounds (`R51_C_B5`) | **RED**: (c) reachable again | 653,170 | 27 | 6 s |
| (B) residual (a), 1 poll/tick (`R51_Residual`) | **REACHABLE** | 804,942 | 32 | n/a |
| (B) residual (b), 1 poll/tick | **REACHABLE** | 345,279 | 26 | n/a |
| (B) residual (a), 2 polls/tick (`R51_ResidualBurst`) | **REACHABLE** | 1,486,947 | 33 | n/a |
| (B) residual (b), 2 polls/tick | **REACHABLE** | 524,835 | 26 | n/a |
| (C) Correct: P1–P3, P5, P5_Spread, USAfterB (15 invariants, 4 action properties; `R51.cfg`) | **GREEN** | 55,000,011 | 59 | 8 min 31 s |
| (C) Correct with bursts (`R51_Burst`, 2 polls/tick) | P5 green; **P5_Spread RED** (R51-F1) | 1,098,650 (stopped) | 26 | 7 s |
| (C) B1′ (`R51_B1`) | **RED**, NoTimelyExpiry (12 states) | 24,373 | 15 | <1 s |
| (C) B3 (`R51_B3`) | **RED**, NoTimelyExpiry (10 states) | 10,870 | 13 | <1 s |
| (C) B4 (`R51_B4`) | **RED**, P5_UnavailablePeriod (11 states) | 6,309 | 12 | <1 s |
| (C) B2 (`R51_B2`, N = 1, MaxTime 5, MaxFaults 0) | **GREEN** on the full set | 3,095,528 | 46 | 38 s |
| (D) Termination (`R51_Live`, N = 1, MaxTime 7, 1 poll/tick, PollEachTick) | **GREEN** (see note) | 494,025 | 60 | 22 s |
| Sanity, 8 witnesses (`R51_Sanity`, ghosts on) | all reachable (healthy) | n/a | 9–28 | n/a |

**Termination note.** The first `R51_Live` run was red because of a bound artifact:

1. The attempt latched at MaxTime = 7.
2. The one-start-per-tick cap allowed no further poll in that final tick, so the ship never ran.

The cap is now lifted at `now = MaxTime` when `PollEachTick` is TRUE. That is the liveness configuration only. Every
safety cfg sets `PollEachTick = FALSE`, so their behaviour is unchanged by the edit; the safety `.out` files were
produced before it. The artifact run's output was not kept in the repository. Termination at N = 2 was not run: the
N = 2 safety space is already 55M states, and the liveness graph would not fit in 30 minutes.

**Why the (A) result is not vacuous.** B5 goes red at identical bounds. The correct-model sanity run reaches an
orphaned in-flight write and an orphaned fence. So the bounds can express the race, and the fence removes it.

**B4 trace.**

1. The first poll ever starts at 4 > B + OpPeriod = 3.
2. It fences, and its fetch fails.
3. EVIDENCE_UNAVAILABLE commits at 4, with `failed_polls = 0`.

### 6.3 Residual reachability under revision 5.1

In each trace the attempt is timely-eligible: buried at 1 = B with the predicate passing.

**(c) Leftover ending write beats a live latch: UNREACHABLE.** This holds at 1 and at 2 polls per tick, with one
kill, delayed commits and drops, checked exhaustively at the bounds above. A leftover ending write carries the
version its invocation fenced. Any successor must commit its own fence before it fetches, and that commit bumps the
version. The leftover write then fails its guard, or it committed earlier, in which case the successor's fence fails
on state and the successor never observes anything.

B5 (no fence) restores (c) in 27 steps:

1. With polls in ticks 2 and 4, two failures are counted.
2. The decider sends EVIDENCE_UNAVAILABLE and is killed.
3. A successor reads the same version, fetches eligibility and sends its latch.
4. The leftover write commits first.

**(a) Killed-before-write timely observation: REACHABLE**, at 1 poll per tick (32 steps).

1. The tick-1 poll fences, fetches eligibility at B and is killed before writing.
2. The polls started at 2, at 3 and at 4 (the decider) all run their fence, fetch and write, and all their fetches
   fail. The evidence was obtainable the whole time (`e1 = 2`); the sources answered stale or with an error.
3. `unavailable_since = 2`. `failed_polls` reaches 2 by tick 4.
4. The decider's fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE commits at 4.

What it needs:

- a kill between the timely fetch and its write;
- **every scheduled poll from the first failed poll through the decision runs, and every one fails to obtain the
  evidence;**
- the decider's re-fetch fails too.

No poll is skipped. The fence wait shifts the tick-3 poll's fetch into tick 4, which is within the invocation
timeout.

**(b) Timely burial never observed: REACHABLE**, at 1 poll per tick (26 steps).

1. Burial happens at 1. The calendars have not returned (`e1 = e2 = 0`) through tick 4.
2. The polls started at 2, at 3 and at 4 (the decider) all fail.
3. EVIDENCE_UNAVAILABLE commits at 4.

What it needs: every scheduled poll in the period runs and fails, with the evidence genuinely not yet available.
Whether A2.1 covers (b) is still the B-meaning question (finding F2).

**With bursts (2 polls/tick), polls can be skipped.**

- (a): the shortest trace needs no skip. The killed observer and a second poll both run in tick 1.
- (b): the polls start at 2, 4 and 4, so **tick 3 has no poll at all**. Two failures at 2 and 4 make
  `failed_polls = 2`, and the attempt ends at 4.

`R51_Burst` shows the same against `P5_Spread`: polls at 3, 5 and 5, tick 4 skipped, EVIDENCE_UNAVAILABLE at 5. The
count requirement is met while a scheduled interval had no poll (R51-F1).

### 6.4 Design findings (revision 5.1)

**R51-F1. `failed_polls ≥ scheduled polls − allowance` counts polls, not intervals, so bursts can fill the gaps.**
EventBridge redelivery, Lambda asynchronous retries, or a poller that visits an attempt more than once per run can
add failed polls inside one interval. Those extra failures make up for an interval in which no poll ran at all. So
"every scheduled poll in the period ran and failed" is not what the counter guarantees. At one poll per interval it
is: `R51.cfg` is green on `P5_Spread`.

Candidate repairs, **not modelled**:

- count at most one failed poll per poll interval, for example by keeping the last counted interval and incrementing
  only when it changes;
- or keep the set or bitmap of failed intervals and require the period's intervals, less the allowance.

**R51-F2. The fence closes (c), as the design claims.** It costs one extra committed write per poll per attempt. It
also introduces an orphaned-fence path, which the sanity run reaches. An orphaned fence that commits late only
invalidates a live successor's writes. That is safe, but the successor's work is wasted and it must re-poll.

**R51-F3. The version guard on the `failed_polls` increment is load-bearing, and the design does not state it.** The
design names the version guard for the fence and the ending write. If the `fail` write were guarded only on (state,
attempt id), a duplicate send (an ambiguous response, then a retry) or a leftover increment would count one failed
poll twice. That is the same inflation as R51-F1. This model guards every write on the fenced version, so this is not
exercised; it is stated for the design and the code.

**R51-F4. (a) and (b) are narrowed as the design states, under one poll per interval.** Both now need every
scheduled poll from the first failed poll after B through the decision to run and fail. (a) additionally needs a kill
between a timely fetch and its write. A "fail" includes a source that is up but stale. The design's residual
statement is accurate at one poll per interval. With bursts it holds only after R51-F1 is repaired.

Files added (in `formal/tla/issuer-lifecycle/`):

- `IssuerLifecycleR51.tla`
- `IssuerLifecycleR51.cfg` / `.out`
- `IssuerLifecycleR51_{Burst,B1,B2,B3,B4,C_Correct,C_B5,Residual,ResidualBurst,Sanity,Live}.cfg` / `.out`
- `run-witnesses-r51.sh`

---

## 7. Revision 5.2 (`IssuerLifecycleR52.tla`, minimal variant)

This section models design revision 5.2, step 5. Finding R51-F1 is repaired by a set of failed interval indices, and
R51-F3 by stating that every lifecycle write is version-guarded. The module is `IssuerLifecycleR51.tla` with four
changes; everything else is as in section 6. The AI collaborator entered this model. It is PROPOSED, not adopted.

### 7.1 Changes

- **The failed-interval set.**
  - The record keeps `fi[i]`, the set of failed interval indices. An index is (fetch start − `unavailable_since`)
    ÷ PollInterval.
  - A committed `fail` write adds its index. Indices at or beyond `Expected` lie outside the period and are not
    recorded.
  - Each interval counts once. A committed success clears the set, together with `unavailable_since` and
    `failed_polls`.
- **The end condition.** EVIDENCE_UNAVAILABLE needs `now − unavailable_since ≥ OpPeriod` and
  `|fi ∩ 0..Expected−1| ≥ Expected − Allowance`, plus the failed fetch and failed re-fetch.
- **Version guards.** Every write is version-guarded, as it already was in R51 (R51-F3).
- **`P5_Spread` is measured on fetch-start ticks.** The design defines the interval by the fetch start, so: the
  committed failed polls' fetches fall in at least `Expected − Allowance` distinct ticks in
  [`unavailable_since`, decision).
- **B6.** Revision 5.2 with the `failed_polls` counter instead of the set, which is the R51 rule.

**Bounds.** N = 1; B = declared + 1; OpPeriod 2 and PollInterval 1, so Expected = 2; Allowance 0; 2 polls per tick;
MaxFaults 1. MaxTime is 6 for the Burst, B6 and Sanity runs, and 5 for the residual and (c) runs.

### 7.2 Results

| # | Run | Result | Distinct states | Depth | Time |
|---|---|---|---|---|---|
| 1 | 2 polls per tick (`R52_Burst`: P5, P5_Spread, NoTimelyExpiry, USAfterB), exhaustive | **GREEN** | 18,055,522 | 91 | 2 min 31 s |
| 1 | Vacuity at the same bounds (`R52_Sanity`) | EVIDENCE_UNAVAILABLE, refusal and ship all **reachable** | n/a | 16–26 | n/a |
| 2 | Burst traces (polls at 2,4,4 / 3,5,5) | **No longer end the attempt.** Covered by #1: no reachable EVIDENCE_UNAVAILABLE end leaves an interval of the period without a failed fetch. | | | |
| 3 | Residual (a), 2 polls per tick (`R52_ResidualBurst`) | **REACHABLE**, with a failed fetch in every interval | 1,725,115 | 33 | n/a |
| 3 | Residual (b), 2 polls per tick | **REACHABLE**, with a failed fetch in every interval | 591,795 | 26 | n/a |
| 4 | (c), correct model, 2 polls per tick (`R52_C_Correct`), exhaustive | **NOT violated: UNREACHABLE** | 7,833,548 | 80 | 1 min 06 s |
| 5 | B6, counter instead of set (`R52_B6`) | **RED on P5_Spread** | 684,153 | 26 | 4 s |

**B6 trace (#5).**

1. A poll fetches at 3, fails, and sets `unavailable_since = 3`.
2. The poll started at 4 waits for its fence and fetches at 5. It fails.
3. A second poll fetches at 5 and fails, and with `failed_polls = 2` it ends the attempt.

Fetch ticks {3, 5}: interval 1 (tick 4) had no fetch, and the counter still allowed the end. This is the 3,5,5 shape
from section 6, on fetch-start ticks. Under the set rule the same polls give `fi = {0}` (index 2 lies outside the
period), so the attempt does not end. That is #1.

**Residual traces (#3).**

- **(a).** The tick-1 poll fetches eligibility at B and is killed. Fetches at 2, 3 and 4 all fail, with the evidence
  obtainable throughout. `fi` becomes {0, 1}. The tick-4 decider's fetch and re-fetch fail, and EVIDENCE_UNAVAILABLE
  commits.
- **(b).** Burial at 1, calendars pending. Fetches at 2 and 3 fail, so `fi = {0, 1}` (two polls ran in tick 3; one
  of them fetched in tick 3). The tick-4 decider fails, and EVIDENCE_UNAVAILABLE commits.

Both shortest traces have a failed fetch in **every** interval of the period. #1 shows exhaustively that no reachable
EVIDENCE_UNAVAILABLE end lacks one. So, at 2 polls per tick, (a) and (b) are reachable **only** when every interval
from `unavailable_since` to the decision contains a failed fetch. (a) also needs a kill between the timely fetch and
its write.

### 7.3 Findings (revision 5.2)

**R52-F1. The repair works.** The set of interval indices restores "every interval of the period had a failed poll"
under bursts. B6 shows that the counter alone does not.

**R52-F2. Minor, for the implementation: intervals are keyed by fetch start, not by the schedule tick.** A poll that
waits for its fence across an interval boundary fetches in the next interval. Its own scheduled interval can then be
left without a failed fetch, and the attempt waits longer. That is safe: it only delays the end. The runbook's
operating period should allow for it. Revision 5.2 measures what the design says, so no change is needed.

No other finding. Not re-run for revision 5.2: P1–P3 at N = 2, B1′, B3, B4, B2, termination. The R52 changes touch
only the end condition and its bookkeeping. P5 and NoTimelyExpiry were re-checked in #1.

Files added (in `formal/tla/issuer-lifecycle/`):

- `IssuerLifecycleR52.tla`
- `IssuerLifecycleR52_{Burst,B6,ResidualBurst,C_Correct,Sanity}.cfg` / `.out`
- `run-witnesses-r52.sh`

---

## 8. Revision 5.3 (`IssuerLifecycleR53.tla`)

This section models design revision 5.3, step 5, after `docs/reviews/issuance-lifecycle/CODEX-CONFIRM-3.md` (ILC3-01
to ILC3-03 and section B). The module is `IssuerLifecycleR52.tla` with the changes below; its header lists them. The
AI collaborator entered this model. It is PROPOSED, not adopted.

### 8.1 Changes

- **Rolling window (ILC3-03).**
  - `failed_intervals` holds **absolute** indices, `fetch_start ÷ PollInterval`, of committed failed fetches started
    after B. A committed success clears it.
  - EVIDENCE_UNAVAILABLE needs `|Win(now) ∩ failed_intervals| ≥ Expected − Allowance`, plus the failed fetch and
    failed re-fetch. `unavailable_since` is kept (for `USAfterB`) but no longer gates the end.
  - The constant `WindowMode` chooses `Win` (see R53-F1). With c = now ÷ PollInterval:
    - `"completed"`: c−Expected..c−1, the Expected most recent completed intervals. This is the main reading.
    - `"literal"`: c−Expected+1..c, the window ending *at* the current interval, counting committed failures only.
- **P5 restated over interval membership (ILC3-02).** At the ending commit, at least `Expected − Allowance` intervals
  of the decision's window each contain a committed failed fetch that **started** in that interval.
  `P5_SpreadOld` is the R51/R52 cardinality property (distinct fetch-start times before the decision), kept for B7.
- **`AllowKill` (ILC3-01).** FALSE disables `Kill`.
- **Companions.**
  - B6 and B7: the R51 counter rule.
  - B8: the R52 fixed window, with indices relative to `unavailable_since` and only the first Expected counted.
- **The liveness relief at MaxTime is capped at one extra start.** The R51 relief allowed unlimited starts at
  MaxTime, which makes the state space infinite whenever an attempt never ends, because every fence bumps the
  version. The first Live_A0 run reached depth 3,953 and was stopped. Safety cfgs set `PollEachTick = FALSE` and are
  unaffected.
- **Bounds.** OpPeriod 2, PollInterval 1 (so Expected = 2), B = declared + 1, Lease = Timeout = 1. All cfgs use
  PollInterval = 1, which makes B8's relative index equal R52's. The rest are stated per run.

### 8.2 Results

| Item | Run | Result | Distinct states | Depth | Time |
|---|---|---|---|---|---|
| (5) | **Correct safety** (`R53.cfg`: P1–P3, USAfterB, P5 membership, 4 action properties; N = 2, MaxTime 6, 1 poll/tick, MaxFaults 1, Allowance 0) | **GREEN** | 41,001,345 | 60 | 6 min 35 s |
| (5) | Correct, 2 polls per tick (`R53_Burst`: P5, NoTimelyExpiry, USAfterB; N = 1, MaxTime 6) | **GREEN** | 20,956,376 | 91 | 2 min 41 s |
| (5) | (c) on the correct model, 2 polls per tick, exhaustive (`R53_C_Correct`) | **NOT violated: UNREACHABLE** | 8,322,323 | 80 | 1 min 06 s |
| (5) | B1′ / B3 | **RED**, NoTimelyExpiry | 20,527 / 10,093 | 15 / 14 | <1 s |
| (5) | B4 | **RED**, P5 | 6,373 | 13 | <1 s |
| (5) | B6, counter, 2 polls per tick | **RED**, P5 (membership) | 692,218 | 26 | 4 s |
| (2) | **B7**, counter, **1 poll per tick**, `P5_SpreadOld` on fetch-start times | **RED** | 443,391 | 25 | 3 s |
| (3) | **ILC3-01**: (a) with Kill disabled (`R53_NoKill`, 2 polls/tick, MaxFaults 1 used by Drop/Resend) | **REACHABLE** | 722,985 | 35 | n/a |
| (3) | (a) killed observer / (b) unobserved, 2 polls/tick (`R53_ResidualBurst`) | **both REACHABLE** | 1,743,266 / 613,974 | 34 / 26 | n/a |
| (4) | Rolling window recovers after a gap (`R53_Roll`, EndAfterGapUnreachable; 1 poll/tick, no faults) | **REACHABLE** (healthy) | 257,044 | 33 | 3 s |
| (4) | **B8** fixed window: stranding state reached (`R53_B8`, FixedWindowStranded) | **REACHABLE** | 7,503 | 15 | <1 s |
| (4) | B8: an attempt with a gap in its fixed window never ends (`R53_B8_NoEnd`), exhaustive | **HOLDS**: never ends | 488,041 | 53 | 4 s |
| (4) | Termination, rolling window, **Allowance 1** (`R53_Live_A1`; N = 1, MaxTime 7, PollEachTick, no faults) | **GREEN** | 19,487 | 47 | 1 s |
| (4) | Termination, rolling window, **Allowance 0** (`R53_Live_A0`) | **RED** (R53-F2) | 199,541 | 66 | 6 s |
| (4) | Termination, `"literal"` window, Allowance 0 (`R53_Live_Literal`) | **RED** (R53-F1) | 249,606 | 66 | 8 s |
| (4) | Termination, B8 fixed window, Allowance 0 (`R53_Live_B8`) | **RED**: strands | 122,301 | 66 | 6 s |

### 8.3 What the traces show

**B7 (ILC3-02 reproduced).** At one poll per tick, under the counter rule:

1. A fetch at 3 fails.
2. The poll started at 4 waits for its fence and fetches at 5. It fails.
3. A poll at 5 fails, and the counter reaches 2. The attempt ends at 5.

Fetch-start ticks are {3, 5}, and interval 4 has no failed fetch. R51 reported `P5_Spread` green at one poll per tick
only because its ghost recorded invocation-start ticks {3, 4}. Section 6's statement that one poll per tick gives
coverage (R51-F1, "At one poll per interval it is: `R51.cfg` is green on `P5_Spread`") is **withdrawn**: it was a
property of the ghost, not of the rule. The R53 membership property is red for the counter (B6) and green for the
rolling set.

**ILC3-01, path (a) without a kill.**

1. Burial at 1 = B. The tick-1 poll fetches eligibility and sends its latch.
2. The store drops the latch. Nobody is killed.
3. Fetches at 2, 3 and 4 fail, with the evidence obtainable throughout.
4. `failed_intervals = {2, 3}`, and the tick-4 decider ends the attempt EVIDENCE_UNAVAILABLE.

The design's revised wording of (a), "an observed eligible presentation whose latch never commits (killed, dropped or
guard-failed)", is the right one.

**(a) and (b) at 2 polls per tick.**

- (a): the timely observer is killed. Committed failed fetches start at 2 and 3. The decider at 4 fails its fetch and
  re-fetch.
- (b): calendars pending. Failed fetches at 2 and 3; the decider at 4.

Both need a committed failed fetch in **every** interval of the completed window (Allowance 0). The green `R53_Burst`
run shows that no reachable end lacks one.

**ILC3-03, stranding.**

- `R53_Roll` (rolling window): failures at 2, 4 and 5, with interval 3 missing. The attempt still ends at 6 on window
  4..5.
- B8 (fixed window): failures at 3 and later, with interval 4 missing. Exhaustively, no such attempt ever ends. The
  `Live_B8` lasso polls at every tick to MaxTime with the attempt still open.

### 8.4 Findings (revision 5.3)

**R53-F1. "The intervals ending at the current one" must exclude the current interval, or count the decider's own
failed fetch.** Under the literal reading (`"literal"`: the current interval must already be in the committed set),
at one poll per interval the current interval holds only the decider, whose failure is not yet committed. The window
is therefore never covered, and the attempt **strands**. `Live_Literal` is red: it polls every tick from 2 to 7 with
every interval failing and never ends. Its trace ends in a latch at the bound, which is a bound artifact.

The model's `"completed"` reading (the Expected most recent *completed* intervals) avoids this and is green on all
safety. The design text should name it.

**R53-F2. At Allowance 0 the rolling window can still be starved, by alternating fetch-start slips.** A poll that
starts at t can fetch at t or at t+1 (fence wait, within the invocation timeout). `Live_A0`:

1. Fetches start at 2, 4, 4, 6, 6, 7.
2. Intervals 3 and 5 have no fetch start, although a poll ran in every tick.
3. No two consecutive completed intervals are both covered, so the attempt never ends.

The lasso sits at MaxTime, but the pattern repeats with period 2. Allowance 1 (`Live_A1`, green) removes it: a fetch
can slip at most one interval, so two consecutive intervals are never both empty.

Real deployment: the poll interval is 600 s and the timeout 300 s. Starvation needs the slip to alternate, which
requires schedule jitter, but nothing in the design excludes it. Two options, neither modelled:

- **Allowance ≥ 1 per window**, or more generally enough to absorb slips (any allowance of at least 1 sufficed
  here).
- Index the interval by the invocation's **scheduled** time rather than its fetch start, which is what R51's ghost
  did. That trades away ILC3-02's precision about when the evidence was actually checked.

So the claim "never strands the attempt" holds for the rolling window only with Allowance ≥ 1, or under a
no-alternating-slip assumption.

**R53-F3. P5 as now checked is the membership property Codex asked for.** It is green for the rolling set (1 and 2
polls per tick) and red for the counter (B6, B7) and for the single-poll rule (B4). The residual paths (a) (including
without a kill) and (b) are reachable, and only with a committed failed fetch in every interval of the completed
window (less the allowance). (c) stays unreachable.

**Not re-run for revision 5.3** (their last results are in the sections named):

- B2 (sections 6 and 7);
- B5, the no-fence (c) companion (section 6; R53 re-checked only that (c) is unreachable on the correct model);
- the R5.1/R5.2 sanity witnesses: ship, refusal, expiry, discard, orphans (sections 6 and 7);
- the residual runs at 1 poll per tick (section 6; R53 ran 2 polls per tick);
- termination at N = 2 (never run; N = 1 only);
- `R5_SendReading` and the revision-4/5 cfgs.

R53 also does not model ILC3-04 (S3 lifecycle expiry of live attempt material). The store abstraction hides it.

Files added (in `formal/tla/issuer-lifecycle/`):

- `IssuerLifecycleR53.tla`
- `IssuerLifecycleR53.cfg` / `.out`
- `IssuerLifecycleR53_{Burst,B1,B3,B4,B6,B7,B8,B8_NoEnd,C_Correct,ResidualBurst,NoKill,Roll,Live_A1,Live_A0,Live_Literal,Live_B8}.cfg`
  / `.out`
- `run-witnesses-r53.sh`
