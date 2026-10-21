#!/usr/bin/env python3
"""Run every mutant of mutate.py through the independent verifier, via the differential adapter, exactly as
prototype/differential/ADAPTER.md runs it (from the repository root, indep venv, conformance environment):

  TESSERA_V1_TEST_RELEASE=<seed>/release.json TESSERA_V1_TEST_RELEASE_KEY=.../universe-release-key.json \
  TESSERA_V1_TEST_CATALOG=.../universe-catalog.json \
  prototype/indep-verifier/.venv/bin/python prototype/differential/adapter.py --trust <seed>/trust.json --bundle <m>

Each mutant runs with its seed's own trust.json and release.json (unchanged). One result line per mutant in
out/<op>/<seed>.jsonl.gz (resumable: a finished file is skipped).

  campaign.py [--ops op1,op2] [--seeds A-a,...] [--jobs 12] [--timeout 60] [--tmp DIR]
"""
import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import mutate  # noqa: E402

PY = str(REPO / "prototype/indep-verifier/.venv/bin/python")
ADAPTER = "prototype/differential/adapter.py"
FIELDS = {"verdict", "reason", "T", "revocation", "historical_security", "standing"}
VERDICTS = {"VALID_STRICT", "INVALID", "UNVERIFIABLE"}


def run_one(seed, path, timeout):
    c = REPO / "prototype/conformance"
    env = dict(os.environ, TESSERA_V1_TEST_RELEASE=str(c / "cases" / seed / "release.json"),
               TESSERA_V1_TEST_RELEASE_KEY=str(c / "universe-release-key.json"),
               TESSERA_V1_TEST_CATALOG=str(c / "universe-catalog.json"))
    cmd = [PY, ADAPTER, "--trust", f"prototype/conformance/cases/{seed}/trust.json", "--bundle", str(path)]
    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"robust": "TIMEOUT", "elapsed": round(time.monotonic() - t0, 3)}
    el = round(time.monotonic() - t0, 3)
    out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    r = {"exit": p.returncode, "elapsed": el}
    try:
        obj = json.loads(out)
        lines = out.strip("\n").count("\n")
        # Since 2026-10-19 the verifier prints {"stable": six, "utc_assessment": {...}} (profile 3.5, 7.4).
        if isinstance(obj, dict) and set(obj) == {"stable", "utc_assessment"}:
            obj = obj["stable"]
    except Exception:
        obj, lines = None, None
    if p.returncode != 0:
        r["robust"] = "CRASH" if "Traceback" in err else "NONZERO_EXIT"
        r["stderr"] = err[-1500:]
        r["stdout"] = out[-300:]
    if isinstance(obj, dict):
        r.update({k: obj.get(k) for k in FIELDS})
        bad = (set(obj) != FIELDS or lines != 0 or obj.get("verdict") not in VERDICTS
               or obj.get("revocation") != "NOT_EVALUATED" or obj.get("historical_security") != "NOT_EVALUATED"
               or obj.get("standing") != "ABSENT/NOT_ISSUED_IN_PROFILE"
               or not (obj.get("T") is None or isinstance(obj.get("T"), str)) or not isinstance(obj.get("reason"), str))
        if bad:
            r.setdefault("robust", "NONSIX")
            r["stdout"] = out[-600:]
    else:
        r.setdefault("robust", "NONSIX")
        r["stdout"] = out[-600:]
        r.setdefault("stderr", err[-1500:])
    if err and "stderr" not in r:
        r["stderr_note"] = err[-400:]
    return r


def task(op, seed, timeout, tmpdir, outdir):
    try:
        return _task(op, seed, timeout, tmpdir, outdir)
    except Exception:
        import traceback
        return op, seed, 'GENERATOR ERROR ' + traceback.format_exc()[-800:], 0


def _task(op, seed, timeout, tmpdir, outdir):
    outp = Path(outdir) / op / f"{seed}.jsonl.gz"
    if outp.exists():
        return op, seed, "skip", 0
    outp.parent.mkdir(parents=True, exist_ok=True)
    ms = mutate.mutants(op, seed)
    cache = {}
    tmp = Path(tmpdir) / f"{op}-{seed}-{os.getpid()}.json"
    part = outp.with_suffix(".part")
    with gzip.open(part, "wt") as f:
        for n, m in enumerate(ms):
            h = hashlib.sha256(m.bundle).hexdigest()
            if h in cache:
                res = dict(cache[h], cached=True)
            else:
                tmp.write_bytes(m.bundle)
                res = run_one(seed, tmp, timeout)
                cache[h] = res
            rec = {"id": f"{op}/{seed}/{n}", "op": op, "seed": seed, "sub": m.sub, "desc": m.desc, "meta": m.meta,
                   "sha256": h, "size": len(m.bundle), **res}
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    tmp.unlink(missing_ok=True)
    part.rename(outp)
    return op, seed, "done", len(ms)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ops", default=",".join(mutate.OPS))
    ap.add_argument("--seeds")
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--tmp")
    ap.add_argument("--outdir", default=str(HERE / "out"))
    a = ap.parse_args()
    seeds = a.seeds.split(",") if a.seeds else mutate.seed_ids()
    tmpdir = a.tmp or tempfile.mkdtemp(prefix="tessera-mutation-")
    jobs = [(op, s) for op in a.ops.split(",") for s in seeds]
    t0 = time.monotonic()
    with ProcessPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(task, op, s, a.timeout, tmpdir, a.outdir) for op, s in jobs]
        for fu in as_completed(futs):
            try:
                op, s, st, n = fu.result()
            except Exception as e:  # generator failure: report, keep going
                print(f"TASK ERROR {e!r}", flush=True)
                continue
            print(f"{time.monotonic() - t0:8.1f}s {op:5s} {s:12s} {st} {n}", flush=True)


if __name__ == "__main__":
    main()
