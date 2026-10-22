"""Pin the effective no-tool agent and account for the CLI's broad init inventory."""
from pathlib import Path
import json
from iald_orchestrator import antigravity as a
from iald_orchestrator.safe_files import replace_bytes, save_json

base=Path(__file__).resolve().parent
comparison=json.loads((base/'validation/antigravity_capability_comparison.json').read_bytes())
assert comparison['same_advertised_inventory']
assert set(comparison['positive']['tool_events'])=={'view_file'}
assert not comparison['negative']['tool_events']
assert comparison['negative']['response'].strip()=='SEM_FERRAMENTAS'
# The positive control demonstrated tool invocation, not successful file access:
# headless permission policy independently denied that public file read.
global_agent=Path(r'C:\Users\rotol\.gemini\config\agents\iald-text\agent.md')
text='''---
name: iald-text
description: Executor textual da integracao IALD, sem ferramentas.
tools: []
mainAgent: true
subagent: false
inheritCustomizations: false
excludeDefaultComponents: true
commandExecutionPolicy: "off"
mcpServers: []
skills: []
plugins: []
rules: []
hooks: []
---

Responda em portugues ao pedido recebido usando apenas o contexto fornecido. Produza texto ou codigo textual. Nao use ferramentas, delegacao, leitura de arquivos, navegacao ou acoes externas. Nao invente execucao, prova, hash ou resultado. Se faltar informacao, indique a lacuna. Preserve os estatutos fornecidos. Limite a resposta a 1500 palavras.
'''
for p in (a.AGENT,a.WORK/'.agents/agents/iald-text.md',global_agent):
    replace_bytes(p,text.encode('utf-8'))
hooks=a.WORK/'.agents/hooks.json'
if hooks.exists():
    config=json.loads(hooks.read_bytes())
    for hook in config.values():hook['enabled']=False
    save_json(hooks,config)
save_json(base/'validation/antigravity_client_inventory.json',{
    'advertised_tools':comparison['negative']['init_tools'],
    'meaning':'Build inventory differs from effective custom agent tools; measured with controlled profiles.',
    'comparison':'validation/antigravity_capability_comparison.json',
    'positive_control':'view_file invoked; read independently denied by headless permission policy',
    'negative_control':'no tool events; SEM_FERRAMENTAS'})

path=base/'iald_orchestrator/antigravity.py'
data=path.read_text(encoding='utf-8')
data=data.replace("RECEIPT = BASE / 'validation/antigravity_connection.json'", """RECEIPT = BASE / 'validation/antigravity_connection.json'
GLOBAL_AGENT = Path(r'C:\\Users\\rotol\\.gemini\\config\\agents\\iald-text\\agent.md')
INVENTORY = BASE / 'validation/antigravity_client_inventory.json'


def validate_profile():
    # Google CLI resolves this named agent globally on this host. Pin all copies.
    import yaml
    data = AGENT.read_bytes()
    for path in (GLOBAL_AGENT, WORK / '.agents/agents/iald-text.md'):
        if path.read_bytes() != data:
            raise RuntimeError('Perfis Antigravity divergentes; revalidacao necessaria.')
    parts = data.decode('utf-8').split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise RuntimeError('Perfil Antigravity invalido.')
    config = yaml.safe_load(parts[1])
    expected = {'name':'iald-text', 'tools':[], 'mainAgent':True, 'subagent':False,
        'inheritCustomizations':False, 'excludeDefaultComponents':True,
        'commandExecutionPolicy':'off', 'mcpServers':[], 'skills':[],
        'plugins':[], 'rules':[], 'hooks':[]}
    if not isinstance(config, dict) or any(type(config.get(k)) is not type(v) or config.get(k) != v for k,v in expected.items()):
        raise RuntimeError('Antigravity nao confirmou o perfil textual restrito; pedido nao enviado.')
    if set(config) - set(expected) - {'description'}:
        raise RuntimeError('Perfil Antigravity ganhou capacidades nao validadas.')
    return config
""")
data=data.replace("    binary = EXE.stat()", "    validate_profile()\n    binary = EXE.stat()")
data=data.replace("'agent_sha256': hashlib.sha256(AGENT.read_bytes()).hexdigest()}",
    "'agent_sha256': hashlib.sha256(AGENT.read_bytes()).hexdigest(),\n            'global_agent_sha256': hashlib.sha256(GLOBAL_AGENT.read_bytes()).hexdigest(),\n            'inventory_sha256': hashlib.sha256(INVENTORY.read_bytes()).hexdigest()}")
data=data.replace("    if RECEIPT.is_file():\n        record", "    try:\n        current_signature = signature()\n    except (OSError, ValueError, RuntimeError):\n        return 'installed_pending_auth_validation'\n    if RECEIPT.is_file():\n        record")
data=data.replace("record.get('signature') == signature()", "record.get('signature') == current_signature")
old="""    if event.get('event') != 'init' or init.get('tools') != []:
        raise RuntimeError('Antigravity não confirmou o perfil sem ferramentas; pedido não enviado.')"""
new="""    validate_profile()
    tools = init.get('tools')
    inventory = json.loads(INVENTORY.read_bytes())['advertised_tools']
    # CLI 1.2.9 advertises the same build catalogue for different custom tools.
    # Effective capability exclusion is configured by excludeDefaultComponents
    # and tools=[] above. Never accept an unknown inventory or mutable profile.
    if event.get('event') != 'init' or not isinstance(tools, list) or (tools != [] and tools != inventory):
        raise RuntimeError('Inventario Antigravity mudou; pedido nao enviado.')"""
assert old in data
data=data.replace(old,new)
data=data.replace('    args = [str(EXE)', '    validate_profile()\n    args = [str(EXE)')
replace_bytes(path,data.encode('utf-8'))
print('Perfil restrito e validacao de inventario corrigidos; pronto para teste real pelo adaptador.')
