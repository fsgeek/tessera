"""OpenPGP v4 pieces for rule O (ENCODING-V1 §5.2): the P-256 key body and its fingerprints, and one detached
binary-document signature packet in the GnuPG 2.4 subpacket layout (hashed {33 issuer fingerprint, 2 creation time},
unhashed {16 issuer key id}), the layout the issuer's stand-in signer produces."""
import hashlib
import struct

P256_OID = bytes.fromhex("2a8648ce3d030107")


def point65(public_key):
    """cryptography EC public key -> uncompressed SEC1 point (65 bytes)."""
    n = public_key.public_numbers()
    return b"\x04" + n.x.to_bytes(32, "big") + n.y.to_bytes(32, "big")


def key_body(point, created):
    """The v4 public-key packet body (RFC 9580 §5.5.2) for ECDSA P-256; `created` is bound into the fingerprints."""
    return bytes([4]) + struct.pack(">I", created) + bytes([19, len(P256_OID)]) + P256_OID + struct.pack(">H", 515) + point


def fp_gpg(body):
    """The profile's gpg-sha256 fingerprint (ENCODING-V1 §4.3): SHA-256 of the body only."""
    return "gpg-sha256:" + hashlib.sha256(body).hexdigest()


def v4_fingerprint(body):
    """The OpenPGP v4 fingerprint (SHA-1 over 0x99, length, body), used only in subpackets 33 and 16."""
    return hashlib.sha1(b"\x99" + struct.pack(">H", len(body)) + body).digest()


def subpacket(typ, data):
    assert len(data) + 1 < 192
    return bytes([len(data) + 1, typ]) + data


def mpi(v):
    return struct.pack(">H", v.bit_length()) + v.to_bytes((v.bit_length() + 7) // 8, "big")


def hashed_area(fpr, created):
    return subpacket(33, b"\x04" + fpr) + subpacket(2, struct.pack(">I", created))


def sig_digest(document, hashed):
    """SHA-256 over the document, the hashed signature header and the v4 trailer: the digest the HSM signs."""
    head = bytes([4, 0x00, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
    return hashlib.sha256(document + head + b"\x04\xff" + struct.pack(">I", len(head))).digest()


def sig_packet(hashed, unhashed, left16, r, s):
    body = (bytes([4, 0x00, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
            + struct.pack(">H", len(unhashed)) + unhashed + left16 + mpi(r) + mpi(s))
    return (bytes([0x88, len(body)]) if len(body) <= 255 else bytes([0x89]) + struct.pack(">H", len(body))) + body
