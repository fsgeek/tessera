# Review brief: key ceremony revision 1 (owner, 2026-11-02)

Review `docs/ceremony/CEREMONY.md` in /home/tony/projects/tessera, read-only (write only your report). It is the
procedure the author will follow on an offline Tails session to create the V1 repository root (YubiKey A) and the
release key (YubiKey B). Context: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` (§5–§8, §11), `docs/V1-OPERATIONS-RUNBOOK.md`
§1, `docs/V1-PROFILE.md` §15.4 and §6.3, `docs/phase-0-prereg-amendment-10.md` row 34 (A10.4.2), and the rehearsal
record `docs/ceremony/2026-11-01-rehearsal-1.md` (Tails GnuPG + YubiKey 5 signatures passed the verifier's git
signature path).

Please check:
1. **Correctness of each command** for Tails 6 (Debian 12, GnuPG 2.2.x) and a YubiKey 5 (OpenPGP 3.4): order of
   key-attr / keytocard / forcesig / uif; whether `keytocard` removes the local secret only on `save`; whether the
   revocation certificate path is right; whether any step leaves a plaintext secret on a persistent medium.
2. **Gaps against the custody draft and registered text**: anything §6–§8 or A10.4.2 requires that this procedure
   omits or contradicts (for example the session conditions in §5, the custody record contents, the independence of
   A and B). Distinguish registered requirements from the owner's own choices.
3. **Failure handling**: what the author should do if a step fails midway (e.g. keytocard fails after backups,
   a restore test fails, a PIN is entered wrongly), and whether the procedure says so.
4. **The owner decisions listed in the document** (hardware mode, LUKS2 via Disks with one passphrase for both layers
   of one key's backups, KDF off, no expiry): any that weaken a stated property.

Report findings with severity, file:line and a concrete failing scenario; say plainly if a section is sound.
Write the report to docs/reviews/ceremony/CODEX-REVIEW.md.

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
