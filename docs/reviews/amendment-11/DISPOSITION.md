# Amendment 11 review: owner disposition (2026-10-28)

The review is `CODEX-REVIEW.md` (verdict: not ready; A11-01 to A11-07, two prechecks FAILED). All findings were
applied to the draft. The revised draft goes to one confirmation pass before the author.

| ID | Sev | Disposition |
|---|---|---|
| A11-01 | High | All six A1 fields are kept, with per-algorithm readings (§A11.2 item 1). The evidence is pinned by `FLOOR-MANIFEST.sha256`, whose hash is fixed at signing and must be regenerated if any listed file changes first. Discharge conditions (a)–(d) require the deployed-zip identity check, and an unresolved defect blocks discharge. Adoption is distinguished from discharge. |
| A11-02 | High | Disclosed as a retrospective relaxation after the deadline and after the code existed. The historical qualification is kept and does not extend to the replacement. R5b is cited, with why it does not settle the question. The hybrid with the replacement depends on the ruling. |
| A11-03 | High | Accepted against the owner. `DEPLOY.md` reused the spike keys, contradicting HYBRID-SUPPLEMENT §11 item 6. Reversed: production uses new keys. Added as sweep item 3. §A11.4 now requires owner decisions on registered parameters to be checked first. |
| A11-04 | High | Condition (i) preserves every A9.6 custody and policy requirement, plus the frozen record's properties. Conditions (iii) and (iv) define the re-earned evidence and the identification of the tested image and configuration. |
| A11-05 | Med | §A11.2 item 5 distinguishes security-policy findings (historical security, beside the verdict) from conformance defects (fixed in a named release, never preserved). |
| A11-06 | Low | The split is stated: 219 DER cases at library level, 21 P1363 cases reaching neither interface. |
| A11-07 | Med | Each outcome-informed change is disclosed separately. The blanket claim of vacuity is replaced (only the two curve fields lack a referent for ML-DSA). The stale PENDING sentence is removed. |
| H3 | — | Wording changed to "AWS-based examples". A measurement protocol is required before measurement, and redefining the window as a demonstration is ruled out. |
| Citations | — | The custody citation is pinned to `270ca49:docs/V1-PROFILE.md:1023-1037`. S1 is cited as an owner operational resolution (`V1-SERVICE-RESOLUTIONS.md:20`). The stale supplement locator is corrected in §A11.3. |
| Precheck: trigger | FAIL→fixed | A11-02 |
| Precheck: binding text | FAIL→fixed | S1's authority level is stated |

## Confirmation (`CODEX-CONFIRM.md`): owner disposition

Six findings were CLOSED, A11-01 was PARTIAL, and the wider sweep found one registered commitment and two stale
defaults. All four prechecks PASSED.

