# Slot-2 policy signer: deployed-slot evidence (A9.6; Codex HS-02)

Captured 2026-10-14, 03:47 to 03:59 UTC, by the owner instance. Design: `DESIGN.md` (owner decisions 2026-10-14).
Instrument code under A9.2; it is the V1 issuer's design input, not service code. Every result below came from the
deployed path: client (AWS profile `tessera`) -> SQS -> Cloud Run job (GCP) -> Cloud KMS HSM -> SQS -> client. No
`gcloud kms asymmetric-sign` call was made by the instrument. That direct call was the gap HS-02 named.

Reproduce: `prototype/.venv/bin/python prototype/policy-signer/client.py evidence all`. Re-check (a) offline:
`... client.py verify-a`. Run log: `out/client-run.log`. Captures: `out/evidence-{a,b,c}.json`.

## Summary

| Item | Result |
|---|---|
| (a) valid genuine V1 hybrid attest frame, declared time = now, signed via the queue; verified offline in P8 A and B | **PASS** |
| (b) declared time 25 h in the past | **REFUSED** `DECLARED_TIME_OUTSIDE_EPSILON` (PASS) |
| (c) wrong tag (two forms) and wrong `key_fp` | **REFUSED** `TAG_UNKNOWN`, `TAG_MISMATCH`, `KEY_FP_MISMATCH` (PASS) |
| (d) issuer AWS role has no path to the GCP key | shown (below); the AWS-side inventory is complete for us-east-2 only, see the note |
| (e) signer version, key version, IAM policies, queue ARNs | recorded below |
| (f) resource manifest with teardown | `RESOURCES.md` |

## The deployed path (the record HS-02 asks for)

- **Signer version.** Image `us-east1-docker.pkg.dev/tessera-slot2/slot2/signer@sha256:80342551793c08249a454436b54bdb6713f6a4c95fa5a9bad095493cd227adb5`
  (the job pins the digest, so pushing a tag cannot change what runs). Every response carries
  `code_sha256 = 66d4d2abaa8586c422f5c8e9e689fe0e9cf00b84d7706dada545929edfa9f485`. That is SHA-256 over
  `signer/main.py || signer/p8_codec.py`, computed inside the container; it equals the same hash over the files in this
  directory. Base `python:3.14-slim` (Unicode 16.0.0, checked at build); pinned deps in `signer/requirements.txt`
  (cryptography 50.0.2, rfc8785 0.1.4, boto3 1.43.113).
- **Vendored decoder.** `signer/p8_codec.py` holds gen.py lines 41-477, 620-658 and 732-751 verbatim
  (gen.py sha256 `cd86740e…5ccc`). `deploy.sh vendor-check` diffs the ranges and reports them identical.
- **Clock policy.** The signer reads its own clock (`time.time()` in Cloud Run, whose system clock Google synchronizes)
  and refuses an attest frame iff `|declared_issue_time − clock| > ε`, with ε = 86400 s (A9.2) hard-coded. The policy is
  code, and no request field or queue attribute reaches it. Every response echoes the signer clock.
- **Policy, in order, before any HSM call.** (1) The frame decodes as `tessera-v1/attest` or `tessera-v1/manifest`,
  within schema, using the vendored P8 decoder. Any other tag in T, or one not in T, is refused. (2) `common.alg` (manifest:
  `alg`) ∈ ALLOWED_ALGS = {`KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`}, the hybrid pair id that this branch
  tests. (3) attest `signer.key_fp` (manifest `sset[0]`) = `gpg-sha256:b6e37f7c8120ca19cca86cc9617d4ec50b2875a799ee976d9d0253e01c7a077c`.
  (4) The attest declared-time check. At startup the signer fetches the HSM public key and refuses to run unless
  `fp_gpg(key, created 1791946553 = 2026-10-14T02:55:53Z)` equals the pinned fingerprint. After signing it verifies
  the HSM's DER signature with OpenSSL. It then gates the packet through the rule-O codec (`decode_sig`, slot gpg)
  before returning it. A refusal returns no signature, and the job logs it.
- **Output.** One v4 type-0x00 OpenPGP packet (rule O), 119 bytes, built as in `spike_gcp.py`: hashed {issuer
  fingerprint, creation time = signer clock}, unhashed {issuer key id}. KMS `asymmetricSign` is called with the SHA-256
  digest of the v4 preimage, with CRC32C integrity checked in both directions.
- **Queue path.** `arn:aws:sqs:us-east-2:477139661040:tessera-slot2-requests` → job → `arn:aws:sqs:us-east-2:477139661040:tessera-slot2-responses`.
  The job is a Cloud Run **job** (no URL, no service), started each minute by Cloud Scheduler `slot2-signer-tick` as
  `slot2-invoker` (`roles/run.invoker` on this job only: `run.jobs.run`, no overrides). Observed latency: 3 to 70 s.
