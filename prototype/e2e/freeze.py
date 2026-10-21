#!/usr/bin/env python3
"""TEST freeze assembler (V1-PROFILE §15.8, §1 catalog entry, §9/§15.6 dependency manifest).

Builds, from tracked blob bytes at ONE named commit, the four hashed objects and the catalog that a receipt binds:

  spec object     part format of §15.8 over SPEC_PATHS (profile, ENCODING-V1, the registered hybrid supplement, A9)
  vectors object  part format over every tracked regular file under formal/p8/vectors/ plus EXTRA_VECTOR_PATHS
  preamble        TEST preamble bytes (below)
  dependency      TEST dependency manifest in the §15.6 schema (below)
  catalog         the conformance-universe catalog form (EA-01), alg = the registered hybrid pair id

The hashes go into a freeze record written OUTSIDE the parts (§15.8 "Hashes live outside"). An independent
byte-agreement check re-reads every part with `git show` and compares (check_agreement).

TEST NAMESPACE. These are not the 30 Oct freeze. The preamble and the dependency manifest say TEST in their bytes,
so every receipt signed over them carries TEST hashes in its signed common bytes; the catalog carries a "TEST"
member; the output directory is work/test-freeze/<commit>/ and the record says namespace TEST. The spec and vectors
objects are exact §15.8 assemblies of the named commit and are NOT marked (the recipe admits only tracked blobs); the
preamble and catalog hashes are what make a TEST receipt unmistakable. The path inventory below is a TEST choice:
the real inventory (RES §L non-P8 vector files) is a freeze decision that has not been made.

Read-only on the repository (git cat-file / ls-tree / show). Writes only under prototype/e2e/work/.

  uv run python e2e/freeze.py [--commit HEAD] [--out DIR]
"""
import argparse
import re
import subprocess
from pathlib import Path

from common import REPO, WORK, U, gen, jcs, sha256hex, write_atomic, write_json, log

SPEC_PATHS = ["docs/V1-PROFILE.md", "docs/phase-0-prereg-amendment-9.md", "formal/p8/ENCODING-V1.md",
              "formal/p8/HYBRID-SUPPLEMENT.md"]
VECTOR_DIRS = ["formal/p8/vectors/"]
EXTRA_VECTOR_PATHS = ["prototype/conformance/cases-index.json"]   # TEST stand-in for RES §L's non-P8 vector files
PATH_RE = re.compile(r"[A-Za-z0-9._/-]+")

PREAMBLE = (b"TEST ONLY - NOT A PRODUCTION RECEIPT. Tessera V1 end-to-end pipeline proof (TEST freeze namespace). "
            b"A Tessera V1 receipt attests that these exact bytes were presented to the Tessera V1 service and "
            b"existed before a specific Bitcoin block. It attests no submitter, no meaning, no revocation status and "
            b"no standing. This preamble is a TEST stand-in, not the frozen preamble.\n")

_DEPS = [  # (id, title, sections) -- V1-PROFILE §9: A9's eight entries plus the added standards
    ("bitcoin-formats", "Bitcoin header, double SHA-256, merkle and non-witness transaction formats", ["header", "tx"]),
    ("dnssec-algorithms", "DNSSEC algorithms 8 (RFC 5702, RFC 3110) and 13 (RFC 6605); DS digests 2 (RFC 4509), 4",
     ["all"]),
    ("dnssec-core", "RFC 1035, 1982, 2181, 4034, 4035, 5011, 9718; RFC 9102 informative", ["all"]),
    ("ecdsa-p256", "ECDSA P-256 (FIPS 186-5)", ["6"]),
    ("ecma-262", "ECMA-262 Number::toString", ["Number::toString"]),
    ("fips-204", "FIPS 204 ML-DSA-65 and the supplement SPKI encoding (hybrid)", ["all"]),
    ("git-objects", "git object format, gitformat-signature(5) and SHA-1DC", ["all"]),
    ("json", "RFC 8259 and RFC 3339", ["all"]),
    ("openpgp", "RFC 9580 OpenPGP", ["5.2", "5.5"]),
    ("opentimestamps", "OpenTimestamps DetachedTimestampFile (V1-PROFILE 15.2)", ["all"]),
    ("rfc4648", "RFC 4648 base64", ["4"]),
    ("rfc5652", "RFC 5652 CMS (root-anchors .p7s)", ["all"]),
    ("rfc8785", "RFC 8785 JCS", ["all"]),
    ("sha-1", "SHA-1 for git object linkage, with collision detection", ["all"]),
    ("sha-256", "FIPS 180-4 SHA-256", ["6.2"]),
    ("unicode", "Unicode 16.0.0 UCD and UAX #15 (NFC)", ["all"]),
]


