"""Independent static delta auditor; candidate modules are data only."""
import ast, hashlib, json, os, copy
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).parent
OLD=BASE.parent/'guard_wsl_integration_preparation'
NEW=BASE.parent/'guard_wsl_integration_preparation_v2'
REVIEW=BASE.parent/'revisao_guard_wsl_estatica'
checks=[]
def pin(p):
 raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def check(name,ok,detail=None):
 checks.append({'name':name,'ok':bool(ok),'detail':detail})
 if not ok:raise RuntimeError(name)
def same(p,q):
 actual=pin(p);return all(actual[k]==q[k] for k in ('bytes','sha256'))
def persist(name,obj):
 p=BASE/name;raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();assert not p.exists()
 t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;os.replace(t,p)
def dump(tree):return ast.dump(tree,include_attributes=False)
def norm(text):return text.replace('guard_wsl_integration_preparation_v2','guard_wsl_integration_preparation')
for directory,name in [(OLD,'MANIFESTO_PREPARACAO_WSL.json'),(NEW,'MANIFESTO_PREPARACAO_WSL_V2.json'),(REVIEW,'MANIFESTO_REVISAO_WSL.json')]:
 for q in read(directory/name)['artifacts']:check('manifest:'+directory.name+'/'+Path(q['path']).name,same(Path(q['path']),q))
a=read(OLD/'CONTRATO_WSL.json');b=read(NEW/'CONTRATO_WSL.json')
for q in b['local_pins']:check('V2localpin:'+q['relative_path'],same(NEW/q['relative_path'],q))
for q in b['windows_pins']:check('Windowspin:'+q['path'],same(Path(q['path']),q))
r=read(NEW/'RUNTIME_READONLY_RECEIPT.json')
for q in b['linux_pins']:
 row=next(x for x in r['linux_files'] if x['path']==q['path']);check('Linuxdocumentarypin:'+q['path'],all(row[k]==q[k] for k in ('bytes','sha256')),'No WSL/UNC runtime reread')
for k in a:
 if k not in ('schema','local_pins','acceptance'):check('contract_preserved:'+k,a[k]==b[k])
check('only_intended_contract_keys',set(b)==set(a)|{'revision'})
check('acceptance_additive',b['acceptance']['required'][:-1]==a['acceptance']['required'] and b['acceptance']['failure']==a['acceptance']['failure'] and b['acceptance']['not_proved']==a['acceptance']['not_proved'])
check('unchanged_identity_bytes',(OLD/'IDENTIDADE_PREPARADA.json').read_bytes()==(NEW/'IDENTIDADE_PREPARADA.json').read_bytes())
check('unchanged_guard_bytes',(OLD/'sources/audit_guard.py').read_bytes()==(NEW/'sources/audit_guard.py').read_bytes())
check('unchanged_runtime_document',(OLD/'RUNTIME_READONLY_RECEIPT.json').read_bytes()==(NEW/'RUNTIME_READONLY_RECEIPT.json').read_bytes())
oldtext={};newtext={};trees={}
for name in ['common.py','worker.py','linux_control.py','launch_windows.py']:
 oldtext[name]=(OLD/name).read_text(encoding='utf-8-sig');newtext[name]=(NEW/name).read_text(encoding='utf-8-sig');trees[name]=ast.parse(newtext[name]);check('AST:'+name,True)
 imports={q.name.split('.')[0] for x in ast.walk(trees[name]) if isinstance(x,ast.Import) for q in x.names}|{(x.module or '').split('.')[0] for x in ast.walk(trees[name]) if isinstance(x,ast.ImportFrom)}
 check('no_scientific_imports:'+name,not imports&{'numpy','lal','lalsimulation','bilby','dynesty','scipy'},sorted(imports))
 check('fixed_rebase_present:'+name,'guard_wsl_integration_preparation_v2' in newtext[name])
for name in ['common.py','worker.py']:check('byte_text_identical_except_rebase:'+name,norm(newtext[name])==oldtext[name])
old_capture='                buffers[key.data].extend(chunk)\n                g.need(len(buffers[key.data])<=32768,"Child output overflow")'
new_capture='                room=32768-len(buffers[key.data])\n                buffers[key.data].extend(chunk[:room])\n                g.need(len(chunk)<=room,"Child output overflow")'
check('linux_only_clip_delta',norm(newtext['linux_control.py']).replace(new_capture,old_capture)==oldtext['linux_control.py'])
# Compare complete Windows AST excluding the intended Capture/wait delta and added receipt field.
def stripped_windows(text,remove_capture_field):
 t=ast.parse(text)
 t.body=[x for x in t.body if not (isinstance(x,(ast.ClassDef,ast.FunctionDef)) and x.name in ('Capture','wait'))]
 if remove_capture_field:
  matches=0
  for x in ast.walk(t):
   if isinstance(x,ast.Dict):
    for i in reversed(range(len(x.keys))):
     k=x.keys[i]
     if isinstance(k,ast.Constant) and k.value=='capture_state':del x.keys[i];del x.values[i];matches+=1
  check('one_capture_state_field',matches==1)
 return dump(t)
