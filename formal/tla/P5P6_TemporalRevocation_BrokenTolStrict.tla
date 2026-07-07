---------------- MODULE P5P6_TemporalRevocation_BrokenTolStrict ----------------
(***************************************************************************)
(* Tessera Band 0 — P5 DELIBERATELY BROKEN, the SUBTLE variant:           *)
(* receipt-NARROWED tolerances. The implementation honors the SMALLER of  *)
(* the verifier's tolerance and the receipt-declared one ("the receipt    *)
(* only asks for a tighter window — surely stricter is safe?").            *)
(*                                                                          *)
(* Why this is a real bug and not extra safety: it hands the ISSUER       *)
(* control over verification outcomes. An issuer can craft a receipt      *)
(* that verifies for parties checking promptly but fails for anyone      *)
(* whose anchor-to-declared gap exceeds the receipt's narrowed window —   *)
(* issuer-selected verdict manipulation, violating "delta and epsilon     *)
(* belong to the verifier" (A1.2 P5) just as surely as enlargement does.  *)
(*                                                                          *)
(* THE POINT OF THIS MODULE: every pure safety invariant PASSES here —    *)
(* VerifierOwnsTolerances holds (narrowed acceptance is still inside the  *)
(* maxima), WindowRespected holds, ForgeryRejected holds. Only            *)
(* ReceiptIndependence catches it. Expected result: TLC green on all     *)
(* safety invariants, VIOLATING ReceiptIndependence — proving that        *)
(* invariant is load-bearing, not decorative.                              *)
(* Identical state space; only the effective-tolerance computation        *)
(* differs.                                                                 *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax

ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax

NoRev == MaxTime + 1

VARIABLES declared, signed, anchor, confirmedAt, revoked,
          polDelta, polEps, rcptDelta, rcptEps

Init ==
  /\ declared  \in 0..MaxTime
  /\ anchor    \in 0..MaxTime
  /\ confirmedAt \in 0..MaxTime
  /\ signed    \in 0..anchor
  /\ revoked   \in 0..MaxTime \cup {NoRev}
  /\ polDelta  \in 0..DeltaMax
  /\ polEps    \in 0..EpsilonMax
  /\ rcptDelta \in 0..RcptTolMax
  /\ rcptEps   \in 0..RcptTolMax

Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
                    polDelta, polEps, rcptDelta, rcptEps>>

Min(a, b) == IF a < b THEN a ELSE b

(* BROKEN: effective tolerances honor receipt-declared NARROWING — in     *)
(* every conjunct, including the A2.2 confirmation-timing one.             *)
TemporalOKWith(rd, re) ==
  /\ anchor >= declared - Min(polEps, re)
  /\ anchor <= declared + Min(polDelta, rd)
  /\ confirmedAt <= declared + Min(polDelta, rd)

AuthorizedThroughWindow ==
  /\ revoked > declared
  /\ revoked > anchor

StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow

StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)

(* Safety invariants from the correct module. EXPECTED: ALL HOLD — the    *)
(* narrowing bug is invisible to them.                                      *)
ForgeryRejected ==
  (revoked <= signed) => ~StrictAccept

WindowRespected ==
  StrictAccept => (/\ anchor - declared <= polDelta
                   /\ declared - anchor <= polEps
                   /\ confirmedAt - declared <= polDelta)

VerifierOwnsTolerances ==
  StrictAccept =>
    (/\ anchor - declared <= DeltaMax
     /\ declared - anchor <= EpsilonMax
     /\ confirmedAt - declared <= DeltaMax)

(* Independence invariant from the correct module. EXPECTED: VIOLATED —   *)
(* the verdict now varies with the receipt-declared tolerances.            *)
ReceiptIndependence ==
  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    StrictAcceptWith(rd, re) <=> StrictAccept

=================================================================================
