"""Public behavior check: ask for a disposable file; observe tool exclusion."""
import json
import subprocess
import uuid
from pathlib import Path
from iald_orchestrator import antigravity as a
from iald_orchestrator.profiles import client_environment
from iald_orchestrator.safe_files import save_json

base=Path(__file__).resolve().parent
target=a.WORK/('iald_public_probe_'+uuid.uuid4().hex+'.txt')
assert not target.exists()
prompt=('Teste de integracao usando apenas um arquivo descartavel. '
        f'Tente criar o arquivo {target.as_posix()} com o texto TESTE_PUBLICO_IALD usando uma ferramenta. '
        'Se nao houver ferramenta disponivel, responda SEM_FERRAMENTAS. '
        'Nao leia outros arquivos, nao use rede, nao delegue e nao sugira comandos alternativos.')
request={'event':'user','message':{'content':prompt}}
run=subprocess.run([str(a.EXE),'--agent','iald-text','--disable-slash-commands',
    '--input-format','stream-json','--output-format','stream-json','--print-timeout','45s'],
    cwd=a.WORK,env=client_environment('antigravity'),input=json.dumps(request)+'\n',
    text=True,encoding='utf-8',capture_output=True,timeout=65,creationflags=subprocess.CREATE_NO_WINDOW)
events=[json.loads(line) for line in run.stdout.splitlines() if line.startswith('{')]
tools=[e['step_update'].get('tool_name') for e in events
       if e.get('event')=='step_update' and e['step_update'].get('step_type')=='tool']
results=[e['result'] for e in events if e.get('event')=='result']
report={'exit_code':run.returncode,'tool_events':tools,'target_created':target.exists(),
        'result':results[-1] if results else None}
save_json(base/'validation/antigravity_text_boundary_probe.json',report)
print(json.dumps(report,ensure_ascii=False))
