"""Deliver completed algebra and reviews; the large Fourier run stays pending."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT';D=H/'gauge_generator_reviews_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        assert existing,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(data)
    assert t.read_bytes()==data;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False),existing)
gen=json.loads((H/'first_curvature_gauge_generating/results.json').read_bytes())
cub=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())
ka=json.loads((H/'kimi_curved_antifield_audit/audit_results.json').read_bytes())
da=json.loads((H/'deepseek_logarithmic_contact_audit/audit_results.json').read_bytes())
kr=json.loads((H/'kimi_curved_antifield_audit/RECEIPT.json').read_bytes())
dr=json.loads((H/'deepseek_logarithmic_contact_audit/RECEIPT.json').read_bytes())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
gf=O/'ENTREGA_016_A7b_gerador_Taylor_covarante_primeira_curvatura.md'
write(gf,f'''[DERIVED — gerador exato em K1; REAL — CAS; OPEN — amplitude integrada]
# A7.b — soma dos jatos, preservando a ordem
Abertura SHA256 `{opening}`. UTC {now}.

No mesmo campo radial v_a(x)=[delta_a^b-K(z delta_a^b-x_a x^b)/6]
v_b exp(p.x)+O(K²), derivamos uma expressão fechada para

    sum_n D_y D_x^n D_i G(v)/n! = exp(p.x) (P0+P1+P2) +O(K²),

onde Pj é homogêneo de grau j em x. D_y/D_i são mantidos quando o vértice
os exige. p é formal REAL nesta fórmula; as fases i são restauradas por
grau homogêneo antes da integração. Não identificamos boost com rotação.

**Derivação para todo n.** Em K1, a expansão de uma palavra de derivadas
recebe: (a) a segunda derivada do coframe, escolhendo dois lugares;
(b) uma derivada de Gamma atuando no índice final, escolhendo dois lugares;
(c) uma derivada de Gamma atuando em outro índice de derivada, escolhendo
três lugares ordenados. Os demais lugares dão fatores p. Ao selecionar k
lugares do bloco radial de tamanho n, a multiplicidade é binomial(n,k).
Dividir por n! e somar n dá exp(p.x)/k!. O termo de grau3 é zero porque
d_x Gamma(x,x)=0 na carta normal do espaço-forma. Assim restam graus0..2;
não é ajuste de uma série truncada nem hipótese de momento comutante.

Conferência: palavras ordenadas com comprimentos1,3,5 contra a recursão
covariante anterior; gerador contra palavras até comprimento radial8,
dez fibras, duas escolhas de p/v e quatro disposições de índices dos
vértices. {gen['checks']} controles, rc0, CPU{gen['cpu_seconds']}s.

**Integração necessária:** os primeiros termos curvos têm grau angular
até6. Sua projeção harmônica exige momentos até12. A regra anterior, grau8,
não pode ser reutilizada como prova dessa integração. Construímos uma regra
exata por nove órbitas de vetores inteiros, {len(cub['nodes'])} nós, pesos
racionais (alguns negativos). Todos os {cub['checks']} monômios até grau12
foram conferidos; simetrias de sinal verificadas para os ímpares.
CPU{cub['cpu_seconds']}s, rc0. Os pesos não são probabilidades.

Uma execução separada está usando estes objetos e multiplicadores de
Laurent que preservam l>m. Seus resultados não integram esta entrega:
curved_pair_fourier_check.py, sessão própria93180, ainda não terminal
na última consulta. Nenhuma amplitude completa ou Q2 é declarada paga.
''')
kf=O/'ENTREGA_016_A7b_auditoria_Kimi_fonte_curva.md'
write(kf,f'''[REAL — auditoria geométrica; DERIVED — correções; DECLARADO — parecer Kimi]
# A7.b — fonte curva: correções antes de aproveitar o parecer
Abertura SHA256 `{opening}`. UTC {now}. Job `{kr['job_id']}`.
Uso informado {kr['usage']}; resposta integral e recibo preservados.

**Aceito:** o transporte paralelo com índice superior
Pi=I+K(zI-xx^t)/6 satisfaz a equação radial nesta ordem. Não confundir
essa aceitação com validação do bitensor misto da função mundo.

**Erros localizados:**
1. A equação principal põe a derivada do segundo termo U2 em M; a tabela
do próprio parecer a põe corretamente em G_Q. Como U2=h_am D_b c^m,
o termo correto é -2 T_ab (D_b^X D_Y G_Q) M_am. Para G_Q=t,M=1,
a regra correta dá1; derivar M dá0. Não executamos o pseudocódigo
incompleto como se fosse uma implementação.
2. Para g_ab=delta_ab-K(delta_ab z-x_a x_b)/3,
sum_c (partial_b g_ac)x_c=K(delta_ab z-x_a x_b)/3, em geral não zero.
A identidade radial g_ab x_b=x_a é verdadeira; não autoriza apagar a
derivada de x_b ao diferenciá-la.
3. Na convenção z=x²: (nabla z)²=4z e Box z=8-2Kz. Se z_alt=sigma/2=z/4,
(nabla z_alt)²=z_alt e Box z_alt=2-2K z_alt. Não misturar os coeficientes.
4. Delta=(r/sin r)^3=1+r²/2+...; sqrt(Delta)=1+r²/4+... .
u0=1+Kz/4 é compatível com sqrt(Delta), sem redefinir z.
5. Calor vezes calor é K²: o exemplo dá {ka['heat_product']}. Não entra
como termo linearK só por receber derivadas espaciais.

{ka['checks']} verificações próprias, rc0, CPU{ka['cpu_seconds']}s.
O parecer deixa a amplitude total OPEN e oferece um placeholder, não
um CAS completo. Conservamos o conteúdo aproveitável, os erros e as
lacunas separadamente; não substituímos os motores já verificados.
''')
df=O/'ENTREGA_016_A7b_auditoria_DeepSeek_contatos_logaritmicos.md'
write(df,f'''[DERIVED — fórmula preservada, argumento corrigido; REAL — CAS; OPEN — amplitude]
# A7.b — revisão DeepSeek dos contatos logarítmicos
Abertura SHA256 `{opening}`. UTC {now}. Job `{dr['job_id']}`.
Uso {dr['usage']}. Custo estimado informado {dr['cost_estimate_range_usd']}USD,
tarifa de pico como teto da estimativa, não fatura. Nenhuma repetição.

A fórmula recebida para R(D[z^-n L^ell])-D R(z^-n L^ell) coincide com
a fórmula da bancada sob a hipótese de polo simples da família base.
Mas a frase de que apenas t0,t1 da soma de Leibniz contribuem é falsa:

    ell=2, c(a)=a³, T(a)=rho/a:
    parcelas = [-6rho,+6rho,-2rho], soma=-2rho.

O corte t<=1 daria0. A forma final correta resulta da soma completa.
Para c=a^m, o termo m=ell+1 usa
sum_t binomial(ell,t)(-1)^t/(t+1)=1/(ell+1); o termo m=ell>=1 usa
sum_(t>=1) binomial(ell,t)(-1)^t=-1. A exceção ell=m=0 dá0.
O resto analítico da família não contribui para esse comutador local.

Conferimos graus ell0..6,m0..8 com e sem resto analítico. Também foram
conferidas as três contas do perfil: -3K/32, -37K/384 e -K/3072.
São {da['checks']} controles, rc0, CPU{da['cpu_seconds']}s.
O termo u0 citado é raiz de Van Vleck; chamar apenas de determinante
sem a raiz pode reproduzir a confusão corrigida na revisão Kimi.

A concordância vale para a álgebra do perfil sob R fixada. Não preenche
por si só existência distributiva, bitensores, soma causal ou Q2.
''')
files=[Path(__file__),gf,kf,df]
for stem in ('first_curvature_gauge_generating','angular_cubature_degree12'):
    files += [H/(stem+'_check.py'),H/(stem+'_run.log'),H/stem/'PRE_REGISTER.json',H/stem/'results.json',H/stem/'manifest.json']
files.append(H/'first_curvature_gauge_generating_engine.py')
for stem,receive,audit in [('kimi_curved_antifield_audit','receive_kimi_curved_antifield.py','audit_kimi_curved_antifield.py'),
                           ('deepseek_logarithmic_contact_audit','receive_deepseek_logarithmic_contact.py','audit_deepseek_logarithmic_contact.py')]:
    files += [H/receive,H/audit]+[H/stem/name for name in ('ANSWER.md','RECEIPT.json','AUDIT_PRE_REGISTER.json','audit_results.json','audit_run.log')]
manifest=dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'manifest.json',manifest)
for row in manifest['artifacts']:assert sha(Path(row['path']))==row['sha256']
ledger=O/'LEDGER_016.jsonl';events=[]
for provider,receipt,slug in [('kimi',kr,'kimi_a7_curved_antifield_source'),
                            ('deepseek',dr,'deepseek_a7_logarithmic_contact_skeptic')]:
    payload=H/'orchestration_curved_source'/(slug+'_submit.json');body=json.loads(payload.read_bytes())
    events.append(dict(at=now,event='A7_CURVED_REVIEW_RECEIVED_AND_AUDITED',provider=provider,target='A7.b',
        job_id=receipt['job_id'],request_id=body['request_id'],execution_task_id=receipt.get('execution_task_id'),
        prompt_sha256=hashlib.sha256(body['prompt'].encode()).hexdigest(),response_sha256=receipt['answer_sha256'],
        usage=receipt['usage'],cost_estimate_usd=receipt.get('cost_estimate_usd'),
        cost_status=receipt.get('cost_status','SUBSCRIPTION_COST_NOT_METERED'),new_external_execution=False,
        delivery_manifest_sha256=sha(D/'manifest.json'),full_Q2=False))
cpu=sum(q['cpu_seconds'] for q in (gen,cub,ka,da))
events.append(dict(at=now,event='A7_EXACT_GAUGE_GENERATOR_AND_CUBATURE',checks=gen['checks']+cub['checks'],
 audit_checks=ka['checks']+da['checks'],cpu_seconds=cpu,full_Q2=False))
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
rows=[json.loads(line) for line in ledger.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
parents={}
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
    ix=ids(row);value=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and value is not None:known[root(ix[0])]=Decimal(str(value))
cost=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,ledger_sha256=sha(ledger),known_partial_usd=str(cost),
 number_of_metered_identity_groups=len(known),unknown_calls_not_zero=True))
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: gerador covariante1728 + cubatura grau12/1820 + auditoriasKimi45/DeepSeek131; rc0,CPU{cpu}s. Custo parcial conhecidoUS${cost}, desconhecidos não são zero. Fourier curvo ainda executando sessão93180; Q2 OPEN.\n'.encode(),True)
cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',gauge_generator_reviews_manifest=str(D/'manifest.json'),
 partial_metered_cost_usd=str(cost))
v['completed_this_turn']=['FirstK covariant Taylor generator for all n derived,1728checks',
 'Degree12 S3 exact cubature1820checks; replaces degree8 only where higher harmonics demand it',
 'Kimi curved source45checks: preserve parallel propagator, reject mixed-z/derivative errors',
 'DeepSeek contact review131checks: formula accepted, full Leibniz sum required']
v['own_live_processes']=[dict(session_id=93180,script='curved_pair_fourier_check.py',
 status='RUNNING_CONFIRMED_BY_WRITE_STDIN',last_checked_utc=now)]
v['next']=['Poll own session93180, do not restart; log A7/curved_pair_fourier_run.log',
 'Full firstK pair still excludes source Einstein image,finite tadpole,W and higher arities',
 'Source orientation and nonlocal-reference derivative ordering must be established before combination',
 'A7.b until approximately20:32UTC; thenA7.c if unpaid,A7.d,A8,PartB,finalaudit']
v['latest_orchestration']=dict(at=now,source='Official coordinator completion message',registered=5,staging=5,
 currently_executing='Kimi ghost_curved_hessian_reduction')
v['latest_live_execution']=dict(job_id='3979f662-13f0-4848-8948-b9dacb8c590e',
 status='execution_waiting_owned_by_coordinator',observed_utc=now)
v['pending_orchestration']='5 nonterminal/5 staging per coordinator; reviews retain original prompts'
put(cont,v,True)
print(json.dumps(dict(delivered=True,artifacts=len(files),checks=gen['checks']+cub['checks']+ka['checks']+da['checks'],
 cpu_seconds=cpu,known_partial_cost_usd=str(cost),full_Q2=False)))
