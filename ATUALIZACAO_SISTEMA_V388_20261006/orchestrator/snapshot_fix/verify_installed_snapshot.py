"""Read the installed snapshot in a fresh process; no provider or original-source execution."""
from pathlib import Path
import os,sys,json,hashlib
W=Path(__file__).resolve().parent;BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True;sys.path.insert(0,str(BASE))
from iald_orchestrator import canonical_memory as memory
from iald_orchestrator.safe_files import save_json
sha=lambda b:hashlib.sha256(b).hexdigest()
prep=json.loads((W/'PREPARATION.json').read_bytes())
if Path(memory.__file__).resolve()!=BASE/'iald_orchestrator/canonical_memory.py' or sha(Path(memory.__file__).read_bytes())!=prep['candidate_module_sha256']:raise ValueError('New process loaded unexpected module')
m,fresh=memory.load(BASE/'state/canonical_memory')
if fresh!='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED' or m['generation']!=prep['generation'] or m['index_sha256']!=prep['index_sha256']:raise ValueError('Installed memory identity differs')
p=memory.prepare('TGL Hubble razão v388',BASE/'state/canonical_memory')
if p['receipt']['generation']!=m['generation']:raise ValueError('Retrieval generation differs')
if sha((BASE/'project_fisica/MANIFESTO_LOCAL.json').read_bytes())!=prep['historical_catalog_sha256']:raise ValueError('Historical catalog changed')
result={'status':'PASS_NEW_PROCESS_SNAPSHOT_VERIFIED','pid':os.getpid(),'interpreter':sys.executable,'module_sha256':prep['candidate_module_sha256'],'generation':m['generation'],'index_sha256':m['index_sha256'],'documents':len(m['documents']),'chunks':m['chunks'],'freshness':fresh,'retrieval_receipt':p['receipt'],'old_mcp_hot_reload_verified':False,'providers_called':0}
save_json(W/'NEW_PROCESS_VERIFICATION.json',result);print(json.dumps({k:v for k,v in result.items() if k!='retrieval_receipt'},ensure_ascii=False))
