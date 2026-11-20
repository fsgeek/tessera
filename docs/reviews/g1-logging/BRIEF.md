# Review brief: issuer structured logging, detection gap G1 (steward, 2026-11-20)

Review commit a874852 (merged in c6d86eb) in /home/tony/projects/tessera: `service/issuer/tessera_issue/logs.py`,
the changes to `lambda_app.py`, `pipeline.py`, `service.py`, `service/issuer/LOGGING.md` and
`service/issuer/tests/test_logging.py`. Read-only except your report. Context: `docs/V1-DETECTION-CONTRACT.md` (G1, D3-D5).

Check, with severity, file:line and a concrete scenario:
1. Behaviour: can any logging path raise, block, reorder, or alter a lifecycle write, a fence, a guard, or a response
   (including exception re-raise in the API wrapper and the `finally` in poll)?
2. Leakage: can any line carry request content, a content digest, the plaintext request key, the API key, a
   pre-signed URL, credentials, or AWS error text that embeds them (poller_note truncation)?
3. Completeness for detection: does every SIGLOG# write emit `signer_response`; does every disposition that D5 names
   (`unrequested`, `malformed`, `bad-signature`, refusal reasons) reach a line; is any committed transition missing
   (superseded writes, StageError paths)? Would CloudWatch JSON metric filters match the documented fields?
4. Do the tests exercise these properties, or only the happy path?
Write docs/reviews/g1-logging/CODEX-REVIEW.md. Findings only.

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
