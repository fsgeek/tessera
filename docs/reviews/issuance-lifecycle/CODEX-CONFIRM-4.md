**Verdict: not ready to implement the entire ungated part as written.** The lifecycle core can proceed independently of the author decision, but the proposed storage fix still permits premature deletion. Correct ILC4-01 first; the author need not decide step 5 before that work proceeds.

Review was read-only, with no repository edits or git writes. Reviewer-created material is under [scratch evidence](/tmp/tmp.aRpLH86bRI/EVIDENCE.md).

**A. Previous findings**

| Finding | Status | Assessment |
|---|---|---|
| ILC3-01 — residual requires a kill | **CLOSED** | [Design:107](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:107) covers any observed eligible presentation whose latch never commits. R53’s no-kill witness supplies the dropped-write example. |
| ILC3-02 — spread is not interval membership | **CLOSED** | R53 records fetch-start times and checks membership in the decision’s completed window. The earlier one-poll-per-tick claim is explicitly withdrawn at [RESULTS:790](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:790). |
| ILC3-03 — fixed window strands | **CLOSED for the fixed-window defect** | The window now rolls. Recovery after a gap is reachable; B8 preserves the broken fixed-window behavior. The broader termination claim needs ILC4-02’s qualification. |
| ILC3-04 — live material expires | **PARTIAL** | [Design:171](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:171) adds live-object protection, but its tagging mechanism does not establish 30-day retention after ending. |

**B. R53 spot-check**

**P5 now asserts the requested property.** [Win:267](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla:267) selects the most recent completed intervals. At the ending commit, [lines 377–381](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla:377) require enough of those intervals to contain committed failed fetches whose **fetch-start time** belongs to that interval.

The window is evaluated at `w.dec`, the ending decision time, rather than the later store-commit time. That matches the requested **decision’s window**. It does not prove continuous unavailability, protect an uncommitted success, or establish the shipping obligation.

**Allowance-1 termination is meaningful at its stated bounds.** I reproduced the original run: **19,487 distinct states, termination green**. Removing the extra MaxTime start also produced green with the same state count. Thus this particular positive result does not depend on the end-of-time relief.

Its limits remain substantial:

- N=1, Expected=2, Allowance=1, no faults, one invocation start per tick, and the stated fairness/write-resolution assumptions.
- It does not establish termination for registered N=3 or arbitrary operating periods.
- A scratch N=2 probe, restricted to permanently pending evidence, went red after allocating attempt 2 at time 4 and exhausting polling at MaxTime=7. That is a **horizon artifact**, not evidence of unbounded nontermination. A multi-attempt check needs sufficient horizon and explicit treatment of the bound.

**The companions are real broken designs.**

| Companion | Mutation and significance |
|---|---|
| **B4** | Ends after elapsed time and one failed poll, without historical window coverage or the second fetch. P5 correctly rejects it; I reproduced red. |
| **B6** | Uses a failure counter instead of interval membership. Bursts can satisfy the counter despite missing intervals. Its reported P5 failure matches the mutation. |
| **B7** | Uses the same counter design at one invocation start per tick. Fence delay still separates invocation start from fetch start. I reproduced the old spread property failing. |
| **B8** | Requires coverage of the original fixed window. A missed interval remains irrecoverable. I reproduced the exhaustive “no end after a gap” result: **488,041 states**. This is deliberately a green invariant describing broken behavior. |

[RESULTS:859](/home/tony/projects/tessera/formal/tla/issuer-lifecycle/RESULTS.md:859) accurately lists the omissions: B2, no-fence B5, sanity witnesses, one-poll residual witnesses, earlier variants, and multi-attempt termination. These omissions do not erase the checked repairs. They do mean:

- R53 has no fresh positive sanity evidence for every lifecycle outcome.
- The fence companion’s sensitivity remains inherited evidence; R53 freshly checks only the correct side.
- Storage, signer authorization, external-work idempotence, signing closure, and post-latch assembly remain outside this model’s assurance.

**C. Implementation boundary and author decision**

After correcting storage retention, these can proceed: attempt isolation, immutable attempt material, single-writer lifecycle, fencing and version guards, preserved-presentation latch, complete-negative expiry/discard, atomic end-and-allocate, atomic final refusal, and the public view.

They are common machinery for the author’s stated options. No implementation can be guaranteed immune to arbitrary future author changes, but these choices do not presuppose which obligation yields.

