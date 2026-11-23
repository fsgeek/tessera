# V1 verifier release procedure (each release)

Owner instance (Claude Opus 5.5), 2026-11-23. This is custody draft §9 (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`) cut
to what registered text requires, with the owner decisions that fill its blanks. The author performs his part from
one printed sheet per sitting: `docs/ceremony/release-REHEARSAL-SHEET.md` (once, TEST key) and
`docs/ceremony/release-v1-1-SHEET.md` (release 1, YubiKey B). Later releases get a sheet of the same form.

Labels: **[REG]** registered text (cited); **[OWNER DECISION]** decided by the steward, recorded here;
**[PROPOSAL]** the owner instance's, not registered and not yet decided by anyone, open to the author's correction.

## What binds

- **[REG] A10.4.2** (`docs/phase-0-prereg-amendment-10.md`, author adopted 2026-10-18). Independence of the release
  key from the DNS credential, the repository key and the issuing AWS account, established before the first public
  verifier release by a written custody and release-authorization procedure that states who authorizes, where
  signing happens and how backups stay outside the operational environment; (C01) an independent review-and-build
  environment that checks each candidate against an approved baseline kept outside the operational environment and
  binds approval to the exact archive hash; (C02) controlled media into and out of the signing session. The dated
  custody record names the procedure. If independence cannot be established, the author receives a NARROW-MODEL
  before that release.
- **[REG] A10 row 36.** Every release before the first public verifier release is a TEST release; a TEST signature
  cannot authenticate a production release; production authentication rejects TEST authority, including TEST
  provisioning overrides. *Before the first public verifier release, a rehearsal must show that an otherwise
  correct archive with only a TEST signature is refused by the production acquisition and verification procedure,
  including when the TEST key is supplied through the test interface.*
- **[REG] Profile §15.9 R1–R6** (frozen at the 30 Oct freeze): the archive `tessera-verifier-v1-<n>.parts` in the
  §15.8 part format; `RELEASE.json` and its binding equalities, checked before signing and again by `install.sh`;
  the detached binary OpenPGP v4 type-0x00 ECDSA P-256 SHA-256 signature over the exact archive bytes, checked
  against rule O in the signing session; acceptance by a trusted checker, then `gpgv` with a keyring holding only the
  authenticated key; production key signs only `PRODUCTION`; the fingerprint from at least two channels independent
  of the operational environment, named in the custody record, and a dated first-production-release bootstrap record;
  a hashed dependency lock.
- **Custody draft §9** is **not** registered text: it is the owner's draft, and whether the author adopts it is
  question 3 below. Only A10.4.2's required contents bind; the draft's §9 steps are followed here as proposals that
  meet them. *(Was labelled [REG]; review precheck "Binding text", 2026-11-23.)*

## Owner decisions

1. **[OWNER DECISION, NOT APPLIED]** *Archive name `tessera-verifier-1.0.0.tar`.* It contradicts frozen text:
   profile §15.9 R1 names the file `tessera-verifier-v1-<n>.parts` (`<n>` a canonical decimal) in the §15.8 part
   format and says "The custody draft's `.tar` is replaced". The release is therefore
   **`tessera-verifier-v1-1.parts`**, release number `1`. Using `.tar` or `1.0.0` would change frozen registered text
   after the freeze: an amendment, the author's to make, and nothing gained for V1.
2. **[OWNER DECISION]** The signature is a detached OpenPGP binary signature, SHA-256, over the exact archive bytes,
   by the release key `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` on YubiKey B (equal to R3).
3. **[OWNER DECISION]** Tools: the GnuPG in the Tails image the author used at the ceremony (2.4.7 then). Its
   version lines and the SHA-256 of its `gpgv` binary are recorded at the rehearsal, and the production sitting checks
   the same lines and hash. R3 pins upstream
   gpgv 2.4.4 and accepts a distribution build only if it reproduces upstream on the release-format vectors, so the
   rehearsal runs Tails' gpgv on them.
4. **[OWNER DECISION, 2026-11-23, review H1]** First-release baseline (custody draft §9, "For the first release ...
   say how you create it"): commit `b134cdf` (the Codex-reviewed verifier package, 2026-10-26, a descendant of the
   freeze commit `52ee179`), dated by its OpenTimestamps proof (Bitcoin block 973240), which the author checks on the
   Pangolin against two explorers over Tor (`release_tool.py baseline`). That shows the anchored commit cannot have
   been rewritten after 2026-10-26 (given genuine chain data and Git's object hashes); it does not show the author's
   approval of it, a preparer could have proposed a different pre-existing tree, and a NUC compromised before the
   anchor is out of scope. The candidate is approved as a change from that baseline: at the rehearsal the Pangolin
   makes the change list itself (`release_tool.py diff`: every file that enters the archive, plus the signing script
   and vectors, in full where added or changed), and the author reads that output on the Pangolin's screen
   (`less`), reads the two scripts from the files themselves, checks their `sha256sum` against their lines in the
   list, and writes the SHA-256 of the whole list file on his rehearsal sheet. A NUC printout is only a reading aid
   and is never what he approves. At the production sitting the Pangolin makes the list again; its whole-file SHA-256
   must equal his rehearsal value, or the sitting stops. He then rebuilds the archive there, and every hash he
   compares later is the Pangolin's. The freeze objects are recomputed as before
   (`assemble.py --commit 270ca49`; `check` against `52ee179`). *Not established:* that the author signed the
   baseline. No commit here is signed by his YubiKey A; the freeze commit and `b134cdf` are signed by the NUC's commit
   key. The baseline is dated and reviewed, not author-signed.
5. **[OWNER DECISION]** The checker (custody draft §9 item 4): `sha256sum` plus
   `service/verifier/release/release_tool.py`, which the author reads on the Pangolin's screen. Its hash is the
   approved change list's line for it, checked with `sha256sum` on the Pangolin and again offline. Ordinary
   acquisition outside the ceremony relies on a checker and `gpgv` its caller selected; nothing stronger is claimed. A relying party's copy from GitHub
   is authenticated only by that party's own reading or trust in GitHub. gpgv: the Tails binary whose SHA-256 the
   rehearsal records after it passes the vectors; the production sitting compares its hash (review M4).
6. **[OWNER DECISION]** Before signing, the author checks the release fingerprint against his ORCID record
   (`https://orcid.org/0000-0002-0651-5019`) **and** his paper ceremony record.

## Roles and places

- **The NUC (owner instance):** prepares the candidate and the summary; publishes. Never holds the release key; never
  writes a medium that enters a signing session.
- **The Pangolin, networked Tails boot** (the review-and-build environment, C01) **[PROPOSAL, replaces the draft's
  "review VM"]:** amnesic; holds no secret; gets source only from GitHub; rebuilds the archive itself; writes the new
  INPUT stick.
- **The Pangolin, offline Tails boot** (the signing session): network off, no internal disk mounted, keyring in
  memory; loads only what INPUT carries; runs nothing from the archive.
- **Media (C02):** INPUT is new or a never-NUC spare, identified by its serial before it is formatted, written only
  by the networked Tails boot; it carries the archive the author built, the release public key, `release_tool.py`
  and `sign-release.sh` (plus the vectors at rehearsal), and is removed before the key is used. **[PROPOSAL]** The
  custody draft's transfer rule 3 allows only the archive and the key on INPUT; the two scripts and the vectors are
  added because the session must check and sign with something. Each is executed offline only after its SHA-256
  equals the value the author approved in the networked boot (the change list's line, or the vectors' digest). OUT
  is new and never-NUC on entry, identified by serial, written only after every check passes and read back; it
  carries only the signature and `record.txt` (plus the TEST public key at rehearsal); it goes to the NUC and never
  returns to a signing session. A run that does not end in `==> PASS` leaves OUT quarantined. The offline boot mounts
  no internal disk (checked by the sheet and the script). No stick that has been in the NUC or another everyday
  computer enters.

## Steps for each release

**A. Preparation on the NUC (owner)**
1. Commit the release's files under `service/verifier/release/v1-<n>/` (`trust.json`, and `release_constants.py`
   from `release_tool.py constants`). Push the source commit to GitHub.
