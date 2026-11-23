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

## 2026-11-10 — slot-2 scheduler paused (owner)

The author's Google billing alert ($10/month budget exceeded) traced to `tessera-signer-gpg-tick`, which ran the
Cloud Run job (1 vCPU, 512 MiB, ~30–40 s) **every minute** since 2026-11-02, polling an empty queue: about 1,440
executions a day. No window exists, so nothing could be signed. Paused at 2026-11-10 ~13:35Z
(`gcloud scheduler jobs pause`). `deploy.sh scheduler` now sets every 10 minutes (the issuer poller's cadence; a
request's budget is days). Resume only when the window is published. Remaining standing GCP cost: two HSM key
versions (`slot2-v1`, and `slot2-spike` until its deletion), artifact storage.

## 2026-11-13 — window prepared (owner)

- Key assertion signed by the repository root (`docs/ceremony/2026-11-13-assertion-signing.md`): commit `aad530ed…`,
  DNS TXT published and DNSSEC-validated, OTS anchored at block 975705 (8 confirmations at check).
- `service/issuer/config/root-ksks.json`: the DNS root KSK entries (KSK-2017 closed 2026-10-11, KSK-2024 open),
  exported as data from `formal/trust-sources/` with the prototype's `trustcfg.roots()` (which cross-checks the
  IANA XML, its .p7s and the DS digests). Data, not code; the issuer's pre-ship parser validates it.
