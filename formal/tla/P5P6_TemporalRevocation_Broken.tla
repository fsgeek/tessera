--------------------- MODULE P5P6_TemporalRevocation_Broken ---------------------
(***************************************************************************)
(* Tessera Band 0 — P6 DELIBERATELY BROKEN: point-evaluated authorization. *)
(* This is P6 exactly as it stood after review round 1 — authorization    *)
(* checked only at declared_issue_time — the weakness GPT-5.5's round-2   *)
(* review found by hand. The model reproduces that attack mechanically:   *)
(* expected result is TLC VIOLATING ForgeryRejected with the concrete     *)
(* assignment (declared just before revocation, signed at/after it,       *)
(* anchor still inside the delta window).                                   *)
(*                                                                          *)
(* A green run of this module would mean the security invariant is        *)
(* vacuous. State space and variables match the correct module exactly    *)
(* (apples-to-apples); only AuthorizedPointOnly differs.                    *)
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

TemporalOK ==
  /\ anchor >= declared - polEps
  /\ anchor <= declared + polDelta

(* BROKEN: authorization evaluated at the declared time ONLY — the        *)
(* anchor-window clause is missing.                                        *)
AuthorizedPointOnly == revoked > declared

StrictAccept == TemporalOK /\ AuthorizedPointOnly

(* Same security theorem as the correct module. EXPECTED: VIOLATED.       *)
ForgeryRejected ==
  (revoked <= signed) => ~StrictAccept

=================================================================================
