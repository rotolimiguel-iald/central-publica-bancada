"""Record smooth-reference contacts and the external density transport."""
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
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((H/'smooth_source_contact/results.json').read_bytes())
d=json.loads((H/'covariant_source_density/results.json').read_bytes())
# Separate the two placements of external derivatives instead of using p+q=0
# to erase derivative ordering before covariant integration by parts.
M=s.Matrix([[2,0],[0,1],[2,1]])
split=s.Matrix([[s.sympify(x) for x in row] for row in d['split_values']])
A=M.gauss_jordan_solve(split[:,0]+split[:,2])[0]
B=M.gauss_jordan_solve(split[:,1]+split[:,3])[0]
assert list(A)==[s.Rational(13,12),s.Rational(19,12)]
assert list(B)==[-3,-s.Rational(1,2)]
save(H/'covariant_source_density/derivative_placements.json',dict(
    basis=['2(v.T.p)','tr(T)(p.v)'],A_source_first_jet=list(map(str,A)),B_ghost_first_jet=list(map(str,B)),
    real_space='K[-13/6 (nabla_b T^ab)v_a -19/12(nabla_a trT)v^a -6 T^ab nabla_a v_b -1/2 trT nabla_a v^a]',
    after_first_order_IBP='K[-23/6 T^ab nabla_a v_b +13/12 trT nabla_a v^a]',
    unresolved='Third-order principal source jets still require derivative-order transport; not a final covariant ghost operator'))
smooth=f'''[DERIVED — contribuição de referência suave; REAL — CAS; OPEN — soma Ward]
# A7.b — resíduo nulo não elimina o contato finito
Abertura SHA256 `{opening}`. UTC {now}.

Na bolha h-dagger/c já construída, trocar um propagador pela diferença suave W
entre duas referências de Hadamard deixa apenas três tipos com grau de escala4:

    (partial_Y W_G)(partial_X partial_Y z^-1),
    (partial_X partial_Y z^-1)(partial_Y W_H),
    (partial_X partial_Y z^-1)W_H nabla(v).

Os demais produtos têm grau abaixo4 e são localmente integráveis. Termos
superiores do Taylor de W também reduzem o grau; W_G W_H é suave.
O numerador angular da derivada segunda é -2delta_ij+8n_i n_j.
Sua média em S3 é zero, pois <n_i n_j>=delta_ij/4. Logo **a mudança suave
não altera o resíduo logarítmico desta bolha**. A conclusão não exige escolher
W=0 e não se estende por esse argumento a outros grafos ou à anomalia completa.

Mas a prescrição fixa R tem

    R(partial_i partial_j z^-1)-partial_i partial_j z^-1
      =-(C/4)delta_ij delta,
    R(partial_Xi partial_Yj z^-1)-partial_Xi partial_Yj z^-1
      =+(C/4)delta_ij delta.

Aqui C é retirado como nas entregas anteriores (euclidiano:-4pi²); a
continuação Lorentziana completa não é presumida. Multiplicação por um
coeficiente suave reduz esse contato ao seu valor de coincidência.

**Mapa local nos jatos suaves.** Todos os W e suas primeiras derivadas abaixo
são avaliados em X=Y, em referencial normal; fatores globais da bolha ficam
separados. Denote D_a v^b o primeiro jato externo. Por contração dos mesmos
vértices da fonte e do ghost,

    N_W/C = -1/4 T^munu v^m (partial_Ymu W_G^mnu)
             -1/2 T^ab sum_m [
                 v^r partial_Yr W_H(am,bm)
                 +(D_b v^r) W_H(am,rm)+(D_m v^r) W_H(am,br)
                 -delta_bm/2 v^r sum_l partial_Yr W_H(am,ll)
                 -delta_bm sum_l (D_l v^r) W_H(am,lr) ].

Índices repetidos são somados. Na primeira parcela, o numerador métrico
trace-reversed contrai com a reversão de traço do vértice ghost: I_tr²=id.
Por isso aparece T^munu, e não I_tr(T)^munu. A fórmula representa a diferença
entre estender os kernels fora da diagonal por R e conservar a derivada do
propagador já estendido. Não é uma anomalia física inferida de W.

Controle: W_H(ab,cd)=wI(delta_ac delta_bd+delta_ad delta_bc)/2+wT delta_ab delta_cd,
primeiros jatos nulos e W_G sem contribuição dão

    N_W/C=-(wI+wT)T^ab D_a v_b
           -(wI/4-wT/2)tr(T) D_a v^a.

Com wI=1,wT=0,T01=T10=1,D0v1=1, o resultado é -1, não zero.
É controle algébrico, não alegação de que jatos arbitrários definem um estado
físico no espaço curvo. O cancelamento com os outros contatos ainda deve ser
testado na mesma referência admissível. CAS:{r['checks']}assertivas,rc0,
CPU{r['cpu_seconds']}s. Não foi acrescentado leitor/gate ao programa.
'''
density=f'''[DERIVED — transporte da fonte externa; REAL — CAS; OPEN — operador covariante completo]
# A7.b — o transporte dos propagadores não dispensa o da fonte
Abertura SHA256 `{opening}`. UTC {now}.

O relatório anterior fixou T^ab como densidade contravariante em coordenadas.
Se t^ab representa o tensor fonte no referencial transportado a partir de Y,

    T(X)=sqrt(g(X)) P(X,Y) t(X) P(X,Y)^t,
    P(x,0)=I+(K/6)(Iz-xx^t),   sqrt(g)=1-Kz/2+…,
    T=t-(K/6)[z t+xx^t t+t xx^t]+… .

Essa parcela deve multiplicar o núcleo plano antes da leitura covariante.
Sua ordem em x é2: contribui ao termo de Taylor de ordem1 na parcela v
e de ordem0 na parcela Dv. Não é correção arbitrária dos coeficientes.

Na base 2(v^t t p), tr(t)(p·v), a contribuição geométrica com fonte
coordinate fixa era (-10/3,5/3). Depois de incluir a densidade e o
transporte dos índices da fonte, o perfil passa a **(-23/12,13/12)**.
Ambos os resultados são preservados com a respectiva convenção; não se
deve transportar a propriedade "sem traço" do perfil antigo ao novo.

As colocações das derivadas permanecem separadas:

| termo | coeficiente de 2(vtp) | coeficiente de tr(t)(pv) |
|---|---:|---:|
| Taylor de primeira ordem da fonte, parcela v |13/12|19/12|
| primeiro jato do ghost externo, parcela Dv |-3|-1/2|
| soma do perfil de momentos |-23/12|13/12|

Em posição, a parte explicitamente proporcional a K fornece

    K[-13/6 (nabla_b t^ab)v_a -19/12(nabla_a trt)v^a
       -6 t^ab nabla_a v_b -1/2 trt nabla_a v^a].

Sob integração por partes de primeira ordem e suporte compacto, vira
K[-23/6 t^ab nabla_a v_b+13/12 trt divv]. Isso ainda NÃO identifica
todo o operador covariante: a parte principal contém jatos simétricos
de terceira ordem da fonte e de segunda ordem junto a Dv. Ao transportar
essas derivadas, os comutadores geram termos de curvatura adicionais.
Apagá-los por conservação de momento antes dessa operação seria circular.

CAS: três polarizações de ajuste, compatibilidade da terceira linha,
polarização densa não axial (resultado -33), identidade da densidade
transportada;rc0,CPU{d['cpu_seconds']}s. A fórmula dos jatos geométricos
usa os controles independentes da entrega anterior. Não é repetição de laço.

Escopo: contribuição singular, duas inserções, primeira ordem K, interior
de cutoff constante. A parte suave não muda esse resíduo, mas seus contatos
finitos foram mantidos na entrega irmã. Ainda faltam a ordenação covariante
completa, a prescrição finita e a soma causal. A7.b ativa; originais/gate intactos.
'''
reports=[(O/'ENTREGA_016_A7b_referencia_suave_contatos.md',H/'smooth_source_contact/DERIVACAO.md',smooth),
 (O/'ENTREGA_016_A7b_transporte_densidade_fonte.md',H/'covariant_source_density/DERIVACAO.md',density)]