Exactly these behaviors must remain gated:

- Committing `EVIDENCE_UNAVAILABLE` from sampled failure.
- Ending or allocating a successor **because of that condition**.
- Final refusal, cleanup, or terminal public status derived from that condition.
- Any replacement timeout, “signing closed,” deployment deadline, or age rule that produces the same ending indirectly.
- Claims of full lifecycle compliance or guaranteed termination while this path remains disabled.

Failure-history collection can remain diagnostic. With the gate closed, incomplete evidence leaves the attempt open; final refusal still operates when N attempts have ended through permitted paths.

The author decision identifies a real conflict, but needs the qualifications in ILC4-03:

| Option | Consequence |
|---|---|
| **Shipping yields after sustained sampled failure** | An amendment authorizes ending despite potentially timely eligibility, defines the sampling rule, and accepts lost shipping opportunities. |
| **Termination yields** | Preserve open attempts and retry recovery indefinitely. This preserves the opportunity to ship; it cannot manufacture permanently lost evidence. |
| **A long operating period** | Delays the tradeoff and may reduce exposure. Any finite period retains the counterexample; length alone resolves neither obligation. Coverage parameters also need ILC4-02’s repair. |

A2.1’s permission is specifically **lag exceeds S**, not “now exceeds the deadline”:

- Under **service-observation B**, path (b) may fall outside the shipping guarantee when observation lag exceeds S. Failed samples alone do not establish that antecedent. Path (a) includes protected timely observations, but “observed before the deadline” and `B−C≤S` are not interchangeable tests.
- Under **burial-time B**, timely burial remains timely despite missing issuer observations. Later failed fetches do not establish excessive burial lag.
- Under either reading, an already protected eligibility cannot acquire refusal permission merely because persistence failed or time passed. The author should reconcile the prose/model meanings explicitly.

**D. New findings**

**ILC4-01 — Medium: tagging `ended` does not start a post-end retention clock.**

[Design:174](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:174) changes the age rule to an `ended` tag filter while promising 30 days after ending. S3’s age-based expiration remains based on object creation; an old object can become immediately eligible when tagged. [AWS lifecycle documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)

This matters for preserved presentations and results written before a delayed terminal commit. Protect live objects, then base deletion eligibility on a persisted **request-ended timestamp**. An age backstop must not undercut that retention. This is the blocker within the requested ungated scope.

**ILC4-02 — Medium: allowance ≥1 is insufficient for arbitrary operating periods.**

[Design:89–93](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:89) permits arbitrary whole-number periods with allowance ≥1. The positive model covers only two intervals.

A scratch four-interval, allowance-1 probe found termination red. Fetches at `2,2,4,4,6,6,8,8…` leave only two of every four completed intervals covered; three are required. The alternating pattern can continue beyond the finite horizon.

Constrain the supported parameters or establish a scheduling/coverage assumption sufficient for them. “Allowance at least 1” alone is not that assumption. This affects the gated path.

**ILC4-03 — Medium: the conflict paragraph overstates what waiting achieves and which residuals are protected.**

[Design:118–124](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:118) says both paths violate shipping and that never ending “does the reverse.” Under observation-time B, path (b) need not be protected. Under permanent evidence loss, waiting does not ensure shipping.

State the conflict over **protected timely-eligible cases**, distinguish retaining an opportunity from achieving shipment, and distinguish the lag test from the deadline test. The author decision remains necessary.

**Owner prechecks**

| Check | Result | File:line evidence |
|---|---|---|
| **1. Capture row** | **PASS** | [Design:19](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:19) makes no attacker-key rejection or capture-visibility claim. [V1-CONTRACT:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and §4 retain the dual-capture limitation. |
| **2. Trigger clause** | **PASS, with step 5 gated** | [Design:125](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:125) withholds implementation pending amendment. The citation at line 99 does **not** independently authorize ending; ILC4-03 requires clearer framing. |
| **3. Requester** | **PASS** | [Design:17](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:17) specifies signing/stamping order without claiming custody alone provides security. [A9:401](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:401) explicitly recognizes queue-controller signing capability. Signer authorization is not certified here. |
| **4. Binding text** | **PASS for the gated proposal** | [Design:121–126](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:121) identifies the departure and reserves authorization to an author amendment. Disabling that path does not itself discharge A2.3 termination. |

