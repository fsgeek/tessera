"""RFC 8785 (JCS) canonicalization with the P8 rejection list (spec §3.1, R-3.1..R-3.4, R-4.2).

THROWAWAY PROTOTYPE. Every place this file had to decide something the spec does not
determine is tagged `GUESS G-nn`; see GUESSES.md.
"""
from __future__ import annotations

import json
import math
import unicodedata
from decimal import Decimal


class CanonicalizationRejected(ValueError):
    """Input is outside the accepted domain (R-3.4). Never normalized, always refused."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


# --- parsing with the rejection list -------------------------------------------------------

def _reject_constant(name: str):
    raise CanonicalizationRejected("P8_NAN_INFINITY", name)


def _no_dup_pairs(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise CanonicalizationRejected("P8_DUPLICATE_NAME", repr(k))
        _check_string(k)
        seen[k] = v
    return seen


def _check_string(s: str) -> None:
    for ch in s:
        cp = ord(ch)
        # GUESS G-04: "non-I-JSON strings" read as RFC 7493 §2.1: no surrogates, no noncharacters.
        if 0xD800 <= cp <= 0xDFFF:
            raise CanonicalizationRejected("P8_NON_IJSON_STRING", f"surrogate U+{cp:04X}")
        if (0xFDD0 <= cp <= 0xFDEF) or (cp & 0xFFFE) == 0xFFFE:
            raise CanonicalizationRejected("P8_NON_IJSON_STRING", f"noncharacter U+{cp:04X}")
    # GUESS G-05: "inputs relying on Unicode normalization assumptions" read as: any string
    # (member names included) that is not already in NFC is rejected.
    if unicodedata.normalize("NFC", s) != s:
        raise CanonicalizationRejected("P8_UNICODE_NORMALIZATION", repr(s))


# PHASE 3 hook (tessera_proto/real/canonical.py): which reading of R-3.4's "numbers not exactly
# representable as IEEE 754 doubles" is in force. "literal" is phase 1's G-03 and stays the default;
# "value-preserving" is the RFC 8785 / I-JSON reading (accept iff the number's decimal VALUE survives
# parse-to-double-then-serialize). Set only through real.canonical.number_rule().
NUMBER_RULE = "literal"


def _parse_float(lit: str):
    if NUMBER_RULE != "literal":
        from .real.canonical import parse_number
        return parse_number(lit, NUMBER_RULE)
    d = Decimal(lit)
    f = float(lit)
    if math.isinf(f) or math.isnan(f):
        raise CanonicalizationRejected("P8_NUMBER_NOT_DOUBLE", lit)
    if f == 0.0 and (lit.lstrip().startswith("-")):
        raise CanonicalizationRejected("P8_NEGATIVE_ZERO", lit)
    # GUESS G-03: "numbers not exactly representable as IEEE 754 doubles" read LITERALLY:
    # the decimal literal must equal the double exactly. This rejects 0.1 (which must then be
    # string-encoded per R-3.2). The weaker "round-trips" reading would accept 0.1.
    if Decimal(f) != d:
        raise CanonicalizationRejected("P8_NUMBER_NOT_DOUBLE", lit)
    # GUESS G-03b: "numeric edge cases" read as: subnormals rejected too.
    if f != 0.0 and abs(f) < 2.2250738585072014e-308:
        raise CanonicalizationRejected("P8_NUMERIC_EDGE_CASE", lit)
    return f


def _parse_int(lit: str):
    if NUMBER_RULE != "literal":
        from .real.canonical import parse_number
        return parse_number(lit, NUMBER_RULE)
    n = int(lit)
    if lit.lstrip().startswith("-") and n == 0:
        raise CanonicalizationRejected("P8_NEGATIVE_ZERO", lit)
    f = float(n)
    if math.isinf(f) or int(f) != n:
        raise CanonicalizationRejected("P8_NUMBER_NOT_DOUBLE", lit)
    return f  # JCS has one number type; keep it a double


def parse_strict(data: bytes):
    """Parse UTF-8 JSON bytes, refusing everything outside the accepted domain."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalizationRejected("P8_TRAILING_OR_LEADING_BYTES", "BOM")  # GUESS G-06
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        raise CanonicalizationRejected("P8_NOT_UTF8", str(e)) from None
    try:
        value = json.loads(
            text,
            object_pairs_hook=_no_dup_pairs,
            parse_constant=_reject_constant,
            parse_float=_parse_float,
            parse_int=_parse_int,
        )
    except CanonicalizationRejected:
        raise
    except json.JSONDecodeError as e:
        code = "P8_TRAILING_BYTES" if "Extra data" in str(e) else "P8_MALFORMED_JSON"
        raise CanonicalizationRejected(code, str(e)) from None
    _walk_strings(value)
    return value


def _walk_strings(v):
    if isinstance(v, str):
        _check_string(v)
    elif isinstance(v, list):
        for x in v:
            _walk_strings(x)
    elif isinstance(v, dict):
        for k, x in v.items():
            _check_string(k)
            _walk_strings(x)


# --- serialization (RFC 8785 §3.2) ---------------------------------------------------------

def _es_number(x: float) -> str:
    if math.isnan(x) or math.isinf(x):
        raise CanonicalizationRejected("P8_NAN_INFINITY", repr(x))
    if x == 0.0:
        if math.copysign(1.0, x) < 0:
            raise CanonicalizationRejected("P8_NEGATIVE_ZERO", "-0")
        return "0"
    sign = "-" if x < 0 else ""
    t = Decimal(repr(abs(x))).normalize().as_tuple()
    digits = "".join(map(str, t.digits))
    k = len(digits)
    n = k + t.exponent
    if k <= n <= 21:
        s = digits + "0" * (n - k)
    elif 0 < n <= 21:
        s = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        s = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        s = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + ("+" if e >= 0 else "-") + str(abs(e))
    return sign + s


_ESC = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\f": "\\f", "\n": "\\n", "\r": "\\r", "\t": "\\t"}


def _es_string(s: str) -> str:
    _check_string(s)
    out = ['"']
    for ch in s:
        if ch in _ESC:
            out.append(_ESC[ch])
        elif ord(ch) < 0x20:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _ser(v) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return _es_number(_parse_int(str(v)))
    if isinstance(v, float):
        return _es_number(v)
    if isinstance(v, str):
        return _es_string(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(_ser(x) for x in v) + "]"
    if isinstance(v, dict):
        for k in v:
            if not isinstance(k, str):
                raise CanonicalizationRejected("P8_MALFORMED_JSON", f"non-string key {k!r}")
        keys = sorted(v.keys(), key=lambda k: k.encode("utf-16-be"))
        return "{" + ",".join(_es_string(k) + ":" + _ser(v[k]) for k in keys) + "}"
    raise CanonicalizationRejected("P8_MALFORMED_JSON", f"type {type(v).__name__}")


def canonicalize(value) -> bytes:
    """JCS bytes of an in-memory JSON value (already inside the domain)."""
    return _ser(value).encode("utf-8")


def canonicalize_text(data: bytes) -> bytes:
    """Ingestion boundary: strict-parse submitted JSON bytes, then JCS them."""
    return canonicalize(parse_strict(data))


def is_canonical(data: bytes) -> bool:
    """Verifier side (V6): bytes are inside the domain AND already canonical."""
    return canonicalize(parse_strict(data)) == data
