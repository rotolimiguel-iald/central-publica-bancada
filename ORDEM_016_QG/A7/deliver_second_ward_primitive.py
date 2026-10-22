"""Record second-K Ward measure and its restricted local quadratic primitive."""
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
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
folders=['second_curvature_ward_v2','linear_curvature_tadpole','local_quadratic_ward_primitive','local_ward_family_einstein']
results={};files=[]
for folder in folders:
    results[folder]=json.loads((H/folder/'results.json').read_bytes())
    m=H/folder/'manifest.json'
    for a in json.loads(m.read_bytes())['files']:
        p=Path(a['path']);assert sha(p)==a['sha256'];files.append(p)
    files.append(m)
checks=sum(r['checks'] for r in results.values());cpu=sum(r['cpu_seconds'] for r in results.values())
rp=O/'ENTREGA_016_A7b_Ward_K2_e_primitiva_quadratica_local.md';assert not rp.exists()
save(rp,f'''[DERIVED — componente logarítmico local e primitiva; REAL — CAS; OPEN — Q2 completa]
# A7.b — Ward K², tadpole linear e primitiva quadrática
Abertura SHA256 `{opening}`. UTC {now}.

**Calibração:** jatos covariantes da 1-forma até ordem5 e K², incluindo
coframe e conexão do espaço-forma. A derivada dupla da identidade
clássica E G(c)=0 foi conferida em768 componentes;48 componentes
reproduzem a Ward primeiraK anterior. Duas extrações completam818
controles. Não se impôs zero à Ward de laço.

Retirando i*hbar*A0, A0=1/(8pi²), na base K²[G(v),g(p.v)]:

    H_loop G = [4/3,−20/3]
    E R      = [20/3,8/3]
    soma     = [8,−4].

A fonte já paga é R=G(3Box(v)/8−grad(divv)/4−37Kv/8)+2Kg divv.
Usando E G=0, E R=−4K Hess(divv)+4Kg Box(divv)+12K²g divv.
Essa fórmula e os jatos dão os coeficientes acima sem ajuste.

**Tadpole linear:** contração dos vértices cúbicos com os Green
coincidentes. A densidade é hbar*A0*K²*tau*trh, com tau_métrica=−6,
tau_ghost=0, tau_total=−6. Dez fibras verificam a proporcionalidade
ao traço,31controles. A variação não linear clássica desta densidade,
integrada com suporte compacto, contribui tau*K²[G(v)−g(p.v)].
Logo o resíduo medido DEPOIS dessa parcela é

    R_K2(v)=2K²[G(v)+g(p.v)],

e continua não nulo. A primeiraK permanece

    R_K1(v)=K[−p²G(v)/2+2pp(p.v)−5gp²(p.v)/2].

**Primitiva local desse componente:** na convenção de símbolo covariante
com derivadas simétricas, defina o operador formalmente autoadjunto
deltaH_t. Seu símbolo Kp², na base
[p²trAB,p²trA trB,pAp trB,pBp trA,pABp], tem coeficientes

    [1/2−t/2, 9/4+t/2, −1−t/2, −1−t/2, t].

A contribuição desse operador à Ward K² é[−t−13/3,2t+38/3].
Acrescente o símbolo K², na base[trAB,trA trB],

    [t+7/3,−t−22/3].

Então deltaH_t G(v)=−R_K1(v)−R_K2(v) nas ordens calculadas,
para todo t real.97controles polinomiais, incluindo um momento fora
do eixo usado na determinação dos coeficientes.

O funcional é explícito:

    B_t[h]=(1/2) integral h·deltaH_t h,
    s0 B_t=integral h·deltaH_t G(c).

Autoadjunção usa os coeficientes invariantes paralelos, simetria entre
as fibras, duas derivadas simetrizadas e suporte compacto. Assim, o
componente logarítmico integrado, linear em h e c, aqui MEDIDO admite
essa primitiva relativa ao diferencial livre. Não é uma conclusão sobre
todos os componentes da anomalia não linear nem sobre sua parte finita.

**A liberdade t foi identificada, não escolhida:**

    partial_t deltaH_t = −K E/2.

640 controles, dez fibras e dois momentos, verificam a igualdade nas
duas ordens homogêneas. Ward não determina esse parâmetro porque
E G=0. Isso não classifica as31direções do ajusteA2 anterior e não
demonstra não trivialidade de uma classe na cohomologia BV completa.

**Cutoff e continuação:** para chi inerte e B_chi=1/2 integral chi h·D h,
a polarização fornece s0 B_chi=integral h·(chi D+[D,chi]/2)G(c).
Reutiliza-se a identidade já verificada em finite_cutoff_contact e
finite_cutoff_position; seus testes anteriores são planos e não são
apresentados como novos testes curvos. Aqui D=deltaH_t tem ordem2:
se sua parte diferencial é K C^ij nabla_(i nabla_j),

    [D,chi]T=K C^ij[(nabla_i nabla_j chi)T+2(nabla_i chi)nabla_j T].

O termo K² comuta com chi. Esses contatos precisam entrar; a parte
s1 B_t, de ordem h²c, também não foi apagada. A identificação com a
quebra completa da prescrição temporal ainda exige essa hierarquia.
Nenhum t selecionado, contratermo adotado ou prescrição alterada.

Pacote:{checks} controles, CPU{cpu}s. Falhas técnicas preservadas:
primeiro avaliador omitiu uma soma em m (NameError, versão v2 ao lado);
primeira invocação da auditoriaEinstein usou Python semSympy (rc1),
seguida pelo runtime simbólico já existente (rc0), sem instalar pacote.
Logs, fontes, predecessores e resultados têm hashes no manifesto.
Gate, kernel e originais intactos. A7.b continua; Q2 completa OPEN.
''')
mp=O/'ENTREGA_016_MEDIDA_Ward_segundaK_com_tadpole.md';assert not mp.exists()
save(mp,f'''[REAL — resíduo não nulo na prescrição corrente; DERIVED — primitiva local delimitada]
Abertura SHA256 `{opening}`. UTC {now}.

Tentativa: somar Hessiana de laço, fonteBV e tadpole linear sem ajustar
coeficientes. Resultado:(H_loop G+ER+Gamma1_linear Lc h)_K2 tem
coeficientes[2,2] na base[K²G,K²g divc].
Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/linear_curvature_tadpole_check.py.
rc0,31controles; logSHA256 `{sha(H/'linear_curvature_tadpole_run.log')}`.
CPU{results['linear_curvature_tadpole']['cpu_seconds']}s. Nenhuma chamada externa.

Uma família B_t cancela esse componente e o da primeiraK quando
variada por s0, conforme entrega; não foi adotada nem apresentada como
prova da QME completa. Próxima etapa: contatoschi, s1 B_t e a comparação
com a anomalia temporal finita, preservando esse resíduo como evidência.
''')
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_SECOND_K_WARD_AND_LOCAL_QUADRATIC_PRIMITIVE'
assert marker.encode() not in raw
raw+=(json.dumps(dict(event=marker,at=now,target='A-7.b',provider='local',checks=checks,cpu_seconds=cpu,
    report_sha256=sha(rp),measure_sha256=sha(mp),full_Q2=False,new_external_execution=False))+'\n').encode();save(ledger,raw)
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
extra=['oneform_second_curvature_engine.py','second_curvature_ward_check.py','second_curvature_ward_run.log',
    'second_curvature_ward_v2_run.log','linear_curvature_tadpole_run.log','local_quadratic_ward_primitive_run.log',
    'local_ward_family_einstein_run.log','local_ward_family_einstein_symbolic_run.log','finite_cutoff_contact/results.json','finite_cutoff_position/results.json']
