# Scoped confirmation: receipt fix after the HIGH (steward, 2026-11-22)

In /home/tony/projects/tessera, commit 4154be5 answers `docs/reviews/receipt-ca/CODEX-REVIEW.md`. Review ONLY `git show 4154be5`
and the code it touches. Dispositions: HIGH (legacy fallback unreachable, 403 -> 502): the fallback is removed; receipts
issued before the change are copied to their digest names by `service/issuer/tools/migrate_receipts.py` (run before
and after the deployment), and the API role gains s3:ListBucket for prefix `result/*` so a missing object is 404 ->
410. MEDIUM (legacy hash check covers the API read only): moot without the fallback; the API no longer reads the body
and relies on digest naming plus S2's client check. MEDIUM (whole-object read): removed. Binding text: only digest
names are served, as A12 change 5 says.
Report CONFIRMED / PARTIAL / NOT FIXED for each, with file:line and a concrete scenario, and check the migration tool:
can it overwrite, delete, copy bytes that don't match the COMPLETE record, or miss a pre-change receipt that should be
retrievable? Is the IAM condition correct for HeadObject 404 behaviour? Read-only except your report.
Exit (pre-registered): this is the one scoped confirmation; the steward then fixes any named item and deploys.
Write docs/reviews/receipt-ca/CODEX-CONFIRM.md. Findings only.

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
