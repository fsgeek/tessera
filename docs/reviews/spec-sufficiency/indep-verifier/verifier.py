"""Throwaway spec-sufficiency probe, not a conforming V1 verifier.

Only the four documents named in GAPS.md supplied protocol requirements.
The CLI consumes raw objects, NOT an invented Tessera bundle container.
No path through this program returns VALID_STRICT.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

PROFILE = "tessera-v1-strict"
CLASSICAL = "OPENPGP4-ECDSA-P256-SHA256"
ATTEST = b"tessera-v1/attest"
MANIFEST = b"tessera-v1/manifest"
ANCHOR = b"tessera-v1/receipt-anchor-sig"
SNAPSHOT = b"tessera-v1/dnssec-snapshot"
TAGS = {ATTEST, MANIFEST, ANCHOR, SNAPSHOT}
CAP = 1 << 24
HEX = r"[0-9a-f]{64}"
ALG = r"[A-Z0-9][A-Z0-9-]{0,63}"
FP = r"(?:spki|gpg)-sha256:" + HEX


class Reject(Exception):
    """A specified failure in the implemented portion of the codec."""


class Stop(Exception):
    """Probe limitation or spec gap; never silently converted to a V1 verdict."""


class Pairs(list):
    """Preserve duplicate object members until their rejection category."""


@dataclass(frozen=True)
class Number:
    literal: str


def require(condition, reason):
    if not condition:
        raise Reject(reason)


def matches(pattern, value):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def utc(value):
    require(matches(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value), "SCHEMA")
    try:
        # Deliberate year choice: Gregorian years 0001..9999 (GAPS G18).
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        raise Reject("SCHEMA") from None


def domain(value):
    if not isinstance(value, str) or len(value) > 241:
        return False
    labels = value.split(".")
    return len(labels) >= 2 and all(matches(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", x) for x in labels)


def closed(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()), "SCHEMA")


def jcs_without_numbers(value):
    """Exact E §1.3 serialization for the implemented, number-free domain."""
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if isinstance(value, list):
        return b"[" + b",".join(jcs_without_numbers(x) for x in value) + b"]"
    if isinstance(value, dict):
        keys = sorted(value, key=lambda k: k.encode("utf-16-be"))
        return b"{" + b",".join(jcs_without_numbers(k) + b":" + jcs_without_numbers(value[k]) for k in keys) + b"}"
    raise Stop("NUMBER_FORMATTING_NOT_IMPLEMENTED")


def payload(raw):
    require(len(raw) <= CAP, "LENGTH_CAP")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise Reject("JSON_ENCODING") from None
    try:
        value = json.loads(text, object_pairs_hook=Pairs, parse_int=Number, parse_float=Number,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except RecursionError:
        # Python's own recursion ceiling is not a protocol JSON_DEPTH decision.
        raise Stop("PARSER_RECURSION_LIMIT") from None
    except ValueError:
        raise Reject("JSON_SYNTAX") from None

    objects, strings, numbers = [], [], []
    max_depth = 0
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        if isinstance(item, Pairs):
            max_depth = max(max_depth, depth + 1)
            objects.append(item)
            for key, child in item:
                strings.append(key)
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            max_depth = max(max_depth, depth + 1)
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, str):
            strings.append(item)
        elif isinstance(item, Number):
            numbers.append(item)
    require(max_depth <= 64, "JSON_DEPTH")
    require(all(len({k for k, _ in obj}) == len(obj) for obj in objects), "JSON_DUPLICATE_NAME")
    if unicodedata.unidata_version != "16.0.0":
        raise Stop("UNICODE_16_TABLES_REQUIRED")
    for string in strings:
        require(all(not (0xD800 <= ord(c) <= 0xDFFF or 0xFDD0 <= ord(c) <= 0xFDEF
                         or ord(c) & 0xFFFF in (0xFFFE, 0xFFFF)
                         or unicodedata.category(c) == "Cn") for c in string), "JSON_STRING")
        require(unicodedata.normalize("NFC", string) == string, "JSON_STRING")
    if numbers:
        # ES(d) is specified, but not reproduced in these documents. Do not use
        # Python repr as an unexamined replacement or reject valid numbers.
        raise Stop("NUMBER_FORMATTING_NOT_IMPLEMENTED")

    def unpack(item):
        if isinstance(item, Pairs):
            return {k: unpack(v) for k, v in item}
        if isinstance(item, list):
            return [unpack(v) for v in item]
        return item

    value = unpack(value)
    require(jcs_without_numbers(value) == raw, "JSON_NONCANONICAL")
    return value


def schema(value, tag):
    if tag == MANIFEST:
        closed(value, "alg issuer key_fp sset ver")
        require(matches(ALG, value["alg"]) and domain(value["issuer"]), "SCHEMA")
        require(matches(r"spki-sha256:" + HEX, value["key_fp"]), "SCHEMA")
        require(isinstance(value["sset"], list) and len(value["sset"]) == 1
                and matches(r"gpg-sha256:" + HEX, value["sset"][0]), "SCHEMA")
        require(value["ver"] == "map-v1", "SCHEMA")
        return
    closed(value, "common signer")
    common = value["common"]
    closed(common, "alg binding_forms content declared_issue_time issuer manifest_sha256 preamble_sha256 profile spec vectors_sha256")
    closed(value["signer"], "key_fp")
    closed(common["spec"], "id sha256")
    require(matches(ALG, common["alg"]) and domain(common["issuer"]), "SCHEMA")
    forms = common["binding_forms"]
    require(isinstance(forms, list) and bool(forms)
            and all(matches(r"[A-Z][A-Z0-9_]{0,31}", f) for f in forms), "SCHEMA")
    require(forms == sorted(set(forms)), "SCHEMA")
    utc(common["declared_issue_time"])
    require(common["profile"] == PROFILE, "SCHEMA")
    require(all(matches(HEX, common[k]) for k in ("manifest_sha256", "preamble_sha256", "vectors_sha256")), "SCHEMA")
    require(matches(r"[a-z0-9][a-z0-9._/-]{0,127}", common["spec"]["id"])
            and matches(HEX, common["spec"]["sha256"]), "SCHEMA")
    require(matches(FP, value["signer"]["key_fp"]), "SCHEMA")


class Reader:
    def __init__(self, data):
        self.data, self.offset = data, 0

    def take(self, size):
        require(self.offset + size <= len(self.data), "TRUNCATED")
        result = self.data[self.offset:self.offset + size]
        self.offset += size
        return result

    def integer(self, width):
        return int.from_bytes(self.take(width), "big")

    def header(self, expected):
        tag = self.take(self.integer(1))
        require(tag in TAGS, "TAG_UNKNOWN")
        require(tag == expected, "TAG_MISMATCH")

    def finish(self):
        require(self.offset == len(self.data), "TRAILING")


def frame(raw, tag):
    reader = Reader(raw)
    reader.header(tag)
    require(reader.integer(2) == 1, "CV_UNKNOWN")
    size = reader.integer(4)
    require(size <= CAP, "LENGTH_CAP")
    data = reader.take(size)
    reader.finish()
    value = payload(data)
    schema(value, tag)
    return value


def signature(raw, alg):
    require(bool(raw), "SIG_EMPTY")
    require(len(raw) <= (1024 if alg == CLASSICAL else 65536), "LENGTH_CAP")
    if alg != CLASSICAL:
        return None  # Explicitly opaque, never a signature verification success.
    reader = Reader(raw)
    kind = reader.integer(1)
    require(kind in (0x88, 0x89), "SIG_PACKET")
    size = reader.integer(1 if kind == 0x88 else 2)
    require((kind == 0x88 and size <= 255) or (kind == 0x89 and 256 <= size <= 1021), "SIG_PACKET")
    body = reader.take(size)
    reader.finish()
    inner = Reader(body)
    try:
        require(inner.take(4) == b"\x04\x00\x13\x08", "SIG_FORMAT")
        hashed = inner.take(inner.integer(2))
        unhashed = inner.take(inner.integer(2))
        prefix = inner.take(2)
        scalars = []
        for _ in range(2):
            bits = inner.integer(2)
            require(1 <= bits <= 256, "SIG_FORMAT")
            scalar = int.from_bytes(inner.take((bits + 7) // 8), "big")
            require(scalar.bit_length() == bits, "SIG_FORMAT")
            scalars.append(scalar)
        inner.finish()
    except Reject:
        raise Reject("SIG_FORMAT") from None
    if hashed or unhashed:
        # E 464 specifies shortest subpacket lengths but not their wire encoding.
        raise Stop("OPENPGP_SUBPACKET_LENGTH_ENCODING_REQUIRED")
    return {"hashed": hashed, "unhashed": unhashed, "digest_prefix": prefix, "r": scalars[0], "s": scalars[1]}


def anchor(raw):
    reader = Reader(raw)
    reader.header(ANCHOR)
    require(reader.integer(1) == 2, "ANCHOR_COUNT")
    result = []
    for _ in range(2):
        size = reader.integer(4)
        require(size <= CAP + 64, "LENGTH_CAP")
        f = reader.take(size)
        parsed = frame(f, ATTEST)
        alg = parsed["common"]["alg"]
        size = reader.integer(4)
        require(size != 0, "SIG_EMPTY")
        require(size <= (1024 if alg == CLASSICAL else 65536), "LENGTH_CAP")
        sig = reader.take(size)
        signature(sig, alg)
        result.append((f, parsed, sig))
    reader.finish()
    return result


def receipt_consistency(manifest_raw, slots):
    manifest = frame(manifest_raw, MANIFEST)
    common = slots[0][1]["common"]
    require(jcs_without_numbers(common) == jcs_without_numbers(slots[1][1]["common"]), "RECEIPT_COMMON_MISMATCH")
    for slot, fp in zip(slots, (manifest["key_fp"], manifest["sset"][0])):
        require(slot[1]["signer"]["key_fp"] == fp, "RECEIPT_SLOT")
    # The conditions are explicit in PROOF 83; the reason label is local.
    require(common["manifest_sha256"] == hashlib.sha256(manifest_raw).hexdigest()
            and common["issuer"] == manifest["issuer"] and common["alg"] == manifest["alg"], "PROBE_MANIFEST_BINDING")
    return common


def snapshot(raw):
    reader = Reader(raw)
    reader.header(SNAPSHOT)
    size = reader.integer(4)
    require(1 <= size <= CAP, "LENGTH_CAP")  # zero-size reason is chosen; GAPS G30
    body = reader.take(size)
    reader.finish()
    return body


def issuance_window(not_before, not_after, declared, verified_time):
    """Only call with authenticated evidence, not untrusted bundle assertions."""
    before, after = utc(not_before), utc(not_after)
    require(after > before, "DNS_WINDOW")
    require((after - before).total_seconds() <= 7776000, "DNS_WINDOW_LENGTH")
    require(utc(declared) >= before and verified_time <= after, "ISSUANCE_WINDOW")


def report(status, reason, **extra):
    return {"probe_status": status, "probe_reason": reason, "v1_verdict": None,
            "T": None, "revocation": "NOT_EVALUATED", "historical_security": "NOT_EVALUATED",
            "standing": "ABSENT/NOT_ISSUED_IN_PROFILE", **extra}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor", type=Path, required=True, help="raw A_sig, not a bundle")
    parser.add_argument("--manifest", type=Path, required=True, help="raw F_manifest")
    args = parser.parse_args()
    try:
        raw = args.anchor.read_bytes()
        slots = anchor(raw)
        common = receipt_consistency(args.manifest.read_bytes(), slots)
        result = report("STOPPED", "FULL_VERIFIER_SPEC_GAPS", anchor_sha256=hashlib.sha256(raw).hexdigest(),
                        common_alg=common["alg"], structural_checks="passed implemented subset",
                        next_required=["bundle container", "public keys and possession proofs",
                                       "registered binding forms", "OTS and confirmation rules",
                                       "DNSSEC snapshot body", "distributed authenticated trust configuration"])
    except Reject as failure:
        result = report("REJECTED_SUBSET", str(failure))
    except Stop as failure:
        result = report("STOPPED", str(failure))
    except OSError as failure:
        result = report("INPUT_ERROR", str(failure))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
