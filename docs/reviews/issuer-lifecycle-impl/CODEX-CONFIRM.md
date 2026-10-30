**Verdict: not ready for deployment work, even with the gate closed.**

Validation: **182 passed in 103.92 s**. My adapted original probes and additional adversarial probes: **12 passed**, including assertions reproducing the remaining defects. Four supplied mutations—`NOPRUNE`, `ILI04`, `ILI07_RAW`, and `GATE`—each caused the targeted test to fail.

No repository edits or git writes. Scratch evidence: [probes](/tmp/tmp.lgKk0SQtBY/test_confirmation.py), [results](/tmp/tmp.lgKk0SQtBY/probes3.log). I did not rerun TLC or validate deployed infrastructure.

**A — Original findings**

| Finding | Status | Assessment |
|---|---|---|
| ILI-01 | **PARTIAL** | Contradiction, transaction-shape, signature, and frozen-git cases are repaired. Dependency classification still mishandles snapshot trust failures; ILC-I-01. |
| ILI-02 | **PARTIAL** | An impossibility path exists, but its predicate is insufficient and some execution paths never reach it; ILC-I-01/04. |
| ILI-03 | **CLOSED** | Complete all-contradicted evidence is classified invalid; pending evidence remains open. |
| ILI-04 | **CLOSED** | Durable signatures reconcile before closure. Independently reproduced. |
| ILI-05 | **PARTIAL** | Ordinary slow-header progress works. Invocation bounds and progress under recovery remain defective; ILC-I-02/03/05. |
| ILI-06 | **CLOSED** | Shipping with subsequently available lower headers is covered; `NOPRUNE` now fails that test. |
| ILI-07 | **CLOSED** | External oversized reasons are bounded and referenced separately; disabling bounding fails the test. |
| ILI-08 | **CLOSED** | Initial content check precedes allocation; later loss uses recovery or atomic end-and-refuse. Documentation qualifications remain below. |
| ILI-09 | **CLOSED** | The original FAILED/margin/“always” statements are corrected. New documentation inconsistencies remain; ILC-I-06. |

**E — Findings**

1. **ILC-I-01 — High: `SNAPSHOT_IMPOSSIBLE` can discard a repairable, timely-anchored snapshot.**  
   [pipeline.py:847](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:847), [pipeline.py:877](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:877), [pipeline.py:948](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:948).

   Row **13.5 depends on trust configuration**, as well as snapshot bytes. I retained an originally timely snapshot, advanced the chain beyond the MTP threshold, and changed only the configured KSK interval. The real verifier returned `KSK_OUTSIDE_RELIANCE_PERIOD`; the issuer discarded attempt 1 as `SNAPSHOT_IMPOSSIBLE`. Restoring the configuration and testing the original attempt produced **COMPLETE**.

   MTP excludes new timely anchors. It does **not** establish that an existing anchored snapshot cannot become lawful after configuration or evidence repair. Likewise, “no pending calendar” alone does not establish the required incurability. Separate configuration-dependent failures and prove the existing presentation cannot be repaired before discarding.

2. **ILC-I-02 — High: the budget does not bound an invocation to 300 seconds.**  
   [pipeline.py:144](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:144), [pipeline.py:280](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:280), [pipeline.py:299](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:299), [pipeline.py:518](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:518).

   Four signing sends taking 80 seconds apiece produced a **320-second poll**, without other costs. The AWS configuration permits four attempts per call. Signing sends have no budget checks; neither do individual response processing, full active-request enumeration, or cleanup operations.

   Header costs also omit checkpoint storage calls, assume exactly two explorers although the adapter accepts more, and treat HTTP timeouts as complete work-unit bounds. The 30-second pre-ship allowance is an assertion rather than an enforced limit. A 60-second reserve does not cover these unbounded sequences.

3. **ILC-I-03 — Medium: checkpoint recovery can livelock on a stale suffix.**  
   [pipeline.py:675](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:675).

   With a stale cached header at `h+4`, linked-header validation fails and the fresh pass restarts at `h`. Under the original 12-second/request explorer conditions, each invocation refreshes only `h..h+2`. The next invocation restarts that same work.

   **Reproduced for six polls:** the stale height was never fetched; the attempt remained at `evidence`. Recovery needs durable invalidation or a durable refresh position, so completed refresh work advances toward the inconsistent suffix.

4. **ILC-I-04 — Medium: snapshot rejection can bypass the impossibility path indefinitely.**  
   [pipeline.py:604](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:604), [pipeline.py:966](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:966).

   `_snapshot_impossible` runs only after finalization reaches a snapshot-related verifier failure. Once stage `snapshot` repeatedly rejects captured DNS material, it never reaches that check—even after the MTP threshold is exceeded.

   **Reproduced:** a late, complete snapshot first caused recapture; after further chain progress, persistent malformed captures left the attempt latched at `snapshot`. This exceeds DESIGN’s example of bad DNS remaining open *while MTP has not passed* the limit.

