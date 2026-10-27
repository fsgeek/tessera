Found **11 issues**. The issuer suite passed: **75 passed, 1 skipped** in 35.52s. Terraform validation was skipped because Terraform is not installed. No files were edited.

1. **IS-01 — High: a receipt can complete before its signature audit log is durable.**  
   [pipeline.py:134](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:134) saves the signature and marks its job satisfied before `siglog_add()` at line 141. If that log write fails, later polls can seal and ship using the saved signature while response delivery is delayed or missed. Fault injection produced **COMPLETE with only three signature-log entries**. The fourth hash remained in request metadata, but was absent from the append-only log. SQS short polling permits false-empty responses. [AWS documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)  
   **Fix:** durably log each response before making its signature eligible, and require that log record when sealing.

2. **IS-02 — High: completion can cross the 24-hour deadline.**  
   [pipeline.py:330](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:330) uses the timestamp captured before assembly and verification. There is no fresh deadline check before storing the result and committing COMPLETE. Starting verification at acceptance +86,399 seconds and advancing the clock two seconds during verification produced **COMPLETE at +86,401**, with `ended_at` backdated to +86,399.  
   **Fix:** recheck the clock immediately before completion, enforce the deadline in the terminal transition, and record the actual transition time.

3. **IS-03 — High: the signing stop does not stop queued signing work.**  
   [pipeline.py:169](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:169) sends requests without an enforced signing deadline. Failing the issuer request does not invalidate queued work. A request accepted at the acceptance cutoff, then processed after `sign_until`, produced **two KMS signatures and one GPG possession signature after the stop**, although its issuer state was FAILED.  
   **Fix:** enforce the window’s signing cutoff at each policy signer immediately before the signing operation. Issuer-side enqueue checks alone cannot enforce it.

4. **IS-04 — High: a failed tombstone write permits reuse of a terminal request key.**  
   [api.py:111](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:111) creates the request separately from its tombstone. If the subsequent tombstone write fails, a retry takes the existing-record path and never repairs it. Reproduction: create REFUSED, fail the tombstone write, retry and receive REFUSED; after 30-day TTL deletion, clear the refusal condition and submit the same key. It returns **202 ACCEPTED** during a longer issuance window.  
   **Fix:** atomically create the request and tombstone, and repair missing tombstones on existing-record responses.

5. **IS-05 — High: racing submissions can store refused content.**  
   [api.py:108](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:108) writes content before winning request creation. A concurrent submission can create REFUSED between the initial lookup and that write. The losing caller then returns the existing refusal while leaving its content stored. The reproduced interleaving returned **REFUSED to both callers with a content blob remaining**. Refused records never enter pipeline cleanup.  
   **Fix:** establish durable ownership before storing content, with a recoverable initialization state and cleanup for abandoned uploads.

6. **IS-06 — High: pre-signed downloads bypass both expiry and credential enforcement.**  
   [api.py:143](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:143) requests the default 900-second URL without considering `available_until`. One second before expiry, it still issues a URL valid for another 900 seconds. That URL also requires no submitting credential: another credential—or an unauthenticated holder—can use it. AWS explicitly defines these URLs as bearer tokens. [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)  
   **Fix:** serve downloads through a credential-checking endpoint that enforces request expiry. Cap any download authorization at the remaining retention interval.

7. **IS-07 — Medium: deletion depends on asynchronous lifecycle processing, and failed cleanup is abandoned.**  
   [pipeline.py:69](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:69) commits the terminal state before deleting content/work. A deletion failure removes the request from future active processing, so cleanup is never retried. Completed results have no explicit expiry deletion; [main.tf:110](/home/tony/projects/tessera/service/issuer/infra/main.tf:110) relies on S3 lifecycle expiration. AWS rounds that eligibility time to the next midnight and deletes asynchronously, so it does not implement deletion exactly 30 days after termination. [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-lifecycle.html)  
   **Fix:** persist cleanup obligations and expiry deadlines, retry deletion independently of request state, and verify completion.

8. **IS-08 — Medium: concurrent responses can trigger signing again despite a complete verified set.**  
   [pipeline.py:137](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:137) uses whole-record compare-and-set updates. Two consumers handling different jobs can both write valid signature blobs, then one loses its metadata update. The response is nevertheless logged and acknowledged. Reproduction left **four individually verified signatures**, but one missing job hash; [pipeline.py:180](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:180) subsequently enqueued another signing request. Terraform’s concurrency limit mitigates overlapping invocations of that Lambda, but the store protocol itself is unsafe with two pollers.  
   **Fix:** persist job results independently or merge them atomically, and reconcile verified stored signatures before resending.

9. **IS-09 — Medium: accepted 1 MiB content cannot traverse SQS.**  
   [signers.py:53](/home/tony/projects/tessera/service/issuer/tessera_issue/signers.py:53) base64-encodes a frame whose content is already base64-encoded. A permitted 1 MiB submission produced an attestation message of **1,865,175 bytes**, exceeding SQS’s **1,048,576-byte** maximum. The stand-ins do not enforce this limit, so local tests conceal the failure. [AWS API reference](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html)  
   **Fix:** transport large frames through immutable, digest-bound objects referenced by the queue, while preserving the stamped client limit.

10. **IS-10 — Medium: IAM grants unnecessary object mutation rights.**  
    [main.tf:188](/home/tony/projects/tessera/service/issuer/infra/main.tf:188) grants the API `PutObject` on completed results, although it only writes submissions. [main.tf:211](/home/tony/projects/tessera/service/issuer/infra/main.tf:211) grants the poller write/delete access to configuration, although it only reads it. Compromise of either role therefore permits mutations beyond its required operations, including receipt replacement or window-configuration replacement.  
    **Fix:** separate permissions by action and prefix: API write-content/read-results; configuration read-only; poller mutation limited to operational object namespaces. No issuer KMS grant or public S3 allow was found.

11. **IS-11 — Medium: truncated DNS responses can prevent TCP fallback.**  
    [dns.py:136](/home/tony/projects/tessera/service/issuer/tessera_issue/dns.py:136) fully parses the UDP answer before examining its truncation flag. A TC-marked response ending inside RDATA raises before reaching the TCP branch. Reproduction returned **`DnsError: truncated RDATA`, with zero TCP connection attempts**. This can stall otherwise valid issuance until FAILED.  
    **Fix:** inspect the DNS header’s TC bit before parsing answer records, then fetch and parse the complete TCP response.

These are local review and fault-injection findings; the passing stand-in suite does not cover these failure paths.


