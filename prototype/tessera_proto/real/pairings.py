"""Item 2: which KMS + GPG pairings can form one two-signer receipt under R-3.12. THROWAWAY.

R-2.1 / R-4.13: "KMS ... and local GPG counter-signs ... Both signatures cover the same canonical bytes."
R-3.12: the six non-fingerprint fields -- including the ALGORITHM -- are equal across signer slots;
the authority tuple carries one `alg`.

Pairings built here, each verified by the phase-1 verifier (+ real algorithms):

  P1  KMS ECDSA_SHA_256 (RAW, over the frame)  +  gpg nistp256 OpenPGP detached signature
      -> one alg id cannot describe both: the OpenPGP signature is over frame || trailer.
  P2  KMS ECDSA_SHA_256                         +  gpg ed25519 (gpg 2.4's default key type)
      -> different curves, different schemes.
  P3  KMS ECDSA_SHA_256                         +  gpg-agent PKSIGN over SHA-256(frame), nistp256 key
      -> same alg id, same bytes; VALID. But the GPG slot is no longer an OpenPGP signature: no
         packet, no trailer, nothing gpg --verify can check. The "portable WHO layer" is a raw
         ECDSA signature from a key that happens to live in a GPG keyring.
  P4  KMS-backed OpenPGP (KMS DIGEST over SHA-256(frame || trailer)) + gpg nistp256 OpenPGP
      -> same alg id OPENPGP4-ECDSA-P256-SHA256; VALID; both signatures gpg-verifiable. The KMS custodian
         signs a 32-byte digest it cannot interpret. This is the de-stubbed world's choice.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

from .. import frame, objects
from ..crypto import b64e
from ..issuer import ChainSchedule, anchor_layer, build_attest_layer
from . import openpgp as P
from .gpg import ALG_PGP_ED25519, ALG_PGP_P256, GpgHome, GpgSlotKey, KmsOpenPGPSlotKey
from .kms import ALG_ECDSA, KmsSlotKey


@dataclass
class GpgAgentSlotKey:
    """A nistp256 key held by gpg-agent, used through PKSIGN on SHA-256(msg): a raw ECDSA-P256-SHA256
    signature (DER) with an SPKI public key -- the same shape as KMS's."""
    label: str
    inner: GpgSlotKey
    alg: str = ALG_ECDSA

    @classmethod
    def generate(cls, label: str, home: GpgHome) -> "GpgAgentSlotKey":
        return cls(label, GpgSlotKey.generate(label, home, ALG_PGP_P256))

    @property
    def pub_raw(self) -> bytes:
        k = P.first_public_key(self.inner.pub_raw).crypto_key()
        return k.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

    @property
    def fp(self) -> str:
        from ..crypto import fingerprint
        return fingerprint(self.alg, self.pub_raw)

    def sign(self, msg: bytes) -> bytes:
        r, s = self.inner.home.agent_pksign(self.inner.fpr, hashlib.sha256(msg).digest())
        return utils.encode_dss_signature(r, s)


def build_pair_layer(world, slot_keys, content: dict, declared: int, per_slot_alg: bool) -> dict:
    """An honest two-slot layer. per_slot_alg=False follows R-3.12 (one alg, slot A's); True presents
    each slot under its own algorithm id (what a KMS+GPG issuer would naturally do)."""
    layer = build_attest_layer(object_type="OT_ATTEST", content=content, declared=declared,
                               issuer_id=world.issuer.issuer_id, slot_keys=slot_keys,
                               channels=world.channels if hasattr(world, "channels") else [world.dns, world.repo],
                               alg=slot_keys[0].alg)
    if per_slot_alg:
        for s, k in zip(layer["slots"], slot_keys):
            s["alg"] = k.alg
    layer["anchor"] = anchor_layer(layer, world.chain, declared, ChainSchedule(), world.params.k)
    return {"bundle_format": "tessera-proto-bundle/0", "layers": [layer], "embedded": objects.embedded_objects()}


def pairings(home: GpgHome) -> dict:
    return {
        "P1 KMS-ECDSA + gpg-OpenPGP(P-256)": [KmsSlotKey.generate("kms"), GpgSlotKey.generate("gpgP", home, ALG_PGP_P256)],
        "P2 KMS-ECDSA + gpg-OpenPGP(Ed25519)": [KmsSlotKey.generate("kms"), GpgSlotKey.generate("gpgE", home, ALG_PGP_ED25519)],
        "P3 KMS-ECDSA + gpg-agent raw ECDSA": [KmsSlotKey.generate("kms"), GpgAgentSlotKey.generate("agent", home)],
        "P4 KMS-OpenPGP + gpg-OpenPGP(P-256)": [KmsOpenPGPSlotKey.generate("kmsP"), GpgSlotKey.generate("gpgP2", home, ALG_PGP_P256)],
    }
