"""Persist bounded results and model receipt with byte backups."""
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
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'ghost_minimal_heat/results.json').read_bytes())
report=f'''[DERIVED — operador ghost em fundo fixo; REAL — controles CAS; OPEN — contatos causais]
# A7.b — redução covariante da contribuição quadrática ghost
Abertura SHA256 `{opening}`. UTC {now}.

Não se varia o fundo g nem se diferencia o calor livre on-shell. Varia-se
somente h no operador realmente presente na ação069: Q(h)c=C_g L_c(g+h).
Identificamos vetores/covetores por g, h como endomorfismo, K a curvatura,
C_nu(h)=nabla^mu h_mu,nu-(1/2)nabla_nu trh. A expansão dá exatamente

    Q(h)=(I+h)(box+3K)+A^lambda nabla_lambda+B,
    A^lambda_nu,rho=nabla_rho h^lambda_nu+nabla^lambda h_rho,nu
                      -nabla_nu h^lambda_rho+delta^lambda_nu C_rho(h),
    B_nu,rho=nabla_rho C_nu(h).

O termo de ordem zero usa dois comutadores distintos. Com a convenção
R^a_bmn=K(delta^a_m g_bn-delta^a_n g_bm),

    [nabla^mu,nabla_rho]h_mu,nu=4K h_rho,nu-K g_rho,nu trh,
    h_mu,a [nabla^mu,nabla_nu]c^a=K(trh g_nu,rho-h_nu,rho)c^rho.

Sua soma é 3K h. Também nabla_lambda A^lambda=B+box h: os dois
comutadores adicionais cancelam por simetria de h. Tudo isso foi conferido
por índices no CAS. Em coordenadas normais, h coordenadamente constante
tem B=-2K h, enquanto box c=partial²c-Kc na origem; o termo 2K h restante
cancela. Esse controle impede confundir componentes constantes com campo
covariantemente paralelo. O operador reduzido reproduz o vértice plano
inteiro, não apenas seu símbolo principal.

## Resíduo integrado, com as hipóteses analíticas explícitas

Perto de h=0, M=I+h é invertível como série formal. Escreva
Qtilde=M^-1 Q=box+3K+a^mu nabla_mu+b, com a=M^-1 A,b=M^-1 B.
Com a conexão nablatilde=nabla+a/2, o endomorfismo é
E=3K+b-(nabla_mu a^mu)/2-a_mu a^mu/4. Até grau2 em h:

    E1=(B-box h)/2,
    E2=-hB+(1/2)nabla_mu(h A^mu)-(1/4)A_mu A^mu,
    Omega1_mu,nu=F_mu,nu/2, F_mu,nu=nabla_mu A_nu-nabla_nu A_mu,
    Omega2_mu,nu=-[nabla_mu(h A_nu)-nabla_nu(h A_mu)]/2
                  +[A_mu,A_nu]/4.

Para o traço local de calor integrado, a classificação de invariantes de
operador Laplace fornece tr(E²/2+R E/6+Omega²/12), além da parte puramente
geométrica fixa e divergências. Os coeficientes 1/2,1/6,1/12 são os mesmos
fixados pelo transporte de calor livre já derivado; o uso dessa classificação
para E não paralelo é uma hipótese analítica explicitada, não uma saída CAS.
Como R=12K,E0=3K e nabla Omega0=0, a parte quadrática, módulo divergências, é

    a4_2 = tr{{ 5K[-hB-A_mu A^mu/4]
             +(B-box h)^2/8+F_mu,nu F^mu,nu/48
             +Omega0_mu,nu[A^mu,A^nu]/24 }}.

Essa expressão mantém a ordem matricial e os comutadores da conexão. Ela
é covariante e contém a contribuição curva, mas ainda não foi reduzida a
uma base mínima de operadores K nabla² e K² nem combinada ao setor métrico.
Não foi extraída do número de calor livre -571K²/15.

Para identificar seu log com o operador original Q, usamos a ciclicidade
do resíduo logarítmico de símbolos: variando log Q, o fator M acrescenta
Tr(M^-1 delta M), puramente multiplicativo, sem termo de símbolo de ordem-4.
Assim não acrescenta resíduo log. Isto **não** é identidade dos determinantes
finitos; uma anomalia multiplicativa finita/contato não foi descartada.
Ciclicidade/classificação do resíduo permanecem condições analíticas a auditar.
As integrações por partes usam h compacto ou identificam densidades módulo
divergência. Com cutoff variável, suas derivadas precisam ser restauradas.

## Controle contra o laço já calculado

No plano, h=a A exp(ipx)+b B exp(-ipx). O coeficiente de ab em a4_2 é
tr(E1_A E1_B)+(1/6)tr(Omega1_A Omega1_B). Ele reproduz, SEM ajuste de fator,
os cinco coeficientes da bolha ghost já medida, com A0 retirado:

    [1/12,7/48,-1/8,-1/12,1/6].

Conferidos os55 pares da base simétrica, uma polarização densa não axial,
a troca de pernas, o vértice simbólico e os comutadores. {r['checks']} checks,
3 controles negativos; rc0, CPU {r['cpu_seconds']}s. Retirar a curvatura
da conexão do calor plano altera o teste e12 por -1/3. A peça ghost
isolada continua longitudinalmente não nula (e00/e00 dá1/16).

É uma fórmula candidata explícita para o resíduo ghost curvo, com controle
plano independente. Não é a hierarquia causal completa, não calcula a parte
finita de Q2 e não demonstra cancelamento com os outros setores. A auditoria
externa pedirá a redução dos operadores e um contraexemplo à identificação
do log, se houver. Nenhum original, kernel ou gate foi alterado.
'''
rp=O/'ENTREGA_016_A7b_reducao_ghost_curvo.md';save(rp,report);save(H/'ghost_minimal_heat/DERIVACAO.md',report)
# Recovering a result is not a new execution; preserve its IDs and usage.
job='2177daf6-29db-4d0c-940a-63d4c582fa04';rec=json.loads((H/'received_reviews'/f'{job}.json').read_bytes())
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
events=[dict(event='A7_KIMI_METRIC_REVIEW_RECEIVED',at=now,provider='kimi',target='A-7.b',
 job_id=job,request_id=rec['request_id'],execution_id=rec['execution_id'],
 prompt_sha256=rec['prompt_sha256'],response_sha256=rec['response_sha256'],
 usage=rec['result_metadata'].get('usage'),cost_estimate_usd=rec['result_metadata'].get('cost_estimate_usd'),
 new_external_execution=False,statute='DECLARADO_RECEIVED_AND_READ_LOCAL_AUDIT_PENDING'),
 dict(event='A7_GHOST_FIXED_BACKGROUND_MINIMAL_HEAT',at=now,provider='local',target='A-7.b',
 cpu_seconds=r['cpu_seconds'],checks=r['checks'],negative_controls=3,report_sha256=sha(rp),
 full_Q2=False,new_external_execution=False)]
