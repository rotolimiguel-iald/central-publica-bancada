"""Record the first actual current diagram and the required gauge-fixing flux."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;D=H/'classical_current_insertion_delivery';D.mkdir(exist_ok=False)
O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,t):write(p,p.read_bytes()+t.encode())
names=['classical_current_jets','metric_current_insertion_v2','localized_gauge_fixing_commutators'];artifacts=[];rs=[]
for name in names:
 m=H/name/'manifest.json'
 for row in json.loads(m.read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256'],row['path']
 rs.append(json.loads((H/name/'results.json').read_bytes()));artifacts.append(m)
checks=sum(r['checks'] for r in rs);cpu=sum(r['cpu_seconds'] for r in rs);assert checks==1367
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
proof=r'''[DERIVED — inserção métrica da corrente e fluxo localizado de gauge; Q2 OPEN]

## Corrente métrica como vértice

J_BV(h,h,c) previamente construído é homogêneo de grau2 nos12 marcadores
de derivada (p,q,k): V2 tem grau2, Lie grau1 e a corrente de Green grau1.
Portanto a polarização quadrática recupera exatamente seus78 monômios,
sem truncar uma série nem ajustar uma aproximação. Obtida a realização
para c0 e todos55 pares simétricos de fibras, com a troca para100 pares.
990 comparações conferem dois pontos não axiais, corrente, divergência e
troca das pernas. Há276 monômios de segunda derivada interna e159 de
segunda derivada no ghost externo. Um vértice apenas de primeiras
derivadas por perna perderia essas contribuições.

## Primeira inserção realmente contraída

O vértice -partial_mu chiY J_BV^mu foi contraído com o vértice EH cúbico
completo localizado em X. Conservaram-se os jatos internos de ordem2 e
os jatos externos do ghost; adjunção em Y usa produtos de(d_i-eta_i),
e em X -(d_i+lambda_i) para a perna derivada. A extensão usa o mesmo
R=FP[(1-a)mu^(2a)z^a], C_D=RD-DR e q->q-lambda na diagonal.
350 verificações comparam o kernel simbólico com contrações racionais
no ponto(1,2,-1,1), incluindo suas derivadas. Essa comparação audita a
implementação; não afirma independência dos vértices de entrada.

Normalização explícita: /16 por par métrico, SEM fator de simetria do
diagrama. Para h11,c0 e q=(2,1,0,0), normalizado por CE=-4pi²:
* lambda=0,eta=e0: fora diagonal -12104/117649; contato -63841/3840.
* lambda=e0-e1,eta=e0: fora diagonal -175792/117649; contato131279/3840.
Não somar esses números à Ward com fator ajustado pelo resultado. A
montagem deve derivar os pesos e incluir as outras correntes abaixo.

Falha v1 preservada: 0/16 do Python introduziu float nos termos nulos.
No primeiro comparador que falhou,716/16807 virou0.04260129707859826,
diferença-6.24500451351651e-17. v2 usa Rational/Fraction explicitamente,
sem tolerância ou alteração de física. Logs/diagnóstico/predecessores
permanecem no manifesto. Não se chama a v1 de aritmética exata.

## Correção de convenção ao lado e correntes que faltam

BV069 §3,eq7, fixa s0barc=-b, não +b. O parágrafo ghost em
localized_brst_flux/DERIVACAO.md usou +b; fica CORRIGIDO AO LADO.
Nenhum código do cálculo métrico utilizou esse sinal, mas a montagem
ghost deve seguir a fonte. Para Igh=integral chi barc divZ:
sIgh=integral chi[-b divZ-barc div(sZ)]
    =integral(chi db+dchi b)Z+(chi dbarc+dchi barc)sZ.
Não misturar essa convenção com antighost hermitiano/fator i alternativo.

Ponha Z=L_c h, w=c.partial c. A identidade graduada é s0Z=-G w.
Para as transformações localizadas s1chi h=chi Z, s1chi c=chi w,
mantendo S0 sem cutoff e Vghostchi=integral chi barc C Z:
s0Vghostchi+s1chi S0gf
 = integral b[C,chi]Z-barc[Q,chi]w, Q=CG.
No plano, C é divergência com reversão de traço, Q=box em notação de
derivada real (seu símbolo Fourier tem o i² separado):
[C,chi]Z_nu=(d_mu chi)(Z_mu,nu-delta_mu,nu trZ/2),
[Q,chi]w=(box chi)w+2(d_mu chi)d_mu w.
Integrando por partes o termo box chi, a corrente é
J_gf^mu=b_nu Zbar_mu,nu+(d_mu barc_nu)w^nu-barc_nu d_mu w^nu,
com contribuição +integral dchi.J_gf. A fonte métrica tem contribuição
-integral dchi.J_BV na convenção da seção anterior. Isso ainda não é o
colchete completo nos setores com antifields externos.

27 verificações CAS incluem a identidade s0Z=-Gw com momentos e
polarizações SIMBÓLICOS arbitrários de duas ondas Grassmann ímpares,
os comutadores em campos/cutoff polinomiais e a divergência exata entre
as duas formas de J_gf. Controles não nulos:[C,chi]Z=(568,207,-121,988)
e -barc[Q,chi]w=-488 num ponto declarado. O sinal+ b incorreto já deixa
variação40 na ação livre de um controle; o sinal-b a cancela.

Consequência: b não propaga como um laço independente, mas o termo b h c
da corrente pode contrair pela entrada mista b-h. Também há a corrente
barc c c no diagrama ghost. Faltam essas inserções quânticas e seus pesos,
curvatura, partes suaves/tadpoles, aridades superiores e causalidade.
A soma de fonte+pares anterior nunca foi declarada Q2 e não recebe esse
estatuto agora. Nada mudou em um.py, kernel, horizonte, Atlas ou gate.
'''
write(D/'DERIVACAO.md',proof.encode())
artifacts += [D/'DERIVACAO.md',Path(__file__),H/'classical_current_jet_run.log',H/'metric_current_insertion_run.log',H/'metric_current_insertion_run_v2.log',H/'localized_gauge_fixing_commutator_run.log',H/'metric_current_insertion_v2/V1_FAILURE_DIAGNOSIS.json',H/'metric_current_insertion_engine.py',H/'metric_current_insertion_check.py',H/'localized_brst_flux/DERIVACAO.md']
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,full_Q2=False,
 supersedes=dict(engine=str(H/'metric_current_insertion_engine.py'),engine_sha256=sha(H/'metric_current_insertion_engine.py'),reason='Exact division correction; v1 failure retained'),
 erratum=dict(source=str(H/'localized_brst_flux/DERIVACAO.md'),source_sha256=sha(H/'localized_brst_flux/DERIVACAO.md'),correction='Ghost prose must use s0barc=-b as BV069; metric calculations not affected'),
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts]);write(D/'manifest.json',dump(manifest))
ledger=O/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='METRIC_CURRENT_V1_EXACT_DIVISION_FAILURE',target='A7.b',rc=1,cpu_seconds=None,remote_call=False,log_sha256=sha(H/'metric_current_insertion_run.log')))+'\n')
append(ledger,json.dumps(dict(at=now.isoformat(),event='CLASSICAL_CURRENT_QUANTUM_INSERTION_AND_GAUGE_FLUX',target='A7.b',rc=0,checks=checks,cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json'),remote_call=False))+'\n')
total=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 e=json.loads(line);k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (k is None or k not in seen):
  total+=Decimal(str(v))
  if k:seen.add(k)
start=datetime.fromisoformat(json.loads((H/'classical_current_jets/PRE_REGISTER.json').read_bytes())['at']);wall=(now-start).total_seconds()/3600
note=f'''[DERIVED — primeira inserção da corrente no laço; fluxo ghost/b identificado]

{now.isoformat()}. Abertura SHA256 {opening}.

Corrente realizada com jatos até ordem2 e contraída com vértice EH
completo: {checks} verificações (990+350+27), CPU{cpu}s, três rc0.
O contato da inserção h11,c0 com dchiY=e0 dá-63841/3840 sobre CE,
sem atribuir ainda o peso global do diagrama. Dados completos no manifesto.

Fonte BV069 conferida: s0barc=-b. Corrigido AO LADO o parágrafo da entrega
clássica que usou+b; o cálculo métrico não dependia dele. A localização
produz b[C,chi]Z-barc[Q,chi]w, e sua corrente integrada foi derivada e
conferida. Portanto faltam as inserções mistas b-h e barc c c, além da
montagem com curvatura/aridades. Isso localiza o próximo cálculo; Q2 OPEN.

v1 do novo motor preservada: divisão0/16 introduziu float; v2 usa racionais
exatos, sem tolerância. Manifesto {D/'manifest.json'};
SHA256 {sha(D/'manifest.json')}. Comandos A4/symbolic_runtime/Scripts/python.exe
-X utf8 -B A7/classical_current_jet_check.py, metric_current_insertion_check_v2.py,
localized_gauge_fixing_commutator_check.py, separadamente. Logs no manifesto.
Bancada registrada{wall:.6f}h; CPU da tentativa falha não medida.
Parcial externo US${total}; nenhuma nova chamada nesta entrega.
Originais e gate preservados. Próximo: contrair J_gf e reunir pesos da Ward.
'''
out=O/'ENTREGA_016_A7b_insercao_corrente_e_fluxo_gauge.md';assert not out.exists();write(out,note.encode())
measure=O/'ENTREGA_016_MEDIDA_sinal_antighost_e_corrente_b.md';assert not measure.exists();write(measure,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS/MEDIDA: corrente inserida e fluxo gauge,1367checks CPU{cpu}s,bancada{wall:.6f}h;sinalbarc corrigido ao lado;parcialUS${total};Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_processes=[],
 completed_this_turn=['Metric current jet realization990checks','Actual metric current insertion350checks','Gauge-fixing commutators27checks; s0barc sign corrected from BV069'],
 classical_current_insertion_manifest=str(D/'manifest.json'),
 next=['Contract J_gf=b Zbar+(dbarc)w-barc dw using mixed b-h and directed ghost propagators; derive Ward diagram weights',
 'Continue curvature,smooth,tadpole and higher arities within A7b deadline20:32UTC','Await independent Kimi/MiMo results through coordinator; no duplicate calls',
 'A7c/d,A8,ORDEM015 PartB and final full requirement audit remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(out),checks=checks,cpu_seconds=cpu,partial_cost=str(total))))
