"""Record the curvature fiber calculation and the held-payload reconciliation."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode('utf-8') if isinstance(value,str) else value
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw;tmp.replace(p)
def js(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((HERE/'connection_curvature/results.json').read_bytes())
assert r['checks_passed']==33
report=f'''[DERIVED — curvatura das fibras; REAL — CAS exato; OPEN — coeficiente curvo interagente]
# A7.b — o que as massas escalares não representam

Abertura SHA256 `{opening}`; UTC {now}.

Modelo087, curvatura seccional K, d=4. Aqui K não é o gerador modular nem κ,
o acoplamento. No cálculo algébrico tangente euclidiano fixamos
R^rho_sigma_mu_nu=K(delta^rho_mu delta_sigma_nu-delta^rho_nu delta_sigma_mu).
A matriz Ω_mu_nu é antissimétrica na fibra vetorial; na fibra simétrica age
por ΩH+HΩ^T. A projeção simétrica no tensor de dimensão16 permite conferir,
por outra representação, o traço obtido na base simétrica de dimensão10.

Incluindo a soma sobre pares ORDENADOS de índices μ,ν:

| fibra | posto | tr Ω_mu_nu Ω^mu_nu |
|---|---:|---:|
| covetores/ghost |4| -24K² |
| tensores simétricos |10| -144K² |
| tensores antissimétricos (controle) |6| -48K² |

O índice da representação simétrica é d+2=6 vezes o vetorial; o da exterior
é d-2=2. A soma das duas dá o tensor inteiro. O vetor de traço da métrica é
anulado por Ω; a parte de traço não acrescenta curvatura de conexão escalar.
Os seis geradores preservam a forma de fibra e comutam com E do modelo.

Para os endomorfismos definidos em P=box+E_m e Q=box+E_g da entrega anterior,
E_m=-2K id+2K g tr e E_g=3K id:

    tr E_m=-12K, tr E_m²=72K²;
    tr E_g=12K,  tr E_g²=36K².

Esses E são os das fontes, NÃO uma escolha implícita do sinal E de uma fórmula
de kernel de calor após Wick. Esse dicionário precisa acompanhar qualquer uso
de coeficientes de calor. A combinação algébrica com pesos de determinante
1/2 métrico -1 ghost dá tr Ω² ponderado=-48K²; ainda não é um coeficiente
logarítmico completo, porque faltam os outros invariantes e suas constantes.

Substituir a fibra métrica por dez escalares com massas efetivas produziria
Ω=0, perdendo -144K². O teste recusa essa substituição, a contagem16 em vez10,
e a falta do fator2 dos pares ordenados. Conferir E sozinho não confere um
propagador tensorial curvo nem a segunda variação da ação com gauge de fundo.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/connection_curvature_check.py; rc0,33checks,3negativos; wall
{r['wall_seconds']}s,CPU {r['cpu_seconds']}s. Plano, log e hashes no manifesto.
Não foi calculado a4 nem a autoenergia curva nem a anomalia ghost1/forma4.
Este é o próximo insumo exato do ramo A7.b, não conclusão do ramo ou do gate.
'''
save(HERE/'connection_curvature/DERIVACAO_CONEXAO.md',report)
save(OUT/'ENTREGA_016_A7b_curvatura_das_fibras.md',report)
files=[HERE/'connection_curvature_check.py',HERE/'connection_curvature_run.log',
       HERE/'connection_curvature/PRE_REGISTER.json',HERE/'connection_curvature/results.json',
       HERE/'connection_curvature/DERIVACAO_CONEXAO.md']
js(HERE/'connection_curvature/manifest.json',dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files],
    full_Q2=False,gate_changed=False))
catalog=json.loads((HERE/'orchestration_metric_v2/prepared_units.json').read_bytes())
unit=catalog[0];assert sha(Path(unit['payload']))==unit['payload_sha256']
ack=dict(at=now,source='official message from coordinator',
    source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    request_id=unit['request_id'],status='V2_RECONCILED_WAITING_QUEUE_CAPACITY_AFTER_A7_CONTACTS',
    provider='kimi',job_id=None,external_execution=False,
    note='Coordinator rechecked entire queue; no job/execution; same ID/position; other two units unchanged')
js(HERE/'orchestration_metric_v2/coordinator_acknowledgment.json',ack)
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_CONNECTION_CURVATURE_AND_KIMI_V2_20260924'
if marker.encode() not in raw:
    events=[dict(event=marker,at=now,provider='local',target='A-7.b',rc=0,
        checks=33,controls=3,cpu_seconds=r['cpu_seconds'],opening_sha256=opening,
        manifest_sha256=sha(HERE/'connection_curvature/manifest.json'),full_Q2=False),
        dict(event=marker,at=now,provider='kimi',target='A-7.b',request_id=unit['request_id'],
        phase='V2_RECONCILED_BEFORE_ANY_SUBMISSION',payload_sha256=unit['payload_sha256'],
        supersedes_sha256=unit['supersedes_sha256'],tokens=None,cost_usd=None,
        external_execution=False,opening_sha256=opening)]
    save(ledger,raw+''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);c=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if c is not None and key:costs[key]=Decimal(str(c))
total=sum(costs.values(),Decimal(0))
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes())
d['at']=now;d['connection_curvature_manifest']=str(HERE/'connection_curvature/manifest.json')
d['completed_this_turn'].append('Connection curvature S2 and T* traces:33checks/3controls')
d['latest_orchestration']=dict(catalog=str(HERE/'orchestration_metric_v2/prepared_units.json'),
    status=ack['status'],request_ids=[u['request_id'] for u in catalog])
d['next']=['Compute curved/marked BV pieces with fixed background gauge; do not infer from10scalar masses',
    'Recover queued A7 reviews without duplicate calls',
    'Preserve principal quadratic transverse result; Q2 ghost1/form4 and finite contacts remain OPEN']
js(p,d)
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now} — A7.b PROGRESSO: curvatura das fibras33checks/3controles, trOmega2 metrica=-144K²/ghost=-24K²; nao equivale a10escalares. Kimi v2 reconciliada ANTES de submissao, mesmo ID, sem nova chamada. CPU {r["cpu_seconds"]}s; bancada22:33–22:38UTC ~0,083h, adicional ao intervalo anterior. Estimativas externas parciais US${total}. Abertura {opening}. [{marker}]\n'.encode())
for a in json.loads((HERE/'connection_curvature/manifest.json').read_bytes())['artifacts']:
    assert sha(Path(a['path']))==a['sha256']
print(json.dumps(dict(status='DELIVERED',connection_checks=33,kimi_v2=ack['status'],
    partial_cost_usd=str(total),full_Q2=False,gate_changed=False),ensure_ascii=False))
