"""Deliver the first-curvature source profile with its coordinate scope explicit."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
import sympy as s
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b)
    assert b and tmp.read_bytes()==b;tmp.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'curved_source_jet/results.json').read_bytes())
a=json.loads((H/'curved_source_jet_audit/results.json').read_bytes())
# The audit's numeric assertions passed, but its prose said trace-reversed.
# Keep that source/result immutable and record a correction alongside it.
v=s.Matrix(s.symbols('v0:4'));p=s.Matrix(s.symbols('p0:4'));I=s.eye(4)
R=-s.Rational(10,3)*(p*v.T+v*p.T)+s.Rational(5,3)*I*p.dot(v)
assert s.expand(s.trace(R))==0
ItrK=p*v.T+v*p.T-I*p.dot(v)
defect=s.simplify(R+s.Rational(10,3)*ItrK)
assert defect==-s.Rational(5,3)*I*p.dot(v)
corrected=dict(a,supersedes_path=str(H/'curved_source_jet_audit/results.json'),
    supersedes_sha256=sha(H/'curved_source_jet_audit/results.json'),
    statement='The first-K normal-coordinate angular profile is -10K/3 times the TRACELESS projection of the gauge tensor',
    wording_correction='trace-reversed replaced by traceless; no numeric coefficient changed',
    additional_symbolic_checks=2,trace=0,trace_reversed_defect='-5/3 delta (p.v)',
    operator_identification='Not yet converted to a covariant differential operator on external fields')
save(H/'curved_source_jet_audit/results_v2.json',corrected)
cpu=r['cpu_seconds']+a['cpu_seconds']
report=f'''[DERIVED — contribuição singular de primeira curvatura; REAL — CAS exato; OPEN — soma causal]
# A7.b — bitensores na primeira bolha antifield–ghost
Abertura SHA256 `{opening}`. UTC {now}.

**Escopo e convenção da fonte.** Cálculo auxiliar euclidiano do coeficiente K
no espaço-forma, retirando 1/(4pi²) de cada propagador, os fatores globais
4kappa, ghost e a fase da fonte. A fonte externa T^ab no integrando é uma
densidade contravariante, pareada com h_ab por d⁴X. Se o antifield original
for escrito usando o volume, T inclui esse volume e a elevação dos índices.
Não se deve manter T constante e multiplicar novamente pelo volume em X.
O vértice ghost usa o volume em Y; Y=0 em coordenadas normais. Essa convenção
especifica o perfil de coordenadas calculado, não muda a ação069.

**Transporte incluído.** A conexão normal é
Gamma^a_mb=-(K/3)(delta_ab x_m+delta_am x_b-2delta_mb x_a).
Integrá-la ao longo do segmento fornece, com d=X-Y,s=X+Y,

    P^a_b'(X,Y)=delta_ab+(K/6)[delta_ab(X²-Y²)+d_a s_b-2s_a d_b]+… .

Verificados por álgebra: P^t g(X)P=g(Y), inversão X/Y, R^a_bmn,
os jatos de P e do propagador métrico, antes de pôr Y=0. Para o bitensor
com índices baixos G_ab'=g_ac(X)P^c_b',

    G_ab'(x,0)=delta_ab-(K/6)(delta_ab z-x_a x_b),
    partial_Yj G_ab'|Y=0=(K/2)(x_a delta_bj-delta_aj x_b).

O numerador métrico é S_ab,c'd'=(G_ac'G_bd'+G_ad'G_bc'-g_ab(X)g_c'd'(Y))/2.
Usamos os perfis já derivados: H/(4kappa)=(1+Kz/4)S/z
+(K/2)delta_ab delta_cd L+W_H+…; ghost=(1+Kz/4)P/z
-(5K/4)delta_mn L+W_G+… . L=log(mu²z). Só a parte singular geométrica
entra nesta execução; os jatos suaves W continuam uma obrigação explícita.

Os dois vértices são os mesmos: T^ab[c^m partial_m h_ab+2h_am partial_b c^m]
e -(nabla^mu barc^nu)[L_v h_munu-g_munu tr(L_v h)/2]. O script realiza
suas contrações por índices, incluindo derivadas X/Y do transporte, sem
inferir a curvatura a partir de uma massa escalar. O termo quartico de
distância geodésica tem primeiro jato Y e misto XY nulos em Y=0 nesta ordem.

**Controle plano e resultado.** Com fator angular A0=1/(8pi²) retirado e
Taylor de exp(-ip·x), a parte plana reproduz exatamente

    R0(p)v=-(3/8)p²(p v^t+v p^t)+(1/2)p p^t(p·v).

A contribuição singular de ordem K dá o perfil angular local

    R_K(p)v=-(10K/3)(p v^t+v p^t)+(5K/3)delta(p·v).

Os coeficientes de L cancelam nesta contração; os dois coeficientes acima
foram ajustados em três polarizações e conferidos nas quarenta polarizações
axiais e numa combinação densa não axial. O traço de R_K é zero.
**Errata ao lado:** a frase automática do primeiro JSON da auditoria dizia
"trace-reversed". O número mostra "traceless": a diferença para
-(10/3)I_tr(K_gauge v) é -(5/3)delta(p·v), não zero. JSONv2 preserva a
correção e o SHA do predecessor; nenhuma conta foi apagada ou repetida.

Ao omitir os jatos transversais dos dois propagadores, o primeiro controle
muda por -17/4. Portanto esses jatos têm contribuição efetiva. Execuções
rc0: {r['checks']}+{a['checks']} assertivas, mais2 da errata; CPU {cpu}s.
As muitas assertivas de componentes não são provas analíticas independentes.

**Ainda não pago.** Este perfil usa fontes em coordenadas normais e Taylor
ordinário. Sua comparação com um operador covariante em campos externos
exige transportar também os jatos das fontes/densidade; não identificamos
automaticamente R_K com um novo termo covariante de ação. Faltam W, extensão
finita, contatos do cutoff e reunião com os demais vértices da hierarquia.
O resultado não é a quebra Ward completa, nem prova de seu cancelamento.
Sem alteração de um.py, kernel ou gate. A7.b permanece ativa.
'''
rp=O/'ENTREGA_016_A7b_bitensores_fonte_curva.md';save(rp,report)
save(H/'curved_source_jet/DERIVACAO.md',report)
files=[H/n for n in ['curved_source_jet_engine.py','curved_source_jet_check.py','curved_source_jet_run.log',
 'curved_source_jet/PRE_REGISTER.json','curved_source_jet/results.json','curved_source_jet/manifest.json',
 'curved_source_jet_audit.py','curved_source_jet_audit_run.log','curved_source_jet_audit/PRE_REGISTER.json',
 'curved_source_jet_audit/results.json','curved_source_jet_audit/results_v2.json','curved_source_jet_audit/manifest.json',
 'curved_source_jet/DERIVACAO.md']]+[Path(__file__),rp]
save(H/'curved_source_jet/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(f),sha256=sha(f),bytes=f.stat().st_size) for f in files]))
ledger=O/'LEDGER_016.jsonl';marker='A7_CURVED_SOURCE_PARALLEL_BITENSOR_JETS'
if marker.encode() not in ledger.read_bytes():
    event=dict(event=marker,at=now,provider='local',target='A-7.b',cpu_seconds=cpu,
      checks=r['checks']+a['checks']+2,report_sha256=sha(rp),full_Q2=False,new_external_execution=False)
    save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()];parents={}
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
    ix=ids(row);v=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
cost=sum(known.values(),Decimal(0))
save(H/'curved_source_jet/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),
 ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Source first-curvature singular normal-coordinate profile computed with both-endpoint jets',
 'Flat coefficients reproduced;40basis polarizations+dense nonaxis and geometric transport audited',
 'Incorrect prose trace-reversed corrected alongside to traceless; numerical coefficients preserved'],
 curved_source_manifest=str(H/'curved_source_jet/delivery_manifest.json'),
 next=['Convert normal-coordinate source density jets to covariant derivative expansion; include smooth-reference jets before claiming full amplitude',
       'Recover distinct pending reviews once completed; no duplicate calls',
       'A7.c only if24h exhausted;A7.d,A8,ORDEM015 PartB and full audit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO:bitensores completos de primeiraK no perfil singular h*c;{r["checks"]}+{a["checks"]}+2assertivas,CPU{cpu}s;normalização plana recuperada,curvatura(-10/3,5/3),W/contatos/somaOPEN. Custo parcialUS${cost};desconhecidos nãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
print(json.dumps(dict(report=str(rp),manifest=str(H/'curved_source_jet/delivery_manifest.json'),
 cpu_seconds=cpu,known_partial_cost=str(cost),status='ACTIVE_PROGRESS')))
