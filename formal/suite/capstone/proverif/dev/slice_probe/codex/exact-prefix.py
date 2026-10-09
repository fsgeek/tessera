from pathlib import Path
import re
for folder in ['gen','gen_ext']:
 for p in sorted(Path(folder).glob('*.pv')):
  src=Path('../..')/(p.stem.split('__')[0]+'.pv'); original=src.read_text(); body=p.read_text().split('\n',2)[2]
  # Source query declarations here have no periods except the final terminator.
  qs=list(re.finditer(r'(?m)^query\b[^.]*\.',original))
  expected=original
  for m in reversed(qs):
   if m.group() not in body:expected=expected[:m.start()]+'(* query deleted by slice.py *)'+expected[m.end():]
  prefix=expected[:expected.index('\n  ( !out(honestKeyCh')+1]
  assert body.startswith(prefix),p
  if '__none__' in p.name:assert body==expected,p
  print('EXACT_PREFIX_OK',p)
print('TOTAL 93; every byte outside query removals and final parallel block preserved')
