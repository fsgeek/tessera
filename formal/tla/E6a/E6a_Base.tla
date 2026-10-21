------------------------------ MODULE E6a_Base ------------------------------
(***************************************************************************)
(* Tessera, exit item E6a (A9 §A9.2; A3 §A3.6.2 items 2 and 3).            *)
(* STATUS: PROPOSED, 2026-10-19, produced by the AI collaborator (owner   *)
(* work, Claude Opus 5.5); not adopted; the commit is the author's.       *)
(*                                                                         *)
(* Shared inputs for the E6a family. Nothing here decides a verdict.      *)
(* The verdict modules (E6a_AlgVerdict and its _Broken companions) EXTEND *)
(* this module; E6a_Props states the invariants once, so every companion  *)
(* is checked against the same formulas (the P4 _Broken copy drifted to    *)
(* seven of eleven invariants: 2026-09-06 review item 5).                  *)
(*                                                                         *)
(* What one state is: one presented input to the verifier, abstracted to  *)
(*   dispatch  -- did the input pass profile dispatch ("in") or not       *)
(*                ("out": unknown profile label, bad layer structure,      *)
(*                unsupported request; V1-PROFILE §3.1 D1-D4)              *)
(*   alg[s]    -- per signature slot, the algorithm identifier's form      *)
(*                (A3 §A3.6.2 item 2's list, below)                        *)
(*   sig[s]    -- per slot, the signature: absent, present but not         *)
(*                verifying, present and verifying                         *)
(*   ev[e]     -- per required evidence member: absent, present and        *)
(*                failing, present and passing                             *)
(*   waived    -- the verifier's declared waiver set (A1.2.1). V1 is       *)
(*                strict-only, so its configuration has no waivable check. *)
(* The verdict is DERIVED from these by the verdict modules; it is never  *)
(* stored, as in P4.                                                       *)
(***************************************************************************)
EXTENDS FiniteSets

CONSTANTS
  Slots,       \* signature slots named by the signed manifest (V1: kms, gpg)
  EvItems,     \* required evidence members (abstract; V1: e.g. the DNS and git channels)
  WaivableEv   \* evidence members a degraded policy may waive (A1.2.1, P10); V1: {}

ASSUME WaivableEv \subseteq EvItems

(* A3 §A3.6.2 item 2, exact. "supported" is the catalog-supported id.     *)
(* "unsupported" is the ONE UNVERIFIABLE case: a well-formed, correctly    *)
(* bound, but unsupported identifier. The other five are the registered   *)
(* INVALID list: missing identifier; identifier/signature encoding        *)
(* mismatch; malformed parameters; identifier prohibited by policy;       *)
(* substitution of the signed identifier. (The sixth INVALID item, "a     *)
(* known algorithm whose signature fails", is alg = "supported" with       *)
(* sig = "bad".)                                                           *)
AlgForms == {"supported", "unsupported",
             "missing", "encoding_mismatch", "malformed", "prohibited",
             "substituted"}
InvalidAlgForms == AlgForms \ {"supported", "unsupported"}

SigForms      == {"absent", "bad", "good"}
EvForms       == {"absent", "bad", "good"}
DispatchForms == {"in", "out"}

(* The checks the verifier performs on a dispatched input. Each slot has   *)
(* an algorithm check and a signature check; each evidence member one      *)
(* check. These are the P4 module's abstract `Checks`, made concrete.      *)
AlgCheck(s) == <<"alg", s>>
SigCheck(s) == <<"sig", s>>
EvCheck(e)  == <<"ev", e>>

AlgChecks == {AlgCheck(s) : s \in Slots}
SigChecks == {SigCheck(s) : s \in Slots}
EvChecks  == {EvCheck(e) : e \in EvItems}
AllChecks == AlgChecks \cup SigChecks \cup EvChecks

(* A1.2.1: identifier binding and signature verification (P3, P8) are    *)
(* non-waivable; only declared redundancy (here: an authority-evidence     *)
(* channel, P10) may be waived. Waiving a whole signature slot (P2's       *)
(* degraded subset) is NOT modelled; V1 has no waivers at all.             *)
WaivableChecks    == {EvCheck(e) : e \in WaivableEv}
NonWaivableChecks == AllChecks \ WaivableChecks

Statuses == {"pass", "fail", "unperformable"}
Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}

(* Reason classes, abstracted from V1-PROFILE §15.7's codes:              *)
(*   OUT_OF_PROFILE -- rows 1.1-1.4 (dispatch)                             *)
(*   FAILED         -- any INVALID code (the model does not pick which)    *)
(*   MEMBER_MISSING -- row 2.2 (a required member absent)                  *)
(*   ALG_UNKNOWN    -- row 7.1                                             *)
(*   OK             -- success                                             *)
(* Row 2.2 precedes row 7.1 in the total check order, so an input with    *)
(* both an absent member and an unknown alg, and no failure, reports      *)
(* MEMBER_MISSING (conformance case AGG-d).                                *)
Reasons == {"OUT_OF_PROFILE", "FAILED", "MEMBER_MISSING", "ALG_UNKNOWN", "OK"}

VARIABLES dispatch, alg, sig, ev, waived

inputs == <<dispatch, alg, sig, ev, waived>>

(* Every combination of inputs and every legal policy. As in P4, a policy *)
(* naming a non-waivable check is not in the enumeration (excluded, not   *)
(* rejected; READING-AID-P4).                                              *)
Init ==
  /\ dispatch \in DispatchForms
  /\ alg      \in [Slots -> AlgForms]
  /\ sig      \in [Slots -> SigForms]
  /\ ev       \in [EvItems -> EvForms]
  /\ waived   \in SUBSET WaivableChecks

Next == UNCHANGED inputs

Required == AllChecks \ waived

(***************************************************************************)
(* Shared derivation helpers. A verdict module supplies a status map `st` *)
(* (one status per check); these turn it into a verdict and a reason.     *)
(* The in-profile verdict is P4's own VerdictFor, instantiated on the     *)
(* derived status map: P4 is reused, not restated, and its file is not    *)
(* edited.                                                                 *)
(***************************************************************************)
LOCAL P4(st) == INSTANCE P4_VerifierStates
                  WITH Checks      <- AllChecks,
                       NonWaivable <- NonWaivableChecks,
                       status      <- st,
                       waived      <- waived

(* Dispatch is terminal (A9.5; V1-PROFILE §3.1): an out-of-profile input  *)
(* is UNVERIFIABLE and nothing else is evaluated. Inside, P4 decides.     *)
VerdictFrom(st) ==
  IF dispatch = "out" THEN "UNVERIFIABLE" ELSE P4(st)!VerdictFor(waived)

P4VerdictOf(st) == P4(st)!VerdictFor(waived)

ReasonFrom(st) ==
  IF dispatch = "out" THEN "OUT_OF_PROFILE"
  ELSE IF \E c \in Required : st[c] = "fail" THEN "FAILED"
  ELSE IF \E c \in Required \cap EvChecks : st[c] = "unperformable"
    THEN "MEMBER_MISSING"
  ELSE IF \E c \in Required \cap (AlgChecks \cup SigChecks) :
            st[c] = "unperformable"
    THEN "ALG_UNKNOWN"
  ELSE "OK"

=============================================================================
