# Verifier release 1: refreshing the header pins before the sitting

For the owner on the NUC (planned: Wednesday evening, 2026-11-25), when the steward has read new production anchor
heights from the issuer's records. Release 1 is unsigned, so the pins are added to the same trust file: it stays trust
version `"1"` with a zero `previous_sha256`. Each refresh makes a new candidate; the rehearsal and production sheets
must carry the new values before either sitting, and the author reads the new change list on screen at the rehearsal.

Run every command from the worktree root, `/home/tony/projects/tessera/.worktrees/release-pins` (branch
`release-pins`), with the tree clean. Replace `H1,H2` with the new anchor heights, comma-separated, no spaces. List
the receipt's anchor height **and, if different, its snapshot proof's anchor height** for every new receipt: the
verifier requires h*…h*+5 of all three proofs (profile §7.2 "Coverage"). Heights already pinned may be repeated; they
are checked against both explorers and left unchanged. A height whose h+5 does not yet have 6 confirmations (tip below
h+10, about 100 minutes after h) is refused: leave it out and say so.

## Step 2: add the pins

**2.1** Fetch, check and add:
```
python3 service/verifier/release/release_tool.py pins --trust service/verifier/release/v1-1/trust.json --heights H1,H2
```
Expect two lines, exit 0:
```
PINS ADDED <6 × new heights>: <each added height, ascending>
  <60 + added> pins; as_of <newest pinned header time>; trust sha256 <8 groups>; release_constants.py regenerated
```
`as_of` here is steward preparation policy (owner decision 2026-11-24): newest pinned header time, never below the
previous `as_of`, never above the local clock; the profile only requires a valid nondecreasing horizon. The command holds
a lock (`trust.json.lock`, removed at the end) so one run at a time, and writes both files or neither.
Any `REFUSED:` line (explorers disagree, a header not hashing to its id, a broken link, too few confirmations, an
existing pin contradicted) is a stop: nothing is written on refusal. A `curl` error: run it once more.

**2.2** Tests (no network):
```
cd service/verifier && TESSERA_VERIFY_INSTALL_JSON=/home/tony/projects/tessera/service/verifier/install.json /home/tony/projects/tessera/service/verifier/.venv/bin/python -m pytest -q -p no:cacheprovider; cd ../..
```
Expect `1 failed, 166 passed` (the failure is `test_independence.py::…test_loaded_modules_come_from_the_service_tree_only`,
worktree-only). The `Pins` tests use their own fixture and do not change with the trust file.

**2.3** Commit the source (the post-commit hook then adds an `ots: stamp` commit; that is expected):
```
git add service/verifier/release/v1-1/trust.json service/verifier/release/v1-1/release_constants.py && git commit -q -m "Release v1-1: pin anchors H1,H2" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
**2.4** Name the source commit (the commit that last changed the trust file, not the stamp commit):
```
SRC=$(git log -1 --format=%H -- service/verifier/release/v1-1/trust.json) && echo $SRC
```
Expect 40 hex digits, not `cb474356…` (candidate 4's).

## Step 3: rebuild, check, update the documents

**3.1** Build from the worktree:
```
B1=$(mktemp -d) && python3 service/verifier/release/release_tool.py build --repo . --commit $SRC --out $B1/out
```
Expect `BUILT tessera-verifier-v1-1.parts  sha256 <8 groups>`: the new candidate hash.

**3.2** Build again from an independent clone, with the clone's own tool:
```
C=$(mktemp -d) && git clone -q --no-local . $C/t && git -C $C/t checkout -q $SRC && python3 $C/t/service/verifier/release/release_tool.py build --repo $C/t --commit HEAD --out $C/out
```
Expect the same `BUILT` line as 3.1.

**3.3** Byte-compare:
```
cmp $B1/out/tessera-verifier-v1-1.parts $C/out/tessera-verifier-v1-1.parts && echo IDENTICAL
```
Expect `IDENTICAL`.

**3.4** The author's check, from the clone:
```
python3 $C/t/service/verifier/release/release_tool.py check $C/out/tessera-verifier-v1-1.parts --repo $C/t
```
Expect 12 lines: `CHECK PASS`, the new archive hash, `source commit <SRC>`, `trust file sha256 <as in 2.1> version 1
as_of <as in 2.1>`, `parts 31`, `header pins <count> heights: …` listing every pinned height.

**3.5** The change list, from both checkouts:
```
python3 service/verifier/release/release_tool.py diff --repo . --base b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --commit $SRC --out $B1/diff.txt
```
```
python3 $C/t/service/verifier/release/release_tool.py diff --repo $C/t --base b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --commit HEAD --out $C/diff.txt
```
Expect the same line twice: `DIFF 7 added or changed, 0 removed; sha256 of the text above <8 groups>`.

**3.6** Byte-compare, install and hash the change list:
```
cmp $B1/diff.txt $C/diff.txt && cp $B1/diff.txt docs/releases/v1-1/DIFF.txt && sha256sum docs/releases/v1-1/DIFF.txt
```
Expect one line: the new whole-file digest.

**3.7** Sources (both explorers, every pin; IANA):
```
python3 service/verifier/release/release_tool.py sources $B1/out/tessera-verifier-v1-1.parts | tee $B1/sources.txt | tail -1 && wc -l < $B1/sources.txt
```
Expect `SOURCES PASS: 2 KSKs and <count> pins equal their public sources.` and `<count + 3>`.

**3.8** Update by hand, with the values from 3.1-3.7 (`release_tool.py` and `sign-release.sh` do not change on a
refresh, so their hashes stay):
- `docs/ceremony/release-REHEARSAL-SHEET.md` and `docs/ceremony/release-v1-1-SHEET.md`: the source commit (table, in
  groups of 8, and the `git checkout` line), the change list's last line (table and the `Want one line` after `diff`),
  the change list's whole-file digest, the archive hash (table and `Want one line` after `build`), the `check`
  paragraph (`source commit`, `trust file sha256`, `as_of`, `header pins <count> heights`) and the block of heights
  under it (one run of six per line), the `sources` paragraph (`exactly <count + 3> lines`, `<count> height …`,
  `<count> pins`).
- `docs/releases/v1-1/SUMMARY.md`: title and candidate number, the candidate table (bytes from `wc -c`, hash, source
  commit, change list), Reproducibility, the hash table (archive, both change-list rows, trust file,
  `release_constants.py` from `sha256sum service/verifier/release/v1-1/release_constants.py`), the header-pins row,
  `as_of`, "What these pins cover" (the newest pinned anchor height), and a new "Checks run" entry.
- Then search for the old values; expect no hits outside `docs/releases/v1-1/evidence/` and `docs/reviews/`:
```
grep -rn "e88a0a78\|f5e88951\|ea02b7b8\|59199eaf\|cb474356" docs/ceremony docs/releases/v1-1/SUMMARY.md
```
**3.9** Commit the documents and the transcript (`$B1/sources.txt` copied to
`docs/releases/v1-1/evidence/candidate-<n>.txt` with the build, check and diff lines), then push `release-pins` so the
source commit is on GitHub before the sitting.

## Candidate 4, for reference (2026-11-24)

Anchors 975705, 976141, 976209, 976283, 976445, 976596, 976735, 976918, 977072, 977216; 60 pins; `as_of`
`2026-11-23T14:44:14Z`; source `cb474356aafa95a5bf8c35128aaec654b2b3e33f`; archive `e88a0a78…56e8f19c`; change list
whole file `f5e88951…1226e95f`; `sources` 63 lines.
