#!/usr/bin/env python3
"""Enforcing supervisor for the counted runs of SLICE-PREREG-2026-10-09.md (A8.3, A8.4).

  run_counted.py --audit-only   pre-run audit only; runs nothing; exit 0 only if every check passes
  run_counted.py --dry-run      audit, then print the run plan; runs nothing
  run_counted.py --execute      audit, then controls -> primaries -> fallbacks -> A8.4, under the page's boxes

The audit is the one the page requires BEFORE any run (and each run's blob is re-checked after it):
  * tool pins: slice.py, derive_a84.py, ProVerif, the library (sha256);
  * the manifest (MANIFEST.tsv) counts are fixed below; the gen/ and a84/ directories hold exactly the manifest's files;
  * every source blob equals its manifest blob; every file's git blob equals its manifest blob;
  * every slice is byte-identical to slice.py's output from its source, AND passes the independent checks ported
    from dev/slice_probe/codex/audit.py and exact-prefix.py (prefix bytes, in-order unchanged replicated components,
    deleted-component rule per slice name, one kept query);
  * no prohibited construct (get/else on tables, sync, phase, restriction, axiom, lemma, nounif, `not` declarations,
    choice/diff/noninterf/weaksecret, ...), and no `set` line other than `set selFun = Term.`;
  * each A8.4 file equals derive_a84.py's output from its source.
Any failure exits nonzero. Checked counts must be nonzero and equal the manifest counts.

Never removes anything. Refuses to execute over an existing counted.log or out/*.
"""
import sys, os, re, hashlib, runpy, subprocess, tempfile, threading, time, datetime, collections, argparse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))          # .../proverif/slice
PV = os.path.dirname(HERE)                                  # .../proverif
SLICEPY = os.path.join(PV, 'dev', 'slice_probe', 'slice.py')
DERIVE = os.path.join(PV, 'dev', 'prereg_scratch', 'derive_a84.py')
LIB = os.path.abspath(os.path.join(PV, '..', '..', 'lib', 'tessera_theory.pvl'))
PROVERIF = os.path.expanduser('~/.local/bin/proverif')
MANIFEST = os.path.join(HERE, 'MANIFEST.tsv')
LOG = os.path.join(HERE, 'counted.log')
OUT = os.path.join(HERE, 'out')

PINS = {  # sha256, from the page
    SLICEPY: '6a9ee118b889a4d3af40dd397baba9151f7b2c9a51fb3c4334249c80fbb12d97',
    DERIVE: 'de35439b35889f1475afef012b968f03e3f90cdd2b7cc4c4b9ddad3b5af92b6d',
    PROVERIF: 'ff1dff7a9819e3efd0e841deff8d2ef2a28bc18010d1775e7a20f84b5c6cf5a0',
    LIB: '7cf45a21b8c8b8f6ae68283a0407cbf4da047b8a9d4a120089b0612e325fa993',
}
EXPECTED_COUNTS = {'control': 41, 'primary': 33, 'fallback': 33, 'a84': 13}   # frozen manifest counts
EXPECTED_SOURCES = 11
BOXES = {  # slice -> (MemoryMax GB, timeout s)
    'depth0': (4, 1800), 'depth0.cone': (4, 1800), 'depth1': (8, 3600), 'depth1.cone': (8, 3600), 'a84': (16, 7200),
}
SLICE_BUDGET_GB = 24
ALLOWED_SET = ['set selFun = Term.']
PROHIBITED = (r'\b(get|insert|table|sync|phase|restriction|axiom|lemma|nounif|not|equivalence|noninterf|weaksecret|'
              r'choice|diff|barrier|elimtrue|pred|clauses)\b')
ANCHOR_BLOCK = '\n  ( !out(honestKeyCh'

# --------------------------------------------------------------------------- helpers
def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gitblob(p_or_bytes):
    b = open(p_or_bytes, 'rb').read() if isinstance(p_or_bytes, str) else p_or_bytes
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()

def uncomment(s):
    out = []; i = 0; depth = 0
    while i < len(s):
        if s[i:i + 2] == '(*': depth += 1; out.extend('  '); i += 2
        elif s[i:i + 2] == '*)' and depth: depth -= 1; out.extend('  '); i += 2
        else: out.append(s[i] if not depth or s[i] == '\n' else ' '); i += 1
    if depth: raise ValueError('unbalanced comment')
    return ''.join(out)