def dependency_manifest():
    entries = [{"digest_sha256": None, "edition": "TEST", "errata": "TEST", "failure_consequence": "TEST",
                "id": i, "redistribution": "TEST", "retrieval": "TEST", "sections": s, "title": "TEST: " + t}
               for i, t, s in _DEPS]
    return jcs({"entries": sorted(entries, key=lambda e: e["id"]), "format": "tessera-v1-deps/1"})


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True).stdout


def resolve(commit):
    return git("rev-parse", "--verify", commit + "^{commit}").decode().strip()


def ls_tree(commit, paths):
    """{path: (mode, blob id)} for tracked entries under the given paths at the commit."""
    out = {}
    for line in git("ls-tree", "-r", "-z", commit, "--", *paths).split(b"\0"):
        if not line:
            continue
        meta, path = line.split(b"\t", 1)
        mode, typ, oid = meta.decode().split()
        out[path.decode()] = (mode, typ, oid)
    return out


def blob(commit, path):
    return git("cat-file", "blob", f"{commit}:{path}")


def inventory(commit):
    spec_tree = ls_tree(commit, SPEC_PATHS)
    vec_tree = ls_tree(commit, VECTOR_DIRS + EXTRA_VECTOR_PATHS)
    for want in SPEC_PATHS:
        if want not in spec_tree:
            raise SystemExit(f"spec part not tracked at {commit}: {want}")
    for want in EXTRA_VECTOR_PATHS:
        if want not in vec_tree:
            raise SystemExit(f"vector part not tracked at {commit}: {want}")
    inv = {}
    for name, tree in (("spec", spec_tree), ("vectors", vec_tree)):
        paths = []
        for p, (mode, typ, _) in sorted(tree.items()):
            if typ != "blob" or mode not in ("100644", "100755"):
                raise SystemExit(f"not a tracked regular file: {p} ({mode} {typ})")   # no symlink following
            if not PATH_RE.fullmatch(p) or p.startswith("/") or any(c in ("", ".", "..") for c in p.split("/")):
                raise SystemExit(f"path outside the §15.8 grammar: {p!r}")
            paths.append(p)
        inv[name] = sorted(paths, key=lambda s: s.encode())
    return inv


def part_object(commit, paths):
    parts = [(p, blob(commit, p)) for p in paths]
    obj = U.part_object(parts)
    return obj, [{"path": p, "length": str(len(b)), "sha256": sha256hex(b)} for p, b in parts]


def parse_parts(obj):
    """Inverse of the part format (used by the agreement check)."""
    out, i = [], 0
    while i < len(obj):
        nl = obj.index(b"\n", i)
        head = obj[i:nl].decode("ascii")
        m = re.fullmatch(r"tessera-v1-part ([A-Za-z0-9._/-]+) (0|[1-9][0-9]*)", head)
        if not m:
            raise ValueError(f"bad part header at {i}: {head!r}")
        n = int(m.group(2))
        data = obj[nl + 1:nl + 1 + n]
        if len(data) != n or obj[nl + 1 + n:nl + 2 + n] != b"\n":
            raise ValueError("bad part body")
        out.append((m.group(1), data))
        i = nl + 2 + n
    return out


def catalog(spec, vectors, preamble, deps):
    return {
        "D": "wamason.com", "TEST": "TEST freeze catalog (prototype/e2e); not the frozen catalog",
        "alg": gen.ALG_HYBRID, "alg_prohibited": [], "binding_forms": ["STMT_DIRECT"], "delta_s": str(U.DELTA),
        "dependency_manifest_sha256": sha256hex(deps), "dnssec_algorithms": ["13", "8"], "ds_digest_types": ["2", "4"],
        "epsilon_s": str(U.EPS), "k": str(U.K), "utc_delta_s": str(U.UTC_DELTA_S), "utc_m": str(U.UTC_M),
        "preamble_sha256": sha256hex(preamble), "spec_id": U.SPEC_ID,
        "spec_sha256": sha256hex(spec), "vectors_sha256": sha256hex(vectors),
    }


