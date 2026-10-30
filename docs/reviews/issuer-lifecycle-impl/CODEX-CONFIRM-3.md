**Verdict: not ready for deployment work, even with the gate closed.** One scheduling defect remains with obtainable signer responses; it is separate from permanent-dependency limits awaiting the author.

Validation: **216 passed in 131.49 seconds**. All eight targeted mutations were detected, including `GATE`. Three independent probes passed, reproducing the cold-start defect, checking timely snapshot capture, and measuring drain-share overshoot. No repository edits or git writes; scratch is in [/tmp/tmp.pyt6bZDeCk](/tmp/tmp.pyt6bZDeCk).

| Previous finding | Status | Assessment |
|---|---|---|
| ILC-I2-01 | **CLOSED under the owner decision** | S3 body consumption is inside the guard; elapsed timing is monotonic. HTTP/DNS/SDK total-time bounds remain stated limits, not established guarantees. |
| ILC-I2-02 | **CLOSED** | Expired anchored RRSIG intervals now cause recapture or reach the impossibility proof. Configuration-dependent failures remain retryable. |
| ILC-I2-03 | **CLOSED** | Calendar work reserves a checkpoint write. The guarded-adapter regression reaches every calendar. |
| ILC-I2-04 | **PARTIAL** | Paged enumeration and request-work allocation repair the original probes. Signer-slot fairness fails across cold starts. |
| ILC-I2-05 | **CLOSED for the reproduced defect** | Rejected captures no longer trap receipt processing in `stamp`; a latch without a snapshot enters capture processing. |

The original seven round-2 probes produced **five failed defect-reproduction assertions and two passes**: the five repaired behaviors changed; the accepted HTTP/DNS limits remain reproducible.

**ILC-I3-01 — Medium, DEFECT: signer-slot fairness depends on container reuse.**

[pipeline.py:364](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:364) stores `drain_turn` only on the issuer object. A cold start reconstructs the signers in KMS-first order at [lambda_app.py:46](/home/tony/projects/tessera/service/issuer/tessera_issue/lambda_app.py:46).

With continuously replenished KMS responses and SQS calls taking 20 seconds, I reset only that volatile rotation between polls, retaining stores and queues. After **eight cold-start-equivalent polls**:

- Both KMS signatures were recorded.
- Both valid GPG responses remained queued.
- The request remained in `signing`.

One warm continuation immediately serviced GPG and advanced the request to `stamp`. This distinguishes scheduling starvation from dependency failure.

The one-third allocation protects request work from continuous draining, but does not ensure fairness **between signer queues** across cold starts. Persist the starting slot or give each slot an independent opportunity before allowing one queue to consume the drain allocation.

Evidence: [probe](/tmp/tmp.pyt6bZDeCk/test_third.py), [output](/tmp/tmp.pyt6bZDeCk/third.log).

**ILC-I3-02 — Low, documentation: “at most a third” overstates the drain allocation.**

[DESIGN.md:224](/home/tony/projects/tessera/service/issuer/DESIGN.md:224) says draining may use “at most a third.” The checks at [pipeline.py:375](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:375) occur between response-processing units, without reserving their remaining cost.

A probe using 60-second SQS calls spent **120 seconds draining against a 96.67-second share**. Describe this as a cooperative allocation checked between units. This is a precision correction, not a reinstatement of the withdrawn total-time guarantee.

The other mechanisms and gate:

- **No-snapshot impossibility:** sound under the existing header/chain assumptions. [pipeline.py:1043](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:1043) requires neither a stored snapshot proof nor a committed snapshot reference before using `NO_SNAPSHOT`; the MTP test then excludes future timely anchors. With MTP still permitting a timely anchor, my independent probe captured a snapshot and advanced to `finalize`. I found no premature discard in this path.
- **Paged enumeration:** the DynamoDB continuation token and durable request position repair the original enumeration starvation. Position advances before request work.
- **Gate:** **still closed**. Diagnostic failure history authorizes no sampled-unavailability ending. The `GATE` mutation failed the never-completes test and four other lifecycle tests.
- **Remaining endings:** I found no additional wrongful-ending defect in the examined paths. The cold-start starvation is the remaining demonstrated implementation defect; permanent dependency failures remain unresolved author-policy cases.

**DESIGN’s termination disclosure is honest**, at [DESIGN.md:187](/home/tony/projects/tessera/service/issuer/DESIGN.md:187): the limits explicitly leave A2.3 unmet, disclosure discharges nothing, and [DESIGN.md:247](/home/tony/projects/tessera/service/issuer/DESIGN.md:247) keeps the ending policy gated. It needs the drain wording correction above and disclosure or repair of ILC-I3-01.

| Owner precheck | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | The reviewed lifecycle changes add no attacker-key rejection or capture-visibility claim. Dual-channel capture still permits attacker-key receipts: [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37), [72](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72). |
| Trigger clause | **PASS** | Snapshot discard requires the byte-dependent/completeness conditions or actual absence of a snapshot, plus the MTP exclusion: [pipeline.py:1040](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:1040). |
| Requester | **PASS** | The design identifies the issuer as the signing-work requester: [DESIGN.md:19](/home/tony/projects/tessera/service/issuer/DESIGN.md:19); IAM grants queue submission at [main.tf:255](/home/tony/projects/tessera/service/issuer/infra/main.tf:255). Live signer authorization remains unverified. |
| Binding text | **FAIL** | Volatile queue rotation can prevent progress despite obtainable responses: [pipeline.py:364](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:364). The permanent-dependency decision supplies no waiver for this scheduling defect against [A2.3:288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:288). |

Logs: [suite](/tmp/tmp.pyt6bZDeCk/suite.log), [prior probes](/tmp/tmp.pyt6bZDeCk/old-probes.log), [mutations](/tmp/tmp.pyt6bZDeCk/mutations.log). No deployed AWS or TLC validation was performed.

