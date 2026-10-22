"""Independent pure recheck of the fixed P3 receipt delta; no scientific execution."""
import ast,copy,json,datetime,errno,inspect,math,types
from pathlib import Path
from audit_provenance import OUT,atomic,metadata
b=OUT.parent/'preregistros'/'conjunto_d'/'p3_preparacao';s=OUT/'p3_delta_snapshot';old=OUT/'p3_review_snapshot';checks=[]
def ck(n,c,d=None):checks.append(dict(name=n,passed=bool(c),detail=d))
c=json.loads((s/'CONTRATO_P3.json').read_text());o=json.loads((old/'CONTRATO_P3.json').read_text())
for x in json.loads((s/'MANIFESTO_P3_PREPARADO_V2.json').read_text())['files']:
 m,_=metadata(Path(x['path']));ck('manifest_v2:'+x['relative_path'],m['sha256']==x['sha256'] and m['bytes']==x['bytes'])
for rel,pin in c['inputs'].items():
 m,_=metadata((b/rel).resolve());ck('input_v2:'+rel,m['sha256']==pin['sha256'] and m['bytes']==pin['bytes'])
for key in ['jobs','priors','mass_prior_normalization','noise','grid','sampler','limits','convergence','data_rule','fixed_parameters','free_parameters','qualified_arrays','qualified_result','stop_rules']:
 ck('unchanged:'+key,c[key]==o[key])
for key,pin in o['inputs'].items():
 if key not in ['driver_p3.py']:ck('unchanged_input:'+key,c['inputs'][key]==pin)
ns={};exec(compile(ast.parse((s/'failure_audit.py').read_text()),'frozen_failure_audit','exec'),ns)
Audit=ns['FailureAudit'];Budget=ns['BudgetStop'];NoneError=ns['SourceReturnedNone'];params={'mass_1':50.,'mass_2':35.,'dtau220':-.4,'dtau440':0.,'domega220':0.,'domega440':0.}
cases=[('EDOM_text',RuntimeError('Internal function call failed: Input domain error'),True,'DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT'),('EDOM_errno',OSError(errno.EDOM,'bounded fake error'),True,'DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT'),('generic_after',RuntimeError('generic'),True,'EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT'),('generic_before',ValueError('invalid synthetic parameter'),False,'EXCEPTION_BEFORE_NATIVE_ATTEMPT'),('temporal',RuntimeError('WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION; widen registered segment'),False,'TEMPORAL_GUARD_BEFORE_NATIVE'),('budget_before',Budget('MAXCALL'),False,'BUDGET_STOP'),('budget_after',Budget('SIGNAL_14'),True,'BUDGET_STOP'),('deadline_before',TimeoutError('Source deadline reached'),False,'BUDGET_STOP'),('deadline_after',TimeoutError('Source deadline reached'),True,'EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT')]
metrics=[]
for name,exc,attempt,kind in cases:
 a=Audit();counter=[0,0.,0]
 def fail():
  if attempt:counter[0]+=1
  raise exc
 try:a.guard(fail,params,counter)
 except Exception as got:
  ck(name+':same_exception',got is exc);a.external(got,params);a.external(got,params)
 else:ck(name+':same_exception',False)
 ss=a.summary(counter);e=ss['events'][0]
 ck(name+':classification',a.kind_for(exc)==kind)
 ck(name+':dedup_and_evidence',len(ss['events'])==1 and e['parameters']==params and e['message']==str(exc) and e['native_attempts_before']==0 and e['native_attempts_after']==int(attempt))
 ck(name+':unknown_total',ss['domain_error_total'] is None)
 metrics.append(dict(case=name,kind=kind,recognized=ss['recognized_domain_exception_count']))
