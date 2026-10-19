#!/usr/bin/env python3
"""TEST repository key and the git key-assertion commit (V1-PROFILE §6.3, §15.4).

The key is a THROWAWAY P-256 OpenPGP key made by GnuPG in a fresh GNUPGHOME created with mkdtemp under
prototype/e2e/work/ (never ~/.gnupg). It stands in for the repository root (YubiKey 2 later); the verifier path it
exercises is the same: v4 ECDSA P-256 public-key body in the trust configuration, rule-O `gpgsig` on the commit.

The repository is a local git repository under work/. Git and GnuPG run with GIT_CONFIG_GLOBAL=/dev/null and
GIT_CONFIG_NOSYSTEM=1 so that no user configuration (signing format, hooks, templates) reaches the commit.

  uv run python e2e/repo.py key   [--dir work/repo-key]
  uv run python e2e/repo.py commit --key-dir D --repo R --kms-hex H --gpg-hex H --not-before T --not-after T
  uv run python e2e/repo.py value --kms-hex H --gpg-hex H --not-before T --not-after T     # print the 255-byte value

The commit is NOT stamped here: stamping is the driver's `stamp-git` stage (OpenTimestamps, network).
"""
import argparse
import os
import struct
import subprocess
import tempfile
from pathlib import Path

from common import WORK, U, gen, b64, sha256hex, write_atomic, write_json, read_json, log, now

ASSERTION_PATH = "tessera-v1/key-assertion"


class RepoError(Exception):
    pass


def assertion_value(kms_hex, gpg_hex, not_before, not_after):
    """The ENC §7 canonical value: exactly 255 bytes, no trailing LF; also the TXT record's one string."""
    v = gen.dns_value(kms_hex, gpg_hex, not_after, not_before).encode()
    if len(v) != 255:
        raise RepoError(f"value is {len(v)} bytes, not 255")
    if U.ts(not_after) <= U.ts(not_before) or U.ts(not_after) - U.ts(not_before) > 90 * 86400:
        raise RepoError("window must be non-empty and at most 90 days")
    return v


# ------------------------------------------------------------------------------------------------ key
def _gpg(home, *args, input=None):
    env = dict(os.environ, GNUPGHOME=str(home))
    r = subprocess.run(["gpg", "--batch", "--no-tty", *args], env=env, input=input, capture_output=True)
    if r.returncode:
        raise RepoError("gpg " + " ".join(args[:2]) + ": " + r.stderr.decode(errors="replace").strip())
    return r.stdout


def _packets(data):
    """[(tag, body)] of a binary OpenPGP packet stream (old and new formats)."""
    out, i = [], 0
    while i < len(data):
        h = data[i]
        if not h & 0x80:
            raise RepoError("not a packet")
        if h & 0x40:
            tag, l0 = h & 0x3F, data[i + 1]
            if l0 < 192:
                n, j = l0, i + 2
            elif l0 < 224:
                n, j = ((l0 - 192) << 8) + data[i + 2] + 192, i + 3
            else:
                n, j = struct.unpack(">I", data[i + 2:i + 6])[0], i + 6
        else:
            tag, lt = (h >> 2) & 0x0F, h & 3
            w = {0: 1, 1: 2, 2: 4}[lt]
            n, j = int.from_bytes(data[i + 1:i + 1 + w], "big"), i + 1 + w
        out.append((tag, data[j:j + n]))
        i = j + n
    return out


