------------------- MODULE P5P6_TemporalRevocation_BrokenTol -------------------
(***************************************************************************)
(* Tessera Band 0 — P5 DELIBERATELY BROKEN: receipt-controlled            *)
(* tolerances. The implementation bug A1.2 P5 forbids: the verifier       *)
(* honors the LARGER of its own tolerance and the receipt-declared one    *)
(* ("the receipt says 96 hours is fine, so 96 hours is fine"). A          *)
(* malicious issuer writes an enormous window into the receipt and the    *)
(* temporal guarantee dissolves.                                            *)
(*                                                                          *)
(* Expected result: TLC VIOLATES VerifierOwnsTolerances — exhibiting an   *)
(* acceptance whose anchor-to-declared gap exceeds the strict maxima,     *)
(* enabled by an oversized rcptDelta/rcptEps. A green run would mean the  *)
(* invariant cannot detect receipt-controlled enlargement.                  *)
(* State space and variables match the correct module exactly; only the   *)
(* effective-tolerance computation differs.                                 *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax

ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax

NoRev == MaxTime + 1

VARIABLES declared, signed, anchor, revoked,
          polDelta, polEps, rcptDelta, rcptEps

Init ==
  /\ declared  \in 0..MaxTime
  /\ anchor    \in 0..MaxTime
  /\ signed    \in 0..anchor
  /\ revoked   \in 0..MaxTime \cup {NoRev}
  /\ polDelta  \in 0..DeltaMax
  /\ polEps    \in 0..EpsilonMax
  /\ rcptDelta \in 0..RcptTolMax
  /\ rcptEps   \in 0..RcptTolMax

Next == UNCHANGED <<declared, signed, anchor, revoked,
                    polDelta, polEps, rcptDelta, rcptEps>>

Max(a, b) == IF a > b THEN a ELSE b

(* BROKEN: effective tolerances honor receipt-declared enlargement.       *)
(* Parameterized shape matches the correct module (apples-to-apples).      *)
TemporalOKWith(rd, re) ==
  /\ anchor >= declared - Max(polEps, re)
  /\ anchor <= declared + Max(polDelta, rd)

AuthorizedThroughWindow ==
  /\ revoked > declared
  /\ revoked > anchor

StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow

StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)

(* Same invariant as the correct module. EXPECTED: VIOLATED.              *)
VerifierOwnsTolerances ==
  StrictAccept =>
    (anchor - declared <= DeltaMax /\ declared - anchor <= EpsilonMax)

=================================================================================
