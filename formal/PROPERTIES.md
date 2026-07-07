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
