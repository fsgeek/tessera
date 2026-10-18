# Non-author review: V1 release-key custody and release authorization

2026-10-17. **Result: revise before using this procedure to satisfy A10.4.2.** Nine findings: two HIGH, six MEDIUM and one LOW. The draft does not yet establish, checkably, that capturing the operational credentials or their NUC gives neither access to release-signing capability nor a way to obtain an unwanted signed release.

The principal attack needs no stolen release key. A compromised NUC can prepare a malicious archive and a reassuring summary containing that archive's correct hash. The stated approval steps can then produce a genuine signature over an unwanted release. An offline key, a PIN and a touch do not establish which release the author intended to authorize.

HIGH identifies a path around the claimed signing or authorization boundary. MEDIUM identifies a material missing procedure, check or recovery condition needed to establish that boundary. LOW identifies a bounded wording/style correction. These are document-review findings, not reports of an executed exploit or an observed compromise. This review makes no author choice of hardware or threat model.

## Reviewed material and evidence boundary

Read `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` in full, `docs/plain/STE-STYLE.md` in full, A10's release-authorization and custody provisions, A9.5's trust-configuration authority, V1-PROFILE §5 and §14.2 items 1–2, and V1-OPERATIONS-RUNBOOK §6. The profile and runbook require authenticated bootstrap, rotation, bounded recovery and a defined signed release, in addition to storage separation. They still mark those implementation choices OPEN.

Repository HEAD: `7d7f94d797048f96df9a2b129962a5604439f4ae`. Reviewed custody-draft SHA-256: `cd456e6be8a461adcb5f4d027286c6c96dd8db4b53d4045e552d981d2bf7c865`. All draft line references below refer to that file. A10 remains proposed; this review checks the procedure against its proposed gate without adopting it.

Checked current primary documentation for the OpenPGP PIN/touch controls and software-to-card key transfer, cited beside the relevant findings. No physical device, configured signing system, backup, passphrase, ceremony record or completed rehearsal was inspected. No secret was requested, generated, restored or copied.

## Findings and exact fixes

### C01 — HIGH: the compromised NUC supplies the evidence for its own release authorization

**Locations:** :56–65, :76–77. Governing requirements: A10:418–424 and :437–440; runbook:131–133.

Suppose the NUC supplies archive M, hash SHA256(M), and a summary saying that only expected entries were added. M can instead contain an extra attacker service-key entry, changed old entries, different pins, or a verifier that ignores the compiled configuration check. The author reads the benign summary, recomputes SHA256(M), and signs. Every specified step can succeed. Even a perfectly accurate summary of the trust file would not expose changed verifier code. “Recheck ... with special care” provides no independent source for the check.

The draft also omits the standing release checker. Checking whether additions are expected does not establish unchanged old entries, permitted endpoint closure, the hash/version chain or the proposed service-key authorization closure. A checker supplied by the captured NUC would not independently establish them either.

**Exact fix:** replace §5's approval steps and the compromised-NUC bullet with a procedure containing all of these actions:

1. Keep the last approved trust file, the frozen specification/catalog hashes and the author's approved release baseline outside the NUC. For the first release, create that baseline independently; the NUC's first summary is not the baseline.
2. On a clean review/build system independent of the NUC, check the actual candidate source and trust file against that baseline. Use a trusted, version-pinned release checker. Check the existing invariants and, if adopted, A10's complete initial schedule, unchanged entries, non-overlap and `not_before > previous as_of` rules. Reject every unexplained change, including deletions and verifier-code changes.
3. Check new service-key fingerprints and windows against an authorization record that the author established independently of the NUC and the two authority channels. Matching those channels alone must never authorize an entry. Record the non-secret provenance for other new trust entries too.
4. Build the reviewed source in the clean environment, or independently establish that the candidate executable is that build. Bind approval to the exact final archive hash and its actual trust-file/catalog hashes. Transfer that approved result to the signing session by the controlled method in C02. A NUC-authored summary remains an aid, not authorization evidence.
5. Sign only that approved archive, then verify the signature over the same bytes. Record the approved hashes and the author's decision. Reject a changed candidate and repeat authorization.

