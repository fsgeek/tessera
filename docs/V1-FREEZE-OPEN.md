# V1 freeze: the open items of profile §14.2, checked

> **Status: OWNER WORKING NOTE, 2026-10-19** (Claude Opus 5.5, owner instance). Read-only survey plus one proposed
> profile section. It changes no registered sentence and does not edit `docs/V1-PROFILE.md`. If it disagrees with
> A9 or A10, they win. Every effort figure is **my estimate**, not a measurement. Each state was checked against the
> file named, not against another tracker. "Instrument" means code under `prototype/` (A9:198-200): it can inform an
> item but discharges nothing until its output enters a frozen object.

## 1. Summary

| # | Item (`docs/V1-PROFILE.md:1270-1358`) | State | Remaining (my estimate) | Freeze critical path? |
|---|---|---|---|---|
| 1 | Release-key custody | NOT NEEDED FOR FREEZE (gate is the first public release) | 0.25 d of profile text before the freeze; the gate work after it | no (text only) |
| 2 | Release artefact and release-signature format | DONE for the format, 2026-10-19 (profile §15.9; instrument changes remain) | 0.5 d instrument (e2e TEST release to §15.9, `--production` removed) | no (text frozen-ready) |
| 3 | Pre-freeze trust-configuration values | DONE for the freeze, 2026-10-19 (profile §5 "Sourced trust values") | 0 for the freeze; ICANN CA second path, repository entry and pins at config v1 | no |
| 4 | Hybrid branch | DONE | 0 | no |
| 5 | Slot-2 custody choice | DONE 2026-10-19 (profile §8 "Slot-2 custody record", monoculture checked) | 0 | no |
| 6 | Repository-root algorithm | NOT BEGUN | 0.1 d, on 20 Oct when YubiKey 2 arrives | only if the answer is not P-256 |
| 7 | Freeze assembly | PARTIAL (TEST assembler and byte-agreement check run) | 1.5 d, after 2, 3, 5, 15 | **yes** |
| 8 | Conformance vectors | PARTIAL (352 cases, 352/352 agree; freeze inclusion open) | 0.75 d | **yes** (feeds 7) |
| 9 | ENCODING-V1 and PROOF wording | DONE | 0 | no |
| 10 | Snapshot re-capture in §15.3 form | DONE (instrument, real-1) | 0 | no |
| 11 | Decision-function completion | DONE (text; vectors via 8) | 0 | no |
| 12 | DNSSEC/body completion | DONE (text; vectors via 8) | 0 | no |
| 13 | Proof completion | DONE (text; vectors via 8) | 0 | no |
| 14 | Signature completion | DONE (text; vectors via 8) | 0 | no |
| 15 | Dependency closure | BUILT 2026-10-19 (44 entries, sha256 20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063; formal/dependency-sources/MANIFEST.md); profile §9, §15.6, §15.9 folded in [OWNER 2026-10-19, item 15]; open: gpgv version not fixed, owner review | 1.5–2 d | **yes** (its hash is in the catalog) |
| 16 | Total report-check table plus multi-failure cases | DONE (instrument; enters the vectors via 8) | 0 | no |

**Counts: 8 DONE, 6 PARTIAL, 1 NOT BEGUN, 1 NOT NEEDED FOR FREEZE, 0 MOOT.** *Updated 2026-10-19 after the profile edits: 11 DONE, 3 PARTIAL (7, 8, 15), 1 NOT BEGUN, 1 NOT NEEDED FOR FREEZE.* No §14.2 item is about the listing:
the listing came from A10, not from this list. The cut (`docs/decisions/2026-10-19-listing-cut.md`) makes nothing
here moot, and the proposed release format below has no listing, OTS stamp or C0/C1 bootstrap in it.

