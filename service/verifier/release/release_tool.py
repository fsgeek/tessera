#!/usr/bin/env python3
"""Tessera V1 verifier release tool (profile section 15.9 R1-R5). Standard library only; Python 3.9 or later.
It runs on the NUC, on Tails (the author's sitting) and on a relying party's machine. It never signs.

  build     --repo R --commit C [--namespace PRODUCTION] [--release 1] --out DIR
            Assemble tessera-verifier-v1[-TEST]-<n>.parts from tracked blob bytes at commit C (R1), generate
            RELEASE.json (R2), check every R2 binding equality, print the archive SHA-256. Deterministic.
  check     ARCHIVE --repo R
            The author's check: archive grammar, R2 equalities, every part equal to its blob at the named source
            commit, the catalog and freeze record equal to the freeze commit's, then a summary to compare by eye.
  sources   ARCHIVE
            Networked (Tor on Tails): KSK digests against IANA root-anchors.xml; header pins against two explorers.
  verify-sig ARCHIVE SIG --fingerprint F --key KEY [--gpgv P]
            R3 acceptance: one unarmored rule-O signature whose issuer is F, then gpgv with a keyring holding only
            the key KEY, whose own fingerprint must be F.
  acquire   ARCHIVE SIG --fingerprint F --key KEY --out DIR [--gpgv P]
            verify-sig, then R2 equalities, then unpack into a new directory DIR. Run DIR/service/verifier/install.sh.
  bindings  ROOT
            install.sh's check of R2 on an unpacked release; prints the release_constants.py path to install.

F is the release key's full fingerprint as the relying party obtained it out of band (R5): never from the release.
"""
import argparse
import ast
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

FREEZE_COMMIT = "52ee17918c5ed841587d78cb2ca3e8c54c4682d2"   # the author's freeze-record commit (OTS-anchored)
FREEZE_RECORD = "formal/freeze-v1/FREEZE-RECORD.md"
FREEZE_RECORD_SHA256 = "05542967b091424a614afd38a32cfb847b9b6b3f0e5a7b7103b11cd22d95575e"
FROZEN_CATALOG = "formal/freeze-v1/objects/catalog.json"
FROZEN_CATALOG_SHA256 = "aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2"
V = "service/verifier/"
FILES = ["docs/V1-RELYING-PARTY.md", FROZEN_CATALOG, V + "README.md", V + "install.sh", V + "pyproject.toml",
         V + "requirements.lock", V + "release/release_tool.py"]
DIRS = [V + "tessera_verify/", V + "vendor/"]
EXCLUDE = {V + "tessera_verify/release_constants.py"}          # the source tree's unprovisioned copy
MANIFEST_KEYS = {"format", "namespace", "release", "profile", "source_commit", "trust_config_sha256",
                 "trust_config_version", "catalog_sha256", "freeze_record_sha256", "parts", "release_key_successor"}
CONSTANT_NAMES = ["NAMESPACE", "TRUST_SHA256", "CATALOG_SHA256", "CATALOG_BYTES", "UNICODE_VERSION"]
HEADER = re.compile(rb"tessera-v1-part ([A-Za-z0-9._/-]+) (0|[1-9][0-9]*)\n")
HEX64, DEC = re.compile(r"[0-9a-f]{64}"), re.compile(r"0|[1-9][0-9]*")
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551   # P-256 group order
P256_OID = bytes.fromhex("2a8648ce3d030107")


class Refused(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Refused(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def jcs(obj):  # RFC 8785 for this manifest: ASCII strings, null and objects only, no numbers
    out = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    need(out.isascii(), "manifest is not ASCII")
    return out.encode()


def stem(namespace, n):
    return "tessera-verifier-v1-%s%s" % ("TEST-" if namespace == "TEST" else "", n)


def release_dir(namespace, n):
    return V + "release/v1-%s%s/" % ("TEST-" if namespace == "TEST" else "", n)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), check=True, capture_output=True).stdout


