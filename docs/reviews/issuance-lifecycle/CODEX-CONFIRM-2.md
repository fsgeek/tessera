**Verdict: not ready to implement.** Revision 3 removes concurrent poller execution, but it still permits loss of timely eligibility, and its lease argument does not cover the interval from observation to sending the write. Step 10 needs to check the registered property without redefining eligibility as successful persistence.

Review was read-only; no repository edits or git writes. Constructed counterexamples are in [scratch](/tmp/tmp.OmyIY8mGav/counterexamples.txt). These are protocol traces, not TLC results.

### A. ILC-01–05

“CLOSED” below concerns the design correction, not implementation conformance.

| Finding | Status | Assessment against registered text |
|---|---|---|
| **ILC-01 — timely observation loses to expiry** | **PARTIAL** | [Steps 1–4](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) remove simultaneous poller invocations and the API lifecycle writer. But “counts once that write is durable” weakens the protected event, and the delayed-write argument is incomplete. [A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153) requires the inclusive boundary to be latch-winning. See ILC2-01–02. |
| **ILC-02 — premature permanent failure** | **PARTIAL** | [Step 6](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:75) correctly waits for every calendar, but “no pending calendar” does not establish that every attestation’s qualifying header evidence is complete. [A2:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161) does not authorize treating recoverable missing evidence as permanent predicate failure. See ILC2-03. |
| **ILC-03 — unavailable-evidence refusal** | **PARTIAL** | [Step 5](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:71) expressly protects durable latches and uses the single writer. It still treats absence of a durable latch as sufficient protection against refusing timely eligibility. A2.3’s termination obligation does not cancel [A2.1’s eligibility protection](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130). |
| **ILC-04 — overbroad post-latch discard** | **CLOSED** | [Step 7](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:78) preserves the qualifying presentation, retries transient failures, and restricts discard to incurable failures. That respects [A9’s completeness invariant](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:165) and [not-after prohibition](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:422). The implementation must classify the underlying failure, rather than merely classify a verifier reason code. |
| **ILC-05 — terminal guards and retry recovery** | **CLOSED** | [Steps 1 and 8](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) specify state/attempt guards and atomic end-and-allocate, including refusal. This addresses duplicate transitions and the between-attempt crash gap, consistent with [A2.3’s atomic refusal requirement](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:278). |

### B–C. Protocol attack and new findings

**ILC2-01 — High: persistence is substituted for the registered eligibility event.**

[Revision:55](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:55) says:

> “The observation counts once that write is durable.”

That is a substantive restriction. An observation at B followed by a crash before persistence becomes an observation that never counted. Disclosure as a residual does not establish compatibility with the registered latch obligation.

The model makes the discrepancy sharper. [`NewBlock`:68–71](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:68) records `burialAtWall` when burial occurs. [`EligibleInLifecycle`:49](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49) tests that time; there is no issuer-fetch or persistence prerequisite. A2 expressly identifies this expression as its mechanized boundary counterpart at [155–156](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153).

Consequently, **the stated residual is not the only path**:

1. Burial occurs on time.
2. No issuer invocation observes it before sources become unavailable.
3. Step 5 eventually ends the unlatched attempt.

No killed, undurable observation is needed. Polling delay or starvation can produce the same gap.

A2’s prose also calls B the service’s observation time at [115–124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:115). That creates a refinement question between prose and model; it does not authorize silently replacing either with durable-write time. Step 10 must expose and resolve that distinction, preserving the existing property rather than proving a weaker replacement.

**ILC2-02 — High: waiting until B + lease does not drain every timely-observation write.**

[Revision:59–62](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:59) relies on the clock decision’s assumption that AWS resolves a request within fifteen minutes **of sending it** ([clock decision:27–29](/home/tony/projects/tessera/docs/decisions/2026-10-27-service-clock-tolerance.md:27)). Observation and sending are separate events.

With B = 0 and lease = 900 seconds:

