"""Preserve the end-of-turn evidence and current orchestration receipts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def save(p,b):
    old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with bk.open('xb') as f:f.write(old)
    assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and b;t.replace(p)
costs={}
for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    k=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if v is not None and k:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)));at=datetime.now(timezone.utc).isoformat()
verified=0
for folder in ['metric_primitive_zero_ghost','metric_primitive_zero_ghost_audit','constant_ghost_eom',
               'constant_ghost_transverse','antifield_quadratic_primitive','shifted_antifield']:
    for item in json.loads((HERE/folder/'manifest.json').read_bytes())['artifacts']:
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'];verified+=1
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes())
d.update(at=at,partial_metered_cost_usd=total,
    prepared_primitive_reviews_status='V2_RECONCILED_STAGING_AFTER_MARKED',
    deepseek_d2_received='A6_EQUACAO_DA_VERDADE/received_reviews/14baed7e-08f4-4787-aeea-8538cc7dd075.md',
    deepseek_d2_local_review='PENDING_FULL_READ',latest_verified_artifacts=verified)
save(p,json.dumps(d,ensure_ascii=False,indent=2).encode())
opening=hashlib.sha256((OUT/'ENTREGA_016_ABERTURA_operador.md').read_bytes()).hexdigest()
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {at} — A7.b rodada PROGRESSO: {verified}artefatos hash-conferidos; primitivaBVv2 reconciliada sem nova chamada. DeepSeekD2recuperado, revisão integral pendente. Custo parcialUS${total}. Q2finitaOPEN, metaACTIVE. Abertura{opening}.\n'.encode())
print(json.dumps(dict(verified_artifacts=verified,partial_cost_usd=total,goal='ACTIVE')))
