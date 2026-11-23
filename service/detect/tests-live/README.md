# Tessera V1 Live Detection Tests (`service/detect/tests-live/`)

Live detection test suite prepared from `docs/V1-DETECTION-CONTRACT.md` (using **D1–D4 as built**), `docs/V1-CONTRACT.md` §4, and `docs/reviews/detection-tests/BRIEF-gemini.md` (**r5**). Full test matrix and expected evidence classes live in [`docs/reviews/detection-tests/PLAN.md`](../../../docs/reviews/detection-tests/PLAN.md).

## Hard Safety Guarantees Built Into the Code

Every live call passes through [`safety.py`](safety.py):
1. **Strict `us-east-2` endpoint pinning (no overrides):** every `boto3` client pins `region_name="us-east-2"` and an explicit official AWS `endpoint_url`, refuses `AWS_REGION` / `AWS_DEFAULT_REGION` outside `us-east-2`, and refuses `AWS_ENDPOINT_URL`, `AWS_ENDPOINT_URL_*`, `AWS_USE_FIPS_ENDPOINT`, and `AWS_USE_DUALSTACK_ENDPOINT`. Global IAM (`iam.amazonaws.com`) is permitted only with explicit `allow_global_iam=True` for the brief's scoped D7 IAM and throwaway Lambda role tests.
2. **Fresh-run exclusivity & live tag/name/account verification:** pre-flight refuses to start if a ledger file or any AWS resource with `run_id` already exists. Every mutation, dependent call, cleanup, and recovery action re-verifies live AWS ownership by tag (`purpose=detection-test` AND `run_id=<run_id>`), name prefix (`tessera-dtest-<run_id>-*`), caller account ID, and region before any destructive call — never trusting a ledger mapping alone.
3. **Intent-before-create journaling:** a durable `creating` entry is flushed to disk BEFORE every AWS create (including dependent resources: KMS grants, API GW usage-plan keys, IAM inline policies, Lambda permissions, and IAM access keys without logging credential material). Crash recovery reconciles intents via live tag/prefix scans, refuses unverified targets, persists results, and exits non-zero if any residual or refused resource remains.
4. **Production alarm topic protection:** the sole production write permitted by Rule 1 is subscribing our verified throwaway SQS queue (`tessera-dtest-<run_id>-obs-q`) to `tessera-v1-alarms` and unsubscribing that exact live-verified SQS subscription after observation completes. Topic policy and existing subscriptions are never modified; `sns:Unsubscribe` verifies live `TopicArn`, `Protocol == "sqs"`, and `Endpoint == arn:aws:sqs:us-east-2:<acct>:tessera-dtest-<run_id>-obs-q`.
5. **No recorded POSTs & pinned HTTP transport (r5 Rule 3):** `TESSERA_API` is pinned to `https://<10-char-id>.execute-api.us-east-2.amazonaws.com/v1`; HTTP proxies and ALL redirects are disabled/refused; `TESSERA_SMOKE_KEY` is sent only to the pinned host; `D3b` (oversized 413 POST) is **removed** (`NOT COVERED`) because the issuer writes a durable `REFUSED/TOO_LARGE` record + 400-day watcher trace; `D3a` sends only non-UUID `Tessera-Request-Key` rejected with 400 before any DB write; non-2xx POST refusal is checked immediately on status before reading the body.
6. **Single process-wide limiter & daily quota accounting:** one shared `RateLimiter` paces all API traffic strictly below 5 rps (burst 1). `SmokeTestQuotaTracker` accounts for prior same-day `smoke-test` access-log requests (default cap 60; raised to 120 only when entering opt-in `d4c` last).
7. **Zero URL or secret leakage (Rule 5):** SQS queues are identified by queue name (never URL); `sanitize_value` scrubs all `http(s)://` URLs, SQS URLs, secrets, AWS key IDs, and sensitive dict keys/values; SNS messages store strictly allowlisted structured identifiers (no raw excerpts); exceptions log only class names (and AWS error code token), never `str(exc)`.

## Setup & Offline Unit Tests

```bash
cd service/detect/tests-live
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run offline safety and correlation unit tests (no AWS credentials or network needed):

```bash
../../issuer/.venv/bin/python -m pytest -q test_safety_unit.py
```

## Environment Variables (Live Run Only — Never Saved to Disk)

| Variable | Required for | Purpose |
|---|---|---|
| `TESSERA_API` | `--suite api`, `d2`, `d3`, `d4`, `all` | Exact `https://<id>.execute-api.us-east-2.amazonaws.com/v1` stage URL |
| `TESSERA_SMOKE_KEY` | `d3a`, `d4a`, `d4c` | The `smoke-test` API key provided by the author at run time |
| AWS session (`AWS_PROFILE` or exported credentials) | All AWS tests + observer SQS | Short-lived session in `us-east-2` |

