"""The TEST universe for V1 conformance: DNS hierarchy, synthetic Bitcoin chain, OTS proofs, git objects,
trust configuration, test release and frozen-catalog stand-in.

Everything is deterministic and TEST-labelled. Nothing here is mainnet, a real DNS key, or a real release.
Formats follow docs/V1-PROFILE.md §15 (cited inline as P§n).
"""
import base64
import calendar
import hashlib
import json
import struct
import time

import tcrypto as tc
from tcrypto import gen

ALG_V1 = gen.ALG_V1
ALG_HYBRID = gen.ALG_HYBRID          # pair id of formal/p8/HYBRID-SUPPLEMENT-DRAFT.md §1 (registered only under "hybrid")
INSTALLATIONS = ("classical", "hybrid")
PROFILE = gen.PROFILE
D = "wamason.com"                     # P§6.3: profile constant D (the test universe uses the real name, TEST keys)
SPEC_ID = "tessera-v1-strict/verification-spec/1"
DELTA, EPS, K = 72 * 3600, 24 * 3600, 6
U32 = 1 << 32


# ----------------------------------------------------------------------------------------------- time
def ts(s):
    """RFC 3339 'YYYY-MM-DDTHH:MM:SSZ' -> integer seconds (proleptic Gregorian, no leap seconds; P§7.1)."""
    y, mo, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
    hh, mm, ss = int(s[11:13]), int(s[14:16]), int(s[17:19])
    return _days_from_civil(y, mo, d) * 86400 + hh * 3600 + mm * 60 + ss


def _days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def rfc3339(t):
    days, rem = divmod(t, 86400)
    z = days + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    y += m <= 2
    return f"{y:04d}-{m:02d}-{d:02d}T{rem // 3600:02d}:{rem % 3600 // 60:02d}:{rem % 60:02d}Z"


assert rfc3339(ts("2026-11-10T12:00:00Z")) == "2026-11-10T12:00:00Z"
assert ts("1970-01-01T00:00:00Z") == 0 and ts("2106-02-07T06:28:16Z") == U32


def sha256(b):
    return hashlib.sha256(b).digest()


def sha256d(b):
    return sha256(sha256(b))


def jcs(v):
    return gen.jcs(v)


def b64(b):
    return base64.b64encode(b).decode()


# ----------------------------------------------------------------------------------------------- keys
class Keys:
    """All TEST keys of the universe, created lazily from seeds."""
    _cache = {}

    @classmethod
    def p256(cls, seed, created=1790000000):
        k = ("p256", seed, created)
        if k not in cls._cache:
            cls._cache[k] = tc.P256Key(seed, created)
        return cls._cache[k]

    @classmethod
    def mldsa65(cls, seed):
        k = ("mldsa65", seed)
        if k not in cls._cache:
            cls._cache[k] = tc.MLDSA65Key(seed)
        return cls._cache[k]


# ----------------------------------------------------------------------------------------------- DNS
T_A, T_TXT, T_DS, T_RRSIG, T_DNSKEY = 1, 16, 43, 46, 48
CLASS_IN = 1


def name_wire(name):
    name = name.rstrip(".")
    if name == "":
        return b"\x00"
    out = b""
    for lb in name.split("."):
        out += bytes([len(lb)]) + lb.encode("ascii")
    return out + b"\x00"


def label_count(name):
    name = name.rstrip(".")
    if not name:
        return 0
    labels = name.split(".")
    return len(labels) - (1 if labels[0] == "*" else 0)


def key_tag(rdata):
    ac = 0
    for i, b in enumerate(rdata):
        ac += b if i & 1 else b << 8
    ac += (ac >> 16) & 0xFFFF
    return ac & 0xFFFF


class ZKey:
    """A TEST DNSSEC key. alg 8 (RSA/SHA-256), 13 (P-256/SHA-256) or 15 (Ed25519, unsupported by V1)."""

    def __init__(self, seed, alg, flags=256, protocol=3):
        self.seed, self.alg, self.flags, self.protocol = seed, alg, flags, protocol
        if alg == 8:
            self.priv = tc.rsa_key("dns:" + seed)
            self.pub = tc.rsa_dnskey_pub(self.priv)
        elif alg == 13:
            self.priv = Keys.p256("dns:" + seed)
            self.pub = self.priv.point[1:]
        elif alg == 15:
            self.priv = tc.ed25519_key("dns:" + seed)
            self.pub = tc.ed25519_pub(self.priv)
        else:
            raise ValueError(alg)

    def rdata(self, flags=None, protocol=None):
        f = self.flags if flags is None else flags
        p = self.protocol if protocol is None else protocol
        return struct.pack(">HBB", f, p, self.alg) + self.pub

    @property
    def tag(self):
        return key_tag(self.rdata())

    def sign(self, data):
        if self.alg == 8:
            return tc.rsa_sign(self.priv, data)
        if self.alg == 13:
            r, s = self.priv.sign_digest(sha256(data))
            return r.to_bytes(32, "big") + s.to_bytes(32, "big")
        return self.priv.sign(data)


