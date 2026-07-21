--------------------------- MODULE P5cP5P6_BridgeSlack ---------------------------
(***************************************************************************)
(* Tessera Band 0 — slack-parameter analysis companion to the bridge      *)
(* (P5cP5P6_Bridge.tla). PURPOSE: evidence for the clock-precedence       *)
(* ruling (A2 round-2 blocker), NOT protocol semantics. The committed     *)
(* bridge is untouched; whichever way the ruling goes, its consequences   *)
(* land there and in P5c, per the round-2 disposition.                     *)
(*                                                                          *)
(* THE QUESTION. A2.1 ships on chain time; P5c expires attempts on its    *)
(* fused wall clock; the bridge's WallClockDivergence witness proved the  *)
(* two disagree off the boundary. Candidate two-clock rule: the attempt   *)
(* lifecycle is wall-clock-governed with slack S beyond the chain window  *)
(* (alive while now <= declared + Delta + S); shipping remains            *)
(* chain-governed inside that envelope. Analysis target: the              *)
(* chain-valid-but-discarded residue class is empty iff S >= the          *)
(* consensus lag bound (MaxSkew here).                                     *)
(*                                                                          *)
(* CORRECTION (2026-07-21, non-author bench contract, Codex): "consensus  *)
(* lag bound" above OVERCLAIMS. Bitcoin consensus gives median-time-past  *)
(* plus the two-hour future bound — neither yields a fixed finite bound   *)
(* on the BACKWARD lag between a block's timestamp and the wall time it   *)
(* is observed; the symmetric MaxSkew abstraction (inherited from the     *)
(* bridge) is STRONGER than consensus on exactly the difficult half. L    *)
(* (= MaxSkew here) is a DECLARED ENVIRONMENT/OPERATIONAL-POLICY          *)
(* ASSUMPTION, and every result of this module reads conditionally:       *)
(* under a declared maximum backward timestamp-lag assumption L, slack    *)
(* S >= L makes every chain-timely attempt operationally timely at the    *)
(* moment eligibility is reached. Whether such an L is registrable is     *)
(* part of the clock-precedence ruling itself. The companion              *)
(* P5cP5P6_BridgeSlack_Latch variant closes the related scheduler gap:    *)
(* this module's Ship checks the lifecycle at EXECUTION time, excluding   *)
(* shipped states latch-at-eligibility semantics would allow.              *)
(*                                                                          *)
(* THE RESIDUE CLASS IS DEFINED ON OPPORTUNITY, NOT OUTCOME. Under        *)
(* interleaving, expired-and-unshipped-and-chain-valid is reachable at    *)
(* ANY slack — laziness alone gets there (nothing forces Ship). The       *)
(* checkable statement is: every chain-valid attempt had a live shipping  *)
(* opportunity — the lifecycle had not expired when burial completed.     *)
(* burialAtWall records that instant; ChainValidBurialInLifecycle is the  *)
(* invariant. The outcome-form residue appears as the LifecycleBinds      *)
(* sanity witness so the narrowing is visible, not silent. Consequence    *)
(* for the ruling: at sufficient slack, "no chain-valid attempt is        *)
(* discarded" is a CONTRACT obligation (act on the live opportunity),     *)
(* not a provable liveness property — the A2.3 proof-vs-contract split,   *)
(* again.                                                                   *)
(*                                                                          *)
(* WHY MaxSkew IS THE BOUND. A block arriving at wall time w carries      *)
(* ts \in [w - MaxSkew, w + MaxSkew], so w <= ts + MaxSkew. Chain-valid   *)
(* puts ts <= declared + Delta on the designated block, hence             *)
(* burialAtWall <= declared + Delta + MaxSkew. Main cfg checks            *)
(* S = MaxSkew green; _BrokenSlack checks S = MaxSkew - 1 red on exactly  *)
(* ChainValidBurialInLifecycle; the BurialAtCutoff sanity witness shows   *)
(* the bound is achieved, making the iff sharp at this discretization.     *)
(*                                                                          *)
(* Everything else — decoupled skewed non-monotonic timestamps, derived   *)
(* confirmedAt, independent issuer/verifier transcriptions, the DepthK    *)
(* pin as checked invariant, no reorgs, single attempt, stateless         *)
(* verdicts — is carried unchanged from the bridge; see its header.       *)
(* Ship differs in exactly one conjunct: the lifecycle guard.              *)
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
  now,        \* wall clock (ticks; carries no block semantics here)
  chain,      \* sequence of block timestamps; chain[i] = timestamp of block i
  declared,   \* declared_issue_time of the single attempt (NoTime until Declare)
  anchorH,    \* chain index (height) of the block containing the anchor
  pendingAnchor, \* anchor submitted, waiting for the next block
  shipped,    \* issuance completed under the strict rule + lifecycle guard
  shipAtWall, \* wall-clock time at the Ship instant (NoTime before)
  burialAtWall \* wall-clock time when burial to the designated block
               \* completed (NoTime before) — the shipping-opportunity instant

vars == <<now, chain, declared, anchorH, pendingAnchor, shipped, shipAtWall,
          burialAtWall>>

(* Block timestamps: consensus-bounded skew around arrival time, non-    *)
(* monotonicity allowed (no constraint against earlier blocks).           *)
BlockTimestamps == {t \in 0..(MaxTime + MaxSkew) :
                      t >= now - MaxSkew /\ t <= now + MaxSkew}

(* The candidate lifecycle rule under analysis: wall-clock-governed with  *)
(* slack S beyond the chain window.                                        *)
LifecycleAlive == now <= declared + Delta + Slack

Init ==
  /\ now = 0 /\ chain = <<>>
  /\ declared = NoTime /\ anchorH = NoAnchor /\ pendingAnchor = FALSE
  /\ shipped = FALSE /\ shipAtWall = NoTime /\ burialAtWall = NoTime

Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ UNCHANGED <<chain, declared, anchorH, pendingAnchor, shipped, shipAtWall,
                 burialAtWall>>

(* A block arrives, carrying a skewed timestamp. If an anchor is pending, *)
(* this block includes it. If this block completes burial to the          *)
(* designated block (issuer convention: anchorH + DepthK), record the     *)
(* wall clock — the first instant Ship's chain guard is evaluable.        *)
(* DepthK >= 1, so the including block never completes burial itself.     *)
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

(* Submit the anchor; it lands in the next block to arrive (calendar      *)
(* delay = however long NewBlock takes to fire).                           *)
AnchorNext ==
  /\ declared # NoTime /\ anchorH = NoAnchor /\ ~pendingAnchor
  /\ pendingAnchor' = TRUE
  /\ UNCHANGED <<now, chain, declared, anchorH, shipped, shipAtWall,
                 burialAtWall>>

(***************************************************************************)
(* The two independent transcriptions of "the k-th-confirmation block",   *)
(* carried unchanged from the bridge.                                      *)
(***************************************************************************)

IssuerDesignatedH == anchorH + DepthK
IssuerConfirmedTs == chain[IssuerDesignatedH]

VerifierDesignatedH(h) == h + KConf - 1
VerifierConfirmedTs(h) == chain[VerifierDesignatedH(h)]

(* The verifier's full VALID_STRICT (A2.2), stateless over the chain.     *)
(* Only evaluated under a definedness guard (headers present).             *)
VerdictValid(d, h) ==
  /\ d - Epsilon <= chain[h]                       \* conjunct 1 (epsilon side)
  /\ chain[h] <= d + Delta                         \* conjunct 2 (anchor window)
  /\ VerifierConfirmedTs(h) <= d + Delta           \* conjunct 3 (A2.2, new)

(* Ship: the bridge's full three-conjunct chain guard PLUS the candidate  *)
(* lifecycle guard — the one-conjunct difference from the bridge.          *)
Ship ==
  /\ ~shipped /\ anchorH # NoAnchor
  /\ Len(chain) >= IssuerDesignatedH               \* buried to depth DepthK
  /\ declared - Epsilon <= chain[anchorH]
  /\ chain[anchorH] <= declared + Delta
  /\ IssuerConfirmedTs <= declared + Delta
  /\ LifecycleAlive                                \* the slack rule under test
  /\ shipped' = TRUE /\ shipAtWall' = now
  /\ UNCHANGED <<now, chain, declared, anchorH, pendingAnchor, burialAtWall>>

Next == Tick \/ NewBlock \/ Declare \/ AnchorNext \/ Ship

(* Terminal states deadlock at the bounds — run TLC with -deadlock.        *)

(***************************************************************************)
(* Invariants.                                                             *)
(***************************************************************************)

(* Carried from the bridge, unchanged in statement; Ship's guard is       *)
(* strictly stronger, so these must stay green.                            *)
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

(* THE ANALYSIS TARGET. Every chain-valid attempt had a live shipping     *)
(* opportunity: the lifecycle had not expired at the instant burial       *)
(* completed. Claim under test: green iff Slack >= MaxSkew (main cfg      *)
(* S = MaxSkew green; _BrokenSlack S = MaxSkew - 1 red on exactly this).   *)
ChainValidBurialInLifecycle ==
  (/\ anchorH # NoAnchor /\ burialAtWall # NoTime
   /\ VerdictValid(declared, anchorH))
  => burialAtWall <= declared + Delta + Slack

(* Vacuity witnesses — _Sanity cfg, TLC -continue, filtered per           *)
(* scripts/filter-tlc-output.sh; VIOLATIONS are the healthy result.        *)
(* In order: shipping reachable under the strengthened guard; wall-clock  *)
(* divergence live WITHIN the slack envelope (ship after the chain        *)
(* deadline in wall terms — the slack rule's point); the outcome-form     *)
(* laziness residue live even at sufficient slack (scope of the           *)
(* invariant made visible: opportunity, not outcome); the cutoff          *)
(* achieved (burial exactly at declared + Delta + Slack, chain-valid —    *)
(* the MaxSkew bound is tight, the iff is sharp).                          *)
ShipUnreachable == ~shipped
WallClockDivergenceUnreachable ==
  ~(shipped /\ shipAtWall > declared + Delta)
LifecycleBindsUnreachable ==
  ~(/\ anchorH # NoAnchor /\ ~shipped /\ burialAtWall # NoTime
    /\ VerdictValid(declared, anchorH)
    /\ now > declared + Delta + Slack)
BurialAtCutoffUnreachable ==
  ~(/\ anchorH # NoAnchor /\ burialAtWall # NoTime
    /\ VerdictValid(declared, anchorH)
    /\ burialAtWall = declared + Delta + Slack)

================================================================================
