# Signer review: owner disposition (2026-10-27)

Owner instance (Claude Opus 5.5). The review is `CODEX-REVIEW.md`, the log is `codex.log`, and its scope was
`service/signer-kms/`, `service/signer-gcp/`, issuer packaging and `service/issuer/DEPLOY.md`. All findings were
applied. The owner prechecks found two failures in the owner's own text, requester and binding text, and both are
corrected below.

| ID | Sev | Disposition | Evidence |
|---|---|---|---|
| SG-01 | Med | GCP signer: the stop and `sign_by` are checked before a resend as well as before signing, and again after the HSM call. A signature returned after a cutoff is withheld (`SIGNING_STOPPED`) and logged as `withheld`; the README says the HSM has still produced it. | `test_SG01_signature_returned_after_sign_by_is_withheld`, `test_SG01_a_cached_signature_is_not_resent_after_sign_by` |
| SG-02 | Med | GCP signer: the frame is fetched first, then one clock reading serves ε and both cutoffs. The README's claim that ε "fails safe" under a clock fault is withdrawn. The KMS signer already fetched first (`signer.py:229-232`). | `test_SG02_epsilon_is_checked_after_a_slow_frame_fetch` |
| SG-03 | High | `deploy.sh retire-instrument` tolerates only "already gone". It disables the old service account, which ends inherited grants as well, then verifies that the scheduler and job are absent, that the account is bound on neither the key nor the project, and that it is disabled; otherwise it fails. The "not found" match was checked against real gcloud output for all three resource types: Cloud Run says "Cannot find job", which the first pattern missed. It is a gate before issuance (`DEPLOY.md` step 7). | read-only describes of nonexistent names, 2026-10-27 |
| SG-04 | Med | Both READMEs now list the narrower routes: direct Lambda invocation, `iam:PassRole`, `run.jobs.runWithOverrides`, and the role's session credentials. `DEPLOY.md` step 8 lists the holders of each before issuance. The placement decision is corrected: an ordinary IAM grant cannot override the key policy's explicit Deny, so the route is `PutKeyPolicy`. | text |
| SG-05 | Med | `aws_lambda_runtime_management_config` pins both issuer functions when `runtime_version_arn` is set. `DEPLOY.md` uses the real resource; it had shown nested syntax. The smoke test (step 9) is the first run of the detector on Lambda. | `test_SG05_both_functions_are_pinned_to_the_install_record_runtime`; `terraform validate` |
| Binding text | — | The clock-tolerance decision called the signers' stop "the binding check". It is an owner operating control, and L1 says the 96-hour margin is not a registered rule. Corrected. | text |

**Q2 (pinning the other slot's key in the manifest):** not added. The review found it narrows only what C3 already
grants; it goes on the V2 candidate list. **Q3 (TEST keys):** *superseded 2026-10-28: reusing the spike keys contradicted `formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6 (Amendment 11 review, A11-03); production uses new keys.* The original disposition read: the keys are reused;
the archived TEST receipts fail under the frozen catalog with `SPEC_UNKNOWN`. Because nothing separates TEST from
production at signing time, every receipt signed after a window's records name the keys is a production receipt.
**Q5:** the signers bound when signing *starts* against a correct clock, and withhold late results. They cannot
bound clock faults, and they have no durable deduplication across deliveries. That is consistent with
`docs/V1-CONTRACT.md` §3 ("One receipt per presentation" is not guaranteed).

No second review round is planned before deployment. The deployment session itself (`DEPLOY.md` steps 7–9) is the
next check, and its gates are mechanical.