- **Federation (no static keys).** The job fetches a Google ID token for `slot2-signer` from the metadata server
  (audience `tessera-slot2-sqs`) and calls `AssumeRoleWithWebIdentity` on `arn:aws:iam::477139661040:role/tessera-slot2-signer-sqs`
  for a 900 s session. Trust: `Federated: accounts.google.com`, StringEquals `accounts.google.com:sub` =
  `accounts.google.com:aud` (azp) = `100451337620005518976` (the SA's unique ID) and `accounts.google.com:oaud` =
  `tessera-slot2-sqs`. Inline policy `slot2-queues` grants exactly `sqs:ReceiveMessage`, `sqs:DeleteMessage` and
  `sqs:ChangeMessageVisibility` on the request queue and `sqs:SendMessage` on the response queue. No managed policies are attached.
- **Key version.** `projects/tessera-slot2/locations/us-east1/keyRings/tessera-v1/cryptoKeys/slot2-spike/cryptoKeyVersions/1`,
  EC_SIGN_P256_SHA256, protection HSM, ENABLED, attestation CAVIUM_V2_COMPRESSED, created 2026-10-14T02:55:53Z. The
  public key PEM fetched at 03:57 has the same sha256 (`1e948f80…02d2`) as `spike-pq/out-gcp/capture.json`.

## (a) Valid frame enqueued and signed: PASS

Frames were built as in `spike_v1_hybrid.py`: the hybrid manifest and one attestation pair under the pair id,
`declared_issue_time` = now (2026-10-14T03:54:04Z). Slot kms was signed by AWS KMS ML-DSA-65 (`alias/tessera-pq-spike`,
e4a7deb4-…, EXTERNAL_MU). Slot gpg came **only** from the policy signer via the queue (request
`req-e9c75c88753f4eea93ef3171514b5a60`, SQS message `0b7995b7-17f5-47e6-9db0-001156dfb63c`, execution
`slot2-signer-mwsd7`, signer clock 03:54:22Z). The gpg manifest-possession signature also came through the signer
(`req-418c4510f7f74a43ac378a29149ef5e8`, kind `manifest`). Offline results (`client.py verify-a`, reading only
`out/evidence-a.json`):

| Check | Result |
|---|---|
| slot-2 sig: P8 A rule-O codec (`gen.decode_sig`, slot gpg) | True |
| slot-2 sig: P8 B rule-O codec (`check.sig_check`, slot gpg) | True |
| slot-2 sig: A ECDSA verify over its frame (`gen.verify_openpgp4`) | True |
| slot-2 sig: B ECDSA verify over its frame (`check.pgp4_verify`) | True |
| tampered frame rejected by A and B | True |
| full receipt (manifest, both frames, both sigs, A_sig), with keys: A `check_receipt` | True |
| full receipt: B `receipt` | True |
| receipt with the slot-2 sig swapped for the possession sig: A and B reject | True |
| kms sig (EXTERNAL_MU) over the full frame: cryptography + dilithium-py | True |
| manifest possession, gpg (via signer): A and B | True / True |
| manifest possession, kms: A and B | True |

Frame f1 776 B, sha256 `fd8b05948a4fb875f0f186e2d444f19e845124297976fe34d9ce88d62fe8205d`. Slot-2 signature 119 B, sha256
`3bccd051fde66c58e5a5ce139eb0ff303a7bdd951908b4a1cda845aff132790e`. A_sig sha256
`ab722ecfa96c1ef15d24415cf6cf4fca7a61bcac1bda7d5161a2ce2e29f7c92a`. (An identical earlier run at 03:48, made before
`deploy.sh harden`, also passed. The record above is the post-hardening run.)

## (b) Declared time 25 h in the past: REFUSED

`req-27fcdf765135441cadd487a515f0a362`, execution `slot2-signer-hj87m`: status `REFUSED`, reason
`DECLARED_TIME_OUTSIDE_EPSILON`, detail `declared 2026-10-13T02:54:35Z, signer clock 2026-10-14T03:55:22Z, difference
-90047 s, epsilon 86400 s`. No `sig_b64` was returned. Before deployment, the same code was tested locally at the
boundaries: −24 h + 5 s was accepted, and +25 h was refused.

## (c) Wrong tag / wrong key_fp: REFUSED

| Request | Frame | Result |
|---|---|---|
| `req-627ec67e998c48bd8da5e25066ba35de` | valid attest payload under tag `tessera-v1/receipt` (not in T) | REFUSED `TAG_UNKNOWN` |
| `req-bce77657a2b4455bbb8fb78306b5a5bd` | same payload under `tessera-v1/receipt-anchor-sig` (in T, not a slot-2 document) | REFUSED `TAG_MISMATCH` |
| `req-078228a3a3a948b1af17576a6e454925` | genuine attest frame whose `signer.key_fp` is the kms slot's `spki-sha256:d1b35a0e…a7a4` | REFUSED `KEY_FP_MISMATCH` |

The Cloud Logging records for job `slot2-signer` list all six requests with the same status and reason
(`jsonPayload.event="response"`).

## (d) The issuer's AWS role has no path to the GCP key

The issuer role is the tessera SSO role, `arn:aws:sts::477139661040:assumed-role/AccountFullAccessRole/…`.

GCP side, read 2026-10-14 ~03:57Z:
- **Key IAM policy** (`slot2-spike`): exactly two bindings, both `serviceAccount:slot2-signer@…`:
  `roles/cloudkms.signer` and `roles/cloudkms.publicKeyViewer`. Key ring `tessera-v1` IAM policy: empty. No other key
  is in the ring.
- **Project IAM**: `user:wamason@gmail.com` owner; `slot2-builder` `roles/logging.logWriter`; Google-managed service
  agents only. Enabling run and cloudbuild had auto-granted `roles/editor` to the Compute default SA and
  `cloudbuild.builds.builder` to the legacy Cloud Build SA. Editor carries `iam.serviceAccounts.actAs` and
  `run.jobs.update`, an indirect route to the key through the job, so both grants were removed (`deploy.sh harden`).
  Nothing runs as either SA.
- **Workload identity pools**: none, including deleted ones. No AWS principal can exchange AWS credentials for a GCP
  token.
- **Service-account keys** (user-managed) for slot2-signer, slot2-invoker and slot2-builder: none. The SA IAM policies
  of all three are empty: nobody holds actAs or token-creator on them.
- **Endpoints**: `gcloud run services list` is empty. Job IAM: only slot2-invoker, `roles/run.invoker`.

AWS side:
- IAM users: none, so no access keys exist.
- us-east-2: 0 Secrets Manager secrets, 0 SSM parameters, 0 S3 buckets. Every other region refuses
  `ListSecrets`/`DescribeParameters` for this role by explicit org SCP deny (`p-phwst3c9`). Read as: this account
  operates in us-east-2 only. *Note:* this role could not enumerate those regions, so the inventory there rests on the
  SCP, not on a listing.
- The only cross-cloud artifact is role `tessera-slot2-signer-sqs`. It grants queue access only (not GCP), and only to
  `accounts.google.com` tokens whose sub/azp is the signer SA. The issuer role calling `sts:AssumeRole` on it:
  `AccessDenied`. A Google ID token for the human user `wamason@gmail.com` presented to `AssumeRoleWithWebIdentity`:
  `AccessDenied`. The trust binds to the SA, not to any Google identity.

Taken together: no GCP credential exists in AWS. The key's IAM policy names only the signer SA, and no federation
runs from AWS into GCP. The issuer role can only enqueue to, and read from, the two queues.

## (e) Exact versions and policies

The signer image digest, code hash, key version, role trust and permissions, and queue ARNs are given above under
"The deployed path". Job `slot2-signer` generation 4: SA `slot2-signer@…`, 1 vCPU, 512 MiB, timeout 120 s, max
retries 0, env (non-secret configuration only) REQUEST/RESPONSE queue URLs, AWS_ROLE_ARN, AWS_AUDIENCE,
KMS_KEY_VERSION, KEY_CREATED, KEY_FP, ALLOWED_ALGS, SIGNER_IMAGE, RUN_SECONDS=40. Scheduler: `* * * * *` UTC, ENABLED,
OAuth as slot2-invoker. Queues: SSE-SQS, retention 86400 s, no resource policy (in-account IAM governs them).

## (f) Resources

See `RESOURCES.md` for every resource created, the auto-grants removed, and the teardown commands.

## Limits (stated, not hidden; DESIGN.md decision 7)

- Whoever controls the AWS account can enqueue any valid frame with a current declared time, and the signer signs it
  (C3, accepted). The ε check limits this to minting at the current time.
- **Manifest frames carry no `declared_issue_time`.** The signer checks their tag, schema, alg and `sset[0]`, but the
  ε check cannot apply to them. An AWS-side takeover can therefore obtain manifest-possession signatures for this
  key at any time. These bind the manifest, not any content or time.
- Whoever controls the GCP project (`wamason@gmail.com` is owner) defeats slot 2 alone. That is the same human who
  administers the AWS account, so this shows separate technical custody only. It does not show separation of
  control (A9.6 *Limit*).
- ALLOWED_ALGS holds only the hybrid id. Under the registered fallback, the job's ALLOWED_ALGS must become
  `OPENPGP4-ECDSA-P256-SHA256`, which is a GCP-side redeploy that AWS cannot perform.
- The signer trusts Cloud Run's system clock. A clock fault shows up as refusals, which fail safe.