2. Build twice from two checkouts; the archives must be byte-identical. Run `release_tool.py check` and `sources`.
   Produce the change list `release_tool.py diff --base <baseline> --commit <source>` twice; byte-identical. Anything
   in it not needed for the release is removed from the archive rather than explained.
3. Write `docs/releases/v1-<n>/SUMMARY.md`: every change from the last approved release, every hash and its trace.
   For release 2 onward, also `tessera-verify --previous <last trust> --next <new trust>` must print `ACCEPT`
   (the release checker's invariants, custody §9 item 5).
4. Give the author the printed sheet, which carries the source and baseline commits and the expected values (and,
   if he wants one, the change list printed as a reading aid). They can only stop the sitting: the author's own
   Pangolin results decide.

**B. Independent approval (author, networked Tails)**, custody §9 items 1–14:
5. Clone from GitHub; `diff` makes the change list on the Pangolin. Rehearsal: read the two scripts from the files
   and the whole list on the Pangolin's screen; `sha256sum` of the two scripts equals their lines in it; write the
   list file's whole SHA-256 on the sheet and record the approval. Production: the list file's whole SHA-256 equals
   the rehearsal's written value, or stop; the scripts' lines in it equal their `sha256sum`.
5a. `baseline` shows the baseline's OpenTimestamps block and time.
6. Recompute the freeze objects; rebuild the archive from the source commit; write its hash (it must also equal the
   sheet's).
7. `release_tool.py check`: `CHECK PASS`, then compare the printed authority entries by eye: the repository key
   fingerprint with paper and ORCID; namespace `PRODUCTION`; the release number; successor none (or the named
   successor, with its own authorization).
8. `release_tool.py sources`: the KSK digests and every pin equal their public sources, over Tor.
9. Check the release and repository-root fingerprints on ORCID against the paper ceremony record; a mismatch is a
   stop.
10. Record the decision on paper; write the archive he built, the public key and the two scripts to INPUT.

**C. Signing (author, offline Tails)**, custody §9 "Signing" 1–6:
11. Copy INPUT into memory; compare the three hashes with the paper; remove INPUT.
12. `inspect`: grammar, R2 equalities, namespace `PRODUCTION`. The key file is exactly `CADC…035E`; paper, ORCID and
    screen agree; YubiKey B is the card.
13. Compare the archive hash with the paper one last time; sign (PIN, touch); remove YubiKey B.
14. Verify the new signature as a relying party would (rule O, signer, `gpgv` with only that key).
15. A copy with one byte changed must fail.
16. Write the signature and `record.txt` to OUT; shut down.

**D. Publication (owner, NUC)**, custody §9 "Publication":
17. `release_tool.py acquire` (no `--out`) with fingerprint `CADC…035E` over the NUC's own archive and the signature
    from OUT: `ACQUIRED PRODUCTION release 1, sha256 …`. `acquire` reads each file once into a private copy and
    checks only that copy; the printed SHA-256 is of the bytes it checked (review H2).
18. Publish the archive file whose SHA-256 equals that printed value, the signature and the summary (check the
    published copies' hashes after upload); make an OpenTimestamps proof of the archive.
19. Release 1 only: write, publish and stamp the dated **first-production-release bootstrap record** (R5): the freeze
    record by hash, the production key's full fingerprint, the channels that carry it. The freeze record is not
    amended.
20. If the candidate changes after approval, it is rejected and steps 2–16 repeat.

## Before the first public verifier release (gates this procedure does not close)

From `formal/freeze-v1/FREEZE-RECORD.md` "Before the first public verifier release" and `service/issuer/DEPLOY.md`:
- The rehearsal (A10 row 36), done by the author from `release-REHEARSAL-SHEET.md`, and its dated record.
- The dated custody record naming this procedure (A10.4.2), with the setup actually used.
- **Two** fingerprint channels independent of the operational environment (R5 frozen rule; custody §8 names ORCID).
- Off-site copy of each key's material, out of reach of a fire at home (`DEPLOY.md`, owner 2026-11-10).
- The custody record must say where YubiKey B and each of its backups are kept and how each stays outside the
  operational environment (A10.4.2: "how backups stay outside the operational environment"); the sheets do not
  supply that record (review M5).
- The root (repository key) rotation protocol (`DEPLOY.md`, owner 2026-11-06).
- The GCP VPC Service Controls perimeter; a policy for responses the signer was not asked for (E-06). Their status is
  not checked here.

## Proposals (not registered; the author may correct)

- **[PROPOSAL]** The networked Tails boot on the Pangolin is the review-and-build environment (C01), in place of the
  draft's review VM. It is amnesic, holds no credential and reaches only GitHub, IANA, two block explorers and ORCID
  over Tor. It is not independent of GitHub: a GitHub captor could serve altered source. The author's checks catch a
  change to any file that enters the archive (the change list made and read there, its whole-file hash written at
  the rehearsal and compared at production, the dated baseline)
  and to the authority entries (paper, ORCID, public sources). The unchanged verifier code is approved as the dated,
  reviewed baseline `b134cdf`, not by the author's reading.
- **[PROPOSAL]** The rehearsal uses a TEST key made in memory, not a YubiKey: the card path (PIN, touch, the
  `--card-status` link) was exercised at the ceremony and on 2026-11-13, and the production sheet uses the corrected
  form.
- **[PROPOSAL]** OUT reaches the NUC by any route: it carries only public data, and step 17 verifies it.
- **[PROPOSAL]** The laptop credential check (custody §5) is replaced by Tails' amnesia: the Pangolin's installed
  system is never booted for release work, and no Tails session uses persistent storage.
- **[PROPOSAL]** Later releases add, on their sheet, the release checker's `ACCEPT` against the previous trust file.
  That check needs Python 3.14 and cryptography, which an offline Tails lacks, so it runs in the networked boot
  after a hashed install. (A NUC-only comparison cannot stand in for C01's independent check; withdrawn, review
  precheck "Binding text".) To decide before release 2.

These steps establish what the author intended. They do not prove the verifier correct.

## Questions for the author (before the production sitting)

1. **The second fingerprint channel.** R5 (frozen) requires at least two channels independent of the operational
   environment, named in the custody record before the first public verifier release. ORCID is one. What is the
   second (the profile's recommendation was a Zenodo record under your ORCID, or a printed copy)? Without it, R5's
   rule is not met and the gate stays open.
2. **Off-site copy.** Is one copy of YubiKey B's material (backup stick or passphrase paper) now where a fire at home
   cannot reach it? The custody record states it (yes, or the date it will be).
3. **This procedure.** Do you adopt it, with its proposals (networked Tails as the review-and-build environment, a
   TEST key in memory for the rehearsal), as the procedure the custody record names? Correct any proposal you reject.
4. **What release 1 covers.** Its pins cover the first production receipt only. Every later receipt needs a later
   release, and so a signing sitting, before a relying party can verify it. Is that cadence acceptable for V1?
5. **The baseline.** The steward's plan was to root the baseline in the freeze commit as signed by your YubiKey A.
   It is not: `52ee179`, like every commit here, is signed by the NUC's commit key (`2B9C…3835`), and YubiKey A has
   signed only the parentless key-assertion commit. The sheets therefore root the baseline in time instead (`b134cdf`,
   OpenTimestamps block 973240, 2026-10-26): that commit cannot have been rewritten since, but a NUC compromised
   before then could have shaped it, and the sheet's naming of it is the preparer's proposal. Is a dated, Codex-reviewed baseline enough for C01's "approved
   baseline", or do you want to approve it explicitly (for example by signing, with a key of yours, a statement
   naming `b134cdf`) before the production sitting?
