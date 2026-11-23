# Verifier release 1: release summary (candidate 2, unsigned)

Owner instance (Claude Opus 5.5), 2026-11-23. This is the release summary of custody draft §9 ("Preparation on the
NUC"). It is an aid, not evidence of approval: the author's reading of the printed change list (`DIFF.txt`) and his
own build and checks on the Pangolin (`docs/ceremony/release-v1-1-SHEET.md`) are the approval. Procedure:
`docs/V1-RELEASE-PROCEDURE.md`. Candidate 1 (`49e65de3…`, source `7b986e8`) is withdrawn after the Codex review
(`docs/reviews/release-v1-1/CODEX-REVIEW.md`; dispositions in `DISPOSITION.md` there).

## The candidate

| | |
|---|---|
| Archive | `tessera-verifier-v1-1.parts` (profile §15.9 R1; 709298 bytes, 31 parts) |
| Archive SHA-256 | `7fd00606 b5591d9a 3a410512 776e3a0e 82fa2662 8c179987 49ca1a0d a61de614` |
| Namespace, release | `PRODUCTION`, `1`; `release_key_successor` null |
| Source commit | `f2511c0d87f390396b50e687a7bef496544462da` (branch `release-fixes`; must be on GitHub before the sitting) |
| Baseline commit | `b134cdfdacc5d89f2748fa7ec15c46e38b51a32c` (the Codex-reviewed verifier, 2026-10-26; OpenTimestamps block 973240) |
| Change list | `DIFF.txt`, last line `DIFF 7 added or changed, 0 removed; sha256 of the text above 09bd9d55 fcfa0501 f7a60b51 6849227f def0f749 a9a685e5 f8756ac4 82e6c874` |
| Signature (to be made) | `tessera-verifier-v1-1.parts.sig`: detached, binary, OpenPGP v4 type 0x00, ECDSA P-256, SHA-256, by `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` (YubiKey B) |
| Build | `python3 service/verifier/release/release_tool.py build --repo . --commit f2511c0d87f390396b50e687a7bef496544462da --out OUT` |

**Reproducibility.** Built twice on 2026-11-23: once from the `release-fixes` worktree with its own tool, once from an
independent `git clone --no-local` checked out at the source commit with the clone's copy of the tool. The two archives
are byte-identical (`cmp`), both SHA-256 `7fd00606…a61de614`. The archive depends only on tracked blob bytes at the
source commit and at the freeze commit; no time, user, path or file mode enters it. Git reads ignore replace refs
(review L1). The change list was produced the same two ways and is byte-identical.

## The approved baseline (A10.4.2 C01; review H1)

The author's approval does not rest on anything the NUC computes at release time:
- **Baseline.** Commit `b134cdf` is the verifier package as Codex reviewed it (352/352 conformance), with the freeze
  commit `52ee179` as its ancestor. Its OpenTimestamps proof (`timestamps/anchored/b134cdf….ots`) is anchored in
  Bitcoin block 973240, header time 2026-10-26T13:12:22Z, four weeks before any release file existed (2026-11-23).
  `release_tool.py baseline` checks that proof against the block header from two explorers over Tor, on the
  Pangolin. Whoever prepared this candidate could not have chosen the baseline's bytes.
- **The change.** `DIFF.txt` lists every file that enters the archive with its SHA-256 and prints in full each one
  added or changed since the baseline: `release_tool.py`, `sign-release.sh` (not in the archive; it runs in the
  signing session), `install.sh`, `README.md`, `requirements.lock`, `release/v1-1/trust.json` and
  `release/v1-1/release_constants.py`. The verifier code (`tessera_verify/`), the vendored SHA-1DC source, the
  relying-party text, the catalog and the release vectors are unchanged since the baseline. The author reads and signs
  the printed copy; on the Pangolin, `sha256sum` of the two scripts, and the change list's own last line as the tool
  he read recomputes it, must equal his paper. His reading is then of the real change, and the scripts that run are
  the ones he read.
- **The hashes he compares later** (the archive, the two scripts, the key file, the vectors) are computed on the
  Pangolin from that source. The sheet also prints them; a printed value that differs from the Pangolin's is a stop,
  so the paper can stop the sitting but cannot choose what is signed.

**What this does not establish.** The baseline is dated, not signed by the author: no commit in this repository is
signed by YubiKey A (all are signed by the NUC's commit key `2B9C…3835`, including the freeze commit; the 2026-11-13
key assertion is a parentless commit outside this history). A compromise of the NUC before 2026-10-26 could have shaped
the baseline; the defence there is the Codex review of `b134cdf` and the first production receipt's verification under
it (2026-11-16), not this procedure. The author does not review the verifier code itself; he approves the change from
a dated, reviewed baseline.

## What is in it

`RELEASE.json` (generated, R2) and 30 parts copied verbatim from the source commit:

- **Verifier code**: `service/verifier/tessera_verify/*.py` (12 files) except `release_constants.py`, whose
  unprovisioned source-tree copy is left out; `README.md`. `pyproject.toml` is no longer in the archive: the install
  has no build step.
- **This release's bindings**: `service/verifier/release/v1-1/trust.json` and `…/v1-1/release_constants.py`
  (`NAMESPACE = 'PRODUCTION'`, the trust and catalog hashes, the catalog bytes, `UNICODE_VERSION = '16.0.0'`; no
  machine facts). `install.sh` copies it into the package after the tree and R2 checks.
- **Catalog**: `formal/freeze-v1/objects/catalog.json`, the frozen bytes at their frozen path.
- **Installer and dependencies**: `install.sh` and `requirements.lock` (cffi 2.1.1, cryptography 50.0.2, pycparser
  3.12, with the SHA-256 of the five wheel files a Linux x86_64 glibc CPython 3.14 can use; installed with hashes
  required and source builds refused, R6). **Limit:** release 1 installs only on Linux x86_64 with glibc.
- **SHA-1DC**: `vendor/SHA1DC-PIN.md` and the vendored upstream source (9 files, including the SHAttered PDF used as
  the install-time known answer).
- **Relying-party text**: `docs/V1-RELYING-PARTY.md`.
- **Release tool**: `service/verifier/release/release_tool.py`, which `install.sh` uses for its tree and R2 checks.

Not in it: tests, the release vectors, the signing script, the issuer, anything under `prototype/`. Acquisition
refuses an archive that lacks any of R1's required part classes (review M3).

## Every hash and how it traces

| Object | SHA-256 | Traces to |
|---|---|---|
| Archive | `7fd00606b5591d9a3a410512776e3a0e82fa26628c17998749ca1a0da61de614` | Rebuilt by the author on the Pangolin at the source commit; equal, or stop. |
| Change list `DIFF.txt` (text above its last line) | `09bd9d55fcfa0501f7a60b516849227fdef0f749a9a685e5f8756ac482e6c874` | Recomputed by `release_tool.py diff` on the Pangolin; equal to the author's signed paper, or stop. |
| Freeze record (`formal/freeze-v1/FREEZE-RECORD.md` at `52ee179`) | `05542967b091424a614afd38a32cfb847b9b6b3f0e5a7b7103b11cd22d95575e` | `RELEASE.json` `freeze_record_sha256`. Commit `52ee179` (2026-10-24) is signed by the NUC commit key `2B9C…3835`, not by the author's YubiKey; its OpenTimestamps proof is anchored in block 972977; it is an ancestor of the baseline. |
| Catalog (`catalog.json`, 662 bytes) | `aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2` | The freeze record's table row; byte-equal to the file at `52ee179`; recomputed by `formal/freeze-v1/assemble.py --commit 270ca49`. Equals `release_constants.CATALOG_SHA256`; `CATALOG_BYTES` equals the part. |
| Spec object (named in the catalog) | `397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf` | The freeze record; recomputed by the assembler. Bound through the catalog's `spec_sha256`. |
| Vectors object (named in the catalog) | `19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f` | As above, `vectors_sha256`. |
| Preamble (named in the catalog) | `1eebd4a8c2ac405117ba5c4951f053c92459952194a760993dafea1c8959468f` | As above (review L2). |
| Dependency manifest (named in the catalog) | `20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063` | As above (review L2). |
| Trust file (`release/v1-1/trust.json`) | `9faa03683df7506cefa07afa4c0629182ebc5d4286b97801e1053cb8d86a7f89` | `trust_config_sha256` = `release_constants.TRUST_SHA256`. Not in the freeze record (trust is per release, profile §5). Byte-identical to `docs/smoke/2026-11-16-first-receipt/trust.json`. Printed in full in `DIFF.txt`. |
| `release_constants.py` (v1-1) | `f30e2e5988fc10a9b610e942b3a27952ed374d94b8e66350c9b470c87eef306a` | Generated by `release_tool.py constants` from the trust file and catalog; printed in full in `DIFF.txt`. |
| `release_tool.py` | `a4531c7d527953b26cfb6c7c72e404207f38152398e4fb944c7fd977b0e6539f` | Printed in full in `DIFF.txt`; the author reads it there. |
| `docs/ceremony/sign-release.sh` (not in the archive) | `4f7ac1b4d33d4147bb3c9f4eff1c1c6ddea76bd4d7045242c7ea1055bb014275` | As above. |
| `service/release-vectors/` (all files; rehearsal only) | `66d149cd999d0cccfca10c984715d3edbbddb6ad4ba2b789682d45b0c43eca93` | `find … \| sort \| xargs sha256sum \| sha256sum` on the Pangolin; unchanged since the baseline; checked again offline before `run.py` runs. |
| Release public key `docs/ceremony/keys/release-CADC…035E.pub.asc` | `1a817ae39f97450184d85e5c09bbdc0a301b18be65c8c3975144d3d8160cf6f3` | The key received on REL-PUB at the 2026-11-10 ceremony (`2026-11-10-operator-data.md`: `1a817ae39f974501…`); its fingerprint is on the author's paper and ORCID record. |

The other parts' hashes are in `RELEASE.json` `parts` and on `DIFF.txt`'s file list; `release_tool.py check`
compares each part with its blob at the source commit.

### The trust file's authority entries

| Entry | Value | Source; check at the sitting |
|---|---|---|
| Repository key | v4 fingerprint `6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A`, open from `2026-11-10T19:44:55Z` | YubiKey A, ceremony 2026-11-10. The author compares it with his paper record and with ORCID (both sheets). |
| KSK-2017 | tag 20326, DS `e06d44b8…c7f8ec8d`, signing ended 2026-10-11, reliance 21 days | IANA `root-anchors.xml`; `release_tool.py sources` compares over Tor. |
| KSK-2024 | tag 38696, DS `683d2d0a…c0fb2b16`, signing from 2026-10-11 | As above. |
| Header pins | 12: heights 975705–975710 and 976141–976146 | Fetched from blockstream.info and mempool.space, which agreed, on 2026-11-16; `sources` re-checked all 12 on 2026-11-23; the author repeats it over Tor. |

`version` `"1"`, `previous_sha256` 64 zeros, `as_of` `2026-11-16T15:48:11Z`. No previous release exists, so the
release checker's cross-release invariants have nothing to compare; acquisition requires release 1 to carry trust
version `"1"` with a zero `previous_sha256`.

**What these pins cover** (review L2). Pins are per header height. A bundle verifies only if every header it supplies
and every header it requires is pinned (else `UNVERIFIABLE / HEADERS_NOT_COVERED`, profile §5), and only if it meets
every other verification condition. The pinned ranges are the six-header segments at 975705 (the key assertion's OTS
anchor, 2026-11-13) and 976141 (the first production receipt's, 2026-11-16). Release 1 is known to cover the first
production receipt's bundle. A later receipt whose required headers all fall inside those ranges would also be
covered; in practice each later anchor is at a new height, which needs a later release (trust version 2 or more) made
by this procedure with a signing sitting.

## Checks run on the NUC, 2026-11-23 (candidate 2)

Transcripts: `evidence/candidate-2.txt`, `evidence/dry-rehearse-2.txt`.
- Two builds, byte-identical (above); `release_tool.py check` from the clone: `CHECK PASS`, 31 parts.
- `release_tool.py baseline` for `b134cdf`: `BASELINE PASS … block 973240, header time 2026-10-26T13:12:22Z`
  (direct HTTPS, not Tor).
- `release_tool.py sources` (run on candidate 1, same trust file): `SOURCES PASS: 2 KSKs and 12 pins equal their
  public sources` (direct HTTPS, not Tor).
- Acquisition of the candidate signed by a throwaway TEST key, production fingerprint `CADC…035E`: refused with
  `signed by <TEST>, not by the authenticated key CADC…035E`, exit 1, nothing unpacked, both with the production key
  file and with the TEST key file offered. With `--namespace TEST` and the TEST key, the `PRODUCTION`-labelled archive
  is refused (`namespace is PRODUCTION, not the expected TEST`). One changed byte: `gpgv refused (exit 1)`.
- A control, not a release and not an R4(a) TEST release: with the TEST fingerprint and key named as the authority,
  `acquire --out` verifies, unpacks into a new directory and runs that tree's `install.sh` (tree check, R2, hashed
  wheels, no build step). The installed verifier, default (production) mode, on the first production receipt:
  `VALID_STRICT / OK`, `T` `2026-11-16T14:35:57Z`, `A-UTC-7200-6`. It refuses the section 3.5 flags and the
  `TESSERA_V1_TEST_*` variables with `TEST_AUTHORITY_REFUSED`, exit 2, no verdict. The refusal comes before the
  files are read; this run offered placeholder files; candidate 1's run (`evidence/row36.txt`) offered an authentic
  TEST record.
- `install.sh` run by hand on an unpacked tree: refused (`installed only by release_tool.py acquire`). Started as
  `acquire` starts it, on a tree with one stray module: `the tree is not exactly the release: extra […stray.py]`; with
  one byte appended to `verify.py`: `part hash differs`; no `.venv` created in either case.
- `sign-release.sh rehearse` in a simulated session (paths and the network, route, swap, USB-disk, OUT-mount and tmpfs
  checks replaced; Ubuntu gpg 2.4.4): every step passed with the exact refusal strings, vectors 9/9, OUT written and
  read back.
- `service/verifier/tests/test_release_tool.py`: 22 pass. The whole verifier suite with the main checkout's venv: 156
  pass, 1 fails (the known worktree-only independence check, which loads the main checkout's editable install); with
  the worktree's own venv, installed by the new `install.sh`: 157 pass.

### A10 row 36: what is shown, what remains (review M1)

Registered (R4, A10 row 36): an otherwise correct archive signed only by a TEST key is refused by the production
acquisition procedure, including when the TEST public key is offered as the key; and an installed production verifier
refuses the section 3.5 interface.
1. **Acquisition leg.** Shown on the NUC (above) and, at the rehearsal, by `acquire` itself on Tails: two refusals
   with the exact string and nothing unpacked. Any other failure (an I/O error, a different refusal) fails the
   rehearsal.
2. **Installed-verifier leg.** `TEST_AUTHORITY_REFUSED`, exit 2, no verdict, by flags and by variables: NUC evidence
   only (`evidence/row36.txt`, `evidence/candidate-2.txt`). It needs Python 3.14 and cryptography, which an offline
   Tails lacks; the rehearsal sheet says so. The dead-service test (a clean Linux x86_64 machine) can repeat it.
3. Signature checks with the TEST fingerprint named are controls showing that the refusals are by key; they are not
   R4(a) TEST releases (that archive is labelled `PRODUCTION`).

Remains for the rehearsal: the same run on the Pangolin under Tails, offline, by the author, with Tails' GnuPG,
including its gpgv on the vectors; the networked phase (change list, baseline, build, check, sources over Tor); the
real stick, mount, eject and card paths, which no simulation here exercised; the measured time.

## The checker and gpgv (review M4)

- **The checker** is `release_tool.py`. For the author it is authenticated by his reading it in the printed change
  list and by `sha256sum`, on the Pangolin and again offline, equalling that list's line for it. For a relying party,
  R3 asks only that the checker be available before the archive runs: a copy fetched from GitHub is authenticated by
  nothing but the relying party's own reading or trust in GitHub. Nothing more is claimed.
- **gpgv.** R3 pins upstream GnuPG 2.4.4 and accepts a distribution build only if it reproduces upstream on the
  release-format vectors. The build qualified is the Tails binary whose SHA-256 the rehearsal prints and records in
  `record.txt` after it passed 9/9; the production sitting compares its binary's hash with that value. An ordinary
  acquisition uses whatever `gpgv` its `PATH` or `--gpgv` names; nothing here establishes that it is the pinned or a
  qualified build.
- The hashed issuer-fingerprint subpacket is no longer required (rule O allows its absence); when present it must name
  the authenticated key. The signer is established by `gpgv` with a keyring holding only that key.

## Publication (review H2)

`acquire` reads the archive and the signature once, writes that copy into a private temporary directory for `gpgv`,
and parses, checks and (with `--out`) unpacks only the bytes it read. It prints their SHA-256. At publication the owner
runs `acquire` (no `--out`) over the NUC's archive and the signature from OUT, and publishes the file whose SHA-256
equals the printed one; that equality, not the file name, is what binds the published bytes to the signature.

## What changed from the TEST release used in the smoke test (2026-11-16)

| | Smoke test (TEST) | Release 1 (candidate 2) |
|---|---|---|
| Form | No archive. A `tessera-v1-test-release/1` record through the §3.5 instrument interface, `--mode test`, from the source checkout | The §15.9 R1 archive, R2 manifest, R3 signature over the whole archive, code included |
| Signer | An in-memory P-256 key made by `rp_verify.py`, discarded | The production release key `CADC…035E`, YubiKey B, offline on Tails |
| Mode | TEST, provisioned in memory for one process | PRODUCTION, from the installed `release_constants.py`; every TEST flag or variable is refused |
| Trust file | `trust.json`, SHA-256 `9faa0368…d86a7f89` | The same bytes |
| Catalog | The frozen catalog (`aaf4306f…`), carried inside the TEST record | The same bytes, as a part and compiled into `release_constants.py` |
| Verifier code | `tessera_verify/` as of `b134cdf` (2026-10-26) | Unchanged: no commit has touched `tessera_verify/` since `b134cdf` (`DIFF.txt`: `unchanged`) |
| Installer, dependencies | `install.sh` editable install, `requirements.txt` without hashes | `install.sh`: release trees only from `acquire`, exact-tree and R2 checks, the constants installed, no build step; wheels from `requirements.lock`, hashes required |
| New | — | `release_tool.py`, `release/v1-1/`, `requirements.lock`, a README section |

## Owner choices made here (no registered text decides them)

- The release's own files live under `service/verifier/release/v1-<n>/`, and `install.sh` installs that
  `release_constants.py`. The source tree's `tessera_verify/release_constants.py` stays unprovisioned, so the source
  tree's tests and TEST harness keep working. Every part is still a verbatim blob at the source commit (R1).
- "The freeze record" in `freeze_record_sha256` is `formal/freeze-v1/FREEZE-RECORD.md` at the freeze commit `52ee179`
  (the JSON form is labelled draft).
- The trust file is the smoke test's, unchanged: its entries were already checked against their sources, and it
  covers the first production receipt.
- The baseline is `b134cdf`, not the freeze commit: the verifier code did not exist at `52ee179`, so a change list
  from the freeze would print all of it (about 7000 lines). `b134cdf` is the reviewed package, dated by OpenTimestamps.
- The lock covers Linux x86_64 glibc only, so the author's change list carries 21 lines of it instead of 170, and no
  sdist (which would need an unhashed build backend) can be chosen.
