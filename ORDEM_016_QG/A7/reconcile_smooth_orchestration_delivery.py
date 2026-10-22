"""Append orchestration receipts and correct mixed-delivery cost aggregation."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'mixed_smooth_delivery'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,raw,replace=False):
    if p.exists():
        assert replace,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;tmp.replace(p)
def add(p,text):put(p,p.read_bytes()+text.encode(),True)
def obj(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2).encode())

sources=['a7_smooth_completion_pending_submissions.json',
         'mimo_sse_operational_validation_20260925.json']
copied=[]
for name in sources:
    source=BASE/'state/handoffs'/name;target=D/name
    put(target,source.read_bytes());assert sha(target)==sha(source)
    copied.append(dict(path=str(target),sha256=sha(target)))
cat=json.loads((D/sources[0]).read_bytes())
assert sha(Path(cat['catalog']))==cat['catalog_sha256']
for u in cat['units']:
    assert sha(Path(u['source']))==u['payload_sha256']
val=json.loads((D/sources[1]).read_bytes());r=val['receipt']['result']
assert val['status']=='ready' and r['text']=='42'
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
assert not any(x.get('request_id')==val['request_id'] for x in rows)
events=[dict(at=now.isoformat(),event='ORCHESTRATION_SMOOTH_CATALOG_ACCEPTED',
    target='A7.b',request_ids=[u['request_id'] for u in cat['units']],
    status='STAGING_WAITING_CAPACITY',new_remote_execution=False),
    dict(at=now.isoformat(),event='MIMO_SSE_PUBLIC_OPERATIONAL_VALIDATION_RECEIVED',
    target='A7.b_support_infrastructure',provider='mimo',request_id=val['request_id'],
    tokens=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],
    cost_status=r['cost_status'],prompt_sha256=hashlib.sha256(val['actual_prompt'].encode()).hexdigest(),
    response_sha256=hashlib.sha256(r['text'].encode()).hexdigest(),
    receipt_sha256=sha(D/sources[1]),new_remote_execution=False,
    scientific_result=False,executed_by='authorized coordinator')]
rows+=events
seen=set();scientific=Decimal(0);infra=Decimal(0);items=[]
for row in rows:
    value=row.get('cost_estimate_usd')
    if value is None:value=row.get('cost_usd')
    if value is None:continue
    key=row.get('execution_task_id') or row.get('job_id') or row.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    amount=Decimal(str(value))
    if row.get('target')=='A7.b_support_infrastructure':infra+=amount
    else:scientific+=amount
    items.append(dict(key=key,event=row.get('event'),amount=str(amount)))
total=scientific+infra
old=D/'cost_summary.json'
obj(D/'cost_summary_v2.json',dict(at=now.isoformat(),supersedes=str(old),
    predecessor_sha256=sha(old),
    correction='Previous aggregation omitted cost_usd when cost_estimate_usd absent; preserved original.',
    known_scientific_estimates_usd=str(scientific),
    known_operational_validation_usd=str(infra),
    known_total_usd=str(total),items=items,
    completeness='PARTIAL; provider-priced estimates not invoice; unknown costs not zero'))
events.append(dict(at=now.isoformat(),event='COST_AGGREGATION_CORRECTION',
    target='A7.b',missing_legacy_field='cost_usd',
    known_total_usd=str(total),details=str(D/'cost_summary_v2.json')))
add(ledger,''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events))
opening=OUT/'ENTREGA_016_ABERTURA_operador.md'
note=f'''[REAL — recibos operacionais conferidos; análises científicas novas pendentes]

{now.isoformat()}. Abertura SHA256 {sha(opening)}.
As três novas unidades foram aceitas pela coordenação em staging,
com IDs e hashes conferidos. Ainda aguardam vagas, não respostas.
Kimi mantém a chamada corrente e a sequência científica preparada.
A próxima vaga é reservada à revisão DeepSeek de quarta ordem já preparada.

MiMo: validação operacional única do transporte SSE respondeu42,
com23 tokens de entrada e3 de saída,3.67s. Custo estimado
USD{infra}. O coordenador comunicou liberação do HOLD e início da
unidade f0385e3c-5186-4fba-95d8-41b3bf325b92, sem repetir terminais.
O teste curto não comprova sustentação de uma resposta longa.

Correção contábil ao lado: finalize_mixed_smooth_delivery.py somou apenas
cost_estimate_usd, omitindo o registro legado cost_usd. O somador v2 lê
ambos, deduplica por identidade e preserva o resumo anterior. Parcial
científico USD{scientific}; operacional USD{infra}; total conhecido
USD{total}. Não é fatura nem total completo; custos desconhecidos não são zero.
Recibos e discriminação em {D}.
'''
put(OUT/'ENTREGA_016_A7b_ampliacao_orquestra_e_custo_adendo.md',note.encode())
add(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} ADENDO: três revisões aceitas em staging; MiMo SSE validado e tarefa científica retomada pela coordenação. Correção soma inclui cost_usd legado: científicoUS${scientific}, operacionalUS${infra}, totalparcialUS${total}; resumo anterior preservado.\n')
p=H/'CONTINUIDADE.json';cont=json.loads(p.read_bytes())
cont.update(at=now.isoformat(),partial_metered_cost_usd=str(total),
    scientific_partial_metered_cost_usd=str(scientific),
    smooth_completion_acceptance=str(D/sources[0]),
    pending_orchestration='New Kimi2/DeepSeek1 accepted staging; next free slot DeepSeek d317; Kimi6c210 and MiMof0385 running per coordinator; operational SSE only validated short public response')
put(p,json.dumps(cont,ensure_ascii=False,indent=2).encode(),True)
obj(D/'orchestration_adendum_manifest.json',dict(at=now.isoformat(),
    artifacts=copied+[dict(path=str(D/'cost_summary_v2.json'),sha256=sha(D/'cost_summary_v2.json')),
        dict(path=str(Path(__file__)),sha256=sha(Path(__file__)))],gate_changed=False))
print(json.dumps(dict(accepted=len(cat['units']),scientific=str(scientific),infra=str(infra),total=str(total))))
