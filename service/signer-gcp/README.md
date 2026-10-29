# Slot-2 policy signer (GCP Cloud KMS HSM, P-256, OpenPGP v4)

> **Status: OWNER DRAFT, 2026-10-27** (built by an agent for the owner). Built and tested locally against fake
> SQS, S3 and KMS clients. **Not deployed, not reviewed.** Nothing here has run in GCP or AWS. The 2026-10-14
> instrument (`prototype/policy-signer/`) is the design input. This package does not import it.

One Cloud Run **job** execution drains the issuer's `gpg` request queue for a time budget (40 s). For each request it
either signs the frame with the HSM key, producing one rule-O packet (ENCODING-V1 §5.2), or refuses with a reason.
Either way it answers on the `gpg` response queue. Queue messages and referenced frame objects are untrusted input.
Placement: `docs/decisions/2026-10-27-v1-signer-placement.md` item 1 (slot 2 stays on GCP, with its own policy and
logs).

## What it enforces

Every check runs before the HSM is asked to sign. Each one has a test in `tests/test_policy.py` unless another file
is named.

| Check | Refusal reason |
|---|---|
| The body is one JSON object of at most 1 MiB, in exactly one of the issuer's two shapes (below), with a valid `request_id`, an RFC 3339 `sign_by`, and canonical base64 or a `frames/<rid>/<sha256>` reference | `BAD_REQUEST` |
| IS-09: the object at `frame_ref` (in the configured bucket only) exists, and its SHA-256 is `frame_sha256` | `FRAME_UNAVAILABLE`, `FRAME_DIGEST_MISMATCH` |
| The frame decodes under the **service verifier's codec** (`tessera_verify.codec.read_frame`) as `tessera-v1/attest` or `tessera-v1/manifest`, within schema | the codec's code (`TAG_MISMATCH`, `TAG_UNKNOWN`, `TRUNCATED`, `TRAILING`, `SCHEMA`, `JSON_*`, ...) |
| The alg (attest `common.alg`, manifest `alg`) is the registered pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` | `ALG_NOT_ALLOWED` |
| Attest `signer.key_fp` is this key's `gpg-sha256` fingerprint. For a manifest, `sset[0]` must be | `KEY_FP_MISMATCH` |
| Attest: \|`declared_issue_time` − signer clock\| ≤ ε = 24 h (A9.2; runbook §3) | `DECLARED_TIME_OUTSIDE_EPSILON` |
| IS-03: the clock, read again **immediately before the HSM call**, is not past the configured `SIGN_UNTIL`, and not past the request's `sign_by` | `SIGNING_STOPPED` |
| The HSM output verifies under the key, and the packet passes the service verifier's `parse_signature`, `sig_policy` and `signature_verifies` on the frame (the issuer's own checks) | after 3 deliveries: `SIGNER_ERROR` |
| Any unexpected exception | `INTERNAL` (signs nothing) |

At startup, before any message is read or any AWS credential is obtained, the job checks the KMS public key. The
key-version name must be the configured one, the algorithm `EC_SIGN_P256_SHA256` and the protection level `HSM`. The
key's `gpg-sha256` fingerprint, computed with `KEY_CREATED`, must equal the pinned `KEY_FP`. If any check fails, the
job exits with status 2 and serves nothing (`tests/test_signer.py::test_startup_*`).

ε, the allowed alg and the policy are code. Configuration holds only the deployment facts: queues, bucket, key
version, fingerprint and signing stop. No field of a request can change the policy.

## What it assumes

- **The Cloud Run system clock is right.** Nothing here detects a clock fault, and none fails safe in general. For ε
  the check is relative to that same clock, so a declaration that tracks a faulty clock passes (SG-02; this first
  said ε "fails safe"). A clock running slow would sign after `SIGN_UNTIL` or `sign_by`. Every check runs on one
  clock reading taken after the frame is in hand and immediately before signing or resending. A signature the HSM
  returns after a cutoff is withheld and logged, but the HSM has still produced it (SG-01).
- **The service verifier's codec is correct.** It is the same code that verifies receipts. The 2026-10-14 instrument
  used P8 implementation A instead. The two can name the same rejection differently. The issuer records the reason
  and does not interpret it.
- `KEY_CREATED` is the creation time bound into the published fingerprint. The configured values for `slot2-spike`
  v1 reproduce the pinned `gpg-sha256:b6e37f7c…077c` from the archived public key. This was checked once by hand on
  2026-10-27; it is not a test. For the production key (`SLOT2_KEY_*`, a new key), the job's startup check rebuilds the fingerprint from the
  live public key and `KEY_CREATED`, and refuses to run on a mismatch.
- The Cloud KMS `publicKey` response carries `protectionLevel`. This is assumed from the API reference and not
  checked against the live API. If the field is absent, the job refuses to run (fail safe, but it blocks deployment).
- `SIGN_UNTIL` is set per window (issuance-not-after − 96 h), and the job is redeployed when the window changes.
  After `SIGN_UNTIL` the job refuses everything.
- SQS delivers at least once. See E-02 below.

## The requester check: who can cause a slot-2 signature

1. **Anything that can write to its request queue** (`tessera-v1-issuer-gpg-requests`): the issuer's poller role,
   and any principal in AWS account 477139661040 that holds, or can grant itself, `sqs:SendMessage` on it. This is
   C3: capturing the issuing account means slot 2 signs. The policy limits what a captor gets: V1 attest or manifest
   frames under the pair id that name this key, with a declared time within 24 h of the signer's clock, before the
   stop. Writing to `frames/*` without the queue gets nothing. A substituted object fails the digest check.
2. **Anyone who can change the Cloud Run job, or run code as its service account, in project `tessera-slot2`.** That
   means `run.jobs.update` together with `iam.serviceAccounts.actAs` on `tessera-signer-gpg@`, or token creation for
   that account. With either, they can sign anything, with no policy. Pushing an image alone does not change the job,
   because the job pins its image by digest. Narrower still: `run.jobs.runWithOverrides` on the job lets one
   execution change its environment (`SIGN_UNTIL`, the queues) without changing the job (SG-04). The scheduler's
   `roles/run.invoker` grant does not include it. `service/issuer/DEPLOY.md` step 8 lists who holds it before
   issuance starts.
3. **Anyone who can change the key's IAM** (`cloudkms.cryptoKeys.setIamPolicy` on the production key, or project
   owner/editor). They can grant themselves `cloudkms.signer` and bypass the policy.
4. **While the 2026-10-14 instrument still exists**, also anything that can write to `tessera-slot2-requests`,
   because its job `slot2-signer` signs with the same key. `deploy.sh retire-instrument` removes that job and its key
   grants. Until it runs, items 1 to 3 are not the whole list.

Items 2 and 3 are the "GCP project takeover defeats slot 2" limit the instrument already stated.

## AWS credentials

There is no static credential anywhere, the same as the instrument. The job runs as `tessera-signer-gpg@tessera-slot2`.
The Google metadata server mints an **ID token** for that account with audience `tessera-v1-signer-gpg`. STS
`AssumeRoleWithWebIdentity` exchanges it for the role `tessera-v1-signer-gpg-federated`. That role's trust names
`accounts.google.com` with the account's unique ID as `sub` and `aud`, and the audience as `oaud`. The federated
role may do one thing: `sts:AssumeRole` into `tessera-v1-issuer-signer-gpg`, the issuer's Terraform signer role.
`signer_principals = { gpg = "arn:aws:iam::477139661040:role/tessera-v1-signer-gpg-federated" }` makes that role. It
already grants `sqs:ReceiveMessage`/`DeleteMessage` on the gpg request queue, `sqs:SendMessage` on the gpg response
queue, and **`s3:GetObject` on `frames/*`** (`service/issuer/infra/main.tf`, `data.aws_iam_policy_document.signer`).
The bucket uses SSE-S3, so no KMS decrypt grant is needed. The code is in `tessera_signer/gcp.py` `aws_clients`
(tests: `tests/test_adapters.py`).

**Why two hops.** The issuer's signer role trusts an *AWS* principal (`principals { type = "AWS" }`). A Google
identity cannot assume such a role directly. The hop needs **no Terraform change**. The cost is one IAM role made
outside Terraform, by `deploy.sh role`.

**The one-hop alternative (a Terraform change, not made here; `service/issuer/infra/` is being edited elsewhere).**
For the `gpg` slot, the signer role trusts the web identity itself:

```hcl
# variables.tf
variable "signer_web_identities" {
  description = "Per slot: a Google service account (unique ID) and ID-token audience allowed to assume the signer role by web identity, instead of an AWS principal."
  type        = map(object({ sub = string, oaud = string }))
  default     = {}
}

# main.tf, data "aws_iam_policy_document" "signer_assume": for_each over
#   setunion(keys(var.signer_principals), keys(var.signer_web_identities)), and for a slot in signer_web_identities:
statement {
  actions = ["sts:AssumeRoleWithWebIdentity"]
  principals {
    type        = "Federated"
    identifiers = ["accounts.google.com"]
  }
  condition {
    test     = "StringEquals"
    variable = "accounts.google.com:sub"
    values   = [var.signer_web_identities[each.key].sub]
  }
  condition {
    test     = "StringEquals"
    variable = "accounts.google.com:aud"          # for Google tokens AWS maps this key to azp (the account's ID)
    values   = [var.signer_web_identities[each.key].sub]
  }
  condition {
    test     = "StringEquals"
    variable = "accounts.google.com:oaud"         # the token's own aud
    values   = [var.signer_web_identities[each.key].oaud]
  }
}
# aws_iam_role.signer, data.aws_iam_policy_document.signer and aws_iam_role_policy.signer iterate over the same union.
```

With that change, `AWS_ROLE_ARN` is `tessera-v1-issuer-signer-gpg`, `AWS_CHAIN_ROLE_ARN` is unset, and the
federated role and `deploy.sh role` are not needed.

## Protocol

The issuer's side is authoritative: `service/issuer/tessera_issue/signers.py`, `SlotSigner.send` and the stand-in.
`tests/test_issuer_protocol.py` drives this signer with the issuer's own `SlotSigner`. It builds requests inline and
by reference, reads the responses, and verifies them with `SlotSigner.verify`.

- Request, inline: `{"request_id", "sign_by", "frame_b64"}`.
- Request, by reference: `{"request_id", "sign_by", "frame_ref", "frame_sha256"}`.
- Response: `{"v": 1, "request_id", "sqs_message_id", "status": "SIGNED"|"REFUSED", "kind"?, "sig_b64"?,
  "sig_sha256"?, "frame_sha256"?, "reason"?, "detail"?, "signer": {"slot": "gpg", "clock", "code_sha256",
  "image", "key_version", "key_fp", "epsilon_s", "alg", "sign_until"}}`.
- The issuer reads `request_id`, `status`, `sig_b64` and `reason`. The other fields are for logs and operators.

Differences from the instrument's protocol, where the issuer's protocol governs:

| # | Instrument (2026-10-14) | This signer | Why |
|---|---|---|---|
| 1 | Request members exactly `{request_id, frame_b64}` | Adds `sign_by` (**required**), and the reference shape `{frame_ref, frame_sha256}` | IS-03, IS-09. The issuer's `SlotSigner.send` allows `sign_by=None`, but its pipeline always sends one. A request with no deadline is refused, not signed at any later time |
| 2 | Any base64 that `b64decode(validate=True)` accepts | Canonical base64 only | The issuer sends canonical base64. The verifier's `b64` is used |
| 3 | `REQUEST_MALFORMED`, `REQUEST_TOO_LARGE` | `BAD_REQUEST`, with the detail in `detail` | The stand-in's reason |
| 4 | — | New reasons: `SIGNING_STOPPED`, `FRAME_UNAVAILABLE`, `FRAME_DIGEST_MISMATCH` | IS-03, IS-09 |
| 5 | `ALLOWED_ALGS` from the environment | The pair id, in code | The policy is code |
| 6 | Codec: vendored P8 implementation A (gen.py) | The service verifier's codec | No `formal/` or `prototype/` code in the service. Refusal codes can be named differently |
| 7 | Self-check: rule-O codec only | Codec, `sig_policy`, and verification on the frame (the issuer's checks) | The issuer would reject anything else as `bad-signature` |
| 8 | Signature creation time: a separate `time.time()` | The same clock read as the stop check | So the creation time is never past `SIGN_UNTIL` or `sign_by` |
| 9 | The same request twice in one run: signed twice | The second gets the first signature again | E-02: fewer orphan signatures |
| 10 | Response `signer.allowed_algs` | `signer.alg`, `signer.slot` (the stand-in's), `signer.sign_until`, top-level `sig_sha256` | Logging |
| 11 | Startup: name, algorithm, fingerprint | Also `protectionLevel == HSM` and the PEM's CRC32C | Stated custody |
| 12 | Queues `tessera-slot2-*`, made by the instrument's script; role with SQS rights directly | The issuer's Terraform queues `tessera-v1-issuer-gpg-*`; role chained to the Terraform signer role (adds `s3:GetObject frames/*`) | One set of queues per slot |
| 13 | Visibility timeout 60 s | 120 s (the issuer's Terraform default for request queues) | — |
| 14 | Started by Cloud Scheduler, or `gcloud run jobs execute` from the client (E-01 fix) | Cloud Scheduler every minute. **The issuer's SNS wake topic for `gpg` has no subscriber** | See E-01 |

The stand-in decodes a manifest frame without checking which key `sset[0]` names. This signer keeps the
instrument's stricter check (`KEY_FP_MISMATCH`). The issuer's real manifests name the window's gpg key, so they pass.

## E-01 and E-02 on this side

- **E-01 (on-demand start).** The issuer publishes to the SNS topic `tessera-v1-issuer-gpg-wake`. A GCP job cannot
  subscribe to SNS without a public HTTPS endpoint, so this signer does not try. Cloud Scheduler runs the job every
  minute from window open to `SIGN_UNTIL`, and the scheduler is paused afterwards. The issuer's poller runs every
  10 min, so a one-minute tick adds little latency. The cost is one short execution a minute, the instrument's
  measured cost profile (`prototype/policy-signer/RESOURCES.md` G11). **Open:** whether the wake topic should get a
  subscriber, or the issuer should stop publishing for `gpg`.
- **E-02 (late and duplicate answers).** Every signature is logged to Cloud Logging (request id, frame SHA-256,
  signature SHA-256) **before** its response is sent (`test_every_signature_is_logged_before_its_response`). If the
  issuer retries with the same request id and frame inside one run, the retry gets the same signature
  (`test_duplicate_request_in_one_run_gets_the_same_signature`). Across runs there is no memory. If a response was
  sent but its delete failed, the next run signs again, and both responses carry the same request id and verify
  (`test_redelivery_after_a_failed_delete_signs_again_in_a_later_run`). The issuer's drain records the second
  response as a duplicate. A request whose `sign_by` has passed by the time a run reaches it is refused
  (`test_late_request_past_sign_by_is_refused_not_signed`). That puts a time bound on any late signature.

## Deploy

Requires `gcloud` (logged in, project `tessera-slot2`) and the `tessera` AWS profile. Nothing below has been run.

```bash
cd service/signer-gcp && .venv/bin/python -m pytest -q          # green first
export REQUEST_QUEUE_URL=...  RESPONSE_QUEUE_URL=...  FRAME_BUCKET=...   # terraform output signer_queues / result_bucket
export SIGN_UNTIL=YYYY-MM-DDTHH:MM:SSZ                           # issuance-not-after minus 96 h
./deploy.sh sas                 # runtime and scheduler service accounts
./deploy.sh role                # AWS federated role (needs the runtime account's unique ID)
#   then, in service/issuer/infra: signer_principals = { gpg = "<printed ARN>" }; terraform apply
./deploy.sh keyiam              # cloudkms.signer + publicKeyViewer on $SLOT2_KEY (the NEW production key) for the runtime account only
./deploy.sh registry            # artifact repo tessera-signer
./deploy.sh build               # stages signer-gcp + verifier, Cloud Build, records .image-digest
./deploy.sh job                 # Cloud Run job tessera-signer-gpg, image by digest
./deploy.sh run-now             # one execution; its log must show "start" with the pinned key_fp, then "done"
./deploy.sh scheduler           # every minute while signing is possible
./deploy.sh harden              # re-check project and key IAM
./deploy.sh retire-instrument   # delete slot2-signer job/scheduler and its key grants (requester check item 4)
```

## Tests

```bash
uv venv .venv --python 3.14 && uv pip install -p .venv/bin/python cryptography==50.0.2 pytest
.venv/bin/python -m pytest -q
```

`pyproject.toml` puts `../verifier` and `../issuer` on the test path. The issuer is used only by
`test_issuer_protocol.py`. `test_independence.py` checks that the package imports nothing from `prototype/`,
`formal/` or the issuer.

## Not done, or not known

- Nothing has run against real Cloud KMS, SQS, S3 or STS. The adapters are tested over fake transports only.
- The `python:3.14-slim` base image is referenced by tag, not digest. It should be pinned by digest before the first
  real build.
- The policy does not pin the frame's `issuer` domain, or the manifest's `key_fp` (the KMS slot's fingerprint). A
  captor of the queue could get the gpg key's possession signature over a manifest that pairs it with a KMS key of
  its own. Whether that is within C3 as registered is for the owner to judge. Configuration could narrow it.
- No review has been run. A Codex review and an owner read come before deployment.
