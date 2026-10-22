"""Deliver the full integrated ghost log; preserve causal/analytic limitations."""
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
r=json.loads((H/'ghost_curved_hessian/results.json').read_bytes())
report=f'''[DERIVED — resíduo ghost integrado condicionado; REAL — CAS exato; OPEN — Q2 causal]
# A7.b — contribuição ghost curva quadrática em todos os componentes
Abertura SHA256 `{opening}`. UTC {now}.

**Objeto.** Q(h)=C_g L_c(g+h), com g FIXO no espaço-forma4D, Ric=3K g.
Somente h varia. Do operador reduzido Qtilde=(I+h)^-1Q e do resíduo de calor
da entrega anterior, mantidas suas hipóteses analíticas, foi calculado o
termo quadrático inteiro. Não se diferenciou o calor livre on-shell.
Notação: t=trh, u_nu=nabla^mu h_mu,nu, d=divu; todos os produtos usam g.

**Resultado integrado, módulo divergências:**

    a4_2[h] = (box h)^2/24+7(box t)^2/96-d(box t)/8
              -(nabla u)^2/24+d²/12
            +K[7(nabla h)^2/12-17(nabla t)^2/12
                +(7/2)u·nabla t-(79/24)u²]
            +(13K²/6)(4h²-t²).

O fator angular e a ponderação do determinante seguem a convenção da bolha
anterior. A polarização bilinear plana reproduz exatamente os cinco
coeficientes [1/12,7/48,-1/8,-1/12,1/6], sem ajuste de normalização.

Uma forma ordenada de sua Hessiana, com G(v)_ab=nabla_a v_b+nabla_b v_a,
é (a integração usa volume de fundo, não uma segunda densidade variável):

    Hghost(h) = box²h/12+(7/48)g box²t
      -(Hess(box t)+g box d)/8-G(box u)/24+Hess(d)/6
      +K[-7box h/6+(17/6)g box t
          -(7/2)(Hess t+g d)+(79/24)G(u)]
      +(13K²/3)(4h-g t).

Essa fórmula é o segundo diferencial da densidade integrada acima; box u
é o laplaciano covariante de vetor/covetor. Não se permutam suas derivadas
como escalares. A forma integrada, e não uma extensão temporal finita,
é o objeto demonstrado pela redução algébrica desta entrega.

**Como foi obtido.** A expressão-mãe é
tr{{5K[-hB-A_mu A^mu/4]+(B-boxh)^2/8+F²/48+Omega0[A,A]/24}}.
Cada termo foi convertido em palavras ordenadas de derivadas covariantes.
O adjunto inverte a palavra e acrescenta (-1)^n; a contração de fibras
continua explícita. O operador não reduzido tem3080 termos; o representante
de quatro derivadas tem1060. A diferença a primeira ordem emK fixa os quatro
coeficientes de gradiente; a ordemK² fixa os dois coeficientes sem derivadas.

Os jatos foram calculados em coordenadas normais, sem projetar fora
comutadores. Para a ordemK há dois algoritmos: inserção única de Gamma
diferenciada e recorrência direta da derivada de cada slot tensorial.
Para K² usa-se a conexão cúbica extraída independentemente da métrica exata:

    g=I-(K/3)(zI-xx^t)+(2K²/45)(z²I-zxx^t)+…,
    Gamma2^a_bc= -z(x_b delta_ac+x_c delta_ab)/45
                 -(2z/15)x_a delta_bc+(8/45)x_a x_b x_c.

Conferidos64 componentes em cada ordem da conexão,2560 jatos de quarta
derivada por dois algoritmos, os55 pares bilineares da base simétrica em
cada ordem e um controle denso não axial. Covariância O(4) e homogeneidade
estendem o teste completo axial: o operador local de ordem4 tem somente
as ordens p⁴,Kp²,K². Essas verificações dão a identidade diferencial
algébrica no espaço-forma, condicionada à expressão-mãe de calor.

**Controles.** No canal h=f g, a redução devolve
integral[7(box f)²/8-19K(df)²/2], medido antes independentemente; o potencial
K² se anula para h=f g constante covariante. Descartar os comutadores muda
o primeiro controleK por -34/9. Apagar o potencialK² muda por104/3.
{r['checks']} checks de componentes,2 negativos,rc0,CPU {r['cpu_seconds']}s.
Os coeficientes foram explorados antes desta verificação, registrado no plano;
não se apresenta esse ajuste como análise cega nem como2913 provas distintas.

**Alcance.** As condições ainda são as da redução de calor: classificação
local do resíduo, ciclicidade do resíduo de símbolos sob o fator multiplicativo,
h formalmente pequeno, suporte compacto ou divergências mantidas à parte.
Não é igualdade de determinantes FINITOS. Com cutoff variável há contatos
a restaurar. Não inclui a Hessiana métrica, tadpoles métricos, fontes BV nem
a soma de ghost1/Q2. A continuação causal completa permanece aberta.
Nenhuma alteração de um.py, kernel, gate ou originais. Próximo cálculo:
vértices cúbico/quártico métricos de curvatura e sua combinação com a fonte.
'''
rp=O/'ENTREGA_016_A7b_ghost_curvo_quadratico.md';save(rp,report);save(H/'ghost_curved_hessian/DERIVACAO.md',report)
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_COMPLETE_CURVED_GHOST_INTEGRATED_LOG'
if marker.encode() not in raw:
 event=dict(event=marker,at=now,provider='local',target='A-7.b',checks=r['checks'],
 cpu_seconds=r['cpu_seconds'],report_sha256=sha(rp),full_Q2=False,new_external_execution=False)
 save(ledger,raw+(json.dumps(event,ensure_ascii=False)+'\n').encode())
