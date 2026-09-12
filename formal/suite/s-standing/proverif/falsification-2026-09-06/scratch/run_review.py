from pathlib import Path
import subprocess,concurrent.futures
files=sorted(Path('scratch').glob('*.pv'))
def run(p):
 with p.with_suffix('.out').open('w') as out:
  try:r=subprocess.run(['proverif','-lib','./tessera_theory.pvl',str(p)],stdout=out,stderr=subprocess.STDOUT,timeout=90);return p.name,r.returncode
  except subprocess.TimeoutExpired:return p.name,'TIMEOUT'
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for name,code in ex.map(run,files): print(name,code,flush=True)
