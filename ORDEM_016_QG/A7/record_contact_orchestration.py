"""Record acknowledged delegations, reviewed reuse, and bench continuity."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
DEST=HERE/'orchestration_contacts'
REV=HERE.parent/'A6_EQUACAO_DA_VERDADE/received_reviews'
B=HERE.parent/'A6_EQUACAO_DA_VERDADE/B_fechamentos'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,data):
    if isinstance(data,str): data=data.encode('utf-8')
    assert not p.exists() and data,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(data)
    assert t.read_bytes()==data
    t.replace(p)
def replace(p,data):
    if isinstance(data,str): data=data.encode('utf-8')
    old=p.read_bytes()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.replacement_'+stamp)
    new(t,data)
    t.replace(p)
    assert p.read_bytes()==data

now=datetime.now(timezone.utc).isoformat()
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
catalog=json.loads((DEST/'prepared_units.json').read_bytes())
for u in catalog:
    assert sha(Path(u['payload']))==u['payload_sha256']
ack=dict(at=now,source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    evidence_channel='official_send_message_to_thread_incoming',
    status='ACKNOWLEDGED_STAGED_PENDING_QUEUE_CAPACITY',
    coordinator_receipt='BASE/state/handoffs/a7_contacts_pending_submissions.json',
    coordinator_receipt_read_locally=False,
    message='Catalog received; both hashes and IDs verified; staged after A6, A7 initial and filtration. Zero new calls/submissions; Kimi B3a still executing.',
    units=[dict(request_id=u['request_id'],provider=u['provider'],job_id=None) for u in catalog])
new(DEST/'coordinator_acknowledgment.json',json.dumps(ack,ensure_ascii=False,indent=2))

job='656a254a-0c11-4c7c-990f-1ba3d4515701'
receipt=json.loads((REV/(job+'.json')).read_bytes())
source=B/'PenaltyThreeLocksBridge_v2.lean'
compiled=json.loads((B/'penalty_bridge_02.json').read_bytes())
audit=json.loads((B/'penalty_bridge_02_audit.json').read_bytes())
assert sha(source)==compiled['source_sha256']
assert sha(B/'penalty_bridge_02.log')==compiled['log_sha256']
assert compiled['rc']==0 and audit['auditoria']=='PASSA'
assert not audit['sorry'] and not audit['fora_do_trio']
assert sha(REV/(job+'.md'))==receipt['response_sha256']
review=f'''[REAL — confronto com prova existente; DECLARADO — rascunho MiMo]
# MiMo B4 — reuso da ponte já compilada

Abertura sha256 `{opening}`.
Resposta integral lida, sha256 `{receipt['response_sha256']}`.
Fonte existente sha256 `{sha(source)}`; log sha256 `{sha(B/'penalty_bridge_02.log')}`.
Compilação anterior rc0; auditoria 2/2 declarações no trio e zero sorry.

O caminho matemático sugerido pelo MiMo coincide com a prova existente:
expandir Fin3, converter adjuntos e identificar o mesmo núcleo/projetor.
As duas igualdades estão em penalty_eq_kernel_H3L e reading_eq_kernel_PF.
O arquivo existente já usa a orientação correta de
LinearMap.adjoint_toContinuousLinearMap e simp only para a segunda igualdade.

O helper proposto eq_of_forall_inner_eq tem encadeamento mal formado na aplicação
de norm_eq_zero.mp e pow_eq_zero_iff; também precisa tratar a coerção complexa.
Nenhum motivo para introduzi-lo: o lema de adjunto já resolve a ponte.
Não compilei o candidato MiMo nem atribuo rc0 a ele. Não fiz nova implementação,
novo ciclo Lean ou nova chamada. A compilação conferida é a anterior da bancada.
Não identifica as matrizes float do runtime, fluxo modular, estado físico ou gate.
'''
new(REV/'REVISAO_MIMO_A6_B4.md',review)
ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
event=dict(event='A7_CONTACT_REVIEWS_STAGED_AND_B4_REUSED_20260924',at=now,
    target='A7.b/A6.B4_review',provider='local_coordination',external_calls=0,
    requests=[u['request_id'] for u in catalog],
    catalog_sha256=sha(DEST/'prepared_units.json'),
    acknowledgment_sha256=sha(DEST/'coordinator_acknowledgment.json'),
    review_sha256=sha(REV/'REVISAO_MIMO_A6_B4.md'),
    status='WAITING_QUEUE_CAPACITY_NO_NEW_PROVIDER_EXECUTION')
assert not any(x.get('event')==event['event'] for x in rows)
replace(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for row in rows:
    cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    key=row.get('execution_id') or row.get('job_id') or row.get('request_id') or row.get('execution_task_id')
    if cost is not None and key: costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
delivery=f'''[REAL — delegação preparada e recebida; OPEN — novas execuções]
# A7 — mais duas unidades, sem repetição de provas

Abertura sha256 `{opening}`.

| Executor | Unidade | Estado verificado |
|---|---|---|
| Kimi K3 máximo | Revisão adversarial da extensão tensorial e seus contatos | Prévia seleciona Kimi; catálogo recebido pela coordenação; aguarda vaga |
| MiMo | Tabela tipada dos contatos EOM, cutoff e extensão, com controles | Prévia seleciona MiMo; catálogo recebido; aguarda vaga |

IDs: `{catalog[0]['request_id']}` e `{catalog[1]['request_id']}`.
Catálogo sha256 `{sha(DEST/'prepared_units.json')}`; recibo de recebimento
sha256 `{sha(DEST/'coordinator_acknowledgment.json')}`. Fontes, hashes, linhas,
prévia e restrições estão em A7/orchestration_contacts. Mesma memória comum;
uma chamada por unidade; executor obrigatório. Não declarei uso efetivo novo.

A coordenação confirmou Kimi B3a em execução única. Os dois novos pedidos
ficam após os catálogos anteriores, sem duplicar fila, worker ou chamadas.

MiMo B4 recebido e revisado: reaproveita duas igualdades já compiladas, como
documentado em received_reviews/REVISAO_MIMO_A6_B4.md. Não foi necessário criar
outro módulo nem recompilar. Resposta externa não é prova por consenso.

Custo parcial registrado e deduplicado por execução: US${total}; estimativa,
não fatura completa, nem custo da assinatura Kimi. Esta preparação fez zero
chamadas novas. Gate e originais permanecem intactos.
'''
new(OUT/'ENTREGA_016_A7_orquestracao_contatos.md',delivery)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
replace(progress,progress.read_bytes()+f'\n- {now} — A7 delegação contatos: 2 novas unidades preparadas/recebidas (Kimi,MiMo), aguardam vaga; zero chamada nova. A6.B4 MiMo revisado por reuso de prova existente. Custo parcial deduplicado US${total}; bancada não instrumentada.\n'.encode())
cp=HERE/'CONTINUIDADE.json'
c=json.loads(cp.read_bytes())
c.update(at=now,previous_goal_turn='PROGRESS',
    completed_this_turn=['One-pair coherent tensor extension: 41 exact checks, 8 controls',
        'Two new distinct contact units previewed and acknowledged by coordinator',
        'MiMo B4 recovered and reviewed; existing compiled bridge reused'],
    tensor_extension_manifest=str(HERE/'tensor_extension/manifest.json'),
    latest_orchestration=dict(catalog=str(DEST/'prepared_units.json'),
        status=ack['status'],request_ids=event['requests']),
    next=['Complete multilocal prescription and Ward sum within A7.b timebox',
          'Consume existing delegated results without duplicating requests',
          'A7.d, A8, ORDEM015 PartB and final reports remain'],
    partial_metered_cost_usd=str(total))
replace(cp,json.dumps(c,ensure_ascii=False,indent=2))
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7_orquestracao_contatos.md'),
    partial_metered_cost_usd=str(total),new_units=2,acknowledged=True),ensure_ascii=False))
