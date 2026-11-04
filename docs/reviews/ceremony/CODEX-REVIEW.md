# Ceremony revision 1 — Codex review

Reviewed 2026-11-02 against `docs/reviews/ceremony/BRIEF.md`, including all four owner prechecks. Recommendation: revise and rehearse the corrected procedure before generating production keys. Two command compatibility defects block the stated Tails 6 / Debian 12 / GnuPG 2.2 target. The isolation and acceptance conditions also need completion.

Snapshot: HEAD `54b382cd308291cf92457ff640584fba51ffc02c`; reviewed working-tree `docs/ceremony/CEREMONY.md` SHA-256 `1957f82babb5ad45d48b3b0ff3265bad5690eaf5c4f686affc5ab5101f98e8fc` (untracked at review time). Only this report was written in the repository. No production card, PIN, secret or backup was accessed. This is a source/document review, not a hardware rehearsal or independence certification.

## Findings

### C01 — HIGH: P-256 card attribute selection needs expert mode

**Location:** `docs/ceremony/CEREMONY.md:69–73`.

On GnuPG 2.2.40, `key-attr` calls `ask_curve`; NIST P-256 is marked expert-only. `admin` enables card administration, not GnuPG expert mode. With the printed `gpg --card-edit`, selection `3` is unavailable; the operator cannot complete this step as written. Use `gpg --expert --card-edit`, select the displayed P-256 entry, read the attributes back, and rehearse the complete prompt sequence. For encryption/authentication, an empty algorithm response leaves the existing attribute unchanged; spell out those responses rather than “leave ... as they are.”

Evidence: upstream [2.2.40 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/card-util.c), `ask_card_keyattr`; [keygen.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/keygen.c), `ask_curve`. The Debian bookworm patch set inspected below does not alter this selection.

### C02 — HIGH: `uif` is unavailable in the stated GnuPG 2.2 target

**Location:** `docs/ceremony/CEREMONY.md:116–138`, also `:45` and `:56`.

Upstream 2.2.40's card-edit command table has no `uif` command; its status renderer also lacks the expected UIF display. I inspected Debian `2.2.40-1.1+deb12u2`'s patch set and found no UIF backport. Thus the printed command cannot establish fixed touch on this target. A reader who treats continuation of the interactive session as success can leave touch disabled; alternatively the required status check blocks completion. This is not evidence that the recorded rehearsal failed: that record names neither the Tails nor GnuPG version, so its successful command cannot establish 2.2 compatibility.

Pin and record the actual Tails, GnuPG, scdaemon and card firmware versions. Either use an offline-available, pinned YubiKey Manager with `ykman openpgp keys set-touch sig fixed`, or select and rehearse a GnuPG version supporting the printed command. Check fixed/permanent explicitly: ordinary `on` is weaker than the promised non-disableable policy and must not be accepted as equivalent at line 137. No online installation during the secret session.

