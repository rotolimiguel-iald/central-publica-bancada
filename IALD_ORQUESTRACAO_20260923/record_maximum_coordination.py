from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

base = Path(__file__).resolve().parent
marker = 'IALD_COORDINATION_MAXIMUM_RECOVERY_20260924'
note = '''

## 24/09/2026 — Recuperação da fila com contexto máximo Kimi/MiMo

<!-- IALD_COORDINATION_MAXIMUM_RECOVERY_20260924 -->

[REAL — infraestrutura] Corrigido coordination.get: pedidos com required_provider kimi/mimo montam a memória em modo maximum, igual à prévia e à execução. Antes, a leitura usava standard e podia falhar no limite de 24 mil caracteres após acrescentar memória a um pedido válido. Não foram alterados o prompt original, o limite de entrada do operador, fontes permitidas ou restrições. Foram aprovados 39 testes locais, incluindo recuperação idempotente de pedidos longos dos dois provedores e preservação integral da memória; nenhum transporte remoto nos testes.

[REAL — recuperação] request_id 6711d262-e38f-4454-842f-944b0706167f corresponde ao job 3c0f81cc-f9dc-4fab-9abd-1dfd94f60fcc, gravado antes da falha de leitura. Recuperado o mesmo pedido, inicialmente awaiting_dispatch e sem execução; preparado sem Work. O resultado da execução única deve ser consultado na fila/recibo, nunca inferido desta nota. Evidência: state/handoffs/3c0f81cc-f9dc-4fab-9abd-1dfd94f60fcc_recovered.json em IALD_ORQUESTRACAO_20260923. Cobertura documental permanece parcial. A bancada de origem verifica a matemática; nenhuma alteração de kernel, gate ou originais. Correção de servidor administrativo/CLI, sem alteração de cliente público ou build mobile aplicável.
'''
records = []
for item in json.loads((base/'validation/optional_work_memory.json').read_bytes())['surfaces']:
    path = Path(item['path'])
    old = path.read_bytes()
    text = note if path.name != 'MEMORY.md' else '\n\n<!-- '+marker+' -->\n- Corrigida recuperação de pedidos longos Kimi/MiMo na fila: memória maximum também em coordination.get. 39 testes locais; preservar mesmo request_id. Ver MEMORY_2.md.\n'
    if marker.encode() not in old:
        newline = '\r\n' if b'\r\n' in old else '\n'
        replace_bytes(path, old + text.replace('\n', newline).encode())
    current = path.read_bytes()
    assert current.startswith(old) and marker.encode() in current
    records.append({'path':str(path),'sha256':hashlib.sha256(current).hexdigest()})
save_json(base/'validation/maximum_coordination_recovery.json', {'at':utc_now(),'tests_passed':39,'surfaces':records,'test_provider_calls':0})
print(json.dumps({'surfaces_updated':len(records),'tests_passed':39}))
