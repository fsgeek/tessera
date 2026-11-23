# Review brief: first verifier release candidate and its sheets (steward, 2026-11-23)

In /home/tony/projects/tessera review `service/verifier/release/release_tool.py`, `docs/ceremony/sign-release.sh`,
the `install.sh` release mode, `docs/V1-RELEASE-PROCEDURE.md`, `docs/releases/v1-1/SUMMARY.md` and the two sheets
`docs/ceremony/release-REHEARSAL-SHEET.md`, `docs/ceremony/release-v1-1-SHEET.md`, against the frozen profile
(`docs/V1-PROFILE.md` §15.9 release format, §5 header pins), A10.4.2 and row 36, and
`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`. Read-only except your report; no network, no keys. With severity, file:line and
a concrete scenario:
1. Can the archive be built non-reproducibly, or can the sheet's hash comparison pass while different bytes are signed?
2. Can a TEST-signed release, a modified part, or a wrong trust file or catalog be accepted by acquisition or install?
3. Does each sheet step do what it says on Tails, with explicit pass strings and failure rules, and could the author be
   led to sign something other than the approved archive, or to bring networked media into the signing session?
4. Does the summary trace every hash to the freeze record correctly? Is any statement in the procedure or summary
   stronger than the code or the registered text?
Write docs/reviews/release-v1-1/CODEX-REVIEW.md. Findings only. Pre-registered exit: the steward fixes HIGH and MEDIUM
with the smallest change; one scoped confirmation only for a HIGH that touches what gets signed; then the rehearsal.

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
