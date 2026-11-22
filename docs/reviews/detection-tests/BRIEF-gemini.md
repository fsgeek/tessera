# Brief: detection tests for Tessera V1 (for Gemini via `agy`; steward draft, 2026-11-22)

**Status: DRAFT for the author's approval. Nothing here runs until the author approves it and starts an AWS session.**

You are writing and running the tests that show Tessera's detections fire (gate item 3,
`service/issuer/DEPLOY.md` "Gate before any client beyond smoke-test"). Work **from the detection contract and the
threat model, not from the alarm code**: `docs/V1-DETECTION-CONTRACT.md`, `docs/V1-CONTRACT.md` §4 (failure model).
Do not read `service/detect/infra/` or `service/watcher/` before your tests are written; you may read them afterwards
to explain a failure. A detection that has never been seen to fire is a claim, not a control. Codex reviews your tests
and results afterwards.

## Hard safety rules (any breach ends the run)
1. **Never modify, delete, disable or invoke-with-side-effects any production resource**: anything named
   `tessera-v1-*`, the KMS key `alias/tessera-v1-kms`, the CloudTrail trail, the results bucket, the request table,
   the issuer or signer functions, their queues, or the alarm topic and its subscription. Read-only calls on them are
   allowed.
2. Fire each detection with **throwaway resources** you create for the test, named `tessera-dtest-<run id>-*`, tagged
   `purpose=detection-test`, in **us-east-2 only** (the organization SCP denies other regions). Delete every one at the
   end, and list what you created and deleted. A KMS key you create is scheduled for deletion with the minimum window.
3. The API may be exercised only through API Gateway with the `smoke-test` key, which the author provides at run
   time, and only for: read-only GETs, and POSTs designed to be refused (oversized, malformed). No request that would
   be accepted for issuance.
4. No flood above the usage plan's rate (5 rps, burst 20); a throttling test uses short bursts, under one minute.
5. No credentials, keys or URLs in your output files.

## What to show, per detection
For each: what you did (exact API calls), the time, the alarm email or SNS message you observed (subject, time; the
author forwards the emails or you read a test subscription you created on a throwaway SQS queue subscribed to the
alarm topic — subscribing is allowed; unsubscribe at the end), and the measured latency against the contract's
"fires within". Report FIRED / DID NOT FIRE / NOT TESTABLE (with reason) for each.
- **D7** (EventBridge, us-east-2): one event from each rule family on throwaway resources: KMS (create key,
  put key policy, schedule deletion), S3 (create bucket, put bucket policy, delete bucket), SNS (create topic, set
  attributes, delete), SQS, DynamoDB (create, update TTL, delete table), CloudWatch (put and delete an alarm), Logs
  (create group, put retention, delete), EventBridge (put and delete a rule), Lambda (create function, add
  permission, update configuration, delete), API Gateway (create and delete a throwaway REST API and key).
  CloudTrail: NOT TESTABLE unless a throwaway trail can be created and changed without touching the production trail.
- **D7 IAM** (watcher, once deployed): create a throwaway role, attach and detach an inline policy, delete it.
- **D10**: Lambda `Errors` on a production function is NOT TESTABLE under rule 1 unless a refused API request makes
  the API function raise; find out from the contract, do not force it. Budget: NOT TESTABLE.
- **D1–D4** (once deployed): throttling burst; missing and invalid keys; oversized and malformed POSTs with the
  smoke-test key; per-key volume against the invitation record.
- **D5, D6, D8, D9** (once the watcher is deployed): describe how each could be fired without rule 1's resources; most
  will be NOT TESTABLE against production and need the watcher's staging replay (state it; do not improvise).

## Output
`docs/reviews/detection-tests/RESULTS-<date>.md`: the table, the evidence, the cleanup list, and every deviation from
this brief. Your test code goes in `service/detect/tests-live/` with a README stating how to rerun it.
