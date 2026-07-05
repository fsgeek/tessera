# Review: Band 0 TLA+ models, Codex, round 2

Review artifact, same discipline as prior rounds. Reviewer: Codex
(OpenAI), reviewing the revisions produced by its own round-1 findings
(`2026-07-05-codex-tla-review.md`). Date: 2026-07-05. The reviewer
independently reran TLC across all seven configurations then existing and
reproduced every result.

## Disposition summary (author + AI collaborator, 2026-07-05)

1. **"Acceptance never depends on receipt tolerances" overclaimed (Low)
   — confirmed, and resolved by strengthening the model rather than
   softening the comment.** Codex was right that
   `VerifierOwnsTolerances`/`WindowRespected` prove only bounded
   acceptance, not noninterference — and the gap is real, not
   rhetorical: a bug giving receipt tolerances a NARROWING influence
   (effective window = min(policy, receipt)) passes every safety
   invariant while handing the issuer control over other parties'
   verification outcomes (issuer-selected verdict manipulation). The
   amendment's "delta and epsilon belong to the verifier" is meant
   literally, so:
   - the acceptance computation is refactored to take the receipt
     tolerances as explicit (deliberately ignored) arguments
     (`StrictAcceptWith(rd, re)`);
   - a new `ReceiptIndependence` invariant quantifies over all receipt
     tolerance pairs and asserts the verdict is identical — full
     noninterference, strictly stronger than the safety bounds;
   - a third broken variant (`_BrokenTolStrict`, the min-window bug)
     demonstrates the invariant is load-bearing: TLC shows all three
     safety invariants HOLD on it while `ReceiptIndependence` is
     violated (`polDelta = 1, rcptDelta = 0, declared = 0, anchor = 1` —
     the receipt's narrowed window flips an accept to a reject).
   The enlarging variant (`_BrokenTol`) was refactored to the same
   parameterized shape for apples-to-apples parity.
2. **P5 tracker row ambiguity (Low) — confirmed, fixed.** The tracker
   now splits P5 (verifier side, `P5P6_TemporalRevocation.tla`) from
   P5c (issuance corollary, `P5c_IssuanceProtocol.tla`) as separate
   rows, each with its artifact.

Round-1 items re-verified by the reviewer as addressed: P4 exact
classification (iff invariants); verifier-owned tolerance maxima with
the enlarging broken variant; the issuance corollary as a real state
machine with the shallow-ship/reorg counterexample.

## Full review text (verbatim)

Findings

- Low: The P5/P6 model now prevents receipt-enlarged acceptance, but the
  comment slightly overclaims "acceptance never depends on" receipt
  tolerances. formal/tla/P5P6_TemporalRevocation.tla:118 proves accepted
  receipts stay within verifier maxima and verifier policy via
  VerifierOwnsTolerances/WindowRespected; it does not prove full
  noninterference from rcptDelta/rcptEps. A receipt-controlled stricter
  window would still pass these safety invariants. Not a security break
  for the oversized-window attack, but if "ignore receipt tolerances" is
  meant literally, add an explicit independence invariant.

- Low: P5's issuance corollary is now modeled, but the tracker still
  lists P5's main artifact only as formal/PROPERTIES.md:20, while the
  issuance part lives in formal/tla/P5c_IssuanceProtocol.tla:1. The
  cross-cutting note captures this, but the P5 row should probably list
  both artifacts or split verifier-side P5 and issuance-corollary P5c to
  avoid later audit ambiguity.

Confirmed Addressed

- P4 exact classification is properly actioned. The iff-style invariants
  at formal/tla/P4_VerifierStates.tla:112 address the prior "one-way
  safety only" concern.
- Verifier-owned tolerance maxima are modeled with polDelta/polEps
  versus adversarial rcptDelta/rcptEps, and BrokenTol catches oversized
  receipt-controlled acceptance.
- The confirmation-depth issue is now represented by a real state
  machine in formal/tla/P5c_IssuanceProtocol.tla:109, with the broken
  shallow-ship model producing the intended reorg counterexample.

Validation

I reran TLC. Main P4, P5/P6, and P5c pass. Broken P4, broken
point-revocation P5/P6, broken tolerance, and broken shallow-ship all
fail for the intended reasons. The P5c sanity config also shows
shipping, reissue-then-ship, and reorg-surviving ship are reachable.
