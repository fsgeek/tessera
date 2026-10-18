# Disposition: Codex review of the UTC-bound and capture-visibility memo (2026-10-17)

The owner accepted all seven findings. They are applied to
`docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md`, using Codex's exact text wherever the review gave
it. The memo stays RECOMMENDED.

- **F01 (MEDIUM), ACCEPTED.** U2 now uses U_TSA = max_i(genTime_i + a_i), with finite authenticated accuracy
  allowances, in both the trust bullet and the recommendation. The text is Codex's.
- **F02 (MEDIUM), ACCEPTED.** The changes:
  - "never misused" becomes "trustworthy when this token was produced".
  - Historical path verification is separated from key safety and revocation, and A9.4 is no longer used to waive
    TSA revocation.
  - Anchoring is described as preservation only.
  - Pinning an intermediate CA is described as a trust choice.
  - "Every observed TSA" is limited to the sample.
  - The unresolved use requirements are recorded, and not made obligations.
- **F03 (MEDIUM), ACCEPTED: Codex's wrapper alternative.** `utc_assessment` holds U and `assumption_id`, outside
  the six stable fields. This option keeps A9.4's contract simplest: no supersession of A9.1/A9.4, and no change to
  the stable JSON, the CLI or the agreement cases. U stays recomputable from the stable T's headers. The six-to-seven
  rows are removed.
- **F04 (MEDIUM), ACCEPTED.** U is computed with uint64 widening and no modular reduction, using Codex's normative
  sentence. The 2106 claim is limited to verifying preserved receipts. Vectors are added for the uint32 maximum and
  for a 2106 verifier clock.
- **F05 (MEDIUM), ACCEPTED.** The fallback is rewritten in Codex's text. Release-key independence is an existing
  A9.5 prerequisite, put to the author as a NARROW-MODEL if it is unavailable. Cutting the listing does not cure it.
  The cut-order addition is labelled a gate change.
- **F06 (LOW), ACCEPTED.** The future rule is stated relative to the receiving node's clock, with its clock-error
  caveat. BIP 54's period-end rule is added, and PR #35793 is marked open and proposed.
- **F07 (LOW), ACCEPTED.** The changes:
  - The table becomes Codex's ordered classifier, with a shared endpoint counting as overlap and registered
    precedence applying.
  - Completeness is restated as authorization closure, with additions only strictly after the previous `as_of`.
  - Schema constraints are added.
  - "Authentic release" now includes trustworthy authorization behaviour.
  - Vectors are added for an exact future match, an unlisted future overlap, a shared endpoint, and additions at
    versus after the horizon.
- **Also applied, from the review's "Questions checked" (not numbered findings):**
  - the α⁶ caveat;
  - A-UTC described as "sufficient, not minimal";
  - Δ and m frozen in the specification;
  - the amendment inventory gains A9.1's trust item, A9.5's list and A9.6's first window;
  - "all verdicts unchanged" is withdrawn in favour of the scenario-mapping statement.
