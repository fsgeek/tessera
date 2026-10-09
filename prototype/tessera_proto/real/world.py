"""The de-stubbed world (THROWAWAY): same shape as tessera_proto.world.World.

  slot A ("KMS")  KmsOpenPGPSlotKey: ECDSA P-256 private key in emulated KMS, OpenPGP v4 signature
                  packets assembled locally, KMS called with MessageType=DIGEST
  slot B ("GPG")  GpgSlotKey: a real nistp256 key in /usr/bin/gpg (throwaway GNUPGHOME)
                  -> both slots carry alg OPENPGP4-ECDSA-P256-SHA256, the only pairing found that
                     satisfies R-3.12's equal-algorithm rule while keeping the GPG signature a real,
                     gpg-verifiable OpenPGP signature (see PHASE3-REPORT, item 2)
  anchor          RegtestOtsChain: real OTS proof format, real Bitcoin header/tx/merkle format,
                  REGTEST difficulty, two calendars
  channels        STILL STUBBED (Ed25519 channel keys): wamason.com has no DNSSEC today, and the git
                  channel's real evidence is analysed separately (real/dnssec.py, real/gitchannel.py)
"""
from __future__ import annotations

from ..crypto import KeyPair
from ..issuer import Channel, Issuer, Params
from ..world import T0, World
from . import algs, canonical
from .gpg import GpgHome, GpgSlotKey, KmsOpenPGPSlotKey
from .ots import RegtestOtsChain

_HOME: GpgHome | None = None


def gpg_home() -> GpgHome:
    global _HOME
    if _HOME is None:
        import atexit
        _HOME = GpgHome()
        atexit.register(close)   # remove the throwaway GNUPGHOME even if the caller forgets
    return _HOME


def close():
    global _HOME
    if _HOME is not None:
        _HOME.close()
        _HOME = None


def make_world_real(issuer_id: str = "wamason.com", params: Params | None = None,
                    number_rule: str = "value-preserving") -> World:
    algs.register()
    canonical.set_number_rule(number_rule)
    p = params or Params()
    chain = RegtestOtsChain(T0 - 3600)
    skI = KmsOpenPGPSlotKey.generate("skI-kms", created=T0 - 86400)
    skB2 = GpgSlotKey.generate("skB2-gpg", gpg_home())
    dns, repo = Channel("dns", KeyPair.generate("skS-dns")), Channel("repo", KeyPair.generate("skR-repo"))
    iss = Issuer(issuer_id, [skI, skB2], [dns, repo], chain, p)
    return World(chain, skI, skB2, dns, repo, iss, p)
