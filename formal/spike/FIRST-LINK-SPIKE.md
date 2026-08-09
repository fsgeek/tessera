# First-link mechanism spike — pre-registration

Status: ADOPTED (clerk-drafted 2026-08-08 from A3 §A3.2.1/§A3.3 and
the four-model panel; author-signed at commit `8ae4720`, OTS-stamped,
2026-08-09 — registered before evidence, per the SPIKE.md discipline.
A prior version of this line said DRAFT after the signing commit; the
label lagged the record and the record governs.)

## Purpose

Discharge the §A3.2.1 boundary invariant with mechanism evidence:

> Two manifests that differ in any authority-relevant fact must not be
> supportable by the same evidence.

The spike selects the first-link mechanism (the fork A3 deliberately
left open: digest publication, authorized tuple, or another
construction) *after* evidence, per the §A3.2.1 override. The drafted
capstone ledger interface is the spike's scaffolding — one artifact.

## Carried obligations (already registered in A3 §A3.3/§A3.9 — not new, restated here so this document is self-contained)

- Representative complexity first: the §A3.2 witness chain, the
  structural worst case, ablating toward the break point on failure.
- Per-query timebox declared before running; three named outcomes:
  query violation = counterexample; timeout = mechanism failure, not
  property evidence; termination = evidence for the checked
  abstraction only.
- Predictions registered before running, per query.
- The transcription-pattern capstone remains a non-binding
  implementation candidate, subject to this spike.

## Panel-added exit criteria (2026-08-08 four-model panel; sources in `docs/reviews/2026-08-08-A3-panel-disposition.md` §3)

1. **Authority-relevance map (Kimi 3).** A registered enumeration of
   which manifest fields are authority-relevant (e.g. key
   fingerprints, issuer identity, algorithm identifiers) and which
   are non-authoritative (display labels, optional metadata),
   produced as a spike artifact *before* the broken companion is
   judged. The companion must then differ **only** in an
   authority-relevant field.
2. **Genuine two-worlds broken companion (Grok).** Two
   authority-distinct manifests sharing evidence; the consuming
   linkage query must fail. Cardinality-only checks do not discharge
   this. **Failure of the spike to produce such a companion is an
   amendment trigger, not a soft "mechanism still open."**
3. **Adversary linkage (DeepSeek).** The A1.3 capability "control any
   subset of authority channels but not all" is explicitly cited in
   the capstone-ledger entry for the floor's proof obligation.
4. **Standing-mechanism coverage (Kimi 1, Grok 3).** The chosen
   standing-evidence mechanism (§A3.7.1) is modeled in the symbolic
   suite before Band 0 exit, under the same adversary. The spike
   names and resolves, explicitly, the design-space tension between
   abandoned-artifact-alone testability and A2.4's
   exactly-one-shipped-anchor rule; a mechanism that cannot satisfy
   both must say which registered statement needs amending, before
   implementation.
5. **Test-condition recording (DeepSeek).** Every standing /
   dead-project test records whether the artifact was presented with
   or without lineage context. The alone-case is the hard case and
   must be present.

Optional (DeepSeek suggestion 1 increment): predictions may carry
numeric probabilities; qualitative predictions satisfy the registered
floor.

## Related registered obligation (ruled 2026-08-09; a prior version of this section said "pending author ruling" — the label lagged the record)

- **Kimi 2 — integrated adversarial lifecycle model** (issuance →
  wrapping → supersession → refusal → verification → tending, with a
  standing-transplant broken companion). REGISTERED in A3 §A3.9 at
  `8ae4720`: mandatory, triggered on this spike's completion, green —
  or timeout disposed by signed amendment — before the H1a
  crypto-core freeze. Not part of this spike's Q-ladder; recorded
  here because its adversary and ledger terms should be chosen
  compatibly from the start.

## Artifacts this spike must leave behind

1. The authority-relevance map (registered, versioned).
2. The mechanism decision document (DECISION.md pattern: criteria
   fixed before evidence, scoring on record, rejected alternatives
   named).
3. Correct + broken companion models with committed `.out` evidence.
4. Capstone-ledger entries for every discharged or residual
   assumption, per the §A3.3 conservation rule.
5. Registered predictions vs. observed outcomes, per query.
