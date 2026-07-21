--------------------- MODULE P5cP5P6_Bridge_BrokenAnchorSubst ---------------------
(***************************************************************************)
(* Bridge companion, DELIBERATELY BROKEN — the obligated one: the         *)
(* verifier SUBSTITUTES the anchor (inclusion-block) timestamp for the    *)
(* k-th-confirmation timestamp. This is the 2026-07-18 alarm made         *)
(* mechanical: a verifier that cannot see WHICH block granted the k-th    *)
(* confirmation, only a number it treats as confirmedAt — here, the       *)
(* wrong number (anchorAt).                                                *)
(*                                                                          *)
(* Expected result (TLC -continue): TWO invariants red, two faces of the  *)
(* one defect —                                                            *)
(* - ShippedDesignatedAgree: issuer evaluated block h+DepthK, verifier    *)
(*   reads block h.                                                        *)
(* - LateBurialRejected: an abandoned artifact whose TRUE k-th            *)
(*   confirmation is late but whose anchor timestamp is in-window is      *)
(*   ACCEPTED — the burial delay vanishes in the handoff, exactly the     *)
(*   narrowed alarm.                                                       *)
(* The _Green cfg (PinAgreement, HonestShipAccepted) must pass: the       *)
(* substitution accepts MORE, never less, so honest receipts still        *)
(* verify — which is precisely why this defect is invisible to the        *)
(* happy path and needs the abandoned-artifact tripwire.                   *)
(* NOTE the invariants below keep their antecedents on the TRUE           *)
(* k-th-confirmation quantity (TrueConfirmedTs); only the verifier's      *)
(* derivation is broken. Substituting inside the antecedent too would     *)
(* quietly redefine "late burial" and the invariant would pass — the      *)
(* same seam-burial this companion exists to expose.                       *)
(* Identical to P5cP5P6_Bridge except VerifierDesignatedH /               *)
(* VerifierConfirmedTs.                                                    *)
(***************************************************************************)
EXTENDS Integers, Sequences

CONSTANTS MaxTime, Delta, Epsilon, KConf, DepthK, MaxSkew, MaxBlocks

ASSUME /\ Delta \in Nat /\ Epsilon \in Nat /\ MaxTime \in Nat
       /\ KConf \in Nat \ {0} /\ DepthK \in Nat \ {0}
       /\ MaxSkew \in Nat /\ MaxBlocks \in Nat \ {0}

NoAnchor == -1
NoTime   == -1

VARIABLES now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall

vars == <<now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall>>

BlockTimestamps == {t \in 0..(MaxTime + MaxSkew) :
                      t >= now - MaxSkew /\ t <= now + MaxSkew}

Init ==
  /\ now = 0 /\ chain = <<>>
  /\ declared = NoTime /\ anchorH = NoAnchor /\ pendingAnchor = FALSE
  /\ shipped = FALSE /\ shipAtWall = NoTime

Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ UNCHANGED <<chain, declared, anchorH, pendingAnchor, shipped, shipAtWall>>

NewBlock ==
  /\ Len(chain) < MaxBlocks
  /\ \E ts \in BlockTimestamps :
       chain' = Append(chain, ts)
  /\ anchorH' = IF pendingAnchor THEN Len(chain) + 1 ELSE anchorH
  /\ pendingAnchor' = FALSE
  /\ UNCHANGED <<now, declared, shipped, shipAtWall>>

Declare ==
  /\ declared = NoTime
  /\ declared' = now
  /\ UNCHANGED <<now, chain, anchorH, pendingAnchor, shipped, shipAtWall>>

AnchorNext ==
  /\ declared # NoTime /\ anchorH = NoAnchor /\ ~pendingAnchor
  /\ pendingAnchor' = TRUE
  /\ UNCHANGED <<now, chain, declared, anchorH, shipped, shipAtWall>>

IssuerDesignatedH == anchorH + DepthK
IssuerConfirmedTs == chain[IssuerDesignatedH]

(* THE BREAK: the verifier reads the inclusion block.                      *)
VerifierDesignatedH(h) == h
VerifierConfirmedTs(h) == chain[h]

(* The true quantity, for the invariants' antecedents only.                *)
TrueDesignatedH(h) == h + KConf - 1
TrueConfirmedTs(h) == chain[TrueDesignatedH(h)]

VerdictValid(d, h) ==
  /\ d - Epsilon <= chain[h]
  /\ chain[h] <= d + Delta
  /\ VerifierConfirmedTs(h) <= d + Delta

(* Ship unchanged: the honest issuer still evaluates the full strict      *)
(* predicate on the true quantities.                                       *)
Ship ==
  /\ ~shipped /\ anchorH # NoAnchor
  /\ Len(chain) >= IssuerDesignatedH
  /\ declared - Epsilon <= chain[anchorH]
  /\ chain[anchorH] <= declared + Delta
  /\ IssuerConfirmedTs <= declared + Delta
  /\ shipped' = TRUE /\ shipAtWall' = now
  /\ UNCHANGED <<now, chain, declared, anchorH, pendingAnchor>>

Next == Tick \/ NewBlock \/ Declare \/ AnchorNext \/ Ship

PinAgreement == DepthK = KConf - 1

ShippedDesignatedAgree ==
  shipped =>
    /\ IssuerDesignatedH = VerifierDesignatedH(anchorH)
    /\ IssuerConfirmedTs = VerifierConfirmedTs(anchorH)

HonestShipAccepted ==
  shipped => VerdictValid(declared, anchorH)

LateBurialRejected ==
  (/\ anchorH # NoAnchor /\ ~shipped
   /\ Len(chain) >= TrueDesignatedH(anchorH)
   /\ TrueConfirmedTs(anchorH) > declared + Delta)
  => ~VerdictValid(declared, anchorH)

================================================================================
