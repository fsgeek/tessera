#!/usr/bin/env bash
# Sign (or rehearse signing) a Tessera verifier release, offline on Tails (owner, 2026-11-23). Read before running.
#   bash /tmp/s.sh rehearse     a throwaway TEST key made in memory; shows the A10 row-36 refusals; no YubiKey
#   bash /tmp/s.sh sign         YubiKey B (serial 39975596), the production release key CADC...035E
# Reads /media/amnesia/INPUT/{tessera-verifier-v1-1.parts, release.pub.asc, release_tool.py[, release-vectors/]},
# copies them into memory once and asks you to remove INPUT before any key is used. Runs only files whose SHA-256 you
# wrote in the networked session from the approved source. Writes only to /media/amnesia/OUT, after every check, and
# reads back what it wrote. It never runs or installs anything from the archive.
set -u
export LC_ALL=C LANG=C
MODE="${1:-}"
REL_FPR=CADC96CF002355F8E83FE97FAFF80961D825035E
REL_SERIAL=39975596
NAME=tessera-verifier-v1-1.parts
IN=/media/amnesia/INPUT; OUT=/media/amnesia/OUT; W=/tmp/rel
fail() { printf '\n==> FAIL: %s\n\n' "$*"; exit 1; }
quarantine() { printf '\n==> FAIL: %s\n==> OUT IS QUARANTINED: write QUARANTINE on it; nothing on it is used.\n\n' "$*"; exit 1; }
say()  { printf '\n%s\n' "$*"; }
ask()  { printf '\n%s Type yes: ' "$1"; read -r ok; [ "$ok" = yes ] || fail "not confirmed; nothing signed"; }
disk_of() { lsblk -nrso NAME,TYPE "$1" 2>/dev/null | awk '$2=="disk"{print $1; exit}'; }
stick() { local d; d=$(disk_of "$(findmnt -n -o SOURCE --target "$1")"); lsblk -ndo SERIAL,SIZE,MODEL "/dev/$d" 2>/dev/null; }
# expect_refusal TEXT COMMAND...: the command must exit 1, and its whole error output must be exactly "REFUSED: TEXT".
expect_refusal() {
  local want="$1"; shift
  local err rc; err=$("$@" 2>&1 >/dev/null); rc=$?
  [ "$rc" -eq 1 ] && [ "$err" = "REFUSED: $want" ] || fail "expected exit 1 and exactly 'REFUSED: $want', got exit $rc: $err"
  echo "  $err"
}
[ "$MODE" = rehearse ] || [ "$MODE" = sign ] || fail "say 'rehearse' or 'sign'"
T0=$(date -u +%Y-%m-%dT%H:%M:%SZ)

say "1. Session checks:"
for i in /sys/class/net/*; do
  [ -e "$i/device" ] || continue
  [ "$(cat "$i/operstate")" = down ] || fail "hardware network interface $(basename "$i") is not down"
done
[ -z "$(ip route show default)$(ip -6 route show default)" ] || fail "a default route exists"
[ "$(awk 'NR>1 && $1 !~ /^\/dev\/zram/' /proc/swaps | wc -l)" -eq 0 ] || fail "non-zram swap is active"
for src in $(findmnt -rn -o SOURCE | sed 's/\[.*//' | grep '^/dev/' | sort -u); do
  d=$(disk_of "$src"); [ -n "$d" ] || continue
  [ "$(lsblk -ndo TRAN "/dev/$d")" = usb ] || fail "$src is mounted and is not on a USB stick (an internal disk?)"
done
command -v python3 >/dev/null || fail "python3 is not available"
[ -s "$IN/$NAME" ] && [ -s "$IN/release.pub.asc" ] && [ -s "$IN/release_tool.py" ] || fail "INPUT must hold $NAME, release.pub.asc, release_tool.py"
[ "$MODE" = sign ] || [ -s "$IN/release-vectors/run.py" ] || fail "INPUT must hold release-vectors/ for the rehearsal"
[ "$(findmnt -n -o TARGET --target "$OUT" 2>/dev/null)" = "$OUT" ] || fail "$OUT is not mounted (format a stick FAT, volume name OUT)"
[ -z "$(ls -A "$OUT")" ] || fail "$OUT is not empty: format it again"
[ -e "$W" ] && fail "$W exists: this is not a fresh session; shut down and start again"
mkdir "$W" && cp "$IN/$NAME" "$IN/release.pub.asc" "$IN/release_tool.py" "$W/" || fail "copy from INPUT"
[ "$MODE" = sign ] || cp -R "$IN/release-vectors" "$W/" || fail "copy release-vectors"
export GNUPGHOME=$(mktemp -d /tmp/gnupg.XXXXXX) && chmod 700 "$GNUPGHOME"
[ "$(findmnt -n -o FSTYPE --target "$W")" = tmpfs ] && [ "$(findmnt -n -o FSTYPE --target "$GNUPGHOME")" = tmpfs ] || fail "/tmp is not in memory"
GPGV=$(command -v gpgv) || fail "no gpgv"
gpg --version | head -1; gpgv --version | head -1
sha256sum "$GPGV" | awk '{h=$1; printf "  gpgv binary %s\n    ", $2; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
echo "  INPUT stick: $(stick "$IN")"
echo "  OUT stick:   $(stick "$OUT")"
ask "INPUT's serial is the one you wrote in Part 1, and OUT is the stick your sheet names?"

