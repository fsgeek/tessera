**CF-01 and CF-03 remain PARTIAL. CF-02, CF-04 and CF-05 are CLOSED**, subject to the CF-02 runtime assumption below.

I made no tracked-file edits or git writes. Scratch artifacts are under [/tmp/tmp.NNIr6fW7u7](/tmp/tmp.NNIr6fW7u7).

The issuer suite passed: **108 passed, 1 skipped in 61.59 seconds**. I ran the requested pytest invocation with bytecode disabled and its cache redirected into scratch space. Terraform validation was skipped.

**Historical-source limitation:** `git show dc5b601^:service/issuer/tessera_issue/pipeline.py` fails because the parent contains no issuer package. I recovered the relevant source listings from the committed review logs instead. Against the pre-CF listings, the 11 selected tests produced **9 failures, 2 passes**; these are not all behavioral regressions.

| Finding | Assessment and evidence |
|---|---|
| **CF-01 — PARTIAL** | [pipeline.py:80](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:80) now persists cleanup before checking time, and settles the initial COMPLETE write afterward. `test_CF01_slow_cleanup_obligation_write_cannot_carry_completion_past_the_deadline` and `test_CF01_slow_terminal_write_cannot_carry_completion_past_the_deadline` both fail behaviorally against pre-CF code: it remains COMPLETE. The crash test also distinguishes old behavior. However, the new confirmation write has another persistence-boundary gap; see CF2-01. The “completion seen before deadline” test fails on old code only because `confirmed_at` is absent; its public-state assertions pass there. |
| **CF-02 — CLOSED within the stated Lambda bound** | [pipeline.py:100](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:100) retains the cleanup obligation through `fence_until`, repeatedly deletes, and requires an empty listing after that interval. Both `test_CF02_upload_that_commits_after_the_end_is_still_deleted` and `test_CF02_signature_written_after_termination_is_still_deleted` fail behaviorally against pre-CF code, leaving objects behind. The upload case explicitly commits the object before raising to its caller. `test_CF02_write_lease_covers_every_lambda_timeout` passes against both versions; it is a configuration guard. The closure depends on the documented assumption that all object commits finish within the 900-second writer bound; a Lambda timeout alone is not evidence that a remote in-flight write was cancelled. |
| **CF-03 — PARTIAL** | [api.py:205](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:205) rechecks expiry after the object check, closing that exact delay scenario. `test_CF03_no_url_is_minted_after_expiry_even_if_the_object_check_is_slow` fails behaviorally against pre-CF code, which returns 303. But the fix inserts a blocking record read after sampling the clock, reopening the expiry race; see CF2-02. |
| **CF-04 — CLOSED** | [aws.py:209](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:209) checks per-object `Errors`, raises immediately, and bounds deletion rounds. [pipeline.py:135](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:135) catches that error per obligation and continues. Both `test_CF04_s3_delete_reports_per_object_errors_and_is_bounded` and `test_CF04_one_failing_deletion_does_not_starve_other_cleanups` fail behaviorally against pre-CF code, reaching the simulated invocation timeout. |
| **CF-05 — CLOSED** | [test_review_fixes.py:193](/home/tony/projects/tessera/service/issuer/tests/test_review_fixes.py:193) now checks durable ACCEPTED/upload ownership after the failed upload and preservation of the original record on retry. `test_IS05_interrupted_upload_is_recovered_by_a_retry` fails against the original pre-IS-05 API at the intended assertion: `first is None`. It passes against pre-CF code, correctly: CF-05 strengthens coverage of the earlier IS-05 implementation fix. |

**New defects introduced by the fixes**

1. **CF2-01 — High: confirmation can become durable after the completion deadline.**  
   [api.py:61](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:61) samples time before saving `confirmed_at`. Start at deadline −1 second, let the initial unconfirmed COMPLETE commit, then delay the confirmation save two seconds. The persisted result is confirmed COMPLETE at deadline +1, with `confirmed_at` and `ended_at` set to deadline −1.

   Scratch test `test_delayed_confirmation_commit` reproduces this. The initial COMPLETE commit did precede the deadline; the defect concerns the new rule that it does not count or appear as COMPLETE until confirmation is durable. The existing terminal-delay test delays the first write, leaving this second boundary uncovered.

   **Suggested fix:** define one authoritative completion event and align deadline enforcement, public visibility and timestamps with it. If durable confirmation is that event, enforce its deadline at the storage commit boundary; another client-side clock check merely moves the gap. Add delayed-confirmation and commit-then-error cases.

2. **CF2-02 — Medium: the new record read permits minting after expiry.**  
   [api.py:205](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:205) samples `now`, then calls `requests.get`, then checks expiry using the earlier timestamp. Start at expiry −1 second and delay that read two seconds: the handler returns **303 and mints a URL at expiry +1**.

   Scratch test `test_delayed_expiry_record_read` reproduces this, observing one presigned URL.

   **Suggested fix:** read the record first, then sample the clock and check expiry immediately before `presign`, preserving the 300-second URL design. Add a delayed-record-read regression.

Both additional tests and their failure output are preserved in [test_adversarial.py](/tmp/tmp.NNIr6fW7u7/tests/test_adversarial.py) and [new-results.txt](/tmp/tmp.NNIr6fW7u7/new-results.txt).

**READY FOR DEPLOYMENT WORK: NO — resolve CF2-01 and CF2-02 before treating this confirmation gate as cleared.**

