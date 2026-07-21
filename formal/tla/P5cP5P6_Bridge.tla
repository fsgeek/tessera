------------------------------ MODULE P5cP5P6_Bridge ------------------------------
(***************************************************************************)
(* Tessera Band 0 — the TLA+<->TLA+ correspondence bridge (tracker        *)
(* obligation, surfaced 2026-07-18, narrowed by non-author check: the     *)
(* alarming "burial delay vanishes" form did NOT reproduce; what remained *)
(* is that P5c models depth operationally under a single fused clock      *)
(* while P5P6 takes confirmedAt as a free integer, and the join — "the    *)
(* confirmedAt the verifier reads is the timestamp of the very block the  *)
(* issuer's ship rule evaluated" — was asserted in comments, checked      *)
(* nowhere).                                                                *)
(*                                                                          *)
(* This module checks that join. Three deliberate departures from P5c's   *)
(* abstractions:                                                            *)
(* - BLOCK TIMESTAMPS ARE DECOUPLED FROM THE TICK CLOCK. A block          *)
(*   arriving at wall time `now` carries a timestamp chosen               *)
(*   nondeterministically in [now - MaxSkew, now + MaxSkew] — skewed and  *)
(*   NON-MONOTONIC, per A2.1's named residuals. Time can pass without a   *)
(*   block arriving (the Q2 fusion, undone).                               *)
(* - confirmedAt is DERIVED from the chain, never latched and never a     *)
(*   free variable. Latching it under P5c's single clock would make the   *)
(*   correspondence true by construction — the pre-named vacuity trap.     *)
(* - ISSUER AND VERIFIER ARE TRANSCRIBED INDEPENDENTLY, each from its     *)
(*   own registered text. The issuer speaks P5c's depth convention        *)
(*   (depth counts blocks AFTER inclusion; evaluate the block that        *)
(*   brings depth to DepthK). The verifier speaks A2.1/A2.2's height      *)
(*   convention (the block at height h + k - 1, Bitcoin counting). The    *)
(*   convention pin DepthK = k - 1 is deliberately NOT an ASSUME — it is  *)
(*   the INVARIANT PinAgreement, instantiated by the cfg, so an           *)
(*   off-by-one in either transcription or in the cfg goes red instead    *)
(*   of being assumed away (the READ-AND-CHALLENGE Q6 seam, mechanical).   *)
(*                                                                          *)
(* Ship's guard is the FULL three-conjunct VALID_STRICT on chain          *)
(* quantities — not conjunct 3 alone. Design-time finding (registered in  *)
(* docs/reviews/2026-07-21-claude-predictions-bridge-bench.md, routed to  *)
(* the A2 review rounds): under decoupled non-monotonic timestamps,       *)
(* conjunct 3 alone does not imply conjunct 2, so a conjunct-3-only      *)
(* issuer could honestly ship a receipt the verifier rejects on the       *)
(* anchor-time window. A2.1's prose states only conjunct 3 in "The       *)
(* rule"; the identical-predicate framing (A2.2, P5c header) implies the  *)
(* full guard transcribed here.                                            *)
(*                                                                          *)
(* Abstractions, named:                                                     *)
(* - Single issuance attempt; no Reissue, no refusal, no attempt bound.   *)
(*   The retry loop is P5c's discharged territory and is orthogonal to    *)
(*   the ship/verify seam. An unshipped anchored attempt here doubles as  *)
(*   the abandoned-anchor artifact of A2.0.                                *)
(* - No reorgs: A1.6 treats depth >= k as permanent, and P5c discharges   *)
(*   what that assumption buys at ship time. Designated blocks are        *)
(*   therefore immutable here, so verify-later equals verify-at-ship;     *)
(*   re-checking the correspondence under reorg is NOT discharged by      *)
(*   this module.                                                          *)
(* - Verification is stateless (P9): the verdict is an operator over the  *)
(*   chain, not an action. Artifacts are "presented" by predicating       *)
(*   invariants on the current (declared, anchorH) pair — shipped or      *)
(*   abandoned. The headers-unavailable arm (UNVERIFIABLE) is out of      *)
(*   scope: verdict operators are only evaluated under definedness        *)
(*   guards.                                                                *)
(*                                                                          *)
(* Reading guide (Tony): Tick advances wall time only. NewBlock appends   *)
(* a timestamp to the chain — blocks and time are now separate events.    *)
(* Declare stamps the attempt; AnchorNext puts the anchor in the NEXT     *)
(* block to arrive. Ship fires only on the full strict predicate over    *)
(* chain timestamps; shipAtWall records the wall clock at that instant    *)
(* so the sanity witness can exhibit wall-clock/chain-time divergence     *)
(* (ship after the wall deadline, chain-time in window) — the state the   *)
(* fused clock could not represent.                                        *)
(***************************************************************************)
EXTENDS Integers, Sequences

CONSTANTS MaxTime, Delta, Epsilon, KConf, DepthK, MaxSkew, MaxBlocks

ASSUME /\ Delta \in Nat /\ Epsilon \in Nat /\ MaxTime \in Nat
       /\ KConf \in Nat \ {0} /\ DepthK \in Nat \ {0}
       /\ MaxSkew \in Nat /\ MaxBlocks \in Nat \ {0}

NoAnchor == -1
NoTime   == -1

VARIABLES
  now,        \* wall clock (ticks; carries no block semantics here)
  chain,      \* sequence of block timestamps; chain[i] = timestamp of block i
  declared,   \* declared_issue_time of the single attempt (NoTime until Declare)
  anchorH,    \* chain index (height) of the block containing the anchor
  pendingAnchor, \* anchor submitted, waiting for the next block
  shipped,    \* issuance completed under the strict rule
  shipAtWall  \* wall-clock time at the Ship instant (NoTime before)

vars == <<now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall>>

(* Block timestamps: consensus-bounded skew around arrival time, non-    *)
(* monotonicity allowed (no constraint against earlier blocks).           *)
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

(* A block arrives, carrying a skewed timestamp. If an anchor is pending, *)
(* this block includes it (height = its chain index).                      *)
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

(* Submit the anchor; it lands in the next block to arrive (calendar      *)
(* delay = however long NewBlock takes to fire).                           *)
AnchorNext ==
  /\ declared # NoTime /\ anchorH = NoAnchor /\ ~pendingAnchor
  /\ pendingAnchor' = TRUE
  /\ UNCHANGED <<now, chain, declared, anchorH, shipped, shipAtWall>>

(***************************************************************************)
(* The two independent transcriptions of "the k-th-confirmation block".   *)
(***************************************************************************)

(* ISSUER side, transcribed from P5c's convention: depth counts blocks    *)
(* after inclusion; the block that brings the anchor to depth DepthK sits *)
(* DepthK positions after the including block.                             *)
IssuerDesignatedH == anchorH + DepthK
IssuerConfirmedTs == chain[IssuerDesignatedH]

(* VERIFIER side, transcribed from A2.1/A2.2 vocabulary: the including    *)
(* block is the first confirmation; the block granting the k-th           *)
(* confirmation has height h + k - 1.                                      *)
VerifierDesignatedH(h) == h + KConf - 1
VerifierConfirmedTs(h) == chain[VerifierDesignatedH(h)]

(* The verifier's full VALID_STRICT (A2.2), stateless over the chain.     *)
(* Only evaluated under a definedness guard (headers present).             *)
VerdictValid(d, h) ==
  /\ d - Epsilon <= chain[h]                       \* conjunct 1 (epsilon side)
  /\ chain[h] <= d + Delta                         \* conjunct 2 (anchor window)
  /\ VerifierConfirmedTs(h) <= d + Delta           \* conjunct 3 (A2.2, new)

(* Ship: the issuer evaluates the FULL strict predicate on chain          *)
(* quantities, in its own (depth) convention. See the header note on why  *)
(* all three conjuncts and not only the third.                             *)
Ship ==
  /\ ~shipped /\ anchorH # NoAnchor
  /\ Len(chain) >= IssuerDesignatedH               \* buried to depth DepthK
  /\ declared - Epsilon <= chain[anchorH]
  /\ chain[anchorH] <= declared + Delta
  /\ IssuerConfirmedTs <= declared + Delta
  /\ shipped' = TRUE /\ shipAtWall' = now
  /\ UNCHANGED <<now, chain, declared, anchorH, pendingAnchor>>

Next == Tick \/ NewBlock \/ Declare \/ AnchorNext \/ Ship

(* Terminal states deadlock at the bounds — run TLC with -deadlock.        *)

(***************************************************************************)
(* Invariants — the join, checked.                                         *)
(***************************************************************************)

(* THE CONVENTION PIN, as an invariant instead of an ASSUME: the two      *)
(* transcriptions designate the same block iff DepthK = k - 1. The        *)
(* _BrokenPin cfg instantiates DepthK = KConf and must go red here with a *)
(* length-1 trace.                                                          *)
PinAgreement == DepthK = KConf - 1

(* The join itself: for a shipped receipt, the quantity the issuer's Ship *)
(* guard evaluated IS the quantity the verifier derives from the shipped  *)
(* headers — same designated block, same timestamp. This is the sentence  *)
(* that used to live only in comments.                                     *)
ShippedDesignatedAgree ==
  shipped =>
    /\ IssuerDesignatedH = VerifierDesignatedH(anchorH)
    /\ IssuerConfirmedTs = VerifierConfirmedTs(anchorH)

(* A2.1's headline claim, checked instead of asserted: no honestly-       *)
(* shipped receipt fails the verifier. (No reorgs, so verify-later        *)
(* equals verify-at-ship; see abstractions.)                               *)
HonestShipAccepted ==
  shipped => VerdictValid(declared, anchorH)

(* The A2.0/A2.2 rejection, and the broken-bridge tripwire: an abandoned  *)
(* artifact whose true k-th-confirmation timestamp falls outside the      *)
(* window is INVALID. The _BrokenAnchorSubst companion (verifier reads    *)
(* the inclusion-block timestamp instead) accepts exactly these — red.    *)
LateBurialRejected ==
  (/\ anchorH # NoAnchor /\ ~shipped
   /\ Len(chain) >= VerifierDesignatedH(anchorH)
   /\ VerifierConfirmedTs(anchorH) > declared + Delta)
  => ~VerdictValid(declared, anchorH)

(* Vacuity witnesses — _Sanity cfg, TLC -continue, filtered per           *)
(* scripts/filter-tlc-output.sh; VIOLATIONS are the healthy result.        *)
(* In order: shipping reachable at all; the burial gap is a real          *)
(* quantity (confirmedAt differs from the anchor timestamp — the value    *)
(* P5P6 alone could not see); the non-monotonic case is live              *)
(* (confirmedAt BEFORE the anchor timestamp, A2.1's named residual);      *)
(* the epsilon side is live (anchor timestamp before declared — the       *)
(* phenomenon P5c's fused clock made unrepresentable); wall-clock/        *)
(* chain-time divergence is live (shipped after the wall deadline, chain  *)
(* time in window — the fusion, undone); the late-burial abandoned        *)
(* artifact exists (feeds LateBurialRejected and the broken companion).    *)
ShipUnreachable == ~shipped
BurialGapUnreachable ==
  ~(shipped /\ IssuerConfirmedTs # chain[anchorH])
NonMonotonicShipUnreachable ==
  ~(shipped /\ IssuerConfirmedTs < chain[anchorH])
EpsilonSideUnreachable ==
  ~(anchorH # NoAnchor /\ declared # NoTime /\ chain[anchorH] < declared)
WallClockDivergenceUnreachable ==
  ~(shipped /\ shipAtWall > declared + Delta)
LateBurialArtifactUnreachable ==
  ~(/\ anchorH # NoAnchor /\ ~shipped
    /\ Len(chain) >= VerifierDesignatedH(anchorH)
    /\ VerifierConfirmedTs(anchorH) > declared + Delta)

================================================================================