a=Audit();counter=[0,0.,0]
def none():counter[0]+=1;counter[2]+=1;return None
try:a.guard(none,params,counter)
except NoneError as got:a.external(got,params)
ss=a.summary(counter);ck('None_abort_separate_not_EDOM',len(ss['events'])==1 and ss['source_returned_none_count']==1 and ss['source_returned_none_counter_raw']==1 and ss['recognized_domain_exception_count']==0 and ss['domain_error_total'] is None)
a=Audit();counter=[0,0.,0];seen=[];token=object()
def bound(frequency,mass,dtau440=0.,**kwargs):seen.append((frequency,mass,dtau440,kwargs));counter[0]+=1;return token
wrapped=a.wrap(bound,lambda:params,counter);argument=object();returned=wrapped(argument,50.,dtau440=0.,domega220=0.,domega440=0.)
ck('signature_preserved',inspect.signature(wrapped)==inspect.signature(bound))
ck('forward_once_exact_args_return',returned is token and len(seen)==1 and seen[0][0] is argument and seen[0][1:]==(50.,0.,{'domega220':0.,'domega440':0.}) and counter[0]==1)
ck('success_no_failure_events',not a.summary(counter)['events'])
# Exercise exactly the outer handlers as copied AST, with pre-recorded source errors.
t=ast.parse((s/'driver_p3.py').read_text());main=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='main');outer=next(x for x in main.body if isinstance(x,ast.Try))
trial=ast.Try(body=[ast.Raise(exc=ast.Name(id='exc',ctx=ast.Load()))],handlers=copy.deepcopy(outer.handlers),orelse=[],finalbody=[])
for name,exc,attempt,kind in cases:
 fa=Audit();before=[0,0.,0];after=[int(attempt),0.,0];fa._record(fa.classify(exc,before,after),exc,params,before,after)
 env={'exc':exc,'BudgetStop':Budget,'failures':fa,'last_parameters':params}
 exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(trial)],type_ignores=[])),'exact_outer_handlers','exec'),env)
 expected='BUDGET_EXHAUSTED_PARTIAL' if kind=='BUDGET_STOP' else 'FAILED'
 ck('handler:'+name,env['status']==expected and len(fa.events)==1)
# Delta preserved the budget AST; verify boundary through changed logl with arithmetic stand-in.
ob=next(x for x in ast.walk(ast.parse((old/'driver_p3.py').read_text())) if isinstance(x,ast.FunctionDef) and x.name=='budget');nb=next(x for x in ast.walk(main) if isinstance(x,ast.FunctionDef) and x.name=='budget')
ck('budget_AST_identical',ast.dump(ob)==ast.dump(nb))
nl=next(x for x in ast.walk(main) if isinstance(x,ast.FunctionDef) and x.name=='logl');fac=ast.parse('def make():\n ll_calls=9999\n last_parameters=None\n return None').body[0];fac.body=fac.body[:2]+[copy.deepcopy(nb),copy.deepcopy(nl),ast.parse('return logl, lambda: ll_calls').body[0]]
class Fake:
 calls=0
 def log_likelihood_ratio(self,v):self.calls+=1;return 0.
fake=Fake();en={'c':c,'BudgetStop':Budget,'time':types.SimpleNamespace(perf_counter=lambda:0.,process_time=lambda:0.),'started':0.,'likelihood':fake,'parameters':lambda v:params.copy(),'counts':[0,0.,0],'math':math}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fac],type_ignores=[])),'delta_budget_boundary','exec'),en);f,n=en['make']();f(None)
try:f(None)
except Budget:stopped=True
else:stopped=False
ck('changed_wrapper_stops_10001',n()==10000 and fake.calls==1 and stopped)
argv=json.loads((s/'COMANDO_EXATO_NAO_EXECUTADO.json').read_text())['argv'];ch=metadata(b/'CONTRATO_P3.json')[0]['sha256'];ck('exact_launch_current_contract',argv[-1]==ch and argv[-2].endswith('/launch_p3.py'))
ck('still_no_auth_no_execution',not (b/'AUTORIZACAO_COORDENACAO.json').exists() and not (b/'EXECUTION_001').exists())
ck('no_scientific_modules',not any(x in __import__('sys').modules for x in ['numpy','lal','lalsimulation','bilby','dynesty']))
r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'P3_01_RESOLVED_BY_PURE_DELTA_REVIEW','checks':checks,'count':len(checks),'passed':sum(x['passed'] for x in checks),'cases':metrics,'command_checked_not_executed':argv,'contract_sha256_read':ch,'PE_jobs':0,'native_waveforms':0,'scientific_likelihood_objects':0,'original_scripts_executed':False}
atomic(OUT/'REVISAO_P3_DELTA_RESULT.json',json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['checks','cases','command_checked_not_executed']}));print(json.dumps([x for x in checks if not x['passed']]))
