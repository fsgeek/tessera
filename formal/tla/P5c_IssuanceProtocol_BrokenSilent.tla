------------------ MODULE P5c_IssuanceProtocol_BrokenSilent ------------------
(***************************************************************************)
(* Tessera Band 0 — P5c refusal semantics, DELIBERATELY BROKEN: the       *)
(* construction the round-3 review warned against, implemented verbatim.  *)
(* "Merely adding a separately enabled Refuse action does not show that   *)
(* it eventually fires: TLA+ requires a liveness property and, commonly,  *)
(* an appropriate fairness assumption when an enabled action could        *)
(* otherwise be postponed." Here Refuse IS a separately enabled action    *)
(* and there is NO fairness — so the state "final window expired, nothing *)
(* shipped, no refusal recorded" is reachable: the silent-deadlock STATE  *)
(* the atomic-entry construction makes unrepresentable.                    *)
(*                                                                          *)
(* Expected result: TLC VIOLATES NoSilentDeadlock — shortest trace is     *)
(* the straight-line run to exhaustion, ending in the Tick that crosses   *)
(* the final deadline with Refuse not yet fired. Every OTHER invariant    *)
(* of the main module must HOLD (checked by the _Green cfg): Refuse's     *)
(* guard is honest (RefusedOnlyWhenExhausted), nothing unsets refused     *)
(* (RefusalLatched), and the ship-side invariants are untouched. Red on   *)
(* exactly the deadlock invariant — AMONG THE CHECKED SET (Codex          *)
(* finding 4): the red run plus the _Green control demonstrate isolation  *)
(* over the enumerated invariants and property, not absence of every      *)
(* conceivable semantic difference. Within that scope the point stands:   *)
(* NoSilentDeadlock isolates the atomicity of the entry, not any other    *)
(* property of the refusal design.                                         *)
(*                                                                          *)
(* Identical state space and actions except: Tick does not record the     *)
(* refusal; a separate Refuse action does, whenever it gets around to it.  *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, Delta, DepthK, MaxAttempts

ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
       /\ MaxAttempts \in Nat \ {0}

NoAnchor == -1

VARIABLES now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs, refused

vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs, refused>>

Init ==
  /\ now = 0 /\ declared = 0
  /\ anchorAt = NoAnchor /\ depth = 0
  /\ shipped = FALSE /\ shippedOrphaned = FALSE
  /\ attempts = 1 /\ reorgs = 0
  /\ refused = FALSE

(* THE BREAK: Tick advances time but records nothing — crossing the final *)
(* deadline leaves refused = FALSE until Refuse happens to fire.           *)
Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts,
                 reorgs, refused>>

Anchor ==
  /\ ~shipped /\ anchorAt = NoAnchor
  /\ anchorAt' = now /\ depth' = 0
  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
                 refused>>

Reorg ==
  /\ anchorAt # NoAnchor /\ depth < DepthK
  /\ reorgs < 2
  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
  /\ UNCHANGED <<now, declared, shipped, attempts, refused>>

Ship ==
  /\ ~shipped /\ anchorAt # NoAnchor
  /\ depth >= DepthK
  /\ now <= declared + Delta
  /\ shipped' = TRUE
  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
                 reorgs, refused>>

Reissue ==
  /\ ~shipped /\ now > declared + Delta
  /\ attempts < MaxAttempts
  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
  /\ attempts' = attempts + 1
  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused>>

(* The separately enabled Refuse: guard is the honest exhaustion          *)
(* condition (so RefusedOnlyWhenExhausted still holds), but nothing       *)
(* forces it to fire before — or ever after — the deadline crossing.       *)
Refuse ==
  /\ ~shipped /\ ~refused
  /\ attempts = MaxAttempts /\ now > declared + Delta
  /\ refused' = TRUE
  /\ UNCHANGED <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
                 attempts, reorgs>>

Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue \/ Refuse

(***************************************************************************)
(* Invariants — copied verbatim from the main module; only their          *)
(* verdicts differ.                                                        *)
(***************************************************************************)

NoShippedOrphan == ~shippedOrphaned

ShippedIsSound ==
  shipped =>
    /\ anchorAt # NoAnchor
    /\ anchorAt >= declared
    /\ anchorAt <= declared + Delta
    /\ depth >= DepthK

ExpiredCannotShip ==
  (~shipped /\ now > declared + Delta) => ~ENABLED Ship

NoSilentDeadlock ==
  (~shipped /\ attempts = MaxAttempts /\ now > declared + Delta) => refused

RefusedOnlyWhenExhausted ==
  refused => /\ ~shipped
             /\ attempts = MaxAttempts
             /\ now > declared + Delta

RefusalLatched == [][refused => refused']_vars

================================================================================
