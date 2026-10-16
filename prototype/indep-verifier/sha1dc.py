"""Row 14.4 hook: the owner-pinned SHA-1DC detector (decision 2026-10-14).

Added after the independent build, by the differential-test operator, to supply the
missing input named in A04. It implements no reading: it runs the pinned detector over
the git-framed object bytes and reports its prescribed collision return. Pin record:
prototype/vendor/SHA1DC-PIN.md.
"""
import hashlib
import subprocess
from pathlib import Path

UPSTREAM_COMMIT = 'a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988'
BINARY = Path(__file__).resolve().parent.parent / 'vendor' / 'sha1collisiondetection' / 'bin' / 'sha1dcsum'
# Local build pin of BINARY (compiler-dependent); see the pin record.
BINARY_SHA256 = '3fa8472a23ff8ecc6c91b5193bc6e6e7a7ef1a1bbfbbff769a89bda0634dd5fb'


class Unavailable(Exception):
    pass


def available():
    try:
        return hashlib.sha256(BINARY.read_bytes()).hexdigest() == BINARY_SHA256
    except OSError:
        return False


def collision(kind, body):
    """True iff the pinned detector reports a collision for "<kind> <len>\\0" || body."""
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
