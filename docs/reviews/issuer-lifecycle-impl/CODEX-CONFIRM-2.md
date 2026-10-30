**Verdict: not ready for deployment work, even with the step-5 gate closed.**

Validation: **205 passed in 130.95 seconds**. Seven additional probes passed by reproducing defects. Fourteen targeted mutations were detected: five repair mutations, eight client-guard bypasses, and `GATE`. No repository edits or git writes.

Evidence: [additional probes](/tmp/tmp.iALl276cQE/test_round2.py), [results](/tmp/tmp.iALl276cQE/round2-final.log), [suite](/tmp/tmp.iALl276cQE/suite.log), [mutations](/tmp/tmp.iALl276cQE/mutations.log). No deployed AWS or TLC validation.

**A — Previous findings**

| Finding | Status | Assessment |
|---|---|---|
| ILC-I-01 | **PARTIAL** | The repairable KSK-configuration case is fixed. Blanket retry of row 13.5 introduces the RRSIG failure below. |
| ILC-I-02 | **PARTIAL** | Client method admission is substantially implemented. Total invocation bounds remain unestablished. |
| ILC-I-03 | **CLOSED** | The original stale-suffix probe now progresses; durable invalidation repairs that scenario. |
| ILC-I-04 | **CLOSED** | The recapture stage now evaluates impossibility before capturing. Initial capture has a separate gap below. |
| ILC-I-05 | **PARTIAL** | Held qualifying evidence is evaluated first. Calendar cursor persistence can still fail systematically. |
| ILC-I-06 | **CLOSED** | The reported classification, refusal-reason, and pre-allocation-content descriptions are reconciled. The new deadline claims have separate defects. |

I reran the original probe file: **8 passed, 4 failed**. Those four failures are old defect-reproduction assertions whose observed behavior has changed as intended. The old raw fake-signer probe still produces 320 seconds because its replacement `send` bypasses the deployed adapters; it does not establish an SQS guard bypass.

**B/F — Findings**

