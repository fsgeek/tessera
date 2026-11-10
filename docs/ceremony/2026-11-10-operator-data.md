# Key Creation Data

Captured via pictures, added here for recording; discrepancies should be resolved by reviewing pictures, not by assuming this text is correct.

Suggestion: Having three words with the same 1-2 letters is cognitively challenging for the human.  Recommendation: Test, Root, Deploy

Suggestion: in Step

## Summary (owner, 2026-11-10, from the photos; each value cites its photo in `tmp/ceremony/`)

Values were read from the photos by a helper agent and checked by the owner where independent evidence exists (the
two production fingerprints, from the public sticks themselves; the swap finding, from 12.01.51). Times in photo
names are local; screen clocks show GMT. Photo SHA-256 manifest: `2026-11-10-photos.SHA256SUMS`.

| | Root (YubiKey A) | Release (YubiKey B) | Rehearsal (YubiKey C, final run) |
|---|---|---|---|
| GnuPG / scdaemon | 2.4.7 / 2.4.7 (12.01.51) | 2.4.7 / 2.4.7 (13.03.54) | 2.4.7 / 2.4.7 (09.47.42) |
| Hardware network interfaces | none (12.01.51) | none (13.03.54) | none (10.55.00) |
| Default route | none (12.01.51) | none (13.03.54) | none (10.55.00) |
| YubiKey serial | **39975687** (12.01.51) | **39975596** (13.04.51) | 39975816 |
| Card before | empty, PIN retries 3 0 3, rsa2048 ×3, UIF off (12.01.51) | same (13.04.51) | — |
| Key attributes | nistp256 ×3, PASS (12.04.10) | nistp256 ×3, PASS (13.07.17) | nistp256 ×3 |
| Fingerprint | **6BDA 2155 9F18 D5DB 8E13 12C3 6321 0B5F F92A D30A** (12.04.10 … 12.46.56); matches the key received on ROOT-PUB | **CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E** (13.07.17 … 13.15.32); matches REL-PUB | 5FEB C5A5 … 9F29 D60F (throwaway) |
| Backup (LUKS) | LUKS2, aes-xts-plain64, /dev/sdb1; written and restored, PASS (12.09.57; first attempt FAIL before unlock) | LUKS2, aes-xts-plain64, /dev/sdb1; PASS (13.10.50) | LUKS2, PASS |
| Signature PIN / touch | forced / `S UIF-1 %02+`, PASS (12.38.14) | forced / `S UIF-1 %02+`, PASS (13.15.32) | forced / `%02+` |
| No-touch test | `gpg: signing failed: Timeout`, exit=2, PASS (12.46.56) | same, PASS (13.15.32; first attempt `Bad PIN`, rerun passed) | same, PASS (11.46.31) |
| Public key received (owner, NUC) | `key.pub.asc` SHA-256 `001565af5b4bd9bc…` | `key.pub.asc` SHA-256 `1a817ae39f974501…` | not brought |
| Proof verified by the verifier's code | yes; tampered copy fails | yes; tampered copy fails | — |
| Part 2 `verify` | **not photographed: open** | **not photographed: open** | — |

### Findings for the record
- **Swap check was hollow.** `swapon: command not found` for the user (every `start`), so the script's check
  passed vacuously. The author ran `sudo swapon` by hand (12.01.51): `/dev/zram0`, 62.2G, 0B used. zram is
  RAM-backed, so secrets did not reach a disk. Fixed in the script for future runs (`/proc/swaps`, zram only).
- **Network check:** the first run failed on Tails' internal `veth-*` links (09.47.42); fixed (commit `c4de168`).
- **Rehearsal runs named REL:** while learning the flow, rehearsal runs on card C generated two other keys named
  "Tessera release key": `0B22 AC78 5B0A CFD7 DD2C BFAB 5117 0613 8025 093E` (10.35.01) and
  `F00E C3CB 6C3F 8DEB 55B6 7818 7AA5 7263 C70C 21B1` (11.22.35; read from notes, not re-checked). They are
  **throwaway and must never be mistaken for the release key**. The production release key is `CADC…035E`.
- `card` printed "card is empty" on a partly reconfigured card (nistp256 rsa2048 rsa2048, 10.25.23): harmless, since
  no key was present, but the check reads "no key" rather than "factory state".
- REL `tests`: two `Bad PIN` before the passing rerun (13.15.32). A later correct PIN resets the user-PIN counter.
- The script's SHA-256 was verified in every offline session: `2602c0e0…9daeb07d` (10.22.18, 10.23.24, 11.58.58,
  13.03.54).

### Open (author)
1. Was Part 2 (`verify`) run for Root and Release, and did each print PASS?
2. The step-7 hashes on the public sheet for Root and Release: do they equal `001565af…` and `1a817ae3…`?
3. Any stick or card still holding a rehearsal key (especially the two named "Tessera release key") reformatted or
   reset? YubiKey C reset?
4. Storage: each YubiKey, its backup stick and its passphrase paper in different places; A's and B's not together.

# Pictures


![2026-11-10_09.43.21.jpg](../../tmp/ceremony/2026-11-10_09.43.21.jpg)

