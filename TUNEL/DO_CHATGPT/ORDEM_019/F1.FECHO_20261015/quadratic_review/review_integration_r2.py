"""Static candidate comparison and selective runtime verification, never executes main."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,math,re,time
B=Path(__file__).resolve().parent
P=B.parent
IR=P/'INTEGRATION_QUADRATIC_R3.json'
OLD=P.parent/'F1.TEMPO.V394'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def put(p,v):
 raw=(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
start=now();tick=time.perf_counter()
i=load(IR)
for k in ['candidate','baseline','script','runtime','new_source']:assert sha(i[k]['path'])==i[k]['sha256'],k
candidate=Path(i['candidate']['path']);baseline=Path(i['baseline']['path'])
t1=ast.parse(baseline.read_text(encoding='utf-8'));t2=ast.parse(candidate.read_text(encoding='utf-8'))
def funcs(t):return {n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
def assigns(t):return {n.targets[0].id:n for n in t.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
f1,f2=funcs(t1),funcs(t2);a1,a2=assigns(t1),assigns(t2)
changed=sorted(k for k in f1 if k not in f2 or ast.dump(f1[k],include_attributes=False)!=ast.dump(f2[k],include_attributes=False))
added=sorted(set(f2)-set(f1));assert changed==i['changed_existing_functions']
assert added==['_v394_quadratic_residual','regra_quadratica_v394','v394_quadratic_checks']
changed_assign=sorted(k for k in a1 if k not in a2 or ast.dump(a1[k],include_attributes=False)!=ast.dump(a2[k],include_attributes=False))
lit=lambda d,n:ast.literal_eval(d[n].value)
e1,e2=lit(a1,'_EMBEDDED_KERNEL_FILES'),lit(a2,'_EMBEDDED_KERNEL_FILES')
assert set(e2)-set(e1)=={'TGLExt/RuleQuadraticResidual.lean'}
echanges=sorted(k for k in e1 if e1[k]!=e2[k]);assert echanges==['TGL/Audit.lean','TGLExt.lean']
assert e2['TGLExt/RuleQuadraticResidual.lean'].encode('utf-8')==Path(i['new_source']['path']).read_bytes()
for rel,text in e2.items():assert (candidate.parent/'tgl_kernel'/rel).read_bytes()==text.encode('utf-8'),rel
assert e2['TGLExt.lean']==e1['TGLExt.lean']+'\nimport TGLExt.RuleQuadraticResidual\n'
assert e2['TGL/Audit.lean']=='import TGLExt.RuleQuadraticResidual\n\n'+e1['TGL/Audit.lean']
flags1,flags2=lit(a1,'_LEAN_THEOREM_FLAGS'),lit(a2,'_LEAN_THEOREM_FLAGS')
assert all(flags2[k]==v for k,v in flags1.items())
assert {k:v for k,v in flags2.items() if k not in flags1}==i['new_flags']
c1,c2=lit(a1,'_V394_FORMAL_CONTRACT'),lit(a2,'_V394_FORMAL_CONTRACT')
assert c1['expected_ladder']==7153 and c2['expected_ladder']==7171
assert {k:v for k,v in c1.items() if k!='expected_ladder'}=={k:v for k,v in c2.items() if k!='expected_ladder'}
ins1,ins2=lit(a1,'_V394_INSCRIPTIONS'),lit(a2,'_V394_INSCRIPTIONS')
assert all(ins2[k]==v for k,v in ins1.items())
assert {k:v for k,v in ins2.items() if k not in ins1}==i['new_inscriptions']
for x in ins2.values():assert hashlib.sha256(x['text'].encode('utf-8')).hexdigest()==x['sha256']
rt=funcs(ast.parse(Path(i['runtime']['path']).read_text(encoding='utf-8')))
for name in added:assert ast.dump(f2[name],include_attributes=False)==ast.dump(rt[name],include_attributes=False)
maincalls={n.func.id:n.lineno for n in ast.walk(f2['main']) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['tempo_frequencia_v394','regra_quadratica_v394','emit_figures']}
assert maincalls['tempo_frequencia_v394']<maincalls['regra_quadratica_v394']<maincalls['emit_figures']
assert 'regra_quadratica_v394' in ast.unparse(f2['_v394_article_tex'])
# Actual read-only logs: old full audit plus independently compiled new declarations.
root_path=OLD/'formal_verified/ROOT_AUDIT.json';root=load(root_path)
review_path=B/'BUILD_REVIEW_R2.json';review=load(review_path)
assert root['passed'] and review['status']=='PASSA'
axioms={};logs=[]
def ingest(path):
 text=Path(path).read_text(encoding='utf-8')
 assert 'sorryAx' not in text and ': error:' not in text
 for name,items in re.findall(r"'(.+?)' depends on axioms: \[([^]]*)\]",text):
  value=[x.strip() for x in items.split(',') if x.strip()]
  assert name not in axioms or axioms[name]==value
  axioms[name]=value
 for name in re.findall(r"'(.+?)' does not depend on any axioms",text):axioms[name]=[]
 logs.append(pin(path))
for entry in root['results']:
 assert entry['exit_code']==0 and entry['passed']
 for key in ['source','stdout','stderr','olean']:
  assert sha(entry[key]['path'])==entry[key]['sha256']
 ingest(entry['stdout']['path'])
entry=review['builds'][0]
assert entry['exit_code']==0 and entry['passed']
ingest(entry['log']['path'])
trio={'propext','Classical.choice','Quot.sound'}
formal={'all_verified':bool(root['passed'] and entry['passed']),'axiom_report':axioms}
for flag,name in flags2.items():formal[flag]=name in axioms and set(axioms[name])<=trio
# Execute definitions and selected pure constants only. No import of um.py, no top-level main.
selected=[n for n in t2.body if isinstance(n,ast.FunctionDef) and (('v394' in n.name and n.name!='_v394_article_tex') or n.name=='prove_external_ladder')]
ns={'math':math,'__name__':'quadratic_independent_subset'}
for name in ['SEALED_CODATA_ALPHA','H_PLANCK_EXACT']:
 ns[name]=ast.literal_eval(a2[name].value)
exec(compile(ast.Module(body=[a2['HBAR_EXACT']],type_ignores=[]),str(candidate),'exec'),ns)
for name in ['_V394_FORMAL_CONTRACT','_V394_QUADRATIC_CONTRACT','_V394_INSCRIPTIONS','_EMBEDDED_KERNEL_FILES']:
 ns[name]=lit(a2,name)
exec(compile(ast.Module(body=selected,type_ignores=[]),str(candidate),'exec'),ns)
ladder=ns['prove_external_ladder'](1,formal)
core={'kernel_formalization':formal,'external_ladder':ladder}
clock=ns['tempo_frequencia_v394'](core)
result=ns['regra_quadratica_v394'](core)
assert ladder['n_theorems_clean']==ladder['n_theorems_expected']==7171
assert clock['all_verified'] and result['all_verified'] and result['runtime_executed']
controls=[]
def reject(label,change):
 case=copy.deepcopy(core);change(case)
 got=ns['regra_quadratica_v394'](case)
 ok=got['all_verified'] is False and got['runtime_executed'] is False
 controls.append({'name':label,'passed':ok,'verdict':got['verdict']});assert ok
name=ns['_V394_QUADRATIC_CONTRACT']['theorems'][0]
reject('missing_compiled_theorem',lambda c:c['kernel_formalization']['axiom_report'].pop(name))
reject('foreign_axiom',lambda c:c['kernel_formalization']['axiom_report'].__setitem__(name,['sorryAx']))
reject('formal_not_verified',lambda c:c['kernel_formalization'].__setitem__('all_verified',False))
reject('ladder_count_wrong',lambda c:c['external_ladder'].__setitem__('n_theorems_clean',7170))
reject('ladder_boolean',lambda c:c['external_ladder'].__setitem__('n_theorems_clean',True))
reject('time_dependency_not_verified',lambda c:c['tempo_frequencia_v394'].__setitem__('all_verified',False))
rel='TGLExt/RuleQuadraticResidual.lean';saved=ns['_EMBEDDED_KERNEL_FILES'][rel]
ns['_EMBEDDED_KERNEL_FILES'][rel]=saved+'\n-- mutation\n'
reject('embedded_source_mutation',lambda c:None)
ns['_EMBEDDED_KERNEL_FILES'][rel]=saved
assert sha(candidate)==i['candidate']['sha256'] and sha(baseline)==i['baseline']['sha256']
receipt={'unit':'F1.FECHO_20261015','claim_event':845,'status':'PASSA_COMPONENTE_INTEGRADO_AGUARDA_RITO_INTEGRAL','start_utc':start,'end_utc':now(),'seconds':time.perf_counter()-tick,'integration':pin(IR),'candidate':pin(candidate),'baseline':pin(baseline),'script':pin(__file__),'changed_functions':changed,'added_functions':added,'changed_assignments':changed_assign,'changed_embedded_old_sources':echanges,'all_materialized_1237_files_match_embedded':len(e2)==1237,'formal_evidence':[pin(root_path),pin(review_path)]+logs,'axiom_names_parsed':len(axioms),'ladder':{'clean':ladder['n_theorems_clean'],'expected':ladder['n_theorems_expected'],'all_verified':ladder['all_verified']},'time_dependency':clock,'quadratic_consumer':result,'refusal_controls':controls,'main_executed':False,'article_and_seal_rendered':False,'input_report_scope':'Merged actual prior root audit and independently compiled new module; selective pure-consumer test, not complete R3 rite.','originals_memory_production_gate_touched':False}
put(B/'INTEGRATION_REVIEW_R2.json',receipt)
print(json.dumps({'status':receipt['status'],'clock_checks':clock['runtime']['check_count'],'quadratic_checks':result['runtime']['check_count'],'refusals':len(controls),'sha256':sha(B/'INTEGRATION_REVIEW_R2.json')},ensure_ascii=False))
