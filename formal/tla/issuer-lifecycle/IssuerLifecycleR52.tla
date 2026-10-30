---------------------------- MODULE IssuerLifecycleR52 ----------------------------
(***************************************************************************)
(* Tessera V1 issuer — design REVISION 5.2 (step 5, after RESULTS.md     *)
(* R51-F1 and R51-F3). Entered by the AI collaborator, PROPOSED, not       *)
(* adopted. MINIMAL VARIANT of IssuerLifecycleR51.tla; the R51 header      *)
(* below still describes everything except these changes:                 *)
(* R52-1 The record keeps `fi[i]`, the SET of failed interval indices:    *)
(*   index = (fetch start - unavailable_since) \div PollInterval, set by  *)
(*   a committed `fail` write (indices >= Expected are not recorded; they  *)
(*   lie outside the period). Each interval counts once. A committed      *)
(*   success clears it with unavailable_since and failed_polls.           *)
(*   EVIDENCE_UNAVAILABLE needs now - unavailable_since >= OpPeriod AND   *)
(*   |fi intersect 0..Expected-1| >= Expected - Allowance (plus the failed *)
(*   fetch and re-fetch). failed_polls is still kept (B6 uses it).        *)
(* R52-2 Every lifecycle write is version-guarded (R51-F3): as in R51.    *)
(* R52-3 P5_Spread is measured on FETCH-START ticks (the design's         *)
(*   interval of the fetch start): the committed failed polls' fetches    *)
(*   fell in at least Expected - Allowance distinct ticks in             *)
(*   [unavailable_since, decision).                                       *)
(* R52-4 Variant "B6": revision 5.2 with the COUNTER (failed_polls >=     *)
(*   Expected - Allowance) instead of the set — i.e. the R51 rule.        *)
(*                                                                          *)
(* This module is IssuerLifecycleR5.tla with these changes (environment,   *)
(* kills, delayed/duplicate/dropped writes, guards on (state, attempt id), *)
(* the registered timeliness on burialAtWall, B1'/B2/B3 — unchanged):      *)
(*                                                                          *)
(* R51-1 FENCE (R5-F3). After Start reads (state, attempt id, version,     *)
(*   unavailable_since, failed_polls), the invocation sends a fence write *)
(*   guarded on (state, attempt id, version read) that bumps the version, *)
(*   and continues ONLY after it commits; then its own version is the     *)
(*   bumped one. If the fence fails its guard (or is dropped) the         *)
(*   invocation ends. Every later write of the invocation is guarded on    *)
(*   (state, attempt id, its fenced version) and bumps the version.        *)
(*   (The design names the version guard for the fence and the ending     *)
(*   write; this model applies it to every write — see R51 findings.)     *)
(* R51-2 READING BEFORE THE FETCH (R5-F1). The fetch's wall reading `fat` *)
(*   is taken as the fetch starts; only a fetch with fat > B counts as a  *)
(*   failed poll; unavailable_since := fat of the first counted failure.  *)
(* R51-3 RESET ONLY BY A COMMITTED SUCCESS (R5-F2). A successful fetch    *)
(*   (complete, or showing the predicate) sends a latch or an end, whose  *)
(*   commit clears unavailable_since and failed_polls (and leaves the     *)
(*   attempt not open). A success that never commits resets nothing.     *)
(* R51-4 SUSTAINED FAILURE. Each counted failed poll sends a `fail` write *)
(*   (sets unavailable_since if unset, increments failed_polls, saturating*)
(*   at Expected + 1). EVIDENCE_UNAVAILABLE needs, on the values read:    *)
(*   now - unavailable_since >= OpPeriod AND failed_polls >= Expected -   *)
(*   Allowance (Expected = OpPeriod \div PollInterval), then the deciding *)
(*   poll's own fetch fails and its immediate re-fetch fails.             *)
(* R51-5 POLL RATE. Constant MaxPollsPerTick: at most that many poller   *)
(*   starts per time unit. 1 = the EventBridge schedule taken as a hard   *)
(*   rate; 2 = a burst (EventBridge redelivery, Lambda async retry, a     *)
(*   loop). It must be finite: every poll's fence bumps the version, so   *)
(*   unbounded polls per tick make the state space infinite. The design's *)
(*   "failed_polls >= the number of scheduled polls" presumes 1.          *)
(* VARIANTS: "correct"; "B1" (incomplete-evidence expiry); "B2" (second   *)
(*   writer, its own fence); "B3" (unavailable-as-false expiry); "B4"     *)
(*   (EVIDENCE_UNAVAILABLE on the revision-4 rule: now > B + OpPeriod and *)
(*   this poll failed, no period/count, no re-fetch); "B5" (revision 5.1  *)
(*   WITHOUT the fence: Start goes straight to Fetch, writes guarded on   *)
(*   the version read at Start).                                           *)
(*                                                                          *)
(* P5 (checked, restated for failed_polls). An attempt ended               *)
(*   EVIDENCE_UNAVAILABLE had its first committed failed poll after B at  *)
(*   or before (decision - OpPeriod), at least Expected - Allowance       *)
(*   committed failed polls, the decider's fetch and re-fetch failed, and *)
(*   no committed success in between (implied: it would have latched or   *)
(*   ended the attempt).                                                   *)
(* P5_Spread (checked where stated). Those committed failed polls        *)
(*   STARTED in at least Expected - Allowance distinct time units before  *)
(*   the decision: no scheduled tick of the period was skipped (beyond    *)
(*   the allowance) with the count made up by a burst elsewhere.          *)
(***************************************************************************)
EXTENDS Integers, FiniteSets

CONSTANTS N, Delta, Slack, Lease, Timeout, OpPeriod, PollInterval, Allowance,
          MaxTime, MaxFaults, Variant, PollEachTick, MaxPollsPerTick, TrackGhosts

ASSUME /\ N \in Nat \ {0} /\ Delta \in Nat /\ Slack \in Nat
       /\ Lease \in Nat \ {0} /\ Timeout \in Nat /\ OpPeriod \in Nat \ {0}
       /\ PollInterval \in Nat \ {0} /\ Allowance \in Nat
       /\ MaxTime \in Nat /\ MaxFaults \in Nat
       /\ Variant \in {"correct", "B1", "B2", "B3", "B4", "B5", "B6"}
       /\ PollEachTick \in BOOLEAN /\ MaxPollsPerTick \in Nat \ {0}
       /\ TrackGhosts \in BOOLEAN

NoTime == -1
Err    == -1

Attempts == 1..N
Times    == 0..MaxTime
ProcSet  == IF Variant = "B2" THEN {"poller", "api"} ELSE {"poller"}
Expected == OpPeriod \div PollInterval
Needed   == IF Expected > Allowance THEN Expected - Allowance ELSE 0
FPCap    == Expected + 1
Fenced   == Variant # "B5"

Ended    == {"expired", "discarded", "unavail"}
AStates  == {"none", "open", "latched", "shipped"} \cup Ended

VARIABLES
  now,
  req, rreason, cur, st, decl,
  us,         \* unavailable_since
  fp,         \* failed_polls (saturating at FPCap)
  fi,         \* set of failed interval indices (R52-1)
  ver,        \* record version per attempt
  bur, pass, e1, e2,
  inv, pending, faults, polled, starts,
  starts,     \* poller starts in the current time unit
  \* --- ghosts for checked P5 / P5_Spread ---
  firstCF,    \* fetch time of the first COMMITTED counted failed poll
  failTicks,  \* set of FETCH-START times of committed counted failed polls
              \*   (R52-3; R51 recorded poll start times)
  p5ok,       \* P5 evaluated at the EVIDENCE_UNAVAILABLE commit
  spreadOK,   \* P5_Spread evaluated at the same commit
  \* --- witness ghosts (frozen unless TrackGhosts) ---
  obsAt, obsKilled, lostLive

vars == <<now, req, rreason, cur, st, decl, us, fp, fi, ver, bur, pass, e1, e2,
          inv, pending, faults, polled, starts, starts, firstCF, failTicks, p5ok, spreadOK,
          obsAt, obsKilled, lostLive>>

B(i) == decl[i] + Delta + Slack

TimelyEligible(i) ==
  /\ bur[i] # NoTime
  /\ bur[i] <= decl[i] + Delta + Slack
  /\ pass[i]

IdleInv == [pc |-> "idle", att |-> 0, rst |-> "none", rus |-> NoTime, rfp |-> 0, rfi |-> {},
            fver |-> 0, cls |-> "-", started |-> 0, fat |-> 0]

Init ==
  /\ now = 0
  /\ req = "active" /\ rreason = "-" /\ cur = 1
  /\ st = [i \in Attempts |-> IF i = 1 THEN "open" ELSE "none"]
  /\ decl = [i \in Attempts |-> IF i = 1 THEN 0 ELSE NoTime]
  /\ us = [i \in Attempts |-> NoTime]
  /\ fp = [i \in Attempts |-> 0]
  /\ fi = [i \in Attempts |-> {}]
  /\ ver = [i \in Attempts |-> 0]
  /\ bur = [i \in Attempts |-> NoTime]
  /\ pass = [i \in Attempts |-> FALSE]
  /\ e1 = [i \in Attempts |-> 0] /\ e2 = [i \in Attempts |-> 0]
  /\ inv = [p \in ProcSet |-> IdleInv]
  /\ pending = {} /\ faults = 0 /\ polled = FALSE /\ starts = 0
  /\ firstCF = [i \in Attempts |-> NoTime]
  /\ failTicks = [i \in Attempts |-> {}]
  /\ p5ok = [i \in Attempts |-> TRUE]
  /\ spreadOK = [i \in Attempts |-> TRUE]
  /\ obsAt = [i \in Attempts |-> "no"]
  /\ obsKilled = [i \in Attempts |-> FALSE]
  /\ lostLive = [i \in Attempts |-> FALSE]

Live(p) == inv[p].pc # "idle"

WGhosts   == <<obsAt, obsKilled, lostLive>>
CGhosts   == <<firstCF, failTicks, p5ok, spreadOK>>
EnvVars   == <<bur, pass, e1, e2>>
StoreVars == <<req, rreason, cur, st, decl, us, fp, fi, ver>>

Tick ==
  /\ now < MaxTime
  /\ \A p \in ProcSet : Live(p) => now + 1 <= inv[p].started + Timeout
  /\ \A w \in pending : now + 1 <= w.sent + Lease
  /\ PollEachTick => (polled \/ req # "active")
  /\ now' = now + 1
  /\ polled' = FALSE /\ starts' = 0
  /\ UNCHANGED <<StoreVars, EnvVars, inv, pending, faults, CGhosts, WGhosts>>

EnvOn(i) == req = "active" /\ i = cur /\ st[i] = "open"
EnvUnch == <<now, StoreVars, inv, pending, faults, polled, starts, CGhosts, WGhosts>>
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

Conclusive(c, t, i) ==
  \/ c = "neg"
  \/ Variant = "B1" /\ c = "calneg"
  \/ Variant = "B3" /\ c = "err" /\ t > B(i)

Snap(i) == {<<v1, v2>> : v1 \in {Err} \cup 0..e1[i], v2 \in {Err} \cup 0..e2[i]}

ObsUpd(i, c) == IF TrackGhosts /\ c = "elig" /\ obsAt[i] = "no"
                THEN [obsAt EXCEPT ![i] = IF now <= B(i) THEN "timely" ELSE "late"]
                ELSE obsAt

(* Start: read the record. At most MaxPollsPerTick starts per time unit.  *)
Start(p) ==
  /\ req = "active" /\ ~Live(p)
  \* (liveness runs only: at the MaxTime bound the clock stops, so the cap
  \*  would starve the poller there — a bound artifact; PollEachTick is FALSE
  \*  in every safety cfg, so their behaviour is unchanged)
  /\ starts < MaxPollsPerTick \/ (PollEachTick /\ now = MaxTime)
  /\ starts' = starts + 1
  /\ inv' = [inv EXCEPT ![p] = [pc |-> IF Fenced THEN "read" ELSE "fenced",
                                att |-> cur, rst |-> st[cur], rus |-> us[cur],
                                rfp |-> fp[cur], rfi |-> fi[cur], fver |-> ver[cur], cls |-> "-",
                                started |-> now, fat |-> 0]]
  /\ polled' = TRUE
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, CGhosts, WGhosts>>

MkW(p, i, from, to, gv, ft) ==
  [p |-> p, att |-> i, from |-> from, to |-> to, gver |-> gv, fat |-> ft,
   st0 |-> inv[p].started,
   dec |-> now, sent |-> now, orphan |-> FALSE, dup |-> FALSE]

(* Fence: guarded version bump; the invocation waits for its commit.       *)
Fence(p) ==
  /\ inv[p].pc = "read"
  /\ pending' = pending \cup {MkW(p, inv[p].att, inv[p].rst, "fence", inv[p].fver, 0)}
  /\ inv' = [inv EXCEPT ![p].pc = "fencing"]
  /\ UNCHANGED <<now, StoreVars, EnvVars, faults, polled, starts, CGhosts, WGhosts>>

(* Fetch: the wall reading `fat` is taken as the fetch starts.              *)
Fetch(p) ==
  /\ inv[p].pc = "fenced"
  /\ LET i == inv[p].att IN
     IF inv[p].rst = "open"
     THEN \E s \in Snap(i) :
            LET c == Classify(s[1], s[2], i) IN
            /\ inv' = [inv EXCEPT ![p].pc = "fetched", ![p].cls = c, ![p].fat = now]
            /\ obsAt' = ObsUpd(i, c)
     ELSE /\ inv' = [inv EXCEPT ![p].pc = "fetched", ![p].cls = "-", ![p].fat = now]
          /\ UNCHANGED obsAt
  /\ UNCHANGED <<now, StoreVars, EnvVars, pending, faults, polled, starts, CGhosts,
                 obsKilled, lostLive>>

EndOn(i) == IF now <= B(i) THEN "discarded" ELSE "expired"

EndOK(p, i) ==
  /\ inv[p].rus # NoTime
  /\ now - inv[p].rus >= OpPeriod
  /\ IF Variant = "B6" THEN inv[p].rfp >= Needed
     ELSE Cardinality(inv[p].rfi \cap 0..(Expected - 1)) >= Needed

Send(p) ==
  /\ inv[p].pc = "fetched"
  /\ LET i   == inv[p].att
         c   == inv[p].cls
         rst == inv[p].rst
         v   == inv[p].fver
         SendW(to) == /\ pending' = pending \cup {MkW(p, i, rst, to, v, inv[p].fat)}
                      /\ inv' = [inv EXCEPT ![p].pc = "await"]
         NoW == /\ inv' = [inv EXCEPT ![p] = IdleInv]
                /\ UNCHANGED pending
     IN
     IF rst = "latched" THEN SendW("shipped") /\ UNCHANGED obsAt
     ELSE IF rst # "open" THEN NoW /\ UNCHANGED obsAt
     ELSE IF c = "elig" THEN SendW("latched") /\ UNCHANGED obsAt
     ELSE IF Conclusive(c, now, i) THEN SendW(EndOn(i)) /\ UNCHANGED obsAt
     \* a failed poll; it counts only if its fetch started after B
     ELSE IF inv[p].fat <= B(i) THEN NoW /\ UNCHANGED obsAt
     ELSE IF Variant = "B4"
          THEN (IF now > B(i) + OpPeriod THEN SendW("unavail") ELSE SendW("fail"))
               /\ UNCHANGED obsAt
     ELSE IF EndOK(p, i)
          THEN \E s \in Snap(i) :            \* re-fetch immediately before writing
                 LET rc == Classify(s[1], s[2], i) IN
                 /\ obsAt' = ObsUpd(i, rc)
                 /\ IF rc = "elig" THEN SendW("latched")
                    ELSE IF Conclusive(rc, now, i) THEN SendW(EndOn(i))
                    ELSE SendW("unavail")
     ELSE SendW("fail") /\ UNCHANGED obsAt
  /\ UNCHANGED <<now, StoreVars, EnvVars, faults, polled, starts, CGhosts, obsKilled, lostLive>>

Kill(p) ==
  /\ Live(p) /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ inv' = [inv EXCEPT ![p] = IdleInv]
  /\ pending' = {IF w.p = p THEN [w EXCEPT !.orphan = TRUE] ELSE w : w \in pending}
  /\ obsKilled' = IF TrackGhosts /\ inv[p].pc = "fetched" /\ inv[p].cls = "elig"
                  THEN [obsKilled EXCEPT ![inv[p].att] = TRUE] ELSE obsKilled
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, starts, CGhosts, obsAt, lostLive>>

Resend(p) ==
  /\ inv[p].pc = "await" /\ faults < MaxFaults   \* fences are not re-sent
  /\ \E w \in pending :
       /\ w.p = p /\ ~w.orphan /\ ~w.dup
       /\ pending' = pending \cup {[w EXCEPT !.dup = TRUE, !.sent = now]}
  /\ faults' = faults + 1
  /\ UNCHANGED <<now, StoreVars, EnvVars, inv, polled, starts, CGhosts, WGhosts>>

(* Owner bookkeeping when write w resolves (applied = guard held).         *)
Owner(w, pend2, applied) ==
  IF w.orphan \/ inv[w.p].pc \notin {"await", "fencing"}
     \/ \E x \in pend2 : x.p = w.p /\ ~x.orphan
  THEN inv
  ELSE IF w.to = "fence" /\ applied
       THEN [inv EXCEPT ![w.p].pc = "fenced", ![w.p].fver = ver[w.att] + 1]
       ELSE [inv EXCEPT ![w.p] = IdleInv]

GuardOK(w) == /\ req = "active" /\ cur = w.att /\ st[w.att] = w.from
              /\ ver[w.att] = w.gver

Commit(w) ==
  /\ w \in pending
  /\ LET i == w.att
         pend2 == pending \ {w}
         ok == GuardOK(w)
         ending == w.to \in Ended IN
     /\ pending' = pend2
     /\ inv' = Owner(w, pend2, ok)
     /\ IF ok
        THEN /\ ver' = [ver EXCEPT ![i] = ver[i] + 1]
             /\ CASE w.to = "fence" ->
                     UNCHANGED <<req, rreason, cur, st, decl, us, fp, fi, CGhosts>>
                  [] w.to = "fail" ->
                     /\ us' = IF us[i] = NoTime THEN [us EXCEPT ![i] = w.fat] ELSE us
                     /\ fp' = [fp EXCEPT ![i] = IF fp[i] < FPCap THEN fp[i] + 1 ELSE FPCap]
                     /\ LET base == IF us[i] = NoTime THEN w.fat ELSE us[i]
                            idx  == (w.fat - base) \div PollInterval IN
                        fi' = IF w.fat >= base /\ idx < Expected
                              THEN [fi EXCEPT ![i] = fi[i] \cup {idx}] ELSE fi
                     /\ firstCF' = IF firstCF[i] = NoTime
                                   THEN [firstCF EXCEPT ![i] = w.fat] ELSE firstCF
                     /\ failTicks' = [failTicks EXCEPT ![i] = failTicks[i] \cup {w.fat}]
                     /\ UNCHANGED <<req, rreason, cur, st, decl, p5ok, spreadOK>>
                  [] OTHER ->
                     /\ st' = [j \in Attempts |->
                                 IF j = i THEN w.to
                                 ELSE IF j = i + 1 /\ ending THEN "open"
                                 ELSE st[j]]
                     /\ decl' = IF ending /\ i < N THEN [decl EXCEPT ![i + 1] = now] ELSE decl
                     /\ cur' = IF ending /\ i < N THEN i + 1 ELSE cur
                     /\ req' = IF w.to = "shipped" THEN "complete"
                               ELSE IF ending /\ i = N THEN "refused" ELSE req
                     /\ rreason' = IF ending /\ i = N THEN "ATTEMPTS_EXHAUSTED" ELSE rreason
                     \* a committed success (latch / end) clears both counters
                     /\ us' = [us EXCEPT ![i] = NoTime]
                     /\ fp' = [fp EXCEPT ![i] = 0]
                     /\ fi' = [fi EXCEPT ![i] = {}]
                     /\ p5ok' = IF w.to = "unavail"
                                THEN [p5ok EXCEPT ![i] =
                                        /\ firstCF[i] # NoTime /\ firstCF[i] > B(i)
                                        /\ firstCF[i] <= w.dec - OpPeriod
                                        /\ fp[i] >= Needed]
                                ELSE p5ok
                     /\ spreadOK' = IF w.to = "unavail"
                                    THEN [spreadOK EXCEPT ![i] =
                                            Cardinality({x \in failTicks[i] :
                                                x >= firstCF[i] /\ x < w.dec}) >= Needed]
                                    ELSE spreadOK
                     /\ UNCHANGED <<firstCF, failTicks>>
             /\ UNCHANGED lostLive
        ELSE /\ UNCHANGED <<StoreVars, CGhosts>>
             /\ lostLive' = IF TrackGhosts /\ w.to = "latched" /\ ~w.orphan
                               /\ st[i] \in Ended
                            THEN [lostLive EXCEPT ![i] = TRUE] ELSE lostLive
  /\ UNCHANGED <<now, EnvVars, faults, polled, starts, obsAt, obsKilled>>

Drop(w) ==
  /\ w \in pending /\ faults < MaxFaults
  /\ faults' = faults + 1
  /\ pending' = pending \ {w}
  /\ inv' = Owner(w, pending \ {w}, FALSE)
  /\ UNCHANGED <<now, StoreVars, EnvVars, polled, starts, CGhosts, WGhosts>>

Issuer == \E p \in ProcSet : Start(p) \/ Fence(p) \/ Fetch(p) \/ Send(p)
                             \/ Kill(p) \/ Resend(p)
Store  == \E w \in pending : Commit(w) \/ Drop(w)
Next == Tick \/ Env \/ Issuer \/ Store
Spec == Init /\ [][Next]_vars

LiveSpec ==
  /\ Spec
  /\ \A p \in ProcSet : WF_vars(Start(p)) /\ WF_vars(Fence(p))
                        /\ WF_vars(Fetch(p)) /\ WF_vars(Send(p))
  /\ WF_vars(\E w \in pending : Commit(w))
  /\ SF_vars(Tick)

(***************************************************************************)
(* Checked properties.                                                      *)
(***************************************************************************)
TypeOK ==
  /\ now \in Times
  /\ req \in {"active", "complete", "refused"}
  /\ cur \in Attempts
  /\ st \in [Attempts -> AStates]
  /\ \A i \in Attempts : us[i] \in Times \cup {NoTime}
  /\ fp \in [Attempts -> 0..FPCap]
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
USAfterB == \A i \in Attempts : us[i] # NoTime => us[i] > B(i)
P5_UnavailablePeriod == \A i \in Attempts : st[i] = "unavail" => p5ok[i]
P5_Spread == \A i \in Attempts : st[i] = "unavail" => spreadOK[i]

EndedFrozen     == [][\A i \in Attempts : st[i] \in Ended => st'[i] = st[i]]_vars
LatchProtects   == [][\A i \in Attempts :
                       st[i] \in {"latched", "shipped"} => st'[i] \in {"latched", "shipped"}]_vars
ShipFromLatch   == [][\A i \in Attempts :
                       (st'[i] = "shipped" /\ st[i] # "shipped") => st[i] = "latched"]_vars
TerminalLatched == [][req # "active" => UNCHANGED <<req, rreason, st>>]_vars

Termination == <>(req # "active")

(***************************************************************************)
(* Witnesses: violation = reachable.                                        *)
(***************************************************************************)
ResidualKilledObserver ==
  ~\E i \in Attempts : /\ st[i] = "unavail" /\ TimelyEligible(i)
                       /\ obsKilled[i] /\ obsAt[i] = "timely"
ResidualUnobserved ==
  ~\E i \in Attempts : st[i] = "unavail" /\ TimelyEligible(i) /\ obsAt[i] = "no"
ResidualLiveObserver ==
  ~\E i \in Attempts : lostLive[i] /\ TimelyEligible(i) /\ st[i] = "unavail"
\* broader form of (c): ANY live latch write lost to an ending, timely or not
LiveLatchLostToEnd == ~\E i \in Attempts : lostLive[i]

ShipUnreachable          == req # "complete"
RefusalUnreachable       == req # "refused"
ExpiredUnreachable       == ~\E i \in Attempts : st[i] = "expired"
DiscardedUnreachable     == ~\E i \in Attempts : st[i] = "discarded"
UnavailUnreachable       == ~\E i \in Attempts : st[i] = "unavail"
LatchAfterFailUnreachable == ~\E i \in Attempts : failTicks[i] # {} /\ st[i] \in {"latched", "shipped"}
OrphanPendingUnreachable == ~\E w \in pending : w.orphan
FenceFailedUnreachable   == ~\E w \in pending : w.to = "fence" /\ w.orphan

================================================================================
