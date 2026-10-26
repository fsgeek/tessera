#!/usr/bin/env bash
# Install the V1 service verifier from this directory only (it reads nothing outside it).
#   bash install.sh
# Creates .venv (Python 3.14, Unicode 16.0.0, pinned requirements), checks the six pinned SHA-1DC source digests
# (vendor/SHA1DC-PIN.md), builds the detector in build/, runs known-answer checks, and writes install.json: the
# per-installation record (profile 15.9 R2), outside any signed archive, unsigned, carrying no authority.
# Offline except the package install. Needs: uv or python3.14, and cc + make.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/vendor/sha1collisiondetection"
BUILD="$HERE/build/sha1collisiondetection"
PYTHON="$HERE/.venv/bin/python"
die() { echo "install: $*" >&2; exit 1; }

if [ ! -x "$PYTHON" ]; then
  if command -v uv >/dev/null 2>&1; then uv venv --python 3.14 "$HERE/.venv"
  elif command -v python3.14 >/dev/null 2>&1; then python3.14 -m venv "$HERE/.venv"
  else die "need uv or python3.14"; fi
fi
if command -v uv >/dev/null 2>&1; then
  uv pip install --python "$PYTHON" -r "$HERE/requirements.txt" pytest
  uv pip install --python "$PYTHON" --no-deps -e "$HERE"
else
  "$PYTHON" -m pip install --no-cache-dir -r "$HERE/requirements.txt" pytest
  "$PYTHON" -m pip install --no-cache-dir --no-deps -e "$HERE"
fi
"$PYTHON" - <<'PY' || die "Python must be 3.14 with Unicode 16.0.0 tables"
import sys, unicodedata
assert sys.version_info[:2] == (3, 14), sys.version
assert unicodedata.unidata_version == '16.0.0', unicodedata.unidata_version
PY

command -v cc >/dev/null 2>&1 && command -v make >/dev/null 2>&1 || die "need cc and make"
check() { echo "$2  $SRC/$1" | sha256sum -c --quiet - || die "SHA-1DC source digest mismatch: $1"; }
check lib/sha1.c       364a00322dd93914cf319d4ae45e3644ba45b713dc2e403c8382921abfdcf8e5
check lib/sha1.h       78f97f092c20329d1fa8d9a8cbb3d53bb90be19cbc49f1917605a9ddf520de83
check lib/ubc_check.c  7b0db83569ba82965dc0d16e51e9ad85167cdfdab343f9a02c2c475bfdd93956
check lib/ubc_check.h  4a140693701da167b4709c4c1b330800a0c29f2a065d0d819567a27b3171a09f
check src/main.c       abb081e087604a2aa27ace3059ee1fdc840b903405e6ecb97e160ae857af53ed
check Makefile         7c394be47a03e6843a9780e2e8bc4e16e0a44800305715edcd09364cd44fdfb2

mkdir -p "$HERE/build"
# Replace only our own previous build directory (literal path under build/).
[ -d "$BUILD" ] && rm -r "$BUILD"
mkdir "$BUILD"
cp -R "$SRC/lib" "$SRC/src" "$SRC/Makefile" "$BUILD/"
make -C "$BUILD" bin/sha1dcsum >"$HERE/build/make.log" 2>&1 || { tail -20 "$HERE/build/make.log" >&2; die "build failed"; }
BIN="$BUILD/bin/sha1dcsum"
[ "$(printf 'abc' | "$BIN" - | cut -d' ' -f1)" = "a9993e364706816aba3e25717850c26c9cd0d89d" ] || die "sha1dcsum known-answer failed"
"$BIN" "$SRC/test/shattered-1.pdf" | grep -q '\*coll\*' || die "sha1dcsum did not detect the SHAttered PDF"

HASH="$(sha256sum "$BIN" | cut -d' ' -f1)"
"$PYTHON" -I - "$HERE" "$BIN" "$HASH" <<'PY'
import json, sys
sys.path.insert(0, sys.argv[1])
from tessera_verify import install_record
json.dump(install_record.current_facts(sys.argv[2], sys.argv[3]), open(sys.argv[1] + '/install.json', 'w'), indent=1, sort_keys=True)
PY
echo "installed. run: $HERE/.venv/bin/tessera-verify --help   (tests: $HERE/.venv/bin/python -m pytest $HERE/tests)"
