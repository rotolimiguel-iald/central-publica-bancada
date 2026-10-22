from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
base=root.parent/'IALD_ORQUESTRACAO_20260923'
sys.path.insert(0,str(base))
from iald_orchestrator.runtime import Runtime
r=json.loads((root/'A2/delegation_a23_core.json').read_bytes())
assert r['job_id'] is None
c={'mission_id':'ORDEM_016','branch_id':'A2.3.a','lemma_id':'gaussian_core_density',
   'role':'draft','required_provider':'mimo','max_calls':1,
   'max_cost_usd':None,'max_output_tokens':131072}
runtime=Runtime(recover=False)
preview=runtime.preview(r['prompt'],c)
assert preview['selected']=='mimo',preview.get('status')
data={'operation':'submit','prompt':r['prompt'],'request_id':r['request_id'],'execution_constraints':c}
for name,value in [('a23_mimo_submit.json',data),('a23_mimo_preview.json',preview)]:
 p=root/'A2'/name
 assert not p.exists(),p
 b=json.dumps(value,ensure_ascii=False,indent=2).encode()
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b
 t.rename(p)
print(json.dumps({'request_id':r['request_id'],'selected':preview['selected'],
 'canonical_memory':preview.get('canonical_memory'),'status':preview['status'],
 'payload_sha256':hashlib.sha256((root/'A2/a23_mimo_submit.json').read_bytes()).hexdigest()},ensure_ascii=False))
