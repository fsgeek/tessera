# Release v1-1 review: dispositions

Owner instance (Claude Opus 5.5), 2026-11-23, on `CODEX-REVIEW.md` with the steward's dispositions (smallest change;
prefer removing a capability over guarding it; each sheet one linear printable sheet). Source commit of the new
candidate: `f2511c0d87f390396b50e687a7bef496544462da`; archive `7fd00606b5591d9a3a410512776e3a0e82fa26628c17998749ca1a0da61de614`
(built twice, byte-identical); change list `docs/releases/v1-1/DIFF.txt`. Candidate 1 (`49e65de3…`) is withdrawn.

## HIGH

**H1. Candidate preparation can determine what the author signs.** MECHANISM, with a premise correction.
- The steward's disposition rooted the baseline in "the freeze commit he signed with YubiKey A (52ee179)". That is not
  the record: `52ee179` (2026-10-24) is signed by `2B9C F308 … 42C7 3835`, the passphraseless NUC commit key named in
  `docs/phase-0-prereg.md` §4.2, as is every commit in this repository. YubiKey A (`6BDA…D30A`, made 2026-11-10) has
  signed only the parentless key-assertion commit `aad530ed…`, which commits to no source. A signature check against
  the root key therefore cannot be written for this baseline.
- Done instead: the baseline is rooted in **time**. Commit `b134cdf` (the Codex-reviewed verifier package, a
  descendant of `52ee179`) has an OpenTimestamps proof anchored in Bitcoin block 973240 (header time
  2026-10-26T13:12:22Z). New `release_tool.py baseline` checks that proof (the profile §15.2 operations) against the
  block header from blockstream.info and mempool.space over Tor, and that `52ee179` is an ancestor. A candidate
  preparer of November cannot change those bytes. `52ee179` cannot serve as the baseline itself: the verifier code did
  not exist there, so its change list would print about 7000 lines.
- New `release_tool.py diff` writes the one printed change list: every file that enters the archive with its SHA-256,
  and in full each one added or changed since the baseline (`release_tool.py`, `install.sh`, `README.md`, the lock,
  `trust.json`, `release_constants.py`), plus `sign-release.sh` and the vectors, which run in the signing session.
  The last line is the SHA-256 of the text above it. The author reads and signs the paper before the sitting. On the
  Pangolin: `sha256sum` of the two scripts equals their lines on his paper (the tools he read are the ones that run),
  `diff` reproduces the last line (his paper is the real change), `baseline` passes, then he builds the archive. Every
  hash he later compares offline is the one the Pangolin computed or confirmed. The sheet still prints them; a
  difference is a stop, so the NUC's paper can only stop the sitting.
- Removed from the archive because not needed: `pyproject.toml` (no build step, M7). Trimmed: the lock, to the five
  wheels a Linux x86_64 glibc CPython 3.14 uses (21 lines in the change list instead of 170); release 1 therefore
  installs only on that platform, stated in SUMMARY.
- Not established, and stated in SUMMARY, the procedure and its question 5 for the author: that the author approved
  the baseline. It is dated and reviewed, not author-signed; a NUC compromise before 2026-10-26 is outside what this
  catches. **Needs the author/steward:** accept a dated baseline for C01, or have the author approve `b134cdf`
  explicitly before the production sitting.
- The change list is about 1200 lines (the release tool is most of it), so reading it is a separate session before
  the sitting (estimated 2 hours, once); the sittings stay within about 90 minutes each.

**H2. Acquisition can unpack bytes other than those authenticated.** MECHANISM. `acquire` now reads the archive and
the signature once, writes that copy into a private temporary directory for `gpgv`, and parses, checks and unpacks
only the bytes it read; it prints their SHA-256 (`verify_bytes`). The procedure's publication step publishes the file
whose SHA-256 equals that printed value and checks the uploaded copies; the old claim ("shows the published archive is
the byte string the author signed") is restated accordingly in the procedure and SUMMARY.

## MEDIUM

**M1. The rehearsal could pass without the registered refusal paths.** MECHANISM. The rehearsal's row 36 step now runs
`acquire --out` (not `verify-sig`) with the production fingerprint, offering first the production key file and then
the TEST key file. Each must exit 1 with exactly `REFUSED: signed by <TEST>, not by the authenticated key CADC…035E`
and must leave no output directory; any other failure (an I/O error, another refusal) fails the run. The changed-byte
check must exit 1 with `REFUSED: gpgv refused (exit 1)`. The installed-verifier leg (`TEST_AUTHORITY_REFUSED`, exit 2,
no verdict) cannot run on Tails (no Python 3.14); the script and the sheet say so, and SUMMARY records it as NUC-only
evidence (`evidence/row36.txt`, `evidence/candidate-2.txt`). The TEST-key `verify-sig` pass is described as a control,
not an R4(a) TEST release.

**M2. Install checked a manifest-selected subset and trusted the tree.** MECHANISM. `bindings` now walks the whole
unpacked tree, refuses links and non-regular files, and requires the file set to be exactly `RELEASE.json` plus the
manifest's parts, before R2. `install.sh` runs that check before it creates anything (so a previously installed tree,
with its `.venv`, is refused), and installs an unpacked release only when started by `acquire --out` on the tree it
just authenticated and unpacked (`TESSERA_ACQUIRED_ROOT` equal to the tree). That variable stops a stale or copied
tree from being installed by mistake; it is not a security boundary against someone who sets it by hand (who could
as well edit `install.sh`). Installer-generated files (`.venv`, `build/`, `install.json`, the copied constants) all
appear after the check.

