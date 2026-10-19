# Findings from real issuance (instrument runs)

Each finding names which of the three it changes: **contract** (`docs/V1-CONTRACT.md`), **model** (formal/), or
**implementation**. Contract changes get the most scrutiny (the author's method, travelog 2026-10-19).

## E-01 — slot-2 signer paused; manual resume (real-1, 2026-10-19)

- **What happened.** The `sign` stage timed out after 240 s: the policy signer runs only on Cloud Scheduler ticks,
  and the scheduler was paused (as recorded). The owner resumed it for the stage and paused it after.
- **Implementation.** The issuer must start the signer on demand, or the operating state must keep it running while
  issuance is possible. Runbook item.
- **Model / contract.** None.

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
- **Limits.** One run, one verifier (the second implementation, the conformance suite's, was not run on it). TEST
  repository key, TEST freeze, no service-key listing. Instrument evidence only (A9.2).
