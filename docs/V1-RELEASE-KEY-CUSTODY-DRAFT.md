# V1 release-key custody and release authorization (DRAFT for the author's correction)

Status: DRAFT, owner instance, 2026-10-17. Revised 2026-10-17 for the non-author review, findings C01–C09 [R6].
This draft proposes a procedure for the release-key independence gate [R1]. The gate stays open until review and the
recorded checks pass. The author corrects this draft. It contains no secret and must never contain one.

## 1. Gate and dates

- The gate must close before the first public verifier release. *(Author: the gate text [R1] says "before the
  freeze". Amend it to match, or keep the freeze date.)*
- The release format must be frozen by 30 October 2026. The format is the release archive, the signature format
  and the verification commands.
- Each release before the gate must use the test release key. No production trust anchor accepts the test release
  key.
- If the gate cannot close before the first public verifier release, the author receives a NARROW-MODEL [R1]. A
  NARROW-MODEL is a smaller model of the attacker, and only the author can accept it. Removal of the service-key
  list does not repair a failed gate.

## 2. Terms

Technical names:

- **SHA-256** is a hash function. A hash is a short value that a program computes from bytes. A change to the bytes
  gives a different hash.
- **OpenPGP** is a standard format for keys and signatures. **GnuPG** is a program that uses it.
- **P-256** is an elliptic curve. ECDSA signatures can use it.
- **YubiKey 5** is a small USB hardware device that holds private keys. Its OpenPGP function signs with them.
  **ykman** is the program that configures it.
- **PIN** is a short secret code that unlocks the YubiKey for one use.
- **USB** is the connector standard for removable drives and the YubiKey.
- **DNS** is the Domain Name System. The DNS credential is the login that can change the DNS records of wamason.com.
- **AWS** is Amazon Web Services. The AWS account holds the AWS key.
- **OpenTimestamps** is a service and file format that puts a hash into Bitcoin.
- **NUC** is a small Intel computer. Here it is the operational computer.
- **VM** is a virtual machine: a simulated computer that runs inside another computer.
- **Live-boot session** is an operating system that starts from a removable medium and runs in memory only.

Proposed local terms (owner proposals; a reviewer must check them):

| Word | Meaning |
|---|---|
| owner instance | The AI collaborator on the operational computer. It never holds the release key or its passphrase. |
| operational computer | The NUC. It holds the AWS login, the Google Cloud login and the Tessera repository. |
| laptop | The author's System76 laptop. It is not the operational computer. |
| release archive | The exact file that the release key signs. It contains the verifier and its trust file. |
| release summary | A text that the owner instance writes about a candidate release. It is an aid, not evidence of approval. |
| approved baseline | The last approved trust file, the frozen specification and catalog hashes, and the hash of the approved verifier code. The author keeps it outside the NUC. |
| authorization record | The author's record of each service-key fingerprint and window that the author approves. The author makes it without the NUC and without the two authority records. |
| release checker | The program that compares a candidate trust file with the previous trust file and prints ACCEPT or REJECT. |
| review VM | A clean VM on the laptop for review and build work. It holds no secret. |
| signing session | A fresh live-boot session that holds the release key for one operation. |
| transfer medium | A removable medium that carries files into or out of the signing session. |
| custody | The storage of the release key and the control of its use. |
| custody record | The dated public record of custody. It contains no secret and no physical location. |
| test release key | A separate key that signs releases before the gate. No production trust anchor accepts it. |

## 3. What the release key signs

The release key signs each verifier release. The verifier contains the hash of its trust file. The trust file has
no separate signature.

The trust file lists the DNS root keys, the repository keys and the Bitcoin pins. If the service-key list is adopted
[R1], the trust file also lists the service keys for each window. A person with signing capability for the release
key can make a verifier trust anything.

Proposed format *(Author: confirm before 30 October)*:

- The signature is a detached OpenPGP binary-document signature over the exact bytes of the release archive.
- The release key is an OpenPGP key with ECDSA on P-256. The hash algorithm is SHA-256.
- The archive name is `tessera-verifier-<version>.tar` *(Author: confirm the name and version rule)*.
- The signing and verification tools have pinned versions *(Author: name GnuPG and its dependencies, with versions)*.
- The author must never sign a text SHA-256 value instead of the archive.

Candidate commands, with public placeholders only. Rehearsal must test them before they are final:

```text
gpg --digest-algo SHA256 --local-user <RELEASE-FINGERPRINT> --detach-sign --output <ARCHIVE>.sig <ARCHIVE>
gpgv --keyring <RELEASE-PUBLIC-KEY-FILE> <ARCHIVE>.sig <ARCHIVE>
```

## 4. Separation rules

These rules separate access paths, not people. The author controls every credential. V1 claims no separation of
control. The requirement: a person who captures the DNS credential, the repository key or the AWS account gets no
signing capability for the release key. That person also gets no way to make the author sign an unwanted release.

1. The release key must be different from the repository key and from both service keys.
2. The release key must never exist on the NUC.
3. The release key must exist only in a YubiKey, on its encrypted media, or in the memory of a signing session.
4. No disk that contains recoverable release secrets can ever start a computer that has a network connection.
5. The laptop and the signing session must hold no credential for DNS, AWS, Google Cloud or the repository.
6. The NUC must have no access path to the laptop. The author keeps it so.
7. No medium that the NUC wrote can enter a signing session.
8. Only the author can authorize a release. The owner instance prepares releases.

## 5. Machines and media

### The laptop

1. Before the rehearsal, the author must check the laptop for these items:
   - git credential helpers and stored git credentials;
   - GitHub CLI (`gh`) tokens;
   - cloud command-line tools with logins (AWS, Google Cloud);
   - browser sessions that are logged in to DNS, AWS, Google Cloud or the repository host;
   - inbound access: an SSH server, and entries in `~/.ssh/authorized_keys`.
2. The author must remove each credential and inbound path that the check finds.
3. The custody record must state the check date and the result, with no credential value.

The laptop's `~/.ssh/config` shows no outbound credentials. The other items are not yet checked.

### The review VM

- Review and build work must run in a clean VM on the laptop. A VM on the NUC is not acceptable.
- The VM holds no secret. The author keeps a snapshot at each step for later audit.
- Snapshots help an audit. They do not make the VM independent of the NUC.
- The candidate reaches the VM by *(Author: say how, for example a fetch of a public repository commit)*.
  The VM treats the candidate as untrusted data.

### The signing session

The release key is used only in a fresh live-boot session. Each session must meet these conditions:

1. The live image is *(Author: name the distribution and version)*.
2. The author must verify the image checksum and the distribution signature on a device independent of the NUC.
   *(Author: name that device.)*
3. The session must start from its own boot medium. It must not start from a transfer medium.
4. The session must not mount an internal disk. It must have no swap, no hibernation and no network.
5. Autorun of removable media must be off.
6. The session must not run or install any content of the candidate release.
7. The session must load no script or configuration from the NUC.
8. A new session must start after review or build work. Each signing operation uses a new session.

*(Author: say which hardware runs the signing session, for example the laptop with its internal disk not mounted.)*

### Transfer rules

1. Each medium must have one role: boot, YubiKey backup, encrypted primary, input transfer or output transfer.
2. The NUC must never write an input transfer medium. The review VM writes it.
3. The input medium must contain only the approved archive and the public release key. Each is an inert file.
4. The session must copy the input files to memory and check their hashes against the paper record.
5. The author must disconnect the input medium before the release key is unlocked.
6. The output medium must receive only the signature and the allowlisted public record.
7. The author must shut down the session before the output medium goes to the NUC.
8. An output medium that the NUC touched must never return to a signing session.

Peripheral assumption: read-only mounting does not authenticate a USB controller. A hostile USB device can act as a
keyboard or a boot device. This procedure keeps NUC-written devices out of the signing session. It does not resist
hostile firmware in a new USB device or in the signing hardware. *(Author: choose the transfer medium, for example
new USB drives used for one role, or write-once optical discs with a trusted reader.)*

If the chosen setup cannot meet these rules, independence stays OPEN. The author-visible NARROW-MODEL route then
applies.

## 6. Custody

- **Primary:** a YubiKey 5 with the OpenPGP function. The YubiKeys arrive on 20 October 2026.
- **Fallback:** an encrypted key file on a separate encrypted primary medium. In this mode the key is exportable
  software. Only this offline procedure protects it. The YubiKey PIN and touch rules do not apply.
- **Backups:** two encrypted copies, each on its own medium, in two different places. Neither place is with the NUC.
  *(Author: confirm that two places exist. Do not tell the owner instance where.)*
- The custody record must state which primary is in use.

Encryption and passphrase:

1. The backup and primary encryption must use a pinned tool, format and setting. *(Author: name them.)*
2. The passphrase must be strong and unique. The author must generate it inside the offline boundary.
   *(Author: state the method, not the result.)*
3. The paper copy of the passphrase must be stored apart from the encrypted media.
4. The YubiKey PINs and reset code must be new values, not operational passwords.

Secret handling:

- Never put a passphrase, PIN, reset code, secret-key export or unpublished revocation certificate into the
  repository, an AI chat, the NUC password store or a command transcript. Never put a screenshot of one there.
- Type each secret only into a local protected prompt, never as a command argument.
- Records contain settings and pass or fail results only.
- Keep the revocation certificate offline until its authorized use. It is not part of the public ceremony record.

## 7. YubiKey configuration

Do these steps offline in a signing session, after the author chooses the model, firmware and `ykman` version.

1. Label the release YubiKey apart from the repository YubiKey and the second-key hardware.
2. Put no operational credential on the release YubiKey.
3. Change the default user PIN and admin PIN.
4. Set an independent reset code under the same secret rules, or record that no reset code exists.
   *(Author: choose.)*
5. Set the signature PIN policy to `always`. Set touch for the signing slot to `fixed`. `fixed` stops anyone
   from turning touch off without deleting the private key.

```text
ykman openpgp access set-signature-policy always
ykman openpgp keys set-touch sig fixed
```

6. Read back the settings from the actual YubiKey.
7. Test that signing fails without touch. Test that a second signing request needs a new PIN.
8. Record the caching behavior of the GnuPG agent. The YubiKey setting alone does not show a fresh prompt.
9. Never use up the retry counters of the production YubiKey on purpose.
10. Record the model, firmware, settings and results. Never record a PIN value.
11. Disconnect the YubiKey immediately after each approved operation.

Touch confirms that a person is present. Touch does not confirm which archive the YubiKey signs. The approval steps
remain necessary.

## 8. Key ceremony (once)

Rehearse the whole ceremony with a throwaway key first (see "Rehearsal").

1. Start a signing session. Set the GnuPG home to a temporary folder in memory.
2. Generate the release key (OpenPGP, ECDSA P-256). Write its full fingerprint on paper.
3. Make the two encrypted backups. In file mode, also make the encrypted primary medium.
4. List each intended persistent copy by a non-secret label.
5. In hardware mode, load the key into the YubiKey and configure it (see "YubiKey configuration").
6. Export the public key to the output medium. Never export a secret key to a transfer medium.
7. Delete the temporary exports and keyring. Stop the GnuPG agent. Detach every protected medium.
8. Shut down the session.
9. For each backup, start a new session with a new temporary keyring. Restore that backup only.
10. Compare the full fingerprint with the paper. Make a test signature and verify it.
11. In a separate session, test the selected primary in the same way.
12. A cached key or unlocked agent must never stand in for the copy under test.

Persistent copies after the ceremony:

- Hardware mode: the YubiKey and the two encrypted backups only.
- File mode: the encrypted primary medium and the two encrypted backups only.
- None of these media can be used for transfer, boot or operational storage. None can touch the NUC.

The session runs in memory, so it creates no plaintext secret on a disk. Do not describe ordinary file deletion as
proven erasure. *(Author: if any persistent residue cannot be avoided, state the selected method.)*

Public-key bootstrap:

1. On a device independent of the NUC, compute the full fingerprint of the exported public key.
2. Compare it with the paper.
3. After publication, check the actual key and fingerprint in each place: the freeze record, the verifier
   documentation and the user documentation.
4. Keep the approved public key and fingerprint outside the NUC.
5. Give users one authenticated way to get the fingerprint that does not pass through the NUC, the repository or
   DNS. *(Author: name it, or state authenticated first acquisition as an assumption with a concrete delivery
   method.)*

Two matching web publications alone do not authenticate the release key.

Custody record: write a dated record with the fingerprint, the custody mode, the procedure revision and hash, the
signing setup, the laptop credential check, and confirmation that the backups are in two places. Do not record
where they are. Link the rehearsal record.

## 9. Each release

Preparation on the NUC:

1. The owner instance must prepare the verifier release and its trust file.
2. It must write a release summary that lists every change from the last approved release.
3. It must include the SHA-256 hash of the release archive.
4. The author must check the actual release through the independent approval steps below.

The summary does not replace those steps.

Independent approval in the review VM:

1. The author must keep the approved baseline outside the NUC.
2. For the first release, the author must create the baseline independently. The first NUC summary is not the
   baseline. *(Author: say how you create it.)*
3. Check the actual candidate source and trust file against the baseline.
4. Use a trusted, version-pinned release checker. *(Author: name the checker and its pinned hash.)*
5. The checker must check the existing release invariants: unchanged entries and pins, nondecreasing `as_of`,
   version plus one, the `previous_sha256` chain, and no retroactive close of an open end.
6. If the service-key list is adopted, the checker must also check the complete initial schedule, non-overlap of
   windows, and `not_before` later than the previous `as_of`.
7. Reject every unexplained change, including deletions and changes to verifier code.
8. Check each new service-key fingerprint and window against the authorization record.
9. A match with the two authority records must never authorize an entry.
10. For other new trust entries, record their non-secret source.
11. Build the reviewed source in the review VM.
12. Check that the built verifier contains the approved trust-file hash and the frozen catalog binding.
13. Record the approved hashes: the archive, the trust file and the catalog.
14. Record the author's decision. Write the approved archive and the public key to a new input medium.

*(Author: say how you obtain each service-key fingerprint without the NUC and the two authority records.)*

Signing:

1. Start a new signing session. Copy the input files to memory and disconnect the input medium.
2. Compare the archive hash with the approved hash. If they differ, stop.
3. Unlock the primary and sign the archive.
4. Verify the signature over the same bytes with the ceremony public key.
5. Change one byte in a copy of the archive. Its verification must fail.
6. Write the signature and the public record to the output medium. Shut down the session.

Publication on the NUC:

1. The owner instance publishes exactly the verified archive and signature, and the summary.
2. It makes an OpenTimestamps proof for the release archive.

If the candidate changes after approval, reject it and repeat the approval.

These steps establish what the author intended. They do not prove that the verifier is correct.

The time for one release is an estimate until rehearsal measures it. V1 needs an initial public verifier release under
the production release key. Each later verifier release must follow this procedure. A later service window requires a
separately registered rotation before issuance can resume.

## 10. If something goes wrong

- **The NUC is compromised:** stop signing when the NUC is compromised. Establish a clean review and transfer path
  before another release. Missing key files on the NUC do not establish safe release authorization.
- **Stop events:** stop new releases after unexplained YubiKey loss, theft, suspected unauthorized signing, backup
  exposure or secret exposure. Record the hash of the last approved release and the uncertainty. Do not date or
  reject old signatures from their stated signing time alone.
- **Same-key restart:** reuse the same release key only after a documented event shows that no old usable copy
  escaped, for example verified destruction of a failed YubiKey. A lost YubiKey that is not recovered fails this
  test. Treat uncertain theft as a possible distribution compromise. Record the remaining risk.
- **Normal rotation:** while the current release key is trusted, a release signed by it authorizes the new
  fingerprint. The new key needs new custody and a tested transition.
- **Possible compromise or loss of all copies:** a signature of a possibly captured release key cannot tell the
  author's successor from an attacker's. A new key posted only through the NUC, the repository or DNS is not
  authenticated. *(Author: name an independently authenticated delivery path for a replacement key, or state that
  V1 has no assured recovery path and that new releases stay stopped.)*
- **After any of these:** keep genuine old releases available for existing receipts. Do not promise remote
  revocation or detection of a malicious release sent privately. Record the restart conditions and who confirms
  them. *(Author: name who confirms.)*

These rules concern the release key only. They add no service-key rotation and no new verifier revocation rule.

## 11. Rehearsal

Before the rehearsal, the author must select the machine, primary mode, tool versions, backup method,
passphrase-generation method and transfer method. Do not record physical locations or secret values.

The dated rehearsal record must contain: the procedure revision and hash, equipment and tool identifiers, the public
test-key fingerprint, test-archive hashes, expected and observed results, failures and corrections, and reviewer and
author acknowledgment. It must cover at least these cases:

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

- Rehearse the mode selected for the first public release. If the fallback is selected later, rehearse and review
  it before use.
- Store only public evidence and non-secret statements about storage and cleanup.
- Link this procedure and the rehearsal record from the custody record.
- A failed or skipped case keeps its claim OPEN. A hardware purchase or a time estimate cannot replace it.

## 12. Limits

- The independence claim depends on four conditions: a trusted signing setup and tools, independent author intent,
  effective secret and media separation, and authenticated first acquisition of the release key.
- This procedure does not protect a user who receives a false verifier release sent only to that user.
- It does not make a capture of the DNS credential or the repository key public.
- A stolen usable YubiKey, an exposed backup or a malicious signature that the author was led to make is a
  distribution compromise. This is true without extraction of the private key.
- A paper procedure is not deployment evidence. The real ceremony and the rehearsal establish the boundary.

## References

- [R1] Amendment 10 (proposed), release-key custody gate (A10.4.2) and service-key list (A10.4.1, option (e));
  `docs/phase-0-prereg-amendment-10.md`.
- [R2] Amendment 9, trust-configuration authority (A9.5).
- [R3] `docs/V1-PROFILE.md` section 5 and section 14.2 items 1–2.
- [R4] `docs/V1-OPERATIONS-RUNBOOK.md` section 6.
- [R5] `docs/plain/STE-STYLE.md`.
- [R6] `docs/reviews/custody/CODEX-REVIEW.md`, findings C01–C09.
- GnuPG key management: https://gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html
- YubiKey Manager OpenPGP commands: https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html
