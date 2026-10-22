"""Deliver the checked endpoint derivative/IBP stage and current queue receipt."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'bilocal_covariant_jets_delivery';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if p.exists():
        assert update,p;old=p.read_bytes()
        backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode(),update)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'bilocal_covariant_jets_v2/results.json').read_bytes())
report=O/'ENTREGA_016_A7b_derivadas_covariantes_dois_extremos.md'
write(report,f'''[DERIVED — integração por partes; REAL — CAS exato; OPEN — soma de Ward]
# A7.b — derivar antes de ancorar
Abertura SHA256 `{opening}`. UTC {now}.

Implementado o cálculo de jatos covariantes no extremo Y dos propagadores
bilocais, mantendo todos os índices de derivadas como slots tensoriais.
O ghost tem índice superior em X, com sinal positivo da conexão; os
índices em Y são inferiores. O tensor métrico carrega dois em cada extremo.
O auxiliar w=(X-Y)² só é imposto depois das derivadas e da ancoragem.

Os comutadores [D_i,D_j] no extremo Y foram cotejados com a ação explícita
de R^a_bij/K=delta_ai delta_bj-delta_aj delta_bi:232 identidades simbólicas,
com todos os componentes ghost e os100 componentes simétricos métricos,
para os pares de derivadas(0,1) e(1,3). Isso testa os pares especificados;
não é uma afirmação de execução exaustiva para toda palavra arbitrária.

**Redução que será aplicada aos laços.** Considere a contribuição bilocal,
com o teste em X absorvido nos coeficientes e k=G(c) em Y:

 B[h,k]=int dvolX dvolY [B0^(ab) k_ab+B1^(jab) D_j k_ab],
 B0 e B1 simétricos nos últimos índices a,b.

Para c compacto, a integração por partes dá o coeficiente de c_b:

 W^b=2[-D_a B0^(ab)+D_a D_j B1^(jab)].

Em Y=0 de UMA carta RNC fixa, a primeiraK:

 W^b=2[-partial_a B0^(ab)+partial_a partial_j B1^(jab)]
      +K[8/3 sum_a B1_0^(aab)-2/3 sum_a B1_0^(baa)]+O(K²).

Os coeficientes B são componentes coordenadas ANTES de ancorar. Os termos
adicionais vêm da derivada da conexão na primeira divergência. Escrever
Gamma(0)=0 e descartar suas derivadas apagaria esses termos. A simplificação
usa a conexão RNC da bancada e a simetria a,b; não aplica dY=-dX.

**Controle independente.** Expandiu-se a forma fraca em c_b, partial_i c_b
e partial_i partial_j c_b, mantendo sqrt(g)=1-KY²/2. A derivada de Euler
coordenada foi comparada ao motor de divergências. Os oito coeficientes
(quatro componentes, ordensK0/K1) coincidiram em campos polinomiais racionais.
Suprimir as derivadas da conexão dá resíduos304/3,344/3,128,424/3 nesses
campos: quatro controles negativos. Não foram ajustados coeficientes de laço.

O primeiro checker falhou em rc1 porque extraiu coeff(K,0) de expressão
ainda não expandida; v2 expande antes de extrair. O motor foi preservado,
assim como o log falho. O v2 terminou rc0,240 checks,CPU{r['cpu_seconds']}s.
O custo da tentativa v1 não foi medido. Fontes e logs no manifesto.

**Limite preciso:** B0/B1 ainda não foram preenchidos pelos vértices Wick
completos. Esta etapa fornece a redução e o motor de derivadas; não fornece
o coeficiente totalQ2. Os contatos do regulador, tadpoles, W e aridades
superiores continuam separados. Próximo: inserir os pares métricos/ghost
no mesmo cálculo, depois comparar com a fonte Einstein na mesma prescrição.

Orquestração: a revisão MiMo0e8fc209 terminou IncompleteRead, sem resultado,
uso/custo desconhecidos; não repetida. A coordenação informou início único
do Kimi96648157 (quartico métrico), sessão28410 de sua propriedade.
Nenhum original, kernel ou gate alterado. A7.b continua ativo no timebox.
'''.encode())
failure=C/'IALD_ORQUESTRACAO_20260923/state/handoffs/0e8fc209-ca23-4868-bac3-bc5b053936bf_delivery.json'
raw=failure.read_bytes();failed=json.loads(raw);write(D/'MIMO_FAILURE_RECEIPT.json',raw)
files=[Path(__file__),report,H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py',
 H/'bilocal_covariant_jet_check.py',H/'bilocal_covariant_jet_run.log',
 H/'bilocal_covariant_jet_check_v2.py',H/'bilocal_covariant_jet_v2_run.log',D/'MIMO_FAILURE_RECEIPT.json',
 H/'bilocal_covariant_jets/PRE_REGISTER.json',H/'bilocal_covariant_jets_v2/PRE_REGISTER.json',
 H/'bilocal_covariant_jets_v2/results.json',H/'bilocal_covariant_jets_v2/manifest.json']
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=r['checks'],negative_controls=len(r['negative_controls']),
 cpu_seconds=r['cpu_seconds'],full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ledger=O/'LEDGER_016.jsonl'
events=[dict(at=now,event='A7_BILOCAL_COVARIANT_JETS_DELIVERED',target='A7.b',checks=r['checks'],
 negative_controls=len(r['negative_controls']),cpu_seconds=r['cpu_seconds'],full_Q2=False,
 delivery_manifest_sha256=sha(D/'manifest.json')),
 dict(at=now,event='MIMO_GHOST_SKEPTIC_TERMINAL_FAILURE_RECEIVED',target='A7.b',provider='mimo',
 job_id=failed['job_id'],execution_task_id=failed['execution_task_id'],tokens=None,cost_estimate_usd=None,
 cost_status='UNKNOWN_NOT_ZERO',error=failed['error'],result=None,retried=False,receipt_sha256=sha(failure))]
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
parents={};rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and cost is not None:known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,ledger_sha256=sha(ledger),known_partial_usd=str(total),unknown_not_zero=True))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: jatosY covariantes e integração por partes bilocal conferidos240checks/4negativos,rc0,CPU{r["cpu_seconds"]}s. V1coeficiente não expandido falhou e permanece. MiMo0e8fc falhou terminal/uso desconhecido,semrepetição. Custo parcialUS${total}; Q2 OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',bilocal_covariant_jets_manifest=str(D/'manifest.json'),own_live_processes=[])
v['completed_this_turn']+=['Two-endpoint covariant jets and generic Ward integration by parts:240checks/4negatives; loop coefficients not inserted yet']
v['latest_live_execution']=dict(job_id='96648157-7424-49ad-b606-6cafe72b9988',
 status='COORDINATOR_REPORTED_EXECUTING',session_id_owned_by_coordinator=28410,observed_utc=now)
v['next']=['Use bilocal_covariant_jet_engine to insert loop B0/B1 before anchoring; current generic IBP formula checked',
 'Do not repeat failed MiMo0e8fc; new Kimi96648157 owned by coordinator',
 'Review corrected gamma/F² report; old integrated ghost density unchanged',
 'A7.b deadline approximately20:32UTC then A7.c/d,A8,PartB/final; goal active']
put(p,v,True)
for item in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(artifacts=len(files),checks=r['checks'],negative_controls=len(r['negative_controls']),cpu_seconds=r['cpu_seconds'],goal='ACTIVE')))
