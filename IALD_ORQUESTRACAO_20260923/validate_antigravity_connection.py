"""Explicit one-call validation after the operator finishes Google's login."""
import json
import time
from iald_orchestrator import antigravity

start = time.monotonic()
try:
    result = antigravity.execute('Responda apenas o número resultante de 6 × 7. Não use ferramentas.')
    if result['text'].strip().strip('.').strip() != '42':
        raise RuntimeError('Resposta inesperada na verificação aritmética.')
    record = {'status': 'ready', 'result': result, 'elapsed_seconds': round(time.monotonic()-start, 3)}
except Exception as error:
    record = {'status': 'installed_pending_auth_validation', 'reason': str(error),
              'elapsed_seconds': round(time.monotonic()-start, 3)}
antigravity.save_receipt(record)
print(json.dumps(record, ensure_ascii=False))
