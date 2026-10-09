# scratch: builds slice/MANIFEST.tsv (rows.txt, with the fallbacks of rows 12, 14, 15 changed to depth1.cone)
import subprocess, os, glob
os.chdir('/home/tony/projects/tessera/formal/suite/capstone/proverif')
SRCBLOB = {'cap_cc02_d':'221b997477a282092c8e9e2e5eec718523eee873','cap_cc03_d':'cc6f21c8928a00021820ee6f6617c8cdbe283140',
 'cap_cc04_d':'a88ded5036dbfe14f9ea79ba66d5b3f22286d12a','cap_cc05_d':'897f56809be6b8e8f315a34de88d452455505525',
 'cap_cc06_d':'ee1bce1be260392bea5e052d6baa52aecf566226','cap_cc07i_d':'ff70204731186f62d7f5f1c5d98ed33ea7718073',
 'cap_cc07ii_d':'14434b6185ef96684aaecc13b883c86dc9fe4f52','cap_cc08_d':'0406e86f91951d419b9c9dfb1a506efe05f8634c',
 'cap_cc08ii_d':'d862bf69b234bddeed681ae1a1f1c99df71edac1','cap_cc17_d':'19b706af3d835c32355c288f23def063d3cf5676',
 'capstone_d':'527ff7e35d9cda12377046295bd2c24e4bd34f92'}
def blob(p): return subprocess.check_output(['git','hash-object',p],text=True).strip()
for s,b in SRCBLOB.items(): assert blob(s+'.pv')==b, s
rows=[l.split() for l in open('dev/prereg_scratch/rows.txt')]
COND={3:'T',12:'T,L',14:'L',15:'L',30:'H'}
out=['#kind\tid\tfile\tblob\tsrc\tsrcblob\tslice\tquery\tcond\texpect']
def line(kind,i,src,sl,q,cond,expect):
    f=f'gen/{src}__{sl}__{q}.pv'; assert os.path.exists('slice/'+f),f
    out.append('\t'.join([kind,i,f,blob('slice/'+f),src+'.pv',SRCBLOB[src],sl,q,cond,expect]))
for n,(src,q,p,fb) in enumerate(rows,1):
    if n in (12,14,15):
        assert fb=='depth0.cone'; fb='depth1.cone'
    c=COND.get(n,'-')
    line('primary',str(n),src,p,q,c,'false+trace'); line('fallback',str(n),src,fb,q,c,'false+trace')
for f in sorted(glob.glob('slice/gen/capstone_d__*.pv')):
    _,sl,q=os.path.basename(f)[:-3].split('__')
    line('control',f'C:{sl}:{q}','capstone_d',sl,q,'-','false+trace' if q=='a46' else 'true')
for f in sorted(glob.glob('slice/a84/a84_*.pv')):
    nm=os.path.basename(f)[4:-3]
    out.append('\t'.join(['a84','A:'+nm,f[6:],blob(f),nm+'.pv',blob(nm+'.pv'),'a84','C-Q6k+A8.4w','-','see-run_counted']))
open('slice/MANIFEST.tsv','w').write('\n'.join(out)+'\n')
print(len(out)-1)
