"""Custody of the candidate's cutoff/nonlinear descent; originals untouched."""
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
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(b)
    assert b and tmp.read_bytes()==b;tmp.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
files=[];results=[]
for folder in ['curved_cutoff_descent','curved_cutoff_green']:
    m=H/folder/'manifest.json'
    for a in json.loads(m.read_bytes())['files']:
        p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
    files.append(m);results.append(json.loads((H/folder/'results.json').read_bytes()))
checks=sum(x['checks'] for x in results);cpu=sum(x['cpu_seconds'] for x in results)
source=H.parents[1]/'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md'
report=O/'ENTREGA_016_A7b_cutoff_e_descida_nao_linear_da_primitiva.md';assert not report.exists()
save(report,f'''[DERIVED — extensão da candidata local; REAL — CAS; OPEN — identificação com Q2 completa]
# A7.b — cutoff e descida não linear da primitiva quadrática
Abertura SHA256 `{opening}`. UTC {now}.

Prossegue a família D_t da entrega Ward_K2_e_primitiva_quadratica_local,
sem escolher t nem adotar um contratermo. Fixe a referência espaço-forma,
K constante, cutoff real inerte chi e suporte compacto. Todas as
contrações e a medida abaixo são da referência, inerte sob s.

## 1. Operador localizado e corrente nova
Escreva D_t=K C^ij nabla_(i nabla_j)+K² A. Os coeficientes C e A são
paralelos e simétricos entre as fibras. Para tensores simétricos X,Y,

    C^ij(X,Y)=-delta^ij(d1 X.Y+d2 trX trY)
      -d3(X^ij trY+trX Y^ij)
      -d4/2 (X^i_a Y^ja+X^j_a Y^ia),
    A(X,Y)=(t+7/3)X.Y-(t+22/3)trX trY,
    (d1,d2,d3,d4)=(1/2-t/2,9/4+t/2,-1-t/2,t).

A escrita em quadro ortonormal se covariantiza com a métrica de
referência. A simetria de C e A é algébrica; foi também conferida em
toda a base de dez fibras, todos os dezesseis pares de índices e nos
dois coeficientes afins em t. Não se pressupôs autoadjunção do operador
localizado chi D isolado. O gradiente correto é

    B_chi[h]=1/2 integral chi h.D_t h,
    F=M_chi h,  M_chi=(chi D_t+D_t chi)/2
                =chi D_t+[D_t,chi]/2,
    [D_t,chi]T=K C^ij[(nabla_i nabla_j chi)T
                                  +2(nabla_i chi)nabla_j T].

O termo K² comuta com chi. Na prova escrita, integração por partes,
paralelismo e simetria fornecem estas identidades para campos suaves
de suporte compacto. O CAS usa jatos polinomiais em coordenadas
normais até K², com a conexão já calibrada; o produto chi*h foi
calculado por dois caminhos: antes das derivadas coordenadas e pela
regra covariante de Leibniz.

## 2. Variação não linear explícita
Na convenção da classe087, s h=L_c(gbar+h), s c=c.grad c. A segunda
igualdade é ímpar: equivale a [c,c]/2, não a um colchete de vetores
comutativos iguais. Referência, t e chi são inertes. Segue

    s B_chi = integral [G(c)+L_c h].F
            =s0 B_chi+s1 B_chi,
    s1 B_chi=integral (L_c h).F.

Depois de uma integração por partes, a corrente do ghost é

    J_r=F^ab nabla_r h_ab
             -2 nabla_a[(gbar_rb+h_rb)F^ab],
    [G(c)+L_c h].F = c^r J_r
             +nabla_a[2c^r(gbar_rb+h_rb)F^ab].

Isso exibe o termo h²c e a corrente de fronteira, incluindo as
derivadas de chi dentro de F. Não se confundiu a densidade pontual
com seu funcional integrado. Fonte da convenção BRST: classe087,
SHA256 `{sha(source)}`; não se transportou seu H4 para ghost1.

## 3. Consistência da candidata, com a fronteira mantida
Para dois parâmetros pares u,v usados apenas na polarização dos
dois ghosts ímpares, L_u L_v-L_v L_u=L_[u,v]. A checagem covariante
incluiu a referência e a perturbação, até duas derivadas externas e
K². A polarização da variação da densidade deixa a expressão de
Green com X=L_v(gbar+h), Y=L_u(gbar+h):

    X.M_chi Y-(M_chi X).Y = nabla_i I^i,
    I^i=K chi [C^ij(X,nabla_jY)-C^ij(nabla_jX,Y)].

Essa identidade decorre da forma divergente
M=K nabla_i(chi C^ij nabla_j)+K C^ij chi_;ij/2+K²chi A.
Logo s(sB_chi)=0 como funcional integrado, com a corrente local
indicada. É a consistência de uma candidata exata já construída;
NÃO é inferência de que toda quebra quântica seja essa candidata.

## 4. Evidência e alcance
{checks} verificações exatas; CPU {cpu}s. Três controles negativos:
omitir o contatochi deixa835/4 em uma componente; omitir s1B deixa
53611 em uma amostra; sinal errado do colchete deixa-10. Uma segunda
auditoria encontrou12 amostras com divergência pontual não nula,
embora a corrente integre a zero no suporte compacto. Os números são
dos campos de teste normalizados no script, não constantes físicas.

**O que foi pago:** extensão local com cutoff e variação não linear
da família quadrática que cancelava o componente h*c logarítmico
medido. **O que falta nesta etapa:** comparar s1B com o coeficiente
quântico h²c e ligar as partes finitas da prescrição temporal aos
mesmos grafos covariantes. As identidades universais de contato
logarítmico já existem e serão reutilizadas; não se introduziu uma
nova prescrição. Nenhum t escolhido, gate movido ou original alterado.
''')
measure=O/'ENTREGA_016_MEDIDA_cutoff_nao_pode_ser_apagado.md';assert not measure.exists()
save(measure,f'''[REAL — controles negativos da candidata; DERIVED — corrente explícita]
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: localizar a primitiva D_t por chi e conservar somente
chi D_t, ou descartar s1B. Ambos falham. Na amostra t=0,K^1,
o primeiro perde835/4 na componente00 e o segundo perde53611.
Com os contatos completos, a identidade de Noether fecha.

Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/curved_cutoff_descent_check.py (rc0,1497 controles) e
A7/curved_cutoff_green_audit.py (rc0,6708 controles).
LogsSHA256: `{sha(H/'curved_cutoff_descent_run.log')}` e
`{sha(H/'curved_cutoff_green_run.log')}`. CPU total{cpu}s.
Nenhuma chamada externa nesta medição. Próximo ramo da mesma A7.b:
confrontar a candidata com os componentes finitos/não lineares da
prescrição; s²B=0 sozinho não identifica a anomalia medida.
''')
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_CURVED_CUTOFF_NONLINEAR_CANDIDATE_DESCENT'
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,
    report_sha256=sha(report),measure_sha256=sha(measure),new_external_execution=False,full_Q2=False))+'\n').encode();save(ledger,raw)
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
files += [source,H/'curved_cutoff_descent_run.log',H/'curved_cutoff_green_run.log',report,measure,Path(__file__)]
files=list(dict.fromkeys(files));manifest=H/'curved_cutoff_descent/delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',completed_this_turn=[
    'Actual curved D_t cutoff and s1B current,1497checks,3negative controls',
    'All coefficient adjoints and explicit polarized Green/WZ current,6708checks,12nonzero local divergences'],
    curved_cutoff_descent_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    curved_ward_review_status='COORDINATOR_CONFIRMED_STAGING_LAST_POSITION_7',
    pending_orchestration='5registered/7staging last official report; one worker; no duplicate calls',
    next=['Actual finite temporal contact and quantum h2c comparison; candidate WZ alone is not full Q2',
          'Reuse existing logarithmic_contact_engine; new D_t and cutoff source in delivery_manifest',
          'Recover pending reviewers with same IDs; do not alter their independent payloads',
          'A7.c only after24h A7.b if unpaid; then A7.d,A8,PartB and final audit'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: cutoff e descida nao linear da candidata; {checks} controles, CPU{cpu}s; Q2completaOPEN. Custo parcialUS${cost}, desconhecido≠zero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(report),measure=str(measure),checks=checks,cpu_seconds=cpu,artifacts=len(files),partial_cost=str(cost))))
