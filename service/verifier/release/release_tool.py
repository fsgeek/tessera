#!/usr/bin/env python3
"""Tessera V1 verifier release tool (profile section 15.9 R1-R5). Standard library only; Python 3.9 or later.
It runs on the NUC, on Tails (the author's sitting) and on a relying party's machine. It never signs.

  build     --repo R --commit C [--namespace PRODUCTION] [--release 1] --out DIR
            Assemble tessera-verifier-v1[-TEST]-<n>.parts from tracked blob bytes at commit C (R1), generate
            RELEASE.json (R2), check every R2 binding equality, print the archive SHA-256. Deterministic.
  diff      --repo R --base B --commit C [--release 1] --out FILE
            The author's reading copy: every file that enters the archive (plus the signing script and the release
            vectors) that was added or changed between the baseline commit B and C, in full, with each file's
            SHA-256 at C. The last line is the SHA-256 of everything above it; the printed copy carries the same line.
  baseline  --repo R --commit B --source C
            Networked (Tor on Tails): B's OpenTimestamps proof (timestamps/anchored/B.ots at C) against the block
            header from two explorers; prints the block height and its header time. Also: the freeze commit is an
            ancestor of B.
  check     ARCHIVE --repo R
            Archive grammar, R2 equalities, every part equal to its blob at the named source commit, the catalog and
            freeze record equal to the freeze commit's, then the authority entries to compare by eye.
  inspect   ARCHIVE
            Offline (the signing session): archive grammar and R2 equalities only; prints namespace, release, hash.
  sources   ARCHIVE
            Networked (Tor on Tails): KSK digests against IANA root-anchors.xml; header pins against two explorers.
  verify-sig ARCHIVE SIG --fingerprint F --key KEY [--gpgv P]
            R3 signature check alone: one unarmored rule-O signature, the key file is exactly the key F, then gpgv
            with a keyring holding only that key. Says nothing about the namespace.
  acquire   ARCHIVE SIG --fingerprint F --key KEY [--namespace PRODUCTION|TEST] [--out DIR] [--gpgv P]
            Reads ARCHIVE and SIG once into a private directory and uses only that copy: verify-sig, R2 equalities,
            the expected namespace (PRODUCTION unless TEST is named). Without --out it stops there. With --out it
            unpacks into the new directory DIR and runs DIR/service/verifier/install.sh on it.
  bindings  ROOT
            install.sh's check on an unpacked release: the tree holds exactly the manifest's files, and R2 holds;
            prints the release_constants.py path to install.

F is the release key's full fingerprint as the relying party obtained it out of band (R5): never from the release.
"""
import argparse
import ast
import base64
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

FREEZE_COMMIT = "52ee17918c5ed841587d78cb2ca3e8c54c4682d2"   # the author's freeze-record commit (OTS-anchored)
FREEZE_RECORD = "formal/freeze-v1/FREEZE-RECORD.md"
FREEZE_RECORD_SHA256 = "05542967b091424a614afd38a32cfb847b9b6b3f0e5a7b7103b11cd22d95575e"
FROZEN_CATALOG = "formal/freeze-v1/objects/catalog.json"
FROZEN_CATALOG_SHA256 = "aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2"
V = "service/verifier/"
SHA1DC = V + "vendor/sha1collisiondetection/"
FILES = ["docs/V1-RELYING-PARTY.md", FROZEN_CATALOG, V + "README.md", V + "install.sh", V + "requirements.lock",
         V + "release/release_tool.py"]
DIRS = [V + "tessera_verify/", V + "vendor/"]
EXCLUDE = {V + "tessera_verify/release_constants.py"}          # the source tree's unprovisioned copy
REQUIRED = FILES + [V + "vendor/SHA1DC-PIN.md", V + "tessera_verify/__init__.py", V + "tessera_verify/cli.py",
                    V + "tessera_verify/verify.py"] + [SHA1DC + p for p in (
                        "lib/sha1.c", "lib/sha1.h", "lib/ubc_check.c", "lib/ubc_check.h", "src/main.c", "Makefile",
                        "test/shattered-1.pdf")]               # R1's required parts; install.sh needs every one
READ_ALSO = ["docs/ceremony/sign-release.sh"]                   # run in the signing session; not in the archive
READ_ALSO_DIRS = ["service/release-vectors/"]
MANIFEST_KEYS = {"format", "namespace", "release", "profile", "source_commit", "trust_config_sha256",
                 "trust_config_version", "catalog_sha256", "freeze_record_sha256", "parts", "release_key_successor"}