rows=[json.loads(t) for t in ledger.read_text('utf-8-sig').splitlines() if t.strip()];parents={}
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
save(H/'ghost_curved_hessian/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(cost),
 ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
files=[H/p for p in ['ghost_covariant_word_engine.py','spaceform_covariant_jet_engine.py',
 'ghost_curved_hessian_check.py','ghost_curved_hessian_run.log','ghost_curved_hessian/VERIFICATION_PLAN.json',
 'ghost_curved_hessian/results.json','ghost_curved_hessian/manifest.json','ghost_curved_hessian/DERIVACAO.md',
 'ghost_curved_hessian/COST_SNAPSHOT.json']]+[Path(__file__),rp]
save(H/'ghost_curved_hessian/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Full integrated quadratic ghost log derived with K derivative and K² potential terms',
 'Normal-coordinate connection to K² and independent derivative-word recurrence checked;2913assertions',
 'Kimi curvature unit confirmed running by Coordination.get; no duplicate dispatch'],
 ghost_curved_hessian_manifest=str(H/'ghost_curved_hessian/delivery_manifest.json'),
 latest_live_execution=dict(job_id='679d8876-d8b9-44db-ae96-3f8f8f67fb54',execution_id='4ead6294-6bed-403f-9932-c1b255c0a8ef',status='running',observed_utc='2026-09-25T03:02:28Z'),
 next=['Metric curvature cubic/quartic vertices then curved loops/tadpoles; combine with ghost and source terms',
 'Keep external pending reviews independent; no payload mutations',
 'Finite temporal hierarchy and fullQ2 remain;A7.c onlyafter24h;A7.d,A8,PartB and finalaudit remain'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: logghostcurvo quadrático inteiro condicionado,2913checks,CPU{r["cpu_seconds"]}s;Kgradientes e13K²(4h²-t²)/6. Q2OPEN;originais/gateintactos. Custo parcialUS${cost};desconhecidosnãozero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
print(json.dumps(dict(report=str(rp),manifest=str(H/'ghost_curved_hessian/delivery_manifest.json'),cost_known_partial=str(cost))))
