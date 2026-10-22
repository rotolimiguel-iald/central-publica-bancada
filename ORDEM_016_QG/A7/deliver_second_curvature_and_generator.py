"""Custody of the K2 radial calculation and exact response to Kimi P1."""
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
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def data(rel):return json.loads((H/rel).read_bytes())
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
folders=['metric_action_hessian_calibration','metric_second_curvature_bitensor','position_metric_second_curvature_v2','metric_A2_generator']
results={f:data(f+'/results.json') for f in folders};files=[]
for f in folders:
    manifest=H/f/'manifest.json'
    if manifest.exists():
        for a in data(f+'/manifest.json')['files']:
            p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
        files.append(manifest)
    else:
        files.extend(p for p in (H/f).iterdir() if p.is_file())
checks=sum(r.get('checks',r.get('matching',0)) for r in results.values())
cpu=sum(r['cpu_seconds'] for r in results.values())
review=H/'received_reviews/f1293276-0c3a-4b5b-bbf6-b3585a862ad2.md'
rp=O/'ENTREGA_016_A7b_segunda_curvatura_e_gerador_A2.md';assert not rp.exists()
save(rp,f'''[DERIVED — jatos/gerador locais; REAL — CAS; OPEN — Q2 completa]
# A7.b — segunda curvatura e gerador da redefinição
Abertura SHA256 `{opening}`. UTC {now}.

**Calibração da ação:**400 componentes da Hessiana extraída dos termos
quadráticos GammaGamma e potencial coincidem com o operador livre usado
nos laços, em duas escolhas de momento e ordens K0/K1. Zero diferenças.
Isso exclui essa divergência específica como causa do resíduo Ward da
entrega anterior; não faz esse resíduo desaparecer.

**Jatos K²:** calculados com os mapas de Jacobi dos dois extremos,
conexão radial e medida sinc(sqrt(K)r)^3. São6604 controles: quatro
séries,5000 componentes contra os jatos K0/K1 anteriores e1600
componentes do coeficiente logarítmico K² contra o calor coincidente.
A continuação depende das hipóteses de fundo de curvatura constante
escritas no motor; a parte suave W permanece separada.

**Bolha radial K²:**55 pares de fibras,3207 controles, na base
[tr(AB),tr(A)tr(B)], antes da transferência por partes na perna B:

| parcela | tr(AB) | tr(A)tr(B) |
|---|---:|---:|
| propagadores derivativos e volume |37|23/4|
| conexão externa |56|−14|
| potencial cruzado |−528|132|
| potencial ao quadrado |576|−144|
| soma |141|−81/4|

O coeficiente explícito de log(z) nesta média angular foi zero nas
duas estruturas. A soma ainda não é a Hessiana integrada: faltam os
adjuntos K², combinações com ghost/tadpole no mesmo ordenamento e os
termos suaves/finitos/cutoff. Não somar de novo as parcelas diagnósticas
de endomorfismo, pois já estão nos propagadores completos desta conta.

O primeiro conversor esparso falhou localmente (PolynomialError 1/z);
v2 conserva denominador z³ antes de impor z=x². Fontes/logs falhos
preservados, sem promoção de uma execução falha a resultado.

**Resposta ao Kimi — P1:** o parecer recuperado, SHA256
`{sha(review)}`, pede gerador de A2 e origem do fator−2.
Para A2 bilinear simétrica local, h par, u ímpar, s0h=Gc e s0u=Eh:

    F_A = integral u·A2(h,h)
    s0 F_A = integral (Eh)·A2(h,h) − 2u·A2(h,Gc).

O sinal vem da regra de Leibniz graduada; o2, da simetria bilinear.
Inclui obrigatoriamente o companheiro sem antifields (Eh)·A2 e os
antighosts de u=4κ(h*+C*barc). O fator global do laço pode multiplicar
a identidade inteira, não somente a parcela h*hc.

A checagem exata fez4912 controles, incluindo3 negativos (trocar
sinal, retirar o2, omitir o companheiro), nilpotência livre, ghost number
e100 pares de fibras do representante efetivo de57termos. São428
componentes não nulos nessa amostra polinomial. A simetria geral segue
também diretamente da simetrização explícita do motor; o exemplo
de três fibras testa a identidade graduada, não substitui essa definição.

Helmholtz não é requisito para esse gerador linear em antifields:
A0=h1²,A1=0 não é gradiente de uma ação escalar dos campos, mas
F=u0 h1² produz E0 h1²−2u0 h1 g1 exatamente. Logo, a falta de
integrabilidade Euler-Lagrange não obstrui esta redefinição BV.
O que ficou pago é esse gerador local na convenção livre já calibrada;
não se conclui QME completa, canonicidade única ou cancelamento de Q2.

**P2 conservado:** rank49 de80 deixa31 parâmetros no sistema usado.
Os três laços externos ao plano não demonstram eliminação de todas
essas direções. Não chamá-las automaticamente de ambiguidades físicas;
redundâncias de base/cohomologia exigem análise própria. Não escolhemos
novo representante para forçar Ward.

**Correção de contexto ao parecer:**087 usa sigma constante projetado;
069 é o fundo físico sigma=id. A afirmação oposta do parecer está
invertida. O regulador auxiliar Euclidiano O(4) também não é, só pelo
nome compacto, a projeção angular ontológica da TGL.

Pacote:{checks} controles, CPU{cpu}s, quatro execuções rc0.
Manifesto local em position_metric_second_curvature_v2/delivery_manifest.json.
Nenhum original, um.py, kernel ou gate alterado. O resíduo Ward primeiraK
continua registrado; seguem adjuntos K² e hierarquia causal finita.
''')
marker='A7_SECOND_K_RADIAL_AND_A2_GENERATOR';ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,report_sha256=sha(rp),full_Q2=False,new_external_execution=False))+'\n').encode();save(ledger,raw)
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
extra=['metric_action_hessian_calibration.py','metric_action_hessian_calibration_run.log',
    'metric_second_curvature_bitensor_engine.py','metric_second_curvature_bitensor_run.log',
    'position_metric_second_curvature_engine.py','position_metric_second_curvature_check.py',
    'position_metric_second_curvature_run.log','position_metric_second_curvature_v2_run.log',
    'metric_A2_generator_run.log','received_reviews/f1293276-0c3a-4b5b-bbf6-b3585a862ad2.json']
