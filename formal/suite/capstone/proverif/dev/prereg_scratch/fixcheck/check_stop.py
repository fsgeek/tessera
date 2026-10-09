"""Stop-race, launch-lock, batch-lock, kill and jobs tests for the fixed runner. No ProVerif; stub commands via the
test-only _cmd hook of run_one (never passed by --execute)."""
from pathlib import Path
import runpy, json, shutil, tempfile, threading, time, os, sys, argparse, inspect
base=Path(__file__).resolve().parent
shutil.copy2(base/'copy/suite/capstone/proverif/slice/run_counted.py',base/'runner_stop_copy.py')
res=[]
def rec(t,got,want):res.append(dict(test=t,got=got,want=want,ok=got==want))
def fresh():
    import importlib.util
    sp=importlib.util.spec_from_file_location('rc_%d'%time.time_ns(),str(base/'runner_stop_copy.py')); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); n=vars(m)
    td=Path(tempfile.mkdtemp(dir=base/'tmp'))
    (td/'out').mkdir(); (td/'gen').mkdir()
    n['HERE']=str(td); n['OUT']=str(td/'out'); n['LOG']=str(td/'counted.log')
    return n,td
def mkrow(n,td,i):
    f=td/'gen'/f'm{i}.pv'; f.write_text('model %d\n'%i)
    return dict(kind='primary',id=str(i),file=f'gen/m{i}.pv',blob=n['gitblob'](str(f)),slice='depth1',cond='-',expect='-')
def setup(k):
    n,td=fresh(); rows=[mkrow(n,td,i) for i in range(k)]
    prov={str(td/r['file']):('gitblob',r['blob']) for r in rows}
    lib=td/'lib.pvl'; lib.write_text('lib\n'); prov[str(lib)]=('sha256',n['sha256'](str(lib)))
    n['BOXES']['depth1']=(8,3600)
    batch=n['Batch'](prov,n['Budget'](8))
    return n,td,rows,batch,lib
def stub(td,body):
    s=td/'stub.sh'; s.write_text('#!/bin/sh\necho x >> %s/launches\n%s\n'%(td,body)); s.chmod(0o755); return [str(s)]
def launches(td):
    p=td/'launches'; return len(p.read_text().split()) if p.exists() else 0
