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
- [x] Cross-model correspondence (TLA+ ↔ TLA+): P5c (issuance) and P5P6
      (verifier) agree on the A2.1 confirmation predicate in prose but
      model the quantity incompatibly — operational `depth` vs. free
      integer `confirmedAt`; the join was asserted, not checked.
      **Bridge model built and checked 2026-07-21:**
      `formal/tla/P5cP5P6_Bridge.tla` — block timestamps decoupled from
      the tick clock (skewed, non-monotonic), `confirmedAt` DERIVED from
      the chain (never latched — the by-construction vacuity trap
      avoided), issuer and verifier transcribed independently (depth
      convention vs. height-h+k−1 convention), with the `DepthK = k − 1`
      pin as a checked INVARIANT, not an ASSUME. Green (456k states):
      PinAgreement, ShippedDesignatedAgree (the join itself),
      HonestShipAccepted (A2.1's by-construction claim, now checked),
      LateBurialRejected; all six vacuity witnesses fire, including the
      ε side (unrepresentable under P5c's fused clock) and wall-clock/
      chain-time divergence. Companions: `_BrokenAnchorSubst` (the
      obligated one — verifier substitutes `anchorAt`) red on exactly
      the correspondence + late-burial invariants, isolation green
      passes; `_BrokenWallClock` (P5c's fused-clock ship rule
      transplanted) red on HonestShipAccepted — A2.1's "why chain time
      on both sides" exhibited; `_BrokenPin` cfg (DepthK = KConf) red at
      configuration time. Scoped abstractions, named in the module: one
      attempt (no retry/refusal), no reorgs (A1.6 permanence — reorg
      re-verification NOT discharged here), stateless verdicts, no
      UNVERIFIABLE arm. **Design-time finding routed to the A2 review
      rounds:** A2.1's "The rule" sentence states conjunct 3 only; under
      decoupled clocks conjunct 3 does not imply conjunct 2, so the
      issuer must evaluate the full VALID_STRICT at ship (the bridge's
      Ship does; A2.1's prose should say so). Calibration artifact:
      `docs/reviews/2026-07-21-claude-predictions-bridge-bench.md`.
      Surfaced 2026-07-18; "burial delay vanishes" did NOT reproduce
      under Codex non-author check on the fused model, and the bridge
      confirms: the vanishing requires the broken substitution.
      NON-AUTHOR REVIEW PENDING; disposition to be registered in
      Amendment 3. See
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
      latches** — storage durability, retrievability, and reporting are
      Amendment 3 disposition items (the refusal tracker line; A2.3's
      draft text was aligned to this split 2026-07-21). Also explicitly unclaimed: that the final
      crossing ever occurs (Tick is postponable; safety-only).
      Calibration artifact:
      `docs/reviews/2026-07-20-claude-predictions-p5c-refusal-bench.md`
      (first run caught a TLA+ precedence bug that silently disabled the
      atomic entry — `NoSilentDeadlock` flagged its own author's error).
