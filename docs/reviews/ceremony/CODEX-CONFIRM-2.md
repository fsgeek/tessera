# Ceremony revision 3 — Codex confirmation 2

Reviewed 2026-11-04 against `BRIEF-CONFIRM-2.md`, including all four appended owner prechecks. **Revision 3 is not yet ready for production key generation: F01 remains HIGH and F03 remains partly unresolved.** The in-session backup restoration fixes the previous last-copy shutdown defect under the stated trusted-session assumptions.

Snapshot: HEAD `a10bd19a18e3f0c395c9d38b2809a17e107a9097`; working-tree `docs/ceremony/CEREMONY.md` SHA-256 `5a7d17887f1c901c7646cf1566e7f9ccf44bada1c8da795e9f290f394878d832`. References below are to that file unless qualified. Repository review was read-only except this report; pre-existing ceremony, deployment and log changes were preserved. No production key, card, PIN, backup or secret was accessed. Synthetic software-key probes ran in temporary directories and were cleaned up. This is document/source confirmation, not a Tails/YubiKey rehearsal or release-independence certification.

## Requested dispositions

| Finding/residual | Resolved by revision 3? | Evidence and limit |
|---|---|---|
| F01 — fixed-touch readback | **NO, HIGH** | Lines 165–171 require colon value 2. The inspected upstream parser destroys that distinction before formatting. See correction below. |
| F02 — last-copy shutdown | **YES at the procedural level** | Lines 132–140 restore and sign with each export before transfer; 151 gates S7 on both tests; 216 gates failed-transfer shutdown on both proven backups. Lines 221–222 preserve a working card and distinguish total loss. This does not prove later media durability. |
| F03 — fresh-boot variables | **PARTLY, MEDIUM remains** | Lines 193–196 supply variables and complete backup commands, with the actual-stick substitution stated. Lines 199–204 still omit both assignments in the separate card-only boot. |
| F04 — destination/LUKS check | **YES for the reported mount-confusion defect** | Lines 121–123 require the exact target and backing-device type `crypt`; 129–131 inspect the partition under that mapper and require LUKS version 2. An ordinary directory or similarly named mount no longer passes. Identity of the physical stick still depends on the operator's Disks/Files selection at 117–121 and the one-stick rule, not cryptographic device authentication. |
| F05 — bootstrap | **YES as an explicitly deferred gate** | Lines 233–243 require independent fingerprint computation, retained public keys, actual-publication comparison and a channel outside NUC/repository/DNS, selected by the author before production use. No particular channel has yet been selected or tested; this resolves the ceremony's omission, not authenticated acquisition itself. |
| C02 residual — versions/fixed touch | **PARTLY** | scdaemon is now printed/recorded at 65,74; GnuPG/Tails likewise. Card firmware is still not explicitly collected or included in the custody record (80–82,228–232). F01 prevents permanence confirmation on inspected upstream versions. The version inference at 253–254 remains an inference. |
| C03 residual — isolation | **PARTLY** | Lines 30,53–55,60–76 prohibit unlocked persistence, require tmpfs, check links/swap/internal mounts, identify hardware and explicitly ban NUC scripts/configuration. The prior explicit no-autorun condition remains absent; custody draft §5, line 128, supplies it as a proposed session condition. State/check it here or cite its application. No claim of live-session isolation is established by this review. |
| C04 residual — backup/failure safety | **PARTLY overall** | F02 and F04 are repaired; F03 still prevents literal completion of final card acceptance. S5 export, fingerprint and signing checks are materially stronger (119–140). |
| C06 residual — custody record | **PARTLY** | Lines 228–243 add/retain public records, independent computation, outside retention and bootstrap obligations; 129–131 record selected LUKS fields. Firmware and protected secret-export settings are still unspecified. The filter records Version/cipher/PBKDF, not the full KDF/cost settings, tool versions or export-protection format requested in the earlier review. These are custody-draft completeness gaps, not a registered mandate for a particular cipher. |

## F01 retained HIGH — correction to my revision-2 recommendation

**Lines 165–171,261.** My earlier report incorrectly said numeric colon output preserves the permanent/on distinction. That recommendation was wrong; revision 3 follows it faithfully. The error arose from inspecting the formatter without following the incoming status parser.

