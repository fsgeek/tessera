# Release rehearsal (TEST key): operator sheet

You read, on the Pangolin's own screen, the change list the Pangolin makes from GitHub (every change since the dated
baseline), approve it and write its digest on this sheet; build the release yourself; then sign it offline with
a throwaway TEST key that the script makes in memory. The production acquisition must then **refuse** that
TEST-signed archive (A10 row 36). No YubiKey is used. Nothing from this sitting is ever a release.

**Time:** Part 1 about 75 minutes plus about 2 hours reading the change list on screen (once; the production sitting
compares against the digest you write here). Part 2 about 30 minutes.

| Stick | What | Rule |
|---|---|---|
| INPUT | a purple stick that has never been in the NUC or any everyday computer | written only in Part 1; afterwards kept purple, away from the NUC |
| OUT | the other purple stick, never in the NUC or any everyday computer **on entry** | goes to the owner after Part 2; never returns to a signing session |

Every command is on its own line: type one, press Enter, read the result, then the next. **[PHOTO]** = photograph the
screen. **[WRITE]** = write on this sheet. Hashes are shown in groups of 8; the screen shows them without spaces.

**Stop rule, all parts:** if anything differs from what is written here, or a value on paper, ORCID and screen
disagree: stop, **[PHOTO]**, shut down, tell the owner. Nothing has been signed; nothing needs cleaning up.

Values (each must equal what you see, in full):

| Name | Value |
|---|---|
| source commit | `b22e08f2 98da6aef 8d750322 d2ee006e b9738f33` |
| baseline commit | `b134cdfd acc5d89f 2748fa7e c15c46e3 8b51a32c` (the Codex-reviewed verifier, dated 2026-10-26) |
| freeze commit | `52ee1791 8c5ed841 587d78cb 2ca3e8c5 4c4682d2` |
| change list, last line | `DIFF 7 added or changed, 0 removed; sha256 of the text above 74e65031 abd7ff75 6a574a6b 4c417f4d 41a6f65a bf9ed9e8 e95126e3 a90e33fa` |
| change list, whole file `/tmp/diff.txt` | `c7bbb193 842decff 8854e483 f91ac60e d17563be 5a700cd2 6736194e 15ab3ff1` |
| archive `tessera-verifier-v1-1.parts` | `1342b5b9 815eba01 c07ba464 702a2444 56515d5c 2afa38a0 f1814e88 088dc272` |
| `release_tool.py` | `5225491c 3a8ff58c d63be3a0 0b44c51a d617667f 8a20e412 0b75966c 01e7c458` |
| `sign-release.sh` | `20d5e19c 1ff46f0a f25b3dc9 308290e3 014a3084 c0c887a0 31b450e3 8a2df15a` |
| release public key file | `1a817ae3 9f974501 84d85e5c 09bbdc0a 301b18be 65c8c397 5144d3d8 160cf6f3` |
| release vectors (all files) | `66d149cd 999d0ccc fca10c98 4715d3ed bbddb6ad 4ba2b789 682d45b0 c43eca93` |
| release key fingerprint | `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` |
| repository root fingerprint | `6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A` |

## Before the sitting (optional)

The owner may give you `docs/releases/v1-1/DIFF.txt` printed, to read beforehand and mark. It is only a reading aid:
it was printed by the NUC, and you do not sign or approve it. What you approve is the change list the Pangolin itself
makes in Part 1, read on the Pangolin's screen.

## Part 1: check, build, decide (a Tails boot, network ON)

Welcome Screen: **set an administration password** (needed for *Disks*); do not unlock Persistent Storage. Connect
to Tor. No stick inserted yet. Open a terminal.

```
git clone https://github.com/fsgeek/tessera.git
```
```
cd tessera
```
```
git checkout b22e08f298da6aef8d750322d2ee006eb9738f33
```
```
git rev-parse HEAD
```
Want: the source commit, in full.
```
sha256sum service/verifier/release/release_tool.py docs/ceremony/sign-release.sh
```
Want: the `release_tool.py` and `sign-release.sh` values above. These two scripts run in both sittings.
```
python3 service/verifier/release/release_tool.py diff --repo . --base b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --commit HEAD --out /tmp/diff.txt
```
Want one line: `DIFF 7 added or changed, 0 removed; sha256 of the text above 74e65031 abd7ff75 6a574a6b 4c417f4d
41a6f65a bf9ed9e8 e95126e3 a90e33fa`.
```
sha256sum /tmp/diff.txt
```
Want: the change list, whole file, value above. **[WRITE]** the eight groups you see:
____________________________________________________________ (the production sitting compares against this).
```
grep -E '  (service/verifier/release/release_tool.py|docs/ceremony/sign-release.sh)$' /tmp/diff.txt
```
Want two lines whose hashes equal the two `sha256sum` results above.

