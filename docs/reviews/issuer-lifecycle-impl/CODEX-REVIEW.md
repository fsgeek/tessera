**Verdict: not ready for deployment work, even with the gate closed.**

The lifecycle core largely follows revision 5.3.1, but permanent-failure handling, signing recovery, runtime budgeting, and test coverage need correction. I made no repository or git writes. Scratch work is under [/tmp/tmp.H7U54TsUGg](/tmp/tmp.H7U54TsUGg).

Validation: **158 passed in 87.97 s**, with bytecode/cache writes disabled and pytest temporary files redirected to scratch. Seven additional scratch probes reproduced the cases below. I inspected R53 and its recorded results; I did not rerun TLC.

**Findings**

1. **ILI-01 — High: the post-latch incurable set is incomplete.**  
   [pipeline.py:83](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:83), [pipeline.py:589](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:589), [pipeline.py:720](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:720).

   A proof can contain both a qualifying branch and a contradicted branch at the selected height. `fetch_evidence` ignores `select`’s contradiction flag; pruning retains both branches at that height. The attempt latches, then pre-ship returns `INVALID/OTS_MERKLE_MISMATCH`. That reason is absent from `COMMITTED_BYTES_REASONS`, so the immutable, invalid presentation is retried forever. **Reproduced.**

   The eleven listed reasons are consistent with immutable failures in the current assembly path, but they are not exhaustive. Other missing cases include receipt transaction-shape/txid failures and failures attributable to frozen git material. Classification must distinguish those from replaceable snapshot/configuration failures.

   **Fix:** classify failures by their actual evidence dependency and repairability. Reject or discard a definitively invalid preserved presentation with a recorded reason; test each classification against a real verifier outcome.

2. **ILI-02 — Medium: known incurable snapshot failure has no ending path.**  
   [pipeline.py:696](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:696), [pipeline.py:714](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:714), [pipeline.py:730](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:730).

   Snapshot problems either wait, recapture, or retry. There is no representation of “this frozen attempt cannot obtain any lawful snapshot.” Consequently, under the brief’s **“can never be anchored” premise**, the attempt remains latched forever rather than taking step 7’s reasoned discard.

   The scratch probe reproduced the `SNAPSHOT_TIME → recapture → stamp → retry` loop. It does **not** establish irreparability merely from elapsed wall time: timestamps are nonmonotone, and historical evidence may recover.

   **Fix:** add an evidence-based permanent-failure classification. Do not introduce an age-based discard. Proven impossibility belongs outside the pending sampled-unavailability gate; indefinite retry of that proven-impossible case leaves A2.3 termination unmet outside that gate.

3. **ILI-03 — Medium: complete, contradicted evidence is classified as pending.**  
   [pipeline.py:602](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:602).

   With no pending calendars, every full segment obtained, and every attestation contradicted by its pinned header, `sel is None` prevents classification as negative. The result is `pending` indefinitely. **Reproduced.**

   This is conclusive invalid evidence under [profile §7.1:889](/home/tony/projects/tessera/docs/V1-PROFILE.md:889), rather than missing evidence. Conversely, `sel is None` alone is insufficient to conclude failure.

   **Fix:** distinguish complete authenticated contradiction from incomplete/nonqualifying evidence. Record an explicit invalid-evidence reason; do not fabricate a failed temporal conjunct.

4. **ILI-04 — Medium: signing closure precedes recovery of completed signing.**  
   [pipeline.py:410](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:410), [pipeline.py:415](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:415).

   All four signatures can already exist in S3 and the durable “used” log while their request-record updates were lost. After signing closes, `st_signing` discards before `_reconcile` can recover them. The request becomes `REFUSED/SIGNING_CLOSED` although no further signature is necessary. **Reproduced.**

   **Fix:** reconcile durable signatures before deciding whether signing is still required, then seal a complete recovered set regardless of closure. Add this interleaving to the closure tests.

