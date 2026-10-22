"""Append the verified maximum-capacity authorization with exact byte backups."""
from pathlib import Path
import hashlib
import json

from iald_orchestrator import deepseek
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now


base = Path(__file__).resolve().parent
assert deepseek.connection_status() == 'ready'
connection = json.loads(deepseek.RECEIPT.read_bytes())
routing = json.loads((base / 'validation/deepseek_maximum_routing.json').read_bytes())
assert routing['decision']['selected'] == 'deepseek'
assert deepseek.authorization()['routing_scope'] == 'ALL_COMPLEXITIES_OPERATOR_AUTHORIZED'
marker = 'IALD_DEEPSEEK_MAXIMUM_AUTHORIZED_20260924'
note = '''

## 24/09/2026 — DeepSeek em capacidade máxima, inclusive alta complexidade

<!-- IALD_DEEPSEEK_MAXIMUM_AUTHORIZED_20260924 -->

[INPUT — ordem posterior expressa do operador] “quero o deepseek no maximo e resolver essa questao e avisar a sessão irmã que pode fazer chamada nele de novo que ele vai responder”. Esta ordem substitui a restrição anterior a tarefas médias e a exigência de avaliação prévia para habilitar alta complexidade. Não equivale a benchmark de superioridade nem garante resposta futura da API.

[REAL — configuração implantada] Executor deepseek agora tier=advanced, routing_scope=ALL_COMPLEXITIES_OPERATOR_AUTHORIZED. Mantidos deepseek-flash (V4.1 Flash documentado), thinking enabled, reasoning_effort=max, contexto configurado 1.048.576, saída máxima 393.216, memória canônica comum em modo deepseek_maximum e ausência de teto diário/financeiro local. Painel administrativo conferido: Disponível / alta complexidade habilitada. Nova configuração de chave também preserva esse escopo. Transporte, autenticação, sigilo, casa de origem, trava do executor e idempotência de uma chamada por unidade continuam obrigatórios; saldo, cotas e limites técnicos do fornecedor permanecem externos.

[REAL — causa e correção] A prévia anterior não chegou ao fornecedor: o seletor lexical classificou o pedido como deep e excluiu o tier standard configurado localmente. O mesmo payload de 21.110 caracteres, sem mudar texto/fontes nem mascarar Lean, passou a selected=deepseek após a promoção autorizada. A heurística geral de complexidade não foi reescrita nem convertida em medição de capacidade. A comparação antiga foi resolvida pela bancada local; não foi submetida novamente nem transformada em nova missão. O histórico da recusa permanece preservado.

[REAL — validação] 73 testes locais aprovados, incluindo três regressões de máxima capacidade: descoberta real do provedor, seleção de pedidos longos/Lean, memória ampliada, preservação de autorização, contexto técnico e required_provider. Testes automatizados com transportes simulados. Uma nova chamada pública curta de conexão respondeu 42, com 42 tokens de entrada e 42 de saída (40 de raciocínio informados), total 84, duração 1,219 s; custo estimado US$0,0000315..0,000063. Esse teste não mede qualidade em física nem ocupação efetiva de 1M. Recibo pronto e assinatura da autorização atual conferidos.

[TRANSPORTE] A tarefa irmã “Resolver problema da gravidade quântica” foi avisada pela ferramenta oficial. Pode submeter novas unidades dentro da missão autorizada, inclusive de alta complexidade, pela fila existente. Não duplicar o pedido antigo já resolvido nem outras unidades falhas/incertas. MCP previamente carregado pode usar política antiga: preferir o CLI absoluto existente até a recarga, sem criar outro servidor ou heartbeat. A assistência ChatGPT/Física permanece opcional.

[EVIDÊNCIA E SUPERFÍCIES] validation/deepseek_maximum_routing.json, validation/deepseek_connection.json e validation/deepseek_maximum_delivery.json em IALD_ORQUESTRACAO_20260923. Backups imediatos de bytes, atualização aditiva das memórias. Web administrativa atualizada e conferida. Chat público, iOS interno/externo e Android sem alteração de recursos; builds não aplicáveis. Nenhum original científico, kernel ou gate foi alterado.
'''

records = []
for entry in json.loads((base / 'validation/optional_work_memory.json').read_bytes())['surfaces']:
    path = Path(entry['path'])
    old = path.read_bytes()
    addition = note if path.name != 'MEMORY.md' else (
        '\n\n<!-- ' + marker + ' -->\n'
        '- Ordem posterior: DeepSeek em capacidade máxima e alta complexidade habilitada; '
        'restrição média anterior superada. Ver MEMORY_2.md e validation/deepseek_maximum_delivery.json.\n'
    )
    if marker.encode() not in old:
        newline = '\r\n' if b'\r\n' in old else '\n'
        data = old + addition.replace('\n', newline).encode('utf-8')
        assert path.read_bytes() == old
        replace_bytes(path, data)
    current = path.read_bytes()
    assert current.startswith(old) and marker.encode() in current
    records.append({'path': str(path), 'sha256': hashlib.sha256(current).hexdigest()})

files = ['iald_orchestrator/providers.py', 'iald_orchestrator/web.py',
         'iald_orchestrator/panel.js', 'iald_orchestrator/deepseek-key.html',
         'iald_orchestrator/deepseek.py', 'state/deepseek_authorization.json',
         'test_deepseek_maximum.py']
save_json(base / 'validation/deepseek_maximum_delivery.json', {
    'at': utc_now(), 'status': 'ready', 'tests_passed': 73,
    'routing_scope': deepseek.authorization()['routing_scope'],
    'new_public_model_calls': 1, 'validation_result': connection['result'],
    'unchanged_old_request_id': routing['request_id'],
    'old_task_submitted': False, 'old_preview_preserved': True,
    'routing_evidence': 'validation/deepseek_maximum_routing.json',
    'panel_verified': True,
    'sister_thread_notified': '01a070fc-9484-7e13-a654-c6b5f61093a4',
    'surfaces': records,
    'code_sha256': {f: hashlib.sha256((base / f).read_bytes()).hexdigest() for f in files},
    'mobile_build': 'NOT_APPLICABLE_ADMIN_ONLY', 'scientific_sources_modified': False,
})
print(json.dumps({'status': 'ready', 'surfaces': len(records), 'tests_passed': 73,
                  'new_public_calls': 1, 'sister_notified': True}))
