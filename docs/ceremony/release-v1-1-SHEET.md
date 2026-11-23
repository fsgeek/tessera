# Verifier release 1 (YubiKey B): operator sheet (one sitting, about 90 minutes)

You build release 1 yourself from GitHub and check it, then sign that archive with YubiKey B in an offline session.
Your signature says: *this exact archive is Tessera's first production verifier release.* The owner then publishes
the archive the NUC built, which must be byte-identical to yours, or your signature does not verify over it.

| Item | What | Rule |
|---|---|---|
| INPUT | the rehearsal's INPUT stick, or a new stick (never in the NUC) | written only in Part 1 |
| OUT | a **new** stick (never in the NUC, never used for the rehearsal's OUT) | goes to the owner after Part 2; never returns |
| YubiKey B | the release key, white tag | inserted only when the script asks |
| Paper | your 2026-11-10 ceremony record (release fingerprint) | at hand for Part 1 and Part 2 |

Every command is on its own line: type one, press Enter, read the result, then the next. **[PHOTO]** = photograph the
screen. **[WRITE]** = write on this sheet. Never photograph or type into chat a PIN. **Start time:** ________

The owner's values (compare in full; each is in groups of 8):
- source commit: `7b986e83 57d26b1f d1604217 e1a5a2a6 d3868f23`
- archive `tessera-verifier-v1-1.parts`: `49e65de3 b460c589 25c75329 35dabd91 8d81828f df8cf4b8 ff9be745 b730d829`
- `release_tool.py`: `3a506e9e ae09e24f 25aa41c5 f1847778 2bebb86f 2082d1b5 4d16d284 820e045c`
- `sign-release.sh`: `f9a0a5f6 ed1bfe0b f5abd402 da2be73b e5982cb6 c53334c4 55c4377a 2cf5c5b4`
- release public key: `1a817ae3 9f974501 84d85e5c 09bbdc0a 301b18be 65c8c397 5144d3d8 160cf6f3`
- the GnuPG version lines you wrote at the rehearsal: __________________ / __________________

## Part 1: build, check, decide (a Tails boot, network ON)

Welcome Screen: **set an administration password** (needed for *Disks*); do not unlock Persistent Storage. Connect
to Tor. No stick and no YubiKey inserted. Open a terminal.

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
Want: the three values above, in that order. (You read both scripts at the rehearsal; these are the same bytes.)
```
python3 formal/freeze-v1/assemble.py --repo . --commit 270ca49 --out /tmp/fz
```
Want, among its lines: `spec.bin 470034 397581f7…` and `catalog.json 662 aaf4306f…`.
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
Want: 14 lines ending `SOURCES PASS: 2 KSKs and 12 pins equal their public sources.` **[PHOTO]**
```
gpg --show-keys docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc
```
Want: one `pub nistp256 2026-11-10 [SC]` line, the fingerprint `CADC 96CF 0023 55F8 E83F  E97F AFF8 0961 D825 035E`,
`uid Tessera release key`, and no `sub` line.

**The fingerprint check.** In Tor Browser open `https://orcid.org/0000-0002-0651-5019`. Compare the release key in
the Biography, the fingerprint on screen, and your **paper ceremony record**: all three must be
`CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E`. **[WRITE]** ORCID = paper = screen: yes / no ________

**Your decision.** Sign only if every Want above held. **[WRITE]** approve release 1, archive hash as written above:
yes / no ________ , time ________

Insert INPUT. In *Disks*: INPUT → *Format Disk* → `+` → *For use with all systems (FAT)*, volume name `INPUT`. Open it
in *Files*. Then:
```
cp /tmp/out/tessera-verifier-v1-1.parts service/verifier/release/release_tool.py docs/ceremony/sign-release.sh /media/amnesia/INPUT/
```
```
cp docs/ceremony/keys/release-CADC96CF002355F8E83FE97FAFF80961D825035E.pub.asc /media/amnesia/INPUT/release.pub.asc
```
```
sha256sum /media/amnesia/INPUT/*
```
Want: the archive, release key (as `release.pub.asc`), `release_tool.py` and `sign-release.sh` values above. Eject
INPUT; shut down.

## Part 2: sign (a new Tails boot, network OFF)

Welcome Screen: **set an administration password**; do not unlock Persistent Storage; **Offline Mode** (networking
disabled). Insert INPUT and OUT, not YubiKey B. In *Disks*: OUT → *Format Disk* → `+` → FAT, volume name `OUT`. Open
both in *Files*. Open a terminal.

**If the script prints FAIL before you touch YubiKey B:** nothing is signed. **[PHOTO]**, shut down, tell the owner.
**If a PIN is refused once:** stop; do not try again; remove YubiKey B, shut down, tell the owner (the retry counter
must never run out). **If it prints FAIL after signing:** nothing reaches OUT; the signature disappears with the
session. **[PHOTO]**, shut down, tell the owner. Never reset the card, whatever fails.

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
It asks you, in order:
1. The `gpg (GnuPG)` and `gpgv (GnuPG)` lines: they must equal the rehearsal's, written above. If not: press
   Ctrl-C, shut down, tell the owner.
2. Three hashes: compare each with this sheet, in full; type `yes`.
3. Eject INPUT in *Files*, remove it, press Enter.
4. After `INSPECT PASS: PRODUCTION release 1` and the key lines: compare the fingerprint with your **paper** and with
   what you wrote from **ORCID**; type `yes`.
5. Insert YubiKey B, press Enter. Want `Serial number ....: 39975596` (or the card's serial line) and the
   `Signature key` line `CADC 96CF …`.
6. The archive hash once more: compare with the eight groups you **[WRITE]**-ed in Part 1; type `yes`.
7. Enter the user PIN; touch YubiKey B when it blinks.
8. Remove YubiKey B, press Enter.

Then it runs to the end. Want: `SIGNATURE PASS: rule O, signer CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E`;
`MUTATION REFUSED (as required)`; the OUT listing with `record.txt` and `tessera-verifier-v1-1.parts.sig` only; and
`==> PASS: sign`. **[PHOTO]** the SIGNATURE PASS line, the OUT hashes and the final PASS. **[WRITE]** the first 8
characters of the `.sig` hash: ________

Eject OUT; remove it; shut down. **End time:** ________

## After

- OUT goes to the owner. YubiKey B goes back to its place, apart from its backup stick and passphrase paper.
- Tell the owner "signed", the `.sig` hash's first 8 characters and the times. The owner checks the signature over
  the NUC's own archive with the release tool, publishes the archive, the signature and the summary, stamps them,
  and writes the bootstrap record.
