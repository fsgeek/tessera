#!/usr/bin/env python3
"""P8 second decoder for profile tessera-v1-strict (implementation B).

Written separately from gen.py and shares no code with it or with prototype/. It uses only the Python
standard library. It does NOT use the json module or the rfc8785 package for anything under test: it
has its own UTF-8 decoder, JSON parser, number rule, ECMAScript number formatter, RFC 8785 serializer,
frame, anchor, manifest, receipt and DNS-record decoders, and its own SPKI and OpenPGP key encoders.
Since 2026-10-12 it also has its own OpenPGP signature-packet parser (the §5.2 slot rule) and its own
ECDSA P-256 verifier (Jacobian coordinates; A uses affine), used to verify the committed signatures and
the negative controls. It verifies; it never signs.
(The json module reads the vector files themselves, which are test data, not inputs under test.)

Hybrid supplement (2026-10-14, formal/p8/HYBRID-SUPPLEMENT-DRAFT.md): B also has its own rule-R codec, its
own strict DER parser for the ML-DSA-65 SPKI, and its own ML-DSA-65 verifier (FIPS 204 Verify, pure mode,
empty context). Where A uses the butterfly NTT, B evaluates and interpolates at the 256 roots directly; it
reads bit fields with a cursor where A uses big integers. It reads hybrid-golden.json and hybrid-reject.json
after the baseline files and reports them on a separate line.

What is shared with implementation A, stated so it is not mistaken for independence:
  - Python's unicodedata tables (Unicode 16.0.0) for NFC and the assigned-code-point test;
  - Python's float() (correctly rounded decimal -> binary64) and repr() (shortest round-trip digits);
  - hashlib's SHA-256, and (hybrid) hashlib's SHAKE-128 and SHAKE-256.

Run:  python3 formal/p8/vectors/check.py      (exit 0 iff every vector agrees)
"""
import hashlib
import json
import os
import re
import struct
import sys
import unicodedata

if unicodedata.unidata_version != "16.0.0":
    sys.exit("check.py needs Unicode 16.0.0 tables (Python 3.14)")


class Bad(Exception):
    def __init__(self, code, why=""):
        super().__init__(code + (": " + why if why else ""))
        self.code = code


# ===================================== UTF-8 (strict, RFC 3629) =====================================
def utf8_decode(b):
    out, i, n = [], 0, len(b)
    while i < n:
        c = b[i]
        if c < 0x80:
            out.append(c)
            i += 1
            continue
        if 0xC2 <= c <= 0xDF:
            need, cp, lo = 1, c & 0x1F, 0x80
        elif 0xE0 <= c <= 0xEF:
            need, cp, lo = 2, c & 0x0F, 0x800
        elif 0xF0 <= c <= 0xF4:
            need, cp, lo = 3, c & 0x07, 0x10000
        else:
            raise Bad("JSON_ENCODING", f"lead byte {c:#x}")
        if i + need >= n:
            raise Bad("JSON_ENCODING", "truncated sequence")
        for k in range(1, need + 1):
            t = b[i + k]
            if t & 0xC0 != 0x80:
                raise Bad("JSON_ENCODING", "bad continuation")
            cp = (cp << 6) | (t & 0x3F)
        if cp < lo or cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
            raise Bad("JSON_ENCODING", f"overlong, surrogate or out of range U+{cp:X}")
        out.append(cp)
        i += need + 1
    return "".join(map(chr, out))


# ===================================== JSON parser (RFC 8259) =====================================
NUM_RX = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
WS = " \t\n\r"


class Parser:
    def __init__(self, s):
        self.s, self.i = s, 0

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in WS:
            self.i += 1

    def fail(self, why):
        raise Bad("JSON_SYNTAX", f"{why} at {self.i}")

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def document(self):
        self.ws()
        v = self.value()
        self.ws()
        if self.i != len(self.s):
            self.fail("text after the value")
        return v

    def value(self):
        c = self.peek()
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c == '"':
            return self.string()
        for word, val in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(word, self.i):
                self.i += len(word)
                return val
        m = NUM_RX.match(self.s, self.i)
        if m and m.end() > self.i:
            self.i = m.end()
            return ("N", m.group(0))
        self.fail("no value")

    def obj(self):
        self.i += 1
        members = []
        self.ws()
        if self.peek() == "}":
            self.i += 1
            return ("O", members)
        while True:
            self.ws()
            if self.peek() != '"':
                self.fail("member name expected")
            k = self.string()
            self.ws()
            if self.peek() != ":":
                self.fail("':' expected")
            self.i += 1
            self.ws()
            members.append((k, self.value()))
            self.ws()
            c = self.peek()
            self.i += 1
            if c == "}":
                return ("O", members)
            if c != ",":
                self.fail("',' or '}' expected")

    def arr(self):
        self.i += 1
        items = []
        self.ws()
        if self.peek() == "]":
            self.i += 1
            return ("A", items)
        while True:
            self.ws()
            items.append(self.value())
            self.ws()
            c = self.peek()
            self.i += 1
            if c == "]":
                return ("A", items)
            if c != ",":
                self.fail("',' or ']' expected")

    def hex4(self):
        h = self.s[self.i:self.i + 4]
        if len(h) != 4 or any(ch not in "0123456789abcdefABCDEF" for ch in h):
            self.fail("bad \\u escape")
        self.i += 4
        return int(h, 16)

    def string(self):
        self.i += 1
        units = []
        simple = {'"': 0x22, "\\": 0x5C, "/": 0x2F, "b": 8, "f": 12, "n": 10, "r": 13, "t": 9}
        while True:
            if self.i >= len(self.s):
                self.fail("unterminated string")
            ch = self.s[self.i]
            self.i += 1
            if ch == '"':
                break
            if ord(ch) < 0x20:
                self.fail("raw control character")
            if ch != "\\":
                units.append(ord(ch))
                continue
            e = self.s[self.i:self.i + 1]
            self.i += 1
            if e in simple:
                units.append(simple[e])
            elif e == "u":
                units.append(self.hex4())
            else:
                self.fail("bad escape")
        out, k = [], 0
        while k < len(units):          # pair surrogate escapes; keep a lone one for the domain check
            u = units[k]
            if 0xD800 <= u <= 0xDBFF and k + 1 < len(units) and 0xDC00 <= units[k + 1] <= 0xDFFF:
                out.append(0x10000 + ((u - 0xD800) << 10) + (units[k + 1] - 0xDC00))
                k += 2
            else:
                out.append(u)
                k += 1
        return "".join(map(chr, out))


