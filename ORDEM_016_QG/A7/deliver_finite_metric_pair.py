"""Custody of measured raw metric pair finite contact, explicitly scoped."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'finite_metric_pair';now=datetime.now(timezone.utc).isoformat()
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        assert existing,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
def put(p,obj,existing=False):write(p,json.dumps(obj,ensure_ascii=False,indent=2).encode(),existing)
r=json.loads((D/'results.json').read_bytes())
assert r['status']=='RAW_PAIR_COMPONENT_MEASURED' and not r['full_Q2']
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
text=f'''[DERIVED — diferença local de um par métrico; REAL — CAS; OPEN — soma completa]
# A7.b — contato finito do kernel métrico com jatos covariantes
Abertura SHA256 `{opening}`. UTC {now}.

Mantivemos os vértices W2/W1 e de potencial, Green bitensorial G0/G1/GL,
a medida geométrica e os jatos ordenados usados na Hessiana logarítmica.
Agora substituímos o peso de Taylor pelos projetores harmônicos do contato
finito já verificados, sem mudar R=FP[(1-a)mu^(2a)z^a .]. A integração
usa os128 nós racionais existentes da cubatura de S3 até grau8.

Para dois vértices com n_x,n_y derivadas internas, ordem geométrica r,
o contato usa m=n_x+n_y-2r. Jatos de ordem covariante o, e potências
explícitas e_x,e_y do potencial, satisfazem o+r+e_x+e_y=ordemK.
Os monômios q^I já trazem seus coeficientes: não se reaplica o divisor I!.
O sinal (-1)^m vem da ação da derivada do delta no teste. Permanecem o
sinal da integração por partes da perna ancorada e o sinal relativo dos
vértices de potencial, calibrados na construção logarítmica anterior.

Harmônicos escalares l0 dão contato zero RELATIVO a R(U_b L^r). Por isso
o kernel geométrico r2, com m0, não gera esta diferença; a parcela K²
ainda recebe contribuições dos jatos covariantes dos kernels r0 e r1 e
dos vértices de potencial. Isso não descarta a amplitude não local r2.

## Resultados
Na base K[p²trAB,p²trA trB,pAp trB,pBp trA,pABp], os coeficientes são:

    {r['first_K_coefficients']}

Na base K²[trAB,trA trB], são:

    {r['second_K_coefficients']}

Normalização: contato/C do PAR MÉTRICO CRU, com o fator1/16 herdado do
motor posicional. Ainda NÃO aplicado o peso de Wick -1/2, nem acrescentado
o tadpole finito, o ghost, W suave ou as fases causais Lorentzianas.
Diferença entre os coeficientes pAp trB e pBp trA:

    {r['first_K_exchange_defect']}

Esse diagnóstico é preservado. Uma diferença de referências não deve ser
tratada como contratermo admissível ou operador físico sem conferir suas
simetrias e a amplitude de referência que a acompanha.

## Verificação e limite
PrimeiraK: cinco pares escolhidos por posto algébrico, mais um novo par
de fibras e um novo momento não axial. Dos quatro pares chamados holdouts
no pré-registro, três já estavam no ajuste: são RECHECAGENS, não evidência
independente. SegundaK: dois coeficientes obtidos de dois pares e conferidos
em dois pares adicionais. O relatório conserva valores de cada parcela
geométrica e logarítmica, sem impor que logs desapareçam por hipótese.
São {r['checks']} comparações de reconstrução, rc0, CPU{r['cpu_seconds']}s.

Não é a quebra Ward total: falta a combinação com o par ghost finito,
tadpoles, contatos da fonte na mesma referência e W admissível. A passagem
entre esta representação harmônica e a representação principal anterior
foi enviada em tarefa distinta ao Kimi. Nenhum gate ou original alterado.
'''
out=O/'ENTREGA_016_A7b_contatos_finitos_bolha_metrica.md';write(out,text)
files=[Path(__file__),H/'finite_metric_pair_engine.py',H/'finite_metric_pair_check.py',
       H/'finite_metric_pair_run.log',D/'PRE_REGISTER.json',D/'results.json',D/'manifest.json',
       H/'finite_angular_contact/manifest.json',H/'finite_angular_contact_engine.py',
       H/'position_metric_ordered_operator_engine.py',out]
manifest=dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'delivery_manifest.json',manifest)
for row in manifest['artifacts']:assert sha(Path(row['path']))==row['sha256']
ledger=O/'LEDGER_016.jsonl'
event=dict(event='A7_RAW_METRIC_PAIR_FINITE_CONTACT',at=now,target='A-7.b',
    rc=0,cpu_seconds=r['cpu_seconds'],checks=r['checks'],external_execution=False,
    manifest_sha256=sha(D/'delivery_manifest.json'),log_sha256=sha(H/'finite_metric_pair_run.log'),
    full_Q2=False)
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: diferença finita do par métrico K1/K2 medida, {r["checks"]} reconstruções (incluindo rechecagens), CPU{r["cpu_seconds"]}s, rc0; Q2 inteira OPEN.\n'.encode(),True)
continuity=H/'CONTINUIDADE.json';v=json.loads(continuity.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',finite_metric_pair_manifest=str(D/'delivery_manifest.json'))
v['completed_this_turn'].append('Raw metric finite pair K1/K2 measured with ordered covariant jets; rc0; 7reconstruction comparisons including fit rechecks')
v['next']=['Compute matching ghost finite raw-pair contact with fixed R and same harmonic reference',
    'Check normalization, reference-symmetry and smooth W before any full Ward combination',
    'Finite metric process finished; no need to rerun fitted samples',
    'Independent queued reviews unchanged; A7.c after24h if unpaid; A7.d,A8,PartB,finalaudit remain']
put(continuity,v,True)
print(json.dumps(dict(verified=True,artifacts=len(files),firstK=r['first_K_coefficients'],
    secondK=r['second_K_coefficients'],exchange_defect=r['first_K_exchange_defect'])))
