from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'TUNEL/DO_CHATGPT'
DEST = HERE / 'orchestration'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p, raw):
    if isinstance(raw, str):
        raw = raw.encode('utf-8')
    if p.exists():
        old = p.read_bytes()
        if old == raw:
            return
        backup = p.with_name(p.name + '.bak_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and raw
    temp.replace(p)

catalog = json.loads((DEST / 'prepared_units.json').read_bytes())
opening = sha(OUT / 'ENTREGA_016_ABERTURA_operador.md')
for unit in catalog:
    payload_path = Path(unit['payload'])
    assert sha(payload_path) == unit['payload_sha256']
    payload = json.loads(payload_path.read_bytes())
    assert payload['request_id'] == unit['request_id']
    assert payload['execution_constraints']['required_provider'] == unit['selected']
    receipt = json.loads((DEST / (unit['slug'] + '_receipt.json')).read_bytes())
    for source in receipt['source_receipts']:
        assert sha(Path(source['path'])) == source['sha256']

now = datetime.now(timezone.utc).isoformat()
marker = 'A7_ORCHESTRATION_FOUR_UNITS_PREPARED_20260924'
ledger = OUT / 'LEDGER_016.jsonl'
raw = ledger.read_bytes()
if marker.encode() not in raw:
    events = [dict(event=marker, at=now, provider=u['provider'], target='A-7.b',
                   request_id=u['request_id'], payload_sha256=u['payload_sha256'],
                   phase='PREPARED_FOR_EXISTING_COORDINATOR', external_execution=False,
                   tokens=None, cost_usd=None, opening_sha256=opening) for u in catalog]
    save(ledger, raw + ''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in events).encode())
costs = {}
for line in ledger.read_text(encoding='utf-8-sig').splitlines():
    if not line.strip():
        continue
    event = json.loads(line)
    cost = event.get('cost_estimate_usd', event.get('cost_usd', event.get('custo_usd')))
    key = event.get('execution_id') or event.get('job_id') or event.get('request_id') or event.get('execution_task_id')
    if cost is not None and key:
        costs[key] = Decimal(str(cost))
total = sum(costs.values(), Decimal(0))
report = OUT / 'ENTREGA_016_A7_orquestracao_adicional.md'
if not report.exists():
    rows = '\n'.join(f"| {u['provider']} | {u['slug']} | `{u['request_id']}` |" for u in catalog)
    save(report, f'''[REAL — preparação e prévias locais; INPUT — distribuição à coordenação existente]

# A7 — quatro unidades adicionais

Abertura SHA256: `{opening}`.
Data UTC: {now}.

Pedido do operador: “distribua mais tarefas para os modelos, principalmente para o Kimi ele está respodendo muito bem, vamos acelerar usar todos os nossos recursos a nosso favor, contratei o plano máximo do kimi para te ajudar”.

| Executor | Unidade | request_id |
|---|---|---|
{rows}

As quatro prévias selecionaram os executores obrigatórios. Fontes, linhas, SHA256 e recibos estão no catálogo `{DEST / 'prepared_units.json'}` (SHA256 `{sha(DEST / 'prepared_units.json')}`). A memória científica canônica comum será acrescentada pelo adaptador. Cada unidade admite uma chamada, sem substituição silenciosa ou duplicação.

O catálogo foi enviado pela ferramenta oficial à tarefa coordenadora 01a0ce2b-8c2f-71b0-a9a8-91b17715a569 para despacho após os catálogos anteriores. Neste registro, estas quatro unidades estão PREPARADAS, não há resultado de execução delas. A fila operacional tinha cinco jobs ativos: DeepSeek H3 em execução e quatro A6 aguardando. Não foi criado outro worker nem alterada a fila.

Kimi recebe a prescrição dos produtos temporais e a ligação cohomológica à anomalia. MiMo confere a especialização do modelo e os dados ausentes. DeepSeek revisa sinais/graduações de Wess–Zumino e propõe controles CAS. O fundo sigma constante projetado da087 permanece distinto do fundo físico sigma=id da069. A classe clássica H4 não será promovida a coeficiente quântico.

Falha de preparação preservada em prepare_orchestration.py: fim de excerto155 para fonte de152linhas. Corrigida em prepare_orchestration_v2.py; nenhum envio remoto por esses scripts; IDs preservados. Nenhum cálculo de anomalia foi realizado nesta preparação. A prescrição deverá ser fixada antes do cálculo local.

Ledger SHA256 `{sha(ledger)}`; estimativas explícitas deduplicadas US${total}, incompletas e não equivalentes à fatura. Novas unidades sem consumo informado; não se atribui custo zero à assinatura. Zero escrita em originais, kernel, memórias canônicas ou gate.
''')
progress = OUT / 'ENTREGA_016_PROGRESSO.md'
raw = progress.read_bytes()
if marker.encode() not in raw:
    save(progress, raw + f'\n- {now} — A7.b EM ANDAMENTO: quatro unidades preparadas/encaminhadas (Kimi2,MiMo1,DeepSeek1); prévias e fontes conferidas; despacho depende da fila existente. Nenhuma anomalia calculada nesta preparação; nenhum gate movido. Estimativas externas registradas US${total}, incompletas; tempo dedicado de bancada não isolado. Abertura {opening}. [{marker}]\n'.encode())
print(json.dumps(dict(report=str(report), catalog_sha256=sha(DEST/'prepared_units.json'),
                      units=len(catalog), stage='PREPARED_FOR_COORDINATOR',
                      explicit_recorded_cost_usd=str(total)), ensure_ascii=False))
