"""Record prepared/reconciled work without calling it an execution."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,raw):
    if isinstance(raw,str):raw=raw.encode()
    if path.exists():
        old=path.read_bytes()
        if raw==old:return
        backup=path.with_name(path.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw and raw;temp.replace(path)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
catalog=json.loads((HERE/'orchestration_completion/prepared_units.json').read_bytes())
v4=json.loads((HERE/'orchestration_primitive_v4/prepared_units.json').read_bytes())[0]
verified={}
for group in ['constant_ghost_full_basis','general_marked','quadratic_metric_fit','quadratic_metric_joint','bv_gradient_fit','bv_gradient_audit']:
    manifest=json.loads((HERE/group/'manifest.json').read_bytes())
    for a in manifest['artifacts']:
        path=Path(a['path']);assert sha(path)==a['sha256'],str(path);verified[str(path)]=a['sha256']
for u in catalog+[v4]:
    pp=Path(u['payload']);assert sha(pp)==u['payload_sha256'];payload=json.loads(pp.read_bytes())
    assert payload['request_id']==u['request_id'] and payload['execution_constraints']['required_provider']==u['provider']
    rec=json.loads((pp.parent/(u['slug']+'_receipt.json')).read_bytes())
    for source in rec['sources']:assert sha(Path(source['path']))==source['sha256']
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_COMPLETION_REVIEWS_STAGED'
if marker.encode() not in raw:
    events=[dict(event=marker,at=now,provider=u['provider'],target='A-7.b',request_id=u['request_id'],
                 phase='PREPARED_AND_ACKNOWLEDGED_STAGING',payload_sha256=u['payload_sha256'],
                 new_external_execution=False,tokens=None,cost_usd=None) for u in catalog]
    events.append(dict(event='A7_PRIMITIVE_V4_RECONCILED',at=now,provider='kimi',request_id=v4['request_id'],
                       payload_sha256=v4['payload_sha256'],new_external_execution=False,
                       predecessor_v3='Local preview rejected >24000 prompt characters, no submission'))
    save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for ln in ledger.read_text('utf-8-sig').splitlines():
    if not ln.strip():continue
    x=json.loads(ln);v=x.get('cost_estimate_usd',x.get('cost_usd',x.get('custo_usd')))
    k=x.get('execution_id') or x.get('job_id') or x.get('request_id') or x.get('execution_task_id')
    if k and v is not None:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
snapshot=dict(at=now,source='Official message from coordinator01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    nonterminal_registered=dict(kimi=2,mimo=2,deepseek=1,total=5),
    staging=dict(kimi=5,mimo=5,deepseek=0,total=10),
    currently_executing='MiMo model_input_audit',new_prepared_requests=[u['request_id'] for u in catalog],
    primitive_v4_reconciled=True,verified_unique_artifacts=len(verified),partial_metered_cost_usd=total,
    unknown_costs_not_zero=True,new_remote_execution_by_this_script=False)
snapshot_path=HERE/'orchestration_completion/STATUS_DISPATCH.json'
assert not snapshot_path.exists();save(snapshot_path,json.dumps(snapshot,ensure_ascii=False,indent=2))
report=f'''[REAL — duas novas unidades preparadas, prévias corretas e staging confirmado; DECLARADO — respostas ainda sujeitas à revisão]
# ORDEM016 — distribuição ampliada após completar R1 principal
Abertura SHA256 `{opening}`. UTC {now}.

Kimi recebeu para staging a tarefa alta covariant_primitive_contacts
({catalog[0]['request_id']}): diferencial covariante da primitiva e termos de
curvatura/cutoff, distinto do cálculo de laços/calor já atribuído a ele.
MiMo recebeu completion_independent_check ({catalog[1]['request_id']}):
auditoria racional independente com coeficientes fixos, sem refazer ajuste.
As prévias selecionaram os executores pedidos; nenhuma chamada remota nesta
preparação. IDs, hashes, fontes e projeções estão em orchestration_completion.
A coordenadora confirmou os dois em staging após primitive_v4.

A unidade Kimi metric_primitive já preparada foi atualizada ANTES de submissão,
mesmoID/posição. A v3 excedeu o limite local24000caracteres e foi recusada na
prévia; v4 transporta20538caracteres de trechos exatos e passou selected=kimi.
Memória científica comum permanece ampliada pelo adaptador. Isso não é uma
nova chamada nem alteração de infraestrutura/cota; falha v3 preservada.

Snapshot oficial:5 pedidos registrados não terminais (Kimi2,MiMo2,DeepSeek1)
e10 ainda em staging (Kimi5,MiMo5). MiMo model_input em execução; os demais
aguardam. Worker único segue preenchendo vagas, com mesma ordem e IDs.
Registrar/preparar não significa executar ou obter resposta.

Dois resultados Kimi já concluídos foram recuperados sem repetição:
temporal317370entrada/21299saída, cohomology317625entrada/24438saída;
os recibos completos estão em A7/received_reviews. Custos vieram null e
continuam desconhecidos, não zero. Revisão local integral ainda pendente;
as ressalvas da coordenação são pistas de auditoria, não prova incorporada.

Conferidos por hash{len(verified)} artefatos científicos únicos nas seis
entregas desta rodada. R1principal completado com470identidades,800skew,
3laços fora do plano e7negativos. Q2finita continuaOPEN. Custo externo parcial
deduplicado conhecidoUS${total}; não é fatura nem total com custos desconhecidos.
Nenhum original, kernel, gate ou infraestrutura alterado. GoalACTIVE.
'''
save(OUT/'ENTREGA_016_A7_orquestracao_complemento_BV.md',report)
failure=json.loads((HERE/'orchestration_primitive_v3/LOCAL_PREVIEW_FAILURE.json').read_bytes())
measure=f'''[REAL — prévia local recusada antes da submissão]
# A7 — projeção do pedido Kimi
Abertura SHA256 `{opening}`.
Comando: C:/Python314/python.exe -X utf8 -B A7/prepare_primitive_review_v3.py.
rc1: {failure['exception']}.
Prompt{failure['prompt_chars']}caracteres. Evidência estruturada
orchestration_primitive_v3/LOCAL_PREVIEW_FAILURE.json,
SHA256{sha(HERE/'orchestration_primitive_v3/LOCAL_PREVIEW_FAILURE.json')}.
Não há arquivo stdout capturado dessa tentativa; traceback foi devolvido pela
ferramenta exec_command. Nenhuma chamada externa. Próximo passo executado:
prepare_primitive_review_v4.py, rc0,20538caracteres,selected=kimi; mesma missão,
fontes com faixas ehashes, mesmoID; preservado o payload recusado.
'''
save(OUT/'ENTREGA_016_MEDIDA_previa_Kimi_contexto_v3.md',measure)
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',latest_orchestration=snapshot,
    new_prepared_reviews=str(HERE/'orchestration_completion/prepared_units.json'),
    prepared_primitive_reviews_status='V4_RECONCILED_STAGING_AFTER_MARKED',
    partial_metered_cost_usd=total,latest_verified_artifacts=len(verified),
    recovered_kimi_reviews=['ba337b71-5345-44e7-8481-04a24ba1569e','1cb94397-825d-4005-8dc1-933481d302c0'])
d['completed_this_turn'].append('Two new Kimi/MiMo complementary reviews staged; primitive updated v4 before submission; two Kimi results recovered without rerun')
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — ORQUESTRAÇÃO:2novas unidadesKimi/MiMo confirmadas em staging; snapshot5registrados+10preparados. Kimi primitivev4mesmoID;v3prévia recusada preservada. DoisKimi recebidos semnovaexecução. CustoparcialUS${total};{len(verified)}artefatos revalidados. Abertura{opening}.\n'.encode())
print(json.dumps(snapshot,ensure_ascii=False))
