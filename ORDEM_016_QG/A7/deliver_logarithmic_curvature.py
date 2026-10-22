"""Deliver the logarithmic extension maps and first curved pair profiles."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
lc=json.loads((HERE/'logarithmic_contact/results.json').read_bytes());hp=json.loads((HERE/'hadamard_pair_curvature/results.json').read_bytes())
report=f'''[DERIVED — contatos logarítmicos e primeiros perfis curvos; REAL — CAS; OPEN — soma causal curva]
# A7.b — a extensão fixa aplicada aos termos de Hadamard
Abertura SHA256 `{opening}`. UTC {now}.

Conservada a prescrição de um par R(u)=FP[(1-a)mu^(2a)z^a u], definida
em tensor_extension antes dos cálculos finitos. A recorrência escalar
diferencial anterior não é silenciosamente aplicada aos numeradores:
sua correção por resíduos já consta daquela entrega. Aqui L=log(mu²z)
usa a mesma escala fixa. C=box(z^-1)/delta, conforme assinatura.

**Fórmula nova.** Se D[mu^(2a)z^(a-n)]=sum_j c_j(a)T_j(a), e rho_j é
o resíduo simples de T_j, então

    R(D[z^-n L^ell])-D R(z^-n L^ell)
      = -sum_j rho_j [c_j^(ell+1)(0)/(ell+1)
                                  +1_(ell>=1)c_j^(ell)(0)].

Derivação: introduza um segundo parâmetro b para o log e diferencie
ell vezes em b ANTES da parte finita em a. A diferença contém
sum_(t=0)^ell binom(ell,t)[c^(ell-t)(0)-c^(ell-t)(a)]partial_a^t T.
Apenas o polo contribui. Multiplicar por (1-a) dá as duas parcelas;
as somas binomiais são 1/(ell+1) e -1. Descartar polos múltiplos dá
um resultado diferente. O termo extra deriva da prescrição já fixada.

Para um símbolo homogêneo P_m(q), escreva Delta_q para seu Laplaciano.
Depois de retirar C, alguns mapas necessários são:

| núcleo | ordem D | contato |
|---|---:|---|
| z^-1 |3| -Delta_q P3/12 |
| z^-1 L |3| +Delta_q P3/24 |
| z^-1 |4| -Delta_q P4/16 + q² Delta_q²P4/384 |
| z^-1 L |4| 5Delta_q P4/96 + q² Delta_q²P4/768 |
| L |4| -Delta_q²P4/48 |
| L² |4| -Delta_q²P4/24 |

Controles por identidades distributivas: contato(box,z^-1)=-C delta;
contato(box,z^-1 L)=0 (definição do R2 anterior);
contato(box²,z^-1 L)=(3/2)C box delta;
contatos(box²,L)=-4C delta e (box²,L²)=-8C delta.
São {lc['checks']} verificações exatas em27mapas, duas assinaturas,
comparando a fórmula fechada com a parte finita completa, mais controles.
CPU {lc['cpu_seconds']}s,rc0. A existência distributiva é insumo analítico,
não teorema provado pelo CAS.

**Aplicação ao começo da expansão curva.** No referencial de transporte
paralelo do espaço-forma, normalize cada propagador pelo fator escalar
1/(4pi²), conservando separadamente a inversa de fibra e as fases:

    G_A = I/z +(K/4)I -(E_A+2K I)L/4 + W_A + jatos superiores.

u0=Delta^(1/2)=1+Kz/4+…; a integral de Mellin do termo t a1 do calor
tem coeficiente -L/4, e a1=E+2K. W_A é o resto suave de referência;
não foi escolhido zero. O produto de dois fatores contém

    I/z² + [(K/2)I+W_A tensor I+I tensor W_B]/z
          -[E_A tensor I+I tensor E_B+4K I] L/(4z) + … .

E_m tem autovalores -2K (sem traço) e6K (traço); E_g=3K. Portanto o
coeficiente L/z vale, respectivamente nos pares (m0,m0),(m0,mtr),
(mtr,mtr),(m0,g),(mtr,g),(g,g): 0,-2K,-4K,-5K/4,-13K/4,-5K/2.
Seis perfis e seus mapas constam no JSON, {hp['checks']}checks,rc0,
CPU {hp['cpu_seconds']}s. Exemplo (m0,g), só a parte geométrica:

    ordem3: -(3K/32)Delta_q P3;
    ordem4: -(37K/384)Delta_q P4-(K/3072)q²Delta_q²P4.

Somam-se os contatos de W_A tensor I+I tensor W_B; esses dados permanecem
explícitos. Ainda faltam a contração dos bitensores, seus jatos direcionais,
os vértices de curvatura, tadpoles e a soma de inserções da hierarquia causal.
Não se usou este perfil escalar como substituto de dez escalares para o
gráviton, nem como amplitude curva completa. A7.b continua ativa; Q2
completa e o gate não são declarados pagos.

Fontes, preregistros, comandos/scripts e logs nos dois manifestos.
'''
rp=HERE/'logarithmic_contact/DERIVACAO_LOG_E_CURVATURA.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_contatos_logaritmicos_curvatura.md',report)
configs=[('logarithmic_contact',['logarithmic_contact_engine.py','logarithmic_contact_check.py','logarithmic_contact_run.log'],
          [HERE/'tensor_extension/PRE_REGISTER.json',HERE/'tensor_extension/DERIVACAO_TENSORIAL.md']),
         ('hadamard_pair_curvature',['hadamard_pair_curvature_check.py','hadamard_pair_curvature_run.log'],
          [HERE/'spaceform_heat/results.json',HERE/'logarithmic_contact/results.json'])]
for folder,names,extra in configs:
    files=[HERE/n for n in names]+[HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json',rp]+extra
    save(HERE/folder/'manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]),ensure_ascii=False,indent=2))
ledger=OUT/'LEDGER_016.jsonl';marker='A7_LOGARITHMIC_CONTACTS_AND_CURVED_PAIR_PROFILES'
cpu=lc['cpu_seconds']+hp['cpu_seconds']
if marker.encode() not in ledger.read_bytes():
    event=dict(event=marker,at=now,provider='local',target='A-7.b',cpu_seconds=cpu,
        checks=lc['checks']+hp['checks'],report_sha256=sha(rp),full_curved_Q2=False)
    save(ledger,ledger.read_bytes()+(json.dumps(event,ensure_ascii=False)+'\n').encode())
# Union aliases before summing cost records; missing values remain missing.
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()];parent={}
def root(k):
    parent.setdefault(k,k)
    if parent[k]!=k:parent[k]=root(parent[k])
    return parent[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for row in rows:
    ix=ids(row)
    for k in ix[1:]:parent[root(k)]=root(ix[0])
known={}
for row in rows:
    ix=ids(row);value=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    if ix and value is not None:known[root(ix[0])]=(Decimal(str(value)),row.get('provider',row.get('provedor','unknown')))
by={}
for value,provider in known.values():by[provider]=by.get(provider,Decimal(0))+value
total=sum(by.values(),Decimal(0))
save(HERE/'logarithmic_contact/COST_SNAPSHOT.json',json.dumps(dict(at=now,ledger_sha256=sha(ledger),
    measured_partial_by_provider={k:str(v) for k,v in by.items()},total_known_partial=str(total),
    missing_costs_not_zero=True,billing_not_verified=True),indent=2))
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',partial_metered_cost_usd=str(total),
    completed_this_turn=['27 logarithmic contact maps derived under unchanged prescription,2345checks',
        'First curved Hadamard pair profiles and geometric contact parts,17checks,smooth W retained'],
    logarithmic_contact_manifest=str(HERE/'logarithmic_contact/manifest.json'),
    hadamard_pair_manifest=str(HERE/'hadamard_pair_curvature/manifest.json'),
    next=['Contract actual curved bitensors and source vertices; smooth reference and causal hierarchy must be fixed consistently',
          'Read pending Kimi/MiMo reviews without duplicate calls',
          'A7.c if24h exhausted; A7.d,A8,Part B and final audit remain'])
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO:27mapas logarítmicos+6perfis curvos,2345+17checks,CPU{cpu}s;Wsuave preservado,Q2curvaOPEN. Custo externo conhecido parcialUS${total},MiMo{by.get("mimo")},DeepSeek{by.get("deepseek")};desconhecidos não zero. LedgerSHA256{sha(ledger)}. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),cpu_seconds=cpu,cost_partial=str(total),status='ACTIVE_PROGRESS'),ensure_ascii=False))