**M3. No expected namespace; partial envelope check.** MECHANISM. `acquire` takes `--namespace` (default
`PRODUCTION`; `TEST` only when named) and refuses any other label. `check_bindings` requires every R1 part class
(the lock, the SHA-1DC pin and the source files `install.sh` checks, `install.sh`, the relying-party text, the release
tool, the verifier's entry modules, trust, constants, catalog), every manifest value except `parts` and the successor
to be a string, `trust_config_version` a canonical decimal string, the trust file's `format` and `profile`, and, for
release 1, trust version `"1"` with a zero `previous_sha256`. Authenticated key selection stays the prerequisite: a
caller who supplies a TEST fingerprint as if it were the production one has substituted the bootstrap authority, and
no label check can detect that (a test says so).

**M4. R3 did not establish the checker and gpgv identity claimed.** WORDING plus MECHANISM. The checker is
authenticated for the author by his reading it in the change list and by `sha256sum` equalling that list's line, on
the Pangolin and offline; for a relying party, by nothing but his own reading or trust in GitHub (SUMMARY says so).
The script prints and records the SHA-256 of the `gpgv` binary that passed the vectors on Tails; the production sheet
compares it with the rehearsal's. SUMMARY claims no more than that. The hashed issuer-fingerprint subpacket is now
optional, as rule O allows; when present it must name the authenticated key, and the signer is established by `gpgv`
with the sole authenticated key.

**M5. Media checks the custody procedure relies on.** MECHANISM and WORDING. Each stick is identified by its USB serial
(`lsblk`) before it is formatted and again in the offline session (the script prints both sticks' serials and asks).
OUT must be never-NUC on entry in both sheets, and new for production. The internal-disk mount check is on both
sheets (`lsblk … MOUNTPOINTS`) and in the script (every mounted device must sit on a USB disk). Nothing on INPUT runs
offline unless its SHA-256 was approved in the networked boot: `sign-release.sh` (hashed by hand before it runs),
`release_tool.py` (hashed by the script and compared), and in the rehearsal the vectors directory (one digest over
every file, computed in Part 1, compared before `run.py` runs). The procedure records the transferred scripts as a
proposal against the draft's transfer rule 3. Backups: the procedure's gate list now requires the custody record to
say where YubiKey B and each backup are kept and how each stays outside the operational environment; the production
sheet no longer implies that putting the card back supplies that record.

**M6. Ambiguous stop conditions and an output-count error.** MECHANISM and WORDING. `sources` is "exactly 15 lines" (14
plus PASS); `check` "exactly 12 lines"; `assemble.py` its five full lines; every freeze and archive value in full. Each
sheet has one stop rule at the top, and the ORCID and paper comparisons say "No is a stop" where they are recorded.
The production sheet gives the exact card lines and says Ctrl-C and remove YubiKey B for any other card line; the
script also refuses a card whose serial is not 39975596 or whose key is not `CADC…035E`. OUT is written only after
every check, each file is read back and compared, an extra file fails, and any failed write, `sync` or readback ends in
`OUT IS QUARANTINED`; PASS prints only after the readback. The rehearsal's Tor allowance is now one retry, then the
error is written down as an incomplete source check; the production sheet stops on a second failure. ORCID is in the
procedure's online route list. Not done here: the real Tails clone, Tor fetches, mount and eject, card discovery and
PIN paths remain unverified until the rehearsal; the dry run (`evidence/dry-rehearse-2.txt`) replaced paths and
session checks and used Ubuntu GnuPG.

**M7. Unhashed build dependency.** MECHANISM (removal). The editable `pip install -e` is gone, and with it setuptools:
`install.sh` puts the tree on the venv's path with a `.pth` file and writes a `tessera-verify` launcher. Wheels install
with `--require-hashes` and `--no-build` (uv) or `--only-binary=:all:` (pip), so no sdist and no build backend can
be fetched. `pyproject.toml` leaves the archive. Checked: `acquire --out` installed the candidate from the trimmed
lock on the NUC (5 wheels), and the installed verifier gave `VALID_STRICT` on the first production receipt.

## LOW

**L1. Replacement refs.** Fixed (one line): every git read uses `--no-replace-objects`.

**L2. Freeze trace and pin scope.** Fixed in SUMMARY: the preamble and dependency-manifest rows are added (both
recomputed by the assembler; both sheets now show all five assembler lines); pin coverage is stated per supplied and
required header height, not by issue order; both sheets compare the repository root as well as the release key on
ORCID, as SUMMARY says. The OpenTimestamps proof of the freeze commit is now checked (the baseline's, whose ancestor
it is); the public-key blob hash still traces only to the ceremony record.

## Owner prechecks

- **Trigger clause (FAIL).** The rehearsal no longer claims row 36 from two signature checks; it runs acquisition and
  names the installed-verifier leg as NUC evidence.
- **Requester (FAIL).** See H1: the NUC's paper can now only stop the sitting; what is signed is decided by the
  author's reading of the change list and his own Pangolin build, from a baseline the NUC could not change after
  2026-10-26.
- **Binding text (FAIL).** Custody draft §9 is relabelled as not registered; the checker's extra issuer-fingerprint
  requirement is removed (M4); the proposal that a later release could be compared on the NUC alone is withdrawn.
  New, and labelled: the dated (not author-signed) baseline is an owner decision with an open question to the author.

## Tests

`service/verifier/tests/test_release_tool.py`: 22 pass (7 new: required parts and string types, exact install tree,
`install.sh` by hand, the change list's determinism and self-hash, the baseline proof's anchor height, the expected
namespace, a signature without the issuer fingerprint). Whole verifier suite, main checkout's venv: 156 pass, 1 fails
(the known worktree-only independence check: it loads the main checkout's editable install). With the worktree's
own venv, installed by the new `install.sh`: 157 pass.
