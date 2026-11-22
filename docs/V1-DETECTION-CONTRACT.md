# V1 detection contract (DRAFT, steward, 2026-11-19)

Item 1 of the gate before any client beyond `smoke-test` (`service/issuer/DEPLOY.md:86-116`). For each attack or
fault: what it must leave, where, which alarm fires, how fast, and who is told. The detection tests (item 3) are
written from this document and the threat model by another model family, not from the alarm code. A detection that
has never been seen to fire is a claim, not a control.

Status of facts: from a survey of the code, Terraform and applied state on 2026-11-19. Platform behaviour (AWS,
GCP) is marked *(platform)* and is what the tests must confirm, not assume.

## Who is told
Every alarm publishes to one SNS topic, `tessera-v1-alarms`, with an email subscription to the author (address a
Terraform variable, not in the repository). The watcher also writes each finding to its own log. The steward is not
running continuously; **the author's email is the only real-time path**, and the contract promises nothing faster.

## What exists today (gaps the build must close)
- **G1** The issuer API and poller Lambdas emit no application log lines; poller notes and `poll()` summaries are
  discarded (`service.py:51-54`, `pipeline.py:176-187`). Signer-response dispositions (`unrequested` = E-06,
  `malformed`, `bad-signature`, ...) exist only as `SIGLOG#` items in DynamoDB.
- **G2** The CloudTrail trail is management-events only, not delivered to CloudWatch Logs. `kms:Sign` is a
  management read event. Nothing reads the trail.
- **G3** No alarm, metric filter, budget or notification topic exists anywhere.
- **G4** GCP: Cloud KMS Data Access logs (`useToSign`) are off; `_Default` keeps 30 days *(platform)*. Slot 2 has
  no counterpart to `kms:Sign` records.
- **G5** No record joins the stores. `REQ#` and the receipt object expire 30 days after a request ends; the
  CloudTrail `kms:Sign` events can be joined to signatures only by time and count.

## The Arariwa (item 0)
**(a) Trace record**, one per request that reaches a terminal state, written by the watcher, never by the issuer:
credential digest and API key id, request id and SHA-256 of the request key, content SHA-256 and length, state and
reason, each attempt id with its jobs (slot, signer request id, frame SHA-256, signature SHA-256), the matched
CloudTrail `kms:Sign` event ids (by the reconciliation rule below), anchor heights, receipt SHA-256, verification
verdict. Stored in an S3 bucket with Object Lock COMPLIANCE until the window's not-after + 400 days. This is the
accounting ledger: "who requested this receipt, and was it ours?" remains answerable after 30 days.

