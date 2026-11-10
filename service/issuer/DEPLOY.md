# Deploying the V1 issuer and its signers (owner, 2026-10-27)

> **Status: OWNER DRAFT, revised after the signer review** (`docs/reviews/signers/CODEX-REVIEW.md`, SG-01 to SG-05).
> These are the steps for the first deployment. They run in the author's login session (`aws login --profile
> tessera`; Terraform takes it via `eval "$(aws configure export-credentials --profile tessera --format env)"`).
> The owner runs them: the author, 2026-10-30, "I have a bucket and a trowel, and they bless your actions." (An
> earlier version said no agent runs any of them; that was a prior owner's rule.) The irreversible choices are
> still the author's: the trail retention in step 5, which Object Lock COMPLIANCE can never shorten. GCP steps run
> on the NUC, where `gcloud` is logged in. The run record is `DEPLOY-RUN.md`.

## Before the session (owner, no credentials)

1. `service/verifier/install.sh` has been run, so the pinned SHA-1DC binary exists.
2. All suites are green: issuer, `service/signer-kms`, `service/signer-gcp` (`.venv/bin/python -m pytest -q` in each).
3. Packages, each built deterministically (record each SHA-256):
   - `cd service/issuer && mkdir -p dist && .venv/bin/python package.py dist/issuer-bootstrap.zip`
   - `cd service/signer-kms && mkdir -p dist && .venv/bin/python package.py dist/signer-kms.zip`
   (`package.py` does not create `dist/`.) The run record for each deployment is `service/issuer/DEPLOY-RUN.md`.

## Keys and what counts as production — OWNER DECISION, revised 2026-10-28

**V1 uses new production keys, not the spike keys.** The hybrid registration commits to deleting both spike keys
(`formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, lines 524-526): "Both spike keys are deleted after the re-capture
verifies, once the review clears." The first version of this section reused them. That contradicted the
commitment, and Codex found it (`docs/reviews/amendment-11/CODEX-REVIEW.md`, A11-03). In the session:

- **KMS:** `aws kms create-key --key-spec ML_DSA_65 --key-usage SIGN_VERIFY`. Its id and fingerprint are
  `kms_key_id` and `key_fp` in step 5.
- **Slot 2:** a new HSM key in keyring `tessera-v1` (`gcloud kms keys create ... --protection-level=hsm
  --default-algorithm=ec-sign-p256-sha256 --purpose=asymmetric-signing`). Its version, `createTime` and fingerprint
  are exported as `SLOT2_KEY`, `SLOT2_KEY_VERSION`, `SLOT2_KEY_CREATED` and `SLOT2_KEY_FP` for
  `service/signer-gcp/deploy.sh`, which has no key defaults (the version number defaults to 1) and refuses the spike key.
- Both keys are recorded in the external custody record before either signs (profile §8).
- The spike keys are deleted (KMS: schedule deletion; GCP: destroy the key version) once the conditions in the
  supplement hold.

**Nothing separates TEST from production at signing time** (signer review, Q3). From the moment a window's
authority records name the new keys, every receipt they sign is a production receipt. The smoke test below
produces a real receipt over honest smoke-test content.

## In the session (author logged in: `aws login --profile tessera`)

0. **Gate: the slot-2 custody decision** (Amendment 11 §A11.5 item 2, c036). **Satisfied 2026-10-29:** Amendment
   11 was signed at `f01e086` with Option 1. `service/signer-gcp/` is the production slot-2 signer, subject to
   conditions (i)–(iv) of §A11.5 item 2, which steps 6–8 below evidence before the first shipped receipt.
   Production never uses `prototype/` code (`formal/freeze-v1/FREEZE-RECORD.md:62`).

1. **Issuer, bootstrap.** `terraform -chdir=infra plan -var lambda_zip=../dist/issuer-bootstrap.zip -out tfplan`.
   Read the plan together, then `terraform -chdir=infra apply tfplan`. The bootstrap package has no `install.json`,
   so pre-ship refuses and no receipt can ship from it.
2. **Install facts on Lambda.**
   `aws lambda invoke --profile tessera --function-name <poller> --payload '{"tessera":"install-facts"}' --cli-binary-format raw-in-base64-out install-facts.json`
3. **Runtime version.** `aws lambda get-function-configuration --profile tessera --function-name <poller>
   --query RuntimeVersionConfig.RuntimeVersionArn --output text`. This value is `RUNTIME_ARN` below.
4. **Issuer, deployable and pinned.** `.venv/bin/python package.py dist/issuer.zip --install-json install-facts.json`,
   then plan and apply with `-var lambda_zip=../dist/issuer.zip -var runtime_version_arn=$RUNTIME_ARN`. That pins
   both functions (`aws_lambda_runtime_management_config`, SG-05), so AWS cannot patch the runtime under the recorded
   Unicode digest. Collecting the facts hashes the SHA-1DC binary but does not run it. Step 9 shows it runs.
5. **KMS signer.** `terraform -chdir=../signer-kms/infra plan` with the issuer's queue and bucket outputs,
   `kms_key_id`, `key_fp` and `trail_retention_days`. The retention has no default, because Object Lock COMPLIANCE
   retention can never be shortened; choose it here. The plan **replaces the key's whole policy**: the account root
   keeps key administration (including `PutKeyPolicy`), only the signer role may `kms:Sign`, and everyone else is
   explicitly denied it. Read that diff, then apply.