![2026-11-10_13.07.17.jpg](../../tmp/ceremony/2026-11-10_13.07.17.jpg)

![2026-11-10_13.15.32.jpg](../../tmp/ceremony/2026-11-10_13.15.32.jpg)

![2026-11-10_12.01.51.jpg](../../tmp/ceremony/2026-11-10_12.01.51.jpg)

![2026-11-10_11.46.31.jpg](../../tmp/ceremony/2026-11-10_11.46.31.jpg)

![2026-11-10_12.04.10.jpg](../../tmp/ceremony/2026-11-10_12.04.10.jpg)

![2026-11-10_10.35.01.jpg](../../tmp/ceremony/2026-11-10_10.35.01.jpg)

![2026-11-10_13.03.54.jpg](../../tmp/ceremony/2026-11-10_13.03.54.jpg)

![2026-11-10_11.06.13.jpg](../../tmp/ceremony/2026-11-10_11.06.13.jpg)

![2026-11-10_10.54.05.jpg](../../tmp/ceremony/2026-11-10_10.54.05.jpg)

![2026-11-10_12.38.14.jpg](../../tmp/ceremony/2026-11-10_12.38.14.jpg)

![2026-11-10_12.25.01.jpg](../../tmp/ceremony/2026-11-10_12.25.01.jpg)

![2026-11-10_10.23.24.jpg](../../tmp/ceremony/2026-11-10_10.23.24.jpg)

![2026-11-10_11.03.11.jpg](../../tmp/ceremony/2026-11-10_11.03.11.jpg)

![2026-11-10_09.47.42.jpg](../../tmp/ceremony/2026-11-10_09.47.42.jpg)

![2026-11-10_10.25.23.jpg](../../tmp/ceremony/2026-11-10_10.25.23.jpg)

![2026-11-10_11.20.11.jpg](../../tmp/ceremony/2026-11-10_11.20.11.jpg)

![2026-11-10_10.38.10.jpg](../../tmp/ceremony/2026-11-10_10.38.10.jpg)

![2026-11-10_11.17.13.jpg](../../tmp/ceremony/2026-11-10_11.17.13.jpg)

![2026-11-10_13.10.50.jpg](../../tmp/ceremony/2026-11-10_13.10.50.jpg)

![2026-11-10_11.42.35.jpg](../../tmp/ceremony/2026-11-10_11.42.35.jpg)

![2026-11-10_11.18.57.jpg](../../tmp/ceremony/2026-11-10_11.18.57.jpg)

![2026-11-10_10.24.27.jpg](../../tmp/ceremony/2026-11-10_10.24.27.jpg)

![2026-11-10_11.58.58.jpg](../../tmp/ceremony/2026-11-10_11.58.58.jpg)

![2026-11-10_09.32.08.jpg](../../tmp/ceremony/2026-11-10_09.32.08.jpg)

![2026-11-10_10.22.18.jpg](../../tmp/ceremony/2026-11-10_10.22.18.jpg)

![2026-11-10_10.57.40.jpg](../../tmp/ceremony/2026-11-10_10.57.40.jpg)

![2026-11-10_12.46.56.jpg](../../tmp/ceremony/2026-11-10_12.46.56.jpg)

![2026-11-10_10.25.07.jpg](../../tmp/ceremony/2026-11-10_10.25.07.jpg)

![2026-11-10_13.04.51.jpg](../../tmp/ceremony/2026-11-10_13.04.51.jpg)

![2026-11-10_11.27.51.jpg](../../tmp/ceremony/2026-11-10_11.27.51.jpg)

![2026-11-10_11.07.32.jpg](../../tmp/ceremony/2026-11-10_11.07.32.jpg)

![2026-11-10_11.37.28.jpg](../../tmp/ceremony/2026-11-10_11.37.28.jpg)

![2026-11-10_10.14.38.jpg](../../tmp/ceremony/2026-11-10_10.14.38.jpg)

![2026-11-10_11.30.01.jpg](../../tmp/ceremony/2026-11-10_11.30.01.jpg)

![2026-11-10_11.45.12.jpg](../../tmp/ceremony/2026-11-10_11.45.12.jpg)

![2026-11-10_10.59.10.jpg](../../tmp/ceremony/2026-11-10_10.59.10.jpg)

![2026-11-10_09.44.22.jpg](../../tmp/ceremony/2026-11-10_09.44.22.jpg)

![2026-11-10_12.09.57.jpg](../../tmp/ceremony/2026-11-10_12.09.57.jpg)

![2026-11-10_11.18.29.jpg](../../tmp/ceremony/2026-11-10_11.18.29.jpg)

![2026-11-10_11.22.35.jpg](../../tmp/ceremony/2026-11-10_11.22.35.jpg)

![2026-11-10_10.55.00.jpg](../../tmp/ceremony/2026-11-10_10.55.00.jpg)

![2026-11-10_10.15.53.jpg](../../tmp/ceremony/2026-11-10_10.15.53.jpg)

![2026-11-10_11.21.25.jpg](../../tmp/ceremony/2026-11-10_11.21.25.jpg)
