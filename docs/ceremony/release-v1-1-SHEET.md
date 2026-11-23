# Verifier release 1 (YubiKey B): operator sheet

You confirm the changes you approved at the rehearsal, build release 1 yourself from GitHub and check it, then sign
that archive with YubiKey B in an offline session. Your signature says: *this exact archive is Tessera's first
production verifier release.* The owner then publishes the archive the NUC built, which must be byte-identical to
yours, or your signature does not verify over it.

**Time:** Part 1 about 60 minutes, Part 2 about 30. Nothing to read beforehand if the source commit below is the
rehearsal's; if it is not, the owner gives you a new printed change list first and this sheet is reprinted.

| Item | What | Rule |
|---|---|---|
| INPUT | the rehearsal's INPUT (purple), or a new stick; never in the NUC or any everyday computer | written only in Part 1 |
| OUT | a **new** stick, never in the NUC or any computer, not the rehearsal's OUT | goes to the owner after Part 2; never returns |
| YubiKey B | the release key, white tag, serial 39975596 | inserted only when the script asks |
| Paper | your 2026-11-10 ceremony record; the change list you signed at the rehearsal | at hand for both parts |

Every command is on its own line: type one, press Enter, read the result, then the next. **[PHOTO]** = photograph the
screen. **[WRITE]** = write on this sheet. Never photograph or type into chat a PIN. Hashes are shown in groups of 8.

**Stop rule, all parts:** if anything differs from what is written here, or paper, ORCID and screen disagree: stop,
**[PHOTO]**, shut down, tell the owner. Before YubiKey B is inserted nothing has been signed.

Values (each must equal what you see, in full):

