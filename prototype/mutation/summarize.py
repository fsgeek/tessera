#!/usr/bin/env python3
"""Summarize out/<op>/<seed>.jsonl.gz: counts per operator and sub-operator, verdict/reason distribution,
every VALID_STRICT mutant with a rule-based classification hint, and every robustness finding.

  summarize.py [--outdir out] [--json summary.json]

Classification hints are mechanical aids for the manual review recorded in REPORT.md; they never decide (B)
alone. 'T_CHANGED' marks a VALID_STRICT mutant whose T differs from the seed's expected T.
"""
import argparse
import base64
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mutate  # noqa: E402


def seed_T(seed):
    return json.loads((mutate.CASES / seed / "expected.json").read_text())["T"]


def ots_hint(seed, member, offset):
    L = mutate.load(seed)["layer"]
    path = {"receipt_anchor.ots": ("receipt_anchor", "ots"), "dns.ots": ("dns", "ots"), "git.ots": ("git", "ots")}[member]
    data = base64.b64decode(mutate.get_path(L, path))
    try:
        root, node, end = mutate.ots_parse(data)
    except Exception as e:
        return f"unparsed ({e})"
    if offset < root:
        return "proof header/digest"
    lv = mutate.ots_leaves_at(node, offset)
    if lv is None:
        return "outside timestamp"
    hdrs = set(int(h) for h in L["headers"])
    desc = []
    for x in lv:
        if x["kind"] == "btc":
            desc.append(f"btc@{x['height']}{'' if x['height'] in hdrs else '(no header)'}")
        else:
            desc.append(x["kind"])
    return "leaves under flipped item: " + ", ".join(sorted(set(desc)))


def hint(r):
    op, sub, meta = r["op"], r["sub"], r.get("meta", {})
    if op == "op1":
        reg = meta.get("region", "")
        if ".unhashed." in reg and not reg.endswith(".len"):
            return "A?", f"region {reg}: P§8 rule O 'Unhashed area: ignored entirely, critical bits included'"
        return "REVIEW", f"region {reg}"
    if op == "op1x":
        m = meta.get("member", "")
        if m.startswith("issuer_record"):
            return "A?", "issuer_record: P§2.1/§15.1 unsigned diagnostics, never alter verification"
        if m.endswith(".ots"):
            return "REVIEW", ots_hint(r["seed"], m, meta["offset"])
        return "REVIEW", m
    if op == "op4":
        d = r["desc"]
        if "issuer_record" in d and d.startswith("drop"):
            return "A?", "P§2.1 'Absence of issuer_record is allowed'"
        if "pending" in d or "duplicate whole timestamp" in d or "unheadered" in d or "drop root sibling" in d:
            return "A?", "OTS inert structure: P§15.2 (pending URI ignored; duplicate identical branches no effect; " \
                         "unqualified, uncontradicted attestations do not select h*)"
        return "REVIEW", d
    return "REVIEW", r["desc"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(HERE / "out"))
    ap.add_argument("--json", default=str(HERE / "summary.json"))
    a = ap.parse_args()
    per_op = Counter()
    per_sub = Counter()
    verdicts = defaultdict(Counter)
    reasons = defaultdict(Counter)
    cands, robust = [], []
    seeds_done = defaultdict(set)
    for f in sorted(Path(a.outdir).glob("*/*.jsonl.gz")):
        with gzip.open(f, "rt") as fh:
            for line in fh:
                r = json.loads(line)
                op = r["op"]
                per_op[op] += 1
                per_sub[(op, r["sub"].split(":")[0] if op in ("op2",) else r["sub"])] += 1
                seeds_done[op].add(r["seed"])
                v = r.get("verdict")
                verdicts[op][v] += 1
                reasons[op][f"{v}/{r.get('reason')}"] += 1
                if r.get("robust"):
                    robust.append(r)
                if v == "VALID_STRICT":
                    cls, why = hint(r)
                    r["hint"], r["hint_why"] = cls, why
                    r["T_CHANGED"] = r.get("T") != seed_T(r["seed"])
                    cands.append(r)
    out = {"per_op": per_op, "seeds_done": {k: len(v) for k, v in seeds_done.items()},
           "per_sub": {f"{k[0]}|{k[1]}": v for k, v in sorted(per_sub.items())},
           "verdicts": verdicts, "reasons": {k: dict(v.most_common()) for k, v in reasons.items()},
           "valid_strict": len(cands), "robust": len(robust)}
    Path(a.json).write_text(json.dumps(out, indent=1, sort_keys=True, default=dict) + "\n")
    with open(HERE / "candidates.jsonl", "w") as fh:
        for r in cands:
            fh.write(json.dumps({k: r[k] for k in ("id", "op", "seed", "sub", "desc", "meta", "T", "T_CHANGED",
                                                   "hint", "hint_why", "sha256")}, sort_keys=True) + "\n")
    with open(HERE / "robustness.jsonl", "w") as fh:
        for r in robust:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps({"per_op": per_op, "valid_strict": len(cands), "robust": len(robust),
                      "verdicts": verdicts}, default=dict, indent=1))


if __name__ == "__main__":
    main()