CONSTANT_NAMES = ["NAMESPACE", "TRUST_SHA256", "CATALOG_SHA256", "CATALOG_BYTES", "UNICODE_VERSION"]
HEADER = re.compile(rb"tessera-v1-part ([A-Za-z0-9._/-]+) (0|[1-9][0-9]*)\n")
HEX64, DEC = re.compile(r"[0-9a-f]{64}"), re.compile(r"0|[1-9][0-9]*")
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551   # P-256 group order
P256_OID = bytes.fromhex("2a8648ce3d030107")
EXPLORERS = ("https://blockstream.info/api", "https://mempool.space/api")


class Refused(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Refused(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_json(raw, what):
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError:
        raise Refused(what + " is not JSON") from None


def jcs(obj):  # RFC 8785 for this manifest: ASCII strings, null and objects only, no numbers
    out = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    need(out.isascii(), "manifest is not ASCII")
    return out.encode()


def stem(namespace, n):
    return "tessera-verifier-v1-%s%s" % ("TEST-" if namespace == "TEST" else "", n)


def release_dir(namespace, n):
    return V + "release/v1-%s%s/" % ("TEST-" if namespace == "TEST" else "", n)


def git(repo, *args):
    # --no-replace-objects: a local replace ref must not change what a commit resolves to (review L1).
    return subprocess.run(["git", "--no-replace-objects", "-C", repo] + list(args), check=True,
                          capture_output=True).stdout


def blobs_at(repo, commit):
    """{path: blob id} of tracked regular files at commit: no working tree, no newline conversion, no symlinks."""
    out = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.split(b" ")
        if kind == b"blob" and mode in (b"100644", b"100755"):
            out[path.decode()] = oid.decode()
    return out


def read_blob(repo, oid):
    return git(repo, "cat-file", "blob", oid)


def resolve(repo, commit):
    return git(repo, "rev-parse", "--verify", commit + "^{commit}").decode().strip()


def archive_paths(tree, namespace, n):
    d = release_dir(namespace, n)
    want = set(FILES) | {d + "trust.json", d + "release_constants.py"}
    return want | ({p for p in tree if any(p.startswith(x) for x in DIRS)} - EXCLUDE)


# ---- section 15.8 part format ----

def assemble(parts):
    out = bytearray()
    for path in sorted(parts):
        out += b"tessera-v1-part %s %d\n" % (path.encode(), len(parts[path])) + parts[path] + b"\n"
    return bytes(out)


def parse_archive(data):
    parts, pos, last = {}, 0, None
    while pos < len(data):
        m = HEADER.match(data, pos)
        need(m, "bad part header at byte %d" % pos)
        path, n = m.group(1).decode(), int(m.group(2))
        need(not path.startswith("/") and all(c not in ("", ".", "..") for c in path.split("/")), "bad path " + path)
        need(last is None or path > last, "paths not strictly sorted at " + path)
        start = m.end()
        need(start + n < len(data) + 1 and data[start + n:start + n + 1] == b"\n", "bad part length " + path)
        parts[path], pos, last = data[start:start + n], start + n + 1, path
    need(parts, "empty archive")
    return parts


# ---- R2: manifest, constants, binding equalities ----

def constants_source(namespace, trust, catalog):
    return ('"""Release bindings (profile 15.9 R2), generated for one release; installed by install.sh as\n'
            'tessera_verify/release_constants.py. Machine-independent facts only."""\n'
            "NAMESPACE = %r\nTRUST_SHA256 = %r\nCATALOG_SHA256 = %r\nCATALOG_BYTES = %r\nUNICODE_VERSION = '16.0.0'\n"
            % (namespace, sha(trust), sha(catalog), catalog)).encode()


def parse_constants(src):
    """Read the five assignments without executing anything."""
    tree = ast.parse(src.decode("ascii"))
    body = tree.body[1:] if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) else tree.body
    got = {}
    for node in body:
        need(isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name),
             "release_constants.py holds something other than assignments")
        got[node.targets[0].id] = ast.literal_eval(node.value)
    need(list(got) == CONSTANT_NAMES, "release_constants.py names %s" % list(got))
    return got


