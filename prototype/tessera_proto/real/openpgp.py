"""OpenPGP v4 packets (RFC 4880 §5.2, §5.5, §12.2; RFC 9580 §5.2.4 for v4). THROWAWAY.

Just enough to answer "exactly which bytes does an OpenPGP signature sign?" and to verify gpg's
output with `cryptography` alone (no gpg at verification time):

  v4 signature over a binary document (sigtype 0x00):
      digest = H( document || hashed_header || 0x04 0xFF || be32(len(hashed_header)) )
      hashed_header = version(4) | sigtype | pubkey_alg | hash_alg | be16(len(hashed_subpackets)) | hashed_subpackets
  The key then signs `digest`, NOT the document:
      ECDSA (alg 19):      ECDSA over the digest (the digest is the "hash" input of ECDSA)
      EdDSA legacy (22):   PureEdDSA (Ed25519) over the DIGEST BYTES as its message
      RSA (1):             PKCS#1 v1.5 over the digest
  The unhashed subpacket area is NOT signed: anyone can rewrite it and the signature still verifies.

Also builds signatures (for the KMS-backed OpenPGP signer) and v4 public-key packets + fingerprints.
"""
from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa, utils
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

PK_RSA, PK_ECDSA, PK_EDDSA_LEGACY, PK_ED25519_V6 = 1, 19, 22, 27
H_SHA256, H_SHA512 = 8, 10
HASHES = {H_SHA256: hashlib.sha256, H_SHA512: hashlib.sha512, 9: hashlib.sha384, 2: hashlib.sha1}
CRYPTO_HASH = {H_SHA256: hashes.SHA256, H_SHA512: hashes.SHA512, 9: hashes.SHA384}
OID_P256 = bytes.fromhex("2a8648ce3d030107")
OID_ED25519_LEGACY = bytes.fromhex("2b06010401da470f01")

SUB_CREATION_TIME, SUB_ISSUER_KEYID, SUB_ISSUER_FPR, SUB_KEY_FLAGS = 2, 16, 33, 27


class PGPError(ValueError):
    pass


# ------------------------------------------------------------------ packet framing

def iter_packets(data: bytes):
    """Yield (tag, body, raw_packet_bytes). Old and new format; no partial lengths."""
    i = 0
    while i < len(data):
        start = i
        h = data[i]
        if not h & 0x80:
            raise PGPError("not a packet header")
        if h & 0x40:  # new format
            tag = h & 0x3F
            i += 1
            o = data[i]
            if o < 192:
                ln, i = o, i + 1
            elif o < 224:
                ln, i = ((o - 192) << 8) + data[i + 1] + 192, i + 2
            elif o == 255:
                ln, i = struct.unpack(">I", data[i + 1:i + 5])[0], i + 5
            else:
                raise PGPError("partial body lengths not supported")
        else:
            tag = (h >> 2) & 0x0F
            lt = h & 3
            i += 1
            if lt == 0:
                ln, i = data[i], i + 1
            elif lt == 1:
                ln, i = struct.unpack(">H", data[i:i + 2])[0], i + 2
            elif lt == 2:
                ln, i = struct.unpack(">I", data[i:i + 4])[0], i + 4
            else:
                raise PGPError("indeterminate length")
        body = data[i:i + ln]
        i += ln
        yield tag, body, data[start:i]


def new_packet(tag: int, body: bytes) -> bytes:
    n = len(body)
    if n < 192:
        ln = bytes([n])
    elif n < 8384:
        n2 = n - 192
        ln = bytes([(n2 >> 8) + 192, n2 & 0xFF])
    else:
        ln = b"\xff" + struct.pack(">I", n)
    return bytes([0xC0 | tag]) + ln + body


