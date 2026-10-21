#!/usr/bin/env python3
"""V1 freeze assembler (profile tessera-v1-strict, section 15.8, section 1 catalog entry, section 14.2 item 7).

Not the TEST assembler (prototype/e2e/freeze.py): no TEST marking in any object. Reads only tracked regular-file blob
bytes at ONE named commit (git ls-tree / cat-file; no working-tree overlay, no newline conversion, no symlink
following). Standard library only; imports nothing from prototype/.

Objects (written to OUT/objects/):
  spec.bin                  section 15.8 part object over SPEC_PATHS (PR-08: A9, A10, PROOF are parts)
  vectors.bin               section 15.8 part object, inventory per prototype/conformance/VECTORS-OBJECT.md
  preamble.bin              PREAMBLE below (DRAFT bytes; see FREEZE-RECORD-DRAFT.md)
  dependency-manifest.json  formal/dependency-sources/dependency-manifest.json, blob bytes verbatim
  catalog.json              section 1 catalog entry, RFC 8785 (all values strings, arrays or objects)
Hashes go in OUT/freeze-record.json, outside every part (section 15.8 "Hashes live outside").

  python3 assemble.py --repo DIR --commit C --out DIR        assemble
  python3 assemble.py --repo DIR --check OUT                 independent byte-agreement check (needs a clean
                                                             checkout of the record's commit at --repo)
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SPEC_PATHS = ["docs/V1-PROFILE.md", "docs/phase-0-prereg-amendment-9.md", "docs/phase-0-prereg-amendment-10.md",
              "formal/p8/ENCODING-V1.md", "formal/p8/HYBRID-SUPPLEMENT.md", "formal/p8/PROOF.md"]
SIGNED = {"docs/phase-0-prereg-amendment-9.md": "2ad3489", "docs/phase-0-prereg-amendment-10.md": "9ade764"}
DEPS_PATH = "formal/dependency-sources/dependency-manifest.json"

# VECTORS-OBJECT.md "Enters the vectors object"
P8_DIR = "formal/p8/vectors/"
CONF = "prototype/conformance/"
CONF_FILES = [CONF + f for f in ("cases-index.json", "cases.py", "issue.py", "universe.py", "tcrypto.py", "run.py")]
CASE_KEEP = {"expected.json", "previous.json", "next.json", "bundle.recipe.json", "base.json", "request.txt"}
CASE_DROP = {"bundle.json", "release.json", "trust.json", "catalog.json"}          # embed object hashes (EA-10)
EXPECT_COUNTS = {"expected.json": 352, "previous.json": 8, "next.json": 8, "bundle.recipe.json": 2, "base.json": 2,
                 "request.txt": 1}

SPEC_ID = "tessera-v1-strict/verification-spec/1"
ALG = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256"       # registered hybrid pair id (profile section 1)
D = "wamason.com"
DELTA_S, EPSILON_S, K = 72 * 3600, 24 * 3600, 6                  # profile section 1 "Parameters"
UTC_DELTA_S, UTC_M = 7200, 6                                     # profile section 7.4, A10:284-285

# The purpose preamble is an owner text in PREAMBLE.txt (2026-10-21); the draft that was embedded here overclaimed
# "presented to the Tessera V1 service", which is false when both authority channels are captured.
PREAMBLE = (Path(__file__).resolve().parent / "PREAMBLE.txt").read_bytes()

PATH_RE = re.compile(r"[A-Za-z0-9._/-]+")
HEAD_RE = re.compile(rb"tessera-v1-part ([A-Za-z0-9._/-]+) (0|[1-9][0-9]*)")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def ls_tree(repo, commit, paths):
    out = {}
    for line in git(repo, "ls-tree", "-r", "-z", commit, "--", *paths).split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, typ, oid = meta.decode().split()
            out[path.decode()] = (mode, typ, oid)
    return out


def check_path(p, mode, typ):
    if typ != "blob" or mode not in ("100644", "100755"):
        sys.exit(f"not a tracked regular file: {p} ({mode} {typ})")
    if not PATH_RE.fullmatch(p) or any(c in ("", ".", "..") for c in p.split("/")):
        sys.exit(f"path outside the section 15.8 grammar: {p!r}")


def inventory(repo, commit):
    spec = ls_tree(repo, commit, SPEC_PATHS)
    if sorted(spec) != sorted(SPEC_PATHS):
        sys.exit(f"spec parts missing at {commit}: {sorted(set(SPEC_PATHS) - set(spec))}")
    for p, c in SIGNED.items():
        if spec[p][2] != git(repo, "rev-parse", f"{c}:{p}").decode().strip():
            sys.exit(f"{p} at {commit} differs from its signing commit {c}")
    vec = ls_tree(repo, commit, [P8_DIR])
    conf = ls_tree(repo, commit, CONF_FILES)
    if sorted(conf) != sorted(CONF_FILES):
        sys.exit(f"vector parts missing: {sorted(set(CONF_FILES) - set(conf))}")
    vec.update(conf)
    counts = {}
    for p, e in ls_tree(repo, commit, [CONF + "cases/"]).items():
        name = p.rsplit("/", 1)[1]
        if name in CASE_KEEP:
            vec[p] = e
            counts[name] = counts.get(name, 0) + 1
        elif name not in CASE_DROP:
            sys.exit(f"case file in neither list of VECTORS-OBJECT.md: {p}")
    if counts != EXPECT_COUNTS:
        sys.exit(f"case file counts {counts} != VECTORS-OBJECT.md {EXPECT_COUNTS}")
    inv = {}
    for name, tree in (("spec", spec), ("vectors", vec)):
        for p, (mode, typ, _) in tree.items():
            check_path(p, mode, typ)
        inv[name] = [(p, tree[p][2]) for p in sorted(tree, key=lambda s: s.encode())]
    return inv


def part_object(parts):
    return b"".join(f"tessera-v1-part {p} {len(b)}\n".encode("ascii") + b + b"\n" for p, b in parts)


def jcs(obj):
    """RFC 8785 for objects whose leaves are ASCII strings (no numbers): sorted keys, no whitespace."""
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    if not s.isascii():
        sys.exit("catalog must be ASCII for this serializer")
    return s.encode("ascii")


def catalog(spec, vectors, preamble, deps):
    return {"D": D, "alg": ALG, "alg_prohibited": [], "binding_forms": ["STMT_DIRECT"], "delta_s": str(DELTA_S),
            "dependency_manifest_sha256": sha(deps), "dnssec_algorithms": ["13", "8"], "ds_digest_types": ["2", "4"],
            "epsilon_s": str(EPSILON_S), "k": str(K), "preamble_sha256": sha(preamble), "spec_id": SPEC_ID,
            "spec_sha256": sha(spec), "utc_delta_s": str(UTC_DELTA_S), "utc_m": str(UTC_M),
            "vectors_sha256": sha(vectors)}


def assemble(repo, commit, out):
    commit = git(repo, "rev-parse", "--verify", commit + "^{commit}").decode().strip()
    inv = inventory(repo, commit)
    blobs = {k: [(p, git(repo, "cat-file", "blob", oid)) for p, oid in v] for k, v in inv.items()}
    spec, vectors = part_object(blobs["spec"]), part_object(blobs["vectors"])
    deps = git(repo, "cat-file", "blob", f"{commit}:{DEPS_PATH}")
    if b"TEST" in deps:
        sys.exit("dependency manifest contains TEST")
    objs = {"spec.bin": spec, "vectors.bin": vectors, "preamble.bin": PREAMBLE, "dependency-manifest.json": deps,
            "catalog.json": jcs(catalog(spec, vectors, PREAMBLE, deps))}
    (out / "objects").mkdir(parents=True, exist_ok=False)
    for n, b in objs.items():
        (out / "objects" / n).write_bytes(b)
    rec = {
        "format": "tessera-v1-freeze-record-draft/1", "commit": commit,
        "recipe": "V1-PROFILE section 15.8 canonical recipe; tracked blob bytes at the named commit",
        "spec_id": SPEC_ID, "alg": ALG,
        "objects": {n: {"file": "objects/" + n, "length": str(len(b)), "sha256": sha(b)} for n, b in objs.items()},
        "inventory": {k: [{"path": p, "blob": oid, "length": str(len(b)), "sha256": sha(b)}
                          for (p, oid), (_, b) in zip(inv[k], blobs[k])] for k in inv},
        "dependency_manifest_source": {"path": DEPS_PATH,
                                       "blob": git(repo, "rev-parse", f"{commit}:{DEPS_PATH}").decode().strip()},
        "signing_commits": SIGNED,
    }
    (out / "freeze-record.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    return rec


def parse_parts(obj):
    out, i = [], 0
    while i < len(obj):
        nl = obj.index(b"\n", i)
        m = HEAD_RE.fullmatch(obj[i:nl])
        if not m:
            raise ValueError(f"bad header at {i}")
        n = int(m.group(2))
        data = obj[nl + 1:nl + 1 + n]
        if len(data) != n or obj[nl + 1 + n:nl + 2 + n] != b"\n":
            raise ValueError("bad part body")
        out.append((m.group(1).decode(), data))
        i = nl + 2 + n
    return out


def check(repo, out):
    """Independent byte-agreement: parse each object back, compare every part with the clean checkout's file AND
    with `git show`, recompute every recorded hash and the catalog's object hashes."""
    rec = json.loads((out / "freeze-record.json").read_text())
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    if head != rec["commit"] or git(repo, "status", "--porcelain", "--untracked-files=no"):
        sys.exit("--repo is not a clean checkout of the record's commit")
    objs = {}
    for n, o in rec["objects"].items():
        objs[n] = (out / o["file"]).read_bytes()
        assert sha(objs[n]) == o["sha256"] and str(len(objs[n])) == o["length"], n
    for n, key in (("spec.bin", "spec"), ("vectors.bin", "vectors")):
        parts = parse_parts(objs[n])
        paths = [p for p, _ in parts]
        assert paths == [e["path"] for e in rec["inventory"][key]], key
        assert paths == sorted(paths, key=lambda s: s.encode()) and len(set(paths)) == len(paths), key
        for p, data in parts:
            assert (Path(repo) / p).read_bytes() == data, f"worktree bytes disagree: {p}"
            assert git(repo, "show", f"{rec['commit']}:{p}") == data, f"git show disagrees: {p}"
    assert objs["dependency-manifest.json"] == (Path(repo) / DEPS_PATH).read_bytes()
    cat = json.loads(objs["catalog.json"])
    assert jcs(cat) == objs["catalog.json"]
    for f, n in (("spec_sha256", "spec.bin"), ("vectors_sha256", "vectors.bin"), ("preamble_sha256", "preamble.bin"),
                 ("dependency_manifest_sha256", "dependency-manifest.json")):
        assert cat[f] == sha(objs[n]), f
    for o in objs.values():
        assert b"TEST" not in o or o in (objs["spec.bin"], objs["vectors.bin"]), "TEST marking in an authored object"
    print("agreement OK", rec["commit"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--commit")
    ap.add_argument("--out")
    ap.add_argument("--check")
    a = ap.parse_args()
    if a.check:
        check(Path(a.repo), Path(a.check))
    else:
        rec = assemble(Path(a.repo), a.commit, Path(a.out))
        for n, o in rec["objects"].items():
            print(f"{n:26s} {o['length']:>9s} {o['sha256']}")


if __name__ == "__main__":
    main()
