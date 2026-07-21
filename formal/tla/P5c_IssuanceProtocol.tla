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
(* REFUSAL STATE (2026-07-20, round-3 ruling 4, AUTHOR-ADOPTED FOR        *)
(* STAGE-ONE DRAFTING): the refusal is modeled by ATOMIC ENTRY — the      *)
(* Tick that expires the FINAL attempt's window records `refused` in the  *)
(* same transition. Reaching refusal is thereby a transition-level        *)
(* SAFETY fact; no separately enabled Refuse action, no fairness          *)
(* assumption, no liveness claim. The discharged claim (narrowed          *)
(* 2026-07-20 on Codex review of this work, which withdrew its own        *)
(* round-3 phrase "durably recorded and available for retrieval" as too   *)
(* strong): the ABSTRACT REFUSAL STATE IS ENTERED ATOMICALLY AND          *)
(* LATCHES. A latched Boolean proves in-model persistence — not storage   *)
(* durability, not retrievability, not reporting. Those three, and        *)
(* A2.3's registered word "reported", are implementation/handoff          *)
(* obligations for Amendment 3 disposition, not silently absorbed here.   *)
(* Honest residuals, named: (a) Reissue is postponable, so a run can      *)
(* stall mid-loop with attempts unexhausted and no refusal; (b) Tick      *)
(* itself is postponable, so even the final crossing is not guaranteed    *)
(* to occur — atomic entry proves that IF the crossing Tick occurs, its   *)
(* post-state contains the refusal, never that it occurs. Both are the    *)
(* explicitly-unclaimed liveness ("eventual issuance remains unclaimed";  *)
(* round-3 clean rationale: a bounded, explicit negative result is        *)
(* preferable to silent deadlock). What IS claimed: no reachable state    *)
(* has the final window expired without the refusal recorded              *)
(* (NoSilentDeadlock), the record is entered only on genuine exhaustion   *)
(* (RefusedOnlyWhenExhausted), and it latches (RefusalLatched, an         *)
(* action property). Companion P5c_IssuanceProtocol_BrokenSilent          *)
(* implements the review's warned construction (separately enabled       *)
(* Refuse) and must go red on exactly NoSilentDeadlock among the          *)
(* checked set.                                                            *)
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
(*   refusal (a first-class outcome, durably recorded — see the refusal   *)
(*   note above for what "recorded" does and does not claim), not an      *)
(*   artifact of the bounded model. The unbounded "eventually ships"      *)
(*   liveness claim is NOT checked (bounded model), and the safety        *)
(*   claims are what this module discharges. MaxTime must be at least     *)
(*   MaxAttempts * (Delta + 1) or the final window cannot expire and      *)
(*   every refusal invariant passes VACUOUSLY — the _Sanity witnesses     *)
(*   exist to catch exactly that misconfiguration. The committed cfgs     *)
(*   use MaxAttempts * (Delta + 1) + DepthK = 14: the extra DepthK        *)
(*   ticks exercise the post-refusal burial path (anchor lands after or   *)
(*   at the refusal, deepens to full depth, Ship stays disabled) —        *)
(*   without them that path is claimed but unreachable (Codex finding 5,  *)
(*   2026-07-20).                                                          *)
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
  reorgs,          \* reorg count (capped; for reachability witnesses)
  refused          \* the durable refusal record (A2.3 / round-3 ruling 4)

vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
          attempts, reorgs, refused>>

Init ==
  /\ now = 0 /\ declared = 0
  /\ anchorAt = NoAnchor /\ depth = 0
  /\ shipped = FALSE /\ shippedOrphaned = FALSE
  /\ attempts = 1 /\ reorgs = 0
  /\ refused = FALSE

(* Time advances; an included, unorphaned anchor gains one confirmation   *)
(* per tick (depth capped at DepthK — beyond k, nothing changes).          *)
(*                                                                          *)
(* ATOMIC ENTRY (round-3 ruling 4, construction 1): the tick that carries *)
(* the clock past the FINAL attempt's window records the refusal in the   *)
(* SAME transition. There is no separately enabled Refuse action to       *)
(* postpone — the state in which the last window has expired but no       *)
(* refusal is recorded does not exist. The disjunct also keeps `refused`  *)
(* latched (belt; no action ever unsets it — RefusalLatched is the        *)
(* checked form of that claim).                                            *)
Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
  /\ refused' = (refused \/ (~shipped /\ attempts = MaxAttempts
                                      /\ now + 1 > declared + Delta))
  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts, reorgs>>

(* The OTS calendar lands the stamp in a block — at any time (delays are  *)
(* modeled by this action simply not firing yet). Deliberately NOT        *)
(* guarded on ~refused: a discarded attempt's stamp landing after the     *)
(* refusal is exactly the A2.4 case "a discarded attempt's transaction    *)
(* confirming later confers nothing" — the model keeps that path          *)
(* reachable, and the Ship guard, not this one, is what makes the late    *)
(* anchor worthless. Witness coverage, stated precisely (Codex finding    *)
(* 5): RefusalWithLiveAnchorUnreachable shows an anchor PRESENT in a      *)
(* refused state; RefusalBuriedAnchorUnreachable shows it BURIED to full  *)
(* depth post-refusal with Ship still disabled — the latter needs the     *)
(* +DepthK headroom in MaxTime (14), and at 12 it is unreachable.          *)
Anchor ==
  /\ ~shipped /\ anchorAt = NoAnchor
  /\ anchorAt' = now /\ depth' = 0
  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
                 refused>>

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
  /\ UNCHANGED <<now, declared, shipped, attempts, refused>>

(* Issuance completes — STRICT rule per the registered text: the anchor   *)
(* is buried at depth k AND we are still within delta of the declared     *)
(* time. (anchorAt <= now always, so the block time is in-window a        *)
(* fortiori.)                                                               *)
(*                                                                          *)
(* BOUNDARY RACE, intentional (Codex finding 1): with integral time,      *)
(* Ship's guard (now <= declared + Delta) and the refusal trigger         *)
(* (now + 1 > declared + Delta, i.e. now >= declared + Delta) BOTH hold   *)
(* at exactly now = declared + Delta — and there is no tick where         *)
(* neither holds. At the deadline instant a fully-buried anchor may       *)
(* ship, or the clock may advance and refuse; the scheduler's choice is   *)
(* the model's honest image of the physical race between burial and       *)
(* clock. Both branches are safe and the outcomes are mutually            *)
(* exclusive (RefusedOnlyWhenExhausted). Eligibility at the boundary      *)
(* does not oblige shipping — the deadline governs completion; a          *)
(* "qualification guarantees issuance" contract would be a liveness       *)
(* claim, and this module makes none.                                      *)
Ship ==
  /\ ~shipped /\ anchorAt # NoAnchor
  /\ depth >= DepthK
  /\ now <= declared + Delta
  /\ shipped' = TRUE
  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
                 reorgs, refused>>

(* The window expired without completion: discard the attempt, redeclare  *)
(* fresh. The old attempt never ships — its declared time is gone.         *)
Reissue ==
  /\ ~shipped /\ now > declared + Delta
  /\ attempts < MaxAttempts
  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
  /\ attempts' = attempts + 1
  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused>>

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

(* THE DEADLOCK INVARIANT (round-3 ruling 4): no silent terminal failure. *)
(* If the final attempt's window has expired and nothing shipped, the     *)
(* refusal record already exists — there is NO reachable state in which   *)
(* issuance is dead but undocumented. This is the state-level shadow of   *)
(* the atomic entry in Tick; the _BrokenSilent companion (separately      *)
(* enabled Refuse) must violate exactly this invariant and nothing else.   *)
NoSilentDeadlock ==
  (~shipped /\ attempts = MaxAttempts /\ now > declared + Delta) => refused

(* The negative outcome is sound: refusal is recorded ONLY on genuine     *)
(* exhaustion — final attempt, window expired, nothing shipped. (The      *)
(* conjuncts stay true once entered: Reissue is disabled by               *)
(* attempts = MaxAttempts so declared is frozen, now is monotone, and     *)
(* Ship is disabled forever by the expired window — so refused and        *)
(* shipped are mutually exclusive as a corollary.)                         *)
RefusedOnlyWhenExhausted ==
  refused => /\ ~shipped
             /\ attempts = MaxAttempts
             /\ now > declared + Delta

(* The in-model latch: every step either preserves refused or sets it;    *)
(* no step unsets it. Action property (PROPERTIES in the cfg, not         *)
(* INVARIANTS). This proves LOGICAL state persistence only — storage      *)
(* durability, retrievability, and reporting are implementation/handoff   *)
(* obligations (see the header's narrowed claim).                          *)
RefusalLatched == [][refused => refused']_vars

(* Vacuity witnesses — _Sanity cfg, TLC -continue; VIOLATIONS are the     *)
(* healthy result: shipping is reachable at all, after a re-issue, and    *)
(* after surviving a reorg; refusal is reachable at all, after a reorg,   *)
(* with a live (late, worthless) anchor present — the A2.4                *)
(* discarded-attempt case — and with that anchor BURIED to full depth     *)
(* post-refusal while Ship stays disabled (the off-happy-path trace of    *)
(* Codex finding 5). If RefusalUnreachable is NOT violated, the refusal   *)
(* invariants above are vacuous — check MaxTime >=                        *)
(* MaxAttempts * (Delta + 1); if RefusalBuriedAnchorUnreachable is NOT    *)
(* violated, the post-refusal burial path is untested — check the         *)
(* + DepthK headroom (14).                                                 *)
ShipUnreachable        == ~shipped
ReissueShipUnreachable == ~(shipped /\ attempts > 1)
ReorgShipUnreachable   == ~(shipped /\ reorgs > 0)
RefusalUnreachable               == ~refused
RefusalAfterReorgUnreachable     == ~(refused /\ reorgs > 0)
RefusalWithLiveAnchorUnreachable == ~(refused /\ anchorAt # NoAnchor)
RefusalBuriedAnchorUnreachable   == ~(refused /\ depth >= DepthK)

================================================================================
