#!/usr/bin/env python3
"""P8 golden and rejection vectors for profile tessera-v1-strict (implementation A).

Encoding: formal/p8/ENCODING-V1.md. Proof: formal/p8/PROOF.md.

Uses only the Python standard library plus the `rfc8785` package (Trail of Bits), and none of
prototype/. It is implementation A: it encodes every golden vector, builds every rejection vector by
mutation, and checks with its own decoder that each golden vector decodes and each rejection vector is
rejected with its expected reason code. check.py is implementation B, written separately.

Revision 2026-10-12 (CODEX-REVIEW findings 4, 5, 6, 9, 10): the receipt anchor is A_sig, which commits
each slot's exact detached signature. A also makes real ECDSA P-256 signatures (RFC 6979 nonces, test keys
d = 1 and d = 2) in OpenPGP v4 packets for the signature, anchor, receipt and negative-control vectors.
For that it uses hmac (RFC 6979) and SHA-1 (only to fill OpenPGP's issuer-fingerprint subpacket, which no
V1 check reads).

Hybrid supplement (2026-10-14, formal/p8/HYBRID-SUPPLEMENT-DRAFT.md, OWNER-PROPOSED): rule R under the pair
id KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256. A carries its own ML-DSA-65 (FIPS 204: KeyGen, Sign from
the message or from an external mu, Verify; butterfly NTT), checked by hand against dilithium-py 1.4.0 and
cryptography 50.0.2 (identical public key and deterministic signature from one seed). The hybrid vectors go
to hybrid-golden.json and hybrid-reject.json; golden.json and reject.json stay byte-identical to the
2026-10-12 baseline. The hybrid section reads the real captures in prototype/spike-pq/out-kms/ and out-gcp/.

Run:  uv run --no-project --with rfc8785==0.1.4 python formal/p8/vectors/gen.py
Writes golden.json, reject.json, hybrid-golden.json and hybrid-reject.json next to this file. Output is
deterministic.
"""
import datetime
import decimal
import hashlib
import hmac
import json
import os
import re
import struct
import sys
import unicodedata

import rfc8785

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


def decode_anchor(b):
    """A_sig -> [(F_kms, S_kms), (F_gpg, S_gpg)], exact bytes, manifest slot order."""
    r = _Reader(b)
    _read_header(r, T_ANCHOR)
    if r.take(1)[0] != 2:
        raise Reject("ANCHOR_COUNT", "V1 anchors exactly two slots")
    slots = []
    for slot in range(2):
        n = int.from_bytes(r.take(4), "big")
        if n > MAX_PAYLOAD + 64:
            raise Reject("LENGTH_CAP", str(n))
        f = r.take(n)
        alg = decode_frame(f, T_ATTEST)["common"]["alg"]
        n = int.from_bytes(r.take(4), "big")
        if n == 0:
            raise Reject("SIG_EMPTY", "empty signature")
        if n > sig_cap(alg, slot):
            raise Reject("LENGTH_CAP", f"signature length {n}")
        s = decode_sig(r.take(n), alg, slot)
        slots.append((f, s))
    if r.rest():
        raise Reject("TRAILING", "bytes after the second signature")
    return slots


def decode_snapshot(b):
    r = _Reader(b)
    _read_header(r, T_SNAPSHOT)
    n = int.from_bytes(r.take(4), "big")
    if n > MAX_PAYLOAD:
        raise Reject("LENGTH_CAP", str(n))
    if n == 0:
        raise Reject("SCHEMA", "empty snapshot")
    if r.rest() < n:
        raise Reject("TRUNCATED", "snapshot shorter than its length prefix")
    if r.rest() > n:
        raise Reject("TRAILING", "bytes after the snapshot")
    return r.take(n)


def check_receipt(fm, f0, s0, f1, s1, anchor, keys=None):
    """Codec checks, then (when keys are given) signature verification over the bytes the anchor commits.
    keys = ((x, y) of the kms point, (x, y, created) of the gpg point)."""
    m = decode_frame(fm, T_MANIFEST)
    a0 = decode_frame(f0, T_ATTEST)
    a1 = decode_frame(f1, T_ATTEST)
    if a0["signer"]["key_fp"] != m["key_fp"] or a1["signer"]["key_fp"] != m["sset"][0]:
        raise Reject("RECEIPT_SLOT", "a frame's fingerprint is not its slot's manifest fingerprint")
    if jcs(a0["common"]) != jcs(a1["common"]):
        raise Reject("RECEIPT_COMMON_MISMATCH", "the two frames bind different common bytes")
    c = a0["common"]
    if c["manifest_sha256"] != hashlib.sha256(fm).hexdigest() or c["issuer"] != m["issuer"] or c["alg"] != m["alg"]:
        raise Reject("RECEIPT_MANIFEST_MISMATCH", "common does not match the manifest frame")
    committed = decode_anchor(anchor)
    if committed != [(f0, s0), (f1, s1)]:
        raise Reject("RECEIPT_ANCHOR_MISMATCH", "anchor preimage is not over these frames and signatures in slot order")
    if keys is not None:
        if c["alg"] not in SIG_RULES:
            raise Reject("UNVERIFIABLE", "stage (c): algorithm id not registered for this profile")
        kms_key, (gx, gy, created) = keys
        if c["alg"] == ALG_HYBRID:                   # kms key: the exact ML-DSA-65 SPKI DER (hybrid supplement)
            kq = decode_spki_mldsa65(kms_key)
            kfp = fp_spki(kms_key)
        else:
            kq = kms_key
            kfp = fp_kms(_point(*kms_key))
        if kfp != m["key_fp"] or fp_gpg(_point(gx, gy), created) != m["sset"][0]:
            raise Reject("KEY_MISMATCH", "a public key does not have its slot's manifest fingerprint")
        for slot, ((f, s), q) in enumerate(zip(committed, (kq, (gx, gy)))):   # the committed bytes only
            if not verify_slot(c["alg"], slot, f, s, q):
                raise Reject("SIG_INVALID", "signature does not verify over its frame under its slot key")
    return c


# ---- hybrid supplement: the kms slot's ML-DSA-65 key, and slot verification by rule ----------------
# SubjectPublicKeyInfo DER for ML-DSA-65: SEQUENCE { SEQUENCE { OID 2.16.840.1.101.3.4.3.18 } (parameters
# absent), BIT STRING { 0 unused bits, the 1952-byte FIPS 204 public key } }. 22 fixed bytes, then the key.
SPKI_MLDSA65_PREFIX = bytes.fromhex("308207b2300b0609608648016503040312038207a100")


def decode_spki_mldsa65(der):
    """The exact DER SPKI or KEY_FORMAT. DER is a single encoding, so 'exact' is a prefix-and-length test."""
    if len(der) != len(SPKI_MLDSA65_PREFIX) + MLDSA65_PK_LEN or der[:len(SPKI_MLDSA65_PREFIX)] != SPKI_MLDSA65_PREFIX:
        raise Reject("KEY_FORMAT", "not the DER SubjectPublicKeyInfo of an ML-DSA-65 public key")
    return der[len(SPKI_MLDSA65_PREFIX):]


def fp_spki(der):
    return "spki-sha256:" + hashlib.sha256(der).hexdigest()


def verify_slot(alg, slot, msg, sig, key):
    """key: the raw ML-DSA-65 public key for rule R; the (x, y) point for rule O."""
    if sig_rule(alg, slot) == "raw-mldsa65-pure":
        return mldsa65_verify(key, msg, sig)
    return verify_openpgp4(msg, sig, key)


def slot_key(alg, slot, key, manifest):
    """KEY_FORMAT, then KEY_MISMATCH against the slot's manifest fingerprint. Returns the verification key."""
    want = manifest["key_fp"] if slot == 0 else manifest["sset"][0]
    if slot == 0 and alg == ALG_HYBRID:
        q, fp = decode_spki_mldsa65(key), fp_spki(key)
    elif slot == 0:
        q, fp = key, fp_kms(_point(*key))
    else:
        q, fp = key[:2], fp_gpg(_point(key[0], key[1]), key[2])
    if fp != want:
        raise Reject("KEY_MISMATCH", "the key does not have its slot's manifest fingerprint")
    return q


def check_possession(fm, slot, sig, key):
    """A slot's manifest-possession signature (R-3.38): the slot's own rule over F_manifest. Order: manifest
    codec; key format and fingerprint (registered id only); signature codec; stage (c); verification."""
    m = decode_frame(fm, T_MANIFEST)
    alg = m["alg"]
    q = slot_key(alg, slot, key, m) if alg in SIG_RULES else None
    decode_sig(sig, alg, slot)
    if alg not in SIG_RULES:
        raise Reject("UNVERIFIABLE", "stage (c): algorithm id not registered for this profile")
    if not verify_slot(alg, slot, fm, sig, q):
        raise Reject("POSSESSION_INVALID", "possession signature does not verify over the manifest frame")
    return m


def check_signature_r(msg, sig, spki):
    """One rule-R signature on its own: codec, key format, verification (used for the real KMS captures)."""
    decode_sig(sig, ALG_HYBRID, 0)
    if not mldsa65_verify(decode_spki_mldsa65(spki), msg, sig):
        raise Reject("SIG_INVALID", "ML-DSA-65 signature does not verify")


def check_key_kms(spki, key_fp):
    """The kms slot's transported key under the hybrid id: KEY_FORMAT, then KEY_MISMATCH."""
    decode_spki_mldsa65(spki)
    if fp_spki(spki) != key_fp:
        raise Reject("KEY_MISMATCH", "the key does not have the kms slot's fingerprint")


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


# --------------------------------------------------------------------------------------------------
# Real signatures for the vectors: ECDSA P-256 (FIPS 186-5) with RFC 6979 nonces, in OpenPGP v4
# signature packets (RFC 9580 §5.2.3, §5.2.4). The test keys are d = 1 (point G, slot kms) and d = 2
# (point 2G, slot gpg): public, ILLUSTRATIVE, matching K-01 and K-02. Not part of the P8 codec.
# --------------------------------------------------------------------------------------------------
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


def _add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return None
        return _double(x1, y1)
    lam = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (lam * lam - x1 - x2) % P
    return x3, (lam * (x1 - x3) - y1) % P


def _mul(k, pt):
    acc = None
    for bit in bin(k)[2:]:
        acc = _add(acc, acc)
        if bit == "1":
            acc = _add(acc, pt)
    return acc


def rfc6979_k(d, h, extra=b""):
    """RFC 6979 §3.2 with HMAC-SHA-256; `extra` is §3.6 additional data."""
    x, hb = d.to_bytes(32, "big"), (int.from_bytes(h, "big") % N).to_bytes(32, "big")
    v, k = b"\x01" * 32, b"\x00" * 32
    k = hmac.new(k, v + b"\x00" + x + hb + extra, "sha256").digest()
    v = hmac.new(k, v, "sha256").digest()
    k = hmac.new(k, v + b"\x01" + x + hb + extra, "sha256").digest()
    v = hmac.new(k, v, "sha256").digest()
    while True:
        v = hmac.new(k, v, "sha256").digest()
        cand = int.from_bytes(v, "big")
        if 1 <= cand < N:
            return cand
        k = hmac.new(k, v + b"\x00", "sha256").digest()
        v = hmac.new(k, v, "sha256").digest()


def ecdsa_sign(d, h, extra=b""):
    k = rfc6979_k(d, h, extra)
    r = _mul(k, (GX, GY))[0] % N
    s = pow(k, -1, N) * (int.from_bytes(h, "big") + r * d) % N
    assert r and s
    return r, s


def ecdsa_verify(q, h, r, s):
    if not (1 <= r < N and 1 <= s < N):
        return False
    w = pow(s, -1, N)
    pt = _add(_mul(int.from_bytes(h, "big") * w % N, (GX, GY)), _mul(r * w % N, q))
    return pt is not None and pt[0] % N == r


# RFC 6979 Appendix A.2.5 (P-256, SHA-256, message "sample") pins the nonce derivation.
_X6979 = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
assert rfc6979_k(_X6979, hashlib.sha256(b"sample").digest()) == \
    0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60


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


def openpgp_sign(frame_bytes, d, pt, key_created, sig_created, extra=b""):
    """A detached v4 binary-document (type 0x00) signature, laid out as GnuPG 2.4.4 lays it out:
    hashed {issuer fingerprint (33), creation time (2)}, unhashed {issuer key ID (16)}.
    The issuer fingerprint is OpenPGP's own SHA-1 v4 fingerprint: interop metadata that no V1 check
    reads (V1 binds keys by the slot fingerprints of §3.3)."""
    fpr = hashlib.sha1(b"\x99" + struct.pack(">H", len(openpgp_v4_body(pt, key_created)))
                       + openpgp_v4_body(pt, key_created)).digest()
    hashed = _subpacket(33, b"\x04" + fpr) + _subpacket(2, struct.pack(">I", sig_created))
    unhashed = _subpacket(16, fpr[-8:])
    h = openpgp_v4_sig_digest(frame_bytes, hashed)
    r, s = ecdsa_sign(d, h, extra)
    return openpgp_v4_sig_packet(hashed, unhashed, h[:2], r, s)


def verify_openpgp4(frame_bytes, sig, q):
    """ECDSA verification of one committed signature packet over one frame. The left-16 field is not
    signed and is not consulted."""
    hashed, r, s = decode_sig_openpgp4(sig)
    return ecdsa_verify(q, openpgp_v4_sig_digest(frame_bytes, hashed), r, s)


# --------------------------------------------------------------------------------------------------
# ML-DSA-65 (FIPS 204), implementation A: key generation, signing (deterministic and hedged) and
# verification, pure ML-DSA with an empty context only. Used to make and check the rule-R vectors
# (HYBRID-SUPPLEMENT-DRAFT.md). Butterfly NTT (FIPS 204 Algorithms 41/42); big-integer bit packing.
# Not part of the P8 codec: the codec only fixes rule R's byte length (ENCODING-V1 §5.2).
# --------------------------------------------------------------------------------------------------
MLDSA_Q = 8380417
MLDSA_D = 13
MLDSA_K, MLDSA_L, MLDSA_ETA, MLDSA_TAU, MLDSA_LAMBDA, MLDSA_OMEGA = 6, 5, 4, 49, 192, 55
MLDSA_G1 = 1 << 19
MLDSA_G2 = (MLDSA_Q - 1) // 32
MLDSA_BETA = MLDSA_TAU * MLDSA_ETA
MLDSA65_PK_LEN = 32 + 32 * 10 * MLDSA_K                                                  # 1952
MLDSA65_SIG_LEN = MLDSA_LAMBDA // 4 + 32 * 20 * MLDSA_L + MLDSA_OMEGA + MLDSA_K           # 3309
_MLDSA_ZETAS = [pow(1753, int(f"{i:08b}"[::-1], 2), MLDSA_Q) for i in range(256)]


def _mldsa_h(data, n):
    return hashlib.shake_256(data).digest(n)


def _ntt(w):
    w, m, ln = list(w), 0, 128
    while ln >= 1:
        for start in range(0, 256, 2 * ln):
            m += 1
            z = _MLDSA_ZETAS[m]
            for j in range(start, start + ln):
                t = z * w[j + ln] % MLDSA_Q
                w[j + ln] = (w[j] - t) % MLDSA_Q
                w[j] = (w[j] + t) % MLDSA_Q
        ln //= 2
    return w


