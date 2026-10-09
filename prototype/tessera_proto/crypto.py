"""Keys, fingerprints, signatures. In-process keys only (no KMS, no GPG) -- see GUESSES G-12, G-13.

Includes a TEST-ONLY DSKS emulation hook (`DSKSOracle`). Real Ed25519 offers no way to compute
the symbolic library's `dsks(s, r)`; the hook stands in for that adversary capability so the
C-C5 trace can be replayed. It is EMULATED, not a real attack on Ed25519.
"""
from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

ALG_ED25519 = "Ed25519"

# GUESS G-11: algorithm identifiers are an open encoding (O-03). Strings. One supported, one
# "known but unsupported" (registered distinctly from unknown, R-2.38 applies by analogy to
# the algorithm check per §9.2 rows 3-4), and anything else is "unknown".
ALGS_SUPPORTED = {ALG_ED25519}
ALGS_KNOWN_UNSUPPORTED = {"ML-DSA-65", "ECDSA-P256-SHA256"}
CANARY_ALG = "TESSERA-RESERVED-UNRECOGNIZED-0"  # R-9.13 reserved unrecognized identifier

# PHASE 3 hook: real signature algorithms register a verifier here (tessera_proto/real/algs.py):
# alg id -> verify(pub_raw, sig, msg) -> bool. Empty unless real.algs.register() was called.
EXTRA_VERIFIERS: dict = {}


def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"), validate=True)


def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fingerprint(alg: str, pub_raw: bytes) -> str:
    # GUESS G-10: fingerprint function unspecified. sha256(alg || 0x00 || raw public key), hex,
    # prefixed. (GPG v4 fingerprints are SHA-1 over a key packet; not used here.)
    return "fp1:" + sha256_hex(alg.encode("ascii") + b"\x00" + pub_raw)


@dataclass
class KeyPair:
    label: str
    sk: Ed25519PrivateKey = field(repr=False)
    alg: str = ALG_ED25519

    @classmethod
    def generate(cls, label: str) -> "KeyPair":
        return cls(label, Ed25519PrivateKey.generate())

    @property
    def pub_raw(self) -> bytes:
        return self.sk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    @property
    def fp(self) -> str:
        return fingerprint(self.alg, self.pub_raw)

    def sign(self, msg: bytes) -> bytes:
        return self.sk.sign(msg)


class DSKSOracle:
    """TEST-ONLY emulation of the symbolic `dsks(s, r)` constructor (library rewrite: a key
    derived from one seen signature s under which s verifies, over s's ORIGINAL message only).

    `derive(honest_pub, sig)` returns a fresh KeyPair the adversary fully holds (it can sign
    under it, as the trace's possession proof `sign((POSS, ...), dsks(...))` requires), and
    registers that `sig` -- and only `sig` -- also verifies under the derived public key for
    whatever message `sig` verifies under `honest_pub`. Nothing else is granted (R-2.43).
    """

    def __init__(self):
        self._map: dict[tuple[bytes, bytes], tuple[bytes, str]] = {}
        self.uses: list[tuple[str, bool]] = []

    def derive(self, honest_pub_raw: bytes, sig: bytes, label: str = "dsks", honest_alg: str = ALG_ED25519) -> KeyPair:
        kp = KeyPair.generate(label)
        self._map[(kp.pub_raw, sig)] = (honest_pub_raw, honest_alg)
        return kp

    def lookup(self, pub_raw: bytes, sig: bytes) -> tuple[bytes, str] | None:
        return self._map.get((pub_raw, sig))


def _verify_plain(alg: str, pub_raw: bytes, sig: bytes, msg: bytes) -> bool:
    if alg in EXTRA_VERIFIERS:
        return EXTRA_VERIFIERS[alg](pub_raw, sig, msg)
    if alg != ALG_ED25519:
        raise ValueError("unsupported algorithm reached verify()")
    try:
        Ed25519PublicKey.from_public_bytes(pub_raw).verify(sig, msg)
        return True
    except (InvalidSignature, ValueError):
        return False


def verify(alg: str, pub_raw: bytes, sig: bytes, msg: bytes, dsks: DSKSOracle | None = None) -> bool:
    if _verify_plain(alg, pub_raw, sig, msg):
        return True
    if dsks is not None:
        found = dsks.lookup(pub_raw, sig)
        if found is not None:
            orig, orig_alg = found
            if _verify_plain(orig_alg, orig, sig, msg):
                dsks.uses.append(("dsks-accepted", True))
                return True
            dsks.uses.append(("dsks-message-mismatch", False))
            return False
    return False
