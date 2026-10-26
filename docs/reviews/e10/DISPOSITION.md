# Disposition of the E10 extraction review (2026-10-26)

**Parties.** Owner: Claude Opus 5.5. Reviewer: Codex ([CODEX-REVIEW.md](CODEX-REVIEW.md)). The verdict was
ACCEPTABLE AFTER E10R-01 to E10R-06.

**Findings.** Two are HIGH, three MEDIUM and one LOW. All six are accepted and applied. Codex's stated fixes were
used throughout. Where a fix needed a choice, the choice closest to the registered text was taken (A1.7 item 2,
A9.2/A9.4, profile §15.7), and each one is listed below.

**Files edited.** Only `formal/e10/` (the spec, the 53 vectors, INDEX, and the new `materialize.py` and
`fixtures/`) and this file.

## Owner decisions applied

- **Revocation (TMP-10).** The vector follows V1: `VALID_STRICT`, with `revocation: NOT_EVALUATED` (A9.4). The
  disagreement with P6, which rejects, is stated in the file.
- **Missing `a_sig` (E6A-07).** The vector follows V1: `UNVERIFIABLE / MEMBER_MISSING:a_sig` (profile §13 note
  13, author-accepted in E9 row 3). The model's INVALID is stated as a divergence. The earlier "left to the owner"
  wording is replaced.
- **Issuer vectors.** ISS-01 to ISS-04 keep the status "requires staging harness".

## Findings

| Finding | Sev. | Disposition | Files |
|---|---|---|---|
| E10R-01 | HIGH | **Applied.** See "E10R-01 in detail" below the table. | `formal/e10/materialize.py`; `formal/e10/fixtures/`; E10-SPEC status block, §2, §8; INDEX `fixtures` |
| E10R-02 | MEDIUM | **Applied.** Alternatives and controls are now explicit subcases, each with its own request and report. E6A-01 has `.i` (HY-b2-H, `UNVERIFIABLE / ALG_UNKNOWN`) and `.ii` (HY-e1-C, `INVALID / RECEIPT_COMMON_MISMATCH`). P4-03 has `.degraded` (L-06) and `.strict-control` (L-06s, `VALID_STRICT / OK`). Every subcase lists `coverage.exact` and `coverage.analogous`. `covered_by` now holds exact matches only, and the new `analogous_to` holds the rest: UTC-03 (T 14:00Z), A-e2, ALG-01, L-03, L-04b, HY-N3. **Choice:** a vector counts as covered when at least one subcase is exact. The 14 covered / 39 new count is unchanged, and each of the 14 has an exact case. | the four vectors named, every verifier vector (`subcases`, `analogous_to`), INDEX, E10-SPEC §6 |
| E10R-03 | MEDIUM | **Applied.** See "E10R-03 in detail" below the table. | all 49 verifier vectors, INDEX, E10-SPEC §1 |
| E10R-04 | HIGH | **Applied.** See "E10R-04 in detail" below the table. | E10-ISS-01..04 (`staging_harness`), INDEX, E10-SPEC §3.3, §5 |
| E10R-05 | MEDIUM | **Applied, Codex's construction.** SP3-01's L0 form uses the same receipt's S_kms as `possession.kms`. This needs only a post-issue edit and no TEST key, and gives `INVALID / POSSESSION_INVALID`, T 12:20Z (a_sig untouched). POS-a is kept as the TEST-form subcase with exact coverage. | E10-SP3-01, `materialize.py`, E10-SPEC §5 |
| E10R-06 | LOW | **Applied.** See "E10R-06 in detail" below the table. | all vectors (`source`), E10-SPEC status block |

### E10R-01 in detail

- **The concretizer.** `materialize.py` builds all 68 verifier subcases as concrete TEST-universe fixtures in
  run.py's layout, through `issue.py`, plus named post-issue edits. Reused conformance constructions are called
  unchanged from `cases.py`. It also writes 6 issuer TEST oracles.
- **Oracle and construction.** The expected report is data in each vector file, and the materializer copies it. Its
  only cross-check is T and U against the issuer's plan.
- **Reproducibility.** `--check` rebuilds the fixtures and compares them with `MANIFEST.json`, which holds the
  sha256 of every output and every source. No file differed.
- **Independent run.** The independent verifier, through the differential adapter, gives **68/68 AGREE** on the six
  fields, `utc_assessment` and `detail` (`fixtures/RUN-INDEP.json`).