check('windows_AST_only_capture_wait_receipt_delta',stripped_windows(oldtext['launch_windows.py'],False)==stripped_windows(norm(newtext['launch_windows.py']),True))
c=newtext['common.py'];l=newtext['linux_control.py'];w=newtext['launch_windows.py']
for name,ok in [
 ('errors_per_stream','self.errors={key:None for key in self.buffers}' in w),
 ('eof_per_stream_false','self.eof={key:False for key in self.buffers}' in w),
 ('normal_eof_exact','if raw==b"":\n                    self.eof[key]=True\n                    return' in w),
 ('read_exceptions_recorded','except BaseException as exc:' in w and 'self.errors[key]={"type":type(exc).__name__,"message":str(exc)[:1000]}' in w),
 ('read_type_guard','if not isinstance(raw,bytes):raise TypeError' in w),
 ('require_no_errors_raises','if any(error is not None for error in self.errors.values()):' in w),
 ('join_requires_errors_and_eof','self.require_no_errors()\n        if any(t.is_alive() for t in self.threads):return False\n        if not all(self.eof.values()):raise RuntimeError' in w),
 ('join_requires_no_overflow','if self.overflow:raise RuntimeError("WSL output overflow")\n        return True' in w),
 ('wait_polls_errors','while proc.poll() is None:\n        cap.require_no_errors()' in w),
 ('wait_after_join_error_check','if not cap.join(deadline):raise TimeoutError("Stream capture not joined")\n    cap.require_no_errors()' in w),
 ('both_capture_states_persisted','"capture_state":{"primary":None if pcap is None else pcap.snapshot(),\n                         "cleanup":None if ccap is None else ccap.snapshot()}' in w),
 ('windows_logical_cap','extend(raw[:room])' in w),
 ('linux_logical_cap',new_capture in l),
 ('postreceipt_and_postflush','Final IO exceeded nominal60s' in w and 'Terminal stdout IO exceeded nominal60s' in w),
 ('cleanup_finally_preserved','g.fresh(run/"STOP.json"' in w and 'cleaner,ccap,cargv=launch' in w),
 ('request_same',a['request_id']==b['request_id']=='4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf'),
 ('single60_no_retry',b['limits']['nominal_total_s']==60 and b['limits']['max_control_runs']==1 and b['limits']['retry'] is False),
 ('command_contract_pin',same(NEW/'CONTRATO_WSL.json',read(NEW/'COMANDO_PROPOSTO_NAO_EXECUTADO.json')['contract'])),
 ('command_exact_V2_path',read(NEW/'COMANDO_PROPOSTO_NAO_EXECUTADO.json')['argv'][-2]==str(NEW/'launch_windows.py')),
]:check(name,ok)
for directory in (OLD,NEW):
 for n in ('AUTORIZACAO_ROOT.json','CLAIM.json','RUN','RESULT.json'):check('unconsumed:'+directory.name+'/'+n,not (directory/n).exists())
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'STATIC_DELTA_ACCEPTED_NO_BLOCKER_LOCATED_NOT_EXECUTED','reviewer':'chatgpt-codex/ordem-018/preregistros','request_id':b['request_id'],'map_before_seq':523,'source_manifest':pin(NEW/'MANIFESTO_PREPARACAO_WSL_V2.json'),'original_manifest':pin(OLD/'MANIFESTO_PREPARACAO_WSL.json'),'original_review_manifest':pin(REVIEW/'MANIFESTO_REVISAO_WSL.json'),'contract':pin(NEW/'CONTRATO_WSL.json'),'check_count':len(checks),'checks':checks,'resolved_findings':['WSL-01','WSL-02'],'candidate_imports':0,'candidate_executions':0,'WSL_invocations':0,'hooks':0,'stubs':0,'authorizations_created':0,'claims_created':0,'scope':'Static AST/text/hash only; Linux pins compared to admitted documentary receipt. Not behavioral qualification or authorization.'}
persist('RECIBO_REVISAO_WSL_V2.json',receipt)
print(json.dumps({'check_count':len(checks),'receipt':pin(BASE/'RECIBO_REVISAO_WSL_V2.json'),'contract':receipt['contract']},ensure_ascii=False))