say "2. The files now in memory. Compare each with the value you wrote in Part 1, in full:"
sha256sum "$W/$NAME" "$W/release_tool.py" "$W/release.pub.asc" | awk '{h=$1; printf "  %s\n    ", $2; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
if [ "$MODE" = rehearse ]; then
  VEC=$(cd "$W" && find release-vectors -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1)
  echo "$VEC" | awk '{h=$1; printf "  release-vectors (all files)\n    "; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
fi
ask "Every value equals what you wrote?"
say "Eject INPUT in Files and remove it now. Then press Enter."; read -r _
[ -z "$(findmnt -n -o TARGET --target "$IN" 2>/dev/null | grep -x "$IN")" ] || fail "INPUT is still mounted: eject and remove it, then run again from step 0"

say "3. The archive (read only; nothing in it is run):"
python3 -I "$W/release_tool.py" inspect "$W/$NAME" || fail "the archive is not a well-formed release: DO NOT SIGN"
python3 -I - "$W/$NAME" <<'EOF' || fail "the archive's namespace is not PRODUCTION: DO NOT SIGN"
import json, re, sys
d = open(sys.argv[1], 'rb').read(); m = re.match(rb'tessera-v1-part RELEASE.json ([0-9]+)\n', d)
assert m and json.loads(d[m.end():m.end() + int(m.group(1))])['namespace'] == 'PRODUCTION'
print('  namespace PRODUCTION')
EOF

say "4. The release public key on INPUT:"
gpg --show-keys --with-fingerprint "$W/release.pub.asc" 2>/dev/null | sed -n '1,3p'
python3 -I - "$W/release_tool.py" "$W/release.pub.asc" "$REL_FPR" <<'EOF' || fail "release.pub.asc is not the release key CADC...035E: DO NOT SIGN"
import importlib.util, sys
s = importlib.util.spec_from_file_location('rt', sys.argv[1]); rt = importlib.util.module_from_spec(s); s.loader.exec_module(rt)
rt.release_key(sys.argv[2], sys.argv[3]); print('  key file holds exactly the key', rt.groups(sys.argv[3]))
EOF
gpg --import "$W/release.pub.asc" 2>/dev/null || fail "import of release.pub.asc"

if [ "$MODE" = sign ]; then
  ask "Paper, ORCID and screen all read CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E?"
  say "Insert YubiKey B now, then press Enter."; read -r _
  # A plain --card-status links the card's key to this fresh keyring (2026-11-13); retry a just-inserted card.
  for t in 1 2 3; do gpg --card-status >/dev/null 2>&1 && break; sleep 2; done
  gpg --card-status | grep -E 'Serial|Signature key'
  serial=$(gpg --card-status 2>/dev/null | sed -n 's/^Serial number[ .]*: *//p')
  card=$(gpg --with-colons --card-status 2>/dev/null | awk -F: '$1=="fpr"{print toupper($2)}')
  [ "$serial" = "$REL_SERIAL" ] && [ "$card" = "$REL_FPR" ] || fail "the card is not YubiKey B (serial '$serial', key '$card'): remove it"
  SIGNER=$REL_FPR; KEY="$W/release.pub.asc"; UID_="Tessera release key <tessera@wamason.com>"
  say "5. Last check before signing. The archive you are signing:"
  sha256sum "$W/$NAME" | awk '{h=$1; printf "  "; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
  ask "This equals the archive hash you wrote in Part 1 (your own build)? This signs."
  say "Signing: enter the user PIN, then touch the key when it blinks."
  gpg --local-user "$REL_FPR!" --digest-algo SHA256 --output "$W/$NAME.sig" --detach-sign "$W/$NAME" || fail "signing failed: remove YubiKey B"
  say "Remove YubiKey B now, then press Enter."; read -r _