for e in events:
 if e['event'].encode() not in raw:raw+=(json.dumps(e,ensure_ascii=False)+'\n').encode()
save(ledger,raw)
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
save(H/'ghost_minimal_heat/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),
 ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
files=[H/p for p in ['ghost_minimal_heat_engine.py','ghost_minimal_heat_check.py',
 'ghost_minimal_heat_run.log','ghost_minimal_heat/PRE_REGISTER.json','ghost_minimal_heat/results.json',
 'ghost_minimal_heat/manifest.json','ghost_minimal_heat/DERIVACAO.md','ghost_minimal_heat/COST_SNAPSHOT.json']]+[Path(__file__),rp]
save(H/'ghost_minimal_heat/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Fixed-background ghost operator reduced covariantly; flat bubble reproduced with127checks',
 'Explicit integrated quadratic ghost heat residue written with analytic assumptions visible',
 'Kimi metric review received; next Kimi curvature unit running; queue advanced'],
 ghost_minimal_heat_manifest=str(H/'ghost_minimal_heat/delivery_manifest.json'),
 next=['Reduce curved ghost quadratic residue to differential Hessian; audit analytic scope independently',
 'Review Kimi metric report errors and clarify double-gauge wording without changing paid coefficients',
 'A7.b full curved sum/finite hierarchy;A7.c only24h;A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: redução ghost covariante em fundo fixo,127checks,CPU{r["cpu_seconds"]}s, log integrado condicionado; Q2OPEN. Kimi métrico recebido; custo parcialUS${cost},desconhecidos nãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
print(json.dumps(dict(report=str(rp),cost_known_partial=str(cost),manifest=str(H/'ghost_minimal_heat/delivery_manifest.json')),ensure_ascii=False))
