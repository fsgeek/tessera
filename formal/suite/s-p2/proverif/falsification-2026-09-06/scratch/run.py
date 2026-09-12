from pathlib import Path
import subprocess,json,concurrent.futures,time
jobs=json.loads(Path('scratch/jobs.json').read_text())
def run(j):
 p=Path(j['file']); t=time.monotonic()
 with p.with_suffix('.out').open('w') as f:
  try:r=subprocess.run(['proverif','-lib','./tessera_theory.pvl',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=90);j['exit']=r.returncode
  except subprocess.TimeoutExpired:j['exit']='timeout'
 j['seconds']=round(time.monotonic()-t,2)
 j['results']=[f'{i}: {l}' for i,l in enumerate(p.with_suffix('.out').read_text().splitlines(),1) if l.startswith('RESULT')]
 return j
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 results=list(ex.map(run,jobs))
Path('scratch/results.json').write_text(json.dumps(results,indent=2))
for j in results:
 print(j['file'],j['exit'],j['seconds'], ' '.join(x.split('event(')[-1].split('(')[0]+':'+x.split(' is ')[-1] for x in j['results']))
