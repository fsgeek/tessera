# Band 0 — property obligations tracker

Working tracker for discharging the pre-registered properties of
Amendment 1 §A1.2 (commit `03cd3db`, anchored). The *authoritative*
statements live in the amendment; this file only tracks discharge status
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
| P5   | Temporal soundness (two-sided)     | [model]+[assum]| TLA+               | open   | —        |
| P6   | Revocation over uncertainty window | [model]        | TLA+               | open   | —        |
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
- [ ] Parameter ratification at Band 0 exit: δ = 72h, ε = 24h, k = 6.
