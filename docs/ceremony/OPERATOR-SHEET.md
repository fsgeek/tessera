# Key ceremony — operator sheet (one process, run three times)

The reasoning and review history are in `CEREMONY.md`. The steps are done by `tessera-ceremony.sh`, which you read
before running. Every command you type is on its own line: type one, press Enter, read the result, then the next.

| Run | `L` | YubiKey | Encrypted backup stick | Public stick |
|---|---|---|---|---|
| 1 rehearsal | `REH` | C | volume name `REH-PRIV` | volume name `REH-PUB` |
| 2 root | `ROOT` | A | `ROOT-PRIV` | `ROOT-PUB` |
| 3 release | `REL` | B | `REL-PRIV` | `REL-PUB` |

Stick labels are yours (what each holds). The short names are only the **volume names** typed into *Disks*.
The script reaches you on the **INPUT** stick: a new stick that has **never** been in the NUC, written by the
Pangolin in a separate, networked Tails session (below). The NUC is not in the path.

**If a step prints FAIL**, nothing has been deleted: fix what it says and run the same step again. Never reboot
between `generate` and `tests` unless the owner says so: the key is in memory until it is on the card and backed up.
Never photograph or type into chat a PIN or passphrase. **[PHOTO]** = photograph the screen. **[WRITE]** = write on the public sheet.

## Before the session: write the INPUT stick (a separate Tails boot, network ON)

On the Pangolin, boot Tails **with** networking (it connects through Tor). No YubiKey, no other stick inserted.
When Tor is connected, open a terminal:
```
git clone https://github.com/fsgeek/tessera.git
```
```
cd tessera
```
```
git checkout <the commit the owner names>
```
```
sha256sum docs/ceremony/tessera-ceremony.sh
```
It must equal the owner's hash. **[WRITE]** it, in groups of 8. *(If `git` is not found: in Tor Browser open
`https://raw.githubusercontent.com/fsgeek/tessera/<commit>/docs/ceremony/tessera-ceremony.sh`, save it to the
Tor Browser folder, and run `sha256sum` on the saved file instead; then copy that file in the step below.)*
Insert the new INPUT stick; in *Disks*, format it (FAT,
volume name `INPUT`); open it in *Files*; then:
```
cp docs/ceremony/tessera-ceremony.sh /media/amnesia/INPUT/
```
```
sha256sum /media/amnesia/INPUT/tessera-ceremony.sh
```
Same hash. Eject; shut down. This session is amnesic: nothing from it persists except the INPUT stick.

## Part 1 (one boot)

Welcome Screen: **set an administration password**; do **not** unlock Persistent Storage. Network off.
Insert the INPUT stick, open it in *Files*, open a terminal.

**0. Check and read the script**
```
sha256sum /media/amnesia/INPUT/tessera-ceremony.sh
```
It must equal the paper. Then read it (space pages, q quits):
```
less /media/amnesia/INPUT/tessera-ceremony.sh
```
Copy it into memory:
```
cp /media/amnesia/INPUT/tessera-ceremony.sh /tmp/c.sh
```
```
sha256sum /tmp/c.sh
```
Same hash again. Eject INPUT and remove it. From here on, every step is `bash /tmp/c.sh <step>`.

**1. Start** **[PHOTO]** **[WRITE]** GnuPG version
```
bash /tmp/c.sh start ROOT
```
(`REH`, `ROOT` or `REL`.)

**2. Card** — insert the run's YubiKey only. **[WRITE]** serial.
```
bash /tmp/c.sh card
```

**3. PINs** — the script shows what to type.
```
bash /tmp/c.sh pins
```

**4. P-256 slot**
```
bash /tmp/c.sh slot
```

**5. Generate** — enter the passphrase twice when asked. **[WRITE]** the fingerprint, then read it back.
```
bash /tmp/c.sh generate
```

**6. Backup** — first, in *Disks*: the `L-PRIV` stick → ⋮ *Format Disk* (GPT) → `+` → *Internal disk for use with
Linux systems only (Ext4)*, volume name `ROOT-PRIV` (etc.), *Password protect volume (LUKS)*, the key's passphrase.
Open it in *Files*. Then: **[WRITE]** LUKS type and cipher.
```
bash /tmp/c.sh backup
```
It asks for the passphrase once more (the restore test). On PASS, eject `L-PRIV` and remove it.

**7. Public stick** — in *Disks*: the `L-PUB` stick → *Format Disk* (GPT) → `+` → *For use with all systems (FAT)*,
volume name `ROOT-PUB` (etc.), no password. Open it in *Files*. Then: **[WRITE]** the hash.
```
bash /tmp/c.sh public
```
Leave it in.

**8. Onto the card** — the script shows what to type.
```
bash /tmp/c.sh tocard
```

**9. Policy** **[PHOTO]** (the `S UIF-1` line)
```
bash /tmp/c.sh policy
```

**10. Tests** **[PHOTO]** — the first signature needs a touch; the second must not be touched. **[WRITE]** the error text.
```
bash /tmp/c.sh tests
```

**11. Check the public stick yourself** (typed by hand, not by the script). **[PHOTO]**
```
ls -la /media/amnesia/ROOT-PUB
```
Want: `key.pub.asc`, `proof.txt`, `proof.txt.asc`, nothing else.
```
gpg --show-keys /media/amnesia/ROOT-PUB/key.pub.asc
```
Want: a line starting `pub` and **no line starting `sec`**, and your fingerprint. Then eject, remove, shut down.

## Part 2 (a new boot)

Welcome Screen as before. INPUT stick: repeat step 0 (check, read, copy to `/tmp/c.sh`). Open `L-PRIV` in *Files*
(passphrase). Have the YubiKey ready but not inserted.
```
bash /tmp/c.sh verify ROOT
```
Type the fingerprint from the sheet; insert the YubiKey when asked; PIN and touch; remove it when asked; then the
passphrase for the backup. Want PASS. Eject; shut down.

## After each run

- **Run 1:** reset C (`gpg --card-edit`, then `admin`, `factory-reset`, `y`, `yes`, `q`).
- **Runs 2–3:** the YubiKey and its `L-PRIV` stick go to **different places**; the passphrase paper to a third.
  A's and B's things are not stored together. Tell the owner only "done". The `L-PUB` stick goes to the owner and
  never returns to a signing session.
- **From step 8 on, never reset the card**, whatever fails. Keep the card and the backup and bring the photos.
