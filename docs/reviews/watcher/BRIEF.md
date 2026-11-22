# Review brief: the detection watcher (steward, 2026-11-22)

In /home/tony/projects/tessera, review `service/watcher/` and its Terraform in `service/detect/infra/` (merged in
11b58b9), against `docs/V1-DETECTION-CONTRACT.md` (Arariwa section; D5, D6, D7 IAM, D8, D9; Status). Not deployed.
Read-only except your report. Report with severity, file:line and a concrete scenario:
1. Missed detection: any attack or fault in D5/D6/D7-IAM/D8 that the code would not alarm on (cursor skips, pagination,
   CloudTrail file discovery across regions and late delivery, time-order matching errors, a crash between finding
   and state save, a finding that fails to publish).
2. Independence and least privilege: can the watcher's role write any issuer store, or more than its own buckets, log
   and the alarm topic? Can an issuer-side principal silence or alter the watcher's state or trace records?
3. Secrets: can any finding, log line or trace record carry request content, the plaintext request key, an API key
   value, a URL, or exception text?
4. Trace records: Object Lock COMPLIANCE correctly configured and enforced on every write; retention computed
   correctly from `service/issuer/config/window.json`; written exactly once per terminal request.
5. D9: does the heartbeat alarm fire on every failure mode (Lambda error, timeout, schedule disabled, throttling)?
6. Packaging: deterministic; frozen verifier included as the issuer includes it; install-record step correct.
7. Statements in `service/watcher/README.md` and the contract Status that overstate what the code does.
Write docs/reviews/watcher/CODEX-REVIEW.md. Findings only. Pre-registered exit: the steward fixes every HIGH and
MEDIUM; one scoped confirmation if any HIGH; then deployment with the author's session.

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
