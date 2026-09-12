------------------------- MODULE P4_VerifierStates_Broken -------------------------
(***************************************************************************)
(* Tessera Band 0 — P4, DELIBERATELY BROKEN: the classic fail-open bug.   *)
(* An unperformable check is silently treated as if it passed ("we        *)
(* couldn't reach the trust root, assume it's fine") — precisely the      *)
(* promotion of UNVERIFIABLE toward VALID that P4 forbids and §4.6 calls  *)
(* the place fail-open bugs hide.                                          *)
(*                                                                         *)
(* Expected: TLC REPORTS AN INVARIANT VIOLATION (NoSilentPromotion, or    *)
(* StrictMeansEverything) with the concrete status/policy assignment as   *)
(* the counterexample. A green run of this module would mean the          *)
(* invariants are vacuous.                                                 *)
(***************************************************************************)
EXTENDS FiniteSets

CONSTANTS Checks, NonWaivable

ASSUME NonWaivable \subseteq Checks

Waivable == Checks \ NonWaivable

Statuses == {"pass", "fail", "unperformable"}

Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}

VARIABLES status, waived

Init ==
  /\ status \in [Checks -> Statuses]
  /\ waived \in SUBSET Waivable

Next == UNCHANGED <<status, waived>>

RequiredUnder(W) == Checks \ W

(* BROKEN: no unperformable clause — a check that cannot be performed is  *)
(* skipped, i.e. treated as pass. Fail-open.                               *)
VerdictFor(W) ==
  IF \E c \in RequiredUnder(W) : status[c] = "fail"
    THEN "INVALID"
  ELSE IF W = {}
    THEN "VALID_STRICT"
    ELSE "VALID_DEGRADED"

Verdict == VerdictFor(waived)

(* Same invariants as the correct module. *)
(* CORRECTION 2026-09-06 (review item 5): the FIRST SEVEN of the correct    *)
(* module's eleven. The four exact-classification formulas (ExactInvalid,   *)
(* ExactUnverifiable, ExactStrict, ExactDegraded) are not carried here, and *)
(* P4_VerifierStates.cfg checks all eleven. Of the seven,                   *)
(* UnverifiableIsHonest is vacuous in this module (the broken VerdictFor    *)
(* never returns UNVERIFIABLE). The _Green cfg (2026-09-06) records which   *)
(* of the seven the fail-open defect turns red; see                         *)
(* falsification-2026-09-06/FIXES-2026-09-06.md.                            *)
Partition == Verdict \in Verdicts

Monotonicity ==
  (\E c \in NonWaivable : status[c] = "fail") =>
    \A W \in SUBSET Waivable : VerdictFor(W) = "INVALID"

NoSilentPromotion ==
  (\E c \in NonWaivable : status[c] = "unperformable") =>
    \A W \in SUBSET Waivable :
      VerdictFor(W) \in {"INVALID", "UNVERIFIABLE"}

ValidNeedsNonWaivablePass ==
  (Verdict \in {"VALID_STRICT", "VALID_DEGRADED"}) =>
    \A c \in NonWaivable : status[c] = "pass"

StrictMeansEverything ==
  Verdict = "VALID_STRICT" => \A c \in Checks : status[c] = "pass"

DegradedNeedsExplicitWaiver ==
  Verdict = "VALID_DEGRADED" => (waived # {} /\ waived \subseteq Waivable)

UnverifiableIsHonest ==
  Verdict = "UNVERIFIABLE" =>
    /\ \E c \in RequiredUnder(waived) : status[c] = "unperformable"
    /\ \A c \in RequiredUnder(waived) : status[c] # "fail"

===================================================================================
