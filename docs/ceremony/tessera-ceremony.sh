#!/usr/bin/env bash
# Tessera key ceremony step runner (owner, 2026-11-06). Run on an offline Tails session, one step at a time:
#   bash /media/amnesia/INPUT/tessera-ceremony.sh <step>
# Part 1 (one boot):  start REH|ROOT|REL, card, pins, slot, generate, backup, public, tocard, policy, tests
# Part 2 (new boot):  verify REH|ROOT|REL
# Every step ends with PASS or FAIL. A FAIL never deletes anything: fix the cause and run the same step again.
# State (run name, keyring path, fingerprint) is kept in /tmp/tessera-ceremony.env, in RAM.
# Secret key material exists only in RAM keyrings under /tmp (tmpfs) and on the LUKS backup volume; the public
# stick receives only key.pub.asc, proof.txt and proof.txt.asc. Read it before running it: that, not the checksum, is what protects against a bad script.
set -u
export LC_ALL=C LANG=C
STATE=/tmp/tessera-ceremony.env
EMAIL=tessera@wamason.com

pass() { printf '\n==> PASS: %s\n\n' "$*"; exit 0; }
fail() { printf '\n==> FAIL: %s\n    Nothing was deleted. Fix the cause and run this step again.\n\n' "$*"; exit 1; }
say()  { printf '\n%s\n' "$*"; }
load() { [ -f "$STATE" ] || fail "no state: run 'start' first (Part 1) or 'verify' (Part 2)"; . "$STATE"; export GNUPGHOME; }
save() { printf 'L=%q\nGNUPGHOME=%q\nFPR=%q\nRESTORE_OK=%q\n' "$L" "$GNUPGHOME" "${FPR:-}" "${RESTORE_OK:-0}" > "$STATE" || fail "could not save state to $STATE"; }
keyname() { case "$1" in REH) echo "Tessera REHEARSAL";; ROOT) echo "Tessera repository root";; REL) echo "Tessera release key";; esac; }
mounted_at() { [ "$(findmnt -n -o TARGET --target "$1" 2>/dev/null)" = "$1" ]; }
card_fpr() { gpg --with-colons --card-status 2>/dev/null | awk -F: '$1=="fpr"{print toupper($2)}'; }

