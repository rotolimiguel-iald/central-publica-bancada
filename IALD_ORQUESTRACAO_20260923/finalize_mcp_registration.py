"""Preserve every prior option after the CLI normalized an existing empty args key."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tomllib

base=Path(__file__).resolve().parent
config=Path(r'C:\Users\rotol\.codex\config.toml')
source=config.with_name('config.toml.bak_20260923_135822_459283')
original=source.read_bytes()
old=config.read_bytes()
prior=tomllib.loads(original.decode())
current=tomllib.loads(old.decode())
name='iald-orchestrator'
expected={'command':r'C:\Python314\python.exe','args':[str(base/'mcp_server.py')]}
assert current['mcp_servers'].pop(name)==expected
assert prior['mcp_servers']['node_repl']['args']==[]
assert 'args' not in current['mcp_servers']['node_repl']
current['mcp_servers']['node_repl']['args']=[]
assert current==prior,'Outra alteração concorrente exige revisão.'
newline='\r\n' if b'\r\n' in original else '\n'
addition=newline.join(['',f'[mcp_servers.{name}]',
    'command = '+json.dumps(expected['command']),
    'args = '+json.dumps(expected['args']), ''])
new=original+addition.encode()
parsed=tomllib.loads(new.decode())
assert parsed['mcp_servers'].pop(name)==expected and parsed==prior
backup=config.with_name(config.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
backup.write_bytes(old)
assert backup.read_bytes()==old
temp=config.with_name(config.name+'.orchestrator.tmp')
temp.write_bytes(new)
assert temp.read_bytes()==new and config.read_bytes()==old
os.replace(temp,config)
assert config.read_bytes()==new
report={'timestamp':datetime.now().isoformat(),'status':'REGISTERED','server':name,
    'backup':str(backup),'original_backup':str(source),
    'tools':['iald_orchestration_status','iald_selection_preview'],
    'config_sha256':hashlib.sha256(new).hexdigest(),'other_options_preserved':True,
    'normalization_corrected':'O CLI removeu node_repl.args vazio; opção reposta. Demais bytes originais preservados.',
    'scope':'Consulta local por stdio; sem porta de rede ou execução de modelos.'}
out=base/'validation'/'mcp_registration.json'
tmp=out.with_suffix('.tmp');tmp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
assert tmp.stat().st_size>0
os.replace(tmp,out)
print(json.dumps(report,ensure_ascii=False))
