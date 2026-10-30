**Verdict: not ready to implement.** The fence repair is sound within the checked bounds, but the residual remains incomplete, and revision 5.2’s fixed interval window can prevent termination.

Review was read-only, with no repository edits or git writes. All reviewer-created files are under [scratch evidence](/tmp/tmp.nSu1oGphAh/EVIDENCE.md). Revision-5.2 files appeared during review; observations about them concern a captured, in-progress model, not completed section-7 results.

**A. Previous findings**

| Finding | Status | Assessment |
|---|---|---|
| **ILC2-01 — persistence substituted for eligibility** | **PARTIAL** | [Design:52](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:52) now preserves chain timeliness independently of persistence. However, timely eligibility can still end `EVIDENCE_UNAVAILABLE`. Acknowledging that departure does not discharge [A2.1:130](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:130) or its inclusive latch obligation at line 153. The author decision remains outstanding. |
| **ILC2-02 — observation-to-send gap defeats lease draining** | **CLOSED** | [Steps 4–5](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:57) remove lease-based negative inference and fence before fetching. Once the successor’s fence commits, the predecessor’s ending write cannot pass its version guard. The no-fence companion reproduces the race. This closes the specific ordering defect, not all lost-observation paths. |
| **ILC2-03 — calendar completion does not fix selection** | **CLOSED** | [Design:59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:59) now requires every attestation’s full pinned, linked segment. That addresses the missing-lower-header counterexample and matches the requested historical profile §7.1 at `270ca49:879–891`. |

The design correctly retains the three conjuncts required by A2.2 and A3.7.3, frozen signatures and fresh stamps under A9.5, local refusal under A9.7, and A9’s completeness and not-after checks. These are design assessments, not implementation conformance findings.

**E. New findings**

**ILC3-01 — High: residual (a) unnecessarily requires a killed invocation.**

[Design:98](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:98) names a timely observer killed before writing. But a timely observation can also be lost when its latch write is rejected, without any invocation being killed. The design itself says an uncommitted success resets nothing at [line 76](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:76).

I disabled `Kill` in scratch copies and added a reachability witness. TLC found the path in both R51 and the captured R52:

1. Eligibility is fetched at the inclusive boundary.
2. Its latch write is sent but dropped without applying.
3. Subsequent fetch failures satisfy the operating-period rule.
4. `EVIDENCE_UNAVAILABLE` commits.

The R52 trace includes committed failures in both required intervals, so the interval-set repair does not remove this path. See [R52 counterexample](/tmp/tmp.nSu1oGphAh/r52-drop/drop.out:27).

Broaden (a) to **an observed eligible presentation whose latch never commits**, including crashes, rejected writes, and failed guards. Neither source outage nor process death is necessary.

**ILC3-02 — Medium: `P5_Spread` does not establish the interval coverage attributed to it.**

[RESULTS:509](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:509) describes distinct invocation-start ticks, then equates that with no skipped scheduled tick. The actual ghost records `w.st0`, whereas the design counts the interval in which the **fetch starts**: [R51:318](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR51.tla:318).

There are two differences:

- Distinct invocation starts can have fetches in the same later interval.
- Enough distinct historical ticks do not establish coverage of every interval in a particular operating period.

A scratch probe changed only this ghost’s timestamp from invocation start to fetch start. `P5_Spread` then failed with committed failed fetches at 2 and 4, an ending decision at 4, and no failed fetch at 3: [counterexample](/tmp/tmp.nSu1oGphAh/spread-fetch.out:27).

Thus [RESULTS:635](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:635) overstates the guarantee even with one invocation start per tick. R52 begins repairing the timestamp distinction, but its checked spread property still counts distinct fetch times rather than directly asserting the required interval membership.

**ILC3-03 — High: the initial operating-period window can become permanently impossible to satisfy.**

[Design:79](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:79) needs a rule for advancing or restarting a failed coverage window. The captured R52 interpretation records only indices below `Expected`: [R52:334](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR52.tla:334). Its ending guard requires enough indices from that initial window: [R52:254](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR52.tla:254).

With period 2, interval 1, allowance 0:

- The first committed failure starts the window at 2.
- Interval `[3,4)` has no committed failure.
- All later polls fail, but their interval indices are outside the counted window.

The missing interval can never be recovered. If evidence never completes, there is neither a successful reset nor another ending path.

TLC reached an open, unburied attempt with `unavailable_since=2`, `fi={0}`, and three committed failures by time 6, without faults: [witness](/tmp/tmp.nSu1oGphAh/stranded.out:27). This is a reachability result plus a structural argument for continued nontermination, **not** a TLC liveness counterexample.

Specify a rolling window or a restart rule that preserves the coverage requirement. Parameter validation must also define partial intervals and constrain the allowance.

**ILC3-04 — Medium: the change inventory omits storage expiration that can destroy live attempt material.**

The design permits prolonged open attempts and retries transient post-latch failures indefinitely: [design:112](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:112). Existing infrastructure expires every object under `content/`, `work/`, `frames/`, and `result/` after 31 days: [main.tf:101](/home/tony/projects/tessera/service/issuer/infra/main.tf:101).

Consequently, a sufficiently delayed live attempt can lose its frozen material independently of evidence-source recovery. S3 lifecycle expiration is based on object age and matching filters; it does not consult the request’s lifecycle state. [AWS lifecycle documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html)

Add retention/lifecycle handling to the implementation inventory. The model’s durable-store abstraction hides this concrete failure.

**B. Model fidelity and property meanings**

The models faithfully represent a useful **lifecycle core**, not all steps 1–10.

