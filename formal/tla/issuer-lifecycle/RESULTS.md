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
