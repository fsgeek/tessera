#!/usr/bin/env bash
# Sign (or rehearse signing) a Tessera verifier release, offline on Tails (owner, 2026-11-23). Read before running.
#   bash /tmp/s.sh rehearse     a throwaway TEST key made in memory; shows the A10 row-36 refusals; no YubiKey
#   bash /tmp/s.sh sign         YubiKey B, the production release key CADC...035E
# Reads /media/amnesia/INPUT/{tessera-verifier-v1-1.parts, release.pub.asc, release_tool.py[, release-vectors/]},
# copies them into memory and asks you to remove INPUT before any key is used. Writes only to /media/amnesia/OUT.
# It never runs or installs anything from the archive: release_tool.py comes from GitHub beside it, not from inside it.
set -u
export LC_ALL=C LANG=C
MODE="${1:-}"
REL_FPR=CADC96CF002355F8E83FE97FAFF80961D825035E
NAME=tessera-verifier-v1-1.parts
IN=/media/amnesia/INPUT; OUT=/media/amnesia/OUT; W=/tmp/rel
fail() { printf '\n==> FAIL: %s\n\n' "$*"; exit 1; }
say()  { printf '\n%s\n' "$*"; }
[ "$MODE" = rehearse ] || [ "$MODE" = sign ] || fail "say 'rehearse' or 'sign'"
T0=$(date -u +%Y-%m-%dT%H:%M:%SZ)

