#!/usr/bin/env bash
# One-command install of the independent V1 verifier instrument (TEST release tooling).
#   prototype/indep-verifier/packaging/install.sh
# Creates indep-verifier/.venv (Python 3.14, Unicode 16.0.0, pinned requirements), builds the pinned SHA-1DC
# detector from prototype/vendor/sha1collisiondetection after checking the source digests in SHA1DC-PIN.md,
# records the local binary hash in sha1dc_build.json, and runs known-answer smoke checks. Offline except the
# pip/uv package install. Needs: uv or python3.14, and cc + make.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IND="$(dirname "$HERE")"
SRC="$(dirname "$IND")/vendor/sha1collisiondetection"
BUILD="$HERE/build/sha1collisiondetection"
PYTHON="$IND/.venv/bin/python"

die() { echo "install: $*" >&2; exit 1; }

# 1. Python 3.14 environment
if [ ! -x "$PYTHON" ]; then
  if command -v uv >/dev/null 2>&1; then uv venv --python 3.14 "$IND/.venv"
  elif command -v python3.14 >/dev/null 2>&1; then python3.14 -m venv "$IND/.venv"
  else die "need uv or python3.14"; fi
fi
if command -v uv >/dev/null 2>&1; then
  uv pip install --python "$PYTHON" -r "$IND/requirements.txt"
else
  "$PYTHON" -m pip install --no-cache-dir -r "$IND/requirements.txt"
fi
"$PYTHON" - <<'PY' || die "Python must be 3.14 with Unicode 16.0.0 tables"
import sys, unicodedata
assert sys.version_info[:2] == (3, 14), sys.version
assert unicodedata.unidata_version == '16.0.0', unicodedata.unidata_version
PY

# 2. Pinned SHA-1DC source digests (SHA1DC-PIN.md; commit a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988)
command -v cc >/dev/null 2>&1 && command -v make >/dev/null 2>&1 || die "need cc and make"
check() { echo "$2  $SRC/$1" | sha256sum -c --quiet - || die "SHA-1DC source digest mismatch: $1"; }
check lib/sha1.c       364a00322dd93914cf319d4ae45e3644ba45b713dc2e403c8382921abfdcf8e5
check lib/sha1.h       78f97f092c20329d1fa8d9a8cbb3d53bb90be19cbc49f1917605a9ddf520de83
check lib/ubc_check.c  7b0db83569ba82965dc0d16e51e9ad85167cdfdab343f9a02c2c475bfdd93956
check lib/ubc_check.h  4a140693701da167b4709c4c1b330800a0c29f2a065d0d819567a27b3171a09f
check src/main.c       abb081e087604a2aa27ace3059ee1fdc840b903405e6ecb97e160ae857af53ed
check Makefile         7c394be47a03e6843a9780e2e8bc4e16e0a44800305715edcd09364cd44fdfb2

# 3. Build in a private copy (default flags, safe-hash on, as the pin records)
mkdir -p "$HERE/build"
rm -rf "${HERE:?}/build/sha1collisiondetection"
mkdir "$BUILD"
cp -R "$SRC/lib" "$SRC/src" "$SRC/Makefile" "$BUILD/"
make -C "$BUILD" bin/sha1dcsum >"$HERE/build/make.log" 2>&1 || { tail -20 "$HERE/build/make.log" >&2; die "build failed"; }
BIN="$BUILD/bin/sha1dcsum"

# 4. Known-answer checks: plain SHA-1 passes; the SHAttered PDF (in the vendored test/ directory) is detected
[ "$(printf 'abc' | "$BIN" -)" = "a9993e364706816aba3e25717850c26c9cd0d89d  -" ] \
  || [ "$(printf 'abc' | "$BIN" - | cut -d' ' -f1)" = "a9993e364706816aba3e25717850c26c9cd0d89d" ] \
  || die "sha1dcsum known-answer failed"
"$BIN" "$SRC/test/shattered-1.pdf" | grep -q '\*coll\*' || die "sha1dcsum did not detect the SHAttered PDF"

# 5. Record the local build pin (the hash is compiler-dependent)
HASH="$(sha256sum "$BIN" | cut -d' ' -f1)"
"$PYTHON" - "$IND/sha1dc_build.json" "$BIN" "$HASH" <<'PY'
import json, sys
json.dump({'upstream_commit': 'a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988', 'binary': sys.argv[2],
           'binary_sha256': sys.argv[3]}, open(sys.argv[1], 'w'), indent=1)
PY

# 6. Self-test
( cd "$IND" && "$PYTHON" -I -c "import sys; sys.path.insert(0,'.'); import sha1dc; assert sha1dc.available(), 'SHA-1DC not available'" ) \
  || die "verifier cannot see the SHA-1DC binary"
( cd "$IND" && "$PYTHON" -m unittest discover -s tests ) >"$HERE/build/tests.log" 2>&1 \
  || { tail -20 "$HERE/build/tests.log" >&2; die "test suite failed"; }
echo "installed: $(tail -3 "$HERE/build/tests.log" | tr '\n' ' ')"
echo "run:  $HERE/verify --test-release R --test-release-key K --trust TRUST --bundle BUNDLE"
