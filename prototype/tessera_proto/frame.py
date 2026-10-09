"""The P8 four-field signed frame (spec §3.2, R-3.9): type_tag || canonicalization_version ||
payload_length || payload.

The binary layout is OPEN in the spec (R-3.10, §11 O-01). Everything about bytes here is
GUESS G-01 / G-02 (see GUESSES.md).

Layout chosen:
    u8   tag_len
    tag  ASCII, tag_len bytes          (domain-separation tag; also names the object type, G-07)
    u16  canonicalization_version, big-endian
    u64  payload_length, big-endian
    payload  (JCS bytes)
"""
from __future__ import annotations

import struct
from dataclasses import dataclass

# GUESS G-07: P7 enumerates object types; R-3.11 lists BOTH a "domain-separation tag" AND an
# "object type" in the signed bytes. The four-field frame has one tag slot. We fold both into
# one ASCII tag "tessera/v0/<OT_NAME>": the prefix is the domain separation, the suffix the type.
TAG_PREFIX = "tessera/v0/"
OBJECT_TYPES = (
    "OT_ATTEST", "OT_WRAPPER", "OT_MANIFEST", "OT_AUTHEVID", "OT_CONFVEC",
    "OT_REVIEWREC", "OT_SPEC", "OT_TLR", "OT_REFUSAL",
)

# GUESS G-02: canonicalization version identifiers are not enumerated (§8 table). We use u16
# integers; 1 = "RFC 8785 JCS + Tessera precision rule, prototype".
CANON_VERSIONS_KNOWN = {1: "JCS-RFC8785+precision/proto-1"}
CANON_V1 = 1


class FrameError(ValueError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}")
        self.code = code


@dataclass(frozen=True)
class Frame:
    object_type: str
    canon_version: int
    payload: bytes

    def encode(self) -> bytes:
        tag = (TAG_PREFIX + self.object_type).encode("ascii")
        return (
            struct.pack(">B", len(tag)) + tag
            + struct.pack(">H", self.canon_version)
            + struct.pack(">Q", len(self.payload))
            + self.payload
        )


def encode(object_type: str, canon_version: int, payload: bytes) -> bytes:
    return Frame(object_type, canon_version, payload).encode()


def decode(fb: bytes) -> tuple[Frame, list[tuple[str, str]]]:
    """Parse a frame; return (frame, list of (check_id, failure_code)).

    Raises FrameError only if nothing further can be read. Separate P8 failures are reported
    as a list so the verifier can record each check's own status (R-5.16: no order dependence).
    """
    fails: list[tuple[str, str]] = []
    if len(fb) < 1:
        raise FrameError("P8_FRAME_TRUNCATED")
    tl = fb[0]
    if len(fb) < 1 + tl + 2 + 8:
        raise FrameError("P8_FRAME_TRUNCATED")
    try:
        tag = fb[1:1 + tl].decode("ascii")
    except UnicodeDecodeError:
        raise FrameError("P8_TYPE_TAG_MALFORMED") from None
    off = 1 + tl
    (cv,) = struct.unpack(">H", fb[off:off + 2])
    off += 2
    (plen,) = struct.unpack(">Q", fb[off:off + 8])
    off += 8
    rest = fb[off:]
    if not tag.startswith(TAG_PREFIX):
        fails.append(("V8", "P7_DOMAIN_TAG_UNKNOWN"))
        ot = tag
    else:
        ot = tag[len(TAG_PREFIX):]
        if ot not in OBJECT_TYPES:
            fails.append(("V8", "P7_OBJECT_TYPE_UNKNOWN"))
    if cv not in CANON_VERSIONS_KNOWN:
        fails.append(("V1", "P8_CANON_VERSION_UNKNOWN"))
    if len(rest) < plen:
        fails.append(("V5", "P8_LENGTH_PREFIX_MISMATCH"))
        payload = rest
    else:
        payload = rest[:plen]
        if len(rest) > plen:
            fails.append(("V3", "P8_TRAILING_BYTES"))
    fr = Frame(ot, cv, payload)
    # V2: independent reconstruction. Only meaningful when the length field was honest.
    if not fails and fr.encode() != fb:
        fails.append(("V2", "P8_FRAME_RECONSTRUCTION_MISMATCH"))
    return fr, fails
