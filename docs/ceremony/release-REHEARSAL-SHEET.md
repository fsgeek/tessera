# Release rehearsal (TEST key): operator sheet (one sitting, about 90 minutes)

You build the release yourself from GitHub, check it, then sign it in an offline session with a throwaway TEST key
that the script makes in memory. The production procedure must then **refuse** that TEST-signed archive (A10 row
36). No YubiKey is used. Nothing from this sitting is ever a release.

| Stick | What | Rule |
|---|---|---|
| INPUT | a purple rehearsal stick (never in the NUC) | written only in Part 1; keep it purple afterwards |
| OUT | the other purple stick | goes to the owner after Part 2; never returns to a signing session |

Every command is on its own line: type one, press Enter, read the result, then the next. **[PHOTO]** = photograph the
screen. **[WRITE]** = write on this sheet. **Start time:** ________ (write it now).

The owner's values (compare in full; each is in groups of 8):
- source commit: `7b986e83 57d26b1f d1604217 e1a5a2a6 d3868f23`
- archive `tessera-verifier-v1-1.parts`: `49e65de3 b460c589 25c75329 35dabd91 8d81828f df8cf4b8 ff9be745 b730d829`
- `release_tool.py`: `3a506e9e ae09e24f 25aa41c5 f1847778 2bebb86f 2082d1b5 4d16d284 820e045c`
- `sign-release.sh`: `f9a0a5f6 ed1bfe0b f5abd402 da2be73b e5982cb6 c53334c4 55c4377a 2cf5c5b4`
- release public key: `1a817ae3 9f974501 84d85e5c 09bbdc0a 301b18be 65c8c397 5144d3d8 160cf6f3`

## Part 1: build and check (a Tails boot, network ON)

Welcome Screen: **set an administration password** (needed for *Disks*); do not unlock Persistent Storage. Connect
to Tor. No stick inserted yet. Open a terminal.

**If anything in Part 1 differs from what is written here:** stop, **[PHOTO]**, shut down, tell the owner. Nothing
has been signed; nothing needs cleaning up.

```
git clone https://github.com/fsgeek/tessera.git
```
```
cd tessera
```
```
git checkout 7b986e8
```
```
git rev-parse HEAD
```
Want: the source commit above, in full.
```
sha256sum service/verifier/release/release_tool.py docs/ceremony/sign-release.sh docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: the three values above, in that order. Read both scripts (space pages, q quits):
```
less service/verifier/release/release_tool.py
```
```
less docs/ceremony/sign-release.sh
```
Recompute the frozen objects from source:
```
python3 formal/freeze-v1/assemble.py --repo . --commit 270ca49 --out /tmp/fz
```
Want, among its lines: `spec.bin 470034 397581f7…` and `catalog.json 662 aaf4306f…` (the freeze record's values).
Build the release yourself:
```
python3 service/verifier/release/release_tool.py build --repo . --commit 7b986e8 --out /tmp/out
```
Want: `BUILT tessera-verifier-v1-1.parts  sha256 49e65de3 b460c589 …` equal to the archive value above. **[WRITE]**
the eight groups you see: ____________________________________________________________
```
python3 service/verifier/release/release_tool.py check /tmp/out/tessera-verifier-v1-1.parts --repo .
```
Want: `CHECK PASS`, `namespace PRODUCTION release 1 successor None`, the catalog `aaf4306f …`, and `repository key
6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A`. Compare that key with your paper ceremony record. **[PHOTO]**
```
python3 service/verifier/release/release_tool.py sources /tmp/out/tessera-verifier-v1-1.parts
```
Want: 14 lines ending `SOURCES PASS: 2 KSKs and 12 pins equal their public sources.` (a few minutes over Tor).
**[PHOTO]** *(Rehearsal only: if it fails with `curl` or a network error rather than an unequal value,
**[WRITE]** the error and go on; the owner fixes it before the production sitting.)*

In Tor Browser open `https://orcid.org/0000-0002-0651-5019`. In the Biography, compare the release key and the
repository root with your paper ceremony record. **[WRITE]** ORCID = paper: yes / no ________

Insert INPUT. In *Disks*: INPUT → *Format Disk* → `+` → *For use with all systems (FAT)*, volume name `INPUT`. Open it
in *Files*. Then:
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
sha256sum /media/amnesia/INPUT/*.*
```
Want: the archive, release key (as `release.pub.asc`), `release_tool.py` and `sign-release.sh` values above. Eject
INPUT; shut down.

## Part 2: sign with a TEST key (a new Tails boot, network OFF)

Welcome Screen: **set an administration password**; do not unlock Persistent Storage; **Offline Mode** (networking
disabled). Insert INPUT and OUT. In *Disks*: OUT → *Format Disk* → `+` → FAT, volume name `OUT`. Open both in
*Files*. Open a terminal.

**If the script prints FAIL:** nothing has left the session. **[PHOTO]** the message, shut down, tell the owner.
Restart from Part 2 only if the owner says so (INPUT is still good).

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
It then asks you, in order:
1. **[WRITE]** the `gpg (GnuPG)` and `gpgv (GnuPG)` version lines: __________________ / __________________
2. Three hashes: compare each with this sheet, in full; type `yes`.
3. Eject INPUT in *Files*, remove it, press Enter.

Then it runs to the end without questions. Want, in order: `INSPECT PASS: PRODUCTION release 1`; the release key
`CADC 96CF …`; `TEST key …` (a new throwaway fingerprint); `SIGNATURE PASS` for the TEST key; `MUTATION REFUSED (as
required)`; **twice** `ROW 36 REFUSED … (as required)`; the vector table ending `9/9 match`; the OUT listing; and
`==> PASS: rehearse`. **[PHOTO]** the row 36 lines, the vector table and the final PASS.

Eject OUT; shut down. **End time:** ________

## After

OUT goes to the owner (it holds the TEST signature, the TEST public key and `record.txt`; all public). Keep INPUT
purple and away from the NUC: it may be the INPUT of the production sitting. Tell the owner the start and end times
and anything you wrote above.
