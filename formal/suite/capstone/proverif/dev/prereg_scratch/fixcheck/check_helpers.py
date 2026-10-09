from pathlib import Path
import runpy,json,shutil
base=Path(__file__).resolve().parent
shutil.copy2(base/'copy/suite/capstone/proverif/slice/run_counted.py',base/'runner_helpers_copy.py')
n=runpy.run_path(str(base/'runner_helpers_copy.py'))
parse=n['parse_results']
def x(t,expect='true',rc=0,prov=True,cond='-'):return dict(row=dict(expect=expect,cond=cond),res=parse(t),rc=rc,prov=prov)
res=[]
def rec(test,got,want):res.append(dict(test=test,got=got,want=want,ok=got==want))
T='A trace has been found.\n'
rec('per-query trace',[(r['verdict'],r['trace']) for r in parse(T+'RESULT not event(E()) is false.\n\nRESULT not event(W()) is true.\n')],[('false',True),('true',False)])
for name,v,w in [('negative green',x('RESULT not event(E()) is true.'),'OK'),('negative red',x(T+'RESULT not event(E()) is false.'),'RED'),
 ('positive traced red',x(T+'RESULT not event(E()) is false.','false+trace'),'OK'),('positive untraced red',x('RESULT not event(E()) is false.','false+trace'),'INCONCLUSIVE'),
 ('positive green',x('RESULT not event(E()) is true.','false+trace'),'CAVEAT_GREEN_A46'),('rc nonzero',x('RESULT not event(E()) is true.',rc=124),'INCONCLUSIVE'),
 ('provenance mismatch',x('RESULT not event(E()) is true.',prov=False),'PROVENANCE')]:rec(name,n['control_status'](v),w)
for cond in ['-','T','T,L','L','H']:rec('fallback predicate '+cond,n['counted_primary'](x(T+'RESULT not event(E()) is false.',cond=cond)),cond=='-')
S='RESULT event(E()) ==> kS = kV is %s.\n'
W='RESULT not event(W()) is %s.\n'
tag=n['a84_tags']
rec('A84 rc=124 safety true + witness',tag(x(S%'true'+T+W%'false',rc=124)).split()[0],'UNCOUNTABLE_rc=124')
rec('A84 rc=124 safety false+trace',tag(x(T+S%'false'+T+W%'false',rc=124)).split()[0],'UNCOUNTABLE_rc=124')
rec('A84 prov mismatch',tag(x(S%'true'+T+W%'false',prov=False)).split()[0],'UNCOUNTABLE_PROVENANCE')
rec('A84 only one result',tag(x(S%'true')).split()[0],'UNCOUNTABLE_RESULT_SET')
rec('A84 three results',tag(x(S%'true'+W%'true'+W%'true')).split()[0],'UNCOUNTABLE_RESULT_SET')
rec('A84 safety false no trace',tag(x(S%'false'+T+W%'false')),'C-Q6k=NOT_SHOWN A8.4w=REACHABLE_WITH_TRACE')
rec('A84 safety false trace',tag(x(T+S%'false'+T+W%'false')),'C-Q6k=false+trace A8.4w=REACHABLE_WITH_TRACE')
rec('A84 green + reachable witness',tag(x(S%'true'+T+W%'false')),'C-Q6k=true GREEN_NONVACUOUS_ELIGIBLE A8.4w=REACHABLE_WITH_TRACE')
rec('A84 green + untraced witness',tag(x(S%'true'+W%'false')),'C-Q6k=true GREEN_WITHHELD_non_vacuity_not_shown A8.4w=INCONCLUSIVE_non_vacuity_not_shown')
rec('A84 green + unreachable witness',tag(x(S%'true'+W%'true')),'C-Q6k=true GREEN_WITHHELD_non_vacuity_not_shown A8.4w=UNREACHABLE_prediction_falsified')
# set-scan helper
class A:
    def __init__(s):s.fail=[]
    def bad(s,m):s.fail.append(m)
def scan(text,allow):
    a=A();n['construct_scan'](a,'t',text,allow_sets=allow);return bool(a.fail)
rec('set scan: indented set rejected (lib)',scan('x.\n  set maxDepth = 1.\n',[]),True)
rec('set scan: tab/newline-split set rejected',scan('x.\n\tset\n maxDepth = 1.\n',[]),True)
rec('set scan: mid-line set rejected',scan('x. set maxDepth = 1.\n',[]),True)
rec('set scan: extra after allowed rejected',scan('set selFun = Term.\nset maxDepth = 1.\n',['set selFun = Term.']),True)
rec('set scan: indented allowed accepted',scan('  set   selFun =  Term.\n',['set selFun = Term.']),False)
rec('set scan: commented set ignored',scan('(* set maxDepth = 1. *)\n',[]),False)
(base/'helper-tests.json').write_text(json.dumps(res,indent=2)+'\n')
bad=[r['test'] for r in res if not r['ok']]
print('HELPER TESTS: %d total, %d passed, failures: %s'%(len(res),len(res)-len(bad),bad))
