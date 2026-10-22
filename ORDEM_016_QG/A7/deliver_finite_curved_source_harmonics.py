"""Custody of the actual first-curvature geometric source pair extension."""
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
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(b);assert b and q.read_bytes()==b;q.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
files=[];results=[]
for folder in ['finite_curved_source_harmonics_v2','finite_curved_source_harmonics_audit']:
    m=H/folder/'manifest.json'
    for a in json.loads(m.read_bytes())['files']:
        p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
    files.append(m);results.append(json.loads((H/folder/'results.json').read_bytes()))
checks=sum(r['checks'] for r in results);cpu=sum(r['cpu_seconds'] for r in results)
report=O/'ENTREGA_016_A7b_contato_finito_curvo_da_fonte.md';assert not report.exists()
save(report,f'''[DERIVED — extensão explícita de componente singular; REAL — CAS; OPEN — soma Ward completa]
# A7.b — contato finito curvo da bolha antifield–ghost
Abertura SHA256 `{opening}`. UTC {now}.

**Objeto efetivamente calculado:** os kernels A(T,v;x) e B(T,dv;x)
de curved_source_jet_engine na primeira ordemK, com os dois vértices
e bitensores já usados no log. Acrescentou-se ANTES da extensão o
transporte da densidade externa

    delta T=-z T/6-(xx^t T+T xx^t)/6.

Permanecem retirados os fatores globais dos propagadores,4kappa e
fases de Fourier. É a parcela singular geométrica, em cálculo
auxiliar euclidiano; não se afirma que os jatos suavesW sejam zero.

## A mesma prescrição, agora aplicada aos kernels
Conserva-se R=FP[(1-a)mu^(2a)z^a .], fixada antes destas contas.
Para escrever explicitamente R dos numeradores anisotrópicos,
decompusemos P(x)=sum z^j H_l(x), Delta_x H_l=0, e usamos

    H_l(partial)z^(a-b)
      =2^l product_(j=0)^(l-1)(a-b-j) H_l(x)z^(a-b-l).

Derivadas em a incluem os termoslog. Inverter essa identidade
determina uma representação por derivadas de R(z^-b L^r). Quando
o coeficiente tem zero simples, usa-se uma potência adicional deL;
o coeficiente do termo anulado pela derivada é fixado emzero apenas
na REPRESENTAÇÃO. Nenhuma constante de R é ajustada.

O contato de normalização é computado pelos mapas Laurent já pagos:

    R[H_l(partial)f]-H_l(partial)R[f]=C N_l[H_l,f]delta.

Logo a saída consiste na representação diferencial completa MAIS
seu contato local. Esta representação é uma referência de cálculo;
não foi chamada de prescrição BRST-invariante.

## Resultado e verificação independente
Para A, o contato local na primeiraK é

    Delta A/C=K[-13(q.T.v)/48-19 trT(q.v)/96],

com q representando derivadas do delta. Para B, o contato RELATIVO
à sua representação harmônica diferencial exibida é zero. Isso
NÃO diz que B seja zero ou que não contenha logaritmos: o controle
T00=1,v=e0 dá numeradorlog

    6x0²-2x1²-2x2²-2x3²,

não nulo. A média esférica desse log é zero; descartá-lo destruiria
o kernel fora da diagonal.

Foram calculados40 casos (dez fibrasT vezes quatro ghosts, p=e0)
e um caso denso não axial. A auditoria reconstruiu os80 kernels
A/B das40 amostras por derivadas radiais literais. Outra rota,
sem a inversão diferencial, usa a projeção esférica l=1:

    Delta A/C=(K/8)sum_i <A_geom(n)n_i>_S3 q_i.

Ela reproduz os mesmos coeficientes. Não incluir deltaT muda o
contato: em T00=1,v=e0 o erro é47q0/96. Assim, só o log previamente
medido não determina todos estes termos de extensão.

Movendo a derivada do delta para o ghost no funcional, a diferença
local tem a expressão covariante de primeira ordem

    Delta R(v)/C=-K[13G(v)+19g divv]/96,
    E Delta R(v)/C
       =19K[Hess(divv)-g Box(divv)-3Kg divv]/48.

A segunda identidade foi verificada com o operador físico E e
jatos reais covariantes, em duas amostras polinomiais atéK². Seu
termoK² é a imagem desse contatoK; NÃO inclui uma fonteK² ainda
não calculada. A parcelaG anula por E G=0; usou-se
E(gf)=-2Hess f+2gBox f+6Kgf, sem substituição por operador
gauge-fixado.

**Alcance:** {checks} controles exatos, CPU{cpu}s, duas execuçõesrc0.
Ainda faltam os contatos finitos das outras bolhas e a soma com
a referência diferencial não local, suas ordenações covariantes e
os jatosW. O contato acima é a diferença entre duas escritas do
MESMO kernel estendido; não é sozinho Q2, nem justificativa para
zerar a quebra por escolha de contratermo. Os dados completos e
hashes estão no manifesto. Gate, kernel e originais intactos.

Falha técnica preservada: v1 substituiu z=x² antes de expandir e
cancelar os denominadores, produzindo PolynomialError; v2 muda
apenas essa ordem algébrica. Fonte, pré-registro e logv1 permanecem.
''')
measure=O/'ENTREGA_016_MEDIDA_densidade_no_contato_finito_curvo.md';assert not measure.exists()
save(measure,f'''[REAL — transporte de densidade indispensável nesta extensão]
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: omitir a correção da densidade externa no kernel da
bolha h*-c. Na amostra T00=1,v=e0, o contato local difere por
47q0/96. A representação corrigida coincide com os momentos
esféricos e reconstrói os kernels originais. Log de média zero
não autoriza apagar seu numerador anisotrópico.

Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/finite_curved_source_harmonics_check_v2.py e
A7/finite_curved_source_harmonics_audit.py. rc0/rc0,
202+264controles,CPU{cpu}s. LogsSHA256
`{sha(H/'finite_curved_source_harmonics_v2_run.log')}` e
`{sha(H/'finite_curved_source_harmonics_audit_run.log')}`.
Falha técnica v1retida; nenhuma execução remota nova. Próximo
passo: contatos das bolhas métricas/ghost na MESMA extensão,
preservando a referência diferencial e a ordenação dos adjuntos.
''')
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_FINITE_CURVED_SOURCE_HARMONIC_EXTENSION'
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,
    report_sha256=sha(report),new_external_execution=False,full_Q2=False))+'\n').encode();save(ledger,raw)