def _intt(w):
    w, m, ln = list(w), 256, 1
    while ln < 256:
        for start in range(0, 256, 2 * ln):
            m -= 1
            z = MLDSA_Q - _MLDSA_ZETAS[m]
            for j in range(start, start + ln):
                t = w[j]
                w[j] = (t + w[j + ln]) % MLDSA_Q
                w[j + ln] = z * (t - w[j + ln]) % MLDSA_Q
        ln *= 2
    return [x * 8347681 % MLDSA_Q for x in w]


def _pmul(a, b):
    return [x * y % MLDSA_Q for x, y in zip(a, b)]


def _padd(a, b):
    return [(x + y) % MLDSA_Q for x, y in zip(a, b)]


def _psub(a, b):
    return [(x - y) % MLDSA_Q for x, y in zip(a, b)]


def _centered(r, alpha):
    r %= alpha
    return r - alpha if r > alpha // 2 else r


def _inf_norm(vec):
    return max(abs(_centered(x, MLDSA_Q)) for p in vec for x in p)


def _pack(coeffs, bits):
    acc = 0
    for i, c in enumerate(coeffs):
        acc |= c << (bits * i)
    return acc.to_bytes(32 * bits, "little")


def _unpack(b, bits):
    acc, mask = int.from_bytes(b, "little"), (1 << bits) - 1
    return [(acc >> (bits * i)) & mask for i in range(256)]


def _rej_ntt_poly(seed):
    n = 894
    while True:
        buf, out = hashlib.shake_128(seed).digest(n), []
        for i in range(0, n - 2, 3):
            v = buf[i] | buf[i + 1] << 8 | (buf[i + 2] & 0x7F) << 16
            if v < MLDSA_Q:
                out.append(v)
                if len(out) == 256:
                    return out
        n *= 2


def _rej_bounded_poly(seed):
    n = 272
    while True:
        buf, out = hashlib.shake_256(seed).digest(n), []
        for byte in buf:
            for half in (byte & 15, byte >> 4):
                if half < 9:
                    out.append((MLDSA_ETA - half) % MLDSA_Q)
                    if len(out) == 256:
                        return out
        n *= 2


def _expand_a(rho):
    return [[_rej_ntt_poly(rho + bytes([s, r])) for s in range(MLDSA_L)] for r in range(MLDSA_K)]


def _mat_vec_ntt(a_hat, v_hat):
    out = []
    for row in a_hat:
        acc = [0] * 256
        for a, v in zip(row, v_hat):
            acc = _padd(acc, _pmul(a, v))
        out.append(acc)
    return out


def _sample_in_ball(c_tilde):
    n = 8 + 272
    while True:
        buf = hashlib.shake_256(c_tilde).digest(n)
        signs, pos, c, ok = int.from_bytes(buf[:8], "little"), 8, [0] * 256, True
        for i in range(256 - MLDSA_TAU, 256):
            while pos < n and buf[pos] > i:
                pos += 1
            if pos >= n:
                ok = False
                break
            j = buf[pos]
            pos += 1
            c[i] = c[j]
            c[j] = MLDSA_Q - 1 if (signs >> (i + MLDSA_TAU - 256)) & 1 else 1
        if ok:
            return c
        n *= 2


def _decompose(r):
    r %= MLDSA_Q
    r0 = _centered(r, 2 * MLDSA_G2)
    if r - r0 == MLDSA_Q - 1:
        return 0, r0 - 1
    return (r - r0) // (2 * MLDSA_G2), r0


def _high_bits(p):
    return [_decompose(x)[0] for x in p]


def _w1_encode(w1):
    return b"".join(_pack(p, 4) for p in w1)


def _use_hint(hint, r):
    r1, r0 = _decompose(r)
    if not hint:
        return r1
    return (r1 + 1) % 16 if r0 > 0 else (r1 - 1) % 16


def mldsa65_keygen(xi):
    """FIPS 204 ML-DSA.KeyGen_internal for ML-DSA-65 from a 32-byte seed. Returns (pk bytes, private state)."""
    seed = _mldsa_h(xi + bytes([MLDSA_K, MLDSA_L]), 128)
    rho, rho_p, key = seed[:32], seed[32:96], seed[96:]
    a_hat = _expand_a(rho)
    s1 = [_rej_bounded_poly(rho_p + r.to_bytes(2, "little")) for r in range(MLDSA_L)]
    s2 = [_rej_bounded_poly(rho_p + (r + MLDSA_L).to_bytes(2, "little")) for r in range(MLDSA_K)]
    t = [_padd(_intt(x), e) for x, e in zip(_mat_vec_ntt(a_hat, [_ntt(p) for p in s1]), s2)]
    t1, t0 = [], []
    for p in t:
        lo = [_centered(x, 1 << MLDSA_D) for x in p]
        t1.append([(x - y) >> MLDSA_D for x, y in zip(p, lo)])
        t0.append([y % MLDSA_Q for y in lo])
    pk = rho + b"".join(_pack(p, 10) for p in t1)
    return pk, (a_hat, s1, s2, t0, key, _mldsa_h(pk, 64))


def mldsa65_sign(priv, message, rnd=bytes(32)):
    """Pure ML-DSA-65, empty context (FIPS 204 Algorithm 2 with ctx = empty, then Algorithm 7).
    rnd = 32 zero bytes is FIPS 204's deterministic variant."""
    return mldsa65_sign_mu(priv, _mldsa_h(priv[5] + b"\x00\x00" + message, 64), rnd)


