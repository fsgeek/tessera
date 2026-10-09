from pathlib import Path
import shutil, subprocess, hashlib, json, os
base=Path(__file__).resolve().parent
repo=Path('/home/tony/projects/tessera')
pv=repo/'formal/suite/capstone/proverif'
suite=base/'copy/suite'; cpv=suite/'capstone/proverif'; sl=cpv/'slice'
sl.mkdir(parents=True,exist_ok=True)
import re
for d in ('gen','a84'): shutil.copytree(pv/'slice'/d,sl/d,dirs_exist_ok=True)
for f in ('run_counted.py','MANIFEST.tsv','AUDIT.txt'): shutil.copy2(pv/'slice'/f,sl/f)
manifest=(sl/'MANIFEST.tsv').read_text(); runner=(sl/'run_counted.py').read_text()
MSHA=re.search(r"MANIFEST_SHA256 = '([0-9a-f]{64})'",runner).group(1)
assert MSHA==hashlib.sha256(manifest.encode()).hexdigest()
def repin_manifest(text):
 (sl/'MANIFEST.tsv').write_text(text);(sl/'run_counted.py').write_text(runner.replace(MSHA,hashlib.sha256(text.encode()).hexdigest()))
for ln in manifest.splitlines():
 if ln and not ln.startswith('#'): shutil.copy2(pv/ln.split('\t')[4],cpv/ln.split('\t')[4])
for f in ('dev/slice_probe/slice.py','dev/prereg_scratch/derive_a84.py'):
 p=cpv/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pv/f,p)
(suite/'lib').mkdir(exist_ok=True);shutil.copy2(repo/'formal/suite/lib/tessera_theory.pvl',suite/'lib/tessera_theory.pvl')
(base/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(base/'tmp'),PYTHONDONTWRITEBYTECODE='1')
results=[]
def run(name):
 p=subprocess.run(['python3',str(sl/'run_counted.py'),'--audit-only'],capture_output=True,text=True,env=env)
 (base/(name+'.txt')).write_text(p.stdout+p.stderr)
 results.append({'test':name,'rc':p.returncode,'failures':[s for s in p.stdout.splitlines() if s.startswith('FAIL')][:4]})
def blob(b):return hashlib.sha1(b'blob %d\0'%len(b)+b).hexdigest()
run('baseline')
r=manifest.splitlines()[1].split('\t'); target=sl/r[2]; original=target.read_bytes()
for name,b,repin in [('blob_mismatch',original+b'\n',False),('prefix_alteration',original.replace(b'free ',b'free altered_',1),True),('component_alteration',original.replace(b'!out(honestKeyCh',b'!out(alteredKeyCh',1),True),('query_alteration',original.replace(b'query ',b'query changed: bitstring, ',1),True),('prohibited_slice',original+b'\nphase 1.\n',True),('unexpected_set_slice',original+b'\nset maxDepth = 1.\n',True)]:
 target.write_bytes(b)
 if repin: repin_manifest(manifest.replace(r[3],blob(b)))
 else: (sl/'MANIFEST.tsv').write_text(manifest)
 run(name)
 target.write_bytes(original);(sl/'MANIFEST.tsv').write_text(manifest);(sl/'run_counted.py').write_text(runner)
lib=suite/'lib/tessera_theory.pvl'; origlib=lib.read_bytes()
for name,addition in [('prohibited_library',b'\nphase 1.\n'),('unexpected_set_library',b'\nset maxDepth = 1.\n'),('indented_set_library',b'\n  set maxDepth = 1.\n')]:
 lib.write_bytes(origlib+addition)
 (sl/'run_counted.py').write_text(runner.replace(hashlib.sha256(origlib).hexdigest(),hashlib.sha256(lib.read_bytes()).hexdigest()))
 run(name)
 lib.write_bytes(origlib);(sl/'run_counted.py').write_text(runner)
# Manifest-semantics changes with files, blobs and counts untouched (manifest NOT repinned in runner => pin must reject)
lines=[]
for ln in manifest.splitlines():
 f=ln.split('\t')
 if f[0]=='control' and f[9]=='true': f[9]='false+trace';ln='\t'.join(f)
 lines.append(ln)
(sl/'MANIFEST.tsv').write_text('\n'.join(lines)+'\n');run('control_expectation_tamper')
lines=[]
for ln in manifest.splitlines():
 f=ln.split('\t')
 if f[0]=='primary' and f[8]!='-': f[8]='-';ln='\t'.join(f)
 lines.append(ln)
(sl/'MANIFEST.tsv').write_text('\n'.join(lines)+'\n');run('condition_removal_tamper')
(sl/'MANIFEST.tsv').write_text(manifest)
(base/'audit-tests.json').write_text(json.dumps(results,indent=2)+'\n')
bad=[r['test'] for r in results if (r['test']=='baseline')!=(r['rc']==0)]
print(json.dumps(results,indent=2))
print('AUDIT TESTS: %d total, %d behaved as required (baseline passes, every mutation rejected), failures: %s'%(len(results),len(results)-len(bad),bad))
