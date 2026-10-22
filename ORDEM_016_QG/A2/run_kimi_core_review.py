from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys

folder=Path(__file__).resolve().parent
root=folder.parents[1]
base=root/'IALD_ORQUESTRACAO_20260923'
out=root/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def replace(p,data):
    old=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with backup.open('xb') as f:f.write(old)
    assert backup.read_bytes()==old
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(data)
    assert temp.read_bytes()==data
    temp.replace(p)
payload=json.loads((folder/'a23_kimi_direct_submit.json').read_bytes())
preview=json.loads((folder/'a23_kimi_direct_preview.json').read_bytes())
receipt_path=folder/'a23_kimi_direct_receipt.json'
r=json.loads(receipt_path.read_bytes())
assert r['status']=='prepared_direct'
assert payload['request_id']==r['request_id'] and preview['selected']=='kimi'
assert hashlib.sha256(payload['prompt'].encode()).hexdigest()==r['prompt_sha256']
r['status']='direct_dispatching';r['dispatched_at']=now.isoformat()
data=json.dumps(r,ensure_ascii=False,indent=2).encode()
replace(receipt_path,data)
replace(base/'state/session_requests'/f"{r['request_id']}.json",data)
ledger=out/'LEDGER_016.jsonl'
entry={'ts':now.isoformat(),'alvo':'A-2','ramo':'A-2.3.a','provedor':'kimi','role':'skeptic',
       'request_id':r['request_id'],'job_id':None,'tokens_in':None,'tokens_out':None,'custo_usd':None,
       'question_sha256':r['prompt_sha256'],'answer_sha256':None,
       'desfecho':'direct_dispatch_authorized_by_latest_operator_message',
       'note':'Official submit_execution; no Work coordination; independent new review unit, not retry of failed MiMo.'}
replace(ledger,ledger.read_bytes()+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
print(json.dumps({'request_id':r['request_id'],'status':'direct_dispatching','provider':'kimi'}),flush=True)
call=subprocess.run([sys.executable,'-X','utf8','-B',str(base/'transport_cli.py')],
    input=json.dumps(payload,ensure_ascii=False).encode(),capture_output=True)
for name,raw in [('a23_kimi_direct_stdout.json',call.stdout),('a23_kimi_direct_stderr.txt',call.stderr)]:
    p=folder/name;assert not p.exists()
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw
    temp.rename(p)
r['cli_returncode']=call.returncode;r['returned_at']=datetime.now(timezone.utc).isoformat()
try:
    result=json.loads(call.stdout)
    r['execution_task_id']=result.get('id');r['status']=result.get('status','returned_unknown')
    r['error']=result.get('error');r['result_sha256']=hashlib.sha256(call.stdout).hexdigest()
except Exception:
    r['status']='uncertain_cli_output';r['error']='No JSON task result; do not retry automatically.'
data=json.dumps(r,ensure_ascii=False,indent=2).encode()
replace(receipt_path,data);replace(base/'state/session_requests'/f"{r['request_id']}.json",data)
print(json.dumps({k:r.get(k) for k in ['request_id','execution_task_id','status','error','cli_returncode']},ensure_ascii=False),flush=True)
