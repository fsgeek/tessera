# Verifier release 1: release summary (candidate, unsigned)

Owner instance (Claude Opus 5.5), 2026-11-23. This is the release summary of custody draft §9 ("Preparation on the
NUC"). It is an aid, not evidence of approval: the author's own build and check on the Pangolin
(`docs/ceremony/release-v1-1-SHEET.md`) are the approval steps. Procedure: `docs/V1-RELEASE-PROCEDURE.md`.

## The candidate

| | |
|---|---|
| Archive | `tessera-verifier-v1-1.parts` (profile §15.9 R1; 709203 bytes, 32 parts) |
| Archive SHA-256 | `49e65de3 b460c589 25c75329 35dabd91 8d81828f df8cf4b8 ff9be745 b730d829` |
| Namespace, release | `PRODUCTION`, `1`; `release_key_successor` null |
| Source commit | `7b986e8357d26b1fd1604217e1a5a2a6d3868f23` (branch `release-rc`; must be on GitHub before the sitting) |
| Signature (to be made) | `tessera-verifier-v1-1.parts.sig`: detached, binary, OpenPGP v4 type 0x00, ECDSA P-256, SHA-256, by `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` (YubiKey B) |
| Build | `python3 service/verifier/release/release_tool.py build --repo . --commit 7b986e8357d26b1fd1604217e1a5a2a6d3868f23 --out OUT` |

**Reproducibility.** Built twice on 2026-11-23: once from this worktree, once from an independent `git clone
--no-local` checked out at the source commit, each with its own copy of the tool. The two archives are byte-identical
(`cmp`), both SHA-256 `49e65de3…b730d829`. The archive depends only on tracked blob bytes at the source commit and at
the freeze commit; no time, user, path or file mode enters it.

## What is in it

`RELEASE.json` (generated, R2) and 31 parts copied verbatim from the source commit:

- **Verifier code**: `service/verifier/tessera_verify/*.py` (12 files) except `release_constants.py`, whose
  unprovisioned source-tree copy is left out; `pyproject.toml`; `README.md`.
- **This release's bindings**: `service/verifier/release/v1-1/trust.json` and `…/v1-1/release_constants.py`
  (`NAMESPACE = 'PRODUCTION'`, the trust and catalog hashes, the catalog bytes, `UNICODE_VERSION = '16.0.0'`; no
  machine facts). `install.sh` copies it into the package after re-checking R2.
- **Catalog**: `formal/freeze-v1/objects/catalog.json`, the frozen bytes at their frozen path.
- **Installer and dependencies**: `install.sh` (now with a release mode) and `requirements.lock` (cffi 2.1.1,
  cryptography 50.0.2, pycparser 3.12, with the SHA-256 of every PyPI file; installed with `--require-hashes`, R6).
- **SHA-1DC**: `vendor/SHA1DC-PIN.md` and the vendored upstream source (9 files, including the SHAttered PDF used as
  the install-time known answer).
- **Relying-party text**: `docs/V1-RELYING-PARTY.md`.
- **Release tool**: `service/verifier/release/release_tool.py`, used by `install.sh` to re-check R2. A relying party
  gets the same file separately from GitHub before acquisition (R3: the checker is available before the archive is
  executed).

Not in it: tests, the release vectors, the issuer, anything under `prototype/`.

## Every hash and how it traces

| Object | SHA-256 | Traces to |
|---|---|---|
| Archive | `49e65de3b460c58925c7532935dabd918d81828fdf8cf4b8ff9be745b730d829` | Rebuilt by the author from GitHub at the source commit; equal, or stop. |
| Freeze record (`formal/freeze-v1/FREEZE-RECORD.md` at `52ee179`) | `05542967b091424a614afd38a32cfb847b9b6b3f0e5a7b7103b11cd22d95575e` | `RELEASE.json` `freeze_record_sha256`. Commit `52ee17918c5e…` is the author's signed freeze commit (2026-10-24); OpenTimestamps proof `timestamps/anchored/52ee179….ots`. |
| Catalog (`catalog.json`, 662 bytes) | `aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2` | The freeze record's table row; byte-equal to `formal/freeze-v1/objects/catalog.json` at `52ee179`; recomputed from source by `formal/freeze-v1/assemble.py --commit 270ca49` (2026-11-23: equal). Equals `release_constants.CATALOG_SHA256`; `CATALOG_BYTES` equals the part. |
| Spec object (named in the catalog) | `397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf` | The freeze record; recomputed by the assembler (equal). Bound through the catalog's `spec_sha256`. |
| Vectors object (named in the catalog) | `19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f` | As above, `vectors_sha256`. |
| Trust file (`release/v1-1/trust.json`) | `9faa03683df7506cefa07afa4c0629182ebc5d4286b97801e1053cb8d86a7f89` | `trust_config_sha256` = `release_constants.TRUST_SHA256`. Not in the freeze record (trust is per release, profile §5). Byte-identical to `docs/smoke/2026-11-16-first-receipt/trust.json` (its `SHA256SUMS`). |
| `release_constants.py` (v1-1) | `f30e2e5988fc10a9b610e942b3a27952ed374d94b8e66350c9b470c87eef306a` | Generated once by `release_tool.py constants` from the trust file and catalog, then committed. |
| `release_tool.py` | `3a506e9eae09e24f25aa41c5f18477782bebb86f2082d1b54d16d284820e045c` | The author reads it before use; this hash goes on his paper. |
| `docs/ceremony/sign-release.sh` (not in the archive) | `f9a0a5f6ed1bfe0bf5abd402da2be73be5982cb6c53334c455c4377a2cf5c5b4` | As above. |
| Release public key `docs/ceremony/keys/release-CADC…035E.pub.asc` | `1a817ae39f97450184d85e5c09bbdc0a301b18be65c8c3975144d3d8160cf6f3` | The key received on REL-PUB at the 2026-11-10 ceremony (`2026-11-10-operator-data.md`: `1a817ae39f974501…`); its fingerprint is on the author's paper and ORCID record. |

The other parts' hashes are in `RELEASE.json` `parts`; `release_tool.py check` compares each part with its blob at
the source commit.

### The trust file's authority entries

| Entry | Value | Source; check at the sitting |
|---|---|---|
| Repository key | v4 fingerprint `6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A`, open from `2026-11-10T19:44:55Z` | YubiKey A, ceremony 2026-11-10. The author compares it with his paper record and ORCID. |
| KSK-2017 | tag 20326, DS `e06d44b8…c7f8ec8d`, signing ended 2026-10-11, reliance 21 days | IANA `root-anchors.xml`; `release_tool.py sources` compares over Tor. |
| KSK-2024 | tag 38696, DS `683d2d0a…c0fb2b16`, signing from 2026-10-11 | As above. |
| Header pins | 12: heights 975705–975710 and 976141–976146 | Fetched from blockstream.info and mempool.space, which agreed, on 2026-11-16. `sources` re-checked all 12 against both on 2026-11-23 (all equal); the author repeats it over Tor. |

`version` 1, `previous_sha256` 64 zeros, `as_of` `2026-11-16T15:48:11Z`. No previous release exists, so the release
checker's cross-release invariants have nothing to compare.

**What these pins cover.** 975705 is the key assertion's OTS anchor (2026-11-13) and 976141 the first production
receipt's (2026-11-16). Every bundle header must be pinned, else `UNVERIFIABLE / HEADERS_NOT_COVERED` (profile §5).
So release 1 verifies the first production receipt and nothing anchored later. Each later receipt height needs a
later release (trust version 2 or more), made by this procedure with a signing sitting.

## Checks run on the NUC, 2026-11-23

- `release_tool.py check` from the independent clone: `CHECK PASS`.
- `release_tool.py sources`: `SOURCES PASS: 2 KSKs and 12 pins equal their public sources` (direct HTTPS, not Tor).
- The candidate unpacked, `install.sh` run inside it (R2 re-check, hashed lock), then the installed verifier in its
  default (production) mode on the first production receipt: `VALID_STRICT / OK`, `T` `2026-11-16T14:35:57Z`,
  `A-UTC-7200-6`, the same stable result as the smoke test.
- `install.sh` in an unpacked tree with one byte appended to `verify.py`: `REFUSED: part hash differs: …verify.py`,
  then `release bindings (R2) failed: not installed`.
- `service/verifier/tests/test_release_tool.py`: 15 pass. The whole verifier suite: 149 pass, 1 fails (the known
  worktree-only independence check, which loads the main checkout's editable install).

### A10 row 36 (a TEST-signed release must be refused): what is shown, what remains

Shown on the NUC (`evidence/row36.txt`, `evidence/dry-rehearse.txt`):
1. The production candidate signed only by a throwaway TEST key, presented to the acquisition procedure
   (`release_tool.py acquire`, fingerprint `CADC…035E`): refused, `signed by <TEST>, not by the authenticated key`,
   with the production public key and again with the TEST public key offered as the key. Nothing was unpacked.
2. The same signature verifies when the TEST fingerprint and key are named explicitly (R4 path (a)), so the refusals
   are by key, not because the tool refuses everything.
3. The committed release vectors under the acceptance rule: all 9 cases give their `accept` value, including 09
   (TEST key offered as the keyring: gpgv exits 0, acceptance refuses).
4. The installed production verifier refuses the §3.5 interface: an authentic `tessera-v1-test-release/1` record
   (the kind the smoke test used, which the source tree accepts in `--mode test` with `VALID_STRICT`) gives
   `TEST_AUTHORITY_REFUSED`, exit 2, both by flags and by `TESSERA_V1_TEST_*` variables.
5. The rehearsal script's TEST branch (`sign-release.sh rehearse`) in a simulated session (Tails paths and session
   checks replaced; Ubuntu gpg 2.4.4): every step passed, row 36 refused twice, vectors 9/9.

Remains for the rehearsal (A10.4.2 requires a rehearsal; these are its parts): the same TEST branch on the Pangolin
under Tails, offline, by the author, with Tails' GnuPG (2.4.7 at the ceremony), including its gpgv on the vectors (R3:
a distribution build is acceptable only if it reproduces upstream's exit status); the networked phase's build, check
and source comparison over Tor; the measured time. Item 4 needs Python 3.14 and cannot run on Tails; it is evidence
from the NUC only, and the dead-service test (a clean machine) can repeat it.

## What changed from the TEST release used in the smoke test (2026-11-16)

| | Smoke test (TEST) | Release 1 (candidate) |
|---|---|---|
| Form | No archive. A `tessera-v1-test-release/1` record (two hashes, raw r‖s) through the §3.5 instrument interface, `--mode test`, from the source checkout | The §15.9 R1 archive, R2 manifest, R3 signature over the whole archive, code included |
| Signer | An in-memory P-256 key made by `rp_verify.py`, discarded | The production release key `CADC…035E`, YubiKey B, offline on Tails |
| Mode | TEST, provisioned in memory for one process | PRODUCTION, from the installed `release_constants.py`; every TEST flag or variable is refused |
| Trust file | `trust.json`, SHA-256 `9faa0368…d86a7f89` | The same bytes |
| Catalog | The frozen catalog (`aaf4306f…`), carried inside the TEST record | The same bytes, as a part and compiled into `release_constants.py` |
| Verifier code | `tessera_verify/` as of `b134cdf` (2026-10-26) | Unchanged: no commit has touched `tessera_verify/` since `b134cdf` |
| Installer, dependencies | `install.sh` from `requirements.txt`, no hashes | `install.sh` adds the release mode (R2 re-check, constants install); dependencies from `requirements.lock`, hashes required |
| New | — | `release_tool.py`, `release/v1-1/`, `requirements.lock`, a README section |

## Owner choices made here (no registered text decides them)

- The release's own files live under `service/verifier/release/v1-<n>/`, and `install.sh` installs that
  `release_constants.py`. The source tree's `tessera_verify/release_constants.py` stays unprovisioned, so the source
  tree's tests and TEST harness keep working. Every part is still a verbatim blob at the source commit (R1).
- "The freeze record" in `freeze_record_sha256` is `formal/freeze-v1/FREEZE-RECORD.md` at the signed freeze commit
  `52ee179` (the JSON form is labelled draft).
- The trust file is the smoke test's, unchanged: its entries were already checked against their sources, and it
  covers the first production receipt.
- Acceptance also requires the hashed issuer-fingerprint subpacket (rule O allows its absence); GnuPG 2.4 always
  writes it, and the signer's identity cannot otherwise be confirmed before `gpgv` runs.
