"""Carry the real failed call into the queue's explicit limit guard."""
import json
from pathlib import Path
from iald_orchestrator.runtime import Runtime

base=Path(__file__).resolve().parent
record=json.loads((base/'validation'/'claude_corrected_run.json').read_bytes())
assert record['is_error'] and 'spend limit' in record['result']
runtime=Runtime(recover=False)
with runtime.db() as db:
    db.execute('INSERT OR IGNORE INTO provider_blocks VALUES(?,?,?)',(
        'claude',record['timestamp'],
        'Limite informado no teste de 23/09/2026 às 09:38 BRT. Cota atual não reconsultada; conferir no cliente oficial antes de permitir nova tentativa.'))
print('Recusa real registrada; nenhum novo pedido ao provedor.')
