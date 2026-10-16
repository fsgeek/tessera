#!/usr/bin/env python3
"""Run any V1 verifier over the conformance cases and report per-case agreement with expected.json.

  run.py --verifier "CMD" [--cases DIR] [--only ID,ID] [--release-checker "CMD"] [--timeout S] [--json OUT]

Invocation per bundle case:   CMD --trust <case>/trust.json --bundle <bundle>
  plus `--request <value>` only for cases that carry request.txt (L-06; the profile makes the request a verifier
  input, P:213-215, but the CLI has no request flag: EA-02).
Environment given to the verifier (TEST universe stand-ins for what a release compiles in; EA-01):
  TESSERA_V1_TEST_RELEASE      <case>/release.json   (compiled trust-config hash + catalog, signed)
  TESSERA_V1_TEST_RELEASE_KEY  universe-release-key.json (bootstrap release public key)
  TESSERA_V1_TEST_CATALOG      universe-catalog.json, or <case>/catalog.json where the case carries one (the
                               hybrid-registered installation: universe-catalog-hybrid.json; the same catalog is
                               inside the case's signed release.json)

Verifier output (EA-03): stdout must contain one JSON object holding the six stable fields `verdict`, `reason`,
`T`, `revocation`, `historical_security`, `standing`, either at top level or under `stable`, `result` or
`report`. A startup refusal (no verdict) must exit nonzero and mention TRUST_CONFIG_UNAUTHENTICATED on stdout or
stderr, with no six-field object.

Release-checker cases (L-53..L-56c) run only with --release-checker: `CMD --previous P --next N`, expected to
print ACCEPT or REJECT (EA-12).

Outcomes: AGREE; DISAGREE (a non-ambiguous field differs); AMBIG-ONLY (differs only in a field the case marks as
resting on an expectation ambiguity); ERROR (no parsable output); SKIP.
"""
import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ("verdict", "reason", "T", "revocation", "historical_security", "standing")


def materialize(case_dir, tmp):
    rec = case_dir / "bundle.recipe.json"
    if not rec.exists():
        return case_dir / "bundle.json"
    r = json.loads(rec.read_text())
    base = (case_dir / "base.json").read_bytes()
    assert r["kind"] == "pad_layer"
    marker = b'}],"profile":"tessera-v1-strict"}'
    i = base.rindex(marker)
    overhead = len(b',"zz_pad":""')
    n = r["target_size"] - len(base) - overhead
    out = Path(tmp) / f"{case_dir.name}.bundle.json"
    with open(out, "wb") as f:
        f.write(base[:i])
        f.write(b',"zz_pad":"')
        chunk = b"A" * (1 << 20)
        left = n
        while left > 0:
            f.write(chunk[:min(left, len(chunk))])
            left -= min(left, len(chunk))
        f.write(b'"')
        f.write(base[i:])
    assert out.stat().st_size == r["target_size"], out.stat().st_size
    return out


def find_stable(text):
    dec = json.JSONDecoder()
    i = 0
    found = None
    while True:
        j = text.find("{", i)
        if j < 0:
            return found
        try:
            obj, end = dec.raw_decode(text, j)
        except json.JSONDecodeError:
            i = j + 1
            continue
        for cand in (obj, obj.get("stable"), obj.get("result"), obj.get("report")):
            if isinstance(cand, dict) and "verdict" in cand and "reason" in cand:
                found = (cand, obj)
                return found
        i = end