| Name | Value |
|---|---|
| source commit | `f2511c0d 87f39039 6b50e687 a7bef496 544462da` (the rehearsal's) |
| baseline commit | `b134cdfd acc5d89f 2748fa7e c15c46e3 8b51a32c` |
| printed changes, last line | `DIFF 7 added or changed, 0 removed; sha256 of the text above 09bd9d55 fcfa0501 f7a60b51 6849227f def0f749 a9a685e5 f8756ac4 82e6c874` |
| archive `tessera-verifier-v1-1.parts` | `7fd00606 b5591d9a 3a410512 776e3a0e 82fa2662 8c179987 49ca1a0d a61de614` |
| `release_tool.py` | `a4531c7d 527953b2 6cfb6c7c 72e40420 7f381523 98e4fb94 4c7fd977 b0e6539f` |
| `sign-release.sh` | `4f7ac1b4 d33d4147 bb3c9f4e ff1c1c6d dea76bd4 d7045242 c7ea1055 bb014275` |
| release public key file | `1a817ae3 9f974501 84d85e5c 09bbdc0a 301b18be 65c8c397 5144d3d8 160cf6f3` |
| release key fingerprint | `CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E` |
| repository root fingerprint | `6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A` |
| GnuPG lines at the rehearsal | ______________________ / ______________________ (from your rehearsal sheet) |
| gpgv binary at the rehearsal | ____________________________________________________________ (from your rehearsal sheet) |

## Part 1: check, build, decide (a Tails boot, network ON)

Welcome Screen: **set an administration password** (needed for *Disks*); do not unlock Persistent Storage. Connect
to Tor. No stick and no YubiKey inserted. Open a terminal.

```
git clone https://github.com/fsgeek/tessera.git
```
```
cd tessera
```
```
git checkout f2511c0d87f390396b50e687a7bef496544462da
```
```
git rev-parse HEAD
```
Want: the source commit, in full.
```
sha256sum service/verifier/release/release_tool.py docs/ceremony/sign-release.sh
```
Want: the `release_tool.py` and `sign-release.sh` values above, equal to their lines in your signed change list.
```
python3 service/verifier/release/release_tool.py diff --repo . --base b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --commit HEAD --out /tmp/diff.txt
```
Want one line, equal to the last line of your signed change list: `DIFF 7 added or changed, 0 removed; sha256 of the
text above 09bd9d55 fcfa0501 f7a60b51 6849227f def0f749 a9a685e5 f8756ac4 82e6c874`.
```
python3 service/verifier/release/release_tool.py baseline --repo . --commit b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --source HEAD
```
Want exactly two lines:
`BASELINE PASS: b134cdfdacc5d89f2748fa7ec15c46e38b51a32c existed by Bitcoin block 973240, header time 2026-10-26T13:12:22Z (blockstream.info and mempool.space agree);`
and `  freeze commit 52ee17918c5ed841587d78cb2ca3e8c54c4682d2 is its ancestor.` **[PHOTO]**
```
python3 formal/freeze-v1/assemble.py --repo . --commit 270ca49 --out /tmp/fz
```
Want exactly these five lines:
```
spec.bin                      470034 397581f781830b38ce1d07a25867f26d2c025e439cdd2a94e83ee77685d26daf
vectors.bin                  3123748 19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f
preamble.bin                    1205 1eebd4a8c2ac405117ba5c4951f053c92459952194a760993dafea1c8959468f
dependency-manifest.json       41181 20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063
catalog.json                     662 aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2
```
```
python3 service/verifier/release/release_tool.py build --repo . --commit HEAD --out /tmp/out
```
Want one line: `BUILT tessera-verifier-v1-1.parts  sha256 7fd00606 b5591d9a 3a410512 776e3a0e 82fa2662 8c179987 49ca1a0d
a61de614`. **[WRITE]** the eight groups you see: ____________________________________________________________
```
python3 service/verifier/release/release_tool.py check /tmp/out/tessera-verifier-v1-1.parts --repo .
```
Want exactly 12 lines: `CHECK PASS: …`; the archive line with the hash above; `namespace PRODUCTION release 1
successor None`; `source commit f2511c0d…`; `freeze commit 52ee1791… record sha256 05542967 b091424a 614afd38 a32cfb84
7b9b6b3f 0e5a7b71 03b11cd2 2d95575e`; `catalog sha256 aaf4306f ed070119 022c8486 219f5160 dc869eda a929f323 d962fbb6
79e27fc2`; `trust file sha256 9faa0368 3df7506c efa07afa 4c062918 2ebc5d42 86b97801 e1053cb8 d86a7f89 version 1 as_of
2026-11-16T15:48:11Z`; `parts 31`; `repository key 6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A from
2026-11-10T19:44:55Z to None`; two `root KSK` lines (KSK-2017 tag 20326, KSK-2024 tag 38696); `header pins 12 heights:
975705 975706 975707 975708 975709 975710 976141 976142 976143 976144 976145 976146`. Compare the repository key with
your paper ceremony record. **[PHOTO]**
```
python3 service/verifier/release/release_tool.py sources /tmp/out/tessera-verifier-v1-1.parts
```
Want exactly 15 lines: 2 `KSK-… digest equals IANA root-anchors.xml`, 12 `height … pin equals blockstream.info and
mempool.space`, then `SOURCES PASS: 2 KSKs and 12 pins equal their public sources.` If it fails with a network error,
run it once more; a second failure, or any unequal value, is a stop. **[PHOTO]**
```
sha256sum docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: the release public key file value above.
```
gpg --show-keys docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: one `pub nistp256 2026-11-10 [SC]` line, the release key fingerprint above, `uid Tessera release key
<tessera@wamason.com>`, and no `sub` line.

**The fingerprint check.** In Tor Browser open `https://orcid.org/0000-0002-0651-5019`. Compare the release key and
the repository root in the Biography with your **paper ceremony record** and with the two fingerprints above.
**[WRITE]** ORCID = paper = sheet, both keys: yes / no ________ . No is a stop.

**Your decision.** Sign only if every Want above held. **[WRITE]** approve release 1, archive hash as written above:
yes / no ________ , time ________

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
sha256sum /media/amnesia/INPUT/tessera-verifier-v1-1.parts /media/amnesia/INPUT/release_tool.py /media/amnesia/INPUT/sign-release.sh /media/amnesia/INPUT/release.pub.asc
```
Want, in that order: the archive (equal to what you wrote), `release_tool.py`, `sign-release.sh` and release public
key file values above. Eject INPUT in *Files*; remove it; shut down.

## Part 2: sign (a new Tails boot, network OFF)

Welcome Screen: **set an administration password**; do not unlock Persistent Storage; **Offline Mode** (networking
disabled). Insert INPUT and OUT, not YubiKey B. Open a terminal.
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
bash /tmp/s.sh sign
```
**If it prints `==> FAIL` before YubiKey B is inserted:** nothing is signed. **[PHOTO]**, shut down, tell the owner.
**If a PIN is refused once:** stop; do not try again; remove YubiKey B, shut down, tell the owner (the retry counter
must never run out). **If any card line differs from step 5 below:** press Ctrl-C, remove YubiKey B, shut down, tell
the owner. **If it prints `==> FAIL` after signing**, or the run ends without `==> PASS: sign`: remove YubiKey B; if
the message says OUT IS QUARANTINED, write QUARANTINE on OUT, and nothing on it is used; **[PHOTO]**, shut down, tell
the owner. Never reset the card, whatever fails.

It asks you, in order:
1. After the `gpg (GnuPG)` and `gpgv (GnuPG)` lines and the `gpgv binary` hash: these three must equal the
   rehearsal's, written above (if not: Ctrl-C, shut down, tell the owner). The INPUT stick line must show the serial
   you wrote in Part 1 and the OUT line the serial you wrote in Part 2; type `yes`.
2. Three values: the archive (equal to what you wrote in Part 1), `release_tool.py` and the release public key file
   (equal to the values above); type `yes`.
3. Eject INPUT in *Files*, remove it, press Enter.
4. After `INSPECT PASS: PRODUCTION release 1, 31 parts, R2 bindings hold.`, `namespace PRODUCTION` and the key lines
   ending `key file holds exactly the key CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E`: compare that fingerprint
   with your **paper** and with **ORCID** as you checked it in Part 1; type `yes`.
5. Insert YubiKey B, press Enter. Want exactly two card lines: `Serial number ....: 39975596` and `Signature key ....:
   CADC 96CF 0023 55F8 E83F  E97F AFF8 0961 D825 035E`. The script also refuses any other serial or key.
6. The archive hash once more: compare with the eight groups you wrote in Part 1; type `yes`. This signs.
7. Enter the user PIN; touch YubiKey B when it blinks.
8. Remove YubiKey B, press Enter.

Then it runs to the end. Want, in order: `SIGNATURE PASS: rule O, signer CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825
035E, gpgv exit 0 with only that key.`; `REFUSED: gpgv refused (exit 1): …BAD signature…` and `MUTATION REFUSED (as
required)`; the OUT listing with exactly `record.txt` and `tessera-verifier-v1-1.parts.sig`, their hashes; and
`==> PASS: sign. …`. **[PHOTO]** the SIGNATURE PASS line, the OUT hashes and the final PASS. **[WRITE]** the `.sig`
hash, 8 groups: ____________________________________________________________

Eject OUT; remove it; shut down. **End time:** ________

## After

- OUT goes to the owner. YubiKey B goes back to its place; where it and its backup are kept is stated in the custody
  record, not here.
- Tell the owner "signed", the `.sig` hash and the times. The owner runs the release tool's `acquire` over the NUC's
  own archive and the signature from OUT, publishes the exact bytes it reports, the signature and the summary, stamps
  them, and writes the bootstrap record.
