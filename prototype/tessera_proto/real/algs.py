"""Register the real signature algorithms with the phase-1 verifier (THROWAWAY).

  ECDSA-P256-SHA256               KMS ECDSA_SHA_256 (DER signature over the frame; SPKI public key)
  RSA-PSS-SHA256                  KMS RSASSA_PSS_SHA_256 (salt 32)
  OPENPGP4-ECDSA-P256-SHA256      an OpenPGP v4 signature packet whose DOCUMENT is the frame
  OPENPGP4-EDDSA-ED25519-SHA256   the same with a legacy EdDSA (Ed25519) key, gpg 2.4's default

Registration is global and idempotent; the phase-1 Ed25519 path is unchanged, so registering does
not move any phase-1/2 verdict (the stub world never uses these ids).
"""
from __future__ import annotations

from .. import crypto
from . import gpg, kms

REAL_ALGS = (kms.ALG_ECDSA, kms.ALG_RSAPSS, gpg.ALG_PGP_P256, gpg.ALG_PGP_ED25519)


def register() -> None:
    crypto.EXTRA_VERIFIERS[kms.ALG_ECDSA] = lambda pub, sig, msg: kms.verify_spki(kms.ALG_ECDSA, pub, sig, msg)
    crypto.EXTRA_VERIFIERS[kms.ALG_RSAPSS] = lambda pub, sig, msg: kms.verify_spki(kms.ALG_RSAPSS, pub, sig, msg)
    for a in (gpg.ALG_PGP_P256, gpg.ALG_PGP_ED25519):
        crypto.EXTRA_VERIFIERS[a] = (lambda alg: lambda pub, sig, msg: gpg.verify_openpgp_slot(alg, pub, sig, msg))(a)
    crypto.ALGS_SUPPORTED.update(REAL_ALGS)
    crypto.ALGS_KNOWN_UNSUPPORTED.difference_update(REAL_ALGS)