# 1. stop while waiters are queued on memory: only the first launches; waiters wake, launch nothing, memory returns
n,td,rows,batch,lib=setup(4)
cmd=stub(td,'echo "RESULT not event(E()) is true."; sleep 1.5')
out=[]
def worker(r): out.append(n['run_one'](r,batch,_cmd=cmd))
th=[threading.Thread(target=worker,args=(r,)) for r in rows]
[t.start() for t in th]; time.sleep(0.5)
batch.set_stop('test stop')
t0=time.time(); [t.join(10) for t in th]
rec('stop race: launches after queued waiters + stop',launches(td),1)
rec('stop race: cancelled workers return None',sorted(o is None for o in out),[False,True,True,True])
rec('stop race: waiters woken promptly (<1.4s of first run end)',time.time()-t0<1.4,True)
rec('stop race: memory fully released',batch.budget.free,8)
# 2. launch after stop refused
n,td,rows,batch,lib=setup(1)
batch.set_stop('x')
rec('post-stop run_one refused',n['run_one'](rows[0],batch,_cmd=stub(td,'true')),None)
rec('post-stop: no launch, no out file',(launches(td),os.listdir(td/'out')),(0,[]))
rec('post-stop: memory untouched',batch.budget.free,8)
# 3. model changed before launch: no launch, shared stop, hashes logged
n,td,rows,batch,lib=setup(2)
(td/rows[0]['file']).write_text('tampered\n'); open(n['LOG'],'x').close()
rec('model tampered before launch: refused',n['run_one'](rows[0],batch,_cmd=stub(td,'true')),None)
rec('model tampered: stopped, no launch',(batch.stopped(),launches(td)),(True,0))
rec('model tampered: the OTHER row is also refused (shared stop)',n['run_one'](rows[1],batch,_cmd=stub(td,'true')),None)
lg=Path(n['LOG']).read_text()
rec('model tampered: actual hash logged',('PROVENANCE MISMATCH' in lg and 'actual='+n['gitblob'](str(td/rows[0]['file'])) in lg),True)
rec('model tampered: memory released',batch.budget.free,8)
# 4. library (shared input) changed before launch of an UNRELATED model
n,td,rows,batch,lib=setup(1); open(n['LOG'],'x').close(); lib.write_text('changed lib\n')
rec('library changed before launch: refused',(n['run_one'](rows[0],batch,_cmd=stub(td,'true')),launches(td)),(None,0))
# 5. shared file changed DURING a run (persistent change): run flagged, stop set
n,td,rows,batch,lib=setup(2); open(n['LOG'],'x').close()
x=n['run_one'](rows[0],batch,_cmd=stub(td,'echo changed >> %s; echo "RESULT not event(E()) is true."'%lib))
rec('change during run: prov False and batch stopped',(x['prov'],batch.stopped()),(False,True))
rec('change during run: next launch refused',(n['run_one'](rows[1],batch,_cmd=stub(td,'true')),launches(td)),(None,1))
# 6. leftover children killed before memory is returned
n,td,rows,batch,lib=setup(1); open(n['LOG'],'x').close()
x=n['run_one'](rows[0],batch,_cmd=stub(td,'sleep 60 </dev/null >/dev/null 2>&1 &\necho $! > %s/child.pid'%td))
time.sleep(0.3); pid=int((td/'child.pid').read_text())
try: os.kill(pid,0); alive=True
except ProcessLookupError: alive=False
rec('orphan subprocess killed on return',alive,False)
# 7. normal run is OK and logged
n,td,rows,batch,lib=setup(1); open(n['LOG'],'x').close()
x=n['run_one'](rows[0],batch,_cmd=stub(td,'echo "RESULT not event(E()) is true."'))
rec('normal stub run: rc0, prov OK, one RESULT, not stopped',(x['rc'],x['prov'],len(x['res']),batch.stopped()),(0,True,1,False))
# 8. pool_run: stop_on triggers shared stop; remaining queued rows do not launch
n,td,rows,batch,lib=setup(4); open(n['LOG'],'x').close()
orig=n['run_one']; n['run_one']=lambda r,b,stop_on=None: orig(r,b,stop_on=stop_on,_cmd=stub(td,'echo "RESULT not event(E()) is false."; sleep 0.3'))
xs=n['pool_run'](rows,3,batch,stop_on=lambda x:'red')
rec('pool_run: at most first job wave launched (jobs=3 but 8G budget => 1 at a time)',launches(td),1)
rec('pool_run: stopped with reason',batch.reason,'red')
# 9. batch lock + existing artifacts
n,td=fresh()
fd1,why1=n['claim_batch'](); rec('claim: clean dir ok',why1,None)
fd2,why2=n['claim_batch'](); rec('claim: second concurrent claim refused',(fd2,'another batch' in why2),(None,True))
os.close(fd1)
fd3,why3=n['claim_batch'](); rec('claim: after release ok',why3,None); 
# lock held while artifacts are examined: log/out absence verified under the lock
open(n['LOG'],'x').close()
fd4,why4=n['claim_batch'](); rec('claim: lock still held by fd3 -> refused first',(fd4,'another batch' in why4),(None,True))
os.close(fd3)
fd5,why5=n['claim_batch'](); rec('claim: EMPTY counted.log refused',('counted.log exists' in (why5 or '')),True); os.close(fd5)
os.remove(n['LOG']); (td/'out'/'a.out').write_text('x')
fd6,why6=n['claim_batch'](); rec('claim: non-empty out/ refused',('out/' in (why6 or '')),True); os.close(fd6)
# 10. cross-process lock (real second process)
import subprocess
n,td=fresh(); fd,why=n['claim_batch']()
code='import runpy,sys;import importlib.util as u;sp=u.spec_from_file_location("r",%r);m=u.module_from_spec(sp);sp.loader.exec_module(m);n=vars(m);n["HERE"]=%r;n["OUT"]=%r;n["LOG"]=%r;fd,w=n["claim_batch"]();print(w)'%(str(base/'runner_stop_copy.py'),str(td),str(td/'out'),str(td/'counted.log'))
o=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True).stdout.strip()
rec('claim: second PROCESS refused cleanly',o,'another batch holds the lock; refusing'); os.close(fd)
# 11. --jobs validation, kill-after in command, no CLI/env test hook
n,td=fresh()
for v in ('0','-3'):
    try: n['positive_int'](v); ok=False
    except argparse.ArgumentTypeError: ok=True
    rec('jobs=%s rejected'%v,ok,True)
rec('jobs=2 accepted',n['positive_int']('2'),2)
c=n['build_cmd'](4,1800,'r','f')
rec('timeout has --kill-after=10s before the box',c[c.index('timeout')+1:c.index('timeout')+3],['--kill-after=10s','1800'])
src=(base/'runner_stop_copy.py').read_text()
rec('_cmd hook not reachable from main (only run_one signature)',('_cmd=' in src.split('def main')[1]),False)
rec('no environment override in runner',('os.environ' in src),False)
(base/'stop-tests.json').write_text(json.dumps(res,indent=2)+'\n')
bad=[r['test'] for r in res if not r['ok']]
print('STOP/LOCK TESTS: %d total, %d passed, failures: %s'%(len(res),len(res)-len(bad),bad))
for r in res:
    if not r['ok']: print(r)
