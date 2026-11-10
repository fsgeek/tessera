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

say "What you are about to sign (read the kms=, gpg= and dates):"
echo "------------------------------------------------------------"
cat "$IN/payload.txt"
echo "------------------------------------------------------------"
sha256sum "$IN/payload.txt"

say "Recomputing the tree from the value in the message:"
python3 - "$IN/payload.txt" <<'EOF' || fail "the commit's tree does not match the value in its message: DO NOT SIGN"
import hashlib, sys
p = open(sys.argv[1], 'rb').read()
head, msg = p.split(b'\n\n', 1)
tree = head.split(b'\n')[0]
assert tree.startswith(b'tree '), 'no tree line'
lines = msg.split(b'\n')
value = [l for l in lines if l.startswith(b'v=tessera1;')]
assert len(value) == 1 and len(value[0]) == 255, 'message must hold exactly one 255-byte value'
def oid(k, b): return hashlib.sha1(k + b' ' + str(len(b)).encode() + b'\0' + b).digest()
sub = b'100644 key-assertion\0' + oid(b'blob', value[0])
root = b'40000 tessera-v1\0' + oid(b'tree', sub)
want = oid(b'tree', root).hex().encode()
print('tree in commit:   ', tree[5:].decode()); print('tree from value:  ', want.decode())
assert tree[5:] == want, 'mismatch'
print('MATCH')
EOF

printf '\nDoes the text above name the right keys and dates? Type yes to sign: '; read -r ok
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
