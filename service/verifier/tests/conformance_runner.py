"""Run the SERVICE verifier over the instrument's conformance cases, reading the case files as DATA.

  python tests/conformance_runner.py [--cases DIR] [--only ID,ID] [--jobs N] [--json OUT]

Nothing from prototype/ is imported or executed: this file reads each case's trust.json, release.json, bundle (or
bundle.recipe.json + base.json), request.txt, expected.json and the universe release public key, then drives the
`tessera_verify` command line (explicit TEST mode, profile 15.9) as a subprocess and compares its output with
expected.json. Outcomes: AGREE, DISAGREE, AMBIG-ONLY (differs only in a field the case marks as resting on an
expectation ambiguity), ERROR (no parsable output), as the instrument's own runner defines them.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / 'prototype' / 'conformance' / 'cases'
KEY = ROOT / 'prototype' / 'conformance' / 'universe-release-key.json'
FIELDS = ('verdict', 'reason', 'T', 'revocation', 'historical_security', 'standing')


def materialize(case, tmp):
    rec = case / 'bundle.recipe.json'
    if not rec.exists(): return case / 'bundle.json'
    r = json.loads(rec.read_text()); base = (case / 'base.json').read_bytes()
    assert r['kind'] == 'pad_layer'
    marker = b'}],"profile":"tessera-v1-strict"}'
    i = base.rindex(marker); n = r['target_size'] - len(base) - len(b',"zz_pad":""')
    out = Path(tmp) / (case.name + '.bundle.json')
    with open(out, 'wb') as f:
        f.write(base[:i]); f.write(b',"zz_pad":"'); left = n; chunk = b'A' * (1 << 20)
        while left > 0: f.write(chunk[:min(left, len(chunk))]); left -= min(left, len(chunk))
        f.write(b'"'); f.write(base[i:])
    assert out.stat().st_size == r['target_size']
    return out


def stable_object(text):
    """The first JSON object in the output carrying verdict and reason, at top level or under `stable`."""
    dec = json.JSONDecoder(); i = 0
    while True:
        j = text.find('{', i)
        if j < 0: return None
        try: obj, end = dec.raw_decode(text, j)
        except json.JSONDecodeError: i = j + 1; continue
        for cand in (obj, obj.get('stable')):
            if isinstance(cand, dict) and 'verdict' in cand and 'reason' in cand: return cand, obj
        i = end


def cli(*args, timeout=300):
    return subprocess.run([sys.executable, '-m', 'tessera_verify', *args], capture_output=True, timeout=timeout)


def run_case(case, tmp):
    exp = json.loads((case / 'expected.json').read_text()); meta = exp['_meta']; cid = meta['id']
    if meta['kind'] == 'release_check':
        p = cli('--previous', str(case / 'previous.json'), '--next', str(case / 'next.json'))
        out = (p.stdout + p.stderr).decode('utf-8', 'replace')
        got = 'REJECT' if 'REJECT' in out else 'ACCEPT' if 'ACCEPT' in out else None
        return {'id': cid, 'kind': 'release_check', 'outcome': 'AGREE' if got == exp['release_check'] else 'ERROR' if got is None else 'DISAGREE',
                'expected': exp['release_check'], 'got': got}
    args = ['--mode', 'test', '--test-release', str(case / 'release.json'), '--test-release-key', str(KEY),
            '--trust', str(case / 'trust.json'), '--bundle', str(materialize(case, tmp))]
    if (case / 'request.txt').exists(): args += ['--request', (case / 'request.txt').read_text().strip()]
    try: p = cli(*args)
    except subprocess.TimeoutExpired: return {'id': cid, 'kind': 'bundle', 'outcome': 'ERROR', 'why': 'timeout'}
    out, err = p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')
    got = stable_object(out)
    if 'refusal' in exp:
        ok = got is None and p.returncode != 0 and exp['refusal'] in (out + err)
        return {'id': cid, 'kind': 'bundle', 'outcome': 'AGREE' if ok else 'DISAGREE', 'expected': {'refusal': exp['refusal']},
                'got': {'exit': p.returncode, 'verdict': got[0].get('verdict') if got else None, 'stderr': err[-200:]}}
    if got is None: return {'id': cid, 'kind': 'bundle', 'outcome': 'ERROR', 'why': f'no six-field object (exit {p.returncode})', 'stderr': err[-400:]}
    stable, whole = got
    diffs = [f for f in FIELDS if stable.get(f) != exp[f]]
    got_utc = whole.get('utc_assessment') if whole is not stable else None
    if 'utc_assessment' in exp and (got_utc != exp['utc_assessment'] or 'utc_assessment' in stable): diffs.append('utc_assessment')
    outcome = 'AGREE' if not diffs else 'AMBIG-ONLY' if set(diffs) <= set(meta.get('ambiguous_fields', [])) else 'DISAGREE'
    return {'id': cid, 'kind': 'bundle', 'outcome': outcome, 'diffs': diffs,
            'expected': {f: exp[f] for f in FIELDS}, 'got': {f: stable.get(f) for f in FIELDS}, 'got_utc': got_utc}


def run_all(cases=DEFAULT_CASES, only=None, jobs=4, echo=False):
    dirs = sorted(p for p in Path(cases).iterdir() if (p / 'expected.json').exists())
    if only: dirs = [d for d in dirs if d.name in only]
    results = []
    with tempfile.TemporaryDirectory(prefix='tessera-svc-conformance-') as tmp, ThreadPoolExecutor(jobs) as ex:
        for r in ex.map(lambda d: run_case(d, tmp), dirs):
            results.append(r)
            if echo and r['outcome'] != 'AGREE': print(r['outcome'], r['id'], r.get('expected'), r.get('got'), r.get('why', ''), flush=True)
    return results


def summarize(results):
    counts = {}
    for r in results: counts[r['outcome']] = counts.get(r['outcome'], 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cases', default=str(DEFAULT_CASES)); ap.add_argument('--only'); ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--json'); a = ap.parse_args()
    results = run_all(a.cases, set(a.only.split(',')) if a.only else None, a.jobs, echo=True)
    counts = summarize(results)
    print('cases:', len(results), 'summary:', json.dumps(counts, sort_keys=True))
    if a.json: Path(a.json).write_text(json.dumps(results, indent=1) + '\n')
    return 0 if set(counts) <= {'AGREE'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