1. **ILC-I2-01 — High: the deadline guard does not establish “never overrun.”**

   [aws.py:222](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:222), [ots.py:314](/home/tony/projects/tessera/service/issuer/tessera_issue/ots.py:314), [dns.py:153](/home/tony/projects/tessera/service/issuer/tessera_issue/dns.py:153), [deadline.py:64](/home/tony/projects/tessera/service/issuer/tessera_issue/deadline.py:64).

   The client-call search found guarded entry points for DynamoDB, S3, SQS, SNS, calendar, explorer, and resolver requests. **It did not establish that every blocking operation is guarded:**

   - **S3:** `get_object` returns before `Body.read()`. The guard has already reset `CALL_TIMEOUT`; body consumption is outside it. A simulated body read advanced the invocation by **400 seconds**.
   - **HTTP:** `urlopen` and buffered `read(65536)` can perform multiple blocking reads without revisiting the total deadline. A real local server dripping bytes took **0.416 seconds with a 0.1-second total configured**.
   - **DNS:** the remaining time is reused across successive blocking operations. UDP send/receive share one timeout; TCP `sendall` inherits the connection timeout before the next `left()` check. A controlled probe consumed **1.1 seconds against a 1.0-second total**, with each operation respecting its individual allowance. Configurable hostname resolution adds another unbounded component.
   - **Pre-ship:** 30 seconds is an admission estimate, with no interruption mechanism.
   - The invocation deadline uses the integer wall clock, rather than a monotonic elapsed-time clock.

   **AWS arithmetic:** `3 × (3 + 8) + 2 × 20 = 73 seconds` correctly includes three configured attempts and conservatively allows two maximum backoffs. But connect/read timeouts are not a total-operation deadline; the arithmetic does not bound streamed bodies or all transport activity. See the [Botocore configuration reference](https://docs.aws.amazon.com/botocore/latest/reference/config.html).

   Consequently, DESIGN’s **“stall, no overrun”** envelope is demonstrated for its synthetic clients, not established for the actual transports. Lambda’s eventual hard kill is not graceful deadline enforcement.

2. **ILC-I2-02 — High: a genuinely expired snapshot RRSIG is retried forever without recapture.**

   [pipeline.py:109](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:109), [dnssec.py:288](/home/tony/projects/tessera/service/verifier/tessera_verify/dnssec.py:288), [verify.py:247](/home/tony/projects/tessera/service/verifier/tessera_verify/verify.py:247).

   I generated correctly signed snapshots valid at capture but expired at their eventual anchor time. The real verifier returned **`INVALID/RRSIG_NOT_VALID_AT_EVAL_TIME`**. Four polls retained the same snapshot in `finalize`; capture count remained **1**.

   This evaluates validity at the snapshot’s **anchored historical time**, not today’s wall time. Waiting cannot repair that signature interval.

   **Yes: this outcome needs a byte/evidence-dependent recapture path**, with impossibility assessed only when the existing presentation’s incurability is established. Classify at the necessary reason/witness level: all of row 13.5 is too broad, but blindly declaring every root-authentication failure configuration-independent would repeat the prior wrongful-discard defect.

3. **ILC-I2-03 — Medium: calendar work leaves insufficient budget to persist its progress.**

   [pipeline.py:755](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:755).

   `_upgrade` continues while at least **50 seconds** remain. Its subsequent S3 checkpoint requires **73 seconds** of admission allowance.

   With real guarded adapters and 20 pending calendars taking 20 seconds each, **three successive polls asked exactly calendars 0–11**. Each then failed the cursor write:

   > `s3.put_object: worst case 73 s, 40 s available`

   Calendars 12–19 were never reached. Changed proof bytes can likewise fail to persist. Reserve the required checkpoint writes before spending the remaining budget; the local-store cursor test misses this interaction.

4. **ILC-I2-04 — Medium: active-request enumeration can prevent every request from receiving a turn.**

   [pipeline.py:170](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:170), [aws.py:120](/home/tony/projects/tessera/service/issuer/tessera_issue/aws.py:120).

   `active()` rereads every indexed request before returning anything. The durable scheduling cursor is consulted only afterward.

   **Reproduced with 15 requests and 20-second DynamoDB calls:** three polls exhausted their budgets during enumeration; no request advanced or allocated an attempt. This occurs at the advertised per-call progress latency, rather than the disclosed 30-second slow-store limit.

   Enumeration needs resumable pagination or another bounded scheduling mechanism. Continuous signer-response work can also consume the invocation before enumeration; the request cursor does not provide fairness across those work classes.

5. **ILC-I2-05 — Medium: initial snapshot rejection still bypasses receipt classification indefinitely.**

   [pipeline.py:650](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:650).

   After stamping the receipt, `st_stamp` requires successful DNS capture before entering `evidence`. Persistent malformed captures therefore prevent evaluation of the receipt proof altogether.

   **Reproduced:** after chain progress beyond the attempt’s temporal limit, four further polls remained at `stamp`. The new impossibility check repairs *recapture after finalization*, not this initial-capture path.

   An obtainable, conclusive negative receipt should not be hidden behind successful snapshot acquisition. Snapshot impossibility may need additional evidence, but receipt classification can proceed independently.

**C — Deviations**

| Deviation | Judgment |
|---|---|
| Smaller SDK configuration | **No CF3-01 regression:** its test passes. Three total attempts means fewer opportunities to recover from transient errors than the former four. Standard retries still handle throttling, subject to retry quota; exhausted retries surface errors for later poll retries. This trades immediate resilience for shorter waits and does not itself prove a total bound. No live throttling experiment was performed. See [AWS retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html). |
| Configuration-dependent snapshot retries | Keeping KSK/reliance-period failures and header-dependent 13.4 outcomes repairable is appropriate. Treating **every 13.5 outcome** that way is defective: ILC-I2-02. |
| Six-header segment stored together | **Sound as a cache optimization:** [pipeline.py:715](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:715) checks size and linkage before using it; per-height recovery remains. It changes neither receipt eligibility nor the chain assumptions. It is not independent authentication against arbitrary store corruption. |

**D — Step-5 gate**

**Still closed.** Diagnostic failure history authorizes no ending, successor, refusal, or cleanup. The targeted `GATE` mutation fails the never-completes test. The defects above do not enable sampled-unavailability refusal.

**E — Remaining ways to stay open indefinitely outside that gate**

| Path | Assessment |
|---|---|
| Irreparable RRSIG failure retained in `finalize` | **Defect:** ILC-I2-02. |
| Calendar progress/cursor repeatedly lost | **Defect:** ILC-I2-03. |
| Enumeration or continuously replenished response work prevents scheduling | **Defect:** ILC-I2-04. |
| Initial snapshot capture repeatedly rejected | **Defect:** ILC-I2-05. |
| A stage repeatedly exceeds the available budget before its durable completion | **Stated slow-store limit**, provided described as a progress limitation; the claimed no-overrun guarantee remains defective. |
| Snapshot recapture where impossibility cannot be proved—pending proof, unobtainable MTP headers, or insufficient chain progress | **Stated limit.** Absence of an impossibility proof cannot authorize discard. |
| Latched snapshot proof never becomes usable; permanently missing preserved presentation or assembly material | **Stated external-evidence/storage limit.** Outside the unlatched step-5 ending policy. |
| Unrepaired catalog, trust configuration, verifier availability, or persistent header/presentation disagreement | **Stated operator/dependency limit.** No age-based ending is authorized. |
| Persistent store/queue failures, failed guarded commits, or stage exceptions before a terminal write | **Operational limitation**, with no general termination guarantee. Signing closure cannot complete a transition when its prerequisite reads/writes remain unavailable. |
| Chain never reaches the git precommitment depth, or initial calendars never accept a stamp | **Dependency limit before evidence processing.** No general finite completion bound follows. |

These limits may be honestly disclosed for bounded development work. Disclosure does **not** discharge [A2.3’s termination obligation](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288).

**Owner prechecks**

| Check | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | No reviewed repair claim adds attacker-key rejection or capture visibility. [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and [§4:72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72) explicitly permit attacker-key receipts after dual-channel capture. |
| Trigger clause | **PASS** | [pipeline.py:948](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:948) now requires a byte-only invalid failure and complete proof before the MTP impossibility consequence. The previous KSK trigger counterexample is repaired. |
| Requester | **PASS** | [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19) identifies the issuer’s ability to enqueue signing work; [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255) grants it. Signer authorization in deployment remains unverified. |
| Binding text | **FAIL** | [pipeline.py:110](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:110) uses an owner classification to retry incurably invalid snapshots indefinitely; scheduling defects also prevent progress with obtainable evidence. These leave [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288) unmet outside the gated policy choice. DESIGN’s disclosure supplies no registered waiver. |