say "1. Session checks:"
for i in /sys/class/net/*; do
  [ -e "$i/device" ] || continue
  [ "$(cat "$i/operstate")" = down ] || fail "hardware network interface $(basename "$i") is not down"
done
[ -z "$(ip route show default)$(ip -6 route show default)" ] || fail "a default route exists"
[ "$(awk 'NR>1 && $1 !~ /^\/dev\/zram/' /proc/swaps | wc -l)" -eq 0 ] || fail "non-zram swap is active"
command -v python3 >/dev/null || fail "python3 is not available"
[ -s "$IN/$NAME" ] && [ -s "$IN/release.pub.asc" ] && [ -s "$IN/release_tool.py" ] || fail "INPUT must hold $NAME, release.pub.asc, release_tool.py"
[ "$MODE" = sign ] || [ -s "$IN/release-vectors/run.py" ] || fail "INPUT must hold release-vectors/ for the rehearsal"
[ "$(findmnt -n -o TARGET --target "$OUT" 2>/dev/null)" = "$OUT" ] || fail "$OUT is not mounted (format a stick FAT, volume name OUT)"
[ -e "$W" ] && fail "$W exists: this is not a fresh session; shut down and start again"
mkdir "$W" && cp "$IN/$NAME" "$IN/release.pub.asc" "$IN/release_tool.py" "$W/" || fail "copy from INPUT"
[ "$MODE" = sign ] || cp -R "$IN/release-vectors" "$W/" || fail "copy release-vectors"
export GNUPGHOME=$(mktemp -d /tmp/gnupg.XXXXXX) && chmod 700 "$GNUPGHOME"
[ "$(findmnt -n -o FSTYPE --target "$W")" = tmpfs ] && [ "$(findmnt -n -o FSTYPE --target "$GNUPGHOME")" = tmpfs ] || fail "/tmp is not in memory"
gpg --version | head -1; gpgv --version | head -1
echo "ok"

say "2. The files now in memory. Compare each with your paper, in full:"
sha256sum "$W/$NAME" "$W/release_tool.py" "$W/release.pub.asc" | awk '{h=$1; printf "  %s\n    ", $2; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
printf '\nAll three equal the paper? Type yes: '; read -r ok; [ "$ok" = yes ] || fail "not confirmed; nothing signed"
say "Eject INPUT in Files and remove it now. Then press Enter."; read -r _
[ -z "$(findmnt -n -o TARGET --target "$IN" 2>/dev/null | grep -x "$IN")" ] || fail "INPUT is still mounted: eject and remove it, then run again from step 0"

say "3. The archive (read only; nothing in it is run):"
python3 -I "$W/release_tool.py" inspect "$W/$NAME" || fail "the archive is not a well-formed release: DO NOT SIGN"
python3 -I - "$W/$NAME" <<'EOF' || fail "the archive's namespace is not PRODUCTION: DO NOT SIGN"
import json, re, sys
d = open(sys.argv[1], 'rb').read(); m = re.match(rb'tessera-v1-part RELEASE.json ([0-9]+)\n', d)
assert m and json.loads(d[m.end():m.end() + int(m.group(1))])['namespace'] == 'PRODUCTION'
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
  say "5. Compare the fingerprint above with your PAPER ceremony record and with what you wrote from ORCID."
  printf 'Paper, ORCID and screen all read CADC 96CF 0023 55F8 E83F E97F AFF8 0961 D825 035E? Type yes: '; read -r ok
  [ "$ok" = yes ] || fail "not confirmed; nothing signed"
  say "Insert YubiKey B now, then press Enter."; read -r _
  # A plain --card-status links the card's key to this fresh keyring (2026-11-13); retry a just-inserted card.
  for t in 1 2 3; do gpg --card-status >/dev/null 2>&1 && break; sleep 2; done
  gpg --card-status | grep -E 'Serial|Signature key'
  card=$(gpg --with-colons --card-status 2>/dev/null | awk -F: '$1=="fpr"{print toupper($2)}')
  [ "$card" = "$REL_FPR" ] || fail "the card is not YubiKey B (card holds '$card')"
  SIGNER=$REL_FPR
  say "6. Last check before signing. The archive you are signing:"
  sha256sum "$W/$NAME" | awk '{h=$1; printf "  "; for(i=1;i<=64;i+=8) printf "%s ", substr(h,i,8); print ""}'
  printf 'This equals the archive hash on your paper (built by you in the networked session)? Type yes to sign: '; read -r ok
  [ "$ok" = yes ] || fail "not confirmed; nothing signed"
  say "Signing: enter the user PIN, then touch the key when it blinks."
  gpg --local-user "$REL_FPR!" --digest-algo SHA256 --output "$W/$NAME.sig" --detach-sign "$W/$NAME" || fail "signing failed"
  say "Remove YubiKey B now, then press Enter."; read -r _
else
  say "5. Rehearsal: making a throwaway TEST key in memory (never a release key)."
  gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key \
      "THROWAWAY TEST release key, rehearsal $T0 <throwaway@invalid>" nistp256 sign never 2>/dev/null || fail "TEST key generation"
  SIGNER=$(gpg --with-colons --list-secret-keys 2>/dev/null | awk -F: '$1=="fpr"{print toupper($10); exit}')
  [ -n "$SIGNER" ] && [ "$SIGNER" != "$REL_FPR" ] || fail "TEST key"
  gpg --export "$SIGNER" 2>/dev/null > "$W/test.pub.pgp" || fail "TEST key export"
  echo "  TEST key $SIGNER"
  say "6. Signing the PRODUCTION archive with the TEST key only."
  gpg --batch --pinentry-mode loopback --passphrase '' --local-user "$SIGNER!" --digest-algo SHA256 \
      --output "$W/$NAME.sig" --detach-sign "$W/$NAME" 2>/dev/null || fail "TEST signing failed"
fi

say "7. Verify the signature over the same bytes, as a relying party would:"
python3 -I "$W/release_tool.py" verify-sig "$W/$NAME" "$W/$NAME.sig" --fingerprint "$SIGNER" \
  --key "$([ "$MODE" = sign ] && echo "$W/release.pub.asc" || echo "$W/test.pub.pgp")" || fail "the new signature does not verify"

say "8. One changed byte must fail:"
python3 -I - "$W/$NAME" "$W/mutated" <<'EOF' || fail "mutation copy"
import sys; b = bytearray(open(sys.argv[1], 'rb').read()); b[len(b) // 2] ^= 1; open(sys.argv[2], 'wb').write(b)
EOF
if python3 -I "$W/release_tool.py" verify-sig "$W/mutated" "$W/$NAME.sig" --fingerprint "$SIGNER" \
     --key "$([ "$MODE" = sign ] && echo "$W/release.pub.asc" || echo "$W/test.pub.pgp")" 2>/dev/null; then
  fail "a changed archive verified: DO NOT USE THIS SIGNATURE"
fi
echo "  MUTATION REFUSED (as required)"

if [ "$MODE" = rehearse ]; then
  say "9. A10 row 36: the archive signed only by the TEST key must be refused by the production procedure."
  for key in "$W/release.pub.asc" "$W/test.pub.pgp"; do
    if python3 -I "$W/release_tool.py" verify-sig "$W/$NAME" "$W/$NAME.sig" --fingerprint "$REL_FPR" --key "$key"; then
      fail "a TEST-signed archive was accepted with key $(basename "$key")"
    fi
    echo "  ROW 36 REFUSED with key $(basename "$key") (as required)"
  done
  say "10. This Tails gpgv against the release-format vectors (profile 15.9 R3):"
  python3 -I "$W/release-vectors/run.py" "$(command -v gpgv)" | tee "$W/vectors.txt"
  grep -q '^9/9 match$' "$W/vectors.txt" || fail "this gpgv does not reproduce upstream on the vectors"
fi

say "11. Writing OUT:"
{ echo "mode $MODE"; echo "started $T0"; echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "signer $SIGNER"; gpg --version | head -1; gpgv --version | head -1
  sha256sum "$W/$NAME" "$W/$NAME.sig" | sed "s#$W/##"
  [ "$MODE" = sign ] || cat "$W/vectors.txt"; } > "$W/record.txt"
cp "$W/$NAME.sig" "$W/record.txt" "$OUT/" || fail "could not write to $OUT"
[ "$MODE" = sign ] || cp "$W/test.pub.pgp" "$OUT/" || fail "could not write to $OUT"
sync
ls -la "$OUT"
sha256sum "$OUT"/* | sed "s#$OUT/##"
printf '\n==> PASS: %s. Eject OUT, shut down. OUT goes to the owner and never returns to a signing session.\n\n' "$MODE"
