# Findings from real issuance (instrument runs)

Each finding names which of the three it changes: **contract** (`docs/V1-CONTRACT.md`), **model** (formal/), or
**implementation**. Contract changes get the most scrutiny (the author's method, travelog 2026-10-19).

## E-01 — slot-2 signer paused; manual resume (real-1, 2026-10-19)

- **What happened.** The `sign` stage timed out after 240 s: the policy signer runs only on Cloud Scheduler ticks,
  and the scheduler was paused (as recorded). The owner resumed it for the stage and paused it after.
- **Implementation.** The issuer must start the signer on demand, or the operating state must keep it running while
  issuance is possible. Runbook item.
- **Model / contract.** None.
- **Implementation fix (2026-10-19).** `signers.PolicySignerGpg.trigger()` runs `gcloud run jobs execute slot2-signer
  --project tessera-slot2 --region us-east1 --async` once per request batch (logged, recorded in
  `<run>/sigs/requests.json`); `run.json` `signers.trigger_slot2` (default true in real mode) turns it off. The
  scheduler stays paused. Tests: `tests/test_signers_fixes.py` (`test_trigger_*`, `test_make_default_on...`,
  `test_init_real_writes_trigger_option`), subprocess mocked, never executed.

## E-02 — a signed but unshipped frame, and a second signature over the same frame (real-1, 2026-10-19)

- **What happened.** The first `sign` attempt got S_kms over f_kms, then timed out waiting for slot 2. Its slot-2
  request (`req-35144572…`) was probably processed when the scheduler resumed; the response is unread in the SQS
  response queue (prediction: not checked). The retry signed f_kms again. ML-DSA-65 signing is randomized, so two
  distinct valid S_kms exist over identical bytes.
- **Implementation.** Retrying must drain or cancel outstanding requests and keep every signature made (record,
  then destroy or quarantine). Today it leaves them in an SQS queue.
- **Model.** P5c models issuance as sign-then-stamp, with no state for a signature that is made but never shipped.
  The model has no notion of an orphan signature.
- **Contract.** Open question: does V1 promise one receipt per presentation? A holder of the orphan signatures could
  anchor a second receipt over the same frames with a different `A_sig`, so a different receipt id. The owner's
  prediction is that this is harmless to G1–G11 (it is the same presentation, honestly signed), but the contract
  does not say so. **Decided 2026-10-19 (owner, CLARIFY):** checked against G1–G11, a second receipt over the same
  honest frames violates none of them. Stated in `docs/V1-CONTRACT.md` §3 ("One receipt per presentation"). The
  implementation fix and the P5c gap stay open.
- **Implementation fix (2026-10-19).** (a) Request ids are written to `<run>/sigs/requests.json` before enqueue; before
  and after each batch `PolicySignerGpg.drain()` reads the response queue, records every signature found for those ids
  (request id, frame sha256, signature sha256) in `<run>/sigs/orphans.json`, and deletes the messages. (b) Every KMS
  signature, slot-2 response, and any stale signature file about to be replaced is recorded in `orphans.json`, including
  from failed attempts. (c) `driver.st_sign` reuses a complete on-disk set that verifies over the exact frame bytes (no
  KMS call, no request, no trigger). Tests: `tests/test_signers_fixes.py` (`test_retry_drains_orphan_responses...`,
  `test_failed_attempt_kms_signatures_recorded...`, `test_sign_stage_idempotent...`, `test_corrupt_set_is_resigned...`),
  SQS faked in memory. Limit: drain is best-effort (messages hidden by another reader's visibility timeout, or not yet
  produced, are caught on the next retry). The P5c model gap remains open.

## E-03 — first real receipt: VALID_STRICT, and negative controls on the same bytes (real-1, 2026-10-19)

- **Result.** Receipt `6efd88af9a162d59c843fc0800d9e18eda5e68a73e3e7af9df2a9712ba2facfb`, bundle sha256
  `28eaaea4…69ad` (3,713,975 B). T = 2026-10-19T17:49:13Z; h_git = 972177, h_receipt = h_snapshot = 972187, so
  h_git + 5 < h_receipt. Signers: AWS KMS ML-DSA-65 (`alias/tessera-pq-spike`) and GCP HSM P-256 through the policy
  signer. DNSSEC: live `_tessera-v1.wamason.com` TXT under the real KSK-2024. Verifier: `prototype/indep-verifier`,
  provisioned by a TEST-signed release. Verdict `VALID_STRICT / OK`.
- **Controls (owner, run by hand on the real bundle).** Byte-identical copy: VALID_STRICT. Python re-serialization:
  INVALID / JSON_NONCANONICAL (correct: canonical bytes are required). One character flipped at seven points along
  `a_sig`: all INVALID (SIG_INVALID ×4, JSON_SYNTAX ×2, RECEIPT_COMMON_MISMATCH ×1). One flipped in the OTS proof:
  INVALID / OTS_FORMAT.
- **Cross-check with independent libraries.** `conformance/selfcheck.py` on `receipts/real-1`: OK (`cryptography`
  ECDSA and ML-DSA-65, dnspython DNSSEC validation at T_snap, python-opentimestamps, hashlib git ids, pins).
  *Correction, same day:* the owner first wrote that "the second verifier" was not run. There is only one V1
  verifier; the differential compares it with the conformance suite's expected verdicts. selfcheck is the
  independent cross-check, and it does not decide verdicts.
- **Limits.** One run, one V1 verifier plus the selfcheck. TEST
  repository key, TEST freeze, no service-key listing. Instrument evidence only (A9.2).

## E-04 — wrong KSK-2017 publication date in the trust-configuration builder (2026-10-19)

- **What happened.** Sourcing the trust values from primary documents (`formal/trust-sources/VALUES.md`) showed
  `trustcfg.py` had KSK-2017's publication as 2017-08-11; ICANN gives 2017-07-11. KSK-2024's publication
  (2025-01-11) was unsourced and null.
- **Implementation.** Corrected in `trustcfg.py`; tests pass. `receipts/real-1/trust.json` carries the old date; its
  verdict does not depend on it (the snapshot is from 2026-10-19, long after both dates).
- **Contract / model.** None. Open for the freeze: neither the KSK-2017 signing end nor the KSK-2024 signing start on
  2026-10-11 has a published time of day; the reliance rule must not depend on one.

## E-05 — real-1 is refused by the current verifier after the catalog gained Δ and m (2026-10-19)

- **What happened.** A10:284-285 puts Δ = 7200 s and m = 6 in the catalog. The verifier now requires them there
  and fails closed (`CATALOG_UNAUTHENTICATED`) when they are absent. real-1's TEST release predates the fields, so
  the current verifier refuses to verify it.
- **Reading.** Correct behaviour: a release binds its catalog, and a catalog without the UTC parameters cannot
  support the `utc_assessment` the profile now requires. real-1 still verifies with the verifier code at
  `9095b86`, the release it was issued under. It was a TEST pipeline proof, not a keepsake.
- **Implementation.** `freeze.py` now writes both fields; the dry run gives `VALID_STRICT` with
  `utc_assessment`. The next real run will exercise them.
- **Contract / model.** None. It shows that a catalog change before the freeze strands earlier TEST receipts, and
  that is acceptable only because none of them is a production receipt.

## E-06 — second real receipt, with the fixed driver and `utc_assessment` (real-2, 2026-10-20)

- **Result.** Receipt `5930c48a942baf1a6b375417739e5b424c373a61c5b49e5178eb85e79f019d89`, bundle sha256
  `47a6096e…d2a0`. TEST freeze of `8ea8bfa`. h_git = 972230, h_receipt = h_snapshot = 972237. T =
  2026-10-20T01:36:51Z; `utc_assessment` U = 2026-10-20T04:00:33Z under A-UTC-7200-6. Verdict `VALID_STRICT / OK`.
  `selfcheck.py`: OK. Controls: byte-identical VALID_STRICT; seven `a_sig` flips all INVALID.
- **E-01 fix exercised.** The slot-2 signer was started on demand (`gcloud run jobs execute`); the scheduler stayed
  PAUSED throughout (checked after the run). Both slot-2 requests were answered in the first attempt.
- **E-02 fix exercised.** Every signature made is logged with frame and signature hashes
  (`receipts/real-2/signature-log.json`: two KMS, two slot-2). No retry was needed, so the drain path ran only on
  an empty queue.
- **Still open.** real-1's orphaned slot-2 response (`req-35144572…`) is not drained by real-2: the drain reads only
  the current run's request ids. **Closed 2026-10-20 (owner):** the response queue held exactly one message,
  `req-35144572…`, status SIGNED, over frame `8818d7ea…` (real-1's attestation frame). Recorded in full in
  `receipts/real-1/orphan-drain.json`, then deleted; the queue is empty. Open for the service: a rule for responses
  it did not request (record, then delete), so that no signature leaves the issuer unlogged.
