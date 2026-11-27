# Verifier release 1: release summary (candidate 5, unsigned)

Owner instance (Claude Opus 5.5), 2026-11-23; candidate 4, 2026-11-24; candidate 5 (pin refresh), 2026-11-26. This is the release summary of custody draft §9 ("Preparation on the
NUC"). It is an aid, not evidence of approval: the author's reading, on the Pangolin's screen, of the change list the
Pangolin itself makes (`DIFF.txt` here is the NUC's copy, a reading aid only) and his own build and checks there
(`docs/ceremony/release-v1-1-SHEET.md`) are the approval. Procedure: `docs/V1-RELEASE-PROCEDURE.md`. Candidate 1
(`49e65de3…`, source `7b986e8`) is withdrawn after the Codex review (`docs/reviews/release-v1-1/CODEX-REVIEW.md`;
dispositions in `DISPOSITION.md` there). Candidate 2 (`7fd00606…`, source `f2511c0`) is withdrawn after the scoped
confirmation (`CODEX-CONFIRM.md`): only `sign-release.sh` changed (final pass, `DISPOSITION.md`), so candidate 3's
parts are byte-identical to candidate 2's and only `RELEASE.json`'s `source_commit` differs. Candidate 3 (`f50e5388…`,
source `554a1fb`) is superseded by candidate 4 before any sitting: its trust file pinned only the first production
receipt's anchor, so every later receipt was `UNVERIFIABLE / HEADERS_NOT_COVERED` under it. Candidate 4 adds the pins
of eight later production anchors (48 pins) with a new `release_tool.py pins` subcommand; three parts differ from
candidate 3 (`release_tool.py`, `trust.json`, `release_constants.py`), and the release is still release 1, trust
version `"1"`, zero `previous_sha256`. Candidate 5 is candidate 4 refreshed by `REFRESH.md` on 2026-11-26: the pins of
two later production anchors (977379, 977531; 12 pins). Three parts differ from candidate 4: `trust.json`,
`release_constants.py`, and `release_tool.py`, which carries the pins fixes of `1f9d914` (Codex-reviewed before the
fix, not after; merged on 2026-11-24 without a rebuild). *(Corrected 2026-11-27: the first text of this paragraph said
only the first two differ; the author found the tool's hash unequal to the sheet's at the rehearsal.)* The receipt anchored at 977690 (2026-11-26) was too recent to pin (tip 977695, below h+10) and is left out.

## The candidate

| | |
|---|---|
| Archive | `tessera-verifier-v1-1.parts` (profile §15.9 R1; 720698 bytes, 31 parts) |
| Archive SHA-256 | `1342b5b9 815eba01 c07ba464 702a2444 56515d5c 2afa38a0 f1814e88 088dc272` |
| Namespace, release | `PRODUCTION`, `1`; `release_key_successor` null |
| Source commit | `b22e08f298da6aef8d750322d2ee006eb9738f33` (branch `release-pins`; must be on GitHub before the sitting) |
| Baseline commit | `b134cdfdacc5d89f2748fa7ec15c46e38b51a32c` (the Codex-reviewed verifier, 2026-10-26; OpenTimestamps block 973240) |
| Change list | `DIFF.txt`, last line `DIFF 7 added or changed, 0 removed; sha256 of the text above 74e65031 abd7ff75 6a574a6b 4c417f4d 41a6f65a bf9ed9e8 e95126e3 a90e33fa`; whole file SHA-256 `c7bbb193 842decff 8854e483 f91ac60e d17563be 5a700cd2 6736194e 15ab3ff1` |
| Signature (to be made) | `tessera-verifier-v1-1.parts.sig`: detached, binary, OpenPGP v4 type 0x00, ECDSA P-256, SHA-256, by `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` (YubiKey B) |
| Build | `python3 service/verifier/release/release_tool.py build --repo . --commit b22e08f298da6aef8d750322d2ee006eb9738f33 --out OUT` |

**Reproducibility.** Candidate 5 was built twice on 2026-11-26: once from the `release-pins` worktree with its own tool,
once from an independent `git clone --no-local` checked out at the source commit with the clone's copy of the tool. The
two archives are byte-identical (`cmp`), both SHA-256 `1342b5b9…088dc272` (candidates 3 and 4 were built the same way on
2026-11-23 and 2026-11-24). The archive depends only on tracked blob bytes at the
source commit and at the freeze commit; no time, user, path or file mode enters it. Git reads ignore replace refs
(review L1). The change list was produced the same two ways and is byte-identical.

## The baseline and the change (A10.4.2 C01; review H1)

- **Baseline.** Commit `b134cdf` is the verifier package as Codex reviewed it (352/352 conformance), with the freeze
  commit `52ee179` as its ancestor. Its OpenTimestamps proof (`timestamps/anchored/b134cdf….ots`) is anchored in
  Bitcoin block 973240, header time 2026-10-26T13:12:22Z, four weeks before any release file existed (2026-11-23).
  `release_tool.py baseline` checks that proof against the block header from two explorers over Tor, on the
  Pangolin. What this shows: the anchored commit's bytes cannot have been rewritten after 2026-10-26, provided the
  explorers serve genuine chain data and Git's object hashes hold. What it does not show: that the author approved
  that baseline (question 5 of the procedure is open), or which commit should be the baseline. A preparer could
  propose a different tree that already existed; the author's check is that the sheet names `b134cdf` and the tool
  proves that commit's date. A NUC compromised before the anchor could have shaped the baseline; that case is outside
  what this procedure addresses.
- **The change.** `release_tool.py diff` lists every file that enters the archive with its SHA-256 and prints in full
  each one added or changed since the baseline: `release_tool.py`, `sign-release.sh` (not in the archive; it runs in
  the signing session), `install.sh`, `README.md`, `requirements.lock`, `release/v1-1/trust.json` and
  `release/v1-1/release_constants.py`. The verifier code (`tessera_verify/`), the vendored SHA-1DC source, the
  relying-party text, the catalog and the release vectors are unchanged since the baseline. At the rehearsal the
  Pangolin makes the change list itself; the author reads that output on its screen (`less`), reads the two scripts
  from the files themselves (the tool writes the list, including its own text), checks that the scripts'
  `sha256sum` equal their lines in the list, and writes the SHA-256 of the whole list file on his rehearsal sheet. A
  NUC printout is at most a reading aid and is not approved. At the production sitting the Pangolin makes the list
  again and its whole-file SHA-256 must equal the value on his rehearsal sheet, or the sitting stops.
- **The hashes he compares later** (the archive, the two scripts, the key file, the vectors) are computed on the
  Pangolin from that source. The sheet also prints them; a printed value that differs from the Pangolin's is a stop,
  so the paper can stop the sitting but cannot choose what is signed.

**What this does not establish.** The baseline is dated, not signed or approved by the author: no commit in this
repository is signed by YubiKey A (all are signed by the NUC's commit key `2B9C…3835`, including the freeze commit;
the 2026-11-13 key assertion is a parentless commit outside this history). The defence for the baseline's contents is
the Codex review of `b134cdf` and the first production receipt's verification under it (2026-11-16), not this
procedure. The author does not review the verifier code itself; he approves the change from a dated, reviewed
baseline, if he accepts that baseline (procedure, question 5).

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
| Archive | `1342b5b9815eba01c07ba464702a244456515d5c2afa38a0f1814e88088dc272` | Rebuilt by the author on the Pangolin at the source commit; equal, or stop. |
| Change list `DIFF.txt` (text above its last line) | `74e65031abd7ff756a574a6b4c417f4d41a6f65abf9ed9e8e95126e3a90e33fa` | Printed by `release_tool.py diff` as the list's last line. |
| Change list `DIFF.txt` (whole file) | `c7bbb193842decff8854e483f91ac60ed17563be5a700cd26736194e15ab3ff1` | `sha256sum` of the list the Pangolin makes; written by the author at the rehearsal after reading that list on screen; at production, equal to that written value, or stop. |
| Freeze record (`formal/freeze-v1/FREEZE-RECORD.md` at `52ee179`) | `05542967b091424a614afd38a32cfb847b9b6b3f0e5a7b7103b11cd22d95575e` | `RELEASE.json` `freeze_record_sha256`. Commit `52ee179` (2026-10-24) is signed by the NUC commit key `2B9C…3835`, not by the author's YubiKey; its OpenTimestamps proof is anchored in block 972977; it is an ancestor of the baseline. |
| Catalog (`catalog.json`, 662 bytes) | `aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2` | The freeze record's table row; byte-equal to the file at `52ee179`; recomputed by `formal/freeze-v1/assemble.py --commit 270ca49`. Equals `release_constants.CATALOG_SHA256`; `CATALOG_BYTES` equals the part. |
| Spec object (named in the catalog) | `397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf` | The freeze record; recomputed by the assembler. Bound through the catalog's `spec_sha256`. |
| Vectors object (named in the catalog) | `19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f` | As above, `vectors_sha256`. |
| Preamble (named in the catalog) | `1eebd4a8c2ac405117ba5c4951f053c92459952194a760993dafea1c8959468f` | As above (review L2). |
| Dependency manifest (named in the catalog) | `20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063` | As above (review L2). |
| Trust file (`release/v1-1/trust.json`) | `3ef97f19527d76168dab10d85f396a6d5c8a602cb63047a5610986460e69a176` | `trust_config_sha256` = `release_constants.TRUST_SHA256`. Not in the freeze record (trust is per release, profile §5). The smoke test's trust file (`docs/smoke/2026-11-16-first-receipt/trust.json`, `9faa0368…`) plus 60 pins and a later `as_of`; every other byte of its content unchanged. Printed in full in `DIFF.txt`. |
| `release_constants.py` (v1-1) | `5807a8e7d634c1e9cd0c6d70c55761a48fe28aaa712da857df7e88cc91d7afa8` | Regenerated by `release_tool.py pins` (the same generator as `constants`) from the trust file and catalog; printed in full in `DIFF.txt`. |
| `release_tool.py` | `5225491c3a8ff58cd63be3a00b44c51ad617667f8a20e4120b75966c01e7c458` | Printed in full in `DIFF.txt`; the author reads it there. Candidate 4's tool was `2d2694fb…ba103880`; `1f9d914` changed it after candidate 4 was built. |
| `docs/ceremony/sign-release.sh` (not in the archive) | `20d5e19c1ff46f0af25b3dc9308290e3014a3084c0c887a031b450e38a2df15a` | As above. |
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
| Header pins | 72: the six-header runs h…h+5 at h = 975705, 976141, 976209, 976283, 976445, 976596, 976735, 976918, 977072, 977216, 977379, 977531 | The first 12 fetched from blockstream.info and mempool.space, which agreed, on 2026-11-16. The other 48 by `release_tool.py pins` on 2026-11-24 (both explorers byte-equal on every raw header, each hashing to its id and linking to the one before, h+5 with at least 6 confirmations: tip 977299). The last 12 by `pins` on 2026-11-26 (same checks; tip 977695). `sources` re-checked all 72 on 2026-11-26; the author repeats it over Tor. |

`version` `"1"`, `previous_sha256` 64 zeros, `as_of` `2026-11-25T16:20:25Z` (see below). No previous release exists, so the
release checker's cross-release invariants have nothing to compare; acquisition requires release 1 to carry trust
version `"1"` with a zero `previous_sha256`.

**What these pins cover** (review L2). Pins are per header height. A bundle verifies only if every header it supplies
and every header it requires is pinned (else `UNVERIFIABLE / HEADERS_NOT_COVERED`, profile §5 "Header pins", §7.2),
and only if it meets every other verification condition. The required headers are h*…h*+5 of the selected attestation
of each of the three proofs (receipt, snapshot, git; §7.2 "Coverage"). The pinned runs are at 975705 (the key
assertion's OTS anchor, 2026-11-13), 976141 (the first production receipt's receipt and snapshot anchor, 2026-11-16)
and the later production anchor heights the steward read from the issuer's records on 2026-11-24 (976209,
976283, 976445, 976596, 976735, 976918, 977072, 977216) and 2026-11-26 (977379, 977531). **Release 1 covers the headers of every receipt anchored at or
below 977531 whose three proofs anchor at pinned heights; a receipt anchored above 977531, or one whose snapshot proof
anchored at a height not in this list, needs a later release** (a refresh before the sitting, `REFRESH.md`, or trust
version 2 or more made by this procedure with a signing sitting). Known to verify: the 11 production receipts anchored at or below 977531
(`VALID_STRICT` under the candidate 5 trust file, 2026-11-26, TEST-mode check, `evidence/candidate-5-all-receipts.md`).
The receipt anchored at 977690 gives `UNVERIFIABLE / HEADERS_NOT_COVERED` under it, as expected; receipts are fetched only by the steward.

**`as_of`.** The profile fixes no value; it constrains it. §5 "Open endpoints" (`docs/V1-PROFILE.md` lines 597-599):
an open KSK's reliance and an open repository key's use run to `as_of`, and evidence later than `as_of` under an open
entry gives `UNVERIFIABLE / TRUST_HORIZON`; §5 release invariants (line 603) and §15.5 (line 1705): `as_of` is
nondecreasing; §15.5 (line 1694): an open entry's `signing_start` ≤ `as_of`. The evidence times compared with it are
T_snap (line 507) and T_git (line 762), each nTime(h*) of a proof's anchor (§7.1). Owner choice: `as_of` is the latest
header time among the pinned headers, `2026-11-25T16:20:25Z` (block 977536, the newest pinned height; both explorers),
never earlier than the previous `as_of` and never later than the preparing machine's clock. It is at or after the
T_snap and T_git of every proof anchored at a pinned height, so no covered receipt meets `TRUST_HORIZON`, and it
asserts only that KSK-2024 and the repository key were still signing at a time already past. The 2026-11-16 value
(`2026-11-16T15:48:11Z`) was the smoke-test machine's clock (`rp_verify.py`), not a header time.

## Checks run on the NUC, 2026-11-26 (candidate 5)

Transcripts: `evidence/candidate-5.txt`, `evidence/candidate-5-all-receipts.md`.
- Step 1: 12 COMPLETE requests; three receipts newer than candidate 4 (anchors 977379, 977531, 977690), every
  candidate 4 pin still present in the receipts. 977690 left out (tip 977695 < h+10).
- `release_tool.py pins --heights 977379,977531`: `PINS ADDED 12`, 72 pins, `as_of 2026-11-25T16:20:25Z` (direct HTTPS).
- Verifier tests: `1 failed, 170 passed` (the worktree-only independence test; 170 since the pins tests of `1f9d914`).
- Two builds, byte-identical; `check` from the clone: `CHECK PASS`, 31 parts, 72 pins.
- `diff` from both checkouts, byte-identical: `… 74e65031 … a90e33fa`, whole file `c7bbb193…15ab3ff1` (1384 lines).
- `sources`: `SOURCES PASS: 2 KSKs and 72 pins equal their public sources.` (75 lines, direct HTTPS).
- All 12 COMPLETE receipts under the candidate 5 trust file (TEST wrapper): 11 `VALID_STRICT / OK`, 977690's receipt
  `UNVERIFIABLE / HEADERS_NOT_COVERED`, as predicted before the run.

## Checks run on the NUC, 2026-11-24 (candidate 4)

Transcript: `evidence/candidate-4.txt`.
- `release_tool.py pins --heights 976209,976283,976445,976596,976735,976918,977072,977216`: `PINS ADDED 48`, 60 pins,
  `as_of 2026-11-23T14:44:14Z` (direct HTTPS, not Tor; both explorers' tip 977299, so every h+5 had at least 79
  confirmations). The previous 12 pins and every other entry are unchanged; the verifier's own append-only checker
  (`policy.check_extension`, with the version bump a later release would make simulated) and its trust-file parser
  accept the new file against the old.
- Two builds, byte-identical (above); `release_tool.py check` from the clone: `CHECK PASS`, 31 parts, 60 pins.
- `release_tool.py diff` from both checkouts, byte-identical: `DIFF 7 added or changed, 0 removed; … ea02b7b8 …
  23b91e2f`, whole file `f5e88951…1226e95f` (1325 lines).
- `release_tool.py sources` on the archive: `SOURCES PASS: 2 KSKs and 60 pins equal their public sources.` (63 lines,
  direct HTTPS).
- The first production receipt under the candidate 4 trust file (TEST release record made in memory, as in the
  2026-11-16 smoke test, source-tree verifier): `VALID_STRICT / OK`, `T` `2026-11-16T14:35:57Z`. Not repeated: the
  install from an acquired candidate 4 tree, the acquisition refusals and the simulated signing rehearsal; the
  verifier code, `install.sh` and `sign-release.sh` are unchanged from candidate 3, and the refusals do not depend on
  the trust file.
- `service/verifier/tests/test_release_tool.py`: 32 pass (22 before, plus 10 for `pins` on recorded explorer answers,
  `tests/fixtures_pins/`). The whole verifier suite with the main checkout's venv: 166 pass, 1 fails (the known
  worktree-only independence check).