files+=[H/r for r in extra]+[rp,mp,Path(__file__)];files=list(dict.fromkeys(files))
manifest=H/'local_quadratic_ward_primitive/delivery_manifest.json';assert not manifest.exists()
save(manifest,dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',completed_this_turn=['SecondK Ward818checks, pre-tadpole[8,-4]',
    'Linear tadpole31checks tau=-6, residualK2[2,2]','Quadratic local primitive97checks; parameter remains unchosen',
    'Homogeneous freedom=-K EinsteinHessian/2,640checks'],local_quadratic_primitive_manifest=str(manifest),partial_metered_cost_usd=str(cost),
    next=['Extend local primitive with cutoff currents and nonlinear s1B_t; compare against finite temporal anomaly, not just log',
        'No representative selected and no prescription changed; both raw Ward residuals preserved',
        'Current coordinator5registered/6staging, Kimi completion running; recover same IDs only',
        'A7.c after24h if unpaid, then A7.d,A8,PartB and finalaudit'])
save(cont,d)
progress=O/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: WardK²+tadpole eprimitivaquadrática delimitada; {checks}controles, CPU{cpu}s. Resíduoprescrição[2,2]preservado;familialocalnãoadotada;Q2OPEN. Custo parcialUS${cost}, desconhecido≠zero. Abertura{opening};ledger{sha(ledger)}.\n'.encode())
for a in json.loads(manifest.read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(report=str(rp),measure=str(mp),checks=checks,cpu_seconds=cpu,artifacts=len(files),partial_cost=str(cost))))
