"""Register the tested local MCP using the official CLI, preserving configuration."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib
from iald_orchestrator.providers import client_command

base=Path(__file__).resolve().parent
home=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))
config=home/'config.toml'
old=config.read_bytes()
before=tomllib.loads(old.decode('utf-8'))
name='iald-orchestrator'
expected={'command':r'C:\Python314\python.exe','args':[str(base/'mcp_server.py')]}
existing=before.get('mcp_servers',{}).get(name)
if existing:
    assert all(existing.get(k)==v for k,v in expected.items()),'Nome MCP já possui outra configuração.'
    print('MCP já registrado com a configuração esperada.')
    raise SystemExit(0)
backup=config.with_name(config.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
backup.write_bytes(old)
assert backup.read_bytes()==old
assert config.read_bytes()==old
command=client_command('codex')
assert command
result=subprocess.run(command+['mcp','add',name,'--',expected['command'],*expected['args']],
    capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=30)
assert result.returncode==0,'O cliente oficial recusou o registro; configuração deve ser conferida.'
new=config.read_bytes()
after=tomllib.loads(new.decode('utf-8'))
added=after['mcp_servers'].pop(name)
assert all(added.get(k)==v for k,v in expected.items())
if not after['mcp_servers'] and 'mcp_servers' not in before:
    after.pop('mcp_servers')
assert before==after,'O registro alterou outras opções; conferir diferenças antes de usar.'
receipt={'timestamp':datetime.now().isoformat(),'status':'REGISTERED', 'server':name,
    'backup':str(backup),'tools':['iald_orchestration_status','iald_selection_preview'],
    'config_sha256':hashlib.sha256(new).hexdigest(),'other_options_preserved':True,
    'scope':'Consultas locais por stdio; sem nova porta de rede e sem ferramenta de execução.'}
output=base/'validation'/'mcp_registration.json'
temp=output.with_suffix('.tmp')
temp.write_bytes(json.dumps(receipt,ensure_ascii=False,indent=2).encode())
assert temp.stat().st_size>0
os.replace(temp,output)
print(json.dumps(receipt,ensure_ascii=False))
