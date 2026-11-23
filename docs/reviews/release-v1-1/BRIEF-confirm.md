# Scoped confirmation: release v1-1 after fixes (steward, 2026-11-23)

In /home/tony/projects/tessera, commits f2511c0 and ae80a5b (merged) answer `docs/reviews/release-v1-1/CODEX-REVIEW.md`;
dispositions in `docs/reviews/release-v1-1/DISPOSITION.md`. Note the changed premise for H1: the freeze commit is not
signed by YubiKey A (every repository commit is signed by the NUC commit key); the baseline is now `b134cdf`, rooted in
its OpenTimestamps proof (block 973240), plus one printed diff the author reads and reproduces on the Pangolin.
Review only those commits and the files they touch. Read-only except your report; no network, no keys.
For H1 and H2 (both touch what gets signed or accepted): CONFIRMED / PARTIAL / NOT FIXED, file:line, concrete
scenario. Can the author, following the production sheet, sign bytes other than those he rebuilt from the approved
baseline and diff? Can acquisition accept bytes other than those gpgv authenticated? Is the time-rooted baseline
stated honestly (what it catches, what it does not)? Briefly confirm the MEDIUMs. Exit (pre-registered): the steward
fixes any NOT FIXED with the smallest change; then the rehearsal. No further round.
Write docs/reviews/release-v1-1/CODEX-CONFIRM.md. Findings only.

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
