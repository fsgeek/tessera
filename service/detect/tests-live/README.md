# Tessera V1 Live Detection Tests (`service/detect/tests-live/`)

Live detection tests prepared from `docs/V1-DETECTION-CONTRACT.md` (D1–D4 as built), `docs/V1-CONTRACT.md` §4 and `docs/reviews/detection-tests/BRIEF-gemini.md` (r5), narrowed by the **steward removal pass** (2026-11-23, `docs/reviews/detection-tests/FIXES.md`). The test matrix and evidence classes are in [`docs/reviews/detection-tests/PLAN.md`](../../../docs/reviews/detection-tests/PLAN.md).

## Safety properties

1. **Production alarm topic is never called.** Nothing subscribes to, unsubscribes from, or reads the subscriptions of `tessera-v1-alarms`. Delivery evidence is read-only CloudWatch alarm history (API rows) plus the steward's mailbox read.
2. **No IAM, S3, CloudTrail-trail or Lambda resources.** Those clients are not available in `safety.py`.
3. **API binding.** `TESSERA_API` must be exactly `https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1`. No other host receives `TESSERA_SMOKE_KEY`. Proxies and redirects are refused.
4. **Run identity.** The runner generates the run ID (12 hex characters from uuid4); it cannot be supplied. Preflight (caller identity plus a tag search for the new ID) runs before any ledger file exists. If preflight refuses, no ledger is written.
5. **One run at a time.** An exclusive lock file `run-output/.lock` (O_CREAT|O_EXCL) is held for every live run and every recovery, and released in `finally`. Pacing (one limiter, ≤ 2 rps) and the smoke-key quota guard are **per process**, so concurrent runs are not supported. If a crash leaves the lock, confirm no run is active, then delete `run-output/.lock` by hand.
6. **Intent-before-create, tag-only recovery.** Every remaining resource is tagged `purpose=detection-test` and `run_id=<id>` in its create call, and is a type the us-east-2 Resource Groups Tagging API indexes. An intent is flushed before each create. A create rejected with a 4xx closes as `not_created`; any other create failure stays `unresolved`. Recovery finds resources only by tag search, re-verifies ownership on the service, deletes, and never closes an intent because a search missed it.
7. **Fail closed and redact.** Any residual, refused or failed item gives a non-zero exit. Output and ledgers hold resource names and class names only: no URLs, no account IDs inside ARNs, no exception text, no response bodies. Response headers are kept only when they match a strict pattern. If today's smoke-key access-log count cannot be read, smoke-key rows do not start.

## Tests that remain

- **`d7-kms`** (`D7-kms-policy`, `D7-kms-disable`, `D7-kms-delete`): throwaway key tagged at creation (no alias, no grant); `PutKeyPolicy`, `DisableKey`, `ScheduleKeyDeletion(7 days)`.
- **`d7-sns`** (`D7-sns-topic-attr`, `D7-sns-topic-delete`): throwaway topic; `SetTopicAttributes(Policy)`, `DeleteTopic`. No subscriptions.
- **`d7-apigw`** (`D7-apigw-key-create`, `D7-apigw-key-update`, `D7-apigw-plan-update`): disabled throwaway API key and usage plan; no REST API, no plan-key attachment.
- **`d7-sup`**: `d7-sup-sqs`, `d7-sup-ddb`, `d7-sup-cw`, `d7-sup-logs`, `d7-sup-eb`.
- **API**: `d2a` (+ `D1c`), `d2b`, `d3a`, `d4a`, and opt-in `d4c` (`--include-quota-exhaustion`, always last).

Removed (NOT COVERED in PLAN.md): `d3b`, `d7-s3`, `d7-cloudtrail`, `d7-lambda`, `d7-iam-role`, `d7-iam-access-key`, the production-topic observer, KMS grant, API Gateway plan-key, and throwaway-topic subscribe/unsubscribe.

## Setup and offline tests

```bash
cd service/detect/tests-live
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q          # offline: no AWS, no network, no boto3 needed
```

## Running

```bash
.venv/bin/python run_tests.py --dry-run --suite all     # no calls, no files
.venv/bin/python run_tests.py --suite d7
.venv/bin/python run_tests.py --suite d7-sup
.venv/bin/python run_tests.py --suite api                # needs TESSERA_API, TESSERA_SMOKE_KEY
.venv/bin/python run_tests.py --cleanup-ledger ledger-<run_id>.json   # recovery, inside run-output/
```

The runner waits the longest contract latency of the selected rows (10 or 15 min, or `--wait-seconds`) before reading CloudTrail and alarm history. Exit 0 means only that the script finished and cleaned up. Hand `steward_mailbox_handoff` from the ledger to the steward for the email check.

| Variable | Needed for | Purpose |
|---|---|---|
| `TESSERA_API` | API rows | Must equal the pinned deployed URL above |
| `TESSERA_SMOKE_KEY` | `d3a`, `d4a`, `d4c` | `smoke-test` key, supplied at run time |
| AWS session | all live rows | Short-lived session, `us-east-2` |