def assemble(commit="HEAD", out=None):
    commit = resolve(commit)
    out = Path(out) if out else WORK / "test-freeze" / commit[:12]
    inv = inventory(commit)
    spec, spec_parts = part_object(commit, inv["spec"])
    vectors, vec_parts = part_object(commit, inv["vectors"])
    preamble, deps = PREAMBLE, dependency_manifest()
    cat = catalog(spec, vectors, preamble, deps)
    objs = {"spec.bin": spec, "vectors.bin": vectors, "preamble.bin": preamble, "dependency-manifest.json": deps,
            "catalog.json": jcs(cat)}
    for name, data in objs.items():
        write_atomic(out / "objects" / name, data)
    record = {
        "namespace": "TEST",
        "note": "TEST freeze for the end-to-end pipeline proof. Not the 30 Oct freeze; nothing here may be relied on.",
        "commit": commit, "recipe": "V1-PROFILE §15.8 canonical recipe (tracked blob bytes at the named commit)",
        "spec_id": U.SPEC_ID, "alg": gen.ALG_HYBRID,
        "objects": {name: {"file": "objects/" + name, "length": str(len(d)), "sha256": sha256hex(d)}
                    for name, d in objs.items()},
        "inventory": {"spec": spec_parts, "vectors": vec_parts},
        "test_choices": ["preamble text is a TEST stand-in", "dependency manifest fields are TEST",
                         "vectors inventory = formal/p8/vectors/ tracked files + " + ", ".join(EXTRA_VECTOR_PATHS),
                         "A9 part taken from the freeze commit, not separately from its signing commit 2ad3489"],
        "without": ["A10 service-key listing", "utc_assessment"],
    }
    write_json(out / "freeze-record.json", record)
    check_agreement(out)
    log(f"TEST freeze of {commit[:12]} -> {out}")
    for name, o in record["objects"].items():
        log(f"  {name:26s} {o['length']:>9s} B  sha256 {o['sha256']}")
    return out


def check_agreement(out):
    """Independent byte-agreement check: re-read each part with `git show` (a different git path from cat-file)
    and compare with the parsed object; recompute every recorded hash from the files."""
    out = Path(out)
    rec = __import__("json").loads((out / "freeze-record.json").read_text())
    for name, o in rec["objects"].items():
        data = (out / o["file"]).read_bytes()
        assert sha256hex(data) == o["sha256"] and str(len(data)) == o["length"], name
    for obj_name, key in (("spec.bin", "spec"), ("vectors.bin", "vectors")):
        parts = parse_parts((out / "objects" / obj_name).read_bytes())
        assert [p for p, _ in parts] == [e["path"] for e in rec["inventory"][key]]
        assert [p for p, _ in parts] == sorted((p for p, _ in parts), key=lambda s: s.encode())
        for p, data in parts:
            shown = subprocess.run(["git", "-C", str(REPO), "show", f"{rec['commit']}:{p}"], check=True,
                                   capture_output=True).stdout
            assert shown == data, f"part bytes disagree: {p}"
    cat = __import__("json").loads((out / "objects" / "catalog.json").read_bytes())
    for field, obj_name in (("spec_sha256", "spec.bin"), ("vectors_sha256", "vectors.bin"),
                            ("preamble_sha256", "preamble.bin"),
                            ("dependency_manifest_sha256", "dependency-manifest.json")):
        assert cat[field] == rec["objects"][obj_name]["sha256"], field
    return True


def load(freeze_dir):
    """The objects of an assembled freeze: dict of bytes plus the catalog object and record."""
    import json
    fd = Path(freeze_dir)
    o = {k: (fd / "objects" / k).read_bytes() for k in
         ("spec.bin", "vectors.bin", "preamble.bin", "dependency-manifest.json", "catalog.json")}
    o["catalog"] = json.loads(o["catalog.json"])
    o["record"] = json.loads((fd / "freeze-record.json").read_text())
    return o


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--out")
    a = ap.parse_args()
    assemble(a.commit, a.out)


if __name__ == "__main__":
    main()
