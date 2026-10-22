from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys

folder=Path(__file__).resolve().parent
base=folder.parents[1]/'IALD_ORQUESTRACAO_20260923'
out=folder.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)

def write(path, raw):
    if path.exists():
        old=path.read_bytes()
        backup=path.with_name(path.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream: stream.write(old)
        assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream: stream.write(raw)
    assert temp.read_bytes()==raw
    temp.replace(path)

destination=folder/'a23_kimi_mutation_submit_result.json'
assert not destination.exists()
data=(folder/'a23_kimi_mutation_submit.json').read_bytes()
result=subprocess.run([sys.executable,'-X','utf8','-B',str(base/'transport_cli.py')],
                      input=data,capture_output=True)
write(destination,result.stdout)
write(folder/'a23_kimi_mutation_submit_stderr.txt',result.stderr)
assert result.returncode==0, result.stderr.decode(errors='replace')
job=json.loads(result.stdout)
receipt=json.loads((folder/'a23_kimi_mutation_receipt.json').read_bytes())
assert job['request_id']==receipt['request_id']
receipt.update(job_id=job['id'],status=job['stage'],submitted_at=now.isoformat())
raw=json.dumps(receipt,indent=2,ensure_ascii=False).encode()
write(folder/'a23_kimi_mutation_receipt.json',raw)
write(base/'state/session_requests'/(receipt['request_id']+'.json'),raw)
entry={'ts':now.isoformat(),'event':'coordination_submitted','provedor':'kimi',
       'alvo':'A-2','ramo':'A-2.3.a','request_id':job['request_id'],'job_id':job['id'],
       'question_sha256':receipt['prompt_sha256'],'answer_sha256':None,
       'tokens_in':None,'tokens_out':None,'custo_usd':None,
       'desfecho':'registered_'+job['stage'],'execution_constraints':receipt['execution_constraints']}
ledger=out/'LEDGER_016.jsonl'
write(ledger,ledger.read_bytes()+(json.dumps(entry,ensure_ascii=False)+'\n').encode())
print(json.dumps({'job_id':job['id'],'request_id':job['request_id'],'stage':job['stage']},ensure_ascii=False))
