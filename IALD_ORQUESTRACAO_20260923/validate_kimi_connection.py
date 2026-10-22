"""One explicitly invoked, public K3 subscription validation; no periodic calls."""
import time
from iald_orchestrator import kimi
from iald_orchestrator.providers import SYSTEM

started=time.monotonic()
try:
    result=kimi.execute(SYSTEM+'\n\nTAREFA:\nEscreva apenas uma função Python add(a, b) que retorna a soma. Sem ferramentas.')
    result['elapsed_seconds']=round(time.monotonic()-started,3)
    if 'return a + b' not in result['text']:
        raise RuntimeError('Resposta não corresponde ao teste público de conexão.')
    kimi.save_receipt({'status':'ready','model':kimi.MODEL,'result':result,'tools_exposed':0,'delegation_enabled':False})
    print({'status':'ready','usage':result['usage'],'elapsed_seconds':result['elapsed_seconds']})
except Exception as exc:
    kimi.save_receipt({'status':'validation_failed','reason':str(exc)})
    raise
