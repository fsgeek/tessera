"""ENCODING-V1 byte layouts the issuer writes (frames, A_sig, snapshot envelope, the key-assertion value), and the
key fingerprints. Every frame written here is read back with the service verifier's own decoder before use.
Layouts follow formal/p8/ENCODING-V1.md sections 2-7 (copied from the P8 reference encoder, not imported)."""
import hashlib
import struct

from tessera_verify.codec import read_frame, read_anchor, registered_codecs

from .util import ALG, D, PROFILE, SPEC_ID, jcs, rfc3339, sha256hex, ts

T_ATTEST = b"tessera-v1/attest"
T_MANIFEST = b"tessera-v1/manifest"
T_ANCHOR = b"tessera-v1/receipt-anchor-sig"
T_SNAPSHOT = b"tessera-v1/dnssec-snapshot"
MAX_PAYLOAD = 1 << 24
MLDSA65_SPKI_PREFIX = bytes.fromhex("308207b2300b0609608648016503040312038207a100")
P256_OID = bytes.fromhex("2a8648ce3d030107")
WINDOW_MAX_SECONDS = 90 * 86400


class EncodeError(ValueError):
    pass


def header(tag):
    return bytes([len(tag)]) + tag


def frame(tag, payload):
    if len(payload) > MAX_PAYLOAD:
        raise EncodeError("payload above 2^24 bytes")
    return header(tag) + struct.pack(">HI", 1, len(payload)) + payload


def fp_kms(spki_der):
    return "spki-sha256:" + hashlib.sha256(spki_der).hexdigest()


def fp_gpg(v4_body):
    return "gpg-sha256:" + hashlib.sha256(v4_body).hexdigest()


def openpgp_v4_body(point65, created):
    return bytes([4]) + struct.pack(">I", created) + bytes([19, len(P256_OID)]) + P256_OID + struct.pack(">H", 515) + point65


def encode_manifest(kms_fp, gpg_fp, alg=ALG, issuer=D):
    f = frame(T_MANIFEST, jcs({"alg": alg, "issuer": issuer, "key_fp": kms_fp, "sset": [gpg_fp], "ver": "map-v1"}))
    read_frame(f, "tessera-v1/manifest")
    return f


def common_metadata(content_b64, declared_issue_time, manifest, catalog):
    return {"alg": catalog["alg"], "binding_forms": ["STMT_DIRECT"], "content": content_b64,
            "declared_issue_time": declared_issue_time, "issuer": D, "manifest_sha256": sha256hex(manifest),
            "preamble_sha256": catalog["preamble_sha256"], "profile": PROFILE,
            "spec": {"id": SPEC_ID, "sha256": catalog["spec_sha256"]}, "vectors_sha256": catalog["vectors_sha256"]}


def encode_attest(common, key_fp):
    f = frame(T_ATTEST, jcs({"common": common, "signer": {"key_fp": key_fp}}))
    read_frame(f, "tessera-v1/attest")
    return f


def encode_anchor(f_kms, s_kms, f_gpg, s_gpg):
    """A_sig: header || 0x02 || per slot in manifest order: u32 len(F) || F || u32 len(S) || S (ENC section 5)."""
    out = header(T_ANCHOR) + bytes([2])
    for part in (f_kms, s_kms, f_gpg, s_gpg):
        out += struct.pack(">I", len(part)) + part
    read_anchor(out, registered_codecs(ALG))
    return out


def encode_snapshot_envelope(body):
    if not 1 <= len(body) <= MAX_PAYLOAD:
        raise EncodeError("snapshot body length")
    return header(T_SNAPSHOT) + struct.pack(">I", len(body)) + body


def assertion_value(kms_fp, gpg_fp, not_before, not_after):
    """The ENC section 7 value: exactly 255 bytes, no LF; the TXT string and the git blob."""
    nb, na = ts(not_before), ts(not_after)
    if rfc3339(nb) != not_before or rfc3339(na) != not_after:
        raise EncodeError("window times must be canonical RFC 3339 seconds")
    if not 0 < na - nb <= WINDOW_MAX_SECONDS:
        raise EncodeError("window must be non-empty and at most 90 days")
    v = (f"v=tessera1;profile={PROFILE};kms={kms_fp.split(':')[1]};gpg={gpg_fp.split(':')[1]};"
         f"issuance-not-before={not_before};issuance-not-after={not_after}").encode("ascii")
    if len(v) != 255:
        raise EncodeError(f"assertion value is {len(v)} bytes, not 255")
    return v


def txt_rdata(value):
    if len(value) > 255:
        raise EncodeError("TXT string too long")
    return bytes([len(value)]) + value
