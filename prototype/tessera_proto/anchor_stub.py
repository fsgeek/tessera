"""*** STUB ANCHOR *** -- a local hash chain standing in for OpenTimestamps + Bitcoin (§3.5, §4.5).

NOT OpenTimestamps, NOT Bitcoin, no proof of work, no network. Blocks are mined on demand at
caller-chosen timestamps so tests can drive the temporal predicate. The proof format below is
GUESS G-20 (OTS proof structure is out of scope here).

Header:  {"height", "prev", "time", "merkle_root"}; header hash = sha256(JCS(header)).
Proof:   {"digest", "txid", "height", "path": [["L"|"R", hex], ...]}  (path to merkle_root)
txid:    double-SHA-256 of b"STUB-TX" || digest   (R-3.42's "identity handle", stub form)
"""
from __future__ import annotations

from . import jcs
from .crypto import sha256, sha256_hex


def header_hash(h: dict) -> str:
    return sha256_hex(jcs.canonicalize(h))


def txid_for(digest_hex: str) -> str:
    return sha256(sha256(b"STUB-TX" + bytes.fromhex(digest_hex))).hex()


def _merkle(leaves: list[bytes]) -> tuple[bytes, list[list[tuple[str, bytes]]]]:
    if not leaves:
        return sha256(b""), []
    paths: list[list[tuple[str, bytes]]] = [[] for _ in leaves]
    level = [(leaf, [i]) for i, leaf in enumerate(leaves)]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            a, ia = level[i]
            if i + 1 < len(level):
                b, ib = level[i + 1]
            else:
                b, ib = a, []
            for j in ia:
                paths[j].append(("R", b))
            for j in ib:
                paths[j].append(("L", a))
            nxt.append((sha256(a + b), ia + ib))
        level = nxt
    return level[0][0], paths


def leaf_for(txid_hex: str) -> bytes:
    return sha256(b"STUB-LEAF" + bytes.fromhex(txid_hex))


def merkle_root_from_path(txid_hex: str, path: list) -> str:
    cur = leaf_for(txid_hex)
    for side, sib_hex in path:
        sib = bytes.fromhex(sib_hex)
        cur = sha256(cur + sib) if side == "R" else sha256(sib + cur)
    return cur.hex()


class StubChain:
    def __init__(self, genesis_time: int):
        g = {"height": 0, "prev": "00" * 32, "time": genesis_time, "merkle_root": sha256(b"").hex()}
        self.headers: list[dict] = [g]
        self.pending: list[str] = []  # digests
        self.proofs: dict[str, dict] = {}

    @property
    def tip(self) -> int:
        return len(self.headers) - 1

    def submit(self, digest_hex: str) -> str:
        self.pending.append(digest_hex)
        return txid_for(digest_hex)

    def mine(self, time: int) -> dict:
        txids = [txid_for(d) for d in self.pending]
        root, paths = _merkle([leaf_for(t) for t in txids])
        h = {"height": self.tip + 1, "prev": header_hash(self.headers[-1]), "time": time,
             "merkle_root": root.hex()}
        self.headers.append(h)
        for d, t, p in zip(self.pending, txids, paths):
            self.proofs[d] = {"digest": d, "txid": t, "height": h["height"],
                              "path": [[s, x.hex()] for s, x in p]}
        self.pending = []
        return h

    def proof(self, digest_hex: str) -> dict | None:
        return self.proofs.get(digest_hex)

    def segment(self, h: int, k: int) -> list[dict] | None:
        if h + k - 1 > self.tip:
            return None
        return [dict(x) for x in self.headers[h:h + k]]

    def header_store(self) -> dict[int, str]:
        """What a verifier-distributed header store (R-2.19) would ship: height -> header hash."""
        return {x["height"]: header_hash(x) for x in self.headers}
