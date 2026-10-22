"""Custody for the conditional covariant primitive and accepted review queue."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H = Path(__file__).resolve().parent
C = H.parents[1]
O = C / 'TUNEL/DO_CHATGPT'
BASE = C / 'IALD_ORQUESTRACAO_20260923'
D = H / 'contact_bridge_delivery'
D.mkdir(exist_ok=True)
now = datetime.now(timezone.utc).isoformat()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, b, update=False):
    if isinstance(b, str):
        b = b.encode('utf-8')
    if p.exists():
        assert update, p
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:8])
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(b)
    assert b and tmp.read_bytes() == b
    tmp.replace(p)
    assert p.read_bytes() == b

def put(p, v, update=False):
    write(p, json.dumps(v, ensure_ascii=False, indent=2), update)

r = json.loads((H / 'bilocal_curved_contact_primitive/results.json').read_bytes())
files = [Path(__file__)]
mp = H / 'bilocal_curved_contact_primitive/manifest.json'
for row in json.loads(mp.read_bytes())['artifacts']:
    p = Path(row['path'])
    assert sha(p) == row['sha256'], p
    files.append(p)
files += [mp, H / 'bilocal_curved_contact_primitive/DERIVACAO.md',
          H / 'bilocal_curved_contact_primitive_run.log',
          H / 'prepare_contact_bridge_reviews.py',
          H / 'prepare_contact_bridge_reviews_v2.py',
          H / 'orchestration_contact_bridge/PREVIEW_FAILURE.json']
catalog = H / 'orchestration_contact_bridge_v2/prepared_units.json'
units = json.loads(catalog.read_bytes())
for u in units:
    assert sha(Path(u['payload'])) == u['payload_sha256']
files.extend(p for p in catalog.parent.iterdir() if p.is_file())
acceptance = BASE / 'state/handoffs/a7_contact_bridge_v2_pending_submissions.json'
assert acceptance.exists()
write(D / 'COORDINATOR_ACCEPTANCE.json', acceptance.read_bytes())
files.append(D / 'COORDINATOR_ACCEPTANCE.json')
put(D / 'QUEUE_SNAPSHOT.json', dict(at=now,
    source='Official coordinator message, snapshot 2026-09-25 09:54 UTC; not a promise of current execution',
    capacity=5, nonterminal=5,
    kimi_running='9118ccb7-dd63-49b6-9340-773caa74812e',
    kimi_waiting=['6c210ea9-cc1e-4c09-a039-3d469ae4f090',
                  '3ceb40a7-8ef6-4f56-87b4-bf301e2a0337', 'efbb6f84 (short id from coordinator)'],
    mimo_waiting_held='f0385e3c-5186-4fba-95d8-41b3bf325b92',
    mimo_new_failure='bf606625-201a-41ee-adb1-462bc72d0cdc: IncompleteRead; usage/cost unknown, not zero',
    newly_accepted_requests=[u['request_id'] for u in units],
    new_units_status='ACCEPTED_STAGING_NOT_SUBMITTED',
    kernel_changed=False, repeated_remote_calls=False))
files.append(D / 'QUEUE_SNAPSHOT.json')
opening = sha(O / 'ENTREGA_016_ABERTURA_operador.md')
report = O / 'ENTREGA_016_A7b_primitiva_covariante_e_divisao_das_revisoes.md'
write(report, f'''[DERIVED — identidade da completação covariante até O(K), condicionada à ponte distribucional; Q2 OPEN]

Data {now}. Abertura SHA256 {opening}.

A família quadrática N_bct satisfaz N_bct G=A_cov até primeira ordem
na curvatura, nas duas completações de regulador, com b,c,t livres.
Foram conferidas {r['checks']} igualdades simbólicas em todos os momentos
e polarizações; CPU {r['cpu_seconds']}s. Não foi escolhido contratermo.
O comando do cálculo foi A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/bilocal_curved_contact_primitive_check.py; terminou com rc0.
Log SHA256 {sha(H / 'bilocal_curved_contact_primitive_run.log')}.

O alcance é a identidade do operador covariante definido no cálculo.
Passar do contato em derivadas de delta nos dois extremos para esse
operador exige conferir transposição, sinal, densidade e mudança de
âncora. Essa ressalva permanece explícita: não se afirma ainda que o
contato efetivamente medido foi removido, nem que a Q2 completa foi paga.

## Divisão de trabalho a pedido do operador

- Kimi: ponte entre o contato em frame normal e a completação covariante,
  incluindo derivadas ímpares e transposição entre os extremos.
- DeepSeek: autoadjunta da Hessiana de quarta ordem e expansão ordenada
  dos termos do corte, incluindo [N,chi]/2 e o sinal na próxima descida.
- Bancada: verifica as respostas contra fontes e cálculos locais.

Prévia Kimi: 21049 caracteres, selected=kimi. Prévia DeepSeek: 15673,
selected=deepseek. Ambos receberam restrição de uma chamada por unidade
e memória científica comum pelo adaptador. Catálogo e recibo estão em
{catalog.parent}. A coordenação aceitou staging depois do catálogo
bilocal_completion_v2; ainda não há job_id para as duas novas unidades.
A fila estava em 5/5, com Kimi ativo. Não se abriu outro worker.

A primeira preparação Kimi tinha 24111 caracteres e foi recusada
LOCALMENTE na prévia, antes de qualquer envio. V2 retirou apenas uma fonte
auxiliar redundante. A tentativa e os dois pacotes são preservados.

MiMo acumulou outra falha IncompleteRead; o pedido seguinte está retido
para revisão do transporte. Não foram repetidas chamadas terminais.
Os pareceres harmônico/suave recém-entregues pelo Kimi serão auditados
separadamente; não se promove conclusão textual a prova.

Permanecem fora deste resultado W geral, demais diagramas locais, K²,
aridades superiores e valores de contorno lorentzianos. Próximo passo:
auditar a ponte e os termos localizados, continuando A7.b no prazo vigente.
Nenhuma alteração de um.py, kernel, gate, fonte científica ou parâmetro.
''')
files.append(report)
files = list(dict.fromkeys(files))
put(D / 'manifest.json', dict(at=now, opening_sha256=opening,
    checks=r['checks'], cpu_seconds=r['cpu_seconds'], full_Q2=False,
    artifacts=[dict(path=str(p), sha256=sha(p)) for p in files]))
ledger = O / 'LEDGER_016.jsonl'
event = dict(at=now, event='A7_COVARIANT_CONTACT_PRIMITIVE_AND_REVIEWS_STAGED',
    target='A7.b', checks=r['checks'], cpu_seconds=r['cpu_seconds'],
    remote_call=False, new_provider_calls=0,
    request_ids=[u['request_id'] for u in units],
    delivery_manifest_sha256=sha(D / 'manifest.json'),
    full_Q2=False, status='CONDITIONAL_COVARIANT_IDENTITY_AND_ACCEPTED_STAGING')
write(ledger, ledger.read_bytes() + (json.dumps(event) + '\n').encode(), True)

parents = {}
def root(k):
    parents.setdefault(k, k)
    if parents[k] != k:
        parents[k] = root(parents[k])
    return parents[k]
def ids(row):
    return [str(row[k]) for k in ('execution_id', 'execution_task_id', 'job_id', 'request_id') if row.get(k)]
rows = [json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for row in rows:
    keys = ids(row)
    for k in keys[1:]:
        parents[root(k)] = root(keys[0])
known = {}
for row in rows:
    keys = ids(row)
    cost = row.get('cost_estimate_usd', row.get('cost_usd', row.get('custo_usd')))
    if keys and cost is not None:
        known[root(keys[0])] = Decimal(str(cost))
total = sum(known.values(), Decimal())
put(D / 'COST_SUM.json', dict(at=now, known_partial_usd=str(total),
    unknown_not_zero=True, newly_staged_calls_executed=0, ledger_sha256=sha(ledger)))
p = O / 'ENTREGA_016_PROGRESSO.md'
write(p, p.read_bytes() + f'\n- {now} A7.b PROGRESS: N G=A_cov até O(K),256checks,CPU{r["cpu_seconds"]}s; ponte distribucional em auditoria. Novas revisões Kimi/DeepSeek aceitas em staging, zero novos envios. MiMo HOLD transporte. Custo parcial conhecido US${total}; Q2 OPEN.\n'.encode(), True)
p = H / 'CONTINUIDADE.json'
state = json.loads(p.read_bytes())
state.update(at=now, previous_goal_turn='PROGRESS', own_live_processes=[],
    curved_contact_primitive_manifest=str(D / 'manifest.json'),
    contact_bridge_review_catalog=str(catalog),
    partial_metered_cost_usd=str(total), quantum_anomaly_computed=False,
    pending_orchestration='Kimi nonlocal running at09:54UTC; harmonic/smooth responses await local audit. NewKimi/DeepSeek accepted staging. MiMo fourth IncompleteRead and HOLD future dispatch. See snapshot.',
    latest_live_execution=dict(status='COORDINATOR_OWNED_NO_OWN_PROCESS', source=str(D / 'QUEUE_SNAPSHOT.json')),
    completed_this_turn=['256 symbolic checks N G=A_cov through O(K), formal completion only',
                        'Two new independent review units previewed and accepted staging; no duplicate calls'],
    next=['Audit contact-to-covariant bridge and fourth-order cutoff terms',
          'Read and audit new Kimi harmonic/smooth responses, retain failures and local ambiguities',
          'A7.b deadline2026-09-25T20:32Z; then A7.c/d, A8, PartB and full final audit'])
put(p, state, True)
for row in json.loads((D / 'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(row['path'])) == row['sha256']
print(json.dumps(dict(artifacts=len(files), checks=r['checks'],
    cpu_seconds=r['cpu_seconds'], known_partial_usd=str(total),
    new_remote_executions=0, report=str(report), goal='ACTIVE')))
