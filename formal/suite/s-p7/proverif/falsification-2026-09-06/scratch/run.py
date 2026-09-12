from pathlib import Path
import subprocess,concurrent.futures,json,sys,time
files=[Path(x) for x in sys.argv[1:]] if len(sys.argv)>1 else sorted(Path('scratch').glob('*.pv'))
def run(p):
 t=time.time()
 with p.with_suffix('.out').open('w') as f:
  try:r=subprocess.run(['proverif','-lib','./tessera_theory.pvl',str(p)],stdout=f,stderr=subprocess.STDOUT,timeout=90);code=r.returncode
  except subprocess.TimeoutExpired: f.write('\nREVIEW TIMEOUT 90s\n');code=124
 return {'file':str(p),'exit':code,'seconds':round(time.time()-t,3)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for r in ex.map(run,files): print(json.dumps(r),flush=True)
