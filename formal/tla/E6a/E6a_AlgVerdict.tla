---------------------------- MODULE E6a_AlgVerdict ----------------------------
(***************************************************************************)
(* Tessera, exit item E6a: the P4 partition transition for an unknown     *)
(* algorithm, with dispatch, the mixed failed/unperformable case, and     *)
(* missing signature versus missing evidence.                             *)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(*                                                                         *)
(* Registered text: A3 §A3.6.2 item 2 (the verdict boundary) and item 3   *)
(* ("the formal model's P4-partition transition with a broken companion  *)
(* -- a verifier that fail-opens past an unknown algorithm must go red"); *)
(* A4 §A4.2 (FAIL over UNPERFORMABLE); A9 §A9.5 (dispatch); A9 C3         *)
(* (a missing signature fails). V1-PROFILE §3 and §15.7 for V1's codes.   *)
(*                                                                         *)
(* P4_VerifierStates.tla is NOT edited. It is instantiated (in E6a_Base)  *)
(* with the derived status map below; its VerdictFor decides every       *)
(* in-profile verdict. Run with -DTLA-Library=<repo>/formal/tla so SANY   *)
(* finds it.                                                               *)
(***************************************************************************)
EXTENDS E6a_Base

(* Classification of inputs into check outcomes -- the part E6a adds.     *)
AlgStatus(s) ==
  CASE alg[s] = "supported"   -> "pass"
    [] alg[s] = "unsupported" -> "unperformable"   \* the one UNVERIFIABLE case
    [] OTHER                  -> "fail"            \* A3.6.2 item 2's INVALID list

(* An absent signature is a codec failure whatever the algorithm (A9 C3; *)
(* conformance ALG-02). Signature semantics are performed only for the    *)
(* supported id; otherwise they are unperformable (blocked by the alg     *)
(* check, V1-PROFILE row 9.2 "(blocked: 7.1)").                           *)
SigStatus(s) ==
  IF sig[s] = "absent" THEN "fail"
  ELSE IF alg[s] # "supported" THEN "unperformable"
  ELSE IF sig[s] = "bad" THEN "fail"
  ELSE "pass"

(* An absent evidence member is unperformable, not a failure (A9 case d2; *)
(* V1-PROFILE row 2.2 MEMBER_MISSING).                                     *)
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
