# Scoped confirmation: watcher review dispositions (steward, 2026-11-22)

In /home/tony/projects/tessera, commit 76d3f9b (merged in ac7012f) answers `docs/reviews/watcher/CODEX-REVIEW.md`;
dispositions in `docs/reviews/watcher/DISPOSITION.md`. Review ONLY `git show 76d3f9b` and the code it touches. For
each finding H1-H4, M1-M9, L1 report CONFIRMED / PARTIAL / NOT FIXED with file:line and a concrete scenario; for
NARROWED items, check that the narrowed README/contract statement is now true of the code. Sweep the class for H4:
any path where a secret or exception text reaches the log, SNS, the outbox, state or a trace. Check also that no
change weakens a detection that was correct before. Read-only except your report.
Exit (pre-registered, final for this module before deployment): the steward fixes any NOT FIXED item and any new
HIGH and runs the suites; no further round before deployment; the gate's item-3 tests (another family) follow.
Write docs/reviews/watcher/CODEX-CONFIRM.md. Findings only.

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
