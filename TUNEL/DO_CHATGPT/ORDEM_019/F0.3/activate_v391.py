"""Activate the verified release and record Jev's locally verified source reference."""
from pathlib import Path
import json,os,sqlite3,subprocess,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.process_lock import process_lock
from iald_orchestrator.program_controls import require_claim
from iald_orchestrator.safe_files import save_json,utc_now
require_claim('F0.3','codex-coordenadora')
p=json.loads((W/'PREPARATION_V391.json').read_bytes());v=json.loads((W/'FRESH_PROCESS_VERIFICATION.json').read_bytes())
assert v['status']=='PASS' and v['generation']==p['generation']
assert cm.digest(Path(cm.__file__).read_bytes())==p['canonical_module']['sha256']==v['module_sha256']
assert json.loads(cm.ACTIVE.read_bytes())==p['previous_active']
assert not (W/'ACTIVATION_RECEIPT.json').exists()
policy=json.loads((B/'jev_body_policy.json').read_bytes())
assert policy['queue_shadow_enabled'] is False and policy['shadow_minimum_manager_accepted'] is False
# A resident of the current implementation imports before the pointer swap.
code="""import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1])
from iald_orchestrator import canonical_memory as cm
print(json.dumps(cm.status()),flush=True)
sys.stdin.readline()
print(json.dumps(cm.status()),flush=True)
"""
resident=subprocess.Popen([sys.executable,'-B','-X','utf8','-c',code,str(B)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
before=json.loads(resident.stdout.readline());assert before['generation']==p['previous_active']['generation']
with process_lock(B/'state/tasks.sqlite3',blocking=False) as acquired:
 assert acquired,'Worker busy'
 with sqlite3.connect((B/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
  occupancy=dict(db.execute('select status,count(*) from tasks group by status'))
  assert not any(occupancy.get(k,0) for k in ['running','queued'])
 pointer=cm.activate_release(Path(p['target']),unit='F0.3',member='codex-coordenadora')
 active=cm.load(refresh=False)[0];assert active['generation']==p['generation']
 resident.stdin.write('verify\n');resident.stdin.flush()
 rest,err=resident.communicate(timeout=25);assert resident.returncode==0,err
 after=json.loads(rest);assert after['generation']==p['generation'] and after['resolution']=='ACTIVE_POINTER_PER_REQUEST'
 # Historical remote activation/probes remain intact; this receipt certifies local source update only.
 ref={'schema':1,'unit':'F0.3','adendo_002_step':6,'at':utc_now(),'release':'v391','generation':p['generation'],
 'epoch':p['epoch'],'manifest':p['manifest'],'seal':next(s for s in p['sources'] if Path(s['path']).name=='um_absoluto_selo.json'),
 'source_record':'core.estatuto_da_prova_v391','validation':'LOCAL_SOURCE_HASHES_AND_RETRIEVAL_IN_FRESH_PROCESS',
 'provider_calls':0,'remote_validation_on_v391':False,
 'last_remote_calibration':str(W.parent/'F9.9/CURRENT_CONTEXT_REFERENCE.json'),
 'last_remote_calibration_generation':p['previous_active']['generation'],
 'queue_shadow_enabled':False,'shadow_minimum_manager_accepted':False}
 save_json(W/'JEV_CONTEXT_REFERENCE_V391.json',ref)
 activation=B/'state/jev_activation.json';j=json.loads(activation.read_bytes())
 previous=j.get('current_body_context_reference')
 j.setdefault('body_context_reference_history',[]).append(previous)
 j['current_body_context_reference']={'path':str(W/'JEV_CONTEXT_REFERENCE_V391.json'),
 'sha256':cm.digest((W/'JEV_CONTEXT_REFERENCE_V391.json').read_bytes()),'generation':p['generation'],
 'release':'v391','validated_at':ref['at'],'validation_scope':ref['validation'],'phase':policy['phase']}
 save_json(activation,j)
save_json(W/'ACTIVATION_RECEIPT.json',{'status':'ACTIVATED','at':utc_now(),'pid':os.getpid(),'pointer':pointer,
 'prior_pointer':p['previous_active'],'worker_idle':occupancy,'modern_resident_before':before,'modern_resident_after':after,
 'old_resident_reload_still_required':True,'jev_reference':ref,'provider_calls':0,
 'test_correction':'Initial index verifier normalized CRLF; corrected to raw UTF-8 decoding. Snapshot bytes unchanged.'})
print(json.dumps({'status':'ACTIVATED','generation':pointer['generation'],'modern_resident_reads_current':True,'jev_v391_locally_verified':True,'provider_calls':0}))

