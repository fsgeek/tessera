# Key ceremony — operator sheet (one process, run three times)

Final form, top to bottom. The reasoning and review history are in `CEREMONY.md`; you do not need it to run this.

| Run | `L` | YubiKey | Encrypted backup stick | Public stick | Key name |
|---|---|---|---|---|---|
| 1 rehearsal | `REH` | C | `REH-PRIV` | `REH-PUB` | `Tessera REHEARSAL` |
| 2 root | `ROOT` | A | `ROOT-PRIV` | `ROOT-PUB` | `Tessera repository root` |
| 3 release | `REL` | B | `REL-PRIV` | `REL-PUB` | `Tessera release key` |

The stick labels are the author's: what each stick holds (for example "Root: backup (private)" and "Root: public").
The short names in the table are only the **volume names** typed into *Disks* when formatting; the commands find
the stick by that name (`/media/amnesia/ROOT-PRIV`).

Rules: one run per sitting. Network cable out, Wi-Fi off. Only the sticks this sheet names, one at a time. Never
photograph or type into chat a PIN, passphrase or secret key. Each key's passphrase and PINs are its own (run 1:
throwaway). **If anything goes wrong in Part 1, shut down and start Part 1 again; step 2 resets the card.**
Photograph (public output only) the lines marked 📷. Write values marked ✎ on the public sheet.

## Part 1 (one boot)

Tails Welcome Screen: **set an administration password** (needed for formatting); do **not** unlock Persistent
Storage. Open a terminal. Every command runs in this one terminal.

**1. Session** 📷
```
L=ROOT
gpg --version | head -1; ip -brief link; swapon --show
export GNUPGHOME="$(mktemp -d /tmp/gnupg.XXXXXX)"; chmod 700 "$GNUPGHOME"
findmnt -n -o FSTYPE --target "$GNUPGHOME"
```
(`L=` is `REH`, `ROOT` or `REL` from the table.) Want: links other than `lo` DOWN, nothing from `swapon`, last line
`tmpfs`. ✎ the GnuPG version.

**2. Card.** Insert the run's YubiKey only. `gpg --card-status`. ✎ the serial.
- Run 1 (C): reset it: `gpg --card-edit` → `admin` → `factory-reset` → `y` → `yes` → `q`.
- Runs 2–3 (A, B): it must show no keys and PIN retries `3 0 3`. If not, stop.

**3. PINs:** `gpg --card-edit` → `admin` → `passwd` → `3` (admin, default `12345678`) → `1` (user, default
`123456`) → `q` → `q`.

**4. P-256 slot:** `gpg --expert --card-edit` → `admin` → `key-attr` → signature: `2` (ECC), then NIST P-256;
encryption and authentication: keep current → admin PIN → `q`.

**5. Key** (in memory):
```
gpg --expert --full-generate-key
```
`10` (ECC sign only) → NIST P-256 → `0` (no expiry) → the run's key name → email `tessera@wamason.com` → passphrase.
```
gpg --list-keys
FPR=<the 40 characters, no spaces>
gpg --list-keys "$FPR" >/dev/null && echo FPR-OK
```
✎ the fingerprint, then read it back.

**6. Encrypted backup** (`L-PRIV` stick). *Disks* → the stick → ⋮ *Format Disk* (GPT) → `+` → *Internal disk for
use with Linux systems only (Ext4)* → name `ROOT-PRIV` (etc.) → *Password protect volume (LUKS)* → the key's
passphrase. Open it in *Files* (enter the passphrase), then:
```
B="/media/amnesia/$L-PRIV"; DEV="$(findmnt -n -o SOURCE --target "$B")"
[ "$(findmnt -n -o TARGET --target "$B")" = "$B" ] && [ "$(lsblk -no TYPE "$DEV")" = crypt ] && echo LUKS-OK || echo FAIL
sudo cryptsetup status "$DEV" | grep -E 'type|cipher|device'
gpg --export-secret-keys --armor "$FPR" > "$B/secret.asc" && test -s "$B/secret.asc" && echo SECRET-OK || echo FAIL
gpg --export --armor "$FPR" > "$B/public.asc" && test -s "$B/public.asc" && echo PUBLIC-OK || echo FAIL
cp "$GNUPGHOME/openpgp-revocs.d/$FPR.rev" "$B/revocation.rev" && echo REV-OK || echo FAIL
sync
```
Want: `LUKS-OK`, `type: LUKS2` (✎ type and cipher), `SECRET-OK`, `PUBLIC-OK`, `REV-OK`. Now prove it restores, in a
separate keyring, while the key is still in memory:
```
T="$(mktemp -d /tmp/r.XXXXXX)"; chmod 700 "$T"
GNUPGHOME="$T" gpg --batch --import "$B/secret.asc" && echo IMPORTED
echo r > "$T/r.txt"; GNUPGHOME="$T" gpg --local-user "$FPR" --armor --detach-sign "$T/r.txt" && GNUPGHOME="$T" gpg --verify "$T/r.txt.asc" "$T/r.txt" && echo RESTORE-OK
gpgconf --homedir "$T" --kill gpg-agent; rm -rf "$T"
```
Want: `IMPORTED`, `RESTORE-OK`. If not, do not go on: format the stick again and redo step 6. Eject in *Files*;
remove the stick.

