"""Stand-ins for local runs and tests: a synthetic Bitcoin chain, an OpenTimestamps calendar on it, a TEST DNSSEC
hierarchy for wamason.com, a TEST repository key and key-assertion commit, window preparation, and the relying
party's TEST trust configuration and TEST release record. Everything is TEST-labelled and nothing is mainnet.

The calendar, explorer and resolver stand-ins also serve the wire protocols (serve_*), so the real clients in
ots.py, chain.py and dns.py are exercised against them."""
import hashlib
import json
import struct

from tessera_verify.release_auth import jcs_ascii

from . import ots
from .chain import HeaderSource, pin_of
from .dns import QUERIES, T_DNSKEY, T_DS, T_RRSIG, T_TXT, SnapshotSource, name_wire
from .encode import assertion_value, txt_rdata
from .testkeys import MLDSA65Key, P256Key, armor, drbg, pgp_sign
from .util import DAY, HOUR, b64e, jcs, rfc3339, sha256, sha256d, sha256hex
from .window import Window

U32 = 1 << 32


# ------------------------------------------------------------------------------------------------ chain
def _compact(n):
    return bytes([n]) if n < 253 else b"\xfd" + struct.pack("<H", n)


class StandInChain(HeaderSource):
    """Blocks are mined explicitly (mine()); each block's nTime is the clock, strictly increasing. Calendars
    attached with attach() have their pending commitments included in the next block."""

    def __init__(self, clock, base_height=950000):
        self.clock, self.base = clock, base_height
        self.blocks = {base_height: {"time": clock() - 600, "txs": [sha256d(b"TEST coinbase %d" % base_height)]}}
        self.tip_h = base_height
        self.calendars = []

    def attach(self, cal):
        self.calendars.append(cal)

    def mine(self, n=1):
        for _ in range(n):
            h = self.tip_h + 1
            t = max(self.clock(), self.blocks[self.tip_h]["time"] + 1)
            txs = [sha256d(b"TEST coinbase %d" % h)]
            for cal in self.calendars:
                txs += cal.include(h)
            self.blocks[h] = {"time": t, "txs": txs}
            self.tip_h = h
        return self.tip_h

    def tip(self):
        return self.tip_h

    def _levels(self, h):
        level = list(self.blocks[h]["txs"])
        levels = [level]
        while len(level) > 1:
            if len(level) % 2:
                level = level + [level[-1]]
            level = [sha256d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
            levels.append(level)
        return levels

    def merkle_path(self, h, txid):
        """Conventional suffix (profile 15.2): (append | prepend 32 bytes, sha256, sha256) per level."""
        levels = self._levels(h)
        idx, ops = levels[0].index(txid), []
        for level in levels[:-1]:
            lv = level + [level[-1]] if len(level) % 2 else level
            ops.append((0xF0, lv[idx + 1]) if idx % 2 == 0 else (0xF1, lv[idx - 1]))
            ops += [(0x08, b""), (0x08, b"")]
            idx //= 2
        return ops

    def header(self, h):
        b = self.blocks[h]
        if "header" not in b:                        # a mined block never changes
            prev = sha256d(self.header(h - 1)) if h - 1 in self.blocks else sha256d(b"TEST pre-chain")
            root = self._levels(h)[-1][0]
            b["header"] = (struct.pack("<i", 0x20000000) + prev + root + struct.pack("<I", b["time"] % U32)
                           + struct.pack("<I", 0x17030ECD) + struct.pack("<I", h & 0xFFFFFFFF))
        return b["header"]

    def headers(self, heights):
        out = {}
        for h in sorted(heights):
            if h not in self.blocks:
                raise KeyError(f"no block {h}")
            out[h] = self.header(h)
        return out

    def serve_esplora(self, method, url, body):
        """Esplora-style explorer API for chain.ExplorerHeaders."""
        path = url.split("://", 1)[-1].split("/", 1)[1]
        parts = path.split("/")
        if parts[-3:] == ["blocks", "tip", "height"]:
            return 200, str(self.tip_h).encode()
        if "block-height" in parts:
            h = int(parts[-1])
            return (200, pin_of(self.header(h)).encode()) if h in self.blocks else (404, b"")
        if parts[-1] == "header":
            for h in self.blocks:
                if pin_of(self.header(h)) == parts[-2]:
                    return 200, self.header(h).hex().encode()
            return 404, b""
        return 404, b""


class StandInCalendar:
    """A calendar that, at each mined block, puts one OP_RETURN transaction per pending commitment into it."""

    def __init__(self, chain, uri="https://stand-in-calendar.invalid"):
        self.chain, self.uri = chain, uri
        self.pending, self.mined = [], {}           # commitment -> (height, prefix, suffix, txid)
        chain.attach(self)

    def _tx(self, m):
        prevout = drbg("prevout:" + m.hex(), 32) + struct.pack("<I", 0)
        script_sig = drbg("scriptsig:" + m.hex(), 31)
        inp = prevout + _compact(len(script_sig)) + script_sig + b"\xff\xff\xff\xff"
        prefix = struct.pack("<i", 2) + b"\x01" + inp + b"\x01" + struct.pack("<q", 0) + _compact(34) + b"\x6a\x20"
        return prefix, struct.pack("<I", 0)

    def include(self, h):
        txids = []
        for m in self.pending:
            prefix, suffix = self._tx(m)
            txid = sha256d(prefix + m + suffix)
            self.mined[m] = (h, prefix, suffix, txid)
            txids.append(txid)
        self.pending = []
        return txids

    def submit(self, message):
        if message not in self.mined and message not in self.pending:
            self.pending.append(message)
        node = ots.Node()
        node.att(ots.PENDING, ots.pending_payload(self.uri))
        return node.ser()

    def fetch(self, commitment):
        if commitment not in self.mined:
            return None
        h, prefix, suffix, txid = self.mined[commitment]
        root = ots.Node()
        node = root.op(0xF1, prefix).op(0xF0, suffix).op(0x08).op(0x08)
        for opcode, arg in self.chain.merkle_path(h, txid):
            node = node.op(opcode, arg)
        node.att(ots.BTC, ots._varuint(h))
        return root.ser()

    def serve(self, method, url, body):
        """The calendar HTTP protocol for ots.HttpCalendar."""
        if method == "POST" and url == self.uri + "/digest":
            return 200, self.submit(body)
        if method == "GET" and url.startswith(self.uri + "/timestamp/"):
            got = self.fetch(bytes.fromhex(url.rsplit("/", 1)[1]))
            return (200, got) if got else (404, b"")
        return 404, b""


# ------------------------------------------------------------------------------------------------ DNS
def key_tag(rdata):
    ac = 0
    for i, b in enumerate(rdata):
        ac += b if i & 1 else b << 8
    ac += (ac >> 16) & 0xFFFF
    return ac & 0xFFFF


class ZoneKey:
    """A TEST DNSSEC key, algorithm 13 (ECDSA P-256 SHA-256)."""

    def __init__(self, seed, ksk):
        self.k = P256Key("dns:" + seed)
        self.flags = 257 if ksk else 256

    @property
    def rdata(self):
        return struct.pack(">HBB", self.flags, 3, 13) + self.k.point[1:]

    @property
    def tag(self):
        return key_tag(self.rdata)


def ds_rdata(owner, key):
    return struct.pack(">HBB", key.tag, 13, 2) + hashlib.sha256(name_wire(owner) + key.rdata).digest()


def _labels(owner):
    return len([x for x in owner.rstrip(".").split(".") if x])


def rrsig(owner, rtype, rdatas, ttl, key, signer, inception, expiration):
    head = struct.pack(">HBBIIIH", rtype, 13, _labels(owner), ttl, expiration % U32, inception % U32, key.tag) \
        + name_wire(signer)
    ow = name_wire(owner)
    data = head + b"".join(ow + struct.pack(">HHIH", rtype, 1, ttl, len(r)) + r for r in sorted(rdatas))
    return head + key.k.sign_raw(data)


class StandInDns(SnapshotSource):
    """The TEST hierarchy . -> com -> wamason.com -> _tessera-v1.wamason.com TXT = the window's assertion value.
    RRSIGs are made at capture time, valid from 5 days before to 10 days after it."""

    def __init__(self, value, seed="stand-in"):
        self.value = value
        z = lambda n, ksk: ZoneKey(f"{seed}:{n}", ksk)  # noqa: E731
        self.root_ksk, self.root_zsk = z("root-ksk", True), z("root-zsk", False)
        self.com_ksk, self.com_zsk = z("com-ksk", True), z("com-zsk", False)
        self.w_ksk, self.w_zsk = z("w-ksk", True), z("w-zsk", False)
        self.captures = 0

    def groups(self, now):
        inc, exp = now - 5 * DAY, now + 10 * DAY
        D = "wamason.com."
        plan = [(".", T_DNSKEY, [self.root_ksk.rdata, self.root_zsk.rdata], 172800, self.root_ksk, "."),
                ("com.", T_DS, [ds_rdata("com.", self.com_ksk)], 86400, self.root_zsk, "."),
                ("com.", T_DNSKEY, [self.com_ksk.rdata, self.com_zsk.rdata], 86400, self.com_ksk, "com."),
                (D, T_DS, [ds_rdata(D, self.w_ksk)], 86400, self.com_zsk, "com."),
                (D, T_DNSKEY, [self.w_ksk.rdata, self.w_zsk.rdata], 3600, self.w_ksk, D),
                ("_tessera-v1." + D, T_TXT, [txt_rdata(self.value)], 300, self.w_zsk, D)]
        return [(o, t, rds, ttl, rrsig(o, t, rds, ttl, k, s, inc, exp)) for o, t, rds, ttl, k, s in plan]

    def capture(self, now):
        self.captures += 1
        body = b""
        for owner, t, rds, ttl, sig in self.groups(now):
            ow = name_wire(owner)
            for r in sorted(rds):
                body += ow + struct.pack(">HHIH", t, 1, ttl, len(r)) + r
            body += ow + struct.pack(">HHIH", T_RRSIG, 1, ttl, len(sig)) + sig
        return body

    def serve(self, clock):
        """A resolver transport for dns.LiveDns: answers with the owner name compressed to the question."""
        def t(query):
            groups = {(o.rstrip(".") or ".", t): (rds, ttl, sig) for o, t, rds, ttl, sig in self.groups(clock())}
            qid = query[:2]
            i, labels = 12, []
            while query[i]:
                labels.append(query[i + 1:i + 1 + query[i]].decode())
                i += 1 + query[i]
            qtype = struct.unpack(">H", query[i + 1:i + 3])[0]
            qname = ".".join(labels) or "."
            question = query[12:i + 5]
            rds, ttl, sig = groups[(qname, qtype)]
            answers = [(qtype, r) for r in rds] + [(T_RRSIG, sig)]
            msg = qid + struct.pack(">HHHHH", 0x8180, 1, len(answers), 0, 0) + question
            for rt, rd in answers:
                msg += b"\xc0\x0c" + struct.pack(">HHIH", rt, 1, ttl, len(rd)) + rd
            return msg
        return t

    def root_entries(self, start):
        out = []
        for name, k in (("TEST-ROOT-KSK (stand-in)", self.root_ksk),):
            rd = k.rdata
            out.append({"algorithm": "13", "dnskey_rdata": b64e(rd), "ds_sha256": sha256hex(b"\x00" + rd),
                        "key_tag": str(k.tag), "name": name, "publication": None, "reliance_lifetime_s": "1814400",
                        "revocation": None, "signing_end": None, "signing_start": start,
                        "sources": [{"description": "TEST stand-in root KSK; not a real DNS key",
                                     "sha256": sha256hex(rd), "uri": "test:stand-in-root-ksk"}]})
        return out


# ------------------------------------------------------------------------------------------------ git
def git_id(kind, body):
    return hashlib.sha1(f"{kind} {len(body)}".encode() + b"\x00" + body).digest()


def tree(entries):
    es = sorted(entries, key=lambda e: e[1].encode() + (b"/" if e[0] == "40000" else b""))
    return b"".join(m.encode() + b" " + n.encode() + b"\x00" + oid for m, n, oid in es)


def signed_commit(value, repo_key, when):
    """The key-assertion commit: tessera-v1/key-assertion = value, gpgsig by the TEST repository key."""
    readme = b"TEST issuer repository (stand-in). Not the Tessera repository.\n"
    sub = tree([("100644", "key-assertion", git_id("blob", value))])
    root = tree([("100644", "README", git_id("blob", readme)), ("40000", "tessera-v1", git_id("tree", sub))])
    ident = f"TEST Issuer <test-issuer@wamason.com> {when} +0000".encode()
    payload = b"tree " + git_id("tree", root).hex().encode() + b"\nauthor " + ident + b"\ncommitter " + ident + \
        b"\n\nTEST: publish the tessera-v1 key assertion\n"
    lines = armor(pgp_sign(payload, repo_key, when)).split("\n")
    gpgsig = ("gpgsig " + lines[0] + "\n" + "".join(" " + ln + "\n" for ln in lines[1:])).encode()
    end = payload.index(b"\n\n") + 1
    commit = payload[:end] + gpgsig + payload[end:]
    return commit, [root, sub], value


# ------------------------------------------------------------------------------------------------ world
class World:
    """Every stand-in a local issuer needs, on one clock."""

    def __init__(self, clock, seed="stand-in"):
        self.clock, self.seed = clock, seed
        self.chain = StandInChain(clock)
        self.calendar = StandInCalendar(self.chain)
        self.kms_key = MLDSA65Key(f"{seed}:kms")
        self.gpg_key = P256Key(f"{seed}:gpg", created=clock() - 30 * DAY)
        self.repo_key = P256Key(f"{seed}:repository", created=clock() - 30 * DAY)
        self.dns = None
        self.window = None

    def prepare_window(self, not_before, not_after):
        """The operator's window preparation, with stand-ins: assertion value, signed commit, its stamp taken to
        k = 6, the DNS record published. -> Window."""
        value = assertion_value(self.kms_key.fp_kms, self.gpg_key.fp_gpg, not_before, not_after)
        commit, trees, blob = signed_commit(value, self.repo_key, self.clock() - HOUR)
        stamp_input = (git_id("commit", commit).hex() + "\n").encode()
        proof = ots.stamp(sha256(stamp_input), [self.calendar], drbg("git-nonce:" + self.seed, 16))
        for _ in range(6):
            self.clock.advance(600)
            self.chain.mine(1)
        proof, _ = ots.upgrade(proof, [self.calendar])
        self.dns = StandInDns(value, self.seed)
        start = rfc3339(self.clock() - 60 * DAY)
        trust_base = {"root_ksks": self.dns.root_entries(start),
                      "repository_keys": [{"domain": "wamason.com", "key": b64e(self.repo_key.pgp_body),
                                           "signing_end": None, "signing_start": start,
                                           "sources": [{"description": "TEST stand-in repository key",
                                                        "sha256": sha256hex(self.repo_key.pgp_body),
                                                        "uri": "test:stand-in-repository-key"}]}]}
        self.window = Window(not_before, not_after, self.kms_key.spki, self.gpg_key.pgp_body, value,
                             {"commit": commit, "trees": trees, "blob": blob, "ots": proof}, trust_base).check()
        return self.window


def relying_party_trust(window, headers, as_of):
    """The relying party's TEST trust configuration: the window's entries plus pins for the given headers."""
    from .preship import trust_object
    return jcs(trust_object(window.trust_base, {h: pin_of(v) for h, v in headers.items()}, as_of))


def make_test_release(trust_bytes, catalog_obj, release_key):
    """A `tessera-v1-test-release/1` record (the verifier's TEST harness interface, never a release) and the key
    file. -> (release bytes, key bytes)."""
    cat = dict(catalog_obj, TEST="frozen catalog provisioned for an issuer stand-in run; TEST authority only")
    body = {"catalog": cat, "catalog_sha256": hashlib.sha256(jcs_ascii(cat)).hexdigest(),
            "format": "tessera-v1-test-release/1", "trust_config_sha256": sha256hex(trust_bytes)}
    rs = release_key.sign_raw(jcs_ascii(body))
    spki_sha = sha256hex(release_key.spki)
    rel = {"release": body, "signature": {"alg": "ECDSA-P256-SHA256", "r_s_hex": rs.hex(), "signer_spki_sha256": spki_sha}}
    key = {"TEST": "TEST release key of the issuer stand-in run", "spki_b64": b64e(release_key.spki),
           "spki_sha256": spki_sha}
    return json.dumps(rel).encode(), json.dumps(key).encode()
