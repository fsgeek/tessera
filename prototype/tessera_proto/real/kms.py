"""AWS-KMS-style asymmetric signing, emulated locally with `cryptography`. THROWAWAY. No AWS.

What is emulated (from AWS KMS's documented Sign API; behaviour NOT verified against AWS here):
  * key specs ECC_NIST_P256 and RSA_3072; GetPublicKey returns DER SubjectPublicKeyInfo;
  * signing algorithms ECDSA_SHA_256 (DER-encoded X9.62 signature, random nonce) and
    RSASSA_PSS_SHA_256 (MGF1-SHA-256, salt length = 32 = digest length);
  * MessageType RAW: KMS hashes the message itself; the message is limited to 4096 bytes;
  * MessageType DIGEST: the caller sends the 32-byte SHA-256 digest; KMS never sees the message.

The point for Tessera: with RAW, KMS signs the frame bytes. With DIGEST (forced for any frame over
4096 bytes), KMS signs a digest the caller computed, and the custody domain never sees what it signed.
Either way the resulting signature verifies over the frame with an ordinary ECDSA-P256-SHA256 /
RSA-PSS-SHA256 verifier, so "signs the frame bytes" holds at the verifier, not at the custodian.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa, utils

RAW_LIMIT = 4096
ALG_ECDSA = "ECDSA-P256-SHA256"
ALG_RSAPSS = "RSA-PSS-SHA256"
P256_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


class KmsValidationException(ValueError):
    pass


@dataclass
class KmsKey:
    key_spec: str                       # "ECC_NIST_P256" | "RSA_3072"
    _sk: object = field(repr=False, default=None)
    calls: list = field(default_factory=list, repr=False)   # audit trail: what the custodian saw

    @classmethod
    def create(cls, key_spec: str) -> "KmsKey":
        if key_spec == "ECC_NIST_P256":
            sk = ec.generate_private_key(ec.SECP256R1())
        elif key_spec == "RSA_3072":
            sk = rsa.generate_private_key(public_exponent=65537, key_size=3072)
        else:
            raise KmsValidationException(key_spec)
        return cls(key_spec, sk)

    def get_public_key(self) -> bytes:
        return self._sk.public_key().public_bytes(serialization.Encoding.DER,
                                                  serialization.PublicFormat.SubjectPublicKeyInfo)

    def sign(self, message: bytes, message_type: str, signing_algorithm: str) -> bytes:
        if message_type == "RAW" and len(message) > RAW_LIMIT:
            raise KmsValidationException(f"RAW message is {len(message)} bytes; limit {RAW_LIMIT}")
        if message_type == "DIGEST" and len(message) != 32:
            raise KmsValidationException("DIGEST must be 32 bytes for a SHA-256 algorithm")
        self.calls.append({"type": message_type, "len": len(message), "alg": signing_algorithm,
                           "saw": message if message_type == "DIGEST" else hashlib.sha256(message).digest()})
        h = hashes.SHA256()
        if signing_algorithm == "ECDSA_SHA_256":
            alg = ec.ECDSA(h) if message_type == "RAW" else ec.ECDSA(utils.Prehashed(h))
            return self._sk.sign(message, alg)
        if signing_algorithm == "RSASSA_PSS_SHA_256":
            pad = padding.PSS(mgf=padding.MGF1(h), salt_length=32)
            return self._sk.sign(message, pad, h if message_type == "RAW" else utils.Prehashed(h))
        raise KmsValidationException(signing_algorithm)


def verify_spki(alg: str, spki_der: bytes, sig: bytes, msg: bytes) -> bool:
    try:
        pub = serialization.load_der_public_key(spki_der)
        if alg == ALG_ECDSA:
            pub.verify(sig, msg, ec.ECDSA(hashes.SHA256()))
        elif alg == ALG_RSAPSS:
            pub.verify(sig, msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32), hashes.SHA256())
        else:
            return False
        return True
    except (InvalidSignature, ValueError):
        return False


def ecdsa_malleate(der_sig: bytes) -> bytes:
    """(r, s) -> (r, n - s): a second valid ECDSA signature on the same message, computable by ANYONE
    from the first. FIPS 186 / X9.62 ECDSA (and so KMS, and OpenSSL's verifier) accept both."""
    r, s = utils.decode_dss_signature(der_sig)
    return utils.encode_dss_signature(r, P256_N - s)


@dataclass
class KmsSlotKey:
    """A signer-slot key in the phase-1 KeyPair shape, backed by the emulated KMS key.

    pub_raw is the DER SPKI (what KMS GetPublicKey returns). Frames up to 4096 bytes go as RAW, larger
    ones as DIGEST -- which a real issuer would be forced into for any inline SBOM of size."""
    label: str
    kms: KmsKey
    alg: str = ALG_ECDSA
    force_digest: bool = False

    @classmethod
    def generate(cls, label: str, alg: str = ALG_ECDSA, **kw) -> "KmsSlotKey":
        return cls(label, KmsKey.create("ECC_NIST_P256" if alg == ALG_ECDSA else "RSA_3072"), alg, **kw)

    @property
    def pub_raw(self) -> bytes:
        return self.kms.get_public_key()

    @property
    def fp(self) -> str:
        from ..crypto import fingerprint
        return fingerprint(self.alg, self.pub_raw)

    def sign(self, msg: bytes) -> bytes:
        sa = "ECDSA_SHA_256" if self.alg == ALG_ECDSA else "RSASSA_PSS_SHA_256"
        if self.force_digest or len(msg) > RAW_LIMIT:
            return self.kms.sign(hashlib.sha256(msg).digest(), "DIGEST", sa)
        return self.kms.sign(msg, "RAW", sa)