def parse_text(b):
    if b[:3] == b"\xef\xbb\xbf":
        raise Bad("JSON_SYNTAX", "BOM")
    text = utf8_decode(b)
    try:
        return Parser(text).document()
    except RecursionError:
        raise Bad("JSON_DEPTH", "recursion")


# ===================================== number rule and formatting =====================================
def _decimal(lit):
    """literal -> (negative, digit string without leading/trailing zeros, exponent) or zero marker."""
    m = re.fullmatch(r"(-?)([0-9]+)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?", lit)
    neg, ip, fp, ex = m.group(1) == "-", m.group(2), m.group(3) or "", int(m.group(4) or 0)
    digits = (ip + fp).lstrip("0")
    if not digits:
        return neg, "", 0
    exp = ex - len(fp)
    stripped = digits.rstrip("0")
    return neg, stripped, exp + (len(digits) - len(stripped))


def es_string(f):
    """ECMAScript Number::toString for a finite double (RFC 8785 §3.2.2.3)."""
    if f == 0:
        return "0"
    sign = "-" if f < 0 else ""
    _, digits, exp = _decimal(repr(abs(f)).replace("e+", "e"))
    k = len(digits)
    n = exp + k
    if k <= n <= 21:
        body = digits + "0" * (n - k)
    elif 0 < n <= 21:
        body = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        body = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        body = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + ("+" if e >= 0 else "-") + str(abs(e))
    return sign + body


def number(lit):
    neg, digits, exp = _decimal(lit)
    if not digits:
        if neg:
            raise Bad("JSON_NUMBER", "negative zero")
        return 0.0
    f = float(lit)
    if f != f or f in (float("inf"), float("-inf")):
        raise Bad("JSON_NUMBER", "not a finite double")
    if f == 0 or _decimal(es_string(f)) != (neg, digits, exp):
        raise Bad("JSON_NUMBER", "value not preserved")
    return f


# ===================================== domain checks =====================================
def nodes(t):
    stack = [t]
    while stack:
        x = stack.pop()
        yield x
        if isinstance(x, tuple) and x[0] == "O":
            for k, v in x[1]:
                yield k
                stack.append(v)
        elif isinstance(x, tuple) and x[0] == "A":
            stack.extend(x[1])


def depth_of(t):
    if isinstance(t, tuple) and t[0] in "OA":
        kids = [v for _, v in t[1]] if t[0] == "O" else t[1]
        return 1 + max([depth_of(v) for v in kids] or [0])
    return 0


def string_ok(s):
    for ch in s:
        c = ord(ch)
        if 0xD800 <= c < 0xE000:
            raise Bad("JSON_STRING", "surrogate")
        if c in range(0xFDD0, 0xFDF0) or c % 0x10000 in (0xFFFE, 0xFFFF):
            raise Bad("JSON_STRING", "noncharacter")
        if unicodedata.category(ch) == "Cn":
            raise Bad("JSON_STRING", "unassigned")
    if unicodedata.normalize("NFC", s) != s:
        raise Bad("JSON_STRING", "not NFC")


def to_value(t):
    if isinstance(t, tuple):
        if t[0] == "O":
            return {k: to_value(v) for k, v in t[1]}
        if t[0] == "A":
            return [to_value(v) for v in t[1]]
        return number(t[1])
    return t


def ingest(b, limit=62):
    t = parse_text(b)
    if depth_of(t) > limit:
        raise Bad("JSON_DEPTH")
    for x in nodes(t):
        if isinstance(x, tuple) and x[0] == "O":
            names = [k for k, _ in x[1]]
            if len(names) != len(set(names)):
                raise Bad("JSON_DUPLICATE_NAME")
    for x in nodes(t):
        if isinstance(x, str):
            string_ok(x)
    for x in nodes(t):
        if isinstance(x, tuple) and x[0] == "N":
            number(x[1])
    return to_value(t)


# ===================================== RFC 8785 serializer =====================================
def jcs(v):
    if v is None:
        return b"null"
    if v is True:
        return b"true"
    if v is False:
        return b"false"
    if isinstance(v, float):
        return es_string(v).encode()
    if isinstance(v, str):
        out = ['"']
        for ch in v:
            c = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == "\\":
                out.append("\\\\")
            elif c < 0x20:
                out.append({8: "\\b", 9: "\\t", 10: "\\n", 12: "\\f", 13: "\\r"}.get(c, "\\u%04x" % c))
            else:
                out.append(ch)
        out.append('"')
        return "".join(out).encode("utf-8")
    if isinstance(v, list):
        return b"[" + b",".join(jcs(x) for x in v) + b"]"
    if isinstance(v, dict):
        keys = sorted(v, key=lambda k: k.encode("utf-16-be"))
        return b"{" + b",".join(jcs(k) + b":" + jcs(v[k]) for k in keys) + b"}"
    raise TypeError(type(v))


def payload_value(b):
    v = ingest(b, limit=64)
    if jcs(v) != b:
        raise Bad("JSON_NONCANONICAL")
    return v


# ===================================== field grammars =====================================
def leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def date_ok(y, m, d):
    if not (1 <= y <= 9999 and 1 <= m <= 12):
        return False
    dim = [31, 29 if leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return 1 <= d <= dim


def is_time(s):
    if not isinstance(s, str) or len(s) != 20:
        return False
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", s):
        return False
    return date_ok(int(s[0:4]), int(s[5:7]), int(s[8:10])) and int(s[11:13]) < 24 and int(s[14:16]) < 60 and int(s[17:19]) < 60


def is_date(s):
    return (isinstance(s, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s) is not None
            and date_ok(int(s[0:4]), int(s[5:7]), int(s[8:10])))


def is_domain(s):
    if not isinstance(s, str) or len(s) > 241 or "." not in s:
        return False
    for lb in s.split("."):
        if not (1 <= len(lb) <= 63) or lb[0] == "-" or lb[-1] == "-":
            return False
        if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in lb):
            return False
    return True


def is_str(x, rx):
    return isinstance(x, str) and re.fullmatch(rx, x) is not None


HEX64 = r"[0-9a-f]{64}"
KMSFP = r"spki-sha256:[0-9a-f]{64}"
GPGFP = r"gpg-sha256:[0-9a-f]{64}"


