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

## Consolidated draft review (`CODEX-REVIEW-CONSOLIDATED.md`, 2026-10-29): owner disposition

The draft was consolidated from the Levadura panel's 28 findings. The review found that all 28 are accounted for
and the custody options are stated neutrally. It found three high findings, two of them the panel's own pattern
again (a fix that leaves a copy of the text elsewhere unchanged), and three prechecks FAILED. All findings applied:

| ID | Sev | Disposition |
|---|---|---|
| A11X-01 | High | The K-R row adds the supplement's copy of the E§5.2 sentence (`HYBRID-SUPPLEMENT.md:274-276`). The historical "issuer-computed μ" capture labels are stated to still fit. |
| A11X-02 | High | Row 8 adds A10's plain-language passages (`:106-124`), its additions list (`:213-226`) and the row-26 note (`:432`). They are kept as the dated record of the 2026-10-18 adoption and superseded as descriptions of V1. In V1 no listing rejection, pre-commitment or preservation duty exists, and attacker-key receipts pass after capture of both channels (V1-CONTRACT §2, §4). |
| A11X-03 | High | The owner's own c016 sentence said expiry could "override" a latch, which A2.1 forbids. It now says the latch excludes expiry and describes the revision-3 design (one writer; expiry only after B plus the lease, on fresh evidence). |
| A11X-04 | Med | Row 10 adds `PROOF.md:485` ("No check reads it"), scoped as in :134-135. "B never computes it" stays. |
| A11X-05 | Low | The K-R row no longer calls source wording "unchanged". The unchanged restrictions are named and cited (:151-153, :157), and the actor change is stated. |
| Paraphrases | — | The table states that the "Was" cells of rows 3, 4, 7 and 8 are paraphrases; only quoted words are exact. |

The owner repairs in §A11.7 remain listed, not done (the live S4 still has the 24-hour rule). They are done with the
issuer lifecycle change.

## Consolidated confirmation (`CODEX-CONFIRM-CONSOLIDATED.md`): owner disposition

A11X-01 to -05 and the paraphrase labelling were CLOSED. A11XC-01 (High): row 8 still missed A10's closing summary
(`:795-799`, "deliberately rejects new cases: receipts under unlisted keys") and the listing parts of the
reconciliation item (`:810-812`). This was the fourth missed copy for the listing cut, so the owner did not repair
it alone. The owner grepped every registered text (prereg, A1–A10, PROOF, ENCODING-V1, HYBRID-SUPPLEMENT,
HYBRID-REGISTRATION-RECORD, FREEZE-RECORD, profile at `270ca49`) for the listing's vocabulary (`service_keys`,
`SERVICE_KEYS_NOT_LISTED`, `unlisted`, `LISTING_`, `A10.4.1`, `key listing`, `listing evidence`, `listing
pre-commit`). Every hit is now disposed by row 8: either named explicitly or covered as adoption history, the
mechanism section or frozen copies. A9:157 and profile :531 ("unlisted rollover") are DNSSEC terms, unrelated.

**Row-8 confirmation (`CODEX-CONFIRM-ROW8.md`):** A11XC-01 CLOSED; independent wider search found no undisposed hit. Ready for the author. Owner tidy: the mechanism-section range is corrected to `:462-611` (all of A10.4.1, which ends where A10.4.2 begins at :612).

## Author's pre-signing Codex read (relayed by the author, 2026-10-29): owner disposition

The author ran the draft by Codex before ruling. Codex leaned toward Option 1 and asked for two bounded corrections.
Both are applied:
- **DEPLOY.md gate.** A step 0 now makes the whole deployment wait for the §A11.5 item 2 ruling, recorded in the
  signed amendment. It states what each option means for the steps, and that no option uses `prototype/` code.
  A11.7 c036 is updated to match.
- **Stale lifecycle summary in A11.7 c016.** The summary described revision 3 (expiry after the boundary plus the
  write lease), while the design is now at revision 4 (expiry only on complete negative evidence, no lease timing).
  The owner had revised the design twice after writing the summary. A11 now defers to the design document instead
  of restating it. Following Codex's caution, it also says that **signing A11 does not accept any residual the
  lifecycle design states**: such a residual is assessed in the lifecycle work against A2.1 and A2.3, and needs its
  own author decision if it remains.

Codex also noted that §A11.2 item 4 is a continuing operational duty: re-runs on every verifier or library change,
every new upstream vector commit, and at least quarterly. This is stated in the amendment, and the author should
weigh it as an ongoing cost, not a one-time approval.

## Author's question on the operational triggers (2026-10-29): owner disposition

The author asked whether §A11.2 item 4's triggers are the right boundaries or educated guesses. Owner assessment:
- Code or library change is required: the evidence is bound to bytes.
- "Every upstream vector commit" had the right purpose at the wrong grain: it now triggers only on files for the
  algorithms in use.
- "Quarterly" was a guess standing in for knowledge outside the vector suite. It is replaced by advisory and erratum
  triggers, plus a calendar backstop labelled as an operating guess, to be reviewed on a year of run records.

Item 4 is rewritten so that each trigger states what it detects. This is an unreviewed edit to the draft. The
owner's confirmation runs before signing.

A boundary candidate raised to the author, not added to A11: the verifier's DNSSEC signature checks (RSA alg 8,
ECDSA P-256 alg 13, which ground G4) are inventoried but not profiled (`formal/p3-verification-profile/PROFILE.md:54-58`).
No registered property asks for a verification profile for them.

## Custody ruling as an owner decision (2026-10-29)

The author asked whether the custody ruling is irreversible or scope-changing. Owner's answer:
- Option 1 is neither. It changes no V1 scope. The practical lock-in is the first production receipt under the
  hybrid keys, at deployment, and a later amendment can revisit it before then.
- Option 2 is the scope change: it drops PQ and amends the freeze, for no claim V1 makes.

So the choice does not need the author's separate ruling. It needs his signature, because Option 1 relaxes a
registered reading, and signing A11 gives that. The ruling block, the header, §A11.5 item 2, change-table row 7 and
DEPLOY step 0 now record Option 1 as the owner's decision, adopted by signing. Option 2 is kept as the alternative
not taken, and the retrospective-relaxation disclosure is unchanged.

**Decision-wording confirmation (`CODEX-CONFIRM-DECISION.md`):** A11D-01 (stale "recommendation, not a decision", "Until the author rules", "If the author picks Option 1") fixed; A11D-02 to -04 PASS. A grep for the stale phrasings finds none left.
