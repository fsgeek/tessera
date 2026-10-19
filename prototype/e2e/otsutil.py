"""OpenTimestamps for the issuer: a closed-grammar reader (V1-PROFILE §15.2), lowest-height selection (§7.1), the
transaction-shape / merkle-suffix subset and the txid, plus two stamping backends:

  RealOts   `ots stamp` / `ots upgrade` against the public calendars (network; the real run only)
  StubOts   a synthetic chain and calendar for the dry run (universe.Chain / universe.Proof); no network

The issuer-side reader is written here, not imported from either verifier, so that the driver's pre-ship checks
are not the verifier checking itself.
"""
import json
import os
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path

from common import U, sha256, sha256d, write_atomic, write_json, read_json, log

MAGIC = U.OTS_MAGIC
TAG_BTC, TAG_PENDING = U.TAG_BTC, U.TAG_PENDING


class OtsError(Exception):
    pass


@dataclass
class Att:
    height: int
    msg: bytes
    path: list          # [(opcode, arg, input message)]


def _varuint(b, i):
    v = sh = 0
    for n in range(5):
        if i >= len(b):
            raise OtsError("truncated varuint")
        c = b[i]
        i += 1
        v |= (c & 0x7F) << sh
        sh += 7
        if not c & 0x80:
            if n and c == 0:
                raise OtsError("non-shortest varuint")
            if v > 0xFFFFFFFF:
                raise OtsError("varuint too large")
            return v, i
    raise OtsError("varuint too long")


def parse(raw):
    """-> (file digest, [Att bitcoin], [pending uri]). Raises OtsError outside the V1 grammar."""
    if len(raw) > 1 << 20 or not raw.startswith(MAGIC):
        raise OtsError("not an OTS file in the V1 grammar")
    i = len(MAGIC)
    major, i = _varuint(raw, i)
    if major != 1 or raw[i:i + 1] != b"\x08":
        raise OtsError("major version or file-hash op")
    digest = raw[i + 1:i + 33]
    i += 33
    btc, pending = [], []
    stack = [(digest, [], 0)]
    while stack:
        msg, path, depth = stack.pop()
        if depth > 256:
            raise OtsError("depth")
        if raw[i:i + 1] == b"\xff":
            i += 1
            stack.append((msg, path, depth))
        if i >= len(raw):
            raise OtsError("truncated")
        op = raw[i]
        i += 1
        if op == 0:
            tag = raw[i:i + 8]
            i += 8
            n, i = _varuint(raw, i)
            payload = raw[i:i + n]
            i += n
            if len(payload) != n or n > 8192:
                raise OtsError("payload")
            if tag == TAG_BTC:
                h, j = _varuint(payload, 0)
                if j != len(payload) or len(msg) != 32:
                    raise OtsError("bitcoin attestation")
                btc.append(Att(h, msg, path))
            elif tag == TAG_PENDING:
                m, j = _varuint(payload, 0)
                if j + m != len(payload) or m > 1000:
                    raise OtsError("pending attestation")
                pending.append(payload[j:].decode("ascii", "replace"))
            else:
                raise OtsError("attestation tag " + tag.hex())
        elif op in (0x08, 0xF0, 0xF1):
            arg = b""
            if op != 0x08:
                n, i = _varuint(raw, i)
                arg = raw[i:i + n]
                i += n
                if len(arg) != n or not 1 <= n <= 4096:
                    raise OtsError("op argument")
            res = sha256(msg) if op == 0x08 else (msg + arg if op == 0xF0 else arg + msg)
            if len(res) > 4096:
                raise OtsError("message too long")
            stack.append((res, path + [(op, arg, msg)], depth + 1))
        else:
            raise OtsError(f"op {op:#x} outside the V1 grammar")
    if i != len(raw):
        raise OtsError("trailing bytes")
    return digest, btc, pending


