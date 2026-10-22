"""Three tiny, public-input real runs; no patent documents are sent to providers."""
from pathlib import Path
import json
import os
import time
import uuid
from iald_orchestrator.runtime import Runtime, now

base=Path(__file__).resolve().parent
stamp=now().replace(':','').replace('.','')
runtime=Runtime(base/'validation'/('smoke_'+stamp))
prompts=[('local','Responda apenas o número que resulta de 2 + 2.'),
         ('codex','Demonstre em uma única frase por que a soma de dois números pares é par. Não use ferramentas.'),
         ('claude','Demonstre em uma única frase por que o produto de dois números ímpares é ímpar. Não use ferramentas.')]
receipts=[]
for expected,prompt in prompts:
    task=runtime.submit(prompt,str(uuid.uuid4()))
    deadline=time.monotonic()+290
    while time.monotonic()<deadline:
        task=runtime.task(task['id'])
        if task['status'] not in ('queued','running'):break
        time.sleep(1)
    receipt={'task_id':task['id'],'status':task['status'],'expected_provider':expected,
             'selected':(task.get('decision') or {}).get('selected'),'result':task.get('result'),'error':task.get('error')}
    receipts.append(receipt)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)
    if task['status']!='result_ready':break
payload=json.dumps({'timestamp':now(),'scope':'Public-input integration smoke test; no general quality benchmark','runs':receipts},ensure_ascii=False,indent=2).encode()
target=base/'validation'/('real_runs_'+stamp+'.json')
temp=target.with_suffix('.tmp');temp.write_bytes(payload);assert temp.read_bytes()==payload;os.replace(temp,target)
print(str(target),flush=True)
