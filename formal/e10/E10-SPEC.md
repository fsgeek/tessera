# E10: model-derived conformance vectors for `tessera-v1-strict`

> **STATUS: PROPOSED.** Extracted by the owner instance (Claude Opus 5.5) on 2026-10-26, ahead of the 13 Nov date
> (A9.2, `docs/phase-0-prereg-amendment-9.md:209-211`; `formal/freeze-v1/FREEZE-RECORD.md:80`). Not adopted. It
> changes no registered sentence, model, configuration, `.out` file or conformance case. If it disagrees with A9,
> A10 or `docs/V1-PROFILE.md`, they win and this page is wrong.
>
> **Revised 2026-10-26 after the Codex non-author review** (`docs/reviews/e10/CODEX-REVIEW.md`, E10R-01..06;
> dispositions in `docs/reviews/e10/DISPOSITION.md`). The revision adds the concretizer and its concrete outputs
> (§8), splits alternatives and controls into subcases, gives every executable subcase all six stable fields plus
> the A10 UTC assessment, defines the issuer staging sequences, and repairs source locators.
>
> **Not done here, and owed:**
> - The non-author review of the concretizer (`formal/e10/materialize.py`) and of its outputs that A1.7 item 2
>   requires (`docs/phase-0-prereg-amendment-1.md:550-554`). Codex reviewed the scenario design; the concretizer
>   did not exist then.
> - The spot audit of the fixtures by eye.
> - Running the vectors against AWS. That is the 20 Nov item (A9.2: "E10 vectors run against AWS"). The four
>   issuer vectors also need a staging harness that does not yet exist (§5).
>
> Until that review is done, every expected value below is the extractor's reading of profile §15.7. One
> independent check exists: the independent verifier agrees with all 68 subcase expectations (§8).

## 1. What E10 requires, and what counts

- **A1.7 item 2** (`phase-0-prereg-amendment-1.md:536-559`). Concrete fixtures are extracted from the model checker's
  checked traces. Each one names its inputs and the verdict the model requires. The vectors are testing evidence,
  not proof of equivalence. The trace-to-fixture step carries its own fidelity risk, so it is reviewed under the
  non-author discipline.
- **The BAND0-EXIT row for E10** (`formal/BAND0-EXIT.md:70`) names five cases:
  - late burial → `INVALID`
  - headers missing → `UNVERIFIABLE`
  - the P9 two-machine case
  - the P7 verdict-independence case
  - A3.9's refuse-to-ship issuance case

  Two tracker boxes also feed it: `formal/PROPERTIES.md` "Conformance vectors extracted from checked traces" and
  "A2.2 conformance-vector cases".
- **Scope.** Only V1 results count: a strict request, no standing, no wrappers, no degraded mode, and no service-key
  listing (the listing was cut by E9 row 2). Where a source model was run only in degraded mode, it is used only as
  the scenario source. Its strict counterpart is cited where one exists: a capstone strict run, or the S-P2
  diagnostics d7–d12. A strict outcome is never inferred from a degraded run.
- **Expected values** follow `docs/V1-PROFILE.md` §15.7: the first failed row, otherwise the first unperformable
  row. Every expected report also carries `revocation: NOT_EVALUATED`, `historical_security: NOT_EVALUATED` and
  `standing: ABSENT/NOT_ISSUED_IN_PROFILE` (§3.4).
- **Every executable subcase states all six stable fields**, T included, including for `INVALID` results
  (profile §3.4). Each states how its T is derived (`T_derivation`): T = nTime(h*) where a_sig and the receipt proof
  are as stamped; null where a_sig was edited without a re-stamp (row 11.2), where no attestation qualifies (row
  11.4), or where dispatch is terminal. Where a vector allows a re-stamp, the re-stamped and unstamped forms are
  separate subcases with separate reports (SP1-01, SP2-04, G10-03; SP2-06 has an L3 and an L0 form).
- **The A10 UTC assessment is stated separately**, as `expected.utc_assessment` beside the six fields, never inside
  them (A10.1.1; profile 7.4; the run.py contract): `assumption_id: A-UTC-7200-6` and `utc_upper_bound` =
  7200 + max nTime(h*..h*+5), null exactly when T is null.
