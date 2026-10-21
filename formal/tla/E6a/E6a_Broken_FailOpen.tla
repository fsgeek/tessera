-------------------- MODULE E6a_Broken_FailOpen --------------------
(***************************************************************************)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(* DELIBERATELY BROKEN companion of E6a_AlgVerdict. It differs from the   *)
(* correct module ONLY at the line marked BROKEN. It is checked against   *)
(* the same E6a_Props formulas. It discharges nothing; it shows that the  *)
(* invariants can see this defect.                                        *)
(* DEFECT (A3 §A3.6.2 item 3, the registered companion): the verifier    *)
(* fails open past an unknown algorithm. An unsupported id is treated as  *)
(* if it passed, and the slot's opaque signature is accepted unchecked.   *)
(* PREDICTED RED (V1 cfg, written before running): UnknownAlgGivesUnverifiable, *)
(* UnknownAlgNeverValid, AlgUnknownReasonExact, ExactUnverifiableIn,      *)
(* ExactStrictIn. General cfg: those plus ExactDegradedIn. PREDICTED      *)
(* GREEN: every group F formula (P4 alone cannot see this defect).        *)
(***************************************************************************)
EXTENDS E6a_Base

AlgStatus(s) ==
  CASE alg[s] = "supported"   -> "pass"
    [] alg[s] = "unsupported" -> "pass"            \* BROKEN: fail-open
    [] OTHER                  -> "fail"

SigStatus(s) ==
  IF sig[s] = "absent" THEN "fail"
  ELSE IF alg[s] = "unsupported" THEN "pass"       \* BROKEN: opaque signature accepted
  ELSE IF alg[s] # "supported" THEN "unperformable"
  ELSE IF sig[s] = "bad" THEN "fail"
  ELSE "pass"

EvStatus(e) ==
  CASE ev[e] = "absent" -> "unperformable"
    [] ev[e] = "bad"    -> "fail"
    [] ev[e] = "good"   -> "pass"

DerivedStatus ==
  [c \in AllChecks |->
     CASE c[1] = "alg" -> AlgStatus(c[2])
       [] c[1] = "sig" -> SigStatus(c[2])
       [] c[1] = "ev"  -> EvStatus(c[2])]

Verdict == VerdictFrom(DerivedStatus)
Reason  == ReasonFrom(DerivedStatus)

INSTANCE E6a_Props WITH statusMap <- DerivedStatus,
                        verdictV  <- Verdict,
                        reasonV   <- Reason

=============================================================================
