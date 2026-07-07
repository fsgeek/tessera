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
(* SEMANTIC FORK, RESOLVED (Amendment 2, ratified 2026-07-07): the        *)
(* registered "confirmed ... within delta" is ratified in its STRICT      *)
(* reading, defined on the chain-visible observable (A2.1):               *)
(*   confirmed_at := timestamp(block h+k-1)  <=  declared + delta         *)
(* evaluated IDENTICALLY by the issuer at Ship and by the verifier (the   *)
(* A2.2 third conjunct; see P5P6_TemporalRevocation's confirmedAt).       *)
(* Under this module's single-clock abstraction (block timestamps equal   *)
(* real time, blocks arrive one per tick) Ship's "now <= declared +       *)
(* Delta" at depth k IS the chain-time predicate, so the action needed    *)
(* no change. Convention pin (A2.1): this module's depth counts blocks    *)
(* AFTER inclusion (depth 0 = just included); Bitcoin convention counts   *)
(* the including block as the first confirmation; hence DepthK = k - 1    *)
(* (strict default k = 6 => DepthK = 5). MaxAttempts is protocol          *)
(* semantics per A2.3 — N attempts, then explicit fail-closed refusal     *)
(* (N ratified at Band 0 exit, working default 3) — no longer a mere      *)
(* state-space bound; see the abstractions note below.                     *)
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
(* - MaxTime bounds the state space. MaxAttempts, post-A2.3, is protocol  *)
(*   semantics: exhausting it means issuance terminates in explicit       *)
(*   refusal (a first-class outcome, reported), not an artifact of the    *)
(*   bounded model. The unbounded "eventually ships" liveness claim is    *)
(*   NOT checked (bounded model) — termination is by construction (A2.3), *)
(*   and the safety claims are what this module discharges.                *)
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
