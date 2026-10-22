"""Seal measured principal-sector progress and preserve unsuccessful ansatzes."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;CHAT=HERE.parents[1];OUT=CHAT/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(b)
    assert b and t.read_bytes()==b;t.replace(p)
def fresh(p,o):assert not p.exists();save(p,json.dumps(o,ensure_ascii=False,indent=2))
groups=[('general_marked','general_marked_compute.py','general_marked_run.log'),
        ('quadratic_metric_fit','quadratic_metric_fit.py','quadratic_metric_fit_run.log'),
        ('quadratic_metric_joint','quadratic_metric_joint_fit.py','quadratic_metric_joint_run.log'),
        ('bv_gradient_fit','bv_gradient_fit.py','bv_gradient_fit_run.log'),
        ('bv_gradient_audit','bv_gradient_audit.py','bv_gradient_audit_run.log')]
rs={x:json.loads((HERE/x/'results.json').read_bytes()) for x,_,_ in groups}
r=rs['bv_gradient_fit'];audit=rs['bv_gradient_audit'];gen=rs['general_marked']
assert r['rank']==r['augmented_rank']==49 and r['polynomial_checks']==470
assert all(x=='0' for x in r['DeltaZ_coefficients']) and r['gradient_coefficients']==['-1/3','0']
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
cpu=sum(x['cpu_seconds'] for x in rs.values());wall=sum(x['wall_seconds'] for x in rs.values())
report=f'''[DERIVED — decomposição do vértice principal h*hc; REAL — álgebra racional/CAS; OPEN — Q2 causal finita]
# A7.b — a derivada do ghost completa o vértice principal

Abertura SHA256 `{opening}`. UTC {now}.

Calculamos400 componentes de R1(H,p;r,v)=G-M/4 como polinômios exatos
em p=a e0,r=b e0+c e1:10H×10T×4v. O fator comum retirado é4iκA0,
A0=1/(8π²). O motor reutiliza o vértice cúbico EH, homogêneo de grau2,
e a extração do log UV previamente auditada. Cinco comparações cúbicas e
quinze comparações com o motor Sympy direto passaram;400 limites de ghost
constante coincidiram com a rodada anterior e todos os termos têm grau3.

A candidata anterior deixou116 componentes com resíduo. Apenas acrescentar
uma mudança quadrática simétrica de métrica A2, em57 contrações O(4), deu
posto33 contra34 no sistema aumentado. Permitir também as21 componentes
DeltaZ, mantendo bracket e os seis coeficientes constantes, deu48 contra49.
Esses negativos são preservados; não são provas de obstrução BV geral.

O termo que faltava nesse ansatz é permitido pela álgebra graduada:

    D1(E;r,v)=1/2 [ sym(r,Ev)-sym(v,Er) ],
    sym(x,y)=(xy^T+yx^T)/2.

Ele é antissimétrico na contração das fibras:
<T,D1(E)>=-<E,D1(T)>, e some para r=0. O segundo termo testado,
D2=[sym(v,r)trE-I(v·Er)]/2, tem a mesma propriedade. As800 identidades
de antissimetria foram verificadas em base. Para uma matriz de fibras
antissimétrica C e um jato ímpar d de ghost,

    delta[ (1/2) u_A C_AB d u_B ] = u_A C_AB d E_B,
    delta u=E, delta d=delta E=0.

Isso segue diretamente da regra graduada; um teste exterior de três fibras
conferiu identidade, nilpotência e graus. Usar derivada não graduada falha.
Logo D1 pode vir de um gerador local quadrático em antifields com derivada
do ghost; não é um tensor livre acrescentado sem primitiva.

O sistema completo,656 equações escalares em80 coeficientes, tem posto49
igual ao aumentado. Uma solução (parâmetros livres zero) tem DeltaZ=0,
coeficiente de D1=-1/3 e de D2=0. A2, com seus57 coeficientes, está listado
integralmente em bv_gradient_fit/results.json; cada base é simetrizada sob
(H,p)<->(J,r), como define quadratic_metric_engine.py. O resultado exato é

    R1 = Lie_(F_r v) H - K_(p+r) Z_new(H,p;r,v)
         -2 A2(H,p;K_r v,r)
         + [(p+r/2)·v] B(E_pH) - (1/3)D1(E_pH;r,v),
    F_rv=-3r²v/8+r(r·v)/4, B(E)=-E/6-I trE/12.

Z_new é o representante já fixado que conserva o bracket. O sistema
conferiu400 componentes R1,64 do bracket e6 condições constantes:470
identidades polinomiais, sem modificar nenhum coeficiente dos laços.
Por covariância O(4), dois momentos Euclidianos arbitrários podem ser postos
nesse plano; degenerações seguem por continuidade polinomial. Isso fornece
uma identidade tensorial principal, não uma escolha de prescrição causal.

Após congelar os coeficientes, três novos casos com momentos fora do plano
foram computados DIRETAMENTE pelo motor Sympy de laços:25/6,43/6,-245/3,
todos iguais à fórmula. As contribuições D1 nesses casos foram3,3,-6;
retirá-las ou inverter seu sinal falha (seis controles). Há ainda um controle
graduado negativo, totalizando sete. Essas verificações não são independentes
de todas as convenções de vértices; o motor-base já tinha auditoria própria.

Com u=4κ(h*+C*barc), a parcela nova de gerador é -A0/6 integral u D1(∂c)u;
seu diferencial livre produz a parcela calculada, além dos termos de antighost
do deslocamento, que não podem ser descartados. Restam a involução/realidade,
os demais componentes de s1F, os contatos de cutoff, curvatura e partes
finitas da anomalia. A identidade acima não prova QME completa, não atualiza
kernel nem gate. Não houve Lean nesta rodada. Cinco execuções rc0;
CPU total{cpu}s, parede{wall}s; zero novas chamadas externas nesta medição.
'''
rp=HERE/'bv_gradient_fit/DERIVACAO_COMPLETA_PRINCIPAL.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_vertice_principal_completo.md',report)
engines=[HERE/x for x in ['general_marked_engine.py','marked_vertex_engine.py','marked_polynomial_engine.py',
                          'quadratic_metric_engine.py','ghost_primitive_engine.py','bv_gradient_engine.py']]
for folder,script,log in groups:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',rp]+engines
    fresh(HERE/folder/'manifest.json',dict(at=now,opening_sha256=opening,
          artifacts=[dict(path=str(x),sha256=sha(x),bytes=x.stat().st_size) for x in files]))
measure=f'''[REAL — sistemas inconsistentes de ansatzes parciais; OPEN — cohomologia causal completa]
# A7.b — duas tentativas preservadas
Abertura SHA256 `{opening}`.
Comando em ambos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B <script>.
quadratic_metric_fit.py: rc0,522linhas57colunas,rank33/aug34,
CPU{rs['quadratic_metric_fit']['cpu_seconds']}s, logSHA{sha(HERE/'quadratic_metric_fit_run.log')}.
quadratic_metric_joint_fit.py: rc0,656linhas78colunas,rank48/aug49,
CPU{rs['quadratic_metric_joint']['cpu_seconds']}s, logSHA{sha(HERE/'quadratic_metric_joint_run.log')}.
Próximo passo executado no mesmo ramo: acrescentar os dois termos de derivada
do ghost provenientes de gerador BV quadrático, preservando todos os dados
dos laços. Sistema aumentado consistente49/49; entrega
ENTREGA_016_A7b_vertice_principal_completo.md. Não apagar os negativos nem
interpretá-los como ausência de solução em toda a cohomologia. Custo remoto zero.
'''
save(OUT/'ENTREGA_016_MEDIDA_ansatz_BV_sem_gradiente_ghost.md',measure)
ledger=OUT/'LEDGER_016.jsonl';event=dict(event='A7_GENERAL_PRINCIPAL_BV_COMPLETION',at=now,provider='local',target='A-7.b',
    tensor_components=400,polynomial_checks=470,skew_checks=800,direct_loop_checks=3,
    negative_controls=7,cpu_seconds=cpu,rc=0,report_sha256=sha(rp),full_Q2=False,gate_changed=False)
save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
costs={}
for ln in ledger.read_text('utf-8-sig').splitlines():
    if not ln.strip():continue
    x=json.loads(ln);v=x.get('cost_estimate_usd',x.get('cost_usd',x.get('custo_usd')))
    k=x.get('execution_id') or x.get('job_id') or x.get('request_id') or x.get('execution_task_id')
    if k and v is not None:costs[k]=Decimal(str(v))
total=str(sum(costs.values(),Decimal(0)))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,principal_general_BV_manifest=str(HERE/'bv_gradient_fit/manifest.json'),
    full_hstar_hc_matched=True,full_hstar_hc_scope='Principal Euclidean UV log only; not finite causal anomaly',
    next=['Kimi review of complete principal BV primitive with gradient term; same held request v3',
          'Reality, nonlinear differential, cutoff and curvature terms within A7b timebox',
          'Recover temporal/cohomology results without a new execution'],partial_metered_cost_usd=total)
d['completed_this_turn'].append('General R1 principal tensor decomposed by A2+Z+B EOM+ghost-gradient antifield primitive;470 polynomial identities,3 direct off-plane checks,7 negatives')
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: R1principal completo400componentes;470identidades e800skew;3ensaios fora do plano+7negativos;CPU{cpu}s. Dois ansatzes inconsistentes preservados. Q2causalOPEN. Custo externo parcialUS${total}. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),manifest=str(HERE/'bv_gradient_fit/manifest.json'),cpu_seconds=cpu,partial_cost=total)))
