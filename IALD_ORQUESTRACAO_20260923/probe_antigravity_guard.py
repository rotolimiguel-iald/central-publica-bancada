"""Single public diagnostic with the official all-tool deny hook installed."""
import json
import subprocess
from pathlib import Path
from iald_orchestrator import antigravity as a
from iald_orchestrator.profiles import client_environment
from iald_orchestrator.safe_files import save_json

base=Path(__file__).resolve().parent
hook=base/'antigravity_text_guard.py'
command='"C:\\Python314\\python.exe" -X utf8 "'+str(hook)+'" '
save_json(a.WORK/'.agents/hooks.json',{'iald-text-only':{
    'PreToolUse':[{'matcher':'*','hooks':[{'type':'command','command':command+'pretool','timeout':10}]}],
    'PreInvocation':[{'type':'command','command':command+'preinvocation','timeout':10}]}})
prompt='Responda somente o resultado de 6 vezes 7, sem ferramentas.'
request={'event':'user','message':{'content':prompt}}
result=subprocess.run([str(a.EXE),'--agent','iald-text','--disable-slash-commands',
    '--input-format','stream-json','--output-format','stream-json','--print-timeout','60s'],
    cwd=a.WORK,env=client_environment('antigravity'),input=json.dumps(request)+'\n',
    text=True,encoding='utf-8',capture_output=True,timeout=85,creationflags=subprocess.CREATE_NO_WINDOW)
events=[json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
summaries=[]
conversation=None
for event in events:
    if event.get('event')=='init':
        conversation=event.get('conversation_id')
        summaries.append({'event':'init','agent':event['init'].get('agent'),
                          'tools_count':len(event['init'].get('tools',[]))})
    elif event.get('event')=='result':
        summaries.append({'event':'result','result':event.get('result')})
    elif event.get('event')=='step_update':
        step=event['step_update']
        summaries.append({'event':'step_update','type':step.get('step_type'),
                          'tool':step.get('tool_name'),'state':step.get('state')})
records=[]
if conversation:
    records=[json.loads(p.read_bytes()) for p in (base/'state/antigravity_guard').glob(conversation+'_*.json')]
report={'exit_code':result.returncode,'events':summaries,'guard_records':records,
        'stderr_present':bool(result.stderr)}
save_json(base/'validation/antigravity_guard_probe.json',report)
print(json.dumps(report,ensure_ascii=False))