def attest_ok(v):
    try:
        assert isinstance(v, dict) and sorted(v) == ["common", "signer"]
        c, s = v["common"], v["signer"]
        assert isinstance(c, dict) and sorted(c) == ["alg", "binding_forms", "content", "declared_issue_time", "issuer",
                                                     "manifest_sha256", "preamble_sha256", "profile", "spec", "vectors_sha256"]
        assert isinstance(s, dict) and list(s) == ["key_fp"]
        assert is_str(c["alg"], r"[A-Z0-9][A-Z0-9-]{0,63}")
        f = c["binding_forms"]
        assert isinstance(f, list) and f and all(is_str(x, r"[A-Z][A-Z0-9_]{0,31}") for x in f)
        assert all(a < b for a, b in zip(f, f[1:]))
        assert is_time(c["declared_issue_time"]) and is_domain(c["issuer"])
        assert all(is_str(c[k], HEX64) for k in ("manifest_sha256", "preamble_sha256", "vectors_sha256"))
        assert c["profile"] == "tessera-v1-strict"
        sp = c["spec"]
        assert isinstance(sp, dict) and sorted(sp) == ["id", "sha256"]
        assert is_str(sp["id"], r"[a-z0-9][a-z0-9._/-]{0,127}") and is_str(sp["sha256"], HEX64)
        assert is_str(s["key_fp"], KMSFP) or is_str(s["key_fp"], GPGFP)
    except (AssertionError, KeyError):
        raise Bad("SCHEMA", "attestation")


def manifest_ok(v):
    good = (isinstance(v, dict) and sorted(v) == ["alg", "issuer", "key_fp", "sset", "ver"]
            and is_str(v["alg"], r"[A-Z0-9][A-Z0-9-]{0,63}") and is_domain(v["issuer"])
            and is_str(v["key_fp"], KMSFP) and isinstance(v["sset"], list) and len(v["sset"]) == 1
            and is_str(v["sset"][0], GPGFP) and v["ver"] == "map-v1")
    if not good:
        raise Bad("SCHEMA", "manifest")


# ===================================== byte layouts =====================================
TAGS = {b"tessera-v1/attest": "attest", b"tessera-v1/manifest": "manifest",
        b"tessera-v1/receipt-anchor-sig": "anchor", b"tessera-v1/dnssec-snapshot": "snapshot"}
TAG_OF = {v: k for k, v in TAGS.items()}
CAP = 16777216


def need(b, pos, n):
    if pos + n > len(b):
        raise Bad("TRUNCATED")


def tag_at(b, want):
    need(b, 0, 1)
    n = b[0]
    need(b, 1, n)
    tag = bytes(b[1:1 + n])
    if tag not in TAGS:
        raise Bad("TAG_UNKNOWN")
    if TAGS[tag] != want:
        raise Bad("TAG_MISMATCH")
    return 1 + n


def frame_decode(b, want):
    pos = tag_at(b, want)
    need(b, pos, 2)
    if b[pos] != 0 or b[pos + 1] != 1:
        raise Bad("CV_UNKNOWN")
    pos += 2
    need(b, pos, 4)
    length = int.from_bytes(b[pos:pos + 4], "big")
    pos += 4
    if length > CAP:
        raise Bad("LENGTH_CAP")
    remaining = len(b) - pos
    if remaining != length:
        raise Bad("TRUNCATED" if remaining < length else "TRAILING")
    v = payload_value(bytes(b[pos:]))
    (attest_ok if want == "attest" else manifest_ok)(v)
    return v


def frame_encode(kind, value):
    p = jcs(value)
    t = TAG_OF[kind]
    return bytes([len(t)]) + t + b"\x00\x01" + len(p).to_bytes(4, "big") + p


# ---- signature slots (ENCODING-V1 §5.2): the rule is chosen by (common.alg, slot index) ----
V1_ALG = "OPENPGP4-ECDSA-P256-SHA256"
HYB_ALG = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256"     # hybrid supplement (OWNER-PROPOSED)
RULES = {V1_ALG: ["pgp4", "pgp4"], HYB_ALG: ["mldsa65", "pgp4"]}
CAPS = {"pgp4": 1024, "mldsa65": 3309, "opaque": 65536}


def rule_of(alg, slot):
    return RULES.get(alg, ["opaque", "opaque"])[slot]


def subpackets_ok(b, lo, hi):
    """True iff b[lo:hi] is an exact run of subpackets with shortest-form lengths."""
    i = lo
    while i < hi:
        c = b[i]
        if c <= 191:
            ln, i = c, i + 1
        elif c <= 254:
            if i + 1 >= hi:
                return False
            ln, i = (c - 192) * 256 + b[i + 1] + 192, i + 2
        else:
            if i + 4 >= hi:
                return False
            ln, i = int.from_bytes(b[i + 1:i + 5], "big"), i + 5
            if ln <= 16319:
                return False
        if ln < 1 or i + ln > hi:
            return False
        i += ln
    return True


def pgp4_parse(s):
    """-> (hashed area bytes, r, s). One legacy-format tag-2 packet, shortest length form, v4 type 0x00,
    ECDSA (19) with SHA-256 (8); every inner length consumed exactly."""
    if s[0] == 0x88:
        need(s, 1, 1)
        blen, at = s[1], 2
    elif s[0] == 0x89:
        need(s, 1, 2)
        blen, at = int.from_bytes(s[1:3], "big"), 3
        if blen <= 255:
            raise Bad("SIG_PACKET")
    else:
        raise Bad("SIG_PACKET")
    if len(s) - at != blen:
        raise Bad("TRUNCATED" if len(s) - at < blen else "TRAILING")
    end = len(s)
    fmt = Bad("SIG_FORMAT")
    if end - at < 6 or list(s[at:at + 4]) != [4, 0, 19, 8]:
        raise fmt
    hlen = int.from_bytes(s[at + 4:at + 6], "big")
    h0, h1 = at + 6, at + 6 + hlen
    if h1 + 2 > end or not subpackets_ok(s, h0, h1):
        raise fmt
    ulen = int.from_bytes(s[h1:h1 + 2], "big")
    u0, u1 = h1 + 2, h1 + 2 + ulen
    if u1 > end or not subpackets_ok(s, u0, u1):
        raise fmt
    i = u1 + 2                                   # skip the unsigned left-16 field
    ints = []
    for _ in range(2):
        if i + 2 > end:
            raise fmt
        nbits = int.from_bytes(s[i:i + 2], "big")
        nbytes = (nbits + 7) // 8
        if nbits == 0 or nbits > 256 or i + 2 + nbytes > end:
            raise fmt
        v = int.from_bytes(s[i + 2:i + 2 + nbytes], "big")
        if v.bit_length() != nbits:
            raise fmt
        ints.append(v)
        i += 2 + nbytes
    if i != end:
        raise fmt
    return bytes(s[h0:h1]), ints[0], ints[1]