step_start() {
  case "${1:-}" in REH|ROOT|REL) L=$1;; *) fail "usage: start REH|ROOT|REL";; esac
  [ -f "$STATE" ] && fail "a run is already in progress ($STATE exists). Reboot to start over."
  say "Versions:"; gpg --version | head -1; /usr/lib/gnupg/scdaemon --version 2>/dev/null | head -1
  # Only hardware interfaces count (they have a /sys/class/net/<if>/device link). Tails' own veth-* links are
  # virtual: they join its internal compartments (Tor, OnionShare, ...) and reach no hardware (author's run 1).
  say "Hardware network interfaces (each must be DOWN, or none at all):"
  hw_up=0
  for i in /sys/class/net/*; do
    [ -e "$i/device" ] || continue
    n=$(basename "$i"); st=$(cat "$i/operstate" 2>/dev/null); echo "  $n: $st"
    [ "$st" = down ] || hw_up=1
  done
  [ "$hw_up" -eq 0 ] || fail "a hardware network interface is not down (cable or Wi-Fi?)"
  say "Routes to the outside (must be none):"; ip route show default; ip -6 route show default
  [ -z "$(ip route show default)$(ip -6 route show default)" ] || fail "a default route exists"
  # swapon is not on an ordinary user's PATH on Tails (found 2026-11-10: the old check passed vacuously); read the
  # kernel's list instead. zram (compressed RAM) is allowed: it never reaches a disk.
  say "Swap devices (only zram allowed):"; cat /proc/swaps
  nonzram=$(awk 'NR>1 && $1 !~ /^\/dev\/zram/' /proc/swaps | wc -l); [ "$nonzram" -eq 0 ] || fail "a swap device other than zram is active"
  GNUPGHOME=$(mktemp -d /tmp/gnupg.XXXXXX); chmod 700 "$GNUPGHOME"; export GNUPGHOME
  fs=$(findmnt -n -o FSTYPE --target "$GNUPGHOME"); echo "keyring filesystem: $fs"
  [ "$fs" = tmpfs ] || fail "keyring is not on tmpfs"
  FPR=""; RESTORE_OK=0; save
  pass "session ready for run $L. Write the GnuPG version on the public sheet."
}

step_card() {
  load
  say "Card status:"; gpg --card-status || fail "no card found: insert the run's YubiKey"
  say "Write the serial number on the public sheet."
  if [ -n "$(card_fpr)" ]; then
    [ -n "$FPR" ] && [ "$(card_fpr)" = "$FPR" ] && fail "the card holds THIS run's key. Do not reset it. Continue with the next step, or ask the owner"
    if [ "$L" = REH ]; then
      say "The rehearsal card (C) holds a key. Reset it: gpg --card-edit, then: admin, factory-reset, y, yes, q"
      say "Then run this step again."; exit 1
    fi
    fail "this card already holds a key. Runs ROOT and REL need an empty card. Stop and ask the owner."
  fi
  pass "card is empty"
}

step_pins() {
  load
  say "Type, in order:  admin   passwd   3   (admin PIN: old 12345678, then the new one twice)"
  say "                 1   (user PIN: old 123456, then the new one twice)   q   q"
  gpg --card-edit
  pass "PINs done (if gpg reported an error, run this step again)"
}

step_slot() {
  load
  say "Type, in order:  admin   key-attr"
  say "  gpg asks three times (signature, encryption, authentication key)."
  say "  Each time: 2 (ECC), then the number shown for NIST P-256. The admin PIN when asked. Then q"
  gpg --expert --card-edit
  attrs=$(gpg --card-status | awk -F': ' '/^Key attributes/{print $2}'); echo "Key attributes: $attrs"
  [ "$attrs" = "nistp256 nistp256 nistp256" ] || fail "all three key attributes must be nistp256 (run 'slot' again)"
  pass "all three slots are NIST P-256"
}

step_generate() {
  load
  [ -z "$FPR" ] || fail "a key was already generated in this run ($FPR)"
  [ -z "$(gpg --with-colons --list-secret-keys 2>/dev/null)" ] || fail "the keyring already holds a key (a failed earlier attempt?). Ask the owner; do not generate another"
  name="$(keyname "$L")"
  say "Generating '$name <$EMAIL>': NIST P-256, sign only, no expiry. Enter the passphrase when asked."
  gpg --quick-generate-key "$name <$EMAIL>" nistp256 sign never || fail "key generation failed"
  FPR=$(gpg --with-colons --list-secret-keys | awk -F: '$1=="fpr"{print $10; exit}')
  [ ${#FPR} -eq 40 ] || fail "could not read the new fingerprint"
  save
  say "Fingerprint (write it on the public sheet, then read it back):"
  echo "$FPR" | sed 's/.\{4\}/& /g'
  pass "key generated"
}

step_backup() {
  load
  [ -n "$FPR" ] || fail "no key yet: run 'generate'"
  [ "$(card_fpr)" = "$FPR" ] && fail "the key is already on the card: a backup can no longer be made (it would be a card stub)"
  [ "$RESTORE_OK" = 1 ] && fail "the backup already passed its restore test; it is not rewritten"
  B="/media/amnesia/$L-PRIV"
  mounted_at "$B" || fail "$B is not mounted. Format the stick in Disks (Ext4, LUKS, volume name $L-PRIV), then open it in Files"
  DEV=$(findmnt -n -o SOURCE --target "$B")
  [ "$(lsblk -no TYPE "$DEV")" = crypt ] || fail "$B is not an encrypted (LUKS) volume"
  say "LUKS (write type and cipher on the public sheet):"; sudo cryptsetup status "$DEV" | grep -E 'type|cipher|device'
  sudo cryptsetup status "$DEV" | grep -q 'type: *LUKS2' || fail "volume is not LUKS2"
  [ -e "$B/secret.asc" ] && fail "$B/secret.asc already exists. If it came from a failed attempt in THIS session, format the stick again in Disks and rerun"
  gpg --export-secret-keys --armor "$FPR" > "$B/secret.asc" || fail "secret export failed"
  [ -s "$B/secret.asc" ] || fail "secret.asc is empty"
  gpg --export --armor "$FPR" > "$B/public.asc" || fail "public export failed"
  cp "$GNUPGHOME/openpgp-revocs.d/$FPR.rev" "$B/revocation.rev" || fail "revocation certificate copy failed"
  sync || fail "sync failed"
  say "Restore test, in a separate keyring (enter the passphrase when asked):"
  T=$(mktemp -d /tmp/restore.XXXXXX) && [ -d "$T" ] || fail "could not make the restore keyring"; chmod 700 "$T"
  GNUPGHOME="$T" gpg --batch --import "$B/secret.asc" || { rm -rf "$T"; fail "backup did not import"; }
  echo restore > "$T/r.txt"
  GNUPGHOME="$T" gpg --local-user "$FPR" --armor --detach-sign "$T/r.txt" || { rm -rf "$T"; fail "backup did not sign"; }
  GNUPGHOME="$T" gpg --verify "$T/r.txt.asc" "$T/r.txt" || { rm -rf "$T"; fail "backup signature did not verify"; }
  gpgconf --homedir "$T" --kill gpg-agent; rm -rf "$T"
  RESTORE_OK=1; save
  ls -l "$B"
  pass "backup written and restored. Eject $L-PRIV in Files and remove it."
}

step_public() {
  load
  [ -n "$FPR" ] || fail "no key yet"
  O="/media/amnesia/$L-PUB"
  mounted_at "$O" || fail "$O is not mounted. Format the stick in Disks (FAT, no password, volume name $L-PUB), then open it in Files"
  gpg --export --armor "$FPR" > "$O/key.pub.asc" || fail "public export failed"
  sync || fail "sync failed"
  say "SHA-256 of the public key (write it on the public sheet):"; sha256sum "$O/key.pub.asc" || fail "could not hash the public key"
  pass "public key written. Leave $L-PUB in."
}

step_tocard() {
  load
  [ "$RESTORE_OK" = 1 ] || fail "the backup has not passed its restore test: run 'backup' first"
  say "Type, in order:  keytocard   y   1   (passphrase, then admin PIN)   save"
  gpg --edit-key "$FPR"
  [ "$(card_fpr)" = "$FPR" ] || fail "the card does not show the key. From here on: never reset the card; ask the owner"
  pass "key is on the card"
}

step_policy() {
  load
  [ "$(card_fpr)" = "$FPR" ] || fail "the card does not hold this run's key"
  say "Type, in order:  admin   uif 1 permanent   q"
  gpg --card-edit
  if gpg --card-status | grep 'Signature PIN' | grep -q 'not forced'; then
    say "Signature PIN is not forced. Type, in order:  admin   forcesig   q"
    gpg --card-edit
  fi
  pin=$(gpg --card-status | grep 'Signature PIN'); echo "$pin"
  echo "$pin" | grep -Eq 'Signature PIN[ .]*: forced$' || fail "signature PIN is not shown as forced"
  say "Raw touch policy (photograph this):"
  out=$(gpg-connect-agent 'SCD GETATTR UIF-1' /bye); echo "$out"
  echo "$out" | grep -qx 'S UIF-1 %02+' || fail "touch policy is not permanent (want 'S UIF-1 %02+')"
  pass "PIN forced and touch permanent"
}

step_tests() {
  load
  O="/media/amnesia/$L-PUB"; mounted_at "$O" || fail "$O is not mounted"
  echo "tessera $L $(date -u +%FT%TZ)" > ~/proof.txt
  say "Test 1: sign. Enter the user PIN, then TOUCH the key when it blinks."
  gpg --local-user "$FPR" --armor --yes --detach-sign ~/proof.txt || fail "signing failed"
  gpg --verify ~/proof.txt.asc ~/proof.txt || fail "proof does not verify"
  say "Test 2: enter the correct user PIN, then do NOT touch the key. Wait for the error."
  rm -f ~/nt.asc
  gpg --local-user "$FPR" --armor --output ~/nt.asc --detach-sign ~/proof.txt 2> ~/nt.err; rc=$?
  cat ~/nt.err; echo "exit=$rc"
  [ "$rc" -ne 0 ] || fail "signing succeeded without a touch"
  [ -s ~/nt.asc ] && fail "a signature was written without a touch"
  grep -q 'signing failed: Timeout' ~/nt.err || fail "the error was not the card's touch timeout ('signing failed: Timeout'); a wrong or cancelled PIN does not count: run 'tests' again"
  cp ~/proof.txt ~/proof.txt.asc "$O/" || fail "could not copy the proof"
  sync || fail "sync failed"
  pass "touch is enforced. Write the error text above on the public sheet. Eject $L-PUB, then shut down."
}

step_verify() {
  case "${1:-}" in REH|ROOT|REL) L=$1;; *) fail "usage: verify REH|ROOT|REL";; esac
  [ -f "$STATE" ] && fail "state exists: this must be a fresh boot"
  GNUPGHOME=$(mktemp -d /tmp/gnupg.XXXXXX) && [ -d "$GNUPGHOME" ] || fail "could not make the keyring"; chmod 700 "$GNUPGHOME"; export GNUPGHOME
  [ "$(findmnt -n -o FSTYPE --target "$GNUPGHOME")" = tmpfs ] || fail "keyring is not on tmpfs"
  printf 'Type the fingerprint from the public sheet (spaces allowed): '; read -r typed
  FPR=$(echo "$typed" | tr -d ' ' | tr a-f A-F)
  [ ${#FPR} -eq 40 ] || fail "that is not 40 characters"
  B="/media/amnesia/$L-PRIV"; mounted_at "$B" || fail "open $L-PRIV in Files first (passphrase)"
  gpg --import "$B/public.asc" || fail "public key import failed"
  gpg --with-colons --list-keys "$FPR" >/dev/null 2>&1 || fail "the backup's public key does not match the typed fingerprint"
  say "Card test: insert the YubiKey now, then press Enter."; read -r _
  gpg --card-status >/dev/null || fail "no card"
  say "Enter the user PIN, then touch the key when it blinks."
  echo card > ~/c.txt
  gpg --local-user "$FPR" --armor --yes --detach-sign ~/c.txt || fail "the card did not sign"
  gpg --verify ~/c.txt.asc ~/c.txt || fail "card signature does not verify"
  say "CARD-OK. Remove the YubiKey now, then press Enter."; read -r _
  gpg --card-status >/dev/null 2>&1 && fail "the YubiKey is still inserted: remove it and run 'verify' again in a new boot"
  gpg --batch --import "$B/secret.asc" || fail "backup did not import"
  gpg --with-colons --list-secret-keys "$FPR" | awk -F: '$1=="sec"{print $15}' | grep -qE '^(D27600|#)' && fail "the backup holds only a card stub, not the key"
  echo backup > ~/b.txt
  gpg --local-user "$FPR" --armor --yes --detach-sign ~/b.txt || fail "the backup did not sign"
  gpg --verify ~/b.txt.asc ~/b.txt || fail "backup signature does not verify"
  pass "card and backup each work alone. Eject $L-PRIV and shut down."
}

case "${1:-}" in
  start) step_start "${2:-}";; card) step_card;; pins) step_pins;; slot) step_slot;;
  generate) step_generate;; backup) step_backup;; public) step_public;; tocard) step_tocard;;
  policy) step_policy;; tests) step_tests;; verify) step_verify "${2:-}";;
  *) echo "steps: start L | card | pins | slot | generate | backup | public | tocard | policy | tests | verify L"; exit 2;;
esac
