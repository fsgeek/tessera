------------------------------ MODULE E6a_Props ------------------------------
(***************************************************************************)
(* Tessera, exit item E6a: the invariants, stated once.                   *)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(*                                                                         *)
(* Every verdict module (correct and broken) instantiates this module     *)
(* with its own derived status map, verdict and reason:                    *)
(*   INSTANCE E6a_Props WITH statusMap <- DerivedStatus,                   *)
(*                           verdictV  <- Verdict, reasonV <- Reason       *)
(* so the formulas a companion is checked against are, by construction,  *)
(* the formulas the correct module is checked against.                    *)
(*                                                                         *)
(* The invariants speak about the RAW INPUTS (alg, sig, ev), not about    *)
(* the status map. That is the point of E6a: a verifier that classifies   *)
(* an unknown algorithm as "pass" produces a status map on which all of   *)
(* P4's eleven invariants still hold (group F below), because P4 checks   *)
(* the verdict FUNCTION, not the classification of inputs into check      *)
(* outcomes. E6a adds the classification.                                 *)
(***************************************************************************)

CONSTANTS Slots, EvItems, WaivableEv
VARIABLES dispatch, alg, sig, ev, waived, statusMap, verdictV, reasonV

LOCAL B  == INSTANCE E6a_Base
LOCAL P4 == INSTANCE P4_VerifierStates
              WITH Checks      <- B!AllChecks,
                   NonWaivable <- B!NonWaivableChecks,
                   status      <- statusMap,
                   waived      <- waived

(***************************************************************************)
(* Input-level facts: the registered boundary, read off the inputs.       *)
(***************************************************************************)
InP == dispatch = "in"

ReqEv(e) == B!EvCheck(e) \in B!Required

(* A definite defect: something a required check must FAIL on.           *)
(* A3 §A3.6.2 item 2's INVALID list; A9 C3 ("a missing, stripped or       *)
(* substituted [signature] fails"); a required evidence member present    *)
(* and failing.                                                            *)
AlgDefect(s) == alg[s] \in B!InvalidAlgForms
SigDefect(s) == \/ sig[s] = "absent"
                \/ (alg[s] = "supported" /\ sig[s] = "bad")
EvDefect(e)  == ReqEv(e) /\ ev[e] = "bad"
AnyDefect    == \/ \E s \in Slots : AlgDefect(s) \/ SigDefect(s)
                \/ \E e \in EvItems : EvDefect(e)

(* The one UNVERIFIABLE algorithm case, and missing evidence.             *)
Unknown(s)   == alg[s] = "unsupported"
AnyUnknown   == \E s \in Slots : Unknown(s)
EvMissing(e) == ReqEv(e) /\ ev[e] = "absent"
AnyEvMissing == \E e \in EvItems : EvMissing(e)

(* Everything required present and passing.                               *)
AllClean ==
  /\ \A s \in Slots : alg[s] = "supported" /\ sig[s] = "good"
  /\ \A e \in EvItems : ReqEv(e) => ev[e] = "good"

(***************************************************************************)
(* Group A. Dispatch (A9.5; V1-PROFILE §3.1).                             *)
(***************************************************************************)
DispatchTerminal ==
  dispatch = "out" => (verdictV = "UNVERIFIABLE" /\ reasonV = "OUT_OF_PROFILE")

OutOfProfileOnlyAtDispatch ==
  reasonV = "OUT_OF_PROFILE" => dispatch = "out"

(***************************************************************************)
(* Group B. The transition (A3 §A3.6.2 items 2 and 3).                    *)
(***************************************************************************)
(* The registered transition: a well-formed, correctly bound, unsupported *)
(* identifier, with nothing definitely failed, gives UNVERIFIABLE.        *)
UnknownAlgGivesUnverifiable ==
  (InP /\ AnyUnknown /\ ~AnyDefect) => verdictV = "UNVERIFIABLE"

(* The fail-open companion's target: an unknown algorithm never yields    *)
(* any VALID state, under any legal policy, whatever else holds.          *)
UnknownAlgNeverValid ==
  (InP /\ AnyUnknown) => verdictV \in {"INVALID", "UNVERIFIABLE"}

(* The registered INVALID list for the identifier.                        *)
InvalidAlgFormsGiveInvalid ==
  (InP /\ \E s \in Slots : AlgDefect(s)) => verdictV = "INVALID"

(* "A known algorithm whose signature fails" is INVALID.                  *)
KnownAlgBadSigInvalid ==
  (InP /\ \E s \in Slots : alg[s] = "supported" /\ sig[s] = "bad")
    => verdictV = "INVALID"

(* "UNVERIFIABLE for exactly one case", in reason form: the ALG_UNKNOWN   *)
(* reason is reported iff an unknown id is present, nothing failed, and   *)
(* no earlier-ordered unperformable reason (an absent member) applies.    *)
AlgUnknownReasonExact ==
  (reasonV = "ALG_UNKNOWN") <=>
    (InP /\ AnyUnknown /\ ~AnyDefect /\ ~AnyEvMissing)

(***************************************************************************)
(* Group C. Mixed failed / unperformable (A4 §A4.2 precedence, kept       *)
(* inside the profile: Codex review of the V1 derivation, finding 11).    *)
(***************************************************************************)
MixedFailedUnknownInvalid ==
  (InP /\ AnyDefect /\ AnyUnknown) => (verdictV = "INVALID" /\ reasonV = "FAILED")

MixedFailedMissingEvidenceInvalid ==
  (InP /\ AnyDefect /\ AnyEvMissing) => (verdictV = "INVALID" /\ reasonV = "FAILED")

(***************************************************************************)
(* Group D. Missing signature versus missing evidence (Codex finding 11: *)
(* "Missing required signatures and missing required authority evidence   *)
(* also have different registered meanings").                             *)
(***************************************************************************)
(* A9 C3: a missing or stripped required signature FAILS -- INVALID under *)
(* every policy, whatever the algorithm (conformance ALG-02: unknown alg  *)
(* with an empty signature is INVALID / SIG_EMPTY).                        *)
MissingSignatureInvalid ==
  (InP /\ \E s \in Slots : sig[s] = "absent") => verdictV = "INVALID"

(* A missing required evidence member is UNPERFORMABLE, not a failure:    *)
(* alone it gives UNVERIFIABLE / MEMBER_MISSING (case d2).                *)
MissingEvidenceUnverifiable ==
  (InP /\ AnyEvMissing /\ ~AnyDefect)
    => (verdictV = "UNVERIFIABLE" /\ reasonV = "MEMBER_MISSING")

(* ...and never VALID.                                                     *)
MissingEvidenceNeverValid ==
  (InP /\ AnyEvMissing) => verdictV \in {"INVALID", "UNVERIFIABLE"}

(* Absence is not failure: INVALID only from a definite defect.           *)
InvalidNeedsDefect ==
  verdictV = "INVALID" => (InP /\ AnyDefect)

(***************************************************************************)
(* Group E. Exact classification on the inputs (both directions, so an   *)
(* over-conservative verdict cannot pass; the P4 Exact* pattern).         *)
(***************************************************************************)
TypeOK ==
  /\ verdictV \in B!Verdicts
  /\ reasonV  \in B!Reasons
  /\ statusMap \in [B!AllChecks -> B!Statuses]

ReasonMatchesVerdict ==
  /\ (reasonV = "OK")     <=> (verdictV \in {"VALID_STRICT", "VALID_DEGRADED"})
  /\ (reasonV = "FAILED") <=> (verdictV = "INVALID")
  /\ (reasonV \in {"OUT_OF_PROFILE", "MEMBER_MISSING", "ALG_UNKNOWN"})
       <=> (verdictV = "UNVERIFIABLE")

ExactInvalidIn ==
  InP => ((verdictV = "INVALID") <=> AnyDefect)

ExactUnverifiableIn ==
  InP => ((verdictV = "UNVERIFIABLE") <=>
            (~AnyDefect /\ (AnyUnknown \/ AnyEvMissing)))

ExactStrictIn ==
  InP => ((verdictV = "VALID_STRICT") <=> (waived = {} /\ AllClean))

ExactDegradedIn ==
  InP => ((verdictV = "VALID_DEGRADED") <=> (waived # {} /\ AllClean))

(* V1 is strict-only: with no waivable check, VALID_DEGRADED is unreachable. *)
NoDegradedWithoutWaivable ==
  WaivableEv = {} => verdictV # "VALID_DEGRADED"

(***************************************************************************)
(* Group F. Agreement with P4, and P4's own invariants on the derived     *)
(* status map. F1 says the in-profile verdict IS P4's VerdictFor; the     *)
(* P4_* formulas are P4_VerifierStates' eleven, evaluated on statusMap.   *)
(* A companion that mis-classifies inputs leaves group F green: P4 alone  *)
(* cannot see that defect.                                                *)
(***************************************************************************)
AgreesWithP4 == InP => verdictV = P4!VerdictFor(waived)

P4_Partition                 == P4!Partition
P4_Monotonicity              == P4!Monotonicity
P4_NoSilentPromotion         == P4!NoSilentPromotion
P4_ValidNeedsNonWaivablePass == P4!ValidNeedsNonWaivablePass
P4_StrictMeansEverything     == P4!StrictMeansEverything
P4_DegradedNeedsExplicitWaiver == P4!DegradedNeedsExplicitWaiver
P4_UnverifiableIsHonest      == P4!UnverifiableIsHonest
P4_ExactInvalid              == P4!ExactInvalid
P4_ExactUnverifiable         == P4!ExactUnverifiable
P4_ExactStrict               == P4!ExactStrict
P4_ExactDegraded             == P4!ExactDegraded

(***************************************************************************)
(* Vacuity witnesses: used ONLY by the _Sanity runs, where a VIOLATION is *)
(* the healthy result (the situation is reachable, so the implications   *)
(* above are not vacuously true). Each maps to a conformance case shape.  *)
(***************************************************************************)
NeverInStrict      == ~(InP /\ verdictV = "VALID_STRICT")            \* A-a
NeverInDegraded    == ~(InP /\ verdictV = "VALID_DEGRADED")          \* general cfg only
NeverInInvalid     == ~(InP /\ verdictV = "INVALID")
NeverOutOfProfile  == reasonV # "OUT_OF_PROFILE"                     \* L-01..L-06
NeverAlgUnknown    == reasonV # "ALG_UNKNOWN"                        \* ALG-01, L-21
NeverUnknownOpaqueBadSig ==                                          \* HY-b2-H
  ~(InP /\ reasonV = "ALG_UNKNOWN" /\ \E s \in Slots : Unknown(s) /\ sig[s] = "bad")
NeverMixedFailedUnknown == ~(InP /\ AnyDefect /\ AnyUnknown)          \* L-107
NeverUnknownEmptySig ==                                              \* ALG-02
  ~(InP /\ \E s \in Slots : Unknown(s) /\ sig[s] = "absent")
NeverMissingSignature == ~(InP /\ \E s \in Slots : sig[s] = "absent")
NeverMemberMissing == reasonV # "MEMBER_MISSING"                     \* L-09, L-10
NeverMissingEvPlusUnknown ==                                         \* AGG-d
  ~(InP /\ ~AnyDefect /\ AnyEvMissing /\ AnyUnknown)
NeverDefectPlusMissingEv == ~(InP /\ AnyDefect /\ AnyEvMissing)       \* A-d3
NeverWaivedAbsentDegraded ==                                         \* general cfg only
  ~(InP /\ verdictV = "VALID_DEGRADED" /\ \E e \in EvItems : ev[e] = "absent")

=============================================================================
