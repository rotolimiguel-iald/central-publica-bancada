"""Controlled public test of effective per-agent tools, not the init inventory."""
import json
from pathlib import Path
import subprocess
import uuid
from iald_orchestrator import antigravity as a
from iald_orchestrator.profiles import client_environment
from iald_orchestrator.safe_files import replace_bytes, save_json

base=Path(__file__).resolve().parent
profiles=[a.AGENT,a.WORK/'.agents/agents/iald-text.md',Path(r'C:\Users\rotol\.gemini\config\agents\iald-text\agent.md')]
original=[p.read_bytes() for p in profiles]
public=a.WORK/('public_capability_test_'+uuid.uuid4().hex+'.txt')
value='PUBLIC_TEST_'+uuid.uuid4().hex
replace_bytes(public,value.encode())
prompt=(f'Teste publico de capacidade. Leia SOMENTE {public.as_posix()} usando view_file e devolva seu conteudo exato. '
        'Nao leia outros arquivos nem use outras ferramentas. Se view_file nao estiver disponivel, responda SEM_FERRAMENTAS.')

def call(label):
    result=subprocess.run([str(a.EXE),'--agent','iald-text','--disable-slash-commands',
        '--input-format','stream-json','--output-format','stream-json','--print-timeout','50s'],
        cwd=a.WORK, env=client_environment('antigravity'),
        input=json.dumps({'event':'user','message':{'content':prompt}})+'\n',
        text=True,encoding='utf-8',capture_output=True,timeout=70,
        creationflags=subprocess.CREATE_NO_WINDOW)
    events=[json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
    init=next(e['init'] for e in events if e.get('event')=='init')
    final=next(e['result'] for e in events if e.get('event')=='result')
    tools=[e['step_update'].get('tool_name') for e in events
           if e.get('event')=='step_update' and e['step_update'].get('step_type')=='tool']
    observed=value in json.dumps([e.get('step_update',{}).get('tool_info') for e in events])
    return {'label':label,'init_tools':init['tools'],'tool_events':tools,
            'public_value_in_tool_output':observed,
            'tool_diagnostics':[e.get('step_update',{}).get('tool_info') for e in events if e.get('step_update',{}).get('tool_info')],
            'returned_public_value':value in final.get('response',''),
            'response':final.get('response'),'status':final.get('status'),'usage':final.get('usage')}

try:
    # No named hooks: the previous probe proved their path could not resolve in this CLI.
    header=(b'---\nname: iald-text\ndescription: IALD public capability test.\n'
            b'tools: [view_file]\nmainAgent: true\nsubagent: false\n'
            b'inheritCustomizations: false\nexcludeDefaultComponents: true\n'
            b'commandExecutionPolicy: "off"\nmcpServers: []\nskills: []\nplugins: []\nrules: []\nhooks: []\n---\n'
            b'Read only the single public test file explicitly named in the prompt. No other actions.\n')
    for p in profiles:replace_bytes(p,header)
    positive=call('only_view_file')
finally:
    for p,data in zip(profiles,original):replace_bytes(p,data)

negative=call('no_tools')
report={'positive':positive,'negative':negative,
        'same_advertised_inventory':positive['init_tools']==negative['init_tools'],
        'effective_tools_differ':positive['public_value_in_tool_output'] and bool(positive['tool_events']) and
             not negative['returned_public_value'] and not negative['tool_events']}
save_json(base/'validation/antigravity_capability_comparison.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('positive','negative')},ensure_ascii=False))
for item in (positive,negative):
    print(json.dumps({k:v for k,v in item.items() if k not in ('init_tools',)},ensure_ascii=False))
