"""Deliver local computations, source corrections and orchestration receipts."""
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
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
def data(rel):return json.loads((H/rel).read_bytes())
ar=data('kimi_curvature_review_audit/results.json')
qr=data('metric_quartic_vertices/results.json')
jr=data('metric_coincident_jet_v2/results.json')
tr=data('metric_derivative_tadpole/results.json')
report=f'''[DERIVED — vértice e log local; REAL — CAS exato; OPEN — bolha métrica curva e Q2]
# A7.b — vértice quártico derivativo e tadpole métrico
Abertura SHA256 `{opening}`. UTC {now}.

**Escopo:** mesmo fundo fixo g, Ric=3K g, Lambda=3K, expansão G=g+h,
ação -(2kappa)^-1 integral sqrt(G)(R(G)-2Lambda), C_g linear. A seção
euclidiana auxilia o coeficiente UV local; não escolhe um estado físico.

**Vértice.** A parte Gamma-Gamma tem duas pernas derivadas e dois campos
sem derivada. Para matrizes A,B não necessariamente comutantes, escreva
W=sqrt(det(I+h))(I+h)^-1, G,T os numeradores de Gamma de primeira ordem.
O segundo diferencial do integrando é

    D²[W (M^-1 G)(M^-1 T)](A,B), M=I+h.

Usam-se D_A M^-1=-A, D²_AB M^-1=AB+BA,
D_A sqrt(det M)=trA/2 e
D²_AB sqrt(det M)=trA trB/4-trAB/2. Somam-se as6 escolhas de pernas sem
derivadas e as2 ordens das pernas derivadas. O código retorna32kappa V4;
não se divide novamente por4!. Integração por partes: módulo divergências,
com cutoff constante. Os contatos de cutoff seguem separados.

Controles:24 permutações Bose; família conforme G=(1+f)g;
V4(Kc,A,B,C)+soma V3(Lc A,B,C)=0; e, com duas pernas g de momento zero,

    32kappa V4(A,p;B,-p;g,0;g,0)=8*(8kappa V2_EH(A,p;B,-p)).

**Jatos do propagador.** Em quadro ortonormal por transporte radial,
D=-(nabla²+E), E=-2K P_TL+6K P_tr, Omega é a curvatura em S²T*.
A conexão foi extraída da métrica e do coframe, não substituída por massas:

    A_i=(K/2-K²r²/24)(x^a delta_ib-delta_ia x_b)+O(K³r5).

Seu divergente covariante e x·A anulam-se nas ordens usadas.
Com u0=1+Kr²/4+19K²r4/480, a recorrência radial fornece

    U1=E+2K I+r²(KE/4+29K² I/60)
       +(1/12)x^i x^j soma_k Omega_ik Omega_jk+… .

O segundo termo de calor diagonal é
a2=E²/2+2KE+29K²I/15+Omega²/12. Aqui a2 multiplica t² (a4 na
convenção por dimensão). A derivada covariante ordenada inclui
Omega_ij(E+2K)/2. Pela identidade de Synge e pela derivada mista do
exponencial de calor, o log de D^-1 tem jato misto A0 L_ij, onde
A0=1/(8pi²) para ln Lambda e

    L_ij=delta_ij(-2P_TL/3+12P_tr)K²
          -(1/12)soma_k{{Omega_ik,Omega_jk}}.

No caso métrico Omega(E+2K)=0. Soma_i L_ii=E(E+2K), conferida;
no caso escalar a fórmula dá delta_ij E(E+2K)/4. O jato sem derivada
é a1=8K P_tr e o jato com uma derivada é zero na referência invariante.
O propagador físico auxiliar preserva GH=4kappa D^-1 I_tr. Na base
simétrica de10 componentes, sua contração inclui a inversa da matriz de
Gram: S0=I_tr Gram^-1. Esquecer esse fator muda os termos fora da diagonal.

**Tadpole da Hessiana efetiva.** O peso é +(1/2)Tr(GH delta²H), logo
(1/2)*4kappa/(32kappa)=1/16. Para pernas externas A,B,p,-p, resulta

    T_AB/(hbar A0)=K[-2p²trAB+2p²trA trB
       -2(pAp trB+pBp trA)+4pABp]+12K²trAB.

O primeiro bloco tem as duas derivadas externas; o segundo tem as duas
internas. O termo com uma derivada interna é zero nessa referência;
o quartico do potencial já dera zero. Portanto o tadpole log total nesse
recorte está calculado; não se afirma que tadpoles finitos ou com W suave
se anulem. Para A=B=g e momento externo zero, o resultado é48K² hbar A0.

**Verificação:** vértice {qr['checks']} checks, jatos {jr['checks']},
tadpole {tr['checks']}, todos rc0. CPU respectivamente{qr['cpu_seconds']}s,
{jr['cpu_seconds']}s,{tr['cpu_seconds']}s. Os55 pares bilineares conferem
os2 invariantes de ordemK²; há controle denso e3 contrações independentes
por extração do polinômio de momento do vértice completo. A primeira
implementação dos jatos falhou por KeyError ao consultar xx[j,i] antes
de preenchê-lo; v1 e log preservados, v2 corrige apenas a ordem da tabela.

**Próximo elo:** contribuições restantes da bolha métrica com correções
dos propagadores e transporte, depois soma com ghost e fonte BV.
Prescrição causal finita, cutoff e Q2 completa permanecem abertos.
Nenhum um.py, kernel, gate ou fonte canônica foi alterado.
'''
rp=O/'ENTREGA_016_A7b_tadpole_metrico_derivativo.md'
save(rp,report);save(H/'metric_derivative_tadpole/DERIVACAO.md',report)
audit=f'''[REAL — auditoria exata; DECLARADO — parecer externo; OPEN — Q2]
# A7.b — revisão local do parecer Kimi sobre curvatura
Abertura SHA256 `{opening}`. UTC {now}.
Parecer recebido: job679d8876-d8b9-44db-ae96-3f8f8f67fb54;
fonte recebida preservada em received_reviews/ com hash no manifesto.

**Aproveitado:** traços de curvatura(-144,-24)K² e peso de calor livre
-571K²/15 coincidem com o cálculo já entregue. A distinção entre conexão
de fibra e dez campos escalares é correta. Não foi refeito esse laço.

**Correções demonstradas:**
1. D=-(nabla²+E) tem símbolo q²-E. Os denominadores são q²+2K
   (sem traço), q²-6K (traço), q²-3K (ghost), não os sinais da seção7.
2. Em coordenadas normais, partial_i g^ij=-Kx^j e
   g^ij partial_i log sqrt(g)=-Kx^j nessa ordem. Somam -2Kx^j;
   não se cancelam. O controleC5 proposto no parecer falha.
3. Duas inserções lineares de Omega têm ordemK². Derivar em momento
   não transforma esse produto em ordemK, mantida a expansão local UV.
4. A simetria maximal não reduz a Hessiana hh a um único Kp²:
   os4 invariantes bilineares usados pela bancada têm posto4.

**Correção de objeto:** o calor livre no fundo on-shell não é a família
de operadores com h externo, nem sua Hessiana. O valor de uma função num
ponto não determina sua segunda derivada. O resultado ghost já entregue
contém, no canal conforme, integral[7(boxf)²/8-19K(df)²/2], condicionado
à sua redução de calor. Portanto não cabe promover o paralelismo do fundo
à ausência desses termos. Momento externo e momento interno do laço
também precisam de nomes separados. O próprio parecer mantém Kq² OPEN.

A fatoração de determinantes finitos e sua fase não é estabelecida apenas
pela comutação com B; regulação e escopo devem acompanhar a afirmação.
A anulação de uma inserção Omega em linha livre isotrópica não prova
anulação numa bolha com vértices tensoriais arbitrários.

{ar['checks']} controles exatos, rc0, CPU{ar['cpu_seconds']}s.
Nenhuma repetição de chamada, novo laço ou alteração de originais/gate.
Os resultados úteis do modelo são preservados; a proposta de símbolo da
seção7 não será usada sem essas correções. Q2 continua aberta.
'''
ap=O/'ENTREGA_016_A7b_auditoria_Kimi_curvatura.md'
save(ap,audit);save(H/'kimi_curvature_review_audit/DERIVACAO.md',audit)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_METRIC_DERIVATIVE_QUARTIC_TADPOLE',provider='local',target='A-7.b',
    checks=qr['checks']+jr['checks']+tr['checks'],
    cpu_seconds=qr['cpu_seconds']+jr['cpu_seconds']+tr['cpu_seconds'],
    report_sha256=sha(rp),full_Q2=False,new_external_execution=False),
    dict(event='A7_KIMI_CURVATURE_LOCAL_REVIEW',provider='local',target='A-7.b',
    checks=ar['checks'],cpu_seconds=ar['cpu_seconds'],report_sha256=sha(ap),
    full_Q2=False,new_external_execution=False)]