_ZK = {}


def zkey(seed, alg, flags=256):
    k = (seed, alg, flags)
    if k not in _ZK:
        _ZK[k] = ZKey(seed, alg, flags)
    return _ZK[k]


def ds_rdata(owner, dnskey_rdata, digest_type=2, alg=None, tag=None, digest=None):
    pre = name_wire(owner.lower()) + dnskey_rdata
    if digest is None:
        digest = {1: hashlib.sha1, 2: hashlib.sha256, 4: hashlib.sha384}[digest_type](pre).digest()
    return struct.pack(">HBB", key_tag(dnskey_rdata) if tag is None else tag,
                       dnskey_rdata[3] if alg is None else alg, digest_type) + digest


class Sig:
    """One RRSIG to generate. All fields overridable to build defects."""

    def __init__(self, key, inception, expiration, signer=None, labels=None, orig_ttl=None, alg=None, tag=None,
                 corrupt=False, sig_bytes=None, signer_wire=None, key_rdata=None, sign_with=None):
        self.key, self.inception, self.expiration = key, inception % U32, expiration % U32
        self.signer, self.labels, self.orig_ttl = signer, labels, orig_ttl
        self.alg, self.tag, self.corrupt, self.sig_bytes = alg, tag, corrupt, sig_bytes
        self.signer_wire, self.key_rdata, self.sign_with = signer_wire, key_rdata, sign_with


class Group:
    """An RRset and its witnesses (P§15.3 point 1)."""

    def __init__(self, owner, rtype, rdatas, sigs, ttl=3600, sort=True, sig_sort=True, owner_wire=None):
        self.owner, self.rtype, self.rdatas, self.sigs = owner, rtype, list(rdatas), list(sigs)
        self.ttl, self.sort, self.sig_sort, self.owner_wire = ttl, sort, sig_sort, owner_wire
        self.extra_rrs = []      # (owner_wire, type, ttl, rdata) appended raw after the group


def rr_wire(owner_w, rtype, ttl, rdata, cls=CLASS_IN):
    return owner_w + struct.pack(">HHIH", rtype, cls, ttl, len(rdata)) + rdata


def rrsig_rdata(group, sig):
    """Build and sign one RRSIG RDATA (RFC 4034 §3, RFC 4035 §5.3.2 signing input)."""
    owner = group.owner.lower()
    labels = label_count(owner) if sig.labels is None else sig.labels
    ttl = group.ttl if sig.orig_ttl is None else sig.orig_ttl
    alg = sig.key.alg if sig.alg is None else sig.alg
    krd = sig.key.rdata() if sig.key_rdata is None else sig.key_rdata
    tag = key_tag(krd) if sig.tag is None else sig.tag
    signer_w = name_wire(sig.signer.lower()) if sig.signer_wire is None else sig.signer_wire
    head = struct.pack(">HBBIIIH", group.rtype, alg, labels, ttl, sig.expiration, sig.inception, tag) + signer_w
    if sig.sig_bytes is not None:
        return head + sig.sig_bytes
    # signing owner: wildcard expansion when Labels < owner label count (RFC 4035 §5.3.2)
    olabels = owner.rstrip(".").split(".") if owner.rstrip(".") else []
    if labels < len(olabels):
        sowner = "*." + ".".join(olabels[len(olabels) - labels:]) if labels else "*"
    else:
        sowner = owner
    sw = name_wire(sowner)
    rrs = sorted(group.rdatas)
    data = head + b"".join(sw + struct.pack(">HHIH", group.rtype, CLASS_IN, ttl, len(r)) + r for r in rrs)
    signer_key = sig.key if sig.sign_with is None else sig.sign_with
    s = signer_key.sign(data)
    if sig.corrupt:
        s = s[:-1] + bytes([s[-1] ^ 0x01])
    return head + s


