# Deployment run record (first V1 deployment)

Append-only. Each entry: date, step, what was run, the values it produced, and who ran it.

## 2026-10-30 — before the session (owner, no credentials)

Base: `8bcfcda` plus the issuer/signer interface fix (`docs/reviews/issuer-signer-interface/`).

1. **Verifier install.** Already installed; `sha1dcsum` SHA-256 `3fa8472a23ff8ecc6c91b5193bc6e6e7a7ef1a1bbfbbff769a89bda0634dd5fb`
   matches `service/verifier/install.json`.
2. **Suites.** The first run failed both signer suites (signer-kms 2, signer-gcp 7). One cause was a real defect:
   the issuer's attempt-prefixed frame names, which both production signers refuse, would have refused every
   request over 256 KiB. Fixed, confirmed by Codex, and covered by a retained pipeline test (disposition in
   `docs/reviews/issuer-signer-interface/DISPOSITION.md`). After the fix: issuer 235, signer-kms 48, signer-gcp 121,
   verifier 135 (77 subtests), all passing.
3. **Packages** (deterministic: a rebuild of the issuer bootstrap gave the same digest).
   - `service/issuer/dist/issuer-bootstrap.zip` SHA-256 `7789cfbb00e913cae222483ef4d894343bd52be49274be5cd13e2c984183748b`
     (BOOTSTRAP: no `install.json`, so pre-ship refuses until rebuilt in step 4)
   - `service/signer-kms/dist/signer-kms.zip` SHA-256 `3c5d812747f4efd84ca6339efa07d616e3bdff52d1a9330744ab9eea313f2923`

AWS session: `aws sts get-caller-identity --profile tessera` → account 477139661040,
`AccountFullAccessRole` (author login, 2026-10-30).

Next: step 1 (`terraform plan` for the issuer bootstrap), read together with the author.

## 2026-10-30 — in the session (owner ran the commands, under the author's login and with the author's blessing)

The author, on the owner waiting for the author to run `apply`: "Not sure why a steward needs gardener approval... I have a
bucket and a trowel, and they bless your actions." The runbook's "no agent runs any of them" line was a prior
owner's rule, now corrected in DEPLOY.md.

Before step 1, two changes to `infra/`: AWS provider `~> 5.70` → `~> 6.20` (6.71.0), because 5.x rejects the
`python3.14` runtime the verifier requires; and API Gateway access logging (`/aws/apigateway/tessera-v1-issuer-access`,
30 days; account-level CloudWatch role, none existed before). One client key, `smoke-test` (owner decision).

1. **Bootstrap apply.** 46 added, 0 changed, 0 destroyed. Outputs: API `https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1`,
   key id `g8plxeex43` (smoke-test), table `tessera-v1-issuer-requests`, bucket
   `tessera-v1-issuer-results-0241cd18c7441abb3eaab257e8`, kms and gpg request/response queues and wake topics.
   - Deployed IAM read back: the API role has PutItem/GetItem on its table, Put/Delete on `content/*`, Get on
     `result/*` and `config/*`, ListBucket; the poller has its table and index, Put/Get/Delete/Tag on
     `work|result|frames|content/*`, Get `config/*`, Send to both request queues, Receive/Delete/GetAttributes on both
     response queues, Publish to both wake topics. Both roles: `logs:CreateLogStream, PutLogEvents` on `*` (loose;
     to tighten to their own log groups).
   - Unauthenticated and guessed-key calls: 403, each logged (`INVALID_API_KEY`, key id `-`). Missing and guessed
     keys are not distinguishable in the log.
   - **Path:** the routes are at `<api_url>/v1/requests`, i.e. `.../v1/v1/requests` (stage `v1` plus resource
     `/v1`). To be fixed with the custom domain (base-path mapping), not by redeploying now.