## Checks run on the NUC, 2026-11-23 (candidates 2 and 3)

Transcripts: `evidence/candidate-2.txt`, `evidence/dry-rehearse-2.txt` (candidate 2); `evidence/candidate-3.txt`,
`evidence/dry-rehearse-3.txt` (candidate 3: the acquisition refusals, the changed byte, and the signing script's
simulated rehearsal, rerun because the script changed). The install and installed-verifier runs below were made on
candidate 2, whose parts are byte-identical to candidate 3's (only `RELEASE.json`'s `source_commit` differs); they were
not repeated.
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
  checks replaced; Ubuntu gpg 2.4.4), candidate 3: every step passed, each refusal's whole error output equal to the
  full expected line, vectors 9/9, OUT written, read back, listed and hashed. The signing mode's expected changed-byte
  line (with the release key's user ID) is not exercised without YubiKey B.
- `service/verifier/tests/test_release_tool.py`: 22 pass. The whole verifier suite with the main checkout's venv: 156
  pass, 1 fails (the known worktree-only independence check, which loads the main checkout's editable install); with
  the worktree's own venv, installed by the new `install.sh`: 157 pass.

### A10 row 36: what is shown, what remains (review M1)

Registered (R4, A10 row 36): an otherwise correct archive signed only by a TEST key is refused by the production
acquisition procedure, including when the TEST public key is offered as the key; and an installed production verifier
refuses the section 3.5 interface.
1. **Acquisition leg.** Shown on the NUC (above) and, at the rehearsal, by `acquire` itself on Tails: two refusals
   whose whole error output equals the full expected line (not a prefix), and nothing unpacked. Any other failure (an I/O error, a different refusal) fails the
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

- **The checker** is `release_tool.py`. For the author it is authenticated by his reading the file itself on the
  Pangolin and by `sha256sum`, there and again offline, equalling the sheet's value and its line in the change list
  he approved. For a relying party,
  R3 asks only that the checker be available before the archive runs: a copy fetched from GitHub is authenticated by
  nothing but the relying party's own reading or trust in GitHub. Nothing more is claimed.
- **gpgv.** R3 pins upstream GnuPG 2.4.4 and accepts a distribution build only if it reproduces upstream on the
  release-format vectors. The build qualified is the Tails binary whose SHA-256 the rehearsal prints and records in
  `record.txt` after it passed 9/9; the production sitting compares its binary's hash with that value. An ordinary
  acquisition uses whatever `gpgv` its `PATH` or `--gpgv` names; nothing here establishes that it is the pinned or a
  qualified build.
- **Ordinary acquisition** (any run of `acquire` outside the ceremony, the owner's publication step included) relies
  on a checker and a `gpgv` that its caller selected and trusts. Its result is no stronger than those two programs
  and the local machine; nothing in this release establishes more.
- The hashed issuer-fingerprint subpacket is no longer required (rule O allows its absence); when present it must name
  the authenticated key. The signer is established by `gpgv` with a keyring holding only that key.

## Publication (review H2)

`acquire` reads the archive and the signature once, writes that copy into a private temporary directory for `gpgv`,
and parses, checks and (with `--out`) unpacks only the bytes it read. It prints their SHA-256. At publication the owner
runs `acquire` (no `--out`) over the NUC's archive and the signature from OUT, and publishes the file whose SHA-256
equals the printed one; that equality, not the file name, is what binds the published bytes to the signature.

## What changed from the TEST release used in the smoke test (2026-11-16)

| | Smoke test (TEST) | Release 1 (candidate 5) |
|---|---|---|
| Form | No archive. A `tessera-v1-test-release/1` record through the §3.5 instrument interface, `--mode test`, from the source checkout | The §15.9 R1 archive, R2 manifest, R3 signature over the whole archive, code included |
| Signer | An in-memory P-256 key made by `rp_verify.py`, discarded | The production release key `CADC…035E`, YubiKey B, offline on Tails |
| Mode | TEST, provisioned in memory for one process | PRODUCTION, from the installed `release_constants.py`; every TEST flag or variable is refused |
| Trust file | `trust.json`, SHA-256 `9faa0368…d86a7f89` | The same entries plus 60 pins and a later `as_of` (`3ef97f19…0e69a176`) |
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
- The trust file is the smoke test's with pins added: its entries were already checked against their sources. Candidate
  4 adds the six-header runs of the production anchor heights the steward listed on 2026-11-24, so that receipts
  issued since 2026-11-16 are covered without a second signing sitting.
- `release_tool.py pins` refuses unless h+5 has 6 confirmations (`PIN_DEPTH`, tip ≥ h+10). The profile's k = 6 needs
  only that h+5 exists; pins are immutable (§5), so a pin taken at the tip and then reorganized away could never be
  corrected and would make every bundle carrying the real header `INVALID / HEADER_CONFLICTS_PIN`.
- `as_of` is the latest pinned header time (above). The profile constrains it but does not fix it.
- The `pins` subcommand is in `release_tool.py`, so it is in the archive and in the author's reading (83 lines).
  Nothing it does is trusted at the sitting: `sources` re-checks every pin against both explorers over Tor.
- The baseline is `b134cdf`, not the freeze commit: the verifier code did not exist at `52ee179`, so a change list
  from the freeze would print all of it (about 7000 lines). `b134cdf` is the reviewed package, dated by OpenTimestamps.
- The lock covers Linux x86_64 glibc only, so the author's change list carries 21 lines of it instead of 170, and no
  sdist (which would need an unhashed build backend) can be chosen.
