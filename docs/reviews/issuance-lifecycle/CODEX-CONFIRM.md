**Verdict: not ready to implement.** The revision fixes the predicate definition, removes the early latch cutoff, and corrects the twelve-day claim. Step 3 still does not establish latch-winning atomicity; steps 4 and 6 introduce additional ways to discard protected attempts.

Review was read-only. Scratch enumeration is in [interleavings.txt](/tmp/tmp.f0QJh9236H/interleavings.txt). No repository edits or git writes were made.

### A. Confirmation of IL-01–07

Here, **CLOSED** means the revised design addresses the finding, not that implementation conformance has been established.

| Finding | Status | Assessment |
|---|---|---|
| **IL-01: eligibility definition** | **CLOSED** | [Revision:18–22](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) includes authenticated, attempt-bound evidence, six-deep burial, and all three conjuncts. This matches A2.1’s “**full three-conjunct temporal predicate**” ([A2:91–94](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:91)), A2.2’s `declared − ε ≤ anchor_time`, `anchor_time ≤ declared + δ`, and `confirmed_at ≤ declared + δ` ([A2:220–224](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:220)). A3.7.3 expressly retains “the three-conjunct temporal predicate plus the burial-depth requirement,” without requiring the whole envelope verification at ship ([A3:659–673](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:659)). |
| **IL-02: latch boundary and atomicity** | **PARTIAL** | The prohibited margin is removed at revision:47–48, 81–83. However, re-observation plus CAS does not meet “**inclusive and latch-winning**” or “**Atomicity of the latch against the expiry transition**” ([A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153)). See ILC-01. |
| **IL-03: late-observation policy** | **CLOSED** | [Revision:58–59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:58) consistently permits late-observed eligibility while open and prohibits reopening expired attempts. A2.1 says an attempt whose lag exceeds S “**may be refused**” ([A2:135–138](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:135)); refusal is optional. The policy is permissible, although its concurrency implementation remains defective. |
| **IL-04: nominal budget** | **CLOSED** | Revision:33–34, 79–80 correctly follow “a **nominal lifecycle budget**” and “**not a proven wall-clock bound**” ([A2:271–274](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:271)). |
| **IL-05: durable refusal and API** | **PARTIAL** | Revision:67–71 specifies atomic durable refusal and API delivery; revision:91 includes CL-03’s reason set. These address “**explicit refusal, durably recorded**” and refusal “**in the same step**” as final expiry ([A2:265–281](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:265)). A9.7 row 12 substitutes “**Bounded local refusal returned by the API**” ([A9:476](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:476)). But `EVIDENCE_UNAVAILABLE` lacks a safe terminal-transition rule; see ILC-03. |
| **IL-06: change inventory/public semantics** | **CLOSED** | Revision:85–105 incorporates the identified implementation, test and prose sites. Revision:78–80 withdraws misleading `fail_after` semantics. This closes the design inventory finding; it does not certify that future edits cover every dependency. |
| **IL-07: isolation and failure handling** | **PARTIAL** | Attempt isolation and signing closure are substantially addressed. Revision:64 follows A9.5: “**A retry that changes any committed byte needs a fresh stamp**”; the registered order freezes signatures before stamping ([A9:290–296](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:290)). Permanent-failure classification and post-latch discard remain underspecified; see ILC-02 and ILC-04. |

The profile was checked using `git show 270ca49:docs/V1-PROFILE.md`. Its §7.1 states:

> “T is the time of the verified attestation at the **lowest block height** in the presented OTS proof” — lines 860–862.

> “It is presentation-sensitive: a different presentation of the same receipt can select a different T.” — lines 861–862.

Qualification requires the pinned, linked `h…h+5` segment, and an incomplete branch “supplies no time or trust fact” — lines 879–888. These qualifications are central to the remaining defects.

### B. Step 3 concurrency review

**ILC-01 — High: re-observation does not make a timely observation win.**

Affected text: [revision:45–59](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:45), especially the assertion at lines 54–56.