for rp,local,text in reports:save(rp,text);save(local,text)
configs=[('smooth_source_contact',['smooth_source_contact_check.py','smooth_source_contact_run.log']),
 ('covariant_source_density',['covariant_source_density_check.py','covariant_source_density_run.log'])]
for (folder,names),(rp,local,text) in zip(configs,reports):
    files=[H/n for n in names]+[H/folder/n for n in ['PRE_REGISTER.json','results.json','manifest.json','DERIVACAO.md']]+[rp]
    if folder=='covariant_source_density':files.append(H/folder/'derivative_placements.json')
    save(H/folder/'delivery_manifest.json',dict(at=now,opening_sha256=opening,
     artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=O/'LEDGER_016.jsonl';marker='A7_SMOOTH_REFERENCE_AND_EXTERNAL_DENSITY'
cpu=r['cpu_seconds']+d['cpu_seconds']
if marker.encode() not in ledger.read_bytes():
    ev=dict(event=marker,at=now,provider='local',target='A-7.b',cpu_seconds=cpu,
      smooth_contact_checks=r['checks'],new_external_execution=False,full_Q2=False,
      report_sha256=[sha(rp) for rp,_,_ in reports])
    save(ledger,ledger.read_bytes()+(json.dumps(ev,ensure_ascii=False)+'\n').encode())
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()];par={}
def root(k):
    par.setdefault(k,k)
    if par[k]!=k:par[k]=root(par[k])
    return par[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for r0 in rows:
    ix=ids(r0)
    for k in ix[1:]:par[root(k)]=root(ix[0])
known={}
for r0 in rows:
    ix=ids(r0);v=r0.get('cost_estimate_usd',r0.get('cost_usd',r0.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
total=sum(known.values(),Decimal(0))
save(H/'covariant_source_density/COST_SNAPSHOT.json',dict(at=now,total_known_partial=str(total),
 ledger_sha256=sha(ledger),unknown_cost_not_zero=True,billing_not_verified=True))
cont=H/'CONTINUIDADE.json';c=json.loads(cont.read_bytes());c.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 completed_this_turn=['Smooth-reference changes leave zero log residue but nonzero explicit finite contact in source bubble',
  'Transport of external contravariant density included; first-K profile now -23/12,13/12 with derivative placements retained'],
 smooth_source_manifest=str(H/'smooth_source_contact/delivery_manifest.json'),
 covariant_source_density_manifest=str(H/'covariant_source_density/delivery_manifest.json'),
 next=['Build covariant principal source-jet counterterm before commuting derivatives; then combine finite curved Ward contacts',
  'Receive pending distinct Kimi/MiMo/DeepSeek reviews without repetition',
  'A7.c only if24h exhausted;A7.d,A8,PartB and final full audit remain'])
save(cont,c)
p=O/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {now} — A7.b PROGRESSO:resíduo log independente de W nesta bolha,contato finito W explícito;fonte transportada(-23/12,13/12),CPU{cpu}s;Q2curvaOPEN. Custo parcialUS${total},desconhecidos nãozero;ledger{sha(ledger)};abertura{opening}.\n'.encode())
print(json.dumps(dict(reports=[str(rp) for rp,_,_ in reports],cpu_seconds=cpu,cost_partial=str(total),status='ACTIVE_PROGRESS')))
