"""Item 4b: what a signed git commit gives an offline verifier. THROWAWAY.

The registered evidence 2 (R-4.27): "the public git commit publishing the same fingerprints, with the
commit object, its signature, the relevant proof material, and the OTS proof archived in the bundle".

Mechanics (git's object format + OpenPGP), shown on a real commit of this repository that the repo's
own timestamps/ stamps into Bitcoin:
  * the OpenPGP signature covers the commit object WITH THE `gpgsig` HEADER REMOVED (tree id, parent
    ids, author/committer lines with self-asserted dates, message), plus the v4 trailer;
  * the commit id = SHA-1("commit <len>\\0" || object WITH gpgsig) -- this repo is object-format sha1;
  * the published file is reached by SHA-1 ids: commit -> tree -> subtree -> blob. The "relevant proof
    material" is every tree object on that path plus the blob;
  * the repo's OTS stamp covers SHA-256("<40-hex commit id>\\n"), i.e. the anchor reaches the content
    only through SHA-1.
So the channel's trust root is the commit-signing KEY (archived "repository signing keys"), its time
is the OTS anchor, and its integrity rests on SHA-1. Nothing in it shows the commit was ever PUBLIC.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import openpgp as P

REPO = Path(__file__).resolve().parents[3]


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True, timeout=30).stdout


def raw_object(oid: str) -> tuple[str, bytes]:
    typ = git("cat-file", "-t", oid).decode().strip()
    return typ, git("cat-file", typ, oid)


def object_id(typ: str, body: bytes) -> str:
    return hashlib.sha1(f"{typ} {len(body)}\0".encode() + body).hexdigest()


def split_gpgsig(commit: bytes) -> tuple[bytes, bytes]:
    """Return (signed payload = commit without the gpgsig header, armored signature)."""
    lines = commit.split(b"\n")
    out, sig, in_sig, in_header = [], [], False, True
    for ln in lines:
        if in_header and ln == b"":
            in_header = False
            out.append(ln)
            continue
        if in_header and ln.startswith(b"gpgsig "):
            in_sig = True
            sig.append(ln[len(b"gpgsig "):])
            continue
        if in_sig and ln.startswith(b" "):
            sig.append(ln[1:])
            continue
        in_sig = False
        out.append(ln)
    return b"\n".join(out), b"\n".join(sig)


def dearmor(armored: bytes) -> bytes:
    body = armored.split(b"\n\n", 1)[1] if b"\n\n" in armored else armored
    b64 = b"".join(x for x in body.split(b"\n") if x and not x.startswith(b"=") and not x.startswith(b"-----"))
    return base64.b64decode(b64)


@dataclass
class CommitEvidence:
    commit_id: str
    commit_raw: bytes
    signed_payload: bytes
    signature: P.Signature
    path_objects: list[tuple[str, str, bytes]] = field(default_factory=list)   # (type, id, body)

    @property
    def archive_bytes(self) -> int:
        return len(self.commit_raw) + sum(len(b) for _, _, b in self.path_objects) + len(self.signature.raw)


def tree_entry(tree_body: bytes, name: str) -> tuple[str, str] | None:
    i = 0
    while i < len(tree_body):
        sp = tree_body.index(b" ", i)
        nul = tree_body.index(b"\0", sp)
        mode, nm = tree_body[i:sp].decode(), tree_body[sp + 1:nul].decode()
        oid = tree_body[nul + 1:nul + 21].hex()
        i = nul + 21
        if nm == name:
            return mode, oid
    return None


def collect(commit_id: str, path: str) -> CommitEvidence:
    typ, raw = raw_object(commit_id)
    assert typ == "commit" and object_id("commit", raw) == commit_id
    payload, armored = split_gpgsig(raw)
    sig = P.parse_signature(dearmor(armored))
    tree_id = raw.split(b"\n", 1)[0].split()[1].decode()
    objs = []
    cur = tree_id
    for part in path.split("/"):
        t, body = raw_object(cur)
        assert object_id(t, body) == cur
        objs.append((t, cur, body))
        ent = tree_entry(body, part)
        if ent is None:
            raise FileNotFoundError(path)
        cur = ent[1]
    t, body = raw_object(cur)
    objs.append((t, cur, body))
    return CommitEvidence(commit_id, raw, payload, sig, objs)


def verify_offline(ev: CommitEvidence, pubkey_packets: bytes) -> dict:
    """Everything an offline verifier can check from archived bytes, with no git and no gpg."""
    key = None
    for tag, body, _ in P.iter_packets(pubkey_packets):
        if tag == 6:
            key = P.parse_public_key_body(body)
            break
    sig_ok = key is not None and P.verify(ev.signature, key, ev.signed_payload)
    ids_ok = object_id("commit", ev.commit_raw) == ev.commit_id and \
        all(object_id(t, b) == oid for t, oid, b in ev.path_objects)
    links_ok = ev.commit_raw.split(b"\n", 1)[0].split()[1].decode() == ev.path_objects[0][1]
    hdr = dict(ln.split(b" ", 1) for ln in ev.signed_payload.split(b"\n\n", 1)[0].split(b"\n") if b" " in ln)
    committer_time = int(hdr[b"committer"].rsplit(b" ", 2)[1])
    return {"signature_ok": sig_ok, "object_ids_ok": ids_ok, "tree_link_ok": links_ok,
            "signer_fpr": ev.signature.issuer_fpr, "key_fpr": key.fingerprint_v4 if key else None,
            "sig_creation_time": ev.signature.creation_time, "committer_time": committer_time,
            "hash_alg": ev.signature.hash_alg, "pk_alg": ev.signature.pk_alg,
            "archive_bytes": ev.archive_bytes}


# --- full path verification (Track 3 step 11; INSTRUMENT code, A9.2: not evidence for any claim) ---
# What the spec fixes: the blob carries the SAME canonical value as the DNS TXT record (ENCODING-V1 s7.2, D-17), whose
# ABNF is s7 "Value grammar". What it leaves open ("not P8's", s7.2; "the git blob path", out-of-scope list): the path,
# and any byte framing around the value (e.g. a trailing LF). Here: the path is a caller argument, and NO framing is
# accepted (blob == value, byte for byte). The value contains no issuer domain D, so none is extracted from it.
KEY_VALUE_RE = re.compile(
    rb"v=tessera1;profile=tessera-v1-strict;kms=([0-9a-f]{64});gpg=([0-9a-f]{64})"
    rb";issuance-not-before=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"
    rb";issuance-not-after=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")
MAX_WINDOW_S = 7_776_000


class GitPathError(Exception):
    def __init__(self, reason: str, detail: str = ""):
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason


def _entries(tree_body: bytes) -> list[tuple[str, str, str]]:
    out, i = [], 0
    while i < len(tree_body):
        sp = tree_body.find(b" ", i)
        nul = tree_body.find(b"\0", sp + 1) if sp >= 0 else -1
        if sp < 0 or nul < 0 or nul + 21 > len(tree_body):
            raise GitPathError("TREE_MALFORMED")
        out.append((tree_body[i:sp].decode("ascii", "replace"), tree_body[sp + 1:nul].decode("utf-8", "replace"),
                    tree_body[nul + 1:nul + 21].hex()))
        i = nul + 21
    return out


def _utc(s: bytes) -> int:
    try:
        d = datetime.datetime.strptime(s.decode(), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError as e:
        raise GitPathError("KEY_VALUE", f"time {s!r}") from e
    return int(d.timestamp())


def parse_key_value(blob: bytes) -> dict:
    """Exact parse of the s7 value grammar; no trimming, no tolerant parsing."""
    m = KEY_VALUE_RE.fullmatch(blob)     # fullmatch: a trailing LF or any extra byte fails
    if m is None:
        raise GitPathError("KEY_SYNTAX")
    nb, na = _utc(m.group(3)), _utc(m.group(4))
    if na <= nb:
        raise GitPathError("KEY_WINDOW")
    if na - nb > MAX_WINDOW_S:
        raise GitPathError("KEY_WINDOW_LENGTH")
    return {"kms": m.group(1).decode(), "gpg": m.group(2).decode(),
            "issuance_not_before": m.group(3).decode(), "issuance_not_after": m.group(4).decode()}


def verify_key_path(commit_id: str, commit_raw: bytes, path_objects: list[tuple[str, str, bytes]], path: str) -> dict:
    """commit -> root tree -> each subtree -> blob, all from presented bytes (no git). Raises GitPathError(reason).
    path_objects = [root tree, subtree..., blob], one object per path component plus the root."""
    parts = path.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise GitPathError("PATH_COMPONENT", path)
    if object_id("commit", commit_raw) != commit_id:
        raise GitPathError("COMMIT_ID_MISMATCH")
    first = commit_raw.split(b"\n", 1)[0].split(b" ")
    if len(first) != 2 or first[0] != b"tree" or not re.fullmatch(rb"[0-9a-f]{40}", first[1]):
        raise GitPathError("COMMIT_NO_TREE")
    if len(path_objects) != len(parts) + 1:
        raise GitPathError("PATH_OBJECTS_COUNT")
    want = first[1].decode()
    for depth, part in enumerate(parts):
        typ, oid, body = path_objects[depth]
        if typ != "tree":
            raise GitPathError("OBJECT_TYPE", f"depth {depth} is {typ}")
        if oid != want:
            raise GitPathError("LINK_MISMATCH", f"depth {depth}: expected {want}, presented {oid}")
        if object_id("tree", body) != oid:
            raise GitPathError("TREE_ID_MISMATCH", f"depth {depth}")
        hits = [(m, o) for m, n, o in _entries(body) if n == part]
        if not hits:
            raise GitPathError("PATH_NOT_FOUND", part)
        if len(hits) > 1:
            raise GitPathError("PATH_AMBIGUOUS", part)
        mode, want = hits[0]
        if mode != ("40000" if depth < len(parts) - 1 else "100644"):
            raise GitPathError("ENTRY_MODE", f"{part}: {mode}")
    typ, oid, body = path_objects[-1]
    if typ != "blob":
        raise GitPathError("OBJECT_TYPE", f"leaf is {typ}")
    if oid != want:
        raise GitPathError("BLOB_SUBSTITUTED", f"tree names {want}, presented {oid}")
    if object_id("blob", body) != oid:
        raise GitPathError("BLOB_ID_MISMATCH")
    return {"blob_id": oid, "path": path, **parse_key_value(body)}


# --- profile composition (docs/reviews/v1-profile/ F7, 2026-10-13; INSTRUMENT code, A9.2) ---
# V1-PROFILE §6.3 fixes the path (OWNER DECISION 2026-10-13) and A9 requires the git value to equal the DNS value.
# This composition pins the path and compares the blob with the DNSSEC-validated TXT value byte for byte.
# COVERAGE LIMIT, stated: it does NOT verify `gpgsig` under the pinned repository key, the OTS stamp on the commit id,
# or signed issuer == pinned D. Those remain the job of a composition that does not yet exist (F7).
PROFILE_KEY_PATH = "tessera-v1/key-assertion"


def verify_profile_key_assertion(commit_id: str, commit_raw: bytes, path_objects: list[tuple[str, str, bytes]],
                                 dns_txt_strings: list[bytes] | tuple[bytes, ...]) -> dict:
    """Fixed-path git key assertion plus cross-channel equality. `dns_txt_strings` are the character-strings of the
    ONE validated TXT RR (ENC §7: one RRset, one RR, one character-string). Raises GitPathError(reason)."""
    if len(dns_txt_strings) != 1:
        raise GitPathError("DNS_TXT_SHAPE", f"{len(dns_txt_strings)} character-strings")
    dns_value = bytes(dns_txt_strings[0])
    r = verify_key_path(commit_id, commit_raw, path_objects, PROFILE_KEY_PATH)
    if path_objects[-1][2] != dns_value:     # raw bytes; no parse-then-compare, no normalization
        raise GitPathError("DNS_GIT_MISMATCH")
    return {**r, "dns_value_equal": True}