| ID | Disposition |
|---|---|
| A11C-01 (High) | `check_zip` now requires that the zip's `tessera_verify/` hold exactly the tested verifier's files, byte for byte, as well as the wheel identity. Negative control (owner, 2026-10-28): the real package passes, and the same package with one byte changed in `codec.py` fails, naming the file. (A first control run failed on both zips because the owner's harness shared a `ZipInfo` between two archives and corrupted a CRC. That was a harness bug, found and fixed before the result was read.) The manifest was regenerated and its new hash is in A11 §A11.2. |
| K-R (sweep C1) | Added as A11 §A11.5 item 5, with a §A11.3 row and a header disclosure. The assumption (K-R) is unchanged; the enforcement wording (who computes μ, who may `kms:Sign`) goes to the author. The placement decision's "changes no registered sentence" is corrected in place. |
| Spike-key defaults (sweep C2) | `service/signer-gcp/deploy.sh` has no production-key defaults. It requires `SLOT2_KEY`, `SLOT2_KEY_CREATED` and `SLOT2_KEY_FP`, and refuses the spike key (both refusals checked; no gcloud call is made). The spike key is named separately (`SPIKE_KEY`) for `retire-instrument` only. The README and DEPLOY.md are updated. |
| Release gates (sweep C3) | The VPC SC perimeter and the E-06 policy are listed in DEPLOY.md as open release gates. |
| Sweep H3 wording | Reconciled with the amendment: "AWS-based examples". |

## Second confirmation (`CODEX-CONFIRM-2.md`): owner disposition

The K-R item and the deployment-key repair passed, and all four prechecks PASSED. A11C-01 stayed open: Codex built
a zip with `./tessera_verify/codec.py` beside the genuine file, which passed `check_zip` and then overwrote the
checked file on extraction.

- **Fix.** `check_zip` accepts only canonical, unique, relative POSIX entry names, so no `./`, `..`, leading
  `/`, backslash or duplicate. It also refuses symlink entries, which Codex did not raise; the owner added it.
- **Tests.** Codex's attack and five variants are refusal tests, the symlink case is a sixth, and a clean zip must
  pass as a positive control.
- **Owner controls.**
  - The first version of these tests passed vacuously. The hand-built zip failed the wheel-digest check before it
    reached the path check, and that was found by removing the path check and seeing the tests still pass. A
    fixture now records a stand-in binding digest so the zip reaches the path check.
  - With the path check removed, the `./`, leading-`/` and backslash aliases are accepted (3 tests fail), so the
    check carries them. The `//`, `..` and exact-duplicate aliases are also refused by the file-set and content
    comparison.
  - The genuine package built by `service/issuer/package.py` still passes.
- **Wording.** "As deployed" became "as designed (deployment pending)". The K-R citation is `:173-174`. "No
  defaults" became "no key defaults (the version number defaults to 1)".
- **Manifest.** Regenerated; its hash in A11 §A11.2 is `a69204e9f69a2af3a0bcac96991b55109b0ff0f3efdd6e2182424dd347a24a88`.

The final repair was verified by the owner's tests and controls, including Codex's exact construction. No further
Codex round was run on it.

## Third confirmation (`CODEX-CONFIRM-3A.md`, `CODEX-CONFIRM-3B.md`, 2026-10-29): owner disposition

The author asked that Codex, not the owner, confirm the owner's fix claims. The first run was blocked by OpenAI's
filter ("flagged for possible cybersecurity risk"), probably because the owner's brief asked Codex to "try to break"
the check and named archive-manipulation techniques. It was re-run as two briefs describing the defensive purpose.

- **3A (the owner's claims): all CONFIRMED.** These are the refusals, the positive controls (Codex's fresh build of
  the genuine package reproduced the owner's digest `1bfcc569…6446`), the earlier vacuity and its repair, and the
  division between the checks.
- **3B (is the check the right design): `check_zip` cannot establish the claim.** In 23 benign archives, `check_zip`
  passed several on which Python's zipfile and Info-ZIP disagree. AWS does not document Lambda's extractor.
  Disposition, following Codex's recommendation:
  - §A11.2 3(c) is rewritten in Codex's suggested form. The deployed package is bound by exact digest: the zip the
    recorded packager built, matched base64-encoded to AWS `CodeSha256` for every covered function. The amendment
    states that this is package identity, not agreement among extractors.
  - `test_deployed_zip_identity` requires `TESSERA_LAMBDA_CODESHA256` as well as the zip. The owner's controls:
    matching digests for two functions pass, and one wrong digest fails. `test_A11C3B_code_sha256_comparison`
    checks the encoding: hex, as `package.py` prints it, is not AWS's form.
  - The comment in `check_zip` no longer claims that "what extraction writes is exactly what was compared". It is
    build-content evidence.
  - `DEPLOY.md` step 10 reads `CodeSha256` for both functions and runs the floor against the deployed zip.
  - The post-extraction claim (a deployed manifest check of extracted files) is not adopted for V1. The bounded
    package-identity claim is what the amendment states.
  - Codex's note that Terraform does not publish Lambda versions stands. Publishing a version conditional on
    `CodeSha256` is a V2 candidate.
- The manifest was regenerated. The floor gives 1201 passed, 1 skipped.
