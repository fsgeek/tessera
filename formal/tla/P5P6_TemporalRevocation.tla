------------------------ MODULE P5P6_TemporalRevocation ------------------------
(***************************************************************************)
(* Tessera Band 0 — P5 (two-sided temporal soundness) and P6 (revocation  *)
(* over the uncertainty window), jointly: they share the temporal          *)
(* vocabulary of A1.6 and P6's whole content is its interaction with       *)
(* P5's window. Authoritative statements: Amendment 1 §A1.2 (P5, P6),      *)
(* §A1.6.                                                                   *)
(*                                                                          *)
(* SCOPE BOUNDARY (explicit): this module discharges the VERIFIER-SIDE    *)
(* face of P5 — the acceptance predicate over declared/anchor/policy.      *)
(* P5's issuance-protocol corollary (anchor confirmed at depth k within    *)
(* delta, re-issue on late/reorged anchors) is ISSUER-side protocol        *)
(* behavior and is NOT modeled here; it is tracked as a separate            *)
(* obligation in formal/PROPERTIES.md. The model takes `anchor` as an      *)
(* already-usable block time — i.e. post-confirmation — which is exactly   *)
(* what the corollary guarantees the verifier may assume.                   *)
(*                                                                          *)
(* Time is abstract small integers (TLC-bounded); DeltaMax and EpsilonMax  *)
(* are scaled-down stand-ins for the ratified 72h/24h strict maxima — the  *)
(* model checks the LOGIC of the window, not the magnitudes. Signature     *)
(* checks are abstracted as passing (that face belongs to the ProVerif    *)
(* models and P4); this module isolates the temporal/authorization face.   *)
(*                                                                          *)
(* Reading guide (Tony):                                                    *)
(*   declared  - declared_issue_time, what the issuer claims (adversarial: *)
(*               unconstrained; a forger declares whatever helps).          *)
(*   signed    - the actual signing moment. NOT observable by the          *)
(*               verifier; it exists in the model so the security          *)
(*               invariant can quantify over what the verifier cannot see. *)
(*   anchor    - Bitcoin block time of the OTS anchor. The one Layer 2     *)
(*               fact: bytes existed not-after anchor, hence signed <=     *)
(*               anchor is a model CONSTRAINT (the anchor assumption, not  *)
(*               a verifier check).                                         *)
(*   revoked   - the key's revocation time; NoRev = never. Lifecycle is    *)
(*               monotonic per P6 (revocation is terminal), which is what  *)
(*               lets one number represent it.                              *)
(*   polDelta, polEps   - the VERIFIER's chosen tolerances; may be         *)
(*               stricter than the strict maxima, never larger (A1.2 P5:   *)
(*               "delta and epsilon belong to the verifier").               *)
(*   rcptDelta, rcptEps - tolerances DECLARED BY THE RECEIPT, adversarial, *)
(*               possibly enormous. The verifier must IGNORE these: they   *)
(*               appear in the state precisely so the invariants can       *)
(*               check that acceptance never depends on them. A future     *)
(*               edit routing them into TemporalOK breaks                   *)
(*               VerifierOwnsTolerances - see the _BrokenTol companion.    *)
(* The verifier sees declared, anchor, revoked, and its own policy —       *)
(* never signed.                                                            *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax

ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax  \* receipts CAN overclaim

NoRev == MaxTime + 1  \* revocation never happens (sorts after all times)

VARIABLES declared, signed, anchor, revoked,
          polDelta, polEps, rcptDelta, rcptEps

(* Every combination the universe permits. The one constraint is the      *)
(* anchor upper-bound assumption: the signed bytes existed when anchored.  *)
Init ==
  /\ declared  \in 0..MaxTime
  /\ anchor    \in 0..MaxTime
  /\ signed    \in 0..anchor         \* Layer 2: existence not-after anchor
  /\ revoked   \in 0..MaxTime \cup {NoRev}
  /\ polDelta  \in 0..DeltaMax       \* verifier may choose stricter, never larger
  /\ polEps    \in 0..EpsilonMax
  /\ rcptDelta \in 0..RcptTolMax     \* adversarial receipt claims, incl. oversized
  /\ rcptEps   \in 0..RcptTolMax

Next == UNCHANGED <<declared, signed, anchor, revoked,
                    polDelta, polEps, rcptDelta, rcptEps>>

(***************************************************************************)
(* The verifier's temporal/authorization checks — over observables only,  *)
(* and over the VERIFIER'S tolerances only. The computation is written    *)
(* with the receipt tolerances as EXPLICIT ARGUMENTS it deliberately      *)
(* ignores: ReceiptIndependence below quantifies over all argument values *)
(* and pins the ignoring. Any future edit that routes receipt tolerances  *)
(* into the window — enlarging (see _BrokenTol) or, subtler,              *)
(* narrowing (see _BrokenTolStrict: issuer-controlled verdict             *)
(* manipulation that every pure safety invariant misses) — breaks it.     *)
(***************************************************************************)

(* P5: two-sided consistency under the verifier's policy. rd/re are the   *)
(* receipt-declared tolerances — unused by design; the signature exists   *)
(* so independence is checkable.                                            *)
TemporalOKWith(rd, re) ==
  /\ anchor >= declared - polEps
  /\ anchor <= declared + polDelta

TemporalOK == TemporalOKWith(rcptDelta, rcptEps)

(* P6: authorization throughout the uncertainty window —                  *)
(*   key_authorized(declared)  i.e. revocation, if any, is after declared *)
(*   AND no revocation effective at or before anchor.                     *)
(* Note both conjuncts are needed: with polEps > 0 the anchor may precede *)
(* declared, so revoked > anchor does not imply revoked > declared.        *)
AuthorizedThroughWindow ==
  /\ revoked > declared
  /\ revoked > anchor

(* The strict-path temporal verdict (this module's face of VALID_STRICT). *)
StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow

StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)

(***************************************************************************)
(* Invariants.                                                              *)
(***************************************************************************)

(* THE P6 SECURITY THEOREM (the round-2 attack, defeated): bytes signed   *)
(* at or after revocation are never strict-accepted — even though the     *)
(* verifier cannot observe the signing time, and under EVERY verifier     *)
(* policy choice. The proof shape: signed <= anchor (Layer 2), so revoked *)
(* <= signed forces revoked <= anchor, which AuthorizedThroughWindow      *)
(* rejects. TLC checks it exhaustively.                                     *)
ForgeryRejected ==
  (revoked <= signed) => ~StrictAccept

(* P5, restated over acceptance: no strict-accepted receipt sits outside  *)
(* the verifier-policy window (backdating bounded by polDelta,            *)
(* post-dating by polEps).                                                  *)
WindowRespected ==
  StrictAccept => (anchor - declared <= polDelta /\ declared - anchor <= polEps)

(* A1.2 P5, "delta and epsilon belong to the verifier, not the receipt":  *)
(* acceptance NEVER exceeds the strict maxima, whatever tolerances the    *)
(* receipt declares. In this (correct) model rcptDelta/rcptEps are        *)
(* ignored, so this holds; the _BrokenTol companion routes them into the  *)
(* window and TLC exhibits a receipt-enlarged acceptance violating it.    *)
VerifierOwnsTolerances ==
  StrictAccept =>
    (anchor - declared <= DeltaMax /\ declared - anchor <= EpsilonMax)

(* Full noninterference, "ignore receipt tolerances" taken literally: the *)
(* verdict is IDENTICAL under every receipt-declared tolerance pair — not *)
(* merely bounded by the maxima. This is strictly stronger than           *)
(* VerifierOwnsTolerances: a bug giving the receipt a NARROWING influence *)
(* (effective window = min of policy and receipt) passes every safety     *)
(* invariant above — acceptance stays inside the maxima — yet hands the   *)
(* issuer control over other parties' verification outcomes. Only this    *)
(* invariant catches it (_BrokenTolStrict).                                *)
ReceiptIndependence ==
  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    StrictAcceptWith(rd, re) <=> StrictAccept

(* P6 second clause standing alone: acceptance implies the key was        *)
(* authorized at the declared issue time itself.                           *)
AuthorizedAtDeclared ==
  StrictAccept => declared < revoked

(* P6 fail-closed cost, made exact (not just accepted rhetorically): the  *)
(* ONLY honest receipts the interval rule sacrifices are those whose key  *)
(* was revoked inside (declared, anchor] — signed before revocation       *)
(* (honest) but revoked before the anchor confirmed. Everything else      *)
(* honest is accepted if temporally consistent.                            *)
HonestCostIsExactlyTheWindow ==
  (/\ TemporalOK
   /\ signed < revoked          \* honestly signed while authorized
   /\ revoked > declared        \* authorized at declaration too
   /\ ~StrictAccept)
  => (revoked <= anchor)        \* ...then revocation landed in the window

(* Vacuity checks — used ONLY by the _Sanity cfg (run with TLC            *)
(* -continue), where TLC VIOLATING both is the healthy result: each       *)
(* violation exhibits a reachable state satisfying a defined-predicate    *)
(* antecedent, so the implications above are not vacuously true.           *)
AcceptanceUnreachable == ~StrictAccept
HonestCostCaseUnreachable ==
  ~(/\ TemporalOK
    /\ signed < revoked
    /\ revoked > declared
    /\ ~StrictAccept)

=================================================================================
