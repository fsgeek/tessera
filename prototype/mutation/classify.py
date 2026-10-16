#!/usr/bin/env python3
"""Mechanical evidence for classifying VALID_STRICT mutants (candidates.jsonl from summarize.py).

For each candidate, regenerate the mutant and compare it with its seed:
  - changed: the layer leaf paths whose values differ (JSON-level; non-JSON mutants are marked)
  - claim_bytes_equal: a_sig, manifest and keys byte-identical to the seed (content, issuer, declared time, alg,
    keys and the anchored digest are all inside these)
  - T_equal: reported T equals the seed's expected T
  - for OTS changes: the receipt/snapshot/git file digests are unchanged (proof still for the same bytes)
  - for evidence transplants: whether the donor's evidence member equals evidence the seed already carries
Writes classified.jsonl and prints a grouped table. The final (A)/(B) call is made in REPORT.md.
"""
import base64
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mutate  # noqa: E402


def flat(o, p=()):
    if isinstance(o, dict):
        for k in o:
            yield from flat(o[k], p + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, p + (str(i),))
    else:
        yield ".".join(p), o


def ots_digest(b64):
    b = base64.b64decode(b64)
    i = len(mutate.OTS_MAGIC)
    _, i = mutate._varuint(b, i)
    return b[i + 1:i + 33].hex()


def main():
    cands = [json.loads(line) for line in open(HERE / "candidates.jsonl")]
    groups = defaultdict(list)
    for c in cands:
        groups[(c["op"], c["seed"])].append(c)
    out = []
    for (op, seed), cs in sorted(groups.items()):
        ms = mutate.mutants(op, seed)
        L = mutate.load(seed)["layer"]
        T = json.loads((mutate.CASES / seed / "expected.json").read_text())["T"]
        fs = dict(flat(L))
        for c in cs:
            m = ms[int(c["id"].split("/")[2])]
            try:
                obj = json.loads(m.bundle)
                ML = obj["layers"][0]
                fm = dict(flat(ML))
                changed = sorted(k for k in set(fs) | set(fm) if fs.get(k) != fm.get(k))
            except Exception:
                ML, changed = None, ["<non-JSON>"]
            rec = dict(c)
            rec["changed"] = changed
            rec["T_equal"] = c["T"] == T
            if ML is not None:
                rec["claim_bytes_equal"] = all(ML.get(k) == L.get(k) for k in ("a_sig", "manifest", "keys"))
                dig = {}
                for nm, path in (("receipt", ("receipt_anchor", "ots")), ("dns", ("dns", "ots")), ("git", ("git", "ots"))):
                    try:
                        dig[nm] = ots_digest(mutate.get_path(ML, path)) == ots_digest(mutate.get_path(L, path))
                    except Exception:
                        dig[nm] = None
                rec["ots_digest_same"] = dig
                rec["evidence_targets_same"] = {
                    "snapshot_body": ML["dns"]["snapshot_body"] == L["dns"]["snapshot_body"],
                    "git_commit": ML["git"]["commit"] == L["git"]["commit"],
                    "git_blob": ML["git"]["blob"] == L["git"]["blob"]}
            out.append(rec)
    with open(HERE / "classified.jsonl", "w") as fh:
        for r in out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    tab = Counter()
    for r in out:
        ch = r["changed"]
        top = sorted({k.split(".")[0] + ("." + k.split(".")[1] if k.split(".")[0] in ("dns", "git", "receipt_anchor",
                                                                                       "possession") and "." in k else "")
                      for k in ch})
        tab[(r["op"], r["sub"], ",".join(top), r.get("claim_bytes_equal"), r["T_equal"],
             json.dumps(r.get("ots_digest_same"), sort_keys=True), json.dumps(r.get("evidence_targets_same"),
                                                                                sort_keys=True))] += 1
    for k, v in sorted(tab.items()):
        print(v, k)
    final(out)


CATS = {
    "A1": "issuer_record (unsigned optional diagnostics) changed, dropped or swapped",
    "A2": "possession signature: unhashed area, ECDSA s, or another valid signature by the same key over the same "
          "F_manifest",
    "A3": "OTS proof bytes for the same file digest: inert or alternative branches, T unchanged",
    "A4": "header pool: pinned headers added or removed outside what the selected attestations need, T unchanged",
}


def category(r):
    ch = r["changed"]
    if ch and all(k.startswith("issuer_record") for k in ch):
        return "A1"
    if ch and all(k.startswith("possession.") for k in ch):
        return "A2"
    if ch and all(k.endswith(".ots") or k.startswith("headers.") for k in ch) and any(k.endswith(".ots") for k in ch):
        return "A3"
    if ch and all(k.startswith("headers.") for k in ch):
        return "A4"
    return "UNCLASSIFIED"


def final(out):
    """Final category per VALID_STRICT mutant. A category is assigned only if the claim-bearing bytes (a_sig,
    manifest, keys), every OTS file digest, the stamped evidence (snapshot body, git commit, blob) and T are all
    unchanged; anything else is UNCLASSIFIED and must be reviewed by hand."""
    rows, groups = [], defaultdict(list)
    for r in out:
        ok = (r.get("claim_bytes_equal") and r["T_equal"] and all(r.get("ots_digest_same", {}).values())
              and all(r.get("evidence_targets_same", {}).values()))
        cat = category(r) if ok else "UNCLASSIFIED"
        rows.append((r["id"], cat, r["seed"], r["desc"], r["T"]))
        op, seed, n = r["id"].split("/")
        groups[(cat, op, seed)].append(int(n))
    with open(HERE / "valid_strict.tsv", "w") as fh:
        fh.write("id\tclass\tseed\tmutation\tT\n")
        for row in rows:
            fh.write("\t".join(map(str, row)) + "\n")
    with open(HERE / "valid_strict_index.md", "w") as fh:
        fh.write("| Class | Operator | Seed | Mutant indices n (id = op/seed/n) |\n|---|---|---|---|\n")
        for (cat, op, seed), ns in sorted(groups.items()):
            ns.sort()
            rs, s = [], ns[0]
            for a, b in zip(ns, ns[1:] + [None]):
                if b != a + 1:
                    rs.append(str(s) if s == a else f"{s}-{a}")
                    s = b
            fh.write(f"| {cat} | {op} | {seed} | {', '.join(rs)} |\n")
    print(Counter(r[1] for r in rows))


if __name__ == "__main__":
    main()
