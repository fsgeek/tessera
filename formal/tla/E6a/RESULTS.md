# E6a: the unknown-algorithm transition, with companions. TLC results, 2026-10-19

> **STATUS: PROPOSED.** Produced by the AI collaborator (owner work, Claude Opus 5.5) on 2026-10-19. Not adopted;
> the commit is the author's. This file covers exit item E6a (A9 §A9.2, "E6a with companions"; A3 §A3.6.2 item 3).
> It changes no registered sentence. `formal/tla/P4_VerifierStates.tla` was **not edited**: sha256
> `899ebd01…a609` before and after. It was re-run unchanged and reproduces its committed results (§5).
> **Not done yet:** the time-boxed Codex falsification pass (`docs/V1-EXIT-30OCT.md` §11, 0.5 d) and the author's
> E9 read. So this is `checked` (the tool passes), not `discharged`.

## 1. What the models claim

**Claim (plain language).** Take one presented input. A verifier that follows the rules gets these verdicts:

- An algorithm id that is well-formed and correctly bound but unsupported gives `UNVERIFIABLE` (reason
  `ALG_UNKNOWN`). This holds only when nothing else definitely failed. It is the only algorithm case that gives
  `UNVERIFIABLE`.
- These give `INVALID`: a missing id, an encoding mismatch, malformed parameters, an id prohibited by policy, a
  substituted id, and a known algorithm whose signature fails.
- An unknown algorithm never gives any `VALID` verdict, under any legal policy.
- **Mixed case.** If any required check definitely fails, the verdict is `INVALID`, even when an unknown algorithm or
  missing evidence is also present (A4 §A4.2).
- **Missing signature versus missing evidence.** A missing or stripped required signature is a failure: `INVALID`,
  whatever the algorithm (A9 C3; spec V28). A missing required evidence member cannot be checked: on its own it gives
  `UNVERIFIABLE / MEMBER_MISSING`, never `VALID`, and never `INVALID` by itself.
- **Dispatch.** An out-of-profile input gives `UNVERIFIABLE / OUT_OF_PROFILE`, and nothing else is evaluated (A9.5).
  `OUT_OF_PROFILE` never arises after dispatch.
- Every in-profile verdict is exactly P4's `VerdictFor`, applied to the per-check outcomes the input produces.

**The adversary.** Here the adversary chooses the input. In one state, every slot has an algorithm form (7 forms), a
signature form (absent, bad or good) and an evidence form (absent, bad or good). Dispatch is in or out, and the
policy is any legal waiver set. TLC enumerates **every** combination: 7,938 states in the V1 instance and 15,876 in
the general one. The broken companions are the other half. Each one is a verifier with one specific defect, and it
must go red.

**Boundaries. These are not claimed:**

- *Instance.* The instance is fixed: two slots, two evidence members. V1 has no waivable check. The general instance
  makes one evidence member (git) waivable.
- *Codes.* The model has five reason classes. It does not choose among concrete `INVALID` codes, and it does not
  model the total check order beyond one rule: row 2.2 `MEMBER_MISSING` comes before row 7.1 `ALG_UNKNOWN`.
- *Classification.* Which bytes count as "the signature" and which as "evidence" is the profile's assignment. The
  model takes the classes as given; see §6.
