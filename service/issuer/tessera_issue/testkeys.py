"""TEST-ONLY keys for the stand-in signers, the stand-in DNS hierarchy, the stand-in repository key and the TEST
release key. Every key is derived from a public seed string and protects nothing. Adapted (copied, then rewritten
onto `cryptography`) from the conformance universe's TEST cryptography module.

Nothing in the issuer's production path uses this module: only the stand-in implementations and tests do."""
import base64
import hashlib
import struct

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, mldsa, utils

from .encode import MLDSA65_SPKI_PREFIX, fp_gpg, fp_kms, openpgp_v4_body

N_P256 = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
P256_SPKI_PREFIX = bytes.fromhex("3059301306072a8648ce3d020106082a8648ce3d030107034200")


def drbg(seed, n):
    """Deterministic bytes: SHA-256 in counter mode over a TEST seed string."""
    out, i = b"", 0
    while len(out) < n:
        out += hashlib.sha256(f"TEST|{seed}|{i}".encode()).digest()
        i += 1
    return out[:n]


class P256Key:
    """A TEST P-256 key (d from the seed)."""

    def __init__(self, seed, created=1790000000):
        self.seed, self.created = seed, created
        d = int.from_bytes(drbg("p256:" + seed, 32), "big") % (N_P256 - 1) + 1
        self._priv = ec.derive_private_key(d, ec.SECP256R1())
        nums = self._priv.public_key().public_numbers()
        self.x, self.y = nums.x, nums.y
        self.point = b"\x04" + nums.x.to_bytes(32, "big") + nums.y.to_bytes(32, "big")

    @property
    def spki(self):
        return P256_SPKI_PREFIX + self.point

    @property
    def pgp_body(self):
        return openpgp_v4_body(self.point, self.created)

    @property
    def fp_gpg(self):
        return fp_gpg(self.pgp_body)

    @property
    def v4_fpr_sha1(self):
        body = self.pgp_body
        return hashlib.sha1(b"\x99" + struct.pack(">H", len(body)) + body).digest()

    def sign_digest(self, h):
        """-> (r, s) over a 32-byte digest."""
        der = self._priv.sign(h, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return utils.decode_dss_signature(der)

    def sign_raw(self, data):
        """DNSSEC algorithm 13 / TEST release form: r || s over SHA-256(data)."""
        r, s = self.sign_digest(hashlib.sha256(data).digest())
        return r.to_bytes(32, "big") + s.to_bytes(32, "big")


class MLDSA65Key:
    """A TEST ML-DSA-65 key for the kms slot: pure ML-DSA, empty context (rule R), DER SPKI transported key."""

    def __init__(self, seed):
        self.seed = seed
        self._priv = mldsa.MLDSA65PrivateKey.from_seed_bytes(drbg("mldsa65:" + seed, 32))
        self._pub = self._priv.public_key()
        self.spki = self._pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        if self.spki[:22] != MLDSA65_SPKI_PREFIX or len(self.spki) != 1974:
            raise AssertionError("unexpected ML-DSA-65 SPKI layout")

    @property
    def fp_kms(self):
        return fp_kms(self.spki)

    def sign(self, msg):
        sig = self._priv.sign(msg, context=b"")
        self._pub.verify(sig, msg, context=b"")
        return sig


# ------------------------------------------------------------------------------------------- OpenPGP rule O
def subpacket(typ, data):
    n = len(data) + 1
    if n < 192:
        ln = bytes([n])
    elif n < 16320:
        n2 = n - 192
        ln = bytes([(n2 >> 8) + 192, n2 & 0xFF])
    else:
        ln = b"\xff" + struct.pack(">I", n)
    return ln + bytes([typ]) + data


def mpi(v):
    return struct.pack(">H", v.bit_length()) + v.to_bytes((v.bit_length() + 7) // 8, "big")


def pgp_sign(doc, key, sig_created):
    """Detached v4 ECDSA P-256 SHA-256 binary-document signature, GnuPG 2.4 subpacket layout:
    hashed {33 issuer fingerprint, 2 creation time}, unhashed {16 issuer key id}."""
    hashed = subpacket(33, b"\x04" + key.v4_fpr_sha1) + subpacket(2, struct.pack(">I", sig_created))
    unhashed = subpacket(16, key.v4_fpr_sha1[-8:])
    head = bytes([4, 0, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
    h = hashlib.sha256(doc + head + b"\x04\xff" + struct.pack(">I", len(head))).digest()
    r, s = key.sign_digest(h)
    body = head + struct.pack(">H", len(unhashed)) + unhashed + h[:2] + mpi(r) + mpi(s)
    return (bytes([0x88, len(body)]) if len(body) <= 255 else bytes([0x89]) + struct.pack(">H", len(body))) + body


def crc24(data):
    crc = 0xB704CE
    for b in data:
        crc ^= b << 16
        for _ in range(8):
            crc <<= 1
            if crc & 0x1000000:
                crc ^= 0x1864CFB
    return crc & 0xFFFFFF


def armor(sig):
    b64 = base64.b64encode(sig).decode()
    lines = ["-----BEGIN PGP SIGNATURE-----", ""] + [b64[i:i + 64] for i in range(0, len(b64), 64)]
    lines += ["=" + base64.b64encode(crc24(sig).to_bytes(3, "big")).decode(), "-----END PGP SIGNATURE-----"]
    return "\n".join(lines)
