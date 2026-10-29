# KMS-slot policy signer (Tessera V1)

The policy signer for the kms slot (ML-DSA-65 in AWS KMS), placed by
`docs/decisions/2026-10-27-v1-signer-placement.md`: a Lambda in the issuing AWS account, under its own IAM role,
triggered by the issuer's kms request queue. It answers on the kms response queue in the issuer's `SlotSigner` wire
format (`service/issuer/tessera_issue/signers.py`). The issuer holds no KMS permission.

- `tessera_sign_kms/signer.py`: policy, signing and self-check (`KmsSigner`).
- `tessera_sign_kms/lambda_app.py`: SQS event handler, S3 frame fetch, `from_env`.
- `infra/`: a separate Terraform root module, applied after `service/issuer/infra` in the same account.
- Tests: `.venv/bin/python -m pytest -q` (fake KMS, S3 and SQS; a round trip through the issuer's own code, and a
  whole local issuance verified `VALID_STRICT` by the service verifier).

## What it enforces

All checks run before KMS is called. A refusal is a `REFUSED` response with a reason. It is never a silent drop.

| Check | Refusal |
|---|---|
| The request is exactly `{request_id, frame_b64, sign_by}` or `{request_id, frame_ref, frame_sha256, sign_by}`. `sign_by` is required. | `BAD_REQUEST` |
| IS-09: `frame_ref` is `frames/<rid>/<frame_sha256>`. The object read from the issuer's bucket must hash to `frame_sha256`. | `BAD_REQUEST`, `FRAME_UNAVAILABLE`, `FRAME_DIGEST_MISMATCH` |
| The frame decodes, under the service verifier's own decoder, as `tessera-v1/attest` or `tessera-v1/manifest`. | the decoder's code |
| Its `alg` is the hybrid pair. | `ALG_NOT_ALLOWED` |
| Attestation: `signer.key_fp` is this key. Manifest: `key_fp` is this key. | `KEY_FP_MISMATCH` |
| Attestation: \|`declared_issue_time` − clock\| ≤ 24 h (A9.2). | `DECLARED_TIME_OUTSIDE_EPSILON` |
| IS-03: the clock, read just before the KMS call, is not past `sign_by` or past the configured stop (`SIGN_UNTIL`). | `SIGNING_STOPPED` |

After KMS answers, the signature must pass the verifier's rule-R codec and verify over the full frame. The signer
then reads the clock again. A signature that KMS returned after the stop is withheld (`SIGNING_STOPPED`) and logged,
but never sent. KMS is given the FIPS 204 external mu (`EXTERNAL_MU`, `ML_DSA_SHAKE_256`), never the frame.

Transient errors are KMS or S3 failures, or a signature that fails the self-check. The message is then returned to
SQS (`batchItemFailures`), up to three receives. After that the request is refused with `SIGNING_ERROR`. An
unexpected exception is handled the same way and ends in `INTERNAL_ERROR`. Every signature, refusal and retry is one
JSON log line with the request id, frame SHA-256 and signature SHA-256 (when there is one).

On start, the signer reads the key with `GetPublicKey`. It does not start unless the key is ML-DSA-65 and its
`spki-sha256` fingerprint equals the pinned `KEY_FP`. Nothing in a request changes the policy, epsilon or the stop.

## What it assumes

- **The Lambda clock is right.** All three time checks use it. It has the same standing as the slot-2 signer's
  container clock.
- **A KMS call can finish after the stop.** The stop check comes just before the call, and the call can take up to the
  client timeout (20 s per attempt). The second clock reading withholds such a signature, but KMS has still made it,
  and CloudTrail records it.
- **The issuer's bucket is the frame store.** The digest check, not the bucket, is what binds the frame.
- **The key exists.** This module never creates a key. The pinned provider (hashicorp/aws 5.100) does not accept
  `ML_DSA_65`. A new key is also a new window key: it needs a new key assertion and a new DNS record.
- **`aws_kms_key_policy` replaces the key's whole policy.** The new policy keeps account administration (including
  `PutKeyPolicy`, so the key cannot be locked out) without `kms:Sign`, `kms:GetPublicKey` or `kms:CreateGrant`. It
  allows `Sign`/`GetPublicKey` to the signer role only, and denies `kms:Sign` to every other principal ARN.
- **Deployment:** do not put `kms` in the issuer's `signer_principals`. The Lambda role reads the queues directly.
  The issuer's kms wake topic needs no subscriber, because the event source mapping invokes the signer.
- **The record:** the signer's log lines are in CloudWatch Logs, which an account admin can delete. The record that
  cannot be deleted is CloudTrail, kept under Object Lock in COMPLIANCE mode for `trail_retention_days`. CloudTrail
  records `kms:Sign` as a KMS *management* (read) event, not a data event, so the trail keeps all management events,
  read and write, and does not exclude KMS. The same trail records `PutKeyPolicy`, IAM and Lambda changes, and
  `StopLogging`.

## Who can cause a signature (C3, not a weakness to hide)

1. **Anything that can write to the kms request queue.** Today that is the issuer poller role. The signer signs
   whatever passes the policy above. The policy limits *what* is signed: a well-formed V1 frame for this key, inside
   the time limits. It does not decide *whose* content is signed.
2. **Any IAM administrator of the issuing account.** Such an admin can rewrite the key policy (`PutKeyPolicy`),
   change the signer role's trust policy, replace the Lambda's code or environment, or send to the queue. Each of
   these is a management event in the locked trail. The trail can be stopped from then on, but the stop is itself
   logged, and what was already written cannot be erased.
3. **Narrower routes that need no full administration** (SG-04, signer review). These are: any principal allowed
   `lambda:InvokeFunction` on the signer, which can hand it fabricated SQS `Records` directly (the signature goes to
   the response queue, so reading it also needs that queue); any principal allowed `iam:PassRole` on the signer role
   together with Lambda create or update rights, which can run other code as the signer; and anything holding the
   signer role's session credentials. No such grant is made by this module. `service/issuer/DEPLOY.md` step 8 lists
   who holds them before issuance starts, and checking the event source inside the handler cannot replace that
   list.

This is C3 as registered: capturing the issuing AWS account means both slots can sign. The signer narrows the
*route* to a signature to these two. It does not remove either one. V1 promises no detection
(`docs/V1-CONTRACT.md`). A separate signing account is a V2 candidate. With this layout, that move means putting this
module in another account and allowing that account's role cross-account access to the queues.