- `service/issuer/tools/build_window.py` → `service/issuer/config/window.json`: window 2026-11-15T00:00:00Z ..
  2027-02-01T00:00:00Z; kms `a33c216e…`, gpg `6a2d7e75…`; repository root `6BDA…D30A` from 2026-11-10T19:44:55Z.
  Accepted by `window.load_json` (the Lambda's loader) and `preship.check_config`.
- Next: upload to `s3://tessera-v1-issuer-results-0241cd18c7441abb3eaab257e8/config/window.json` (needs the
  author's AWS login), resume the slot-2 scheduler, smoke test after the window opens.
- **Uploaded** 2026-11-13 22:11Z: `config/window.json` (SHA-256 `2c8d9e7b…327242c3`, read back identical).
- **Pre-window check:** one request with the `smoke-test` key → HTTP 403 `REFUSED / OUTSIDE_WINDOW` (request key
  `d8397488-…`): the API Lambda loaded and parsed the production window.
- **Slot-2 scheduler** set to `*/10 * * * *` and resumed (22:11Z).
- Next: smoke test after 2026-11-15T00:00:00Z (step 9), then step 10.

## 2026-11-16 — step 9 smoke test and step 10 (owner): the first production receipt

- Request `ca33cc04-6032-4da0-8a7a-7fffd0373dd3` (key `smoke-test`), content "Tessera V1 smoke test: the first
  production receipt, requested 2026-11-16 by the steward." (SHA-256 `d170b6bf…`). Accepted 12:55:59Z; attempt 1
  open 13:01Z; latched 15:37Z; **COMPLETE 15:46:50Z**, receipt SHA-256 `aca4dfb2…`. No poller errors in the logs.
- **Relying-party verification:** service verifier CLI, trust = the production window's entries (DNS root KSKs,
  repository root `6BDA…D30A`) plus pins of the bundle's 12 headers (975705–975710: the key assertion's k = 6;
  976141–976146: the receipt's anchor), each fetched from blockstream.info and mempool.space and required to agree;
  TEST release over it (the production release, YubiKey B, does not exist yet). **Verdict `VALID_STRICT`**, exit 0.
- **Control:** one character changed inside `layers[0].a_sig` → **`INVALID`**.
- **Step 10:** both functions' `CodeSha256` = `SG7VL7wV…` = `issuer.zip` `486ed52f…`; P3 verification profile with
  the deployed identity: 1202 passed. P3 condition (c) discharged.
- Evidence: `docs/smoke/2026-11-16-first-receipt/` (receipt, content, trust, reports, the check script, SHA256SUMS).

## 2026-11-16 — pilot client and quota (owner)

Usage plan quota 100/day per key added; key `yanantin-pilot` (id `l5hkmlu1yd`) created (apply: 2 added, 1 changed,
0 destroyed; state backed up). The value was written only to `~/.local/share/tessera-handoff/tessera-pilot` (0600,
never printed) for the author to carry to Yanantin. Gate exception recorded in DEPLOY.md.
- 2026-11-17: the author carried the key to Yanantin; the NUC handoff copy was deleted (shred).

## 2026-11-22: detection gap G1 deployed (steward)
Structured application logs (`service/issuer/LOGGING.md`; reviews `docs/reviews/g1-logging/`: review, two
confirmations, final dispositions `f85319d` under the pre-registered exit). Code only; no configuration change.
- Suites on main before packaging: issuer 255, signer-kms 48, signer-gcp 121, verifier 135 (+77 subtests).
- `dist/issuer.zip` (from `f85319d`, `--install-json install-facts.json`) SHA-256
  `3a5520a9d713604dcdf93f00ee443193447a3041e77ec76b7c87b058afff282f`; a second build gave the same digest.
- Plan: 0 to add, 2 to change (`aws_lambda_function.api`, `.poller`: `source_code_hash` only), 0 to destroy. Vars as
  before: `client_names=["smoke-test","yanantin-pilot"]`, `signer_principals={gpg=…:role/tessera-v1-signer-gpg-federated}`,
  runtime pinned `…runtime:e75e9c9c…6aeed`. Applied 2026-11-22T06:03Z under the author's `aws login` session.
  State backed up before and after (`~/.local/share/tessera-tfstate/`).
- **Step 10:** both functions' `CodeSha256` = `OlUgqdcTYE3N+T8A7kQxk0R6MEHnfsdrfIewWK//KC8=` = hex `3a5520a9…`;
  `formal/p3-verification-profile` with `TESSERA_LAMBDA_ZIP`/`TESSERA_LAMBDA_CODESHA256`: 1202 passed. Runtime
  version unchanged.

## 2026-11-22: content-addressed receipts deployed (steward)
Repairs the deployed fixed-key defect (A12-R2-03; A12 change 5). Reviews `docs/reviews/receipt-ca/` (review: one HIGH,
the legacy fallback unreachable under IAM; scoped confirmation; dispositions `4154be5`, `7330ae2`).
- Suites on main: issuer 263, signer-kms 48, signer-gcp 121, verifier 135 (+77 subtests).
- **Migration, pass 1** (before the deploy; `tools/migrate_receipts.py --apply`, create-only): 7 fixed-key receipts, all
  COMPLETE with matching bytes, all copied to their digest names. None had been overwritten.
- `dist/issuer.zip` SHA-256 `f6a5cf1de21a8b273a93f5b0d23b8daff1647399f7ff8a64264f6c0e9b6cf82d` (two builds equal).
  Plan: 0 add, 3 change (API role policy: `ListForHead` = unconditional `s3:ListBucket` on the results bucket; both
  functions' code), 0 destroy. Applied 2026-11-22T06:37Z. State backed up before and after.
- `iam simulate-principal-policy` (API role, `aws:RequestedRegion=us-east-2`): `s3:ListBucket` and `s3:GetObject`
  allowed. Without the region context the SCP region lock shows `explicitDeny`, as expected.
- **Step 10:** both `CodeSha256` = `9qXPHeIa…` = hex `f6a5cf1d…`; `formal/p3-verification-profile`: 1202 passed.
- **Live check:** the deployed API, invoked as `smoke-test` for the first receipt (request key `ca33cc04-…`), answered
  303 to `result/<rid>/<digest>.json` (no fixed key); the 4,876,783 fetched bytes hash to `Tessera-Receipt-SHA256`.
- **Migration, pass 2** (06:42:35Z, after the poller's 300 s timeout had passed since the apply): the same 7, all
  `present` with bytes hashing to their records; no fixed-key receipt was written by old code in between. Exit 0.
  The fixed-key copies remain until each request's normal cleanup; no fixed-key name is served.

## 2026-11-22/23: detection watcher deployed (steward)
`service/watcher/` (the Arariwa: D5, D6 slot 1, D7 IAM, D8, D9, trace records) in `service/detect/infra/`. Reviews
`docs/reviews/watcher/` (review: 4 HIGH, 9 MEDIUM; confirmation: 4 new HIGH from the fixes; final minimal pass per the
pre-registered exit). Suites on main at `286f027`: watcher 398, issuer 263, signer-kms 48, signer-gcp 121, verifier 135.
- Bootstrap `watcher-bootstrap.zip` SHA-256 `ee66c0432b37529aa572b3bea3bacd1ceab67c4662e858df995c203a868e1927`
  (two builds equal). Plan 23 add, 0 change, 0 destroy; applied 2026-11-22T23:56Z.
- Install facts (`service/watcher/install-facts.json`) sampled on runtime
  `arn:aws:lambda:us-east-2::runtime:eaebdc1115476ede1dce9876df554dcaaae527c20c43bd19bfeaa754e9eafb4d`.
- Deployable `watcher.zip` SHA-256 `5cdd50c53452fb5f4bcf9c86c460159f0bcdce86406acac5ffc7c9c91a3f9585` (two builds
  equal). Plan 1 add (runtime pin), 1 change (code); applied 2026-11-23T00:01Z. Deployed `CodeSha256`
  `XN1QxTRS…` = hex `5cdd50c5…`. State backed up before and after each apply.
- Expected alarms from this deployment: one D9 (bootstrap self-check), and D7 IAM findings for the deployment's own
  IAM writes once the watcher reads the trail.