def blobs_at(repo, commit):
    """{path: bytes} of tracked regular files at commit: no working tree, no newline conversion, no symlinks."""
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
    """Every R2 binding equality. Returns (manifest, trust object, constants path)."""
    need("RELEASE.json" in parts, "no RELEASE.json")
    raw = parts["RELEASE.json"]
    m = json.loads(raw)
    need(isinstance(m, dict) and set(m) == MANIFEST_KEYS and jcs(m) == raw, "RELEASE.json is not the closed JCS object")
    need(m["format"] == "tessera-v1-release/1" and m["profile"] == "tessera-v1-strict", "format or profile")
    need(m["namespace"] in ("PRODUCTION", "TEST"), "namespace")
    need(isinstance(m["release"], str) and DEC.fullmatch(m["release"]) and m["release"] != "0", "release number")
    need(isinstance(m["source_commit"], str) and re.fullmatch(r"[0-9a-f]{40}", m["source_commit"]), "source_commit")
    for k in ("trust_config_sha256", "catalog_sha256", "freeze_record_sha256"):
        need(isinstance(m[k], str) and HEX64.fullmatch(m[k]), k)
    s = m["release_key_successor"]
    need(s is None or (isinstance(s, str) and re.fullmatch(r"[0-9A-F]{40}", s)), "release_key_successor")
    others = {p: b for p, b in parts.items() if p != "RELEASE.json"}
    need(isinstance(m["parts"], dict) and set(m["parts"]) == set(others), "parts paths differ from the archive's")
    for p, b in others.items():
        need(m["parts"][p] == sha(b), "part hash differs: " + p)
    d = release_dir(m["namespace"], m["release"])
    tpath, cpath = d + "trust.json", d + "release_constants.py"
    need(tpath in others and cpath in others and FROZEN_CATALOG in others, "a required part is missing")
    trust, catalog = others[tpath], others[FROZEN_CATALOG]
    c = parse_constants(others[cpath])
    need(sha(trust) == m["trust_config_sha256"] == c["TRUST_SHA256"], "trust hash binding")
    need(sha(catalog) == m["catalog_sha256"] == c["CATALOG_SHA256"] and c["CATALOG_BYTES"] == catalog, "catalog binding")
    t = json.loads(trust)
    need(isinstance(t, dict) and t.get("version") == m["trust_config_version"], "trust version binding")
    need(c["NAMESPACE"] == m["namespace"] and c["UNICODE_VERSION"] == "16.0.0", "namespace binding")
    if m["namespace"] == "PRODUCTION":
        need(m["freeze_record_sha256"] == FREEZE_RECORD_SHA256 and m["catalog_sha256"] == FROZEN_CATALOG_SHA256,
             "PRODUCTION catalog is not the freeze record's")
    return m, t, cpath


# ---- build ----