def check_bindings(parts):
    """Every R2 binding equality and R1's required parts. Returns (manifest, trust object, constants path)."""
    need("RELEASE.json" in parts, "no RELEASE.json")
    raw = parts["RELEASE.json"]
    m = load_json(raw, "RELEASE.json")
    need(isinstance(m, dict) and set(m) == MANIFEST_KEYS and jcs(m) == raw, "RELEASE.json is not the closed JCS object")
    for k in MANIFEST_KEYS - {"parts", "release_key_successor"}:
        need(isinstance(m[k], str), "RELEASE.json %s is not a string" % k)
    need(m["format"] == "tessera-v1-release/1" and m["profile"] == "tessera-v1-strict", "format or profile")
    need(m["namespace"] in ("PRODUCTION", "TEST"), "namespace")
    need(DEC.fullmatch(m["release"]) and m["release"] != "0", "release number")
    need(DEC.fullmatch(m["trust_config_version"]) and m["trust_config_version"] != "0", "trust_config_version")
    need(re.fullmatch(r"[0-9a-f]{40}", m["source_commit"]), "source_commit")
    for k in ("trust_config_sha256", "catalog_sha256", "freeze_record_sha256"):
        need(HEX64.fullmatch(m[k]), k)
    s = m["release_key_successor"]
    need(s is None or (isinstance(s, str) and re.fullmatch(r"[0-9A-F]{40}", s)), "release_key_successor")
    others = {p: b for p, b in parts.items() if p != "RELEASE.json"}
    need(isinstance(m["parts"], dict) and set(m["parts"]) == set(others), "parts paths differ from the archive's")
    for p, b in others.items():
        need(isinstance(m["parts"][p], str) and m["parts"][p] == sha(b), "part hash differs: " + p)
    d = release_dir(m["namespace"], m["release"])
    tpath, cpath = d + "trust.json", d + "release_constants.py"
    missing = sorted(set(REQUIRED + [tpath, cpath]) - set(others))
    need(not missing, "a required part is missing: %s" % missing)
    trust, catalog = others[tpath], others[FROZEN_CATALOG]
    c = parse_constants(others[cpath])
    need(sha(trust) == m["trust_config_sha256"] == c["TRUST_SHA256"], "trust hash binding")
    need(sha(catalog) == m["catalog_sha256"] == c["CATALOG_SHA256"] and c["CATALOG_BYTES"] == catalog, "catalog binding")
    t = load_json(trust, "trust.json")
    need(isinstance(t, dict) and t.get("version") == m["trust_config_version"], "trust version binding")
    need(t.get("format") == "tessera-v1-trust/1" and t.get("profile") == "tessera-v1-strict", "trust.json format or profile")
    if m["release"] == "1":   # no earlier release: the chain starts here (profile section 5)
        need(t["version"] == "1" and t.get("previous_sha256") == "0" * 64, "release 1 must carry trust version 1, previous 64 zeros")
    need(c["NAMESPACE"] == m["namespace"] and c["UNICODE_VERSION"] == "16.0.0", "namespace binding")
    if m["namespace"] == "PRODUCTION":
        need(m["freeze_record_sha256"] == FREEZE_RECORD_SHA256 and m["catalog_sha256"] == FROZEN_CATALOG_SHA256,
             "PRODUCTION catalog is not the freeze record's")
    return m, t, cpath


# ---- build ----

def build(repo, commit, namespace, n):
    commit = resolve(repo, commit)
    tree = blobs_at(repo, commit)
    d = release_dir(namespace, n)
    want = archive_paths(tree, namespace, n)
    missing = sorted(want - set(tree))
    need(not missing, "not tracked at %s: %s" % (commit, missing))
    parts = {p: read_blob(repo, tree[p]) for p in want}
    freeze = blobs_at(repo, FREEZE_COMMIT)
    record = read_blob(repo, freeze[FREEZE_RECORD])
    need(parts[FROZEN_CATALOG] == read_blob(repo, freeze[FROZEN_CATALOG]), "catalog differs from the freeze commit's")
    trust = parts[d + "trust.json"]
    manifest = {"format": "tessera-v1-release/1", "namespace": namespace, "release": str(n),
                "profile": "tessera-v1-strict", "source_commit": commit, "trust_config_sha256": sha(trust),
                "trust_config_version": json.loads(trust)["version"], "catalog_sha256": sha(parts[FROZEN_CATALOG]),
                "freeze_record_sha256": sha(record), "parts": {p: sha(b) for p, b in parts.items()},
                "release_key_successor": None}
    parts["RELEASE.json"] = jcs(manifest)
    check_bindings(parts)
    return stem(namespace, n) + ".parts", assemble(parts)


# ---- the author's reading copy and baseline ----