Replace :76–77 with: “Stop signing when the NUC is compromised. Establish a clean review and transfer path before another release. Missing key files on the NUC do not establish safe release authorization.” These steps establish a source of author intent; they do not claim that code review proves the verifier correct.

### C02 — HIGH: network disconnection does not establish a trusted signing environment or safe media crossing

**Locations:** :21–24, :33–34, :41, :46, :59, :62–65.

The NUC writes removable media that enters the signing machine. The procedure does not define trusted boot, permitted input formats, execution restrictions, media reuse or the output crossing. A previously infected laptop remains infected with its radios disabled. A NUC-supplied boot image, executable or exploitable input can bring its influence into the offline session. Malware there can choose different signing input; in file mode it can also copy the unlocked key onto the medium returned to the NUC. These are conditional attack paths left unaddressed by the procedure, not evidence that a particular parser or USB device is exploitable.

The rule “never ... on a machine that is connected to a network” also needs a lifetime boundary. “No network connection when it signs” does not address reconnecting a disk that retains the generated or restored software key.

**Exact fix:** replace the signing-machine placeholder with the selected machine and a versioned clean-boot procedure. Require authenticated boot media/tools obtained independently of the operational NUC. Disable internal-disk mounting, swap, hibernation, networking, autorun and boot from transfer media. Never execute or install candidate release content in a session holding release secrets. Use a fresh signing session after review/build work.

Specify the input and output crossing: dedicated transfer media, separate from boot, primary-key and backup media; inert approved input files only; no scripts or configuration loaded from the NUC; safe archive handling without executing contents; hashes checked after copying to controlled local storage; and signature verification against that same immutable input. Disconnect inbound media before unlocking the key. Return only the verified public signature and an allowlisted public record on separate output media. Reset the signing session before those media return.

Name the peripheral trust assumption. Read-only mounting does not authenticate a USB controller. Use a crossing that avoids a NUC-controlled USB device impersonating a keyboard or boot device, such as write-once data media with a trusted reader, or document the actual controlled alternative and its residual. Do not claim resistance to arbitrary hostile peripheral firmware without a defense. No disk containing recoverable release secrets may later boot online. If the chosen environment cannot meet this boundary, leave independence OPEN and use A10.4.2's author-visible fallback.

### C03 — MEDIUM: the ceremony leaves the complete key-copy and secret lifecycle unspecified

**Locations:** :30–37, :42–50. Applies to both primary forms, especially the offline-file fallback.

