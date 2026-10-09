"""Bitcoin block headers, proof of work and transaction merkle trees. THROWAWAY.

Two uses:
  * verify the archived MAINNET headers (fixtures/) that the repo's real OTS stamps attest into;
  * a REGTEST-DIFFICULTY chain (nBits 0x207fffff, so mining is ~2 hashes in Python) whose blocks,
    transactions and merkle trees are byte-for-byte Bitcoin format, so the de-stubbed issuer can
    produce real-format OpenTimestamps proofs without waiting on mainnet. It proves nothing about
    work; it is labelled REGTEST everywhere it appears.
"""
from __future__ import annotations

import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
REGTEST_BITS = 0x207FFFFF
UINT32_MAX_TIME = 2**32 - 1          # nTime is a uint32: the last representable second is 2106-02-07T06:28:15Z


def sha256d(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def target_from_bits(bits: int) -> int:
    exp, mant = bits >> 24, bits & 0x007FFFFF
    return mant << (8 * (exp - 3)) if exp > 3 else mant >> (8 * (3 - exp))


def work_from_bits(bits: int) -> int:
    return 2**256 // (target_from_bits(bits) + 1)


@dataclass(frozen=True)
class Header:
    version: int
    prev: bytes          # internal byte order
    merkle_root: bytes   # internal byte order (what an OTS BitcoinBlockHeaderAttestation commits to)
    time: int
    bits: int
    nonce: int

    @classmethod
    def parse(cls, raw: bytes) -> "Header":
        if len(raw) != 80:
            raise ValueError("header must be 80 bytes")
        v, = struct.unpack("<i", raw[:4])
        t, b, n = struct.unpack("<III", raw[68:80])
        return cls(v, raw[4:36], raw[36:68], t, b, n)

    def serialize(self) -> bytes:
        return struct.pack("<i", self.version) + self.prev + self.merkle_root + struct.pack("<III", self.time, self.bits, self.nonce)

    @property
    def hash(self) -> bytes:
        return sha256d(self.serialize())

    @property
    def hash_hex(self) -> str:          # display order, as block explorers print it
        return self.hash[::-1].hex()

    def pow_ok(self) -> bool:
        return int.from_bytes(self.hash, "little") <= target_from_bits(self.bits)


def load_mainnet(name: str) -> dict[int, Header]:
    d = json.loads((FIXTURES / name).read_text())
    return {int(h): Header.parse(bytes.fromhex(v["header_hex"])) for h, v in d["headers"].items()}


def check_segment(headers: dict[int, Header], lo: int, hi: int) -> tuple[bool, str]:
    """Linkage + PoW for heights lo..hi. Difficulty-retarget validity is NOT checked (no segment used
    here crosses a 2016-block boundary; a real verifier must check it, or an attacker picks nBits)."""
    for h in range(lo, hi + 1):
        x = headers.get(h)
        if x is None:
            return False, f"HEADER_MISSING:{h}"
        if not x.pow_ok():
            return False, f"POW_INVALID:{h}"
        if h > lo and x.prev != headers[h - 1].hash:
            return False, f"CHAIN_BROKEN:{h}"
        if h > lo and (h % 2016) and x.bits != headers[h - 1].bits:
            return False, f"BITS_CHANGED_OFF_BOUNDARY:{h}"
        if h % 2016 == 0 and h > lo:
            return False, f"RETARGET_NOT_IMPLEMENTED:{h}"
    return True, ""


def median_time_past(headers: dict[int, Header], h: int) -> int | None:
    ts = [headers[x].time for x in range(h - 11, h) if x in headers]
    return sorted(ts)[len(ts) // 2] if len(ts) == 11 else None


# ------------------------------------------------------------------ transactions and merkle trees

def varint(n: int) -> bytes:
    if n < 0xFD:
        return bytes([n])
    if n <= 0xFFFF:
        return b"\xfd" + struct.pack("<H", n)
    return b"\xfe" + struct.pack("<I", n)


def op_return_tx(commitment: bytes, salt: int) -> tuple[bytes, bytes, bytes]:
    """A legacy-serialized one-in, one-out transaction whose output is OP_RETURN <32 bytes>.
    Returns (tx, prefix, suffix) with tx == prefix || commitment || suffix -- the shape OTS calendars
    use, so the proof is `prepend prefix, append suffix, sha256, sha256` -> txid."""
    assert len(commitment) == 32
    prev_out = hashlib.sha256(b"regtest-funding" + struct.pack("<I", salt)).digest() + struct.pack("<I", 0)
    txin = prev_out + varint(0) + struct.pack("<I", 0xFFFFFFFD)
    script = b"\x6a\x20" + commitment
    txout = struct.pack("<q", 0) + varint(len(script)) + script
    prefix = struct.pack("<i", 1) + varint(1) + txin + varint(1) + struct.pack("<q", 0) + varint(len(script)) + b"\x6a\x20"
    suffix = struct.pack("<I", 0)  # locktime
    tx = struct.pack("<i", 1) + varint(1) + txin + varint(1) + txout + suffix
    assert tx == prefix + commitment + suffix
    return tx, prefix, suffix


def coinbase_tx(height: int) -> bytes:
    script = b"\x03" + struct.pack("<I", height)[:3] + b"regtest"
    txin = b"\x00" * 32 + b"\xff\xff\xff\xff" + varint(len(script)) + script + b"\xff\xff\xff\xff"
    txout = struct.pack("<q", 50 * 10**8) + varint(1) + b"\x51"
    return struct.pack("<i", 1) + varint(1) + txin + varint(1) + txout + struct.pack("<I", 0)


def merkle_root_and_paths(txids: list[bytes]) -> tuple[bytes, list[list[tuple[str, bytes]]]]:
    """Bitcoin's tree: sha256d(left || right), last node duplicated on odd levels. Paths are
    [(side, sibling)] with side 'R' = sibling goes on the right."""
    paths: list[list[tuple[str, bytes]]] = [[] for _ in txids]
    level = [(t, [i]) for i, t in enumerate(txids)]
    while len(level) > 1:
        if len(level) % 2:
            level.append((level[-1][0], []))
        nxt = []
        for i in range(0, len(level), 2):
            (a, ia), (b, ib) = level[i], level[i + 1]
            for j in ia:
                paths[j].append(("R", b))
            for j in ib:
                paths[j].append(("L", a))
            nxt.append((sha256d(a + b), ia + ib))
        level = nxt
    return level[0][0], paths
