**CF2-01 remains conditional, not established closed. CF2-02’s record-read race is closed.** The sweep found additional instances and a retention-timestamp problem.

No tracked-file edits or git writes. The requested issuer suite passed: **113 passed, none skipped**, including Terraform validation. [Suite output](/tmp/tmp.qRQiQv17lj/suite-results.txt). Seven scratch tests reproduce the behaviors described below: [tests](/tmp/tmp.qRQiQv17lj/test_cf3.py), [output](/tmp/tmp.qRQiQv17lj/results.txt). These use controlled delays, not live AWS fault injection.

**A — Confirmation assessment**

| Finding | Assessment |
|---|---|
| CF2-01 | The supplied deadline−1 reproduction is closed: no confirmation is attempted inside the final lease. However, the claim that Lambda termination bounds remote commit time remains unsupported. Closure requires an explicit remote-write bound, not merely a Lambda timeout. |
| CF2-02 | Closed for the reported storage-read race. Both `status` and `receipt` now read the record before sampling time; `status` also refreshes time after settlement. A separate potential blocking boundary remains inside AWS presigning, described below. |

The lease argument is mathematically sufficient **if every confirmation write commits or becomes permanently unable to commit within 900 seconds of the decision**. The implementation requires strictly more than 900 seconds remaining, so the equality boundary is conservative.

But [lambda_app.py:32](/home/tony/projects/tessera/service/issuer/tessera_issue/lambda_app.py:32) constructs clients without explicit timeout or retry configuration. [aws.py:82](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:82) conditions the confirmation on record version, not time.

Exactly what the argument assumes:

- DynamoDB confirmation attempts, including retries and backoff, cannot produce a commit later than decision time +900 seconds.
- For CF-02 cleanup, every S3 write from an invocation that observed ACCEPTED likewise commits or becomes permanently impossible within the fence bound.
- Requests already transmitted cannot commit after that bound, even if the caller timed out, received an error, or was killed.
- Credential acquisition, connection establishment, request transmission, response waits, retry delays and any later attempt are included in the bound.
- No writer operates outside the bounded invocations, and clock error or backward movement does not invalidate the margin.

