# Review brief: issuer <-> signer interface, after the frame-reference fix (owner, 2026-10-30)

You are reviewing the Tessera V1 issuer (`service/issuer/`) and its two production signers (`service/signer-kms/`,
`service/signer-gcp/`) in /home/tony/projects/tessera. Read-only, except that you may run the test suites
(`.venv/bin/python -m pytest -q` in each package directory) and write scratch files under /tmp.

## What happened

Before deployment, the owner ran all four suites. The issuer (234) and verifier passed; both signer suites failed.

1. **A real defect.** The issuance-lifecycle rework (commit 9364733) renamed large-frame objects in
   `service/issuer/tessera_issue/pipeline.py` `_send.stash` from `frames/<rid>/<sha256>` to
   `frames/<rid>/<attempt id>-<sha256>`. Both production signers refuse that form: signer-kms `RE_REF`
   (`tessera_sign_kms/signer.py:42`, which also requires the name to equal `frame_sha256`) and signer-gcp `RE_REF`
   (`tessera_signer/policy.py:29`). Every by-reference request (frames over `INLINE_MAX`, 256 KiB) would be refused
   BAD_REQUEST on every attempt, ending the request ATTEMPTS_EXHAUSTED. The issuer suite missed it because its
   stand-in signer does not check the reference form; Codex CONFIRM-10 reviewed the issuer alone.
2. **Test-harness drift.** ILC-I6/ILC-I9 changed `SlotSigner.receive` to return `(handle, body, age)` and to read
   `Message.sent/.seq/.receives`. The signer suites' queue stand-ins and unpacking were not updated.

## The change (FIX.diff in this directory)

- Issuer: the frame object name is exactly `sha256hex(frame)` again, as `service/issuer/DESIGN.md:92` states. The
  owner's reasoning: frames are deleted per request at the end (END_NS), not per attempt; nothing reads the attempt
  prefix; attempts' frames differ (declared time), and identical bytes would share one immutable object.
- A new issuer test checks the exact form the deployed signers accept, and fails without the fix (verified).
- Signer test harnesses: signer-gcp `QueueView.receive` returns the issuer's `Message` with the receive count;
  three-value unpacking in both suites.

Suites after the change: issuer 235, signer-kms 48, signer-gcp 118, verifier 135, all passing.

## What we ask

A. **Confirm or refute the fix.** Is the owner's reasoning right that dropping the attempt prefix loses nothing?
   Check attempt isolation (ILI/ILC findings in `docs/reviews/issuer-lifecycle-impl/`), cleanup and `mark_due`, the
   `_seal`/signature-object paths, retries and late responses from an earlier attempt, and any S3 IAM or lifecycle
   rule in `service/issuer/infra/` or `service/signer-*/infra/` that keys on the object name.
B. **Sweep the class, not the instance.** The defect class is "the issuer and a signer disagree about the wire or
   storage contract, and no test runs them together". Enumerate every field and format that crosses the boundary in
   either direction (request JSON fields and their formats, `request_id` form, `sign_by` format, inline size limits
   against `INLINE_MAX` and each signer's limit, `frame_ref` and bucket/prefix, response fields, status and reason
   strings the issuer acts on, `frame_sha256` echo, signer `slot`/clock fields, key fingerprint form, SQS message
   attributes), and the infrastructure grants that let each signer read the frames prefix. For each, say whether the
   issuer's producer and each signer's consumer agree, citing file:line, and whether any test exercises the real
   signer code against the real issuer code for it.
C. **Test harness changes.** Do the signer-suite edits weaken any test (e.g. by hiding a receive-count case)?

Report findings with severity, file:line, and a concrete failing scenario. Say plainly if you find nothing.
Write your report to docs/reviews/issuer-signer-interface/CODEX-REVIEW.md.

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
