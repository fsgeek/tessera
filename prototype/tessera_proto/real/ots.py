"""OpenTimestamps (python-opentimestamps 0.4.5) against the spec's anchor semantics. THROWAWAY.

What an OTS proof is: a tree of commitment operations (append, prepend, sha256, ...) from
sha256(file) to one or more attestations. A BitcoinBlockHeaderAttestation(height) says "the message
reached here equals the merkle root of the block at `height`". Nothing else is in the proof: no
header, no time, no depth, no transaction id field. The transaction is visible only implicitly, as
the message just before a `sha256, sha256` pair that parses as a Bitcoin transaction.

Verifying one needs, from OUTSIDE the proof: the block header at each attested height (to compare
merkle roots and read nTime), and -- for anything about depth, canonicity or work -- the headers after
it and a reason to believe they are the real chain. That is the spec's "header store".

This module also builds real-format OTS proofs on the REGTEST chain (`RegtestOtsChain`), with the same
structure a calendar produces (per-stamp nonce, calendar merkle aggregation, OP_RETURN transaction,
block merkle path, Bitcoin attestation), and serves as the de-stubbed issuer's anchor.
"""
from __future__ import annotations

import base64
import hashlib
import io
import os
from dataclasses import dataclass, field

from bitcoin.core import CTransaction
from opentimestamps.core.notary import BitcoinBlockHeaderAttestation, PendingAttestation
from opentimestamps.core.op import OpAppend, OpPrepend, OpSHA256
from opentimestamps.core.serialize import BytesDeserializationContext, BytesSerializationContext
from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp, make_merkle_tree

from . import btc

FORMAT = "ots-bitcoin"


def load(data: bytes) -> DetachedTimestampFile:
    return DetachedTimestampFile.deserialize(BytesDeserializationContext(data))


def dump(dtf: DetachedTimestampFile) -> bytes:
    ctx = BytesSerializationContext()
    dtf.serialize(ctx)
    return ctx.getbytes()


@dataclass
class AttPath:
    kind: str                          # "bitcoin" | "pending" | other
    height: int | None
    calendar: str | None
    msg: bytes                         # the commitment the attestation is about (merkle root for bitcoin)
    txids: list[str] = field(default_factory=list)   # display order
    n_ops: int = 0


def _is_tx(msg: bytes) -> bool:
    if len(msg) < 60:
        return False
    try:
        CTransaction.deserialize(msg)
        return True
    except Exception:  # noqa: BLE001
        return False


def attestation_paths(ts: Timestamp, _path=None) -> list[AttPath]:
    out = []
    path = (_path or []) + [ts.msg]
    for att in sorted(ts.attestations, key=repr):
        txids = [btc.sha256d(m)[::-1].hex() for m in path if _is_tx(m)]
        if isinstance(att, BitcoinBlockHeaderAttestation):
            out.append(AttPath("bitcoin", att.height, None, ts.msg, txids, len(path) - 1))
        elif isinstance(att, PendingAttestation):
            out.append(AttPath("pending", None, att.uri, ts.msg, txids, len(path) - 1))
        else:
            out.append(AttPath(type(att).__name__, None, None, ts.msg, txids, len(path) - 1))
    for op, child in ts.ops.items():
        out.extend(attestation_paths(child, path))
    return out


@dataclass
class OtsCheck:
    file_digest_ok: bool
    paths: list[AttPath]
    bitcoin: list[dict]          # per bitcoin attestation: height, header_present, merkle_ok, time, txids
    pending: list[str]

    def verified(self) -> list[dict]:
        return [b for b in self.bitcoin if b["merkle_ok"]]

    def earliest(self) -> dict | None:
        v = self.verified()
        return min(v, key=lambda b: b["height"]) if v else None


def check(dtf: DetachedTimestampFile, file_bytes: bytes | None, headers: dict[int, btc.Header],
          file_digest: bytes | None = None) -> OtsCheck:
    want = file_digest if file_digest is not None else hashlib.sha256(file_bytes).digest()
    ok = isinstance(dtf.file_hash_op, OpSHA256) and dtf.file_digest == want
    paths = attestation_paths(dtf.timestamp)
    bit = []
    for p in paths:
        if p.kind != "bitcoin":
            continue
        h = headers.get(p.height)
        bit.append({"height": p.height, "header_present": h is not None,
                    "merkle_ok": h is not None and h.merkle_root == p.msg,
                    "time": h.time if h else None, "txids": p.txids})
    return OtsCheck(ok, paths, bit, [p.calendar for p in paths if p.kind == "pending"])


# ------------------------------------------------------------------ regtest calendar + chain

