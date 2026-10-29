# V1 issuer: disposition of the Codex review

Review: `docs/reviews/issuer/CODEX-REVIEW.md`. All 11 findings were accepted and fixed; none was judged wrong.
Each regression test reproduces the review's failing scenario and fails on the reviewed code (for
`test_IS05_interrupted_upload_is_recovered_by_a_retry` only since its CF-05 strengthening, below). Tests are in
`service/issuer/tests/test_review_fixes.py` unless marked otherwise. Design changes are recorded in
`service/issuer/DESIGN.md`, "Changes after review".

Suite: `service/issuer/.venv/bin/python -m pytest -q`: **108 passed, 1 skipped** (after the CF fixes below). The skipped test is Terraform
validate: Terraform is not installed. The local end-to-end issuance still verifies **VALID_STRICT** through
`service/verifier` (`--mode test`), both for small content and over the wire protocols with 1 MiB content
(`tests/test_e2e.py`). It also does so through the Lambda handlers on the AWS adapters.

| ID | Sev | Fix | Regression test(s) |
|---|---|---|---|
| IS-01 | High | `pipeline._take` logs a verified response as "used" before it stores the signature or marks the job. `_seal` also requires that log record (`RequestStore.siglog_has`; DynamoDB key `SIGLOG#USED#<id>#<sha>`). `drain` acknowledges a response only after it has been taken. | `test_IS01_signature_is_not_eligible_before_its_log_record_is_durable`, `test_IS01_seal_requires_the_log_record`, `test_IS01_IS07_store_contract_for_used_log_records_and_cleanup_obligations` |
| IS-02 | High | `st_assemble` rechecks the deadline on a fresh clock after the pre-ship checks. `_end` takes the actual transition time and turns a late COMPLETE into FAILED `NOT_COMPLETE_WITHIN_24H`. The cleanup then deletes the stored result. | `test_IS02_completion_cannot_cross_the_24h_deadline` |
| IS-03 | High | Signer requests carry `sign_by`. The signer refuses with `SIGNING_STOPPED` immediately before signing when it is past `sign_by` or past its own configured signing stop (`StandInSigner(sign_until=…)`). **Open:** the deployed slot-2 signer and the KMS-slot signer must implement the same check. | `test_IS03_signers_refuse_queued_work_after_the_signing_stop` |
| IS-04 | High | `RequestStore.create(rec, tombstone_until)` writes the record and its tombstone in one DynamoDB transaction (`TransactWriteItems`). A repeat submission repairs a missing tombstone. | `test_IS04_failed_tombstone_write_cannot_free_the_key`, `test_IS04_existing_record_repairs_a_missing_tombstone`, `test_IS04_dynamo_creates_record_and_tombstone_in_one_transaction` |
| IS-05 | High | The record is created first, with stage `upload`, before any content is stored. A retry finishes an interrupted upload. The poller fails an abandoned upload after 15 min. If the request ended meanwhile, the API deletes the content it just stored. | `test_IS05_racing_refusal_leaves_no_content`, `test_IS05_interrupted_upload_is_recovered_by_a_retry`, `test_IS05_abandoned_upload_fails_after_the_grace_period` |
| IS-06 | High | **Owner decision (supersedes the Range approach):** one plain GET. `GET /v1/requests/{key}/receipt` checks the credential owns the request and it is COMPLETE and not EXPIRED, then mints a fresh pre-signed S3 URL (300 s, never longer, never stored or reused) and answers 303 with `Tessera-Receipt-SHA256`. Nothing is minted for another credential or an expired/non-complete request. No Range requirement, no 416 `RANGE_REQUIRED`. Recorded in DESIGN.md. | `test_IS06_url_is_minted_only_after_the_credential_and_state_checks`, `test_IS06_url_dies_at_300_s_and_the_object_at_30_days`; expiry race at minting: `test_CF03_no_url_is_minted_after_expiry_even_if_the_object_check_is_slow` (`tests/test_confirm_fixes.py`) |
| IS-07 | Med | `_end` records a cleanup obligation (`CLEAN#<rid>`) before committing. Each poll retries outstanding obligations and checks by listing that nothing is left: content, work and frames at the end, the receipt 30 days after. The S3 lifecycle (31 days) is a backstop only. | `test_IS07_failed_cleanup_at_the_end_is_retried`, `test_IS07_results_are_deleted_30_days_after_the_end` |
| IS-08 | Med | Each signature is stored under its own object name (`sig-<job>-<sha256>`). The job update is merged with compare-and-set re-reads (`_record_signature`). Before any re-send, `st_signing` adopts a stored signature that verifies and has its "used" log record (`_reconcile`). | `test_IS08_concurrent_metadata_update_does_not_lose_a_verified_signature`, `test_IS08_stored_verified_signatures_are_reconciled_before_resending` |
| IS-09 | Med | A request message over 256 KiB is sent as `frame_ref` (immutable `frames/<rid>/<sha256>`) plus `frame_sha256`. The signer refuses on a digest mismatch. The in-memory queue now enforces SQS's 1 MiB limit. Frames are deleted with the request, and the signer role reads `frames/*` only. **Open:** the deployed signers must accept `frame_ref`. | `test_IS09_one_mib_content_fits_the_queue_limit`, `test_IS09_queue_stand_in_enforces_the_sqs_limit`, `test_IS09_frame_reference_is_digest_bound` |
| IS-10 | Med | API: Put/Delete on `content/*` only, Get on `result/*`, Get on `config/*`, and List restricted to `content/`. Poller: mutation only on `content/`, `work/`, `frames/` and `result/`; `config/*` is read-only. Signer roles: Get on `frames/*`. | `test_IS10_iam_grants_only_the_object_actions_each_role_uses` |
| IS-11 | Med | `dns.truncated()` reads the TC bit from the header before parsing any record, then the transport fetches over TCP. | `test_IS11_truncated_udp_answer_falls_back_to_tcp` |