def noqueries(s):
    clean = uncomment(s)
    for m in reversed(list(re.finditer(r'(?m)^query\b[^.]*\.', clean))):
        s = s[:m.start()] + s[m.end():]
    return uncomment(s)

def compact(s):
    return re.sub(r'\s+', '', s)

def parts(s):
    pre, sep, tail = s.partition(ANCHOR_BLOCK)
    if not sep: raise ValueError('no final parallel block')
    block = '!out(honestKeyCh' + tail
    block = block.rstrip()
    if not block.endswith(')'): raise ValueError('block does not end with )')
    comps = [x.strip() for x in block[:-1].split('|')]
    if not all(re.fullmatch(r'!\w+(?:\([^;|]*\))?', x) for x in comps): raise ValueError('non-simple component')
    return pre, comps

def head_name(c):
    return re.match(r'!?\s*(\w+)', c).group(1)

class Audit:
    def __init__(self):
        self.fail = []; self.n = collections.Counter()
    def bad(self, msg):
        self.fail.append(msg); print('FAIL', msg)
    def ok(self, key):
        self.n[key] += 1

def read_manifest():
    rows = []
    for ln in open(MANIFEST, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'): continue
        f = ln.split('\t')
        if len(f) != 10: raise ValueError('bad manifest line: ' + ln)
        rows.append(dict(zip(['kind', 'id', 'file', 'blob', 'src', 'srcblob', 'slice', 'query', 'cond', 'expect'], f)))
    return rows

def construct_scan(a, label, text, allow_sets=ALLOWED_SET):
    try: clean = uncomment(text)
    except ValueError as e: a.bad(f'{label}: {e}'); return
    hits = [(clean.count('\n', 0, m.start()) + 1, m.group()) for m in re.finditer(PROHIBITED, clean)]
    if hits: a.bad(f'{label}: prohibited constructs {hits[:5]}')
    sets = re.findall(r'(?m)^set .*', clean)
    if sets != allow_sets: a.bad(f'{label}: unexpected set lines {sets}')
    if re.search(r'\bget\b[^;]*\belse\b', clean): a.bad(f'{label}: get ... else')

# --------------------------------------------------------------------------- the audit
def audit():
    a = Audit()
    for p, want in PINS.items():
        if not os.path.exists(p): a.bad(f'missing tool {p}'); continue
        got = sha256(p)
        if got != want: a.bad(f'tool pin mismatch {p}: {got}'); continue
        a.ok('tool pins')
    if a.fail: return a
    rows = read_manifest()
    cnt = collections.Counter(r['kind'] for r in rows)
    for k, v in EXPECTED_COUNTS.items():
        if cnt[k] != v: a.bad(f'manifest count {k}: {cnt[k]} != {v}')
    if set(cnt) - set(EXPECTED_COUNTS): a.bad(f'unexpected manifest kinds {set(cnt)}')
    files = [r['file'] for r in rows]
    if len(set(files)) != len(files): a.bad('duplicate files in manifest')
    for d in ('gen', 'a84'):
        have = sorted(os.listdir(os.path.join(HERE, d)))
        want = sorted(os.path.basename(r['file']) for r in rows if r['file'].startswith(d + '/'))
        if have != want: a.bad(f'{d}/ file set differs from manifest: extra {sorted(set(have)-set(want))} missing {sorted(set(want)-set(have))}')
        else: a.ok(d + ' dir listing')
    ns = runpy.run_path(SLICEPY)
    make, BANNER, QUERY_RE, CONE_KEEP = ns['make'], ns['BANNER'], ns['QUERY_RE'], ns['CONE_KEEP']
    # library
    libtext = open(LIB, encoding='utf-8').read()
    construct_scan(a, 'lib', libtext, allow_sets=[])
    a.ok('library scan')
    # sources
    srcs = {}
    for r in rows:
        srcs.setdefault(r['src'], set()).add(r['srcblob'])
    if any(len(v) != 1 for v in srcs.values()): a.bad('one source with two expected blobs')
    srctext = {}
    a84_src_names = {r['src'] for r in rows if r['kind'] == 'a84'}
    for s, v in srcs.items():
        p = os.path.join(PV, s)
        got = gitblob(p)
        if got != next(iter(v)): a.bad(f'source blob mismatch {s}: {got}'); continue
        raw = open(p, 'rb').read()
        try: text = raw.decode('utf-8')
        except UnicodeDecodeError: a.bad(f'{s}: not utf-8'); continue
        if text.encode('utf-8') != raw or '\r' in text: a.bad(f'{s}: newline normalization'); continue
        srctext[s] = text
        if s not in a84_src_names or s == 'capstone_d.pv':
            out, d, dq = make(text, 'none', 'all')
            if not (out == text and not d and dq == 0): a.bad(f'{s}: slice.py identity mismatch'); continue
        construct_scan(a, 'source ' + s, text)
        a.ok('sources')
    # slices
    for r in rows:
        if r['kind'] == 'a84': continue
        p = os.path.join(HERE, r['file']); lab = r['file']
        raw = open(p, 'rb').read()
        if gitblob(raw) != r['blob']: a.bad(f'{lab}: blob mismatch'); continue
        a.ok('slice blobs')
        s = r['src']
        if s not in srctext: a.bad(f'{lab}: source unavailable'); continue
        original = srctext[s]; sl, q = r['slice'], r['query']
        name = os.path.basename(r['file'])[:-3]
        if name != f"{s[:-3]}__{sl}__{q}": a.bad(f'{lab}: name does not match manifest fields'); continue
        try:
            saved = raw.decode('utf-8'); body = saved.split('\n', 2)[2]
            made, d, dq = make(original, sl, q)
        except Exception as e: a.bad(f'{lab}: {e}'); continue
        expected = BANNER + (f"(* GENERATED by slice.py from {s}: slice={sl} query={q}; {dq} query declarations deleted; "
                             f"{len(d)} process components deleted: {' ; '.join(d) if d else '(none)'} *)\n") + made
        if expected.encode('utf-8') != raw: a.bad(f'{lab}: differs from slice.py output'); continue
        a.ok('slice == slice.py output')
        try:
            pre, comps = parts(original)
            # exact prefix (port of exact-prefix.py): all bytes outside query removals and the final block
            qs = list(re.finditer(r'(?m)^query\b[^.]*\.', original)); exp = original
            for m in reversed(qs):
                if m.group() not in body: exp = exp[:m.start()] + '(* query deleted by slice.py *)' + exp[m.end():]
            if not body.startswith(exp[:exp.index(ANCHOR_BLOCK) + 1]): a.bad(f'{lab}: prefix bytes altered'); continue
            a.ok('exact prefix')
            # component check (port of audit.py)
            cb = noqueries(body); cp = noqueries(pre)
            if not compact(cb).startswith(compact(cp)): a.bad(f'{lab}: prefix (queries removed) altered'); continue
            final = body[body.rfind('\n  ( ') + 1:].strip()[1:-1].strip()
            kept = [c.strip() for c in final.split('|')]
            it = iter(comps)
            if not all(any(c == k for c in it) for k in kept): a.bad(f'{lab}: kept components not an in-order subsequence'); continue
            before = body[:body.rfind('\n  ( ')]
            if compact(noqueries(before)) != compact(cp): a.bad(f'{lab}: component/declaration bytes before the block altered'); continue
            if not all(c.startswith('!') for c in comps): a.bad(f'{lab}: non-replicated component in source'); continue
            dele = [c for c in comps if c not in kept]
            if len(dele) != len(d): a.bad(f'{lab}: deleted count disagrees with slicer'); continue
            depth = sl.partition('.')[0]
            wrapset = [c for c in comps if head_name(c) in ('WrapStage', 'SUnwrap')]
            d1 = [c for c in comps if c in ('!WrapStage(pk(skS), L1, L2)', '!SUnwrap(L1, L2)')]
            if depth == 'depth0' and not all(c in dele for c in wrapset): a.bad(f'{lab}: depth0 kept a wrapper component'); continue
            if depth == 'depth1' and not all(c in dele for c in d1): a.bad(f'{lab}: depth1 kept an L1->L2 component'); continue
            if '.' not in sl:
                want = wrapset if depth == 'depth0' else d1
                if sorted(dele) != sorted(want): a.bad(f'{lab}: non-cone slice deleted something else'); continue
            else:
                keepset = CONE_KEEP[q]
                def key(c):
                    m = re.match(r'!?\s*(\w+)\s*(?:\(\s*(\w*))?', c)
                    return m.group(1), m.group(1) + ':' + (m.group(2) or '')
                if not all(key(c)[0] in keepset or key(c)[1] in keepset for c in kept):
                    a.bad(f'{lab}: cone kept a component outside CONE_KEEP[{q}]'); continue
            a.ok('components')
            cleanbody = uncomment(body)
            qd = re.findall(r'(?m)^query\b', cleanbody)
            if len(qd) != 1 or not re.search(QUERY_RE[q], cleanbody): a.bad(f'{lab}: not exactly the one kept query'); continue
            if 'query deleted by slice.py' not in body: a.bad(f'{lab}: no deleted-query marker'); continue
            a.ok('one kept query')
        except Exception as e:
            a.bad(f'{lab}: {type(e).__name__} {e}'); continue
        construct_scan(a, lab, saved); a.ok('slice construct scan')
    # A8.4 files
    for r in rows:
        if r['kind'] != 'a84': continue
        p = os.path.join(HERE, r['file']); lab = r['file']
        raw = open(p, 'rb').read()
        if gitblob(raw) != r['blob']: a.bad(f'{lab}: blob mismatch'); continue
        a.ok('a84 blobs')
        with tempfile.TemporaryDirectory() as td:
            o = os.path.join(td, 'o.pv')
            cp = subprocess.run([sys.executable, DERIVE, os.path.join(PV, r['src']), o], capture_output=True, text=True)
            if cp.returncode != 0: a.bad(f'{lab}: derive failed {cp.stderr[:200]}'); continue
            got = open(o, 'rb').read()
        # derive_a84 writes its header with the source file name; compare bytes
        if got != raw: a.bad(f'{lab}: differs from derive_a84.py output'); continue
        a.ok('a84 == derive output')
        text = raw.decode('utf-8'); clean = uncomment(text)
        qs = re.findall(r'(?m)^query\b', clean)
        if len(qs) != 2 or clean.count('==> kS = kV.') != 1: a.bad(f'{lab}: not exactly C-Q6k + A8.4w'); continue
        construct_scan(a, lab, text); a.ok('a84 construct scan')
    # checked counts must be nonzero and equal the manifest counts
    want = {'slice blobs': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'slice == slice.py output': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'exact prefix': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'components': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'one kept query': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'slice construct scan': cnt['control'] + cnt['primary'] + cnt['fallback'],
            'a84 blobs': cnt['a84'], 'a84 == derive output': cnt['a84'], 'a84 construct scan': cnt['a84'],
            'sources': EXPECTED_SOURCES + 0, 'tool pins': len(PINS), 'library scan': 1, 'gen dir listing': 1, 'a84 dir listing': 1}
    # sources counted: distinct srcs (slice sources) -- a84 sources are separate blobs checked above as well
    want['sources'] = len(srcs)
    for k, v in want.items():
        if v == 0 or a.n[k] != v: a.bad(f'checked count {k}: {a.n[k]} != manifest {v}')
    n_slice_src = len({r['src'] for r in rows if r['kind'] != 'a84'})
    if n_slice_src != EXPECTED_SOURCES: a.bad(f'slice sources {n_slice_src} != {EXPECTED_SOURCES}')
    return a

# --------------------------------------------------------------------------- running
def box_of(r): return BOXES[r['slice']]

def parse_results(text):
    lines = text.splitlines(); res = []
    for i, ln in enumerate(lines):
        if not ln.startswith('RESULT '): continue
        verdict = 'true' if ln.endswith(' is true.') else 'false' if ln.endswith(' is false.') else 'other'
        j = i - 1
        while j >= 0 and not lines[j].strip(): j -= 1
        trace = verdict == 'false' and j >= 0 and lines[j].strip() == 'A trace has been found.'
        res.append({'text': ln[7:], 'verdict': verdict, 'trace': trace})
    return res

class Budget:
    def __init__(self, gb): self.free = gb; self.c = threading.Condition()
    def acquire(self, gb):
        with self.c:
            while self.free < gb: self.c.wait()
            self.free -= gb
    def release(self, gb):
        with self.c: self.free += gb; self.c.notify_all()

LOGLOCK = threading.Lock()
def log(line):
    with LOGLOCK, open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')

def run_one(r, budget):
    mem, box = box_of(r)
    f = os.path.join(HERE, r['file']); b = os.path.basename(f)[:-3]
    outp = os.path.join(OUT, b + '.out'); rss = os.path.join(OUT, b + '.rss')
    cmd = ['systemd-run', '--user', '--scope', '-q', '-p', f'MemoryMax={mem}G', '-p', 'MemorySwapMax=0',
           '/usr/bin/time', '-f', '%M', '-o', rss, 'timeout', str(box), 'nice', '-n', '10', PROVERIF, '-lib', LIB, f]
    budget.acquire(mem); t0 = time.time()
    try:
        with open(outp, 'x', encoding='utf-8') as fo: rc = subprocess.run(cmd, stdout=fo, stderr=subprocess.STDOUT).returncode
    finally:
        budget.release(mem)
    wall = time.time() - t0
    try: peak = open(rss).read().strip().splitlines()[-1]
    except Exception: peak = 'NA'
    res = parse_results(open(outp, encoding='utf-8', errors='replace').read())
    blob_after = gitblob(f); prov = blob_after == r['blob']
    qdesc = ' ; '.join(f"[{x['verdict']} trace={int(x['trace'])}] {x['text']}" for x in res) or '(no RESULT line)'
    log(f"{r['kind']} row={r['id']} file={r['file']} blob={blob_after} rc={rc} wall={wall:.1f} peakRSSkB={peak} "
        f"mem={mem}G box={box}s provenance={'OK' if prov else 'MISMATCH'} queries: {qdesc}")
    return {'row': r, 'rc': rc, 'res': res, 'prov': prov}

def kept_result(x):
    """the single result of a slice file (exactly one query); None if not exactly one RESULT line."""
    return x['res'][0] if len(x['res']) == 1 else None

def control_status(x):
    r = x['row']; k = kept_result(x)
    if not x['prov']: return 'PROVENANCE'
    if x['rc'] != 0 or k is None or k['verdict'] == 'other': return 'INCONCLUSIVE'
    if r['expect'] == 'true': return 'OK' if k['verdict'] == 'true' else 'RED'
    # A4.6 positive control: false requires its reconstructed trace
    if k['verdict'] == 'false': return 'OK' if k['trace'] else 'INCONCLUSIVE'
    return 'CAVEAT_GREEN_A46'   # proved true: slice too tight at that depth; recorded, does not stop

def counted_primary(x):
    """Finding 2: the primary satisfies the trigger only with rc=0, a reconstructed false result for the kept query
    and a trace satisfying every row-specific counting condition. Counting conditions (T/H/L) are read from the trace
    (on the same violating accepted frame) by the reader, not by this script; so for a row with a condition the
    script cannot certify 'counted' and always runs the fallback."""
    r = x['row']; k = kept_result(x)
    if x['rc'] != 0 or k is None or k['verdict'] != 'false' or not k['trace']: return False
    return r['cond'] == '-'

def pool_run(rs, jobs, budget, stop_on=None):
    out = []; stop = threading.Event()
    def work(r):
        if stop.is_set(): return None
        x = run_one(r, budget)
        if stop_on and stop_on(x): stop.set()
        return x
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        out = [x for x in ex.map(work, rs) if x is not None]
    return out

def a84_tags(x):
    r = x['row']; q6 = [y for y in x['res'] if '==>' in y['text']]; w = [y for y in x['res'] if '==>' not in y['text']]
    if x['rc'] != 0 or len(q6) != 1 or len(w) != 1: wt = 'INCONCLUSIVE'
    elif w[0]['verdict'] == 'false' and w[0]['trace']: wt = 'REACHABLE_WITH_TRACE'
    elif w[0]['verdict'] == 'true': wt = 'UNREACHABLE_prediction_falsified_green_withheld'
    else: wt = 'INCONCLUSIVE_non_vacuity_not_shown'
    if len(q6) == 1: qt = f"C-Q6k={q6[0]['verdict']}{'+trace' if q6[0]['trace'] else ''}"
    else: qt = 'C-Q6k=INCONCLUSIVE'
    return f"{qt} A8.4w={wt}"

def plan(rows):
    ctl = [r for r in rows if r['kind'] == 'control']; pri = [r for r in rows if r['kind'] == 'primary']
    fb = {r['id']: r for r in rows if r['kind'] == 'fallback'}; a84 = [r for r in rows if r['kind'] == 'a84']
    def line(ph, r, note=''):
        m, t = box_of(r); print(f"{ph:9s} {r['id']:22s} {r['file']:52s} {r['blob'][:12]} {m}G/{t}s expect={r['expect']} {note}")
    print('PHASE 1: controls (stop on RED/PROVENANCE; pause with results withheld on INCONCLUSIVE; A4.6 true = caveat)')
    for r in ctl: line('control', r)
    print('PHASE 2: primaries')
    for r in pri: line('primary', r, f"cond={r['cond']}")
    print('PHASE 3: fallbacks, run unless primary has rc=0, a reconstructed false for the kept query, and (no row condition)')
    for r in pri: line('fallback', fb[r['id']], f"if-trigger(cond={r['cond']}: " + ('always, trace read by reader)' if r['cond'] != '-' else 'primary not counted)'))
    print('PHASE 4: A8.4 (unsliced, one at a time, 16G/7200s; query-specific traces logged)')
    for r in a84: line('a84', r)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--audit-only', action='store_true'); g.add_argument('--dry-run', action='store_true'); g.add_argument('--execute', action='store_true')
    ap.add_argument('--jobs', type=int, default=2, help='concurrent slice runs (sum of MemoryMax <= %d GB)' % SLICE_BUDGET_GB)
    args = ap.parse_args()
    a = audit()
    print('CHECKED', dict(a.n))
    if a.fail:
        print(f'AUDIT FAILED: {len(a.fail)} failure(s)'); sys.exit(1)
    print('AUDIT PASSED; runner sha256', sha256(os.path.abspath(__file__)))
    rows = read_manifest()
    if args.audit_only: sys.exit(0)
    if args.dry_run: plan(rows); sys.exit(0)
    # --execute
    if os.path.exists(LOG) and os.path.getsize(LOG): print('counted.log exists and is non-empty; refusing (no re-run without the author)'); sys.exit(5)
    if os.path.isdir(OUT) and os.listdir(OUT): print('out/ is non-empty; refusing'); sys.exit(5)
    for t in ('/usr/bin/time', '/usr/bin/systemd-run'):
        if not os.path.exists(t): print('missing', t); sys.exit(5)
    os.makedirs(OUT, exist_ok=True)
    budget = Budget(SLICE_BUDGET_GB)
    log(f"# batch start {datetime.datetime.utcnow().isoformat()}Z runner_sha256={sha256(os.path.abspath(__file__))} "
        f"manifest_sha256={sha256(MANIFEST)} proverif=2.05 lib_sha256={PINS[LIB]}")
    def stop(code, why):
        log(f'# BATCH STOPPED code={code}: {why}. No result in this log is to be counted or read until the author rules.')
        print('BATCH STOPPED:', why); sys.exit(code)
    # phase 1: controls
    ctl = [r for r in rows if r['kind'] == 'control']
    log('# PHASE 1 controls')
    xs = pool_run(ctl, args.jobs, budget, stop_on=lambda x: control_status(x) in ('RED', 'PROVENANCE'))
    st = {x['row']['id']: control_status(x) for x in xs}
    for i, s in st.items(): log(f'# control {i} status={s}')
    if any(s == 'PROVENANCE' for s in st.values()): stop(4, 'provenance mismatch in a control')
    if any(s == 'RED' for s in st.values()): stop(4, 'control red: ' + ','.join(i for i, s in st.items() if s == 'RED'))
    if len(xs) != len(ctl) or any(s == 'INCONCLUSIVE' for s in st.values()):
        stop(3, 'control gate incomplete (inconclusive or unrun control): ' + ','.join(i for i, s in st.items() if s == 'INCONCLUSIVE'))
    if any(s == 'CAVEAT_GREEN_A46' for s in st.values()): log('# CAVEAT: A4.6 control proved true (slice too tight at that depth); rows on that slice read with that caveat')
    log('# control gate CLOSED')
    # phase 2: primaries
    pri = [r for r in rows if r['kind'] == 'primary']
    log('# PHASE 2 primaries')
    px = pool_run(pri, args.jobs, budget, stop_on=lambda x: not x['prov'])
    if len(px) != len(pri) or any(not x['prov'] for x in px): stop(4, 'provenance mismatch in a primary')
    # phase 3: fallbacks
    fb = {r['id']: r for r in rows if r['kind'] == 'fallback'}
    todo = [fb[x['row']['id']] for x in px if not counted_primary(x)]
    log(f'# PHASE 3 fallbacks for rows {[r["id"] for r in todo]}')
    fx = pool_run(todo, args.jobs, budget, stop_on=lambda x: not x['prov'])
    if len(fx) != len(todo) or any(not x['prov'] for x in fx): stop(4, 'provenance mismatch in a fallback')
    # phase 4: A8.4, one at a time
    log('# PHASE 4 A8.4')
    for r in [r for r in rows if r['kind'] == 'a84']:
        x = run_one(r, budget)
        log(f"# a84 {r['id']} {a84_tags(x)}")
        if not x['prov']: stop(4, 'provenance mismatch in an A8.4 file')
    log('# batch complete')
    print('batch complete; log:', LOG)

if __name__ == '__main__':
    main()