In both upstream tags inspected, `g10/call-agent.c:754–764` handles `UIF-1/2/3`, indexes the first slot with `keyword[4] - '1'`, and assigns `parm->uif[no] = (data[0] != 0xff)`. This produces only 0 or 1. Consequently ordinary raw values 0, 1 and 2 all become 1. Sources: [2.4.4 parser](https://github.com/gpg/gnupg/blob/gnupg-2.4.4/g10/call-agent.c#L754-L764), [2.4.8 parser](https://github.com/gpg/gnupg/blob/gnupg-2.4.8/g10/call-agent.c#L754-L764).

The formatter at `g10/card-util.c:544–545` prints those already-converted values in slot order. The first field does refer to the signature slot, but cannot be 2 on this path. Separately, the setter at 2250–2258 maps `permanent` to raw byte `0x02`; thus **2 means permanent when setting the policy, but the inspected readback does not preserve it**. Sources: [2.4.4 card utility](https://github.com/gpg/gnupg/blob/gnupg-2.4.4/g10/card-util.c#L544-L545), [2.4.8 card utility](https://github.com/gpg/gnupg/blob/gnupg-2.4.8/g10/card-util.c#L2250-L2258).

Concrete failure: a correctly fixed signing slot on an unpatched inspected stack still prints first value 1, requiring the operator to stop at 171. Accepting 1 instead would not establish fixed touch, or even raw UIF-on from this parser alone. Keep the stop; replace the readback with a separately validated raw/card-policy inspection or a pinned implementation demonstrated to preserve the raw value. Rehearse it on the actual stack. This report supplies no untested replacement command and does not recommend trying to disable touch on a production key. Specific upstream tags do not certify all 2.4.x releases or downstream patches.

## F03 retained MEDIUM — card-only boot still lacks variables

**Lines 189–190,199–204,264.** The prose says to set variables each boot, but the supposedly complete card-only block never sets `B` or `FPR`. Those assignments appear only in the preceding backup-test boot. A clean-shell expansion probe produced import operand `/public.asc` and an empty signing selector. No import was run in that probe.

Concrete failure: the operator starts the required third boot, runs S0, inserts the card and unlocks a backup, then follows 202–203. The public import fails because `/public.asc` does not exist, so the primary test cannot complete. Repeat explicit assignments for the actual mounted backup and paper fingerprint immediately before 202. Keep this boot public-import-only. The revision summary at 264 currently overstates completion.

## S5 restoration, agents and shutdown audit

The per-command `GNUPGHOME="$T"` assignments at 135–136 do not overwrite the shell's original exported home. The import, listing, signing and verification all target the restore home. At 137, `gpgconf --homedir "$T" --kill gpg-agent` targets that home's agent, and deletion targets the restore directory, not the generation keyring. Separate homes also separate agent sockets; see [GnuPG homedir option](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html).

A local GnuPG 2.4.4 probe used a newly generated, passphrase-protected synthetic P-256 primary and two temporary homes. The restore home used a synthetic pinentry responder solely to exercise the protected prompt path without a GUI. The literal `gpg --batch --import` and subsequent sign/verify sequence all exited 0; one GETPIN request occurred. Agent socket paths differed. Killing the restore agent exited 0; the original agent still answered with `--no-autostart`, and the original secret key remained listed. All probe agents/directories were removed. Production commands/configuration were not changed.

A passphrase can be requested during import and cached for the following signature; a second prompt at signing is not required for backup recovery. This probe confirms software-home separation and successful decryption/use, not the actual Tails pinentry GUI, LUKS readback, card behavior or secret erasure. A failed cleanup command should be handled before proceeding; the semicolon at 137 does not itself prove agent termination. No ordinary successful execution here disturbs the original key.

Shutdown paths:

- Line 214 is safe before generation in Session 1. When S0 is reused in Session 2, its “nothing secret exists yet” means no session RAM key; persistent copies already exist. Reword that explanation for accuracy.
- Lines 215 and 217 stop/retry without authorizing loss of the RAM key. Failed backups block S7.
- Line 216 now permits transfer-failure shutdown only with two in-session proven backups. This repairs the original HIGH loss scenario.
- Lines 218–219 reject policy failures after the backup gate; stopping then leaves the proven backups. Normal shutdown at 185 likewise follows S5/S7/S9.
- Lines 220–221 preserve remaining copies and explicitly protect a usable card. A card cannot recreate an exportable secret backup; replacement at 220 needs a usable secret backup as its next clause says. Card-only recovery is the separate owner decision at 221.
- Line 222 describes total unusability and deliberate replacement; it cannot preserve a proven copy because its premise is that none remains usable. The absolute summary at 262–263 should retain this exception and the pre-generation exception.

Thus no remaining instruction authorizes destroying the last demonstrated usable copy on the original F02 scenario. S5 tests do not guarantee that media cannot later fail or the retained passphrase cannot later be lost.

S9's earlier command-completeness note also remains: lines 179–181 name alternate outputs but do not print complete `--output` commands. Print them and verify the second positive signature. An overwrite cancellation or unrelated failure is not a no-touch timeout; the existing acceptance wording requires the expected outcomes.

## Appended owner prechecks

| Check | Result | File:line evidence |
|---|---|---|
| 1. Capture row | **PASS** | `CEREMONY.md:18–24,238–243,257` assigns authority roles, preserves the shared-hardware assumption and explicitly recognizes dual-channel bootstrap substitution. It promises no rejection of fresh attacker-key receipts and no capture visibility. Ground truth: `docs/V1-CONTRACT.md:34–37,50–53,72–74`: fresh attacker-key receipts pass under dual capture; honest-material protection and authentic distribution remain conditional. |
| 2. Trigger clause | **PASS** | `CEREMONY.md:9–11,20–21,238–243` invokes an existing independence prerequisite and a future first-production-use gate, without asserting that release occurred or triggering fallback. Registered basis: `docs/phase-0-prereg-amendment-10.md:616,624–643,668–676`. Key generation is not that release trigger. |
| 3. Requester | **PASS for the bounded ceremony claim** | `CEREMONY.md:9–11,38–49,53–55,173–183,257` places ceremony requests with the author and explicitly defers production candidate review, exact-hash approval and media controls. Exportable backups are acknowledged at 40–43; storage/touch are not claimed to establish requester independence. The operational owner can propose release bytes; the author must independently approve the exact archive under `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:253–278`. That future procedure remains unestablished here. |
| 4. Binding text | **PASS** | `CEREMONY.md:3–11,38–49` distinguishes OWNER DRAFT operating choices from registered A10.4.2 (`docs/phase-0-prereg-amendment-10.md:624–643`). Key generation matches the profile's P-256 primary-key direction (`docs/V1-PROFILE.md:1679,1941–1942`). No ruling budget or fixed 24-hour FAILED rule is imported. Firmware/autorun/settings gaps above are deficiencies against the proposed custody procedure (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:128,165–167,198–200`), not invented signed requirements. Ceremony proof signatures at 176–177 are not production archive signatures governed by profile R3. No contradiction with a registered requirement was found in this bounded review. |

No amendment adoption, freeze compliance, full custody conformance, TEST-authority rejection rehearsal, deployed-package identity, production acquisition or release-independence gate is discharged by this confirmation.
