from pathlib import Path
import runpy,json,shutil
base=Path(__file__).resolve().parent
shutil.copy2(base/'copy/suite/capstone/proverif/slice/run_counted.py',base/'runner_helpers_copy.py')
n=runpy.run_path(str(base/'runner_helpers_copy.py'))
parse=n['parse_results']
def x(t,expect='true',rc=0,prov=True,cond='-'):return dict(row=dict(expect=expect,cond=cond),res=parse(t),rc=rc,prov=prov)
res=[]
res.append(dict(test='per-query trace',results=parse('A trace has been found.\nRESULT not event(E()) is false.\n\nRESULT not event(W()) is true.\n')))
for name,v in [('negative green',x('RESULT not event(E()) is true.')),('negative red',x('A trace has been found.\nRESULT not event(E()) is false.')),('positive traced red',x('A trace has been found.\nRESULT not event(E()) is false.','false+trace')),('positive untraced red',x('RESULT not event(E()) is false.','false+trace')),('positive green',x('RESULT not event(E()) is true.','false+trace')),('rc nonzero',x('RESULT not event(E()) is true.',rc=124)),('provenance mismatch',x('RESULT not event(E()) is true.',prov=False))]:res.append(dict(test=name,status=n['control_status'](v)))
for cond in ['-','T','T,L','L','H']:res.append(dict(test='fallback predicate '+cond,counted=n['counted_primary'](x('A trace has been found.\nRESULT not event(E()) is false.',cond=cond))))
res.append(dict(test='A84 nonzero rc misleading safety tag',tag=n['a84_tags'](x('RESULT event(E()) ==> kS = kV is true.\nA trace has been found.\nRESULT not event(W()) is false.',rc=124))))
(base/'helper-tests.json').write_text(json.dumps(res,indent=2)+'\n')
print('helper tests recorded; no subprocess or execution path invoked')
