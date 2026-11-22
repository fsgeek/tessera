# Review brief: content-addressed receipt objects (steward, 2026-11-22)

In /home/tony/projects/tessera, commit 9d27fb7 (merged in cbc5e54) repairs a deployed defect: receipts were stored at a
fixed, overwritable key `result/<rid>/receipt.json` in an unversioned bucket before the guarded COMPLETE commit, so a
stale delayed put could replace a delivered receipt (`docs/reviews/amendment-12/CODEX-REVIEW-r2.md` A12-R2-03; A12
change 5, `docs/phase-0-prereg-amendment-12.md`, signed 144b9f6). Review `git show 9d27fb7` and the code it touches
(`service/issuer/tessera_issue/pipeline.py`, `api.py`, `aws.py`, `local.py`, DESIGN.md, the new tests). Read-only
except your report. Report with severity, file:line and a concrete scenario:
1. Can any client credential obtain bytes that do not hash to the durable COMPLETE record's `receipt_sha256`,
   including races between the API's check and the client's fetch of the pre-signed URL, for both the new and the
   legacy (fixed-key fallback) path? State exactly what residual remains for legacy receipts.
2. Can an already-issued production receipt (fixed key, issued before this deploys) become unretrievable when it
   should be retrievable, or retrievable when it should not (expired, refused, cleaned)?
3. Does cleanup still delete every result object of a cleaned request, in both naming forms, in the real S3 adapter?
4. Any behaviour change beyond the stated one (headers, status codes, retention, logging of URLs, Lambda memory or
   timeout risk from reading the object in the API)?
Write docs/reviews/receipt-ca/CODEX-REVIEW.md. Findings only. Pre-registered exit: if no HIGH, the steward fixes any
lower findings and deploys; a HIGH gets one scoped confirmation after its fix.

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
