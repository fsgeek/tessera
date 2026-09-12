from pathlib import Path
import json,re
rows=json.load(open('scratch/matrix.json'));assert len(rows)==198,len(rows)
header='mutant\tsource_check\tT\tR_or_R1\tR2\tS\tA\tW_or_W1\tW2\tB\tRESULT_locations'
out=[header]
for r in rows:
 vals={name:(v,line) for name,v,line in r['results']}
 cols=[]
 for names in [('TypeConfused',),('Rescoped','RescopedD1'),('RescopedD2',),('InnerSigTransplanted',),('Reattributed',),('HonestWrappedAccepted','HonestWrappedAcceptedD1'),('HonestWrappedAcceptedD2',),('HonestAccepted',)]:
  v=next((vals[n][0] for n in names if n in vals),'-');cols.append(v)
 out.append('\t'.join([r['out'].replace('.out','.pv'),r['source']+':'+str(r['line'])]+cols+['; '.join(r['out']+':'+str(x[2]) for x in r['results'])]))
Path('scratch/dependencies.tsv').write_text('\n'.join(out)+'\n')
# Group matrix rows into guard kinds, preserving per-level provenance.
kinds=['evidence','tag','digest','slot','possession','poss_tag','poss_manifest','signature','sig_tag','sig_bytes','type','alg','id','fp','hash']
lines=['guard\toutcomes_by_model_and_level\tevidence_rows']
for kind in kinds:
 selected=[]
 for i,r in enumerate(rows,2):
  bits=r['name'].split('_');k='_'.join(bits[3:]) if bits[2].startswith('ev') else '_'.join(bits[2:])
  if k==kind:selected.append((i,r))
 lines.append('\t'.join([kind,'; '.join(r['name']+':'+(','.join(r['changed']) or 'unchanged') for _,r in selected),'; '.join('scratch/dependencies.tsv:'+str(i) for i,_ in selected)]))
Path('scratch/guard_groups.tsv').write_text('\n'.join(lines)+'\n')
# Check baseline results match committed results modulo variable suffixes.
base={'q1d':'sp7_q1_strict_dns_compromised','q1r':'sp7_q1_strict_repo_compromised','q2':'sp7_q2_degraded_compromised','q4o':'sp7_q4_control_opaque_twoversion','q5':'sp7_q5_depth2_correct'}
def results(p):return re.findall(r'RESULT not event\((\w+)\(.*? is (true|false)\.',p.read_text())
verification=[]
for short,stem in base.items():
 a=results(Path('scratch',short+'_baseline.out'));b=results(Path('proverif',stem+'.out'));assert a==b,(short,a,b)
 verification.append(short+' baseline matches committed '+str(len(a))+' results')
# Every reported false event in committed outputs has both a derivation and a trace.
v=['model\tevent\tresult\tderivation\ttrace\tresult_line']
for p in sorted(Path('proverif').glob('*.out')):
 lines=p.read_text().splitlines();start=0
 for i,l in enumerate(lines):
  if l.startswith('-- Query'):start=i
  if l.startswith('RESULT'):
   event=re.search(r'event\((\w+)\(',l)[1];truth=l.endswith('is true.')
   d=[j+1 for j in range(start,i) if lines[j]=='Derivation:'];t=[j+1 for j in range(start,i) if lines[j]=='A trace has been found.']
   if not truth:assert d and t,(p,event)
   v.append('\t'.join([str(p),event,str(truth),str(d[-1] if d else '-'),str(t[-1] if t else '-'),str(i+1)]))
Path('scratch/committed_audit.tsv').write_text('\n'.join(v)+'\n')
verification.append('All committed reachable events have a Derivation and a found trace')
verification.append('198 single-check mutants have complete results; 5 baselines match')
Path('scratch/verification.txt').write_text('\n'.join(verification)+'\n')
print('\n'.join(verification))
