"""Independent P3 static and pure-stub review. No scientific imports or execution."""
from pathlib import Path
import ast,copy,math,json,hashlib,datetime,os,types
from audit_provenance import atomic,metadata,OUT
base=OUT.parent/'preregistros'/'conjunto_d'/'p3_preparacao'
snap=OUT/'p3_review_snapshot'
c=json.loads((snap/'CONTRATO_P3.json').read_text());checks=[];sources=[]
def check(name,condition,detail=None):
 checks.append(dict(name=name,passed=bool(condition),detail=detail))
def rejects(name,fn,typ=Exception):
 try:fn()
 except typ as exc:check(name,True,str(exc))
 else:check(name,False,'No exception')
for row in json.loads((snap/'MANIFESTO_P3_PREPARADO.json').read_text())['files']:
 m,_=metadata(Path(row['path']));sources.append(m);check('manifest:'+row['relative_path'],m['sha256']==row['sha256'] and m['bytes']==row['bytes'])
for rel,pin in c['inputs'].items():
 m,_=metadata((base/rel).resolve());sources.append(m);check('contract:'+rel,m['sha256']==pin['sha256'] and m['bytes']==pin['bytes'])
r=json.loads((OUT/'REVISAO_P3_RUNTIME.json').read_text());check('1162_actual_runtime_pins',len(r['files'])==1162 and all(x['matches_pin'] for x in r['files']))
check('unique_runtime_paths',len({x['path'] for x in r['files']})==len(r['files']))
old=json.loads((base/'../piloto_sintetico/ENVIRONMENT_NATIVE_HASHES.json').resolve().read_text())
print('old runtime keys',list(old))
oldrows=old['files'];newrows={x['path']:x for x in r['files']}
check('165_original_pins_preserved',len(oldrows)==165 and all(x['path'] in newrows and newrows[x['path']]['sha256']==x['sha256'] for x in oldrows))
for fn in ['pseob_source.py','temporal_contract.py','synthetic_adapter_v2.py']:
 check('source_byte_identity:'+fn,(base/'src'/fn).read_bytes()==(base/'../piloto_sintetico/src'/fn).resolve().read_bytes())
rec=json.loads((base/c['qualified_result']).resolve().read_text())
for job in c['jobs']:
 inj=next(x for x in rec['injections'] if x['label']==job['label'])
 check('truth_normalization_chain:'+job['id'],job['truth']==inj['truth'] and job['normalization']==inj['normalization'])
check('noise_pair_not_independent',all(c['jobs'][0]['normalization'][d]['noise_sha256']==c['jobs'][1]['normalization'][d]['noise_sha256'] for d in ['H1','L1']) and c['noise']['independent_realizations'] is False)
ns={};tree=ast.parse((snap/'prior_transform.py').read_text());exec(compile(tree,'frozen_pure_prior','exec'),ns)
tr=ns['transform'];params=ns['parameters'];A=3477.5
check('exact_area_closed_form',(.5*(80**2-35**2)-20*(80-35))+60*(100-80)+(80*(110-100)-.1*(110**2-100**2))==A)
def cdf(m):
 if m<=80:return (.5*(m*m-35*35)-20*(m-35))/A
 if m<=100:return (1687.5+60*(m-80))/A
 return (2887.5+80*(m-100)-.1*(m*m-10000))/A
maxerr=0.;jacerr=0.
for u in [0.,.01,.05,.1,.2,.3,1687.5/A,.5,.6,.7,.8,2887.5/A,.85,.9,.95,.99,1.]:
 v=[.5]*12;v[0]=u;m=tr(v)[0];maxerr=max(maxerr,abs(cdf(m)-u))
 for q in [0.,.5,1.]:
  v[1]=q;p=params(tr(v));check('mass_support:'+str(u)+':'+str(q),35<=p['mass_1']<=110 and 20<=p['mass_2']<=80 and .2-1e-14<=p['mass_ratio']<=1+1e-14)
 if 1e-6<u<1-1e-6 and min(abs(m-80),abs(m-100))>1e-3:
  h=1e-7;v[0]=u-h;ml=tr(v)[0];v[0]=u+h;mr=tr(v)[0]
  jacerr=max(jacerr,abs((mr-ml)/(2*h)*(min(80,m)-max(20,.2*m))/A-1))
check('CDF_roundtrip_17',maxerr<1e-12,maxerr);check('joint_mass_jacobian',jacerr<2e-7,jacerr)
for u in [0.,.25,.5,.75,1.]:
 v=tr([u]*12);check('angle_CDF:'+str(u),abs((1-math.cos(v[6]))/2-u)<1e-14 and abs((1+math.sin(v[8]))/2-u)<1e-14)