5. **ILI-05 — High: one healthy evidence fetch can exceed the entire Lambda budget.**  
   [pipeline.py:100](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:100), [pipeline.py:635](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:635), [chain.py:47](/home/tony/projects/tessera/service/issuer/tessera_issue/chain.py:47), [main.tf:363](/home/tony/projects/tessera/service/issuer/infra/main.tf:363).

   With two explorers, one six-header segment requires 24 sequential header/hash HTTP requests plus two tip requests. At 12 seconds each—below the configured 20-second HTTP timeout—that is **312 seconds**, before calendars, S3, DynamoDB, or the latch write.

   Every invocation can commit another fence and die before making progress. Multiple attestations and multiple requests worsen this; the poller has no durable scheduling cursor or remaining-time budget.

   **Fix:** bound and checkpoint work within the 300-second invocation, preserve fetched immutable material, and schedule requests fairly. Keep reserved concurrency 1 and the fence; do not solve overload by ending attempts.

6. **ILI-06 — Medium: pruning’s load-bearing behavior is untested.**  
   [test_lifecycle.py:356](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:356), [test_lifecycle.py:570](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:570), [test_lifecycle.py:664](/home/tony/projects/tessera/service/issuer/tests/test_lifecycle.py:664).

   I independently ran the supplied `NOPRUNE` mutation against the lifecycle suite: **37 passed**.

   A scratch case exposed the missing distinction: latch a higher passing attestation while the lower segment is unavailable, then add that lower segment to the assembly headers. With pruning, assembly preserves the selected height. Without pruning, selection moves lower and assembly raises `StageError`.

   **Fix:** add this case through finalization/shipping, including lower evidence arriving through snapshot/git header collection. Require pruning removal to fail the test.

7. **ILI-07 — Medium: an uncapped refusal reason can exceed DynamoDB’s item limit.**  
   [pipeline.py:279](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:279), [pipeline.py:165](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:165), [aws.py:54](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:54).

   A signer’s unrestricted `reason` is copied into both the attempt ending and event history. A 210,000-character reason produced a **422,386-byte item** in the scratch probe. AWS limits items to 400 KiB, including attribute names and values. The terminal/allocation write therefore fails instead of completing. [AWS constraints](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Constraints.html)

   **Fix:** validate and cap external reason fields, retain a bounded reason code, and store oversized diagnostics separately by reference. Add serialized-item-size checks to the AWS adapter tests.

8. **ILI-08 — Medium: `CONTENT_UNAVAILABLE` also terminates an allocated attempt.**  
   [pipeline.py:374](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:374), [pipeline.py:380](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:380), [DESIGN.md:29](/home/tony/projects/tessera/service/issuer/DESIGN.md:29).

   `st_frames` commits allocation before reading content. A missing content object then ends the request `FAILED/CONTENT_UNAVAILABLE`, marking the allocated attempt discarded. This contradicts the documented “before any attempt” exception and bypasses normal end-and-allocate handling.

   **Fix:** check content availability before allocation. Once allocated, a storage miss needs recovery or an explicitly justified permanent-failure path.

9. **ILI-09 — Low: documentation still makes incompatible operational claims.**  
   [DESIGN.md:43](/home/tony/projects/tessera/service/issuer/DESIGN.md:43) says a failed pre-ship check becomes `FAILED`; the implementation generally retries or discards. [DESIGN.md:44](/home/tony/projects/tessera/service/issuer/DESIGN.md:44) says the new margin is unapplied, although [window.py:23](/home/tony/projects/tessera/service/issuer/tessera_issue/window.py:23) implements it.

   Also, [window.py:8](/home/tony/projects/tessera/service/issuer/tessera_issue/window.py:8) promises the first attempt “always” has its full lifecycle before signing stops. Acceptance spacing cannot guarantee that when allocation can be delayed.

   **Fix:** reconcile the current descriptions and describe the margin as an operating allowance, without a guaranteed processing bound.

**Conformance and the gate**

| Area | Assessment |
|---|---|
| Attempts and isolation | Implemented: separate material, signing IDs, response routing, declarations and stamps. |
| Single lifecycle writer | Implemented; status/receipt are read-only, poller concurrency is 1. Submission/upload bookkeeping remains separate. |
| Fence before fetch | Implemented for evidence, finalization and recapture; failed fencing prevents fetching. |
| Write guards | Implemented on version, request state, attempt ID and attempt state, including DynamoDB expressions at [aws.py:85](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:85). |
| Eligibility | Own `A_sig` digest, k=6, full linked segments and all three inclusive conjuncts are checked. Invalid-proof classification has ILI-01/03 gaps. |
| Preserved latch | Presentation is written to S3 before its digest/reference commits at [pipeline.py:653](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:653). |
| Negative endings | Partial, stale, failed and pending fetches do not cause expiry. Complete-invalid evidence needs ILI-03’s distinction. |
| Atomic endings | End-and-allocate and final refusal occupy one conditional request-item write. A multi-item transaction is unnecessary for these transitions. |
| Storage lifetime | Corrected: live objects receive no age-expiration tag; cleanup derives eligibility from persisted request end. |
| Public view | Attempt number/state, open boundary, nominal-budget note and refusal reasons are exposed. |