**Read the change.** The release tool writes the change list, including its own text, so read the two scripts from
the files themselves:
```
less service/verifier/release/release_tool.py docs/ceremony/sign-release.sh
```
(Space: next page; `b`: back; `:n`: the second file; `q`: quit.) Then read the whole change list on this screen:
```
less /tmp/diff.txt
```
It lists every file that enters the archive, each with its SHA-256, and prints in full each one added or changed
since the baseline commit: the release tool, the signing script (both just read), `install.sh`, the lock, the trust
file, the release constants, the README. The verifier code and the vendored SHA-1DC source are unchanged since the
baseline (their lines say `unchanged`). A printout, if you have one, may help you follow; it is not what you approve.
**[WRITE]** I approve the change list as read on this screen, whole-file digest as written above: yes / no ________ .
No is a stop.
```
python3 service/verifier/release/release_tool.py baseline --repo . --commit b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --source HEAD
```
Want exactly two lines (about a minute over Tor):
`BASELINE PASS: b134cdfdacc5d89f2748fa7ec15c46e38b51a32c existed by Bitcoin block 973240, header time 2026-10-26T13:12:22Z (blockstream.info and mempool.space agree);`
and `  freeze commit 52ee17918c5ed841587d78cb2ca3e8c54c4682d2 is its ancestor.` So the baseline commit's bytes were
fixed by 2026-10-26, four weeks before any release file, and cannot have been rewritten since, if the two explorers
serve genuine chain data and Git's object hashes hold. It does not show that you approved that baseline (the
procedure's question 5). **[PHOTO]**
If it prints `REFUSED:` with a `curl` network error (exit status 28 is a timeout, 97 a failed connection to Tor;
not an unequal value), check that *Tor Connection* shows connected, then run it once more. A second network failure
is a stop: **[WRITE]** the error here: ______________ .
```
python3 formal/freeze-v1/assemble.py --repo . --commit 270ca49 --out /tmp/fz
```
Want exactly these five lines (the freeze record's table):
```
spec.bin                      470034 397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf
vectors.bin                  3123748 19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f
preamble.bin                    1205 1eebd4a8c2ac405117ba5c4951f053c92459952194a760993dafea1c8959468f
dependency-manifest.json       41181 20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063
catalog.json                     662 aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2
```
Build the release yourself:
```
python3 service/verifier/release/release_tool.py build --repo . --commit HEAD --out /tmp/out
```
Want one line: `BUILT tessera-verifier-v1-1.parts  sha256 1342b5b9 815eba01 c07ba464 702a2444 56515d5c 2afa38a0 f1814e88
088dc272`. **[WRITE]** the eight groups you see: ____________________________________________________________
```
python3 service/verifier/release/release_tool.py check /tmp/out/tessera-verifier-v1-1.parts --repo .
```
Want exactly 12 lines: `CHECK PASS: …`; the archive line with the hash above; `namespace PRODUCTION release 1
successor None`; `source commit b22e08f2…`; `freeze commit 52ee1791… record sha256 05542967 b091424a 614afd38 a32cfb84
7b9b6b3f 0e5a7b71 03b11cd2 2d95575e`; `catalog sha256 aaf4306f ed070119 022c8486 219f5160 dc869eda a929f323 d962fbb6
79e27fc2`; `trust file sha256 3ef97f19 527d7616 8dab10d8 5f396a6d 5c8a602c b63047a5 61098646 0e69a176 version 1 as_of
2026-11-25T16:20:25Z`; `parts 31`; `repository key 6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A from
2026-11-10T19:44:55Z to None`; two `root KSK` lines (KSK-2017 tag 20326, KSK-2024 tag 38696);
`header pins 72 heights: …` followed by the 72 heights below, in this order (twelve runs of six). Compare the
repository key with your paper ceremony record. **[PHOTO]**
```
975705 975706 975707 975708 975709 975710
976141 976142 976143 976144 976145 976146
976209 976210 976211 976212 976213 976214
976283 976284 976285 976286 976287 976288
976445 976446 976447 976448 976449 976450
976596 976597 976598 976599 976600 976601
976735 976736 976737 976738 976739 976740
976918 976919 976920 976921 976922 976923
977072 977073 977074 977075 977076 977077
977216 977217 977218 977219 977220 977221
977379 977380 977381 977382 977383 977384
977531 977532 977533 977534 977535 977536
```
```
python3 service/verifier/release/release_tool.py sources /tmp/out/tessera-verifier-v1-1.parts
```
Want exactly 75 lines: 2 `KSK-… digest equals IANA root-anchors.xml`, 72 `height … pin equals blockstream.info and
mempool.space` (the 72 heights above, ascending), then `SOURCES PASS: 2 KSKs and 72 pins equal their public
sources.` (144 requests over Tor; allow about 18 minutes).
**[PHOTO]** If it fails with `curl` or another network error (not an unequal value), run it once more. If it fails
again the same way, **[WRITE]** the error here: ______________ ; the rehearsal's source check is then incomplete and
is recorded so; go on. An unequal value is a stop.
```
sha256sum docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: the release public key file value above.
```
gpg --show-keys docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: one `pub nistp256 2026-11-10 [SC]` line, the release key fingerprint above, `uid Tessera release key
<tessera@wamason.com>`, and no `sub` line.
```
cd service
```
```
find release-vectors -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum
```
Want: the release vectors value above, then `  -`.
```
cd ..
```
In Tor Browser open `https://orcid.org/0000-0002-0651-5019`. In the Biography, compare the release key and the
repository root with your paper ceremony record and with the two fingerprints above. **[WRITE]** ORCID = paper =
sheet, both keys: yes / no ________ . No is a stop.

Insert INPUT only now. Identify it before formatting:
```
lsblk -o NAME,TRAN,SERIAL,SIZE,LABEL
```
INPUT is the `usb` line that is not your Tails stick. **[WRITE]** its SERIAL: ______________________ . In *Disks*:
INPUT → *Format Disk* → `+` → *For use with all systems (FAT)*, volume name `INPUT`. Open it in *Files*. Then:
```
cp /tmp/out/tessera-verifier-v1-1.parts service/verifier/release/release_tool.py docs/ceremony/sign-release.sh /media/amnesia/INPUT/
```
```
cp docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc /media/amnesia/INPUT/release.pub.asc
```
```
cp -R service/release-vectors /media/amnesia/INPUT/release-vectors
```
```
sha256sum /media/amnesia/INPUT/tessera-verifier-v1-1.parts /media/amnesia/INPUT/release_tool.py /media/amnesia/INPUT/sign-release.sh /media/amnesia/INPUT/release.pub.asc
```
Want, in that order: the archive (equal to what you wrote), `release_tool.py`, `sign-release.sh` and release public
key file values above. Eject INPUT in *Files*; remove it; shut down.

## Part 2: sign with a TEST key (a new Tails boot, network OFF)

Welcome Screen: **set an administration password**; do not unlock Persistent Storage; **Offline Mode** (networking
disabled). Insert INPUT and OUT. Open a terminal.
```
lsblk -o NAME,TRAN,SERIAL,SIZE,LABEL,MOUNTPOINTS
```
Want: no line whose TRAN is not `usb` (the internal disk, `nvme…`) shows a mount point; INPUT's line shows the
SERIAL you wrote in Part 1. **[WRITE]** OUT's SERIAL: ______________________ . In *Disks*: OUT → *Format Disk* → `+`
→ FAT, volume name `OUT`. Open both in *Files*.
```
cp /media/amnesia/INPUT/sign-release.sh /tmp/s.sh
```
```
sha256sum /tmp/s.sh
```
Want: the `sign-release.sh` value above.
```
bash /tmp/s.sh rehearse
```
**If the script prints `==> FAIL`:** **[PHOTO]**, shut down, tell the owner. If the message says OUT IS QUARANTINED,
write QUARANTINE on OUT; nothing on it is used. In every other case OUT is empty.

It asks, in order:
1. After the `gpg (GnuPG)` and `gpgv (GnuPG)` lines, the `gpgv binary` hash and the two stick lines: **[WRITE]** the
   two version lines ______________ / ______________ and the gpgv binary hash, 8 groups:
   ____________________________________________________________ . The INPUT stick line must show the serial you
   wrote in Part 1 and the OUT line the serial you wrote above; type `yes`.
2. Four values: the archive (equal to what you wrote in Part 1), `release_tool.py`, the release public key file and
   the release vectors (equal to the values above); type `yes`.
3. Eject INPUT in *Files*, remove it, press Enter.

Then it runs to the end. Want, in order:
- `INSPECT PASS: PRODUCTION release 1, 31 parts, R2 bindings hold.`, the archive hash, `namespace PRODUCTION`;
- the release key lines and `key file holds exactly the key CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E`;
- `TEST key …` (a new 40-character fingerprint, not the release key's);
- `SIGNATURE PASS: rule O, signer <the TEST key>, …`: a control, showing the TEST signature itself is good;
- `REFUSED: gpgv refused (exit 1): …BAD signature…` and `MUTATION REFUSED (as required)`;
- **twice** `REFUSED: signed by <the TEST key>, not by the authenticated key CADC96CF002355F8E83FE97FAFF80961D825035E`,
  each followed by `ROW 36 REFUSED, nothing unpacked, key offered: …` (first `release.pub.asc`, then `test.pub.pgp`);
- `(The installed verifier's section 3.5 refusal needs Python 3.14 and cannot run here: NUC evidence only.)`;
- the vector table: 9 lines starting `match`, then `9/9 match`;
- the OUT listing: exactly 3 names, `record.txt`, `tessera-verifier-v1-1.parts.sig`, `test.pub.pgp`; then exactly
  3 hash lines, one per file; then `==> PASS: rehearse. …`

**[PHOTO]** the row 36 lines, the vector table and the final PASS. Eject OUT; shut down. **End time:** ________

## After

OUT goes to the owner (the TEST signature, the TEST public key and `record.txt`; all public). Keep this sheet: the
change-list digest you wrote is what the production sitting compares. Keep INPUT purple and
away from the NUC and every everyday computer: it may be the production sitting's INPUT. Tell the owner the times
and everything you wrote. The second half of row 36 (the installed production verifier refusing the section 3.5
interface with `TEST_AUTHORITY_REFUSED`, exit 2, no verdict) needs Python 3.14, which Tails lacks; it is the NUC's
recorded evidence (`docs/releases/v1-1/evidence/`), not part of this sitting.