Let L be the latching worker and E the expiring worker. Both initially read version v, OPEN.

| Interleaving or condition | Result |
|---|---|
| L observes qualifying evidence by B and commits its latch before E’s CAS | Safe: E’s CAS fails. |
| E reads first; L subsequently commits; E then tries its old-version write | Safe: E’s CAS fails. |
| L observes by B; its write stalls; E reads OPEN after B, independently fetches an older/pending proof, and commits expiry | **Violation:** L’s CAS subsequently fails. A timely-eligible attempt expires. |
| E fetches partial evidence; L has the complete pinned segment; E treats “predicate not established” as false | **Same violation.** Successful fetching is not proof of completeness or absence. |
| L crashes after timely observation but before its write; E later obtains poorer evidence | No durable observation protects the attempt. It may expire. Crash recovery is unspecified. |
| E fetches pending evidence; OTS upgrade becomes available; L fetches it by B; E delays its expiry write until after B | **Violation possible.** E’s decision is based on evidence that no longer represents what another worker observed. |
| Both independently fetch the same complete qualifying evidence | E cannot legitimately conclude false. Re-observation works in this restricted case. |
| Explorers disagree | Neither “the latest fetch wins” nor one worker’s failure establishes authoritative absence. The design gives no reconciliation rule. |
| A reorganisation shallower than six displaces a successor near the tip | It can disrupt a newly six-deep observation without removing its inclusion block. A later fetch can lack the former six-header view. Re-fetching must not silently erase the preserved authenticated observation; pin conflicts require explicit handling. |
| Workers’ wall clocks differ | One can decide “after B” while another records “at B.” The note does not define a common lifecycle clock or ordering that makes these decisions consistent. Its visibility tolerance supplies neither. |

A small exhaustive enumeration of the six read/observe/write events, constrained so L’s timely observation precedes E’s post-B fetch, produced **10 schedules; expiry won in three** when E received stale negative evidence. This is a bounded counterexample enumeration, not a model discharge.

The decisive schedule is:

```text
L reads v
L observes qualifying evidence at B
E reads v, OPEN
E reads time > B and fetches stale/pending evidence
E CAS(v → EXPIRED) succeeds
L CAS(v → LATCHED) fails
```

CAS establishes exclusive writes. It does **not** establish precedence of an earlier observation over a later terminal write. Step 3 therefore **does not meet the registered latch obligation**.

For a fixed, correctly authenticated presentation, these races do not by themselves allow a false predicate to latch: step 2 still requires it to hold. Accepting an observation after B is also expressly permitted by this design. However, the design must distinguish a valid latch on one presentation from a later, different presentation that fails.

The repair must specify how observation and terminal decisions are serialized, how pending observations survive crashes, and how stale/partial evidence is distinguished from a conclusive negative. Another CAS alone is insufficient.

**ILC-03 — High: the unavailable-evidence timeout bypasses the protection step 3 needs.**

Affected text: [revision:56–59, 67–71](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:56).

“Evidence unavailable means do not expire” permits an **unbounded wait** under an indefinitely unavailable source. Calling twelve days nominal is correct, but A2.3 still makes termination a contract obligation ([A2:288–289](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288)).

Step 6 supplies a finite operating timeout, but elapsed time alone does not establish its authorization:

- A2.1 permits refusal when the observation lag exceeds S.
- An outage at E does not establish that no worker observed eligibility by B.
- A timely observation may be pending, crashed before persistence, or durably latched elsewhere.
- Step 6 does not expressly restrict this refusal to an unlatched OPEN attempt or make it respect the latch/expiry serialization.

Consequently, **step 6 is not demonstrated consistent with A2.1 and A2.3**. A finite refusal policy can be compatible for genuinely unprotected attempts; this note does not define how it establishes that condition. It must never refuse a latched attempt merely because evidence later becomes unavailable.

### C. Discard, signing closure and shipping

**ILC-02 — High: step 4’s example does not establish permanent failure.**

Affected text: [revision:60–62](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:60).

A2.1 authorizes discard when:

> “the predicate fails **at issuance time**” — [A2:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161).

It does not make every unsuccessful evidence fetch an irrevocable failure.

A currently presented proof whose lowest qualifying height has a late timestamp can later acquire a **lower qualifying attestation**. The selected T and confirmation segment then change. With nonmonotone header times, neither height order nor one late timestamp proves every possible qualifying presentation fails.

Thus step 4 is consistent **only when permanence is actually established**. Its example, as written, establishes failure of the current presentation, not permanent failure of the attempt. It could discard an attempt for which another worker already holds timely qualifying evidence.

Signing closure in [revision:63–66](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:63) is otherwise sound: it prevents fresh signatures while preserving latched and already signed/stamped attempts that can finish. Refusal for `SIGNING_CLOSED` must occur only after the current attempt has legitimately ended and a fresh attempt would require prohibited signing.

**ILC-04 — Medium: step 7 has a valid safety exception but an overbroad discard category.**

Affected text: [revision:72–77](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:72).

Two registered constraints limit shipping:

> “a receipt ships only when complete; an operator refusal never concerns a shipped receipt” — [A9:165](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:165).

> “An attempt whose T would exceed not-after is not shipped.” — [A9:422–423](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:422).

Accordingly, **a temporal latch does not compel shipping an incomplete or otherwise prohibited receipt**. Step 7’s genuine, irreparable `T > not-after` case is consistent with the issuer invariant. Neither the temporal predicate nor A3.7.3 establishes full envelope validity.

However:

- “A verifier verdict other than `VALID_STRICT`” is not itself evidence of permanent failure.
- Missing snapshots, proofs, headers or storage objects can be recoverable.
- A different proof can select a different T; the issuer must preserve the qualifying presentation rather than replace it with a worse one and call the result incurable.
- A2.1:161–162 addresses failure of the temporal predicate, not arbitrary post-latch finalization failures.

**Step 7 honours the shipping obligation only if “permanent” means that the frozen attempt cannot be completed lawfully, including by recovering evidence and using its preserved qualifying proof.** As written, it does not establish that restriction tightly enough. A valid, complete, timely-eligible attempt must not be discarded for scheduling delay, transient dependency failure, or an avoidable change of presentation.

### D. Additional defect

**ILC-05 — Medium: terminal-state guards and retry recovery remain unspecified.**

At [revision:45–75](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:45), step 2 describes a CAS latch without explicitly requiring OPEN/current-attempt state; steps 4 and 7 do not specify equivalent guarded discard transitions. Step 5 also leaves recovery between ending attempt i and creating i+1 undefined.

Require explicit transition guards, atomic attempt allocation or idempotent recovery, and re-evaluation after CAS failure. Otherwise delayed workers can act on ended attempts, retries can duplicate, or a crash can leave the request between attempts. “An expired attempt is never reopened” states the intended invariant but does not specify its enforcement.

### Owner prechecks

| Check | Result | Evidence |
|---|---|---|
| **1. Capture row** | **PASS** | Revision:18–22, 41–44 makes no claim that dual-channel capture rejects attacker keys or reveals capture. [Contract:35–37, 72–73](/home/tony/projects/tessera/docs/V1-CONTRACT.md:35) still governs: attacker-key receipts can pass; issuing-account capture permits signing. |
| **2. Trigger clause** | **FAIL** | Revision:60–62 treats failure of one presented proof as permanent attempt failure. Revision:67–71 uses evidence unavailability as a refusal trigger without establishing absence of protected timely eligibility. Neither cited registered consequence follows from those facts alone. |
| **3. Requester** | **PASS** | Revision:41–44, 63–66 discusses attempt-labelled signature work and signing closure; it makes no security claim based solely on key location or independent signer control. This does not establish requester authorization conformance. |
| **4. Binding text** | **FAIL** | Revision:54–56 asserts a latch guarantee its mechanism does not provide. Revision:60–62 and 67–71 permit terminal outcomes without establishing their compatibility with A2.1’s protected eligibility. Owner operating numbers cannot override that registered obligation. |

