------------------------- MODULE P5cP5P6_BridgeSlack_Latch -------------------------
(***************************************************************************)
(* Latch variant of the slack analysis (P5cP5P6_BridgeSlack.tla) —        *)
(* non-author bench contract, Codex constraint 1 (2026-07-21): "the       *)
(* lifecycle decision must use — or atomically latch — B [the wall time   *)
(* eligibility is reached], not the eventual execution time of Ship,"     *)
(* else the interleaving scheduler can manufacture expiry despite         *)
(* sufficient slack — a modeling artifact, not the clock question.        *)
(*                                                                          *)
(* ONE-CONJUNCT DIFFERENCE from P5cP5P6_BridgeSlack: Ship's lifecycle     *)
(* guard is `burialAtWall <= declared + Delta + Slack` (timeliness        *)
(* latched at the eligibility instant B) instead of                        *)
(* `now <= declared + Delta + Slack` (checked at execution). Under latch  *)
(* semantics an attempt whose eligibility arrived inside the envelope     *)
(* may ship at ANY later wall time — the scheduler cannot expire it —     *)
(* and discard semantics are ruled by B alone. The base module's          *)
(* analysis invariant (defined on B) is carried UNCHANGED and was never   *)
(* exposed to the artifact; what this variant adds to the checked space   *)
(* is the shipped states the execution-time guard excluded (ship after    *)
(* the wall envelope with timely eligibility — the PostEnvelopeShip       *)
(* sanity witness).                                                        *)
(*                                                                          *)
(* Everything else — constants, actions, transcriptions, the L-as-        *)
(* declared-assumption CORRECTION — is the base module's; see its header.  *)
(***************************************************************************)
EXTENDS Integers, Sequences

CONSTANTS MaxTime, Delta, Epsilon, KConf, DepthK, MaxSkew, MaxBlocks, Slack

ASSUME /\ Delta \in Nat /\ Epsilon \in Nat /\ MaxTime \in Nat
       /\ KConf \in Nat \ {0} /\ DepthK \in Nat \ {0}
       /\ MaxSkew \in Nat /\ MaxBlocks \in Nat \ {0}
       /\ Slack \in Nat

NoAnchor == -1
NoTime   == -1

VARIABLES
  now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall,
  burialAtWall

vars == <<now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall,
          burialAtWall>>

BlockTimestamps == {t \in 0..(MaxTime + MaxSkew) :
                      t >= now - MaxSkew /\ t <= now + MaxSkew}

(* Latched lifecycle: timeliness fixed at the eligibility instant B.      *)
EligibleInLifecycle == burialAtWall <= declared + Delta + Slack

Init ==
  /\ now = 0 /\ chain = <<>>
  /\ declared = NoTime /\ anchorH = NoAnchor /\ pendingAnchor = FALSE
  /\ shipped = FALSE /\ shipAtWall = NoTime /\ burialAtWall = NoTime

Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ UNCHANGED <<chain, declared, anchorH, pendingAnchor, shipped, shipAtWall,
                 burialAtWall>>

NewBlock ==
  /\ Len(chain) < MaxBlocks
  /\ \E ts \in BlockTimestamps :
       chain' = Append(chain, ts)
  /\ anchorH' = IF pendingAnchor THEN Len(chain) + 1 ELSE anchorH
  /\ pendingAnchor' = FALSE
  /\ burialAtWall' = IF /\ burialAtWall = NoTime
                        /\ anchorH' # NoAnchor
                        /\ Len(chain) + 1 >= anchorH' + DepthK
                     THEN now ELSE burialAtWall
  /\ UNCHANGED <<now, declared, shipped, shipAtWall>>

Declare ==
  /\ declared = NoTime
  /\ declared' = now
  /\ UNCHANGED <<now, chain, anchorH, pendingAnchor, shipped, shipAtWall,
                 burialAtWall>>

AnchorNext ==
  /\ declared # NoTime /\ anchorH = NoAnchor /\ ~pendingAnchor
  /\ pendingAnchor' = TRUE
  /\ UNCHANGED <<now, chain, declared, anchorH, shipped, shipAtWall,
                 burialAtWall>>

IssuerDesignatedH == anchorH + DepthK
IssuerConfirmedTs == chain[IssuerDesignatedH]

VerifierDesignatedH(h) == h + KConf - 1
VerifierConfirmedTs(h) == chain[VerifierDesignatedH(h)]

VerdictValid(d, h) ==
  /\ d - Epsilon <= chain[h]
  /\ chain[h] <= d + Delta
  /\ VerifierConfirmedTs(h) <= d + Delta

(* Ship under latch: chain guard unchanged; lifecycle guard on B.         *)
(* Eligibility (buried to depth) implies burialAtWall # NoTime.            *)
Ship ==
  /\ ~shipped /\ anchorH # NoAnchor
  /\ Len(chain) >= IssuerDesignatedH
  /\ declared - Epsilon <= chain[anchorH]
  /\ chain[anchorH] <= declared + Delta
  /\ IssuerConfirmedTs <= declared + Delta
  /\ EligibleInLifecycle                           \* the latch, per contract
  /\ shipped' = TRUE /\ shipAtWall' = now
  /\ UNCHANGED <<now, chain, declared, anchorH, pendingAnchor, burialAtWall>>

Next == Tick \/ NewBlock \/ Declare \/ AnchorNext \/ Ship

(* Terminal states deadlock at the bounds — run TLC with -deadlock.        *)

(***************************************************************************)
(* Invariants — identical statements to the base module.                   *)
(***************************************************************************)

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

ChainValidBurialInLifecycle ==
  (/\ anchorH # NoAnchor /\ burialAtWall # NoTime
   /\ VerdictValid(declared, anchorH))
  => burialAtWall <= declared + Delta + Slack

(* Sanity witnesses (violations healthy): shipping reachable; the state   *)
(* the execution-time guard forbade is live — shipped AFTER the wall      *)
(* envelope on timely eligibility (the latch's point: the scheduler       *)
(* cannot expire an eligible attempt).                                     *)
ShipUnreachable == ~shipped
PostEnvelopeShipUnreachable ==
  ~(shipped /\ shipAtWall > declared + Delta + Slack)

================================================================================
