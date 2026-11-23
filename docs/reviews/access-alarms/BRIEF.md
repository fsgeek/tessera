# Review brief: access-log detections D1-D4 (steward, 2026-11-23)

In /home/tony/projects/tessera, review `service/detect/infra/access.tf` against `docs/V1-DETECTION-CONTRACT.md`
rows D1-D4 and the API stage's access-log format (`service/issuer/infra/main.tf`, `access_log_settings`). Not deployed.
Read-only except your report. With severity, file:line and a concrete scenario:
1. Would each CloudWatch Logs JSON filter pattern match the lines API Gateway actually writes for the intended event
   (THROTTLED, INVALID_API_KEY / MISSING_AUTHENTICATION_TOKEN, QUOTA_EXCEEDED, 400/413 for a key, 2xx from an
   uninvited key)? Consider string vs number values, "-" for empty, wildcard semantics, and gateway response types.
2. Missed cases the contract promises (for example a request with no key that still succeeds; status codes other than
   400/413 for malformed input; the API Lambda's own refusals like TOO_LARGE that return 413 vs 400).
3. Alarm math: period, statistic, threshold, comparison and treat_missing_data against each contract latency.
4. Statements in the contract that the alarms do not support.
Write docs/reviews/access-alarms/CODEX-REVIEW.md. Findings only. Pre-registered exit: the steward fixes HIGH and
MEDIUM findings with the smallest change (or narrows the contract), tests each pattern with `aws logs
test-metric-filter` against real access-log lines, and deploys; no further review round.

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
