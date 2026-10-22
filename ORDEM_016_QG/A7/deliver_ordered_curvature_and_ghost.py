"""Deliver ordered curvature Hessian and direct ghost control; preserve gaps."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def read(rel):return json.loads((H/rel).read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
folders=['radial_covariant_second_jet','position_metric_ordered_operator_probe','position_metric_ordered_second','ghost_direct_position','ghost_direct_vertex_audit']
results={f:read(f+'/results.json') for f in folders};files=[]
for folder in folders:
    for a in read(folder+'/manifest.json')['files']:
        p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
    files.append(H/folder/'manifest.json')
checks=sum(r.get('checks',0) for r in results.values());cpu=sum(r['cpu_seconds'] for r in results.values())
ghost=results['ghost_direct_position'];second=results['position_metric_ordered_second']
assert ghost['flat_matches'] and all(v=='0' for v in ghost['difference'])
assert all(v['difference']=='0' for v in results['position_metric_ordered_operator_probe']['values'])
rp=O/'ENTREGA_016_A7b_operador_ordenado_K2_e_ghost_direto.md';assert not rp.exists()
save(rp,f'''[DERIVED — símbolo logarítmico local; REAL — controles CAS; OPEN — Q2 completa]
# A7.b — operador ordenado K² e controle ghost direto
Abertura SHA256 `{opening}`. UTC {now}.

**Ordenamento explícito.** A expansão de Taylor covariante atua em A
ou em nabla_i A, conforme o vértice. Se a perna B carrega nabla_j,
transfere-se por partes com sinal− e aplica-se nabla_j a TODO o jato,
inclusive seus índices de derivada. Não se troca esse resultado por
derivadas totalmente simétricas antes de avaliar os comutadores.

O motor novo usa o coframe e=I−KN/6+K²zN/120, N=zI−xx, e a conexão
do espaço-forma até K². São20759 controles: comparação de K0/K1 com
a construção anterior, anulação dos Taylor totalmente simétricos K²,
paralelismo da métrica e comutador de curvatura.388 jatos K² não nulos
foram observados nas duas polarizações não escalares testadas.

Como controle anterior à nova ordem, a contração direta reproduziu
a bolha primeiraK nos pares (01,01):22/9 e (00,11):−4.
Esses dois probes não substituem a auditoria de100 pares anterior.

**Resultado K² integrado:** na base[tr(AB),tr(A)tr(B)] e após retirar
hbar*A0*K², com A0=1/(8pi²), a construção fornece

| setor | coeficientes |
|---|---|
| bolha métrica bruta | {second['raw_metric']} |
| métrica:−1/2 bolha + tadpole | {second['metric_with_tadpole']} |
| ghost | {second['ghost']} |
| total | {second['total']} |

Os dois coeficientes foram determinados por (01,01) e (00,11).
(00,00) e (11,00) ficaram como controles posteriores e concordaram;
o coeficiente explícito log(z) foi zero nos quatro casos. A estrutura
de dois invariantes decorre da covariância O(4) da construção no ponto,
não de uma reivindicação de varredura numérica de todas as fibras.

O perfil radial anterior era[141,−81/4], ANTES dos adjuntos.
A diferença até o operador integrado é[−97,97/4]. No setor A=B=g
ela anula: a métrica é paralela. A soma nova total nessa direção é−72.
Não apagar o perfil anterior nem apresentá-lo como resultado integrado.

**Ghost sem fatorar o determinante.** Foi calculada a bolha diretamente
do vértice −(nabla_mu barc_nu) vezes a variação de gauge de h com
subtração do traço. A contração dirigida usa o transposto do segundo
vértice; não é a contração de dois vértices métricos simétricos.
O vértice coincide com o Q1 polinomial já existente em160 componentes;
reciprocidade dos Green e não-simetria do vértice completam1361 controles.

Seis pares reproduziram a referência plana. Na primeiraK, cinco
invariantes e um sexto par de controle deram exatamente

    [41/36,−7/3,26/9,26/9,−35/6],

iguais à redução do determinante anterior. As diferenças são todas0;
log(z) também0. Portanto essa fatoração NÃO explica, neste recorte,
o resíduo Ward primeiraK. Essa hipótese foi testada e não sustentada;
o resíduo continua sem alteração. Não houve ajuste para zerá-lo.

**MiMo:** recuperado o mesmo job70db6729-942c-4435-92e6-482d3d842134,
execb592a019-d0ce-4412-b4b4-f27242cedb4f, sem nova chamada. O parecer
é favorável a−571K²/15 no calor livre do fundo fixo e permanece
DECLARADO (revisão textual). Não é Hessiana nem cancelamento Ward.
Correções de justificativa: [E,A]=0 isoladamente não elimina todos
os produtos cruzados; precisam-se ordem em x, paralelismo e traços da
representação concreta. A(0)=0 também não elimina suas derivadas.
O fator(4pi)^−2 e o sinal da integral que define logdet são separados.
Os controles locais anteriores sustentam o valor com esse escopo.

Neste pacote:{checks} asserções exatas, mais2 comparações métricas
e6+6 comparações ghost documentadas; CPU{cpu}s; cinco execuções rc0.
O manifesto agrega as fontes e logs sem sobrescrever predecessores.

**Ainda aberto:** Ward com contatos finitos, cutoff, estado e a
hierarquia temporal especificada; Wess–Zumino/cohomologia completos.
A conta logarítmica não substitui essa aceitação. Segue a verificação
das ordens de Ward restantes e dos contatos. Nenhum gate/kernel/original
alterado, nenhum resultado repassado aos revisores independentes em fila.
''')
mp=O/'ENTREGA_016_MEDIDA_fatoracao_ghost_primeiraK.md';assert not mp.exists()
save(mp,f'''[REAL — comparação exata; OPEN — causa do resíduo Ward]
Abertura SHA256 `{opening}`. UTC {now}.

Hipótese testada: a redução Q=M Qtilde e seu determinante seriam a
origem da discrepância Ward primeiraK. Calculei a bolha ghost original,
com vértices dirigidos e propagadores covariantes; não usei a fatoração.
Resultado na mesma base:41/36,−7/3,26/9,26/9,−35/6.
Diferença em relação à Hessiana reduzida:[0,0,0,0,0].
Seis comparações planas e reciprocidade/vértice sustentam a normalização.

Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/ghost_direct_position_check.py.
rc0; CPU{ghost['cpu_seconds']}s; logSHA256 `{sha(H/'ghost_direct_position_run.log')}`.
Não se mede toda anomalia de multiplicatividade possível; neste setor
a diferença procurada não apareceu. Nenhuma chamada externa adicional.
Próximo: ordemK² de Ward, tadpole linear, contatos finitos e hierarquia
causal. Preservar o resíduo primeiraK e os pareceres independentes.
''')
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_ORDERED_K2_AND_DIRECT_GHOST'
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,
    report_sha256=sha(rp),measure_sha256=sha(mp),full_Q2=False,new_external_execution=False))+'\n').encode();save(ledger,raw)
rows=[json.loads(t) for t in raw.decode('utf-8-sig').splitlines() if t.strip()];parents={}
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
logs=['radial_covariant_second_jet_run.log','position_metric_ordered_operator_probe_run.log','position_metric_ordered_second_run.log','ghost_direct_position_run.log','ghost_direct_vertex_audit_run.log']
files+=[H/x for x in logs]+[H/'receive_mimo_free_heat.py',H/'received_reviews/70db6729-942c-4435-92e6-482d3d842134.md',H/'received_reviews/70db6729-942c-4435-92e6-482d3d842134.json',rp,mp,Path(__file__)]
files=list(dict.fromkeys(files));manifest=H/'position_metric_ordered_second/delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',completed_this_turn=['SecondK ordered radial jets20759checks',
    'Ordered metric firstK2pairs agree','SecondK Hessian:metric[-10,-2],ghost[25/6,-25/24]',
    'Direct nonminimalghost matches5firstKcoefficients; vertexreciprocity1361checks','MiMo freeheat recovered and scoped'],
    ordered_curvature_ghost_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    pending_orchestration='Coordinator5registered/6staging; MiMo freeheat completed/recovered; Kimi completion running; DeepSeek logcontact registered',
    latest_live_execution=dict(job_id='b9d7e1a5-06fd-4f6d-8ed8-e82084aff2e8',status='running_reported_by_coordinator',observed_utc=now),
    next=['Ward K² with one-form jets up to fifth derivatives, linear tadpole and existing BV source; preserve firstK residual',
        'Finite temporal prescription: smooth W/cutoff and full Wess-Zumino/cohomology remain open',
        'Do not repeat failed/uncertain calls; current5registered/6staging via single worker',
        'A7.c only after24h if unpaid, then A7.d,A8,PartB and finalaudit'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: operadorK² eghostdireto; {checks}asserções+14comparações, CPU{cpu}s. Fatoração ghostnãoexplicaWardK1;Q2OPEN. MiMofreeheatrecuperado;Kimi completionrunning. Custo parcialUS${cost}, desconhecido≠zero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),measure=str(mp),checks=checks,cpu_seconds=cpu,artifacts=len(files),partial_cost=str(cost))))
