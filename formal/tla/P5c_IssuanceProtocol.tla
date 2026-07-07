------------------------- MODULE P5c_IssuanceProtocol -------------------------
(***************************************************************************)
(* Tessera Band 0 — P5's issuance-protocol corollary: "issuance is not    *)
(* complete until the anchor is confirmed — buried at a minimum           *)
(* confirmation depth k — within delta of declared_issue_time. If         *)
(* confirmation is delayed past delta for benign reasons (calendar        *)
(* outage, fee spikes, reorg), the receipt is re-issued with a fresh      *)
(* declared time and re-anchored — the failed attempt is discarded, not   *)
(* shipped." (Amendment 1 §A1.2 P5 corollary, §A1.6.)                     *)
(*                                                                          *)
(* Unlike the stateless enumerations (P4, P5/P6 verifier-side), this IS a *)
(* state machine: time advances, anchors land, blocks deepen, reorgs      *)
(* orphan shallow blocks, the issuer ships or re-issues. It discharges    *)
(* the obligation the verifier-side model's scope boundary names: that    *)
(* the verifier may take `anchor` as an already-permanent block time.     *)
(*                                                                          *)
(* SEMANTIC FORK SURFACED BY THIS MODEL (author ratification needed):     *)
(* the registered text reads "confirmed ... within delta", i.e. depth k   *)
(* must be REACHED by declared + delta — the strict reading, modeled      *)
(* here (Ship requires now <= declared + Delta). The permissive           *)
(* alternative — ship whenever depth k is reached, provided the BLOCK     *)
(* TIME anchorAt <= declared + delta — is verifier-aligned (the verifier  *)
(* sees only anchorAt) and would accept some receipts the strict rule     *)
(* re-issues (anchor lands in-window, deepens slowly). The strict rule    *)
(* is safe, merely more conservative; the model follows the registered    *)
(* text. Relaxing it later is a semantic change requiring a recorded      *)
(* decision (and, per A1.1, an amendment if it weakens the property).     *)
(*                                                                          *)
(* Abstractions, named:                                                     *)
(* - Single clock: block timestamps equal real time here. Bitcoin         *)
(*   timestamp skew is verifier-side, absorbed into epsilon (A1.6), out   *)
(*   of scope. Consequence: issuance-side anchors never precede           *)
(*   declaration in this model, so the epsilon side does not appear.      *)
(* - Reorgs never exceed depth k: the A1.6 Layer 2 assumption ("anchors   *)
(*   at depth >= k are treated as permanent") is a PRECONDITION of the    *)
(*   Reorg action, not something proven. The broken companion shows what  *)
(*   the depth-k ship rule buys GIVEN that assumption.                     *)
(* - MaxAttempts / MaxTime bound the state space; the unbounded           *)
(*   "eventually ships" liveness claim is NOT checked (bounded model) —   *)
(*   the safety claims are what this module discharges.                    *)
(*                                                                          *)
(* Reading guide (Tony): this module has real actions. Tick advances      *)
(* time and deepens an included anchor by one block per tick (block       *)
(* arrival = clock tick, a deliberate simplification). Anchor lands the   *)
(* stamp in the chain (depth 0 = just included; k more ticks to bury).    *)
(* Reorg orphans any anchor shallower than k. Ship completes issuance    *)
(* under the strict rule. Reissue discards a timed-out attempt and        *)
(* redeclares at the current time.                                          *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, Delta, DepthK, MaxAttempts

ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
       /\ MaxAttempts \in Nat \ {0}

NoAnchor == -1

VARIABLES
  now,             \* the clock
  declared,        \* declared_issue_time of the CURRENT attempt
  anchorAt,        \* block time of the current anchor (NoAnchor if none)
  depth,           \* confirmations of that anchor (capped at DepthK)
  shipped,         \* issuance completed
  shippedOrphaned, \* a SHIPPED receipt's anchor was orphaned (must stay FALSE)
  attempts,        \* issuance attempts so far
  reorgs           \* reorg count (capped; for reachability witnesses)

vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs>>

Init ==
  /\ now = 0 /\ declared = 0
  /\ anchorAt = NoAnchor /\ depth = 0
  /\ shipped = FALSE /\ shippedOrphaned = FALSE
  /\ attempts = 1 /\ reorgs = 0

(* Time advances; an included, unorphaned anchor gains one confirmation   *)
(* per tick (depth capped at DepthK — beyond k, nothing changes).          *)
Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts, reorgs>>

(* The OTS calendar lands the stamp in a block — at any time (delays are  *)
(* modeled by this action simply not firing yet).                          *)
Anchor ==
  /\ ~shipped /\ anchorAt = NoAnchor
  /\ anchorAt' = now /\ depth' = 0
  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs>>

(* A reorganization orphans any anchor shallower than DepthK. Depth >= k  *)
(* is permanent BY ASSUMPTION (A1.6) — that is the Layer 2 line this      *)
(* model builds on, not a result it proves. If a shipped receipt's anchor *)
(* is orphaned, the harm flag latches (the correct Ship rule makes that   *)
(* unreachable; the broken companion makes it reachable).                  *)
Reorg ==
  /\ anchorAt # NoAnchor /\ depth < DepthK
  /\ reorgs < 2
  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
  /\ UNCHANGED <<now, declared, shipped, attempts>>

(* Issuance completes — STRICT rule per the registered text: the anchor   *)
(* is buried at depth k AND we are still within delta of the declared     *)
(* time. (anchorAt <= now always, so the block time is in-window a        *)
(* fortiori.)                                                               *)
Ship ==
  /\ ~shipped /\ anchorAt # NoAnchor
  /\ depth >= DepthK
  /\ now <= declared + Delta
  /\ shipped' = TRUE
  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts, reorgs>>

(* The window expired without completion: discard the attempt, redeclare  *)
(* fresh. The old attempt never ships — its declared time is gone.         *)
Reissue ==
  /\ ~shipped /\ now > declared + Delta
  /\ attempts < MaxAttempts
  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
  /\ attempts' = attempts + 1
  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs>>

Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue

(* Terminal states (shipped, or out of time/attempts) deadlock at the     *)
(* MaxTime bound — run TLC with -deadlock (checking disabled); the        *)
(* deadlocks are artifacts of the bounded model, not protocol defects.    *)

(***************************************************************************)
(* Invariants — what "the verifier may assume anchor is permanent" costs  *)
(* and buys.                                                                *)
(***************************************************************************)

(* THE HARM INVARIANT (Gemini's finding, discharged): a shipped receipt's *)
(* anchor is never orphaned — no receipt in the wild ever becomes         *)
(* permanently unverifiable through reorg. Holds because Ship requires    *)
(* depth >= k and Reorg touches only depth < k.                            *)
NoShippedOrphan == ~shippedOrphaned

(* A shipped receipt is temporally sound and buried: block time within    *)
(* the window of ITS OWN declared time, at full depth. (Post-ship,        *)
(* declared/anchorAt/depth are frozen: Reissue is disabled by shipped,    *)
(* Anchor by anchorAt, Reorg by depth.)                                     *)
ShippedIsSound ==
  shipped =>
    /\ anchorAt # NoAnchor
    /\ anchorAt >= declared
    /\ anchorAt <= declared + Delta
    /\ depth >= DepthK

(* Discarded attempts stay discarded: after a re-issue, the live declared *)
(* time is the fresh one — there is no state in which an expired          *)
(* declaration ships. (Equivalent state form: an unshipped attempt past   *)
(* its window is exactly an attempt that cannot Ship.)                     *)
ExpiredCannotShip ==
  (~shipped /\ now > declared + Delta) => ~ENABLED Ship

(* Vacuity witnesses — _Sanity cfg, TLC -continue; VIOLATIONS are the     *)
(* healthy result: shipping is reachable at all, after a re-issue, and    *)
(* after surviving a reorg.                                                 *)
ShipUnreachable        == ~shipped
ReissueShipUnreachable == ~(shipped /\ attempts > 1)
ReorgShipUnreachable   == ~(shipped /\ reorgs > 0)

================================================================================
