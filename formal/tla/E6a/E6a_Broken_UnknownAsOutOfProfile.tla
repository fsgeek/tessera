-------------------- MODULE E6a_Broken_UnknownAsOutOfProfile --------------------
(***************************************************************************)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(* DELIBERATELY BROKEN companion of E6a_AlgVerdict. The status            *)
(* classification is the correct module's; only the lines marked BROKEN  *)
(* differ. Checked against the same E6a_Props formulas. It discharges    *)
(* nothing; it shows that the invariants can see this defect.            *)
(* DEFECT: an in-profile unknown algorithm is handled as a dispatch       *)
(* rejection -- terminal OUT_OF_PROFILE, nothing else evaluated. (A9.5:   *)
(* dispatch is the only place OUT_OF_PROFILE arises; an unknown alg is an *)
(* in-profile outcome, V1-PROFILE §3.1 item 5.)                           *)
(* PREDICTED RED: OutOfProfileOnlyAtDispatch, InvalidAlgFormsGiveInvalid, *)
(* KnownAlgBadSigInvalid, AlgUnknownReasonExact,                          *)
(* MixedFailedUnknownInvalid, MixedFailedMissingEvidenceInvalid,          *)
(* MissingSignatureInvalid, MissingEvidenceUnverifiable, ExactInvalidIn,  *)
(* ExactUnverifiableIn, AgreesWithP4. PREDICTED GREEN: the P4_* formulas. *)
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
  CASE ev[e] = "absent" -> "unperformable"
    [] ev[e] = "bad"    -> "fail"
    [] ev[e] = "good"   -> "pass"

DerivedStatus ==
  [c \in AllChecks |->
     CASE c[1] = "alg" -> AlgStatus(c[2])
       [] c[1] = "sig" -> SigStatus(c[2])
       [] c[1] = "ev"  -> EvStatus(c[2])]

HasUnknown == \E s \in Slots : alg[s] = "unsupported"

Verdict ==
  IF dispatch = "out" THEN "UNVERIFIABLE"
  ELSE IF HasUnknown THEN "UNVERIFIABLE"           \* BROKEN: terminal, as if at dispatch
  ELSE VerdictFrom(DerivedStatus)

Reason ==
  IF dispatch = "out" THEN "OUT_OF_PROFILE"
  ELSE IF HasUnknown THEN "OUT_OF_PROFILE"         \* BROKEN
  ELSE ReasonFrom(DerivedStatus)

INSTANCE E6a_Props WITH statusMap <- DerivedStatus,
                        verdictV  <- Verdict,
                        reasonV   <- Reason

=============================================================================