5. **ILC-I-05 — Medium: pending-calendar work can starve already qualifying receipt evidence.**  
   [ots.py:191](/home/tony/projects/tessera/service/issuer/tessera_issue/ots.py:191), [pipeline.py:730](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:730).

   Upgrades revisit pending branches in the same order before header selection. With twelve pending calendar requests taking 20 seconds each, every invocation consumes its budget before selection—even though the proof already contains a qualifying, timely Bitcoin branch.

   **Reproduced across three polls.** Request round-robin does not provide fairness within a request. Preserve an upgrade cursor and allow eligibility evaluation independently of exhausting pending-calendar work.

6. **ILC-I-06 — Low: operational descriptions and CL-03 are not fully reconciled.**  
   [DESIGN.md:164](/home/tony/projects/tessera/service/issuer/DESIGN.md:164), [DESIGN.md:169](/home/tony/projects/tessera/service/issuer/DESIGN.md:169), [V1-CLARIFICATIONS.md:38](/home/tony/projects/tessera/docs/V1-CLARIFICATIONS.md:38).

   - Classification selects an invalid frozen check preferentially, rather than necessarily the first failing check.
   - “Every UNVERIFIABLE result” is retried is inaccurate for snapshot rows, which can lead to discard.
   - CL-03’s attempt-cause list omits direct `SIGNING_CLOSED` and `CONTENT_UNAVAILABLE` causes emitted at [pipeline.py:494](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:494).
   - “Upload never completed” is narrower than the implemented pre-allocation failure: a completed upload subsequently lost before allocation also produces FAILED.

**B — Deviations**

| Deviation | Judgment |
|---|---|
| **1. Prune contradicted branches and ship** | **Sound for the resulting presentation.** Profile §7.1 and verifier row 11.3 reject a contradiction remaining in the presented proof; they do not require presenting every acquired branch. The repaired proof is rechecked. This changes presentation bytes and can change an unpruned presentation’s verdict from INVALID to VALID_STRICT. It leaves `A_sig` and the receipt identifier unchanged and removes no presentation a holder could construct by the same pruning. |
| **2. MTP impossibility proof** | **Sound as a conditional bound on new anchors; insufficient as implemented for overall impossibility.** Along a consensus-valid retained chain, MTP is nondecreasing, so the bound excludes future anchors satisfying row 13.7. Existing snapshot repair remains possible—ILC-I-01. Require the checkpoint to survive: “no reorg deeper than 6” is too loose if it permits removing exactly six blocks; the contract excludes reorganizations of **6 or more**. The assumptions are substantially stated in the code and A1.6, but DESIGN should state them explicitly. |
| **3. Frozen / snapshot / retry rows** | **Not wholly correct.** The added frozen cases repair the reported gaps, but row 13.5 cannot be classified solely as replaceable snapshot material. Its configuration-dependent outcomes require separate handling. |
| **4. Budget/checkpoint/cursor** | **Insufficient.** Cursor-before-work improves fairness among a finite set of requests, provided enumeration completes. It does not prevent invocation overruns, checkpoint-refresh livelock, or calendar starvation. |
| **5. Reason codes versus CL-03** | **Main new codes match; the exhaustive description still needs correction.** See ILC-I-06. Naming a reason does not establish its discard predicate. |

**C — Step-5 gate**

**Still closed in the reviewed implementation.** Diagnostic failure history does not authorize an ending; there is no sampled-unavailability refusal, age deadline, or signing-closure substitute for ending stamped/latched attempts. The `GATE` mutation is detected.

The wrongful snapshot discard above is a separate incurability-classification defect, not evidence that sampled-unavailability policy has been enabled.

**D — Other termination gaps**

**Yes.** ILC-I-03 and ILC-I-05 can prevent progress despite obtainable qualifying evidence. ILC-I-04 can retry indefinitely without evaluating an available impossibility argument. These extend beyond DESIGN’s stated concern that impossibility cannot be proven.

**Owner prechecks**

| Check | Result | Evidence |
|---|---|---|
| **1. Capture row** | **PASS** | Reviewed repair claims add no attacker-key rejection or capture visibility. [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72) remain controlling: attacker-key receipts can pass after dual-channel capture. |
| **2. Trigger clause** | **FAIL** | [pipeline.py:949](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:949) applies incurable-discard consequences without establishing that the existing snapshot is incurable; reproduced by ILC-I-01. Signing-closure’s original trigger defect is repaired. |
| **3. Requester** | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer’s enqueue capability; [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255) grants it. Absence of signing credentials does not establish resistance to unauthorized signing requests. Deployed signer authorization remains unverified. |
| **4. Binding text** | **FAIL** | The implementation’s blanket snapshot predicate contradicts the incurability condition at [lifecycle decision:143](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:143). Progress failures outside the gate also remain against [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288); owner documentation does not waive that registered obligation. |

