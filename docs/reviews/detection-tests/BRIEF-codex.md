# Review brief: the detection test plan and code (steward, 2026-11-23)

In /home/tony/projects/tessera, review `docs/reviews/detection-tests/PLAN.md` and `service/detect/tests-live/`
(written by Gemini 4 Neon from `docs/reviews/detection-tests/BRIEF-gemini.md` r4; not yet run; no AWS calls made).
Read-only except your report. With severity, file:line and a concrete scenario:
1. **Safety first.** Can any code path, argument, retry, cleanup or error path modify, delete, disable, or invoke
   with side effects a production resource (anything `tessera-v1-*`, `alias/tessera-v1-kms`, the production trail,
   the results bucket, the request table, the alarm topic's policy or existing subscription), act outside us-east-2,
   exceed the API rate rule, submit a request that would be accepted for issuance, or write a credential, key or URL
   to output? Check that the guards in `safety.py` are actually applied on every mutating call, not only some.
2. Cleanup: does every created resource reach the ledger before it is created or immediately after, and is it removed
   (or KMS-scheduled) on every exit path including crash recovery? Can cleanup ever target a non-test resource?
3. Plan fidelity: does each PLAN.md row state the contract's promise accurately (D1-D4 from "D1-D4 as built"), with
   the correct latency standard per endpoint, correlating identifiers, and an honest evidence class? Any row whose
   pass would establish less than it claims?
4. Do the tests, as coded, perform what the plan says, and would a FIRED result actually be observed (SNS test
   subscription and the steward's mailbox read) and correlated by identifiers?
5. The opt-ins (`--include-quota-exhaustion`, `--include-cloudtrail`, `--include-iam-access-key`): exactly what does
   each do, and what is its worst case if it fails midway?
Write docs/reviews/detection-tests/CODEX-REVIEW.md. Findings only. Pre-registered exit: the steward fixes every
safety finding (any severity) and HIGH/MEDIUM fidelity findings, with the smallest change; one scoped safety
confirmation if any safety finding was HIGH; then the author decides on running it.

# Owner prechecks, run by the reviewer

> **Status: OWNER PROCESS, 2026-10-27.** Every owner instance has written these down as lessons and then repeated
> the mistakes (the 2026-10-19 stone, and its 2026-10-27 postscript "Naming it did not stop it"). The author's
> answer to "what do new owners get wrong in their first week": *"that they will behave differently from the prior
> instances."* So these checks are not left to the owner's self-review. The owner appends this file verbatim to
> every review brief (Codex or another family), and the reviewer reports each check as PASS or FAIL with file:line.

## Checks

1. **Capture row.** For every plain-language statement of what holds, what happens when an attacker controls both
   authority channels (DNS and git)? If the text implies that the attacker's own keys are rejected, or that a
   capture is detected or made visible, that is FAIL. Ground truth: `docs/V1-CONTRACT.md` §2 (after G10) and §4.
2. **Trigger clause.** For every registered rule cited as authority (an amendment section, a table row, a ruling),
   did the rule's trigger condition actually occur? Citing a consequence whose trigger has not happened is FAIL.
3. **Requester.** For every security claim about keys or signing, who can cause a signature to be made? A claim
   that reasons only about where a key is stored, and not about who can submit work to the signer, is FAIL.
4. **Binding text.** For every sentence the document treats as a requirement, is it registered (a signed amendment,
   the freeze, or a recorded author ruling), or is it something an instance wrote? An unregistered sentence used as a
   requirement is FAIL. Since 2026-10-27, `docs/V1-SCHEDULE.md`'s ruling budget is a known instance of this. Also FAIL: an owner
   requirement (a resolution, a design document, a code constant) that contradicts a registered sentence. Since
   2026-10-29, S4's 24-hour FAILED against A2.3's per-attempt `declared + δ + S` expiry is the known instance.
