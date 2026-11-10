#!/usr/bin/env bash
# Sign the window's key-assertion commit with the repository root (YubiKey A), offline on Tails (owner, 2026-11-10).
#   bash /tmp/s.sh
# Reads /media/amnesia/INPUT/{payload.txt, root.pub.asc}; writes /media/amnesia/OUT/payload.sig.asc.
# Before signing it shows the commit text and recomputes the commit's tree from the 255-byte value in the message:
# if the tree does not match the value you read, it refuses. Read this script before running it.
set -u
export LC_ALL=C LANG=C
ROOT_FPR=6BDA21559F18D5DB8E1312C363210B5FF92AD30A
IN=/media/amnesia/INPUT; OUT=/media/amnesia/OUT
fail() { printf '\n==> FAIL: %s\n\n' "$*"; exit 1; }
say()  { printf '\n%s\n' "$*"; }

say "Session checks:"
for i in /sys/class/net/*; do
  [ -e "$i/device" ] || continue
  [ "$(cat "$i/operstate")" = down ] || fail "hardware network interface $(basename "$i") is not down"
done
[ -z "$(ip route show default)$(ip -6 route show default)" ] || fail "a default route exists"
[ "$(awk 'NR>1 && $1 !~ /^\/dev\/zram/' /proc/swaps | wc -l)" -eq 0 ] || fail "non-zram swap is active"
command -v python3 >/dev/null || fail "python3 is not available (tell the owner)"
export GNUPGHOME=$(mktemp -d /tmp/gnupg.XXXXXX) && chmod 700 "$GNUPGHOME"
[ "$(findmnt -n -o FSTYPE --target "$GNUPGHOME")" = tmpfs ] || fail "keyring is not on tmpfs"
[ -s "$IN/payload.txt" ] && [ -s "$IN/root.pub.asc" ] || fail "INPUT must hold payload.txt and root.pub.asc"
[ "$(findmnt -n -o TARGET --target "$OUT" 2>/dev/null)" = "$OUT" ] || fail "$OUT is not mounted (format a stick FAT, volume name OUT)"
echo "ok"

say "Checking the commit's exact form, then recomputing its tree (nothing is shown before this passes):"
python3 - "$IN/payload.txt" <<'EOF' || fail "the commit is not in the expected form, or its tree does not match its value: DO NOT SIGN"
import hashlib, re, sys
p = open(sys.argv[1], 'rb').read()
# CA-01: only printable ASCII and LF, exact structure, bounded size, before anything reaches the terminal.
assert len(p) < 1024 and all(32 <= b < 127 or b == 10 for b in p), 'non-printable byte or oversized payload'
lines = p.split(b'\n')
ident = rb'Tessera repository root <tessera@wamason\.com> [0-9]{10} \+0000'
assert len(lines) == 8 and lines[7] == b'', 'unexpected number of lines'
assert re.fullmatch(rb'tree [0-9a-f]{40}', lines[0]), 'tree line'
assert re.fullmatch(rb'author ' + ident, lines[1]) and re.fullmatch(rb'committer ' + ident, lines[2]), 'identity lines'
assert lines[3] == b'' and lines[4] == b'Tessera V1 key assertion' and lines[5] == b'', 'message lines'
m = re.fullmatch(rb'v=tessera1;profile=tessera-v1-strict;kms=([0-9a-f]{64});gpg=([0-9a-f]{64});'
                 rb'issuance-not-before=([0-9TZ:-]{20});issuance-not-after=([0-9TZ:-]{20})', lines[6])
assert m and len(lines[6]) == 255, 'value line'
def oid(k, b): return hashlib.sha1(k + b' ' + str(len(b)).encode() + b'\0' + b).digest()
sub = b'100644 key-assertion\0' + oid(b'blob', lines[6])
root = b'40000 tessera-v1\0' + oid(b'tree', sub)
assert lines[0][5:] == oid(b'tree', root).hex().encode(), 'tree does not match the value'
kms, gpg, nb, na = (x.decode() for x in m.groups())
g = lambda h: ' '.join(h[i:i+8] for i in range(0, 64, 8))
print('FORM OK, TREE MATCH. What the root will sign:')
print('  kms service key  spki-sha256:', g(kms))
print('  gpg service key  gpg-sha256: ', g(gpg))
print('  window           ', nb, ' to ', na)
EOF
sha256sum "$IN/payload.txt"
say "These fingerprints come from the owner (the NUC). Your signature authorizes these keys for this window; it does"
say "not prove who holds them. Compare them, in full, with the values the owner gave you."

printf '\nDo the keys and dates above equal the owner'"'"'s values, in full? Type yes to sign: '; read -r ok
[ "$ok" = yes ] || fail "not confirmed; nothing signed"

gpg --import "$IN/root.pub.asc" || fail "root public key import failed"
say "Insert YubiKey A now, then press Enter."; read -r _
card=$(gpg --with-colons --card-status 2>/dev/null | awk -F: '$1=="fpr"{print toupper($2)}')
[ "$card" = "$ROOT_FPR" ] || fail "the card is not YubiKey A (card holds '$card')"
say "Signing: enter the user PIN, then touch the key when it blinks."
gpg --local-user "$ROOT_FPR" --digest-algo SHA256 --armor --output /tmp/payload.sig.asc --detach-sign "$IN/payload.txt" || fail "signing failed"
gpg --verify /tmp/payload.sig.asc "$IN/payload.txt" || fail "signature does not verify"
cp /tmp/payload.sig.asc "$OUT/payload.sig.asc" && sync || fail "could not write to $OUT"
sha256sum "$OUT/payload.sig.asc"
printf '\n==> PASS: signed. Eject OUT and INPUT, remove YubiKey A, shut down. OUT goes to the owner.\n\n'
