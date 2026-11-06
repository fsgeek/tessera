# Confirmation brief 3: key ceremony revision 4 (owner, 2026-11-06)

`docs/ceremony/CEREMONY.md` is now revision 4, after your `CODEX-CONFIRM-2.md`. Read-only except your report. Check:
(1) F01: S8 now reads the raw UIF value with `gpg-connect-agent 'SCD GETATTR UIF-1' /bye`, expecting `S UIF-1 %02%20`.
From the GnuPG 2.4 scdaemon source (app-openpgp.c getattr for UIF-1/2/3, and how assuan percent-escapes status
data), will this return the card's raw DO D6 bytes unaltered, so that 02 means permanent? Cite source lines. The
author's rehearsal 2 will test it on the real stack; tell us what output to expect and what would falsify it.
(2) F03: the card-only boot now sets B and FPR. (3) The new "Rehearsal 2" and "Sticks" sections: any step that
would leave the real ceremony's backup sticks or out stick in a bad state, or any way the dress rehearsal fails to
exercise a step the real ceremony depends on. (4) Any remaining HIGH finding. Write docs/reviews/ceremony/CODEX-CONFIRM-3.md.

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
