# Review brief: Amendment 12 draft, sections A12.1 and A12.2 (steward, 2026-11-17)

Review `docs/phase-0-prereg-amendment-12.md` sections A12.1 (bounded termination) and A12.2 (successor windows) in
/home/tony/projects/tessera. Read-only except your report. Sections 3–5 are placeholders; ignore them.

Check, with severity, file:line and a concrete failing scenario:
1. Does each change quote and correctly locate the registered text it changes (A2 `:135-138`, `:271-289`; A9
   `:405-423`), and does it contradict any other registered sentence (A1–A11, the freeze `formal/freeze-v1/`, the
   frozen profile `docs/V1-PROFILE.md`, `formal/p8/`) that it fails to list?
2. A12.1: is "acceptance + 14 days" coherent with A2.3's nominal budget, the window's acceptance and signing stops
   (L1: acceptance stops 216 h before not-after, signing 96 h), and the lifecycle decision rev 5.3.1
   (`docs/decisions/2026-10-29-issuance-lifecycle.md`)? Any path where a request still never terminates, or where a
   receipt could ship after L_term? Is the standing statement (point 3) consistent with A2.1 and A2.4?
3. A12.2: does sequential replacement as written satisfy A9's own conditions (same owner and path, new keys,
   next.not-before > previous.not-after, the dated rotation registration with vectors and a model) and the frozen
   verifier (DNS_RRSET, DNS_OWNER, ISSUANCE_WINDOW, C4 pre-commitment)? Is there a window of time in which neither
   or both records are valid in a way that harms a receipt?
4. Anything that should be an author decision rather than the steward's (irreversible or scope-changing).
Write docs/reviews/amendment-12/CODEX-REVIEW.md. Findings only.

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
