"""Refresh the measured partial ledger total and staged-review receipt."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def save(p,raw):
    old=p.read_bytes();b=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with b.open('xb') as f:f.write(old)
    assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert raw and t.read_bytes()==raw;t.replace(p)
costs={}
for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    k=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if v is not None and k:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)));at=datetime.now(timezone.utc).isoformat()
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes());d['partial_metered_cost_usd']=total;d['at']=at
d['completed_this_turn'] += ['Local ghost primitive65checks and coordinate320checks;48residual components remain',
    'Kimi metric primitive and MiMo heat audit staged and acknowledged by coordinator',
    'MiMo C2 received and locally reviewed9checks;original baseline46declarations still passes']
save(p,json.dumps(d,ensure_ascii=False,indent=2).encode())
opening=hashlib.sha256((OUT/'ENTREGA_016_ABERTURA_operador.md').read_bytes()).hexdigest()
p=OUT/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {at} — ORQUESTRACAO: mais2unidades Kimi/MiMo preparadas e aceitas em staging; ainda sem job nesta entrega. Agendador medido5pedidos/1execução. MiMoC2concluído e cotejado9checks,CPU0.015625s; P1/P9reproduzidos no escopo do relatório. Custo externo parcial deduplicadoUS${total}; custos desconhecidos não zerados. Abertura{opening}.\n'.encode())
print(json.dumps({'partial_cost_usd':total,'goal':'ACTIVE','two_reviews':'STAGED_NOT_EXECUTED'}))