rows=[json.loads(x) for x in raw.decode('utf-8-sig').splitlines() if x.strip()];parents={}
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
files += [H/'finite_harmonic_extension_engine.py',H/'finite_curved_source_harmonics_check.py',
    H/'finite_curved_source_harmonics/PRE_REGISTER.json',H/'finite_curved_source_harmonics_run.log',
    H/'finite_curved_source_harmonics_v2_run.log',H/'finite_curved_source_harmonics_audit_run.log',report,measure,Path(__file__)]
files=list(dict.fromkeys(files));manifest=H/'finite_curved_source_harmonics_v2/delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',completed_this_turn=[
    'Actual firstK geometric source finite extension:202checks,41cases, density transport included',
    'Independent spherical and literal derivative reconstruction:264checks; E DeltaR computed toK2'],
    finite_curved_source_harmonic_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    next=['Compute matching metric/ghost finite contacts with raw pair kernels and fixed R; harmonic reference not assumed Ward preserving',
          'Useful angular projections in4D: H1(q)=4<k(n)(n.q)>; H2(q)=12<k(n)(n.q)^2>-3q²<k(n)>',
          'For degree-5 kernels: local difference H1/32; for degree-6 nonlog H2 kernels: -5H2/576. Verify mixed logs before use',
          'Respect covariant derivative ordering and vertex potential sign, calibrated in ordered_node; do not infer full Q2 from local differences',
          'Same queued reviews and singleworker; A7.c after24h if unpaid, then A7.d,A8,PartB and finalaudit'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: contato finito curvo efetivo da fonte, {checks}controles,CPU{cpu}s. R preservada;Q2completaOPEN. Custo parcialUS${cost},desconhecido≠zero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(report),checks=checks,cpu_seconds=cpu,artifacts=len(files),partial_cost=str(cost))))
