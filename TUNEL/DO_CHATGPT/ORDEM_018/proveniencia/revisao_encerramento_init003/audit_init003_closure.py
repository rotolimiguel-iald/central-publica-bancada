"""Read-only receipt/static audit; no scientific import, array deserialization or execution."""
from pathlib import Path
import ast,json,hashlib,sys
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parent))
from audit_provenance import atomic,metadata
ROOT=OUT.parents[1];P=ROOT/'preregistros/conjunto_d/p3_init_qualified_003';E=P/'EXECUTION_INIT_QUALIFIED_003'
checks=[];sources={}
def read(path):
 path=Path(path).resolve();m,b=metadata(path);sources[str(path)]=m;return b
def jr(path):return json.loads(read(path))
def check(name,ok):
 checks.append({'name':name,'passed':bool(ok)})
 if not ok:raise AssertionError(name)
def pin(path,row,name):
 b=read(path);check(name,len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
root=jr(P/'RECIBO_ROOT_ENCERRAMENTO_INIT003.json')
for row in root['files']:pin(row['path'],row,'ROOT_receipt_pin:'+str(Path(row['path']).relative_to(P)))
manifest=jr(P/'MANIFESTO_PACOTE_INIT003.json')
for row in manifest['files']:pin(row['path'],row,'consumed_package_pin:'+Path(row['path']).name)
c=jr(P/'CONTRATO_P3.json');cp=hashlib.sha256(read(P/'CONTRATO_P3.json')).hexdigest()
a=jr(P/'AUTORIZACAO_COORDENACAO.json');launch=jr(E/'LAUNCH_STARTED.json');campaign=jr(E/'CAMPAIGN_RECEIPT.json')
check('launch_authorization_pin',launch['authorization_sha256']==hashlib.sha256(read(P/'AUTORIZACAO_COORDENACAO.json')).hexdigest())
check('authorization_contract_jobs',a['authorized'] is True and a['contract_sha256']==cp and a['jobs']==[j['id'] for j in c['jobs']])
check('campaign_contract',campaign['contract_sha256']==launch['contract_sha256']==cp)
check('one_campaign_two_serial_children',campaign['started_jobs']==campaign['planned_jobs']==2 and [j['job_id'] for j in campaign['jobs']]==a['jobs'])
grdir=E/a['jobs'][0]; rbdir=E/a['jobs'][1]
gr=jr(grdir/'RESULT.json');gp=jr(grdir/'PROCESS_RECEIPT.json');rp=jr(rbdir/'PROCESS_RECEIPT.json')
for i,job in enumerate(c['jobs']):
 p=E/job['id']; claim=jr(p/'CLAIM.json');child=jr(p/'CHILD_STARTED.json');process=jr(p/'PROCESS_RECEIPT.json')
 check('claim:'+job['id'],claim=={'contract_sha256':cp,'job_id':job['id']})
 check('child_identity:'+job['id'],child['contract_sha256']==cp and child['job_id']==job['id'])
 check('campaign_process_match:'+job['id'],process==campaign['jobs'][i])
 for name in ['stdout','stderr']:check('process_log_pin:'+job['id']+':'+name,hashlib.sha256(read(p/(name+'.log'))).hexdigest()==process[name+'_sha256'])
check('GR_result_hash',hashlib.sha256(read(grdir/'RESULT.json')).hexdigest()==gp['result_sha256'])
check('GR_contract_identity',gr['contract_sha256']==cp and gr['job_id']==a['jobs'][0] and gr['label']=='GR_GAUSS')
check('GR_STOPPED_NOT_CONVERGED',gr['status']==gp['result_status']=='STOPPED_NOT_CONVERGED' and gp['returncode']==0)
check('GR_delta_ESS_not_converged',gr['delta_logz_before_live_addition']>.1 and gr['weighted_ESS'] is None)
check('GR_counts_under_cap',gr['likelihood_calls']==gr['native_calls']==9738 and gr['likelihood_calls']<c['limits']['max_likelihood_calls'])
check('GR_time_under_limits',gr['wall_s']<c['limits']['wall_soft_s'] and gr['cpu_process_total_s']<c['limits']['cpu_hard_s'] and gp['wall_s']<c['limits']['supervisor_wall_s'])
check('GR_five_cache_denials',len(gr['blocked_operations'])==5 and all('/UNUSED_BYTECODE_CACHE/' in p and p.endswith('.pyc') for p in gr['blocked_operations']))
check('GR_domain_total_unclaimed',gr['failure_receipt']['domain_error_total'] is None and not gr['failure_receipt']['events'])
check('GR_init_PSD_equal',gr['initialization_qualified'] is True and gr['initialization_analytic_after_likelihood']==gr['initialization_analytic_before_likelihood'])
for key in ['wall_s','CPU_s','likelihood_calls','native_calls','native_wall_s','delta_logz','weighted_ESS']:
 source={'CPU_s':'cpu_s','delta_logz':'delta_logz_before_live_addition'}.get(key,key)
 check('root_GR_consistency:'+key,root['GR_'+key]==gr[source])
check('root_GR_denials_equal',root['GR_blocked_operations']==gr['blocked_operations'])
check('root_campaign_wall_equal',root['campaign_wall_s']==campaign['wall_s'])
rbchild=jr(rbdir/'CHILD_STARTED.json')
check('RB_identity_matches_ROOT',rbchild['pid']==root['ROOT_action']['PID']==4721 and rbchild['job_id']==root['ROOT_action']['target_job'])
check('RB_return_minus_SIGTERM',rp['returncode']==root['ROOT_action']['native_process_returncode']==-15)
check('RB_no_final_RESULT',not (rbdir/'RESULT.json').exists() and 'result_status' not in rp)
progress=sorted(rbdir.glob('PROGRESS_*.json')); last=jr(progress[-1])
check('RB_last_progress_identity',progress[-1].name=='PROGRESS_0000400.json' and last==root['RB_last_progress']['state'])
check('RB_last_progress_not_final',last['iteration']==400 and last['calls']==last['native_calls']==1173 and last['wall_s']<rp['wall_s'])
driver=read(P/'driver_p3.py').decode();supervisor=read(P/'launch_p3.py').decode();dast=ast.parse(driver)
logl=next(n for n in ast.walk(dast) if isinstance(n,ast.FunctionDef) and n.name=='logl')
budget=next(n for n in ast.walk(dast) if isinstance(n,ast.FunctionDef) and n.name=='budget')
check('evidence_logl_no_blocked_guard',not any(isinstance(n,ast.Name) and n.id=='blocked' for n in ast.walk(logl)))
check('evidence_budget_no_blocked_guard',not any(isinstance(n,ast.Name) and n.id=='blocked' for n in ast.walk(budget)))
check('evidence_initial_guard_only',driver.count('if blocked:')==1)
check('evidence_supervisor_no_blocked_read','blocked_operations' not in supervisor)
check('evidence_supervisor_partial_accepted','\"STOPPED_NOT_CONVERGED\"' in supervisor and 'row.get(\"result_status\") not in' in supervisor)
check('evidence_no_exit_propagation','sys.exit(main())' not in supervisor)
snapshot=OUT/'snapshot';snapshot.mkdir(exist_ok=True)
for path in [P/'RECIBO_ROOT_ENCERRAMENTO_INIT003.json',E/'CAMPAIGN_RECEIPT.json',grdir/'RESULT.json',gp_path if False else grdir/'PROCESS_RECEIPT.json',rbdir/'PROCESS_RECEIPT.json',progress[-1]]:
 name=path.name if path.parent in [P,E] else path.parent.name+'__'+path.name
 atomic(snapshot/name,read(path))
findings=[
 {'id':'INIT003-END-01','priority':'P2','status':'OPEN_REPAIR_NOT_IMPLEMENTED','title':'Driver does not honor latched audit denials during/after sampling',
  'locations':['driver_p3.py:84-96','driver_p3.py:137-145','driver_p3.py:184-199'],
  'evidence':'Hook appends blocked and raises PermissionError; initialization tests the list once. Library can catch the error later. logl/budget never re-test blocked; final result serializes it but keeps partial/success status.',
  'minimum_design':'Sticky audit violation, checked before/after each likelihood and before accepting partial/result. If strict no-native-after-denial is required, check after deferred imports and before native call; logl postcheck alone can permit the in-flight call. Separate audit-failure classification; never infer EDOM or silently prior-reject.'},
 {'id':'INIT003-END-02','priority':'P2','status':'OPEN_REPAIR_NOT_IMPLEMENTED','title':'Supervisor advances on partial status without audit-validating child result',
  'locations':['launch_p3.py:47-55'],
  'evidence':'Only status/returncode are used; GR blocked_operations length5 was ignored and RB claimed/launched. main returns no status, yielding exit0 after terminal RB -15.',
  'minimum_design':'Validate exact result job/contract, audit state and budget counters before continuation; missing/malformed/violating receipt means terminal no retry. Write explicit campaign disposition and nonzero process exit for terminal failure. Partial/converged/recovery accepted are different axes.'}]
receipt={'status':'TERMINAL_AUDIT_STOP_RULE_FAILURE_CONFIRMED','at':datetime.now(timezone.utc).isoformat(),
 'checks_count':len(checks),'checks':checks,'sources':list(sources.values()),'findings':findings,
 'GR':{k:gr[k] for k in ['status','wall_s','cpu_s','cpu_process_total_s','likelihood_calls','native_calls','native_wall_s','delta_logz_before_live_addition','weighted_ESS','blocked_operations']},
 'RB':{'returncode':rp['returncode'],'supervisor_wall_s':rp['wall_s'],'final_likelihood_calls':None,'final_native_calls':None,'final_cpu_s':None,'last_completed_progress':last},
 'campaign_wall_s':campaign['wall_s'],
 'denial_classification':'Recorded paths are cache .pyc probes. Hook denied operation; no evidence here of successful unallowlisted read, exfiltration, D or physical/domain failure. Exact event mode/timestamp/call index not in original blocked strings.',
 'signal_provenance':'ROOT receipt attests pre-signal driver/job/contract/PGID check and SIGTERM. Child PID/job/contract and process return -15 are cross-checked. Historical process-group inspection not independently reproduced.',
 'diagnostic_archive_access':'Bytes/SHA256 only; no NPZ deserialization or inference.',
 'no_control_or_PE_execution':True,'no_native_imports':True,'no_network':True,'author_package_modified':False,'new_authorization':False}
atomic(OUT/'RECIBO_REVISAO_ENCERRAMENTO_INIT003.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'sources':len(sources),'status':receipt['status'],'findings':[x['id'] for x in findings]}))
