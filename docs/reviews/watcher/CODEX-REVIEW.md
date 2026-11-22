# Codex review of the Arariwa watcher

## HIGH

### H1. A missing receipt aborts the run before any finding is published

`service/detect/infra/watcher.tf:232`, `service/watcher/tessera_watch/stores.py:15`, `service/watcher/tessera_watch/stores.py:53`, `service/watcher/tessera_watch/watcher.py:146`, `service/watcher/tessera_watch/watcher.py:320`

A COMPLETE row names an object that was never stored or has been deleted. The watcher has GetObject and lacks ListBucket on the results bucket, so S3 returns 403 for the absent object. The adapter rethrows it and the run exits before D8, before publishing even unrelated D5/D6/D7 findings already in memory, and before saving state or sending a heartbeat. The next invocation encounters the same row. D9 and the Lambda Errors alarm can signal the stalled watcher while the receipt fault itself stays unreported. The fake-backed missing-object test at `service/watcher/tests/test_d8.py:98` misses this permission interaction. README:26 and contract Status:78 overstate coverage. [S3 GetObject permissions](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)

### H2. An issuer runtime principal controls inputs that can suppress detection and become locked evidence

`service/issuer/infra/main.tf:192`, `service/issuer/infra/main.tf:239`, `service/issuer/infra/main.tf:262`, `service/watcher/tessera_watch/watcher.py:199`, `service/watcher/tessera_watch/watcher.py:268`

The watcher policy grants read access to issuer stores and write access to its own state and trace prefixes, log group, alarm topic and heartbeat namespace (`service/detect/infra/watcher.tf:224`). The checked-in API, poller and KMS signer role policies grant no direct watcher bucket writes. The poller can nevertheless remove an unseen SIGLOG or COMPLETE row before the next scan. It can also change the trace inputs or provide a terminal timestamp far ahead of the current clock. The watcher uses that timestamp as a watermark even if the record later expires. Subsequent genuine terminals below the floor receive neither D8 nor a trace, while successful runs continue to heartbeat. The Arariwa independence claim at contract:36–43 and README:3 needs to distinguish resource separation from the integrity and completeness of issuer-controlled observations.

### H3. D6 lets unverified or unshipped signatures satisfy the count

`service/watcher/tessera_watch/watcher.py:223`, `service/watcher/tessera_watch/watcher.py:243`, `service/issuer/tessera_issue/pipeline.py:549`, `service/issuer/tessera_issue/pipeline.py:563`, `service/issuer/tessera_issue/pipeline.py:584`, `service/issuer/infra/main.tf:262`

A response for a known KMS job that already holds a signature takes the duplicate path before signature validation. Its distinct signature digest counts as one signature for D6, even if the response bytes are invalid. An unmatched Sign in that interval can therefore disappear from the unmatched count. A genuine signed job followed by a failed attempt and no shipped receipt likewise satisfies D6. The poller can submit signing work through the queue and write SIGLOG directly. The time-and-count limit is disclosed at README:42–49, but contract:61 names a signature unaccounted for by a receipt, while contract:40 and Status:77 describe signed-job/KMS-signature reconciliation. These are different coverage claims. The observed count establishes neither receipt accounting nor a verified signature for each counted response.

### H4. Output field selection fails to enforce the secrecy boundary

`service/watcher/tessera_watch/watcher.py:208`, `service/watcher/tessera_watch/watcher.py:217`, `service/watcher/tessera_watch/watcher.py:355`, `service/watcher/tessera_watch/watcher.py:383`, `service/watcher/tessera_watch/lambda_app.py:60`

A bad issuer write can place a URL, plaintext request key, request content or API key value in a field such as SIGLOG reason. The watcher copies it into a D5 finding whenever the disposition triggers, so both the log and SNS receive the raw value. A free-form terminal reason similarly lands in COMPLIANCE storage. Hashing the designated request-key field and selecting nominally bounded fields do not validate their values. SDK and other unexpected exceptions also escape the handler, leaving Lambda to log exception text. A failed GetObject on a malformed issuer-supplied object path can expose that path in an SDK error. The CloudTrail decompression wrapper at `service/watcher/tessera_watch/cloudtrail.py:72` and verifier wrapper at `service/watcher/tessera_watch/receipts.py:152` do bound the errors they catch. README:67 and :96–97 make a broader claim.