The ceremony generates the key in software, makes two backups, restores one, and imports into hardware. It gives no disposition for the original secret keyring, restored key, temporary exports or cached passphrase. Loading a key into a YubiKey does not eliminate the software copies deliberately made beforehand. GnuPG documents replacement of a transferred key by a card stub when the operation is saved; that is not a claim to erase every prior filesystem copy. [GnuPG key-management documentation](https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html#OpenPGP-Key-Management).

“Encrypted” gives no reproducible backup format or passphrase-generation rule. “On paper” gives no independence rule for a reused operational password. Only one backup is restored, and the resulting test signature is not explicitly verified. The fallback must preserve the authorization boundary without relying on hardware touch or non-exportability.

**Exact fix:** add these ceremony and shutdown requirements:

1. Generate/import/restore only in the trusted offline session from C02, using a temporary keyring in volatile memory. Inventory every intended persistent copy using non-secret labels. In hardware mode, retain only the imported hardware copy and the two encrypted backups. In file mode, also retain the separately labelled encrypted primary medium. None of these media may be used for transfer, boot or operational storage, or attached to the NUC.
2. State and pin the backup/primary encryption tool, format and protection settings. Generate a strong, unique passphrase within the trusted offline boundary; state its generation method without recording its result. Store its paper recovery copy separately from the encrypted key media. Generate token secrets independently of operational passwords too.
3. Restore each backup independently into a fresh temporary keyring. Compare the full public fingerprint with the ceremony's paper reference. Make and verify a test signature. Test the selected primary in a separate session. An existing cached key or unlocked agent must not substitute for the backup under test.
4. After import/restore/signing, remove temporary exports and keyrings, stop signing agents, detach protected media and power down the volatile session. Avoid creating plaintext secrets on persistent storage in the first place. State the selected method for any unavoidable persistent residue; ordinary file deletion alone must not be described as proven erasure.
5. For file mode, unlock only the selected primary after release approval, then perform the same verification and shutdown. Record that the key is exportable software protected by the offline procedure. Do not inherit YubiKey PIN/touch claims in this branch.

Never put passphrases, user/admin PINs, reset codes, secret-key exports, unpublished revocation certificates or their screenshots into the repository, AI chat, NUC password store or command transcripts. Enter secrets through local protected prompts, not literal command arguments. Record settings and pass/fail results only. Keep a pre-generated revocation certificate offline until its authorized use; it is not a routine public ceremony-log attachment.

### C04 — MEDIUM: “PIN and touch for each signature” has no precise configuration or check

**Locations:** :30, :45, :49–52.

The OpenPGP applet has distinct signature-PIN and touch settings. The signature PIN can be required every time or once per session; touch can be disabled, required, cached or fixed. The draft names neither selected policy nor a test. It also does not cover the admin PIN or reset code, which can affect access recovery. Yubico documents these controls separately. [YubiKey Manager OpenPGP commands](https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html).

**Exact fix:** after choosing the real model/firmware and tool version, add an offline configuration checklist. Identify the release token separately from the repository root and service tokens; do not put operational credentials on it. Change the default user and admin PINs. Either configure an independent reset code under the same secret boundary or state that it is not configured. For the signing slot, set the signature-PIN policy to `always` and touch to a non-cached policy; `fixed` is a concrete choice that prevents disabling touch without deleting that private key. With a compatible pinned `ykman`, the non-secret policy commands are:

```text
ykman openpgp access set-signature-policy always
ykman openpgp keys set-touch sig fixed
```

Read back the settings on the actual device. Rehearse refusal without touch and refusal without fresh PIN verification, including a second signing request. Document and verify the host agent's caching behavior; the card setting alone does not demonstrate a fresh human prompt. Do not deliberately exhaust the production token's retry counters. Record the model, firmware, settings and results, never PIN values. Disconnect the token immediately after the approved operation. State that touch confirms presence, not the signed archive's contents; C01 remains necessary.

### C05 — MEDIUM: the signed object and trust-file authentication are ambiguous

**Locations:** :9–10, :58, :62–65. Governing requirements: profile:389–407 and :1154–1158; runbook:117–119.

“Then the author signs it” can mean the archive, a digest string or the summary. “Signs ... the trust file” suggests a separate signature, while the governing profile expressly gives the config no signature: its hash is compiled into the signed verifier release. P-256/OpenPGP identifies a key scheme, not the complete release-verification format. There is no pinned verification command or check that the delivered archive contains the approved config and compiled hash.

**Exact fix:** choose and record the release artifact and signature format before the real ceremony. One concrete compatible choice is a detached OpenPGP binary-document signature over the exact release-archive bytes. State the archive filename/version convention, selected signing-key fingerprint, hash algorithm, allowed signature/key format, and pinned signing and verification tools/dependencies. Give the tested signing and verification commands with public placeholders only. Do not sign a textual SHA-256 value while documenting a signature over the archive.

Require offline verification with the ceremony public key, and require a changed archive byte to fail. Verify the approved trust-file hash and frozen catalog binding in the actual distributed verifier; merely hashing files supplied beside a different executable is insufficient. Publish exactly the verified archive/signature pair. Replace :9–10 with: “The release key signs each verifier release. The verifier contains the hash of its trust file. The trust file has no separate signature.” If another format is selected, specify it equally precisely and review it before claiming this item closed.

### C06 — MEDIUM: restoring the same key does not disable a lost or stolen YubiKey

**Locations:** :72–75. Governing requirements: profile:1148–1158; runbook:134–145.

Restoring a backup onto a new token leaves the old token able to use the same private key if its access controls can be satisfied. Theft of signing capability need not involve copying the key. The current “suspected to be copied” trigger misses that case. The draft provides neither a loss/theft classification rule nor bounded authenticated recovery if the key or every backup is lost. An author's later publication on captured channels cannot by itself repair distribution authenticity.

**Exact fix:** replace the two release-key incident bullets with these rules:

1. Stop new releases after unexplained token loss, theft, suspected unauthorized signing, backup exposure or secret exposure. Record the last known approved release hash and the uncertainty. Do not assume old signatures can be dated or invalidated merely from their claimed signing time.
2. Reuse the same key only after a documented event establishes that no old usable copy escaped, such as verified destruction of the failed primary. An unrecovered lost token does not meet that test. Treat uncertain theft as possible distribution compromise; record the remaining risk rather than declaring the key safe.
3. Specify ordinary rotation while the current authority is trusted: authorize the new fingerprint through a release signed by the current key, with new custody and a tested transition. If the current key is possibly usable by an attacker, its signature alone cannot distinguish the author's successor from the attacker's.
4. For possible compromise, name the independently authenticated replacement-key delivery path or explicitly state that V1 has no assured recovery path and new releases remain stopped. Apply the same bounded stop if all usable copies are lost. A fresh key posted only through the NUC, repository or DNS account is not independently authenticated recovery.
5. Keep genuine old releases available for existing receipts; do not promise remote revocation or detection of a privately delivered malicious release. Record restart conditions and who confirms them. A recovery announcement cannot withdraw an attacker-held signing capability.

These rules concern the release key. They do not add a service-key rotation project or a new receipt-verifier revocation rule.

### C07 — MEDIUM: two publications made through the NUC do not establish authenticated bootstrap

**Locations:** :42, :46–50. Governing requirements: profile:399–400 and :1151–1158.

Writing the fingerprint on paper is a useful local reference. Publishing the exported key through the NUC to the repository and website does not show that either publication still contains it, or how a new user authenticates the root. Under the stated capture, the NUC can substitute a different public key at both destinations. The fingerprint is not explicitly carried into the freeze record, documentation or relying-party text as the profile requires. This is a missing bootstrap procedure; it is not a claim that V1 must discover every targeted false download.

**Exact fix:** export the ceremony public key, recompute its full fingerprint independently of the NUC, and compare it with the paper reference. Verify the actual bootstrap key and fingerprint placed in the freeze record, verifier documentation and relying-party text. State how a user obtains at least one authenticated initial fingerprint independently of the possibly captured distribution channels, or state authenticated initial acquisition as an explicit assumption with a concrete delivery method. Two matching web publications alone do not satisfy it. Retain the approved public bootstrap artifacts outside the NUC. Require existing trusted releases to authorize normal replacement keys, as C06 describes.

### C08 — MEDIUM: the rehearsal has no acceptance criteria, record or failure gate

**Locations:** :3–5, :34–37, :43–52, :67. Governing requirement: A10:468–479.

The draft correctly calls for a throwaway rehearsal, but does not say what it must demonstrate or record. A happy-path test signature from one backup does not exercise malicious summaries, artifact substitution, token theft response or file-mode cleanup. The procedure leaves the machine and storage choices to the author, yet its opening says it “establishes the gate.” No inspected evidence establishes an implemented access boundary. The 15-minute estimate is also unmeasured.

**Exact fix:** replace the opening claim with “This draft proposes a procedure for the release-key independence gate. The gate stays open until review and the recorded checks pass.” Require the author to select the actual machine, primary form, tool versions, backup method, secret-generation method and transfer method before rehearsing. Do not ask for physical storage addresses or secret values.

Add a dated rehearsal record with the procedure revision/hash, equipment and tool identifiers, public test-key fingerprint, test-artifact hashes, expected and observed results, failures and corrections, reviewer and author acknowledgment. Require at least these cases:

| Case | Required result |
|---|---|
| Valid throwaway release, primary signing, independent restore of each backup | Expected fingerprint; signatures verify over the intended bytes. |
| NUC supplies a malicious trust file with a benign summary and a matching archive hash | Independent content/authorization checks reject before signing. |
| Candidate changes verifier code or compiled config/catalog binding | Unapproved source/build change is rejected before signing. |
| Candidate changes after approval, or a signed archive byte changes | Pre-sign binding or post-sign verification fails, respectively. |
| Repository credential, DNS credential and AWS account each attempt configuration authorization | No release authorization/signature; the genuine verifier refuses the unauthorized configuration, as the standing profile requires. |
| Hardware branch: missing fresh PIN verification or missing touch | Refusal under the selected, observed policy; no hidden second signature. |
| Selected file branch, including restore and shutdown | Correct signature; only inventoried encrypted persistent copies remain; no plaintext key enters output media. |
| Lost/stolen primary, compromised NUC, unavailable backups | The documented stop and authenticated restart limits are followed; no automatic same-key restart after uncertain theft. |

Exercise the branch actually selected for the freeze. If fallback is later selected, rehearse and review that branch before use. Store only public evidence and non-secret attestations about storage and cleanup. Link the reviewed procedure and record from the dated real custody record. Failed or unperformed cases keep the corresponding claim OPEN; they cannot be replaced by a hardware purchase or the time estimate. Mark 15 minutes as an estimate until measured.

### C09 — LOW: the draft does not yet follow STE-STYLE consistently, and its final release sentence expands future scope

**Locations:** :3–5, :17–18, :21–37, :42, :49, :56–58, :65, :67–68. Style rules 1–2, 5–6 and 9–10.

The numbered steps, active voice and short paragraphs are useful. However, AWS, DNS, NUC, PIN, USB, OpenPGP, P-256, SHA-256 and OpenTimestamps first appear without explanations. “Owner instance,” “custody,” “release archive” and “release summary” also need local definitions or visibly proposed dictionary entries. The procedure sentence beginning “It writes a one-page release summary” has 32 whitespace-separated words, exceeding both the 20-word instruction limit and the 25-word description limit. Many requirements use the present tense instead of the required “must.” Body references to A10/A10.4.2 belong in an end reference list.

“One for each later window” omits the standing condition that successor issuance requires a separately registered rotation. It also hides releases needed for permitted trust/pin updates within the existing window. V1's single window does not establish a fixed future release count.

**Exact fix:** define the technical terms at first use, add visibly proposed local terms for this procedure, put references at the end, and use “must” for mandatory constraints. Split the long step, for example:

> The owner instance must prepare the verifier release and its trust file.
> The owner instance is the AI collaborator on the operational computer.
> It must write a release summary that lists every change from the last approved release.
> It must include the release archive's SHA-256 hash.
> The author must check the actual release through the independent approval steps.

Explain SHA-256 before these steps; do not imply that the summary replaces C01's checks. Replace :67–68 with:

> The time needed for one release is an estimate until rehearsal measures it.
> V1 needs an initial verifier release for the freeze.
> Each later verifier release must follow this procedure.
> A later service window requires a separately registered rotation before issuance can resume.

Preserve the conditional status of A10's service-key listing. Style changes must not introduce a separate signature on the trust file or weaken the access-path requirement into mere key inequality.

## Secret handling and disposition

No secret value is present in the inspected draft. It correctly forbids secrets in the document, keeps the AI from holding the release key/passphrase and asks the author not to disclose backup locations. Those are useful requirements. They do not yet specify safe handling of all PINs, reset material, temporary keys, logs and encrypted-key copies; C03–C04 supply that correction. The public custody record needs fingerprints, settings, procedure identity and check results, not passwords, recovery material or physical addresses.

The independence claim must remain conditional on a trusted signing machine and tools, independently established author intent, effective secret/media separation and authenticated initial release-key acquisition. Separate human controllers are not required by the stated scope. A completed paper procedure is not deployment evidence; the real ceremony and selected-branch rehearsal must establish the recorded boundary. A stolen usable token, software backup exposure or an induced malicious signature is distribution compromise even without private-key extraction.

Resolve the findings and obtain the author's concrete choices, then review the revised procedure and its non-secret evidence. Until then, do not use this draft to close release-key independence. If independence cannot be established before freeze, A10.4.2 requires the author-visible NARROW-MODEL route; removing the service-key list does not repair it. This review changes no instrument, profile, implementation or custody configuration.