else
  say "5. Rehearsal: making a throwaway TEST key in memory (never a release key)."
  UID_="THROWAWAY TEST release key, rehearsal $T0 <throwaway@invalid>"
  gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key "$UID_" nistp256 sign never 2>/dev/null || fail "TEST key generation"
  SIGNER=$(gpg --with-colons --list-secret-keys 2>/dev/null | awk -F: '$1=="fpr"{print toupper($10); exit}')
  [ -n "$SIGNER" ] && [ "$SIGNER" != "$REL_FPR" ] || fail "TEST key"
  gpg --export "$SIGNER" 2>/dev/null > "$W/test.pub.pgp" || fail "TEST key export"
  KEY="$W/test.pub.pgp"
  echo "  TEST key $SIGNER"
  say "6. Signing the PRODUCTION archive with the TEST key only."
  gpg --batch --pinentry-mode loopback --passphrase '' --local-user "$SIGNER!" --digest-algo SHA256 \
      --output "$W/$NAME.sig" --detach-sign "$W/$NAME" 2>/dev/null || fail "TEST signing failed"
fi

say "7. The new signature over the same bytes, with only the signer's key (rehearsal: a control, not a release):"
python3 -I "$W/release_tool.py" verify-sig "$W/$NAME" "$W/$NAME.sig" --fingerprint "$SIGNER" --key "$KEY" \
  || fail "the new signature does not verify"

say "8. One changed byte must be refused by gpgv:"
python3 -I - "$W/$NAME" "$W/mutated" <<'EOF' || fail "mutation copy"
import sys; b = bytearray(open(sys.argv[1], 'rb').read()); b[len(b) // 2] ^= 1; open(sys.argv[2], 'wb').write(b)
EOF
expect_refusal "gpgv refused (exit 1): ['gpgv: BAD signature from \"$UID_\"']" python3 -I "$W/release_tool.py" verify-sig "$W/mutated" "$W/$NAME.sig" \
  --fingerprint "$SIGNER" --key "$KEY"
echo "  MUTATION REFUSED (as required)"

if [ "$MODE" = rehearse ]; then
  say "9. A10 row 36: production acquisition (fingerprint CADC...035E) must refuse the TEST-signed archive, unpack nothing."
  n=0
  for key in "$W/release.pub.asc" "$W/test.pub.pgp"; do
    n=$((n + 1))
    expect_refusal "signed by $SIGNER, not by the authenticated key $REL_FPR" \
      python3 -I "$W/release_tool.py" acquire "$W/$NAME" "$W/$NAME.sig" --fingerprint "$REL_FPR" --key "$key" --out "$W/acq$n"
    [ ! -e "$W/acq$n" ] || fail "acquisition wrote $W/acq$n"
    echo "  ROW 36 REFUSED, nothing unpacked, key offered: $(basename "$key") (as required)"
  done
  echo "  (The installed verifier's section 3.5 refusal needs Python 3.14 and cannot run here: NUC evidence only.)"
  say "10. This Tails gpgv against the release-format vectors (profile 15.9 R3):"
  python3 -I "$W/release-vectors/run.py" "$GPGV" > "$W/vectors.txt"; rc=$?
  cat "$W/vectors.txt"
  [ "$rc" -eq 0 ] && [ "$(tail -1 "$W/vectors.txt")" = "9/9 match" ] || fail "this gpgv does not reproduce upstream on the vectors"
fi

say "11. Writing OUT (only now), then reading it back:"
{ echo "mode $MODE"; echo "started $T0"; echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "signer $SIGNER"; gpg --version | head -1; gpgv --version | head -1; sha256sum "$GPGV"
  sha256sum "$W/$NAME" "$W/$NAME.sig" | sed "s#$W/##"
  [ "$MODE" = sign ] || cat "$W/vectors.txt"; } > "$W/record.txt" || fail "record.txt"
FILES="$NAME.sig record.txt"; [ "$MODE" = sign ] || FILES="$FILES test.pub.pgp"
for f in $FILES; do cp "$W/$f" "$OUT/$f" || quarantine "could not write $f to OUT"; done
sync || quarantine "sync failed"
for f in $FILES; do
  [ "$(sha256sum < "$OUT/$f")" = "$(sha256sum < "$W/$f")" ] || quarantine "OUT's $f does not read back equal"
done
[ "$(ls -A "$OUT" | sort | tr '\n' ' ')" = "$(echo $FILES | tr ' ' '\n' | sort | tr '\n' ' ')" ] || quarantine "OUT holds other files"
ls -A1 "$OUT" || quarantine "could not list OUT"
H=$(cd "$OUT" && sha256sum $FILES) || quarantine "could not hash OUT's files"
echo "$H"
printf '\n==> PASS: %s. Eject OUT, shut down. OUT goes to the owner and never returns to a signing session.\n\n' "$MODE"