## MEDIUM

### M1. Late CloudTrail delivery leaves irreversible time-order matches

`service/watcher/tessera_watch/watcher.py:243`, `service/watcher/tessera_watch/watcher.py:258`, `service/watcher/tessera_watch/watcher.py:304`

A signature logged at 12:30 initially takes a 12:20 Sign. A signature logged at 12:55 can also take 12:20, but cannot take 12:00. If the 12:00 Sign reaches S3 later, the prescribed time order pairs 12:00 with the first signature and 12:20 with the second. The persisted early match prevents that reassignment. D6 can report two unmatched items where the final evidence permits two matches, and the first trace can already be locked with the wrong event ID under the documented rule. A Sign missing at the 45-minute cutoff can also appear after its trace has been finalized. At bootstrap, the missing-signature branch suppresses alarms for signatures logged up to 40 minutes after coverage starts, since it compares the earliest possible Sign time to the coverage start. A signature logged 10 minutes into the coverage window with no Sign therefore gets only a before-coverage trace disposition, beyond the exclusion stated at README:91–93. README:46–49 describes the final time order without the delivery-order dependency.

### M2. Cursor and discovery windows can discard unseen or unpublished evidence

`service/watcher/tessera_watch/watcher.py:138`, `service/watcher/tessera_watch/watcher.py:164`, `service/watcher/tessera_watch/watcher.py:199`, `service/watcher/tessera_watch/watcher.py:268`, `service/watcher/tessera_watch/cloudtrail.py:39`, `service/watcher/tessera_watch/cloudtrail.py:55`

Both adapters follow their continuation keys, and CloudTrail listing enumerates region prefixes rather than filtering for the provider region. The completeness problem is across runs. If the first run discovers an IAM event in a file near the oldest edge of its 24-hour window and dies before its first save, the next run constructs a fresh coverage window. The file can already have aged out before that retry. The same loss can occur with an existing cursor if an SNS outage or repeated crash lasts until an uncommitted file ages out. A file's timestamp is its delivery minute, so late event delivery and an outage that ages out a delivered file are distinct cases. In DynamoDB, a terminal or SIGLOG write that appears more than an hour behind the watermark is skipped forever, even on a later scan that can see it. A poller stall between timestamp selection and commit, or a clock fault, can produce that ordering. README:70–78's “never skips” and loss-free replay claims exceed these bounds. [CloudTrail log file names](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-examples.html)

### M3. Findings lack durable delivery independent of verification, tracing and other findings

`service/watcher/tessera_watch/watcher.py:146`, `service/watcher/tessera_watch/watcher.py:294`, `service/watcher/tessera_watch/watcher.py:304`, `service/watcher/tessera_watch/stores.py:119`, `service/detect/infra/main.tf:57`

A trace PUT failure after D8 has found corrupt bytes prevents SNS publication of that finding and all others in the batch. If the trace write succeeds and Lambda dies before publication or state save, the trace survives but the finding exists only in memory. Replay can change the observed condition or lose the source entirely. For example, an explorer disagreement can resolve before retry, so the original W finding never reaches SNS. During publication, a failed first publish stops subsequent publishes. A persistent bad message or SNS rejection repeats the same failure every invocation. Publishing before cursor commit supports replay while inputs remain accessible, but provides no durable evidence of each finding awaiting publication. A successful SNS API call also leaves email dependent on subscription confirmation, which contract Status:71–72 records as pending. README:29–31 and :74–75 overstate delivery and replay.

### M4. D8 can run out of time before yielding a verdict or unavailable finding

`service/watcher/tessera_watch/watcher.py:287`, `service/watcher/tessera_watch/watcher.py:294`, `service/watcher/tessera_watch/receipts.py:64`, `service/watcher/tessera_watch/receipts.py:79`, `service/watcher/tessera_watch/receipts.py:142`, `service/watcher/tessera_watch/lambda_app.py:42`

