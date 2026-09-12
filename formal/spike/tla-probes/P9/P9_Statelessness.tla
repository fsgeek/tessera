---------------------------- MODULE P9_Statelessness ----------------------------
(***************************************************************************)
(* STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not    *)
(* adopted; the commit is the author's.                                    *)
(*                                                                         *)
(* PROBE — NON-DISCHARGING. Tessera Band 0, P9 (verification              *)
(* statelessness), the optional TLA+ probe commissioned by Amendment 4     *)
(* §A4.1. Asymmetric use rule (A4.1): a green result is NOT evidence and   *)
(* is not cited by any tracker row; a red result or an unrepresentable-    *)
(* attack finding is dispositioned before exit. P9's discharge path is     *)
(* [inspection + vector], unchanged by anything this module reports.       *)
(* Declaration and predictions: PROBE.md in this directory (frozen before  *)
(* the first run). Results: RESULTS-PROBE.md.                              *)
(*                                                                         *)
(* Registered claim (A1 §A1.2 P9): the verdict is a pure function of the   *)
(* bundle and the verifier's declared policy — no service-side state, no   *)
(* live network dependency, appears in the decision. Checkable form of     *)
(* §4.4's hard rule: an attestation must verify with the service dead.     *)
(*                                                                         *)
(* This module proves: nothing (probe tier). What it CHECKS: over one      *)
(* shared state machine — a bundle and policy fixed at Init, a service     *)
(* whose state changes freely, a Consult action any verifier kind may      *)
(* take, runs on one or two machines with machine-local memory — whether   *)
(* each verifier kind's recorded verdicts (i) equal the verdict computed   *)
(* from bundle and policy alone (Purity — the P9 invariant as              *)
(* commissioned) and (ii) equal one another (Agreement — the A4.1 vector's *)
(* first clause, oracle-free).                                             *)
(* This module does not check: the P4 partition (transcribed from          *)
(* P4_VerifierStates.tla, not re-checked); any adversary; bundle contents  *)
(* beyond per-check outcomes; temporal anchoring; wrapper self-containment *)
(* (P7); what a verifier does with a log feed.                             *)
(*                                                                         *)
(* The Verifier constant selects the decision rule. PURE is the correct    *)
(* verifier; the other three are broken companions, each stateful in a    *)
(* way the design forbids:                                                 *)
(*   PURE            Decide yields PureVerdict, consulted or not.          *)
(*   LIVE_FALLBACK   always consults; service says revoked => INVALID,     *)
(*                   else PureVerdict (silent fallback when unreachable).   *)
(*   LIVE_FAILCLOSED always consults; service unreachable => UNVERIFIABLE, *)
(*                   else PureVerdict (fail-closed on a dead service).      *)
(*   REPLAY_LATCH    this machine verified this bundle before => INVALID,  *)
(*                   else PureVerdict (verifier-local history; A3 §A3.1.1  *)
(*                   scopes replay to CALLER policy, so this is forbidden). *)
(* All four kinds share Init, StartRun, Consult, ServiceChange — the       *)
(* correct verifier is not stateless by construction of the state space;   *)
(* the consult path is reachable for it too (Sanity witnesses).            *)
(*                                                                         *)
(* Reading guide: `bundle` and `policy` are the vector's "same bundle and  *)
(* declared policy" and never change in a behavior. `service` is whatever  *)
(* live thing a verifier might touch (Tessera itself, a revocation status, *)
(* a live authority channel, a log). `view` is what Consult read. `seen`   *)
(* is per-machine memory. `verdicts` is the sequence of completed runs;    *)
(* each record carries the machine, the verdict, the service state at the  *)
(* moment of decision, and whether that run consulted.                     *)
(***************************************************************************)
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Checks,           \* the verifier's individual checks (abstract, as in P4)
  NonWaivable,      \* checks no policy may waive (A1.2.1)
  Machines,         \* verification machines (model values)
  ServiceStates,    \* subset of {"authorized","revoked","unreachable"} allowed in this config
  MaxRuns,          \* bound on completed runs per behavior
  RepeatOnMachine,  \* may a machine verify the same bundle twice?
  Verifier          \* "PURE" | "LIVE_FALLBACK" | "LIVE_FAILCLOSED" | "REPLAY_LATCH"

AllServiceStates == {"authorized", "revoked", "unreachable"}
VerifierKinds    == {"PURE", "LIVE_FALLBACK", "LIVE_FAILCLOSED", "REPLAY_LATCH"}

ASSUME NonWaivable \subseteq Checks
ASSUME ServiceStates \subseteq AllServiceStates /\ ServiceStates # {}
ASSUME MaxRuns \in Nat /\ MaxRuns >= 1
ASSUME RepeatOnMachine \in BOOLEAN
ASSUME Verifier \in VerifierKinds

Waivable == Checks \ NonWaivable
Statuses == {"pass", "fail", "unperformable"}
Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}

VARIABLES
  bundle,     \* [Checks -> Statuses]: the archived bundle, abstracted to check outcomes
  policy,     \* SUBSET Waivable: the declared policy (waived set; {} = strict)
  service,    \* the live service's current state
  phase,      \* "idle" | "running"
  machine,    \* machine of the run in progress (meaningful when phase = "running")
  consulted,  \* did the run in progress consult the service?
  view,       \* what it read ("none" if it did not)
  verdicts,   \* Seq of [m: Machines, v: Verdicts, svc: AllServiceStates, cons: BOOLEAN]
  seen        \* [Machines -> BOOLEAN]: machine-local memory of having verified this bundle

vars == <<bundle, policy, service, phase, machine, consulted, view, verdicts, seen>>

Runs == 1..Len(verdicts)

(***************************************************************************)
(* The verdict computed from bundle and policy ALONE — P4's VerdictFor,    *)
(* transcribed from formal/tla/P4_VerifierStates.tla (precedence ratified  *)
(* by A4 §A4.2). Nothing in this definition mentions service, view, or     *)
(* seen; that is the whole of what "pure" means here.                      *)
(***************************************************************************)
Required == Checks \ policy

PureVerdict ==
  IF \E c \in Required : bundle[c] = "fail"
    THEN "INVALID"
  ELSE IF \E c \in Required : bundle[c] = "unperformable"
    THEN "UNVERIFIABLE"
  ELSE IF policy = {}
    THEN "VALID_STRICT"
    ELSE "VALID_DEGRADED"

(* The decision rule of the selected verifier kind. Only PURE is P9's      *)
(* verifier; the other three are the companions PROBE.md declares.         *)
Rule ==
  CASE Verifier = "PURE"            -> PureVerdict
    [] Verifier = "LIVE_FALLBACK"   -> IF view = "revoked"     THEN "INVALID"      ELSE PureVerdict
    [] Verifier = "LIVE_FAILCLOSED" -> IF view = "unreachable" THEN "UNVERIFIABLE" ELSE PureVerdict
    [] Verifier = "REPLAY_LATCH"    -> IF seen[machine]        THEN "INVALID"      ELSE PureVerdict

(* The consulting companions consult on every run before deciding. PURE   *)
(* and REPLAY_LATCH may consult (the log feed) but need not.               *)
MustConsult == Verifier \in {"LIVE_FALLBACK", "LIVE_FAILCLOSED"}

(***************************************************************************)
(* Init: every bundle, every legal policy, every allowed service state.    *)
(***************************************************************************)
Init ==
  /\ bundle \in [Checks -> Statuses]
  /\ policy \in SUBSET Waivable
  /\ service \in ServiceStates
  /\ phase = "idle"
  /\ machine = CHOOSE m \in Machines : TRUE
  /\ consulted = FALSE
  /\ view = "none"
  /\ verdicts = <<>>
  /\ seen = [m \in Machines |-> FALSE]

(* A run begins on machine m. RepeatOnMachine = FALSE makes every machine  *)
(* fresh (the A4.1 vector's "two isolated machines").                       *)
StartRun(m) ==
  /\ phase = "idle"
  /\ Len(verdicts) < MaxRuns
  /\ RepeatOnMachine \/ ~seen[m]
  /\ phase' = "running"
  /\ machine' = m
  /\ consulted' = FALSE
  /\ view' = "none"
  /\ UNCHANGED <<bundle, policy, service, verdicts, seen>>

(* The run in progress reads the service. Available to EVERY verifier     *)
(* kind — in the design, the observability/log feed of A4 §A4.6 and       *)
(* coverage-map row 14, which "may feed a log and may never feed a         *)
(* verdict". P9 is about whether Decide uses what was read.                *)
Consult ==
  /\ phase = "running"
  /\ ~consulted
  /\ consulted' = TRUE
  /\ view' = service
  /\ UNCHANGED <<bundle, policy, service, phase, machine, verdicts, seen>>

(* The run in progress decides. The record keeps the service state at the *)
(* moment of decision and whether the run consulted, for the witnesses.   *)
Decide ==
  /\ phase = "running"
  /\ MustConsult => consulted
  /\ verdicts' = Append(verdicts,
                        [m |-> machine, v |-> Rule, svc |-> service, cons |-> consulted])
  /\ seen' = [seen EXCEPT ![machine] = TRUE]
  /\ phase' = "idle"
  /\ UNCHANGED <<bundle, policy, service, machine, consulted, view>>

(* The live service changes state at any time — between runs, or between  *)
(* a Consult and its Decide. With ServiceStates = {"unreachable"} this     *)
(* action is never enabled: the service is dead throughout (§4.4).         *)
ServiceChange ==
  /\ \E s \in ServiceStates \ {service} : service' = s
  /\ UNCHANGED <<bundle, policy, phase, machine, consulted, view, verdicts, seen>>

(* Stutter once no run can start, so a finished behavior is not reported  *)
(* as a deadlock (deadlock checking is left on as a bookkeeping check).    *)
Finished ==
  \/ Len(verdicts) = MaxRuns
  \/ \A m \in Machines : ~RepeatOnMachine /\ seen[m]

Done ==
  /\ phase = "idle"
  /\ Finished
  /\ UNCHANGED vars

Next ==
  \/ \E m \in Machines : StartRun(m)
  \/ Consult
  \/ Decide
  \/ ServiceChange
  \/ Done

Spec == Init /\ [][Next]_vars

(***************************************************************************)
(* Invariants.                                                             *)
(***************************************************************************)
TypeOK ==
  /\ bundle \in [Checks -> Statuses]
  /\ policy \subseteq Waivable
  /\ service \in ServiceStates
  /\ phase \in {"idle", "running"}
  /\ machine \in Machines
  /\ consulted \in BOOLEAN
  /\ view \in AllServiceStates \cup {"none"}
  /\ Len(verdicts) <= MaxRuns
  /\ \A i \in Runs : verdicts[i] \in
       [m: Machines, v: Verdicts, svc: AllServiceStates, cons: BOOLEAN]
  /\ seen \in [Machines -> BOOLEAN]

(* THE P9 INVARIANT AS COMMISSIONED (A4.1 probe): every verdict the       *)
(* verifier has produced equals the verdict computed from bundle and       *)
(* policy alone. Nothing about service, view, or seen on the right.        *)
Purity ==
  \A i \in Runs : verdicts[i].v = PureVerdict

(* THE A4.1 VECTOR, FIRST CLAUSE, oracle-free: all runs — on whatever     *)
(* machines, under whatever service history — agree with each other.       *)
Agreement ==
  \A i, j \in Runs : verdicts[i].v = verdicts[j].v

(***************************************************************************)
(* Sanity witnesses — used ONLY by the _Sanity cfgs (run with -continue),  *)
(* where TLC VIOLATING a witness is the healthy result (P4 pattern).       *)
(* Which must fire in which configuration is stated in PROBE.md Q2/Q6.     *)
(***************************************************************************)
NeverConsulted          == ~consulted
NeverDecidedDead        == \A i \in Runs : verdicts[i].svc # "unreachable"
NeverDecidedUnconsulted == \A i \in Runs : verdicts[i].cons
NeverDecidedConsulted   == \A i \in Runs : ~verdicts[i].cons
NeverAllRuns            == Len(verdicts) < MaxRuns
NeverTwoMachines        == \A i, j \in Runs : verdicts[i].m = verdicts[j].m
NeverRepeatMachine      == \A i, j \in Runs : i # j => verdicts[i].m # verdicts[j].m
NeverValidStrict        == \A i \in Runs : verdicts[i].v # "VALID_STRICT"

===================================================================================
