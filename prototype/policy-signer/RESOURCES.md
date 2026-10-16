# Slot-2 policy signer: cloud resource manifest (evidence item f)

Created 2026-10-14 by the owner instance with `prototype/policy-signer/deploy.sh`. The only scopes used were AWS account
477139661040 (profile `tessera`, us-east-2) and GCP project `tessera-slot2` (us-east1). No static credentials were
created anywhere: no AWS IAM users or access keys, and no GCP service-account keys. **Pre-existing and not created here:**
the GCP key ring `tessera-v1`, the key `slot2-spike` v1, the AWS KMS key `alias/tessera-pq-spike`, and the project itself.
Teardown never touches them: the hard rule is no deletion, disabling or scheduled destruction of either key.

## GCP, project tessera-slot2

| # | Resource | Identifier | Cost-relevant |
|---|---|---|---|
| G1 | APIs enabled | run, cloudscheduler, artifactregistry, cloudbuild, iamcredentials, sts, **iam** (iam was needed to create service accounts) | no |
| G2 | Service account (runtime) | `slot2-signer@tessera-slot2.iam.gserviceaccount.com` (uniqueId 100451337620005518976) | no |
| G3 | Service account (scheduler) | `slot2-invoker@tessera-slot2.iam.gserviceaccount.com` | no |
| G4 | Service account (build) | `slot2-builder@tessera-slot2.iam.gserviceaccount.com` | no |
| G5 | Key IAM bindings on `slot2-spike` | slot2-signer: `roles/cloudkms.signer`, `roles/cloudkms.publicKeyViewer` | no |
| G6 | Artifact Registry repo | `us-east1-docker.pkg.dev/tessera-slot2/slot2` (docker), with 4 images (`signer`, digests below) | storage, 152 MB |
| G7 | Repo IAM | slot2-builder: `roles/artifactregistry.writer` on repo `slot2` | no |
| G8 | GCS bucket (build source staging) | `gs://tessera-slot2-build-src` (us-east1, uniform access, public access prevention, delete objects after 7 days) | negligible |
| G9 | Bucket IAM | slot2-builder: `roles/storage.objectViewer` on the bucket | no |
| G10 | Project IAM | slot2-builder: `roles/logging.logWriter` (Cloud Build with a user-specified SA needs it) | no |
| G11 | Cloud Run **job** (not a service; no endpoint) | `slot2-signer`, us-east1, image pinned by digest, SA slot2-signer, 1 vCPU, 512 MiB, 120 s timeout, 0 retries | **yes**: one execution per minute, about 20 to 30 s each |
| G12 | Job IAM | slot2-invoker: `roles/run.invoker` on job `slot2-signer` (permissions: run.jobs.run, no overrides) | no |
| G13 | Cloud Scheduler job | `slot2-signer-tick`, us-east1, `* * * * *` UTC, POST `run.googleapis.com/v2/.../jobs/slot2-signer:run`, OAuth as slot2-invoker | small (one job) |
| G14 | Cloud Build builds | 4 builds in us-east1 (983482fc, 5bf4eb91, ea38c277, 82e2139e; all SUCCESS) (build minutes only; no standing resource) | spent |
| G15 | **Removed** auto-grants (side effects of enabling run/cloudbuild) | `990386490765-compute@developer.gserviceaccount.com` `roles/editor` and `990386490765@cloudbuild.gserviceaccount.com` `roles/cloudbuild.builds.builder`, at project level: removed by `deploy.sh harden` | no |
| G16 | Google-managed service agents created by the APIs | run, cloudbuild, cloudscheduler, artifactregistry, containerregistry, pubsub service agents (and the default compute and legacy Cloud Build SAs themselves) | no |

Images in G6 (`signer`): `sha256:80342551793c08249a454436b54bdb6713f6a4c95fa5a9bad095493cd227adb5` (**deployed**, tag
843e6e2729c103ee); superseded during bring-up: `sha256:9e77534331b7...` (wrong metadata path), `sha256:eb7e010b23c5...`
(same, with error detail), `sha256:2ab10ee81847...` (a metadata-probe build). Only the deployed digest is referenced by the job.

## AWS, account 477139661040, us-east-2

