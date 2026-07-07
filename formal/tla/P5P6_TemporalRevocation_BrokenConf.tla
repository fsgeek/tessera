----------------- MODULE P5P6_TemporalRevocation_BrokenConf -----------------
(***************************************************************************)
(* Tessera Band 0 — P5 DELIBERATELY BROKEN: the PRE-AMENDMENT-2 verifier. *)
(* This verifier checks the anchor block time against the window and      *)
(* nothing else — exactly the acceptance predicate as registered before   *)
(* A2.2 added the confirmation-timing conjunct. It therefore ACCEPTS the  *)
(* abandoned-anchor artifact of A2.0: a discarded issuance attempt whose  *)
(* anchor landed in-window but buried past the window, whose transaction  *)
(* confirmed anyway, paired with the never-shipped receipt.                *)
(*                                                                          *)
(* THE POINT OF THIS MODULE (the A2.0 correction, made mechanical): the   *)
(* artifact is NOT a forgery — every anchor-only invariant PASSES here.   *)
(* ForgeryRejected holds (the anchor still bounds signing), and           *)
(* ReceiptIndependence holds (receipt tolerances are still ignored).      *)
(* Only AbandonedArtifactRejected — the invariant born from the A2.2      *)
(* conjunct — is VIOLATED. Expected result: TLC green on ForgeryRejected  *)
(* and ReceiptIndependence, VIOLATING AbandonedArtifactRejected with a    *)
(* concrete artifact (anchor in-window, confirmedAt past it, accepted).   *)
(* A green run on all three would mean the new conjunct is decorative.    *)
(*                                                                          *)
(* (The main module's extended WindowRespected / VerifierOwnsTolerances   *)
(* contain the confirmedAt clause and would flag here too; they are       *)
(* omitted from the cfg so the report names the most specific catcher,    *)
(* per the sanity-ordering working rule.)                                  *)
(* State space and variables match the correct module exactly; only the   *)
(* missing conjunct differs.                                                *)
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

(* BROKEN: the A2.2 confirmation-timing conjunct is MISSING — the         *)
(* verifier as registered before Amendment 2.                              *)
TemporalOKWith(rd, re) ==
  /\ anchor >= declared - polEps
  /\ anchor <= declared + polDelta

AuthorizedThroughWindow ==
  /\ revoked > declared
  /\ revoked > anchor

StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow

StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)

(* Anchor-only invariants from the correct module. EXPECTED: BOTH HOLD —  *)
(* the artifact is not a forgery and involves no receipt tolerance.        *)
ForgeryRejected ==
  (revoked <= signed) => ~StrictAccept

ReceiptIndependence ==
  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    StrictAcceptWith(rd, re) <=> StrictAccept

(* The Amendment 2 invariant. EXPECTED: VIOLATED — the counterexample IS  *)
(* the abandoned-anchor artifact.                                           *)
AbandonedArtifactRejected ==
  (/\ anchor >= declared - polEps
   /\ anchor <= declared + polDelta
   /\ confirmedAt > declared + polDelta)
  => ~StrictAccept

==============================================================================
