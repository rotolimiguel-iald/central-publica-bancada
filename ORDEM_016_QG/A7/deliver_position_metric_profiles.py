"""Custody and operational continuity for position bubble profiles; no model call."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
from fractions import Fraction as F
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b)
    assert b and tmp.read_bytes()==b;tmp.replace(p)
def read(rel):return json.loads((H/rel).read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
flat=read('position_metric_flat/results.json');curve=read('position_metric_curvature_v2/results.json');pot=read('position_metric_potential/results.json')
catalog=read('orchestration_position_metric/prepared_units.json')
verified=[]
for rel in ['position_metric_flat/manifest.json','position_metric_curvature_v2/manifest.json','position_metric_potential/manifest.json']:
    for f in read(rel)['files']:
        assert sha(Path(f['path']))==f['sha256'],f['path'];verified.append(f['path'])
assert pot['coefficients']==read('metric_curvature_vertices/results.json')['K_bubble_cross_coefficients']
for unit in catalog:
    assert sha(Path(unit['payload']))==unit['payload_sha256']
    payload=json.loads(Path(unit['payload']).read_bytes())
    assert payload['request_id']==unit['request_id']
    assert payload['execution_constraints']['required_provider']==unit['selected']
assert curve['log_coefficients']==['0']*5
pc=list(map(F,pot['coefficients']));cc=list(map(F,curve['curvature_coefficients']))
combined=[cc[0]+pc[0],cc[1]+pc[1],cc[2]+pc[2],cc[3]+pc[2],cc[4]+pc[3]]
report=f'''[DERIVED — perfil radial local; REAL — CAS exato; OPEN — conversão covariante e Q2]
# A7.b — contração da bolha métrica em posição
Abertura SHA256 `{opening}`. UTC {now}.

**Resultado novo:** o motor de vértices diferenciados50x50 foi contraído
com os jatos tensoriais nas duas pontas e o volume em coordenadas normais.
O limite plano reproduz os cinco coeficientes obtidos em momentos. O primeiro
teste conferiu7500 componentes dos jatos e cinco valores de laço: total
{flat['checks']} checks, rc0, CPU{flat['cpu_seconds']}s.

O teste ampliado conferiu a decomposição de40 vértices com momentos
independentes, três contrações explícitas por quatro índices, os100 pares
ordenados da fibra e três pares com momento fora do eixo. Inclui controles
de homogeneidade radial. Total{curve['checks']} checks, rc0,
CPU{curve['cpu_seconds']}s. A cubatura racional integra monômios até grau8;
a contagem de derivadas limita o plano a8 e a primeira curvatura a6.

**Correção preservada:** a tentativa inicial presumiu quatro invariantes
simétricos no perfil radial; falhou com `Linear system has no solution`,
rc1 após45.234375s de CPU medidos na última linha. O perfil deixa X eY
em posições diferentes: integra X, ancora Y e usa o quadro radial de Y.
O teste v2 permite separadamente (pAp)trB e(pBp)trA, sem alterar o motor.
O fracasso antigo e seu hash permanecem; não foi forçado um coeficiente.

Retirando K*A0, A0=1/(8*pi²), na base ordenada

    [p²trAB, p²trA trB, (pAp)trB, (pBp)trA, pABp],

a bolha com dois vértices derivativos fornece

    {curve['curvature_coefficients']}.

O coeficiente angular de log(mu²z), mantido até o fim, resultou zero
nos cinco invariantes. Isto não diz que todas as partes finitas ou todos
os diagramas estão livres de log; diz apenas o que este perfil retornou.
Os dois coeficientes mistos diferentes são um aviso para não confundir
esse perfil com a Hessiana covariante integrada autoadjunta.

**Controle independente de potencial:** incluídos os dois posicionamentos
de um vértice cúbico do potencial e um derivativo, com propagadores principais,
a conta em posição reproduz {pot['coefficients']} na base simétrica
anterior. {pot['checks']} pares, rc0, CPU{pot['cpu_seconds']}s. A tabela
foi cotejada com os bytes do resultado em momentos, sem reajuste de fatores.
Somada somente essa parcela ao perfil derivativo, a base ordenada dá

    {list(map(str,combined))}.

Normalização: bolha bruta/A0; NÃO inclui o peso-1/2 da Hessiana efetiva.
As parcelas de inserçãoE já estão no parametrix e não devem ser somadas
novamente. O tadpole quartico previamente pago é outra contribuição.

**Escopo pendente:** converter estes perfis em operador covariante com
derivadas ordenadas e adjuntos; verificar o termoK² completo; combinar
ghost/fonteBV/tadpole; tratar extensão finita, estado e cutoff. Nenhuma
anomalia causal completa ou fechamento físico é inferido. Gate intacto.

**Distribuição adicional:** Kimi recebe a tarefa de conversão radial→covariante;
MiMo recebe auditoria independente da contração esparsa/sinais/grauangular.
As prévias selecionaram os provedores exigidos. A coordenadora confirmou
staging APÓS metric_quartic, com nove unidades aguardando vaga e cinco
registradas no snapshot; uma chamada MiMo em andamento. Estas duas novas
unidades ainda NÃO foram executadas. Os resultados acima não foram enviados
aos revisores. Fontes, hashes, IDs e memória comum constam no catálogo.
'''
rp=O/'ENTREGA_016_A7b_perfis_radiais_bolha_metrica.md'
assert not rp.exists();save(rp,report)
save(H/'position_metric_curvature_v2/DERIVACAO.md',report)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_POSITION_METRIC_RADIAL_PROFILES',at=now,provider='local',target='A-7.b',
    checks=flat['checks']+curve['checks']+pot['checks'],cpu_seconds=flat['cpu_seconds']+curve['cpu_seconds']+pot['cpu_seconds'],
    failed_attempt_cpu_last_observed_seconds=45.234375,report_sha256=sha(rp),new_external_execution=False,full_Q2=False)]
for unit in catalog:
    events.append(dict(event='A7_POSITION_METRIC_ADDITIONAL_UNIT_STAGED',at=now,target='A-7.b',provider=unit['provider'],
        request_id=unit['request_id'],payload_sha256=unit['payload_sha256'],status='STAGED_NOT_SUBMITTED',
        external_execution_started=False,cost_usd=None,source='Official coordinator message; staging9'))
for e in events:
    marker=(e['event'],e.get('request_id'))
    if not any((r.get('event'),r.get('request_id'))==marker for r in [json.loads(t) for t in raw.decode('utf-8-sig').splitlines() if t.strip()]):
        raw+=(json.dumps(e,ensure_ascii=False)+'\n').encode()
save(ledger,raw)
rows=[json.loads(t) for t in ledger.read_text('utf-8-sig').splitlines() if t.strip()];parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for e in rows:
    ix=ids(e)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for e in rows:
    ix=ids(e);v=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
cost=sum(known.values(),Decimal(0))
save(H/'position_metric_curvature_v2/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),ledger_sha256=sha(ledger),unknown_cost_not_zero=True))
rels=['position_metric_bubble_engine.py','position_metric_flat_check.py','position_metric_flat_run.log',
    'position_metric_flat/PRE_REGISTER.json','position_metric_flat/results.json',
    'position_metric_curvature_check.py','position_metric_curvature_run.log','position_metric_curvature/PRE_REGISTER.json',
    'position_metric_curvature_check_v2.py','position_metric_curvature_v2_run.log','position_metric_curvature_v2/PRE_REGISTER.json',
    'position_metric_curvature_v2/raw_values.json','position_metric_curvature_v2/results.json','position_metric_curvature_v2/DERIVACAO.md',
    'position_metric_potential_check.py','position_metric_potential_run.log','position_metric_potential/PRE_REGISTER.json','position_metric_potential/results.json',
    'prepare_position_metric_units.py','orchestration_position_metric/prepared_units.json','position_metric_curvature_v2/COST_SNAPSHOT.json']
files=[H/r for r in rels]+[Path(__file__),rp]
for unit in catalog:
    files.extend([Path(unit['payload']),H/'orchestration_position_metric'/(unit['slug']+'_preview.json'),H/'orchestration_position_metric'/(unit['slug']+'_receipt.json')])
manifest=H/'position_metric_curvature_v2/delivery_manifest.json'
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Position jets/planar loop7505checks','Ordered firstK radial profile157checks, including100pairs','Mixed potential loop55pairs reproduced','Two additional provider units previewed and staged'],
    latest_orchestration=dict(at=now,source='Official coordinator message',registered=5,staging=9,currently_executing='MiMo marked_wick_audit',execution_job='ab543117-b279-407c-8d0a-6d036b234b1b',execution_id='e83a530b-1b85-4374-8990-b60047f59eaa'),
    pending_orchestration='5registered/9staging; worker owns transitions; no duplicate calls',
    position_metric_profile_manifest=str(manifest),position_metric_review_catalog=str(H/'orchestration_position_metric/prepared_units.json'),
    partial_metered_cost_usd=str(cost),
    previous_turn_failure='Four symmetric invariants insufficient for ordered radial profile; v2 uses five without changing engine; v1 retained',
    next=['Convert radial firstK profile to ordered covariant operator; compare adjoints, use independent scalar/tensor jets, no forced Ward',
          'K2/full finite causal BV sum remain; no double counting E insertions',
          'Keep nine staged units and five registered jobs independent; recover terminal responses only by IDs',
          'A7.c only after24h; A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: posição7505+157+55checks; CPU{events[0]["cpu_seconds"]}s + falha45.234375s observados. PerfilK ordenado, Q2OPEN. Kimi/MiMo +2staging(nove aguardam). Custo parcialUS${cost},desconhecidosnãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),verified_artifacts=len(files),checks=events[0]['checks'],cost_partial=str(cost),status='PROGRESS')))