def diff(repo, base, commit, n):
    """Text of every archive file (and READ_ALSO file) added or changed from base to commit; last line its hash."""
    base, commit = resolve(repo, base), resolve(repo, commit)
    new, old = blobs_at(repo, commit), blobs_at(repo, base)
    paths = archive_paths(new, "PRODUCTION", n) | set(READ_ALSO)
    paths |= {p for p in new if any(p.startswith(x) for x in READ_ALSO_DIRS)}
    missing = sorted(paths - set(new))
    need(not missing, "not tracked at %s: %s" % (commit, missing))
    gone = sorted(p for p in old if p not in paths and (p in FILES or p in READ_ALSO or
                  any(p.startswith(x) for x in DIRS + READ_ALSO_DIRS)) and p not in EXCLUDE)
    out = ["Tessera verifier release %s: the files that differ from the baseline" % n,
           "baseline commit %s" % base, "source commit   %s" % commit,
           "Every file below enters the archive except docs/ceremony/sign-release.sh and service/release-vectors/,",
           "which run in the signing session. RELEASE.json is generated by the build and is not listed.", ""]
    changed = []
    for p in sorted(paths):
        b = read_blob(repo, new[p])
        a = read_blob(repo, old[p]) if p in old else None
        status = "unchanged" if a == b else ("changed" if a is not None else "added")
        out.append("%-9s %s  %s" % (status, sha(b), p))
        if a != b:
            changed.append((p, a, b))
    for p in gone:
        out.append("removed   %s  %s" % (" " * 64, p))
    for p, a, b in changed:
        out += ["", "=" * 100, "%s  (%s, %d bytes, sha256 %s)" % (p, "added" if a is None else "changed", len(b), sha(b)),
                "=" * 100]
        if b"\0" in b or (a is not None and b"\0" in a):
            out.append("(binary)")
            continue
        try:
            new_t, old_t = b.decode("utf-8"), (a or b"").decode("utf-8")
        except UnicodeDecodeError:
            out.append("(not UTF-8)")
            continue
        if a is None and p.endswith(".json"):          # one-line JSON, shown indented for reading
            out += ["(the file is one line; shown indented, keys in file order)"] + json.dumps(
                json.loads(new_t), indent=1, ensure_ascii=False).splitlines()
        elif a is None:
            out += new_t.splitlines()
        else:
            out += [l.rstrip("\n") for l in difflib.unified_diff(old_t.splitlines(), new_t.splitlines(),
                                                                  "baseline", "source", n=3, lineterm="")]
    body = ("\n".join(out) + "\n").encode("utf-8")
    line = "DIFF %d added or changed, %d removed; sha256 of the text above %s" % (len(changed), len(gone), groups(sha(body), 8))
    return body + (line + "\n").encode(), line


def ots_heights(raw, digest):
    """Bitcoin attestations [(height, merkle root)] of an OTS proof in the profile section 15.2 grammar over digest."""
    magic = bytes.fromhex("004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e89294")
    pos = [0]

    def take(k):
        need(pos[0] + k <= len(raw), "OTS proof truncated")
        pos[0] += k
        return raw[pos[0] - k:pos[0]]

    def varuint():
        v = 0
        for i in range(5):
            b = take(1)[0]
            v |= (b & 0x7F) << (7 * i)
            if not b & 0x80:
                need(v <= 0xFFFFFFFF and (i == 0 or b), "OTS varuint")
                return v
        raise Refused("OTS varuint")

    need(take(len(magic)) == magic and varuint() == 1 and take(1) == b"\x08", "not an OTS proof")
    need(take(32) == digest, "the OTS proof is not over this file")
    found, stack = [], [(digest, 0)]
    while stack:                                       # the prototype's iterative walk (prototype/e2e/otsutil.py)
        msg, depth = stack.pop()
        need(depth <= 256, "OTS depth")
        if raw[pos[0]:pos[0] + 1] == b"\xff":            # fork: this node continues after the branch that follows
            take(1)
            stack.append((msg, depth))
        op = take(1)[0]
        if op == 0x00:
            tag, payload = take(8), take(varuint())
            if tag == bytes.fromhex("0588960d73d71901"):
                v, i = 0, 0
                for i, b in enumerate(payload):
                    v |= (b & 0x7F) << (7 * i)
                    if not b & 0x80:
                        break
                need(payload and i == len(payload) - 1 and len(msg) == 32, "OTS bitcoin attestation")
                found.append((v, msg))
        elif op in (0x08, 0xF0, 0xF1):
            arg = b"" if op == 0x08 else take(varuint())
            need(op == 0x08 or 1 <= len(arg) <= 4096, "OTS operation argument")
            stack.append((hashlib.sha256(msg).digest() if op == 0x08 else (msg + arg if op == 0xF0 else arg + msg), depth + 1))
        else:
            raise Refused("OTS operation %#x outside the profile grammar" % op)
    need(pos[0] == len(raw), "trailing bytes in the OTS proof")
    return found