def sig_check(s, alg, slot):
    r = rule_of(alg, slot)
    if len(s) == 0:
        raise Bad("SIG_EMPTY")
    if len(s) > CAPS[r]:
        raise Bad("LENGTH_CAP")
    if r == "pgp4":
        pgp4_parse(s)
    if r == "mldsa65" and len(s) != 3309:
        raise Bad("SIG_FORMAT")


def anchor_decode(b):
    pos = tag_at(b, "anchor")
    need(b, pos, 1)
    if b[pos] != 2:
        raise Bad("ANCHOR_COUNT")
    pos += 1
    out = []
    for slot in (0, 1):
        need(b, pos, 4)
        n = int.from_bytes(b[pos:pos + 4], "big")
        pos += 4
        if n > CAP + 64:
            raise Bad("LENGTH_CAP")
        need(b, pos, n)
        f = bytes(b[pos:pos + n])
        alg = frame_decode(f, "attest")["common"]["alg"]
        pos += n
        need(b, pos, 4)
        n = int.from_bytes(b[pos:pos + 4], "big")
        pos += 4
        if n == 0:
            raise Bad("SIG_EMPTY")
        if n > CAPS[rule_of(alg, slot)]:
            raise Bad("LENGTH_CAP")
        need(b, pos, n)
        sg = bytes(b[pos:pos + n])
        sig_check(sg, alg, slot)
        out.append((f, sg))
        pos += n
    if pos != len(b):
        raise Bad("TRAILING")
    return out


def anchor_encode(f0, s0, f1, s1):
    t = TAG_OF["anchor"]
    return bytes([len(t)]) + t + b"\x02" + b"".join(len(x).to_bytes(4, "big") + x for x in (f0, s0, f1, s1))


# ---- ECDSA P-256 verification (Jacobian coordinates), for the integration checks only ----
EC_P = 2**256 - 2**224 + 2**192 + 2**96 - 1
EC_N = int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16)
EC_G = (int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16),
        int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16))


def jdbl(X, Y, Z):
    if Y == 0 or Z == 0:
        return (1, 1, 0)
    p = EC_P
    d = 4 * X * Y * Y % p
    m = 3 * (X - Z * Z) * (X + Z * Z) % p          # a = -3
    X3 = (m * m - 2 * d) % p
    return X3, (m * (d - X3) - 8 * pow(Y, 4, p)) % p, 2 * Y * Z % p


def jadd(A_, B_):
    X1, Y1, Z1 = A_
    X2, Y2, Z2 = B_
    if Z1 == 0:
        return B_
    if Z2 == 0:
        return A_
    p = EC_P
    U1, U2 = X1 * Z2 * Z2 % p, X2 * Z1 * Z1 % p
    S1, S2 = Y1 * pow(Z2, 3, p) % p, Y2 * pow(Z1, 3, p) % p
    if U1 == U2:
        return jdbl(X1, Y1, Z1) if S1 == S2 else (1, 1, 0)
    Hh, Rr = (U2 - U1) % p, (S2 - S1) % p
    X3 = (Rr * Rr - Hh ** 3 - 2 * U1 * Hh * Hh) % p
    return X3, (Rr * (U1 * Hh * Hh - X3) - S1 * Hh ** 3) % p, Hh * Z1 * Z2 % p


def jmul(k, pt):
    acc, cur = (1, 1, 0), (pt[0], pt[1], 1)
    while k:
        if k & 1:
            acc = jadd(acc, cur)
        cur = jdbl(*cur)
        k >>= 1
    return acc


def p256_verify(Q, digest, r, s):
    if not (0 < r < EC_N and 0 < s < EC_N) or not on_curve(*Q):
        return False
    w = pow(s, EC_N - 2, EC_N)
    X, Y, Z = jadd(jmul(int.from_bytes(digest, "big") * w % EC_N, EC_G), jmul(r * w % EC_N, Q))
    if Z == 0:
        return False
    return X * pow(Z * Z, EC_P - 2, EC_P) % EC_P % EC_N == r


def pgp4_verify(frame, sig, Q):
    hashed, r, s = pgp4_parse(sig)
    pre = b"\x04\x00\x13\x08" + len(hashed).to_bytes(2, "big") + hashed
    digest = hashlib.sha256(frame + pre + b"\x04\xff" + len(pre).to_bytes(4, "big")).digest()
    return p256_verify(Q, digest, r, s)


# ---- ML-DSA-65 verification (FIPS 204), implementation B: verify only, pure mode, empty context ----
# Written apart from gen.py. Where A uses the butterfly NTT, B evaluates and interpolates directly:
# the NTT domain is the vector of values at the 256 roots zeta^(2*brv8(i)+1) of X^256 + 1 (FIPS 204
# §7.5), so B computes each transform as a matrix product with power tables it builds itself. Bit
# fields are read with an explicit bit cursor rather than a big integer.
MQ = 8380417
M_K, M_L = 6, 5


def _bitrev8(i):
    r = 0
    for _ in range(8):
        r, i = (r << 1) | (i & 1), i >> 1
    return r


_ROOTS = [pow(1753, 2 * _bitrev8(i) + 1, MQ) for i in range(256)]
_FWD = [[pow(w, j, MQ) for j in range(256)] for w in _ROOTS]                    # row i: powers of root i
_INV256 = pow(256, MQ - 2, MQ)
_BWD = [[pow(_ROOTS[i], (512 - j) % 512, MQ) * _INV256 % MQ for i in range(256)] for j in range(256)]


def m_fwd(f):
    return [sum(a * b for a, b in zip(row, f)) % MQ for row in _FWD]


def m_bwd(fh):
    return [sum(a * b for a, b in zip(row, fh)) % MQ for row in _BWD]


def m_bits(data, width, count):
    """Little-endian bit cursor: `count` unsigned fields of `width` bits."""
    out, cur, nbits, pos = [], 0, 0, 0
    for _ in range(count):
        while nbits < width:
            cur |= data[pos] << nbits
            pos += 1
            nbits += 8
        out.append(cur & ((1 << width) - 1))
        cur >>= width
        nbits -= width
    return out


def m_put4(vals):
    return bytes(vals[i] | (vals[i + 1] << 4) for i in range(0, len(vals), 2))