| Checked claim | What it establishes |
|---|---|
| **P1 / `NoTimelyExpiry`** | Timely eligibility is protected against the modeled `expired` and `discarded` states. It explicitly excludes `unavail`; it does not prove “every timely-eligible attempt ships.” |
| **`NegativeEndsAreTrue`, `LatchIsTrue`, `ExpiryAfterB`** | Negative ends have a failing abstract verdict; latches have a passing verdict; expiry/discard decisions use the stated boundary. The three conjuncts are abstracted into `pass`, not recomputed from headers. |
| **P2 and action properties** | Current-attempt isolation, allocation ordering, one shipped attempt, and modeled state-transition protection. They do not establish exactly-once signing, stamping, publication, or delivery. |
| **P3** | Final modeled end and refusal are atomic; intermediate modeled ends allocate the next attempt atomically. |
| **P4** | Bounded termination under the stated fairness, scheduling, finite-fault and write-resolution assumptions. R51’s completed liveness run uses N=1 and modifies polling at `MaxTime`; it does not establish R52 termination. |
| **P5 / `USAfterB`** | The committed failure history and decision guards described by the formulas. Successful fetches without committed writes remain unprotected. |
| **`P5_Spread`** | The distinct-timestamp cardinality check, subject to ILC3-02—not the stronger interval-coverage claim. |
| **Residual/sanity witnesses** | Reachability or bounded unreachability of their particular ghost predicates, not completeness of the residual taxonomy. |

The fence result is useful evidence: the correct bounded run completes, the no-fence companion goes red at matching bounds, and orphaned writes are reachable. Conversely, B2 staying green is reported honestly; these properties do not require the second-writer companion to fail.

Material abstractions remain:

- **One request:** hides cross-request starvation under one 300-second poller invocation.
- **Two attestations:** covers the lower-header decoy, not arbitrary branch collections or concrete selection/authentication.
- **No reorgs:** assumes buried evidence remains permanent. Six-deep burial does not mechanically exclude deeper reorgs.
- **One clock:** hides premature or delayed period decisions from clock changes between invocations.
- **Durable atomic store:** hides lost evidence and the expiration in ILC3-04.
- **Immediate abstract assembly:** hides packaging, publication and delivery failures.
- **No signing/stamping or signing closure:** step 8’s `SIGNING_CLOSED` behavior is not checked.
- **No post-latch incurable discard:** the model’s unconditional `LatchProtects` is stronger than—and does not represent—step 7.

The last exclusion matters: a temporally eligible attempt can legitimately fail an additional shipping requirement, including A9’s not-after invariant. The model does not check that classification.

**C. Residual and B**

The residual is **not yet precise or complete**:

- Replace killed-before-write with successful observation whose latch never commits.
- State sampled failed fetches and committed records, rather than continuous evidence unavailability.
- Say **every required interval except the allowance**. [Design:104](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:104) currently drops that qualification.
- Resolve ILC3-03 before asserting sustained failure guarantees termination.

Outside `EVIDENCE_UNAVAILABLE`, step 7 can discard temporal eligibility for an incurable completeness/window failure. Signing closure prevents a necessary new attempt; it expressly does not terminate an existing latched or already signed-and-stamped attempt.

The B question is real and fairly raised: [A2:115](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:115) includes service observation-path delay, whereas [`NewBlock`:68](/home/tony/projects/tessera/formal/tla/P5cP5P6_BridgeSlack_Latch.tla:68) records burial independently of observation. Neither a green lifecycle check nor owner prose resolves that refinement.

Two qualifications are needed:

- Keep observation time, burial time, and the deadline distinct; the documents overload “B.”
- The historical path-(c) trace observes eligibility at 3 with deadline 1. Therefore [RESULTS:226](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:226) cannot call that particular observation timely. The categorical statement about (c) in [design:107](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:107) needs qualification, although the fence now closes that race.

**D. AWS implementability**

The AWS primitives are sufficient:

- Conditional version updates can implement the fence and subsequent guards. End-and-allocate can use one item update or a DynamoDB transaction. [AWS conditional writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html)
- Reserved concurrency 1, timeout 300 seconds and a ten-minute schedule are valid and already configured at [main.tf:352](/home/tony/projects/tessera/service/issuer/infra/main.tf:352). Concurrency limits invocations; asynchronous retries and duplicate delivery still require idempotence. [AWS concurrency](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html), [AWS retries](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html)
- A schedule is not proof that every request was visited in every interval. Count actual fetch starts.
- Large preserved presentations can live in immutable S3 objects, written before committing their references in the latch. DynamoDB has a 400-KB item limit and no transaction spanning DynamoDB and S3. [AWS storage guidance](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-use-s3-too.html)

Operating period and allowance can remain runbook numbers. Their permitted values and window semantics must nevertheless be specified. AWS cannot supply the missing termination rule in ILC3-03.

**Owner prechecks**

| Check | Result | Evidence |
|---|---|---|
| **1. Capture row** | **PASS** | [Design:18](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) makes no claim of attacker-key rejection or capture visibility. [Contract:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) explicitly permits attacker-key receipts after dual-channel capture. |
| **2. Trigger clause** | **FAIL** | [Design:93](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:93) cites excessive-lag refusal permission, but unlatched state plus failed polls does not establish its antecedent for previously timely-observed attempts. Disclosure at lines 105–109 correctly leaves this unresolved. |
| **3. Requester** | **PASS** | [Design:15](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:15) and [121](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:121) make no custody-only key-security claim. This does not certify signer authorization; [A9:401](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:401) explicitly recognizes queue-controller signing capability. |
| **4. Binding text** | **FAIL** | [Design:8](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:8) says registered text is unchanged, while [108](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:108) acknowledges incomplete compliance with its shipping obligation. An owner operating rule cannot authorize that departure. The author decision remains necessary. |