def rrsig_sort_key(rd):
    tag = rd[16:18]
    inc, exp = rd[12:16], rd[8:12]
    # signature bytes start after the signer name
    i = 18
    while rd[i] != 0:
        i += 1 + rd[i]
    sigb = rd[i + 1:]
    return (tag, inc, exp, sigb, rd)


def serialize_groups(groups):
    out = b""
    for g in groups:
        ow = name_wire(g.owner.lower()) if g.owner_wire is None else g.owner_wire
        rds = sorted(g.rdatas) if g.sort else list(g.rdatas)
        for rd in rds:
            out += rr_wire(ow, g.rtype, g.ttl, rd)
        srds = [rrsig_rdata(g, s) for s in g.sigs]
        if g.sig_sort:
            srds.sort(key=rrsig_sort_key)
        for rd in srds:
            out += rr_wire(ow, T_RRSIG, g.ttl, rd)
        for (w, t, ttl, rd) in g.extra_rrs:
            out += rr_wire(w, t, ttl, rd)
    return out


# ----------------------------------------------------------------------------------------------- Bitcoin + OTS
def varuint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out += bytes([b | 0x80])
        else:
            return out + bytes([b])


def varbytes(b):
    return varuint(len(b)) + b


def compact(n):
    if n < 253:
        return bytes([n])
    if n <= 0xFFFF:
        return b"\xfd" + struct.pack("<H", n)
    if n <= 0xFFFFFFFF:
        return b"\xfe" + struct.pack("<I", n)
    return b"\xff" + struct.pack("<Q", n)


OTS_MAGIC = bytes.fromhex("00") + b"OpenTimestamps" + bytes.fromhex("0000") + b"Proof" + bytes.fromhex(
    "00bf89e2e884e89294")
TAG_BTC = bytes.fromhex("0588960d73d71901")
TAG_PENDING = bytes.fromhex("83dfe30d2ef90c8e")


def tx_parts(m, seed, variant="std"):
    """A non-witness Bitcoin transaction with output script 6a 20 || m (P§15.2 part 1-2). Returns (prefix, suffix)
    such that P = prefix || m || suffix. variant: std (125 bytes), multi (2 in / 2 out), segwit (witness
    serialization: fails part 1), noncanon (non-shortest CompactSize input count: fails part 1)."""
    prevout = tc.drbg("prevout:" + seed, 32) + struct.pack("<I", 0)
    script_sig = tc.drbg("scriptsig:" + seed, 31)
    ver = struct.pack("<i", 2)
    lock = struct.pack("<I", 0)
    inp = prevout + compact(len(script_sig)) + script_sig + b"\xff\xff\xff\xff"
    opret_head = struct.pack("<q", 0) + compact(34) + b"\x6a\x20"
    if variant == "std":
        return ver + b"\x01" + inp + b"\x01" + opret_head, lock
    if variant == "noncanon":
        return ver + b"\xfd\x01\x00" + inp + b"\x01" + opret_head, lock
    if variant == "multi":
        inp2 = tc.drbg("prevout2:" + seed, 32) + struct.pack("<I", 1) + compact(0) + b"\xfe\xff\xff\xff"
        change = struct.pack("<q", 12345) + compact(22) + b"\x00\x14" + tc.drbg("change:" + seed, 20)
        return ver + b"\x02" + inp + inp2 + b"\x02" + opret_head, change + lock
    if variant == "segwit":
        inp_w = prevout + compact(0) + b"\xff\xff\xff\xff"
        witness = b"\x01" + compact(64) + tc.drbg("wit:" + seed, 64)
        return ver + b"\x00\x01" + b"\x01" + inp_w + b"\x01" + opret_head, witness + lock
    raise ValueError(variant)


class Node:
    """An OTS Timestamp: ordered items, each ('att', tag, payload) or ('op', opbytes, child Node)."""

    def __init__(self):
        self.items = []

    def child(self, opbytes):
        for it in self.items:
            if it[0] == "op" and it[1] == opbytes:
                return it[2]
        n = Node()
        self.items.append(("op", opbytes, n))
        return n

    def ser(self):
        out = b""
        for i, it in enumerate(self.items):
            if i < len(self.items) - 1:
                out += b"\xff"
            if it[0] == "att":
                out += b"\x00" + it[1] + varbytes(it[2])
            else:
                out += it[1] + it[2].ser()
        return out