def run_case(case_dir, verifier, tmp, timeout, env_base):
    exp = json.loads((case_dir / "expected.json").read_text())
    meta = exp["_meta"]
    if meta["kind"] == "release_check":
        return None
    bundle = materialize(case_dir, tmp)
    cmd = shlex.split(verifier) + ["--trust", str(case_dir / "trust.json"), "--bundle", str(bundle)]
    if (case_dir / "request.txt").exists():
        cmd += ["--request", (case_dir / "request.txt").read_text().strip()]
    env = dict(env_base, TESSERA_V1_TEST_RELEASE=str(case_dir / "release.json"))
    if (case_dir / "catalog.json").exists():          # installation-specific catalog (hybrid-registered cases)
        env["TESSERA_V1_TEST_CATALOG"] = str(case_dir / "catalog.json")
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return {"id": meta["id"], "outcome": "ERROR", "why": "timeout"}
    out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    got = find_stable(out)
    if "refusal" in exp:
        ok = got is None and p.returncode != 0 and exp["refusal"] in (out + err)
        return {"id": meta["id"], "outcome": "AGREE" if ok else "DISAGREE",
                "expected": {"refusal": exp["refusal"]},
                "got": {"exit": p.returncode, "verdict": got[0].get("verdict") if got else None,
                        "mentions": exp["refusal"] in (out + err)}}
    if got is None:
        return {"id": meta["id"], "outcome": "ERROR", "why": f"no six-field object (exit {p.returncode})",
                "stderr": err[-400:]}
    stable, whole = got
    diffs = [f for f in FIELDS if stable.get(f) != exp[f]]
    if "detail" in meta:
        d = stable.get("detail", whole.get("detail"))
        if d is not None and d != meta["detail"]:
            diffs.append("detail")
    if not diffs:
        outcome = "AGREE"
    elif set(diffs) <= set(meta.get("ambiguous_fields", [])):
        outcome = "AMBIG-ONLY"
    else:
        outcome = "DISAGREE"
    return {"id": meta["id"], "outcome": outcome, "diffs": diffs,
            "expected": {f: exp[f] for f in FIELDS}, "got": {f: stable.get(f) for f in FIELDS},
            "ambiguities": meta.get("ambiguities", [])}


def run_rc(case_dir, checker, timeout):
    exp = json.loads((case_dir / "expected.json").read_text())
    cmd = shlex.split(checker) + ["--previous", str(case_dir / "previous.json"), "--next", str(case_dir / "next.json")]
    p = subprocess.run(cmd, capture_output=True, timeout=timeout)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    got = "REJECT" if "REJECT" in out else "ACCEPT" if "ACCEPT" in out else None
    return {"id": exp["_meta"]["id"], "outcome": "AGREE" if got == exp["release_check"] else
            ("ERROR" if got is None else "DISAGREE"), "expected": exp["release_check"], "got": got}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verifier", required=True)
    ap.add_argument("--cases", default=str(HERE / "cases"))
    ap.add_argument("--only")
    ap.add_argument("--release-checker")
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--json")
    a = ap.parse_args()
    env = dict(os.environ, TESSERA_V1_TEST_RELEASE_KEY=str(HERE / "universe-release-key.json"),
               TESSERA_V1_TEST_CATALOG=str(HERE / "universe-catalog.json"))
    dirs = sorted(p for p in Path(a.cases).iterdir() if (p / "expected.json").exists())
    if a.only:
        keep = set(a.only.split(","))
        dirs = [d for d in dirs if d.name in keep]
    results = []
    with tempfile.TemporaryDirectory(prefix="tessera-conformance-") as tmp:
        for d in dirs:
            exp = json.loads((d / "expected.json").read_text())
            if exp["_meta"]["kind"] == "release_check":
                r = run_rc(d, a.release_checker, a.timeout) if a.release_checker else \
                    {"id": d.name, "outcome": "SKIP", "why": "no --release-checker"}
            else:
                r = run_case(d, a.verifier, tmp, a.timeout, env)
            results.append(r)
            line = f"{r['outcome']:10s} {r['id']:12s}"
            if r["outcome"] in ("DISAGREE", "AMBIG-ONLY"):
                line += f" expected={r.get('expected')} got={r.get('got')}"
            elif r["outcome"] == "ERROR":
                line += " " + r.get("why", "")
            print(line, flush=True)
    counts = {}
    for r in results:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    print("summary:", json.dumps(counts, sort_keys=True))
    if a.json:
        Path(a.json).write_text(json.dumps(results, indent=1) + "\n")
    sys.exit(0 if counts.get("DISAGREE", 0) == 0 and counts.get("ERROR", 0) == 0 else 1)


if __name__ == "__main__":
    main()
