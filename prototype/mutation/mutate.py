#!/usr/bin/env python3
"""Deterministic mutant generator for the V1 false-accept mutation campaign.

Seeds: the 52 VALID_STRICT bundle cases of prototype/conformance/cases-index.json. Every mutant is regenerated from
the seed bytes and a fixed per-(operator, seed) PRNG string, so a mutant id always denotes the same bytes.

  mutate.py --count                       print mutant counts per operator (and per seed with --verbose)
  mutate.py --emit MID --out FILE         write mutant MID's bundle bytes to FILE; print its metadata and the
                                          verifier command (repository root, adapter, as in differential/ADAPTER.md)

Mutant id: <op>/<seed>/<n>, n the 0-based index within that operator's deterministic list for that seed.
Operators (see REPORT.md): op1 bit flips in signed bytes (A_sig incl. frames and receipt signatures, manifest,
possession signatures, git commit signature); op1x sampled bit flips in every other member; op2 member swaps
between seeds; op3 evidence transplants; op4 structural and re-encoding changes; op5 semantic edits with and
without re-signing under TEST keys that are not in any trust configuration.

Reads only: prototype/conformance/{cases,cases-index.json}, formal/p8/vectors/gen.py and the conformance TEST
helpers (tcrypto, universe) for encoders. Writes nothing except --out.
"""
import argparse
import base64
import copy
import hashlib
import json
import random
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CONF = REPO / "prototype" / "conformance"
sys.path.insert(0, str(CONF))
sys.setrecursionlimit(20000)
import tcrypto as tc  # noqa: E402
import universe as U  # noqa: E402
from tcrypto import gen  # noqa: E402

CASES = CONF / "cases"
OPS = ("op1", "op1x", "op2", "op3", "op4", "op5", "op6")


def b64e(b):
    return base64.b64encode(b).decode()


def b64d(s):
    return base64.b64decode(s, validate=True)


def jcs(obj):
    return U.jcs(obj)


# ----------------------------------------------------------------------------------------------- seeds
def seed_ids():
    idx = json.loads((CONF / "cases-index.json").read_text())
    return [c["id"] for c in idx if c["kind"] == "bundle" and c["expected"].startswith("VALID_STRICT")]


def all_bundle_ids():
    idx = json.loads((CONF / "cases-index.json").read_text())
    return [c["id"] for c in idx if c["kind"] == "bundle" and (CASES / c["id"] / "bundle.json").exists()]


_LOAD = {}


def load(cid):
    if cid not in _LOAD:
        raw = (CASES / cid / "bundle.json").read_bytes()
        try:
            obj = json.loads(raw)
            layer = obj["layers"][0] if isinstance(obj, dict) and isinstance(obj.get("layers"), list) \
                and obj["layers"] and isinstance(obj["layers"][0], dict) else None
        except Exception:
            obj, layer = None, None
        _LOAD[cid] = {"raw": raw, "obj": obj, "layer": layer}
    return _LOAD[cid]


def container(layer):
    return jcs({"layers": [layer], "profile": "tessera-v1-strict"})


def get_path(layer, path):
    o = layer
    for p in path:
        o = o[int(p)] if isinstance(o, list) else o[p]
    return o


def set_path(layer, path, value):
    o = layer
    for p in path[:-1]:
        o = o[int(p)] if isinstance(o, list) else o[p]
    k = path[-1]
    if isinstance(o, list):
        o[int(k)] = value
    else:
        o[k] = value


def del_path(layer, path):
    o = layer
    for p in path[:-1]:
        o = o[int(p)] if isinstance(o, list) else o[p]
    k = path[-1]
    if isinstance(o, list):
        del o[int(k)]
    else:
        del o[k]


