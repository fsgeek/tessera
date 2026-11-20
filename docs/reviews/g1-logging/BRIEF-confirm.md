# Confirmation brief: G1 logging fixes (steward, 2026-11-20)

In /home/tony/projects/tessera, commit 6ca08e2 (merged on main) answers the findings in
`docs/reviews/g1-logging/CODEX-REVIEW.md`. For each finding, report CONFIRMED (fixed), PARTIAL, or NOT FIXED, with
file:line and a concrete scenario where not fixed. Sweep the class, not only the instances: (1) any path by which
exception text, request content, a pre-signed URL, a credential, or a signer-supplied free string reaches any emitted
line (check every `note`, `emit` and logging call and every argument type, including strings built from exceptions by
callers); (2) any path by which a logging failure changes control flow, a return value, or an exception; (3) any
committed transition without a line, or a line without a commit. Also check that mapping unknown signer reasons to
UNRECOGNIZED_REASON (`KNOWN_SIGNER_REASONS`) matches every reason both signers can emit (service/signer-kms,
service/signer-gcp) and changes no other protocol behaviour. Read-only except your report.
Write docs/reviews/g1-logging/CODEX-CONFIRM.md. Findings only.

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