def mpi(x: int | bytes) -> bytes:
    if isinstance(x, bytes):
        x = int.from_bytes(x, "big")
    bits = x.bit_length()
    return struct.pack(">H", bits) + x.to_bytes((bits + 7) // 8, "big")


def read_mpi(b: bytes, off: int) -> tuple[int, int]:
    bits = struct.unpack(">H", b[off:off + 2])[0]
    n = (bits + 7) // 8
    return int.from_bytes(b[off + 2:off + 2 + n], "big"), off + 2 + n


def subpacket(typ: int, data: bytes, critical: bool = False) -> bytes:
    body = bytes([typ | (0x80 if critical else 0)]) + data
    n = len(body)
    assert n < 192
    return bytes([n]) + body


def parse_subpackets(b: bytes) -> list[tuple[int, bytes]]:
    out, i = [], 0
    while i < len(b):
        o = b[i]
        if o < 192:
            n, i = o, i + 1
        elif o < 255:
            n, i = ((o - 192) << 8) + b[i + 1] + 192, i + 2
        else:
            n, i = struct.unpack(">I", b[i + 1:i + 5])[0], i + 5
        out.append((b[i] & 0x7F, b[i + 1:i + n]))
        i += n
    return out


# ------------------------------------------------------------------ public keys

@dataclass
class PublicKey:
    body: bytes               # the v4 public-key packet body (what the fingerprint covers)
    created: int
    alg: int
    point_or_n: bytes | int
    e: int | None = None

    @property
    def fingerprint_v4(self) -> str:
        """RFC 4880 §12.2: SHA-1(0x99 || be16(len) || body). Covers the creation time."""
        return hashlib.sha1(b"\x99" + struct.pack(">H", len(self.body)) + self.body).hexdigest().upper()

    @property
    def key_id(self) -> bytes:
        return bytes.fromhex(self.fingerprint_v4)[-8:]

    def crypto_key(self):
        if self.alg == PK_ECDSA:
            return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), self.point_or_n)
        if self.alg == PK_EDDSA_LEGACY:
            assert self.point_or_n[0] == 0x40
            return Ed25519PublicKey.from_public_bytes(self.point_or_n[1:])
        if self.alg == PK_RSA:
            return rsa.RSAPublicNumbers(self.e, self.point_or_n).public_key()
        raise PGPError(f"pubkey alg {self.alg} not supported here")


def parse_public_key_body(body: bytes) -> PublicKey:
    if body[0] != 4:
        raise PGPError(f"public key version {body[0]} (only v4 here; gpg 2.4 does not make v6 keys)")
    created = struct.unpack(">I", body[1:5])[0]
    alg = body[5]
    if alg in (PK_ECDSA, PK_EDDSA_LEGACY):
        ol = body[6]
        oid = body[7:7 + ol]
        point, _ = read_mpi(body, 7 + ol)
        nbytes = 65 if alg == PK_ECDSA else 33
        if alg == PK_ECDSA and oid != OID_P256:
            raise PGPError("only NIST P-256 here")
        return PublicKey(body, created, alg, point.to_bytes(nbytes, "big"))
    if alg == PK_RSA:
        n, off = read_mpi(body, 6)
        e, _ = read_mpi(body, off)
        return PublicKey(body, created, alg, n, e)
    raise PGPError(f"pubkey alg {alg} not supported here")


def first_public_key(data: bytes) -> PublicKey:
    for tag, body, _ in iter_packets(data):
        if tag == 6:
            return parse_public_key_body(body)
    raise PGPError("no public-key packet")


def ecdsa_p256_key_body(pub: ec.EllipticCurvePublicKey, created: int) -> bytes:
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    point = pub.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    return b"\x04" + struct.pack(">I", created) + bytes([PK_ECDSA, len(OID_P256)]) + OID_P256 + mpi(point)


# ------------------------------------------------------------------ signatures

@dataclass
class Signature:
    raw: bytes                     # the whole signature packet (header included)
    version: int
    sigtype: int
    pk_alg: int
    hash_alg: int
    hashed_area: bytes
    unhashed_area: bytes
    left16: bytes
    mpis: list[int] = field(default_factory=list)

    @property
    def hashed_header(self) -> bytes:
        return bytes([self.version, self.sigtype, self.pk_alg, self.hash_alg]) + \
            struct.pack(">H", len(self.hashed_area)) + self.hashed_area

    def trailer(self) -> bytes:
        """The bytes appended to the document before hashing (RFC 4880 §5.2.4, v4)."""
        hh = self.hashed_header
        return hh + b"\x04\xff" + struct.pack(">I", len(hh))

    def signed_message(self, document: bytes) -> bytes:
        """EXACTLY the byte string that goes into the hash: document || trailer."""
        return document + self.trailer()

    def digest(self, document: bytes) -> bytes:
        return HASHES[self.hash_alg](self.signed_message(document)).digest()

    def hashed_subpackets(self) -> dict[int, bytes]:
        return dict(parse_subpackets(self.hashed_area))

    def unhashed_subpackets(self) -> dict[int, bytes]:
        return dict(parse_subpackets(self.unhashed_area))

    @property
    def creation_time(self) -> int | None:
        v = self.hashed_subpackets().get(SUB_CREATION_TIME)
        return struct.unpack(">I", v)[0] if v else None

    @property
    def issuer_fpr(self) -> str | None:
        v = self.hashed_subpackets().get(SUB_ISSUER_FPR)
        return v[1:].hex().upper() if v else None

    def with_unhashed(self, unhashed: bytes) -> "Signature":
        """Rewrite the UNSIGNED subpacket area -- something any third party can do."""
        body = self.hashed_header + struct.pack(">H", len(unhashed)) + unhashed + self.left16 + \
            b"".join(mpi(x) for x in self.mpis)
        return parse_signature(new_packet(2, body))

    def with_mpis(self, mpis: list[int]) -> "Signature":
        body = self.hashed_header + struct.pack(">H", len(self.unhashed_area)) + self.unhashed_area + \
            self.left16 + b"".join(mpi(x) for x in mpis)
        return parse_signature(new_packet(2, body))