6. **Slot-2 signer** (GCP; `service/signer-gcp/README.md`). Run `deploy.sh` steps in order: `sas`, `role`, then
   re-apply the issuer with `signer_principals`, then `keyiam`, `registry`, `build`, `job`, `run-now`, `scheduler`,
   `harden`.
7. **Gate: retire the prototype signer** (SG-03). `deploy.sh retire-instrument` must end with "instrument retired
   and verified". It fails on any error other than "already gone", disables the old service account, and checks that
   nothing of the instrument can still sign. Issuance does not start until this passes.
8. **Gate: who can cause a signature** (SG-04). List the principals that hold, on the AWS side,
   `lambda:InvokeFunction` on the signer, `iam:PassRole` on the signer role, `sqs:SendMessage` on either request
   queue, and `kms:PutKeyPolicy`. On the GCP side, list those that hold `run.jobs.runWithOverrides` or
   `run.jobs.update` on the job, `iam.serviceAccounts.actAs` / token creation on the runtime account, and
   `cloudkms.cryptoKeyVersions.useToSign` on the key. Record the lists in `docs/reviews/signers/REQUESTERS.md`.
   Anything beyond the issuer, the signers and the author's administrator identity is removed before issuance.
9. **Window and smoke test.** Upload `config/window.json` (L1 dates, both key fingerprints) to the result bucket.
   Then send one real request through the API, run it to VALID_STRICT through `service/verifier`, and include a
   negative control. This is the first run of pre-ship on Lambda, so it also shows the packaged detector works there.
10. **Deployed-package identity** (Amendment 11 §A11.2 3(c)). Read `CodeSha256` for both issuer functions
    (`aws lambda get-function-configuration --profile tessera --function-name <api|poller> --query CodeSha256
    --output text`), then run, from `service/verifier`:
    `TESSERA_LAMBDA_ZIP=../issuer/dist/issuer.zip TESSERA_LAMBDA_CODESHA256=<api>,<poller> .venv/bin/python -m pytest -q
    ../../formal/p3-verification-profile`. Keep the output, the two values and the zip's SHA-256 together in the run
    record. `CodeSha256` is base64 of the raw digest; `package.py` prints hex, and the test converts.

## Gate before any client beyond `smoke-test` (owner, 2026-10-30)

Detection, not only logging. API access logs exist from the first apply (`aws_api_gateway_stage.v1`); nothing watches
them yet, and no alarm exists. Before a second API key is issued:

1. **Detection contract** (owner): each attack or fault, what it must leave in which log, which alarm fires, how fast,
   and who is told. At least: flood and throttling; missing or guessed keys; oversized or malformed requests;
   per-key volume; signer refusals only an attacker or a fault produces (KEY_FP_MISMATCH, unsolicited responses,
   E-06); `kms:Sign` count against issued receipts; CloudTrail `PutKeyPolicy`, IAM changes and `StopLogging`.
2. **Alarms** with notification to the author.
3. **Detection tests built by another model family** (Gemini via `agy`, or grok), from the contract and threat
   model, not from the owner's alarm code: each attack is performed against the deployment and each alarm is seen
   to fire. Codex reviews the tests and results. A detection that has never been seen to fire is a claim, not a
   control.
4. A per-key daily quota on the usage plan.

## Gate before Tessera is relied on: operational posture (owner, 2026-11-06)

The author: "this is theater for this first phase. When Tessera is being used, it will become a target, and we will
need a better posture." The weakest point today is not the key ceremony but the NUC, which holds the author's AWS
administrator session, the GCP project owner's `gcloud`, the repository signing key, and AI agents running with
permission checks bypassed. Tolerable while nothing relies on Tessera; not after. Before the first client beyond
`smoke-test`:

1. No standing administrator credentials on a machine where an agent runs: deployment through short-lived, scoped
   roles; the administrator logins (AWS management account, GCP owner) only on a separate machine.
2. The two signers' control planes on separate machines and credentials, so one machine's capture does not give
   both slots (the direction of V2's disjoint authorities).
3. The repository signing key off the NUC, on a token.
4. Detection seen to fire (the gate above).
5. The V1 contract states the actual operational posture, including today's single administration machine
   (registered text: in A12).

## Not deployment gates, but release gates (still open; `formal/freeze-v1/FREEZE-RECORD.md:84-91`)

Before the first **public verifier release**: the custody procedure and its rehearsal; the production release key;

**Off-site custody** (owner, 2026-11-10, narrowed on the author's account of the building): each key's YubiKey,
backup stick and passphrase paper are kept apart within one access-limited apartment, where theft is remote and fire
is the residual. Before relying parties exist, one copy of each key's material (backup stick or passphrase paper) is
kept where a fire at home cannot reach it.

**Root (repository key) rotation protocol** (owner, 2026-11-06, on the author's question "why don't we have a rotation
protocol for it"). The verifier bounds a repository key only through the trust configuration (an open entry is
usable to the release's `as_of`; profile "Open endpoints"), and the release invariants allow adding a successor and
closing the old interval. What is missing, and is a gate before the first public verifier release: a cryptoperiod
(at most two years), triggers (schedule, custody event, suspected compromise), the procedure (ceremony on a spare
YubiKey, a commit signed by the outgoing root naming its successor, a release adding the new entry and closing the
old), and how relying parties learn of it. Service-key rotation for V1 remains as the runbook says: a registered
mechanism or an end-of-issuance statement before the window's stop.
the fingerprint channels the author names; the release-format vectors; the **GCP VPC Service Controls perimeter**;
and a **policy for responses the signer was not asked for** (E-06). Deployment does not cancel any of them.
