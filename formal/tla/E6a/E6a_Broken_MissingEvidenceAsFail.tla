-------------------- MODULE E6a_Broken_MissingEvidenceAsFail --------------------
(***************************************************************************)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(* DELIBERATELY BROKEN companion of E6a_AlgVerdict. It differs from the   *)
(* correct module ONLY at the line marked BROKEN. It is checked against   *)
(* the same E6a_Props formulas. It discharges nothing; it shows that the  *)
(* invariants can see this defect.                                        *)
(* DEFECT: a missing evidence member is treated as a failure (INVALID)   *)
(* instead of unperformable -- the other direction of the same lumping.  *)
(* PREDICTED RED: UnknownAlgGivesUnverifiable, MissingEvidenceUnverifiable, *)
(* InvalidNeedsDefect, ExactInvalidIn, ExactUnverifiableIn.               *)
(* PREDICTED GREEN: group F.                                              *)
(***************************************************************************)
EXTENDS E6a_Base

AlgStatus(s) ==
  CASE alg[s] = "supported"   -> "pass"
    [] alg[s] = "unsupported" -> "unperformable"
    [] OTHER                  -> "fail"

SigStatus(s) ==
  IF sig[s] = "absent" THEN "fail"
  ELSE IF alg[s] # "supported" THEN "unperformable"
  ELSE IF sig[s] = "bad" THEN "fail"
  ELSE "pass"

EvStatus(e) ==
  CASE ev[e] = "absent" -> "fail"                 \* BROKEN: absence treated as failure
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