## Residual items (outside `service/issuer`)

- IS-03 and IS-09 change the signer wire contract, in a backward-compatible way: `sign_by` is a new field, and
  `frame_ref` is used only for large frames. The deployed slot-2 (GCP) signer and the KMS-slot signer must
  enforce the signing stop and accept `frame_ref` before issuance. Until they do, IS-03 holds only for the stand-in
  signer, and content above about 145 KB cannot be signed. Until then, the issuer still never uses a late
  signature: the request has already ended.
- IS-06: superseded by owner decision (see the IS-06 row above); clients make one plain GET.

## Confirmation review (CF-01 to CF-05)

Review: `docs/reviews/issuer/CODEX-CONFIRM.md`. All five findings were accepted and fixed; none was judged wrong.
Tests are in `service/issuer/tests/test_confirm_fixes.py` unless marked otherwise; races are driven by the fake
clock and by hooks that interleave the concurrent actor at the chosen point (no sleeps). Against the pre-fix sources
(the package with the CF changes reverted) 9 of the 11 new tests fail; the two that pass there are the guard
`test_CF02_write_lease_covers_every_lambda_timeout` and the CF-05 test, which diverges only from pre-IS-05 code.
`test_CF01_completion_seen_before_the_deadline_never_turns_into_failed` guards the new protocol (no COMPLETE to
FAILED flip) rather than reproducing an old failure. Design changes: DESIGN.md, "Changes after review", CF bullets.

| ID | Sev | Fix | Regression test(s) |
|---|---|---|---|
| CF-01 | High | `_end` persists the cleanup obligation, then reads the clock. COMPLETE is committed unconfirmed and settled by `api.settle`: confirmed (with `ended_at` = a clock reading taken after the commit, so never backdated) if that reading is before the deadline, else FAILED `NOT_COMPLETE_WITHIN_24H`; compare-and-set, so a confirmation and a failure never both win. Status and retrieval show COMPLETE only when confirmed; status and the cleanup obligation settle a completion left by an interrupted invocation. Supersedes the IS-02 terminal-transition fix. | `test_CF01_slow_cleanup_obligation_write_cannot_carry_completion_past_the_deadline`, `test_CF01_slow_terminal_write_cannot_carry_completion_past_the_deadline`, `test_CF01_completion_seen_before_the_deadline_never_turns_into_failed`, `test_CF01_unconfirmed_completion_left_by_a_crash_is_settled` |
| CF-02 | Med | Writer fencing by lease: every writer runs inside a Lambda invocation that saw the request ACCEPTED, so no write lands later than `WRITE_LEASE_S` (900 s, the Lambda maximum) after the end was first seen. The obligation records `fence_until` on its first pass; until then each poll deletes again, and only a listing after it discharges the obligation. Covers writes that commit while their caller sees an error. | `test_CF02_upload_that_commits_after_the_end_is_still_deleted`, `test_CF02_signature_written_after_termination_is_still_deleted`, `test_CF02_write_lease_covers_every_lambda_timeout` |
| CF-03 | Med | `api.receipt` re-reads the record and the clock after the object check and answers 410 without minting once the request has expired. URL lifetime stays 300 s (owner design). | `test_CF03_no_url_is_minted_after_expiry_even_if_the_object_check_is_slow` |
| CF-04 | Med | `S3ResultStore.delete` raises on per-object `Errors` in a DeleteObjects response and stops after `DELETE_ROUNDS` (20) listing rounds; the obligation is kept and `cleanup` continues with the others. The S3 test double now reports per-object errors as S3 does. | `test_CF04_s3_delete_reports_per_object_errors_and_is_bounded`, `test_CF04_one_failing_deletion_does_not_starve_other_cleanups` |
| CF-05 | Low | `test_IS05_interrupted_upload_is_recovered_by_a_retry` (`test_review_fixes.py`) now asserts that the failed upload leaves a durable ACCEPTED record at stage `upload` with no content, and that the retry resumes that same record (same `created_at`, one `submitted` event). The pre-fix code stored content before creating any record, so the first assertion fails there. | the strengthened test itself |
| IS-06 row | — | Regression-test column corrected: the superseded Range description is replaced by the current test names. | — |

