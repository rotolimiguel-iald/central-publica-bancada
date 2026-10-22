"""Read-only AST/pin auditor. Never imports or executes the reviewed package."""
from pathlib import Path
import ast, hashlib, json, os
from datetime import datetime, timezone
BASE=Path(__file__).parent
SOURCE=BASE.parent/'guard_wsl_integration_preparation'
checks=[]
def check(name,ok,detail=None):
 checks.append(dict(name=name,ok=bool(ok),detail=detail))
 if not ok:raise RuntimeError(name)
def pin(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def load(n):return json.loads((SOURCE/n).read_bytes())
def same(p,q):return all(pin(p)[k]==q[k] for k in ('bytes','sha256'))
def write(n,obj):
 p=BASE/n;data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():raise RuntimeError('Review output already exists')
 t=p.with_name(p.name+'.tmp');t.write_bytes(data)
 check('write_verify:'+n,t.read_bytes()==data);os.replace(t,p)
manifest=load('MANIFESTO_PREPARACAO_WSL.json')
contract=load('CONTRATO_WSL.json')
check('request_consistent',manifest['request_id']==contract['request_id']==load('IDENTIDADE_PREPARADA.json')['request_id'])
for q in manifest['artifacts']:check('manifest_pin:'+q['relative_path'],same(Path(q['path']),q))
for q in contract['local_pins']:check('contract_local_pin:'+q['relative_path'],same(SOURCE/q['relative_path'],q))
for q in contract['windows_pins']:check('windows_binary_pin:'+q['path'],same(Path(q['path']),q))
runtime=load('RUNTIME_READONLY_RECEIPT.json')
for q in contract['linux_pins']:
 r=next(x for x in runtime['linux_files'] if x['path']==q['path'])
 check('linux_documentary_pin:'+q['path'],all(r[k]==q[k] for k in ('bytes','sha256')),'Documentary match only; no WSL or fresh UNC read in this review')
for k in ('source','copy'):
 q=load('SOURCE_COPY_RECEIPT.json')[k];check('guard_copy:'+k,same(Path(q['path']),q))
check('byte_identical_guard',(SOURCE/'sources/audit_guard.py').read_bytes()==Path(load('SOURCE_COPY_RECEIPT.json')['source']['path']).read_bytes())
sources={};trees={}
for name in ('common.py','linux_control.py','launch_windows.py','worker.py','sources/audit_guard.py'):
 sources[name]=(SOURCE/name).read_text(encoding='utf-8-sig');trees[name]=ast.parse(sources[name]);check('AST:'+name,True)
 imports=sorted({(x.module or '').split('.')[0] for x in ast.walk(trees[name]) if isinstance(x,ast.ImportFrom)}|{a.name.split('.')[0] for x in ast.walk(trees[name]) if isinstance(x,ast.Import) for a in x.names})
 check('no_science_imports:'+name,not set(imports)&{'lal','lalsimulation','bilby','numpy','scipy','dynesty'},imports)
c=sources['common.py'];l=sources['linux_control.py'];w=sources['launch_windows.py'];worker=sources['worker.py']
for name,ok in [
 ('exclusive_fsync_readback_claim','open("xb")' in c and 'os.fsync' in c and 'Receipt readback' in c),
 ('specific_authorization',all(s in c for s in ['Specific authorization required','Authorization contract mismatch','Frozen limits','ROOT review absent','Wrong scope'])),
 ('claim_before_launch',w.index('g.fresh(BASE/"CLAIM.json"')<w.index('primary,pcap,pargv=launch')),
 ('claim_before_child',l.index('g.fresh(BASE/"RUN/LINUX_CLAIM.json"')<l.index('proc=subprocess.Popen')),
 ('case_claim_before_guard',worker.index('g.fresh(out/"CASE_CLAIM.json"')<worker.index('m=types.ModuleType("qualified_audit_guard")')),
 ('no_replay_entry','("CLAIM.json","RUN","RESULT.json")' in w),
 ('stop_before_cleanup',w.index('g.fresh(run/"STOP.json"')<w.index('cleaner,ccap,cargv=launch')),
 ('stop_inside_gate',l.index('fd=gate(g,work)')<l.index('"Fenced before Popen"')<l.index('proc=subprocess.Popen')),
 ('cleanup_same_gate','lockfd=gate(g,deadline)' in l),
 ('pidfd_before_identity_signal',c.index('fd=os.pidfd_open(pid,0)')<c.index('x=proc_identity(pid); need(matches(x,argv)')<c.index('signal.pidfd_send_signal')),
 ('same_uid_errors_visible','Cannot inspect same-UID process identity; cleanup uncertain' in c),
 ('exact_argv_exe','x["exe"]=="/usr/bin/python3.12" and x["argv"]==[s.encode() for s in argv]' in c),
 ('windows_owned_handles','proc.kill();proc.wait' in w),
 ('pidfd_preflight','ownfd=os.pidfd_open(os.getpid(),0);os.close(ownfd)' in l),
 ('success_zero_kills','and not cleanup["stopped"]' in w),
 ('uncertainty_label','UNCERTAIN_ORPHAN_STATE' in w and 'UNCERTAIN_CHILD_STATE' in l),
 ('linux_postreceipt_stdout_checks',l.index('g.fresh(BASE/"RUN/LINUX_RESULT.json",receipt)')<l.index('"Linux final IO exceeded nominal deadline"')<l.index('print(json.dumps(receipt,sort_keys=True),flush=True)')<l.index('"Terminal stdout exceeded Linux deadline"')),
 ('cleanup_postreceipt_stdout_checks',l.index('g.fresh(BASE/"RUN/CLEANUP_RESULT.json",result)')<l.index('print(json.dumps(result,sort_keys=True),flush=True)')<l.index('"Terminal stdout exceeded cleanup deadline"')),
 ('windows_postreceipt_stdout_checks',w.index('g.fresh(BASE/"RESULT.json",receipt)')<w.index('"Final IO exceeded nominal60s; invalidate provisional PASS"')<w.index('print(json.dumps(receipt,sort_keys=True),flush=True)')<w.index('"Terminal stdout IO exceeded nominal60s"')),
 ('explicit_external_acceptance','requires_external_exit0_and_total_deadline' in w),
 ('no_OS_hard_deadline',contract['limits']['OS_hard_deadline_guarantee'] is False),
 ('one_case_60s',contract['limits']['max_control_runs']==1 and contract['limits']['nominal_total_s']==60),
 ('no_retry_resume',contract['limits']['retry'] is False and contract['limits']['resume'] is False),
 ('windows_clip_before_extend','extend(raw[:room])' in w),
 ('linux_extend_before_cap',l.index('buffers[key.data].extend(chunk)')<l.index('g.need(len(buffers[key.data])<=32768')),
 ('no_broad_signal',not any(s in c+l+w for s in ['os.kill(', 'killpg(', 'pkill', 'taskkill', '--terminate'])),
 ('one_linux_control_Popen',sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='Popen' for x in ast.walk(trees['linux_control.py']))==1),
 ('worker_no_Popen',not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='Popen' for x in ast.walk(trees['worker.py']))),
]:check(name,ok)
cap=next(x for x in trees['launch_windows.py'].body if isinstance(x,ast.ClassDef) and x.name=='Capture')
read=next(x for x in cap.body if isinstance(x,ast.FunctionDef) and x.name=='read')
join=next(x for x in cap.body if isinstance(x,ast.FunctionDef) and x.name=='join')
check('WSL01_read_no_exception_transport',not any(isinstance(x,ast.Try) for x in ast.walk(read)),'Observed finding, not a passed behavioral control')
check('WSL01_join_only_thread_liveness','return not any(t.is_alive()' in ast.get_source_segment(w,join),'Observed finding')
for n in ('AUTORIZACAO_ROOT.json','CLAIM.json','RUN','RESULT.json'):check('absent:'+n,not (SOURCE/n).exists())
receipt=dict(status='STATIC_REVIEW_WITH_P2_FINDING_NOT_EXECUTED',created_utc=datetime.now(timezone.utc).isoformat(),request_id=contract['request_id'],map_before_seq=514,source_manifest=pin(SOURCE/'MANIFESTO_PREPARACAO_WSL.json'),contract=pin(SOURCE/'CONTRATO_WSL.json'),sources=[pin(SOURCE/n) for n in sources],check_count=len(checks),checks=checks,findings=['WSL-01','WSL-02'],scope='Independent lexical/AST/hash inspection; no candidate import, WSL, hook, control, scientific code, data D, authorization or claim. Linux14pins documentary-only against prior receipt; Windows3pins and local23manifest entries reread.',candidate_executions=0,wsl_invocations=0,candidate_imports=0,claims_created=0,authorizations_created=0)
write('RECIBO_REVISAO_ESTATICA.json',receipt)
print(json.dumps(dict(check_count=receipt['check_count'],source_manifest=receipt['source_manifest'],contract=receipt['contract'],receipt=pin(BASE/'RECIBO_REVISAO_ESTATICA.json')),ensure_ascii=False))
