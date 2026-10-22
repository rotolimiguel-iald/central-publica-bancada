from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent;BASE=ROOT.parent/'IALD_ORQUESTRACAO_20260923';OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):
    if p.exists():
        old=p.read_bytes();b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(old)
        assert b.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+stamp)
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data and data
    t.replace(p);assert p.read_bytes()==data
origin=BASE/'state/handoffs/db1b6948-4e94-44b8-8818-7143e9e92f40_completed.json'
d=json.loads(origin.read_text(encoding='utf8'));e=d['execution'];r=e['result']
assert d['stage']=='completed' and e['status']=='result_ready'
answer=r['text'];write(HERE/'mimo_reuse_answer.md',answer.encode())
meta=dict(utc=now.isoformat(),request_id=d['request_id'],job_id=d['id'],execution_task_id=e['id'],
          origin_sha256=sha(origin),question_sha256=hashlib.sha256(d['prompt'].encode()).hexdigest(),
          answer_sha256=hashlib.sha256(answer.encode()).hexdigest(),usage=r['usage'],
          cost_estimate_usd=r.get('cost_estimate_usd'),cost_status=r.get('cost_status'),
          request_cost_accounting=r.get('request_cost_accounting'),elapsed_seconds=r.get('elapsed_seconds'),
          model=r.get('model'),canonical_memory=r.get('canonical_memory'),
          status='DECLARADO_MODEL_REVIEW_CONFRONTED_WITH_LOCAL_LEAN')
write(HERE/'mimo_reuse_review_receipt.json',json.dumps(meta,ensure_ascii=False,indent=2).encode())
ledger=OUT/'LEDGER_016.jsonl';old=ledger.read_bytes()
assert not any(json.loads(line).get('event')=='reuse_mimo_review_received' for line in old.decode().splitlines() if line.strip())
event=dict(ts=now.isoformat(),event='reuse_mimo_review_received',alvo='A-3',ramo='A-3.d',provedor='mimo',
           request_id=d['request_id'],job_id=d['id'],execution_task_id=e['id'],question_sha256=meta['question_sha256'],
           answer_sha256=meta['answer_sha256'],raw_usage=r['usage'],custo_usd=None,
           cost_estimate_usd=r.get('cost_estimate_usd'),request_cost_accounting=r.get('request_cost_accounting'),
           cost_reconciliation='TWO_PRICED_ESTIMATES_DIFFER_NOT_INVOICE',elapsed_seconds=r.get('elapsed_seconds'),
           provider_calls_observed=1,desfecho='completed',receipt_sha256=sha(origin))
write(ledger,old+(json.dumps(event,ensure_ascii=False)+'\n').encode())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[REAL — recebimento/confronto; parecer do modelo com estatuto DECLARADO]

# ORDEM 016 — revisão MiMo do reaproveitamento geométrico

UTC {now.isoformat()}. ABERTURA sha256 `{opening}`.

Unidade {d['request_id']}, job {d['id']}, concluída por {r.get('model')}.
Resposta integral e recibo em A3/mimo_reuse_answer.md e mimo_reuse_review_receipt.json.

O parecer confirmou a composição que a bancada já compilou: `refRadius_pos` e
`observer_unit_of_index` exigem somente N, não um ContratoH2 pronto. Portanto
podem fornecer κ>0 e observer_unit sem circularidade; os demais campos
geométricos vêm de WedgeDraggedFrame_v6 por restrição/instanciação. A prova
aceita é ExistingKillingCalibration.geometric_fields_reused, rc0/trio,
não o voto do MiMo. Nenhuma nova camada de funções é necessária.

O rascunho WedgeKillingNormalization_v4 continua não compilado e não incorporado:
suas provas de normalização repetiam fornecedores existentes. A sugestão de
código `def geometricFields ... where` no parecer não tem tipo de resultado
fornecido; é pseudocódigo de composição, não arquivo Lean validado. A bancada
usou o enunciado/conjunção explícitos já compilados.

Correção de alcance: a classificação da derivada `wedge_boost_hasDerivAt` como
«nova» significa não localizada no pacote específico. O kernel tem
ApproximateBoostFlow.boost_flow_hasDerivAt; A2 liga os boosts por permutação
e sinal. Não anunciar inexistência global nem nova descoberta dessa derivada.
O parecer sobre theCurvedFrame vale para aquele frame particular; não exclui
outros frames do acervo.

Uso medido: {r['usage']['prompt_tokens']} tokens de entrada,
{r['usage']['completion_tokens']} saída (inclui raciocínio),
{r['usage']['total_tokens']} total; {r['elapsed_seconds']}s.
O recibo contém DOIS preços diferentes: cost_estimate_usd={r.get('cost_estimate_usd')}
e request_cost_accounting.accounted_usd={r.get('request_cost_accounting',{}).get('accounted_usd')}.
Ambos preservados; nenhum apresentado como fatura. Divergência encaminhada à
coordenação; custo desta unidade não somado como se houvesse valor único reconciliado.
Gasto histórico conhecido anterior permanece US$0.159306135, acrescido desta
unidade com conciliação pendente e demais consumos não informados.

Kimi nesta frente falhou por cota; nenhuma substituição/repetição. Revisão MiMo
não foi tratada como resposta de Kimi. Kernel, gate e originais intactos.
Próxima ação permanece A3.4, ligação da medida orbital à rapidez; H2 completo
não foi declarado por este parecer ou pelo conjunto geométrico.
'''
write(OUT/'ENTREGA_016_MEDIDA_A3d_MiMo_reaproveitamento.md',report.encode())
p=OUT/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n{now.isoformat()} | MiMo A3.d concluído e confrontado: redundâncias confirmadas, composição já compilada mantida. {r["usage"]["total_tokens"]} tokens/{r["elapsed_seconds"]}s; duas estimativas de custo divergentes preservadas para conciliação, não somadas como gasto único. Kimi cota sem repetição.\n'.encode())
print(json.dumps({k:meta[k] for k in ['job_id','usage','cost_estimate_usd','elapsed_seconds']},ensure_ascii=False))