def baseline(repo, commit, source):
    """The proof is committed after the commit it stamps, so it is read from the source commit's tree."""
    commit, source = resolve(repo, commit), resolve(repo, source)
    tree = blobs_at(repo, source)
    stamp, proof = "timestamps/anchored/" + commit, "timestamps/anchored/" + commit + ".ots"
    need(stamp in tree and proof in tree, "no anchored OpenTimestamps proof for %s at %s" % (commit, source))
    data = read_blob(repo, tree[stamp])
    need(data == (commit + "\n").encode(), "the stamped file is not the commit id")
    atts = ots_heights(read_blob(repo, tree[proof]), hashlib.sha256(data).digest())
    need(atts, "the proof has no Bitcoin attestation (pending only)")
    height, root = min(atts)
    headers = []
    for api in EXPLORERS:
        bh = fetch("%s/block-height/%d" % (api, height))
        hdr = bytes.fromhex(fetch("%s/block/%s/header" % (api, bh)))
        need(len(hdr) == 80 and hashlib.sha256(hashlib.sha256(hdr).digest()).digest()[::-1].hex() == bh,
             "%s: header does not hash to its block id" % api)
        headers.append(hdr)
    need(headers[0] == headers[1], "the two explorers disagree on block %d" % height)
    need(headers[0][36:68] == root, "the proof's merkle root is not block %d's" % height)
    git(repo, "merge-base", "--is-ancestor", FREEZE_COMMIT, commit)
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int.from_bytes(headers[0][68:72], "little")))
    print("BASELINE PASS: %s existed by Bitcoin block %d, header time %s (blockstream.info and mempool.space agree);"
          % (commit, height, t))
    print("  freeze commit %s is its ancestor." % FREEZE_COMMIT)


# ---- the author's check ----

def v4_fingerprint(body):
    return hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).hexdigest().upper()


def groups(h, k=4):
    return " ".join(h[i:i + k] for i in range(0, len(h), k))


def check(archive_path, repo):
    data = open(archive_path, "rb").read()
    parts = parse_archive(data)
    m, t, cpath = check_bindings(parts)
    tree = blobs_at(repo, m["source_commit"])
    for p, b in parts.items():
        if p != "RELEASE.json":
            need(p in tree and read_blob(repo, tree[p]) == b, "part differs from its blob at the source commit: " + p)
    freeze = blobs_at(repo, FREEZE_COMMIT)
    record = read_blob(repo, freeze[FREEZE_RECORD])
    need(sha(record) == m["freeze_record_sha256"], "freeze record hash")
    need(("`catalog.json` | 662 | `%s`" % m["catalog_sha256"]).encode() in record, "catalog hash not in the freeze record")
    need(parts[FROZEN_CATALOG] == read_blob(repo, freeze[FROZEN_CATALOG]), "catalog differs from the freeze commit's")
    print("CHECK PASS: grammar, R2 bindings, every part equals its blob at the source commit, catalog = freeze record.")
    print("  archive        %s  sha256 %s" % (os.path.basename(archive_path), groups(sha(data), 8)))
    print("  namespace      %s   release %s   successor %s" % (m["namespace"], m["release"], m["release_key_successor"]))
    print("  source commit  %s" % m["source_commit"])
    print("  freeze commit  %s   record sha256 %s" % (FREEZE_COMMIT, groups(m["freeze_record_sha256"], 8)))
    print("  catalog        sha256 %s" % groups(m["catalog_sha256"], 8))
    print("  trust file     sha256 %s   version %s   as_of %s" % (groups(m["trust_config_sha256"], 8), t["version"], t["as_of"]))
    print("  parts          %d" % len(parts))
    for k in t["repository_keys"]:
        print("  repository key %s  from %s to %s" % (groups(v4_fingerprint(base64.b64decode(k["key"]))),
                                                   k["signing_start"], k["signing_end"]))
    for k in t["root_ksks"]:
        print("  root KSK       %s tag %s DS %s" % (k["name"], k["key_tag"], groups(k["ds_sha256"], 8)))
    hs = sorted(int(h) for h in t["header_pins"])
    print("  header pins    %d heights: %s" % (len(hs), " ".join(str(h) for h in hs)))


def fetch(url):
    """Through Tails' Tor SOCKS port when present; curl is used because urllib has no SOCKS support."""
    args = ["curl", "-fsS", "--max-time", "60", "-A", "tessera-release-check"]
    if os.path.exists("/etc/amnesia"):
        args += ["--socks5-hostname", "127.0.0.1:9050"]
    return subprocess.run(args + [url], check=True, capture_output=True).stdout.decode().strip()


