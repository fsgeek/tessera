------------------------------ MODULE FloorLink_Probe ------------------------------
(***************************************************************************)
(* Tessera — floor-structure VIABILITY PROBE (spike tier; see PROBE.md).  *)
(* This module discharges NOTHING. It mechanizes the contrast between     *)
(* counted and linked evidence floors from A3.2 ("Why linked, not         *)
(* counted") and the 2026-07-28 Ruling 2, to test whether the linked      *)
(* floor is expressible in TLA+ without degenerating (Path B viability).  *)
(*                                                                         *)
(* Shape follows P4_VerifierStates: a degenerate state machine — Init     *)
(* enumerates every configuration, invariants carry all content. One      *)
(* acceptance consumes an authority statement and a key; a possession     *)
(* proof and a set of external evidence objects sit beside it. Evidence   *)
(* binds a (statement, fingerprint) pair; fingerprints are symbolic and   *)
(* injective (fp(k) = k), the spike's hash abstraction. Artifact          *)
(* validity is implicit: every present object is assumed verified as an   *)
(* artifact — linkage BETWEEN valid artifacts is the entire question.     *)
(*                                                                         *)
(* Scope exclusions (PROBE.md): no attacker deduction, no waiver          *)
(* interaction, no per-layer quantification, chain depth one.             *)
(***************************************************************************)

CONSTANTS Stmts, Keys

VARIABLES accStmt, accKey, possKey, evidences

EvidenceObjs == [stmt: Stmts, fp: Keys]

Init ==
  /\ accStmt \in Stmts
  /\ accKey \in Keys
  /\ possKey \in Keys
  /\ evidences \in SUBSET EvidenceObjs

Next == UNCHANGED <<accStmt, accKey, possKey, evidences>>

(***************************************************************************)
(* The chain question: does one evidence object bind BOTH the statement   *)
(* consumed and the key accepted?                                          *)
(***************************************************************************)
ChainClosed == \E e \in evidences : e.stmt = accStmt /\ e.fp = accKey

(***************************************************************************)
(* The three floors, in claimed strictness order.                          *)
(***************************************************************************)

(* A3.2's quoted counted floor: ">= 1 accepted external evidence".        *)
CountedCard == evidences # {}

(* The steelman repair of counting: each counter individually             *)
(* relevance-checked. Note the quantifier shape: two separate \E.         *)
CountedRelevant ==
  /\ \E e \in evidences : e.stmt = accStmt
  /\ \E e \in evidences : e.fp = accKey

(* The linked floor: ONE shared witness closes statement and key          *)
(* together (single \E over a conjunction), and possession is             *)
(* chain-internal — by the same key whose signature is accepted           *)
(* (A3.2 item 3).                                                          *)
Linked == ChainClosed /\ possKey = accKey

(* The registered aTLS-genus configuration ("Why linked, not counted"):   *)
(* evidence exists, but all of it supports a different statement than     *)
(* the one whose authority was accepted.                                   *)
ForeignOnly == evidences # {} /\ \A e \in evidences : e.stmt # accStmt

(***************************************************************************)
(* Must-HOLD invariants (main cfg). The hierarchy is the probe's          *)
(* theorem; the pins are definitional guards in the P4 Exact* style —     *)
(* they protect against future edits, and are declared as such so a      *)
(* green here is not mistaken for depth.                                   *)
(***************************************************************************)
HierarchyLinkedRelevant == Linked => CountedRelevant
HierarchyRelevantCard   == CountedRelevant => CountedCard
LinkedNeverForeignOnly  == Linked => ~ForeignOnly
LinkedPossessionInternal == Linked => possKey = accKey

(***************************************************************************)
(* Witnesses (sanity cfg, run with -continue): TLC VIOLATING each is the  *)
(* healthy result — each names a configuration that must exist for the    *)
(* contrast to have content. Prose mapping per witness:                    *)
(*   W-honest:     the linked floor is satisfiable (vacuity guard).       *)
(*   W-foreign:    CountedCard admits the registered aTLS configuration   *)
(*                 (A3.2 "Why linked, not counted", made a machine trace).*)
(*   W-cross:      CountedRelevant admits split witnesses — no single     *)
(*                 object closes the chain (the two-\E vs one-\E          *)
(*                 quantifier-scope failure; same error class as the      *)
(*                 retracted pair-judge implication, RESULTS.md ledger 4).*)
(*   W-possession: CountedRelevant admits a closed chain possessed by a   *)
(*                 foreign key (A3.2 item 3 is invisible to counting).    *)
(***************************************************************************)
LinkedUnsatisfiable == ~Linked
CardNeverAcceptsForeignOnly == ~(CountedCard /\ ForeignOnly)
RelevantNeverAcceptsOpenChain == ~(CountedRelevant /\ ~ChainClosed)
RelevantNeverAcceptsForeignPossession ==
  ~(CountedRelevant /\ ChainClosed /\ possKey # accKey)

=====================================================================================