**(b) Independent watcher**: a separate Lambda, own read-only role (read `REQ#`/`SIGLOG#`, results bucket, trail
bucket; write only its trace bucket, its log and the alarm topic), every 10 minutes. It shares no code with the
issuer beyond the frozen relying-party verifier. Each run it:
1. re-verifies every newly completed receipt as a relying party would (the smoke test's `rp_verify.py`);
2. reconciles signatures: for slot 1, every CloudTrail `kms:Sign` on `alias/tessera-v1-kms` against signed jobs,
   matched one-to-one in time order within the delivery lag; for slot 2, the same against GCP `useToSign` records
   once G4 is closed;
3. writes trace records for newly terminal requests;
4. publishes a heartbeat metric.

**Limitation, stated:** the watcher runs in the same AWS account as the issuer. An attacker holding that account's
administrator can silence it; D7 makes that noisy, and D9 makes silence itself an alarm, but neither defeats a
careful administrator-level attacker. That is the operational-posture gate's subject, not this one's.

## Detections
Latency is from the event to the email. "Seen to fire" means the item-3 test performed the event on the deployment
and observed the email.

| Id | Attack or fault | Evidence (where) | Alarm | Fires within |
|---|---|---|---|---|
| D1 | Flood; throttling | access log, 429 `THROTTLED` | metric filter; ≥ 50 in 5 min | 10 min |
| D2 | Missing or guessed API keys | access log, 403 `INVALID_API_KEY` / `MISSING_AUTHENTICATION_TOKEN` *(platform)* | metric filter; ≥ 50 in 5 min (the URL is public; scanners are background) | 10 min |
| D3 | Oversized or malformed requests from a valid key | access log 400/413 with non-empty `apiKeyId`; `REQ#` REFUSED `TOO_LARGE` | ≥ 5 in 1 h from any one key | 15 min |
| D4 | Per-key volume; unknown key | access log by `apiKeyId`; invitation record (`config/invitations.json`: who, key id, when, terms, expected volume) | any key above its invited daily volume (yanantin-pilot: 5); any 2xx from a key id not in the invitation record; any `QUOTA_EXCEEDED` | 15 min |
| D5 | Signer refusals only an attacker or a fault produces | `SIGLOG#` (both slots' responses); KMS signer log `refused`; GCP stdout `response`, `refuse_to_run` | any one of: `KEY_FP_MISMATCH`, `FRAME_DIGEST_MISMATCH`, `ALG_NOT_ALLOWED`, `DECLARED_TIME_OUTSIDE_EPSILON`, `BAD_REQUEST`, `TRUNCATED`, `UNRECOGNIZED_REASON`; poller dispositions `unrequested` (E-06), `malformed`, `bad-signature`; KMS signer startup `KeyMismatch` (Lambda Errors); GCP `refuse_to_run` (log-based alert) | 20 min |
| D6 | A signature no receipt accounts for | watcher reconciliation (slot 1: CloudTrail; slot 2: GCP Data Access) | any unmatched `kms:Sign`/`useToSign`; any `kms:Sign` by a principal other than the signer role, or any `AccessDenied` on the key | 1 h (CloudTrail delivery lag *(platform)*) |
| D7 | Control-plane tampering | CloudTrail management write events via EventBridge in us-east-2; **IAM events reach EventBridge only in us-east-1, which the organization's SCP closes to this account, so IAM changes are read by the watcher from the multi-region trail (latency up to ~1 h)**; GCP Admin Activity audit log (always on *(platform)*) | any of: `PutKeyPolicy`, `CreateGrant`, `DisableKey`, `ScheduleKeyDeletion` on the v1 key; `StopLogging`, `DeleteTrail`, `UpdateTrail`, `PutEventSelectors`; IAM changes to the issuer, signer or watcher roles, `CreateAccessKey`; `UpdateFunctionCode`/`Configuration` on the issuer, signer or watcher; trail-bucket policy or lock changes; API key or usage-plan changes; SNS alarm-topic or subscription changes; GCP: KMS IAM policy, key version state, Cloud Run job update | 10 min |
| D8 | A receipt that does not verify | watcher step 1 | any verdict other than `VALID_STRICT` | 20 min |
| D9 | Watcher silent or dead | heartbeat metric | missing for 30 min (missing data = breaching) | 40 min |
| D10 | Service fault | Lambda `Errors` (API, poller, KMS signer); requests non-terminal past their bound; AWS and GCP budgets | any Lambda error; any request open > 24 h (until A12's L_term is live); spend above 50% of the monthly budget | 1 h |

Thresholds are initial values, chosen so a test can cross them; they are tuned on the record, not silently.

## Status (2026-11-22)
- **G1 deployed** (structured logs; `service/issuer/LOGGING.md`; DEPLOY-RUN 2026-11-22). First `poll_summary` line seen in production.
- **Step 2 deployed** (`service/detect/infra/`): topic `tessera-v1-alarms` (us-east-2) with the author's email
  subscription (pending the author's confirmation), D7 EventBridge rules for KMS, CloudTrail, S3, API Gateway, SNS,
  EventBridge, CloudWatch, Logs, SQS, DynamoDB and Lambda, D10 Lambda `Errors` alarms and a $10 monthly budget
  (50% actual, 100% forecast). Not yet: D7 IAM (watcher), D9, D1-D6, D8, GCP-side alarms. None is "seen to fire"
  until item 3's tests.

## The build, in order
1. G1: structured log lines from the API (one per request, with key id, rid, outcome) and the poller (one per state
   transition and per `SIGLOG#` disposition). Needs tests across both signer suites, not the issuer's alone.
2. G3 + D7 + D9 + D10: topic, EventBridge rules (us-east-2 and us-east-1), budgets. Smallest, highest value.
3. Access-log metric filters: D1–D4; invitation record.
4. Watcher: D5 (from `SIGLOG#`), D6, D8, trace records. G4 enabled on GCP for slot 2.
5. Item 3: the tests, by Gemini (`agy`), from this document; Codex reviews tests and results.

## Not covered (stated)
DNS + git capture of the window record, and a requester inside the issuing account (A12 prechecks 1, 3). Content
semantics: Tessera attests what was presented, not whether it is true.