- *Slots.* Waiving a whole signature slot (P2's degraded subset) is not modelled. Neither is cross-slot alg
  equality (V1 row 6.2).
- *Not covered.* Codecs, bytes, keys, time and the adversary's cryptographic actions belong to P1/P3/P7/P8 and the
  symbolic suite.
- *Instruments.* The conformance cases cited below are instrument material. They inform this mapping and discharge
  nothing (A9 instrument rule).

## 2. Files

| File | Role |
|---|---|
| `E6a_Base.tla` | Inputs, `Init`, the check set, and `VerdictFrom` / `ReasonFrom`, which instantiate **P4's own `VerdictFor`** (parametrized `INSTANCE P4_VerifierStates`, found through `-DTLA-Library=formal/tla`). |
| `E6a_Props.tla` | All 32 invariants and 13 vacuity witnesses, stated once over the raw inputs. Every module instantiates it, so the companions are checked against exactly the formulas the correct model is checked against. This avoids the P4 `_Broken` copy drift, where only 7 of 11 invariants were carried (2026-09-06 review item 5). |
| `E6a_AlgVerdict.tla` | The correct model: the classification of inputs into check outcomes. |
| `E6a_Broken_*.tla` (7) | The companions. Each differs from the correct module only on lines marked `BROKEN`. Each header records its predicted red set, written before any run. One prediction (DispatchFallthrough) was revised before its first run; the revision is noted in the file. |
| `E6a_V1.cfg`, `E6a_General.cfg` | The main configurations, with all 32 invariants. |
| `run.sh` | Regenerates everything in `runs/`. TLC 2026.07.31 (`~/.local/lib/tla2tools.jar`), `-workers 1`. |
| `runs/SUMMARY.tsv` | One row per TLC run (495 runs). `runs/main`, `sanity`, `broken`, `matrix` (one log per companion and instance, 32 runs each) and `p4-rerun` hold the raw outputs. |

## 3. Results

### 3.1 Correct model: all GREEN, as registered

| Run | Invariants | Result | States |
|---|---|---|---|
| `E6a_AlgVerdict` + `E6a_V1.cfg` | all 32 | **GREEN** | 15,876 generated, 7,938 distinct, depth 1 |
| `E6a_AlgVerdict` + `E6a_General.cfg` | all 32 | **GREEN** | 31,752 generated, 15,876 distinct, depth 1 |

### 3.2 Vacuity witnesses, one run each

Healthy means RED: the situation is reachable.

| Witness (conformance shape) | V1 | General |
|---|---|---|
| `NeverInStrict` (A-a) | RED | RED |
| `NeverInInvalid` | RED | RED |
| `NeverOutOfProfile` (L-01…L-06) | RED | RED |
| `NeverAlgUnknown` (ALG-01, L-21) | RED | RED |
| `NeverUnknownOpaqueBadSig` (HY-b2-H) | RED | RED |
| `NeverMixedFailedUnknown` (L-107) | RED | RED |
| `NeverUnknownEmptySig` (ALG-02) | RED | RED |
| `NeverMissingSignature` | RED | RED |
| `NeverMemberMissing` (L-09, L-10) | RED | RED |
| `NeverMissingEvPlusUnknown` (AGG-d) | RED | RED |
| `NeverDefectPlusMissingEv` (A-d3) | RED | RED |
| `NeverInDegraded` | **GREEN** (expected: V1 has no waiver) | RED |
| `NeverWaivedAbsentDegraded` | **GREEN** (expected, same reason) | RED |

Every implication in §3.1 has a reachable antecedent in the instance where it is meant to bite. The two V1 greens are
the strict-only result: `NoDegradedWithoutWaivable` holds in both instances.

### 3.3 Broken companions: every one RED

There are two kinds of run per companion:

- An all-invariants run, which stops at the first violation.
- A **per-invariant matrix**: 32 single-invariant runs in each instance, which gives the exact red set.

**All 14 matrices (7 companions × 2 instances) match their predicted red sets exactly**: no extra reds, none
missing, no TLC errors. Every green matrix run covered the full 7,938 or 15,876 states.

| Companion (defect) | First red (all-invariants run, V1) | Exact red set (V1; General identical unless noted) |
|---|---|---|
| **FailOpen.** An unknown alg is treated as passed, and its opaque signature is accepted. **This is the registered A3.6.2 item 3 companion.** | `UnknownAlgGivesUnverifiable`. Counterexample: kms supported/good, gpg **unsupported/bad**, evidence good → the broken verifier says `VALID_STRICT` | `UnknownAlgGivesUnverifiable`, **`UnknownAlgNeverValid`**, `AlgUnknownReasonExact`, `ExactUnverifiableIn`, `ExactStrictIn` (5). General adds `ExactDegradedIn` (6) |
| **MalformedAsUnknown.** Every non-supported id form is treated as unknown | `InvalidAlgFormsGiveInvalid` (gpg alg *missing* → `UNVERIFIABLE`) | `InvalidAlgFormsGiveInvalid`, `AlgUnknownReasonExact`, `MixedFailedUnknownInvalid`, `MixedFailedMissingEvidenceInvalid`, `ExactInvalidIn`, `ExactUnverifiableIn` (6) |
| **MissingSigAsEvidence.** An absent signature is treated as unperformable | `MixedFailedMissingEvidenceInvalid` (both signatures and both evidence members absent → `UNVERIFIABLE`) | `AlgUnknownReasonExact`, `MixedFailedUnknownInvalid`, `MixedFailedMissingEvidenceInvalid`, **`MissingSignatureInvalid`**, `ExactInvalidIn`, `ExactUnverifiableIn` (6) |
| **MissingEvidenceAsFail.** Absent evidence is treated as a failure | `MissingEvidenceUnverifiable` (evidence absent, all else good → `INVALID`) | `UnknownAlgGivesUnverifiable`, **`MissingEvidenceUnverifiable`**, `InvalidNeedsDefect`, `ExactInvalidIn`, `ExactUnverifiableIn` (5) |
| **UnknownDominates.** An unknown alg overrides A4.2 precedence (the shape of Codex finding 11) | `AlgUnknownReasonExact` (unknown alg plus absent signatures → `UNVERIFIABLE / ALG_UNKNOWN`) | `InvalidAlgFormsGiveInvalid`, `KnownAlgBadSigInvalid`, `AlgUnknownReasonExact`, **`MixedFailedUnknownInvalid`**, `MixedFailedMissingEvidenceInvalid`, `MissingSignatureInvalid`, `MissingEvidenceUnverifiable`, `ExactInvalidIn`, `ExactUnverifiableIn`, `AgreesWithP4` (10) |
| **UnknownAsOutOfProfile.** An in-profile unknown alg is handled as a terminal dispatch rejection | `OutOfProfileOnlyAtDispatch` | The 10 above, plus `OutOfProfileOnlyAtDispatch` (11) |
| **DispatchFallthrough.** Out-of-profile input is evaluated anyway | `DispatchTerminal` (dispatch out → evaluated) | **`DispatchTerminal`**, `AlgUnknownReasonExact`, `InvalidNeedsDefect` (3) |

**Finding: P4 alone is blind to all five classification defects.** For FailOpen, MalformedAsUnknown,
MissingSigAsEvidence and MissingEvidenceAsFail, all eleven `P4_*` formulas stay green, and so does `AgreesWithP4`.
For UnknownDominates and UnknownAsOutOfProfile, the eleven `P4_*` formulas stay green. The defect sits in how inputs
become check outcomes, upstream of the function P4 checks. This is why E6a's invariants are stated over the raw
inputs rather than the status map.

## 4. Mapping to the conformance reason codes

| Model situation | Model verdict / reason | V1 code (profile §15.7 row) | Conformance cases (all AGREE, differential run 5) |
|---|---|---|---|
| dispatch out | `UNVERIFIABLE` / `OUT_OF_PROFILE` | rows 1.1–1.4 `OUT_OF_PROFILE` | L-01, L-01b–d, L-02, L-03, L-03b, L-04, L-04b, L-05, L-06 (11) |
| alg `unsupported`, no defect, no missing evidence | `UNVERIFIABLE` / `ALG_UNKNOWN` | row 7.1 `ALG_UNKNOWN` | ALG-01, L-21, HY-a1/a2/a3-C, HY-ak-C, HY-b1-H, HY-d1/d2-C, HY-d1/d2-H (11); HY-b2-H is the unknown alg with a non-verifying opaque signature |
| unknown alg + absent signature | `INVALID` | row 3.1 `SIG_EMPTY` | ALG-02, HY-a4-C. (ALG-03 is a non-empty 65,537-byte signature rejected with `LENGTH_CAP`: a signature-codec defect, which the model does not represent as a separate class. Corrected 2026-10-19, review E6A-01.) |
| alg `substituted` | `INVALID` | row 6.3 `RECEIPT_MANIFEST_MISMATCH` | ALG-04, ALG-05 |
| alg `missing` / `malformed` / `encoding_mismatch` | `INVALID` | codec rows 3.1 / 4.1 (ENC order) | codec cases. (HY-N4 is a truncated signature rejected with `SIG_FORMAT`, a signature-codec defect, not a malformed algorithm id. Corrected 2026-10-19, review E6A-01.) |
| alg `prohibited` | `INVALID` | none: V1's `alg_prohibited` is `[]` | none (unreachable in V1) |
| alg supported, signature bad | `INVALID` | row 9.2 `SIG_INVALID` | F10-f, HY-N2, HY-N6 |
| unknown alg + independent failure (**mixed**) | `INVALID` / `FAILED` | the failed row's code | L-107 (`BUNDLE_OBJECT_HASH`) |
| evidence absent, no defect | `UNVERIFIABLE` / `MEMBER_MISSING` | row 2.2 `MEMBER_MISSING:<path>` | L-09 (case d2), L-10, F03-e, F03-j |
| evidence absent + unknown alg, no defect | `UNVERIFIABLE` / `MEMBER_MISSING` | row 2.2 before row 7.1 | AGG-d |
| defect + evidence absent (**d3**) | `INVALID` | the failed row's code | A-d3 (`DNS_KEY_MISMATCH`) |
| all present and good, strict | `VALID_STRICT` / `OK` | `OK` | A-a |

## 5. P4 kept intact

`run.sh` re-runs P4's committed configurations, unchanged, into `runs/p4-rerun/`. Every result matches the committed
`.out` files:

| Run | Result |
|---|---|
| main | GREEN, 1,944 distinct |
| Sanity (`-continue`) | all four witnesses violated, 1,944 violation reports, the same as committed |
| `_Broken` | RED `StrictMeansEverything` |
| `_Broken_Green` | RED `NoSilentPromotion` |
| `_Broken_Green2` | GREEN |

*Harness note:* the first `SUMMARY.tsv` row for P4 Sanity said GREEN. That was a classifier bug: under `-continue`,
TLC also prints "No error has been found". The row and `run.sh` were corrected; the raw output was always correct.

## 6. Observations for the owner (no change made)

1. **What counts as a "missing signature" in V1.** The model follows A9 C3 ("a missing, stripped or substituted
   one fails") and spec V28: a required signature that is absent is `INVALID`. Here is what V1 does with absent
   signature material:
   - A signature stripped *inside* a present `a_sig` fails in the codec: `SIG_EMPTY` / `TRUNCATED`, `INVALID`. This
     matches the model.
   - An absent `possession.<slot>` member is `UNVERIFIABLE / MEMBER_MISSING` (F03-j). So is a wholly absent `a_sig`
     member (profile §2.1 and the §15.1 closed schema; no conformance case exists for this).

   The profile therefore classes those two absences as *missing evidence*. Both outcomes are fail-closed, so nothing
   is falsely accepted. But whether they are consistent with C3's "fails" is the owner's reading to record. The
   model does not decide it.
2. **Companion count.** The derivation asked for three companions: the fail-open companion, the mixed case, and
   missing-signature versus missing-evidence. They are FailOpen, UnknownDominates/UnknownAsOutOfProfile, and the
   MissingSig/MissingEvidence pair. The other two (MalformedAsUnknown, DispatchFallthrough) test the "exactly one
   case" boundary and the dispatch gate. They were cheap and are recorded as extras.
