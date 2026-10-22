"""Publish free Wick conditions, the arity-two dictionary, and failed-call custody."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'flat_wick_dictionary_delivery'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    assert b
    if p.exists():
        assert replace,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
def put(p,v,replace=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),replace)
def append(p,v):write(p,p.read_bytes()+v.encode('utf-8'),True)
D.mkdir(exist_ok=False)
r=json.loads((H/'flat_free_wick_ward/results.json').read_bytes())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — normalização plana condicional e dicionário de aridade; Q2 curvo OPEN]

# A7.b — condição concreta de primeira ordem

O cálculo reutiliza a base simétrica métrica e generaliza a matriz livre
ao fundo plano de assinatura (-,+,+,+), mantendo o controle euclidiano.
Campos: h_ij (10), b_i (4), c_i (4), barc_i (4). p representa derivada
formal; em Fourier, todas as ocorrências devem usar p=i k, inclusive os
blocos mistos. Não se mudou a continuação dos contatos já calculados.

Se R é o Gram da base, Itr a reversão de traço, Gc=partial_i c_j+partial_j c_i,
C(h)_j=partial^i h_ij-partial_j tr(h)/2 e E=-p² Itr+Itr G C, os blocos são

 P_hb=[[R E/(4 kappa), -C^T eta],[eta C, -2 kappa eta]],
 N_hb=[[-4 kappa Itr R^-1, G eta],[-eta G^T, 0]],
 P_ghost=[[0,-p² eta],[p² eta,0]], N_ghost=[[0,eta],[-eta,0]].

O CAS verifica P N=N P=p² I22, a adjunção graduada de P, a troca de pontos
de N e Q²=0. Qh=Gc, Qbarc=-b. Com epsilon=diag(+1 nos14 bósons,-1 nos8 ghosts),

 Q(p)N(p)+epsilon N(p)Q(-p)^T=0.

Remover os blocos h-b/b-h viola essa última identidade: a componente h00,barc0
é 2p0 no controle euclidiano e -2p0 no lorentziano. Não se descartou o auxiliar.
São {r['checks']} verificações matriciais/controles, CPU{r['cpu_seconds']}s, rc0.

Escolhido um fplus que seja bisolução exata de box, Hplus=N(partial)fplus
herda P Hplus=0 e a identidade Ward. O enunciado é condicional a essa escolha;
não afirma positividade no espaço total de campos de gauge. No espaço plano
lorentziano, o kernel escalar de frequência positiva da onda sem massa é um
candidato habitual; sua existência/condição microlocal não foram objeto deste CAS.

Prova da consequência para Wick: numa contração de dois campos, a derivação
livre produz precisamente QH+epsilon H Q^T. Ela é zero. Nos termos em que
o BRST de um antifield produz a equação livre, surge P H, também zero.
Logo a derivação comuta com cada pareamento e com a soma de Wick:
shat0 T1(F)=T1(s0 F). Assim A1(F)=0 nesta prescrição plana equivarante.
É uma condição suficiente explícita, não a afirmação de que qualquer ordenamento
normal torna A1 zero. A extensão localmente covariante curva continua pendente.
Não se adotou retroativamente um estado ou um T1 para as contas anteriores.

# Dicionário necessário para o contato de segunda ordem

[KNOWN — Fröb, arXiv1803.10235v3, equações74/154, Teoremas3/6;
DERIVED — polarização e subtração abaixo.] Para F,G pares, a expansão em
aridade, com shat0 no alvo quântico e s0 nos funcionais, dá

 T1(A2(F,G)) = (i/hbar)[shat0 T2(F,G)-T2(s0F,G)-T2(F,s0G)
                   -T2(A1(F),G)-T2(F,A1(G))] -T1((F,G)).

Essa expressão conserva ambos os termos A1. A equação162 da fonte é um
caso especial com uma entrada só de antifields e A1 dessa entrada zero;
não serve para eliminar o segundo termo A1 em duas interações genéricas.
Fonte primária: https://arxiv.org/pdf/1803.10235v3 (pp17–18,34–38).

Defina U2(F,G)=T2(F,G)-T1(F) star T1(G), para essa ordem escrita.
Como shat0 é derivação de star e shat0 T1=T1(s0+A1), os termos desconexos
cancelam exatamente na combinação acima. Portanto a mesma fórmula vale
substituindo T2 por U2 em todos os cinco termos dentro dos colchetes.
Não se usou transformada de Legendre: U2 conectado não é, por esse argumento,
o coeficiente W2 da ação efetiva 1PI. Os mapas permanecem distintos.

Com A1=0 efetivamente estabelecido, restam três termos de U2 e o antibracket.
O contato local calculado pela bancada só pode ser identificado com A2 após
conferir os fatores i/hbar, a subtração T1((F,G)) e o Wick T1 da mesma prescrição.
A igualdade das16 componentes da descida testa a condição localizada; não
preenche por si só essas identificações. Os grafos de corrente já existentes
entram nas duas inserções s0F/s0G; não devem ser recriados como novos grafos.

Nenhum novo teorema Lean, estado curvo, normalização de Euler composta ou
gate foi obtido. Próximo passo: usar a crítica dos produtos temporais para
identificar essas subtrações nos coeficientes já calculados, preservando o
recorte do espaço-forma do alvo. A7.b encerra às20:32UTC.
Abertura SHA256={opening}.
'''
write(D/'DERIVACAO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_MEDIDA_Wick_plano_dicionario_aridade2.md',report.encode('utf-8'))
receipt=BASE/'state/handoffs/b34d1e0b-e40c-49f6-8f88-44228bf8718c_delivery.json'
job=json.loads(receipt.read_bytes())['job'];execution=job['execution']
assert job['request_id']=='5e1f8779-8e05-4c22-b4a3-8f107bb78059'
assert execution['status']=='failed' and execution['result'] is None
failure=dict(at=now.isoformat(),request_id=job['request_id'],job_id=job['id'],
    execution_task_id=execution['id'],status=execution['status'],
    prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
    response_sha256=None,response_status='NO_ACCEPTED_RESPONSE',
    receipt_sha256=sha(receipt),error=execution['error'],
    tokens=None,cost_usd=None,unknown_usage_is_not_zero=True,
    coordinator_diagnosis='Official message: APIEmptyResponseError; thinking only, no text/tools, finishReason null; stream interrupted OR reasoning budget exhausted, not distinguished; does not establish credit/quota exhaustion',
    repeated=False)
put(D/'KIMI_FAILED_RECEIPT.json',failure)
paths=[Path(__file__),D/'DERIVACAO.md',D/'KIMI_FAILED_RECEIPT.json',
    H/'flat_free_wick_ward_check.py',H/'flat_free_wick_ward/results.json',
    H/'flat_free_wick_ward/manifest.json']
put(D/'manifest.json',dict(at=now.isoformat(),checks=r['checks'],cpu_seconds=r['cpu_seconds'],
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
new=[]
if not any(v.get('execution_task_id')==execution['id'] for v in entries):
    new.append(dict(failure,event='EXTERNAL_UNIT_FAILED_NO_ACCEPTED_RESPONSE',provider='kimi',target='A7.b'))
new.append(dict(at=now.isoformat(),event='FLAT_FREE_WICK_AND_ARITY_TWO_DICTIONARY',target='A7.b',
    checks=r['checks'],cpu_seconds=r['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))
append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in new))
cost=Decimal(0);seen=set()
for e in entries+new:
    v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None:continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b:condição Wick plana equivarante,14verificações CPU{r["cpu_seconds"]}s;dicionário A2/T2 com A1 e subtração clássica explícitos. Kimi5e1 failed sem resposta;uso desconhecido,não repetido. Custo conhecido parcialUSD{cost}. AberturaSHA256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
state.setdefault('head_history',[]).append({k:state.get(k) for k in
    ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Free covariance Ward and Euler identities for Euclidean/Lorentzian flat signatures',
        'Sufficient condition A1=0 for equivariant flat Wick map; no curved adoption',
        'Arity-two dictionary retains both A1 insertions and classical antibracket',
        'Kimi5e1 failure preserved; next distinct bd879 explicitly authorized'],
    next=['Receive and audit MiMoa46/Kimibd879 and following normalization reviews',
        'Identify computed current contacts with temporal Ward coefficient, including T1 bracket subtraction',
        'Keep curved-space and causal-continuation obligations; A7b deadline20:32UTC'],
    pending_orchestration='Coordinator: MiMoa46 RUNNING executiond6585720 worker68839; Kimi5e1FAILED no response; distinct bd879 authorized; Kimi709 admittedjob8639533b',
    partial_metered_cost_usd=str(cost))
state['flat_wick_dictionary_update']=dict(manifest=str(D/'manifest.json'),full_Q2=False,
    flat_equivariant_candidate_only=True,curved_A1_not_established=True)
put(p,state,True)
for e in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(e['path']))==e['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=r['checks'],
    cpu_seconds=r['cpu_seconds'],known_partial_cost_usd=str(cost))))
