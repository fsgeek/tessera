import subprocess, glob, os, re, difflib
src=open('/home/tony/projects/tessera/formal/suite/capstone/proverif/ladder3-staging/tools/bf56_edit.py').read()
# extract replacement pairs by exec-ing in a sandbox that records rep calls
pairs=[]
ns={'open':lambda *a,**k: type('F',(),{'read':lambda s:'', 'write':lambda s,x:None})()}
code=src.replace("p='capstone.pv'; t=open(p).read()","t=''").replace("open(p,'w').write(t)","")
code=code.replace("""def rep(old,new):
    global t
    assert t.count(old)==1, (t.count(old), old[:60])
    t=t.replace(old,new)""","def rep(old,new): pairs.append((old,new))")
exec(code,{'pairs':pairs})
def bf56(t):
    for old,new in pairs:
        o2,n2=old,new
        if o2 not in t:
            o2=o2.replace("(pkDv: pkey, pkRv: pkey)","(pkSv: pkey)"); n2=n2.replace("(pkDv: pkey, pkRv: pkey)","(pkSv: pkey)")
        c=t.count(o2)
        if c!=1: return None,"anchor count %d for %r"%(c,old[:40])
        t=t.replace(o2,n2)
    return t,None
rows=[]
for f in sorted(glob.glob('*.pv')):
    old=open('../'+f).read(); new=open(f).read()
    ob=subprocess.check_output(['git','hash-object','../'+f]).decode().strip()
    nb=subprocess.check_output(['git','hash-object',f]).decode().strip()
    d=list(difflib.unified_diff(old.splitlines(),new.splitlines(),lineterm='',n=0))
    add=sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    rem=sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    exp,err=bf56(old)
    if err: verdict='ERROR '+err
    elif exp==new: verdict='BF-5/BF-6 only'
    else:
        d2=[l for l in difflib.unified_diff(exp.splitlines(),new.splitlines(),lineterm='',n=0) if l[:1] in '+-' and l[:3] not in ('+++','---')]
        verdict='BF-5/BF-6 + residual: '+str(len(d2))+' lines'
        open('/tmp/resid_'+f+'.txt','w').write("\n".join(d2))
    rows.append((f,ob,nb,add,rem,verdict))
for r in rows: print(*r, sep=' | ')
