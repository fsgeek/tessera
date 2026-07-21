# Band 0 — property obligations tracker

Working tracker for discharging the pre-registered properties of
Amendment 1 §A1.2 (commit `03cd3db`, anchored), as amended by
Amendment 2 (`docs/phase-0-prereg-amendment-2.md`, DRAFT — pending
non-author review and author signature; its model obligations are
tracked here already so they cannot silently lapse). The *authoritative*
statements live in the amendments; this file only tracks discharge status
and artifact locations. If this table and the amendment ever disagree, the
amendment wins — and the disagreement is a bug in this file.

Status values: `open` → `modeling` → `checked` (tool passes) →
`discharged` (tool passes + agreement-gate falsification review passed).
Per A1.1, any weakening of a property is *not* recorded here — it
requires a signed amendment.

| Prop | Short name                         | Discharge      | Tool (A1.4)        | Status | Artifact |
|------|------------------------------------|----------------|--------------------| -------|----------|
| P1   | Integrity (headline)               | [model]        | TLA+ and ProVerif  | open   | —        |
| P2   | Signature-set completeness         | [model]        | TLA+ and ProVerif  | open   | —        |
| P3   | Key binding (anti-DSKS)            | [model]+[assum]| ProVerif; H1a prof.| open   | —        |
| P4   | Fail-closed state logic            | [model]        | TLA+               | checked| `formal/tla/P4_VerifierStates.tla` |
| P5   | Temporal soundness (verifier side) | [model]+[assum]| TLA+               | checked| `formal/tla/P5P6_TemporalRevocation.tla` |
| P5c  | Issuance corollary (depth k, reissue)| [model]      | TLA+               | checked| `formal/tla/P5c_IssuanceProtocol.tla` |
| P6   | Revocation over uncertainty window | [model]        | TLA+               | checked| `formal/tla/P5P6_TemporalRevocation.tla` |
| P7   | Wrapper / object-type soundness    | [model]        | TLA+ and ProVerif  | open   | —        |
| P8   | Canonicalization inj. + framing    | [proof]        | Lean4 or prose+vec | open   | —        |
| P9   | Verification statelessness         | [model]        | TLA+               | open   | —        |
| P10  | Manifest authority                 | [model]        | TLA+               | open   | —        |

Cross-cutting obligations (A1.4, A1.7):

- [x] Tool spike complete; choice committed (`formal/spike/DECISION.md`)
      **before any substantive proof work** (A1.4). **Chosen: ProVerif**
      (2026-07-05; Tamarin rejected on the counterexample-readability
      tie-breaker).
- [ ] Every symbolic lemma carries a prose mapping to its A1.2 property.
- [ ] Cross-model correspondence mapping (TLA+ ↔ symbolic) in the written
      proof.
- [ ] Cross-model correspondence (TLA+ ↔ TLA+): P5c (issuance) and P5P6
      (verifier) agree on the A2.1 confirmation predicate in prose but
      model the quantity incompatibly — operational `depth` vs. free
      integer `confirmedAt`; the join is asserted, not checked. Obligation:
      a bridge model that represents block timestamps *separately* from
      the tick clock and derives `confirmedAt` from headers (latching it
      under P5c's single clock would be true by construction), plus a
      broken-bridge companion substituting `anchorAt` that must go red.
      Surfaced 2026-07-18; the alarming "burial delay vanishes" form did
      NOT reproduce under Codex non-author check — the narrowed obligation
      is what remains. Itemized distinct from the TLA+↔symbolic line
      above; disposition to be registered in Amendment 3. See
      `docs/exploration-2026-07-18-causal-dag-commons.md` §0/§8/§8b.
- [ ] Agreement-gate falsification reviews run by non-author models;
      artifacts in `docs/reviews/`.
- [ ] Conformance vectors extracted from checked traces (feeds H1a).
- [ ] Informal written proof (defend-it-cold) in repository.
- [ ] Parameter ratification at Band 0 exit: δ = 72h, ε = 24h, k = 6,
      and (A2.3) the issuance attempt bound N (working default 3).
- [x] **P5 issuance corollary** (anchor confirmed at depth k within δ;
      re-issue on late/reorged anchors) — modeled as a real state machine
      in `formal/tla/P5c_IssuanceProtocol.tla` (checked; broken companion
      exhibits ship-shallow-then-reorg, the Gemini-named harm). The
      semantic fork the model surfaced (strict vs. permissive reading)
      was RATIFIED strict on 2026-07-07 in the chain-time form —
      `confirmed_at := timestamp(block h+k−1) ≤ declared + δ`, one
      predicate for issuer and verifier — by Amendment 2 (A2.1), which
      also pins the depth convention `DepthK = k − 1`.
- [x] **A2.2 confirmation-timing conjunct (verifier side)** — added to
      `formal/tla/P5P6_TemporalRevocation.tla` (`confirmedAt`,
      `AbandonedArtifactRejected`; checked, all invariants green, all
      vacuity witnesses fire). New broken companion `_BrokenConf` carries
      the pre-A2 verifier: ForgeryRejected and ReceiptIndependence HOLD,
      AbandonedArtifactRejected VIOLATED with the abandoned-anchor
      artifact as the counterexample — the A2.0 correction made
      mechanical (the artifact is no forgery; only the new conjunct
      rejects it).
- [ ] A2.2 conformance-vector cases: late-burial artifact → `INVALID`;
      headers unavailable → `UNVERIFIABLE` (with the general extraction
      obligation above).
- [x] **A2.3 refusal state** (2026-07-20, round-3 ruling 4 construction,
      AUTHOR-ADOPTED FOR STAGE-ONE DRAFTING; non-author review passed
      same day, `docs/reviews/2026-07-20-codex-p5c-refusal-review.md` —
      "accept the atomic-entry safety construction", three prose
      overclaims folded) — `refused` added to
      `formal/tla/P5c_IssuanceProtocol.tla` by **atomic entry**: the Tick
      expiring the FINAL attempt's window records the refusal in the same
      transition, making it a transition-level safety fact — safety-only,
      no fairness, no liveness claim. Checked (all green, MaxTime raised
      8→14: minimum 12 = MaxAttempts·(Delta+1) for the final window to
      expire at all — below it the refusal invariants are vacuous, the
      `RefusalUnreachable` witness guards; +DepthK headroom = 14
      exercises post-refusal burial, the `RefusalBuriedAnchorUnreachable`
      witness guards): `NoSilentDeadlock` (no reachable state with the
      final window expired and no refusal recorded),
      `RefusedOnlyWhenExhausted` (which contains shipped/refused mutual
      exclusion), and action property `RefusalLatched` (in-model latch).
      New companion `P5c_IssuanceProtocol_BrokenSilent` implements the
      review's warned construction (separately enabled Refuse,
      postponable): red on exactly `NoSilentDeadlock` among the checked
      set; its `_Green` cfg (all other invariants) passes. Ship and the
      refusal trigger deliberately overlap at now = declared+Delta — an
      intentional boundary race, named in the module. Discharged claim
      (narrowed on review; the reviewer withdrew its own round-3
      wording): **the abstract refusal state is entered atomically and
      latches** — storage durability, retrievability, reporting, and
      A2.3's registered "reported" are Amendment 3 disposition items (the
      refusal tracker line). Also explicitly unclaimed: that the final
      crossing ever occurs (Tick is postponable; safety-only).
      Calibration artifact:
      `docs/reviews/2026-07-20-claude-predictions-p5c-refusal-bench.md`
      (first run caught a TLA+ precedence bug that silently disabled the
      atomic entry — `NoSilentDeadlock` flagged its own author's error).