- **Executable sequences.** The P9 vectors carry `sequence` (hosts, step order, environment, pass rule). The issuer
  vectors carry `staging_harness` (see E10R-04).
- **Still owed** (stated in the spec's status block and §8):
  - the non-author review of the concretizer and its outputs;
  - the spot audit by eye;
  - the AWS run.

  This disposition does not discharge A1.7's review step.

### E10R-03 in detail

- **All six fields.** Every executable subcase gives all six stable fields, T included, and a `T_derivation`
  stating how T was reached.
- **SP1-01.** Its prose T is replaced by two subcases: `.unstamped` (T null, row 11.2) and `.restamped` (T 12:20Z).
- **Other optional re-stamps.** SP2-04 and G10-03 are split the same way. SP2-06 is split into `.L3` (stamped) and
  `.L0` (splice, T null).
- **UTC assessment.** The A10 UTC assessment is stated separately, as `expected.utc_assessment`
  (`A-UTC-7200-6`, `utc_upper_bound` null exactly when T is null).
- **Previously missing T values.** The eleven vectors with no T now carry one: CAP-01, CAP-04, E6A-01, G10-03,
  P4-04, SP1-02, SP1-03, SP1-04, SP2-04, SP2-06 and SP3-01. Where a_sig and the proof are as stamped, T is 12:20Z;
  the unstamped variants have T null. P7-01, P7-02, P9-01 and P9-02 had no single expected report. Their subcases
  now each carry one. **Choice:** where a vector allowed an optional re-stamp, both variants are kept as subcases, rather than
  picking one.

### E10R-04 in detail

Each issuer vector has a `staging_harness` with a sequence, observations, controls, a pass rule and TEST oracles,
and keeps its "requires staging harness" status.

- **ISS-01.** Observe the decision record (c2 = false), the discard transition and the counter increment. Control:
  ships at the d + δ boundary. A refusal without the discard and counter observations is not a pass.
- **ISS-02.** The harness drives and records W, the confirmed proof and the decision point. The decision must come
  before the attempt's expiry and must not be an expiry. Control: nTime(h*+5) = d + δ ships.
- **ISS-03.** Hold the chain at 1..5 confirmations, observing at each, then release the sixth. The spec states
  explicitly that the model's DepthK = 5 counts successors (`P5c_IssuanceProtocol.tla:202, 262`), so it means
  **six confirmations**. It also states that public polling cannot exclude a premature shipment.
- **ISS-04.** Three expiries, then the refusal. Then restore availability, deliver late evidence and restart, and
  the request must never ship. Controls: recovery during attempt 2, and a frozen clock (stalled versus latched).
- **TEST oracles.** For ISS-01 to ISS-03 these are refuse/ship pairs from the TEST issuer's pre-ship decision.
  Their limits are stated: they show no attempts, discard, N or clock.

### E10R-06 in detail

- **SP2-04.** The combined d8/d11 path is split into one source object per file.
- **Line locators.** Explicit lines were added where they were missing: ISS-01 `.out` (lines 18/25 and 18/23),
  TMP-03 k3 (18-19), TMP-11 Sanity (82-88), E6A-07 RESULTS (155-166), P4-03 RESULTS (88) plus
  `NeverInDegraded_V1.out:46`, P7-03 `capstone.pv:88-94`, P9-03 Vector (29), and POS-01 bridge witness (25, 153).
- **Registered text.** Each combined registered-text locator is split per file.
- **Formula versus evidence.** Every source carries a `role`: `property_definition`, `execution_evidence`,
  `registered_text` or `summary`. Where a formula had been cited as a reachable witness, the run is now cited
  beside it: POS-01 → `runs/sanity/NeverInStrict_V1.out:44-49` (Codex's example) and P4-04 →
  `NeverDefectPlusMissingEv_V1.out:44`.
- **A1 citation.** The A1 concretizer citation now reads `amendment-1.md:550-554`.
- **E6A-05.** The mutation value was corrected to the actual L-03b label, `tessera-v2-strict`.

## Not changed

- **Expected verdicts and reasons.** No expected verdict or reason code changed. Codex found them sound, and the
  independent run agrees.
- **P7.** P7 stays deferred under A9 row 26. P7-01 and P7-02 remain optional V1 analogues and do not discharge
  A6.1.
- **Registered material.** No registered sentence, model, `.out` file or conformance case was edited.