files+=[H/x for x in extra]+[review,rp,Path(__file__)];files=list(dict.fromkeys(files))
manifest=H/'position_metric_second_curvature_v2/delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
    completed_this_turn=['Action/Hessian calibration400checks','SecondK bitensor6604checks',
        'SecondK raw radial55pairs3207checks','Kimi primitive recovered; A2 generator4912checks'],
    second_curvature_generator_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    pending_orchestration='Coordinator reports5registered/7staging; MiMo free_heat_audit started, Kimi curved_antifield_source registered',
    latest_live_execution=dict(job_id='70db6729-942c-4435-92e6-482d3d842134',status='running_reported_by_coordinator',observed_utc=now),
    next=['SecondK anchored-leg adjoints then combined Hessian in identical covariant ordering',
        'FirstK Ward residual persists: reconcile conventions/contacts; never silently retune',
        'Finite causal hierarchy with smooth W/cutoff remains open; A2 generator only local/free',
        'Single worker manages5registered/7staging; do not repeat terminal/uncertain requests',
        'A7.c after24h if acceptance unpaid; A7.d,A8,PartB and full finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: segundaKradial e geradorBV A2; {checks}controles, CPU{cpu}s. KimiP1 delimitado/resolvido localmente; P2semcanonicidade; WardprimeiraKnãozero preservado. Q2OPEN. Custo parcialUS${cost}, desconhecido≠zero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),checks=checks,cpu_seconds=cpu,verified_artifacts=len(files),partial_cost=str(cost))))