def _compact(b, i):
    f = b[i]
    if f < 253:
        return f, i + 1
    w = {253: 2, 254: 4, 255: 8}[f]
    v = int.from_bytes(b[i + 1:i + 1 + w], "little")
    if v < {253: 253, 254: 1 << 16, 255: 1 << 32}[f] or i + 1 + w > len(b):
        raise OtsError("compact size")
    return v, i + 1 + w


def tx_scripts(p):
    """Strict non-witness transaction parse (§15.2 part 1) -> output scripts."""
    i = 4
    n, i = _compact(p, i)
    if n < 1:
        raise OtsError("no inputs (or a segwit marker)")
    for _ in range(n):
        i += 36
        ln, i = _compact(p, i)
        i += ln + 4
    n, i = _compact(p, i)
    if n < 1:
        raise OtsError("no outputs")
    scripts = []
    for _ in range(n):
        i += 8
        ln, i = _compact(p, i)
        scripts.append(p[i:i + ln])
        i += ln
    i += 4
    if i != len(p):
        raise OtsError("transaction bytes not consumed exactly")
    return scripts


def path_tx(att):
    """§15.2 parts (1), (2), (4) on one path. -> display txid, or raises OtsError."""
    path = att.path
    for k in range(len(path) - 1):
        if path[k][0] == path[k + 1][0] == 0x08:
            p = path[k][2]
            j = k
            while j > 0 and path[j - 1][0] in (0xF0, 0xF1):
                j -= 1
            m = path[j][2]
            if len(m) != 32 or b"\x6a\x20" + m not in tx_scripts(p):
                raise OtsError("no OP_RETURN output committing to the message")
            sfx = path[k + 2:]
            if len(sfx) % 3:
                raise OtsError("merkle suffix length")
            for q in range(0, len(sfx), 3):
                a, b, c = sfx[q:q + 3]
                if a[0] not in (0xF0, 0xF1) or len(a[1]) != 32 or b[0] != 0x08 or c[0] != 0x08:
                    raise OtsError("merkle suffix shape")
            return sha256d(p)[::-1].hex()
    raise OtsError("no transaction on the path")


def pin_of(header):
    return sha256d(header)[::-1].hex()


def qualifies(h, headers, pins):
    for i in range(h, h + 6):
        if i not in headers or pins.get(i) != pin_of(headers[i]):
            return False
        if i > h and headers[i][4:36] != sha256d(headers[i - 1]):
            return False
    return True


def select(btc, headers, pins):
    """Lowest qualifying height (§7.1). -> (h*, T, confirmed_at, [Att at h*], contradicted)."""
    contradicted = any(a.height in headers and pins.get(a.height) == pin_of(headers[a.height])
                       and headers[a.height][36:68] != a.msg for a in btc)
    q = [a for a in btc if qualifies(a.height, headers, pins) and headers[a.height][36:68] == a.msg]
    if not q:
        return None, None, None, [], contradicted
    h = min(a.height for a in q)
    nt = lambda x: struct.unpack("<I", headers[x][68:72])[0]  # noqa: E731
    return h, nt(h), nt(h + 5), [a for a in q if a.height == h], contradicted


# ------------------------------------------------------------------------------------------------ real backend
class RealOts:
    """The `ots` client (python-opentimestamps). stamp() submits to the public calendars."""
    name = "real"

    def __init__(self, ots_bin=None):
        self.bin = ots_bin or os.environ.get("OTS_BIN") or shutil.which("ots") or str(
            Path(__file__).resolve().parents[2] / ".venv" / "bin" / "ots")

    def stamp(self, path):
        path = Path(path)
        ots = path.with_name(path.name + ".ots")
        if ots.exists():
            return ots
        r = subprocess.run([self.bin, "stamp", str(path)], capture_output=True, text=True, timeout=300)
        if r.returncode or not ots.exists():
            raise OtsError("ots stamp failed: " + (r.stderr or r.stdout).strip())
        return ots

    def upgrade(self, ots):
        r = subprocess.run([self.bin, "upgrade", str(ots)], capture_output=True, text=True, timeout=300)
        return r.returncode == 0, (r.stdout + r.stderr).strip()

    def advance(self, n):  # real blocks are mined by miners
        pass


