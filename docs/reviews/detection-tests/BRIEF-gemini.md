# Brief: detection tests for Tessera V1 (for Gemini via `agy`; steward draft, 2026-11-22)

**Status: DRAFT r2 (after the author's Codex review, 2026-11-22). Preparing the test code is approved by this brief;
execution needs the author's separate approval and an AWS session.**

You are writing and running the tests that show Tessera's detections fire (gate item 3,
`service/issuer/DEPLOY.md` "Gate before any client beyond smoke-test"). Work **from the detection contract and the
threat model, not from the alarm code**: `docs/V1-DETECTION-CONTRACT.md`, `docs/V1-CONTRACT.md` §4 (failure model).
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
   be accepted for issuance.
4. No flood above the usage plan's rate (5 rps, burst 20); a throttling test uses short bursts, under one minute.
5. No credentials, keys or URLs in your output files. The author supplies the API endpoint and the smoke-test key at
   run time as environment variables (`TESSERA_API`, `TESSERA_SMOKE_KEY`); write them nowhere.
6. Cleanup: list every resource created and its deletion. A KMS key can only be *scheduled* for deletion (minimum 7
   days): report it as "scheduled, deletes on <date>", not as deleted.

## What to show, per detection
**Write a test plan first**, before any test code, one row per *promised* detection in the contract (D1–D10, each
listed event or threshold within it): the promise in the contract's words; the triggering action and the event count
or threshold needed to cross it; the observation endpoint; the contract's latency; and exactly what a pass would
establish. Checks beyond the contract's named cases may be added but never substitute for a promised one.

**Two observation endpoints, recorded separately.** (a) *SNS delivery*: your test SQS subscription's receive time
establishes delivery through SNS only. (b) *Email*: the contract's latency is event-to-email; use the email's arrival
time from its headers (the author forwards the messages; the forwarding time is not the arrival time).

**Three evidence classes, never merged.** For each promised detection report exactly one:
- **PRODUCTION PATH**: the triggering event occurred on the production resource or production request path (only
  possible within rule 3, e.g. D1–D4 through the API).
- **EQUIVALENT BY SCOPE**: fired with a throwaway resource, *and* (after your tests are written) you read the deployed
  rule or code and confirm it does not filter by resource, so the same event on the production resource matches.
  State the rule and the evidence that it is unfiltered.
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
