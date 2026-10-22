"""Record pointwise loop computations and accepted orchestration, with custody."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
from fractions import Fraction
import hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1]
O=C/'TUNEL/DO_CHATGPT';BASE=C/'IALD_ORQUESTRACAO_20260923'
D=H/'bilocal_point_delivery'
now=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if isinstance(b,str):b=b.encode('utf-8')
    if p.exists():
        assert update,p
        previous=p.read_bytes()
        backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8])
        backup.write_bytes(previous);assert backup.read_bytes()==previous
    else:previous=None
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b and len(b)>0;t.replace(p)
    assert p.read_bytes()==b
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2),update)
names=['bilocal_ghost_pair','bilocal_metric_pair_v2','transvection_bilocal_identity','transvection_endpoint_recurrence']
rs={n:json.loads((H/n/'results.json').read_bytes()) for n in names}
for n in names:
    m=json.loads((H/n/'manifest.json').read_bytes())
    for row in m['artifacts']:assert sha(Path(row['path']))==row['sha256'],row['path']
assert rs['bilocal_metric_pair_v2']['status']=='METRIC_LOOP_Y_DIVERGENCE_POINT_EXACT_MEASURED'
g=rs['bilocal_ghost_pair']['values'];m=rs['bilocal_metric_pair_v2']['values']
combined=[[[str(Fraction(g[o][b][ell])-Fraction(m[o][b][ell])/2) for ell in (0,1)]
          for b in range(4)] for o in (0,1)]
checks=sum(r['checks'] for r in rs.values())
cpu=sum(r['cpu_seconds'] for r in rs.values())
old=json.loads((H/'bilocal_metric_pair/results.json').read_bytes())
cpu_all=cpu+old['cpu_seconds']
D.mkdir(exist_ok=True)
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
accept=BASE/'state/handoffs/a7_bilocal_completion_v2_pending_submissions.json'
acceptance=json.loads(accept.read_bytes())
catalog=H/'orchestration_bilocal_completion_v2/prepared_units.json'
assert sha(catalog)==acceptance['catalog_sha256']
for row in acceptance['units']:assert sha(Path(row['source']))==row['payload_sha256']
write(D/'COORDINATOR_ACCEPTANCE.json',accept.read_bytes())
infra=BASE/'validation/provider_parallelism_delivery.json'
receipt=json.loads(infra.read_bytes())
assert receipt['status']=='ACTIVE_TWO_DISTINCT_PROVIDERS_RUNNING'
write(D/'PARALLELISM_RECEIPT.json',infra.read_bytes())
incoming=BASE/'state/handoffs/96648157-7424-49ad-b606-6cafe72b9988_delivery.json'
kr=json.loads(incoming.read_bytes());response=kr['result']
write(D/'KIMI_QUARTIC_RESPONSE.md',response['text'])
put(D/'KIMI_QUARTIC_RECEIPT.json',dict(at=kr['at'],job_id=kr['job_id'],
 execution_task_id=kr['execution_task_id'],model=response['model'],usage=response['usage'],
 source_receipt_sha256=sha(incoming),response_sha256=sha(D/'KIMI_QUARTIC_RESPONSE.md'),
 status='DECLARADO_PENDING_LOCAL_AUDIT',coordinator_text_review=kr['local_review'],
 review_scope=kr['review_scope'],cost_status='SUBSCRIPTION_COST_UNKNOWN_NOT_ZERO'))
put(D/'combined_point.json',dict(at=now,point=[1,0,0,0],external_h='e11',external_Dh=0,
 ghost=g,metric=m,combination='-metric/2+ghost',values=combined,
 shared_propagator_constants_stripped=True,full_Q2=False,source=False,
 contacts=False,tadpoles=False,higher_arities=False))
report=O/'ENTREGA_016_A7b_par_bilocal_pontual_e_orquestracao.md'
write(report,f'''[DERIVED — cálculo pontual dos candidatos; verificações exatas locais; Q2 permanece OPEN]

# Par bilocal e ampliação da orquestração

Data: {now}. Abertura SHA256: {opening}.

## Cálculo realizado

Foram inseridos os vértices existentes dos setores fantasma e métrico na
divergência em Y, com diferenciação antes de Y=0. Ponto X=(1,0,0,0),
h_X=e11 no frame ortonormal, Dh_X=0. Os resultados guardam as normalizações
dos motores; constantes comuns dos propagadores estão removidas.

| componente longitudinal, sem log | K0 | K1 |
|---|---:|---:|
| fantasma | {g[0][0][0]} | {g[1][0][0]} |
| métrico bruto | {m[0][0][0]} | {m[1][0][0]} |
| combinação −métrico/2+fantasma | {combined[0][0][0]} | {combined[1][0][0]} |

Os três componentes transversais e os coeficientes logarítmicos se anulam
neste ponto/jato. O valor não nulo acima NÃO é uma anomalia calculada:
faltam fonte Einstein na mesma orientação, jatos Dh_X, extensão/contatos,
parte suave, tadpoles e aridades restantes. A revisão independente das
conversões de frame está encomendada; os testes não substituem essa revisão.

Ghost: {rs['bilocal_ghost_pair']['checks']} verificações, CPU
{rs['bilocal_ghost_pair']['cpu_seconds']}s, rc0. Métrico v2:
{rs['bilocal_metric_pair_v2']['checks']} verificações, CPU
{rs['bilocal_metric_pair_v2']['cpu_seconds']}s, rc0.
O v1 também terminou rc0, mas criou floats ao dividir por 16 uma soma vazia.
Seu valor curvo {old['values'][1][0][0]} não foi promovido a igualdade exata.
V2 usa Fraction antes da divisão e exige tipos racionais nas saídas.
O v1 e sua errata permanecem preservados, com seus hashes.

## Recorrência derivada

A transvecção k_i^a=delta_i^a−K(X²delta_i^a−XaXi)/3 satisfaz Killing.
As derivações de Lie simultâneas anulam os kernels bilocais truncados:
1.152 verificações simbólicas, dois controles negativos. Delas se obtém,
para os índices inferiores b no extremo Y,

    DY_i G|0 = −LX_i G|0
    DY_j DY_i G|0 = LX_i LX_j G|0
      + K sum_slots(delta_jb G[b→i] − delta_ib G[b→j])|0 + O(K²).

A segunda fórmula foi conferida em 200 identidades de componentes,
simbólicas em X, e dois controles negativos. A demonstração escrita está
em transvection_endpoint_recurrence/DERIVACAO.md. Seu uso em bitensores
com índices derivativos adicionais ainda exige incluir esses índices.

## Orquestração

Duas novas unidades Kimi e uma MiMo aceitas em staging, com request_id,
hashes e previews no catálogo orchestration_bilocal_completion_v2. O
catálogo sem v2 está excluído: sua segunda prévia ultrapassou 24.000
caracteres antes de qualquer submissão. O primeiro pedido manteve seu ID.

A coordenação implantou até três execuções entre fornecedores distintos,
uma por Kimi/MiMo/DeepSeek, mantendo fila única e cinco não terminais.
Recibo registra Kimi e MiMo running simultaneamente; não equivale a
conclusão. Testes relatados: 34 focados e 52 de regressão; quatro testes
web não rodaram por falta de Flask naquele Python. Não houve interrupção
da chamada antiga, duplicação de pedido ou novo heartbeat.

Total local desta entrega: {checks} verificações reportadas (não teoremas
independentes), CPU {cpu}s; incluindo o v1 numérico, CPU {cpu_all}s.
Nenhum original, kernel ou gate alterado. Próximo ramo: mesma identidade
bilocal com fonte e domínio de jatos completo, dentro do timebox A7.b.
''')
files=[Path(__file__),report,D/'combined_point.json',D/'COORDINATOR_ACCEPTANCE.json',D/'PARALLELISM_RECEIPT.json',
 D/'KIMI_QUARTIC_RESPONSE.md',D/'KIMI_QUARTIC_RECEIPT.json',
 H/'bilocal_ghost_pair_engine.py',H/'bilocal_metric_pair_engine.py',H/'bilocal_metric_pair_engine_v2.py',
 H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py',
 H/'METRIC_PAIR_EXACTNESS_ERRATUM.json',H/'prepare_metric_pair_exact_v2.py',
 H/'transvection_endpoint_recurrence/DERIVACAO.md',catalog,
 H/'prepare_bilocal_completion_units.py',H/'prepare_bilocal_completion_units_v2.py',
 H/'orchestration_bilocal_completion/SUPERSEDED.json']
for n in names+['bilocal_metric_pair']:
    files += [H/n/x for x in ('PRE_REGISTER.json','results.json','manifest.json')]
for n in ['bilocal_ghost_pair','bilocal_metric_pair','bilocal_metric_pair_v2',
          'transvection_bilocal_identity','transvection_endpoint_recurrence']:
    runner=H/(n+'_check.py')
    if n=='bilocal_metric_pair_v2':runner=H/'bilocal_metric_pair_check_v2.py'
    files += [runner,H/(n+'_run.log')]
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=checks,cpu_seconds=cpu,
 cpu_including_numeric_predecessor=cpu_all,full_Q2=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ledger=O/'LEDGER_016.jsonl';events=[]
for row in json.loads(catalog.read_bytes()):
    payload=json.loads(Path(row['payload']).read_bytes())
    events.append(dict(at=now,event='A7_BILOCAL_COMPLETION_REVIEW_STAGED',target='A7.b',
      provider=row['provider'],lemma_id=row['lemma'],request_id=row['request_id'],
      prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
      payload_sha256=row['payload_sha256'],status='ACCEPTED_STAGING_NOT_SUBMITTED',
      remote_call=False,tokens=None,cost_estimate_usd=None))
events.append(dict(at=now,event='A7_BILOCAL_POINT_EXACT_AND_TRANSVECTION_DELIVERED',
 target='A7.b',checks=checks,cpu_seconds=cpu,cpu_including_numeric_predecessor=cpu_all,
 full_Q2=False,delivery_manifest_sha256=sha(D/'manifest.json')))
events.append(dict(at=now,event='KIMI_METRIC_QUARTIC_RECEIVED_PENDING_LOCAL_AUDIT',
 target='A7.b',provider='kimi',job_id=kr['job_id'],execution_task_id=kr['execution_task_id'],
 tokens=response['usage'],cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',
 response_sha256=sha(D/'KIMI_QUARTIC_RESPONSE.md'),status='DECLARADO_PENDING_LOCAL_AUDIT'))
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and cost is not None:known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,known_partial_usd=str(total),unknown_not_zero=True,ledger_sha256=sha(ledger)))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: par bilocal calculado num ponto/jato; recorrência Killing derivada. {checks}checks; CPU{cpu_all}s incluindo v1float preservado. Três revisões novas aceitas; coordenação ativou Kimi/MiMo paralelos. Custo parcialUS${total}; desconhecidos não zerados. Q2 OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',own_live_processes=[],
 bilocal_point_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),
 completed_this_turn=['Ghost and metric endpoint loop at one point/hX jet; exact v2 corrects empty-sum float',
 'Simultaneous Killing covariance and first/second endpoint recurrence derived and checked',
 'Two Kimi plus one MiMo new units accepted; single queue now parallel distinct providers'],
 next=['Review Kimi metric_derivative_quartic result96648157; do not repeat',
 'Use Killing recurrence including derivative slots to accelerate full bilocal jets',
 'Compute source in same orientation; complete Dh_X and distribution/contact terms',
 'A7.b deadline around20:32UTC then A7.c/d,A8,PartB/final; goal remains active'])
v['latest_orchestration']=dict(at=now,accepted_new_catalog=str(catalog),
 active_pairs=receipt['activation_evidence'],coordinator_owned_session=48008,
 global_max=3,per_provider=1,max_nonterminal=5,source=str(D/'PARALLELISM_RECEIPT.json'))
v['latest_live_execution']=dict(status='LEGACY_COMPLETED_NEW_KIMI_AND_MIMO_RUNNING',
 legacy_job_id=receipt['legacy_job'],new_jobs=[r['job_id'] for r in receipt['activation_evidence']],
 session_id_owned_by_coordinator=48008,observed_utc=now)
v['bilocal_completion_catalog']=str(catalog)
v['kimi_quartic_received']=str(D/'KIMI_QUARTIC_RESPONSE.md')
put(p,v,True)
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,cpu_including_v1=cpu_all,
 artifacts=len(files),combined=combined,partial_known_cost_usd=str(total),goal='ACTIVE')))
