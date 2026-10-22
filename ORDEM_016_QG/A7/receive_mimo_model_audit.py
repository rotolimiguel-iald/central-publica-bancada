"""Recover the completed, authorized model-input review without execution transitions."""
from pathlib import Path
import hashlib, json, sys, uuid

here = Path(__file__).resolve().parent
base = here.parents[1] / 'IALD_ORQUESTRACAO_20260923'
sys.path.insert(0, str(base))
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination

job = '187b509f-0a81-41e3-9f6a-835c870b525c'
record = Coordination(Runtime(recover=False)).get(job)
execution = record['execution']
assert execution['status'] == 'result_ready'
assert record['execution_constraints']['required_provider'] == 'mimo'
result = execution['result']
body = result['text'].encode('utf-8')
receipt = dict(job_id=job, request_id=record['request_id'], execution_id=execution['id'],
    provider='mimo', prompt_sha256=hashlib.sha256(record['prompt'].encode()).hexdigest(),
    response_sha256=hashlib.sha256(body).hexdigest(),
    result_metadata={k:v for k,v in result.items() if k != 'text'},
    status='DECLARADO_PENDING_LOCAL_REVIEW', new_external_execution=False)
dest = here / 'received_reviews'
dest.mkdir(exist_ok=True)
for suffix, data in [('.md', body), ('.json', json.dumps(receipt, ensure_ascii=False, indent=2).encode())]:
    path = dest / (job + suffix)
    if path.exists():
        assert path.read_bytes() == data
    else:
        temp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
        temp.write_bytes(data)
        assert temp.read_bytes() == data
        temp.replace(path)
print(json.dumps(dict(job_id=job, bytes=len(body), usage=result.get('usage'),
    cost=result.get('cost_estimate_usd'), path=str(dest/(job+'.md'))), ensure_ascii=False))