Evidence: [2.2.40 card-util.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/card-util.c), command table/status renderer; [Debian patch archive](https://deb.debian.org/debian/pool/main/g/gnupg2/gnupg2_2.2.40-1.1+deb12u2.debian.tar.xz); [Yubico OpenPGP commands](https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html). Rehearsal evidence: `docs/ceremony/2026-11-01-rehearsal-1.md:3–5,29–33`.

### C03 — HIGH: the RAM-only and independent-session assumptions are asserted, not enforced

**Location:** `docs/ceremony/CEREMONY.md:24`, `:49–50`, `:75–77`, `:141`, `:147`.

The boot stick is shared and not new, yet there is no prohibition on unlocking Persistent Storage, no explicit temporary RAM GnuPG home, and no check of the actual home/mounts. Tails can persist GnuPG keys. An operator using an existing persistent GnuPG setup generates/imports secrets onto the boot medium; shutdown does not remove those copies. At-rest key protection does not make this RAM-only or preserve the “only copies” inventory. Do not claim that a plaintext persistent write has been observed: the defect is that the procedure does not establish its absence.

Add an explicit no-persistence boot condition, an empty GnuPG home in verified RAM used consistently by every command (including the revocation path), no internal mounts/swap/hibernation, no autorun, no NUC scripts/configuration, and authenticated image verification independent of the NUC. Name the signing hardware and complete the laptop credential/inbound-access check. Specify these conditions for restore boots too. No secrets, photos or transcripts may go to chat/repository/NUC. Stop if any isolation check fails.

These are gaps against the **draft procedure**, `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:99–106,121–133,173–177,210,229–230`; the registered requirement is the independent boundary and controlled crossing, not a registered mandate for these exact commands (`docs/phase-0-prereg-amendment-10.md:624–643`). Tails documents [GnuPG persistence](https://tails.net/doc/persistent_storage/configure/index.en.html#gnupg).

### C04 — HIGH: failure paths can destroy the last usable copy or silently continue with failed backups

**Location:** `docs/ceremony/CEREMONY.md:87–100`, `:109–114`, `:141`, `:145–158`.

The export/copy commands run independently; `sync && ls` can succeed after `gpg` failed and left an empty `secret.asc`. Restore failure is only recorded, with no rejection condition. Scenario: both exports fail, keytocard fails, and the operator reaches shutdown. The sole usable secret vanishes. Another scenario leaves a working card but no recoverable backup and still proceeds to publication.

Require successful exits and nonempty expected outputs for each export/copy, check the mounted destination is the intended LUKS mapper before writing, and require both isolated restore tests plus primary test before accepting custody. Quote paths and substitute the actual label for every backup, including the hard-coded `ROOT-BK1` in the restore example. A directory or filename existing is insufficient evidence of a backup.

Add a short recovery table: on transfer failure preserve the original RAM key and encrypted backups, inspect actual card fingerprint/state, and do not reset/overwrite a production card blindly; do not shut down the last usable secret until a recoverable copy is established. On failed restore stop acceptance/publication, recover from the surviving good copy and replace/retest the failed backup offline. If no good copy remains, generate a new key and discard the abandoned fingerprint from proposed production records. On a wrong PIN stop and inspect remaining retries; do not guess repeatedly or intentionally exhaust counters. On touch timeout retry only after checking state and policy; “timeout means no touch” at line 132 is too categorical for all device/transport failures. Record non-secret outcomes. The draft's general incident section is not a substitute for these immediate ceremony decisions.

### C05 — MEDIUM: positive signing alone does not test the promised PIN/touch behavior or the isolated primary

**Location:** `docs/ceremony/CEREMONY.md:116–139`, `:143–158`.

`forcesig` toggles the current policy; rerunning step 8 after a partial failure can turn forcing off. A single successful signature after a PIN/touch does not prove that signing without touch fails, that a second request requires a fresh PIN, or that agent caching does not supply it. The only card proof uses the generation session; no fresh-session primary test excludes residual software state.

Read the current policy, toggle only if needed, and require the desired readback. Add a controlled no-touch timeout test, a second signing request with observed PIN behavior, and a fresh-session card-only test importing only the public key. Record actual caching behavior and fixed touch. Account for test signatures in the counter: counter 1 ceases to be the acceptance value after additional tests. Do not use incorrect PIN attempts as a negative test. Draft basis: `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:186–204,218–221`; these are draft operational checks, not separately registered rituals.

### C06 — MEDIUM: custody/bootstrap record is incomplete and public author choices are hidden unnecessarily

**Location:** `docs/ceremony/CEREMONY.md:8`, `:164–172`.

The listed custody record lacks the signing setup, laptop credential-check date/result, holder/access boundary, pinned software/firmware/encryption settings, reset-code choice (none is acceptable), and test outcomes. “AUTHOR ... never in the repository” also sweeps public selections such as image version, verification device and publication channels into paper-only choices. A future reviewer then cannot reconstruct the boundary from the dated record. Keep secrets and locations private; record the non-secret choices/results required to identify the procedure and setup.

Bootstrap also needs an independently computed fingerprint, not merely a fingerprint string read from potentially substituted material; an approved public key retained outside the NUC; and a concrete authenticated first-acquisition route plus publication checks. Specify the dated first-production-release bootstrap record's link to the original freeze baseline and actual B fingerprint. Do not copy the custody draft's stale demand to put a post-freeze production fingerprint in the original freeze record. Basis: draft `:234–247`; registered A10.4.2 `:628–633,668–673`; runbook `:121–124`. No first public production release is established by this review, so these are unclosed prerequisites, not a declaration that its deadline has already been breached.

### C07 — MEDIUM: separate keys/sessions do not establish requester independence

**Location:** `docs/ceremony/CEREMONY.md:14–18`, `:35–42`, `:162–172`.

A and B having different secrets/backups is sound, but an attacker controlling DNS/git/AWS can still supply a malicious candidate through the operational environment and solicit the author's touch/signature. Touch does not bind approval to bytes. The ceremony expressly defers per-release authorization to the draft's §9, so it does not itself close A10.4.2. Add an explicit handoff: no production use until independent review/build, baseline, exact archive-hash approval, controlled input media and author-only authorization are implemented and rehearsed. Holding B decides trust only through releases a relying party authenticates and installs; stealing it does not change an already retained verifier.

The theft statement at line 18 is also conditional: knowing a passphrase alone does not produce any key, and paper sheets/tokens must have compatible separation if location compromise is meant to expose at most one key. Separate boots on shared hardware do not withstand compromised shared hardware/boot firmware; retain the draft's peripheral assumption (`:146–149`). Registered basis: A10.4.2 `:624–643`; requester-specific draft basis `:92–98,203–204,260–289`.

## Command and section disposition

| Section / operation | Assessment |
|---|---|
| Two key roles, separate backups and boots | Sound design choices for limiting shared custody exposure, subject to C03/C07; not separation of human control. |
| Card status, changing default admin/user PINs | Correct basic sequence. Record no reset code or configure one; enforce retry handling. |
| `key-attr` before import | Correct order; C01 fixes the command. Do not reconfigure a populated production slot casually. |
| Expert key generation: 10, curve 3, expiry 0 | Correct for upstream 2.2.40: sign-only ECC, NIST P-256, no expiry. UID and fingerprint listing are sound. |
| Export secret/public and revocation path | `~/.gnupg/openpgp-revocs.d/FPR.rev` is correct for the default home and uppercase full fingerprint. If a RAM home is selected, use its path. The auto-generated certificate is deliberately guarded with a leading colon before the armor header; retain the complete file and document authorized-use handling separately. It is not to go to the out stick. C04 covers unchecked failures. |
| `keytocard` then `save` | Correct, but add the preceding “Really move the primary key? (y/N)” → yes prompt. Card import occurs before save; save asks the agent to replace the local secret with a card stub. Quitting is not a rollback of the card write. This is not proven erasure or removal of backups/cache. Require readback and fresh-session signing. |
| PIN force, permanent touch | Order after key import is sensible. `forcesig` is a toggle; `uif` is incompatible with the stated 2.2 target (C02/C05). |
| SHA-256 detached proof and verification | Commands are sound; default signer is unambiguous only with an empty one-key home. Explicit `--local-user "$FPR"` improves recovery safety. Replace angle-bracket placeholders before running; they are not literal shell commands. |
| Separate restore boots without card | Sound and valuable: prevents the card or prior agent standing in for the backup. Requires C03/C04 acceptance conditions. |
| Out-only stick and read-only NUC use | Sound; never return it after NUC contact. Public signatures/key/proof text are appropriate; unpublished revocation material is not. |
| Timing | Honestly labelled estimate; no finding. |

For save behavior see [GnuPG key management](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html) and [2.2.40 keyedit.c](https://github.com/gpg/gnupg/blob/gnupg-2.2.40/g10/keyedit.c), `cmdKEYTOCARD`/`cmdSAVE`. No hardware behavior was inferred solely from a successful signature in the rehearsal.

## Owner choices

- **Hardware mode:** acceptable under A10.4.2, which also permits offline software custody. Backups deliberately remain exportable signing authority; PIN/touch do not protect their use. Every backup and its decryption secret belongs to the access-boundary analysis.
- **LUKS2 with Disks defaults:** reasonable design but not a pinned setting as required by custody draft `:165`. Record exact tool/version, observed LUKS format, cipher/KDF parameters and protected secret-export format without secrets. The GUI description alone does not establish them. Do not treat this draft pinning rule as a registered demand for a particular cipher or two independent passwords.
- **Same password for both layers of one key:** gives no independent second password barrier. For the stated thief-with-stick threat, compromising that password unlocks both layers; this does not contradict a registered two-password requirement (none found). A/B passwords must remain independent and generated offline. Seven-word physical-dice generation is a reasonable recommendation, not an adopted registered word count.
- **Card KDF off:** removes PIN protection against passive USB observation. Defensible only under a trusted host/USB-path assumption; offline alone does not prevent a USB logger. KDF would not stop a malicious signing host that sees entered PINs or asks for unintended signatures. State the accepted boundary rather than “buys nothing.” No registered requirement for KDF-on was found.
- **No expiry:** no contradiction found. Repository validity is evaluated through the configured signing interval; release authentication follows its separately authenticated lineage. Neither establishes automatic compromise detection/recovery. OpenPGP revocation is not evaluated by receipt verification (`docs/V1-CONTRACT.md:45`); retaining a certificate does not add that property.

## Appended owner prechecks

Each result concerns the reviewed document, not a general certification of the system.

| Check | Result | Evidence and disposition |
|---|---|---|
| 1. Capture row | **PASS** | `CEREMONY.md:12–18,171–172` describes authority roles and required B independence; it never promises attacker-key rejection or visibility after DNS+git capture. Ground truth remains `docs/V1-CONTRACT.md:37–39,52–53,72`: honest material protected; fresh attacker-key receipts pass; no detection guarantee. B independence does not restore the cut listing. |
| 2. Trigger clause | **PASS** | `CEREMONY.md:15–16` invokes A10.4.2's unconditional independence prerequisite, which applies under every option (`amendment-10.md:616,624–634`). It does not invoke fallback, claim deadline breach, or use the ceremony/rehearsal to declare the first-public-release gate closed. Required production release rehearsal and TEST rejection remain pending obligations (`:642–657`), not consequences demonstrated here. |
| 3. Requester | **FAIL** | `CEREMONY.md:14–18,35–42` supports independence primarily with storage/session separation and does not identify who may submit work or how author approval binds to bytes. C07 supplies the concrete channel-captor/requester scenario. Deferral to §9 is legitimate scope separation, but prevents treating this ceremony as an independence argument. |
| 4. Binding text | **PASS** | `CEREMONY.md:3–8,33–45` labels owner draft/choices; `:15–16` correctly attributes independence to adopted A10.4.2/row 34 (`amendment-10.md:624–643,770`). No schedule ruling budget or 24-hour FAILED rule is imported. Draft procedural omissions above are labelled draft gaps, not promoted to registered mandates. Owner choices remain proposals for author confirmation; no conflicting registered command/cipher/expiry mandate was found in the cited registration. |

A production key-generation ceremony is not itself a verifier release. This review neither invokes the NARROW-MODEL fallback nor declares registration, release-format freeze compliance, TEST-rejection rehearsal, deployment identity, or the full release gate discharged.
