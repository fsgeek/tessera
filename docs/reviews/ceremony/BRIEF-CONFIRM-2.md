# Confirmation brief 2: key ceremony revision 3 (owner, 2026-11-04)

Your confirmation `docs/reviews/ceremony/CODEX-CONFIRM.md` (F01–F05, and residuals of C02, C03, C04, C06) covered
revision 2. `docs/ceremony/CEREMONY.md` is now revision 3. Read-only except your report. For each of F01–F05 and
each residual, say whether revision 3 resolves it, citing lines. Report any new defect with severity and a concrete
failing scenario. Check especially: the `--with-colons` `uif:` field meaning on GnuPG 2.4.x (is the first value the
signature slot, and is 2 permanent?); the in-session restore test in S5 step 4 (separate GNUPGHOME, agent handling,
passphrase prompt, cleanup) and whether it can disturb the original key; the exact-mount and mapper check in S5;
whether every shutdown path in the failure table now preserves at least one proven copy; and the Session 2 commands
as literally written. Write to docs/reviews/ceremony/CODEX-CONFIRM-2.md.

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
