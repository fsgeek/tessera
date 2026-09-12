------------------------ MODULE P5P6_TemporalRevocation ------------------------
(***************************************************************************)
(* Tessera Band 0 — P5 (two-sided temporal soundness) and P6 (revocation  *)
(* over the uncertainty window), jointly: they share the temporal          *)
(* vocabulary of A1.6 and P6's whole content is its interaction with       *)
(* P5's window. Authoritative statements: Amendment 1 §A1.2 (P5, P6),      *)
(* §A1.6.                                                                   *)
(*                                                                          *)
(* SCOPE BOUNDARY (revised by Amendment 2): this module discharges the    *)
(* VERIFIER-SIDE face of P5 — the acceptance predicate over declared/      *)
(* anchor/confirmedAt/policy. P5's issuance-protocol corollary (ship       *)
(* rule, re-issue, attempt bound) remains ISSUER-side behavior, modeled    *)
(* in P5c_IssuanceProtocol. Amendment 2 (A2.2) gave the corollary a        *)
(* verifier-checkable face — the confirmation-timing conjunct              *)
(* confirmedAt <= declared + delta — and that face lives HERE: it is the   *)
(* same predicate the issuer's Ship rule evaluates (A2.1, one predicate    *)
(* on one chain-visible observable, both sides), so the correspondence     *)
(* between this module's acceptance and P5c's Ship is exact by             *)
(* construction, not by argument.                                           *)
(*                                                                          *)
(* CORRECTION 2026-09-06 (cross-family falsification review, Codex          *)
(* gpt-6-astra;                                                             *)
(* docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md items 8,  *)
(* 12, and Amendment 4 §A4.3; entered by the AI collaborator, PROPOSED, not *)
(* adopted; the header above is left as written per amend-don't-rewrite):   *)
(* - Item 12: "exact by construction, not by argument" (above) predates the *)
(*   bridge model and overstates. The correspondence between this module's  *)
(*   acceptance and P5c's Ship was ASSERTED in comments and checked nowhere *)
(*   until P5cP5P6_Bridge.tla (2026-07-21) checked it as the invariant      *)
(*   ShippedDesignatedAgree — for a shipped receipt, the designated block   *)
(*   and timestamp the issuer's Ship guard evaluated are the ones the       *)
(*   verifier derives from the shipped headers — with the                   *)
(*   _BrokenAnchorSubst companion red (verifier reads the inclusion-block   *)
(*   timestamp instead). Under P5c's single fused clock the two guards      *)
(*   merely coincide; the checked join is the bridge's, and the reader is   *)
(*   sent there.                                                            *)
(* - Item 8: VerifierOwnsTolerances compares the accepted gaps against the  *)
(*   GLOBAL maxima (DeltaMax, EpsilonMax), not against the verifier's       *)
(*   chosen policy; a receipt-driven enlargement from polDelta = 0 to an    *)
(*   effective 1 under DeltaMax = 3 passes it. Ownership in the policy      *)
(*   sense is carried by ReceiptIndependence (verdict identical under every *)
(*   receipt-tolerance pair), and the _BrokenTolStrict companion shows      *)
(*   exactly that division of labour. See also the qualified comment at     *)
(*   ReceiptIndependence.                                                   *)
(* - Amendment 4 §A4.3: AuthorizedAtDeclared's second conjunct, revoked >   *)
(*   declared, is the registered two-conjunct rule; Amendment 1's looser    *)
(*   sentence "revocation effective after anchor_time does not              *)
(*   retroactively change the verdict" is written by §A4.3 as "after both   *)
(*   anchor_time and declared_issue_time". See the comment at               *)
(*   AuthorizedAtDeclared.                                                  *)
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
(*   confirmedAt - timestamp of the block granting the k-th confirmation  *)
(*               (height h+k-1; A2.1). Chain-visible to issuer and        *)
(*               verifier alike. Deliberately UNCONSTRAINED relative to   *)
(*               anchor: block timestamps are not monotonic (A2.1), so    *)
(*               confirmedAt < anchor is a legal state and the model      *)
(*               assumes no ordering.                                      *)
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
(* The verifier sees declared, anchor, confirmedAt, revoked, and its own   *)
(* policy — never signed.                                                   *)
(***************************************************************************)
EXTENDS Integers

CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax

ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax  \* receipts CAN overclaim

NoRev == MaxTime + 1  \* revocation never happens (sorts after all times)

VARIABLES declared, signed, anchor, confirmedAt, revoked,
          polDelta, polEps, rcptDelta, rcptEps

(* Every combination the universe permits. The one constraint is the      *)
(* anchor upper-bound assumption: the signed bytes existed when anchored.  *)
(* confirmedAt carries NO constraint relative to anchor — non-monotonic   *)
(* block timestamps, A2.1.                                                  *)
Init ==
  /\ declared  \in 0..MaxTime
  /\ anchor    \in 0..MaxTime
  /\ confirmedAt \in 0..MaxTime
  /\ signed    \in 0..anchor         \* Layer 2: existence not-after anchor
  /\ revoked   \in 0..MaxTime \cup {NoRev}
  /\ polDelta  \in 0..DeltaMax       \* verifier may choose stricter, never larger
  /\ polEps    \in 0..EpsilonMax
  /\ rcptDelta \in 0..RcptTolMax     \* adversarial receipt claims, incl. oversized
  /\ rcptEps   \in 0..RcptTolMax

Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
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

(* P5: two-sided consistency under the verifier's policy, plus the A2.2   *)
(* confirmation-timing conjunct (third line) — the verifier-checkable     *)
(* face of the issuance corollary, on the verifier's OWN delta. rd/re are *)
(* the receipt-declared tolerances — unused by design; the signature      *)
(* exists so independence is checkable.                                     *)
TemporalOKWith(rd, re) ==
  /\ anchor >= declared - polEps
  /\ anchor <= declared + polDelta
  /\ confirmedAt <= declared + polDelta   \* A2.2: k-th confirmation in-window

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
  StrictAccept => (/\ anchor - declared <= polDelta
                   /\ declared - anchor <= polEps
                   /\ confirmedAt - declared <= polDelta)

(* A1.2 P5, "delta and epsilon belong to the verifier, not the receipt":  *)
(* acceptance NEVER exceeds the strict maxima, whatever tolerances the    *)
(* receipt declares. In this (correct) model rcptDelta/rcptEps are        *)
(* ignored, so this holds; the _BrokenTol companion routes them into the  *)
(* window and TLC exhibits a receipt-enlarged acceptance violating it.    *)
VerifierOwnsTolerances ==
  StrictAccept =>
    (/\ anchor - declared <= DeltaMax
     /\ declared - anchor <= EpsilonMax
     /\ confirmedAt - declared <= DeltaMax)

(* THE A2.0 ARTIFACT, REJECTED (Amendment 2): an anchor whose block is    *)
(* in-window but whose k-th confirmation arrived past the window — the    *)
(* discarded-attempt artifact that strict issuance never ships but whose  *)
(* transaction typically confirms anyway. The pre-A2 verifier             *)
(* (anchor-only checks) accepts it; the _BrokenConf companion carries     *)
(* that verifier, passes every anchor-only invariant, and violates        *)
(* exactly this one.                                                        *)
AbandonedArtifactRejected ==
  (/\ anchor >= declared - polEps
   /\ anchor <= declared + polDelta
   /\ confirmedAt > declared + polDelta)
  => ~StrictAccept

(* Full noninterference, "ignore receipt tolerances" taken literally: the *)
(* verdict is IDENTICAL under every receipt-declared tolerance pair — not *)
(* merely bounded by the maxima. This is strictly stronger than           *)
(* VerifierOwnsTolerances: a bug giving the receipt a NARROWING influence *)
(* (effective window = min of policy and receipt) passes every safety     *)
(* invariant above — acceptance stays inside the maxima — yet hands the   *)
(* issuer control over other parties' verification outcomes. Only this    *)
(* invariant catches it (_BrokenTolStrict).                                *)
(* CORRECTION 2026-09-06 (review item 8): "strictly stronger" holds only    *)
(* for receipt INFLUENCE — independence catches enlargement and narrowing   *)
(* alike, where VerifierOwnsTolerances catches enlargement past the maxima  *)
(* only. It is NOT logically stronger than VerifierOwnsTolerances: an       *)
(* acceptance predicate that ignores its receipt arguments could still      *)
(* accept outside the maxima (e.g. a predicate that hard-codes a bound      *)
(* larger than DeltaMax and ignores its receipt arguments; Init bounds      *)
(* polDelta \in 0..DeltaMax, so no STATE of this model is the example — the *)
(* example is a predicate) and pass this invariant. The two are             *)
(* complementary; the correct module checks both.                           *)
ReceiptIndependence ==
  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    StrictAcceptWith(rd, re) <=> StrictAccept

(* P6 second clause standing alone: acceptance implies the key was        *)
(* authorized at the declared issue time itself.                           *)
(* Amendment 4 §A4.3 (2026-09-06): when the anchor precedes the declared    *)
(* time (possible within epsilon), a revocation after the anchor but at or  *)
(* before the declared time still invalidates — this conjunct says so, and  *)
(* §A4.3 writes Amendment 1's "after anchor_time" sentence as "after both   *)
(* anchor_time and declared_issue_time" to match. Boundary (review item     *)
(* 13): declared < revoked stands in for key_authorized(declared); no       *)
(* activation time is modelled (lifecycle deferred, docket items 18, 26).   *)
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
NonMonotonicAcceptUnreachable ==      \* accepted with confirmedAt < anchor:
  ~(StrictAccept /\ confirmedAt < anchor)  \* non-monotonicity (A2.1) exercised
AcceptanceUnreachable == ~StrictAccept
LateBurialCaseUnreachable ==          \* the A2.0 artifact is reachable, so
  ~(/\ anchor >= declared - polEps    \* AbandonedArtifactRejected is not vacuous
    /\ anchor <= declared + polDelta
    /\ confirmedAt > declared + polDelta)
HonestCostCaseUnreachable ==
  ~(/\ TemporalOK
    /\ signed < revoked
    /\ revoked > declared
    /\ ~StrictAccept)

=================================================================================