check('coordinate_order_periodicity_fixed_zeros',list(ns['FREE'])==c['free_parameters'] and list(ns['PERIODIC'])==[7,9,10] and ns['FIXED']==c['fixed_parameters'])
for name,u in [('short',[.5]*11),('nan',[float('nan')]+[.5]*11),('inf',[float('inf')]+[.5]*11),('negative',[-.1]+[.5]*11),('above_one',[1.1]+[.5]*11)]:rejects('invalid_cube:'+name,lambda u=u:tr(u),ValueError)
# Execute only copied AST nodes budget/logl with arithmetic stand-ins. No actual likelihood object.
dtree=ast.parse((snap/'driver_p3.py').read_text());main=next(x for x in dtree.body if isinstance(x,ast.FunctionDef) and x.name=='main')
budget=next(x for x in ast.walk(main) if isinstance(x,ast.FunctionDef) and x.name=='budget')
logl=next(x for x in ast.walk(main) if isinstance(x,ast.FunctionDef) and x.name=='logl')
audit=next(x for x in ast.walk(main) if isinstance(x,ast.FunctionDef) and x.name=='audit')
factory=ast.parse('def make():\n ll_calls=0\n return None').body[0]
factory.body=[factory.body[0],copy.deepcopy(budget),copy.deepcopy(logl),ast.parse('return logl, lambda: ll_calls').body[0]]
class BudgetStop(RuntimeError):pass
class Clock:
 wall=0.;cpu=0.
 def perf_counter(self):return self.wall
 def process_time(self):return self.cpu
clock=Clock();counts=[0,0.,0]
class ArithmeticStandIn:
 calls=0;value=0.;error=None
 def log_likelihood_ratio(self,v):
  self.calls+=1
  if self.error:raise self.error
  counts[0]+=1
  return self.value
stub=ArithmeticStandIn()
env=dict(c=c,started=0.,time=clock,BudgetStop=BudgetStop,math=math,counts=counts,likelihood=stub,parameters=lambda v:v)
exec(compile(ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[])),'extracted_budget_logl','exec'),env)
f,total=env['make']()
for i in range(10000):f([0.]*12)
rejects('hard_10001_rejected_before_standin',lambda:f([0.]*12),BudgetStop)
check('exact_10000_including_initialization',total()==stub.calls==counts[0]==10000,dict(wrapper=total(),standin=stub.calls,native_standin=counts[0]))
for key,limit in [('wall',3600.),('cpu',3300.)]:
 clock.wall=clock.cpu=0.;setattr(clock,key,limit);ff,_=env['make']();rejects('budget_'+key,lambda:ff([0.]*12),BudgetStop)
clock.wall=clock.cpu=0.
for value in [float('nan'),float('inf'),-1.7976931348623157e308]:
 stub.value=value;ff,_=env['make']();rejects('nonfinite_or_sentinel_aborts:'+str(value),lambda:ff([0.]*12),RuntimeError)
stub.value=0.;stub.error=RuntimeError('Internal function call failed: Input domain error');counts[:]=[0,0.,0];ff,total=env['make']()
rejects('EDOM_exception_propagates',lambda:ff([0.]*12),RuntimeError)
check('EDOM_exception_count_is_zero_reproduced',counts[2]==0,dict(exception='Internal function call failed: Input domain error',EDOM=int(counts[2]),conclusion='P2: final report labels None-only count as EDOM'))
# Exact hook function called directly with artificial event arguments, never installed.
env2=dict(Path=Path,os=os,out=(OUT/'p3_mock_output').resolve(),allowed_data={str((OUT/'p3_mock_allowed.txt').resolve())},blocked=[],audit_paths=set())
exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(audit)],type_ignores=[])),'extracted_audit','exec'),env2)
a=env2['audit'];inside=env2['out']/'log.json';allowed=OUT/'p3_mock_allowed.txt';foreign=OUT/'p3_mock_foreign.txt'
a('open',(str(inside),'w',os.O_CREAT|os.O_WRONLY));a('open',(str(allowed),'r',os.O_RDONLY))
check('audit_accepts_registered_read_and_job_write',len(env2['audit_paths'])==2)
rejects('audit_foreign_read',lambda:a('open',(str(foreign),'r',os.O_RDONLY)),PermissionError)
rejects('audit_foreign_write',lambda:a('open',(str(foreign),'w',os.O_WRONLY)),PermissionError)
for event in ['socket.connect','socket.bind','subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn']:rejects('audit_'+event,lambda event=event:a(event,()),PermissionError)
check('still_no_authorization_or_execution',not (base/'EXECUTION_001').exists() and not (base/'AUTORIZACAO_COORDENACAO.json').exists())
check('no_scientific_imports',not any(x in __import__('sys').modules for x in ['bilby','lal','lalsimulation','dynesty','numpy']))
result=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='CONTROLS_COMPLETE_WITH_P2_REPORTING_FINDING',checks=checks,counts=dict(total=len(checks),passed=sum(x['passed'] for x in checks)),metrics=dict(mass_area=A,max_CDF_error=maxerr,max_relative_mass_jacobian_error=jacerr),source_metadata=sources,PE_jobs=0,native_waveforms=0,actual_likelihood_objects=0,original_scripts_executed=False,author_files_modified=False,scope='AST-extracted guards/stub controls are not execution or qualification of P3 scientific pipeline.')
atomic(OUT/'REVISAO_P3_CONTROLES.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','source_metadata']}))
print('FAILURES',json.dumps([x for x in checks if not x['passed']]))
