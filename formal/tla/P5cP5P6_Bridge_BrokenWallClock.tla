--------------------- MODULE P5cP5P6_Bridge_BrokenWallClock ---------------------
(***************************************************************************)
(* Bridge companion, DELIBERATELY BROKEN: the issuer ships on P5c's       *)
(* literal fused-clock rule transplanted to decoupled clocks — depth      *)
(* reached AND wall clock within the window ("now <= declared + Delta"),  *)
(* no chain-timestamp conjunct at all. Under the single-clock             *)
(* abstraction this rule IS the chain-time predicate (P5c's header says   *)
(* so, correctly); under real, skewed, non-monotonic block timestamps    *)
(* it is not.                                                              *)
(*                                                                          *)
(* Expected result: HonestShipAccepted RED — a skewed block timestamp     *)
(* puts the shipped receipt outside the verifier's window (anchor-time    *)
(* or confirmation conjunct) while the wall clock was still in-window.    *)
(* This mechanically discharges A2.1's rationale paragraph ("why chain    *)
(* time on both sides"): the divergence it names is exhibited, and the    *)
(* fusion in P5c is shown to be load-bearing, not cosmetic.               *)
(* The _Green cfg (PinAgreement, ShippedDesignatedAgree,                  *)
(* LateBurialRejected) must pass: the verifier side is untouched.          *)
(* Identical to P5cP5P6_Bridge except Ship's guard.                        *)
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

VerifierDesignatedH(h) == h + KConf - 1
VerifierConfirmedTs(h) == chain[VerifierDesignatedH(h)]

VerdictValid(d, h) ==
  /\ d - Epsilon <= chain[h]
  /\ chain[h] <= d + Delta
  /\ VerifierConfirmedTs(h) <= d + Delta

(* THE BREAK: wall-clock ship rule — P5c's fused-clock guard, transplanted. *)
Ship ==
  /\ ~shipped /\ anchorH # NoAnchor
  /\ Len(chain) >= IssuerDesignatedH
  /\ now <= declared + Delta
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
   /\ Len(chain) >= VerifierDesignatedH(anchorH)
   /\ VerifierConfirmedTs(anchorH) > declared + Delta)
  => ~VerdictValid(declared, anchorH)

================================================================================