**Remaining: about 6.4–6.9 agent-days**, and about 4 of them are serial. **Critical path:** profile text for items
2, 3, 5 (and item 1's reconciliation) plus the real dependency-manifest bytes (15) → freeze assembly (7), with
item 8's regeneration and inventory done in parallel but before the vectors object is hashed. Item 6 joins the path
only if YubiKey 2 cannot hold a P-256 OpenPGP key.

## 2. Each item

### 1. Release-key custody — NOT NEEDED FOR FREEZE

- **Evidence.** A10.4.2 moves the gate to the first public verifier release (A10:635-643, row 34 at A10:770). What
  the freeze must register is the requirement, the release format (item 2) and "the custody procedure's required
  contents"; those contents are already stated in A10.4.2's "Custody form" bullet (A10:628-634). The procedure
  itself is `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` (DRAFT, author corrections open at §6, §8, §9, §10).
- **What the freeze still needs (0.25 d).** A10.4.2 says profile §5, §14.2 items 1–2 and runbook §6 "are
  reconciled … after this amendment's signing commit" (A10:672-674). Not done: `V1-PROFILE.md:418-419` still says
  the release key's "fingerprint is in the freeze record", which A10.4.2 replaces with the first-production-release
  bootstrap record; `:1270-1272` still frames custody as a freeze item; `docs/V1-OPERATIONS-RUNBOOK.md:115` says
  "Due before the 30 Oct freeze". The proposed text in §3 (R5) supplies the replacement for `:418-419`.
- **After the freeze (gate work, not counted above).** Ceremony, review VM, media crossing, rehearsal including the
  A10 row 36 TEST-refusal rehearsal, custody record. YubiKeys arrive 20 Oct.

### 2. Release artefact and release-signature format — PARTIAL

- **Update 2026-10-19: format DONE.** Profile §15.9 adopts §3 with the owner decisions (code bound per release by `RELEASE.json` `parts`; fingerprint through two independent channels). Departures closed: TEST releases use the §15.9 R3 format over the whole archive; mode comes from the installed archive, no `--production` flag, TEST only by an explicit path (R4); machine facts move to an unsigned `install.json` (R2). Remaining: the instrument changes listed at the end of §15.9.

- **Evidence.** A TEST stand-in runs end to end: `prototype/conformance/universe.py:713-726` (`make_release`),
  `prototype/indep-verifier/release_auth.py` (format `tessera-v1-test-release/1`, production refusal
  `TEST_AUTHORITY_REFUSED`), `prototype/e2e/driver.py:455-474` (stage `release`), the real-1 receipt verified through
  it (`prototype/e2e/receipts/real-1/release.json`, commit `9095b86`), and the rehearsal-shaped unit test
  `prototype/indep-verifier/tests/test_release_auth.py:135-143`. The custody draft proposes the production signature
  (`V1-RELEASE-KEY-CUSTODY-DRAFT.md:63-77`).
- **What is missing.** No production format exists in the profile (`V1-PROFILE.md:425-426`, §3.5 at `:333-335`). The
  TEST stand-in signs only a record of two hashes, not the verifier code (see R3 below).
- **Remaining (1 d).** Adopt §3 below into the profile (0.5 d with a Codex pass), and move the TEST path of the e2e
  `release` stage to the same archive format with a TEST key so that the pre-gate rehearsal tests the real
  production procedure (0.5 d).

### 3. Pre-freeze trust-configuration values — PARTIAL

- **Update 2026-10-19: DONE for the freeze.** Profile §5 "Sourced trust values" (three-way record, citing `formal/trust-sources/`); KSK-2017 publication 2017-07-11; the 2026-10-11 switch needs no time of day, because KSK-2017 reliance runs to 2026-11-01 and KSK-2024's 00:00Z start equals its first RRSIG inception. Carried to config v1: ICANN CA by a second path, repository entry, pins. `formal/trust-sources/` must be committed.

- **Evidence.** Schema done (`V1-PROFILE.md:1541-1582`). Values proposed in the profile: KSK-2017 policy
  `signing_start` 2018-10-11T16:00:00Z, "still OPEN until the sources are archived" (`:527-537`); KSK-2017 end and
  KSK-2024 start 2026-10-11T00:00:00Z, "proposed … until the same three-way record exists" (`:533-535`); L = 21 d
  (`:464`). `prototype/e2e/trustcfg.py` builds real KSK entries from IANA material, byte-matched to live RRsets,
  but the archive is in git-ignored `prototype/e2e/work/root-anchors/` (not tracked: `git ls-files` finds no
  `root-anchors*`), and the `.p7s` check used an `icannbundle.pem` fetched over the same HTTPS channel, "**not** the
  independent bootstrap §5 asks for" (`prototype/e2e/README.md`, "Ran on real material").
- **Remaining for the freeze (0.75 d).** Archive the sources in the tracked tree; obtain the ICANN CA by a second,
  recorded path; write the three-way record (switch time, RRSIG inception evidence, policy value) for the three
  endpoints; settle the profile text.
- **Not needed for the freeze.** The trust configuration is not a frozen spec part; it is compiled into a release
  (§5, `:410-415`). Config v1's repository entry (the real YubiKey 2 key) and its header pins are built for the
  first production release. The real-1 run used a TEST repository key (`prototype/e2e/README.md`, item 6).

### 4. Hybrid branch — DONE

`formal/p8/HYBRID-REGISTRATION-RECORD.md:1-5`; `V1-PROFILE.md:1287-1291`. The frozen spec-object hash it still needs
is item 7's.

### 5. Slot-2 custody choice — PARTIAL

- **Update 2026-10-19: DONE.** Profile §8 "Slot-2 custody record". Monoculture: AWS KMS runs on the AWS Key Management Service HSM (vendor Amazon Web Services, FIPS 140-3 L3, CMVP #4884); Google Cloud HSM devices are Marvell (formerly Cavium). No shared vendor at module level; components below the module are not public. VPC-SC perimeter not deployed (operations).

- **Evidence.** The choice was made: GCP Cloud KMS HSM through the policy signer, "slot-2 custody chosen 2026-10-13"
  (`docs/reviews/hybrid-supplement/DECISIONS.md:3`). The deployed-slot evidence met the 21 Oct deadline on 14 Oct
  (`HYBRID-REGISTRATION-RECORD.md`, evidence item 4; `prototype/policy-signer/EVIDENCE.md:48`, latency 3–70 s). The
  real-1 receipt was signed through it (`prototype/e2e/FINDINGS.md:48-50`).
- **Missing.** A9.6 requires the choice "recorded, dated, in the profile before the 30 Oct freeze" (A9:375-377). The
  profile does not name GCP or an HSM anywhere (`grep -n -i "gcp\|hsm\|google" docs/V1-PROFILE.md`: no hit in §8).
  The monoculture check is open (`docs/V1-OPERATIONS-RUNBOOK.md:52-56`; GCP attests Marvell/Cavium,
  `docs/handoff-2026-10-18-owner-tessera-e4.md:40`; AWS KMS's HSM is not yet identified).
- **Remaining (0.5 d).** Identify AWS KMS's HSM vendor and certification from AWS documentation; write the dated
  §8 record (provider, key version, policy boundary, adapter, public-key packet, measured latency, monoculture
  result).

### 6. Repository-root algorithm — NOT BEGUN

- **Evidence.** YubiKey 2 is not in hand (`V1-PROFILE.md:1271-1272`; arrival 20 Oct). The profile fixes the
  repository key as v4 ECDSA P-256 (`:1538`, `:1568`).
- **Remaining (0.1 d, 20 Oct).** Read the firmware version and confirm the OpenPGP applet generates P-256 (YubiKey 5
  firmware 5.2 or later; a prediction until read). If it cannot, the dependency manifest and §15.4 change before the
  freeze.

### 7. Freeze assembly — PARTIAL

- **Evidence.** `prototype/e2e/freeze.py` assembles the §15.8 spec and vectors objects from tracked blobs at a named
  commit, writes hashes outside the parts, and has an independent byte-agreement check (`freeze.py:185-206`). Its
  preamble, dependency manifest and catalog are TEST stand-ins (`freeze.py:15-19`, `:39-42`, `:65-70`, `:142-150`),
  and its vectors inventory is a TEST choice (`:36`).
- **Remaining (1.5 d, after items 2, 3, 5, 15).** Author the real preamble bytes; one catalog byte format with Δ and
  m added (profile §13 note 15, `:1229-1231`; today the TEST release carries a universe catalog object that
  `release_auth.translate_catalog` converts to `tessera-v1-independent-catalog/1`, so two byte forms exist); the
  real vectors inventory (item 8); the freeze commit; the freeze record (hashes, A9 signing commit, the
  branch-registration entries of `:1305-1309`, refresh of every `A9:nnn` locator).

### 8. Conformance vectors — PARTIAL

- **Evidence.** `prototype/conformance/cases-index.json` has 352 cases. They cover RES §L L-01 to L-111 with
  letter-suffixed ids (for example L-52a/b, L-61a/b, L-111a-c); L-27/L-28 are the r2-F16 replacements
  (`REPORT.md:459-460`); the r2 distinguishing cases are built as `ALG-*`, `RC-*`, `F03-*`, `F05-*` to `F10-*`,
  `F12-*`, `F15-*`, `AGG-*` (`REPORT.md:119-121`). Differential run 6: 352/352 AGREE
  (`prototype/differential/results-run6.json`, untracked).
- **Not built.** L-94, the SHA-1DC collision object, needs a fresh chosen-prefix collision (`REPORT.md:174-178`).
  F04's repository "mixed" case cannot be constructed (`REPORT.md:188-190`). Both need a dated owner disposition in
  the freeze record, not more work.
- **Remaining (0.75 d).** Add Δ and m to the universe catalog and regenerate (deterministic, `REPORT.md`
  "Determinism"); track the 10 untracked `UTC-*` case directories and `results-run6.json`; fix the vectors
  inventory: which case files enter the vectors object, run under the universe TEST catalog and TEST release key
  they embed (EA-10, `REPORT.md`: "the real vectors object … cannot contain these cases, which embed its hash").
  The cases are 1,382 tracked files, 14 MB.

### 9. ENCODING-V1 and PROOF wording — DONE

`V1-PROFILE.md:1329-1337`; `docs/reviews/levadura-contradictions/DISPOSITION.md`.

### 10. Snapshot re-capture in §15.3 form — DONE (instrument)

The real-1 receipt carries a live `_tessera-v1.wamason.com` capture converted to the §15.3 body, stamped and anchored
at height 972187, validated under the real KSK-2024, and cross-checked by dnspython (`prototype/e2e/FINDINGS.md:47-62`,
commit `9095b86`). Every production receipt re-captures anyway (profile §4).

### 11–14. Decision-function, DNSSEC/body, proof and signature completion — DONE

Each item's own text says "Text now in sections …; vectors in item 8" (`V1-PROFILE.md:1338-1349`). The named
vectors exist (item 8 evidence). They count once item 8's cases enter the frozen vectors object.

### 15. Dependency closure — PARTIAL

- **Evidence.** SHA-1DC is pinned by commit and source digests, with its collision-return behaviour recorded
  (`prototype/vendor/SHA1DC-PIN.md`), and `prototype/indep-verifier/packaging/install.sh:34-41` checks the digests.
  The manifest itself is a TEST stand-in with `"TEST"` in every field (`prototype/e2e/freeze.py:65-70`); the profile
  says "Not yet the object" (`V1-PROFILE.md:1064-1068`).
- **Remaining (1.5–2 d).** About 35 entries (§9's list) with editions, sections, errata, digests, retrieval and
  redistribution; archive the referenced bytes or immutable sources; add the release-signature dependency (gpgv,
  from R3 below); hash-pin `cryptography` (today `requirements.txt` pins the version only). Its hash goes into the
  catalog, so it gates item 7.

### 16. Total report-check table plus multi-failure cases — DONE (instrument)

Table in §15.7. Multi-failure cases `AGG-a` to `AGG-h` (across and within stages, including possession, DNS and git)
all AGREE in run 6. They count with item 8.

## 3. Proposed: release format

Proposed text for a new profile §15.9 and for the replacement of `V1-PROFILE.md:418-419` and `:425-426`. Every rule
is **OWNER PROPOSAL 2026-10-19**; the source is given after each. Frozen at the 30 Oct freeze: R1–R6. Executed after
the freeze, before the first public verifier release: the key, the ceremony, the bootstrap record, the rehearsal
(A10.4.2).

**R1. A release is one archive** [sources: A10:639-641; custody draft §2 "release archive"; profile §15.8].
- The **release archive** is one file, `tessera-verifier-v1-<n>.parts` (production) or
  `tessera-verifier-v1-TEST-<n>.parts` (TEST), where `<n>` is the canonical decimal release number.
- Its bytes are the §15.8 part format: header grammar, sorted paths and verbatim blob bytes, all exactly as §15.8.
  Every part is a tracked regular-file blob at one named **source commit**. Nothing is generated during assembly.
- Required parts: `RELEASE.json` (R2); `trust.json`, the exact §15.5 trust-configuration bytes; `catalog.json`, the
  exact frozen catalog bytes (item 7 fixes their format); `release_constants.py` (R2); the verifier source; the
  pinned dependency lock (R6); the vendored SHA-1DC source with `SHA1DC-PIN.md`; the install and run scripts; the
  relying-party text. No other part carries authority.
- *Departure:* the custody draft names a `.tar`. The part format is used because one file set has exactly one byte
  string (no modes, owners, timestamps or tar dialects). The existing assembler and its independent byte-agreement
  check (`prototype/e2e/freeze.py:185-206`) let the review environment rebuild the archive from the source commit and
  compare hashes, which C01's review-and-build step needs. Scripts run as `bash install.sh`, so no file mode is
  needed. The archive is unpacked only after R3 succeeds.

**R2. How the trust configuration and catalog bind** [sources: profile §5 `:410-417`; A10:639-641;
`build_release.py`; `release_auth.provision`].
- `RELEASE.json` is one JCS object with string values only and exactly these keys: `format`
  (`"tessera-v1-release/1"`), `namespace` (`"PRODUCTION"` or `"TEST"`), `release` (= `<n>`), `profile`
  (`"tessera-v1-strict"`), `source_commit` (40 lowercase hex), `trust_config_sha256`, `trust_config_version`,
  `catalog_sha256`, `freeze_record_sha256`, `release_key_successor` (a v4 fingerprint, 40 uppercase hex, or null).
- **Binding equalities**, checked before signing and again by `install.sh`; any failure means no installation:
  SHA-256(`trust.json`) = `trust_config_sha256` = `release_constants.TRUST_SHA256`; SHA-256(`catalog.json`) =
  `catalog_sha256` = `release_constants.CATALOG_SHA256`, and `CATALOG_BYTES` equals `catalog.json`; the version
  inside `trust.json` = `trust_config_version`. Under `PRODUCTION`, `catalog_sha256` equals the catalog hash in the
  freeze record whose SHA-256 is `freeze_record_sha256`.
- At run time the existing rule is unchanged: a `--trust` file whose hash is not `TRUST_SHA256`, or that fails §15.5,
  is `TRUST_CONFIG_UNAUTHENTICATED`, with no verdict.
- Each new release's `trust.json` passes the release checker (§5 release invariants, EA-12) against the previous
  release's `trust.json`.
- *Departure:* `build_release.py` today writes `UNICODE_MODULE_SHA256` and `SHA1DC_AVAILABLE` from the build machine
  into `release_constants.py`, and `verify.py` compares the running interpreter's `unicodedata` file hash with it.
  Those are facts about one installation. They move to install time (as `install.sh` already does with
  `sha1dc_build.json`), so that the archive's bytes do not depend on the build machine.

**R3. The release signature** [sources: custody draft §3 `:63-77`; profile §8 rule O; profile §15.4].
- The signature is a **detached, binary (unarmored) OpenPGP v4 signature of type 0x00** over the exact archive
  bytes, file `<archive>.sig`. Algorithm ECDSA P-256 with SHA-256. It satisfies rule O's grammar and policy
  (section 8), as the git `gpgsig` does after dearmoring (§15.4). GnuPG's output meets this (§8, "GnuPG's output …
  satisfies it").
- The release key is **one v4 ECDSA P-256 primary key with no subkeys**. Its identity is its full v4 fingerprint.
  A signature by any other key, or by a subkey, does not authenticate a release.
- The signature covers the whole archive: the code, the lock, `trust.json`, `catalog.json` and `RELEASE.json`. The
  key never signs a hash written as text (custody draft §3).
- **Relying-party acceptance.** Accept iff the pinned `gpgv` exits 0 on `<archive>.sig <archive>` with a keyring that
  holds **only** the production key whose full fingerprint was obtained by R5. The signing session also checks the
  new signature against rule O before it leaves the session.
- *Departure:* the TEST stand-in (`tessera-v1-test-release/1`) signs only the JCS of `{catalog, catalog_sha256,
  format, trust_config_sha256}` with a raw r‖s value and names the signer by SPKI hash. It does not cover the
  verifier code, so a substituted verifier with a genuine record would pass. It also cannot be produced by the
  YubiKey's OpenPGP applet through GnuPG, which the custody draft uses. It stays only as the §3.5 instrument
  interface for the conformance and differential harnesses, and it is never a release.

**R4. TEST and production** [sources: A10.4.2 row 36 (A10:772), A10:644-660; `release_auth.py`;
`test_release_auth.py:135-143`].
- Every release before the first public verifier release is a **TEST release**: `namespace` `"TEST"`, a `TEST` file
  name, signed by a TEST release key in the R3 format. TEST keys are throwaway v4 P-256 keys and may live on the
  operational computer (as `prototype/e2e/repo.py` does for the TEST repository key), because they authenticate
  nothing. A TEST public key is never published as the release key, never named in the freeze record, the
  bootstrap record or relying-party text, and never named in any `release_key_successor`.
- The production key signs only `namespace` `"PRODUCTION"`. A TEST key signs only `"TEST"`. The signing session
  checks this before signing.
- **Production refusal is by key, not by label.** A TEST signature fails R3 because the production keyring holds
  only the production key. The `TEST` label prevents honest mistakes. It is not a security check, because an
  attacker can remove it (XP-02).
- A `PRODUCTION` archive's `release_constants.py` sets `PRODUCTION = True`. With it, the verifier refuses
  `--test-release`, `--test-release-key` and any `TESSERA_V1_TEST_*` variable with `TEST_AUTHORITY_REFUSED` and no
  verdict, whatever the command line says. *Departure:* today production mode is a CLI flag
  (`verify.py:307`, `release_auth.authenticate(..., production)`), so an invocation without it accepts TEST
  provisioning. The refusal logic itself is reused unchanged.
- **Rehearsal (A10 row 36).** Before the first public release: an otherwise correct archive signed only by a TEST key
  is refused by the R3/R5 acquisition procedure, including when the TEST public key is offered as the key; and the
  installed production verifier refuses the TEST interface. The second half is
  `test_release_auth.py:135-143`; the first half is new.

**R5. Out-of-band authentication of the production key** [sources: A10:668-674 (bootstrap record); custody draft
§8 "Public-key bootstrap" and §10; contract review XP-02 (`docs/reviews/exit-pages/CODEX-REVIEW.md:9-13`);
profile §5 `:418-419`].
- The relying party's root of trust is the production key's **full v4 fingerprint**, obtained **before and apart
  from** any release. A key or fingerprint that arrives with a release, on the same page as a release, or from the
  operational computer, the repository, DNS or the issuing AWS account authenticates nothing.
- The fingerprint is recorded in the dated **first-production-release bootstrap record**. That record names the
  freeze record (by hash) and the production key, and is published and OpenTimestamps-stamped. Publication and
  stamping give a dated public record. They are not authentication.
- **Delivery channel (owner proposal; the author names the final one, custody draft §8 step 5).** For V1's one
  tester (4 Dec): the author gives the full fingerprint directly, in person or by a voice call to a number the tester
  already knows, and the tester compares all 40 hex characters. The author can add a second channel for others. If
  no independent channel is named, the relying-party text states authenticated first acquisition as an assumption,
  as A10.4.2 does ("does not protect a user who … acquires a substituted initial key").
- **Rotation.** A new release key is introduced only by a production release, signed by the current key, whose
  `release_key_successor` names it. The next release is then signed by the successor. (Profile §5 already says
  this.)
- **Loss or compromise.** V1 has no assured recovery. New releases stop. A replacement key needs a new out-of-band
  delivery and a new dated bootstrap record. Genuine old releases stay available for existing receipts (custody
  draft §10).
- **Replacement for `V1-PROFILE.md:418-419`:** "Bootstrap: the production release key's full fingerprint is
  delivered out of band (§15.9 R5) and recorded in the dated first-production-release bootstrap record (A10.4.2).
  The freeze record does not contain it. A new release key is introduced only by a release signed by the current
  one."

**R6. Dependency pinning** [sources: profile §9, §14.2 item 15; `packaging/install.sh`; `SHA1DC-PIN.md`].
- The archive carries a lock with exact versions **and SHA-256 hashes** for every Python package, installed with
  hash checking required. Wheels are retrieved at install time and are not distributed. *Departure:*
  `requirements.txt` pins `cryptography==50.0.2` without a hash.
- Python 3.14 with Unicode 16.0.0 tables is checked at install and at start (as today). SHA-1DC is built from the
  vendored, digest-checked source (as today).
- The relying party's `gpgv` version and the OpenPGP standard it implements are entries in the dependency manifest
  (item 15). Verification is offline after installation; installation is not.

**What the TEST pipeline already does that R1–R6 keep:** the trust-hash refusal, the catalog-hash refusal, the
release checker, `TEST_AUTHORITY_REFUSED`, the §15.8 assembler and byte-agreement check, the SHA-1DC pin and the
install-time checks.

## 4. The two hardest open questions in the release format

1. **Which independent channel delivers the production fingerprint?** Every other rule reduces to "check against
   the authenticated key", and XP-02 rules out the easy answers. The operational computer, the repository, DNS and a
   pair of web pages are all excluded, and so is anything that travels with a release. Voice or in-person delivery
   works for one tester and does not scale. If the author names no channel, every relying party except a
   hand-delivered one relies on an assumption, and G1–G10 then hold only conditionally (contract §2, "the checker's
   verifier release is authentic"). Only the author can supply this channel. It is due before the first public
   release, not the freeze, but the relying-party text frozen on 30 Oct must already say which case applies.
2. **What does the frozen format bind when the production verifier code does not exist yet?** The exit opens
   Phase 1a "for V1-profile code only" (A9:218). The contract says there is only one V1 verifier, and today that is
   the instrument `prototype/indep-verifier/`. R1 freezes the container, the manifest, the bindings and the
   signature, but not the code inventory. Two things must be decided by 30 Oct: (a) whether the first public
   release ships the instrument verifier (promoted out of `prototype/`) or new Phase 1a code; and (b) which parts
   are mandatory, so that the review-and-build check (C01) has a fixed list to compare. If (a) is "new code", the
   rehearsal and the e2e TEST releases test a different program from the one that is shipped.

---

## Owner decisions on the two hardest questions (2026-10-19)

1. **What the frozen release format binds.** OWNER DECISION: the format freezes the envelope (archive parts, release
   manifest binding the trust-configuration and catalog hashes, detached signature, TEST/production key rules), not
   the verifier's code bytes. The verifier code is a release member whose hash the manifest binds per release.
   **Reading of A9.2 "service code never imports it":** "imports" means a runtime or build dependency, not reuse of
   design or source. After the signed opening commit, the service verifier may be ported from
   `prototype/indep-verifier/`; it must then earn its own evidence (E10 vectors against it, the P9 code inspection,
   A9:214) on its own bytes. Instrument results never count for it.
2. **The production release-key fingerprint channel.** The freeze fixes the rule only: the fingerprint is published
   through at least two channels independent of the operational environment (the NUC, this repository, DNS, AWS),
   named in the custody record before the first public verifier release (A10.4.2). The channels are the author's to
   name. Owner recommendation for then: a Zenodo record under the author's ORCID, plus one offline printed copy.

**Added 2026-10-19 (owner):** §15.9 accepts a distribution `gpgv` only if it matches upstream GnuPG 2.4.4 exit status
on the release-format test vectors. Those vectors do not exist yet. They are needed before the first public verifier
release (not for the freeze): valid TEST and production signatures, wrong key, TEST key presented as production,
truncated archive, signature over a different archive.