@dataclass
class RegtestOtsChain:
    """A regtest-difficulty Bitcoin chain plus one or more OTS 'calendars' that aggregate stamps and
    commit their merkle root in an OP_RETURN transaction. REGTEST: no real work."""
    genesis_time: int
    headers: list[btc.Header] = field(default_factory=list)
    pending: dict[str, list[Timestamp]] = field(default_factory=dict)
    calendars: tuple[str, ...] = ("cal-a.regtest.invalid", "cal-b.regtest.invalid")
    second_calendar_lag: int = 2          # blocks; real proofs carry several attestations at different heights
    _salt: int = 0

    def __post_init__(self):
        if not self.headers:
            g = self._mine_header(b"\x00" * 32, [btc.sha256d(btc.coinbase_tx(0))], self.genesis_time)
            self.headers.append(g)

    # -- mining
    def _mine_header(self, prev: bytes, txids: list[bytes], t: int) -> btc.Header:
        root, _ = btc.merkle_root_and_paths(txids)
        n = 0
        while True:
            h = btc.Header(0x20000000, prev, root, t, btc.REGTEST_BITS, n)
            if h.pow_ok():
                return h
            n += 1

    @property
    def tip(self) -> int:
        return len(self.headers) - 1

    def mine(self, t: int, calendars: list[str] | None = None) -> btc.Header:
        """Mine one block at time t, committing the named calendars' pending stamps."""
        height = self.tip + 1
        txs = [btc.coinbase_tx(height)]
        commits = []
        for cal in calendars or []:
            leaves = self.pending.pop(cal, [])
            if not leaves:
                continue
            root_ts = make_merkle_tree(leaves)
            self._salt += 1
            tx, prefix, suffix = btc.op_return_tx(root_ts.msg, self._salt)
            t1 = root_ts.ops.add(OpPrepend(prefix))
            t2 = t1.ops.add(OpAppend(suffix))
            assert t2.msg == tx
            tx_ts = t2.ops.add(OpSHA256()).ops.add(OpSHA256())
            txs.append(tx)
            commits.append(tx_ts)
        txids = [btc.sha256d(x) for x in txs]
        hdr = self._mine_header(self.headers[-1].hash, txids, t)
        _, paths = btc.merkle_root_and_paths(txids)
        for i, tx_ts in enumerate(commits, start=1):
            cur = tx_ts
            assert cur.msg == txids[i]
            for side, sib in paths[i]:
                cur = cur.ops.add(OpAppend(sib) if side == "R" else OpPrepend(sib))
                cur = cur.ops.add(OpSHA256()).ops.add(OpSHA256())
            assert cur.msg == hdr.merkle_root
            cur.attestations.add(BitcoinBlockHeaderAttestation(height))
        self.headers.append(hdr)
        return hdr

    # -- the client side: one stamp, submitted to every calendar
    def stamp(self, digest: bytes) -> DetachedTimestampFile:
        dtf = DetachedTimestampFile(OpSHA256(), Timestamp(digest))
        nonce_ts = dtf.timestamp.ops.add(OpAppend(os.urandom(16))).ops.add(OpSHA256())
        for cal in self.calendars:
            self.pending.setdefault(cal, []).append(nonce_ts)
        return dtf

    def header_store(self) -> dict[int, str]:
        return {i: h.hash_hex for i, h in enumerate(self.headers)}

    def segment_hex(self, lo: int, hi: int) -> dict[str, str]:
        return {str(i): self.headers[i].serialize().hex() for i in range(lo, min(hi, self.tip) + 1)}

    # -- the issuer's step 5 against this chain (called from issuer.anchor_layer)
    def anchor_receipt(self, frames: list[bytes], declared: int, sched, k: int) -> dict:
        from .. import objects
        digest = bytes.fromhex(objects.receipt_digest(frames))     # GUESS G-19 kept: one stamp over both frames
        dtf = self.stamp(digest)
        t = declared + sched.inclusion_delay
        first = self.tip + 1
        self.mine(t, [self.calendars[0]])
        for i in range(1, k + self.second_calendar_lag):
            t += sched.block_interval
            self.mine(t, list(self.calendars[1:]) if i == self.second_calendar_lag else None)
        chk = check(dtf, None, {i: h for i, h in enumerate(self.headers)}, digest)
        e = chk.earliest()
        return {"format": FORMAT, "network": "regtest",
                "ots_b64": base64.b64encode(dump(dtf)).decode(),
                "txid": e["txids"][-1] if e and e["txids"] else None,
                # R-3.48 (docket candidate): embed the k-header segment from the earliest attested height
                "headers_hex": self.segment_hex(first, first + k - 1),
                # presentation copy for the issuer's ship guard and the phase-2 consumers' clocks;
                # the VERIFIER never reads it (it parses headers_hex itself)
                "headers": [{"height": i, "time": self.headers[i].time, "hash": self.headers[i].hash_hex}
                            for i in range(first, first + k)]}