# ------------------------------------------------------------------------------------------------ stub backend
class StubOts:
    """A synthetic calendar and chain, persisted in one JSON file so that every stage can resume.

    stamp() records the file digest as pending; advance(n) mines n blocks (all pending stamps go into the next
    block, block time = wall clock + 60 s per block mined in the same call); upgrade() rewrites the .ots with a
    Bitcoin branch once the stamp is mined. Proofs are universe.Proof serializations: nonce, OP_RETURN transaction,
    conventional merkle path, as a calendar produces. Nothing here is mainnet."""
    name = "stub"

    def __init__(self, state_file, base_height=950000):
        self.f = Path(state_file)
        if self.f.exists():
            self.s = read_json(self.f)
        else:
            import time
            t = int(time.time())
            self.s = {"base": base_height, "tip": base_height, "times": {str(base_height): t - 600}, "stamps": []}
            self._save()

    def _save(self):
        write_json(self.f, self.s)

    def _ntime(self, h):
        return self.s["times"][str(h)]

    def stamp(self, path):
        path = Path(path)
        ots = path.with_name(path.name + ".ots")
        if ots.exists():
            return ots
        digest = sha256(path.read_bytes())
        self.s["stamps"].append({"file": path.name, "digest": digest.hex(), "label": f"stub-{len(self.s['stamps'])}",
                                 "height": None})
        self._save()
        write_atomic(ots, self._proof(self.s["stamps"][-1]))
        return ots

    def advance(self, n):
        import time
        t = max(int(time.time()), self._ntime(self.s["tip"]) + 1)
        for i in range(n):
            h = self.s["tip"] + 1
            for st in self.s["stamps"]:
                if st["height"] is None:
                    st["height"] = h
            self.s["times"][str(h)] = t + 60 * i
            self.s["tip"] = h
        self._save()

    def tip(self):
        return self.s["tip"]

    def _materialize(self):
        chain = U.Chain(self._ntime)
        proofs = {}
        for st in self.s["stamps"]:
            pr = U.Proof(bytes.fromhex(st["digest"]), st["label"])
            pr.add_pending(uri=b"https://stub-calendar.invalid")
            if st["height"] is not None:
                pr.add_btc(chain, st["height"], label="b0")
            proofs[st["label"]] = pr
        chain.build(self.s["base"], self.s["tip"])
        for pr in proofs.values():
            pr.finish(chain)
        return chain, proofs

    def _proof(self, st):
        _, proofs = self._materialize()
        return proofs[st["label"]].serialize()

    def upgrade(self, ots):
        ots = Path(ots)
        name = ots.name[:-4]
        for st in self.s["stamps"]:
            if st["file"] == name and sha256(ots.with_name(name).read_bytes()).hex() == st["digest"]:
                write_atomic(ots, self._proof(st))
                return st["height"] is not None, "stub upgrade"
        raise OtsError("unknown stub stamp " + name)

    def headers(self, heights):
        chain, _ = self._materialize()
        return {h: chain.headers[h] for h in heights}


def k6_ready(ots_path, tip):
    """(ready, lowest Bitcoin height or None): ready when the lowest attested height h has h + 5 <= tip."""
    _, btc, _ = parse(Path(ots_path).read_bytes())
    if not btc:
        return False, None
    h = min(a.height for a in btc)
    return h + 5 <= tip, h


def summary(ots_path):
    d, btc, pend = parse(Path(ots_path).read_bytes())
    return {"digest": d.hex(), "bitcoin_heights": sorted({a.height for a in btc}), "pending": len(pend)}


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(p, json.dumps(summary(p)))
