from pathlib import Path
import json,re
rec=json.load(open('scratch/mutations.json'))
rows=[];pending=[]
for r in rec:
 p=Path('scratch',r['name']+'.out');typed=p.with_name(p.stem+'_typed.out')
 if typed.exists():p=typed
 results=[]
 if p.exists():
  for i,l in enumerate(p.read_text().splitlines(),1):
   m=re.match(r'RESULT not event\((\w+)\(.* is (true|false)\.',l)
   if m:results.append((m[1],m[2],i))
 expected=8 if r['name'].startswith('q5_') else 5 if r['name'].startswith('q4o_') else 6
 if len(results)!=expected:pending.append((r['name'],len(results)))
 else:
  changed=[x[0] for x in results if (x[1]=='true')==x[0].startswith('Honest')]
  rows.append(dict(**r,out=str(p),results=results,changed=changed))
Path('scratch/matrix.json').write_text(json.dumps(rows,indent=2))
print('complete',len(rows),'pending',pending)
for r in rows:
 if r['changed']:print(r['name'],r['changed'])
