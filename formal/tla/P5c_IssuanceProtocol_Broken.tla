---------------------- MODULE P5c_IssuanceProtocol_Broken ----------------------
(***************************************************************************)
(* Tessera Band 0 — P5 issuance corollary, DELIBERATELY BROKEN: shipping  *)
(* on a shallow anchor. Ship requires only inclusion (depth >= 1), not    *)
(* burial at depth k — "it's in a block, ship it." This is the exact bug  *)
(* Gemini's review named: a transient reorganization then orphans the     *)
(* block under an already-shipped receipt, leaving it permanently          *)
(* unverifiable.                                                            *)
(*                                                                          *)
(* Expected result: TLC VIOLATES NoShippedOrphan, with the trace          *)
(* declare -> anchor -> one confirmation -> ship -> reorg. A green run    *)
(* would mean the depth-k rule buys nothing in this model.                  *)
(* Identical state space and actions except Ship's depth precondition —   *)
(* including the 2026-07-20 refusal machinery (atomic entry in Tick),     *)
(* carried verbatim so that claim stays literally true.                    *)
(*                                                                          *)
(* CORRECTION 2026-09-06 (review item 18): "only inclusion (depth >= 1)"   *)
(* above is off by one under this family's convention (depth 0 = just     *)
(* included; header of the main module). The broken Ship fires at depth   *)
(* >= 1 — ONE block after inclusion (Bitcoin's second confirmation), not  *)
(* at inclusion itself — which is still shallower than DepthK and is      *)
(* what the expected trace "anchor -> one confirmation -> ship -> reorg"  *)
(* shows. RECUT 2026-09-06 (item 15): the main module's `refusedAt`       *)
(* recording variable is carried here verbatim so "identical state space  *)
(* and actions except Ship's depth precondition" stays literally true.    *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, Delta, DepthK, MaxAttempts

ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
       /\ MaxAttempts \in Nat \ {0}

NoAnchor == -1
NoRefusal == -1

VARIABLES now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs, refused, refusedAt

vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs, refused, refusedAt>>

Init ==
  /\ now = 0 /\ declared = 0
  /\ anchorAt = NoAnchor /\ depth = 0
  /\ shipped = FALSE /\ shippedOrphaned = FALSE
  /\ attempts = 1 /\ reorgs = 0
  /\ refused = FALSE /\ refusedAt = NoRefusal

Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
  /\ refused' = (refused \/ (~shipped /\ attempts = MaxAttempts
                                      /\ now + 1 > declared + Delta))
  /\ refusedAt' = IF refused' /\ ~refused THEN now + 1 ELSE refusedAt
  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts, reorgs>>

Anchor ==
  /\ ~shipped /\ anchorAt = NoAnchor
  /\ anchorAt' = now /\ depth' = 0
  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
                 refused, refusedAt>>

Reorg ==
  /\ anchorAt # NoAnchor /\ depth < DepthK
  /\ reorgs < 2
  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
  /\ UNCHANGED <<now, declared, shipped, attempts, refused, refusedAt>>

(* BROKEN: ships on mere inclusion — depth >= 1, not DepthK.               *)
(* CORRECTION 2026-09-06 (item 18): depth >= 1 is one block AFTER          *)
(* inclusion (inclusion is depth 0); shallow, not "mere inclusion".        *)
Ship ==
  /\ ~shipped /\ anchorAt # NoAnchor
  /\ depth >= 1
  /\ now <= declared + Delta
  /\ shipped' = TRUE
  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
                 reorgs, refused, refusedAt>>

Reissue ==
  /\ ~shipped /\ now > declared + Delta
  /\ attempts < MaxAttempts
  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
  /\ attempts' = attempts + 1
  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused, refusedAt>>

Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue

(* Same harm invariant as the correct module. EXPECTED: VIOLATED.          *)
NoShippedOrphan == ~shippedOrphaned

================================================================================
