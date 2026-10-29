------------------------------ MODULE IssuerLifecycle ------------------------------
(***************************************************************************)
(* Tessera V1 issuer — the IMPLEMENTATION of the registered issuance       *)
(* lifecycle (A2.1 latch and expiry, A2.3 attempts and refusal), as        *)
(* designed in docs/decisions/2026-10-29-issuance-lifecycle.md, REVISION 4 *)
(* (steps 1-2 and 7-9 of revision 3; steps 3-6 and 10 of revision 4, after *)
(* docs/reviews/issuance-lifecycle/CODEX-CONFIRM-2.md ILC2-01..03).        *)
(* Paired formal side of the issuer change (design step 10). Entered by    *)
(* the AI collaborator, PROPOSED, not adopted.                             *)
(*                                                                          *)
(* RELATION TO THE REGISTERED MODEL. Timeliness is the registered          *)
(* model's chain/wall fact, not the issuer's write:                         *)
(*   P5cP5P6_BridgeSlack_Latch.tla:49                                       *)
(*     EligibleInLifecycle == burialAtWall <= declared + Delta + Slack      *)
(* Here `bur[i]` is attempt i's burialAtWall (the wall time its lowest     *)
(* attestation reached k-deep burial) and `pass[i]` is the chain verdict   *)
(* of the three-conjunct predicate on the attempt's lowest qualifying      *)
(* presentation. An attempt is TIMELY-ELIGIBLE iff                          *)
(*   bur[i] # NoTime /\ bur[i] <= B(i) /\ pass[i],  B(i) = decl+Delta+Slack *)
(* — inclusive boundary, exactly the registered expression. Nothing about  *)
(* any issuer fetch, observation or durable write enters that definition   *)
(* (ILC2-01: the property is not restated on the durable latch).           *)
(*                                                                          *)
(* ENVIRONMENT (per current attempt i; frozen once i has ended):           *)
(* - Bury(i): burial happens at some wall time, possibly after B, possibly *)
(*   never; the chain verdict pass[i] is chosen then.                       *)
(* - Two attestations per attempt (two calendars): a1 at the LOWER height  *)
(*   (its presentation carries pass[i]) and a2 at a HIGHER height, whose   *)
(*   presentation always FAILS a conjunct (the ILC2-03 decoy). e1[i], e2[i] *)
(*   in 0..2: 0 = calendar pending, 1 = Bitcoin attestation returned but   *)
(*   the pinned h..h+5 segment not yet obtainable, 2 = segment obtainable. *)
(*   Monotone. Segments become obtainable only after burial. Partial       *)
(*   header availability that later completes = e2 = 2 while e1 = 1, then  *)
(*   e1 -> 2 (the lower attestation qualifies later).                      *)
(* - Each fetch returns, per attestation, ANY value in 0..e_j or Err: it   *)
(*   may be stale, partial, or fail (outage). This is strictly more        *)
(*   adversarial than "available monotonically except a bounded outage":   *)
(*   a fetch is never assumed to see what is there. No fetch ever shows    *)
(*   MORE than is there (no forged evidence; signatures/authentication are *)
(*   out of scope).                                                        *)
(*                                                                          *)
(* ISSUER (design steps 1-8):                                              *)
(* - Invocations of the poller (ProcSet = {"poller"}) run one at a time    *)
(*   (reserved concurrency 1): Start reads (state, attempt id); Fetch     *)
(*   takes the evidence snapshot; Send takes the wall reading, decides,    *)
(*   and sends ONE guarded write; Await waits for it. Time may pass        *)
(*   between every step (observation-to-send delay), up to Timeout after  *)
(*   Start (the Lambda timeout).                                           *)
(* - Kill: an invocation may die at any step (crash before persistence if *)
(*   before Send). Its sent-but-unresolved writes stay in `pending` and    *)
(*   may still commit, any time up to Lease after their send (the stated  *)
(*   write-duration assumption, clock-tolerance decision 2026-10-27). A    *)
(*   new invocation may start while they are pending.                      *)
(* - Resend: an invocation awaiting an ambiguous response re-sends the    *)
(*   SAME transition (duplicate transition retry). Drop: the store rejects *)
(*   a write outright. Kill, Resend, Drop share the budget MaxFaults.      *)
(* - Every write is guarded on (expected state, attempt id) and is        *)
(*   evaluated atomically at commit (step 1, ILC-05).                      *)
(* - Decision (Send), for read state "open":                               *)
(*     snapshot shows eligibility (a1 segment in hand, pass)  -> LATCH,    *)
(*       at any time while open, however late (step 3);                    *)
(*     snapshot COMPLETE (both attestations, both segments) and the        *)
(*       lowest presentation fails -> end DISCARDED (now <= B) or EXPIRED  *)
(*       (now > B) (steps 4, 6);                                           *)
(*     otherwise (stale, pending, partial, failed) -> no write, unless     *)
(*       now > B + OpPeriod, then end EVIDENCE_UNAVAILABLE (step 5).       *)
(*   For read state "latched": COMPLETE (ship) — step 7's assembly is      *)
(*   abstracted to one write; complete only from latched.                  *)
(* - Ending attempt i allocates i+1 in the same write; if i = N the same   *)
(*   write records REFUSED (step 8; A2.3 atomic entry).                    *)
(* - The API makes no lifecycle writes (step 1).                           *)
(*                                                                          *)
(* VARIANTS (constant Variant; identical state space and actions; the     *)
(* only differences are the three marked guards):                          *)
(*   "correct" — revision 4.                                               *)
(*   "B1"  — B1': expiry/discard on INCOMPLETE evidence: every calendar    *)
(*           has attested and the lowest presentation whose segment is in  *)
(*           hand fails, but a lower attestation's segment is missing (the *)
(*           revision-3 step 6 rule, ILC2-03). Must be RED on              *)
(*           NoTimelyExpiry.                                               *)
(*   "B2"  — a second concurrent writer (the API path of revision 2):      *)
(*           ProcSet = {"poller","api"}, each one instance, running the    *)
(*           same decision procedure with the same guards, concurrently.   *)
(*   "B3"  — expiry on a failed/partial fetch: after B, a snapshot with a  *)
(*           failed source is treated as a negative (absence = false).     *)
(*           Must be RED on NoTimelyExpiry.                                *)
(*                                                                          *)
(* PROPERTIES (plain words; definitions below):                            *)
(* P1  NoTimelyExpiry — an attempt that is timely-eligible on the          *)
(*     registered definition (burialAtWall <= B and the chain predicate    *)
(*     holds) is never ended EXPIRED or DISCARDED. This needs NO           *)
(*     assumption about outages, observation, persistence or the lease:   *)
(*     those can only make a snapshot incomplete, and only a complete     *)
(*     snapshot ends an attempt negatively. NegativeEndsAreTrue is the     *)
(*     stronger form (any negative end has a failing chain verdict).       *)
(*     NOT CLAIMED: that a timely-eligible attempt is never ended          *)
(*     EVIDENCE_UNAVAILABLE. It can be (step 5's A2.1 "lag exceeds S may   *)
(*     be refused" reading); the witnesses ResidualKilledObserver,         *)
(*     ResidualUnobserved and ResidualLiveObserver show three distinct     *)
(*     reachable paths (see RESULTS.md, findings F2, F3).                  *)
(* P2  Mutual exclusion and bounds — one state per attempt (by type);      *)
(*     at most N attempts, allocated in order, only the current one live   *)
(*     (OneLive, AllocatedPrefix); latched/shipped never become ended      *)
(*     (LatchProtects, action); shipped only from latched (ShipFromLatch,  *)
(*     action); no write to an ended attempt takes effect (EndedFrozen,    *)
(*     action); no latch or ship of a non-current attempt (by guard).      *)
(* P3  Refusal is atomic with the final end — never all attempts ended    *)
(*     without REFUSED, never active between attempts (NoSilentEnd,        *)
(*     NeverBetweenAttempts); REFUSED only on exhaustion (RefusedOnly-     *)
(*     WhenExhausted); terminal states latch (TerminalLatched, action).    *)
(* P4  Termination — <>(req # "active") under weak fairness of the poller  *)
(*     and of write resolution, strong fairness of Tick, and the schedule  *)
(*     assumption that the poller starts at least once per time unit      *)
(*     (constant PollEachTick; EventBridge rate). No fairness on evidence: *)
(*     outages may be permanent. Separate cfg (_Live).                     *)
(*                                                                          *)
(* NOT MODELLED: more than one request; more than two attestations; reorgs *)
(* (absorbed by k-deep burial by assumption, A1.6); authentication; the    *)
(* SIGNING_CLOSED reason and signing/stamping work; step 7's post-latch    *)
(* incurable discard; the declared time of attempt i+1 is its allocation   *)
(* instant; clock error between invocations (one wall clock).              *)
(***************************************************************************)
EXTENDS Integers, FiniteSets

CONSTANTS N, Delta, Slack, Lease, Timeout, OpPeriod, MaxTime, MaxFaults,
          Variant, PollEachTick,
          TrackGhosts   \* FALSE freezes every ghost at Init (main/companion/live
                        \* runs); TRUE for the witness cfgs. Issuer actions never
                        \* read a ghost, so this changes no checked behaviour.

ASSUME /\ N \in Nat \ {0} /\ Delta \in Nat /\ Slack \in Nat
       /\ Lease \in Nat \ {0} /\ Timeout \in Nat /\ OpPeriod \in Nat
       /\ MaxTime \in Nat /\ MaxFaults \in Nat
       /\ Variant \in {"correct", "B1", "B2", "B3"}
       /\ PollEachTick \in BOOLEAN /\ TrackGhosts \in BOOLEAN

NoTime == -1
Err    == -1          \* a failed source in a fetched snapshot

Attempts == 1..N
Times    == 0..MaxTime
ProcSet  == IF Variant = "B2" THEN {"poller", "api"} ELSE {"poller"}

Ended    == {"expired", "discarded", "unavail"}
AStates  == {"none", "open", "latched", "shipped"} \cup Ended
Classes  == {"elig", "neg", "calneg", "err", "pending", "-"}

VARIABLES
  now,        \* the one wall clock
  \* --- durable lifecycle record (the store) ---
  req,        \* "active" | "complete" | "refused"
  rreason,    \* refusal reason: "-" | "ATTEMPTS_EXHAUSTED" | "EVIDENCE_UNAVAILABLE"
  cur,        \* current attempt id
  st,         \* [Attempts -> AStates]
  decl,       \* [Attempts -> Times \cup {NoTime}] declared issue time
  \* --- environment (chain, calendars, explorers) ---
  bur,        \* [Attempts -> ...] burialAtWall (registered model's name)
  pass,       \* [Attempts -> BOOLEAN] chain verdict of a1's presentation
  e1, e2,     \* [Attempts -> 0..2] obtainable evidence per attestation
  \* --- issuer processes and in-flight writes ---
  inv,        \* [ProcSet -> invocation record]
  pending,    \* set of sent, unresolved writes
  faults,     \* kills + resends + drops used
  polled,     \* a Start happened since the last Tick (schedule assumption)
  \* --- ghosts (never read by issuer actions) ---
  obsAt,      \* [Attempts -> {"no","timely","late"}] whether the first fetch
              \*   that showed eligibility was at or before B, after B, or none
  obsKilled,  \* [Attempts -> BOOLEAN] an invocation holding an eligible
              \*   snapshot was killed before sending its latch
  lostLive,   \* [Attempts -> BOOLEAN] a NON-killed invocation's latch write
              \*   failed its guard because the attempt had been ended
  sawCalneg,  \* [Attempts -> BOOLEAN] some fetch saw "calendars done, lowest
              \*   in-hand presentation fails, a segment missing"
  dSend,      \* some write was sent strictly after its fetch (obs-to-send delay)
  dCommit,    \* some write committed strictly after its send
  dupApplied  \* a duplicate (re-sent) copy of a write was resolved

vars == <<now, req, rreason, cur, st, decl, bur, pass, e1, e2, inv, pending,
          faults, polled, obsAt, obsKilled, lostLive, sawCalneg, dSend,
          dCommit, dupApplied>>

B(i) == decl[i] + Delta + Slack

(* The registered timeliness, verbatim in form from the Latch model.       *)
TimelyEligible(i) ==
  /\ bur[i] # NoTime
  /\ bur[i] <= decl[i] + Delta + Slack
  /\ pass[i]

IdleInv == [pc |-> "idle", att |-> 0, rst |-> "none", cls |-> "-",
            started |-> 0, late |-> FALSE]

Init ==
  /\ now = 0
  /\ req = "active" /\ rreason = "-" /\ cur = 1
  /\ st = [i \in Attempts |-> IF i = 1 THEN "open" ELSE "none"]
  /\ decl = [i \in Attempts |-> IF i = 1 THEN 0 ELSE NoTime]
  /\ bur = [i \in Attempts |-> NoTime]
  /\ pass = [i \in Attempts |-> FALSE]
  /\ e1 = [i \in Attempts |-> 0] /\ e2 = [i \in Attempts |-> 0]
  /\ inv = [p \in ProcSet |-> IdleInv]
  /\ pending = {} /\ faults = 0 /\ polled = FALSE
  /\ obsAt = [i \in Attempts |-> "no"]
  /\ obsKilled = [i \in Attempts |-> FALSE]
  /\ lostLive = [i \in Attempts |-> FALSE]
  /\ sawCalneg = [i \in Attempts |-> FALSE]
  /\ dSend = FALSE /\ dCommit = FALSE /\ dupApplied = FALSE

Live(p) == inv[p].pc # "idle"

GhostVars == <<obsAt, obsKilled, lostLive, sawCalneg, dSend, dCommit, dupApplied>>
EnvVars   == <<bur, pass, e1, e2>>
StoreVars == <<req, rreason, cur, st, decl>>

(***************************************************************************)
(* Time. A live invocation cannot outlive its Timeout; a sent write        *)
(* resolves (commit or reject) within Lease of its send.                   *)
(***************************************************************************)
Tick ==
  /\ now < MaxTime
  /\ \A p \in ProcSet : Live(p) => now + 1 <= inv[p].started + Timeout
  /\ \A w \in pending : now + 1 <= w.sent + Lease
  /\ PollEachTick => (polled \/ req # "active")
  /\ now' = now + 1
  /\ polled' = FALSE
  \* a snapshot held across a tick: the send will be later than the fetch
  /\ inv' = [p \in ProcSet |-> IF inv[p].pc = "fetched"
                               THEN [inv[p] EXCEPT !.late = TRUE] ELSE inv[p]]
  /\ UNCHANGED <<StoreVars, EnvVars, pending, faults, GhostVars>>

(***************************************************************************)
(* Environment, on the current open attempt only (ended attempts' later    *)
(* evidence is irrelevant to every property: a negative end needs complete *)
(* evidence, so its burial already happened).                              *)
(***************************************************************************)
EnvOn(i) == req = "active" /\ i = cur /\ st[i] = "open"

Bury(i) ==
  /\ EnvOn(i) /\ bur[i] = NoTime
  /\ bur' = [bur EXCEPT ![i] = now]
  /\ \E v \in BOOLEAN : pass' = [pass EXCEPT ![i] = v]
  /\ UNCHANGED <<now, StoreVars, e1, e2, inv, pending, faults, polled, GhostVars>>

Attest1(i) ==
  /\ EnvOn(i) /\ e1[i] = 0 /\ e1' = [e1 EXCEPT ![i] = 1]
  /\ UNCHANGED <<now, StoreVars, bur, pass, e2, inv, pending, faults, polled, GhostVars>>
Attest2(i) ==
  /\ EnvOn(i) /\ e2[i] = 0 /\ e2' = [e2 EXCEPT ![i] = 1]
  /\ UNCHANGED <<now, StoreVars, bur, pass, e1, inv, pending, faults, polled, GhostVars>>
Segment1(i) ==
  /\ EnvOn(i) /\ e1[i] = 1 /\ bur[i] # NoTime /\ e1' = [e1 EXCEPT ![i] = 2]
  /\ UNCHANGED <<now, StoreVars, bur, pass, e2, inv, pending, faults, polled, GhostVars>>
Segment2(i) ==
  /\ EnvOn(i) /\ e2[i] = 1 /\ bur[i] # NoTime /\ e2' = [e2 EXCEPT ![i] = 2]
  /\ UNCHANGED <<now, StoreVars, bur, pass, e1, inv, pending, faults, polled, GhostVars>>

Env == \E i \in Attempts : Bury(i) \/ Attest1(i) \/ Attest2(i)
                            \/ Segment1(i) \/ Segment2(i)

(***************************************************************************)
(* Evidence evaluation on a snapshot (v1, v2), each in {Err} \cup 0..2.    *)
(***************************************************************************)
Classify(v1, v2, i) ==
  IF v1 = 2 /\ pass[i] THEN "elig"                 \* a1 qualifies and passes
  ELSE IF v1 = Err \/ v2 = Err THEN "err"          \* a source failed
  ELSE IF v1 = 2 /\ v2 = 2 THEN "neg"              \* COMPLETE; lowest fails
  ELSE IF v1 >= 1 /\ v2 >= 1 /\ (v1 = 2 \/ v2 = 2)
       THEN "calneg"   \* every calendar attested; lowest IN-HAND fails; a segment missing
  ELSE "pending"

(* === THE VARIANT GUARDS (the only differences between variants) ======= *)
Conclusive(c, t, i) ==
  \/ c = "neg"                                         \* revision 4, step 4
  \/ Variant = "B1" /\ c = "calneg"                    \* B1': incomplete
  \/ Variant = "B3" /\ c = "err" /\ t > B(i)           \* B3: unavailable = false
(* (B2's difference is ProcSet above.)                                     *)

Decide(rst, c, t, i) ==
  IF rst = "open" THEN
    IF c = "elig" THEN "latched"
    ELSE IF Conclusive(c, t, i) THEN (IF t <= B(i) THEN "discarded" ELSE "expired")
    ELSE IF t > B(i) + OpPeriod THEN "unavail"
    ELSE "none"
  ELSE IF rst = "latched" THEN "shipped"
  ELSE "none"

(***************************************************************************)
(* Issuer invocation steps.                                                *)
(***************************************************************************)
(* Start = invocation begins and reads (state, attempt id) of the record.  *)
(* Reserved concurrency 1: one instance per ProcSet member. In "correct",  *)
(* ProcSet is the poller alone.                                            *)
Start(p) ==
  /\ req = "active" /\ ~Live(p)
  /\ inv' = [inv EXCEPT ![p] = [pc |-> "read", att |-> cur, rst |-> st[cur],
                                cls |-> "-", started |-> now, late |-> FALSE]]
  /\ polled' = TRUE
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, GhostVars>>

(* Fetch the attempt's evidence: any stale/partial/failed view.            *)
Fetch(p) ==
  /\ inv[p].pc = "read"
  /\ LET i == inv[p].att
         \* a latched attempt's evidence is preserved (step 7): no fetch needed
         V1 == IF inv[p].rst = "open" THEN {Err} \cup 0..e1[i] ELSE {0}
         V2 == IF inv[p].rst = "open" THEN {Err} \cup 0..e2[i] ELSE {0} IN
     \E v1 \in V1, v2 \in V2 :
       LET c == IF inv[p].rst = "open" THEN Classify(v1, v2, i) ELSE "-" IN
       /\ inv' = [inv EXCEPT ![p].pc = "fetched", ![p].cls = c, ![p].late = FALSE]
       /\ obsAt' = IF TrackGhosts /\ c = "elig" /\ obsAt[i] = "no"
                   THEN [obsAt EXCEPT ![i] = IF now <= B(i) THEN "timely" ELSE "late"]
                   ELSE obsAt
       /\ sawCalneg' = IF TrackGhosts /\ c = "calneg" THEN [sawCalneg EXCEPT ![i] = TRUE]
                       ELSE sawCalneg
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, polled, obsKilled,
                 lostLive, dSend, dCommit, dupApplied>>

(* Send: wall reading (after the read), decision, one guarded write.       *)
Send(p) ==
  /\ inv[p].pc = "fetched"
  /\ LET i == inv[p].att
         d == Decide(inv[p].rst, inv[p].cls, now, i) IN
     IF d = "none"
     THEN /\ inv' = [inv EXCEPT ![p] = IdleInv]        \* defer: no write
          /\ UNCHANGED <<pending, dSend>>
     ELSE /\ pending' = pending \cup
                {[p |-> p, att |-> i, from |-> inv[p].rst, to |-> d,
                  dec |-> now, sent |-> now, orphan |-> FALSE, dup |-> FALSE]}
          /\ inv' = [inv EXCEPT ![p].pc = "await"]
          /\ dSend' = (dSend \/ (TrackGhosts /\ inv[p].late))
  /\ UNCHANGED <<now, StoreVars, EnvVars, faults, polled, obsAt, obsKilled,
                 lostLive, sawCalneg, dCommit, dupApplied>>

(* Kill: the invocation dies at any step. Its sent writes become orphans  *)
(* (still pending, may still commit until sent + Lease).                  *)
Kill(p) ==
  /\ Live(p) /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ inv' = [inv EXCEPT ![p] = IdleInv]
  /\ pending' = {IF w.p = p THEN [w EXCEPT !.orphan = TRUE] ELSE w : w \in pending}
  /\ obsKilled' = IF TrackGhosts /\ inv[p].pc = "fetched" /\ inv[p].cls = "elig"
                  THEN [obsKilled EXCEPT ![inv[p].att] = TRUE] ELSE obsKilled
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, obsAt, lostLive, sawCalneg,
                 dSend, dCommit, dupApplied>>

(* Resend: an ambiguous response; the same transition is sent again.       *)
Resend(p) ==
  /\ inv[p].pc = "await" /\ faults < MaxFaults
  /\ \E w \in pending :
       /\ w.p = p /\ ~w.orphan /\ ~w.dup
       /\ pending' = pending \cup {[w EXCEPT !.dup = TRUE, !.sent = now]}
  /\ faults' = faults + 1
  /\ UNCHANGED <<now, StoreVars, EnvVars, inv, polled, GhostVars>>

(* Owner of a write returns to idle when none of its writes remain.        *)
AfterResolve(w, pend2) ==
  IF ~w.orphan /\ inv[w.p].pc = "await"
     /\ ~\E x \in pend2 : x.p = w.p /\ ~x.orphan
  THEN [inv EXCEPT ![w.p] = IdleInv] ELSE inv

GuardOK(w) == req = "active" /\ cur = w.att /\ st[w.att] = w.from

(* Commit: the store evaluates the guard atomically and applies or rejects. *)
(* Ending attempt i allocates i+1 or records REFUSED in the same write.     *)
Commit(w) ==
  /\ w \in pending
  /\ LET i == w.att
         pend2 == pending \ {w} IN
     /\ pending' = pend2
     /\ inv' = AfterResolve(w, pend2)
     /\ dCommit' = (dCommit \/ (TrackGhosts /\ now > w.sent))
     /\ dupApplied' = (dupApplied \/ (TrackGhosts /\ w.dup))
     /\ IF GuardOK(w)
        THEN /\ st' = [j \in Attempts |->
                         IF j = i THEN w.to
                         ELSE IF j = i + 1 /\ w.to \in Ended THEN "open"
                         ELSE st[j]]
             /\ decl' = IF w.to \in Ended /\ i < N
                        THEN [decl EXCEPT ![i + 1] = now] ELSE decl
             /\ cur' = IF w.to \in Ended /\ i < N THEN i + 1 ELSE cur
             /\ req' = IF w.to = "shipped" THEN "complete"
                       ELSE IF w.to \in Ended /\ i = N THEN "refused"
                       ELSE req
             /\ rreason' = IF w.to \in Ended /\ i = N
                           THEN (IF w.to = "unavail" THEN "EVIDENCE_UNAVAILABLE"
                                 ELSE "ATTEMPTS_EXHAUSTED")
                           ELSE rreason
             /\ UNCHANGED lostLive
        ELSE /\ UNCHANGED StoreVars
             /\ lostLive' = IF TrackGhosts /\ w.to = "latched" /\ ~w.orphan /\ st[i] \in Ended
                            THEN [lostLive EXCEPT ![i] = TRUE] ELSE lostLive
  /\ UNCHANGED <<now, EnvVars, faults, polled, obsAt, obsKilled, sawCalneg, dSend>>

(* Drop: the store rejects the write without applying it.                   *)
Drop(w) ==
  /\ w \in pending /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ pending' = pending \ {w}
  /\ inv' = AfterResolve(w, pending \ {w})
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, GhostVars>>

Issuer == \E p \in ProcSet : Start(p) \/ Fetch(p) \/ Send(p) \/ Kill(p) \/ Resend(p)
Store  == \E w \in pending : Commit(w) \/ Drop(w)

Next == Tick \/ Env \/ Issuer \/ Store

Spec == Init /\ [][Next]_vars

(* Liveness spec: the poller's own steps and write resolution are weakly   *)
(* fair; Tick strongly fair (it is disabled while a write or invocation     *)
(* must first resolve). Kill/Resend/Drop/Env carry no fairness.             *)
LiveSpec ==
  /\ Spec
  /\ \A p \in ProcSet : WF_vars(Start(p)) /\ WF_vars(Fetch(p)) /\ WF_vars(Send(p))
  /\ WF_vars(\E w \in pending : Commit(w))
  /\ SF_vars(Tick)

(***************************************************************************)
(* Invariants.                                                              *)
(***************************************************************************)
TypeOK ==
  /\ now \in Times
  /\ req \in {"active", "complete", "refused"}
  /\ rreason \in {"-", "ATTEMPTS_EXHAUSTED", "EVIDENCE_UNAVAILABLE"}
  /\ cur \in Attempts
  /\ st \in [Attempts -> AStates]
  /\ \A i \in Attempts : decl[i] \in Times \cup {NoTime}
  /\ \A i \in Attempts : bur[i] \in Times \cup {NoTime}
  /\ e1 \in [Attempts -> 0..2] /\ e2 \in [Attempts -> 0..2]
  /\ faults \in 0..MaxFaults

(* P1 — the registered obligation, on burialAtWall.                        *)
NoTimelyExpiry ==
  \A i \in Attempts : st[i] \in {"expired", "discarded"} => ~TimelyEligible(i)

(* P1, stronger: a negative end always has a failing chain verdict.        *)
NegativeEndsAreTrue ==
  \A i \in Attempts : st[i] \in {"expired", "discarded"} =>
                        bur[i] # NoTime /\ ~pass[i]

(* Expiry strictly after B; discard at or before B (inclusive boundary).   *)
(* Checked on the decision instant `dec` (the wall reading at Send; a      *)
(* re-sent duplicate keeps it).                                            *)
ExpiryAfterB ==
  \A w \in pending : (w.to = "expired" => w.dec > B(w.att))
                     /\ (w.to = "discarded" => w.dec <= B(w.att))

(* A latch is only ever written on a true chain verdict.                   *)
LatchIsTrue ==
  \A i \in Attempts : st[i] \in {"latched", "shipped"} =>
                        bur[i] # NoTime /\ pass[i]

(* P2.                                                                      *)
OneLive ==
  \A i \in Attempts : st[i] \in {"open", "latched"} => i = cur
AllocatedPrefix ==
  \A i \in Attempts : (st[i] # "none") <=> (i <= cur)
PastAttemptsEnded ==
  \A i \in Attempts : i < cur => st[i] \in Ended
CompleteIffShipped ==
  /\ (req = "complete") <=> (\E i \in Attempts : st[i] = "shipped")
  /\ \A i, j \in Attempts : st[i] = "shipped" /\ st[j] = "shipped" => i = j

(* P3.                                                                      *)
NoSilentEnd ==
  (\A i \in Attempts : st[i] \in Ended) => req = "refused"
NeverBetweenAttempts ==
  req = "active" => st[cur] \in {"open", "latched"}
RefusedOnlyWhenExhausted ==
  req = "refused" => /\ \A i \in Attempts : st[i] \in Ended
                     /\ cur = N /\ rreason # "-"

(* Action properties (PROPERTIES in the cfg).                              *)
EndedFrozen     == [][\A i \in Attempts : st[i] \in Ended => st'[i] = st[i]]_vars
LatchProtects   == [][\A i \in Attempts :
                       st[i] \in {"latched", "shipped"} =>
                         st'[i] \in {"latched", "shipped"}]_vars
ShipFromLatch   == [][\A i \in Attempts :
                       (st'[i] = "shipped" /\ st[i] # "shipped") =>
                         st[i] = "latched"]_vars
TerminalLatched == [][req # "active" => UNCHANGED <<req, rreason, st>>]_vars

(* P4.                                                                      *)
Termination == <>(req # "active")

(***************************************************************************)
(* Witnesses — _Sanity / _Residual cfgs; VIOLATION = reachable = healthy.  *)
(***************************************************************************)
\* Residual F1 (design's own named residual): an invocation held a timely
\* eligible snapshot (fetched at or before B), was killed before sending
\* its latch, and the timely-eligible attempt was later ended
\* EVIDENCE_UNAVAILABLE.
ResidualKilledObserver ==
  ~\E i \in Attempts : /\ st[i] = "unavail" /\ TimelyEligible(i)
                       /\ obsKilled[i] /\ obsAt[i] = "timely"
\* Residual F2a (ILC2-01): timely-eligible, never observed by any fetch,
\* ended EVIDENCE_UNAVAILABLE. No kill needed.
ResidualUnobserved ==
  ~\E i \in Attempts : st[i] = "unavail" /\ TimelyEligible(i) /\ obsAt[i] = "no"
\* Residual F2b: a LIVE (never killed) invocation's latch write lost its
\* guard to an earlier, killed invocation's delayed EVIDENCE_UNAVAILABLE
\* write, on a timely-eligible attempt.
ResidualLiveObserver ==
  ~\E i \in Attempts : lostLive[i] /\ TimelyEligible(i) /\ st[i] = "unavail"

\* Vacuity witnesses.
ShipUnreachable          == req # "complete"
RefusalUnreachable       == req # "refused"
ExpiredUnreachable       == ~\E i \in Attempts : st[i] = "expired"
DiscardedUnreachable     == ~\E i \in Attempts : st[i] = "discarded"
UnavailUnreachable       == ~\E i \in Attempts : st[i] = "unavail"
SecondAttemptShipUnreachable == ~(req = "complete" /\ st[1] \in Ended)
LateLatchUnreachable     == ~\E i \in Attempts :
                               st[i] = "latched" /\ bur[i] > B(i)
PartialThenLatchUnreachable == ~\E i \in Attempts :
                               st[i] \in {"latched", "shipped"} /\ sawCalneg[i]
OrphanPendingUnreachable == ~\E w \in pending : w.orphan
SendDelayUnreachable     == ~dSend
CommitDelayUnreachable   == ~dCommit
DuplicateUnreachable     == ~dupApplied
TimelyUnobservedLatchUnreachable == ~\E i \in Attempts :
                               st[i] = "latched" /\ TimelyEligible(i)
                               /\ obsAt[i] = "late"

================================================================================