Client timeouts bound waiting, not remote cancellation. Retry limits bound attempts, not necessarily the fate of an already transmitted attempt. Botocore exposes separate connection/read timeouts and retry settings; these do not establish the required server commit deadline. [Botocore configuration](https://docs.aws.amazon.com/botocore/latest/reference/config.html). AWS also explicitly documents that a failed DynamoDB write can have succeeded. [DynamoDB error handling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html).

**Therefore, reusing CF-02’s assumption is logically consistent, but does not make it established.** The previous confirmation already qualified CF-02 on this precise point. The new prose promotes that qualification into a claimed consequence.

**New findings, CF3-01 onward**

1. **CF3-01 — High: confirmation deadline still depends on an unestablished remote commit bound.**  
   Sites: [api.py:65](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:65), [api.py:76](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:76), [DESIGN.md:104](/home/tony/projects/tessera/service/issuer/DESIGN.md:104), [DISPOSITION.md:68](/home/tony/projects/tessera/docs/reviews/issuer/DISPOSITION.md:68).

   Scenario: decide at deadline−901 seconds; an in-flight confirmation commits 902 seconds later. It remains confirmed COMPLETE after the deadline. The scratch test reproduces this permitted-by-the-store-interface behavior. It does **not** demonstrate that AWS actually takes this long.

   Suggested fix: establish and explicitly accept the remote commit assumption, or redesign the authoritative completion event and visibility protocol so correctness does not require it. Explicit client timeouts and retry budgets are useful controls, but alone do not discharge this assumption. This is CF2-01’s remaining gap, not a wholly separate regression.

2. **CF3-02 — Medium: admission uses time sampled before reads and the acceptance write.**  
   Sites: [api.py:140](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:140), [api.py:162](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:162), [api.py:172](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:172).

   Scenario: start one second before `accept_until`; either `requests.get` or `requests.create` takes two seconds. Both scratch cases return **202 ACCEPTED after acceptance closes**, with an earlier `created_at`.

   Suggested fix: sample after admission reads, then address the create boundary explicitly—through a justified write margin or a defined admission linearization event. Moving the clock after reads fixes only half the problem. **Pre-existing, untouched by this diff.**

3. **CF3-03 — Medium: repeat submission can report an expired request as COMPLETE.**  
   Sites: [api.py:115](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:115), [api.py:120](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:120), [api.py:124](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:124).

   Scenario: submit identical content at expiry−1; delay the record read two seconds. The scratch test returns **202 with state COMPLETE at expiry+1**. Tombstone lookup/repair and upload recovery add further blocking boundaries while `_existing` retains the original `now`.

   Suggested fix: check expiry after tombstone operations, and use fresh time for the final view after upload recovery. **Pre-existing, untouched by this diff.**

4. **CF3-04 — Medium: successful confirmation backdates the public end and shortens retention.**  
   Site: [api.py:70](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:70).

   Scenario: confirmation is decided at deadline−901 and commits 900 seconds later, fully respecting the proposed lease. `ended_at` and `expires_at` remain based on the earlier decision. The scratch test demonstrates receipt retrieval returning **410 a full 900 seconds before 30 days after durable confirmation**.

   S4 defines the end as status becoming COMPLETE. Under this protocol, that cannot precede the confirmation commit. “Never earlier than the commit” is true only of the **initial unconfirmed write**, not the write that makes COMPLETE visible.

   Suggested fix: align the authoritative end, reported timestamp and retention origin. This mismatch predates the diff; the new lease test explicitly permits a much larger instance of it.

5. **CF3-05 — Medium, conditional: presigning can hide another blocking operation after the expiry check.**  
   Sites: [api.py:216](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:216), [aws.py:246](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:246).

   Scenario: expiry is checked at expiry−1, then credential refresh inside URL generation blocks two seconds. A URL is minted after expiry. The scratch test reproduces a delayed presigner; it does not exercise a real credential provider.

   Botocore obtains frozen credentials during signing, and supported providers can refresh credentials automatically. [Signer implementation](https://github.com/boto/botocore/blob/develop/botocore/signers.py), [credential providers](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html). This condition is not demonstrated for the intended Lambda environment-credential path.

   Suggested fix: explicitly constrain and verify the nonblocking credential path, or resolve credentials before the final expiry check and sign using that frozen snapshot. Rechecking after generation prevents returning the URL, but cannot support the stronger claim that none was minted. **Pre-existing boundary, not introduced by this diff.**

**B — Complete timing-site inventory**

Paths below are under `service/issuer/tessera_issue/`. “Safe” concerns the requested stale-clock class; it is not general implementation certification.

| Site | Assessment |
|---|---|
| `api.py:43`, `:85` — expiry predicate/view | Pure computation; safe when supplied fresh time. Unsafe caller is `_existing`, CF3-03. |
| `api.py:65–76` — confirmation deadline and save | Conditional safety only; CF3-01. Timestamp/retention mismatch is CF3-04. The failure branch cannot accidentally confirm. |
| `api.py:120`, `:124` — repeat expiry/view | Unsafe: reads, tombstone repair and potentially upload occur after the supplied sample. CF3-03. |
| `api.py:140`, `:162`, `:172` — admission window | Unsafe across reads and create. CF3-02. |
| `api.py:185–194` — status expiry | Safe for present records: clock follows read and is refreshed after settlement. Missing-record tombstone lookup has no expiring COMPLETE decision to carry forward. |
| `api.py:210–216` — receipt expiry | Storage-read ordering fixed. Presigner safety depends on its internals; CF3-05. |
| `pipeline.py:83–90` — terminal deadline | Initial write can be late, but remains unconfirmed; settlement guards public COMPLETE, subject to CF3-01. FAILED/REFUSED timestamps can also precede their durable writes. |
| `pipeline.py:115–118` — cleanup retention | Conservative: time follows record/settlement. Subsequent delay can postpone deletion, not make it premature relative to the stored expiry. Stored expiry itself has CF3-04’s problem. |
| `pipeline.py:120–133` — cleanup fence | Conservative locally: deletion/listing follows the sample. A stale sample can retain the obligation longer. Safety against later remote writes still requires CF3-01’s remote bound. |
| `pipeline.py:138–141` — cleanup entry sample | Safe: `_cleanup_one` does not use this supplied sample for its decisions; it samples again. |
| `pipeline.py:148–152` — request deadline | Stage work can cross the deadline. Safe against public late COMPLETE only through terminal settlement; not a hard stop on all work at 24 hours. |
| `pipeline.py:280–285` — upload grace | Read occurs after stage time was sampled. Conservative: an overdue missing upload can survive another tick; it cannot fail prematurely from that delay. |
| `pipeline.py:290–315` — frames/signing stop | Unsafe as a claim that no frames/jobs are produced after the stop: content reads and writes can cross it. Actual late signing is delegated to signer-side `sign_by`/configured-stop enforcement. That deployment gate remains open. |
| `pipeline.py:321–337` — signing stop/resend | Reconciliation, save, frame retrieval and queue operations can cross the stop. Same signer-side dependency. Already collected signatures may legitimately proceed to sealing. |
| `pipeline.py:326` — retry interval | Safe as a minimum retry interval: delay makes sending later. `sent_at` is a decision timestamp, not an exact enqueue timestamp. |
| `pipeline.py:375–399` — snapshot validity | Stale “now”: header/calendar/storage/DNS work occurs before validation and stamping. Unsafe as a literal “valid at stamping now” claim. Final verifier checks against anchored evidence time prevent this alone from yielding a false VALID_STRICT; likely result is rejection/recapture. |
| `pipeline.py:478–485` — pre-ship/deadline | Receipt storage can cross the fresh check. `_end` rechecks after the obligation write; settlement then guards visibility, subject to CF3-01. |
| `preship.py:45–51` — evaluation time | Historical verification configuration, not a wall-clock signing permission. Delayed verification does not invalidate historical evidence merely by taking time; completion is separately guarded. |
| `signers.py:134` — declared-time epsilon | Frame retrieval precedes this sample. No intervening storage call before the local signing-stop check. Safe for the current TEST implementation’s storage-delay model. |
| `signers.py:141–148` — signing stop/`sign_by` | Checked after reference retrieval, immediately before local TEST signing. It bounds permission to start signing, not completion time of an arbitrarily slow signing primitive. Scratch test demonstrates that distinction. Do not transfer this guarantee to remote KMS/GCP calls without defining their effect boundary. |
| `stores.py:169`, `:172` — simulated TTL | Local operations only; safe for this class. |
| `stores.py:192–201` — memory URL expiry | Local operations only; no blocking storage boundary. |
| `queues.py:45–52` — simulated visibility lease | Local operations only; safe for this class. |
| `window.py:93` — window-length validation | Compares fixed configured endpoints, not a sampled clock; outside the class. |

The remaining modules contain timestamp construction, evidence/block-time comparisons or clock plumbing, but no additional sampled-clock permission check of this class.

**C — Diff-specific conclusion**

The diff fixes the two supplied interleavings and correctly keeps cleanup pending for an unconfirmed completion. I found no additional independent code regression introduced by those changes. Its material remaining problems are the unsupported confirmation-bound claim and the end/retention semantics above. The final-15-minute confirmation cutoff is intentional, disclosed behavior.

**Owner prechecks — changed DESIGN bullets and DISPOSITION addition only**

| Check | Result and locations |
|---|---|
| Capture row | **PASS** — `DESIGN.md:100–109`, `DISPOSITION.md:61–69` make timing/lifecycle claims, not attacker-key rejection or capture-detection claims. They do not contradict `V1-CONTRACT.md:37`, `:72–73`. |
| Trigger clause | **PASS** — `DESIGN.md:104–109`, `DISPOSITION.md:68–69` reference the actual confirmation findings. No registered amendment consequence is invoked without its trigger. Reusing CF-02’s assumption is technically insufficient, but is not a registered-rule trigger violation. |
| Requester | **PASS** — the changed text does not infer signing security from key location or deny the issuer’s ability to submit signer work. `DISPOSITION.md:56–57` retains the deployed-signer integration gate. |
| Binding text | **PASS** — these are descriptions of an owner implementation change and its disclosed cost. `DISPOSITION.md:68` cites S4’s usual latency descriptively; it does not promote that owner resolution into a registered guarantee. No schedule ruling budget is used as authority. |

**READY FOR DEPLOYMENT WORK: NO — resolve the remote-commit assumption and remaining lifecycle timing gaps before clearing this review gate.**