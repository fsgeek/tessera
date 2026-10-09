"""A small local world: honest issuer, two stub channels, stub chain, verifier trust config."""
from __future__ import annotations

from dataclasses import dataclass

from .anchor_stub import StubChain
from .crypto import KeyPair
from .issuer import Channel, Issuer, Params
from .verifier import TrustConfig

T0 = 1_790_000_000  # 2026-09-21T...Z; arbitrary fixed epoch for determinism of times


@dataclass
class World:
    chain: StubChain
    skI: KeyPair     # slot A ("KMS" role; in-process here)
    skB2: KeyPair    # slot B ("GPG" counter-signer role; in-process here)
    dns: Channel     # STUB channel; its key plays the model's skS in degraded fixtures
    repo: Channel    # STUB channel
    issuer: Issuer
    params: Params

    def trust(self, **kw) -> TrustConfig:
        return TrustConfig(channel_keys={"dns": self.dns.key.pub_raw, "repo": self.repo.key.pub_raw},
                           k=self.params.k, delta=self.params.delta, epsilon=self.params.epsilon,
                           header_store=self.chain.header_store(), **kw)


def make_world(issuer_id: str = "wamason.com", params: Params | None = None) -> World:
    p = params or Params()
    chain = StubChain(T0 - 3600)
    skI, skB2 = KeyPair.generate("skI"), KeyPair.generate("skB2")
    dns, repo = Channel("dns", KeyPair.generate("skS-dns")), Channel("repo", KeyPair.generate("skR-repo"))
    iss = Issuer(issuer_id, [skI, skB2], [dns, repo], chain, p)
    return World(chain, skI, skB2, dns, repo, iss, p)
