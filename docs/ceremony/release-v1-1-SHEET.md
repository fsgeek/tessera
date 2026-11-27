# Verifier release 1 (YubiKey B): operator sheet

You confirm that the change list the Pangolin makes now is, byte for byte, the one you read and approved on screen at
the rehearsal (its digest is on your rehearsal sheet), build release 1 yourself from GitHub and check it, then sign
that archive with YubiKey B in an offline session. Your signature says: *this exact archive is Tessera's first
production verifier release.* The owner then publishes the archive the NUC built, which must be byte-identical to
yours, or your signature does not verify over it.

**Time:** Part 1 about 75 minutes, Part 2 about 30. Nothing to read if the source commit below is the
rehearsal's; if it is not, this sheet is reprinted and you read and approve the new change list on screen first, as at
the rehearsal.

| Item | What | Rule |
|---|---|---|
| INPUT | the rehearsal's INPUT (purple), or a new stick; never in the NUC or any everyday computer | written only in Part 1 |
| OUT | a **new** stick, never in the NUC or any computer, not the rehearsal's OUT | goes to the owner after Part 2; never returns |
| YubiKey B | the release key, white tag, serial 39975596 | inserted only when the script asks |
| Paper | your 2026-11-10 ceremony record; your filled-in rehearsal sheet | at hand for both parts |

Every command is on its own line: type one, press Enter, read the result, then the next. **[PHOTO]** = photograph the
screen. **[WRITE]** = write on this sheet. Never photograph or type into chat a PIN. Hashes are shown in groups of 8.

**Stop rule, all parts:** if anything differs from what is written here, or paper, ORCID and screen disagree: stop,
**[PHOTO]**, shut down, tell the owner. Before YubiKey B is inserted nothing has been signed.

Values (each must equal what you see, in full):

| Name | Value |
|---|---|
| source commit | `b22e08f2 98da6aef 8d750322 d2ee006e b9738f33` (the rehearsal's) |
| baseline commit | `b134cdfd acc5d89f 2748fa7e c15c46e3 8b51a32c` |
| change list, last line | `DIFF 7 added or changed, 0 removed; sha256 of the text above 74e65031 abd7ff75 6a574a6b 4c417f4d 41a6f65a bf9ed9e8 e95126e3 a90e33fa` |
| change list, whole file `/tmp/diff.txt` | `c7bbb193 842decff 8854e483 f91ac60e d17563be 5a700cd2 6736194e 15ab3ff1` |
| change list digest you approved | ____________________________________________________________ (from your rehearsal sheet) |
| archive `tessera-verifier-v1-1.parts` | `1342b5b9 815eba01 c07ba464 702a2444 56515d5c 2afa38a0 f1814e88 088dc272` |
| `release_tool.py` | `5225491c 3a8ff58c d63be3a0 0b44c51a d617667f 8a20e412 0b75966c 01e7c458` |
| `sign-release.sh` | `20d5e19c 1ff46f0a f25b3dc9 308290e3 014a3084 c0c887a0 31b450e3 8a2df15a` |
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
git checkout b22e08f298da6aef8d750322d2ee006eb9738f33
```
```
git rev-parse HEAD
```
Want: the source commit, in full.
```
sha256sum service/verifier/release/release_tool.py docs/ceremony/sign-release.sh
```
Want: the `release_tool.py` and `sign-release.sh` values above.
```
python3 service/verifier/release/release_tool.py diff --repo . --base b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --commit HEAD --out /tmp/diff.txt
```
Want one line: `DIFF 7 added or changed, 0 removed; sha256 of the text above 74e65031 abd7ff75 6a574a6b 4c417f4d
41a6f65a bf9ed9e8 e95126e3 a90e33fa`.
```
sha256sum /tmp/diff.txt
```
Want: all eight groups equal to the change-list digest you wrote on your rehearsal sheet (copied above). **Any
difference is a stop:** this is not the change list you approved. (The sheet's printed value must also match.)
```
grep -E '  (service/verifier/release/release_tool.py|docs/ceremony/sign-release.sh)$' /tmp/diff.txt
```
Want two lines whose hashes equal the two `sha256sum` results above: the scripts that run are the ones in the change
list you approved.
```
python3 service/verifier/release/release_tool.py baseline --repo . --commit b134cdfdacc5d89f2748fa7ec15c46e38b51a32c --source HEAD
```
Want exactly two lines:
`BASELINE PASS: b134cdfdacc5d89f2748fa7ec15c46e38b51a32c existed by Bitcoin block 973240, header time 2026-10-26T13:12:22Z (blockstream.info and mempool.space agree);`
and `  freeze commit 52ee17918c5ed841587d78cb2ca3e8c54c4682d2 is its ancestor.` **[PHOTO]**
If it prints `REFUSED:` with a `curl` network error (exit status 28 is a timeout, 97 a failed connection to Tor;
not an unequal value), check that *Tor Connection* shows connected, then run it once more. A second network failure
is a stop: **[WRITE]** the error here: ______________ .
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
sources.` (about 18 minutes over Tor.) If it fails with a network error, run it once more; a second failure,
or any unequal value, is a stop. **[PHOTO]**
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
required)`; the OUT listing, exactly 2 names, `record.txt` and `tessera-verifier-v1-1.parts.sig`, then exactly 2
hash lines, one per file; and `==> PASS: sign. …`. **[PHOTO]** the SIGNATURE PASS line, the OUT hashes and the final
PASS. **[WRITE]** the `.sig` hash, 8 groups: ____________________________________________________________

Eject OUT; remove it; shut down. **End time:** ________

## After

- OUT goes to the owner. YubiKey B goes back to its place; where it and its backup are kept is stated in the custody
  record, not here.
- Tell the owner "signed", the `.sig` hash and the times. The owner runs the release tool's `acquire` over the NUC's
  own archive and the signature from OUT, publishes the exact bytes it reports, the signature and the summary, stamps
  them, and writes the bootstrap record.
