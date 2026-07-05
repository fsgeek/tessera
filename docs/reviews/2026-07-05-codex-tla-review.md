# Review: Band 0 TLA+ models (P4, P5/P6), Codex

Review artifact for the Band 0 TLA+ working material (`formal/tla/`),
same archive-and-disposition discipline as prior reviews. Reviewer: Codex
(OpenAI). Date: 2026-07-05. The reviewer independently reran TLC on the
main, broken, and sanity configurations and reproduced all results,
including the round-2 attack state in the broken P6 model.

## Disposition summary (author + AI collaborator, 2026-07-05)

1. **Verifier-owned tolerances not modeled (Medium) — confirmed, fixed.**
   The P5/P6 model used fixed Delta/Epsilon constants, so it could not
   catch an implementation honoring receipt-declared tolerances — the
   exact bug A1.2 P5 forbids. The model now carries the verifier's chosen
   policy (`polDelta <= DeltaMax`, `polEps <= EpsilonMax`; stricter
   allowed, never larger, by construction) AND adversarial
   receipt-declared tolerances (`rcptDelta`, `rcptEps`, up to oversized
   values). A new invariant `VerifierOwnsTolerances` asserts acceptance
   never exceeds the strict maxima whatever the receipt declares; a new
   broken companion (`_BrokenTol`) routes the receipt tolerances into the
   window (effective = max(policy, receipt)) and TLC exhibits the
   receipt-enlarged acceptance: `polDelta = 0, rcptDelta = 4, declared =
   0, anchor = 4` — accepted 4 units outside the verifier's window.
   All prior invariants (ForgeryRejected etc.) now also quantify over
   every verifier policy choice.
2. **P4 one-way implications, not exact classification (Medium) —
   confirmed, fixed.** An over-conservative verdict function (e.g.,
   everything INVALID) would have passed every safety implication.
   Four iff-form invariants added (`ExactInvalid`, `ExactUnverifiable`,
   `ExactStrict`, `ExactDegraded`) whose right-hand sides partition all
   outcomes; the classification is now pinned in both directions against
   future drift of `VerdictFor`. TLC green over the full enumeration.
3. **Issuance corollary (depth k, re-issue) not represented (Low) —
   confirmed; resolved by explicit boundary, not by modeling.** The
   module discharges the VERIFIER-side face of P5 — the acceptance
   predicate. The issuance-protocol corollary is issuer-side behavior;
   the model takes `anchor` as an already-usable (post-confirmation)
   block time, which is precisely what the corollary guarantees the
   verifier may assume. The boundary is now stated in the module header,
   and the corollary is tracked as a separate open obligation in
   `formal/PROPERTIES.md` so it cannot silently vanish. (Scope decision:
   author ratification pending.)
4. **Stale .out relative to .tla (Low) — confirmed, fixed.** All seven
   evidence files regenerated in one pass from the final sources; the
   regeneration command set is recorded in each file's TLC banner.

## Full review text (verbatim)

Findings

- Medium: P5's "verifier-owned tolerances" rule is not modeled.
  formal/tla/P5P6_TemporalRevocation.tla:32 uses fixed Delta/Epsilon
  constants directly in TemporalOK, but the amendment explicitly says
  receipts must not choose their own tolerances and degraded policy must
  not enlarge them. This model proves the arithmetic window, but it
  cannot catch an implementation/spec bug where the receipt supplies an
  oversized window. Strengthen by adding receipt-declared tolerances and
  verifier-policy tolerances, then prove acceptance depends only on
  verifier policy and rejects receipt-chosen enlargement.

- Medium: P4 checks mostly one-way safety implications, not the full
  exact verdict partition. The definition in
  formal/tla/P4_VerifierStates.tla:56 is reasonable, but the invariants
  would not fully protect against an over-conservative or misclassified
  verdict function if the definition later changed. For example, add
  iff-style properties such as: any required fail iff INVALID; no
  required fail plus required unperformable iff UNVERIFIABLE; no waiver
  plus all checks pass iff VALID_STRICT; nonempty waiver plus all
  required checks pass iff VALID_DEGRADED. The current sanity cfg proves
  all verdicts are reachable, which helps, but does not prove exact
  classification.

- Low: P5's issuance corollary around confirmation depth k and re-issue
  on late/reorged anchors is not represented in the TLA+ model.
  formal/tla/P5P6_TemporalRevocation.tla:21 abstracts anchor as already
  usable block time and assumes signed <= anchor; that is fine for the
  verifier-side temporal check, but it does not model "confirmed at
  depth k within δ" from the amendment. If this artifact is meant to
  discharge only verifier acceptance, document that boundary explicitly.
  If it is meant to cover P5 end-to-end, add confirmation depth/status
  or a separate issuance model.

- Low: formal/tla/P5P6_TemporalRevocation.out appears stale relative to
  the .tla file timestamp. I reran TLC successfully, so this is artifact
  hygiene, not a model failure.

Validation

I ran TLC on the main, broken, and sanity configs. Main P4 and P5/P6
pass. The broken P4 model fails on StrictMeansEverything as intended.
The broken P5/P6 model fails ForgeryRejected with declared = 0, revoked
= 1, signed = 1, anchor = 1, which is exactly the point-evaluated
revocation bug. Sanity configs show the expected reachable
verdict/acceptance cases.

Overall: the models are valid for the scoped arithmetic/state-machine
claims they currently encode. The best strengthening is to make the P4
verdict partition exact and to model verifier-owned temporal policy
rather than only fixed constants.