def leaves(o, path=()):
    if isinstance(o, dict):
        for k in sorted(o):
            yield from leaves(o[k], path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, o


def objects(o, path=()):
    """Every JSON object/array node with its path (the layer included)."""
    if isinstance(o, (dict, list)):
        yield path, o
        items = sorted(o.items()) if isinstance(o, dict) else [(str(i), v) for i, v in enumerate(o)]
        for k, v in items:
            yield from objects(v, path + (k,))


def pstr(path):
    return ".".join(path)


# ----------------------------------------------------------------------------------------------- locators
def sig_regions(sig):
    """OpenPGP v4 signature packet -> list of (start, end, label). Robust to odd input."""
    out = []
    try:
        if sig[0] == 0x88:
            hl = 2
        elif sig[0] == 0x89:
            hl = 3
        elif sig[0] == 0xC2:
            hl = 2
        else:
            return [(0, len(sig), "sig?")]
        out.append((0, hl, "pkt_header"))
        i = hl
        out.append((i, i + 4, "ver/type/pubalg/hashalg"))
        i += 4
        hlen = struct.unpack(">H", sig[i:i + 2])[0]
        out.append((i, i + 2, "hashed_len"))
        i += 2
        out += _subpacket_regions(sig, i, i + hlen, "hashed")
        i += hlen
        ulen = struct.unpack(">H", sig[i:i + 2])[0]
        out.append((i, i + 2, "unhashed_len"))
        i += 2
        out += _subpacket_regions(sig, i, i + ulen, "unhashed")
        i += ulen
        out.append((i, i + 2, "left16"))
        i += 2
        for nm in ("r", "s"):
            bl = struct.unpack(">H", sig[i:i + 2])[0]
            out.append((i, i + 2, f"{nm}_bitlen"))
            i += 2
            n = (bl + 7) // 8
            out.append((i, i + n, f"{nm}_value"))
            i += n
        if i < len(sig):
            out.append((i, len(sig), "trailing"))
    except Exception:
        out.append((0, len(sig), "sig?"))
    return out


def _subpacket_regions(b, i, end, area):
    out = []
    while i < end:
        o1 = b[i]
        if o1 < 192:
            ln, ll = o1, 1
        elif o1 < 255:
            ln, ll = ((o1 - 192) << 8) + b[i + 1] + 192, 2
        else:
            ln, ll = struct.unpack(">I", b[i + 1:i + 5])[0], 5
        typ = b[i + ll] & 0x7F
        out.append((i, i + ll, f"{area}.sp{typ}.len"))
        out.append((i + ll, i + ll + 1, f"{area}.sp{typ}.type"))
        out.append((i + ll + 1, i + ll + ln, f"{area}.sp{typ}.data"))
        i += ll + ln
    return out


def frame_regions(fr, name):
    out = []
    tl = fr[0]
    out.append((0, 1 + tl, f"{name}.tag"))
    out.append((1 + tl, 3 + tl, f"{name}.cv"))
    out.append((3 + tl, 7 + tl, f"{name}.payload_len"))
    payload = fr[7 + tl:]
    base = 7 + tl
    # attribute payload bytes to the innermost JSON key whose text span contains them (approximate)
    text = payload.decode("utf-8", "replace")
    try:
        spans = _json_spans(payload)
    except Exception:
        spans = []
    for s, e, k in spans:
        out.append((base + s, base + e, f"{name}.payload.{k}"))
    out.append((base, base + len(payload), f"{name}.payload"))
    del text
    return out


def _json_spans(b):
    """Byte spans of leaf values in a JCS payload, keyed by dotted path. Minimal scanner over canonical JSON."""
    spans = []
    s = b.decode("utf-8")
    # map char index -> byte index
    cidx = []
    bi = 0
    for ch in s:
        cidx.append(bi)
        bi += len(ch.encode("utf-8"))
    cidx.append(bi)
    dec = json.JSONDecoder()

    def walk(i, path):
        if s[i] == "{":
            i += 1
            if s[i] == "}":
                return i + 1
            while True:
                key, j = dec.raw_decode(s, i)
                i = j + 1  # colon
                i = walk(i, path + [key])
                if s[i] == ",":
                    i += 1
                    continue
                return i + 1
        if s[i] == "[":
            i += 1
            if s[i] == "]":
                return i + 1
            n = 0
            while True:
                i = walk(i, path + [str(n)])
                n += 1
                if s[i] == ",":
                    i += 1
                    continue
                return i + 1
        _, j = dec.raw_decode(s, i)
        spans.append((cidx[i], cidx[j], ".".join(path)))
        return j

    walk(0, [])
    return spans


def asig_parts(a):
    """A_sig -> (header_len, [(start, end) of F_kms, S_kms, F_gpg, S_gpg]) or None."""
    try:
        tl = a[0]
        i = 1 + tl + 1
        parts = []
        for _ in range(4):
            n = struct.unpack(">I", a[i:i + 4])[0]
            parts.append((i + 4, i + 4 + n))
            i += 4 + n
        return 1 + tl, parts
    except Exception:
        return None


def asig_regions(a):
    pr = asig_parts(a)
    if pr is None:
        return [(0, len(a), "a_sig?")]
    hl, parts = pr
    out = [(0, hl, "a_sig.tag"), (hl, hl + 1, "a_sig.count")]
    for (s, e), nm in zip(parts, ("F_kms", "S_kms", "F_gpg", "S_gpg")):
        out.append((s - 4, s, f"a_sig.len({nm})"))
        reg = frame_regions(a[s:e], nm) if nm.startswith("F") else [(x, y, f"{nm}.{l}") for x, y, l in sig_regions(a[s:e])]
        out += [(s + x, s + y, l) for x, y, l in reg]
    return out


def locate(regions, off):
    """Most specific (shortest) region containing off."""
    best = None
    for s, e, l in regions:
        if s <= off < e and (best is None or e - s < best[1] - best[0]):
            best = (s, e, l)
    return best[2] if best else "?"


# ----------------------------------------------------------------------------------------------- OTS
OTS_MAGIC = bytes.fromhex("004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e89294")
BTC_TAG = bytes.fromhex("0588960d73d71901")
PEND_TAG = bytes.fromhex("83dfe30d2ef90c8e")


def _varuint(b, i):
    v, sh = 0, 0
    while True:
        x = b[i]
        i += 1
        v |= (x & 0x7F) << sh
        sh += 7
        if not x & 0x80:
            return v, i


def ots_parse(b):
    """-> (root_offset, root node). node = list of items {s, e, kind, att, height, child}."""
    assert b[:len(OTS_MAGIC)] == OTS_MAGIC
    i = len(OTS_MAGIC)
    _, i = _varuint(b, i)
    assert b[i] == 0x08
    i += 1 + 32
    root = i
    node, j = _ts(b, i)
    return root, node, j


def _ts(b, i):
    items = []
    while True:
        last = b[i] != 0xFF
        if not last:
            i += 1
        it, i = _item(b, i)
        items.append(it)
        if last:
            return items, i


def _item(b, i):
    s = i
    op = b[i]
    if op == 0x00:
        tag = b[i + 1:i + 9]
        n, j = _varuint(b, i + 9)
        payload = b[j:j + n]
        e = j + n
        if tag == BTC_TAG:
            h, _ = _varuint(payload, 0)
            return {"s": s, "e": e, "kind": "btc", "height": h}, e
        return {"s": s, "e": e, "kind": "pending" if tag == PEND_TAG else "other"}, e
    i += 1
    if op in (0xF0, 0xF1):
        n, i = _varuint(b, i)
        i += n
    child, e = _ts(b, i)
    return {"s": s, "e": e, "kind": "op", "child": child}, e


def ots_leaves_at(node, off):
    """All attestations at or below the deepest item containing byte offset off."""
    for it in node:
        if it["s"] <= off < it["e"]:
            if it["kind"] == "op":
                inner = ots_leaves_at(it["child"], off)
                return inner if inner is not None else _all_leaves(it["child"])
            return [it]
    return None


def _all_leaves(node):
    out = []
    for it in node:
        if it["kind"] == "op":
            out += _all_leaves(it["child"])
        else:
            out.append(it)
    return out


def ots_all_leaves(b):
    try:
        _, node, _ = ots_parse(b)
        return _all_leaves(node)
    except Exception:
        return []


# ----------------------------------------------------------------------------------------------- git helpers
def parse_tree(body):
    out, i = [], 0
    while i < len(body):
        sp = body.index(b" ", i)
        nul = body.index(b"\x00", sp)
        out.append((body[i:sp].decode(), body[sp + 1:nul].decode(), body[nul + 1:nul + 21]))
        i = nul + 21
    return out


def split_commit(commit):
    """-> (payload_without_gpgsig, armored_signature_text)."""
    lines = commit.split(b"\n")
    out, sig, i = [], [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(b"gpgsig "):
            sig.append(ln[7:])
            i += 1
            while i < len(lines) and lines[i].startswith(b" "):
                sig.append(lines[i][1:])
                i += 1
            continue
        out.append(ln)
        i += 1
    return b"\n".join(out), b"\n".join(sig).decode()


def dearmor(text):
    lines = text.split("\n")
    body = [ln for ln in lines[2:-1] if not ln.startswith("=")]
    crc = [ln for ln in lines[2:-1] if ln.startswith("=")]
    return b64d("".join(body)), bool(crc)


def rebuild_commit(commit, new_sig=None, tree_id=None, payload_override=None):
    payload, arm = split_commit(commit)
    if tree_id is not None:
        payload = b"tree " + tree_id.encode() + payload[45:]
    sig_bytes, has_crc = dearmor(arm)
    if new_sig is not None:
        sig_bytes = new_sig
    arm2 = tc.armor(sig_bytes, crc="good" if has_crc else "none")
    # re-insert gpgsig after the committer line (the issuer's layout, issue.py finalize_git)
    head, msg = payload.split(b"\n\n", 1)
    return head + b"\n" + U.gpgsig_header(arm2) + b"\n" + msg, payload


# ----------------------------------------------------------------------------------------------- attacker keys
ATT_KMS = tc.P256Key("mutation-attacker-kms")
ATT_GPG = tc.P256Key("mutation-attacker-gpg", 1790000000)
ATT_REPO = tc.P256Key("mutation-attacker-repo", 1759276800)


def decode_asig(a):
    hl, parts = asig_parts(a)
    return [a[s:e] for s, e in parts]


def frame_payload(fr):
    tl = fr[0]
    return gen.decode_payload(fr[7 + tl:])   # number-preserving (L-111a), canonical


def make_frame_like(fr, value):
    tl = fr[0]
    tag = fr[1:1 + tl]
    return gen.frame(tag, jcs(value))


def sig_created(sig):
    for s, e, l in sig_regions(sig):
        if l == "hashed.sp2.data":
            return struct.unpack(">I", sig[s:e])[0]
    return 1790000000


# ----------------------------------------------------------------------------------------------- mutant record
class M:
    __slots__ = ("op", "sub", "desc", "bundle", "meta")

    def __init__(self, op, sub, desc, bundle, **meta):
        self.op, self.sub, self.desc, self.bundle, self.meta = op, sub, desc, bundle, meta


# ----------------------------------------------------------------------------------------------- op1
def op1(seed):
    """Single bit flip in every byte of A_sig (frames, receipt signatures, framing), the manifest, each possession
    signature and the dearmored git commit signature. Bit index per byte from a seeded PRNG."""
    L = load(seed)["layer"]
    rng = random.Random(f"op1|{seed}")
    out = []
    targets = [("a_sig", ("a_sig",)), ("manifest", ("manifest",)), ("possession.kms", ("possession", "kms")),
               ("possession.gpg", ("possession", "gpg"))]
    for name, path in targets:
        data = b64d(get_path(L, path))
        if name == "a_sig":
            regs = asig_regions(data)
        elif name == "manifest":
            regs = frame_regions(data, "F_manifest")
        else:
            regs = [(s, e, f"{name}.{l}") for s, e, l in sig_regions(data)]
        for i in range(len(data)):
            bit = rng.randrange(8)
            mb = bytearray(data)
            mb[i] ^= 1 << bit
            lay = copy.deepcopy(L)
            set_path(lay, path, b64e(bytes(mb)))
            out.append(M("op1", name, f"{name} byte {i} bit {bit}", container(lay), member=name, offset=i, bit=bit,
                         region=locate(regs, i)))
    # git commit signature (dearmored), re-armored with the same CRC presence and re-inserted
    commit = b64d(L["git"]["commit"])
    _, arm = split_commit(commit)
    sig, _ = dearmor(arm)
    regs = [(s, e, f"git_sig.{l}") for s, e, l in sig_regions(sig)]
    for i in range(len(sig)):
        bit = rng.randrange(8)
        mb = bytearray(sig)
        mb[i] ^= 1 << bit
        c2, _ = rebuild_commit(commit, new_sig=bytes(mb))
        lay = copy.deepcopy(L)
        lay["git"]["commit"] = b64e(c2)
        out.append(M("op1", "git_sig", f"git commit signature byte {i} bit {bit}", container(lay), member="git_sig",
                     offset=i, bit=bit, region=locate(regs, i)))
    return out


# ----------------------------------------------------------------------------------------------- op1x
OP1X_CAP = {"keys.kms": 64, "keys.gpg": 64, "receipt_anchor.ots": 400, "dns.ots": 400, "git.ots": 400,
            "dns.snapshot_body": 96, "git.commit": 64, "git.trees.0": 32, "git.trees.1": 32, "git.blob": 48,
            "spec": 8, "vectors": 8, "preamble": 8, "dependency_manifest": 8, "receipt_anchor.txid": 32}


def op1x(seed):
    """Sampled single bit flips in every other member (decoded bytes; hex for txid and headers; raw characters for
    issuer_record and object_format). OTS proofs are covered byte-for-byte up to 400 bytes, then sampled."""
    L = load(seed)["layer"]
    rng = random.Random(f"op1x|{seed}")
    out = []
    for name, cap in OP1X_CAP.items():
        path = tuple(name.split("."))
        sval = get_path(L, path)
        data = bytes.fromhex(sval) if name == "receipt_anchor.txid" else b64d(sval)
        n = len(data)
        pos = list(range(n)) if n <= cap else sorted(set([0, n - 1] + rng.sample(range(n), cap - 2)))
        for i in pos:
            bit = rng.randrange(8)
            mb = bytearray(data)
            mb[i] ^= 1 << bit
            lay = copy.deepcopy(L)
            set_path(lay, path, bytes(mb).hex() if name == "receipt_anchor.txid" else b64e(bytes(mb)))
            out.append(M("op1x", name, f"{name} byte {i} bit {bit}", container(lay), member=name, offset=i, bit=bit))
    for h in sorted(L["headers"], key=int):
        raw = bytes.fromhex(L["headers"][h])
        for i in sorted(rng.sample(range(80), 4)):
            bit = rng.randrange(8)
            mb = bytearray(raw)
            mb[i] ^= 1 << bit
            lay = copy.deepcopy(L)
            lay["headers"][h] = bytes(mb).hex()
            out.append(M("op1x", "headers", f"header {h} byte {i} bit {bit}", container(lay), member=f"headers.{h}",
                         offset=i, bit=bit))
    for name in ("issuer_record.observed_anchor_delay_s", "issuer_record.policy_version", "git.object_format"):
        path = tuple(name.split("."))
        try:
            s = get_path(L, path)
        except (KeyError, TypeError):
            continue
        for i in range(len(s)):
            bit = rng.randrange(7)
            ch = chr(ord(s[i]) ^ (1 << bit))
            lay = copy.deepcopy(L)
            set_path(lay, path, s[:i] + ch + s[i + 1:])
            out.append(M("op1x", name, f"{name} char {i} bit {bit} ({s[i]!r}->{ch!r})", container(lay), member=name,
                         offset=i, bit=bit))
    return out


# ----------------------------------------------------------------------------------------------- op2
SWAP = [("a_sig",), ("manifest",), ("possession",), ("possession", "kms"), ("possession", "gpg"), ("keys",),
        ("keys", "kms"), ("keys", "gpg"), ("receipt_anchor",), ("receipt_anchor", "ots"), ("receipt_anchor", "txid"),
        ("headers",), ("dns",), ("dns", "ots"), ("dns", "snapshot_body"), ("git",), ("git", "blob"),
        ("git", "commit"), ("git", "ots"), ("git", "trees"), ("git", "trees", "0"), ("git", "trees", "1"),
        ("issuer_record",), ("spec",), ("vectors",), ("preamble",), ("dependency_manifest",)]
KEYSET = (("a_sig",), ("manifest",), ("keys",), ("possession",))
OP2_FOREIGN_CAP = 12


def _distinct(donors, path):
    seen = {}
    for d in donors:
        lay = load(d)["layer"]
        if lay is None:
            continue
        try:
            v = get_path(lay, path)
        except (KeyError, IndexError, TypeError, ValueError):
            continue
        k = json.dumps(v, sort_keys=True)
        seen.setdefault(k, (d, v))
    return [seen[k] for k in sorted(seen)]


def _keyfp(lay):
    try:
        return json.dumps(lay["keys"], sort_keys=True)
    except Exception:
        return None


def op2(seed):
    """(2a) every member, every distinct value held by another VALID seed; (2b) key-bearing members from bundle
    cases whose keys differ from the seed's (any expected verdict), capped per member; (2c) the whole key set
    (a_sig, manifest, keys, possession) from each distinct foreign-key case."""
    L = load(seed)["layer"]
    seeds = [s for s in seed_ids() if s != seed]
    out = []
    for path in SWAP:
        try:
            mine = json.dumps(get_path(L, path), sort_keys=True)
        except (KeyError, IndexError):
            mine = None
        for d, v in _distinct(seeds, path):
            if json.dumps(v, sort_keys=True) == mine:
                continue
            lay = copy.deepcopy(L)
            set_path(lay, path, copy.deepcopy(v))
            out.append(M("op2", "2a:" + pstr(path), f"{pstr(path)} from seed {d}", container(lay), member=pstr(path),
                         donor=d))
    rng = random.Random(f"op2|{seed}")
    foreign = [c for c in all_bundle_ids() if c != seed and load(c)["layer"] is not None
               and isinstance(load(c)["layer"].get("keys"), dict) and _keyfp(load(c)["layer"]) != _keyfp(L)]
    for path in KEYSET + (("possession", "kms"), ("possession", "gpg"), ("keys", "kms"), ("keys", "gpg")):
        mine = json.dumps(get_path(L, path), sort_keys=True)
        cands = [(d, v) for d, v in _distinct(foreign, path) if json.dumps(v, sort_keys=True) != mine]
        if len(cands) > OP2_FOREIGN_CAP:
            cands = rng.sample(cands, OP2_FOREIGN_CAP)
        for d, v in cands:
            lay = copy.deepcopy(L)
            set_path(lay, path, copy.deepcopy(v))
            out.append(M("op2", "2b:" + pstr(path), f"{pstr(path)} from foreign-key case {d}", container(lay),
                         member=pstr(path), donor=d))
    groups = {}
    for d in foreign:
        fl = load(d)["layer"]
        try:
            k = json.dumps([get_path(fl, p) for p in KEYSET], sort_keys=True)
        except Exception:
            continue
        groups.setdefault(_keyfp(fl), []).append((k, d))
    for kf in sorted(groups):
        k, d = sorted(groups[kf])[0]
        fl = load(d)["layer"]
        lay = copy.deepcopy(L)
        for p in KEYSET:
            set_path(lay, p, copy.deepcopy(get_path(fl, p)))
        out.append(M("op2", "2c:keyset", f"a_sig+manifest+keys+possession from foreign-key case {d}", container(lay),
                     member="keyset", donor=d))
    return out


# ----------------------------------------------------------------------------------------------- op3
def _merge_headers(target, donor, donor_wins=True):
    h = dict(target)
    for k, v in donor.items():
        if donor_wins or k not in h:
            h[k] = v
    return dict(sorted(h.items(), key=lambda kv: int(kv[0])))


def op3(seed):
    """Evidence transplants from every other VALID seed whose evidence differs: (3a) DNS snapshot+proof, (3b) git
    assertion, (3c) receipt OTS proof (keeping the target txid, and with the donor txid), (3d) header pool, (3e) the
    donor's whole receipt (a_sig + receipt_anchor) onto the target's authority evidence. Variants 'H' also bring
    the donor's headers (donor wins at shared heights); 'h' keep only the target's headers; 'u' add only the donor
    heights the target lacks."""
    L = load(seed)["layer"]
    out = []
    seen = set()
    for d in [s for s in seed_ids() if s != seed]:
        D = load(d)["layer"]
        specs = []
        if D["dns"] != L["dns"]:
            specs.append(("3a:dns", [("dns",)]))
        if D["git"] != L["git"]:
            specs.append(("3b:git", [("git",)]))
        if D["receipt_anchor"]["ots"] != L["receipt_anchor"]["ots"]:
            specs.append(("3c:receipt_ots", [("receipt_anchor", "ots")]))
            specs.append(("3c:receipt_ots+txid", [("receipt_anchor",)]))
        if D["a_sig"] != L["a_sig"] or D["receipt_anchor"] != L["receipt_anchor"]:
            specs.append(("3e:receipt", [("a_sig",), ("receipt_anchor",)]))
        for sub, paths in specs:
            for hv in ("H", "h", "u"):
                lay = copy.deepcopy(L)
                for p in paths:
                    set_path(lay, p, copy.deepcopy(get_path(D, p)))
                if hv == "H":
                    lay["headers"] = _merge_headers(L["headers"], D["headers"], True)
                elif hv == "u":
                    lay["headers"] = _merge_headers(L["headers"], D["headers"], False)
                b = container(lay)
                if b in seen:
                    continue
                seen.add(b)
                out.append(M("op3", f"{sub}/{hv}", f"{sub} from {d}, headers {hv}", b, member=sub, donor=d,
                             headers=hv))
        if D["headers"] != L["headers"]:
            for hv, hdr in (("replace-shared", {k: D["headers"].get(k, v) for k, v in L["headers"].items()}),
                            ("union-target-wins", _merge_headers(L["headers"], D["headers"], False)),
                            ("union-donor-wins", _merge_headers(L["headers"], D["headers"], True))):
                lay = copy.deepcopy(L)
                lay["headers"] = dict(sorted(hdr.items(), key=lambda kv: int(kv[0])))
                b = container(lay)
                if b in seen or lay["headers"] == L["headers"]:
                    continue
                seen.add(b)
                out.append(M("op3", f"3d:headers/{hv}", f"headers from {d} ({hv})", b, member="headers", donor=d,
                             headers=hv))
    return out


# ----------------------------------------------------------------------------------------------- op4
def ser(v, order=None, ws=False, esc=None):
    """Serializer allowing non-canonical choices: order(path, keys)->keys, ws inserts a space after ':' and ','."""
    def go(o, path):
        if isinstance(o, dict):
            ks = sorted(o)
            if order:
                ks = order(path, ks)
            sep = ", " if ws else ","
            col = ": " if ws else ":"
            return "{" + sep.join(json.dumps(k) + col + go(o[k], path + (k,)) for k in ks) + "}"
        if isinstance(o, list):
            return "[" + (", " if ws else ",").join(go(x, path + (str(i),)) for i, x in enumerate(o)) + "]"
        if isinstance(o, str):
            s = json.dumps(o, ensure_ascii=False)
            return esc(path, s) if esc else s
        return json.dumps(o)
    return go(v, ())


def _canon_text(L):
    return container(L).decode()


def _value_text(v):
    return jcs(v).decode()


def _insert_dup(text, L, path):
    """Duplicate the member at path (same value) by textual insertion right after it in the canonical text."""
    parent = get_path(L, path[:-1]) if len(path) > 1 else L
    key = path[-1]
    frag = json.dumps(key) + ":" + _value_text(parent[key])
    # locate parent's object text uniquely: use the full canonical text of the parent
    ptxt = _value_text(parent)
    pi = text.index(ptxt)
    ki = ptxt.index(frag)
    newp = ptxt[:ki + len(frag)] + "," + frag + ptxt[ki + len(frag):]
    return text[:pi] + newp + text[pi + len(ptxt):]


def _ots_root(b):
    root, node, end = ots_parse(b)
    return root, b[root:end]


def op4(seed):
    L = load(seed)["layer"]
    raw = load(seed)["raw"]
    out = []
    canon = _canon_text(L)

    def add(sub, desc, b, **meta):
        out.append(M("op4", sub, desc, b if isinstance(b, bytes) else b.encode(), **meta))

    # drop every member (objects and leaves; array elements)
    for path, _ in list(objects(L))[1:] + [(p, None) for p, _ in leaves(L)]:
        lay = copy.deepcopy(L)
        del_path(lay, path)
        add("drop", f"drop {pstr(path)}", container(lay), member=pstr(path))
    # drop each header singly (also covered above as drop headers.<h>) is included by leaves()
    # duplicate each member (JSON duplicate key, same value) at every object level
    for path, o in objects(L):
        if isinstance(o, dict):
            for k in sorted(o):
                add("dup-key", f"duplicate key {pstr(path + (k,))}", _insert_dup(canon, L, path + (k,)),
                    member=pstr(path + (k,)))
    # duplicate key with a different value (first canonical value, then donor's) for the top-level layer members
    D = load("L-29" if seed != "L-29" else "A-a")["layer"]
    for k in sorted(L):
        if k in D and D[k] != L[k]:
            frag = json.dumps(k) + ":" + _value_text(L[k])
            frag2 = json.dumps(k) + ":" + _value_text(D[k])
            add("dup-key-diff", f"duplicate key {k}, second value from donor (first wins under first-key parse)",
                canon.replace(frag, frag + "," + frag2, 1), member=k)
            add("dup-key-diff", f"duplicate key {k}, first value from donor (last wins under last-key parse)",
                canon.replace(frag, frag2 + "," + frag, 1), member=k)
    # duplicate array elements / reorder arrays
    for desc, trees in (("trees [sub, root]", [L["git"]["trees"][1], L["git"]["trees"][0]]),
                        ("trees [root, root, sub]", [L["git"]["trees"][0]] + L["git"]["trees"]),
                        ("trees [root, sub, sub]", L["git"]["trees"] + [L["git"]["trees"][1]])):
        lay = copy.deepcopy(L)
        lay["git"]["trees"] = trees
        add("array", desc, container(lay), member="git.trees")
    lay = copy.deepcopy(L)
    add("layers", "two identical layers", jcs({"layers": [L, L], "profile": "tessera-v1-strict"}), member="layers")
    add("layers", "empty layers", jcs({"layers": [], "profile": "tessera-v1-strict"}), member="layers")
    add("layers", "layer wrapped in an array", jcs({"layers": [[L]], "profile": "tessera-v1-strict"}),
        member="layers")
    # reorder members (non-canonical key order) at every object level: reversed, and first two swapped
    for path, o in objects(L):
        if isinstance(o, dict) and len(o) > 1:
            for nm, f in (("reversed", lambda ks: ks[::-1]), ("swap01", lambda ks: [ks[1], ks[0]] + ks[2:])):
                txt = ser({"layers": [L], "profile": "tessera-v1-strict"},
                          order=lambda p, ks, path=path, f=f: f(ks) if p == ("layers", "0") + path else ks)
                add("reorder", f"keys of {pstr(path) or 'layer'} {nm}", txt, member=pstr(path))
    txt = ser({"layers": [L], "profile": "tessera-v1-strict"}, order=lambda p, ks: ks[::-1] if p == () else ks)
    add("reorder", "top-level keys reversed", txt, member="top")
    # unknown members at every object level (and top level)
    for path, o in objects(L):
        if isinstance(o, dict):
            for uk, uv in (("zz_unknown", ""), ("aa_unknown", "x"), ("TEST_unknown", {"a": "b"})):
                lay = copy.deepcopy(L)
                tgt = get_path(lay, path) if path else lay
                tgt[uk] = uv
                add("unknown", f"add {uk} under {pstr(path) or 'layer'}", container(lay), member=pstr(path))
    for uk in ("zz_unknown", "aa"):
        add("unknown", f"add top-level {uk}", jcs({"layers": [L], "profile": "tessera-v1-strict", uk: ""}),
            member="top")
    # JSON re-encoding
    b = canon.encode()
    add("reencode", "trailing LF", b + b"\n")
    add("reencode", "trailing space", b + b" ")
    add("reencode", "leading space", b" " + b)
    add("reencode", "UTF-8 BOM", b"\xef\xbb\xbf" + b)
    add("reencode", "space after every ':' and ','", ser({"layers": [L], "profile": "tessera-v1-strict"}, ws=True))
    add("reencode", "pretty-printed indent=1", json.dumps({"layers": [L], "profile": "tessera-v1-strict"}, indent=1,
                                                          sort_keys=True))
    add("reencode", "CRLF + indent", json.dumps({"layers": [L], "profile": "tessera-v1-strict"}, indent=1,
                                                sort_keys=True).replace("\n", "\r\n"))
    add("reencode", "space inside layers array", canon.replace('"layers":[', '"layers":[ ', 1))
    for path, v in leaves(L):
        if not isinstance(v, str) or not v:
            continue
        full = ("layers", "0") + path
        # \/ escape (for base64 '/'), \u escape of the first character, uppercase \u hex
        if "/" in v:
            add("escape", f"'/' as \\/ in {pstr(path)}",
                ser({"layers": [L], "profile": "tessera-v1-strict"},
                    esc=lambda p, s, full=full: s.replace("/", "\\/", 1) if p == full else s), member=pstr(path))
        c0 = v[0]
        add("escape", f"first char as \\u{ord(c0):04x} in {pstr(path)}",
            ser({"layers": [L], "profile": "tessera-v1-strict"},
                esc=lambda p, s, full=full, c0=c0: '"' + "\\u%04x" % ord(c0) + s[2:] if p == full else s),
            member=pstr(path))
        if ord(c0) >= 0x0a and any(ch in "abcdef" for ch in "%04x" % ord(c0)):
            add("escape", f"first char as uppercase \\u{ord(c0):04X} in {pstr(path)}",
                ser({"layers": [L], "profile": "tessera-v1-strict"},
                    esc=lambda p, s, full=full, c0=c0: '"' + "\\u%04X" % ord(c0) + s[2:] if p == full else s),
                member=pstr(path))
    add("escape", "profile value with \\u0074 escape", canon.replace('"profile":"tessera', '"profile":"\\u0074essera'))
    add("escape", "key 'a_sig' spelled with \\u0061", canon.replace('"a_sig":', '"\\u0061_sig":', 1))
    # base64 / hex encoding variants of each binary leaf
    for path, v in leaves(L):
        if not isinstance(v, str) or path[0] in ("issuer_record",) or path == ("git", "object_format"):
            continue
        if path[0] == "headers" or path == ("receipt_anchor", "txid"):
            for nm, nv in (("uppercase hex", v.upper()), ("0x prefix", "0x" + v), ("truncated 1 nibble", v[:-1]),
                           ("extra 00", v + "00")):
                if nv != v:
                    lay = copy.deepcopy(L)
                    set_path(lay, path, nv)
                    add("encoding", f"{pstr(path)}: {nm}", container(lay), member=pstr(path))
            continue
        data = b64d(v)
        variants = [("unpadded", v.rstrip("=")), ("url-safe alphabet", v.replace("+", "-").replace("/", "_")),
                    ("line breaks every 76", "\n".join(v[i:i + 76] for i in range(0, len(v), 76))),
                    ("trailing '='", v + "="), ("raw bytes as hex", data.hex())]
        if v.endswith("="):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            st = v.rstrip("=")
            variants.append(("nonzero pad bits", st[:-1] + alphabet[alphabet.index(st[-1]) | 1] + v[len(st):]))
        for nm, nv in variants:
            if nv != v:
                lay = copy.deepcopy(L)
                set_path(lay, path, nv)
                add("encoding", f"{pstr(path)}: base64 {nm}", container(lay), member=pstr(path))
    # header-pool structure: height key forms
    h0 = sorted(L["headers"], key=int)[0]
    for nm, k in (("leading zero", "0" + h0), ("plus sign", "+" + h0), ("as JSON number", None)):
        if k is not None:
            lay = copy.deepcopy(L)
            lay["headers"][k] = lay["headers"].pop(h0)
            add("encoding", f"header height key {nm}", container(lay), member="headers")
    add("encoding", "header height key as JSON number (text)",
        canon.replace(f'"{h0}":', f'{h0}:', 1), member="headers")
    add("encoding", "issuer_record delay as JSON number (text)",
        canon.replace('"observed_anchor_delay_s":"', '"observed_anchor_delay_s":', 1).replace(
            '","policy_version"', ',"policy_version"', 1) if "issuer_record" in L else canon + " ",
        member="issuer_record")
    # OTS structural changes inside each proof: duplicate branch, sibling pending attestation, sibling Bitcoin
    # attestation at a height without a header and at the selected height; drop a sibling branch
    for name, path in (("receipt", ("receipt_anchor", "ots")), ("dns", ("dns", "ots")), ("git", ("git", "ots"))):
        data = b64d(get_path(L, path))
        try:
            root, node, end = ots_parse(data)
        except Exception:
            continue
        pre, T = data[:root], data[root:end]
        heights = sorted({lf["height"] for lf in _all_leaves(node) if lf["kind"] == "btc"})
        hmax = max([int(h) for h in L["headers"]])
        hmin = min([int(h) for h in L["headers"]])
        pend = b"\x00" + PEND_TAG + U.varbytes(U.varbytes(b"https://mutation.invalid/calendar"))

        def btc(h):
            return b"\x00" + BTC_TAG + U.varbytes(U.varuint(h))
        variants = [("duplicate whole timestamp as sibling", b"\xff" + _first_item_all(T) + T),
                    ("sibling pending attestation", b"\xff" + pend + T),
                    ("sibling Bitcoin attestation at unheadered height max+50", b"\xff" + btc(hmax + 50) + T),
                    ("sibling Bitcoin attestation at unheadered height min-50", b"\xff" + btc(hmin - 50) + T)]
        for h in heights:
            variants.append((f"sibling Bitcoin attestation at headered height {h} (digest as message)",
                             b"\xff" + btc(h) + T))
        if len(node) > 1:
            ks = list(range(len(node)))
            if len(ks) > 8:
                ks = sorted(set([0, len(ks) - 1] + random.Random(f"op4|{seed}|{name}").sample(ks, 6)))
            for k in ks:
                rest = [it for j, it in enumerate(node) if j != k]
                variants.append((f"drop root sibling {k} of {len(node)}", _ser_items(data, rest)))
        for nm, nt in variants:
            if nt is None:
                continue
            lay = copy.deepcopy(L)
            set_path(lay, path, b64e(pre + nt + data[end:]))
            add("ots", f"{name} proof: {nm}", container(lay), member=pstr(path))
        # trailing byte after the proof
        lay = copy.deepcopy(L)
        set_path(lay, path, b64e(data + b"\x00"))
        add("ots", f"{name} proof: trailing 00", container(lay), member=pstr(path))
    # drop / add headers relative to the needed set
    hs = sorted(L["headers"], key=int)
    for nm, extra in (("next height after max", str(int(hs[-1]) + 1)), ("height before min", str(int(hs[0]) - 1))):
        lay = copy.deepcopy(L)
        lay["headers"][extra] = L["headers"][hs[-1]]
        add("headers", f"add header at {nm} (copy of max header bytes)", container(lay), member="headers")
    return out


def _first_item_all(T):
    """For 'ff T T': T itself is a Timestamp; prefixing ff + (T as one item) is only well-formed if T is one item.
    If T has siblings, duplicating it means repeating all its items as siblings: ff i1 ff i2 ... T."""
    try:
        node, end = _ts(T, 0)
    except Exception:
        return T
    if len(node) == 1:
        return T
    return b"".join(T[it["s"]:it["e"]] + b"\xff" for it in node)[:-1]


def _ser_items(data, items):
    if not items:
        return None
    parts = [data[it["s"]:it["e"]] for it in items]
    return b"".join(b"\xff" + p for p in parts[:-1]) + parts[-1]


# ----------------------------------------------------------------------------------------------- op5
def _resign_receipt(L, edit_common=None, edit_manifest=None, mode="none", fresh_sig_time=None):
    """Rebuild the receipt after field edits.
    mode: 'none'   edit frames/manifest, keep every signature (and keys);
          'att'    re-sign both frames with attacker keys; keys/manifest/possession untouched;
          'att-full' attacker keys become the slot keys: new manifest (fingerprints, edits), keys, possession,
                    frames, A_sig. Evidence (DNS, git, OTS) untouched.
    """
    F_kms, S_kms, F_gpg, S_gpg = decode_asig(b64d(L["a_sig"]))
    Fm = b64d(L["manifest"])
    mv = frame_payload(Fm)
    vk, vg = frame_payload(F_kms), frame_payload(F_gpg)
    lay = copy.deepcopy(L)
    if edit_manifest:
        edit_manifest(mv)
    if mode == "att-full":
        mv["key_fp"] = ATT_KMS.fp_kms
        mv["sset"] = [ATT_GPG.fp_gpg]
    Fm2 = make_frame_like(Fm, mv) if (edit_manifest or mode == "att-full") else Fm
    for v in (vk, vg):
        if edit_common:
            edit_common(v["common"])
        if Fm2 != Fm:
            v["common"]["manifest_sha256"] = hashlib.sha256(Fm2).hexdigest()
    if mode == "att-full":
        vk["signer"]["key_fp"] = ATT_KMS.fp_kms
        vg["signer"]["key_fp"] = ATT_GPG.fp_gpg
    F_kms2, F_gpg2 = make_frame_like(F_kms, vk), make_frame_like(F_gpg, vg)
    t = fresh_sig_time or sig_created(S_kms)
    if mode in ("att", "att-full"):
        S_kms, S_gpg = tc.pgp_sign(F_kms2, ATT_KMS, t), tc.pgp_sign(F_gpg2, ATT_GPG, t)
    lay["a_sig"] = b64e(gen.encode_anchor(F_kms2, S_kms, F_gpg2, S_gpg))
    lay["manifest"] = b64e(Fm2)
    if mode == "att-full":
        lay["keys"] = {"gpg": b64e(ATT_GPG.pgp_body), "kms": b64e(ATT_KMS.spki)}
        lay["possession"] = {"gpg": b64e(tc.pgp_sign(Fm2, ATT_GPG, t)), "kms": b64e(tc.pgp_sign(Fm2, ATT_KMS, t))}
    return lay


def _shift_time(s, d):
    return U.rfc3339(U.ts(s) + d)


def _edit_window_text(value, which, delta):
    """Shift one window bound (nb or na) in a DNS/git value string by delta seconds, same encoding."""
    parts = value.split(";")
    out = []
    for p in parts:
        k, _, v = p.partition("=")
        if k == which:
            try:
                v = _shift_time(v, delta)
            except Exception:
                pass
        out.append(f"{k}={v}" if _ else p)
    return ";".join(out)


def op5(seed):
    L = load(seed)["layer"]
    F_kms = decode_asig(b64d(L["a_sig"]))[0]
    common = frame_payload(F_kms)["common"]
    out = []
    edits = [
        ("issuer", "issuer -> attacker.example", lambda c: c.__setitem__("issuer", "attacker.example"),
         lambda m: m.__setitem__("issuer", "attacker.example")),
        ("issuer", "issuer -> wamason.co", lambda c: c.__setitem__("issuer", "wamason.co"),
         lambda m: m.__setitem__("issuer", "wamason.co")),
        ("declared", "declared_issue_time +1 s", lambda c: c.__setitem__(
            "declared_issue_time", _shift_time(c["declared_issue_time"], 1)), None),
        ("declared", "declared_issue_time -1 s", lambda c: c.__setitem__(
            "declared_issue_time", _shift_time(c["declared_issue_time"], -1)), None),
        ("declared", "declared_issue_time -1 day", lambda c: c.__setitem__(
            "declared_issue_time", _shift_time(c["declared_issue_time"], -86400)), None),
        ("declared", "declared_issue_time +2 days", lambda c: c.__setitem__(
            "declared_issue_time", _shift_time(c["declared_issue_time"], 2 * 86400)), None),
        ("declared", "declared_issue_time -30 days", lambda c: c.__setitem__(
            "declared_issue_time", _shift_time(c["declared_issue_time"], -30 * 86400)), None),
        ("alg", "alg -> TEST-OTHER-ALG", lambda c: c.__setitem__("alg", "TEST-OTHER-ALG"),
         lambda m: m.__setitem__("alg", "TEST-OTHER-ALG")),
        ("alg", "alg (frames only) -> TEST-OTHER-ALG", lambda c: c.__setitem__("alg", "TEST-OTHER-ALG"), None),
        ("ver", "manifest ver -> map-v2", None, lambda m: m.__setitem__("ver", "map-v2")),
        ("ver", "manifest ver -> map-v0", None, lambda m: m.__setitem__("ver", "map-v0")),
        ("content", "content: add a field", lambda c: c.__setitem__(
            "content", {"TEST": "mutated content", "orig": c["content"]}), None),
        ("content", "content: replaced by a string", lambda c: c.__setitem__("content", "TEST mutated"), None),
        ("profile", "signed profile -> tessera-v1-other", lambda c: c.__setitem__("profile", "tessera-v1-other"), None),
        ("binding", "binding_forms -> [STMT_DIRECT, STMT_DIGEST]",
         lambda c: c.__setitem__("binding_forms", ["STMT_DIGEST", "STMT_DIRECT"]), None),
        ("spec", "spec.id -> .../2", lambda c: c["spec"].__setitem__("id", "tessera-v1-strict/verification-spec/2"),
         None),
    ]
    for kind, desc, ec, em in edits:
        for mode in ("none", "att", "att-full"):
            try:
                lay = _resign_receipt(L, ec, em, mode)
            except Exception as e:  # an edit the encoder refuses is still recorded as not generated
                print(f"op5 {seed} {desc} {mode}: not generated ({e})", file=sys.stderr)
                continue
            out.append(M("op5", f"{kind}/{mode}", f"{desc}; signatures: {mode}", container(lay), field=kind,
                         mode=mode))
    # pure re-key under attacker keys (no field edit)
    lay = _resign_receipt(L, None, None, "att-full")
    out.append(M("op5", "rekey/att-full", "no field edit; every slot key replaced by attacker TEST keys",
                 container(lay), field="rekey", mode="att-full"))
    lay = _resign_receipt(L, None, None, "att")
    out.append(M("op5", "rekey/att", "no field edit; frames re-signed by attacker keys", container(lay),
                 field="rekey", mode="att"))
    # window values in the authority evidence (git blob, DNS TXT)
    blob = b64d(L["git"]["blob"]).decode()
    body = b64d(L["dns"]["snapshot_body"])
    for which in ("nb", "na"):
        tagname = {"nb": gen.NB, "na": gen.NA}[which]
        for delta in (86400, -86400, 365 * 86400):
            nv = _edit_window_text(blob, tagname, delta)
            if nv == blob:
                continue
            desc = f"window {tagname} {'+' if delta > 0 else ''}{delta // 86400} d"
            # (a) git blob only, trees/commit rebuilt, commit re-signed by attacker repo key
            for gmode in ("blob-only", "rebuild-unsigned", "rebuild-attacker-repo"):
                lay = copy.deepcopy(L)
                g = _git_with_blob(L, nv.encode(), gmode)
                lay["git"].update(g)
                out.append(M("op5", f"window/git-{gmode}", f"{desc} in git blob ({gmode})", container(lay),
                             field="window", mode=gmode))
            # (b) DNS TXT RDATA edit in place (same length) and (c) both channels consistently
            if blob.encode() in body and len(nv) == len(blob):
                lay = copy.deepcopy(L)
                lay["dns"]["snapshot_body"] = b64e(body.replace(blob.encode(), nv.encode()))
                out.append(M("op5", "window/dns", f"{desc} in DNS TXT (in place)", container(lay), field="window",
                             mode="dns"))
                lay2 = copy.deepcopy(lay)
                lay2["git"].update(_git_with_blob(L, nv.encode(), "rebuild-attacker-repo"))
                out.append(M("op5", "window/both", f"{desc} in DNS TXT and git (attacker repo key)", container(lay2),
                             field="window", mode="both"))
    # authority key values: DNS/git value naming attacker fingerprints, receipt fully re-keyed (all consistent
    # except the anchoring and the DNSSEC/git signatures)
    nv = blob
    for k, fp in (("kms", ATT_KMS.fp_kms.split(":")[1]), ("gpg", ATT_GPG.fp_gpg.split(":")[1])):
        parts = [p if not p.startswith(k + "=") else f"{k}={fp}" for p in nv.split(";")]
        nv = ";".join(parts)
    lay = _resign_receipt(L, None, None, "att-full")
    lay["git"].update(_git_with_blob(L, nv.encode(), "rebuild-attacker-repo"))
    if blob.encode() in body and len(nv) == len(blob):
        lay["dns"]["snapshot_body"] = b64e(body.replace(blob.encode(), nv.encode()))
    out.append(M("op5", "authority/att-full", "attacker keys everywhere: receipt, manifest, keys, possession, git "
                 "blob (attacker repo key), DNS TXT value", container(lay), field="authority", mode="att-full"))
    return out


def _git_with_blob(L, blob, gmode):
    g = {"blob": b64e(blob)}
    if gmode == "blob-only":
        return g
    sub = b64d(L["git"]["trees"][1])
    ents = [(m, n, U.git_id("blob", blob) if n == "key-assertion" else o) for m, n, o in parse_tree(sub)]
    sub2 = U.tree_body(ents, sort=False)
    root = b64d(L["git"]["trees"][0])
    rents = [(m, n, U.git_id("tree", sub2) if n == "tessera-v1" else o) for m, n, o in parse_tree(root)]
    root2 = U.tree_body(rents, sort=False)
    commit = b64d(L["git"]["commit"])
    tid = U.git_id("tree", root2).hex()
    if gmode == "rebuild-unsigned":
        c2, _ = rebuild_commit(commit, tree_id=tid)
    else:
        _, payload = rebuild_commit(commit, tree_id=tid)
        _, arm = split_commit(commit)
        old = dearmor(arm)[0]
        sig = tc.pgp_sign(payload, ATT_REPO, sig_created(old))
        c2, _ = rebuild_commit(commit, new_sig=sig, tree_id=tid)
    g["trees"] = [b64e(root2), b64e(sub2)]
    g["commit"] = b64e(c2)
    return g


# ----------------------------------------------------------------------------------------------- driver
# ----------------------------------------------------------------------------------------------- op6
def _sig_body(sig):
    hl = 3 if sig[0] == 0x89 else 2
    return sig[hl:]


def _sig_edit(sig, unhashed=None, s_neg=False):
    """Rebuild a v4 signature packet with a replaced unhashed area and/or s -> n - s (legacy header recomputed)."""
    body = _sig_body(sig)
    hlen = struct.unpack(">H", body[4:6])[0]
    i = 6 + hlen
    ulen = struct.unpack(">H", body[i:i + 2])[0]
    head, old_un, rest = body[:i], body[i + 2:i + 2 + ulen], body[i + 2 + ulen:]
    un = old_un if unhashed is None else unhashed
    left16, j = rest[:2], 2
    rl = struct.unpack(">H", rest[j:j + 2])[0]
    r_mpi = rest[j:j + 2 + (rl + 7) // 8]
    j += len(r_mpi)
    sl = struct.unpack(">H", rest[j:j + 2])[0]
    s = int.from_bytes(rest[j + 2:j + 2 + (sl + 7) // 8], "big")
    tail = rest[j + 2 + (sl + 7) // 8:]
    if s_neg:
        s = tc.N - s
    nb = head + struct.pack(">H", len(un)) + un + left16 + r_mpi + tc.mpi(s) + tail
    return tc.packet(nb, "legacy")


def _unhashed_variants(sig):
    body = _sig_body(sig)
    hlen = struct.unpack(">H", body[4:6])[0]
    i = 6 + hlen
    ulen = struct.unpack(">H", body[i:i + 2])[0]
    old = body[i + 2:i + 2 + ulen]
    return [("s -> n - s (high/low-s malleation)", _sig_edit(sig, s_neg=True)),
            ("unhashed area emptied", _sig_edit(sig, unhashed=b"")),
            ("unhashed type-16 issuer key id -> attacker key id",
             _sig_edit(sig, unhashed=tc.subpacket(16, ATT_GPG.v4_fpr_sha1[-8:]))),
            ("unhashed: add unknown critical subpacket type 100",
             _sig_edit(sig, unhashed=old + tc.subpacket(100, b"TEST", critical=True))),
            ("unhashed: add 1000-octet notation-like subpacket type 20",
             _sig_edit(sig, unhashed=old + tc.subpacket(20, b"\x80\x00\x00\x00" + b"\x00\x04\x03\xe0" + b"TEST" +
                                                         b"X" * 992))),
            ("unhashed: add hashed-style signature-expiration subpacket (type 3) in unhashed area",
             _sig_edit(sig, unhashed=old + tc.subpacket(3, struct.pack(">I", 1))))]


def op6(seed):
    """Targeted malleation of bytes the profile leaves uncovered inside signatures: ECDSA s -> n - s (low-s not
    required, P§8) and unhashed-area rewrites (P§8: ignored entirely), applied to each possession signature, each
    receipt signature inside A_sig, and the git commit signature; plus possession slot swap."""
    L = load(seed)["layer"]
    out = []
    for slot in ("kms", "gpg"):
        sig = b64d(L["possession"][slot])
        for nm, s2 in _unhashed_variants(sig):
            lay = copy.deepcopy(L)
            lay["possession"][slot] = b64e(s2)
            out.append(M("op6", f"possession.{slot}", f"possession.{slot}: {nm}", container(lay),
                         member=f"possession.{slot}", variant=nm))
    lay = copy.deepcopy(L)
    lay["possession"] = {"gpg": L["possession"]["kms"], "kms": L["possession"]["gpg"]}
    out.append(M("op6", "possession.swap", "possession kms <-> gpg swapped", container(lay), member="possession",
                 variant="swap"))
    F0, S0, F1, S1 = decode_asig(b64d(L["a_sig"]))
    for slot in ("kms", "gpg"):
        for nm, s2 in _unhashed_variants(S0 if slot == "kms" else S1):
            parts = (F0, s2, F1, S1) if slot == "kms" else (F0, S0, F1, s2)
            lay = copy.deepcopy(L)
            lay["a_sig"] = b64e(gen.encode_anchor(*parts))
            out.append(M("op6", f"a_sig.S_{slot}", f"receipt signature S_{slot}: {nm}", container(lay),
                         member=f"a_sig.S_{slot}", variant=nm))
    commit = b64d(L["git"]["commit"])
    sig, _ = dearmor(split_commit(commit)[1])
    for nm, s2 in _unhashed_variants(sig):
        lay = copy.deepcopy(L)
        lay["git"]["commit"] = b64e(rebuild_commit(commit, new_sig=s2)[0])
        out.append(M("op6", "git_sig", f"git commit signature: {nm}", container(lay), member="git_sig", variant=nm))
    return out


GEN = {"op1": op1, "op1x": op1x, "op2": op2, "op3": op3, "op4": op4, "op5": op5, "op6": op6}


def mutants(op, seed):
    return GEN[op](seed)


def by_id(mid):
    op, seed, n = mid.split("/")
    return mutants(op, seed)[int(n)]


def command(seed, bundle_path):
    c = "prototype/conformance/cases/" + seed
    return (f"TESSERA_V1_TEST_RELEASE={c}/release.json "
            f"TESSERA_V1_TEST_RELEASE_KEY=prototype/conformance/universe-release-key.json "
            f"TESSERA_V1_TEST_CATALOG=prototype/conformance/universe-catalog.json "
            f"prototype/indep-verifier/.venv/bin/python prototype/differential/adapter.py "
            f"--trust {c}/trust.json --bundle {bundle_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--emit")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.emit:
        m = by_id(a.emit)
        Path(a.out).write_bytes(m.bundle)
        print(json.dumps({"id": a.emit, "op": m.op, "sub": m.sub, "desc": m.desc, "meta": m.meta}, sort_keys=True))
        print("cd " + str(REPO) + " && " + command(a.emit.split("/")[1], a.out))
        return
    if a.count:
        tot = {}
        for op in OPS:
            for s in seed_ids():
                n = len(mutants(op, s))
                tot[op] = tot.get(op, 0) + n
                if a.verbose:
                    print(op, s, n)
        print(json.dumps(tot, sort_keys=True), sum(tot.values()))


if __name__ == "__main__":
    main()