def op_bytes(op):
    if op[0] == "sha256":
        return b"\x08"
    if op[0] == "append":
        return b"\xf0" + varbytes(op[1])
    if op[0] == "prepend":
        return b"\xf1" + varbytes(op[1])
    if op[0] == "raw":
        return op[1]
    raise ValueError(op)


def apply(op, msg):
    if op[0] == "sha256":
        return sha256(msg)
    if op[0] == "append":
        return msg + op[1]
    if op[0] == "prepend":
        return op[1] + msg
    raise ValueError(op)


def run_ops(ops, msg):
    for op in ops:
        msg = apply(op, msg)
    return msg


def btc_payload(h):
    return varuint(h)


def pending_payload(uri=b"https://test-calendar.invalid"):
    return varbytes(uri)


class Chain:
    """A synthetic header chain. No PoW (P§7.2: a hash equal to a pin implies all of it)."""

    def __init__(self, ntime):
        self.ntime = ntime                    # function height -> nTime
        self.txs = {}                         # height -> list of txid (internal byte order)
        self.merkle_override = {}
        self.prev_override = {}
        self.headers = {}

    def register(self, h, txid):
        lst = self.txs.setdefault(h, [sha256d(b"TEST coinbase %d" % h)])
        lst.append(txid)

    def ensure(self, h):
        self.txs.setdefault(h, [sha256d(b"TEST coinbase %d" % h)])

    def merkle_levels(self, h):
        level = list(self.txs[h])
        levels = [level]
        while len(level) > 1:
            if len(level) % 2:
                level = level + [level[-1]]
            level = [sha256d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
            levels.append(level)
        return levels

    def merkle_root(self, h):
        if h in self.merkle_override:
            return self.merkle_override[h]
        return self.merkle_levels(h)[-1][0]

    def merkle_path(self, h, txid):
        """Conventional suffix (P§15.2 part 4): (append|prepend 32 bytes, sha256, sha256)*."""
        levels = self.merkle_levels(h)
        idx = levels[0].index(txid)
        ops = []
        for level in levels[:-1]:
            lv = level + [level[-1]] if len(level) % 2 else level
            if idx % 2 == 0:
                ops.append(("append", lv[idx + 1]))
            else:
                ops.append(("prepend", lv[idx - 1]))
            ops += [("sha256",), ("sha256",)]
            idx //= 2
        return ops

    def build(self, lo, hi):
        prev = sha256d(b"TEST pre-chain %d" % lo)
        for h in range(lo, hi + 1):
            self.ensure(h)
            pv = self.prev_override.get(h, prev)
            hdr = struct.pack("<i", 0x20000000) + pv + self.merkle_root(h) + struct.pack(
                "<I", self.ntime(h) % U32) + struct.pack("<I", 0x17030ECD) + struct.pack("<I", h & 0xFFFFFFFF)
            assert 0 <= self.ntime(h) < U32, (h, self.ntime(h))
            self.headers[h] = hdr
            prev = sha256d(hdr)
        return self.headers


def pin_of(header):
    return sha256d(header)[::-1].hex()


class Proof:
    """An OTS DetachedTimestampFile under construction (P§15.2)."""

    def __init__(self, digest, name):
        self.digest, self.name = digest, name
        self.paths = []          # list of (ops, ('att', tag, payload))
        self.deferred = []       # (prefix_ops, txid, height, post_ops, extra) to finish after the chain exists
        self.txids = {}          # branch label -> display txid

    def add_btc(self, chain, h, label="b0", variant="std", pre="nonce", suffix="conventional",
                contradict=False, post=(), register=True):
        """Bitcoin branch at height h. pre: nonce (append 16, sha256) | double (sha256, sha256: the F09 shape)."""
        if pre == "nonce":
            pre_ops = [("append", tc.drbg(f"nonce:{self.name}:{label}", 16)), ("sha256",)]
        elif pre == "double":
            pre_ops = [("sha256",), ("sha256",)]
        else:
            raise ValueError(pre)
        m = run_ops(pre_ops, self.digest)
        prefix, sfx = tx_parts(m, f"{self.name}:{label}", variant if variant != "nonsha" else "std")
        P = prefix + m + sfx
        tx_ops = [("prepend", prefix), ("append", sfx), ("sha256",), ("sha256",)]
        txid = sha256d(P)
        self.txids[label] = txid[::-1].hex()
        if contradict:
            # the branch claims block h, but block h never includes this transaction (P§7.1 OTS_MERKLE_MISMATCH)
            chain.ensure(h)
            fake = [("append", tc.drbg(f"fake-sibling:{self.name}:{label}", 32)), ("sha256",), ("sha256",)]
            self.paths.append((pre_ops + tx_ops + fake + list(post), ("att", TAG_BTC, btc_payload(h))))
            return txid
        if suffix == "conventional":
            if register:
                chain.register(h, txid)
            self.deferred.append((pre_ops + tx_ops, txid, h, list(post), "conventional"))
        elif suffix == "single":
            # non-conventional suffix: (append 32, sha256) without the second sha256; the block's merkle root is
            # set to the result so the attestation still matches its header
            sib = tc.drbg(f"odd-sibling:{self.name}:{label}", 32)
            ops = pre_ops + tx_ops + [("append", sib), ("sha256",)]
            chain.ensure(h)
            chain.merkle_override[h] = run_ops(ops, self.digest)
            self.paths.append((ops + list(post), ("att", TAG_BTC, btc_payload(h))))
        return txid

    def add_pending(self, uri=b"https://test-calendar.invalid", pre_ops=None, payload=None):
        if pre_ops is None:
            pre_ops = [("append", tc.drbg(f"pending:{self.name}:{uri!r}", 16)), ("sha256",)]
        self.paths.append((list(pre_ops), ("att", TAG_PENDING, pending_payload(uri) if payload is None else payload)))

    def add_raw(self, ops, att):
        self.paths.append((list(ops), att))

    def finish(self, chain):
        for ops, txid, h, post, kind in self.deferred:
            full = ops + chain.merkle_path(h, txid) + post
            self.paths.append((full, ("att", TAG_BTC, btc_payload(h))))
        self.deferred = []

    def check_paths(self, chain):
        """Issuer self-check: each non-contradicting Bitcoin path ends at its header's merkle root."""
        out = {}
        for ops, att in self.paths:
            if att[1] == TAG_BTC:
                msg = run_ops([o for o in ops if o[0] != "raw"], self.digest)
                h = int(_read_varuint(att[2])[0])
                out.setdefault(h, []).append(msg == chain.merkle_root(h))
        return out

    def counts(self):
        """(serialized op items, attestation items) of the proof tree (P§15.2 bounds)."""
        root = self._tree()

        def walk(n):
            o = a = 0
            for it in n.items:
                if it[0] == "att":
                    a += 1
                else:
                    o += 1
                    oo, aa = walk(it[2])
                    o, a = o + oo, a + aa
            return o, a
        return walk(root)

    def _tree(self):
        root = Node()
        for ops, att in self.paths:
            n = root
            for op in ops:
                n = n.child(op_bytes(op))
            n.items.append(att)
        return root

    def serialize(self, major=b"\x01", magic=OTS_MAGIC):
        root = Node()
        for ops, att in self.paths:
            n = root
            for op in ops:
                n = n.child(op_bytes(op))
            n.items.append(att)
        return magic + major + b"\x08" + self.digest + root.ser()


def _read_varuint(b):
    v, sh, i = 0, 0, 0
    while True:
        c = b[i]
        v |= (c & 0x7F) << sh
        i += 1
        if not c & 0x80:
            return v, i
        sh += 7


# ----------------------------------------------------------------------------------------------- git
def git_id(typ, body):
    return hashlib.sha1(f"{typ} {len(body)}".encode() + b"\x00" + body).digest()


def tree_entry(mode, name, oid):
    return mode.encode() + b" " + name.encode() + b"\x00" + oid


def git_sort_key(entry):
    mode, name = entry[0], entry[1]
    return name.encode() + (b"/" if mode == "40000" else b"")


def tree_body(entries, sort=True):
    es = sorted(entries, key=git_sort_key) if sort else entries
    return b"".join(tree_entry(m, n, o) for m, n, o in es)


def gpgsig_header(armored):
    lines = armored.split("\n")
    return ("gpgsig " + lines[0] + "\n" + "".join(" " + ln + "\n" for ln in lines[1:])).encode()


# ----------------------------------------------------------------------------------------------- objects
def part_object(parts):
    """P§15.8 part format: 'tessera-v1-part <path> <length>' LF, bytes, LF; parts sorted by path."""
    out = b""
    for path, data in sorted(parts):
        out += f"tessera-v1-part {path} {len(data)}\n".encode() + data + b"\n"
    return out


SPEC_BYTES = part_object([("prototype/conformance/TEST-SPEC.txt",
                           b"TEST ONLY. Stand-in for the frozen tessera-v1-strict specification object "
                           b"(docs/V1-PROFILE.md, formal/p8/ENCODING-V1.md, A9). Not the frozen object.\n")])
VECTORS_BYTES = part_object([("prototype/conformance/TEST-VECTORS.txt",
                              b"TEST ONLY. Stand-in for the frozen V1 vectors object.\n")])
PREAMBLE_BYTES = (b"TEST ONLY purpose preamble. A Tessera V1 receipt attests that these bytes were presented to "
                  b"the (TEST) service by time T. It attests no submitter and evaluates no revocation.\n")
_DEP_IDS = [("rfc8785", "RFC 8785 JCS"), ("openpgp-rfc9580", "RFC 9580 OpenPGP"),
            ("ecdsa-p256", "ECDSA P-256 (FIPS 186-5)"), ("sha-256", "FIPS 180-4 SHA-256"),
            ("sha-1-git", "SHA-1 for git object linkage (SHA-1DC)"), ("dnssec-algs", "DNSSEC algorithms 8 and 13"),
            ("opentimestamps", "OTS DetachedTimestampFile"), ("bitcoin-headers", "Bitcoin header format")]
DEP_BYTES = jcs({"entries": sorted([{"id": i, "title": t, "edition": "TEST", "sections": ["TEST"],
                                     "errata": "TEST", "digest_sha256": None, "retrieval": "TEST",
                                     "redistribution": "TEST", "failure_consequence": "TEST"}
                                    for i, t in _DEP_IDS], key=lambda e: e["id"]),
                 "format": "tessera-v1-deps/1"})


# The hybrid-registered installation (P§1 "Catalog entry", P§1 "Encoding", P§15.8): the governing spec is the
# baseline plus the dated branch-registration supplement, so its spec object carries one more part, and the catalog's
# single alg is the registered pair id. Registration state is read from the catalog's alg: the pair id is in the
# codec registry exactly when the catalog selects it (A9.6: the supplement takes effect only if the hybrid branch is
# taken). The catalog keeps the classical catalog's field set, so a catalog reader needs no new field.
SPEC_BYTES_HYBRID = part_object([
    ("prototype/conformance/TEST-SPEC.txt",
     b"TEST ONLY. Stand-in for the frozen tessera-v1-strict specification object "
     b"(docs/V1-PROFILE.md, formal/p8/ENCODING-V1.md, A9). Not the frozen object.\n"),
    ("prototype/conformance/TEST-HYBRID-SUPPLEMENT.txt",
     b"TEST ONLY. Stand-in for the dated branch-registration supplement (A9.6) registering "
     b"KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256: slot kms rule R (ML-DSA-65, pure, empty context, exactly "
     b"3309 bytes, key = DER SPKI with OID 2.16.840.1.101.3.4.3.18), slot gpg rule O. Not the registered "
     b"supplement.\n")])


def spec_bytes(installation="classical"):
    return {"classical": SPEC_BYTES, "hybrid": SPEC_BYTES_HYBRID}[installation]


def catalog_alg(installation="classical"):
    return {"classical": ALG_V1, "hybrid": ALG_HYBRID}[installation]


def catalog(installation="classical"):
    """Stand-in for the frozen spec catalog (P§1), compiled into every TEST release."""
    if installation == "hybrid":
        cat = catalog()
        cat.update({"alg": ALG_HYBRID, "spec_sha256": hashlib.sha256(SPEC_BYTES_HYBRID).hexdigest(),
                    "TEST": "conformance universe catalog, hybrid-registered installation (pair id registered by "
                            "the TEST branch-registration supplement stand-in); not the frozen catalog"})
        return cat
    return {
        "alg": ALG_V1,
        "alg_prohibited": [],
        "binding_forms": ["STMT_DIRECT"],
        "D": D,
        "delta_s": str(DELTA),
        "dependency_manifest_sha256": hashlib.sha256(DEP_BYTES).hexdigest(),
        "dnssec_algorithms": ["13", "8"],
        "ds_digest_types": ["2", "4"],
        "epsilon_s": str(EPS),
        "k": str(K),
        "preamble_sha256": hashlib.sha256(PREAMBLE_BYTES).hexdigest(),
        "spec_id": SPEC_ID,
        "spec_sha256": hashlib.sha256(SPEC_BYTES).hexdigest(),
        "vectors_sha256": hashlib.sha256(VECTORS_BYTES).hexdigest(),
        "TEST": "conformance universe catalog; not the frozen catalog",
    }


# ----------------------------------------------------------------------------------------------- root KSKs
def ksk_a():
    return zkey("root-KSK-A(TEST-2017)", 8, 257)


def ksk_b():
    return zkey("root-KSK-B(TEST-2024)", 8, 257)


KSK_A_PERIOD = ("2018-10-11T16:00:00Z", "2026-10-11T00:00:00Z")   # mirrors P§5 KSK-2017 policy values
KSK_B_START = "2026-10-11T00:00:00Z"                               # mirrors P§5 KSK-2024 policy start
RELIANCE_L = 1814400                                               # 21 days, P§5


def _src(desc):
    return [{"description": "TEST " + desc, "sha256": hashlib.sha256(("TEST source " + desc).encode()).hexdigest(),
             "uri": "test:" + desc.replace(" ", "-")}]


def ksk_entry(name, key, start, end, publication=None, revocation=None, L=RELIANCE_L, rdata=None):
    rd = key.rdata() if rdata is None else rdata
    return {"algorithm": str(rd[3]), "dnskey_rdata": b64(rd), "ds_sha256": hashlib.sha256(b"\x00" + rd).hexdigest(),
            "key_tag": str(key_tag(rd)), "name": name, "publication": publication,
            "reliance_lifetime_s": str(L), "revocation": revocation, "signing_end": end, "signing_start": start,
            "sources": _src(name)}


def trust_config(pins, as_of="2026-12-31T00:00:00Z", repo_entries=None, root_ksks=None, version="1",
                 previous=None):
    if root_ksks is None:
        root_ksks = [ksk_entry("TEST-KSK-A", ksk_a(), *KSK_A_PERIOD, publication="2017-08-11T00:00:00Z",
                               revocation="2027-01-11T00:00:00Z"),
                     ksk_entry("TEST-KSK-B", ksk_b(), KSK_B_START, None, publication="2024-07-01T00:00:00Z")]
        root_ksks.sort(key=lambda e: (ts(e["signing_start"]), int(e["key_tag"]), base64.b64decode(e["dnskey_rdata"])))
    if repo_entries is None:
        repo_entries = [repo_entry(Keys.p256("repository-key", 1759276800))]
    return {"as_of": as_of, "format": "tessera-v1-trust/1", "header_pins": pins, "issuer_domain": D,
            "previous_sha256": previous or "0" * 64, "profile": PROFILE, "repository_keys": repo_entries,
            "root_ksks": root_ksks, "version": version}


def repo_entry(key, start="2026-10-01T00:00:00Z", end=None, domain=D):
    return {"domain": domain, "key": b64(key.pgp_body), "signing_end": end, "signing_start": start,
            "sources": _src("repository key " + key.seed)}


# ----------------------------------------------------------------------------------------------- release
def release_key():
    return Keys.p256("release-key")


def make_release(trust_bytes, signer=None, catalog_obj=None):
    """TEST release record: the one compiled trust-config hash plus the compiled catalog hash, signed (raw ECDSA
    P-256 over SHA-256 of the JCS release body, RFC 6979). The release-signature format is OPEN in the profile
    (P§14.2 item 2); this is a TEST stand-in."""
    signer = signer or release_key()
    cat = catalog_obj or catalog()
    body = {"catalog": cat, "catalog_sha256": hashlib.sha256(jcs(cat)).hexdigest(),
            "format": "tessera-v1-test-release/1",
            "trust_config_sha256": hashlib.sha256(trust_bytes).hexdigest()}
    r, s = signer.sign_digest(sha256(jcs(body)))
    return {"release": body,
            "signature": {"alg": "ECDSA-P256-SHA256", "r_s_hex": f"{r:064x}{s:064x}",
                          "signer_spki_sha256": hashlib.sha256(signer.spki).hexdigest()}}


def release_public():
    k = release_key()
    return {"TEST": "release public key of the conformance universe; bootstrap value for TEST releases only",
            "spki_b64": b64(k.spki), "spki_sha256": hashlib.sha256(k.spki).hexdigest()}
