# Tessera V1 Live Detection Tests (`service/detect/tests-live/`)

Live detection test suite prepared from `docs/V1-DETECTION-CONTRACT.md` (using **D1–D4 as built**), `docs/V1-CONTRACT.md` §4, and `docs/reviews/detection-tests/BRIEF-gemini.md`. Full test matrix and expected evidence classes live in [`docs/reviews/detection-tests/PLAN.md`](../../../docs/reviews/detection-tests/PLAN.md).

## Hard Safety Guarantees Built Into the Code

Every live call passes through [`safety.py`](safety.py):
1. **Region locked to `us-east-2`:** every `boto3` client forces `region_name="us-east-2"` and refuses to run if `AWS_REGION` or `AWS_DEFAULT_REGION` is set to another region.
2. **Strict throwaway resource prefix:** every created, modified, or deleted resource name/ARN/URL must match `tessera-dtest-<run_id>-*` and must never contain `tessera-v1`. Every taggable resource is tagged `purpose=detection-test`.
3. **Production alarm topic protection:** the sole production write permitted by Rule 1 is subscribing our own throwaway SQS queue (`tessera-dtest-<run_id>-obs-q`) to `tessera-v1-alarms` and unsubscribing that exact `SubscriptionArn` in `finally`. The topic policy and existing subscriptions are never touched; if `sns:Subscribe` is denied, the runner stops and reports `TopicPolicyChangeRequired`.
4. **No issuance ever:** `POST /v1/requests` accepts raw bytes (≤ 1 MiB) with a UUID `Tessera-Request-Key`. `safety.assert_safe_api_request` enforces that `D3a` sends a provably non-UUID `Tessera-Request-Key` (guaranteed 400 `BAD_REQUEST`) and `D3b` sends `1,100,000` raw bytes (> 1 MiB, guaranteed 413 `TOO_LARGE`). Any `2xx` response to a `POST` immediately aborts the run. Unauthenticated/invalid-key `GET`s are restricted strictly to `/v1/requests/<uuid>`.
5. **Rate & quota guards:** `RateLimiter` enforces a hard ceiling of `4.5` rps and burst `1` (strictly below the usage plan's 5 rps / burst 20). `SmokeTestQuotaTracker` caps `smoke-test` calls at `60` by default (raised to `120` only with `--include-quota-exhaustion`).
6. **Zero secret leakage:** `TESSERA_API` and `TESSERA_SMOKE_KEY` are read only from environment variables and redacted by `safety.sanitize_value` before any ledger write. `D7-iam-access-key` discards credentials immediately in memory without printing or logging them.

## Setup

```bash
cd service/detect/tests-live
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Offline safety unit tests (no AWS credentials or `boto3` needed):

```bash
../../issuer/.venv/bin/python -m pytest -q test_safety_unit.py
```

## Environment Variables

Supply these only at live-run time; **never** commit or write them into any file:

| Variable | Required for | Purpose |
|---|---|---|
| `TESSERA_API` | `--suite api`, `d2`, `d3`, `d4`, `all` | Base HTTPS URL of the deployed API Gateway stage (e.g., `https://.../v1` — no trailing slash needed) |
| `TESSERA_SMOKE_KEY` | `d3a`, `d3b`, `d4a`, `d4c` | The `smoke-test` API key provided by the author at run time |
| AWS session (`AWS_PROFILE` or exported credentials) | All AWS tests + observer SQS | Short-lived session in `us-east-2` |

## What Each Test Does

### D7 Control-Plane Tampering (Throwaway Resources in `us-east-2`)
- **`d7-kms`** (`D7-kms-policy`, `D7-kms-grant`, `D7-kms-disable`, `D7-kms-delete`): creates throwaway symmetric KMS key + `alias/tessera-dtest-<run>-kms`, calls `PutKeyPolicy`, `CreateGrant` (+ `RevokeGrant`), `DisableKey`, and `ScheduleKeyDeletion(PendingWindowInDays=7)`.
- **`d7-s3`** (`D7-s3-policy`, `D7-s3-lock`): creates throwaway bucket `tessera-dtest-<run>-bkt` (`PutBucketPolicy`, `DeleteBucketPolicy`, `DeleteBucket`) and empty Object Lock bucket `tessera-dtest-<run>-lock-bkt` (`PutObjectLockConfiguration`, zero objects written, `DeleteBucket`).
- **`d7-sns`** (`D7-sns-topic`): creates throwaway topic `tessera-dtest-<run>-topic`, calls `SetTopicAttributes`, deletes topic. *(Production `D7-sns-sub` is exercised automatically when the observer subscribes/unsubscribes its throwaway SQS queue on `tessera-v1-alarms`.)*
- **`d7-apigw`** (`D7-apigw-key`, `D7-apigw-plan`): creates throwaway REST API, disabled API key (value never logged), and usage plan; updates both; attaches/detaches key; deletes all.
- **`d7-lambda`** (`D7-lambda-config`, `D7-lambda-code`, `D7-sup-lambda-perm`): creates zero-permission throwaway IAM role + no-op Python Lambda, runs `UpdateFunctionConfiguration`, `UpdateFunctionCode`, `AddPermission` (+ `RemovePermission`), deletes function and role.
- **`d7-cloudtrail`** *(opt-in: `--include-cloudtrail`)* (`D7-ct-update`, `D7-ct-selectors`, `D7-ct-stop`, `D7-ct-delete`): creates single-region throwaway trail `tessera-dtest-<run>-trail` backed by throwaway bucket `tessera-dtest-<run>-ct-bkt`, calls `UpdateTrail`, `PutEventSelectors`, `StopLogging`, `DeleteTrail`, empties and deletes throwaway bucket. Never touches the production trail.
- **`d7-iam-role`** (`D7-iam-role`, watcher multi-region trail path, latency up to ~1 h): creates deny-trust throwaway role `tessera-dtest-<run>-role`, attaches/detaches explicit-Deny inline policy, deletes role.
- **`d7-iam-access-key`** *(opt-in: `--include-iam-access-key`)* (`D7-iam-accesskey`, watcher path): creates zero-permission throwaway IAM user `tessera-dtest-<run>-user`, creates and immediately deletes an access key (secret discarded in memory, never logged), deletes user.
- **Supplementary EventBridge checks** (`--suite d7-sup`): `d7-sup-sqs`, `d7-sup-ddb` (`UpdateTimeToLive`), `d7-sup-cw` (`PutMetricAlarm`/`DeleteAlarms`), `d7-sup-logs` (`PutRetentionPolicy` on `tessera-dtest-<run>-logs`), `d7-sup-eb` (`PutRule`/`DeleteRule`).

### D1–D4 API Gateway Perimeter (Production Path)
- **`d2a`** (`D2a` + `D1c`): 55 × `GET /v1/requests/<uuid>` with no `x-api-key` at 2.0 rps (~28 s). Triggers D2 missing-key and D1c 50+ 4XX backstop.
- **`d2b`** (`D2b`): 55 × `GET /v1/requests/<uuid>` with random invalid `x-api-key` at 2.0 rps. Run after D2 alarm returns to `OK` (or pass `--d2-gap-seconds 600`).
- **`d3a`** (`D3a`): 6 × malformed `POST /v1/requests` (non-UUID `Tessera-Request-Key`, `TESSERA_SMOKE_KEY`, 0.5 rps, expect HTTP 400).
- **`d3b`** (`D3b`): 6 × oversized `POST /v1/requests` (1,100,000 bytes > 1 MiB, `TESSERA_SMOKE_KEY`, 0.5 rps, expect HTTP 413). Run in a separate 1 h window from `d3a` to independently prove 413 logging.
- **`d4a`** (`D4a`): paced read-only `GET /v1/requests/<uuid>` with `TESSERA_SMOKE_KEY` at 1 req / 8 s (`0.125` rps, ≤ 38 req / 5 min so D1c stays silent) until cumulative daily requests reach `55` (> 50).
- **`d4c`** *(opt-in: `--include-quota-exhaustion`, run LAST)* (`D4c`): paced read-only `GET`s with `TESSERA_SMOKE_KEY` until HTTP `429` `QUOTA_EXCEEDED` (hard cap 120). Exhausts `smoke-test`'s daily quota for the remainder of the UTC day.

## Running the Suite

Always validate with `--dry-run` first:

```bash
.venv/bin/python run_tests.py --dry-run --suite all
```

Recommended phased live execution (once author approves live session):

```bash
# 1. D7 EventBridge + supplementary + IAM role (observer SQS polls 180s)
.venv/bin/python run_tests.py --suite d7 --wait-sns-seconds 180
.venv/bin/python run_tests.py --suite d7-sup --wait-sns-seconds 180
.venv/bin/python run_tests.py --suite d7-iam --wait-sns-seconds 60
# Note: D7 IAM findings arrive via the watcher up to ~1 h later; check author mailbox via steward.

# 2. D2a (+ D1c), wait for alarm reset (~10-15 min), then D2b
.venv/bin/python run_tests.py --only d2a --wait-sns-seconds 600
.venv/bin/python run_tests.py --only d2b --wait-sns-seconds 600

# 3. D3a, then D3b (in a separate 1 h window), then D4a
.venv/bin/python run_tests.py --only d3a --wait-sns-seconds 600
.venv/bin/python run_tests.py --only d3b --wait-sns-seconds 600
.venv/bin/python run_tests.py --only d4a --wait-sns-seconds 600

# 4. Opt-in tests (only if explicitly approved by author):
#   --include-cloudtrail
#   --include-iam-access-key
#   --include-quota-exhaustion  (run LAST; exhausts smoke-test daily quota)
```

## Observation & Mailbox Correlation

1. **SNS delivery:** recorded automatically in `run-output/ledger-<run_id>.json` (`sns_messages`) with `sns_timestamp_utc`, `sqs_sent_at_utc`, `received_at_utc`, and parsed identifiers (`cloudtrail_event_id`, `alarm_name`, `state_change_time`).
2. **CloudWatch alarm state:** recorded in `alarm_transitions` (`StateUpdatedTimestamp` from `DescribeAlarmHistory`).
3. **Email arrival:** hand the steward the run's UTC window and correlating identifiers (`tessera-dtest-<run_id>-*`, CloudTrail `eventID`s, alarm names + `StateUpdatedTimestamp`) from the sanitized ledger; the steward reads the author's mailbox read-only and returns arrival timestamps + identifiers to record in `docs/reviews/detection-tests/RESULTS-<date>.md`.

## Cleanup Procedure & Crash Recovery

- Every test deletes its throwaway resources in `finally` blocks and updates `run-output/ledger-<run_id>.json`.
- **KMS keys** cannot be deleted immediately in AWS; they are scheduled with the 7-day minimum (`PendingWindowInDays=7`) and recorded as `scheduled, deletes on YYYY-MM-DD` (never `deleted`).
- If a run is interrupted mid-flight (e.g., `SIGKILL` or network drop), recover cleanly from the flushed ledger:

```bash
.venv/bin/python run_tests.py --cleanup-ledger run-output/ledger-<run_id>.json
```
