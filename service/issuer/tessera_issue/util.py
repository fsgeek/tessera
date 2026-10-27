"""Small shared helpers: hashing, canonical base64, canonical JSON (the service verifier's JCS), RFC 3339 times."""
import base64
import hashlib
import json
import os
import time

from tessera_verify.codec import jcs as _jcs

D = "wamason.com"
PROFILE = "tessera-v1-strict"
SPEC_ID = "tessera-v1-strict/verification-spec/1"
ALG = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256"   # the catalog's registered pair id (hybrid branch)
EPS, DELTA, K = 24 * 3600, 72 * 3600, 6                     # profile section 1; the verifier owns them
HOUR, DAY = 3600, 86400
MIB = 1 << 20
POLICY_VERSION = "tessera-v1-issue-policy/1"


def sha256(b):
    return hashlib.sha256(b).digest()


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def sha256d(b):
    return sha256(sha256(b))


def b64e(b):
    return base64.b64encode(bytes(b)).decode("ascii")


def b64d(s):
    raw = base64.b64decode(s, validate=True)
    if base64.b64encode(raw).decode("ascii") != s:
        raise ValueError("non-canonical base64")
    return raw


def jcs(value):
    """RFC 8785 bytes, the same serializer the service verifier checks container canonicality with."""
    return _jcs(value)


def dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def ts(s):
    """'YYYY-MM-DDTHH:MM:SSZ' -> integer seconds (no leap seconds)."""
    if len(s) != 20 or s[4] != "-" or s[7] != "-" or s[10] != "T" or s[13] != ":" or s[16] != ":" or s[19] != "Z":
        raise ValueError("not an RFC 3339 UTC second: " + repr(s))
    y, mo, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    return _days_from_civil(y, mo, d) * 86400 + int(s[11:13]) * 3600 + int(s[14:16]) * 60 + int(s[17:19])


def rfc3339(t):
    t = int(t)
    days, rem = divmod(t, 86400)
    z = days + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    y += m <= 2
    return f"{y:04d}-{m:02d}-{d:02d}T{rem // 3600:02d}:{rem % 3600 // 60:02d}:{rem % 60:02d}Z"


class SystemClock:
    def __call__(self):
        return int(time.time())


class FakeClock:
    """A settable clock for tests and local runs."""

    def __init__(self, t):
        self.t = int(t)

    def __call__(self):
        return self.t

    def advance(self, s):
        self.t += int(s)
        return self.t


def random_bytes(n):
    return os.urandom(n)
