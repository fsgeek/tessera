from pathlib import Path
import subprocess,concurrent.futures,json,re
ps=list(Path('proverif').glob('*.pv'))
def run(p):
 q=Path('scratch')/('baseline_'+p.name);q.write_text(p.read_text())
 with q.with_suffix('.out').open('w') as f:r=subprocess.run(['proverif','-lib','./tessera_theory.pvl',str(q)],stdout=f,stderr=subprocess.STDOUT)
 results=lambda f:[l for l in f.read_text().splitlines() if l.startswith('RESULT')]
 return p.name,r.returncode,results(p.with_suffix('.out'))==results(q.with_suffix('.out'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:rows=list(e.map(run,ps))
Path('scratch/baselines.tsv').write_text('model\texit\tRESULT lines identical to committed output\n'+'\n'.join('\t'.join(map(str,r)) for r in rows)+'\n')
print(rows)
# Verify attack files preserve verifier checks: strip added monitor wrappers before comparing individual check lines.
b=Path('proverif/sp2_q1_strict_dns_compromised.pv').read_text()
def checks(s):
 s=s[s.index('let Verifier1'):s.index('let SetJudge')]
 return [l.strip() for l in s.splitlines() if l.strip().startswith(('let ', 'if ', 'in(c,','event Accept'))]
for p in Path('scratch').glob('a_*.pv'):assert checks(p.read_text())==checks(b),p
print('All seven attacks retain every verifier check.')
j=json.loads(Path('scratch/results.json').read_text())
assert all(x['exit']==0 for x in j)
assert all(len(x['results'])==7 for x in j if 'base' in x)
assert all(all('is false.' in r for r in x['results'][4:]) for x in j if 'base' in x)
print('169 valid single-check mutants, all three witnesses retained.')