## What Each Test Does

### D7 Control-Plane Tampering (Throwaway Resources in `us-east-2`, Global IAM where scoped)
- **`d7-kms`** (`D7-kms-policy`, `D7-kms-grant`, `D7-kms-disable`, `D7-kms-delete`): throwaway KMS key + alias; `PutKeyPolicy`, `CreateGrant` (+ `RevokeGrant`), `DisableKey`, `ScheduleKeyDeletion(PendingWindowInDays=7)`.
- **`d7-s3`** (`D7-s3-policy-put`, `D7-s3-policy-delete`, `D7-s3-lock`): throwaway bucket (`PutBucketPolicy`, `DeleteBucketPolicy`, `DeleteBucket`) and empty Object Lock bucket (`PutObjectLockConfiguration`, zero objects, `DeleteBucket`).
- **`d7-sns`** (`D7-sns-topic-attr`, `D7-sns-sub-throwaway-subscribe`, `D7-sns-sub-throwaway-unsubscribe`, `D7-sns-topic-delete`): throwaway topic `SetTopicAttributes(Policy)`, throwaway SQS `Subscribe`/`Unsubscribe`, and `DeleteTopic`. *(Production `D7-sns-sub-subscribe` and email-only `D7-sns-sub-unsubscribe` run on `tessera-v1-alarms` via the observer.)*
- **`d7-apigw`** (`D7-apigw-key-create`, `D7-apigw-key-update`, `D7-apigw-plan-update`, `D7-apigw-plan-key`): throwaway REST API, disabled API key (value never read/logged), and usage plan.
- **`d7-lambda`** (`D7-lambda-config`, `D7-lambda-code`, `D7-sup-lambda-perm`): zero-permission throwaway IAM role + no-op Python Lambda (`UpdateFunctionConfiguration`, `UpdateFunctionCode`, `AddPermission`/`RemovePermission`).
- **`d7-cloudtrail`** *(opt-in: `--include-cloudtrail`)* (`D7-ct-update`, `D7-ct-selectors`, `D7-ct-stop`, `D7-ct-delete`): single-region throwaway trail backed by throwaway bucket; records `was_logging_before_stop=False` honestly for `StopLogging`.
- **`d7-iam-role`** (`D7-iam-role-put-policy`, `D7-iam-role-delete-policy`, watcher multi-region trail path, default observer wait **3600 s**): deny-trust throwaway role + inline deny policy.
- **`d7-iam-access-key`** *(opt-in: `--include-iam-access-key`)* (`D7-iam-accesskey`, watcher path, default wait **3600 s**): zero-permission throwaway IAM user + access key (secret discarded in memory, never logged; live enumerate-and-delete in `finally`).
- **Supplementary EventBridge checks** (`--suite d7-sup`): `d7-sup-sqs`, `d7-sup-ddb`, `d7-sup-cw`, `d7-sup-logs`, `d7-sup-eb`.

### D1–D4 API Gateway Perimeter (Production Path)
- **`d2a`** (`D2a` + `D1c`): after verified `OK` baseline, 55 × `GET /v1/requests/<uuid>` with no `x-api-key` at 2.0 rps.
- **`d2b`** (`D2b`): waits for verified `OK` baseline, then 55 × `GET /v1/requests/<uuid>` with random invalid `x-api-key` at 2.0 rps.
- **`d3a`** (`D3a`): after verified `OK` baseline, 6 × `POST /v1/requests` with non-UUID `Tessera-Request-Key` (`TESSERA_SMOKE_KEY`, 0.5 rps, 400 before any DB write). *(`D3b` is removed / `NOT COVERED` under r5 Rule 3.)*
- **`d4a`** (`D4a`): paced read-only `GET /v1/requests/<uuid>` (`0.125` rps, accounting for prior same-day access-log count) to bring daily logged requests to `55` (> 50).
- **`d4c`** *(opt-in: `--include-quota-exhaustion`, enforced LAST)* (`D4c`): paced read-only `GET`s until logged `QUOTA_EXCEEDED` 429 (hard cap 120 daily total).

## Running & Recovery

```bash
# Always validate first with --dry-run (never combine with --cleanup-ledger)
.venv/bin/python run_tests.py --dry-run --suite all

# Live runs automatically keep the observer SQS queue alive for the max contract latency
# (600s EventBridge/D2, 900s D3a/D4, 3600s D7 IAM):
.venv/bin/python run_tests.py --suite d7
.venv/bin/python run_tests.py --suite d7-sup
.venv/bin/python run_tests.py --suite d7-iam
.venv/bin/python run_tests.py --suite api

# Crash recovery (verifies every resource live, persists results, exits non-zero on residuals):
.venv/bin/python run_tests.py --cleanup-ledger run-output/ledger-<run_id>.json
```
