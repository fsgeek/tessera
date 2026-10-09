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
import hashlib
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
