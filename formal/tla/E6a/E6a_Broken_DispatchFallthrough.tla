-------------------- MODULE E6a_Broken_DispatchFallthrough --------------------
(***************************************************************************)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(* DELIBERATELY BROKEN companion of E6a_AlgVerdict. The status            *)
(* classification is the correct module's; only the lines marked BROKEN  *)
(* differ. Checked against the same E6a_Props formulas. It discharges    *)
(* nothing; it shows that the invariants can see this defect.            *)
(* DEFECT: dispatch is not terminal. An out-of-profile input is evaluated *)
(* as if it were in profile (a fallback or normalization, which           *)
(* V1-PROFILE §3.3 forbids), so it can come out VALID or INVALID.         *)
(* PREDICTED RED: DispatchTerminal; and the two formulas not conditioned *)
(* on dispatch = "in" that an evaluated out-of-profile input can break:   *)
(* AlgUnknownReasonExact (ALG_UNKNOWN reported for an out-of-profile      *)
(* input) and InvalidNeedsDefect (INVALID for an out-of-profile input).   *)
(* Every other formula is conditioned on dispatch = "in"; green.          *)
(* (Prediction revised once before any run of this module: the first    *)
(* draft said "DispatchTerminal only", which overlooked those two.)      *)
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

Verdict == P4VerdictOf(DerivedStatus)              \* BROKEN: no dispatch gate

Reason ==
  IF \E c \in Required : DerivedStatus[c] = "fail" THEN "FAILED"   \* BROKEN: no dispatch gate
  ELSE IF \E c \in Required \cap EvChecks : DerivedStatus[c] = "unperformable"
    THEN "MEMBER_MISSING"
  ELSE IF \E c \in Required \cap (AlgChecks \cup SigChecks) :
            DerivedStatus[c] = "unperformable"
    THEN "ALG_UNKNOWN"
  ELSE "OK"

INSTANCE E6a_Props WITH statusMap <- DerivedStatus,
                        verdictV  <- Verdict,
                        reasonV   <- Reason

=============================================================================
