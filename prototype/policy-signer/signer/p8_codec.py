# VENDORED from formal/p8/vectors/gen.py (P8 implementation A, Tessera project; author Tony Mason and the
# Tessera owner instance). Copied VERBATIM, no edits, for the slot-2 policy signer (prototype/policy-signer/,
# instrument code under A9.2; never ships). Only the import block is written here; every other line is a
# byte-for-byte copy of the named gen.py line ranges.
#   source:  formal/p8/vectors/gen.py, sha256 cd86740e8e4abba63b7c715e6f8b41ec9faf7d66e0a09815eb095beeb1455ccc
#            (vendored 2026-10-14; formal/p8/ was untracked in git at that time)
#   ranges:  41-477   Unicode pin, constants, JSON domain, RFC 8785 form, field grammars, frame decode,
#                     rule-O signature-packet decode (decode_sig_openpgp4, decode_sig)
#            620-658  key fingerprints (_point, spki_der, openpgp_v4_body, fp_gpg)
#            732-751  OpenPGP v4 packet encode (_subpacket, _mpi_enc, openpgp_v4_sig_digest, openpgp_v4_sig_packet)
# Re-check:  prototype/policy-signer/deploy.sh vendor-check compares these ranges with gen.py.
import datetime
import decimal
import hashlib
import json
import re
import struct
import sys
import unicodedata

import rfc8785

# ---- gen.py 41-477 ----
UNICODE_VERSION = "16.0.0"
if unicodedata.unidata_version != UNICODE_VERSION:
    sys.exit(f"Unicode tables are {unicodedata.unidata_version}; tessera-v1-strict pins {UNICODE_VERSION}")

# --------------------------------------------------------------------------------------------------
# Constants (ENCODING-V1.md §2, §3)
# --------------------------------------------------------------------------------------------------
CV = 1
MAX_PAYLOAD = 1 << 24
MAX_DEPTH_PAYLOAD = 64
MAX_DEPTH_CONTENT = 62
PROFILE = "tessera-v1-strict"
T_ATTEST = b"tessera-v1/attest"
T_MANIFEST = b"tessera-v1/manifest"
T_ANCHOR = b"tessera-v1/receipt-anchor-sig"       # ENCODING-V1 §5, revision 2026-10-12
T_ANCHOR_FRAMES_ONLY = b"tessera-v1/receipt-anchor"  # withdrawn frame-only layout: NOT in T, vectors only
T_SNAPSHOT = b"tessera-v1/dnssec-snapshot"
ALL_TAGS = (T_ATTEST, T_MANIFEST, T_ANCHOR, T_SNAPSHOT)

# Signature-slot rules (ENCODING-V1 §5.2). A rule is chosen by the frame's common.alg and the slot.
ALG_V1 = "OPENPGP4-ECDSA-P256-SHA256"
# Hybrid pair id (formal/p8/HYBRID-SUPPLEMENT-DRAFT.md, OWNER-PROPOSED): slot kms rule R, raw pure ML-DSA-65
# with an empty context; slot gpg rule O. Codec-known only under the branch-registration supplement.
ALG_HYBRID = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256"
SIG_CAP_OPENPGP4 = 1024          # whole packet, header included
SIG_CAP_OPAQUE = 1 << 16         # a well-formed alg id this profile does not register (stage (c) decides)
SIG_LEN_MLDSA65 = 3309           # rule R: exactly the FIPS 204 ML-DSA-65 signature size; also its cap
SIG_RULES = {ALG_V1: ("openpgp4-ecdsa-p256-sha256", "openpgp4-ecdsa-p256-sha256"),   # (kms, gpg)
             ALG_HYBRID: ("raw-mldsa65-pure", "openpgp4-ecdsa-p256-sha256")}

decimal.getcontext().prec = 1000


class Reject(Exception):
    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}")
        self.code = code


# --------------------------------------------------------------------------------------------------
# JSON domain and canonical form (ENCODING-V1.md §1)
# --------------------------------------------------------------------------------------------------
class _Num:
    __slots__ = ("lit",)

    def __init__(self, lit):
        self.lit = lit


def _reject_constant(name):
    raise Reject("JSON_SYNTAX", f"non-JSON constant {name}")