def sources(archive_path):
    m, t, _ = check_bindings(parse_archive(open(archive_path, "rb").read()))
    xml = fetch("https://data.iana.org/root-anchors/root-anchors.xml")
    for k in t["root_ksks"]:
        hit = re.search(r"<KeyTag>%s</KeyTag>\s*<Algorithm>%s</Algorithm>\s*<DigestType>2</DigestType>\s*<Digest>%s</Digest>"
                        % (k["key_tag"], k["algorithm"], k["ds_sha256"].upper()), xml)
        need(hit, "IANA root-anchors.xml does not list %s tag %s with this digest" % (k["name"], k["key_tag"]))
        print("  %s tag %s: digest equals IANA root-anchors.xml" % (k["name"], k["key_tag"]))
    for h, pin in sorted(t["header_pins"].items(), key=lambda x: int(x[0])):
        got = [fetch("%s/block-height/%s" % (api, h)) for api in EXPLORERS]
        need(got[0] == got[1] == pin, "pin %s: blockstream %s, mempool %s" % (h, got[0], got[1]))
        print("  height %s: pin equals blockstream.info and mempool.space" % h)
    print("SOURCES PASS: %d KSKs and %d pins equal their public sources." % (len(t["root_ksks"]), len(t["header_pins"])))


# ---- R3: rule-O signature and the release key ----

def dearmor(raw):
    if not raw.startswith(b"-----BEGIN PGP PUBLIC KEY BLOCK-----"):
        return raw
    lines = raw.decode("ascii").splitlines()
    end = lines.index("-----END PGP PUBLIC KEY BLOCK-----")
    body = lines[1:end]
    body = body[body.index("") + 1:]                       # skip armor headers up to the blank line
    return base64.b64decode("".join(l for l in body if not l.startswith("=")), validate=True)


def packets(data):
    out, pos = [], 0
    while pos < len(data):
        b = data[pos]
        need(b & 0x80, "not an OpenPGP packet")
        if b & 0x40:                                        # new format
            tag, o = b & 0x3F, data[pos + 1]
            if o < 192:
                n, h = o, 2
            elif o < 224:
                n, h = ((o - 192) << 8) + data[pos + 2] + 192, 3
            else:
                need(o == 255, "partial lengths are not allowed")
                n, h = int.from_bytes(data[pos + 2:pos + 6], "big"), 6
        else:
            tag, lt = (b >> 2) & 0x0F, b & 3
            need(lt != 3, "indeterminate length")
            k = 1 << lt
            n, h = int.from_bytes(data[pos + 1:pos + 1 + k], "big"), 1 + k
        need(pos + h + n <= len(data), "truncated packet")
        out.append((tag, data[pos + h:pos + h + n]))
        pos += h + n
    return out


def release_key(path, fingerprint):
    """The key file must hold exactly one v4 ECDSA P-256 primary key, no subkeys, whose fingerprint is F."""
    raw = dearmor(open(path, "rb").read())
    pk = packets(raw)
    need(pk and pk[0][0] == 6 and [t for t, _ in pk].count(6) == 1, "the key file must hold exactly one primary key")
    need(not any(t in (5, 7, 14) for t, _ in pk), "the key file holds a subkey or a secret key")
    need(all(t in (2, 6, 12, 13) for t, _ in pk), "the key file holds an unexpected packet")
    body = pk[0][1]
    need(body[0] == 4 and body[5] == 19 and body[6] == 8 and body[7:15] == P256_OID, "not a v4 ECDSA P-256 key")
    fpr = v4_fingerprint(body)
    need(fpr == fingerprint, "the key file's fingerprint %s is not the authenticated %s" % (fpr, fingerprint))
    return raw


def subpackets(raw):
    out, pos = [], 0
    while pos < len(raw):
        o = raw[pos]
        if o < 192:
            n, pos = o, pos + 1
        elif o < 255:
            n, pos = ((o - 192) << 8) + raw[pos + 1] + 192, pos + 2
        else:
            n, pos = int.from_bytes(raw[pos + 1:pos + 5], "big"), pos + 5
            need(n >= 16320, "subpacket length")
        need(n >= 1 and pos + n <= len(raw), "subpacket length")
        out.append((raw[pos] & 0x7F, bool(raw[pos] & 0x80), raw[pos + 1:pos + n]))
        pos += n
    return out


