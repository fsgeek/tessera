----------------------------- MODULE IssuerLifecycleR5 -----------------------------
(***************************************************************************)
(* Tessera V1 issuer — implementation of the registered issuance          *)
(* lifecycle, design REVISION 5 (docs/decisions/2026-10-29-issuance-       *)
(* lifecycle.md steps 5, 8, 10 revised after this directory's RESULTS.md   *)
(* findings 1-6). Entered by the AI collaborator, PROPOSED, not adopted.   *)
(*                                                                          *)
(* This module is IssuerLifecycle.tla (revision 4, committed at 8793966)   *)
(* with exactly these changes; everything else — environment, invocation   *)
(* steps, kills, delayed and duplicate writes, guards, the B1'/B2/B3       *)
(* variants, the registered timeliness on burialAtWall — is carried        *)
(* unchanged; read that module's header for it.                            *)
(*                                                                          *)
(* R5-1 (step 5) `us[i]` = the attempt record's unavailable_since, and     *)
(*   `ver[i]` = the record's version (bumped by every applied write to i). *)
(*   A poll of an open attempt after B whose fetch does not succeed, and   *)
(*   which read us[i] = NoTime, writes us[i] := now (guarded on state and  *)
(*   attempt id, like every write; the design gives it no version guard).  *)
(*   A poll whose fetch SUCCEEDS (eligible, or complete) always writes a   *)
(*   latch or an end, which leaves the attempt not open — that write IS   *)
(*   the reset: no separate reset write exists, because no successful      *)
(*   fetch of an open attempt leads to anything else. (So a success whose  *)
(*   write is lost — kill, store rejection — resets nothing. See R5        *)
(*   findings in RESULTS.md.)                                               *)
(*   EVIDENCE_UNAVAILABLE: a live invocation that read us[i] # NoTime with *)
(*   now - us[i] >= OpPeriod, whose fetch did not succeed, RE-FETCHES in   *)
(*   the same step it writes (immediately before writing); if the re-fetch *)
(*   succeeds it latches or ends on it, otherwise it sends the ending      *)
(*   write guarded on (state, attempt id, the version it read).            *)
(* R5-2 (step 8) Per-attempt end reason is the attempt's state (expired,   *)
(*   discarded, unavail). Attempt i < N ending any way allocates i+1;      *)
(*   attempt N ending records REFUSED with ATTEMPTS_EXHAUSTED.             *)
(* R5-3 Variant "B4": EVIDENCE_UNAVAILABLE after a single failed poll —   *)
(*   the revision-4 rule (now > B + OpPeriod and this poll's fetch did not *)
(*   succeed), no unavailable_since, no re-fetch; same version guard.      *)
(*                                                                          *)
(* P5 (checked, the rule's guarantee). An attempt ended                    *)
(*   EVIDENCE_UNAVAILABLE had a failed poll after B at or before           *)
(*   (decision - OpPeriod), and the deciding invocation's own fetch and    *)
(*   re-fetch at the decision both failed; and since that first failed     *)
(*   poll no successful poll's write took effect (implied: such a write    *)
(*   latches or ends the attempt). Checked as P5_UnavailablePeriod.        *)
(* P5-literal (reported, own cfg): "no successful fetch at all during the  *)
(*   final OpPeriod before the ending" — counting fetches whose write was  *)
(*   lost. See RESULTS.md R5 findings for why this form is not attainable *)
(*   by any implementation.                                                *)
(***************************************************************************)
EXTENDS Integers, FiniteSets

CONSTANTS N, Delta, Slack, Lease, Timeout, OpPeriod, MaxTime, MaxFaults,
          Variant, PollEachTick, TrackGhosts,
          USReading   \* "fetch": unavailable_since := the wall reading at the
                      \*   poll's fetch, set only if that fetch was after B;
                      \* "send": := the wall reading at the decision (after the
                      \*   fetch), set if the decision is after B. The design text
                      \*   ("the first poll after B") does not say which.

ASSUME /\ N \in Nat \ {0} /\ Delta \in Nat /\ Slack \in Nat
       /\ Lease \in Nat \ {0} /\ Timeout \in Nat /\ OpPeriod \in Nat \ {0}
       /\ MaxTime \in Nat /\ MaxFaults \in Nat
       /\ Variant \in {"correct", "B1", "B2", "B3", "B4"}
       /\ PollEachTick \in BOOLEAN /\ TrackGhosts \in BOOLEAN
       /\ USReading \in {"fetch", "send"}

NoTime == -1
Err    == -1
NoVer  == -1          \* write carries no version guard

Attempts == 1..N
Times    == 0..MaxTime
ProcSet  == IF Variant = "B2" THEN {"poller", "api"} ELSE {"poller"}

Ended    == {"expired", "discarded", "unavail"}
AStates  == {"none", "open", "latched", "shipped"} \cup Ended

VARIABLES
  now,
  \* --- durable lifecycle record ---
  req, rreason, cur, st, decl,
  us,         \* [Attempts -> Times \cup {NoTime}] unavailable_since
  ver,        \* [Attempts -> Nat] record version per attempt
  \* --- environment ---
  bur, pass, e1, e2,
  \* --- issuer ---
  inv, pending, faults, polled,
  \* --- ghosts used by the CHECKED P5 (always tracked) ---
  firstFail,  \* [Attempts -> ...] wall time of the first non-successful poll
              \*   of the open attempt strictly after B (any invocation)
  p5ok,       \* [Attempts -> BOOLEAN] evaluated when an EVIDENCE_UNAVAILABLE
              \*   end commits: firstFail[i] is after B and at or before the
              \*   ending write's decision instant minus OpPeriod
  \* --- witness-only ghosts (frozen unless TrackGhosts) ---
  obsAt, obsKilled, lostLive,
  lastSucc,   \* [Attempts -> ...] latest successful fetch of the open attempt
  succInWin   \* [Attempts -> BOOLEAN] at the EVIDENCE_UNAVAILABLE commit, a
              \*   successful fetch had happened at time >= commit - OpPeriod

vars == <<now, req, rreason, cur, st, decl, us, ver, bur, pass, e1, e2, inv,
          pending, faults, polled, firstFail, p5ok, obsAt, obsKilled,
          lostLive, lastSucc, succInWin>>

B(i) == decl[i] + Delta + Slack

TimelyEligible(i) ==
  /\ bur[i] # NoTime
  /\ bur[i] <= decl[i] + Delta + Slack
  /\ pass[i]

IdleInv == [pc |-> "idle", att |-> 0, rst |-> "none", rus |-> NoTime,
            rver |-> 0, cls |-> "-", started |-> 0, fat |-> 0]

Init ==
  /\ now = 0
  /\ req = "active" /\ rreason = "-" /\ cur = 1
  /\ st = [i \in Attempts |-> IF i = 1 THEN "open" ELSE "none"]
  /\ decl = [i \in Attempts |-> IF i = 1 THEN 0 ELSE NoTime]
  /\ us = [i \in Attempts |-> NoTime]
  /\ ver = [i \in Attempts |-> 0]
  /\ bur = [i \in Attempts |-> NoTime]
  /\ pass = [i \in Attempts |-> FALSE]
  /\ e1 = [i \in Attempts |-> 0] /\ e2 = [i \in Attempts |-> 0]
  /\ inv = [p \in ProcSet |-> IdleInv]
  /\ pending = {} /\ faults = 0 /\ polled = FALSE
  /\ firstFail = [i \in Attempts |-> NoTime]
  /\ p5ok = [i \in Attempts |-> TRUE]
  /\ obsAt = [i \in Attempts |-> "no"]
  /\ obsKilled = [i \in Attempts |-> FALSE]
  /\ lostLive = [i \in Attempts |-> FALSE]
  /\ lastSucc = [i \in Attempts |-> NoTime]
  /\ succInWin = [i \in Attempts |-> FALSE]

Live(p) == inv[p].pc # "idle"

WGhosts   == <<obsAt, obsKilled, lostLive, lastSucc, succInWin>>
CGhosts   == <<firstFail, p5ok>>
EnvVars   == <<bur, pass, e1, e2>>
StoreVars == <<req, rreason, cur, st, decl, us, ver>>

Tick ==
  /\ now < MaxTime
  /\ \A p \in ProcSet : Live(p) => now + 1 <= inv[p].started + Timeout
  /\ \A w \in pending : now + 1 <= w.sent + Lease
  /\ PollEachTick => (polled \/ req # "active")
  /\ now' = now + 1
  /\ polled' = FALSE
  /\ UNCHANGED <<StoreVars, EnvVars, inv, pending, faults, CGhosts, WGhosts>>

(* Environment: unchanged from revision 4.                                 *)
EnvOn(i) == req = "active" /\ i = cur /\ st[i] = "open"
EnvUnch == <<now, StoreVars, inv, pending, faults, polled, CGhosts, WGhosts>>
Bury(i) ==
  /\ EnvOn(i) /\ bur[i] = NoTime
  /\ bur' = [bur EXCEPT ![i] = now]
  /\ \E v \in BOOLEAN : pass' = [pass EXCEPT ![i] = v]
  /\ UNCHANGED <<e1, e2>> /\ UNCHANGED EnvUnch
Attest1(i) ==
  /\ EnvOn(i) /\ e1[i] = 0 /\ e1' = [e1 EXCEPT ![i] = 1]
  /\ UNCHANGED <<bur, pass, e2>> /\ UNCHANGED EnvUnch
Attest2(i) ==
  /\ EnvOn(i) /\ e2[i] = 0 /\ e2' = [e2 EXCEPT ![i] = 1]
  /\ UNCHANGED <<bur, pass, e1>> /\ UNCHANGED EnvUnch
Segment1(i) ==
  /\ EnvOn(i) /\ e1[i] = 1 /\ bur[i] # NoTime /\ e1' = [e1 EXCEPT ![i] = 2]
  /\ UNCHANGED <<bur, pass, e2>> /\ UNCHANGED EnvUnch
Segment2(i) ==
  /\ EnvOn(i) /\ e2[i] = 1 /\ bur[i] # NoTime /\ e2' = [e2 EXCEPT ![i] = 2]
  /\ UNCHANGED <<bur, pass, e1>> /\ UNCHANGED EnvUnch
Env == \E i \in Attempts : Bury(i) \/ Attest1(i) \/ Attest2(i)
                            \/ Segment1(i) \/ Segment2(i)

Classify(v1, v2, i) ==
  IF v1 = 2 /\ pass[i] THEN "elig"
  ELSE IF v1 = Err \/ v2 = Err THEN "err"
  ELSE IF v1 = 2 /\ v2 = 2 THEN "neg"
  ELSE IF v1 >= 1 /\ v2 >= 1 /\ (v1 = 2 \/ v2 = 2) THEN "calneg"
  ELSE "pending"

(* A fetch SUCCEEDS when it is complete or shows the predicate holding.    *)
Success(c) == c \in {"elig", "neg"}

Conclusive(c, t, i) ==
  \/ c = "neg"
  \/ Variant = "B1" /\ c = "calneg"
  \/ Variant = "B3" /\ c = "err" /\ t > B(i)

Snap(i) == {<<v1, v2>> : v1 \in {Err} \cup 0..e1[i], v2 \in {Err} \cup 0..e2[i]}

(* Ghost bookkeeping for one fetch of open attempt i with class c at now.  *)
FF(i, c) == IF ~Success(c) /\ now > B(i) /\ firstFail[i] = NoTime
            THEN [firstFail EXCEPT ![i] = now] ELSE firstFail
LS(i, c) == IF TrackGhosts /\ Success(c) THEN [lastSucc EXCEPT ![i] = now]
            ELSE lastSucc

Start(p) ==
  /\ req = "active" /\ ~Live(p)
  /\ inv' = [inv EXCEPT ![p] = [pc |-> "read", att |-> cur, rst |-> st[cur],
                                rus |-> us[cur], rver |-> ver[cur],
                                cls |-> "-", started |-> now, fat |-> 0]]
  /\ polled' = TRUE
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, CGhosts, WGhosts>>

Fetch(p) ==
  /\ inv[p].pc = "read"
  /\ LET i == inv[p].att IN
     IF inv[p].rst = "open"
     THEN \E s \in Snap(i) :
            LET c == Classify(s[1], s[2], i) IN
            /\ inv' = [inv EXCEPT ![p].pc = "fetched", ![p].cls = c, ![p].fat = now]
            /\ firstFail' = FF(i, c)
            /\ lastSucc' = LS(i, c)
            /\ obsAt' = IF TrackGhosts /\ c = "elig" /\ obsAt[i] = "no"
                        THEN [obsAt EXCEPT ![i] = IF now <= B(i) THEN "timely" ELSE "late"]
                        ELSE obsAt
     ELSE /\ inv' = [inv EXCEPT ![p].pc = "fetched", ![p].cls = "-"]
          /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, polled, p5ok,
                 obsKilled, lostLive, succInWin>>

MkW(p, i, from, to, val, gv) ==
  [p |-> p, att |-> i, from |-> from, to |-> to, val |-> val, gver |-> gv,
   dec |-> now, sent |-> now, orphan |-> FALSE, dup |-> FALSE]

EndOn(c, i) == IF now <= B(i) THEN "discarded" ELSE "expired"

(* Send: wall reading, decision, at most one guarded write.                *)
(*  OUT(w) — send write w; NONE — defer.                                   *)
Send(p) ==
  /\ inv[p].pc = "fetched"
  /\ LET i   == inv[p].att
         c   == inv[p].cls
         rst == inv[p].rst
         SendW(w) == /\ pending' = pending \cup {w}
                     /\ inv' = [inv EXCEPT ![p].pc = "await"]
         NoW == /\ inv' = [inv EXCEPT ![p] = IdleInv]
                /\ UNCHANGED pending
     IN
     IF rst = "latched"
     THEN SendW(MkW(p, i, "latched", "shipped", 0, NoVer))
          /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     ELSE IF rst # "open" THEN NoW /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     ELSE IF c = "elig" THEN SendW(MkW(p, i, "open", "latched", 0, NoVer))
                             /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     ELSE IF Conclusive(c, now, i)
          THEN SendW(MkW(p, i, "open", EndOn(c, i), 0, NoVer))
               /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     \* the poll counts as "after B" by the reading USReading names
     ELSE IF (IF USReading = "fetch" /\ Variant # "B4" THEN inv[p].fat ELSE now) <= B(i)
          THEN NoW /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     \* --- a non-successful poll after B ---
     ELSE IF Variant = "B4"
          THEN (IF now > B(i) + OpPeriod
                THEN SendW(MkW(p, i, "open", "unavail", 0, inv[p].rver))
                ELSE NoW)
               /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     ELSE IF inv[p].rus = NoTime
          THEN SendW(MkW(p, i, "open", "setUS",
                         IF USReading = "fetch" THEN inv[p].fat ELSE now, NoVer))
               /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
     ELSE IF now - inv[p].rus >= OpPeriod
          THEN \* re-fetch immediately before writing (same step)
               \E s \in Snap(i) :
                 LET rc == Classify(s[1], s[2], i) IN
                 /\ firstFail' = FF(i, rc)
                 /\ lastSucc' = LS(i, rc)
                 /\ obsAt' = IF TrackGhosts /\ rc = "elig" /\ obsAt[i] = "no"
                             THEN [obsAt EXCEPT ![i] = IF now <= B(i) THEN "timely" ELSE "late"]
                             ELSE obsAt
                 /\ IF rc = "elig" THEN SendW(MkW(p, i, "open", "latched", 0, NoVer))
                    ELSE IF Conclusive(rc, now, i)
                         THEN SendW(MkW(p, i, "open", EndOn(rc, i), 0, NoVer))
                    ELSE SendW(MkW(p, i, "open", "unavail", 0, inv[p].rver))
     ELSE NoW /\ UNCHANGED <<firstFail, lastSucc, obsAt>>
  /\ UNCHANGED <<now, StoreVars, EnvVars, faults, polled, p5ok, obsKilled,
                 lostLive, succInWin>>

Kill(p) ==
  /\ Live(p) /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ inv' = [inv EXCEPT ![p] = IdleInv]
  /\ pending' = {IF w.p = p THEN [w EXCEPT !.orphan = TRUE] ELSE w : w \in pending}
  /\ obsKilled' = IF TrackGhosts /\ inv[p].pc = "fetched" /\ inv[p].cls = "elig"
                  THEN [obsKilled EXCEPT ![inv[p].att] = TRUE] ELSE obsKilled
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, CGhosts, obsAt, lostLive,
                 lastSucc, succInWin>>

Resend(p) ==
  /\ inv[p].pc = "await" /\ faults < MaxFaults
  /\ \E w \in pending :
       /\ w.p = p /\ ~w.orphan /\ ~w.dup
       /\ pending' = pending \cup {[w EXCEPT !.dup = TRUE, !.sent = now]}
  /\ faults' = faults + 1
  /\ UNCHANGED <<now, StoreVars, EnvVars, inv, polled, CGhosts, WGhosts>>

AfterResolve(w, pend2) ==
  IF ~w.orphan /\ inv[w.p].pc = "await"
     /\ ~\E x \in pend2 : x.p = w.p /\ ~x.orphan
  THEN [inv EXCEPT ![w.p] = IdleInv] ELSE inv

GuardOK(w) == /\ req = "active" /\ cur = w.att /\ st[w.att] = w.from
              /\ (w.gver = NoVer \/ ver[w.att] = w.gver)

Commit(w) ==
  /\ w \in pending
  /\ LET i == w.att
         pend2 == pending \ {w}
         ending == w.to \in Ended IN
     /\ pending' = pend2
     /\ inv' = AfterResolve(w, pend2)
     /\ IF GuardOK(w)
        THEN /\ ver' = [ver EXCEPT ![i] = ver[i] + 1]
             /\ IF w.to = "setUS"
                THEN /\ us' = [us EXCEPT ![i] = w.val]
                     /\ UNCHANGED <<req, rreason, cur, st, decl, p5ok, succInWin>>
                ELSE /\ st' = [j \in Attempts |->
                                 IF j = i THEN w.to
                                 ELSE IF j = i + 1 /\ ending THEN "open"
                                 ELSE st[j]]
                     /\ decl' = IF ending /\ i < N THEN [decl EXCEPT ![i + 1] = now] ELSE decl
                     /\ cur' = IF ending /\ i < N THEN i + 1 ELSE cur
                     /\ req' = IF w.to = "shipped" THEN "complete"
                               ELSE IF ending /\ i = N THEN "refused" ELSE req
                     /\ rreason' = IF ending /\ i = N THEN "ATTEMPTS_EXHAUSTED" ELSE rreason
                     /\ p5ok' = IF w.to = "unavail"
                                THEN [p5ok EXCEPT ![i] =
                                        /\ firstFail[i] # NoTime
                                        /\ firstFail[i] > B(i)
                                        /\ firstFail[i] <= w.dec - OpPeriod]
                                ELSE p5ok
                     /\ succInWin' = IF TrackGhosts /\ w.to = "unavail"
                                        /\ lastSucc[i] # NoTime
                                        /\ lastSucc[i] >= now - OpPeriod
                                     THEN [succInWin EXCEPT ![i] = TRUE] ELSE succInWin
                     /\ UNCHANGED us
             /\ UNCHANGED lostLive
        ELSE /\ UNCHANGED <<StoreVars, p5ok, succInWin>>
             /\ lostLive' = IF TrackGhosts /\ w.to = "latched" /\ ~w.orphan
                               /\ st[i] \in Ended
                            THEN [lostLive EXCEPT ![i] = TRUE] ELSE lostLive
  /\ UNCHANGED <<now, EnvVars, faults, polled, firstFail, obsAt, obsKilled, lastSucc>>

Drop(w) ==
  /\ w \in pending /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ pending' = pending \ {w}
  /\ inv' = AfterResolve(w, pending \ {w})
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, CGhosts, WGhosts>>

Issuer == \E p \in ProcSet : Start(p) \/ Fetch(p) \/ Send(p) \/ Kill(p) \/ Resend(p)
Store  == \E w \in pending : Commit(w) \/ Drop(w)
Next == Tick \/ Env \/ Issuer \/ Store
Spec == Init /\ [][Next]_vars

LiveSpec ==
  /\ Spec
  /\ \A p \in ProcSet : WF_vars(Start(p)) /\ WF_vars(Fetch(p)) /\ WF_vars(Send(p))
  /\ WF_vars(\E w \in pending : Commit(w))
  /\ SF_vars(Tick)

(***************************************************************************)
(* Checked properties (P1-P4 as in revision 4; P5 new).                    *)
(***************************************************************************)
TypeOK ==
  /\ now \in Times
  /\ req \in {"active", "complete", "refused"}
  /\ rreason \in {"-", "ATTEMPTS_EXHAUSTED"}
  /\ cur \in Attempts
  /\ st \in [Attempts -> AStates]
  /\ \A i \in Attempts : us[i] \in Times \cup {NoTime}
  /\ \A i \in Attempts : ver[i] \in Nat
  /\ faults \in 0..MaxFaults

NoTimelyExpiry ==
  \A i \in Attempts : st[i] \in {"expired", "discarded"} => ~TimelyEligible(i)
NegativeEndsAreTrue ==
  \A i \in Attempts : st[i] \in {"expired", "discarded"} => bur[i] # NoTime /\ ~pass[i]
ExpiryAfterB ==
  \A w \in pending : (w.to = "expired" => w.dec > B(w.att))
                     /\ (w.to = "discarded" => w.dec <= B(w.att))
LatchIsTrue ==
  \A i \in Attempts : st[i] \in {"latched", "shipped"} => bur[i] # NoTime /\ pass[i]
OneLive == \A i \in Attempts : st[i] \in {"open", "latched"} => i = cur
AllocatedPrefix == \A i \in Attempts : (st[i] # "none") <=> (i <= cur)
PastAttemptsEnded == \A i \in Attempts : i < cur => st[i] \in Ended
CompleteIffShipped ==
  /\ (req = "complete") <=> (\E i \in Attempts : st[i] = "shipped")
  /\ \A i, j \in Attempts : st[i] = "shipped" /\ st[j] = "shipped" => i = j
NoSilentEnd == (\A i \in Attempts : st[i] \in Ended) => req = "refused"
NeverBetweenAttempts == req = "active" => st[cur] \in {"open", "latched"}
RefusedOnlyWhenExhausted ==
  req = "refused" => /\ \A i \in Attempts : st[i] \in Ended
                     /\ cur = N /\ rreason = "ATTEMPTS_EXHAUSTED"
(* unavailable_since is only ever a failed poll's time after B.            *)
USAfterB == \A i \in Attempts : us[i] # NoTime => us[i] > B(i)

(* P5 — one failed poll is never enough: an EVIDENCE_UNAVAILABLE end was   *)
(* decided at least OpPeriod after a failed poll of the attempt after B.   *)
(* (The decider's own fetch and re-fetch failing is by construction of     *)
(* Send; no successful poll's write took effect, since such a write would  *)
(* have left the attempt latched or ended.)                                *)
P5_UnavailablePeriod ==
  \A i \in Attempts :
    st[i] = "unavail" =>
      p5ok[i]

EndedFrozen     == [][\A i \in Attempts : st[i] \in Ended => st'[i] = st[i]]_vars
LatchProtects   == [][\A i \in Attempts :
                       st[i] \in {"latched", "shipped"} => st'[i] \in {"latched", "shipped"}]_vars
ShipFromLatch   == [][\A i \in Attempts :
                       (st'[i] = "shipped" /\ st[i] # "shipped") => st[i] = "latched"]_vars
TerminalLatched == [][req # "active" => UNCHANGED <<req, rreason, st>>]_vars

Termination == <>(req # "active")

(***************************************************************************)
(* Reported (not checked) — _Residual / _P5lit cfgs; violation = reachable.*)
(***************************************************************************)
P5_Literal == \A i \in Attempts : st[i] = "unavail" => ~succInWin[i]

ResidualKilledObserver ==
  ~\E i \in Attempts : /\ st[i] = "unavail" /\ TimelyEligible(i)
                       /\ obsKilled[i] /\ obsAt[i] = "timely"
ResidualUnobserved ==
  ~\E i \in Attempts : st[i] = "unavail" /\ TimelyEligible(i) /\ obsAt[i] = "no"
ResidualLiveObserver ==
  ~\E i \in Attempts : lostLive[i] /\ TimelyEligible(i) /\ st[i] = "unavail"

\* Vacuity witnesses.
ShipUnreachable          == req # "complete"
RefusalUnreachable       == req # "refused"
ExpiredUnreachable       == ~\E i \in Attempts : st[i] = "expired"
DiscardedUnreachable     == ~\E i \in Attempts : st[i] = "discarded"
UnavailUnreachable       == ~\E i \in Attempts : st[i] = "unavail"
USSetUnreachable         == ~\E i \in Attempts : us[i] # NoTime
LatchAfterUSUnreachable  == ~\E i \in Attempts : us[i] # NoTime /\ st[i] \in {"latched", "shipped"}
UnavailThenShipUnreachable == ~(req = "complete" /\ st[1] = "unavail")
RefusalAfterUnavailUnreachable == ~(req = "refused" /\ \A i \in Attempts : st[i] = "unavail")
OrphanPendingUnreachable == ~\E w \in pending : w.orphan

================================================================================