**7. Public stick** (`L-PUB` stick). *Disks* → ⋮ *Format Disk* (GPT) → `+` → *For use with all systems (FAT)*,
name `ROOT-PUB` (etc.), no password. Open it in *Files*, then:
```
O="/media/amnesia/$L-PUB"
[ "$(findmnt -n -o TARGET --target "$O")" = "$O" ] && echo PUB-OK || echo FAIL
gpg --export --armor "$FPR" > "$O/key.pub.asc" && sha256sum "$O/key.pub.asc"
```
Want: `PUB-OK` and a hash (✎ the hash). Leave the stick in.

**8. Onto the card** (only after `RESTORE-OK` in step 6):
```
gpg --edit-key "$FPR"
```
`keytocard` → `y` → `1` → passphrase → admin PIN → `save`. Then `gpg --card-status`: the signature key line shows
your fingerprint.

**9. Card policy** 📷 (the last command's output)
```
gpg --card-edit
```
`admin` → `forcesig` → `uif 1 permanent` → `q`. (Run `forcesig` only once: it toggles.)
```
gpg --card-status | grep 'Signature PIN'
gpg-connect-agent 'SCD GETATTR UIF-1' /bye
```
Want: `Signature PIN ....: forced`, then exactly `S UIF-1 %02+` and `OK`. Anything else: stop.

**10. Signing tests** 📷
```
echo "tessera $L $(date -u +%FT%TZ)" > ~/proof.txt
gpg --local-user "$FPR" --armor --detach-sign ~/proof.txt && gpg --verify ~/proof.txt.asc ~/proof.txt && echo PROOF-OK
```
User PIN, then **touch when the key blinks** (no prompt says so). Want `PROOF-OK`.
```
rm -f ~/nt.asc; gpg --local-user "$FPR" --armor --output ~/nt.asc --detach-sign ~/proof.txt; test -s ~/nt.asc && echo SIGNED-WITHOUT-TOUCH || echo NO-SIGNATURE-OK
```
User PIN, **do not touch**, wait for the error. Want `NO-SIGNATURE-OK`.
```
cp ~/proof.txt ~/proof.txt.asc "$O/" && sync && echo PROOF-COPIED
```
Eject the public stick. Remove it.

**11. Shut down.** Remove the YubiKey.

## Part 2 (a new boot: proves the card and the backup each work alone)

Welcome Screen as before. Then:
```
L=ROOT
FPR=<the fingerprint from the sheet>
export GNUPGHOME="$(mktemp -d /tmp/gnupg.XXXXXX)"; chmod 700 "$GNUPGHOME"
```
**12. Card alone.** Insert the YubiKey and the `L-PRIV` stick (open it in *Files*):
```
B="/media/amnesia/$L-PRIV"
gpg --import "$B/public.asc" && gpg --card-status > /dev/null
echo c > ~/c.txt; gpg --local-user "$FPR" --armor --detach-sign ~/c.txt && gpg --verify ~/c.txt.asc ~/c.txt && echo CARD-OK
```
PIN, touch. Want `CARD-OK`. Remove the YubiKey.

**13. Backup alone** (same boot, after step 12):
```
gpg --batch --import "$B/secret.asc"
echo b > ~/b.txt; gpg --local-user "$FPR" --armor --detach-sign ~/b.txt && gpg --verify ~/b.txt.asc ~/b.txt && echo BACKUP-OK
```
Passphrase. Want `BACKUP-OK`. Eject; shut down.

## After each run
- **Run 1:** reset C (as in step 2). Keep `REH-PUB` for the owner if you like; `REH-PRIV` can be reformatted.
- **Runs 2–3:** the YubiKey and its `L-PRIV` stick go to **different places**; the passphrase paper to a third.
  A's and B's things are not stored together. Tell the owner only "done". The `L-PUB` stick goes to the owner, who
  checks the key and proof with the verifier and writes the custody record. It never returns to a signing session.
- If step 6's restore, step 9's readback or step 10's no-touch test fails: the key is **not** used. Bring the
  photos to the owner. If step 12 fails but 13 passes (or the reverse): keep everything, reset nothing, and ask.
