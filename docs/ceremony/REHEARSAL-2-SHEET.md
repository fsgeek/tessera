# Rehearsal 2 — one page (YubiKey C, throwaway key, no USB sticks)

Purpose: check that the card's touch policy reads back as permanent, and that signing without a touch fails.
Welcome Screen: defaults are fine (no admin password needed, do not unlock Persistent Storage). Network off.
Throwaway PINs and passphrase. Never photograph a PIN or passphrase. Photograph steps 1, 6 and 7 only.

**1. Session check** (photo)
```
gpg --version | head -1
export GNUPGHOME="$(mktemp -d /tmp/gnupg.XXXXXX)"; chmod 700 "$GNUPGHOME"
findmnt -n -o FSTYPE --target "$GNUPGHOME"
```
Last line must print `tmpfs`.

**2. Reset C** (start clean): `gpg --card-edit` → `admin` → `factory-reset` → `y` → `yes` → `q`

**3. PINs:** `gpg --card-edit` → `admin` → `passwd` → `3` (admin, default 12345678) → `1` (user, default 123456) → `q` → `q`

**4. P-256 slot:** `gpg --expert --card-edit` → `admin` → `key-attr` → signature: `2` (ECC), then the NIST P-256
number; encryption and authentication: keep current → admin PIN → `q`

**5. Key, then onto the card:**
```
gpg --expert --full-generate-key
```
`10`, NIST P-256 number, `0`, name `Rehearsal 2`, email `tessera@wamason.com`, passphrase. Then:
```
gpg --list-keys
```
Copy the 40-character fingerprint into the next line (no spaces):
```
FPR=
gpg --edit-key "$FPR"
```
`keytocard` → `y` → `1` → passphrase → admin PIN → `save`

**6. Policy and readback** (photo of the last command's output)
```
gpg --card-edit
```
`admin` → `forcesig` → `uif 1 permanent` → `q`
```
gpg --card-status | grep 'Signature PIN'
gpg-connect-agent 'SCD GETATTR UIF-1' /bye
```
Want: `Signature PIN ....: forced`, then `S UIF-1 %02+` and `OK`.

**7. Signing without a touch must fail** (photo)
```
echo test > ~/t.txt; rm -f ~/nt.asc
gpg --local-user "$FPR" --armor --output ~/nt.asc --detach-sign ~/t.txt; test -s ~/nt.asc && echo SIGNED-WITHOUT-TOUCH || echo NO-SIGNATURE-OK
```
Enter the user PIN. **Do not touch** the key; wait for the error. Want: `NO-SIGNATURE-OK`.

**8. Reset C** (as step 2), then shut down.

If a step goes wrong: reboot Tails and start again at step 1. Step 2 resets the card.
