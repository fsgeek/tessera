"""Row 14.4: the owner-pinned SHA-1DC detector (docs/V1-PROFILE.md 15.4; pin record vendor/SHA1DC-PIN.md).

It implements no reading: it runs the pinned detector over the git-framed object bytes and reports its prescribed
collision return. The binary is built on the installing machine by install.sh from the vendored pinned source; its
path and SHA-256 are machine-specific and live in install.json (configure()), never in the signed archive.
"""
import hashlib
import subprocess
from pathlib import Path

UPSTREAM_COMMIT = 'a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988'
BINARY = None            # set by configure() from install.json
BINARY_SHA256 = None


def configure(binary, sha256):
    global BINARY, BINARY_SHA256
    BINARY, BINARY_SHA256 = (Path(binary) if binary else None), sha256


class Unavailable(Exception):
    pass


def available():
    try:
        return BINARY is not None and hashlib.sha256(BINARY.read_bytes()).hexdigest() == BINARY_SHA256
    except OSError:
        return False


def functional():
    """True iff the detector is present, hash-matching, runs, and reports no collision for a known-clean input."""
    try:
        return available() and collision('blob', b'abc') is False
    except Unavailable:
        return False


def collision(kind, body):
    """True iff the pinned detector reports a collision for "<kind> <len>\\0" || body."""
    if not available():
        raise Unavailable()
    framed = kind.encode() + b' ' + str(len(body)).encode() + b'\x00' + body
    try:
        p = subprocess.run([str(BINARY), '-'], input=framed, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        raise Unavailable() from None
    parts = p.stdout.decode('ascii', 'replace').split()
    if p.returncode != 0 or len(parts) not in (2, 3) or len(parts[0]) != 40 or parts[-1] != '-':
        raise Unavailable()
    if len(parts) == 3:
        if parts[1] != '*coll*':
            raise Unavailable()
        return True
    return False
