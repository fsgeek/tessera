Confirmation is **partial**. The issuer suite passed: **98 passed, 1 skipped in 52.66 s**. Terraform validation was skipped because Terraform is unavailable. No files were edited.

I loaded the pre-fix sources preserved in the [original review log](/home/tony/projects/tessera/docs/reviews/issuer/codex.log) into an isolated Python process and ran the current regression cases: **22 failed, 1 passed**. Some failures reflect changed interfaces rather than reproducing the original defect.

1. **CF-01 — High: COMPLETE can still cross the 24-hour deadline.**  
   [_end](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:76) samples and checks the clock **before** persisting the cleanup obligation. Injecting a two-second delay into `cleanup_put`, starting at deadline −1 second, produced **COMPLETE at deadline +1**, with `ended_at` backdated to deadline −1. IS-02 is therefore only partially fixed.  
   **Fix:** persist the obligation before the final clock check, enforce the deadline at the terminal commit boundary, and prevent backdated completion timestamps. Cover delays in both obligation persistence and terminal persistence.

2. **CF-02 — Medium: late writers can leave objects after cleanup has discharged its obligation.**  
   [_finish_upload](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:85) and [_take](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:190) can write after concurrent termination and cleanup. Reproductions produced:
   - An upload retry overlapping the 15-minute failure transition, whose S3 write committed but whose caller failed afterward: **FAILED, content retained, no cleanup obligation**.
   - A signature write following concurrent termination: **FAILED, signature object retained, no cleanup obligation**, logged as `superseded:not-waiting`.

   [_cleanup_one](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:94) treats an empty listing as sufficient to discharge cleanup despite outstanding writers.  
   **Fix:** use durable write intents or writer fencing, and retain cleanup obligations until outstanding writes have finished. Cover writes that commit before the caller receives an error.

3. **CF-03 — Medium: a delayed object check permits URL minting after expiry.**  
   [receipt](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:164) checks expiry through `status()`, then performs an object-size request without rechecking expiry. Starting one second before expiry and delaying that request two seconds produced **303 and a newly minted URL one second after expiry**, while status returned EXPIRED.  
   **Fix:** recheck expiry with a fresh clock after the object check, immediately before minting. Keep the owner’s 300-second URL design.

4. **CF-04 — Medium: one persistent deletion error can starve subsequent cleanup obligations.**  
   [S3ResultStore.delete](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:207) ignores per-object `Errors` and loops without a bound. S3 can return individual deletion failures in a successful response. [AWS DeleteObjects documentation](https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObjects.html).  
   Injecting repeated per-object errors caused repeated deletion attempts until a simulated Lambda timeout; the second obligation was never visited. This inherited helper undermines the new persistent cleanup mechanism.  
   **Fix:** inspect deletion errors, bound work per obligation, and preserve failed obligations while allowing other requests’ cleanup to proceed.

5. **CF-05 — Low: the interrupted-upload test does not distinguish the fix from the old implementation.**  
   [test_IS05_interrupted_upload_is_recovered_by_a_retry](/home/tony/projects/tessera/service/issuer/tests/test_review_fixes.py:193) **passes unchanged against the pre-fix sources**. Both implementations recover from its initial upload failure.  
   **Fix:** assert that the failed upload leaves a durable ACCEPTED record at stage `upload`, and that retry resumes that same record; alternatively, describe it as a functional test and correct the disposition’s blanket regression claim.

Per-finding confirmation:

| Finding | Fixed? | Regression against pre-fix sources |
|---|---|---|
| **IS-01** | **Yes.** Durable logging precedes eligibility; sealing requires the log record. | Both behavioral tests fail: unlogged eligible signature and sealing despite a removed log record. Store-contract cases fail on missing interfaces. |
| **IS-02** | **Partial — CF-01.** The slow-verification scenario is fixed. | Fails behaviorally: old code completes after slow verification. |
| **IS-03** | **Issuer and stand-in fixed; deployed signers remain open.** | Fails behaviorally: queued work produces signatures after the stop. |
| **IS-04** | **Yes.** Atomic creation and missing-tombstone repair are present. | Reuse and repair tests fail behaviorally. Transaction test fails because the old method lacks the new argument. |
| **IS-05** | **Original refusal race fixed; new cleanup race in CF-02.** | Refusal-race test fails behaviorally. Interrupted-upload test **passes**. Abandoned-upload test fails because the old code leaves no request record. |
| **IS-06** | **Owner’s minting design implemented; expiry race remains — CF-03.** | Primary test fails on the old **900-second** lifetime. Second test stops at the absent TTL constant. |
| **IS-07** | **Partial — CF-02 and CF-04.** Ordinary cleanup retry and expiry deletion work. | Both behavioral tests fail: failed deletion is abandoned; expired receipt remains stored. |
| **IS-08** | **Yes for signature metadata merging and reconciliation.** Terminal/write cleanup remains CF-02. | Both tests fail behaviorally through extra signing. An additional interleaving of two distinct response consumers preserved both job results with only two signatures. |
| **IS-09** | **Issuer and stand-in fixed; deployed signers remain open.** | Size test fails at **1,865,175 bytes**; queue-limit test fails to raise. Reference test fails because old code creates no frame references. |
| **IS-10** | **Yes, by static inspection.** | Fails against the original Terraform policy’s result-write grant. Terraform validation remains unrun. |
| **IS-11** | **Yes.** TC inspection precedes answer parsing. | Fails with `DnsError: truncated RDATA` before TCP fallback. |

The [IS-06 disposition row](/home/tony/projects/tessera/docs/reviews/issuer/DISPOSITION.md:20) still contains the superseded Range description in its regression-test column; replace it with the current test names.

Deployed-signer enforcement of `sign_by`, configured signing stops, and digest-bound `frame_ref` retrieval remains a pre-issuance integration gate. The passing stand-in suite does not establish those properties for deployed signers.

**READY FOR DEPLOYMENT WORK: YES AFTER (CF-01–CF-05 are addressed, regression coverage added for the reproduced races, and the IS-06 disposition corrected).**