def m_xof128_coeffs(seed):
    stream, got, need_bytes = b"", [], 1024
    while len(got) < 256:
        stream = hashlib.shake_128(seed).digest(need_bytes)
        got = []
        for k in range(len(stream) // 3):
            b0, b1, b2 = stream[3 * k], stream[3 * k + 1], stream[3 * k + 2] & 127
            val = (b2 << 16) + (b1 << 8) + b0
            if val < MQ:
                got.append(val)
            if len(got) == 256:
                break
        need_bytes += 1024
    return got


def m_challenge(ct):
    tau, stream, need_bytes = 49, b"", 512
    while True:
        stream = hashlib.shake_256(ct).digest(need_bytes)
        sign_bits = [(stream[q // 8] >> (q % 8)) & 1 for q in range(64)]
        c, p, done = [0] * 256, 8, True
        for i in range(256 - tau, 256):
            while p < len(stream) and stream[p] > i:
                p += 1
            if p == len(stream):
                done = False
                break
            j = stream[p]
            p += 1
            c[i] = c[j]
            c[j] = MQ - 1 if sign_bits[i - (256 - tau)] else 1
        if done:
            return c
        need_bytes *= 2


def m_split(r):
    """Decompose with gamma2 = (q-1)/32: (r1, r0), r = r1 * 2*gamma2 + r0 (mod q)."""
    two_g2 = (MQ - 1) // 16
    r = r % MQ
    r0 = r % two_g2
    if r0 > two_g2 // 2:
        r0 -= two_g2
    if r - r0 == MQ - 1:
        return 0, r0 - 1
    return (r - r0) // two_g2, r0


def mldsa65_ok(pk, msg, sig, off=()):
    """off: gates switched off for demonstration vectors only ("norm", "order", "padding")."""
    if len(pk) != 1952 or len(sig) != 3309:
        return False
    rho = pk[:32]
    t1 = [m_bits(pk[32 + 320 * i:], 10, 256) for i in range(M_K)]
    ct, zbytes, hbytes = sig[:48], sig[48:3248], sig[3248:]
    g1 = 1 << 19
    z = [[g1 - v for v in m_bits(zbytes[640 * i:], 20, 256)] for i in range(M_L)]   # signed integers
    if "norm" not in off and max(abs(v) for row in z for v in row) >= g1 - 196:
        return False
    # hint vector: omega = 55 position bytes, then k cumulative counts; strict order, zero padding
    hint = [[0] * 256 for _ in range(M_K)]
    prev_end = 0
    for i in range(M_K):
        end = hbytes[55 + i]
        if not prev_end <= end <= 55:
            return False
        positions = list(hbytes[prev_end:end])
        if "order" not in off and any(a >= b for a, b in zip(positions, positions[1:])):
            return False
        for p in positions:
            hint[i][p] = 1
        prev_end = end
    if "padding" not in off and any(hbytes[prev_end:55]):
        return False
    tr = hashlib.shake_256(pk).digest(64)
    mu = hashlib.shake_256(tr + bytes([0, 0]) + msg).digest(64)
    c_ntt = m_fwd(m_challenge(ct))
    z_ntt = [m_fwd([v % MQ for v in row]) for row in z]
    w1_bytes = b""
    for r in range(M_K):
        acc = [0] * 256
        for s in range(M_L):
            a_rs = m_xof128_coeffs(rho + bytes([s, r]))
            acc = [(x + a * b) % MQ for x, a, b in zip(acc, a_rs, z_ntt[s])]
        t_ntt = m_fwd([(v * 8192) % MQ for v in t1[r]])
        acc = [(x - c * t) % MQ for x, c, t in zip(acc, c_ntt, t_ntt)]
        w = m_bwd(acc)
        digits = []
        for hbit, coeff in zip(hint[r], w):
            hi, lo = m_split(coeff)
            if hbit:
                hi = (hi + (1 if lo > 0 else -1)) % 16
            digits.append(hi)
        w1_bytes += m_put4(digits)
    return hashlib.shake_256(mu + w1_bytes).digest(48) == ct


def snapshot_decode(b):
    pos = tag_at(b, "snapshot")
    need(b, pos, 4)
    n = int.from_bytes(b[pos:pos + 4], "big")
    pos += 4
    if n > CAP:
        raise Bad("LENGTH_CAP")
    if n == 0:
        raise Bad("SCHEMA")
    if len(b) - pos != n:
        raise Bad("TRUNCATED" if len(b) - pos < n else "TRAILING")
    return bytes(b[pos:])


def snapshot_encode(s):
    t = TAG_OF["snapshot"]
    return bytes([len(t)]) + t + len(s).to_bytes(4, "big") + s


def receipt(fm, f0, s0, f1, s1, an, keys=None):
    m = frame_decode(fm, "manifest")
    a, b = frame_decode(f0, "attest"), frame_decode(f1, "attest")
    if (a["signer"]["key_fp"], b["signer"]["key_fp"]) != (m["key_fp"], m["sset"][0]):
        raise Bad("RECEIPT_SLOT")
    if jcs(a["common"]) != jcs(b["common"]):
        raise Bad("RECEIPT_COMMON_MISMATCH")
    c = a["common"]
    if (c["manifest_sha256"], c["issuer"], c["alg"]) != (hashlib.sha256(fm).hexdigest(), m["issuer"], m["alg"]):
        raise Bad("RECEIPT_MANIFEST_MISMATCH")
    committed = anchor_decode(an)
    if committed != [(f0, s0), (f1, s1)]:
        raise Bad("RECEIPT_ANCHOR_MISMATCH")
    if keys is not None:
        if c["alg"] not in RULES:
            raise Bad("UNVERIFIABLE")
        kq, gq, created = keys
        if c["alg"] == HYB_ALG:                          # kms key is the transported SPKI DER itself
            kver, kder = mldsa_spki(kq), kq
        else:
            kver, kder = kq, spki(*kq)
        if ("spki-sha256:" + hashlib.sha256(kder).hexdigest() != m["key_fp"]
                or "gpg-sha256:" + hashlib.sha256(v4_body(*gq, created)).hexdigest() != m["sset"][0]):
            raise Bad("KEY_MISMATCH")
        for slot, ((fr, sg), q) in enumerate(zip(committed, (kver, gq))):     # verify what the anchor commits
            if not slot_verify(c["alg"], slot, fr, sg, q):
                raise Bad("SIG_INVALID")
    return c


def slot_verify(alg, slot, msg, sg, q):
    if rule_of(alg, slot) == "mldsa65":
        return mldsa65_ok(q, msg, sg)
    return pgp4_verify(msg, sg, q)


# ---- hybrid supplement: ML-DSA-65 SPKI (strict DER, parsed field by field), possession, single signatures ----
def der_tlv(b, pos):
    """(tag, start, end) of one DER element at pos; definite, minimal lengths only; else KEY_FORMAT."""
    if pos + 2 > len(b):
        raise Bad("KEY_FORMAT")
    tag, first = b[pos], b[pos + 1]
    pos += 2
    if first < 0x80:
        n = first
    else:
        k = first & 0x7F
        if k == 0 or k > 4 or pos + k > len(b) or b[pos] == 0:
            raise Bad("KEY_FORMAT")
        n = int.from_bytes(b[pos:pos + k], "big")
        pos += k
        if n < 0x80:
            raise Bad("KEY_FORMAT")
    if pos + n > len(b):
        raise Bad("KEY_FORMAT")
    return tag, pos, pos + n


def mldsa_spki(b):
    """SEQUENCE { SEQUENCE { OID id-ml-dsa-65 } , BIT STRING { 00, 1952-byte key } }, nothing else."""
    b = bytes(b)
    t, s0, e0 = der_tlv(b, 0)
    if t != 0x30 or e0 != len(b):
        raise Bad("KEY_FORMAT")
    t, s1, e1 = der_tlv(b, s0)
    if t != 0x30:
        raise Bad("KEY_FORMAT")
    t, s2, e2 = der_tlv(b, s1)
    if t != 0x06 or b[s2:e2] != oid("2.16.840.1.101.3.4.3.18") or e2 != e1:          # parameters must be absent
        raise Bad("KEY_FORMAT")
    t, s3, e3 = der_tlv(b, e1)
    if t != 0x03 or e3 != e0 or e3 - s3 != 1953 or b[s3] != 0:
        raise Bad("KEY_FORMAT")
    return b[s3 + 1:e3]


def slot_key(alg, slot, key, m):
    if slot == 0:
        kder = key if alg == HYB_ALG else spki(*key)
        ver = mldsa_spki(key) if alg == HYB_ALG else key
        good = "spki-sha256:" + hashlib.sha256(kder).hexdigest() == m["key_fp"]
    else:
        x, y, created = key
        ver = (x, y)
        good = "gpg-sha256:" + hashlib.sha256(v4_body(x, y, created)).hexdigest() == m["sset"][0]
    if not good:
        raise Bad("KEY_MISMATCH")
    return ver


def possession(fm, slot, sg, key):
    m = frame_decode(fm, "manifest")
    alg = m["alg"]
    ver = slot_key(alg, slot, key, m) if alg in RULES else None
    sig_check(sg, alg, slot)
    if alg not in RULES:
        raise Bad("UNVERIFIABLE")
    if not slot_verify(alg, slot, fm, sg, ver):
        raise Bad("POSSESSION_INVALID")
    return m


def sig_r(msg, sg, der_key):
    sig_check(sg, HYB_ALG, 0)
    if not mldsa65_ok(mldsa_spki(der_key), msg, sg):
        raise Bad("SIG_INVALID")


def key_kms(der_key, key_fp):
    mldsa_spki(der_key)
    if "spki-sha256:" + hashlib.sha256(der_key).hexdigest() != key_fp:
        raise Bad("KEY_MISMATCH")


def keys_from(k):
    kms = (bytes.fromhex(k["kms"]["spki_der_hex"]) if "spki_der_hex" in k["kms"]
           else (int(k["kms"]["x"], 16), int(k["kms"]["y"], 16)))
    return (kms, (int(k["gpg"]["x"], 16), int(k["gpg"]["y"], 16)), k["gpg"]["created"])


def one_key(k):
    if "spki_der_hex" in k:
        return bytes.fromhex(k["spki_der_hex"])
    if "created" in k:
        return (int(k["x"], 16), int(k["y"], 16), k["created"])
    return (int(k["x"], 16), int(k["y"], 16))


# ===================================== DNS key-publication record =====================================
def owner_labels(w):
    labels, i = [], 0
    while True:
        if i >= len(w):
            raise Bad("DNS_OWNER")
        n = w[i]
        if n == 0:
            if i != len(w) - 1:
                raise Bad("DNS_OWNER")
            return labels
        if n >= 64 or i + n >= len(w):
            raise Bad("DNS_OWNER")
        labels.append(bytes(w[i + 1:i + 1 + n]).decode("latin-1").lower())
        i += n + 1


def dns_decode(D, owner, rrset):
    if owner_labels(owner) != ["_tessera-v1"] + D.split("."):
        raise Bad("DNS_OWNER")
    if len(rrset) != 1:
        raise Bad("DNS_RRSET")
    rd, strs, i = rrset[0], [], 0
    while i < len(rd):
        n = rd[i]
        if i + 1 + n > len(rd):
            raise Bad("DNS_RDATA")
        strs.append(rd[i + 1:i + 1 + n])
        i += n + 1
    if len(strs) != 1:
        raise Bad("DNS_STRINGS")
    v = strs[0]
    if len(v) == 0 or not all(33 <= c <= 126 for c in v):
        raise Bad("DNS_SYNTAX")
    pairs = []
    for part in v.decode("ascii").split(";"):
        k, eq, val = part.partition("=")
        if not eq or not val or "=" in val or not re.fullmatch(r"[a-z][a-z-]*", k):
            raise Bad("DNS_SYNTAX")
        pairs.append((k, val))
    if pairs[0] != ("v", "tessera1") or "v" in [k for k, _ in pairs[1:]]:
        raise Bad("DNS_VERSION")
    names = [k for k, _ in pairs]
    if any(k not in ("v", "profile", "kms", "gpg", "issuance-not-before", "issuance-not-after") for k in names):
        raise Bad("DNS_FIELD_UNKNOWN")
    seen = set()
    for k in names:
        if k in seen:
            raise Bad("DNS_SLOT_DUPLICATE" if k in ("kms", "gpg") else "DNS_FIELD_DUPLICATE")
        seen.add(k)
    if "kms" not in seen or "gpg" not in seen:
        raise Bad("DNS_SLOT_MISSING")
    if not {"profile", "issuance-not-before", "issuance-not-after"} <= seen:
        raise Bad("DNS_FIELD_MISSING")
    if names != ["v", "profile", "kms", "gpg", "issuance-not-before", "issuance-not-after"]:
        raise Bad("DNS_ORDER")
    d = dict(pairs)
    if d["profile"] != "tessera-v1-strict":
        raise Bad("DNS_PROFILE")
    if not (is_str(d["kms"], r"[0-9a-f]{64}") and is_str(d["gpg"], r"[0-9a-f]{64}")
            and is_time(d["issuance-not-after"]) and is_time(d["issuance-not-before"])):
        raise Bad("DNS_VALUE")
    span = epoch(d["issuance-not-after"]) - epoch(d["issuance-not-before"])
    if span <= 0:
        raise Bad("DNS_WINDOW")
    if span > 7776000:  # 90 days of 86400 s (A9, 2026-10-12)
        raise Bad("DNS_WINDOW_LENGTH")
    return d


def epoch(t):
    """'YYYY-MM-DDThh:mm:ssZ' -> Unix seconds, by days-from-civil (proleptic Gregorian)."""
    y, m, dd = int(t[0:4]), int(t[5:7]), int(t[8:10])
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + dd - 1
    days = era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + doy - 719468
    return days * 86400 + int(t[11:13]) * 3600 + int(t[14:16]) * 60 + int(t[17:19])


def window(D, owner, rrset, declared, t_anchor):
    d = dns_decode(D, owner, rrset)
    if epoch(declared) < epoch(d["issuance-not-before"]):
        raise Bad("ISSUANCE_WINDOW")
    if not t_anchor <= epoch(d["issuance-not-after"]):
        raise Bad("ISSUANCE_WINDOW")
    return d


def owner_wire(name):
    return b"".join(bytes([len(x)]) + x.encode() for x in name.split(".")) + b"\x00"


# ===================================== key encodings =====================================
def der(tag, body):
    n = len(body)
    ln = bytes([n]) if n < 128 else bytes([0x80 | ((n.bit_length() + 7) // 8)]) + n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([tag]) + ln + body


def oid(dotted):
    parts = [int(x) for x in dotted.split(".")]
    out = bytes([40 * parts[0] + parts[1]])
    for p in parts[2:]:
        chunk = [p & 0x7F]
        p >>= 7
        while p:
            chunk.append(0x80 | (p & 0x7F))
            p >>= 7
        out += bytes(reversed(chunk))
    return out


def on_curve(x, y):
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    b = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
    return (y * y - x * x * x + 3 * x - b) % p == 0


def spki(x, y):
    pt = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    alg = der(0x30, der(0x06, oid("1.2.840.10045.2.1")) + der(0x06, oid("1.2.840.10045.3.1.7")))
    return der(0x30, alg + der(0x03, b"\x00" + pt))


def v4_body(x, y, created):
    pt = b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")
    o = oid("1.2.840.10045.3.1.7")
    bits = 8 * len(pt) - 5          # 0x04 has three significant bits
    return b"\x04" + created.to_bytes(4, "big") + b"\x13" + bytes([len(o)]) + o + bits.to_bytes(2, "big") + pt


# ===================================== the agreement run =====================================
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    bad = False
    for label, gname, rname in (("", "golden.json", "reject.json"),
                                (" (hybrid supplement)", "hybrid-golden.json", "hybrid-reject.json")):
        golden = json.load(open(os.path.join(here, gname)))["vectors"]
        reject = json.load(open(os.path.join(here, rname)))["vectors"]
        bad = agreement(golden, reject, label) or bad
    sys.exit(1 if bad else 0)


def agreement(golden, reject, label):
    fails = []
    hx = bytes.fromhex
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def rargs(i):
        return [hx(i[n]) for n in ("manifest_hex", "f0_hex", "s0_hex", "f1_hex", "s1_hex", "anchor_hex")]

    def common_from(inp):
        c = {k: v for k, v in inp.items() if k != "content_text_hex"}
        c["content"] = ingest(hx(inp["content_text_hex"]))
        return c

    for g in golden:
        k, i = g["kind"], g.get("input", {})
        try:
            if k == "fingerprint-kms":
                x, y = int(i["x"], 16), int(i["y"], 16)
                assert on_curve(x, y)
                d = spki(x, y)
                assert d.hex() == g["spki_der_hex"] and "spki-sha256:" + sha(d) == g["key_fp"]
            elif k == "fingerprint-gpg":
                x, y = int(i["x"], 16), int(i["y"], 16)
                assert on_curve(x, y)
                body = v4_body(x, y, i["created"])
                fp = hashlib.sha256(body).hexdigest()
                assert body.hex() == g["key_packet_body_hex"] and "gpg-sha256:" + fp == g["key_fp"]
            elif k == "number":
                f = struct.unpack(">d", hx(i["binary64_hex"]))[0]
                assert es_string(f) == g["string"]
            elif k == "content":
                want = hx(g["bytes_hex"])
                assert jcs(ingest(hx(i["text_hex"]))) == want
                assert jcs(payload_value(want)) == want
            elif k == "frame-manifest":
                b = hx(g["bytes_hex"])
                v = frame_decode(b, "manifest")
                assert v == {**i, "ver": "map-v1"} and frame_encode("manifest", v) == b and sha(b) == g["sha256"]
            elif k == "frame-attest":
                b = hx(g["bytes_hex"])
                v = frame_decode(b, "attest")
                mine = {"common": common_from(i["common"]), "signer": {"key_fp": i["key_fp"]}}
                assert jcs(v) == jcs(mine) and frame_encode("attest", mine) == b and sha(b) == g["sha256"]
            elif k == "signature":
                fr, sg = hx(i["frame_hex"]), hx(g["bytes_hex"])
                slot = {"kms": 0, "gpg": 1}[i["slot"]]
                sig_check(sg, i["alg"], slot)
                assert pgp4_verify(fr, sg, (int(i["x"], 16), int(i["y"], 16))) is g["verifies"]
                if "created" in i:          # a real slot-2 capture: its frame names this key's gpg-sha256
                    fp = "gpg-sha256:" + sha(v4_body(int(i["x"], 16), int(i["y"], 16), i["created"]))
                    assert frame_decode(fr, "attest")["signer"]["key_fp"] == fp
            elif k == "signature-mldsa65":
                msg, sg, der_key = hx(i["message_hex"]), hx(g["bytes_hex"]), hx(i["spki_der_hex"])
                sig_check(sg, i["alg"], {"kms": 0, "gpg": 1}[i["slot"]])
                pk = mldsa_spki(der_key)
                assert mldsa65_ok(pk, msg, sg) is g["verifies"]
                if "mu_hex" in i:           # the issuer-side external mu, recomputed here
                    tr = hashlib.shake_256(pk).digest(64)
                    assert hashlib.shake_256(tr + b"\x00\x00" + msg).digest(64) == hx(i["mu_hex"])
            elif k == "fingerprint-kms-spki":
                d = hx(g["spki_der_hex"])
                mldsa_spki(d)
                assert "spki-sha256:" + sha(d) == g["key_fp"]
            elif k == "possession":
                possession(hx(i["manifest_hex"]), {"kms": 0, "gpg": 1}[i["slot"]], hx(g["bytes_hex"]), one_key(i["key"]))
            elif k == "anchor":
                b = hx(g["bytes_hex"])
                parts = [hx(i[n]) for n in ("f0_hex", "s0_hex", "f1_hex", "s1_hex")]
                assert anchor_decode(b) == [(parts[0], parts[1]), (parts[2], parts[3])]
                assert anchor_encode(*parts) == b and sha(b) == g["sha256"]
            elif k == "snapshot":
                b = hx(g["bytes_hex"])
                s = hx(i["snapshot_hex"])
                assert snapshot_decode(b) == s and snapshot_encode(s) == b and sha(b) == g["sha256"]
            elif k == "receipt":
                receipt(*rargs(i), keys_from(i["keys"]))
                assert sha(hx(i["anchor_hex"])) == g["anchor_sha256"]
            elif k == "dns":
                rr = [hx(r) for r in g["rdata_hex"]]
                d = dns_decode(i["D"], hx(g["owner_hex"]), rr)
                want = f"v=tessera1;profile=tessera-v1-strict;kms={i['kms']};gpg={i['gpg']}"
                if i["issuance_not_before"]:
                    want += f";issuance-not-before={i['issuance_not_before']}"
                want += f";issuance-not-after={i['issuance_not_after']}"
                assert want == g["value"] and rr == [bytes([len(want)]) + want.encode()]
                assert d["kms"] == i["kms"] and d["gpg"] == i["gpg"] and d.get("issuance-not-before") == i["issuance_not_before"]
                assert d["issuance-not-after"] == i["issuance_not_after"]
                if g["id"] != "DNS-03":
                    assert hx(g["owner_hex"]) == owner_wire("_tessera-v1." + i["D"])
            elif k == "window":
                window(i["D"], hx(i["owner_hex"]), [hx(r) for r in i["rdata_hex"]], i["declared_issue_time"], i["t_anchor"])
            else:
                raise AssertionError("unknown kind " + k)
        except (AssertionError, Bad) as e:
            fails.append(f"golden {g['id']}: {e!r}")

    entries = {
        "content": lambda i: ingest(hx(i["text_hex"])),
        "frame-attest": lambda i: frame_decode(hx(i["bytes_hex"]), "attest"),
        "frame-manifest": lambda i: frame_decode(hx(i["bytes_hex"]), "manifest"),
        "anchor": lambda i: anchor_decode(hx(i["bytes_hex"])),
        "snapshot": lambda i: snapshot_decode(hx(i["bytes_hex"])),
        "receipt": lambda i: receipt(*rargs(i), keys_from(i["keys"])),
        "dns": lambda i: dns_decode(i["D"], hx(i["owner_hex"]), [hx(r) for r in i["rdata_hex"]]),
        "window": lambda i: window(i["D"], hx(i["owner_hex"]), [hx(r) for r in i["rdata_hex"]],
                                   i["declared_issue_time"], i["t_anchor"]),
        "key-kms": lambda i: key_kms(hx(i["spki_der_hex"]), i["key_fp"]),
        "possession": lambda i: possession(hx(i["manifest_hex"]), {"kms": 0, "gpg": 1}[i["slot"]], hx(i["sig_hex"]),
                                           one_key(i["key"])),
        "signature-r": lambda i: sig_r(hx(i["message_hex"]), hx(i["sig_hex"]), hx(i["spki_der_hex"])),
    }
    agree = controls = demos = 0
    for r in reject:
        if "demonstration" in r or "decoder_failure" in r:
            # HS-03: B's own verifier, with exactly one decoding gate off (must accept) or with every
            # disable-able gate off (a decoder failure must still reject).
            i = r["input"]
            pk = mldsa_spki(hx(i["keys"]["kms"]["spki_der_hex"]))
            fr, sg = hx(i["f0_hex"]), hx(i["s0_hex"])
            if "demonstration" in r:
                ok = (not mldsa65_ok(pk, fr, sg)) and mldsa65_ok(pk, fr, sg, off=(r["demonstration"]["gate_off"],))
            else:
                ok = not mldsa65_ok(pk, fr, sg, off=("norm", "order", "padding"))
            if ok:
                demos += 1
            else:
                fails.append(f"demonstration {r['id']}: B does not isolate the named decoding gate")
        if "control" in r:
            # Negative control: the presented signature verifies (B's own ECDSA), and the anchor over the
            # presented bytes is not the stamped one; the expected rejection is then checked below.
            i, c = r["input"], r["control"]
            kq, gq, _ = keys_from(i["keys"])
            slot = 0 if c["slot"] == "kms" else 1
            fr, sg, q = (hx(i["f0_hex"]), hx(i["s0_hex"]), kq) if slot == 0 else (hx(i["f1_hex"]), hx(i["s1_hex"]), gq)
            alg = frame_decode(fr, "attest")["common"]["alg"]
            if isinstance(q, bytes):
                q = mldsa_spki(q)
            ok = slot_verify(alg, slot, fr, sg, q) is c["presented_sig_verifies"]
            ok = ok and sha(anchor_encode(*rargs(i)[1:5])) != c["stamped_anchor_sha256"]
            if ok:
                controls += 1
            else:
                fails.append(f"control {r['id']}: presented signature did not verify, or its anchor equals the stamped one")
        try:
            entries[r["entry"]](r["input"])
            fails.append(f"reject {r['id']}: ACCEPTED by implementation B (expected {r['expect']})")
        except Bad as e:
            if e.code == r["expect"]:
                agree += 1
            else:
                fails.append(f"reject {r['id']}: rejected as {e.code}, implementation A says {r['expect']}")

    print(f"implementation B{label}: golden {len(golden) - sum(f.startswith('golden') for f in fails)}/{len(golden)} round-trip; "
          f"rejection {agree}/{len(reject)} rejected with the same reason code; "
          f"negative controls {controls}/{sum('control' in r for r in reject)} (signature verifies, anchor check fails)"
          + (f"; gate demonstrations {demos}/{n_demo}" if (n_demo := sum("demonstration" in r or "decoder_failure" in r
                                                                       for r in reject)) else ""))
    for f in fails:
        print("  FAIL", f)
    return bool(fails)


if __name__ == "__main__":
    main()
