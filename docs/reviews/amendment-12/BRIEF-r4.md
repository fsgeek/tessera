# Review brief: Amendment 12 r4 — final scoped round (steward, 2026-11-20)

This is the final round pre-registered in `BRIEF-r3.md`: it checks **only the text narrowed in r4** in
`docs/phase-0-prereg-amendment-12.md` (repository /home/tony/projects/tessera; read-only except your report), against
the r3 findings in `CODEX-REVIEW-r3.md`. Scope:
- A12.1 change 2; change 4 (all three bullets); change 5 bullets "Refusal begins with a fence" and "Access boundary
  and residual"; change 10's last sentences.
- A12.2: the inventory paragraph beginning "Found by searching"; item 4's last two sentences; item 5's first
  condition; item 6; item 8's vector introduction and the two vectors marked changed; the consequence paragraph.
For each scoped passage: does it resolve its r3 finding; is any promise in it false, unconditioned, or contradicted
by cited code or registered text (cite file:line and a failing scenario); does it introduce a new contradiction?
Do not review text outside the scope. Classify HIGHs as PROMISE or DUTY as in round 3.

Exit (pre-registered, final): after this round the steward disposes. Any remaining PROMISE HIGH is resolved by
deleting that promise (keeping only what holds) and the amendment goes to the author with all four reviews attached;
no fifth round.
Write docs/reviews/amendment-12/CODEX-REVIEW-r4.md. Findings only.

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