def rule_o(sig):
    """Profile section 8 rule O, type 0x00: exactly one old-format v4 ECDSA/SHA-256 signature packet. Returns the
    hashed issuer fingerprint if the signature carries one, else None (rule O allows its absence; the signer is then
    established by gpgv with the sole authenticated key)."""
    need(len(sig) <= 1024 and len(sig) >= 2 and sig[0] in (0x88, 0x89), "not one unarmored old-format signature packet")
    n, h = (sig[1], 2) if sig[0] == 0x88 else (int.from_bytes(sig[1:3], "big"), 3)
    need(sig[0] == 0x88 or n > 255, "non-minimal length")
    need(h + n == len(sig), "trailing bytes or a second signature")
    b = sig[h:]
    need(b[:4] == b"\x04\x00\x13\x08", "not v4, type 0x00, ECDSA, SHA-256")
    hl = int.from_bytes(b[4:6], "big"); hashed = subpackets(b[6:6 + hl]); pos = 6 + hl
    ul = int.from_bytes(b[pos:pos + 2], "big"); subpackets(b[pos + 2:pos + 2 + ul]); pos += 2 + ul + 2
    vals = []
    for _ in range(2):
        bits = int.from_bytes(b[pos:pos + 2], "big"); k = (bits + 7) // 8
        need(1 <= bits <= 256, "MPI size"); v = int.from_bytes(b[pos + 2:pos + 2 + k], "big")
        need(v.bit_length() == bits, "non-minimal MPI"); vals.append(v); pos += 2 + k
    need(pos == len(b), "trailing bytes in the signature body")
    need(all(1 <= v < N for v in vals), "r or s out of range")
    created = [d for t, _, d in hashed if t == 2]
    ids = [d for t, _, d in hashed if t == 16]
    fps = [d for t, _, d in hashed if t == 33]
    need(len(created) == 1 and len(created[0]) == 4, "creation time")
    need(len(ids) <= 1 and all(len(d) == 8 for d in ids), "issuer id")
    need(len(fps) <= 1 and all(len(d) == 21 and d[0] == 4 for d in fps), "issuer fingerprint subpacket")
    need(not ids or not fps or ids[0] == fps[0][-8:], "issuer id and fingerprint disagree")
    for t, crit, _ in hashed:
        need(t != 3 and (t in (2, 16, 33) or not crit), "signature policy (expiry or unknown critical subpacket)")
    return fps[0][1:].hex().upper() if fps else None


def verify_bytes(data, sig, fingerprint, key_path, gpgv="gpgv"):
    """R3 over bytes already read once: gpgv sees only a private copy written from these same bytes (review H2)."""
    need(re.fullmatch(r"[0-9A-F]{40}", fingerprint), "the fingerprint must be 40 uppercase hex, no spaces")
    issuer = rule_o(sig)
    need(issuer in (None, fingerprint), "signed by %s, not by the authenticated key %s" % (issuer, fingerprint))
    ring = release_key(key_path, fingerprint)
    with tempfile.TemporaryDirectory() as home:
        os.chmod(home, 0o700)
        paths = {}
        for name, b in (("release.pgp", ring), ("archive", data), ("archive.sig", sig)):
            paths[name] = os.path.join(home, name)
            with open(paths[name], "xb") as f:
                f.write(b)
        r = subprocess.run([gpgv, "--homedir", home, "--keyring", paths["release.pgp"], paths["archive.sig"],
                            paths["archive"]], capture_output=True, text=True)
    need(r.returncode == 0, "gpgv refused (exit %d): %s" % (r.returncode, r.stderr.strip().splitlines()[-1:]))
    return fingerprint


def verify_sig(archive_path, sig_path, fingerprint, key_path, gpgv="gpgv"):
    return verify_bytes(open(archive_path, "rb").read(), open(sig_path, "rb").read(), fingerprint, key_path, gpgv)


def acquire(archive_path, sig_path, fingerprint, key_path, out=None, gpgv="gpgv", namespace="PRODUCTION", install=True):
    """Read once, check, then (with out) unpack and install. Returns (manifest, sha256 of the bytes consumed)."""
    data, sig = open(archive_path, "rb").read(), open(sig_path, "rb").read()
    verify_bytes(data, sig, fingerprint, key_path, gpgv)
    parts = parse_archive(data)
    m, _, _ = check_bindings(parts)
    need(m["namespace"] == namespace, "the archive's namespace is %s, not the expected %s" % (m["namespace"], namespace))
    if out is not None:
        unpack(parts, out)
        if install:
            root = os.path.realpath(out)
            env = dict(os.environ, TESSERA_ACQUIRED_ROOT=root)
            r = subprocess.run(["bash", os.path.join(root, *V.split("/"), "install.sh")], env=env)
            need(r.returncode == 0, "install.sh failed (exit %d) in %s" % (r.returncode, root))
    return m, sha(data)


def unpack(parts, out):
    os.makedirs(out)                                       # must be new
    for p, b in parts.items():
        dest = os.path.join(out, *p.split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "xb") as f:
            f.write(b)


