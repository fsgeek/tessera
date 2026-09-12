from pathlib import Path
import re,difflib
order=['authorityD','authorityR','authorityS','authority_digestD','authority_digestR','authority_digestS','authority_tagD','authority_tagR','authority_tagS','entitled','key_equal','signature_key','tlr_tag','anchor','lookup_identity','lookup','derived_identity','terminal_identity','terminal_predicate','entry_disposition','refused_branch','missing_branch','env_authorityD','env_authorityR','env_authorityS','env_fingerprint','env_core_tuple','env_possession','env_bytes','env_frame_alg','env_frame_id','env_frame_fp','env_manifest','envelope']
lines=['Columns: name; DNS/REPO/DEG RESULT truth vectors in order U,H1,H2,not-Unentitled,not-N1,not-S1,not-S2,not-S3,not-S4,not-Mismatch,not-ReasonCollapsed; each output line cited below.']
for lab in order:
 row=[lab]
 for mode in ['dns','repo','deg']:
  p=Path('scratch',f'm_{mode}_{lab}.out')
  if not p.exists():row.append('-');continue
  res=[(i,l) for i,l in enumerate(p.read_text().splitlines(),1) if l.startswith('RESULT')]
  assert len(res)==11,(p,len(res))
  vec=''.join('T' if l.endswith('true.') else 'F' if l.endswith('false.') else '?' for i,l in res)
  row.append(vec+' '+str(p)+':'+','.join(str(i) for i,l in res))
 lines.append(' | '.join(row))
Path('scratch/dependency-index.txt').write_text('\n'.join(lines)+'\n')
lines=[]
for p in sorted(Path('proverif').glob('*.out')):
 ls=p.read_text().splitlines();start=0
 for i,l in enumerate(ls):
  if l.startswith('-- Query'):start=i
  if l.startswith('RESULT'):
   d=[j+1 for j in range(start,i) if ls[j]=='Derivation:']
   t=[j+1 for j in range(start,i) if ls[j]=='A trace has been found.']
   if l.endswith('false.'):assert d and t,(p,i)
   lines.append(f'{p}:{i+1} | {l} | derivation={d} trace={t}')
Path('scratch/committed-index.txt').write_text('\n'.join(lines)+'\n')
# Store exact single-check diffs with line numbers in original and modified .pv files.
lines=[]
for p in sorted(Path('scratch').glob('m_*.pv')):
 if 'parsefail' in p.stem or p.stem=='m_foreign_tlr_tag':continue
 mode=p.stem.split('_')[1]
 orig=Path('proverif',{'dns':'ss_q1_strict_dns_compromised.pv','repo':'ss_q1_strict_repo_compromised.pv','deg':'ss_q1d_degraded_compromised.pv'}[mode])
 lines.extend(difflib.unified_diff(orig.read_text().splitlines(),p.read_text().splitlines(),str(orig),str(p),lineterm=''))
Path('scratch/mutations.diff').write_text('\n'.join(lines)+'\n')
print('Successful outputs:',sum('RESULT' in p.read_text() for p in Path('scratch').glob('*.out')))
print('Retained parse failures:',len(list(Path('scratch').glob('*parsefail.out'))))
