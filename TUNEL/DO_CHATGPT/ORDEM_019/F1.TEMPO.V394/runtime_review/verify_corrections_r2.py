"""Verify only the reported runtime R1 defects in the additive R2 source."""
from pathlib import Path
import copy, hashlib, json, math, os, sys, time
from datetime import datetime, timezone
import numpy as np
from scipy.linalg import expm
HERE=Path(__file__).resolve().parent
UNIT=HERE.parent
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
paths=[UNIT/'runtime/time_runtime_v394_r2.py',UNIT/'physical_contract/physical_parameters.py']
before=[pin(p) for p in paths]
ns={}
for p in paths:exec(compile(p.read_bytes(),str(p),'exec'),ns)
def audit(event,args):
    if event in {'subprocess.Popen','os.system','socket.connect','socket.bind'}:raise RuntimeError('Forbidden '+event)
    if event=='open':
        p,mode,flags=args
        w=isinstance(mode,str) and any(c in mode for c in 'wax+')
        w=w or isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if w and isinstance(p,(str,bytes)) and not Path(os.fsdecode(p)).resolve().is_relative_to(HERE):raise RuntimeError('External write')
sys.addaudithook(audit)
t0=time.perf_counter();started=datetime.now(timezone.utc).isoformat()
alpha=7.2973525693e-3;hb=6.62607015e-34/(2*math.pi)
full=ns['v394_time_frequency_checks'](ns['v394_physical_parameters'],alpha,hb)
assert full['passed']
checks=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'ok':bool(ok),'detail':detail})
check('phase_extreme_representable',ns['_v394_clock_phase'](1e308,1e308)==.5)
for name,args in [('phase_infinite_output',(1.,5e-324)),('phase_underflow_output',(5e-324,1e308))]:
    try:ns['_v394_clock_phase'](*args)
    except ValueError as exc:check(name,True,str(exc))
    else:check(name,False)
ns['v394_time_frequency_checks']=lambda *args:{'passed':True,'scope':'admission-only mock'}
body='theorem mock : True := True.intro\n'
ns['_V394_FORMAL_CONTRACT']={'theorems':['Mock.theorem'],'source_sha256':{'Mock.lean':hashlib.sha256(body.encode()).hexdigest()},'expected_ladder':100}
ns['_V394_INSCRIPTIONS']={'mock':{'text':'fixture','sha256':hashlib.sha256(b'fixture').hexdigest()}}
ns['_EMBEDDED_KERNEL_FILES']={'Mock.lean':body}
ns['SEALED_CODATA_ALPHA']=alpha;ns['HBAR_EXACT']=hb
valid={'kernel_formalization':{'all_verified':True,'axiom_report':{'Mock.theorem':['propext']},'n_theorems_clean':100,'n_theorems_expected':100}}
check('complete_formal_mock_admitted',ns['tempo_frequencia_v394'](copy.deepcopy(valid))['all_verified'] is True)
for field in ('n_theorems_clean','n_theorems_expected'):
    for value in (None,True,99,101,100.,float('nan')):
        core=copy.deepcopy(valid)
        if value is None:del core['kernel_formalization'][field]
        else:core['kernel_formalization'][field]=value
        out=ns['tempo_frequencia_v394'](core)
        check('ladder_'+field+'_'+repr(value),out['all_verified'] is False and out['runtime_executed'] is False)
core=copy.deepcopy(valid);core['kernel_formalization']['axiom_report']['Mock.theorem']=[['propext']]
out=ns['tempo_frequencia_v394'](core)
check('nested_axiom_refused_without_typeerror',out['all_verified'] is False and out['runtime_executed'] is False)
for kind in ('source','inscription'):
    if kind=='source':ns['_EMBEDDED_KERNEL_FILES']['Mock.lean']=body+'x'
    else:
        ns['_EMBEDDED_KERNEL_FILES']['Mock.lean']=body
        ns['_V394_INSCRIPTIONS']['mock']['text']+='x'
    out=ns['tempo_frequencia_v394'](copy.deepcopy(valid))
    check(kind+'_mutation_refused',out['all_verified'] is False and out['runtime_executed'] is False)
assert all(c['ok'] for c in checks)
result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-t0,'sources':before,'sources_unchanged':[pin(p)==old for p,old in zip(paths,before)],
    'passed':True,'checks':checks,'full_synthetic':full,'scope':'R2 correction verification; formal report mocks test admission only; no Lean claims from mocks.'}
data=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False).encode()
with (HERE/'RUNTIME_R2_CORRECTION_REVIEW.json').open('xb') as f:f.write(data)
print(json.dumps({'result':pin(HERE/'RUNTIME_R2_CORRECTION_REVIEW.json'),'checks':len(checks),
    'runtime_checks':full['check_count'],'max_gkls':max(p['max_gkls_residual'] for p in full['parameter_cases'])},ensure_ascii=False))