**The sampled-unavailability gate is closed.** No lifecycle path produces `EVIDENCE_UNAVAILABLE`, reads diagnostic failure history to decide an ending, or turns an evidence-stage timeout/age/signing closure into an equivalent ending. Stamped and latched attempts survive signing closure. ILI-04 and ILI-08 are separate pre-stamp ending defects, not evidence that step 5 has secretly been enabled.

**Judgment on the seven deviations**

| Deviation | Judgment |
|---|---|
| **(a) Latch the passing presentation in hand; prune to its height** | **Sound for the shipped presentation**, subject to ILI-01/06. Profile §7.1 selects among qualifying branches in the presented proof; a missing lower segment supplies no time fact. Pruning prevents later assembly headers changing that presentation’s selection. This is not owner acceptance of the policy. |
| **(b) Complete evidence with no qualifying attestation remains open** | **Too broad.** Incomplete qualification remains open; complete authenticated contradiction is conclusive invalidity. ILI-03. |
| **(c) `COMMITTED_BYTES_REASONS`** | Listed members are defensible; **the set is incomplete**, and reason-only classification needs provenance. ILI-01. |
| **(d) Permanently impossible snapshot remains latched** | **Incorrect under the stated impossibility premise.** Step 7 should discard with evidence and reason. Elapsed wall time or one `SNAPSHOT_TIME` result does not establish that premise. ILI-02. |
| **(e) `FAILED/CONTENT_UNAVAILABLE` before any attempt** | Defensible for an abandoned upload. The implementation also applies it after allocation. ILI-08. |
| **(f) Signer refusal discards and allocates next** | Defensible for the current unsigned, unstamped attempt; it cannot yet have protected receipt eligibility. Keep routing/logging and bound the supplied reason. |
| **(g) Capped diagnostic runs** | Acceptable while diagnostic only. Capping loses history; it cannot later serve as complete gated coverage evidence without fresh analysis. |

The tests meaningfully exercise selected model interleavings: killed writes, fence sensitivity, duplicate endings, boundary latching and partial recovery. They are **not a complete model-trace replay or implementation refinement check**. Post-latch assembly, signing recovery and AWS execution constraints remain outside R53’s checked assurance.

For AWS, ordinary bounded attempt metadata and S3 presentation references avoid embedding large proofs in DynamoDB; ILI-07 remains the size hole. Request creation correctly uses a transaction for request plus tombstone. Cleanup’s obligation-before-terminal ordering is appropriate. `s3:PutObjectTagging` is granted to the poller at [main.tf:241](/home/tony/projects/tessera/service/issuer/infra/main.tf:241), matching the API’s required permission. [AWS tagging API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectTagging.html)

**Owner prechecks**

| Check | Result | Evidence |
|---|---|---|
| **1. Capture row** | **PASS** | Reviewed lifecycle claims do not promise attacker-key rejection or capture visibility. Ground truth remains [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72): fresh attacker-key receipts pass after dual-channel capture. |
| **2. Trigger clause** | **FAIL** | [pipeline.py:412](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:412) applies signing closure before establishing that signing is still required. Durable recovery can falsify that antecedent—ILI-04. |
| **3. Requester** | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer as queue requester; [pipeline.py:352](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:352) submits the work. Lack of direct signing credentials is not promoted into requester-compromise resistance. Deployed signer authorization remains unverified here. |
| **4. Binding text** | **FAIL** | The owner constant at [pipeline.py:83](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:83), treated as exhaustive at [DESIGN.md:160](/home/tony/projects/tessera/service/issuer/DESIGN.md:160), strands known immutable-invalid attempts. The pending step-5 decision does not waive [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288)’s termination obligation for these separate failures. |

