"""Preserve dispatch state and one independently audited provider result."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H=Path(__file__).resolve().parent
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'differential_normalization_dispatch_delivery'
D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc); stamp=now.strftime('%Y%m%d_%H%M%S_%f')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
    if p.exists():
        assert existing,p
        old=p.read_bytes(); backup=p.with_name(p.name+'.bak_'+stamp)
        assert not backup.exists()
        backup.write_bytes(old); assert backup.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    temp.write_bytes(b); assert b and temp.read_bytes()==b; temp.replace(p)
def put(p,obj,existing=False):
    write(p,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def append(p,text): write(p,p.read_bytes()+text.encode('utf-8'),True)

catalog=H/'orchestration_differential_normalization/prepared_units.json'
units=json.loads(catalog.read_bytes())
for unit in units: assert sha(Path(unit['payload']))==unit['payload_sha256']
audit=json.loads((H/'mimo_weighted_adjoint_review/local_audit.json').read_bytes())
receipt=json.loads((H/'mimo_weighted_adjoint_review/RECEIPT.json').read_bytes())
result=receipt['job']['execution']['result']
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[REAL — distribuição adicional e auditoria local; Q2 integral OPEN]

Preparadas três unidades novas e distintas, com as rotas conferidas:
1. Kimi709ce591: normalização diferencial de inserções compostas, mantendo
   explícita a diferença entre extensão de pares e equação de movimento.
2. Kimid3e54887: dicionário entre ação efetiva, inserção e representante
   local de Ward; identificar A2 sem presumir que o contato isolado já é A2.
3. MiMoa46a463f: auditoria independente de Leibniz, troca de linhas e uma/duas
   derivadas distribuídas; nenhuma escolha de tau por ajuste.
As unidades recebem memória científica comum; os dois Kimi estão configurados
para máximo e o MiMo conserva sua capacidade máxima. Prévia não é execução.

Resposta oficial da coordenação: MiMoa46 admitido no job
ea89a9c0-00c5-4c75-9340-d0efcda7cddd, awaiting_dispatch. Exige encerrar
drain91153 e criar processo auditado para esta unidade. Os dois Kimi estão
em STAGING_PROVIDER_FIFO, após51c, na ordem acima. Cinco admitidos; uma
execução por fornecedor; prazo20:32UTC. Prompts anteriores intactos.

MiMoa369 recebido integralmente e auditado: {audit['checks']} verificações,
CPU{audit['cpu_seconds']}s, rc0. A multiplicidade diagonal e o adjunto ponderado
coincidem com o motor existente. Corrigida a transposição dupla na demonstração:
Q(B)=-Q(B^dagger), não -Q((B^dagger)^T). Um B formalmente autoadjunto pode
não ser simétrico como matriz de símbolos; o controle2x2 verifica essa distinção.

O parecer passou a usar q como momento de Fourier; a bancada usa q como
símbolo de derivada de delta. Não se pode inserir -i sem converter o resto.
A passagem já implementada é A(q-lambda), depois q=D+lambda+eta, portanto
A(D+eta). Cinco controles polinomiais verificam o encadeamento. Nenhum motor
novo, nenhuma troca de sinal no código canônico.

O parecer também listou b-h/correntes ghost como ainda não computados;
eles já estão nos motores e resultados anteriores. Não os duplicar. Falha
de fechamento de um representante não define classe não exata em cohomologia;
é necessário o sistema inhomogêneo e suas inserções.

Uso MiMo: {json.dumps(result['usage'],ensure_ascii=False)}.
Estimativa registrada USD{result['request_cost_accounting']['accounted_usd']},
não fatura; recibo contabilizado uma vez. Originais/kernel/gate intactos.
Abertura sha256={opening}.
'''
write(D/'DERIVACAO_E_ESTADO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_A7b_normalizacao_distribuida_adjunto_auditado.md',report.encode('utf-8'))
paths=[Path(__file__),D/'DERIVACAO_E_ESTADO.md',catalog,
 H/'orchestration_differential_normalization/manifest.json',
 H/'prepare_differential_normalization_reviews.py',
 H/'mimo_weighted_adjoint_review/manifest.json',
 H/'mimo_weighted_adjoint_review/local_audit.json',
 H/'audit_mimo_weighted_adjoint_review.py']
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
 checks=audit['checks'],cpu_seconds=audit['cpu_seconds'],
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
 full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='DIFFERENTIAL_NORMALIZATION_DISPATCH_AND_ADJOINT_AUDIT',
 target='A7.b',checks=audit['checks'],cpu_seconds=audit['cpu_seconds'],
 remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line);value=e.get('cost_estimate_usd',e.get('cost_usd'))
    if value is None: continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen: continue
    if key: seen.add(key)
    cost+=Decimal(str(value))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESSO: 2Kimi+1MiMo preparados/aceitos; MiMo admitido, Kimi staging. MiMoa369 auditado33checks,CPU{audit["cpu_seconds"]}s. Motores preservados; custo conhecido parcialUSD{cost}. Abertura sha256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
keys=['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','partial_metered_cost_usd']
state.setdefault('head_history',[]).append({k:state.get(k) for k in keys})
state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['MiMoa369 weighted adjoint review audited,33checks; no new engine',
 'Two new Kimi normalization/dictionary tasks and one MiMo scalar audit prepared and accepted by coordinator'],
 next=['Derive complete J2 normalization and identification of computed contact with A2; do not refit tau',
 'Receive Kimi5e1/bd879/e710/51c and new normalization units; audit before use',
 'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
 pending_orchestration='Kimi5e1 last observed running; bd879,e710,51c waiting; MiMoa46 jobea89 admitted awaiting new audited worker after drain91153; Kimi709,d3 staging',
 partial_metered_cost_usd=str(cost))
state['differential_normalization_dispatch_update']=dict(at=now.isoformat(),
 manifest=str(D/'manifest.json'),catalog=str(catalog),
 mimo_admitted_job='ea89a9c0-00c5-4c75-9340-d0efcda7cddd',
 own_processes=[],new_engine=False,full_Q2=False,gate_changed=False)
put(p,state,True)
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=audit['checks'],
 known_partial_cost_usd=str(cost),gate_changed=False)))