def _parse_tree(data):
    """Bytes -> tree of dict-as-pairs-list / list / str / _Num / bool / None. Syntax only."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise Reject("JSON_SYNTAX", "byte-order mark")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise Reject("JSON_ENCODING", str(e))
    try:
        return json.loads(
            text,
            object_pairs_hook=lambda pairs: ("obj", pairs),
            parse_float=_Num,
            parse_int=_Num,
            parse_constant=_reject_constant,
        )
    except RecursionError:
        raise Reject("JSON_DEPTH", "parser recursion limit")
    except json.JSONDecodeError as e:
        raise Reject("JSON_SYNTAX", str(e))


def _walk(t):
    yield t
    if isinstance(t, tuple):
        for k, v in t[1]:
            yield k
            yield from _walk(v)
    elif isinstance(t, list):
        for v in t:
            yield from _walk(v)


def _depth(t):
    if isinstance(t, tuple):
        return 1 + max((_depth(v) for _, v in t[1]), default=0)
    if isinstance(t, list):
        return 1 + max((_depth(v) for v in t), default=0)
    return 0


def check_string(s):
    for ch in s:
        cp = ord(ch)
        if 0xD800 <= cp <= 0xDFFF:
            raise Reject("JSON_STRING", f"surrogate U+{cp:04X}")
        if 0xFDD0 <= cp <= 0xFDEF or (cp & 0xFFFE) == 0xFFFE:
            raise Reject("JSON_STRING", f"noncharacter U+{cp:04X}")
        if unicodedata.category(ch) == "Cn":
            raise Reject("JSON_STRING", f"unassigned U+{cp:04X}")
    if not unicodedata.is_normalized("NFC", s):
        raise Reject("JSON_STRING", "not NFC")


def number_value(lit):
    """The value-preserving rule: accept iff the literal's exact decimal value equals the exact
    decimal value of RFC 8785's serialization of the nearest double, and the literal is not a
    negative zero. Returns the double."""
    mant, _, exp = lit.lower().partition("e")
    if exp and abs(int(exp)) > 100000:          # Decimal cannot hold the exponent; decide directly
        if mant.strip("-0.") == "":
            if lit.startswith("-"):
                raise Reject("JSON_NUMBER", "negative zero")
            return 0.0
        raise Reject("JSON_NUMBER", "outside the binary64 range")
    exact = decimal.Decimal(lit)
    if exact == 0 and lit.startswith("-"):
        raise Reject("JSON_NUMBER", "negative zero")
    f = float(lit)
    if f in (float("inf"), float("-inf")):
        raise Reject("JSON_NUMBER", "outside the binary64 range")
    if decimal.Decimal(rfc8785.dumps(f).decode("ascii")) != exact:
        raise Reject("JSON_NUMBER", f"value of {lit} not preserved by RFC 8785")
    return f


def _to_value(t):
    if isinstance(t, tuple):
        return {k: _to_value(v) for k, v in t[1]}
    if isinstance(t, list):
        return [_to_value(v) for v in t]
    if isinstance(t, _Num):
        return number_value(t.lit)
    return t


def ingest(data, max_depth=MAX_DEPTH_CONTENT):
    """Requester JSON text -> value in the accepted domain V. Spelling is normalized; values are not."""
    tree = _parse_tree(data)
    # Category precedence (ENCODING-V1.md §1.4): depth, duplicate names, strings, numbers.
    if _depth(tree) > max_depth:
        raise Reject("JSON_DEPTH", "nesting too deep")
    for node in _walk(tree):
        if isinstance(node, tuple):
            names = [k for k, _ in node[1]]
            if len(set(names)) != len(names):
                raise Reject("JSON_DUPLICATE_NAME", "duplicate member name")
    for node in _walk(tree):
        if isinstance(node, str):
            check_string(node)
    for node in _walk(tree):
        if isinstance(node, _Num):
            number_value(node.lit)
    return _to_value(tree)


def jcs(value):
    return rfc8785.dumps(value)


def decode_payload(data):
    """In-frame payload bytes -> value. Exactly canonical, nothing normalized."""
    v = ingest(data, max_depth=MAX_DEPTH_PAYLOAD)
    if jcs(v) != data:
        raise Reject("JSON_NONCANONICAL", "payload is not its own RFC 8785 serialization")
    return v


# --------------------------------------------------------------------------------------------------
# Field grammars (ENCODING-V1.md §4)
# --------------------------------------------------------------------------------------------------
RE_ALG = re.compile(r"[A-Z0-9][A-Z0-9-]{0,63}")
RE_FORM = re.compile(r"[A-Z][A-Z0-9_]{0,31}")
RE_HEX64 = re.compile(r"[0-9a-f]{64}")
RE_TIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z")
RE_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
RE_LABEL = re.compile(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?")
RE_SPECID = re.compile(r"[a-z0-9][a-z0-9._/-]{0,127}")
RE_FP_KMS = re.compile(r"spki-sha256:[0-9a-f]{64}")
RE_FP_GPG = re.compile(r"gpg-sha256:[0-9a-f]{64}")


def _full(rx, s):
    return isinstance(s, str) and rx.fullmatch(s) is not None


def valid_time(s):
    m = _full(RE_TIME, s) and RE_TIME.fullmatch(s)
    if not m:
        return False
    y, mo, d, h, mi, se = map(int, m.groups())
    try:
        datetime.datetime(y, mo, d, h, mi, se)
    except ValueError:
        return False
    return True


def valid_date(s):
    m = _full(RE_DATE, s) and RE_DATE.fullmatch(s)
    if not m:
        return False
    try:
        datetime.date(*map(int, m.groups()))
    except ValueError:
        return False
    return True


def valid_domain(s):
    if not isinstance(s, str) or not (1 <= len(s) <= 241):
        return False
    labels = s.split(".")
    return len(labels) >= 2 and all(RE_LABEL.fullmatch(lb) for lb in labels)


def _keys(obj, keys):
    return isinstance(obj, dict) and set(obj) == set(keys)


COMMON_KEYS = ("alg", "binding_forms", "content", "declared_issue_time", "issuer", "manifest_sha256",
               "preamble_sha256", "profile", "spec", "vectors_sha256")


def check_attest_schema(v):
    ok = (
        _keys(v, ("common", "signer"))
        and _keys(v["common"], COMMON_KEYS)
        and _keys(v["signer"], ("key_fp",))
    )
    if ok:
        c = v["common"]
        bf = c["binding_forms"]
        ok = (
            _full(RE_ALG, c["alg"])
            and isinstance(bf, list) and len(bf) >= 1
            and all(_full(RE_FORM, f) for f in bf)
            and all(bf[i] < bf[i + 1] for i in range(len(bf) - 1))
            and valid_time(c["declared_issue_time"])
            and valid_domain(c["issuer"])
            and all(_full(RE_HEX64, c[k]) for k in ("manifest_sha256", "preamble_sha256", "vectors_sha256"))
            and c["profile"] == PROFILE
            and _keys(c["spec"], ("id", "sha256"))
            and _full(RE_SPECID, c["spec"]["id"]) and _full(RE_HEX64, c["spec"]["sha256"])
            and (_full(RE_FP_KMS, v["signer"]["key_fp"]) or _full(RE_FP_GPG, v["signer"]["key_fp"]))
        )
    if not ok:
        raise Reject("SCHEMA", "attestation payload schema")


def check_manifest_schema(v):
    ok = (
        _keys(v, ("alg", "issuer", "key_fp", "sset", "ver"))
        and _full(RE_ALG, v["alg"]) and valid_domain(v["issuer"])
        and _full(RE_FP_KMS, v["key_fp"])
        and isinstance(v["sset"], list) and len(v["sset"]) == 1 and _full(RE_FP_GPG, v["sset"][0])
        and v["ver"] == "map-v1"
    )
    if not ok:
        raise Reject("SCHEMA", "manifest payload schema")


# --------------------------------------------------------------------------------------------------
# Byte layouts (ENCODING-V1.md §2, §3, §5, §6)
# --------------------------------------------------------------------------------------------------
def header(tag):
    return bytes([len(tag)]) + tag


def frame(tag, payload, cv=CV):
    assert len(payload) <= MAX_PAYLOAD
    return header(tag) + struct.pack(">HI", cv, len(payload)) + payload


def encode_attest(common, key_fp):
    v = {"common": common, "signer": {"key_fp": key_fp}}
    check_attest_schema(v)
    return frame(T_ATTEST, jcs(v))


def encode_manifest(alg, issuer, kms_fp, gpg_fp):
    v = {"alg": alg, "issuer": issuer, "key_fp": kms_fp, "sset": [gpg_fp], "ver": "map-v1"}
    check_manifest_schema(v)
    return frame(T_MANIFEST, jcs(v))


def encode_anchor(f0, s0, f1, s1):
    """A_sig: header || 0x02 || per slot, in manifest order: u32 len(F) || F || u32 len(S) || S."""
    out = header(T_ANCHOR) + bytes([2])
    for part in (f0, s0, f1, s1):
        out += struct.pack(">I", len(part)) + part
    return out


def encode_anchor_frames_only(f0, f1, tag=T_ANCHOR_FRAMES_ONLY):
    """The withdrawn 2026-10-09 layout. Used only to build rejection vectors."""
    return header(tag) + bytes([2]) + struct.pack(">I", len(f0)) + f0 + struct.pack(">I", len(f1)) + f1


def encode_snapshot(snap):
    assert 1 <= len(snap) <= MAX_PAYLOAD
    return header(T_SNAPSHOT) + struct.pack(">I", len(snap)) + snap


class _Reader:
    def __init__(self, b):
        self.b, self.i = b, 0

    def take(self, n):
        if len(self.b) - self.i < n:
            raise Reject("TRUNCATED", f"need {n} bytes at offset {self.i}")
        out = self.b[self.i:self.i + n]
        self.i += n
        return out

    def rest(self):
        return len(self.b) - self.i


def _read_header(r, expected):
    n = r.take(1)[0]
    tag = r.take(n)
    if tag not in ALL_TAGS:
        raise Reject("TAG_UNKNOWN", repr(tag))
    if tag != expected:
        raise Reject("TAG_MISMATCH", f"{tag!r} where {expected!r} expected")


def decode_frame(b, expected):
    r = _Reader(b)
    _read_header(r, expected)
    cv = int.from_bytes(r.take(2), "big")
    if cv != CV:
        raise Reject("CV_UNKNOWN", str(cv))
    n = int.from_bytes(r.take(4), "big")
    if n > MAX_PAYLOAD:
        raise Reject("LENGTH_CAP", str(n))
    if r.rest() < n:
        raise Reject("TRUNCATED", "payload shorter than its length prefix")
    if r.rest() > n:
        raise Reject("TRAILING", "bytes after the payload")
    v = decode_payload(r.take(n))
    (check_attest_schema if expected == T_ATTEST else check_manifest_schema)(v)
    return v


def _subpacket_area(a):
    """RFC 9580 §5.2.3.7 subpacket lengths, shortest form only, each subpacket nonempty, exact fill."""
    i = 0
    while i < len(a):
        o = a[i]
        if o < 192:
            n, i = o, i + 1
        elif o < 255:
            if i + 2 > len(a):
                raise Reject("SIG_FORMAT", "subpacket length runs past its area")
            n, i = ((o - 192) << 8) + a[i + 1] + 192, i + 2
        else:
            if i + 5 > len(a):
                raise Reject("SIG_FORMAT", "subpacket length runs past its area")
            n, i = int.from_bytes(a[i + 1:i + 5], "big"), i + 5
            if n < 16320:
                raise Reject("SIG_FORMAT", "five-octet subpacket length where a shorter form fits")
        if n == 0 or i + n > len(a):
            raise Reject("SIG_FORMAT", "empty subpacket or subpacket past its area")
        i += n


def _mpi(r):
    bits = int.from_bytes(r.take(2), "big")
    if not 1 <= bits <= 256:
        raise Reject("SIG_FORMAT", f"MPI of {bits} bits")
    v = r.take((bits + 7) // 8)
    if v[0].bit_length() != bits - 8 * (len(v) - 1):
        raise Reject("SIG_FORMAT", "MPI bit count is not exact")
    return int.from_bytes(v, "big")


def decode_sig_openpgp4(s):
    """One v4 OpenPGP signature packet, binary, legacy-format header in its shortest form (ENCODING-V1 §5.2).
    Returns (hashed_area, r, s)."""
    r = _Reader(s)
    ctb = r.take(1)[0]
    if ctb == 0x88:
        n = r.take(1)[0]
    elif ctb == 0x89:
        n = int.from_bytes(r.take(2), "big")
        if n < 256:
            raise Reject("SIG_PACKET", "two-octet length where one octet fits")
    else:
        raise Reject("SIG_PACKET", f"packet header {ctb:#04x} is not a legacy-format signature packet")
    if r.rest() < n:
        raise Reject("TRUNCATED", "signature packet shorter than its length")
    if r.rest() > n:
        raise Reject("TRAILING", "bytes after the signature packet")
    body = _Reader(r.take(n))
    try:
        ver, typ, pub, hal = body.take(4)
        if (ver, typ, pub, hal) != (4, 0x00, 19, 8):
            raise Reject("SIG_FORMAT", f"version {ver} type {typ:#04x} pubalg {pub} hashalg {hal}")
        hashed = body.take(int.from_bytes(body.take(2), "big"))
        _subpacket_area(hashed)
        _subpacket_area(body.take(int.from_bytes(body.take(2), "big")))
        body.take(2)                                     # left 16 bits of the digest: not signed
        rr, ss = _mpi(body), _mpi(body)
    except Reject as e:
        if e.code == "TRUNCATED":
            raise Reject("SIG_FORMAT", "signature body ends early")
        raise
    if body.rest():
        raise Reject("SIG_FORMAT", "bytes after the second MPI inside the packet body")
    return hashed, rr, ss


def sig_rule(alg, slot):
    return SIG_RULES[alg][slot] if alg in SIG_RULES else "opaque"


def sig_cap(alg, slot):
    return {"openpgp4-ecdsa-p256-sha256": SIG_CAP_OPENPGP4,
            "raw-mldsa65-pure": SIG_LEN_MLDSA65}.get(sig_rule(alg, slot), SIG_CAP_OPAQUE)


def decode_sig(s, alg, slot):
    rule, cap = sig_rule(alg, slot), sig_cap(alg, slot)
    if not s:
        raise Reject("SIG_EMPTY", "empty signature")
    if len(s) > cap:
        raise Reject("LENGTH_CAP", f"signature of {len(s)} bytes; cap {cap}")
    if rule == "openpgp4-ecdsa-p256-sha256":
        decode_sig_openpgp4(s)
    elif rule == "raw-mldsa65-pure" and len(s) != SIG_LEN_MLDSA65:
        raise Reject("SIG_FORMAT", f"rule R: {len(s)} bytes where ML-DSA-65 signatures are exactly {SIG_LEN_MLDSA65}")
    return s

# ---- gen.py 620-658 ----
# --------------------------------------------------------------------------------------------------
# Key fingerprints (ENCODING-V1.md §4.3)
# --------------------------------------------------------------------------------------------------
P = 2**256 - 2**224 + 2**192 + 2**96 - 1
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5


def _double(x, y):
    lam = (3 * x * x - 3) * pow(2 * y, -1, P) % P
    x3 = (lam * lam - 2 * x) % P
    return x3, (lam * (x - x3) - y) % P


def _point(x, y):
    assert (y * y - (x ** 3 - 3 * x + B)) % P == 0
    return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")


SPKI_P256_PREFIX = bytes.fromhex("3059301306072a8648ce3d020106082a8648ce3d030107034200")


def spki_der(pt):
    return SPKI_P256_PREFIX + pt


def openpgp_v4_body(pt, created):
    oid = bytes.fromhex("2a8648ce3d030107")
    return bytes([4]) + struct.pack(">I", created) + bytes([19, len(oid)]) + oid + struct.pack(">H", 515) + pt


def fp_kms(pt):
    return "spki-sha256:" + hashlib.sha256(spki_der(pt)).hexdigest()


def fp_gpg(pt, created):
    body = openpgp_v4_body(pt, created)
    return "gpg-sha256:" + hashlib.sha256(body).hexdigest()     # the body only: no 0x99 / length prefix

# ---- gen.py 732-751 ----
def _subpacket(typ, data):
    assert len(data) + 1 < 192
    return bytes([len(data) + 1, typ]) + data


def _mpi_enc(v):
    return struct.pack(">H", v.bit_length()) + v.to_bytes((v.bit_length() + 7) // 8, "big")


def openpgp_v4_sig_digest(frame_bytes, hashed):
    head = bytes([4, 0x00, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
    return hashlib.sha256(frame_bytes + head + b"\x04\xff" + struct.pack(">I", len(head))).digest()


def openpgp_v4_sig_packet(hashed, unhashed, left16, r, s):
    body = (bytes([4, 0x00, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
            + struct.pack(">H", len(unhashed)) + unhashed + left16 + _mpi_enc(r) + _mpi_enc(s))
    assert len(body) <= 255
    return bytes([0x88, len(body)]) + body

