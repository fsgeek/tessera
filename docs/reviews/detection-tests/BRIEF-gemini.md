# Brief: detection tests for Tessera V1 (for Gemini via `agy`; steward draft, 2026-11-22)

**Approved by the author for preparation (plan and test code, no AWS access), 2026-11-23; run by `agy` with
`gemini-4-neon-high`, AWS credentials unreachable.** Status: r4 (r2 answered the author's Codex review of r1; r3 added the mailbox endpoint and D1-D4 as built;
r4, 2026-11-23, answers the author's Codex review of r3). Preparing the test code is approved by this brief;
execution needs the author's separate approval and an AWS session.**

You are writing and running the tests that show Tessera's detections fire (gate item 3,
`service/issuer/DEPLOY.md` "Gate before any client beyond smoke-test"). Work **from the detection contract and the
threat model, not from the alarm code**: `docs/V1-DETECTION-CONTRACT.md` (for D1-D4 use its section "D1-D4 as
built", which supersedes the original rows), `docs/V1-CONTRACT.md` §4 (failure model).
Do not read `service/detect/infra/` or `service/watcher/` before your tests are written; you may read them afterwards
to explain a failure. A detection that has never been seen to fire is a claim, not a control. Codex reviews your tests
and results afterwards.

## Hard safety rules (any breach ends the run)
1. **Never modify, delete, disable or invoke-with-side-effects any production resource**: anything named
   `tessera-v1-*`, the KMS key `alias/tessera-v1-kms`, the CloudTrail trail, the results bucket, the request table,
   the issuer or signer functions, their queues, or the alarm topic, its policy and its existing subscription.
   Read-only calls on them are allowed. **One narrow exception:** you may add one test subscription (an SQS queue
   you created) to the alarm topic and must remove it at the end; you may not change the topic's policy or any
   existing subscription. If your delivery method would need a topic-policy change, stop and report it instead.
2. Fire each detection with **throwaway resources** you create for the test, named `tessera-dtest-<run id>-*`, tagged
   `purpose=detection-test`, in **us-east-2 only** (the organization SCP denies other regions). Delete every one at the
   end, and list what you created and deleted. A KMS key you create is scheduled for deletion with the minimum window.
3. The API may be exercised only through API Gateway with the `smoke-test` key, which the author provides at run
   time, and only for: read-only GETs, and POSTs designed to be refused (oversized, malformed). No request that would
   be accepted for issuance. **Narrow exception for D2:** `GET /v1/requests/{key}` (the status route) for random
   request-key UUIDs, sent with no API key or with a random invalid key, within rule 4's rate.
4. No flood above the usage plan's rate (5 rps, burst 20); a throttling test uses short bursts, under one minute. If
   reaching a detection's threshold (for example D1's 50 `THROTTLED` lines) would require exceeding this rule, that
   detection is NOT COVERED; the desired result is never permission to exceed it. Note that every smoke-test request
   counts toward its daily quota (100) and its D4 volume alarm (50); plan for both.
5. No credentials, keys or URLs in your output files. The author supplies the API endpoint and the smoke-test key at
   run time as environment variables (`TESSERA_API`, `TESSERA_SMOKE_KEY`); write them nowhere.
6. Cleanup: list every resource created and its deletion. A KMS key can only be *scheduled* for deletion (minimum 7
   days): report it as "scheduled, deletes on <date>", not as deleted.

## What to show, per detection
**Write a test plan first**, before any test code, one row per *promised* detection in the contract (D1–D10, each
listed event or threshold within it): the promise in the contract's words; the triggering action and the event count
or threshold needed to cross it; the observation endpoint; the contract's latency; and exactly what a pass would
establish. Checks beyond the contract's named cases may be added but never substitute for a promised one.

**Latency standard per endpoint.** The contract has two: its original table states event-to-email, and its "D1-D4
as built" section states event-to-alarm-state. For each row the plan names which applies to which endpoint: alarm
state (from the alarm's CloudWatch history, `StateUpdatedTimestamp`), SNS receipt, and email arrival. Never pick one
silently. **Correlate by identifiers**, not by subject and time alone: the CloudTrail event id (present in D7 and
watcher message bodies), the alarm name and state-change time, the throwaway resource's name.

**Two observation endpoints, recorded separately.** (a) *SNS delivery*: your test SQS subscription's receive time
establishes delivery through SNS only. (b) *Email*: the contract's latency is event-to-email; use the email's arrival
time. The steward reads the alarm messages' arrival times from the author's mailbox (read-only) and gives them to
  you after each test, with the identifiers above (CloudTrail event id, alarm name and state-change time, resource
  name) as well as event time and subject; you do not need mailbox access and the author forwards nothing.

**Three evidence classes, never merged.** For each promised detection report exactly one:
- **PRODUCTION PATH**: the triggering event occurred on the production resource or production request path (only
  possible within rule 3, e.g. D1–D4 through the API).
- **EQUIVALENT BY SCOPE**: fired with a throwaway resource, *and* (after your tests are written) you read the deployed
  rule *and every later stage of its processing and notification path* (any input transformer, the watcher's
  filters, permissions on the path) and confirm that none filters by resource or behaves differently for the
  production resource, so the same event on it would take the same deployed path to the same notification. State
  each filter checked. This is never reported as if the production resource had been exercised.
- **NOT COVERED**: not testable within the rules (with the reason), or fired only on a throwaway resource whose rule
  *does* filter by resource.
Each row also gets FIRED / DID NOT FIRE, measured latencies (SNS, email) against the contract, and the run time.
**A NOT COVERED or DID NOT FIRE row leaves that part of the gate open.** Do not summarize partial coverage as "the
detection gate passed"; the report states which promised detections remain open.

Candidate actions, to be mapped onto the plan's rows (not a substitute for it):
- **D7** (EventBridge, us-east-2) on throwaway resources: KMS (create key, put key policy, schedule deletion), S3
  (create bucket, put bucket policy, delete), SNS, SQS, DynamoDB (update TTL), CloudWatch (put/delete alarm), Logs
  (put retention), EventBridge (put/delete rule), Lambda (add permission, update configuration), API Gateway
  (throwaway REST API and key). CloudTrail: NOT COVERED unless a throwaway trail can be changed without touching the
  production trail.
- **D7 IAM** (watcher): create a throwaway role, attach and detach an inline policy, delete it.
- **D1–D4**: throttling burst within rule 4; missing and invalid keys; oversized and malformed POSTs with the
  smoke-test key; per-key volume against the invitation record.
- **D10**: Lambda `Errors` on production functions and the budget are likely NOT COVERED; say why.
- **D5, D6, D8, D9**: describe how each could be fired without breaking rule 1; most will be NOT COVERED against
  production and need a staging replay (state it; do not improvise).

## Output
`docs/reviews/detection-tests/PLAN.md` (before code) and `RESULTS-<date>.md`: the table with evidence class, the evidence, the cleanup list, and every deviation from
this brief. Your test code goes in `service/detect/tests-live/` with a README stating how to rerun it.