def make_key(key_dir=None):
    """Create (once) the TEST repository key. -> key record dict (public data + the GNUPGHOME path)."""
    key_dir = Path(key_dir or WORK / "repo-key")
    rec_file = key_dir / "repo-key.json"
    if rec_file.exists():
        return read_json(rec_file)
    key_dir.mkdir(parents=True, exist_ok=True)
    home = Path(tempfile.mkdtemp(prefix="gnupghome-", dir=key_dir))   # fresh, 0700, under work/
    (home / "gpg.conf").write_text("personal-digest-preferences SHA256\ndigest-algo SHA256\ncert-digest-algo SHA256\n"
                                   "no-emit-version\nno-comments\n")
    uid = "TEST Tessera V1 repository key (throwaway, e2e instrument) <test-repo@invalid>"
    _gpg(home, "--pinentry-mode", "loopback", "--passphrase", "", "--quick-gen-key", uid, "nistp256", "sign", "never")
    fpr = [ln.split(b":")[9].decode() for ln in _gpg(home, "--with-colons", "--list-keys").splitlines()
           if ln.startswith(b"fpr:")][0]
    exported = _gpg(home, "--export", fpr)
    tag, body = _packets(exported)[0]
    if tag != 6 or body[0] != 4 or body[5] != 19 or body[6:15] != bytes([8]) + bytes.fromhex("2a8648ce3d030107"):
        raise RepoError("not a v4 ECDSA P-256 primary key")
    created = struct.unpack(">I", body[1:5])[0]
    point = body[17:]
    if body[15:17] != struct.pack(">H", 515) or len(point) != 65 or gen.openpgp_v4_body(point, created) != body:
        raise RepoError("unexpected public-key body layout")
    write_atomic(key_dir / "repo-key.pub.gpg", exported)
    rec = {"TEST": "throwaway repository key; GnuPG private key lives in gnupghome (work/, git-ignored)",
           "gnupghome": str(home), "fpr_v4": fpr, "created": created, "created_rfc3339": U.rfc3339(created),
           "pgp_body_b64": b64(body), "point_hex": point.hex(),
           "export_file": str(key_dir / "repo-key.pub.gpg"), "export_sha256": sha256hex(exported)}
    write_json(rec_file, rec)
    log(f"TEST repository key {fpr} created {rec['created_rfc3339']} in {home}")
    return rec


def stop_agent(key):
    subprocess.run(["gpgconf", "--kill", "gpg-agent"], env=dict(os.environ, GNUPGHOME=key["gnupghome"]),
                   capture_output=True)


# ------------------------------------------------------------------------------------------------ repository
def _git(repo, *args, key=None, input=None):
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", LC_ALL="C")
    if key:
        env["GNUPGHOME"] = key["gnupghome"]
    r = subprocess.run(["git", "-C", str(repo), *args], env=env, input=input, capture_output=True)
    if r.returncode:
        raise RepoError("git " + " ".join(args[:2]) + ": " + r.stderr.decode(errors="replace").strip())
    return r.stdout


def commit_assertion(key, repo, value, out_dir):
    """Write the blob at tessera-v1/key-assertion (no framing), commit signed by the TEST key, and export the git
    evidence (raw commit, root and sub trees, blob, the stamp input `<40-hex id>\\n`) into out_dir."""
    repo, out_dir = Path(repo), Path(out_dir)
    if (out_dir / "git-evidence.json").exists():
        return read_json(out_dir / "git-evidence.json")
    repo.mkdir(parents=True, exist_ok=True)
    if not (repo / ".git").exists():
        _git(repo, "init", "-q", "-b", "main")
    for k, v in (("user.name", "TEST Tessera issuer"), ("user.email", "test-issuer@invalid"),
                 ("user.signingkey", key["fpr_v4"]), ("gpg.format", "openpgp"), ("gpg.program", "gpg"),
                 ("commit.gpgsign", "true"), ("core.autocrlf", "false")):
        _git(repo, "config", k, v)
    (repo / "tessera-v1").mkdir(exist_ok=True)
    (repo / ASSERTION_PATH).write_bytes(value)
    (repo / "README").write_bytes(b"TEST issuer repository (prototype/e2e instrument). Not the Tessera repository.\n")
    _git(repo, "add", "README", ASSERTION_PATH)
    _git(repo, "commit", "-q", "-S" + key["fpr_v4"], "-m", "TEST: publish the tessera-v1 key assertion", key=key)
    cid = _git(repo, "rev-parse", "HEAD").decode().strip()
    commit = _git(repo, "cat-file", "commit", cid)
    root_id = _git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    sub_id = _git(repo, "rev-parse", "HEAD:tessera-v1").decode().strip()
    root, sub = _git(repo, "cat-file", "tree", root_id), _git(repo, "cat-file", "tree", sub_id)
    blob = _git(repo, "cat-file", "blob", "HEAD:" + ASSERTION_PATH)
    if blob != value:
        raise RepoError("blob bytes differ from the value")
    check_commit(commit, root, sub, blob, key)
    files = {"commit.bin": commit, "tree-root.bin": root, "tree-sub.bin": sub, "blob.bin": blob,
             "git-stamp.txt": (cid + "\n").encode()}
    for n, d in files.items():
        write_atomic(out_dir / n, d)
    ev = {"commit_id": cid, "repo": str(repo), "files": {n: sha256hex(d) for n, d in files.items()},
          "stamp_input": "git-stamp.txt (SHA-256 of the 40 lowercase hex commit id plus LF is the proof digest)"}
    write_json(out_dir / "git-evidence.json", ev)
    log(f"assertion commit {cid} signed by TEST key {key['fpr_v4'][-16:]}")
    return ev


