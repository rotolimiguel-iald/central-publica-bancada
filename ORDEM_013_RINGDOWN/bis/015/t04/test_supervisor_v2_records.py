"""Pure record-validation controls; no process, model, or scientific run."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib,math,copy
D=Path(__file__).resolve().parent;p=D/'supervise_t04_v2.py'
tree=ast.parse(p.read_bytes());functions=[v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name in ('qualify_records','pilot_status')]
assert len(functions)==2
env={'math':math};exec(compile(ast.Module(body=functions,type_ignores=[]),str(p),'exec'),env)
items=[dict(label=f'draw{i}') for i in range(400)];lines=[]
for item in items:
    lines.extend([dict(precall=item['label']),dict(return_label=item['label'],status='FINITE_WAVEFORM',error=None,wall_seconds=.1)])
lines.append(dict(summary=True,source_calls=400,edom=0))
tests=[]
def check(name,value):
    assert value,name
    tests.append(dict(name=name,passed=True))
q=env['qualify_records'];s=env['pilot_status']
check('exact400accepted',q(lines,items)[0])
for name,change in [
 ('missing_pair',lambda x:x.pop(0)),('extra_line',lambda x:x.append(dict(precall='extra'))),
 ('wrong_precall',lambda x:x[0].update(precall='wrong')),
 ('wrong_return',lambda x:x[1].update(return_label='wrong')),
 ('nonfinite',lambda x:x[1].update(status='DOMAIN_RETURNED_NONE')),
 ('reported_error',lambda x:x[1].update(error={'type':'error'})),
 ('negative_time',lambda x:x[1].update(wall_seconds=-1)),
 ('nan_time',lambda x:x[1].update(wall_seconds=float('nan'))),
 ('bool_time',lambda x:x[1].update(wall_seconds=True)),
 ('source_calls',lambda x:x[-1].update(source_calls=399)),
 ('edom_count',lambda x:x[-1].update(edom=1)),
 ('missing_summary',lambda x:x[-1].update(summary=False))]:
    v=copy.deepcopy(lines);change(v);check(name,not q(v,items)[0])
v=copy.deepcopy(lines);v[0:4]=v[2:4]+v[0:2];check('order_changed',not q(v,items)[0])
v=copy.deepcopy(items);v[1]=v[0];check('duplicate_planned_label',not q(lines,v)[0])
cr=dict(registration_sha256='fixture',job='job',cleanup={'group_absent':True},status='CHILD_COMPLETED_REQUIRES_REVIEW')
check('pilot_requires_review_only_after_clean_success',s(0,None,False,cr,'fixture','job')==('T04_PILOT_FINISHED_REQUIRES_REVIEW',True))
check('no_receipt',s(0,None,False,None,'fixture','job')[1] is False)
for key,value in [('registration_sha256','wrong'),('job','other'),('cleanup',{'group_absent':False})]:
    v=copy.deepcopy(cr);v[key]=value;check('pilot_'+key,s(0,None,False,v,'fixture','job')[1] is False)
check('pilot_rc_error',s(2,None,False,cr,'fixture','job')[0]=='T04_FAILED_OR_PARTIAL_REQUIRES_BRANCH_REVIEW')
check('pilot_supervisor_error',s(0,{'error':'fixture'},False,cr,'fixture','job')[0]=='T04_FAILED_OR_PARTIAL_REQUIRES_BRANCH_REVIEW')
check('pilot_wall_stop',s(0,None,True,cr,'fixture','job')[0]=='T04_BUDGET_STOPPED_PARTIAL')
v=copy.deepcopy(cr);v['status']='PARTIAL_MAXCALL_NOT_ACCEPTED'
check('pilot_partial_status',s(0,None,False,v,'fixture','job')[0]=='T04_FAILED_OR_PARTIAL_REQUIRES_BRANCH_REVIEW')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='RECORD_VALIDATION_CONTROLS_PASSED',tests=tests,
    source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),scope='Two functions only; no supervisor lifecycle, native source or physical inference claimed',scientific_runs=0)
out=D/'SUPERVISOR_V2_RECORD_TESTS.json'
with out.open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps(dict(status=result['status'],controls=len(tests))))
