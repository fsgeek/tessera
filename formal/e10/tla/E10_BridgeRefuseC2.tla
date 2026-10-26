--------------------------- MODULE E10_BridgeRefuseC2 ---------------------------
(***************************************************************************)
(* E10 extraction aid (STATUS: PROPOSED, owner instance, 2026-10-26).     *)
(* Not a model of record. It EXTENDS the committed bridge module           *)
(* formal/tla/P5cP5P6_Bridge.tla unchanged and adds two formulas only, so  *)
(* that the A3 §A3.9 issuance-path case ("anchor_time = declared+δ+1,      *)
(* confirmed_at = declared+δ−1 → refuse to ship", registered as "extracted *)
(* from the bridge model") has a cited trace in the bridge's own state     *)
(* space. The bridge has no refusal action (header, single attempt), so    *)
(* "refuse" is read here as "Ship is never taken in this state".           *)
(*                                                                          *)
(* C2FailC3PassArtifactUnreachable: vacuity witness, healthy result RED.  *)
(*   The anchored attempt's inclusion-block timestamp is past the window  *)
(*   (conjunct 2 fails) while the k-th confirmation timestamp is inside   *)
(*   it (conjunct 3 passes) and conjunct 1 holds: the decoupled-clock     *)
(*   divergence state the registered vector names.                         *)
(* C2FailNeverShipped: the safety reading, healthy result GREEN. Such an   *)
(*   attempt is never shipped. (It follows from Ship's guard, bridge       *)
(*   lines 171-178; it is checked, not assumed.)                            *)
(***************************************************************************)
EXTENDS P5cP5P6_Bridge

C2FailC3PassState ==
  /\ anchorH # NoAnchor
  /\ Len(chain) >= VerifierDesignatedH(anchorH)
  /\ declared - Epsilon <= chain[anchorH]                \* conjunct 1 holds
  /\ chain[anchorH] > declared + Delta                   \* conjunct 2 fails
  /\ VerifierConfirmedTs(anchorH) <= declared + Delta    \* conjunct 3 holds

C2FailC3PassArtifactUnreachable == ~C2FailC3PassState

C2FailNeverShipped == C2FailC3PassState => ~shipped

================================================================================