def bindings(root):
    """install.sh, before it writes anything: the tree holds exactly RELEASE.json and the manifest's parts (no extra,
    missing or linked file), and every R2 equality holds over the bytes read here."""
    found = set()
    for d, dirs, files in os.walk(root):
        for x in dirs + files:
            full = os.path.join(d, x)
            need(not os.path.islink(full), "a link in the release tree: " + os.path.relpath(full, root))
        for x in files:
            full = os.path.join(d, x)
            need(os.path.isfile(full), "not a regular file: " + os.path.relpath(full, root))
            found.add(os.path.relpath(full, root).replace(os.sep, "/"))
    raw = open(os.path.join(root, "RELEASE.json"), "rb").read()
    m = load_json(raw, "RELEASE.json")
    need(isinstance(m, dict) and isinstance(m.get("parts"), dict), "RELEASE.json")
    want = set(m["parts"]) | {"RELEASE.json"}
    need(found == want, "the tree is not exactly the release: extra %s, missing %s"
         % (sorted(found - want)[:5], sorted(want - found)[:5]))
    parts = {"RELEASE.json": raw}
    for p in m["parts"]:
        need(isinstance(p, str) and HEADER.fullmatch(("tessera-v1-part %s 0\n" % p).encode()), "bad path")
        parts[p] = open(os.path.join(root, *p.split("/")), "rb").read()
    _, _, cpath = check_bindings(parts)
    return cpath


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--repo", default="."); b.add_argument("--commit", required=True)
    b.add_argument("--namespace", default="PRODUCTION", choices=("PRODUCTION", "TEST"))
    b.add_argument("--release", default="1"); b.add_argument("--out", required=True)
    f = sub.add_parser("diff"); f.add_argument("--repo", default="."); f.add_argument("--base", required=True)
    f.add_argument("--commit", required=True); f.add_argument("--release", default="1"); f.add_argument("--out", required=True)
    e = sub.add_parser("baseline"); e.add_argument("--repo", default="."); e.add_argument("--commit", required=True)
    e.add_argument("--source", required=True)
    c = sub.add_parser("check"); c.add_argument("archive"); c.add_argument("--repo", default=".")
    s = sub.add_parser("sources"); s.add_argument("archive")
    n = sub.add_parser("inspect"); n.add_argument("archive")
    for name in ("verify-sig", "acquire"):
        v = sub.add_parser(name); v.add_argument("archive"); v.add_argument("sig")
        v.add_argument("--fingerprint", required=True); v.add_argument("--key", required=True)
        v.add_argument("--gpgv", default="gpgv")
        if name == "acquire":
            v.add_argument("--out"); v.add_argument("--namespace", default="PRODUCTION", choices=("PRODUCTION", "TEST"))
    k = sub.add_parser("constants"); k.add_argument("--trust", required=True); k.add_argument("--catalog", required=True)
    k.add_argument("--namespace", default="PRODUCTION", choices=("PRODUCTION", "TEST")); k.add_argument("--out", required=True)
    i = sub.add_parser("bindings"); i.add_argument("root")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            need(DEC.fullmatch(a.release) and a.release != "0", "release number")
            name, data = build(a.repo, a.commit, a.namespace, a.release)
            os.makedirs(a.out, exist_ok=True)
            with open(os.path.join(a.out, name), "xb") as fh:
                fh.write(data)
            print("BUILT %s  sha256 %s" % (name, groups(sha(data), 8)))
        elif a.cmd == "diff":
            text, line = diff(a.repo, a.base, a.commit, a.release)
            with open(a.out, "xb") as fh:
                fh.write(text)
            print(line)
        elif a.cmd == "baseline":
            baseline(a.repo, a.commit, a.source)
        elif a.cmd == "check":
            check(a.archive, a.repo)
        elif a.cmd == "sources":
            sources(a.archive)
        elif a.cmd == "inspect":
            data = open(a.archive, "rb").read()
            m, _, _ = check_bindings(parse_archive(data))
            print("INSPECT PASS: %s release %s, %d parts, R2 bindings hold." % (m["namespace"], m["release"], len(m["parts"]) + 1))
            print("  sha256 %s" % groups(sha(data), 8))
        elif a.cmd == "verify-sig":
            verify_sig(a.archive, a.sig, a.fingerprint, a.key, a.gpgv)
            print("SIGNATURE PASS: rule O, signer %s, gpgv exit 0 with only that key." % groups(a.fingerprint))
        elif a.cmd == "acquire":
            m, h = acquire(a.archive, a.sig, a.fingerprint, a.key, a.out, a.gpgv, a.namespace)
            print("ACQUIRED %s release %s, sha256 %s%s" % (m["namespace"], m["release"], groups(h, 8),
                  "; unpacked into %s and installed" % a.out if a.out else "; not unpacked (no --out)"))
        elif a.cmd == "constants":
            trust, catalog = open(a.trust, "rb").read(), open(a.catalog, "rb").read()
            with open(a.out, "xb") as fh:
                fh.write(constants_source(a.namespace, trust, catalog))
        elif a.cmd == "bindings":
            print(bindings(a.root))
    except Refused as e:
        print("REFUSED: %s" % e, file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print("REFUSED: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
