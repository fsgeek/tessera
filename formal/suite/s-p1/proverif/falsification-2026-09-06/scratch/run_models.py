from pathlib import Path
import subprocess, concurrent.futures, sys
files=[p for pattern in sys.argv[1:] for p in Path('scratch').glob(pattern)]
def run(p):
 with p.with_suffix('.out').open('w') as out:
  try:
   r=subprocess.run(['proverif','-lib','./tessera_theory.pvl',str(p)],stdout=out,stderr=subprocess.STDOUT,timeout=120)
   status=str(r.returncode)
  except subprocess.TimeoutExpired: status='TIMEOUT';out.write('\nREVIEW TIMEOUT 120s\n')
 lines=[f'{i}: {s}' for i,s in enumerate(p.with_suffix('.out').read_text().splitlines(),1) if s.startswith('RESULT') or 'Error' in s]
 return p.name+' exit='+status+'\n'+'\n'.join(lines)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(run,sorted(files)): print(result,flush=True)