def build(repo, commit, namespace, n):
    commit = git(repo, "rev-parse", "--verify", commit + "^{commit}").decode().strip()
    tree = blobs_at(repo, commit)
    d = release_dir(namespace, n)
    want = set(FILES) | {d + "trust.json", d + "release_constants.py"}
    want |= {p for p in tree if any(p.startswith(x) for x in DIRS)} - EXCLUDE
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
        got = [fetch("%s/block-height/%s" % (api, h)) for api in ("https://blockstream.info/api", "https://mempool.space/api")]
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
    issuer fingerprint from the hashed subpackets (required here: acceptance needs the signer's identity)."""
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
    need(len(fps) == 1 and len(fps[0]) == 21 and fps[0][0] == 4, "issuer fingerprint subpacket")
    need(not ids or ids[0] == fps[0][-8:], "issuer id and fingerprint disagree")
    for t, crit, _ in hashed:
        need(t != 3 and (t in (2, 16, 33) or not crit), "signature policy (expiry or unknown critical subpacket)")
    return fps[0][1:].hex().upper()


def verify_sig(archive_path, sig_path, fingerprint, key_path, gpgv="gpgv"):
    need(re.fullmatch(r"[0-9A-F]{40}", fingerprint), "the fingerprint must be 40 uppercase hex, no spaces")
    issuer = rule_o(open(sig_path, "rb").read())
    need(issuer == fingerprint, "signed by %s, not by the authenticated key %s" % (issuer, fingerprint))
    ring = release_key(key_path, fingerprint)
    with tempfile.TemporaryDirectory() as home:
        os.chmod(home, 0o700)
        kr = os.path.join(home, "release.pgp")
        open(kr, "wb").write(ring)
        r = subprocess.run([gpgv, "--homedir", home, "--keyring", kr, sig_path, archive_path], capture_output=True, text=True)
    need(r.returncode == 0, "gpgv refused (exit %d): %s" % (r.returncode, r.stderr.strip().splitlines()[-1:]))
    return issuer


def acquire(archive_path, sig_path, fingerprint, key_path, out, gpgv="gpgv"):
    verify_sig(archive_path, sig_path, fingerprint, key_path, gpgv)
    parts = parse_archive(open(archive_path, "rb").read())
    m, _, _ = check_bindings(parts)
    unpack(parts, out)
    return m


def unpack(parts, out):
    os.makedirs(out)                                       # must be new
    for p, b in parts.items():
        dest = os.path.join(out, *p.split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "xb") as f:
            f.write(b)


def bindings(root):
    """install.sh: re-read every part from the unpacked tree and check R2 before anything is installed."""
    m = json.loads(open(os.path.join(root, "RELEASE.json"), "rb").read())
    need(isinstance(m, dict) and isinstance(m.get("parts"), dict), "RELEASE.json")
    parts = {"RELEASE.json": open(os.path.join(root, "RELEASE.json"), "rb").read()}
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
    c = sub.add_parser("check"); c.add_argument("archive"); c.add_argument("--repo", default=".")
    s = sub.add_parser("sources"); s.add_argument("archive")
    for name in ("verify-sig", "acquire"):
        v = sub.add_parser(name); v.add_argument("archive"); v.add_argument("sig")
        v.add_argument("--fingerprint", required=True); v.add_argument("--key", required=True)
        v.add_argument("--gpgv", default="gpgv")
        if name == "acquire":
            v.add_argument("--out", required=True)
    k = sub.add_parser("constants"); k.add_argument("--trust", required=True); k.add_argument("--catalog", required=True)
    k.add_argument("--namespace", default="PRODUCTION", choices=("PRODUCTION", "TEST")); k.add_argument("--out", required=True)
    i = sub.add_parser("bindings"); i.add_argument("root")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            need(DEC.fullmatch(a.release) and a.release != "0", "release number")
            name, data = build(a.repo, a.commit, a.namespace, a.release)
            os.makedirs(a.out, exist_ok=True)
            with open(os.path.join(a.out, name), "xb") as f:
                f.write(data)
            print("BUILT %s  sha256 %s" % (name, groups(sha(data), 8)))
        elif a.cmd == "check":
            check(a.archive, a.repo)
        elif a.cmd == "sources":
            sources(a.archive)
        elif a.cmd == "verify-sig":
            verify_sig(a.archive, a.sig, a.fingerprint, a.key, a.gpgv)
            print("SIGNATURE PASS: rule O, signer %s, gpgv exit 0 with only that key." % groups(a.fingerprint))
        elif a.cmd == "acquire":
            m = acquire(a.archive, a.sig, a.fingerprint, a.key, a.out, a.gpgv)
            print("ACQUIRED %s release %s into %s. Next: bash %s/service/verifier/install.sh" % (m["namespace"], m["release"], a.out, a.out))
        elif a.cmd == "constants":
            trust, catalog = open(a.trust, "rb").read(), open(a.catalog, "rb").read()
            with open(a.out, "xb") as f:
                f.write(constants_source(a.namespace, trust, catalog))
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