| # | Resource | Identifier | Cost-relevant |
|---|---|---|---|
| A1 | SQS queue (requests) | `arn:aws:sqs:us-east-2:477139661040:tessera-slot2-requests` (SSE-SQS, retention 1 day, visibility 60 s) | free tier (about 3 requests per minute idle) |
| A2 | SQS queue (responses) | `arn:aws:sqs:us-east-2:477139661040:tessera-slot2-responses` (same settings) | free tier |
| A3 | IAM role | `arn:aws:iam::477139661040:role/tessera-slot2-signer-sqs` (RoleId AROAW6F55ODYKNNIKEIZQ), trust: `accounts.google.com` web identity, `sub` = `aud` (azp) = 100451337620005518976, `oaud` = `tessera-slot2-sqs` | no |
| A4 | Inline role policy | `slot2-queues` on A3: Receive/Delete/ChangeMessageVisibility on A1; SendMessage on A2 | no |

No IAM OIDC provider resource was created: `accounts.google.com` is a built-in web identity provider for STS.

## Local files (not cloud resources)

`prototype/policy-signer/.image-digest` (the deployed digest) and `prototype/policy-signer/out/` (evidence captures:
frames, signatures and public keys only, no credentials).

## Teardown

Run in this order. Nothing below touches `slot2-spike`, its key ring, or `alias/tessera-pq-spike`.

```bash
G="$HOME/.local/bin/gcloud --project=tessera-slot2 --quiet"
A="$HOME/.local/bin/aws --profile tessera --region us-east-2"

# Stop the trigger first, then the job (G13, G12, G11)
$G scheduler jobs delete slot2-signer-tick --location=us-east1
$G run jobs delete slot2-signer --region=us-east1

# Key IAM: remove the signer's two bindings (G5). The key itself stays.
$G kms keys remove-iam-policy-binding slot2-spike --keyring=tessera-v1 --location=us-east1 \
  --member=serviceAccount:slot2-signer@tessera-slot2.iam.gserviceaccount.com --role=roles/cloudkms.signer
$G kms keys remove-iam-policy-binding slot2-spike --keyring=tessera-v1 --location=us-east1 \
  --member=serviceAccount:slot2-signer@tessera-slot2.iam.gserviceaccount.com --role=roles/cloudkms.publicKeyViewer

# Build path (G10, G9/G8, G7/G6)
$G projects remove-iam-policy-binding tessera-slot2 --condition=None \
  --member=serviceAccount:slot2-builder@tessera-slot2.iam.gserviceaccount.com --role=roles/logging.logWriter
$G storage rm --recursive gs://tessera-slot2-build-src     # deletes the bucket and its staged source tarballs
$G artifacts repositories delete slot2 --location=us-east1 # deletes the repo and all four images

# Service accounts (G2-G4)
$G iam service-accounts delete slot2-signer@tessera-slot2.iam.gserviceaccount.com
$G iam service-accounts delete slot2-invoker@tessera-slot2.iam.gserviceaccount.com
$G iam service-accounts delete slot2-builder@tessera-slot2.iam.gserviceaccount.com

# AWS (A4, A3, A1, A2)
$A iam delete-role-policy --role-name tessera-slot2-signer-sqs --policy-name slot2-queues
$A iam delete-role --role-name tessera-slot2-signer-sqs
$A sqs delete-queue --queue-url https://sqs.us-east-2.amazonaws.com/477139661040/tessera-slot2-requests
$A sqs delete-queue --queue-url https://sqs.us-east-2.amazonaws.com/477139661040/tessera-slot2-responses

# Optional: disable the APIs this deployment enabled (G1). cloudkms stays enabled (the key needs it).
$G services disable run.googleapis.com cloudscheduler.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com iamcredentials.googleapis.com sts.googleapis.com
```

To pause rather than tear down (stops nearly all cost): `$G scheduler jobs pause slot2-signer-tick --location=us-east1`.
Resume it with `... resume ...`.

G15 restore (only if something later needs the Google defaults back):
`$G projects add-iam-policy-binding tessera-slot2 --condition=None --member=serviceAccount:990386490765-compute@developer.gserviceaccount.com --role=roles/editor`
and the same for `990386490765@cloudbuild.gserviceaccount.com` with `roles/cloudbuild.builds.builder`.