The wrapper fetches all bundle-supplied heights before verifier validation, with two sequential requests per explorer per height and no total deadline. An invalid bundle with many distinct heights can spend the entire invocation on explorer work. Even ordinary verification can start with 120 seconds remaining while the subprocess timeout is 300 seconds, after the network calls. Lambda can kill the invocation before the wrapper returns W or before findings and pending progress are committed. Another COMPLETE row can also keep getting deferred behind a backlog despite a healthy heartbeat. A parsed layer with a header height decoded as infinity raises OverflowError during integer conversion and bypasses the unavailable handling. README:26, :36–39 and contract:63 overstate the check deadline or retry guarantee.

### M5. A terminal request can receive zero or incomplete trace records

`service/watcher/tessera_watch/stores.py:25`, `service/watcher/tessera_watch/watcher.py:268`, `service/watcher/tessera_watch/watcher.py:288`, `service/watcher/tessera_watch/watcher.py:348`, `service/watcher/tessera_watch/stores.py:109`

A strongly consistent paginated scan can read the relevant SIGLOG partition before the issuer logs a signature and a later page containing REQ after it commits COMPLETE. The job has a signature digest but the watcher has no associated SIGLOG in this pass. An empty match list leaves `waiting` false, allowing a trace to be locked without the expected Sign event ID even when that Sign is available. Another request can expire while pending, in which case the code reports TRACE_RECORD_LOST and marks it done without storing a trace. A missing or invalid terminal timestamp is dropped silently. The conditional create protects ordinary retries against duplicate writes under an existing current key, but provides no guarantee that every terminal gets a record. README:57–68 and contract Status:79 overstate the accounting coverage. [DynamoDB Scan consistency](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html)

### M6. Object Lock protects a version and the retention minimum moves with deployment inputs

`service/detect/infra/watcher.tf:6`, `service/detect/infra/watcher.tf:76`, `service/detect/infra/variables.tf:87`, `service/watcher/tessera_watch/stores.py:100`

The checked-in window plus the default 400 days yields 2028-03-07T00:00:00Z, and each ordinary PUT supplies COMPLIANCE, the explicit date, a checksum and If-None-Match. An override to 30 days changes both the writer and the enforcing policy together, permitting short retention despite contract:33. The policy's DateLessThan statement also does not independently require the date condition key to exist. The trace policy lacks a writer restriction or unconditional guard against delete markers and additional compliant versions. An issuer-side administrator, or a same-account principal independently granted those S3 operations, can hide the locked object behind a delete marker or put a different current version. A retry after a marker can create another version under the same key. The original version remains locked. The state bucket policy only denies insecure transport, so a separately authorized principal can also change the cursor. README:60 and :82–84 need to describe the current-key and version distinction. [S3 Object Lock and delete markers](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html)

### M7. Heartbeat measures sustained silence and has no demonstrated 40-minute bound

`service/detect/infra/watcher.tf:364`, `service/watcher/tessera_watch/watcher.py:152`, `service/detect/infra/variables.tf:14`

Sustained Lambda errors, timeouts, disabled scheduling and throttling all stop new heartbeats if no other invocation completes. Intermittent timeouts or throttles can coexist with enough successful invocations to avoid D9. A disabled schedule can also leave an already queued invocation that completes later. CloudWatch can use older real data from an evaluation range larger than the three configured periods, so three empty periods alone do not establish the stated alarm latency. The separate Errors alarm covers execution errors and timeouts under the default function list. D9 still cannot signal individual failures or an unchecked receipt when the run commits. README:27 and Terraform:362–363 need the sustained-silence and service-evaluation qualifications. [CloudWatch missing-data evaluation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarms-and-missing-data.html)

### M8. The deterministic archive test excludes the resolved dependencies and the install check

`service/watcher/package.py:50`, `service/watcher/package.py:66`, `service/watcher/package.py:87`, `service/watcher/tests/test_package.py:30`, `service/watcher/README.md:101`