Still open, unchanged: deployed-signer enforcement of `sign_by` and the configured signing stop, and digest-bound
`frame_ref` retrieval (IS-03, IS-09), are a pre-issuance integration gate outside `service/issuer`.

## Second confirmation (`CODEX-CONFIRM-2.md`, 2026-10-27): owner disposition

Owner instance (Claude Opus 5.5), 2026-10-27. Codex judged CF-02, CF-04 and CF-05 closed, and CF-01 and CF-03
partial, because each fix opened a new race of the same shape: the clock was read, then a slow storage call ran,
and the check used the stale reading. All findings were applied. The issuer suite passes 113 with none skipped
(Terraform 1.16.7 is now installed, and `terraform validate` runs).

| ID | Sev | Fix | Regression test(s) |
|---|---|---|---|
| CF2-01 | High | A clock check cannot bound when a write commits; the writer lease can, and it is the assumption CF-02 already rests on. `api.settle` confirms only when the decision is at least `WRITE_LEASE_S` before the deadline, so the confirmation commits before the deadline if AWS commits within the lease (stated, not established: CF3-01). Inside the last lease it leaves the request unconfirmed: it reads as ACCEPTED with its `fail_after`, and at the deadline it is FAILED. `_cleanup_one` treats an unconfirmed request as not ended, so it is cleaned up normally once settled. Cost: a request that finishes in the last 15 minutes of its 24 hours fails (S4 states about 3 hours as usual). The DESIGN.md CF-01 bullet's "no timing assumption is needed" was wrong and is corrected. | `test_CF2_01_confirmation_that_commits_late_never_reads_as_complete` (Codex's reproduction), `test_CF2_01_inside_the_last_lease_reads_as_accepted_until_the_deadline`, `test_CF2_01_a_confirmation_decided_before_the_last_lease_commits_before_the_deadline` (guards against an over-strict margin; it passes on the old code too); `test_CF01_completion_seen_before_the_deadline_never_turns_into_failed` moved to before the last lease |
| CF2-02 | Med | `api.receipt` reads the record first and then the clock, immediately before minting. `api.status` had the same order (clock, then record) and is changed the same way. | `test_CF2_02_no_url_is_minted_after_expiry_even_if_the_record_read_is_slow` (Codex's reproduction, counting `presign` calls) |

Not changed: Codex's note that the pre-fix sources cannot be recovered from `dc5b601^` is right. The issuer was
first committed at `dc5b601`, so the pre-fix listings exist only in the review logs.

## Third confirmation, a sweep of the whole class (`CODEX-CONFIRM-3.md`, 2026-10-27): owner disposition

Owner instance, 2026-10-27. The brief asked for every site where a clock reading is compared with a deadline, expiry,
stop or lease while a blocking call runs in between, not only for confirmation of CF2. Codex listed 25 sites. The
owner prechecks all passed on the changed prose. The issuer suite passes 116 with none skipped.

| ID | Sev | Disposition | Regression test(s) |
|---|---|---|---|
| CF3-01 | High | **Stated as a limit, with the client side bounded.** No client check can bound when AWS commits a request already sent. The AWS clients now get explicit timeouts and retries: about 3 minutes worst case, kept under a third of the lease by a test. The remaining assumption is recorded as the service clock tolerance (`docs/decisions/2026-10-27-service-clock-tolerance.md`): service-level transitions may become visible up to 15 minutes after the time they record. No receipt guarantee depends on these times. DESIGN.md and this file now call the CF2-01 bound conditional. | `test_CF3_01_aws_client_time_is_bounded_well_inside_the_writer_lease` |
| CF3-02 | Med | Read half fixed: `submit` reads the clock after the record and tombstone reads. Create half: within the tolerance. Harmless by design, since acceptance stops 120 h before the window ends and signing stops at 96 h (L1). | `test_CF3_02_a_slow_admission_read_cannot_admit_after_acceptance_closes` (Codex's reproduction) |
| CF3-03 | Med | Fixed: `_existing` reads the clock after the tombstone repair, and again after an upload recovery. | `test_CF3_03_a_slow_repeat_read_cannot_report_an_expired_request_as_complete` (Codex's reproduction) |
| CF3-04 | Med | Within the tolerance: `ended_at` is the decision's reading and may precede the confirmation's commit by up to 15 minutes, which shortens the 30-day retention by at most that. The DESIGN.md wording "never earlier than the commit" is narrowed to the first COMPLETE write. | — (a stated limit) |
| CF3-05 | Med (cond.) | Within the tolerance. On Lambda, credentials come from environment variables, which botocore does not refresh, so presigning should not block. This is OWNER ANALYSIS, not verified on Lambda. A URL minted seconds late lives for 300 s. | — |

Sites Codex judged unsafe as a claim about signing (frames and signing stop, `pipeline.py:290-337`) depend on the
signer's own `sign_by` and signing stop. That is the open pre-issuance integration gate (IS-03, IS-09), unchanged.
No further confirmation round is planned for this class. The next issuer review is the deployment review.
