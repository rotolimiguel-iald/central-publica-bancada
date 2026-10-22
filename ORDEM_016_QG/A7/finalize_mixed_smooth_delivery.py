"""Verify existing scientific artifacts, deliver scope, and append own ledger."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H = Path(__file__).resolve().parent
OUT = H.parents[1] / 'TUNEL' / 'DO_CHATGPT'
D = H / 'mixed_smooth_delivery'
D.mkdir(exist_ok=True)
now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def atomic(p, raw, replace=False):
    if p.exists():
        assert replace, p
        old = p.read_bytes()
        bak = p.with_name(p.name + '.bak_' + stamp)
        assert not bak.exists()
        bak.write_bytes(old)
        assert bak.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw and len(raw) > 0
    tmp.replace(p)
    assert p.read_bytes() == raw

def put(p, obj): atomic(p, json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8'))
def append(p, text):
    old = p.read_bytes()
    atomic(p, old + text.encode('utf-8'), replace=True)
    assert p.stat().st_size > len(old)

artifacts = {}
results = []
for name in ['flat_mixed_smooth_bubble', 'flat_mixed_smooth_primitive']:
    manifest = H / name / 'manifest.json'
    for row in json.loads(manifest.read_bytes())['artifacts']:
        p = Path(row['path'])
        assert sha(p) == row['sha256'], p
        artifacts[str(p)] = row['sha256']
    artifacts[str(manifest)] = sha(manifest)
    log = H / (name + '_run.log')
    parsed = json.loads(log.read_text('utf-8-sig').splitlines()[-1])
    result = json.loads((H / name / 'results.json').read_bytes())
    assert parsed == result
    assert result['full_Q2'] is False
    artifacts[str(log)] = sha(log)
    results.append(result)
for p in [Path(__file__), H / 'flat_mixed_smooth_bubble/DERIVACAO.md',
          H / 'prepare_smooth_completion_reviews.py']:
    artifacts[str(p)] = sha(p)

catalog = H / 'orchestration_smooth_completion/prepared_units.json'
units = json.loads(catalog.read_bytes())
for row in units:
    p = Path(row['payload'])
    assert sha(p) == row['payload_sha256']
    q = json.loads(p.read_bytes())
    assert q['request_id'] == row['request_id']
    assert q['execution_constraints']['required_provider'] == row['provider']
    for suffix in ['submit', 'receipt', 'preview']:
        f = p.with_name(p.name.replace('_submit.json', '_' + suffix + '.json'))
        artifacts[str(f)] = sha(f)
artifacts[str(catalog)] = sha(catalog)
opening = OUT / 'ENTREGA_016_ABERTURA_operador.md'
checks = sum(x['checks'] for x in results)
cpu = sum(x['cpu_seconds'] for x in results)
put(D / 'manifest.json', dict(at=now.isoformat(), opening_sha256=sha(opening),
    artifacts=[dict(path=p, sha256=v) for p,v in sorted(artifacts.items())],
    verified_artifacts=len(artifacts), checks=checks, cpu_seconds=cpu,
    rc=0, rc_source='Recorded successful command executions; matching complete result/log rechecked',
    new_remote_calls=0, full_Q2=False, gate_changed=False))

delivery = f'''[DERIVED — contato misto plano e primitiva explícita; Q2 completa OPEN]

Data {now.isoformat()}. Abertura SHA256 {sha(opening)}.

O contato das bolhas com linha suave constante foi calculado a partir dos
vértices existentes. Preservados normalização, sinal da fonte e prescrição.
Na base [p²trAB,p²trA trB,(pAp)trB+(pBp)trA,pABp]:

- métrico I: (23/8,-13/16,1,-2);
- métrico T: (3/4,-3/8,1/2,-1);
- ghost constante: (0,0,0,0).

A soma N_bolha G+E R_W não cancela nos dois setores métricos. Na base
[g p²(p·v),p²Gv,ppᵀ(p·v)] os resíduos são (-1/8,15/8,1/2) e
(5/4,1/4,-1). São diferenças de contato frente à referência definida por
derivação, não a anomalia completa nem sua classe cohomológica.

Construímos N_eff=N_bolha+E L_W+L_W E, autoadjunto, com
N_eff G=N_bolha G+E R_W. Portanto B=-C_E/2 integral h.N_eff h é
primitiva do resíduo neste recorte. A família eta E fica livre: nenhuma
subtração foi escolhida. Faltam jatos de W, curvatura e demais setores.

Evidência: {checks} verificações, CPU {cpu}s, ambos os comandos rc0.
Scripts: flat_mixed_smooth_bubble_check.py e flat_mixed_smooth_primitive_check.py,
executados com A4/symbolic_runtime/Scripts/python.exe -X utf8 -B.
Nota demonstrativa: {H / 'flat_mixed_smooth_bubble/DERIVACAO.md'}.
Manifesto conferido: {D / 'manifest.json'}; SHA256 {sha(D / 'manifest.json')}.

Orquestração ampliada: duas unidades Kimi (exaustão de jatos suaves e
normalização lorentziana do contato) e uma DeepSeek (auditoria independente
desta primitiva). Previews aprovados; preparação não equivale a execução.
Catálogo {catalog}. A coordenação recebeu os IDs para admissão pela fila
única. A revisão DeepSeek anterior tem prioridade na próxima vaga para
aproveitar concorrência entre provedores. MiMo em validação de transporte.

Originais científicos, kernel, gate e memórias canônicas intactos.
Próximo passo da bancada: jatos não constantes e revisão independente;
A7.b permanece dentro do teto, seguido dos ramos obrigatórios A7.c/d.
'''
atomic(OUT / 'ENTREGA_016_A7b_contato_misto_suave_e_primitiva.md', delivery.encode('utf-8'))
measure = f'''[REAL — MEDIDA de resíduo não nulo; não representa obstrução absoluta]

Abertura SHA256 {sha(opening)}. Data {now.isoformat()}.
Tentativa: comparar diretamente contato da bolha mista com fonte suave.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/flat_mixed_smooth_bubble_check.py.
rc0. Log {H / 'flat_mixed_smooth_bubble_run.log'}
SHA256 {sha(H / 'flat_mixed_smooth_bubble_run.log')}.
Identidade: N_bolha G+E R_I=(-g p²(p·v)+15p²Gv+4ppᵀ(p·v))/8,
e N_bolha G+E R_T=5g p²(p·v)/4+p²Gv/4-ppᵀ(p·v).
C_E e prefatores comuns retirados, p derivada real, W constante plano.
CPU bolha {results[0]['cpu_seconds']}s; primitiva {results[1]['cpu_seconds']}s.
Nenhuma chamada remota nova nesta medição. Nenhuma normalização ajustada.
Próximo ramo: primitiva N_eff e jatos suaves completos; a primitiva já
verificada é entregue ao lado, não apaga o resíduo da prescrição original.
'''
atomic(OUT / 'ENTREGA_016_MEDIDA_contato_misto_suave.md', measure.encode('utf-8'))

ledger = OUT / 'LEDGER_016.jsonl'
entries = [dict(at=now.isoformat(), event='A7_FLAT_MIXED_SMOOTH_CONTACT_AND_PRIMITIVE',
    target='A7.b', checks=checks, cpu_seconds=cpu, remote_call=False,
    manifest_sha256=sha(D / 'manifest.json'), full_Q2=False)]
for row in units:
    entries.append(dict(at=now.isoformat(), event='PROVIDER_UNIT_PREPARED_PREVIEW_ONLY',
        provider=row['provider'], target='A7.b', lemma=row['lemma'],
        request_id=row['request_id'], payload_sha256=row['payload_sha256'],
        new_remote_execution=False, status='STAGING_SENT_TO_COORDINATOR',
        tokens=None, cost_estimate_usd=None))
append(ledger, ''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in entries))
seen, cost = set(), Decimal(0)
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip(): continue
    row = json.loads(line)
    value = row.get('cost_estimate_usd')
    if value is None: continue
    key = row.get('execution_task_id') or row.get('job_id') or row.get('request_id')
    if key and key in seen: continue
    if key: seen.add(key)
    cost += Decimal(str(value))
put(D / 'cost_summary.json', dict(known_deduplicated_cost_usd=str(cost),
    completeness='PARTIAL; subscription and failed-call costs unknown, not zero',
    new_remote_executions=0))
append(OUT / 'ENTREGA_016_PROGRESSO.md',
    f'\n- {now.isoformat()} A7.b PROGRESS: contato misto suave plano não cancela; primitiva explícita sem escolha de prescrição; {checks}checks, CPU{cpu}s. Três revisões novas preparadas (Kimi2/DeepSeek1). Custo parcial deduplicado US${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json'; cont=json.loads(p.read_bytes())
cont.update(at=now.isoformat(), previous_goal_turn='PROGRESS',
    completed_this_turn=['Constant smooth mixed bubble contact calculated',
        'Local primitive of actual residual verified',
        'Two new Kimi and one DeepSeek independent units previewed and sent to coordinator'],
    next=['General nonconstant smooth jets and full Ward assembly',
          'Audit received Kimi reviews; preserve pending units',
          'A7.b deadline2026-09-25T20:32Z; then A7.c/d,A8,PartB,final audit'],
    mixed_smooth_manifest=str(D/'manifest.json'),
    smooth_completion_catalog=str(catalog), partial_metered_cost_usd=str(cost),
    pending_orchestration='Coordinator accepted next free slot for DeepSeek d317; new catalog sent; MiMo streaming offline correction awaiting one authorized public operational validation',
    own_live_processes=[])
atomic(p,json.dumps(cont,ensure_ascii=False,indent=2).encode('utf-8'),replace=True)
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_contato_misto_suave_e_primitiva.md'),
    artifacts=len(artifacts), checks=checks,cpu_seconds=cpu,cost_partial=str(cost),
    manifest_sha256=sha(D/'manifest.json'))))
