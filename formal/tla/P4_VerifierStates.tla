---------------------------- MODULE P4_VerifierStates ----------------------------
(***************************************************************************)
(* Tessera Band 0 — P4: fail-closed verifier state logic.                 *)
(* Authoritative property statements: Amendment 1 §A1.2 (P4) and §A1.2.1  *)
(* (the waiver lattice). This module is the machine-checkable form.       *)
(*                                                                         *)
(* The verifier's verdict over a bundle is a pure function (P9) of the     *)
(* per-check outcomes and the verifier's declared policy. TLC exhaustively *)
(* enumerates every combination of check outcomes and every policy, and   *)
(* checks the A1.2/A1.2.1 invariants over all of them. There is no        *)
(* temporal behavior here — evaluation is instantaneous — so the "state   *)
(* machine" is degenerate: all the content is in the Init enumeration and *)
(* the invariants.                                                         *)
(*                                                                         *)
(* Reading guide (Tony): Checks is an abstract set of the verifier's      *)
(* individual checks (signature-verifies, manifest-evidence-validates,    *)
(* temporal-consistency, ...). NonWaivable \subseteq Checks per A1.2.1.   *)
(* `status` assigns each check pass/fail/unperformable; `waived` is the   *)
(* verifier's declared policy (the waived subset; {} = strict). The       *)
(* companion P4_VerifierStates_Broken module implements the classic       *)
(* fail-open bug and TLC produces the violating assignment.               *)
(***************************************************************************)
EXTENDS FiniteSets

CONSTANTS Checks, NonWaivable

ASSUME NonWaivable \subseteq Checks

Waivable == Checks \ NonWaivable

Statuses == {"pass", "fail", "unperformable"}

Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}

VARIABLES status, waived

(* Every combination of check outcomes and every legal policy. A1.2.1:   *)
(* only Waivable checks may appear in a waiver set — a policy naming a    *)
(* non-waivable check is not a legal policy at all.                       *)
Init ==
  /\ status \in [Checks -> Statuses]
  /\ waived \in SUBSET Waivable

Next == UNCHANGED <<status, waived>>

(***************************************************************************)
(* The verdict function, parameterized by the waiver set W so that the    *)
(* monotonicity invariant can quantify over ALL policies for one status   *)
(* assignment. Precedence decision (surfaced by this model, for author    *)
(* ratification): when one required check FAILS and another is            *)
(* UNPERFORMABLE, the verdict is INVALID — a definitive failure is        *)
(* stronger evidence than an open question, and both are fail-closed.     *)
(***************************************************************************)
RequiredUnder(W) == Checks \ W

VerdictFor(W) ==
  IF \E c \in RequiredUnder(W) : status[c] = "fail"
    THEN "INVALID"
  ELSE IF \E c \in RequiredUnder(W) : status[c] = "unperformable"
    THEN "UNVERIFIABLE"
  ELSE IF W = {}
    THEN "VALID_STRICT"
    ELSE "VALID_DEGRADED"

Verdict == VerdictFor(waived)

(***************************************************************************)
(* Invariants — each maps to a clause of A1.2 P4 / A1.2.1.                *)
(***************************************************************************)

(* P4: the four states partition all outcomes (totality; never a bare     *)
(* boolean, never a fifth state).                                          *)
Partition == Verdict \in Verdicts

(* A1.2.1 monotonicity: a failed non-waivable check is INVALID under      *)
(* EVERY policy — no waiver set may promote it.                            *)
Monotonicity ==
  (\E c \in NonWaivable : status[c] = "fail") =>
    \A W \in SUBSET Waivable : VerdictFor(W) = "INVALID"

(* A1.2.1: an unperformable non-waivable check never yields any VALID     *)
(* state, under any policy. (INVALID is permitted: some other required    *)
(* check may have definitively failed.)                                    *)
NoSilentPromotion ==
  (\E c \in NonWaivable : status[c] = "unperformable") =>
    \A W \in SUBSET Waivable :
      VerdictFor(W) \in {"INVALID", "UNVERIFIABLE"}

(* P1-facing corollary: any VALID verdict means every non-waivable check  *)
(* was performed and passed.                                               *)
ValidNeedsNonWaivablePass ==
  (Verdict \in {"VALID_STRICT", "VALID_DEGRADED"}) =>
    \A c \in NonWaivable : status[c] = "pass"

(* P4/§3.1: VALID_STRICT is the fail-closed default — every check, not    *)
(* just the required ones, performed and passed.                           *)
StrictMeansEverything ==
  Verdict = "VALID_STRICT" => \A c \in Checks : status[c] = "pass"

(* A1.2.1: VALID_DEGRADED only arises from an explicit, nonempty waiver   *)
(* within the waivable set — never as a default.                           *)
DegradedNeedsExplicitWaiver ==
  Verdict = "VALID_DEGRADED" => (waived # {} /\ waived \subseteq Waivable)

(* UNVERIFIABLE is honest: it arises only when some required check truly  *)
(* could not be performed (and none failed).                               *)
UnverifiableIsHonest ==
  Verdict = "UNVERIFIABLE" =>
    /\ \E c \in RequiredUnder(waived) : status[c] = "unperformable"
    /\ \A c \in RequiredUnder(waived) : status[c] # "fail"

(***************************************************************************)
(* Vacuity checks — used ONLY by the _Sanity cfg (run with TLC -continue), *)
(* where TLC VIOLATING all four is the healthy result: each verdict is    *)
(* reachable under the correct verdict function, so the implication-      *)
(* shaped invariants above are not vacuously true. If VerdictFor had a    *)
(* bug making any verdict unsatisfiable, its invariants would pass        *)
(* vacuously — these witnesses close that hole.                            *)
(***************************************************************************)
VerdictNeverStrict       == Verdict # "VALID_STRICT"
VerdictNeverDegraded     == Verdict # "VALID_DEGRADED"
VerdictNeverInvalid      == Verdict # "INVALID"
VerdictNeverUnverifiable == Verdict # "UNVERIFIABLE"

===================================================================================