def mldsa65_sign_mu(priv, mu, rnd=bytes(32), _large_z=False):
    """FIPS 204 Algorithm 7 from a precomputed mu: what KMS does with MessageType EXTERNAL_MU. The issuer
    computes mu = mldsa65_external_mu(pk, frame); the output is an ordinary pure ML-DSA signature.
    _large_z (vectors only): return the first iteration whose z FAILS the infinity-norm bound while every
    other check passes, so that a rejection vector isolates the verifier's norm check."""
    a_hat, s1, s2, t0, key, tr = priv
    rho_pp = _mldsa_h(key + rnd + mu, 64)
    s1_hat, s2_hat, t0_hat = [_ntt(p) for p in s1], [_ntt(p) for p in s2], [_ntt(p) for p in t0]
    kappa = 0
    while True:
        y = []
        for r in range(MLDSA_L):
            v = _unpack(_mldsa_h(rho_pp + (kappa + r).to_bytes(2, "little"), 640), 20)
            y.append([(MLDSA_G1 - x) % MLDSA_Q for x in v])
        kappa += MLDSA_L
        w = [_intt(p) for p in _mat_vec_ntt(a_hat, [_ntt(p) for p in y])]
        c_tilde = _mldsa_h(mu + _w1_encode([_high_bits(p) for p in w]), MLDSA_LAMBDA // 4)
        c_hat = _ntt(_sample_in_ball(c_tilde))
        cs1 = [_intt(_pmul(c_hat, p)) for p in s1_hat]
        cs2 = [_intt(_pmul(c_hat, p)) for p in s2_hat]
        z = [_padd(a, b) for a, b in zip(y, cs1)]
        w_cs2 = [_psub(a, b) for a, b in zip(w, cs2)]
        if (_inf_norm(z) >= MLDSA_G1 - MLDSA_BETA) != _large_z:
            continue
        if max(abs(_decompose(x)[1]) for p in w_cs2 for x in p) >= MLDSA_G2 - MLDSA_BETA:
            continue
        ct0 = [_intt(_pmul(c_hat, p)) for p in t0_hat]
        if _inf_norm(ct0) >= MLDSA_G2:
            continue
        # MakeHint(-ct0, w - cs2 + ct0): r = w - cs2 + ct0, and HighBits(r) vs HighBits(r - ct0) = HighBits(w - cs2)
        hints = [[int(_decompose((a + ct) % MLDSA_Q)[0] != _decompose(a)[0]) for a, ct in zip(wc, ctp)]
                 for wc, ctp in zip(w_cs2, ct0)]
        if sum(map(sum, hints)) > MLDSA_OMEGA:
            continue
        hpack, idx = bytearray(MLDSA_OMEGA + MLDSA_K), 0
        for i, hp in enumerate(hints):
            for j, bit in enumerate(hp):
                if bit:
                    hpack[idx] = j
                    idx += 1
            hpack[MLDSA_OMEGA + i] = idx
        zpack = b"".join(_pack([(MLDSA_G1 - _centered(x, MLDSA_Q)) for x in p], 20) for p in z)
        return c_tilde + zpack + bytes(hpack)


def mldsa65_verify(pk, message, sig, _off=()):
    """Pure ML-DSA-65, empty context (FIPS 204 Algorithm 3 with ctx = empty, then Algorithm 8)."""
    return mldsa65_verify_mu(pk, _mldsa_h(_mldsa_h(pk, 64) + b"\x00\x00" + message, 64), sig, _off)


def mldsa65_verify_mu(pk, mu, sig, _off=()):
    """FIPS 204 Algorithm 8 from mu. _off (vector self-checks only) disables named gates, to show that a vector
    fails on that gate alone: "norm" (z bound), "order" (strictly increasing hint indices within a polynomial),
    "padding" (zero hint padding). The count gates (cumulative counts nondecreasing and at most omega) are
    never disabled: without them the hint field cannot be decoded at all."""
    if len(pk) != MLDSA65_PK_LEN or len(sig) != MLDSA65_SIG_LEN:
        return False
    rho, t1 = pk[:32], [_unpack(pk[32 + 320 * i:352 + 320 * i], 10) for i in range(MLDSA_K)]
    c_tilde, zb, hb = sig[:48], sig[48:48 + 3200], sig[48 + 3200:]
    z = [[(MLDSA_G1 - x) % MLDSA_Q for x in _unpack(zb[640 * i:640 * (i + 1)], 20)] for i in range(MLDSA_L)]
    hints, idx = [], 0                                       # HintBitUnpack (FIPS 204 Algorithm 21)
    for i in range(MLDSA_K):
        hp, end = [0] * 256, hb[MLDSA_OMEGA + i]
        if end < idx or end > MLDSA_OMEGA:
            return False
        first = idx
        while idx < end:
            if "order" not in _off and idx > first and hb[idx - 1] >= hb[idx]:
                return False
            hp[hb[idx]] = 1
            idx += 1
        hints.append(hp)
    if "padding" not in _off and any(hb[idx:MLDSA_OMEGA]):
        return False
    if "norm" not in _off and _inf_norm(z) >= MLDSA_G1 - MLDSA_BETA:
        return False
    c_hat = _ntt(_sample_in_ball(c_tilde))
    az = _mat_vec_ntt(_expand_a(rho), [_ntt(p) for p in z])
    w_approx = [_intt(_psub(a, _pmul(c_hat, _ntt([(x << MLDSA_D) % MLDSA_Q for x in t])))) for a, t in zip(az, t1)]
    w1 = [[_use_hint(h, r) for h, r in zip(hp, wp)] for hp, wp in zip(hints, w_approx)]
    return _mldsa_h(mu + _w1_encode(w1), 48) == c_tilde


def mldsa65_external_mu(pk, message):
    """FIPS 204 external mu for pure ML-DSA with an empty context: what the issuer sends KMS as EXTERNAL_MU."""
    return _mldsa_h(_mldsa_h(pk, 64) + b"\x00\x00" + message, 64)


# --------------------------------------------------------------------------------------------------
# DNS key-publication record (ENCODING-V1.md §7)
# --------------------------------------------------------------------------------------------------
DNS_LABEL = "_tessera-v1"
NB, NA = "issuance-not-before", "issuance-not-after"     # ENCODING-V1 §7, §7.1 (2026-10-12)
DNS_KEYS = ("v", "profile", "kms", "gpg", NB, NA)
WINDOW_MAX_SECONDS = 90 * 86400                           # A9 (2026-10-12): not-after - not-before <= 90 days


def dns_name_wire(name):
    out = b""
    for lb in name.split("."):
        out += bytes([len(lb)]) + lb.encode("ascii")
    return out + b"\x00"


def dns_value(kms_hex, gpg_hex, not_after, not_before=None):
    s = f"v=tessera1;profile={PROFILE};kms={kms_hex};gpg={gpg_hex}"
    if not_before is not None:
        s += f";{NB}={not_before}"
    return s + f";{NA}={not_after}"


def utc_seconds(t):
    """A valid_time() string -> seconds since 1970-01-01T00:00:00Z."""
    return int(datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp())


def check_issuance_window(record, declared_issue_time, t_anchor):
    """C4 window rule (ENCODING-V1 §7.1). record: a decode_dns() result. t_anchor: T, the header-time-derived
    time of the earliest verified attestation in the presented OTS proof, as registered (integer Unix seconds)."""
    if utc_seconds(declared_issue_time) < utc_seconds(record[NB]):
        raise Reject("ISSUANCE_WINDOW", "declared issue time before issuance-not-before")
    if t_anchor > utc_seconds(record[NA]):
        raise Reject("ISSUANCE_WINDOW", "T after issuance-not-after")


def dns_rdata(*strings):
    out = b""
    for s in strings:
        b = s.encode("ascii") if isinstance(s, str) else s
        assert len(b) <= 255
        out += bytes([len(b)]) + b
    return out


def _wire_labels(w):
    labels, i = [], 0
    while True:
        if i >= len(w):
            raise Reject("DNS_OWNER", "unterminated name")
        n = w[i]
        if n == 0:
            if i + 1 != len(w):
                raise Reject("DNS_OWNER", "bytes after the root label")
            return labels
        if n > 63 or i + 1 + n > len(w):
            raise Reject("DNS_OWNER", "bad label length")
        labels.append(w[i + 1:i + 1 + n])
        i += 1 + n


def decode_dns(domain, owner_wire, rrset):
    labels = [lb.lower() for lb in _wire_labels(owner_wire)]
    want = [DNS_LABEL.encode()] + [lb.encode() for lb in domain.split(".")]
    if labels != want:
        raise Reject("DNS_OWNER", "owner name is not _tessera-v1.<D>")
    if len(rrset) != 1:
        raise Reject("DNS_RRSET", f"{len(rrset)} TXT records at the owner name")
    rd, strings, i = rrset[0], [], 0
    while i < len(rd):
        n = rd[i]
        if i + 1 + n > len(rd):
            raise Reject("DNS_RDATA", "character-string runs past RDATA")
        strings.append(rd[i + 1:i + 1 + n])
        i += 1 + n
    if len(strings) != 1:
        raise Reject("DNS_STRINGS", f"{len(strings)} character-strings")
    raw = strings[0]
    if not raw or any(c < 0x21 or c > 0x7E for c in raw):
        raise Reject("DNS_SYNTAX", "value must be printable ASCII without spaces")
    fields = []
    for f in raw.decode("ascii").split(";"):
        m = re.fullmatch(r"([a-z][a-z-]*)=([^=]+)", f)
        if not m:
            raise Reject("DNS_SYNTAX", f"bad field {f!r}")
        fields.append(m.groups())
    if fields[0] != ("v", "tessera1") or any(k == "v" for k, _ in fields[1:]):
        raise Reject("DNS_VERSION", "first field must be v=tessera1")
    keys = [k for k, _ in fields]
    for k in keys:
        if k not in DNS_KEYS:
            raise Reject("DNS_FIELD_UNKNOWN", k)
    for k in keys:
        if keys.count(k) > 1:
            raise Reject("DNS_SLOT_DUPLICATE" if k in ("kms", "gpg") else "DNS_FIELD_DUPLICATE", k)
    for k in ("kms", "gpg"):
        if k not in keys:
            raise Reject("DNS_SLOT_MISSING", k)
    for k in ("profile", NB, NA):
        if k not in keys:
            raise Reject("DNS_FIELD_MISSING", k)
    if keys != ["v", "profile", "kms", "gpg", NB, NA]:
        raise Reject("DNS_ORDER", ",".join(keys))
    d = dict(fields)
    if d["profile"] != PROFILE:
        raise Reject("DNS_PROFILE", d["profile"])
    if not (re.fullmatch(r"[0-9a-f]{64}", d["kms"]) and re.fullmatch(r"[0-9a-f]{64}", d["gpg"])
            and valid_time(d[NA]) and valid_time(d[NB])):
        raise Reject("DNS_VALUE", "fingerprint or time grammar")
    if utc_seconds(d[NA]) <= utc_seconds(d[NB]):
        raise Reject("DNS_WINDOW", "issuance-not-after must be strictly later than issuance-not-before")
    if utc_seconds(d[NA]) - utc_seconds(d[NB]) > WINDOW_MAX_SECONDS:
        raise Reject("DNS_WINDOW_LENGTH", "issuance-not-after - issuance-not-before exceeds 90 days")
    return d


# --------------------------------------------------------------------------------------------------
# Vector construction
# --------------------------------------------------------------------------------------------------
def H(b):
    return b.hex()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    golden, reject = [], []

    def expect_reject(fn, code):
        try:
            fn()
        except Reject as e:
            if e.code != code:
                raise AssertionError(f"implementation A gave {e.code}, vector expects {code}")
            return
        raise AssertionError(f"implementation A accepted a vector that expects {code}")

    # ---- keys and fingerprints ----------------------------------------------------------------
    g1 = (GX, GY)
    g2 = _double(GX, GY)
    pt_kms, pt_gpg = _point(*g1), _point(*g2)
    created = int(datetime.datetime(2026, 10, 12, tzinfo=datetime.timezone.utc).timestamp())
    FP_KMS, FP_GPG = fp_kms(pt_kms), fp_gpg(pt_gpg, created)
    golden.append({"id": "K-01", "kind": "fingerprint-kms",
                   "note": "KMS slot: SHA-256 of the DER SubjectPublicKeyInfo; point = P-256 generator (illustrative)",
                   "input": {"x": f"{g1[0]:064x}", "y": f"{g1[1]:064x}"},
                   "spki_der_hex": H(spki_der(pt_kms)), "key_fp": FP_KMS})
    body = openpgp_v4_body(pt_gpg, created)
    golden.append({"id": "K-02", "kind": "fingerprint-gpg",
                   "note": "GPG slot: SHA-256 of the v4 public-key packet body (the bytes the v4 fingerprint hashes after 0x99 || u16 len); point = 2G",
                   "input": {"x": f"{g2[0]:064x}", "y": f"{g2[1]:064x}", "created": created},
                   "key_packet_body_hex": H(body), "key_fp": FP_GPG})

    # ---- canonical content (requester JSON text -> canonical bytes) -----------------------------
    content_cases = [
        ("C-01", '{"b":1,"a":[true,false,null]}', "member order by UTF-16 code units; literals"),
        ("C-02", ' { "z" : "x" ,\n\t"y":[ ] , "x" : { } } ', "insignificant whitespace removed"),
        ("C-03", '[9.8, 9.80, 1E2, 1e21, 5e-324, 123456789012345680000, 0.000001, 1e-7, 2.5e-1, -1.5, 9007199254740992]',
         "value-preserving numbers: spellings normalized, values kept"),
        ("C-04", '["\\u0041\\n\\u001F\\"\\\\\\/\\u00e9", "\\ud83d\\ude00"]', "escapes: only what RFC 8785 requires stays escaped"),
        ("C-05", '{"\\ue000":1,"\\ud83d\\ude00":2,"a":3,"\\u00e9":4}', "UTF-16 ordering puts U+1F600 before U+E000"),
        ("C-06", '"caf\\u00e9 \\u65e5\\u672c"', "NFC text; a bare string is a JSON text"),
        ("C-07", "[" * 62 + "]" * 62, "content depth 62, the maximum"),
        ("C-08", '{"cvss":9.8,"digest":"sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"}', "an SBOM-style statement"),
        ("C-09", "0", "zero"),
        ("C-10", "[0e99999999999999999999, -1.0E+0]", "zero with an extreme exponent is zero; -1.0E+0 is -1"),
    ]
    rfc_b = ["0000000000000001", "7fefffffffffffff", "4340000000000000", "4430000000000000", "44b52d02c7e14af5",
             "44b52d02c7e14af6", "44b52d02c7e14af7", "444b1ae4d6e2ef4e", "444b1ae4d6e2ef4f", "444b1ae4d6e2ef50",
             "3eb0c6f7a0b5ed8c", "3eb0c6f7a0b5ed8d", "41b3de4355555553", "41b3de4355555554", "41b3de4355555555",
             "41b3de4355555556", "41b3de4355555557", "becbf647612f3696", "43143ff3c1cb0959", "8000000000000001",
             "ffefffffffffffff", "c340000000000000"]
    for i, bits in enumerate(rfc_b, 1):
        s = rfc8785.dumps(struct.unpack(">d", bytes.fromhex(bits))[0]).decode()
        golden.append({"id": f"N-{i:02d}", "kind": "number", "note": "RFC 8785 Appendix B value",
                       "input": {"binary64_hex": bits}, "string": s})
        content_cases.append((f"C-N{i:02d}", s, f"RFC 8785 Appendix B {bits} as a literal"))
    for cid, text, note in content_cases:
        data = text.encode("utf-8")
        golden.append({"id": cid, "kind": "content", "note": note, "input": {"text_hex": H(data)},
                       "bytes_hex": H(jcs(ingest(data)))})

    # ---- frames ---------------------------------------------------------------------------------
    D = "wamason.com"
    ALG = "OPENPGP4-ECDSA-P256-SHA256"
    spec_bytes = b"ILLUSTRATIVE: tessera-v1-strict verification specification bytes\n"
    vec_bytes = b"ILLUSTRATIVE: tessera-v1-strict conformance vector bytes\n"
    pre_bytes = b"ILLUSTRATIVE: purpose preamble bytes\n"
    fm = encode_manifest(ALG, D, FP_KMS, FP_GPG)
    golden.append({"id": "M-01", "kind": "frame-manifest", "note": "map-v1 tuple: kms slot in key_fp, gpg slot in sset",
                   "input": {"alg": ALG, "issuer": D, "key_fp": FP_KMS, "sset": [FP_GPG]},
                   "bytes_hex": H(fm), "sha256": sha(fm)})
    content_text = '{"statement":"sbom","name":"caf\\u00e9","cvss":9.8,"digest":"sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"}'

    def common(content_text=content_text, alg=ALG, forms=("STMT_DIRECT",), mh=None, issuer=D):
        return {
            "alg": alg, "binding_forms": list(forms), "content": ingest(content_text.encode()),
            "declared_issue_time": "2026-10-12T14:03:07Z", "issuer": issuer,
            "manifest_sha256": mh or sha(fm), "preamble_sha256": sha(pre_bytes), "profile": PROFILE,
            "spec": {"id": "tessera-v1-strict/verification-spec/1", "sha256": sha(spec_bytes)},
            "vectors_sha256": sha(vec_bytes),
        }

    def common_input(c, content_text):
        d = {k: v for k, v in c.items() if k != "content"}
        d["content_text_hex"] = H(content_text.encode())
        return d

    C0 = common()
    f0 = encode_attest(C0, FP_KMS)
    f1 = encode_attest(C0, FP_GPG)
    golden.append({"id": "F-01", "kind": "frame-attest", "note": "slot kms",
                   "input": {"common": common_input(C0, content_text), "key_fp": FP_KMS}, "bytes_hex": H(f0), "sha256": sha(f0)})
    golden.append({"id": "F-02", "kind": "frame-attest", "note": "slot gpg; equal to F-01 outside the signer member",
                   "input": {"common": common_input(C0, content_text), "key_fp": FP_GPG}, "bytes_hex": H(f1), "sha256": sha(f1)})
    canary_text = '"sha256:2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"'
    C1 = common(canary_text, alg="X-UNKNOWN-ALG-1", forms=("STMT_DIGEST", "STMT_DIRECT"))
    f_can = encode_attest(C1, FP_KMS)
    golden.append({"id": "F-03", "kind": "frame-attest",
                   "note": "well-formed unknown algorithm id: P8 accepts; stage (c) decides UNVERIFIABLE (canary)",
                   "input": {"common": common_input(C1, canary_text), "key_fp": FP_KMS}, "bytes_hex": H(f_can), "sha256": sha(f_can)})
    # ---- signatures: real ECDSA P-256 over the frames (test keys d = 1 and d = 2, ILLUSTRATIVE) --------
    sig_created = int(datetime.datetime(2026, 10, 12, 14, 3, 7, tzinfo=datetime.timezone.utc).timestamp())
    KEYS = (g1, (g2[0], g2[1], created))
    keys_input = {"kms": {"x": f"{g1[0]:064x}", "y": f"{g1[1]:064x}"},
                  "gpg": {"x": f"{g2[0]:064x}", "y": f"{g2[1]:064x}", "created": created}}

    def sign_kms(f, extra=b"", when=sig_created):
        return openpgp_sign(f, 1, pt_kms, created, when, extra)

    def sign_gpg(f, extra=b"", when=sig_created):
        return openpgp_sign(f, 2, pt_gpg, created, when, extra)

    s0, s1 = sign_kms(f0), sign_gpg(f1)
    for gid, slot, f, s, q, note in [
            ("SIG-01", "kms", f0, s0, g1, "slot kms over F-01, key d = 1 (point G); RFC 6979 nonce"),
            ("SIG-02", "gpg", f1, s1, g2, "slot gpg over F-02, key d = 2 (point 2G); RFC 6979 nonce")]:
        assert verify_openpgp4(f, s, q)
        golden.append({"id": gid, "kind": "signature", "note": note + "; one v4 type-0x00 packet, legacy header 0x88",
                       "input": {"frame_hex": H(f), "slot": slot, "alg": ALG, "x": f"{q[0]:064x}", "y": f"{q[1]:064x}"},
                       "bytes_hex": H(s), "verifies": True})
    anc = encode_anchor(f0, s0, f1, s1)
    golden.append({"id": "A-01", "kind": "anchor",
                   "note": "receipt-anchor preimage A_sig over (F-01, SIG-01, F-02, SIG-02); OTS stamps its SHA-256",
                   "input": {"f0_hex": H(f0), "s0_hex": H(s0), "f1_hex": H(f1), "s1_hex": H(s1)},
                   "bytes_hex": H(anc), "sha256": sha(anc)})
    f_can_gpg = encode_attest(C1, FP_GPG)
    sc0, sc1 = b"ILLUSTRATIVE opaque signature bytes, slot kms", b"ILLUSTRATIVE opaque signature bytes, slot gpg"
    anc_can = encode_anchor(f_can, sc0, f_can_gpg, sc1)
    golden.append({"id": "A-02", "kind": "anchor",
                   "note": "canary: unregistered alg id; each signature is opaque (1 to 65536 bytes); stage (c) decides UNVERIFIABLE",
                   "input": {"f0_hex": H(f_can), "s0_hex": H(sc0), "f1_hex": H(f_can_gpg), "s1_hex": H(sc1)},
                   "bytes_hex": H(anc_can), "sha256": sha(anc_can)})
    snap = b"ILLUSTRATIVE DNSSEC snapshot bytes (format fixed by the profile document, not by P8)"
    sp = encode_snapshot(snap)
    golden.append({"id": "S-01", "kind": "snapshot", "input": {"snapshot_hex": H(snap)}, "bytes_hex": H(sp), "sha256": sha(sp)})
    golden.append({"id": "R-01", "kind": "receipt",
                   "note": "manifest + both (frame, signature) slots + anchor preimage; codec checks pass and both "
                           "committed signatures verify under the slot keys",
                   "input": {"manifest_hex": H(fm), "f0_hex": H(f0), "s0_hex": H(s0), "f1_hex": H(f1), "s1_hex": H(s1),
                             "anchor_hex": H(anc), "keys": keys_input},
                   "anchor_sha256": sha(anc)})

    # ---- DNS key-publication record ----------------------------------------------------------------
    kms_hex, gpg_hex = FP_KMS.split(":")[1], FP_GPG.split(":")[1]
    owner = dns_name_wire(f"{DNS_LABEL}.{D}")
    # ILLUSTRATIVE issuance window of exactly 90 days (the A9 maximum); NA30 is a 30-day window.
    NB0, NA0, NA30 = "2026-10-12T00:00:00Z", "2027-01-10T00:00:00Z", "2026-11-11T00:00:00Z"
    assert utc_seconds(NA0) - utc_seconds(NB0) == WINDOW_MAX_SECONDS
    for gid, na, own, note in [("DNS-01", NA30, owner, "a 30-day window (shorter than the 90-day maximum)"),
                               ("DNS-02", NA0, owner, "a window of exactly 90 days: accepted (the bound is inclusive); "
                                                      "255 bytes, the length of every canonical value"),
                               ("DNS-03", NA0, dns_name_wire("_TESSERA-V1.WaMaSoN.com"), "owner name compared case-insensitively")]:
        val = dns_value(kms_hex, gpg_hex, na, NB0)
        rd = dns_rdata(val)
        decode_dns(D, own, [rd])
        golden.append({"id": gid, "kind": "dns", "note": note,
                       "input": {"D": D, "kms": kms_hex, "gpg": gpg_hex, "issuance_not_before": NB0,
                                 "issuance_not_after": na},
                       "owner_hex": H(own), "rdata_hex": [H(rd)], "value": val})
        assert len(val) == 255

    # ---- issuance window (C4 rule over the record, the declared time and T) -------------------------
    rd_win = dns_rdata(dns_value(kms_hex, gpg_hex, NA0, NB0))
    T_NA = utc_seconds(NA0)

    def win_input(declared, t):
        return {"D": D, "owner_hex": H(owner), "rdata_hex": [H(rd_win)], "declared_issue_time": declared, "t_anchor": t}

    for gid, declared, t, note in [
            ("W-01", C0["declared_issue_time"], T_NA, "T = issuance-not-after exactly: accepted (the bound is inclusive)"),
            ("W-02", NB0, utc_seconds(NB0) + 3600, "declared time = issuance-not-before exactly: accepted")]:
        check_issuance_window(decode_dns(D, owner, [rd_win]), declared, t)
        golden.append({"id": gid, "kind": "window", "note": note, "input": win_input(declared, t)})

    # ---- self-check of goldens with implementation A ----------------------------------------------
    assert decode_frame(f0, T_ATTEST)["signer"]["key_fp"] == FP_KMS
    assert decode_frame(fm, T_MANIFEST)["key_fp"] == FP_KMS
    assert decode_anchor(anc) == [(f0, s0), (f1, s1)]
    assert decode_anchor(anc_can) == [(f_can, sc0), (f_can_gpg, sc1)]
    assert decode_snapshot(sp) == snap
    check_receipt(fm, f0, s0, f1, s1, anc, KEYS)
    for g in golden:
        if g["kind"] == "content":
            b = bytes.fromhex(g["bytes_hex"])
            assert jcs(decode_payload(b)) == b

    # ---- rejections: content (ingestion) -----------------------------------------------------------
    def rc(rid, data, code, note):
        if isinstance(data, str):
            data = data.encode("utf-8", errors="surrogatepass")
        expect_reject(lambda: ingest(data), code)
        reject.append({"id": rid, "entry": "content", "input": {"text_hex": H(data)}, "expect": code, "note": note})

    rc("XC-01", '{"a":1,"a":2}', "JSON_DUPLICATE_NAME", "duplicate member name")
    rc("XC-02", '{"a":1,"\\u0061":2}', "JSON_DUPLICATE_NAME", "duplicate name after unescaping")
    rc("XC-03", "-0", "JSON_NUMBER", "negative zero")
    rc("XC-04", "[-0.0e5]", "JSON_NUMBER", "negative zero, other spelling")
    rc("XC-05", "NaN", "JSON_SYNTAX", "NaN is not JSON")
    rc("XC-06", "[Infinity]", "JSON_SYNTAX", "Infinity is not JSON")
    rc("XC-07", "1e400", "JSON_NUMBER", "overflows binary64")
    rc("XC-08", "1e-400", "JSON_NUMBER", "nonzero value underflows to 0")
    rc("XC-09", "333333333.33333329", "JSON_NUMBER", "RFC 8785 would print 333333333.3333333: value changes")
    rc("XC-10", "0.1000000000000000055511151231257827021181583404541015625", "JSON_NUMBER",
       "exactly a double, but RFC 8785 prints 0.1: value changes")
    rc("XC-11", "9007199254740993", "JSON_NUMBER", "2^53+1 is not a double")
    rc("XC-12", "[1e-999999999]", "JSON_NUMBER", "extreme exponent")
    rc("XC-13", '"\\ud800"', "JSON_STRING", "lone surrogate escape")
    rc("XC-14", '"\\uffff"', "JSON_STRING", "noncharacter U+FFFF")
    rc("XC-15", '"\\ufdd0"', "JSON_STRING", "noncharacter U+FDD0")
    rc("XC-16", '"e\\u0301"', "JSON_STRING", "not NFC (e + combining acute)")
    rc("XC-17", '{"e\\u0301":1}', "JSON_STRING", "member name not NFC")
    rc("XC-18", '"\\u0378"', "JSON_STRING", "unassigned in Unicode 16.0.0")
    rc("XC-19", b"\xef\xbb\xbf{}", "JSON_SYNTAX", "byte-order mark")
    rc("XC-20", b'"\xff"', "JSON_ENCODING", "invalid UTF-8")
    rc("XC-21", b'"\xc0\xaf"', "JSON_ENCODING", "overlong UTF-8")
    rc("XC-22", b'"\xed\xa0\x80"', "JSON_ENCODING", "UTF-8-encoded surrogate")
    rc("XC-23", "{} x", "JSON_SYNTAX", "trailing bytes after the JSON text")
    rc("XC-24", "01", "JSON_SYNTAX", "leading zero")
    rc("XC-25", "+1", "JSON_SYNTAX", "plus sign")
    rc("XC-26", "1.", "JSON_SYNTAX", "bare decimal point")
    rc("XC-27", "[" * 63 + "]" * 63, "JSON_DEPTH", "content depth 63")
    rc("XC-28", '"\\u001"', "JSON_SYNTAX", "short escape")
    rc("XC-29", '"a\x01"', "JSON_SYNTAX", "raw control character")
    rc("XC-30", "", "JSON_SYNTAX", "empty text")
    rc("XC-31", "1e99999999999999999999", "JSON_NUMBER", "nonzero value with an extreme exponent")
    rc("XC-32", "-0e99999999999999999999", "JSON_NUMBER", "negative zero with an extreme exponent")
    rc("XC-33", "4.9e-324", "JSON_NUMBER", "rounds to the smallest subnormal, which prints as 5e-324")

    # ---- rejections: frames --------------------------------------------------------------------------
    def rf(rid, data, code, note, entry="frame-attest"):
        exp = {"frame-attest": T_ATTEST, "frame-manifest": T_MANIFEST}[entry]
        expect_reject(lambda: decode_frame(data, exp), code)
        reject.append({"id": rid, "entry": entry, "input": {"bytes_hex": H(data)}, "expect": code, "note": note})

    hdr = header(T_ATTEST)
    payload0 = f0[len(hdr) + 6:]

    def raw_frame(payload, tag=T_ATTEST, cv=CV, n=None):
        return header(tag) + struct.pack(">HI", cv, len(payload) if n is None else n) + payload

    rf("XF-01", raw_frame(payload0, n=len(payload0) + 1), "TRUNCATED", "length prefix +1")
    rf("XF-02", raw_frame(payload0, n=len(payload0) - 1), "TRAILING", "length prefix -1")
    rf("XF-03", raw_frame(payload0, n=MAX_PAYLOAD + 1), "LENGTH_CAP", "length prefix above 2^24")
    rf("XF-04", f0 + b"\x00", "TRAILING", "one trailing byte")
    rf("XF-05", f0 + f0, "TRAILING", "a second frame appended")
    for i, cut in enumerate([0, 1, 10, len(hdr), len(hdr) + 1, len(hdr) + 3, len(hdr) + 6, len(f0) - 1], 6):
        rf(f"XF-{i:02d}", f0[:cut], "TRUNCATED", f"truncated to {cut} bytes")
    rf("XF-14", fm, "TAG_MISMATCH", "a manifest frame where an attestation is expected")
    rf("XF-15", f0, "TAG_MISMATCH", "an attestation frame where a manifest is expected", entry="frame-manifest")
    rf("XF-16", anc, "TAG_MISMATCH", "an anchor preimage where an attestation is expected")
    rf("XF-17", raw_frame(payload0, tag=b"tessera-v2/attest"), "TAG_UNKNOWN", "unknown version in the tag")
    rf("XF-18", bytes([len(T_ATTEST) + 1]) + f0[1:], "TAG_UNKNOWN", "tag-length byte +1")
    rf("XF-19", bytes([len(T_ATTEST) - 1]) + f0[1:], "TAG_UNKNOWN", "tag-length byte -1")
    rf("XF-20", raw_frame(payload0, tag=b"tessera-v1/wrapper"), "TAG_UNKNOWN", "a P7 type V1 does not use")
    rf("XF-21", raw_frame(payload0, cv=0), "CV_UNKNOWN", "canonicalization version 0")
    rf("XF-22", raw_frame(payload0, cv=2), "CV_UNKNOWN", "canonicalization version 2")

    p0 = payload0.decode("utf-8")
    pf = p0.replace('"cvss":9.8', '"cvss":9.80')
    assert pf != p0
    mut = [
        ("XF-23", p0.replace('{"common":', '{ "common":', 1), "JSON_NONCANONICAL", "whitespace"),
        ("XF-24", p0.replace('"cvss":9.8', '"cvss":9.80'), "JSON_NONCANONICAL", "number spelling 9.80"),
        ("XF-25", p0.replace('"name":"café"', '"name":"caf\\u00e9"'), "JSON_NONCANONICAL", "escaped e-acute"),
        ("XF-26", '{"signer":' + p0[p0.index('"signer":') + 9:-1] + ',"common":' + p0[10:p0.index(',"signer":')] + "}",
         "JSON_NONCANONICAL", "members out of order"),
        ("XF-27", p0.replace('"cvss":9.8', '"cvss":-0'), "JSON_NUMBER", "negative zero inside a frame"),
        ("XF-28", p0.replace('"cvss":9.8', '"cvss":9.8,"cvss":9.8'), "JSON_DUPLICATE_NAME", "duplicate name inside a frame"),
        ("XF-29", p0.replace('"cvss":9.8', '"cvss":1E2'), "JSON_NONCANONICAL", "exponent spelling of 100"),
        ("XF-30", p0.replace('"statement":"sbom"', '"statement":"\\u0073bom"'), "JSON_NONCANONICAL", "unnecessary escape"),
    ]
    for rid, ptext, code, note in mut:
        rf(rid, raw_frame(ptext.encode("utf-8")), code, note)

    # schema violations: rebuild a valid-JSON payload with one field wrong
    def schema_case(rid, note, mutate):
        v = {"common": dict(C0), "signer": {"key_fp": FP_KMS}}
        v["common"]["spec"] = dict(C0["spec"])
        mutate(v)
        rf(rid, raw_frame(jcs(v)), "SCHEMA", note)

    schema_case("XF-31", "missing field", lambda v: v["common"].pop("preamble_sha256"))
    schema_case("XF-32", "extra field", lambda v: v["common"].__setitem__("extra", 1))
    schema_case("XF-33", "wrong profile", lambda v: v["common"].__setitem__("profile", "tessera-v1-degraded"))
    schema_case("XF-34", "uppercase hex", lambda v: v["common"].__setitem__("manifest_sha256", sha(fm).upper()))
    schema_case("XF-35", "binding forms unsorted", lambda v: v["common"].__setitem__("binding_forms", ["STMT_DIRECT", "STMT_DIGEST"]))
    schema_case("XF-36", "binding forms duplicated", lambda v: v["common"].__setitem__("binding_forms", ["STMT_DIRECT", "STMT_DIRECT"]))
    schema_case("XF-37", "binding forms empty", lambda v: v["common"].__setitem__("binding_forms", []))
    schema_case("XF-38", "impossible date", lambda v: v["common"].__setitem__("declared_issue_time", "2026-02-30T00:00:00Z"))
    schema_case("XF-39", "leap second", lambda v: v["common"].__setitem__("declared_issue_time", "2026-12-31T23:59:60Z"))
    schema_case("XF-40", "fractional seconds", lambda v: v["common"].__setitem__("declared_issue_time", "2026-10-12T14:03:07.0Z"))
    schema_case("XF-41", "uppercase issuer", lambda v: v["common"].__setitem__("issuer", "WAMASON.com"))
    schema_case("XF-42", "SHA-1 v4 fingerprint scheme (not accepted in V1)", lambda v: v["signer"].__setitem__("key_fp", "openpgp-v4:" + "0" * 40))
    schema_case("XF-43", "fingerprint too short", lambda v: v["signer"].__setitem__("key_fp", FP_KMS[:-2]))
    schema_case("XF-44", "lowercase algorithm id", lambda v: v["common"].__setitem__("alg", ALG.lower()))
    schema_case("XF-45", "signer member carries a slot name", lambda v: v["signer"].__setitem__("slot", "kms"))
    schema_case("XF-46", "number where a string is required", lambda v: v["common"].__setitem__("issuer", 1.0))
    schema_case("XF-47", "single-label issuer", lambda v: v["common"].__setitem__("issuer", "localhost"))
    deep = [[]]
    for _ in range(61):
        deep = [deep]
    rf("XF-48", raw_frame(jcs({"common": {**C0, "content": deep}, "signer": {"key_fp": FP_KMS}})), "JSON_DEPTH",
       "payload depth 65")

    mbad = {"alg": ALG, "issuer": D, "key_fp": FP_GPG, "sset": [FP_KMS], "ver": "map-v1"}
    rf("XF-49", raw_frame(jcs(mbad), tag=T_MANIFEST), "SCHEMA", "manifest with the slots' fingerprint schemes swapped",
       entry="frame-manifest")
    mbad2 = {"alg": ALG, "issuer": D, "key_fp": FP_KMS, "sset": [FP_GPG, FP_GPG], "ver": "map-v1"}
    rf("XF-50", raw_frame(jcs(mbad2), tag=T_MANIFEST), "SCHEMA", "manifest with three slots", entry="frame-manifest")
    mbad3 = {"alg": ALG, "issuer": D, "key_fp": FP_KMS, "sset": [FP_GPG], "ver": "map-v2"}
    rf("XF-51", raw_frame(jcs(mbad3), tag=T_MANIFEST), "SCHEMA", "unknown map version", entry="frame-manifest")

    # ---- rejections: anchor preimage and snapshot ----------------------------------------------------
    def ra(rid, data, code, note):
        expect_reject(lambda: decode_anchor(data), code)
        reject.append({"id": rid, "entry": "anchor", "input": {"bytes_hex": H(data)}, "expect": code, "note": note})

    ah = header(T_ANCHOR)

    def P4(x):
        return struct.pack(">I", len(x)) + x

    def slots(*parts, count=2):
        return ah + bytes([count]) + b"".join(P4(x) for x in parts)

    # pieces of SIG-01, for byte surgery
    hl0 = int.from_bytes(s0[6:8], "big")
    hashed0 = s0[8:8 + hl0]
    ul0 = int.from_bytes(s0[8 + hl0:10 + hl0], "big")
    unhashed0 = s0[10 + hl0:10 + hl0 + ul0]
    left0 = s0[10 + hl0 + ul0:12 + hl0 + ul0]
    mpi_at = 12 + hl0 + ul0
    _, r0, ss0 = decode_sig_openpgp4(s0)
    body0 = s0[2:]

    def poke(sig, i, v):
        b = bytearray(sig)
        b[i] = v
        return bytes(b)

    def armor(sig):
        import base64
        crc = 0xB704CE
        for byte in sig:
            crc ^= byte << 16
            for _ in range(8):
                crc <<= 1
                if crc & 0x1000000:
                    crc ^= 0x1864CFB
        b64 = base64.b64encode(sig).decode()
        lines = "\n".join(b64[i:i + 64] for i in range(0, len(b64), 64))
        return (f"-----BEGIN PGP SIGNATURE-----\n\n{lines}\n="
                + base64.b64encode((crc & 0xFFFFFF).to_bytes(3, "big")).decode() + "\n-----END PGP SIGNATURE-----\n").encode()

    ra("XA-01", slots(f0, s0, count=1), "ANCHOR_COUNT", "one slot")
    ra("XA-02", ah + bytes([3]) + anc[len(ah) + 1:] + P4(f0) + P4(s0), "ANCHOR_COUNT", "three slots")
    ra("XA-03", anc[:-1], "TRUNCATED", "truncated by one byte (inside the gpg signature)")
    ra("XA-04", anc + b"\x00", "TRAILING", "trailing byte after the gpg signature")
    ra("XA-05", ah + bytes([2]) + struct.pack(">I", len(f0) + 1) + f0 + b"\x00" + P4(s0) + P4(f1) + P4(s1),
       "TRAILING", "inner frame carries a trailing byte inside its anchor slot")
    ra("XA-06", f0, "TAG_MISMATCH", "an attestation frame where the anchor preimage is expected")
    ra("XA-07", slots(fm, s0, f1, s1), "TAG_MISMATCH", "a manifest frame inside the anchor preimage")
    ra("XA-08", ah + bytes([2]) + struct.pack(">I", len(f0) + 5) + f0 + P4(s0) + P4(f1) + P4(s1), "TRAILING",
       "first frame length overstated by 5: the frame slot swallows the next prefix, and the inner frame sees trailing bytes")
    ra("XA-09", encode_anchor_frames_only(f0, f1), "TAG_UNKNOWN",
       "the withdrawn frame-only layout under its own tag: not in T, so never accepted (no fallback)")
    ra("XA-10", encode_anchor_frames_only(f0, f1, tag=T_ANCHOR), "SIG_PACKET",
       "the frame-only layout under the new tag: the gpg frame is read as the kms signature and rejected")
    ra("XA-11", slots(f0, b"", f1, s1), "SIG_EMPTY", "empty kms signature")
    ra("XA-12", ah + bytes([2]) + P4(f0) + struct.pack(">I", len(s0) + 1) + s0 + P4(f1) + P4(s1), "TRAILING",
       "kms signature length +1: the slot takes one byte of the next prefix after the packet")
    ra("XA-13", ah + bytes([2]) + P4(f0) + struct.pack(">I", len(s0) - 1) + s0 + P4(f1) + P4(s1), "TRUNCATED",
       "kms signature length -1: the packet runs past its slot")
    ra("XA-14", ah + bytes([2]) + P4(f0) + struct.pack(">I", SIG_CAP_OPENPGP4 + 1) + s0, "LENGTH_CAP",
       "kms signature length above the 1024-byte OpenPGP cap")
    ra("XA-15", slots(f0, s0 + s0, f1, s1), "TRAILING", "an extra signature packet in the kms slot")
    ra("XA-16", slots(f0, s0, f1, s1 + b"\xa8\x03PGP"), "TRAILING", "an extra (marker) packet after the gpg signature")
    ra("XA-17", slots(f0, s0[:-1], f1, s1), "TRUNCATED", "kms signature truncated by one byte, slot length consistent")
    ra("XA-18", slots(f0, armor(s0), f1, s1), "SIG_PACKET", "ASCII-armored signature")
    ra("XA-19", slots(f0, bytes([0xC2, len(body0)]) + body0, f1, s1), "SIG_PACKET",
       "same packet body under an OpenPGP-format (0xC2) header: not the pinned serialization")
    ra("XA-20", slots(f0, bytes([0x89]) + struct.pack(">H", len(body0)) + body0, f1, s1), "SIG_PACKET",
       "two-octet legacy length where one octet fits")
    ra("XA-21", slots(f0, b"\xa8\x03PGP", f1, s1), "SIG_PACKET", "a marker packet instead of a signature packet")
    ra("XA-22", slots(f0, poke(s0, 3, 0x01), f1, s1), "SIG_FORMAT", "signature type 0x01 (text)")
    ra("XA-23", slots(f0, poke(s0, 2, 6), f1, s1), "SIG_FORMAT", "signature version 6")
    ra("XA-24", slots(f0, poke(s0, 4, 22), f1, s1), "SIG_FORMAT", "public-key algorithm 22 (EdDSA)")
    ra("XA-25", slots(f0, poke(s0, 5, 10), f1, s1), "SIG_FORMAT", "hash algorithm 10 (SHA-512)")
    bits_r = int.from_bytes(s0[mpi_at:mpi_at + 2], "big")
    ra("XA-26", slots(f0, s0[:mpi_at] + struct.pack(">H", bits_r + 1) + s0[mpi_at + 2:], f1, s1), "SIG_FORMAT",
       "MPI r bit count overstated by 1")
    ra("XA-27", slots(f0, s0[:6] + struct.pack(">H", len(body0)) + s0[8:], f1, s1), "SIG_FORMAT",
       "hashed subpacket area length runs past the packet body")
    ra("XA-28", slots(f0, bytes([0x88, len(body0) + 1]) + body0 + b"\x00", f1, s1), "SIG_FORMAT",
       "a byte after the second MPI inside the packet body")
    ct = hashed0.index(b"\x05\x02")
    hashed_long = hashed0[:ct] + b"\xff\x00\x00\x00\x05" + hashed0[ct + 1:]
    ra("XA-29", slots(f0, openpgp_v4_sig_packet(hashed_long, unhashed0, left0, r0, ss0), f1, s1), "SIG_FORMAT",
       "five-octet subpacket length where one octet fits")
    ra("XA-30", slots(s0, f0, f1, s1), "TRUNCATED",
       "signature and frame swapped inside the kms slot: the signature is read as a frame (tag length 0x88 runs past it)")
    ra("XA-31", slots(f_can, b"\x00" * (SIG_CAP_OPAQUE + 1), f_can_gpg, sc1), "LENGTH_CAP",
       "unregistered alg id: opaque signature above 65536 bytes")
    ra("XA-32", slots(f_can, sc0, f_can_gpg, b""), "SIG_EMPTY", "unregistered alg id: empty opaque signature")

    def rs(rid, data, code, note):
        expect_reject(lambda: decode_snapshot(data), code)
        reject.append({"id": rid, "entry": "snapshot", "input": {"bytes_hex": H(data)}, "expect": code, "note": note})

    rs("XS-01", sp + b"\x00", "TRAILING", "trailing byte")
    rs("XS-02", sp[:-1], "TRUNCATED", "truncated")
    rs("XS-03", header(T_SNAPSHOT) + struct.pack(">I", 0), "SCHEMA", "empty snapshot")
    rs("XS-04", anc, "TAG_MISMATCH", "an anchor preimage where a snapshot preimage is expected")

    # ---- rejections: receipt (codec checks, then verification of the committed signatures) ---------
    stamped = sha(anc)
    keys_swapped = {"kms": {"x": keys_input["gpg"]["x"], "y": keys_input["gpg"]["y"]},
                    "gpg": {"x": keys_input["kms"]["x"], "y": keys_input["kms"]["y"], "created": created}}

    def keys_of(ki):
        return ((int(ki["kms"]["x"], 16), int(ki["kms"]["y"], 16)),
                (int(ki["gpg"]["x"], 16), int(ki["gpg"]["y"], 16), ki["gpg"]["created"]))

    def rr(rid, m, a, sa, b, sb, p, code, note, ki=keys_input, control=None):
        expect_reject(lambda: check_receipt(m, a, sa, b, sb, p, keys_of(ki)), code)
        v = {"id": rid, "entry": "receipt",
             "input": {"manifest_hex": H(m), "f0_hex": H(a), "s0_hex": H(sa), "f1_hex": H(b), "s1_hex": H(sb),
                       "anchor_hex": H(p), "keys": ki},
             "expect": code, "note": note}
        if control is not None:
            # Negative control: the presented signature is valid, yet it is not the one the stamp commits.
            slot = control
            f, s_, q = (a, sa, keys_of(ki)[0]) if slot == "kms" else (b, sb, keys_of(ki)[1][:2])
            assert verify_openpgp4(f, s_, q), rid
            assert sha(encode_anchor(a, sa, b, sb)) != stamped, rid
            v["control"] = {"slot": slot, "presented_sig_verifies": True, "stamped_anchor_sha256": stamped}
        reject.append(v)

    rr("XR-01", fm, f1, s1, f0, s0, encode_anchor(f1, s1, f0, s0), "RECEIPT_SLOT",
       "signer slots swapped (anchor rebuilt to match)")
    rr("XR-02", fm, f0, s0, f0, s0, encode_anchor(f0, s0, f0, s0), "RECEIPT_SLOT", "the kms slot presented twice")
    f1_splice = encode_attest(common('{"statement":"other"}'), FP_GPG)
    s1_splice = sign_gpg(f1_splice)
    rr("XR-03", fm, f0, s0, f1_splice, s1_splice, encode_anchor(f0, s0, f1_splice, s1_splice), "RECEIPT_COMMON_MISMATCH",
       "content spliced in the gpg slot (validly signed)")
    fm_other = encode_manifest(ALG, "example.org", FP_KMS, FP_GPG)
    rr("XR-04", fm_other, f0, s0, f1, s1, anc, "RECEIPT_MANIFEST_MISMATCH", "manifest frame replaced")
    cw = common(issuer="example.org")
    f0w, f1w = encode_attest(cw, FP_KMS), encode_attest(cw, FP_GPG)
    s0w, s1w = sign_kms(f0w), sign_gpg(f1w)
    rr("XR-05", fm, f0w, s0w, f1w, s1w, encode_anchor(f0w, s0w, f1w, s1w), "RECEIPT_MANIFEST_MISMATCH",
       "issuer differs from the manifest's, manifest hash correct")
    rr("XR-06", fm, f0, s0, f1, s1, encode_anchor(f1, s1, f0, s0), "RECEIPT_ANCHOR_MISMATCH",
       "anchor preimage lists the slots in swapped order")
    rr("XR-07", fm, f0, s0, f1, s1, encode_anchor(f0, s0, f1_splice, s1_splice), "RECEIPT_ANCHOR_MISMATCH",
       "anchor preimage over another frame and signature")
    rr("XR-08", fm, f0, s0, f1, s1, anc + b"\x00", "TRAILING", "anchor preimage with a trailing byte")
    rr("XR-09", fm, f0, s0, f1, s1, encode_anchor_frames_only(f0, f1), "TAG_UNKNOWN",
       "a valid signed receipt presented with a frame-only anchor (the pre-stage-then-sign shape): rejected, no fallback")
    s0_alt = sign_kms(f0, extra=b"a second, independent signature over the same frame")
    s0_mal = openpgp_v4_sig_packet(hashed0, unhashed0, left0, r0, N - ss0)
    s0_unh = openpgp_v4_sig_packet(hashed0, _subpacket(16, bytes(8)), left0, r0, ss0)
    s0_late = sign_kms(f0, when=sig_created + 5 * 365 * 86400)
    _, r1, ss1 = decode_sig_openpgp4(s1)
    hl1 = int.from_bytes(s1[6:8], "big")
    ul1 = int.from_bytes(s1[8 + hl1:10 + hl1], "big")
    s1_mal = openpgp_v4_sig_packet(s1[8:8 + hl1], s1[10 + hl1:10 + hl1 + ul1], s1[10 + hl1 + ul1:12 + hl1 + ul1], r1, N - ss1)
    for s_ in (s0_alt, s0_mal, s0_unh, s0_late):
        assert s_ != s0
    rr("XR-10", fm, f0, s0_alt, f1, s1, anc, "RECEIPT_ANCHOR_MISMATCH",
       "NEGATIVE CONTROL: a second valid kms signature over F-01 (other RFC 6979 nonce); it verifies, but the stamp commits SIG-01",
       control="kms")
    rr("XR-11", fm, f0, s0_mal, f1, s1, anc, "RECEIPT_ANCHOR_MISMATCH",
       "NEGATIVE CONTROL: SIG-01 malleated to (r, n - s); it verifies, but it is not the committed byte string", control="kms")
    rr("XR-12", fm, f0, s0_unh, f1, s1, anc, "RECEIPT_ANCHOR_MISMATCH",
       "NEGATIVE CONTROL: SIG-01 with its unhashed issuer key ID zeroed; it verifies, but it is not the committed byte string",
       control="kms")
    rr("XR-13", fm, f0, s0_late, f1, s1, anc, "RECEIPT_ANCHOR_MISMATCH",
       "NEGATIVE CONTROL: the same frame signed five years later (pre-stage then sign); a frame-only anchor would have "
       "matched it, A_sig does not", control="kms")
    rr("XR-14", fm, f0, s0, f1, s1_mal, anc, "RECEIPT_ANCHOR_MISMATCH",
       "NEGATIVE CONTROL: SIG-02 malleated to (r, n - s) in the gpg slot", control="gpg")
    rr("XR-15", fm, f0, s1, f1, s0, anc, "RECEIPT_ANCHOR_MISMATCH", "signatures swapped between slots, original anchor")
    rr("XR-16", fm, f0, s1, f1, s0, encode_anchor(f0, s1, f1, s0), "SIG_INVALID",
       "signatures swapped between slots, anchor rebuilt over the swap: the codec accepts; the committed signatures "
       "do not verify under their slot keys")
    rr("XR-17", fm, f0, s0, f1, s1, anc, "KEY_MISMATCH", "public keys presented in the wrong slots", ki=keys_swapped)

    # ---- rejections: DNS key-publication record ---------------------------------------------------
    good = dns_value(kms_hex, gpg_hex, NA0, NB0)    # 255 bytes: canonical, exactly a 90-day window
    short = dns_value(kms_hex, gpg_hex, NA0)        # not-before omitted: used only where an earlier code fires
    base = f"v=tessera1;profile={PROFILE};kms={kms_hex};gpg={gpg_hex}"

    def rd_(rid, code, note, value=None, strings=None, rrset=None, own=owner):
        if rrset is None:
            rrset = [dns_rdata(*(strings if strings is not None else [value]))]
        expect_reject(lambda: decode_dns(D, own, rrset), code)
        reject.append({"id": rid, "entry": "dns", "input": {"D": D, "owner_hex": H(own), "rdata_hex": [H(x) for x in rrset]},
                       "expect": code, "note": note})

    rd_("XD-01", "DNS_VERSION", "unknown version", value=good.replace("v=tessera1", "v=tessera2"))
    rd_("XD-02", "DNS_SLOT_MISSING", "gpg slot missing", value=good[:good.index(";gpg=")])
    rd_("XD-03", "DNS_SLOT_DUPLICATE", "kms slot twice", value=base + f";kms={kms_hex}")
    rd_("XD-04", "DNS_FIELD_UNKNOWN", "extra field", value=short + ";x=1")
    rd_("XD-05", "DNS_ORDER", "slots out of order",
        value=f"v=tessera1;profile={PROFILE};gpg={gpg_hex};kms={kms_hex};{NB}={NB0};{NA}={NA0}")
    rd_("XD-06", "DNS_VALUE", "uppercase hex", value=good.replace(kms_hex, kms_hex.upper()))
    rd_("XD-07", "DNS_VALUE", "gpg fingerprint of the wrong length", value=good.replace(gpg_hex, gpg_hex[:-2]))
    rd_("XD-08", "DNS_SYNTAX", "space after a separator", value=short.replace(";profile", "; profile"))
    rd_("XD-09", "DNS_SYNTAX", "trailing separator", value=short + ";")
    rd_("XD-10", "DNS_STRINGS", "value split over two character-strings", strings=[good[:60], good[60:]])
    rd_("XD-11", "DNS_RRSET", "two TXT records at the owner name", rrset=[dns_rdata(good), dns_rdata(good)])
    rd_("XD-12", "DNS_OWNER", "owner name under another domain", value=good, own=dns_name_wire("_tessera-v1.example.org"))
    rd_("XD-13", "DNS_OWNER", "owner name without the underscore label", value=good, own=dns_name_wire("tessera-v1.wamason.com"))
    rd_("XD-14", "DNS_OWNER", "the domain apex itself", value=good, own=dns_name_wire("wamason.com"))
    rd_("XD-15", "DNS_PROFILE", "another profile", value=good.replace(PROFILE, "tessera-v2-strict"))
    rd_("XD-16", "DNS_VALUE", "impossible issuance-not-after time", value=good.replace(NA0, "2027-02-30T00:00:00Z"))
    rd_("XD-17", "DNS_RDATA", "character-string length runs past RDATA", rrset=[bytes([200]) + good.encode()[:50]])
    rd_("XD-18", "DNS_VERSION", "version not first", value=f"profile={PROFILE};v=tessera1;kms={kms_hex};gpg={gpg_hex}")
    rd_("XD-19", "DNS_FIELD_MISSING", "profile missing", value=f"v=tessera1;kms={kms_hex};gpg={gpg_hex}")
    rd_("XD-20", "DNS_SYNTAX", "empty field", value=short.replace(";kms", ";;kms"))
    rd_("XD-21", "DNS_RRSET", "no TXT record", rrset=[])
    rd_("XD-22", "DNS_FIELD_DUPLICATE", "issuance-not-after twice", value=short + f";{NA}=2027-10-13T00:00:00Z")
    rd_("XD-23", "DNS_WINDOW", "issuance-not-after equal to issuance-not-before", value=dns_value(kms_hex, gpg_hex, NB0, NB0))
    rd_("XD-24", "DNS_WINDOW", "issuance-not-after before issuance-not-before",
        value=dns_value(kms_hex, gpg_hex, "2026-10-11T23:59:59Z", NB0))
    rd_("XD-25", "DNS_FIELD_MISSING", "issuance-not-after missing (issuance-not-before present)", value=base + f";{NB}={NB0}")
    rd_("XD-26", "DNS_FIELD_MISSING", "issuance-not-after missing (no window at all)", value=base)
    rd_("XD-27", "DNS_VALUE", "issuance-not-after as a bare date", value=good.replace(NA0, "2027-10-12"))
    rd_("XD-28", "DNS_ORDER", "window fields in the wrong order", value=base + f";{NA}={NA0};{NB}={NB0}")
    rd_("XD-29", "DNS_FIELD_UNKNOWN", "the withdrawn not-before field", value=short + ";not-before=2026-10-12")
    frac = good.replace(NA0, "2027-01-10T00:00:00.0Z")    # 257 bytes: cannot be one character-string
    assert len(frac) == 257
    rd_("XD-30", "DNS_STRINGS", "issuance-not-after with fractional seconds: 257 bytes, so it can only arrive split "
        "over two character-strings (since 2026-10-12, not-before is mandatory)", strings=[frac[:200], frac[200:]])
    rd_("XD-31", "DNS_FIELD_MISSING", "issuance-not-before missing (issuance-not-after present)", value=short)
    rd_("XD-32", "DNS_WINDOW_LENGTH", "window of 90 days + 1 s",
        value=dns_value(kms_hex, gpg_hex, "2027-01-10T00:00:01Z", NB0))
    rd_("XD-33", "DNS_WINDOW_LENGTH", "a one-year window (the 2026-10-12 first-draft example)",
        value=dns_value(kms_hex, gpg_hex, "2027-10-12T00:00:00Z", NB0))

    def rw(rid, declared, t, code, note):
        expect_reject(lambda: check_issuance_window(decode_dns(D, owner, [rd_win]), declared, t), code)
        reject.append({"id": rid, "entry": "window", "input": win_input(declared, t), "expect": code, "note": note})

    rw("XW-01", C0["declared_issue_time"], T_NA + 1, "ISSUANCE_WINDOW", "T = issuance-not-after + 1 s")
    rw("XW-02", "2026-10-11T23:59:59Z", utc_seconds(NB0) + 3600, "ISSUANCE_WINDOW",
       "declared time 1 s before issuance-not-before")
    rw("XW-03", C0["declared_issue_time"], T_NA + 5 * 365 * 86400, "ISSUANCE_WINDOW",
       "a key surviving the service (or stolen) mints years after issuance-not-after")

    meta = {"profile": PROFILE, "canonicalization_version": CV, "unicode_version": UNICODE_VERSION,
            "generator": "formal/p8/vectors/gen.py (implementation A, stdlib + rfc8785 0.1.4)"}
    with open(os.path.join(here, "golden.json"), "w") as fh:
        json.dump({"meta": meta, "vectors": golden}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    with open(os.path.join(here, "reject.json"), "w") as fh:
        json.dump({"meta": meta, "vectors": reject}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"implementation A: {len(golden)} golden vectors, {len(reject)} rejection vectors; all self-checks pass")

    # ============================================================================================
    # Hybrid branch (formal/p8/HYBRID-SUPPLEMENT-DRAFT.md): rule R vectors under ALG_HYBRID. Written
    # to their own files so that golden.json and reject.json above stay byte-identical to the
    # 2026-10-12 baseline. Nothing above this line depends on anything below it.
    # ============================================================================================
    hg, hr = [], []
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    kms_cap_path = os.path.join(root, "prototype", "spike-pq", "out-kms", "capture.json")
    gcp_cap_path = os.path.join(root, "prototype", "spike-pq", "out-gcp", "capture.json")
    v1cap_path = os.path.join(root, "prototype", "spike-pq", "out-v1-hybrid", "capture.json")
    kms_cap_raw, gcp_cap_raw = open(kms_cap_path, "rb").read(), open(gcp_cap_path, "rb").read()
    kms_cap, gcp_cap = json.loads(kms_cap_raw), json.loads(gcp_cap_raw)
    import base64
    b64 = base64.b64decode

    # ---- keys: an ILLUSTRATIVE ML-DSA-65 test key (public seed) for kms; 2G with `created` for gpg ----
    xi = hashlib.sha256(b"tessera-v1 ILLUSTRATIVE ML-DSA-65 test key, slot kms; this seed is public").digest()
    pk_h, priv_h = mldsa65_keygen(xi)
    spki_h = SPKI_MLDSA65_PREFIX + pk_h
    FP_H = fp_spki(spki_h)
    check_key_kms(spki_h, FP_H)
    hg.append({"id": "K-H1", "kind": "fingerprint-kms-spki",
               "note": "hybrid kms slot: spki-sha256 over the ML-DSA-65 SPKI DER (OID 2.16.840.1.101.3.4.3.18, "
                       "parameters absent); ILLUSTRATIVE test key from a public FIPS 204 KeyGen seed",
               "input": {"keygen_seed_xi_hex": H(xi)}, "spki_der_hex": H(spki_h), "key_fp": FP_H})
    spki_real = b64(kms_cap["spki_b64"])
    FP_REAL = fp_spki(spki_real)
    check_key_kms(spki_real, FP_REAL)
    hg.append({"id": "K-H2", "kind": "fingerprint-kms-spki",
               "note": "the REAL AWS KMS ML-DSA-65 key of the 2026-10-13 spike (GetPublicKey output, unchanged)",
               "input": {"source": "prototype/spike-pq/out-kms/capture.json spki_b64", "kms_key_id": kms_cap["key_id"]},
               "spki_der_hex": H(spki_real), "key_fp": FP_REAL})

    # ---- manifest, frames, signatures, anchor, receipt (test keys) -------------------------------
    fmh = encode_manifest(ALG_HYBRID, D, FP_H, FP_GPG)
    hg.append({"id": "M-H1", "kind": "frame-manifest", "note": "map-v1 tuple under the hybrid pair id",
               "input": {"alg": ALG_HYBRID, "issuer": D, "key_fp": FP_H, "sset": [FP_GPG]},
               "bytes_hex": H(fmh), "sha256": sha(fmh)})
    CH = common(alg=ALG_HYBRID, mh=sha(fmh))
    fh0, fh1 = encode_attest(CH, FP_H), encode_attest(CH, FP_GPG)
    big_text = '{"blob":"' + "a" * 4500 + '","statement":"sbom"}'
    CB = common(big_text, alg=ALG_HYBRID, mh=sha(fmh))
    fb0, fb1 = encode_attest(CB, FP_H), encode_attest(CB, FP_GPG)
    assert len(fh0) <= 4096 < len(fb0)
    for gid, f, cc, txt, fp_, note in [
            ("F-H1", fh0, CH, content_text, FP_H, "hybrid, slot kms (frame <= 4096 bytes: KMS RAW signs it whole)"),
            ("F-H2", fh1, CH, content_text, FP_GPG, "hybrid, slot gpg; equal to F-H1 outside the signer member"),
            ("F-H3", fb0, CB, big_text, FP_H, "hybrid, slot kms, frame above 4096 bytes: KMS needs EXTERNAL_MU"),
            ("F-H4", fb1, CB, big_text, FP_GPG, "hybrid, slot gpg, large content")]:
        hg.append({"id": gid, "kind": "frame-attest", "note": note,
                   "input": {"common": common_input(cc, txt), "key_fp": fp_}, "bytes_hex": H(f), "sha256": sha(f)})
    sh0 = mldsa65_sign(priv_h, fh0)                         # FIPS 204 deterministic variant (rnd = 0^32)
    sh1 = sign_gpg(fh1)
    mu_b0 = mldsa65_external_mu(pk_h, fb0)
    sb0 = mldsa65_sign_mu(priv_h, mu_b0)                    # issuer computes mu; the HSM signs mu
    assert sb0 == mldsa65_sign(priv_h, fb0)                 # same bytes as signing the frame itself
    sb1 = sign_gpg(fb1)
    for s_, f in ((sh0, fh0), (sb0, fb0)):
        assert len(s_) == SIG_LEN_MLDSA65 and mldsa65_verify(pk_h, f, s_)
    for gid, f, s_, mode, note in [
            ("SIG-H1", fh0, sh0, "pure", "rule R over F-H1: raw ML-DSA-65, pure, empty context, deterministic variant"),
            ("SIG-H3", fb0, sb0, "external-mu", "rule R over F-H3 (5246-byte frame) made from the issuer-computed mu, "
                                                "as KMS EXTERNAL_MU does; byte-identical to signing the frame itself")]:
        v = {"id": gid, "kind": "signature-mldsa65", "note": note,
             "input": {"message_hex": H(f), "slot": "kms", "alg": ALG_HYBRID, "spki_der_hex": H(spki_h), "mode": mode},
             "bytes_hex": H(s_), "verifies": True}
        if mode == "external-mu":
            v["input"]["mu_hex"] = H(mu_b0)
        hg.append(v)
    for gid, f, s_ in (("SIG-H2", fh1, sh1), ("SIG-H4", fb1, sb1)):
        assert verify_openpgp4(f, s_, g2)
        hg.append({"id": gid, "kind": "signature", "note": "rule O in the gpg slot under the hybrid id (unchanged rule)",
                   "input": {"frame_hex": H(f), "slot": "gpg", "alg": ALG_HYBRID, "x": f"{g2[0]:064x}", "y": f"{g2[1]:064x}"},
                   "bytes_hex": H(s_), "verifies": True})

    # ---- the real captures (prototype/spike-pq): verified, never re-signed or re-framed -------------
    small, big = b64(kms_cap["small_frame_b64"]), b64(kms_cap["big_frame_b64"])
    s_raw, s_mu = b64(kms_cap["sig_raw_small_b64"]), b64(kms_cap["sig_mu_big_b64"])
    check_signature_r(small, s_raw, spki_real)
    check_signature_r(big, s_mu, spki_real)
    assert small[1:1 + small[0]] not in ALL_TAGS                         # the spike frames are V1-SHAPED only
    hg.append({"id": "SIG-H5", "kind": "signature-mldsa65",
               "note": "REAL AWS KMS ML-DSA-65 signature, MessageType RAW, over the spike's 2123-byte V1-shaped frame "
                       "(tag tessera-v1/receipt, not in T: not a V1 frame, so it cannot sit in A_sig; message kept "
                       "byte-exact, not re-framed, because re-framing would void the signature)",
               "input": {"message_hex": H(small), "slot": "kms", "alg": ALG_HYBRID, "spki_der_hex": H(spki_real),
                         "mode": "kms-raw"},
               "bytes_hex": H(s_raw), "verifies": True})
    hg.append({"id": "SIG-H6", "kind": "signature-mldsa65",
               "note": "REAL AWS KMS ML-DSA-65 signature, MessageType EXTERNAL_MU, over the spike's 6075-byte "
                       "V1-shaped frame; mu computed by the issuer from the KMS public key; verifies as an ordinary "
                       "pure signature over the whole frame",
               "input": {"message_hex": H(big), "slot": "kms", "alg": ALG_HYBRID, "spki_der_hex": H(spki_real),
                         "mode": "kms-external-mu", "mu_hex": H(mldsa65_external_mu(spki_real[22:], big))},
               "bytes_hex": H(s_mu), "verifies": True})
    gpem = gcp_cap["spki_pem"]
    gder = b64("".join(ln for ln in gpem.splitlines() if not ln.startswith("-----")))
    assert gder[:len(SPKI_P256_PREFIX)] == SPKI_P256_PREFIX and len(gder) == 91
    gq = (int.from_bytes(gder[27:59], "big"), int.from_bytes(gder[59:91], "big"))
    gframe, gsig = bytes.fromhex(gcp_cap["frame_hex"]), bytes.fromhex(gcp_cap["sig_hex"])
    decode_frame(gframe, T_ATTEST)
    decode_sig(gsig, ALG_HYBRID, 1)
    assert verify_openpgp4(gframe, gsig, gq)
    assert fp_gpg(_point(*gq), gcp_cap["key_created"]) == decode_frame(gframe, T_ATTEST)["signer"]["key_fp"]
    hg.append({"id": "SIG-H7", "kind": "signature",
               "note": "REAL slot-2 signature: GCP Cloud KMS HSM P-256 (2026-10-14), rule O over a real V1 attest frame "
                       "whose signer.key_fp is that key's gpg-sha256; its common.alg is the classical id (captured "
                       "before the pair id existed); rule O is the same rule in the gpg slot under both ids",
               "input": {"frame_hex": H(gframe), "slot": "gpg", "alg": ALG_HYBRID, "x": f"{gq[0]:064x}",
                         "y": f"{gq[1]:064x}", "created": gcp_cap["key_created"]},
               "bytes_hex": H(gsig), "verifies": True})

    anch = encode_anchor(fh0, sh0, fh1, sh1)
    anchb = encode_anchor(fb0, sb0, fb1, sb1)
    for gid, parts_, a_, note in [("A-H1", (fh0, sh0, fh1, sh1), anch, "hybrid A_sig over (F-H1, SIG-H1, F-H2, SIG-H2)"),
                                  ("A-H2", (fb0, sb0, fb1, sb1), anchb, "hybrid A_sig over the large frames (F-H3, SIG-H3, F-H4, SIG-H4)")]:
        assert decode_anchor(a_) == [(parts_[0], parts_[1]), (parts_[2], parts_[3])]
        hg.append({"id": gid, "kind": "anchor", "note": note,
                   "input": {"f0_hex": H(parts_[0]), "s0_hex": H(parts_[1]), "f1_hex": H(parts_[2]), "s1_hex": H(parts_[3])},
                   "bytes_hex": H(a_), "sha256": sha(a_)})
    keys_h = {"kms": {"spki_der_hex": H(spki_h)}, "gpg": keys_input["gpg"]}

    def keys_of_h(ki):
        k = ki["kms"]
        kms = bytes.fromhex(k["spki_der_hex"]) if "spki_der_hex" in k else (int(k["x"], 16), int(k["y"], 16))
        return kms, (int(ki["gpg"]["x"], 16), int(ki["gpg"]["y"], 16), ki["gpg"]["created"])

    for gid, (a, sa, b, sb), a_, note in [
            ("R-H1", (fh0, sh0, fh1, sh1), anch, "hybrid receipt: codec checks pass; the committed ML-DSA-65 (kms) and "
                                                 "P-256 (gpg) signatures verify under the slot keys"),
            ("R-H2", (fb0, sb0, fb1, sb1), anchb, "hybrid receipt over frames above 4096 bytes (kms signed via external mu)")]:
        check_receipt(fmh, a, sa, b, sb, a_, keys_of_h(keys_h))
        hg.append({"id": gid, "kind": "receipt", "note": note,
                   "input": {"manifest_hex": H(fmh), "f0_hex": H(a), "s0_hex": H(sa), "f1_hex": H(b), "s1_hex": H(sb),
                             "anchor_hex": H(a_), "keys": keys_h},
                   "anchor_sha256": sha(a_)})
    ph0, ph1 = mldsa65_sign(priv_h, fmh), sign_gpg(fmh)
    for gid, slot, s_, key, note in [
            ("P-H1", 0, ph0, spki_h, "kms possession: rule R (raw ML-DSA-65) over F_manifest M-H1"),
            ("P-H2", 1, ph1, (g2[0], g2[1], created), "gpg possession: rule O over F_manifest M-H1")]:
        check_possession(fmh, slot, s_, key)
        kin = {"spki_der_hex": H(spki_h)} if slot == 0 else keys_input["gpg"]
        hg.append({"id": gid, "kind": "possession", "note": note,
                   "input": {"manifest_hex": H(fmh), "slot": ["kms", "gpg"][slot], "key": kin}, "bytes_hex": H(s_)})

    # ---- HS-01: GENUINE V1 hybrid frames signed by both real keys (owner run of spike_v1_hybrid.py,
    # 2026-10-14 ~03:23Z). Exact bytes from the archived capture; nothing re-framed or re-signed. -------------
    v1cap_raw = open(v1cap_path, "rb").read()
    v1 = json.loads(v1cap_raw)
    assert v1["alg"] == ALG_HYBRID
    spki_g = b64(v1["spki_b64"])
    assert spki_g == spki_real                                         # the same KMS key as K-H2
    gk = (int(v1["gpg"]["x"], 16), int(v1["gpg"]["y"], 16), v1["gpg"]["created"])
    assert gk[:2] == gq and gk[2] == gcp_cap["key_created"]            # the same GCP HSM key as SIG-H7
    keys_g = {"kms": {"spki_der_hex": H(spki_g)},
              "gpg": {"x": f"{gk[0]:064x}", "y": f"{gk[1]:064x}", "created": gk[2]}}
    fm_g = bytes.fromhex(v1["manifest_hex"])
    mg = decode_frame(fm_g, T_MANIFEST)
    hg.append({"id": "M-G1", "kind": "frame-manifest",
               "note": "GENUINE: the hybrid manifest built from the two real spike keys and signed for possession by both",
               "input": {k: mg[k] for k in ("alg", "issuer", "key_fp", "sset")}, "bytes_hex": H(fm_g), "sha256": sha(fm_g)})
    gparts = {}
    for name, ids in (("small", ("F-G1", "F-G2")), ("big", ("F-G3", "F-G4"))):
        x = v1[name]
        f0g, s0g, f1g, s1g, ag = (bytes.fromhex(x[k]) for k in ("f0_hex", "s0_hex", "f1_hex", "s1_hex", "anchor_hex"))
        gparts[name] = (x["mode"], f0g, s0g, f1g, s1g, ag)
        for fid, f in zip(ids, (f0g, f1g)):
            vv = decode_frame(f, T_ATTEST)                                  # both frames decode as attest
            ctext = jcs(vv["common"]["content"]).decode("utf-8")
            hg.append({"id": fid, "kind": "frame-attest",
                       "note": f"GENUINE {name} frame ({len(f)} bytes), slot {'kms' if f is f0g else 'gpg'}, signed by the real key",
                       "input": {"common": common_input(vv["common"], ctext), "key_fp": vv["signer"]["key_fp"]},
                       "bytes_hex": H(f), "sha256": sha(f)})
    for sid, gid_o, name in (("SIG-G1", "SIG-G2", "small"), ("SIG-G3", "SIG-G4", "big")):
        mode, f0g, s0g, f1g, s1g, ag = gparts[name]
        check_signature_r(f0g, s0g, spki_g)
        v = {"id": sid, "kind": "signature-mldsa65",
             "note": ("GENUINE: real KMS EXTERNAL_MU signature over the real 6753-byte V1 attest frame F-G3 (the selected "
                      "issuer path); mu computed by the issuer from the raw 1952-byte key")
             if mode == "EXTERNAL_MU" else
             ("GENUINE, COMPARATIVE: real KMS RAW signature over the real 758-byte V1 attest frame F-G1. RAW is not the "
              "selected issuer path (owner decision 6: always EXTERNAL_MU); kept to show the two are interchangeable "
              "for the verifier"),
             "input": {"message_hex": H(f0g), "slot": "kms", "alg": ALG_HYBRID, "spki_der_hex": H(spki_g),
                       "mode": "kms-external-mu" if mode == "EXTERNAL_MU" else "kms-raw-comparative"},
             "bytes_hex": H(s0g), "verifies": True}
        if mode == "EXTERNAL_MU":
            v["input"]["mu_hex"] = H(mldsa65_external_mu(spki_g[22:], f0g))
        hg.append(v)
        assert verify_openpgp4(f1g, s1g, gk[:2])
        hg.append({"id": gid_o, "kind": "signature",
                   "note": f"GENUINE: real GCP HSM rule-O signature over the real {name} gpg frame (instrument-direct "
                           "gcloud call, not the deployed policy-signer path)",
                   "input": {"frame_hex": H(f1g), "slot": "gpg", "alg": ALG_HYBRID, "x": f"{gk[0]:064x}",
                             "y": f"{gk[1]:064x}", "created": gk[2]},
                   "bytes_hex": H(s1g), "verifies": True})
    for aid, rid_, name in (("A-G1", "R-G1", "small"), ("A-G2", "R-G2", "big")):
        mode, f0g, s0g, f1g, s1g, ag = gparts[name]
        assert ag == encode_anchor(f0g, s0g, f1g, s1g) and decode_anchor(ag) == [(f0g, s0g), (f1g, s1g)]
        hg.append({"id": aid, "kind": "anchor", "note": f"GENUINE {name} A_sig, as archived",
                   "input": {"f0_hex": H(f0g), "s0_hex": H(s0g), "f1_hex": H(f1g), "s1_hex": H(s1g)},
                   "bytes_hex": H(ag), "sha256": sha(ag)})
        check_receipt(fm_g, f0g, s0g, f1g, s1g, ag, keys_of_h(keys_g))
        hg.append({"id": rid_, "kind": "receipt",
                   "note": f"GENUINE {name} hybrid receipt (kms {mode}{' (comparative)' if mode == 'RAW' else ''}): codec "
                           "checks pass and both real committed signatures verify under the real slot keys",
                   "input": {"manifest_hex": H(fm_g), "f0_hex": H(f0g), "s0_hex": H(s0g), "f1_hex": H(f1g),
                             "s1_hex": H(s1g), "anchor_hex": H(ag), "keys": keys_g},
                   "anchor_sha256": sha(ag)})
    for pid, slot, hexkey in (("P-G1", 0, "kms_hex"), ("P-G2", 1, "gpg_hex")):
        sg_ = bytes.fromhex(v1["possession"][hexkey])
        check_possession(fm_g, slot, sg_, spki_g if slot == 0 else gk)
        hg.append({"id": pid, "kind": "possession",
                   "note": ("GENUINE kms possession over M-G1 (KMS RAW: COMPARATIVE, not the selected EXTERNAL_MU path)"
                            if slot == 0 else "GENUINE gpg possession over M-G1 (GCP HSM, instrument-direct)"),
                   "input": {"manifest_hex": H(fm_g), "slot": ["kms", "gpg"][slot], "key": keys_g[["kms", "gpg"][slot]]},
                   "bytes_hex": H(sg_)})

    # ---- rejections: hybrid A_sig codec (rule R lengths; wrong-slot rules) ----------------------------
    def rah(rid, data, code, note):
        expect_reject(lambda: decode_anchor(data), code)
        hr.append({"id": rid, "entry": "anchor", "input": {"bytes_hex": H(data)}, "expect": code, "note": note})

    ALG_NEAR = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384"     # well-formed, unregistered
    fn0 = encode_attest(common(alg=ALG_NEAR, mh=sha(fmh)), FP_H)
    fn1 = encode_attest(common(alg=ALG_NEAR, mh=sha(fmh)), FP_GPG)
    s_rule_o_kms = sign_kms(fh0)                                       # a rule-O packet over F-H1
    rah("XH-01", slots(fh0, sh0[:-1], fh1, sh1), "SIG_FORMAT", "rule R: ML-DSA-65 signature truncated to 3308 bytes (prefix consistent)")
    rah("XH-02", slots(fh0, sh0 + b"\x00", fh1, sh1), "LENGTH_CAP", "rule R: one trailing byte (3310 > the exact-length cap)")
    rah("XH-03", ah + bytes([2]) + P4(fh0) + struct.pack(">I", len(sh0) + 1) + sh0 + P4(fh1) + P4(sh1), "LENGTH_CAP",
        "rule R: slot length 3310 over a 3309-byte signature (the slot would swallow a prefix byte)")
    rah("XH-04", ah + bytes([2]) + P4(fh0) + struct.pack(">I", len(sh0) - 1) + sh0 + P4(fh1) + P4(sh1), "SIG_FORMAT",
        "rule R: slot length 3308; the signature's last byte would be read as the next prefix")
    rah("XH-05", slots(fh0, b"", fh1, sh1), "SIG_EMPTY", "rule R: empty signature")
    rah("XH-06", slots(fh0, sh0 + sh0, fh1, sh1), "LENGTH_CAP", "rule R: two signatures in the kms slot")
    rah("XH-07", slots(fh0, sh0[:2420], fh1, sh1), "SIG_FORMAT", "rule R: an ML-DSA-44-sized signature (2420 bytes)")
    rah("XH-08", slots(fh0, sh0 + sh0[:1318], fh1, sh1), "LENGTH_CAP", "rule R: an ML-DSA-87-sized signature (4627 bytes)")
    rah("XH-09", slots(fh0, s_rule_o_kms, fh1, sh1), "SIG_FORMAT",
        "wrong-slot rule: a valid OpenPGP P-256 packet in the kms slot under the hybrid id (rule R wants 3309 raw bytes)")
    rah("XH-10", slots(fh0, sh0, fh1, sh0), "LENGTH_CAP",
        "wrong-slot rule: an ML-DSA-65 signature in the gpg slot under the hybrid id (rule O cap 1024)")
    rah("XH-11", slots(fh0, sh1, fh1, sh0), "SIG_FORMAT", "the two slots' signatures swapped: kms holds a 119-byte packet")
    rah("XH-12", slots(f0, sh0, f1, s1), "LENGTH_CAP",
        "wrong id: an ML-DSA-65 signature in the kms slot of classical-id frames (rule O cap 1024)")
    rah("XH-13", slots(fh0, base64.b64encode(sh0), fh1, sh1), "LENGTH_CAP", "rule R: base64 text of the signature (4412 bytes)")
    rah("XH-14", slots(fn0, b"\x00" * (SIG_CAP_OPAQUE + 1), fn1, sh1), "LENGTH_CAP",
        "unknown id (near-miss pair id ending SHA384): opaque codec, cap 65536")

    # ---- rejections: hybrid receipts (codec, keys, verification of the committed signatures) --------
    stamped_h = sha(anch)

    def rrh(rid, m, a, sa, b, sb, p, code, note, ki=keys_h, control=None, gate_off=None, decoder_failure=False):
        """gate_off: the kms signature is valid except for that one FIPS 204 decoding gate (asserted here: A
        accepts it with only that gate disabled). decoder_failure: the hint field cannot be decoded at all
        (asserted here: A rejects it even with every disable-able gate off)."""
        expect_reject(lambda: check_receipt(m, a, sa, b, sb, p, keys_of_h(ki)), code)
        v = {"id": rid, "entry": "receipt",
             "input": {"manifest_hex": H(m), "f0_hex": H(a), "s0_hex": H(sa), "f1_hex": H(b), "s1_hex": H(sb),
                       "anchor_hex": H(p), "keys": ki},
             "expect": code, "note": note}
        if control is not None:
            assert control == "kms" and mldsa65_verify(pk_h, a, sa), rid
            assert sha(encode_anchor(a, sa, b, sb)) != stamped_h, rid
            v["control"] = {"slot": control, "presented_sig_verifies": True, "stamped_anchor_sha256": stamped_h}
        if gate_off is not None:
            assert not mldsa65_verify(pk_h, a, sa) and mldsa65_verify(pk_h, a, sa, _off=(gate_off,)), rid
            v["demonstration"] = {"slot": "kms", "gate_off": gate_off, "accepts_with_only_that_gate_off": True}
        if decoder_failure:
            assert not mldsa65_verify(pk_h, a, sa, _off=("norm", "order", "padding")), rid
            v["decoder_failure"] = True
        hr.append(v)

    sh0_hedged = mldsa65_sign(priv_h, fh0, rnd=hashlib.sha256(b"hedged signing randomness, illustrative").digest())
    assert sh0_hedged != sh0
    rrh("XHR-01", fmh, fh0, sh0_hedged, fh1, sh1, anch, "RECEIPT_ANCHOR_MISMATCH",
        "NEGATIVE CONTROL: a second valid ML-DSA-65 signature over F-H1 (hedged rnd); it verifies, but the stamp commits "
        "SIG-H1", control="kms")
    s_other = mldsa65_sign(priv_h, fh1)
    rrh("XHR-02", fmh, fh0, s_other, fh1, sh1, encode_anchor(fh0, s_other, fh1, sh1), "SIG_INVALID",
        "kms slot holds a valid ML-DSA-65 signature over the gpg frame F-H2 (anchor rebuilt): not over its own frame")
    flip = bytearray(sh0)
    flip[0] ^= 1
    rrh("XHR-03", fmh, fh0, bytes(flip), fh1, sh1, encode_anchor(fh0, bytes(flip), fh1, sh1), "SIG_INVALID",
        "one bit of the ML-DSA-65 commitment hash c~ flipped (anchor rebuilt): codec accepts, verification fails")
    hb = bytearray(sh0)
    hint_at = 48 + 3200
    cnt = hb[hint_at + 55]                                                   # hints in the first polynomial
    assert cnt >= 2
    hb[hint_at], hb[hint_at + 1] = hb[hint_at + 1], hb[hint_at]              # positions out of order
    rrh("XHR-04", fmh, fh0, bytes(hb), fh1, sh1, encode_anchor(fh0, bytes(hb), fh1, sh1), "SIG_INVALID",
        "hint positions out of order (FIPS 204 HintBitUnpack returns failure): a verification failure, not SIG_FORMAT; "
        "accepted with only the order gate off", gate_off="order")
    zb = bytearray(sh0)
    zb[48:51] = b"\x00\x00\x00"                                              # first z coefficient field = 0: z = gamma1
    rrh("XHR-05", fmh, fh0, bytes(zb), fh1, sh1, encode_anchor(fh0, bytes(zb), fh1, sh1), "SIG_INVALID",
        "a z coefficient at gamma1 (infinity-norm bound fails): a verification failure, not SIG_FORMAT")
    s_big_z = mldsa65_sign_mu(priv_h, mldsa65_external_mu(pk_h, fh0), _large_z=True)
    assert mldsa65_verify(pk_h, fh0, s_big_z, _off=("norm",)) and not mldsa65_verify(pk_h, fh0, s_big_z)
    rrh("XHR-12", fmh, fh0, s_big_z, fh1, sh1, encode_anchor(fh0, s_big_z, fh1, sh1), "SIG_INVALID",
        "z infinity norm at or above gamma1 - beta, every other verification step consistent (made from a signing "
        "iteration FIPS 204 rejects): isolates the verifier's norm bound", gate_off="norm")
    p256_spki_hex = H(spki_der(pt_kms))
    rrh("XHR-06", fmh, fh0, sh0, fh1, sh1, anch, "KEY_FORMAT", "a P-256 SPKI presented as the kms key under the hybrid id",
        ki={"kms": {"spki_der_hex": p256_spki_hex}, "gpg": keys_input["gpg"]})
    rrh("XHR-07", fmh, fh0, sh0, fh1, sh1, anch, "KEY_MISMATCH",
        "a well-formed ML-DSA-65 SPKI (the real KMS key) that is not the manifest's kms key",
        ki={"kms": {"spki_der_hex": H(spki_real)}, "gpg": keys_input["gpg"]})
    fmix1 = encode_attest(C0 | {"manifest_sha256": sha(fmh)}, FP_GPG)
    smix1 = sign_gpg(fmix1)
    rrh("XHR-08", fmh, fh0, sh0, fmix1, smix1, encode_anchor(fh0, sh0, fmix1, smix1), "RECEIPT_COMMON_MISMATCH",
        "each slot labelled with its own scheme's id (kms frame: pair id; gpg frame: the classical id), the M9 shape: "
        "common.alg differs, so R-3.12 fails")
    fmn = encode_manifest(ALG_NEAR, D, FP_H, FP_GPG)
    fn0m = encode_attest(common(alg=ALG_NEAR, mh=sha(fmn)), FP_H)
    fn1m = encode_attest(common(alg=ALG_NEAR, mh=sha(fmn)), FP_GPG)
    sn0m, sn1m = mldsa65_sign(priv_h, fn0m), sign_gpg(fn1m)
    rrh("XHR-09", fmn, fn0m, sn0m, fn1m, sn1m, encode_anchor(fn0m, sn0m, fn1m, sn1m), "UNVERIFIABLE",
        "unknown id: a near-miss pair id (SHA384); the codec takes both signatures as opaque, stage (c) gives UNVERIFIABLE")
    rrh("XHR-10", fmh, fh0, sh0, fh1, sh1, encode_anchor(fh0, sh0, fh1, s1), "RECEIPT_ANCHOR_MISMATCH",
        "anchor commits another gpg signature (SIG-02 over the classical F-02)")
    rrh("XHR-11", fmh, fh0, sb0, fh1, sh1, encode_anchor(fh0, sb0, fh1, sh1), "SIG_INVALID",
        "kms slot holds the external-mu signature over F-H3, presented over F-H1 (anchor rebuilt)")

    # ---- HS-03 (Codex review 2026-10-14): wrong mode / context / mu domain; hint-decoding gates ------------
    # Each mode variant is a VALID FIPS 204 signature by the same key, under a different message representative.
    CTX = b"tessera-v1"
    OID_SHA256 = bytes.fromhex("0609608648016503040201")
    mode_variants = [
        ("ctx", "pure ML-DSA with the NONEMPTY context 'tessera-v1' (M' = 00 || 0a || ctx || F)",
         lambda F: b"\x00" + bytes([len(CTX)]) + CTX + F),
        ("hash", "HashML-DSA with SHA-256, empty context (M' = 01 || 00 || OID(SHA-256) || SHA256(F))",
         lambda F: b"\x01\x00" + OID_SHA256 + hashlib.sha256(F).digest()),
        ("noprefix", "mu computed WITHOUT the pure-mode prefix 00 00 (mu = SHAKE256(tr || F))", lambda F: F)]

    def sign_variant(mprime_of, F):
        mu_v = _mldsa_h(priv_h[5] + mprime_of(F), 64)
        s_v = mldsa65_sign_mu(priv_h, mu_v)
        assert mldsa65_verify_mu(pk_h, mu_v, s_v) and not mldsa65_verify(pk_h, F, s_v)
        return s_v

    mode_sigs = {}
    for n_, (tag_, desc, mp) in enumerate(mode_variants):
        sv = sign_variant(mp, fh0)
        mode_sigs[tag_] = sv
        rrh(f"XHR-{13 + n_}", fmh, fh0, sv, fh1, sh1, encode_anchor(fh0, sv, fh1, sh1), "SIG_INVALID",
            f"kms slot: a valid signature by the slot key over F-H1 under {desc}; anchor rebuilt, so the failure is "
            "verification, not anchor mismatch")
    hint_at = 48 + 3200

    def hint_lists(sig):
        h_ = sig[hint_at:]
        out, prev = [], 0
        for i in range(MLDSA_K):
            out.append(list(h_[prev:h_[MLDSA_OMEGA + i]]))
            prev = h_[MLDSA_OMEGA + i]
        return out

    def with_hints(sig, lists, pad=None):
        y, idx = bytearray(MLDSA_OMEGA + MLDSA_K), 0
        for i, lst in enumerate(lists):
            for j in lst:
                y[idx] = j
                idx += 1
            y[MLDSA_OMEGA + i] = idx
        if pad is not None:
            y[idx] = pad
        return sig[:hint_at] + bytes(y)

    hl = hint_lists(sh0)
    assert with_hints(sh0, hl) == sh0 and sum(map(len, hl)) <= MLDSA_OMEGA - 1
    i_d = next(i for i, l_ in enumerate(hl) if l_)
    dup = [list(l_) for l_ in hl]
    dup[i_d].insert(1, dup[i_d][0])
    s_dup = with_hints(sh0, dup)
    rrh("XHR-16", fmh, fh0, s_dup, fh1, sh1, encode_anchor(fh0, s_dup, fh1, sh1), "SIG_INVALID",
        "duplicate hint index in one polynomial (same hint vector, one more entry): accepted with only the order gate "
        "off", gate_off="order")
    s_pad = with_hints(sh0, hl, pad=1)
    rrh("XHR-17", fmh, fh0, s_pad, fh1, sh1, encode_anchor(fh0, s_pad, fh1, sh1), "SIG_INVALID",
        "nonzero unused hint padding byte (hint vector unchanged): accepted with only the padding gate off",
        gate_off="padding")
    over = bytearray(sh0)
    over[hint_at + MLDSA_OMEGA + MLDSA_K - 1] = MLDSA_OMEGA + 1
    rrh("XHR-18", fmh, fh0, bytes(over), fh1, sh1, encode_anchor(fh0, bytes(over), fh1, sh1), "SIG_INVALID",
        "cumulative hint count 56, above omega = 55: the hint field cannot be decoded", decoder_failure=True)
    dec = bytearray(sh0)
    i_c = next(i for i in range(MLDSA_K - 1) if dec[hint_at + MLDSA_OMEGA + i] > 0)
    dec[hint_at + MLDSA_OMEGA + i_c + 1] = dec[hint_at + MLDSA_OMEGA + i_c] - 1
    rrh("XHR-19", fmh, fh0, bytes(dec), fh1, sh1, encode_anchor(fh0, bytes(dec), fh1, sh1), "SIG_INVALID",
        "cumulative hint counts decrease from one polynomial to the next: the hint field cannot be decoded",
        decoder_failure=True)

    # ---- rejections: the kms slot's key encoding (hybrid id) -------------------------------------------
    def rk(rid, der_bytes, code, note, want=FP_H):
        expect_reject(lambda: check_key_kms(der_bytes, want), code)
        hr.append({"id": rid, "entry": "key-kms", "input": {"spki_der_hex": H(der_bytes), "key_fp": want},
                   "expect": code, "note": note})

    def spki_with(oid_last, key_len, params=b"", unused=0, outer_len=None):
        alg_id = bytes([0x30, 11 + len(params), 0x06, 0x09]) + bytes.fromhex("6086480165030403") + bytes([oid_last]) + params
        bit = bytes([0x03, 0x82]) + (key_len + 1).to_bytes(2, "big") + bytes([unused]) + pk_h[:key_len].ljust(key_len, b"\x01")
        body = alg_id + bit
        return bytes([0x30, 0x82]) + (len(body) if outer_len is None else outer_len).to_bytes(2, "big") + body

    assert spki_with(0x12, 1952) == spki_h                                   # the constructor reproduces the exact SPKI
    rk("XK-01", spki_der(pt_kms), "KEY_FORMAT", "a P-256 SPKI (the fallback's kms key form)")
    rk("XK-02", spki_with(0x11, 1312), "KEY_FORMAT", "ML-DSA-44 SPKI (OID ...3.17, 1312-byte key)")
    rk("XK-03", spki_with(0x13, 2592), "KEY_FORMAT", "ML-DSA-87 SPKI (OID ...3.19, 2592-byte key)")
    rk("XK-04", spki_with(0x11, 1952), "KEY_FORMAT", "ML-DSA-44 OID over a 1952-byte key (wrong OID, right length)")
    rk("XK-05", spki_with(0x12, 1952, params=b"\x05\x00"), "KEY_FORMAT",
       "AlgorithmIdentifier with NULL parameters (must be absent)")
    rk("XK-06", spki_h[:-1], "KEY_FORMAT", "truncated by one byte")
    rk("XK-07", spki_h + b"\x00", "KEY_FORMAT", "one trailing byte")
    rk("XK-08", bytes([0x30, 0x83, 0x00]) + spki_h[2:], "KEY_FORMAT", "outer SEQUENCE length in non-minimal long form")
    rk("XK-09", spki_with(0x12, 1952, unused=1), "KEY_FORMAT", "BIT STRING with a nonzero unused-bits octet")
    rk("XK-10", pk_h, "KEY_FORMAT", "the bare 1952-byte FIPS 204 public key, no SPKI")
    pem = ("-----BEGIN PUBLIC KEY-----\n" + "\n".join(base64.b64encode(spki_h).decode()[i:i + 64]
                                                     for i in range(0, 2632, 64)) + "\n-----END PUBLIC KEY-----\n").encode()
    rk("XK-11", pem, "KEY_FORMAT", "PEM text of the exact SPKI")
    rk("XK-12", bytes([0x30, 0x80]) + spki_h[4:] + b"\x00\x00", "KEY_FORMAT", "outer SEQUENCE with BER indefinite length")
    rk("XK-13", spki_real, "KEY_MISMATCH", "a well-formed ML-DSA-65 SPKI whose spki-sha256 is not the slot's fingerprint")

    # ---- rejections: manifest possession (both slots, hybrid id) ---------------------------------------
    def rp(rid, slot, s_, key, code, note, m=fmh):
        k = (spki_h if slot == 0 else (g2[0], g2[1], created)) if key is None else key
        expect_reject(lambda: check_possession(m, slot, s_, k), code)
        kin = ({"spki_der_hex": H(k)} if slot == 0 else {"x": f"{k[0]:064x}", "y": f"{k[1]:064x}", "created": k[2]})
        hr.append({"id": rid, "entry": "possession",
                   "input": {"manifest_hex": H(m), "slot": ["kms", "gpg"][slot], "key": kin, "sig_hex": H(s_)},
                   "expect": code, "note": note})

    rp("XP-01", 0, sh0, None, "POSSESSION_INVALID", "kms possession is SIG-H1, a signature over the attest frame F-H1, not F_manifest")
    rp("XP-02", 1, sh1, None, "POSSESSION_INVALID", "gpg possession is SIG-H2, over F-H2, not F_manifest")
    rp("XP-03", 0, ph0[:-1], None, "SIG_FORMAT", "kms possession truncated to 3308 bytes")
    rp("XP-04", 1, ph0, None, "LENGTH_CAP", "wrong-slot rule: the ML-DSA-65 possession presented for the gpg slot")
    rp("XP-05", 0, ph1, None, "SIG_FORMAT", "wrong-slot rule: the rule-O possession presented for the kms slot")
    rp("XP-06", 0, ph0, spki_real, "KEY_MISMATCH", "kms possession checked under a key that is not the manifest's")
    rp("XP-07", 0, ph0, spki_der(pt_kms), "KEY_FORMAT", "kms possession checked under a P-256 SPKI")
    php = mldsa65_sign(priv_h, fm)
    rp("XP-08", 0, php, None, "POSSESSION_INVALID", "kms possession over the classical manifest M-01, presented for M-H1")
    for n_, (tag_, desc, mp) in enumerate(mode_variants):            # HS-03: wrong mode / context / mu domain
        rp(f"XP-{9 + n_:02d}", 0, sign_variant(mp, fmh), None, "POSSESSION_INVALID",
           f"kms possession: a valid signature by the slot key over F_manifest M-H1 under {desc}")

    # ---- rejections: the real KMS signatures, standalone ----------------------------------------------
    def rsr(rid, msg, s_, code, note, spki_=spki_real):
        expect_reject(lambda: check_signature_r(msg, s_, spki_), code)
        hr.append({"id": rid, "entry": "signature-r",
                   "input": {"message_hex": H(msg), "sig_hex": H(s_), "spki_der_hex": H(spki_)},
                   "expect": code, "note": note})

    rsr("XM-01", small[:-1] + bytes([small[-1] ^ 1]), s_raw, "SIG_INVALID", "real KMS RAW signature over its frame with the last byte changed")
    rsr("XM-02", small, s_mu, "SIG_INVALID", "real KMS EXTERNAL_MU signature checked over the other (small) frame")
    rsr("XM-03", small, s_raw[:-1], "SIG_FORMAT", "real KMS RAW signature truncated by one byte")
    rsr("XM-04", small, s_raw + b"\x00", "LENGTH_CAP", "real KMS RAW signature with one trailing byte")
    rsr("XM-05", mldsa65_external_mu(spki_real[22:], big), s_mu, "SIG_INVALID",
        "the EXTERNAL_MU signature checked over mu itself: the signed message is the frame, never mu")
    rsr("XM-06", small, s_raw, "KEY_FORMAT", "real KMS RAW signature with the SPKI's OID changed to ML-DSA-44",
        spki_=spki_real[:16] + b"\x11" + spki_real[17:])

    # ---- write the hybrid files --------------------------------------------------------------------
    hmeta = dict(meta, generator=meta["generator"] + "; hybrid section",
                 supplement="formal/p8/HYBRID-SUPPLEMENT-DRAFT.md", alg=ALG_HYBRID,
                 kms_capture_sha256=sha(kms_cap_raw), gcp_capture_sha256=sha(gcp_cap_raw),
                 v1_hybrid_capture_sha256=sha(v1cap_raw))
    with open(os.path.join(here, "hybrid-golden.json"), "w") as fh:
        json.dump({"meta": hmeta, "vectors": hg}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    with open(os.path.join(here, "hybrid-reject.json"), "w") as fh:
        json.dump({"meta": hmeta, "vectors": hr}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"implementation A (hybrid): {len(hg)} golden vectors, {len(hr)} rejection vectors; all self-checks pass")


if __name__ == "__main__":
    main()
