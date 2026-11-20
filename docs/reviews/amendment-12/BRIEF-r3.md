# Review brief: Amendment 12 r3, sections A12.1 and A12.2 (steward, 2026-11-20, round 3)

Re-review `docs/phase-0-prereg-amendment-12.md` sections A12.1 and A12.2 in /home/tony/projects/tessera. Read-only
except your report. Sections 3-5 are placeholders; ignore them. r1 and r2 findings are in `CODEX-REVIEW-r2.md` and
`docs/reviews/amendment-12/CODEX-REVIEW-r1.md` and r3's finding map is at the end of the amendment. Two former author
choices are resolved (`DISPOSITION.md`, "Resolution"): do not re-raise them as choices; do check they are registered
honestly and completely.

Do not only confirm r1's instances: sweep the class. Check, with severity, file:line and a concrete failing scenario:
1. Every registered sentence changed is quoted and correctly located (A1-A11, `formal/freeze-v1/`,
   `docs/V1-PROFILE.md`, `docs/V1-CONTRACT.md`, `docs/V1-SERVICE-RESOLUTIONS.md`, `formal/p8/`), and no unlisted
   registered sentence is contradicted.
2. A12.1 change 4: do the cited code locations actually implement single-writer, compare-and-set, fencing and the
   COMPLETE-only delivery the text claims (`service/issuer/`)? Find any path where a receipt is delivered, or its
   object remains retrievable, for a request that ends REFUSED; any path where neither terminal state can be
   recorded under the stated availability assumption; and whether the tie rule as worded can be implemented with
   the clocks the issuer has.
3. A12.2: does drain-then-replace remove r1's A12-05 stranding without a new one? Are item 7's vectors exactly the
   predicates the frozen verifier checks? Is the gap in item 6 and the consequence paragraph computed correctly
   from `service/issuer/config/window.json` and L1?
4. Anything that is irreversible or scope-changing and therefore an author decision.
Write docs/reviews/amendment-12/CODEX-REVIEW-r3.md. Findings only. Pre-registered exit (round 3): classify each HIGH as PROMISE (a registered promise that is false or unconditioned) or DUTY (an implementation duty that is underspecified). If no PROMISE HIGH remains, the steward disposes of the rest and the amendment goes to the author for signing, with the duties carried as gates before the bound is enabled. A PROMISE HIGH means the steward narrows that promise further and one final, scoped round checks only the narrowed text. Sweep the class r2 found: every sentence that describes present code or a present guarantee must match the code cited, or be marked as a future duty.

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
