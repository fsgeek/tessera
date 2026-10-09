"""Item 1: the canonical form against RFC 8785 (JCS) and RFC 7493 (I-JSON). THROWAWAY.

What the spec names (§3.1 R-3.1, R-3.2, R-3.4; prereg §4.3): RFC 8785, "adopted with the precision
rule closing its gap", the rule being "any value not exactly a double (hashes, large/256-bit integers,
blockchain addresses, opaque identifiers) is string-encoded". R-3.4 then lists "numbers not exactly
representable as IEEE 754 doubles" among the inputs that must be REJECTED.

What RFC 8785 actually does (§3.2.2.3): every JSON number is parsed into an IEEE 754 double (the
I-JSON number model, RFC 7493 §2.2) and serialized with the ECMAScript Number-to-String algorithm
(shortest round-trip digits). So 9.8 has a canonical form, "9.8", although the decimal 9.8 is not
exactly a double: JCS never needed a number to be *exactly* a double, only that its *value* survive
the trip through one. JCS also rewrites number spellings ("9.80" -> "9.8", "1E2" -> "100",
"-0" -> "0"): it is itself a normalizing function on lexical form.

Three readings of the precision rule, all of which a builder could defend:

  literal           phase 1 (G-03): the decimal literal must equal a double exactly. Rejects 9.8, 0.1,
                    every decimal CVSS score; accepts nothing RFC 8785's own Appendix B uses for
                    fractional values except dyadic ones.
  value-preserving  the RFC 8785 / I-JSON reading: accept iff Decimal(literal) == Decimal(ES6(double)),
                    i.e. canonicalization does not change the number's value. Accepts 9.8 and 9.80
                    (same value), rejects 333333333.33333329 (JCS would silently change the value) and
                    2**53+1. This is what the examples in the precision rule are about.
  safe-integer      the Trail of Bits `rfc8785` package's domain: integers outside +-(2**53-1) refused
                    even when exactly representable (123456789012345680000 is a double), any finite
                    float accepted and silently rounded (333333333.33333329 -> 333333333.3333333).

`value-preserving` is the reading this module recommends and the de-stubbed path uses. Under it the
phase-2 SBOM (CVSS 9.8) is accepted and canonicalizes to "9.8".
"""
from __future__ import annotations

import contextlib
import json
import math
import struct
from decimal import Decimal

from .. import jcs
from ..jcs import CanonicalizationRejected

RULES = ("literal", "value-preserving", "safe-integer")
MAX_SAFE = 2**53 - 1


def _es6(x: float) -> str:
    return jcs._es_number(x)


def parse_number(lit: str, rule: str) -> float:
    """Parse one JSON number literal under `rule`; return the double or raise CanonicalizationRejected."""
    lit = lit.strip()
    is_int = not any(c in lit for c in ".eE")
    f = float(lit)
    if math.isinf(f) or math.isnan(f):
        raise CanonicalizationRejected("P8_NUMBER_NOT_DOUBLE", lit)
    if f == 0.0 and lit.startswith("-"):
        # R-3.4 rejects -0 explicitly. RFC 8785 would serialize it as "0": a Tessera rule ON TOP of JCS.
        raise CanonicalizationRejected("P8_NEGATIVE_ZERO", lit)
    if rule == "literal":
        if Decimal(f) != Decimal(lit):
            raise CanonicalizationRejected("P8_NUMBER_NOT_DOUBLE", lit)
        return f
    if rule == "value-preserving":
        if Decimal(_es6(f)) != Decimal(lit):
            raise CanonicalizationRejected("P8_NUMBER_VALUE_NOT_PRESERVED", lit)
        return f
    if rule == "safe-integer":
        if is_int and abs(int(lit)) > MAX_SAFE:
            raise CanonicalizationRejected("P8_INTEGER_OUTSIDE_SAFE_RANGE", lit)
        return f
    raise ValueError(rule)


