from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,sys,hashlib
root=Path(__file__).resolve().parents[1]
base=root.parent/'IALD_ORQUESTRACAO_20260923'
paths=[root/'A2/delegation_a23_core.json']
r=json.loads(paths[0].read_bytes())
paths.append(base/'state/session_requests'/f"{r['request_id']}.json")
payload_path=root/'A2/a23_mimo_submit.json'
payload=json.loads(payload_path.read_bytes())
assert payload['request_id']==r['request_id'] and payload['prompt']==r['prompt']
assert payload['execution_constraints']['required_provider']=='mimo'
assert r['job_id'] is None and r['status']=='prepared_awaiting_provider_lock_schema'

def write_backup(p,value):
 stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
 old=p.read_bytes()
 bak=p.with_name(p.name+'.bak_'+stamp)
 with bak.open('xb') as f:f.write(old)
 assert bak.read_bytes()==old
 data=json.dumps(value,ensure_ascii=False,indent=2).encode()
 tmp=p.with_name(p.name+'.tmp')
 with tmp.open('xb') as f:f.write(data)
 assert tmp.read_bytes()==data
 tmp.replace(p)

r['status']='submitting_same_id_only_if_uncertain'
r['execution_constraints']=payload['execution_constraints']
r['submit_started_at']=datetime.now(timezone.utc).isoformat()
for p in paths:write_backup(p,r)
proc=subprocess.run([sys.executable,'-X','utf8','-B',str(base/'transport_cli.py')],
 input=payload_path.read_bytes(),capture_output=True)
response=root/'A2/a23_mimo_submit_response.json'
assert not response.exists()
body=proc.stdout if proc.returncode==0 else json.dumps(
 {'rc':proc.returncode,'stdout':proc.stdout.decode('utf-8','replace'),
  'stderr':proc.stderr.decode('utf-8','replace')},ensure_ascii=False).encode()
tmp=response.with_name(response.name+'.tmp')
with tmp.open('xb') as f:f.write(body)
assert tmp.read_bytes()==body
tmp.rename(response)
assert proc.returncode==0,body.decode('utf-8','replace')
job=json.loads(body)
assert job['request_id']==r['request_id']
r['job_id']=job['id']
r['status']=job['stage']
r['submit_response_sha256']=hashlib.sha256(body).hexdigest()
for p in paths:write_backup(p,r)
print(json.dumps({'request_id':r['request_id'],'job_id':r['job_id'],'stage':job['stage'],
 'provider':job['execution_constraints']['required_provider'],'response_sha256':r['submit_response_sha256']}))