| Time | Event |
|---|---|
| 0 | Poller observes qualifying evidence on time. |
| 2 | It sends the guarded latch write, then is killed. |
| 901 | Successor reads OPEN; a fresh fetch returns stale/pending evidence; expiry commits. |
| 902 | Earlier latch write resolves and fails its guard. |

The write resolved within 900 seconds of sending. Expiry occurred strictly after B + lease. Nevertheless, expiry beat a timely observation.

The guards prevent reopening the expired attempt; **they do not make the timely latch win**. The protocol needs an ordering or recovery mechanism covering observation-to-send as well as send-to-resolution. An undurable observation remains a separate problem even after that repair.

The same unresolved write can overlap a later invocation’s store operations despite reserved concurrency 1.

**ILC2-03 — Medium: calendar completion does not freeze the lowest qualifying height.**

[Step 6:75–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:75) infers that no pending calendar means the lowest qualifying height cannot change.

Counterexample:

- Every calendar proof has returned a Bitcoin attestation.
- A higher attestation has its complete pinned segment and fails a temporal conjunct.
- A lower attestation lacks its header segment.
- Recovering that segment later makes the lower attestation qualify and satisfy the predicate.

This follows directly from [profile:879–891](/home/tony/projects/tessera/docs/V1-PROFILE.md:879): qualification requires the full pinned, linked segment; an incomplete branch supplies no time fact. Header times are nonmonotone.

Step 6 becomes sound only if “complete” includes all evidence needed to establish the claimed stable selection, rather than its parenthetical “no pending calendar.” A missing header must not become permanent failure merely because calendar work finished.

**Invocation overlap and retries.** Reserved concurrency 1 caps simultaneous invocations of this poller function. Timeouts, Lambda retries, and EventBridge redelivery do not themselves bypass that cap; duplicate events remain possible and must be handled sequentially and idempotently. AWS documents both the [concurrency cap](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html) and [asynchronous retries, throttling, and duplicate delivery](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html).

The live configuration is **300 seconds**, not fifteen minutes: [main.tf:352–363](/home/tony/projects/tessera/service/issuer/infra/main.tf:352). Fifteen minutes is the write lease. Even if execution timeout became fifteen minutes against the ten-minute schedule, excess invocations would be throttled/queued; downstream requests already sent remain the relevant overlap.

The API currently still calls `settle` at [api.py:194](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:194). Removing that writer is therefore a necessary implementation change, not an existing guarantee.

**Step 7:** sound as the revised design rule. Preserve the actual qualifying evidence durably, not only its digest, and classify “incurable” against recovery using that presentation.

**Step 8:** sufficient for duplicate **end-and-allocate transitions**, provided the expected state and attempt id are evaluated atomically at commit and a failed or ambiguous write causes a reread. The existing store already uses [version CAS](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:78). This does not provide exactly-once external signing or stamping; attempt-labelled jobs and idempotent recovery still carry that work.

### Owner prechecks

| Check | Result | File:line and assessment |
|---|---|---|
| **1. Capture row** | **PASS** | [Revision:18–22](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18), [78–82](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:78) make no claim that dual-channel capture rejects attacker keys or reveals capture. [Contract:37,72–73](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) remains explicit: attacker-key receipts can pass; issuing-account capture permits issuance. |
| **2. Trigger clause** | **FAIL** | [Revision:71–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:71) does not establish the relevant antecedents: unlatched is not necessarily untimely; no pending calendar is not necessarily permanent predicate failure. |
| **3. Requester** | **PASS** | [Revision:46–51,83–86](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:46) makes no key-security claim based solely on storage or independent custody. Attempt routing and signing closure remain explicit. This is not a certification of signer requester authorization. |
| **4. Binding text** | **FAIL** | [Revision:55,66–74](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:55) introduces durable-write counting and an operating refusal policy without demonstrating compatibility with [A2:130–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130) and its cited burial-time model. An owner residual cannot amend that protection. |

Step 10 should include observation-to-send delay, delayed commits, crashes before persistence, timely burial without observation, partial header recovery, and duplicate transition retries. A green model that starts protection only at durable latch would leave the central discrepancy unchecked.