catalog=data('orchestration_metric_quartic/prepared_units.json')
for unit in catalog:
    payload=data('orchestration_metric_quartic/'+unit['slug']+'_submit.json')
    events.append(dict(event='A7_QUARTIC_UNIT_STAGED',provider=unit['provider'],target='A-7.b',
        request_id=unit['request_id'],payload_sha256=sha(Path(unit['payload'])),
        prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
        status='COORDINATOR_STAGING_CONFIRMED_NOT_EXECUTED',new_external_execution=False))
for e in events:
    e['at']=now
    # New local delivery is single-use; identifiers distinguish the staged units.
    line=(json.dumps(e,ensure_ascii=False)+'\n').encode();raw+=line
save(ledger,raw)
rows=[json.loads(t) for t in ledger.read_text('utf-8-sig').splitlines() if t.strip()]
parents={}
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
save(H/'metric_derivative_tadpole/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),
    ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
rels=['metric_quartic_vertices.py','metric_quartic_vertices_check.py','metric_quartic_vertices_run.log',
 'metric_quartic_vertices/PRE_REGISTER.json','metric_quartic_vertices/results.json',
 'metric_coincident_jet_engine.py','metric_coincident_jet_check.py','metric_coincident_jet_run.log',
 'metric_coincident_jet/PRE_REGISTER.json','metric_coincident_jet_engine_v2.py','metric_coincident_jet_check_v2.py',
 'metric_coincident_jet_v2_run.log','metric_coincident_jet_v2/PRE_REGISTER.json','metric_coincident_jet_v2/results.json',
 'metric_derivative_tadpole_check.py','metric_derivative_tadpole_run.log',
 'metric_derivative_tadpole/PRE_REGISTER.json','metric_derivative_tadpole/results.json',
 'metric_derivative_tadpole/DERIVACAO.md','metric_derivative_tadpole/COST_SNAPSHOT.json',
 'kimi_curvature_review_audit.py','kimi_curvature_review_audit_run.log',
 'kimi_curvature_review_audit/PRE_REGISTER.json','kimi_curvature_review_audit/results.json',
 'kimi_curvature_review_audit/DERIVACAO.md','prepare_metric_quartic_units.py',
 'orchestration_metric_quartic/prepared_units.json']
files=[H/rel for rel in rels]+[Path(__file__),rp,ap]
for u in catalog:
    files += [Path(u['payload']),H/'orchestration_metric_quartic'/(u['slug']+'_preview.json'),
              H/'orchestration_metric_quartic'/(u['slug']+'_receipt.json')]
manifest=H/'metric_derivative_tadpole/delivery_manifest.json'
save(manifest,dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Kimi curvature report audited:18 exact checks; no free-loop recomputation',
       'Quartic derivative vertex98checks; Green jets126checks after preserved KeyError correction',
       'Full local-log metric derivative tadpole59checks: K[-2,2,-2,4]+K²[12,0]',
       'Two new complementary Kimi/MiMo units previewed and staging confirmed'],
    pending_orchestration='5 registered,9staging per official coordinator; MiMo independent_log_audit running at snapshot',
    latest_orchestration=dict(at=now,source='Official coordinator message',registered=5,staging=9,
        currently_executing='MiMo independent_log_audit',execution_job='cc22fd63-7326-4a83-b770-57822c8f874d'),
    latest_live_execution=dict(job_id='cc22fd63-7326-4a83-b770-57822c8f874d',
        execution_id='64cb5aba-39ae-4e48-81c5-6c1009629ac8',status='running_at_coordinator_snapshot'),
    metric_derivative_tadpole_manifest=str(manifest),
    quartic_review_catalog=str(H/'orchestration_metric_quartic/prepared_units.json'),
    kimi_curvature_review_local=str(ap),
    next=['Remaining curved metric bubble: curvature propagator/parallel transport corrections; combine with ghost/source',
          'Recover completed independent reviews only; preserve queue/order/IDs; do not contaminate pending reviewers',
          'Full Q2 finite causal hierarchy open; A7.c only after24h; A7.d,A8,PartB and final audit remain'],
    previous_turn_failure='Jet engine v1 KeyError transposed entry not yet populated; v2 builds table before transpose access')
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: quartico derivativo98checks,jatos126,tadpole59; K[-2,2,-2,4]+K²[12,0]. AuditoriaKimi18checks;2unidades novas em staging,5registradas/9staging no snapshot. CPU local{sum(e.get("cpu_seconds",0) for e in events)}s. Custo parcialUS${cost},desconhecidosnãozero. Q2OPEN. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for item in data('metric_derivative_tadpole/delivery_manifest.json')['artifacts']:
    assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(report=str(rp),audit=str(ap),verified_artifacts=len(files),known_partial_cost=str(cost))))