The archive writer fixes order and timestamps for a given staged tree. Two builds can resolve different transitive wheels or select different artifacts because only the top-level version is pinned and wheel hashes are absent. The watcher includes the same verifier module tree and SHA-1DC detector as the issuer, but stages only the frozen catalog where the issuer copies the whole frozen objects tree (`service/issuer/package.py:85`). Current CLI use of the authenticated TEST catalog explains why that difference can pass the local receipt test. The install-facts path is aligned with the verifier's per-runtime checks, but the build accepts a stale Unicode module hash from another runtime and labels the zip deployable. The README also omits obtaining the runtime ARN from the bootstrap function that produced the facts, a step the issuer documents at `service/issuer/DEPLOY.md:51`. If the runtime changes between sampling and pinning, the rebuilt watcher can heartbeat while every D8 verifier invocation refuses startup. [uv dependency locking](https://docs.astral.sh/uv/pip/compile/)

### M9. A valid receipt can be locked into a trace for the wrong request

`service/watcher/tessera_watch/watcher.py:313`, `service/watcher/tessera_watch/watcher.py:345`, `docs/V1-DETECTION-CONTRACT.md:29`

A storage or assembly fault copies another request's valid receipt to this request's result path and records its matching digest. The verifier sees the valid bundle in isolation. The watcher then joins its verdict and receipt digest with this row's credential, content digest and signer-job data without checking that the verified commitments belong to those inputs. The trace can permanently say VALID_STRICT while misattributing who requested the receipt and which jobs produced it. This concerns the trace's accounting claim. The V1 verifier itself disclaims who submitted the bytes and whether a replayed receipt suits the transaction (`docs/V1-CONTRACT.md:39–43`).

## LOW

### L1. Scope and latency statements conflate several different detection paths

`docs/V1-DETECTION-CONTRACT.md:60`, `docs/V1-DETECTION-CONTRACT.md:62`, `docs/V1-DETECTION-CONTRACT.md:74`, `service/watcher/README.md:23`, `service/watcher/README.md:95`

A KMS signer startup KeyMismatch produces no SIGLOG response and relies on the shared Lambda Errors alarm. A signer refusal logged only by the signer and a GCP refuse_to_run with no response are outside the watcher’s D5 path. IAM latency is roughly an hour in the D7 evidence column and 10 minutes in its deadline column. Also, an AccessDenied on the v1 key from another AWS account is logged only in the caller's account, outside the watcher's issuing-account trail. “Any AccessDenied” needs that visibility qualification. README:95 implies the D1–D4 filters exist in the infra even though Status:74 and the checked-in resources do not establish them. [KMS CloudTrail coverage](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html)

## Owner prechecks

1. **Capture row — PASS.** `docs/V1-DETECTION-CONTRACT.md:90`, `service/watcher/README.md:33`, `docs/V1-CONTRACT.md:34`, `docs/V1-CONTRACT.md:65`. The checks concern observed issuer effects under packaged TEST trust. A fresh passing receipt under attacker keys after DNS and git capture can be issued outside those stores and produce no watcher finding. The recorded Row 2 CUT governs this case.
2. **Trigger clause — FAIL.** `docs/V1-DETECTION-CONTRACT.md:65`, `docs/phase-0-prereg-amendment-12.md:105`. “Until A12's L_term is live” places the D10 threshold transition at enablement. The signed trigger is a gate **before** enabling the bound, with the revised alarm already built, deployed and seen to fire. At a proposed enablement with only the 24-hour alarm, the gate is still open.
3. **Requester — FAIL.** `service/watcher/README.md:24`, `service/watcher/README.md:42`, `service/issuer/infra/main.tf:262`, `service/signer-kms/README.md:63`. D6's signer-role attribution identifies the KMS caller. It does not identify who submitted the work. The poller can drive the real signer through the KMS request queue and supply the accounting rows the watcher relies on, as in H3.
4. **Binding text — FAIL.** `docs/V1-DETECTION-CONTRACT.md:1`, `docs/V1-DETECTION-CONTRACT.md:40`, `docs/V1-DETECTION-CONTRACT.md:61`, `docs/V1-DETECTION-CONTRACT.md:65`, `docs/phase-0-prereg-amendment-12.md:38`, `docs/phase-0-prereg-amendment-12.md:105`. The draft is the requested review baseline. Its 24-hour alarm is an interim operating threshold. Treating that threshold as sufficient through enablement conflicts with the signed A12 gate. Likewise the README’s time-and-count rule documents the chosen implementation and supplies no recorded authority to narrow the draft’s receipt-accounting wording to counting signed jobs.
