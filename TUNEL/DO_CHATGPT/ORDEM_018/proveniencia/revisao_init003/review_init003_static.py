"""Independent static/hash review of INIT003. Never imports or runs author code."""
from pathlib import Path
import ast,difflib,hashlib,json,sys
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent))
from audit_provenance import atomic,metadata
ROOT=OUT.parents[1]; BASE=ROOT/'preregistros/conjunto_d'
P=BASE/'p3_init_qualified_003'; OLD=BASE/'p3_codec_002'; QUAL=BASE/'p3_init_preparation'
checks=[];sources={}
def read(p):
 p=Path(p).resolve();m,b=metadata(p);sources[str(p)]=m;return b
def jr(p):return json.loads(read(p))
def check(n,ok,detail=None):
 checks.append({'name':n,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError(n)
def pin(p,r,label):
 b=read(p);check(label,len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'])
manifest=jr(P/'MANIFESTO_PACOTE_INIT003.json'); c=jr(P/'CONTRATO_P3.json'); old=jr(OLD/'CONTRATO_P3.json')
for row in manifest['files']:pin(row['path'],row,'manifest:'+Path(row['path']).name)
for rel,row in c['inputs'].items():pin(P/rel,row,'input:'+rel)
check('inputs_count',len(c['inputs'])==26)
copies=jr(P/'COPIAS_EXATAS.json')['copies']
for row in copies:
 for side in ['source','destination']:pin(row[side]['path'],row[side],'copy_pin:'+side+':'+Path(row[side]['path']).name)
 check('copy_bytes:'+Path(row['destination']['path']).name,read(row['source']['path'])==read(row['destination']['path']))
cmp=jr(P/'COMPARACAO_ESCOPO.json')
check('fields_count_corrected473',len(cmp['same_contract_fields'])==21)
for field in cmp['same_contract_fields']:check('same_contract_field:'+field,c[field]==old[field])
check('jobs_only_ids_changed',[{k:v for k,v in j.items() if k!='id'} for j in c['jobs']]==[{k:v for k,v in j.items() if k!='id'} for j in old['jobs']])
newids=[j['id'] for j in c['jobs']]
check('new_job_ids',newids==['P3_GR_INIT_QUALIFIED_003','P3_RB_INIT_QUALIFIED_003'] and not set(newids)&set(c['derived_from_failed_CODEC002']['old_jobs']+c['derived_from_failed_V2']['old_jobs']))
check('new_execution_directory',c['execution_directory']=='EXECUTION_INIT_QUALIFIED_003')
for n in [c['execution_directory'],'AUTORIZACAO_COORDENACAO.json','CLAIM.json','CHILD_STARTED.json']:
 check('absent:'+n,not(P/n).exists())
check('no_nested_claim',not list(P.rglob('CLAIM.json')))
check('state_prepared',c['state']=='PREPARED_NOT_EXECUTED')
command=jr(P/'COMANDO_EXATO_NAO_EXECUTADO.json')
check('command_pinned',command['argv'][-1]==hashlib.sha256(read(P/'CONTRATO_P3.json')).hexdigest() and command['argv'][-2].endswith('/p3_init_qualified_003/launch_p3.py'))
driver=read(P/'driver_p3.py').decode(); odriver=read(OLD/'driver_p3.py').decode()
actual_diff=''.join(difflib.unified_diff(odriver.splitlines(True),driver.splitlines(True),fromfile='frozen_p3_codec_002/driver_p3.py',tofile='p3_init_qualified_003/driver_p3.py'))
check('driver_patch_exact',actual_diff==read(P/'DELTA_DRIVER_VS_CODEC002.patch').decode())
ct=read(P/'CONTRATO_P3.json').decode();ot=read(OLD/'CONTRATO_P3.json').decode()
contract_diff=''.join(difflib.unified_diff(ot.splitlines(True),ct.splitlines(True),fromfile='frozen_p3_codec_002/CONTRATO_P3.json',tofile='p3_init_qualified_003/CONTRATO_P3.json'))
check('contract_patch_exact',contract_diff==read(P/'DELTA_CONTRATO_VS_CODEC002.patch').decode())
tree=ast.parse(driver);check('driver_AST',True)
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
check('one_B_no_A',sum(isinstance(n.func,ast.Name) and n.func.id=='build_B' for n in calls)==1 and not any(isinstance(n.func,ast.Name) and n.func.id=='build_A' for n in calls))
check('no_control_guard_or_shim',all(t not in driver for t in ['def deny','__signature__','setattr(W,','setattr(L,','source_attempts','likelihood_evaluation_attempts']))
check('generator_before_original_wrapper',driver.index('wf=generator(cfg)')<driver.index('wf.frequency_domain_source_model=failures.wrap(')<driver.index('likelihood=bilby.gw.likelihood.GravitationalWaveTransient'))
check('checks_before_after_GWT',driver.index('initialization_before.append(verify_analytic_state')<driver.index('likelihood=bilby.gw.likelihood.GravitationalWaveTransient')<driver.index('initialization_after=[verify_analytic_state'))
check('budget_before_every_LL',driver.index('budget();ll_calls+=1')<driver.index('value=float(likelihood.log_likelihood_ratio(last_parameters))'))
check('same_supervisor',read(P/'launch_p3.py')==read(OLD/'launch_p3.py'))
dep=jr(P/'DEPENDENCIA_FACTORY_PIN.json')
check('single_exact_ASD',dep['runtime_path']=='/opt/lal_env/lib/python3.12/site-packages/bilby/gw/detector/noise_curves/aLIGO_O4_high_asd.txt')
pin(P/dep['local_path'],dep,'ASD_snapshot')
for n in ['init_detectors.py','GEOMETRIA_PINADA.json','DEPENDENCIA_FACTORY_PIN.json']:
 check('qualified_copy:'+n,read(P/n)==read(QUAL/n))
for n in ['src/pseob_source.py','src/synthetic_adapter_v2.py','src/temporal_contract.py','prior_transform.py','failure_audit.py','preload_npz_codec.py','CONFIG_SYNTHETIC.json']:
 check('science_source_unchanged:'+n,read(P/n)==read(OLD/n))
qmanifest=jr(QUAL/'MANIFESTO_RESULTADO_INIT.json')
for row in qmanifest['files']:pin(row['path'],row,'qualification465:'+Path(row['path']).name)
qr=jr(QUAL/'CONTROL_INIT_001/RESULT.json'); qs=jr(QUAL/'CONTROL_INIT_SUPERVISION_001/SUPERVISION_RESULT.json')
check('qualified465_terminal',qr['status']=='INITIALIZATION_ONLY_PASS' and qs['status']=='SUPERVISED_INITIALIZATION_ONLY_PASS' and qs['returncode']==0 and qs['child_calls']==1)
check('qualified465_same_two_labels',[r['synthetic_label'] for r in qr['rows']]==[j['label'] for j in c['jobs']])
check('qualified465_zero_science',not any(qr['counters'].values()) and qr['source_native_counter']==[0,0.,0] and qr['blocked_operations']==[] and qr['permission_for_P3'] is False)
for n in ['contract','terminal_receipt']:
 row=c['derived_from_failed_CODEC002'][n];pin(row['path'],row,'terminal_old:'+n)
runtime=jr(P/'RUNTIME_P3_READONLY.json')
rrows={r['path']:r for r in runtime['files']}
for name in ['INTERPRETER_PIN.json','CODEC_CP437_PIN.json','DEPENDENCIA_FACTORY_PIN.json']:
 row=jr(P/name); path=row.get('path',row.get('runtime_path'));rrows[path]=row
vr=jr(P/'VERIFICACAO_RUNTIME_INIT003.json')
check('runtime_receipt_count',len(vr['checks'])==1165 and all(x['passed'] for x in vr['checks']))
check('runtime_receipt_pins',[ (x['actual']['sha256'],x['actual']['bytes']) for x in vr['checks'] ]==[(rrows[x['path']]['sha256'],rrows[x['path']]['bytes']) for x in vr['checks']])
wfg=QUAL/'sources/gw/waveform_generator.py';wb=read(wfg)
wrow=next(r for r in runtime['files'] if r['path'].endswith('/bilby/gw/waveform_generator.py'))
pin(wfg,wrow,'WFG_snapshot_runtime_match')
wt=ast.parse(wb.decode()); wc=next(x for x in wt.body if isinstance(x,ast.ClassDef) and x.name=='WaveformGenerator')
wi=next(x for x in wc.body if isinstance(x,ast.FunctionDef) and x.name=='__init__')
attrs=[(n.lineno,n.targets[0].attr) for n in ast.walk(wi) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Attribute)]
alines={k:line for line,k in attrs}
check('WFG_original_inference_order',alines['frequency_domain_source_model']<alines['source_parameter_keys'])
check('WFG_source_attr_not_descriptor',not any(isinstance(n,ast.FunctionDef) and n.name=='frequency_domain_source_model' for n in wc.body))
snap=OUT/'snapshot';snap.mkdir(exist_ok=True)
for name in ['MANIFESTO_PACOTE_INIT003.json','CONTRATO_P3.json','driver_p3.py','launch_p3.py','DELTA_DRIVER_VS_CODEC002.patch','DELTA_CONTRATO_VS_CODEC002.patch']:
 raw=read(P/name); target=snap/name
 if target.exists():check('snapshot_same:'+name,target.read_bytes()==raw)
 else:atomic(target,raw)
record={'status':'STATIC_REVIEW_NO_NEW_ACTIONABLE_FINDING','at':datetime.now(timezone.utc).isoformat(),
 'checks_count':len(checks),'checks':checks,'sources':list(sources.values()),
 'manifest_files':len(manifest['files']),'exact_copies':len(copies),'science_fields_unchanged':len(cmp['same_contract_fields']),
 'new_job_ids':newids,'findings':[],
 'inherited_limit':'Supervisor wait3610s per child; SIGKILL followed by unbounded wait. 7220s is sum of nominal waits, not absolute OS campaign/cleanup/parent IO deadline.',
 'runtime_scope':'Author read-only receipt1165 checked by local hash/schema/pin matching; installed WSL files not rehashed by this review.',
 'qualified465_scope':'Read-only audit of existing receipts; no rerun, no transfer of initialization pass to PE/convergence.',
 'author_code_imported_or_executed':False,'control_or_P3_run':False,'scientific_arrays_deserialized':False,'D_read':False,'network':False,'originals_modified':False}
atomic(OUT/'RECIBO_REVISAO_INIT003.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'manifest_files':len(manifest['files']),'copies':len(copies),'sources':len(sources),'status':record['status']}))