- **Guarantee rows** are those of `docs/V1-CONTRACT.md` §2 (G1–G10). §5 of that file calls its model/test table
  "mappings, not pairs". Each vector here runs one model scenario as one concrete case. That makes it the test half
  of a real pair for that scenario.

## 2. Files

| Path | What |
|---|---|
| `formal/e10/vectors/E10-*.json` | **53 vector specifications** (schema `tessera-e10-vector/1`). They are data, not code. Each file holds: `source` (one object per file, with explicit `lines` and a `role`: `property_definition`, `execution_evidence`, `registered_text` or `summary`); `scenario`; `base`; `mutations`; `test_universe`; `choices`; `expected` (the single subcase's report, or "see subcases"); `subcases` (verifier side: id, construction, `coverage.exact` / `coverage.analogous`, the full expected report with `utc_assessment`, `T_derivation`); `covered_by` (exact coverage only) / `analogous_to` / `partial_overlap`; `sequence` (P9 vectors: host, step order, environment); `staging_harness` (issuer side: sequence, observations, controls, pass rule, TEST oracles); `live` (modes and needs). |
| `formal/e10/vectors/INDEX.json` | One row per vector with its subcases and fixture paths, the counts, the coverage legend and the live-mode legend (§5). |
| `formal/e10/materialize.py` | The concretizer (§8). Builds every subcase as a TEST-universe fixture and the issuer TEST oracles; `--check` rebuilds and compares hashes. |
| `formal/e10/fixtures/` | Its output: one directory per subcase (`bundle.json`, `trust.json`, `release.json`, `expected.json`, and `request.txt` / `catalog.json` where needed), six `issuer-oracle.json` directories, `MANIFEST.json` (sha256 of every output and of every source it was built from) and `RUN-INDEP.json` (§8). |
| `formal/e10/tla/E10_BridgeRefuseC2.tla`, `run.sh`, `*.cfg`, `*.out` | One E10-specific re-check (§3.3). It `EXTENDS` the committed bridge unchanged. |
| `formal/e10/tla/ttrace-from-first-run/` | TLC trace-explorer files from the first run of `run.sh`, before `-noGenerateSpecTE` was added. Byproducts only; safe to delete. |

**Mutation vocabulary** (the `op` values). Heights are symbolic: `h*` is the receipt proof's selected height
(profile 7.1), and `h*+5` is its confirmation block. The ops are:

- `set_ntime`
- `remove_headers`
- `remove_member`, `add_member`, `replace_member` (layer-relative paths, profile 2.1)
- `frames_set`, `frames_delete` (fields of a frame payload; changing a frame changes `a_sig`)
- `a_sig_set_signature`, `a_sig_rebuild`, `a_sig_truncate`, `a_sig_replace_slot` (ENC §5 re-encoding)
- `issue_with_content` (an ordinary client request)
- `channels`, `dns_txt`, `git` (authority-channel material)
- `restamp` (a new OTS proof over the new `A_sig`)
- `request`, `environment`, `run_set`, `run_sequence` (verifier inputs and execution)

An `a_sig` edit without a re-stamp makes T null, because row 11.2 fails. The reported reason is still the earlier
row, as stated in each file.

**TEST-universe numbers** (used only in `test_universe` and in the T values of TMP vectors):

- Declared time is TB = `2026-11-10T12:00:00Z`.
- h* = 900024 and h*+5 = 900029.
- The honest T is `2026-11-10T12:20:00Z`.
- δ = 259200 s and ε = 86400 s.

Against real receipts, read every height and time symbolically.

## 3. The registered E10 cases

### 3.1 Late burial → `INVALID` (mapped)

| | |
|---|---|
| Traces | `formal/tla/P5P6_TemporalRevocation_BrokenConf.out:35-44` (`AbandonedArtifactRejected`, defined `P5P6_TemporalRevocation.tla:195-199`; state declared 0, anchor 0, confirmedAt 1, polDelta 0); bridge at k = 6: `formal/tla/k6-2026-09-14/Bridge/W_LateBurialArtifactUnreachable.out:25-141` (declared 2, Delta 2, chain ⟨3,3,3,3,5,5⟩, anchorH 1, designated block 6 = h + k − 1) and the broken companion `C_AnchorSubst_Late.out:25-141` (`LateBurialRejected`, `P5cP5P6_Bridge.tla:213-217`) |
| Scenario | The including block is in the window. Its fifth successor carries a time past declared + δ. Strict issuance never ships such a receipt: it is the A2.0 abandoned-anchor artifact. |
| Vectors | **E10-TMP-01** (boundary, +1 s) → `INVALID / CONFIRMATION_LATE` (row 12.3), **covered by L-36b**. **E10-TMP-02** (the traced ratio: T = d + δ/2, confirmed_at = d + 3δ/2) → same, **new**. |
| G | G5, G9 |
| Choices | The traces fix only order relations. "One second past" and "the traced ratio" are both concretizations. Taking the model's unit as δ/2 makes its ε 36 h, not 24 h. That does not matter here, because this trace does not exercise ε. |

### 3.2 Headers missing → `UNVERIFIABLE` (mapped; model source is P4, not a temporal trace)

| | |
|---|---|
| Sources | `formal/tla/P4_VerifierStates.tla:167-168` (`ExactUnverifiable`); `P4_VerifierStates_Sanity.out` witness `VerdictNeverUnverifiable`; the A2.2 text `phase-0-prereg-amendment-2.md:247-251` ("unperformable (headers unavailable) → `UNVERIFIABLE`"); the shallow-ship trace `k6-2026-09-14/P5c/P5c_IssuanceProtocol_Broken_k6.out:25-96` |
| Vectors | **E10-TMP-11**: no headers for the attestation → `UNVERIFIABLE / HEADERS_MISSING` (row 11.4), T null. **Covered by L-43b and UTC-08.** **E10-TMP-12**: h*..h*+4 present, h*+5 absent → same. **New.** |
| G | G9, G5 |
| Choice, stated plainly | **No temporal model has an unperformable arm.** The bridge excludes it by design (`P5cP5P6_Bridge.tla:73-75`), and P5P6 has none. So this case is extracted from P4's partition plus A2.2's registered text, not from a temporal trace. The shallow-ship trace supplies TMP-12's shape. Its own harm, a reorg after ship, cannot be shown in a bundle; it is the issuer vector ISS-03. |

### 3.3 A3.9's refuse-to-ship issuance case (mapped, with one new witness run)

| | |
|---|---|
| Registered | `phase-0-prereg-amendment-3.md:759-765`: `anchor_time = declared + δ + 1`, `confirmed_at = declared + δ − 1`; the issuer must refuse to ship (discard the attempt, count it against N); "extracted from the bridge model". A7.6 (`amendment-7.md:146-162`): the issuer ships on the three conjuncts plus burial depth. |
| Gap found | The bridge has no refusal action, and the registered `_BrokenConjunct3Only` companion was never built (`formal/COVERAGE-MAP.md` row 6: "not yet extant"). No committed trace showed this state. |
| Re-check run (cheap) | `formal/e10/tla/E10_BridgeRefuseC2.tla` `EXTENDS P5cP5P6_Bridge` unchanged and adds two formulas. Results: (a) the witness `C2FailC3PassArtifactUnreachable` is **RED, as it should be**, at k = 3 (`W_C2FailC3Pass_k3.out`) and k = 6 (`W_C2FailC3Pass_k6.out`; declared 0, Delta 2, chain ⟨3,1,1,1,1,1⟩, anchorH 1: anchor = d + δ + 1 unit, confirmation = d + δ − 1 unit, exactly the registered shape); (b) the safety formula `C2FailNeverShipped` is **GREEN over the full space** at k = 3 (456,442 distinct states) and k = 6, skew ±1 (86,849,955 distinct states, 0 left on queue; `S_C2FailNeverShipped_k6.out`). The k = 6 instance is the one in `k6-2026-09-14/RESULTS-K6.md` §3. TLC 2026.07.31, `~/.local/lib/tla2tools.jar`. |
| Vectors | **E10-ISS-01** (issuer side): the attempt is not shipped, it is discarded and it counts against N. **New.** Requires a staging harness: the TEST issuer's `IssueRefused` shows only the c2 refusal, and the bridge invariant shows only non-shipping; the discard and the count are observations of the real issuer (`staging_harness`, §5). **E10-TMP-03** (verifier side): → `INVALID / TIME_AFTER_DECLARED_DELTA` (row 12.2). **New**; L-33 overlaps only partly. Related: **E10-ISS-02**, where the wall-clock companion `C_WallClock_Red.out` ships a receipt that fails conjunct 3. |
| G | G5 |
| Choice | The bridge has no refusal state, so "refuse" is read as "Ship is never taken in this state". This is a witness plus an invariant. It is not the registered companion, which stays unbuilt. |

### 3.4 The P9 two-machine case (mapped; source is a non-discharging probe)

| | |
|---|---|
| Registered | A4.1(ii) as written by A5.1 (`phase-0-prereg-amendment-5.md:58-91`; docket item 30, `band-1-docket.md:99-104`). The registered vector has four parts: an expected-verdict oracle; two isolated machines; the same bundle twice on one machine; and a reachable service that contradicts the bundle. |
| Traces | All from `formal/spike/tla-probes/P9/`: `P9_Statelessness_LiveFailclosed_Vector.out:29-75` (both machines agree on UNVERIFIABLE; the bundle determines INVALID; `Purity` red); `P9_Statelessness_ReplayLatch_Full.out:30-88` (VALID_STRICT, then INVALID, on one machine); `P9_Statelessness_LiveFallback_Full_Agreement.out:30-121` (VALID_STRICT while the service is unreachable, INVALID after `ServiceChange`). The probe is TLA+ and **non-discharging**: its green results are filed and not cited, and these red traces are used only as scenario sources. |
| Vectors | **E10-P9-01** (two isolated machines, each compared with the expected six fields, over A-a, L-36b and L-09); **E10-P9-02** (same bundle repeatedly on one machine: A-a, A-a, L-36b, A-a); **E10-P9-03** (contradicting live DNS, git remote, calendar and API, one step each after an isolated baseline). All **new**. Each file's `sequence` gives the hosts, step order, environment per step and pass rule; the bundles are fixtures. |
| G | G8 |
| Choice | The probe's "optional service" is a revocation view, and V1 consults none. "Which services" is taken from the input list of `formal/P9-CONTRACT-INSPECTION.md`. |

### 3.5 The P7 verdict-independence case (**not mappable as registered**; a V1 analogue is given)

| | |
|---|---|
| Registered | A6.1 (`phase-0-prereg-amendment-6.md:44-53`; docket item 32): a wrapped bundle's inner verdict equals the standalone verdict, under each of the four P4 verdict values, with a re-serializing wrapper as the red bar. |
| Why not as registered | V1 has no wrapper. Two layers are `UNVERIFIABLE / OUT_OF_PROFILE` at dispatch D3, so an inner verdict is never computed inside a wrapper. `VALID_DEGRADED` does not exist in V1. A9 row 26 (`phase-0-prereg-amendment-9.md:490`) moved P7's wrapper half and this H1a vector to *Wrapping and renewal* (A9.3). The registered vector therefore belongs to a later profile. |
| Model side | S-P7 Q4. The opaque control is green, with N1 `HonestWrappedAccepted` reachable (`formal/suite/s-p7/proverif/sp7_q4_control_opaque_twoversion.out:560,574,588,926`). The re-serialization companion is red, with N1 unreachable (`sp7_q4_companion_reserialize_twoversion.out:604`). |
| V1 analogue | **E10-P7-01**: an inner container embedded as opaque base64 in `content`, using inners A-a, KEY-a, L-07 and L-09. The outer verdict is `VALID_STRICT`; the inner bytes are byte-identical and keep their standalone verdict. **E10-P7-02** is the harness red bar: JCS re-serialization turns L-07's INVALID into VALID. **E10-P7-03** is the two-layer form: `OUT_OF_PROFILE`, covered by L-04 and L-05. |
| Choices | "Wrapper" is read as opaque content. Three verdict values instead of four. The red bar tests the embedding harness, not the verifier. |

## 4. The checked V1 models, one by one

| Model | Used for | Not mapped, and why |
|---|---|---|
| **P4** `formal/tla/P4_VerifierStates.tla` | P4-01 (`_Broken.out:28-34`, c5 unperformable → git absent, L-09); P4-02 (`_Broken_Green.out:32-38`, c2 → receipt pending, L-43); P4-03 (degraded request, L-06/L-06s); P4-04 (precedence, A-d3); TMP-11/12 | `c1..c5` are uninterpreted. Mapping a model check to a V1 check is a reading (READING-AID-P4 cast table), and it is listed as a choice in each file. |
| **P5P6** `P5P6_TemporalRevocation.tla` | TMP-01 (`_BrokenConf.out:35-44`); TMP-04 (`_Sanity.out:53-62`); TMP-07/08/09 (`_BrokenTol.out:37-46`, `_BrokenTolStrict.out:35-44`); TMP-10 (`_Broken.out:38-47`) | **P6 (revocation) diverges by design.** The model rejects; V1 reports `VALID_STRICT` with `revocation: NOT_EVALUATED` (A9 cases e, e′). TMP-10 records this divergence and is covered by A-e. The receipt-tolerance variables have no V1 field (profile 2.2). Their carriers, signed `content` and unsigned `issuer_record`, are a choice. |
| **P5c** `P5c_IssuanceProtocol.tla` (k = 6 runs in `k6-2026-09-14/P5c/`) | ISS-03 (`_Broken_k6.out:25-96`); ISS-04 (`P5c_k6_d6_Sanity.out:475-762`, refusal after three expired attempts); TMP-12 | The reorg witnesses (`ReorgShipUnreachable`, `RefusalAfterReorgUnreachable`) are issuer-internal: a bundle shows no reorg. A3.7.2's extended refusal record is not modelled (its PROPERTIES row is open), so ISS-04 expects only "no receipt, refused, latched". |
| **Bridge** `P5cP5P6_Bridge.tla` (k = 6 in `k6-2026-09-14/Bridge/`) | TMP-01/02 (`W_LateBurial…`, `C_AnchorSubst_Late`); TMP-03 and ISS-01 (E10 re-check, §3.3); TMP-04 (`W_NonMonotonicShip…:25-114`); TMP-05 (`W_EpsilonSide…:25-123`); TMP-06 (`W_WallClockDivergence…`, final Ship state 172-178); ISS-02 (`C_WallClock_Red.out`, Ship state 180-186) | The committed k = 3 `.out` files (2026-07-21) name action lines (Tick at line 101, etc.) from an earlier version of the module. The k = 6 runs cite the current lines (Tick at 119 = module lines 118-121). The k = 6 traces are therefore the ones cited. **BridgeSlack{,_Latch}** is evidence for the clock-precedence ruling, not protocol semantics (its own header), so no vector is drawn from it. |
| **E6a** `formal/tla/E6a/` | E6A-01 (FailOpen, `runs/broken/E6a_Broken_FailOpen_V1.out:45-50`); E6A-02 (MissingSigAsEvidence, `:44-49`); E6A-03 (MissingEvidenceAsFail, `:44-49`); E6A-04 (UnknownDominates and UnknownAsOutOfProfile, `:44-49`); E6A-05 (DispatchFallthrough, `:33-38`); E6A-06 (MalformedAsUnknown, `:45-50`); E6A-07 (`E6a_Props.tla:117-121` with RESULTS §6 obs. 1) | E6a gives each slot its own alg, but V1 has one common alg (rows 6.2–6.3). So the mixed-slot counterexamples cannot be reproduced exactly; the choice is recorded in E6A-01 and E6A-04. **E6A-07 is a model/profile divergence**: a wholly absent `a_sig` is INVALID in the model (A9 C3, "missing signature fails") but `UNVERIFIABLE / MEMBER_MISSING:a_sig` in the profile. Both are fail-closed. The file expects the profile's value and flags the divergence. The owner has ruled: V1 governs (profile §13 note 13, author-accepted in E9 row 3). |
| **S-P1** `formal/suite/s-p1/` | SP1-01 (Q3 companion, `sp1_q3_companionA_sig_unbound.out:330-331`, degraded; strict counterpart capstone C-C5 `cap_cc05_a.out:4393…`); SP1-02 (Q4 companion, `sp1_q4_companionB_frame_unsigned.out:327-328`, degraded only); SP1-03/04 (Q1 strict `sp1_q1_strict_{dns,repo}_compromised.out:201`; capstone `capstone.out:5554`, `capstone_b.out:5585`) | Q2 is degraded, and its V1 analogue is the accepted limit (CAP-01). S-P1's strict review mutant `m_D_signature` has no archived `.out`, so it is not cited. **SP1-02 has no strict run.** |
| **S-P2** `formal/suite/s-p2/` | SP2-01..03 (Q3, `sp2_q3…out:354-520`; strict d7 `diagnostics/d7_strict_q3_mutation.out:564`; capstone C-C9 `cap_cc09_a.out:3505,6176`); these are A1.7's own example ("manifest requires {KMS, GPG}, bundle carries only KMS → INVALID"). SP2-04 (Q4; strict d8:645, d11:654,922; C-C17); SP2-05 (Q5-C2 `:363-535`; strict d9:395 green); SP2-06 (d12 `:1362-1428`; Q6-C; capstone C-C16 `cap_cc16_a.out:4014,6605`) | The one-signer manifest M1 is a V1 `SCHEMA` failure, so it is not realisable. **The S-P2 strict models have no content-equality check and no Spliced query.** SP2-06's strict evidence is the capstone run. The duplicate-signature case (S-P2 F8a) was never run, so no vector is drawn from it. d7–d12 are unregistered diagnostics: scenario sources, not discharge. |
| **S-P3** `formal/suite/s-p3/` | G10-01..03 (Q2 `sp3_q2_degraded_compromised.out:195,200`; Q5 `sp3_q5_multikey_correct.out:314,320,326`); SP3-01 (Q4 companion `sp3_q4_companionB_possession_unnamed.out:383`, covered by POS-a) | **Reading S-P3's degraded, sole-compromised-channel model as V1 strict with both channels captured is the extractor's reading.** It is listed as a choice in the G10 files. DSKS with a known private key is not achievable for fixed-generator P-256, so the captor's own key K′ stands in for the derived key. The hybrid ladder H1–H4 is degraded-only. Its V1 face is HY-ak-C and HY-N3, already in the 352. |
| **S-P7** `formal/suite/s-p7/` | P7-01/02 (Q4); P7-04 (Q3 companion `sp7_q3_companion_type_unchecked.out:727`; capstone C-C13(i) `cap_cc13i_a.out:4042,6460`) | Q5, Q5c, Q6a and Q6b (re-scoping through wrappers) and Q7 (recorded version) have no V1 bundle: wrappers stop at dispatch, and V1 has one canonicalization version (CODEC-a). |
| **Capstone** `formal/suite/capstone/` | CAP-01 (C-C1 `cap_cc01_c.out:14277`, the accepted limit, AUTH-i-T); G10-01..03 (C-C1 greens `:9737,9959,14743`); CAP-02 (C-C7(ii) `cap_cc07ii_a.out:12156…`); CAP-03 (C-C7(i) `cap_cc07i_a.out:9385…`); CAP-04 (C-C3=C-C8 `cap_cc03_a.out:3795,4199`); strict counterparts cited in SP1-01, SP2-0x, P7-04 | Not mapped: standing (C-C11, C-C12, C-C18, C-Q6/Q10, A8.4); wrappers (C-C13(ii), C-C15, C-Q4, link 6b); every degraded (d) file, including the eleven `.notrun` files and the 2026-10-09 slice batch; the second issuer, one-signer sets and `skAdv` enrolment. The strict greens C-C2, C-C4, C-C6 and C-C8-i give no evidence that RC-b and RC-c are *necessary*: those checks are required by the spec, not shown necessary by the model. **No companion ran in case (c)**, so G10-01..03 rest on S-P3 and on C-C1's greens, not on a red companion. |

Contract rows with no model source, so no E10 vector: **G6** (A-UTC, unchecked by design); **G7**'s window endpoints;
**G4** beyond abstract authority (concrete DNSSEC and git are not modelled). See V1-CONTRACT §5, "Gaps".

## 5. Running against AWS (20 Nov): what each vector needs

Each file's `live.modes` names one or more of these modes (legend also in `INDEX.json`):

| Mode | Meaning | Vectors |
|---|---|---|
| L0 | Post-issue edit of a real receipt from the AWS issuer; the service verifier runs with the release trust configuration. No service cooperation. | 34 vectors include L0 (INDEX) |
| L1 | Attacker-held keys and re-signing by the tester | SP1-03/04, SP2-04, E6A-01, P4-04, G10-*, CAP-01 |
| L2 | Authority channels the tester controls: a staging domain, repository and trust configuration, or the TEST universe. **Never the production `wamason.com` channels.** | SP1-03/04, G10-*, CAP-01, P9-03 |
| L3 | Frames signed by the service keys over inputs the tester chooses. Needs the TEST issuer, or a staging-only adversarial hook. | SP1-02, SP2-06 (has an L0 variant: splice two real receipts), CAP-04 |
| L4 | Chosen Bitcoin header times. TEST universe only: synthetic chain and TEST pins. Mainnet cannot produce these. | TMP-01..08, ISS-01/02 |
| L5 | Issuer behaviour under fault injection or a simulated chain/clock | ISS-01..04 |
| L6 | Control of the verifier's environment: network isolation, two hosts, a reachable service that contradicts the bundle | P9-01..03 |

**What this means for the service:**

- **Verifier interface.** The service verifier must accept the run.py contract (`prototype/conformance/run.py:6-24`):
  `--trust` and `--bundle`, a request input, and the six stable fields plus `utc_assessment` on stdout. It also needs
  a mode that loads a **TEST release and trust configuration**. Without that mode, the L4 temporal vectors (late
  burial, A3.9, the ε side, the tolerance cases) cannot run against the AWS verifier at all: their header times
  cannot be chosen on mainnet.
- **Issuer test surface.** ISS-01..04 keep the status **requires staging harness**. Each file's `staging_harness`
  defines the sequence, the observations, at least one control, and the pass rule:
  - **ISS-01**: chain held at six confirmations with nTime(h*) = d + δ + 1 and nTime(h*+5) = d + δ − 1. Observe
    the decision record (c2 = false), the attempt's discard transition, and the counter increment. Control: both at
    d + δ ships.
  - **ISS-02**: the harness drives the lifecycle clock W and records it, the confirmed proof, and the decision
    point. The refusal must occur before the attempt's expiry and must not be an expiry. Control: nTime(h*+5) =
    d + δ ships under the same W schedule.
  - **ISS-03**: the chain is held at 1..5 confirmations, with API and outbox observed at each, and then the sixth is
    released. The model's DepthK = 5 counts successors of the including block (`P5c_IssuanceProtocol.tla:202,
    262`), so depth 5 means **six confirmations**, h*..h*+5.
  - **ISS-04**: three expiries are observed, then the refusal. Availability is then restored and late evidence
    delivered, and the refused request must never ship, including across a restart. Controls: recovery during
    attempt 2 ships with no refusal, and a frozen clock produces neither expiry nor refusal (stalled is
    distinguished from latched).

  Run in real time, ISS-04 would take about 3 × 96 h. Through the public API alone, only ISS-03's bundle half can be
  observed: any returned receipt must hold h*..h*+5 for all three proofs. Polling cannot exclude a premature
  shipment. ISS-01..03 also have TEST-issuer oracles (`fixtures/E10-ISS-0n.test-{refuse,control}`). They fix the
  pre-ship decision only.
- **P9 vectors** test the distributed verifier release, not an API. A verifier behind a network API cannot be the
  system under test for "no network". P9-02 does apply to the API, though: repeat submissions must give the same
  six fields.
- **Real material.** L0 vectors need one or two real receipts. CAP-03 and the L0 variant of SP2-06 need two receipts
  with different content. SP3-01's L0 form needs no signing: it copies the receipt's own S_kms into
  `possession.kms` (E10R-05). P7-01 needs a receipt whose content embeds another bundle, issued as an ordinary client
  request.

## 6. Coverage against the 352 conformance cases

- **53 vectors: 39 new, 14 covered; 68 verifier subcases.** A vector is *covered* when at least one of its subcases
  has an exact match: a conformance case that builds the same bytes or the same construction.
- **Covered** (`covered_by`, exact only; *analogous* cases in `analogous_to`): TMP-01 (L-36b, UTC-06), TMP-04 (L-38;
  analogous UTC-03, whose T is 14:00Z, not 12:20Z), TMP-10 (A-e; analogous A-e2), TMP-11 (L-43b, UTC-08), P4-01
  (L-09), P4-02 (L-43), P4-03 (subcase `.degraded` = L-06; the control `.strict-control` = L-06s, which is
  `VALID_STRICT / OK` and is no longer under the degraded expectation), P4-04 (A-d3), E6A-01 (subcase `.i` = HY-b2-H,
  `UNVERIFIABLE / ALG_UNKNOWN`; subcase `.ii` = HY-e1-C, `INVALID / RECEIPT_COMMON_MISMATCH`; analogous ALG-01),
  E6A-05 (L-03b; analogous L-03, L-04b), P7-03 (L-04, L-05), CAP-01 (AUTH-i-T), SP3-01 (subcase `.POS-a` = POS-a;
  the L0 subcase is a new construction; analogous HY-N3), POS-01 (A-a, L-06s).
- **New:** every other vector. 16 of them name a `partial_overlap`: an existing case that tests the same row by
  another path or combined with another failure. The new vectors that close gaps V1-CONTRACT §5 names are:
  - **G10's honest-material transplant tests** (G10-01..03; the contract's "tests missing" row);
  - **one-channel capture** (SP1-03/04);
  - **the isolated content splice** (SP2-06);
  - **gpg-slot stripping** (SP2-01..03);
  - **the A3.9 c2/c3 divergence** (TMP-03);
  - **the P9 vector** (P9-01..03).

## 7. Findings recorded while extracting (no change made)

1. **A3.9's bridge companion `_BrokenConjunct3Only` was registered and never built.** §3.3 supplies a witness and an
   invariant, not the companion.
2. **The headers-missing case has no temporal-model source.** It rests on P4 plus A2.2's text (§3.2).
3. **The P7 vector as registered belongs to a later profile** (A9 row 26). The V1 analogue in §3.5 is a substitute.
   It does not discharge the registered vector.
4. **Two model/V1 divergences are visible in the vectors.** TMP-10: P6 rejects, V1 does not evaluate revocation.
   E6A-07: a missing `a_sig` is INVALID in the model and UNVERIFIABLE in the profile.
5. **Committed bridge `.out` files at k = 3 cite stale action line numbers** (§4, bridge row). The k = 6 runs are
   current.
6. **Several companion reds are degraded-only.** These are S-P1 Q3/Q4 and S-P2 Q3/Q4/Q5. Strict counterparts exist
   for all of them except S-P1 Q4 (SP1-02), which rests on a degraded trace only.
7. **Expected codes for multi-row mutations are readings of §15.7.** Examples: G10-01's row 4.2 before 6.1;
   E6A-06's gpg `SCHEMA`; the `a_sig`-edit cases' T = null. The independent verifier agrees with every one on the
   materialized fixtures (§8). The non-author review of the concretizer should confirm them before 20 Nov.

## 8. Concretizer, fixtures and the independent run (E10R-01)

- **What it is.** `formal/e10/materialize.py` turns each verifier subcase into a concrete TEST-universe fixture
  through the TEST issuer's issue path (`prototype/conformance/issue.py`), plus named post-issue edits. The fixture
  layout is the one `prototype/conformance/run.py` consumes. Reused conformance constructions are called unchanged
  from `cases.py`.
- **Oracle and construction are separate.** The expected report is data in the vector file, and the materializer
  copies it into `expected.json`. It never computes a verdict or reason. Its one cross-check is T and U: where the
  fixture is issuer output and the expected T is non-null, T must equal the issuer plan's nTime(h*) and
  `utc_upper_bound` must equal `issue.expected_U`. Otherwise the run stops.
- **Reproducible.** `materialize.py --check` rebuilds everything into a temporary directory and compares it with
  `fixtures/MANIFEST.json`. That manifest holds the sha256 of every output and of every source (the materializer,
  the vector files, and `issue.py`, `cases.py`, `universe.py`, `tcrypto.py`). The 2026-10-26 check found no
  differing file. All keys, nonces and chains are deterministic TEST material.
- **Outputs.** There are 68 subcase fixtures and 6 issuer TEST oracles. The issuer oracles show refuse on c2 /
  ship at the boundary (ISS-01), refuse on c3 / ship at c3's boundary (ISS-02), and refuse without h*+5 / ship
  with it (ISS-03).
- **Independent run.** `run.py` was run with the independent verifier through `prototype/differential/adapter.py`
  (command in the materializer's docstring). Result: **68/68 AGREE** on the six stable fields, `utc_assessment`
  and `detail` (`fixtures/RUN-INDEP.json`). This is one more implementation agreeing with the extractor's reading.
  It is not the non-author review of the concretizer.
- **What the fixtures are not.** They exercise each vector's construction in the TEST universe. The AWS service is
  not exercised. The L0 subcases are the shape of the post-issue edit to apply to a real receipt. The issuer vectors
  and the P9 environments are not fixtures; they are defined in `staging_harness` and `sequence`.