def parse_signature(data: bytes) -> Signature:
    for tag, body, raw in iter_packets(data):
        if tag != 2:
            continue
        if body[0] != 4:
            raise PGPError(f"signature version {body[0]} (only v4 here)")
        ver, st, pka, ha = body[0], body[1], body[2], body[3]
        hl = struct.unpack(">H", body[4:6])[0]
        hashed = body[6:6 + hl]
        off = 6 + hl
        ul = struct.unpack(">H", body[off:off + 2])[0]
        unhashed = body[off + 2:off + 2 + ul]
        off += 2 + ul
        left16 = body[off:off + 2]
        off += 2
        mpis = []
        while off < len(body):
            x, off = read_mpi(body, off)
            mpis.append(x)
        return Signature(raw, ver, st, pka, ha, hashed, unhashed, left16, mpis)
    raise PGPError("no signature packet")


def verify(sig: Signature, key: PublicKey, document: bytes) -> bool:
    """Verify an OpenPGP v4 binary-document signature with `cryptography` only."""
    if sig.sigtype != 0x00 or sig.pk_alg != key.alg or sig.hash_alg not in HASHES:
        return False
    d = sig.digest(document)
    if d[:2] != sig.left16:
        return False
    k = key.crypto_key()
    try:
        if key.alg == PK_ECDSA:
            r, s = sig.mpis
            k.verify(utils.encode_dss_signature(r, s), d, ec.ECDSA(utils.Prehashed(CRYPTO_HASH[sig.hash_alg]())))
        elif key.alg == PK_EDDSA_LEGACY:
            r, s = sig.mpis
            k.verify(r.to_bytes(32, "big") + s.to_bytes(32, "big"), d)   # Ed25519 over the DIGEST
        elif key.alg == PK_RSA:
            (s,) = sig.mpis
            k.verify(s.to_bytes((key.point_or_n.bit_length() + 7) // 8, "big"), d, padding.PKCS1v15(),
                     utils.Prehashed(CRYPTO_HASH[sig.hash_alg]()))
        else:
            return False
        return True
    except (InvalidSignature, ValueError):
        return False


def build_signature(document: bytes, key: PublicKey, created: int, sign_digest, hash_alg: int = H_SHA256,
                    sigtype: int = 0x00, extra_hashed: bytes = b"") -> bytes:
    """Build a v4 signature packet. `sign_digest(digest) -> (r, s)` is the only place the private key
    acts -- for the KMS-backed signer it is a KMS Sign call with MessageType=DIGEST."""
    fpr = bytes.fromhex(key.fingerprint_v4)
    hashed = subpacket(SUB_ISSUER_FPR, b"\x04" + fpr) + subpacket(SUB_CREATION_TIME, struct.pack(">I", created)) + extra_hashed
    unhashed = subpacket(SUB_ISSUER_KEYID, key.key_id)
    proto = Signature(b"", 4, sigtype, key.alg, hash_alg, hashed, unhashed, b"", [])
    d = HASHES[hash_alg](document + proto.trailer()).digest()
    r, s = sign_digest(d)
    body = proto.hashed_header + struct.pack(">H", len(unhashed)) + unhashed + d[:2] + mpi(r) + mpi(s)
    return new_packet(2, body)


def certification_message(key: PublicKey, uid: bytes) -> bytes:
    """What a user-ID self-certification (0x13) hashes before its trailer (RFC 4880 §5.2.4)."""
    return b"\x99" + struct.pack(">H", len(key.body)) + key.body + b"\xb4" + struct.pack(">I", len(uid)) + uid


def transferable_public_key(key: PublicKey, uid: bytes, created: int, sign_digest) -> bytes:
    """Key packet + user ID + positive self-certification, so `gpg --import` accepts a key whose
    private half lives in (emulated) KMS."""
    msg = certification_message(key, uid)
    flags = subpacket(SUB_KEY_FLAGS, b"\x03")  # certify + sign
    sig = build_signature(msg, key, created, sign_digest, sigtype=0x13, extra_hashed=flags)
    return new_packet(6, key.body) + new_packet(13, uid) + sig