2. **Install facts on Lambda:** Python 3.14, Unicode 16.0.0, `unicode_module_sha256`
   `62c4ae6033685dc674a1464257b68c632e21182314a52de559d499861232f2d3` (differs from the NUC's, as expected),
   `sha1dc_binary_sha256` `3fa8472a…dd5fb` (identical to the local build). Saved as `install-facts.json`.
3. **Runtime:** `arn:aws:lambda:us-east-2::runtime:e75e9c9c41239a44ec0c6835b8565881fa9de069823be371f86023888ce6aeed`.
4. **Deployable, pinned.** `dist/issuer.zip` SHA-256 `486ed52fbc1529d5a5dfa850d23fe84d65b7e782ed50797dc909464ad2283cf7`.
   Apply: 3 added, 3 changed, 1 destroyed (the API Gateway deployment, replaced). Both functions report
   `CodeSha256` `SG7VL7wVKdWl36hQ0j/oTWW354LtUHl9yQlGStIoPPc=` (= `486ed52f…` hex) and runtime management
   `Manual` on the ARN above.

State backups: `~/.local/share/tessera-tfstate/` (0700), after each apply.

## 2026-10-30 — new production keys (step 5 and 6 prerequisites; neither has signed anything)

These identities are the external custody record's first entries (A11 §A11.5 item 2 (ii); profile §8).

| Slot | Key | Created (UTC) | Fingerprint |
|---|---|---|---|
| kms | AWS KMS `arn:aws:kms:us-east-2:477139661040:key/2c9ba2cf-ca0d-4a04-ad26-657840f32944`, alias `alias/tessera-v1-kms`, ML_DSA_65, SIGN_VERIFY, origin AWS_KMS, tag project=tessera-v1. Default key policy until step 5 replaces it. | 2026-10-30T20:01:31Z | `spki-sha256:a33c216e4151f7202b4863f9edebf060b374ee1bb91ff9ca5734b8e7ba75679f` |
| gpg (slot 2) | GCP KMS `projects/tessera-slot2/locations/us-east1/keyRings/tessera-v1/cryptoKeys/slot2-v1/cryptoKeyVersions/1`, HSM, EC_SIGN_P256_SHA256, attestation CAVIUM_V2_COMPRESSED, label project=tessera-v1 | 2026-10-30T20:01:48Z (`SLOT2_KEY_CREATED=1793390508`) | `gpg-sha256:6a2d7e757b99b46e469dd81f293387b7cfdbe3a1cab2b614dd2d26ecc79dda59` (v4 fingerprint `2d9645a3e6236fec9c611ad390d500a104210130`) |

Fingerprints computed with the code that checks them (`tessera_issue.encode.fp_kms` form over `GetPublicKey`;
`tessera_signer.openpgp.key_body`/`fp_gpg` with the createTime above). The spike keys (`alias/tessera-pq-spike`,
`slot2-spike`) are untouched; they are deleted once HYBRID-SUPPLEMENT §11 item 6's conditions hold.

## 2026-11-02 — step 5, KMS signer (owner)

Owner decisions: **not-after 2027-02-01T00:00:00Z, sign_until 2027-01-28T00:00:00Z**
(not-before = publication of the key assertion); **trail retention 1096 days** (asymmetric cost: too long costs
storage, too short loses the signing record irrecoverably); no TEST window (its ≥ 10-day minimum, from the L1
margins, would hold `_tessera-v1.wamason.com` longer than the ceremony delays production). AWS provider for
`signer-kms/infra` moved to `~> 6.20` (6.71.0), as for the issuer.

- Package `dist/signer-kms.zip` SHA-256 `3c5d812747f4efd84ca6339efa07d616e3bdff52d1a9330744ab9eea313f2923`.
- Apply: 14 added, 0 changed, 0 destroyed. Function `tessera-v1-signer-kms`, role
  `arn:aws:iam::477139661040:role/tessera-v1-signer-kms-role`, trail `tessera-v1-signer-kms-trail`, bucket
  `tessera-v1-signer-kms-trail-13dedbd0aa681d7e13ea797992`.
- Live key policy read back: `KeyAdministrationWithoutSign` (account root, no Sign), `SignerRoleOnly` (Sign,
  GetPublicKey), `DenySignToEveryoneElse` (Deny Sign unless principal is the signer role).
- Negative check: the author's `AccountFullAccessRole` session calling `kms:Sign` → AccessDenied, "explicit deny in a
  resource-based policy".
- Object Lock on the trail bucket: COMPLIANCE, 1096 days. Trail logging: true.

## 2026-11-02 — steps 6–8, slot-2 signer and gates (owner)

- `deploy.sh sas`: created `tessera-signer-gpg@` and `tessera-signer-invoker@` (no keys). `role`:
  `arn:aws:iam::477139661040:role/tessera-v1-signer-gpg-federated`.
- Issuer re-apply with `signer_principals={gpg=<federated role>}`: 2 added (role and policy
  `tessera-v1-issuer-signer-gpg`): Receive/Delete/GetAttributes on gpg-requests, Send on gpg-responses, Get on
  `frames/*`; trust: the federated role only.
- `keyiam`: `slot2-v1` IAM = signer + publicKeyViewer for `tessera-signer-gpg@` only. `registry`: `tessera-signer`.
  `build`: Cloud Build `713ce333-…`, SUCCESS, image
  `us-east1-docker.pkg.dev/tessera-slot2/tessera-signer/signer-gpg@sha256:6306b4fb3490b70b24c1791478c6a0b22358ebbf77ec730fedc7d2da7d2ec79a`.
- `job`, `run-now`: execution `tessera-signer-gpg-7kkb9` completed; log `start
  gpg-sha256:6a2d7e757b99b46e469dd81f293387b7cfdbe3a1cab2b614dd2d26ecc79dda59` (the pinned production fingerprint),
  exit 0. `scheduler`, `harden`: done.
- **Step 7 gate:** `retire-instrument` → deleted jobs `slot2-signer-tick` and `slot2-signer`, removed the
  prototype's bindings on `slot2-spike`, disabled `slot2-signer@`; "instrument retired and verified".
- **Step 8 gate:** `docs/reviews/signers/REQUESTERS.md`. Passes: beyond the poller, the two signers and the author's
  administrator identity, no principal can cause a signature. Findings: the account is an Organizations member (the
  management account 871341458535 is the author's login and has a role-management path); the IAM simulator is
  unusable under Organizations, so the list is a policy reading pending review; prototype role
  `tessera-slot2-signer-sqs` remains, harmless to V1, for cleanup.

Next: step 9 needs the window: the ceremony (repository root), the key-assertion commit with k = 6, the DNS TXT,
`config/window.json`. Then the smoke test and step 10.
