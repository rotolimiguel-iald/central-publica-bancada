"""Custody and accounting for a reviewed MiMo receipt; no model call."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;D=H/'mimo_frame_review';O=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,text):write(p,p.read_bytes()+text.encode())
def dump(obj):return json.dumps(obj,ensure_ascii=False,indent=2).encode()
for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
r=json.loads((D/'results.json').read_bytes());receipt=json.loads((D/'RECEIPT.json').read_bytes())
p=H/'orchestration_bilocal_completion_v2/mimo_bilocal_frame_index_implementation_audit_submit.json';payload=json.loads(p.read_bytes())
catalog=json.loads((p.parent/'prepared_units.json').read_bytes());assert next(x for x in catalog if x['payload']==str(p))['payload_sha256']==sha(p)
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md');log=H/'mimo_frame_review_run.log'
u=receipt['result']['usage'];cached=u['prompt_tokens_details']['cached_tokens'];miss=u['prompt_tokens']-cached
discount=(Decimal(miss)*Decimal('.435')+Decimal(cached)*Decimal('.0036')+Decimal(u['completion_tokens'])*Decimal('.87'))/Decimal(1000000)
conservative=(Decimal(u['prompt_tokens'])*Decimal('.435')+Decimal(u['completion_tokens'])*Decimal('.87'))/Decimal(1000000)
assert discount==Decimal(str(receipt['result']['cost_estimate_usd']))
assert conservative==Decimal(receipt['result']['request_cost_accounting']['accounted_usd'])
reconciliation=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/mimo_c763_cost_reconciliation.json'
write(D/'COST_RECONCILIATION.json',reconciliation.read_bytes())
m=D/'delivery_manifest.json';assert not m.exists()
write(m,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,
 artifacts=[dict(path=str(q),sha256=sha(q)) for q in [D/'manifest.json',D/'DERIVACAO.md',D/'COST_RECONCILIATION.json',log,p,Path(__file__)]],full_Q2=False)))
ledger=O/'LEDGER_016.jsonl';rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
assert not any(x.get('execution_task_id')==receipt['execution_task_id'] for x in rows)
event=dict(at=now.isoformat(),event='MODEL_REVIEW_RECEIVED_AND_AUDITED',provider='mimo',target='A7.b',
 branch='bilocal_frame_index_implementation_audit',request_id=payload['request_id'],job_id=receipt['job_id'],execution_task_id=receipt['execution_task_id'],
 usage=u,cost_estimate_usd=str(discount),conservative_no_cache_cost_usd=str(conservative),
 cost_status='IMPLEMENTED_RATES_NOT_INVOICE_ALTERNATIVES_NOT_ADDITIVE',prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
 payload_sha256=sha(p),response_sha256=sha(D/'RESPONSE.md'),receipt_sha256=sha(D/'RECEIPT.json'),
 scientific_status=r['verdict'],remote_call_by_this_script=False)
append(ledger,json.dumps(event,ensure_ascii=False)+'\n');rows.append(event)
append(ledger,json.dumps(dict(at=now.isoformat(),event='FRAME_REVIEW_LOCAL_AUDIT',target='A7.b',checks=r['checks'],cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(m),remote_call=False))+'\n')
seen=set();total=Decimal(0)
for e in rows:
 key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (key is None or key not in seen):
  total+=Decimal(str(v))
  if key:seen.add(key)
note=f'''[DERIVED — parecer MiMo parcialmente aproveitado; fontes e normalizações corrigidas]

{now.isoformat()}. Abertura SHA256 {opening}.

frame2 correto. A afirmação de completude da conexão por frame2 foi
refutada por um vetor constante no frame: -1/6+2/3=1/2, e a ordem
trocada produz -1/2. A derivada da conexão é indispensável.
Os dois motores já incluem termos explícitos +(8/3)v1/m-(2/3)v2.
tensor(a,a) é 1, não2; frob vazio é int0 exato, nãofloat.

1116 controles, CPU{r['cpu_seconds']}s, rc0.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/mimo_frame_review_check.py.
Log SHA256 {sha(log)}. Derivação {D/'DERIVACAO.md'}.
Manifesto {m}, SHA256 {sha(m)}.

Custo da mesma chamada: US${discount} com cache e US${conservative}
na contabilidade conservadora sem desconto de cache. Fórmulas
reconciliadas por tokens e tarifas implementadas; não são duas chamadas,
não somar. Fatura não consultada. Parcial conhecido do ledger, usando
cost_estimate_usd com desconto quando fornecido: US${total}.

Nenhum motor foi alterado para acomodar o parecer. Q2 integral OPEN.
Próximo: composição dos jatos suaves com a corrente EH localizada.
'''
p=O/'ENTREGA_016_A7b_auditoria_MiMo_frame_e_conexao.md';assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b MEDIDA/PROGRESS: MiMo frame auditado,1116checks CPU{r["cpu_seconds"]}s; conexão preservada; custo reconciliado; parcial US${total}.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),mimo_frame_review_manifest=str(m),partial_metered_cost_usd=str(total),
 next=['Localized full EH tadpole: separate same-leg second jets from GammaGamma mixed jets','A7b deadline20:32Z; A7c/d,A8,PartB and final remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(m),checks=r['checks'],partial_known_cost=str(total))))
