from pathlib import Path
import re,hashlib,json,subprocess
root=Path(__file__).resolve().parent.parent
stems=['cap_cc03_d__depth0.cone__cq5','cap_cc08_d__depth0.cone__cq5','cap_cc04_d__depth1.cone__cq4r','cap_cc04_d__depth1.cone__link6b','cap_cc07i_d__depth0.cone__cq8','cap_cc07i_d__depth0.cone__link4','cap_cc07i_d__depth0__auhk','cap_cc07ii_d__depth0.cone__cq8','cap_cc07ii_d__depth0.cone__link4','cap_cc17_d__depth0.cone__link2a','cap_cc17_d__depth0__sf','cap_cc02_d__depth0.cone__link5']
ns={'__name__':'audit_import'}
exec(compile((root/'slice.py').read_text(),str(root/'slice.py'),'exec'),ns)
lines=[]
for stem in stems:
 p=next(p for p in [root/'gen_ext'/(stem+'.pv'),root/'gen'/(stem+'.pv')] if p.exists())
 src,sl,q=stem.split('__'); original=(root/'../../'/(src+'.pv')).read_text(); saved=p.read_text(); body='\n'.join(saved.splitlines()[2:])+'\n'
 expected,dropped,nq=ns['make'](original,sl,q)
 assert body==expected,stem
 # Independently compare all text before the final parallel block, ignoring query declarations only.
 def prefix(t):
  t=re.sub(r'(?ms)^query\b.*?\.[ \t]*$','',t)
  t=t.replace('(* query deleted by slice.py *)','')
  return t[:t.index('\n  ( !')]
 assert prefix(original)==prefix(body),stem
 # Current final components are unchanged members, in original order.
 def comps(t): return ns['split_top'](t[t.index('\n  ( !')+1:].strip())
 oc=comps(original); bc=comps(body); it=iter(oc)
 assert all(any(c==x for x in it) for c in bc),stem
 assert all(c.startswith('!') for c in oc),stem
 out=(root/'out'/(stem+'.out')).read_text()
 assert 'A trace has been found.' in out
 assert any(l.startswith('RESULT') and 'is false.' in l for l in out.splitlines())
 lines.append(f'{stem}: regenerated exactly; prefix unchanged except queries; unchanged replicated components retained in order; reconstructed false; deleted={len(dropped)}; sha256={hashlib.sha256(p.read_bytes()).hexdigest()}')
for line in (root/'codex2/reruns.jsonl').read_text().splitlines():
 r=json.loads(line); new=(root/r['output']).read_text(); old=(root/'out'/Path(r['output']).name).read_text()
 assert old.splitlines()[0].startswith('EXPLORATORY PROBE ')
 match=new=='\n'.join(old.splitlines()[1:])+'\n'
 assert match
 lines.append(f"{r['output']}: byte-identical to saved output after removing its single exploratory banner; rc={r['returncode']}; seconds={r['seconds']}")
lines.append('The raw identical_to_saved=false fields in reruns.jsonl include the saved exploratory banner; normalized comparisons above resolve that difference.')
lines.append('HEAD '+subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip())
lines.append('proverif binary sha256 '+hashlib.sha256((Path.home()/'.local/bin/proverif').read_bytes()).hexdigest())
lines.append('library sha256 '+hashlib.sha256((root/'../../../../lib/tessera_theory.pvl').read_bytes()).hexdigest())
(root/'codex2/audit.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
