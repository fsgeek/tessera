# V1 detection contract (DRAFT, steward, 2026-11-19)

Item 1 of the gate before any client beyond `smoke-test` (`service/issuer/DEPLOY.md:86-116`). For each attack or
fault: what it must leave, where, which alarm fires, how fast, and who is told. The detection tests (item 3) are
written from this document and the threat model by another model family, not from the alarm code. A detection that
has never been seen to fire is a claim, not a control.

Status of facts: from a survey of the code, Terraform and applied state on 2026-11-19. Platform behaviour (AWS,
GCP) is marked *(platform)* and is what the tests must confirm, not assume.

## Who is told
Every alarm publishes to one SNS topic, `tessera-v1-alarms`, with an email subscription to the author (address a
Terraform variable, not in the repository). The watcher also writes each finding to its own log and to a durable
outbox it republishes from until SNS accepts it; a finding that can be neither queued nor published stops the run's
commit, so the next run finds it again if its source remains. Delivery is promised to the topic; the email
additionally needs the author's confirmed subscription. The steward is not running continuously; **the author's email
is the only real-time path**, and the contract promises nothing faster.

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

**(b) Independent watcher**: a separate Lambda, own read-only role on the issuer's stores (read `REQ#`/`SIGLOG#`,
results bucket, trail bucket; write only its own state and trace buckets, its log, the heartbeat metric and the alarm
topic), every 10 minutes. It shares no code with the issuer beyond the frozen relying-party verifier. Each run it:
1. re-verifies every newly completed receipt as a relying party would (the smoke test's `rp_verify.py`), and checks
   that the receipt's content and signatures are its own request's;
2. reconciles signatures: for slot 1, CloudTrail `kms:Sign` events on `alias/tessera-v1-kms` against the signatures
   the issuer verified and used, by time and count, one-to-one in time order within the delivery lag; for slot 2, the
   same against GCP `useToSign` records once G4 is closed;
3. writes trace records for newly terminal requests;
4. publishes a heartbeat metric.

**What "independent" means here, stated:** resource separation, not the integrity of issuer-controlled
observations. No issuer role can write the watcher's buckets, and the watcher cannot write the issuer's. But `REQ#`
and `SIGLOG#` are the issuer's own records: a principal able to write the issuer table can suppress D5 and D8 for the
rows it deletes or alters before the watcher reads them, and can write `used` entries for Signs it caused through the
KMS request queue. CloudTrail is the independent evidence: a deleted or never-written `SIGLOG#` `used` entry (with no
other `used` entry of that digest) still leaves its `kms:Sign`, which surfaces as an unmatched Sign under D6; a deleted
or altered COMPLETE row whose `used` entries remain does not (it suppresses D8 and the trace record).

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
| D5 | Signer refusals only an attacker or a fault produces | `SIGLOG#` (both slots' responses; the watcher's path); KMS signer log `refused`; GCP stdout `response`, `refuse_to_run` | any one of: `KEY_FP_MISMATCH`, `FRAME_DIGEST_MISMATCH`, `ALG_NOT_ALLOWED`, `DECLARED_TIME_OUTSIDE_EPSILON`, `BAD_REQUEST`, `TRUNCATED`, `UNRECOGNIZED_REASON`; poller dispositions `unrequested` (E-06), `malformed`, `bad-signature` (watcher, from `SIGLOG#`); KMS signer startup `KeyMismatch` (no response: the shared Lambda `Errors` alarm only); a refusal logged only by a signer, and GCP `refuse_to_run` with no response (log-based alert, not built) | 20 min |
| D6 | A signature the issuer did not verify and use | watcher reconciliation (slot 1: CloudTrail `kms:Sign` events against the signatures the issuer verified and used, by time and count; slot 2: GCP Data Access) | any `kms:Sign`/`useToSign` no such signature accounts for; any `kms:Sign` by a principal other than the signer role, or any `AccessDenied` on the key recorded in the issuing account's trail (one made from another account is logged only there) | 1 h (CloudTrail delivery lag *(platform)*) |
| D7 | Control-plane tampering | CloudTrail management write events via EventBridge in us-east-2; **IAM events reach EventBridge only in us-east-1, which the organization's SCP closes to this account, so IAM changes are read by the watcher from the multi-region trail (latency up to ~1 h)**; GCP Admin Activity audit log (always on *(platform)*) | any of: `PutKeyPolicy`, `CreateGrant`, `DisableKey`, `ScheduleKeyDeletion` on the v1 key; `StopLogging`, `DeleteTrail`, `UpdateTrail`, `PutEventSelectors`; IAM changes to the issuer, signer or watcher roles, `CreateAccessKey`; `UpdateFunctionCode`/`Configuration` on the issuer, signer or watcher; trail-bucket policy or lock changes; API key or usage-plan changes; SNS alarm-topic or subscription changes; GCP: KMS IAM policy, key version state, Cloud Run job update | 10 min (IAM, via the watcher: up to ~1 h) |
| D8 | A receipt that does not verify, or is not its request's | watcher step 1 | any verdict other than `VALID_STRICT`; a receipt whose content or signatures are not its record's (compared where the record holds them); a missing or unreadable receipt object | 20 min (a check that cannot be made, or one deferred behind a backlog: `RECEIPT_UNCHECKED` within 6 h) |
| D9 | Watcher silent or dead (sustained) | heartbeat metric | no heartbeat in three consecutive 10-minute periods (`FILL` to 0; missing data = breaching) | 40 min after the last heartbeat with metrics ingested on time, plus CloudWatch evaluation *(platform)* |
| D10 | Service fault | Lambda `Errors` (API, poller, KMS signer); requests non-terminal past their bound; AWS and GCP budgets | any Lambda error; any request open > 24 h (until A12's L_term is live); spend above 50% of the monthly budget | 1 h |

Thresholds are initial values, chosen so a test can cross them; they are tuned on the record, not silently.

## D1-D4 as built (2026-11-23; `service/detect/infra/access.tf`; review `docs/reviews/access-alarms/`)
These supersede the D1-D4 rows above where they differ. Latencies are event to alarm state (one evaluation period
plus CloudWatch's evaluation delay); event-to-email is what the item-3 tests measure.
- **D1** 50+ `THROTTLED` log lines in 5 min. API Gateway may omit log lines for excessive 429s, so a backstop alarms on
  the API's own metrics: 300+ requests or 50+ 4XX responses in 5 min.
- **D2** 50+ `INVALID_API_KEY` or `MISSING_AUTHENTICATION_TOKEN` in 5 min: missing or invalid keys **or unknown
  routes** (the log cannot tell which key a caller sent).
- **D3** 5+ logged 400/413 in 1 h from one invited key; any logged 400/413 from a key not in the invitation record.
  Gateway-level 413/431 rejections may not be logged (the 4XX backstop counts them).
- **D4** each invited key's logged requests per day above its invited volume; any logged success from a key not in
  the invitation record; any observed `QUOTA_EXCEEDED` (the usage-plan quota is best-effort).
- **The invitation record** is the `invitations` map in `access.tf` (key id, name, expected daily volume), kept in step
  with the issuer's `client_names`. A key added to the issuer but not to the map fails loudly (D4 unknown-key success).
- Filter patterns were tested with `aws logs test-metric-filter`: against 58 real access-log lines (no false match;
  the pilot volume filter matched exactly its 20 lines) and against synthetic lines in the exact logged format for
  each event (each matched only its own). That shows matching, not emission or delivery.

## Deployed (2026-11-23)
- **Watcher deployed** (`service/watcher/`, DEPLOY-RUN 2026-11-22/23), pinned, `CodeSha256` = `watcher.zip` `5cdd50c5…`.
  First run of the deployable package (00:07Z): 8 receipts re-verified (no D8 finding), 8 trace records written,
  heartbeat sent; 2 D7 IAM findings, both the deployment's own IAM writes. Heartbeat alarm returned to OK at 00:12Z.
  This is operation, not the gate's item 3: no detection is "seen to fire" until another family's tests show it.

## Status (2026-11-22)
- **G1 deployed** (structured logs; `service/issuer/LOGGING.md`; DEPLOY-RUN 2026-11-22). First `poll_summary` line seen in production.
- **Step 2 deployed** (`service/detect/infra/`): topic `tessera-v1-alarms` (us-east-2) with the author's email
  subscription (pending the author's confirmation), D7 EventBridge rules for KMS, CloudTrail, S3, API Gateway, SNS,
  EventBridge, CloudWatch, Logs, SQS, DynamoDB and Lambda, D10 Lambda `Errors` alarms and a $10 monthly budget
  (50% actual, 100% forecast). Not yet deployed: D1-D6, D7 IAM, D8, D9 (D5, D6 slot 1, D7 IAM, D8 and D9 are built,
  below), GCP-side alarms. None is "seen to fire" until item 3's tests.
- **Step 4, watcher: built, not deployed** (`service/watcher/`, `service/detect/infra/watcher.tf`): D5 from `SIGLOG#`,
  D6 slot 1 (CloudTrail `kms:Sign` reconciled by time and count against the kms signatures the issuer verified and
  used; foreign principal; `AccessDenied` in this account's trail), D7 IAM writes from the trail, D8 (stored bytes
  against `receipt_sha256`, the frozen verifier as a relying party, and the receipt bound to its record), D9 heartbeat
  alarm (sustained silence), trace records 0(a) under Object Lock COMPLIANCE until not-after + 400 days, one per
  terminal request. Owner's unit tests only. Codex review and its dispositions:
  `docs/reviews/watcher/CODEX-REVIEW.md`, `docs/reviews/watcher/DISPOSITION.md`. **D6 slot 2 (GCP `useToSign`) is a
  TODO** until G4. Latencies and limits: `service/watcher/README.md`.

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
