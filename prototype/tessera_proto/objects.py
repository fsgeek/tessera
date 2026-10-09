"""Object shapes shared by issuer and verifier (spec §3.3-§3.6). Field names, nesting and
encodings here are GUESSES (see GUESSES.md G-08, G-09, G-14..G-19, G-21..G-24).
"""
from __future__ import annotations

import datetime as _dt
import struct

from . import frame, jcs
from .crypto import b64e, sha256_hex

SPEC_ID = "tessera-verify/prototype-phase1"
POLICY_VERSION = "proto-issue-policy-0"
BINDING_FORMS_KNOWN_SUPPORTED = {"STMT_DIGEST", "STMT_DIRECT"}
BINDING_FORMS_KNOWN_UNSUPPORTED = {"STMT_MERKLE"}  # invented, for the distinct-code test
TUPLE_VERSION = "map-v1"

EMBEDDED_SPEC_TEXT = (
    "Tessera prototype verification procedure. THROWAWAY. Follows docs/implementation-spec.md "
    "section 5 as of 2026-10-06; see prototype/GUESSES.md for every decision the spec left open."
)


def ts(t: int) -> str:
    # GUESS G-16: time encoding. RFC 3339 UTC string, second precision (R-3.2 forbids raw
    # non-double numbers; an int would be a double, but we string-encode to be safe).
    return _dt.datetime.fromtimestamp(t, _dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s: str) -> int:
    d = _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.UTC)
    return int(d.timestamp())


def authority_tuple(issuer_id: str, key_fp: str, sset: list[str], alg: str, ver: str = TUPLE_VERSION) -> dict:
    # GUESS G-08: map-v1 tuple as a JSON object with these member names.
    # GUESS G-09: `key_fp` is the PRIMARY (slot A) signer; `sset` lists the OTHER required
    # signers' fingerprints in slot order, so required arity = 1 + len(sset). Chosen to match
    # the C-C2 trace's honest tuple authTuple(issuerId2, fp(pk(skI)), signers1(fp(pk(skB2))), ...).
    return {"issuer_id": issuer_id, "key_fp": key_fp, "sset": list(sset), "alg": alg, "ver": ver}


def tuple_bytes(t: dict) -> bytes:
    return jcs.canonicalize(t)


def manifest_hash(t: dict) -> str:
    # GUESS G-14: "manifest hash" (R-3.11) = sha256 over the JCS of the authority TUPLE only,
    # mirroring the model's mh = h(t). The real manifest's other members (public keys, binding
    # forms, evidences) are NOT under this hash. See PREDICTIONS item 2 in PHASE1-REPORT.
    return "sha256:" + sha256_hex(tuple_bytes(t))


def slot_fps(t: dict) -> list[str]:
    return [t["key_fp"], *t["sset"]]


def attest_payload(common: dict, key_fp: str) -> bytes:
    # GUESS G-15 (the R-3.12a "encoding map", OPEN O-79): the canonical payload is
    #   {"common": {...everything equal across slots...}, "signer": {"key_fp": ...}}
    # "payload equal across signer slots" is then a statement about `common`'s bytes.
    return jcs.canonicalize({"common": common, "signer": {"key_fp": key_fp}})


def attest_common(issuer_id, alg, mh, declared, content, binding_forms, spec_hash, extra=None) -> dict:
    c = {
        "alg": alg,
        "issuer_id": issuer_id,
        "manifest_hash": mh,
        "declared_issue_time": ts(declared),
        "binding_forms": sorted(binding_forms),  # GUESS G-17: set encoded as sorted array
        "spec": {"id": SPEC_ID, "hash": spec_hash},
        "issue_policy_version": POLICY_VERSION,  # R-3.46 "records its issue-time policy version"
        "content": content,
    }
    if extra:
        c.update(extra)
    return c


def receipt_digest(frames: list[bytes]) -> str:
    # GUESS G-19 / CONTRADICTION-adjacent: R-3.42 "exactly one anchor proof ... over its
    # canonical bytes", but under R-3.12 reading (a) a two-signer receipt has TWO frames. We
    # anchor sha256 over u32-length-prefixed frames in slot order.
    acc = b"".join(struct.pack(">I", len(f)) + f for f in frames)
    return sha256_hex(b"tessera/v0/receipt-digest\x00" + acc)


def evidence_payload(form: str, t: dict) -> bytes:
    if form == "STMT_DIGEST":
        return jcs.canonicalize({"form": form, "digest": manifest_hash(t)})
    if form == "STMT_DIRECT":
        return jcs.canonicalize({"form": form, "statement": t})
    raise ValueError(form)


def evidence_frame(form: str, t: dict) -> bytes:
    # GUESS G-21: channel evidence (DNSSEC / git+OTS in the spec) STUBBED as an Ed25519
    # signature by a per-channel key over an OT_AUTHEVID frame. Real evidence is not built.
    return frame.encode("OT_AUTHEVID", frame.CANON_V1, evidence_payload(form, t))


def possession_frame(t: dict) -> bytes:
    # GUESS G-22: possession = signature over an OT_MANIFEST frame whose payload is the tuple's
    # JCS bytes (model: sign((POSS, t), sk)).
    return frame.encode("OT_MANIFEST", frame.CANON_V1, tuple_bytes(t))


def attempt_core(t: dict, possession_b64: list[str], sigs_b64: list[str], declared_str: str) -> dict:
    # GUESS G-24: model attemptCore(t, ppf, sg, decl) generalized to n slots.
    return {"tuple": t, "possession": possession_b64, "signatures": sigs_b64, "declared_issue_time": declared_str}


def attempt_id(core: dict) -> str:
    return "aid:" + sha256_hex(jcs.canonicalize(core))


def embedded_objects() -> dict:
    spec_bytes = EMBEDDED_SPEC_TEXT.encode()
    return {
        "spec": {"type": "OT_SPEC", "id": SPEC_ID, "bytes_b64": b64e(spec_bytes), "hash": "sha256:" + sha256_hex(spec_bytes)},
        "conformance_vectors": [
            {"type": "OT_CONFVEC", "name": "canary-unknown-algorithm", "alg": "TESSERA-RESERVED-UNRECOGNIZED-0",
             "expected_verdict": "UNVERIFIABLE", "note": "R-3.53 fixed floor; prototype carries the label, not a full vector"},
        ],
        "standards_dependencies": [
            {"standard": "RFC 8785", "edition": "2020-06", "sections": "3.2", "failure_consequence": "canonical bytes unreconstructible"},
            {"standard": "RFC 8032", "edition": "2017-01", "sections": "5.1", "failure_consequence": "signatures unverifiable"},
        ],
        "purpose_preamble": "This package records that certain bytes existed and were signed by Tessera's issuer keys. It does not say they are true.",
    }


def spec_hash() -> str:
    return "sha256:" + sha256_hex(EMBEDDED_SPEC_TEXT.encode())