def check_commit(commit, root, sub, blob, key):
    """Issuer pre-checks (P§15.4): ids, path, one gpgsig header and no other extra header, rule-O signature
    shape (P8 implementation A's codec) verifying over the payload under the TEST key."""
    end = commit.index(b"\n\n")
    heads = commit[:end].split(b"\n")
    names = [h.split(b" ", 1)[0] for h in heads if not h.startswith(b" ")]
    if names.count(b"gpgsig") != 1 or set(names) - {b"tree", b"parent", b"author", b"committer", b"gpgsig"}:
        raise RepoError(f"commit headers outside the closed grammar: {names}")
    payload_heads, armor, in_sig = [], [], False
    for h in heads:
        if h.startswith(b"gpgsig "):
            armor.append(h[7:])
            in_sig = True
        elif in_sig and h.startswith(b" "):
            armor.append(h[1:])
        else:
            in_sig = False
            payload_heads.append(h)
    payload = b"\n".join(payload_heads) + b"\n\n" + commit[end + 2:]
    al = armor
    if al[:2] != [b"-----BEGIN PGP SIGNATURE-----", b""] or al[-1] != b"-----END PGP SIGNATURE-----":
        raise RepoError("armor framing (headers or blank lines)")
    import base64
    sig = base64.b64decode(b"".join(x for x in al[2:-1] if not x.startswith(b"=")))
    gen.decode_sig_openpgp4(sig)       # rule-O codec and subpacket policy (raises Reject)
    if not gen.verify_openpgp4(payload, sig, (int(key["point_hex"][2:66], 16), int(key["point_hex"][66:], 16))):
        raise RepoError("gpgsig does not verify over the commit payload under the TEST key")
    tree_id = heads[0][5:].decode()
    if U.git_id("tree", root).hex() != tree_id:
        raise RepoError("commit tree id")
    if U.tree_entry("40000", "tessera-v1", U.git_id("tree", sub)) not in root:
        raise RepoError("root tree lacks tessera-v1 (40000)")
    if sub != U.tree_entry("100644", "key-assertion", U.git_id("blob", blob)):
        raise RepoError("sub tree is not exactly key-assertion (100644)")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["key", "commit", "value"])
    ap.add_argument("--dir", default=str(WORK / "repo-key"))
    ap.add_argument("--key-dir", default=str(WORK / "repo-key"))
    ap.add_argument("--repo", default=str(WORK / "issuer-repo"))
    ap.add_argument("--out", default=str(WORK / "git-evidence"))
    for f in ("kms-hex", "gpg-hex", "not-before", "not-after"):
        ap.add_argument("--" + f)
    a = ap.parse_args()
    if a.cmd == "key":
        print(make_key(a.dir)["fpr_v4"])
        return
    v = assertion_value(a.kms_hex, a.gpg_hex, a.not_before, a.not_after)
    if a.cmd == "value":
        print(v.decode())
        return
    k = make_key(a.key_dir)
    print(commit_assertion(k, a.repo, v, a.out)["commit_id"])


if __name__ == "__main__":
    main()