@contextlib.contextmanager
def number_rule(rule: str):
    """Temporarily switch the prototype's JCS number domain (phase-1 default: 'literal')."""
    assert rule in RULES
    old = jcs.NUMBER_RULE
    jcs.NUMBER_RULE = rule
    try:
        yield
    finally:
        jcs.NUMBER_RULE = old


def set_number_rule(rule: str) -> str:
    assert rule in RULES
    old, jcs.NUMBER_RULE = jcs.NUMBER_RULE, rule
    return old


# RFC 8785 Appendix B: IEEE 754 bit patterns and their required ES6 serializations (a subset).
RFC8785_APPENDIX_B = [
    ("0000000000000000", "0"),
    ("8000000000000000", "0"),            # -0 serializes as "0" in JCS; Tessera rejects -0 on INPUT
    ("0000000000000001", "5e-324"),       # a subnormal: phase 1's G-03b rejects this as input
    ("8000000000000001", "-5e-324"),
    ("7fefffffffffffff", "1.7976931348623157e+308"),
    ("ffefffffffffffff", "-1.7976931348623157e+308"),
    ("4340000000000000", "9007199254740992"),
    ("c340000000000000", "-9007199254740992"),
    ("4430000000000000", "295147905179352830000"),
    ("44b52d02c7e14af5", "9.999999999999997e+22"),
    ("44b52d02c7e14af6", "1e+23"),
    ("44b52d02c7e14af7", "1.0000000000000001e+23"),
    ("444b1ae4d6e2ef4e", "999999999999999700000"),
    ("444b1ae4d6e2ef4f", "999999999999999900000"),
    ("444b1ae4d6e2ef50", "1e+21"),
    ("3eb0c6f7a0b5ed8c", "9.999999999999997e-7"),
    ("3eb0c6f7a0b5ed8d", "0.000001"),
    ("41b3de4355555553", "333333333.3333332"),
    ("41b3de4355555554", "333333333.33333325"),
    ("41b3de4355555555", "333333333.3333333"),
    ("41b3de4355555556", "333333333.3333334"),
    ("41b3de4355555557", "333333333.33333343"),
    ("becbf647612f3696", "-0.0000033333333333333333"),
    ("43143ff3c1cb0959", "1424953923781206.2"),
]


def double_from_bits(h: str) -> float:
    return struct.unpack(">d", bytes.fromhex(h))[0]


def appendix_b_results() -> list[tuple[str, str, str, str]]:
    """(bits, expected, prototype serializer, rfc8785 package) for every vector."""
    try:
        import rfc8785
    except ImportError:  # pragma: no cover
        rfc8785 = None
    out = []
    for bits, want in RFC8785_APPENDIX_B:
        x = double_from_bits(bits)
        mine = _es6(x) if not (x == 0 and math.copysign(1, x) < 0) else "0 (prototype raises on -0)"
        ref = rfc8785.dumps(x).decode() if rfc8785 else "n/a"
        out.append((bits, want, mine, ref))
    return out


def classify(literals: list[str]) -> dict[str, dict[str, str]]:
    """For each literal: what each reading does with it, and what the `rfc8785` package does."""
    import rfc8785
    res = {}
    for lit in literals:
        row = {}
        for rule in RULES:
            with number_rule(rule):
                try:
                    row[rule] = jcs.canonicalize_text(('{"n":' + lit + "}").encode()).decode()[5:-1]
                except CanonicalizationRejected as e:
                    row[rule] = "REJECT " + e.code
        try:
            row["rfc8785-package"] = rfc8785.dumps(json.loads(lit)).decode()
        except Exception as e:  # noqa: BLE001
            row["rfc8785-package"] = "REJECT " + type(e).__name__
        res[lit] = row
    return res


PROBE_LITERALS = ["9.8", "9.80", "0.1", "1E2", "1e21", "5e-324", "333333333.33333329", "9007199254740993",
                  "123456789012345680000", "-0", "0.30000000000000004"]
