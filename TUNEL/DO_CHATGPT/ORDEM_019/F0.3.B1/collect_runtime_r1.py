import hashlib,json,re,subprocess,urllib.request
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BENCH=Path(r"C:\IALD\Bancada_Um")
NOS=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mtime_utc=datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat())
def save(n,d):
 p=ROOT/n
 with p.open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
 return pin(p)
with urllib.request.urlopen('http://127.0.0.1:18777/api/estado',timeout=15) as r:state=json.loads(r.read().decode('utf-8'))
statepin=save('LIVE_STATE_FULL_R1.json',dict(observed_at=datetime.now(timezone.utc).isoformat(),endpoint='http://127.0.0.1:18777/api/estado',response=state))
um=NOS/'um.py';ut=um.read_text(encoding='utf-8');up=pin(um)
up['version']=re.search(r'^UM_VERSION\s*=\s*[\"\']([^\"\']+)',ut,re.M).group(1)
up['alpha']=float(re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',ut,re.M).group(1))
files=[BENCH/'um_bancada.py',BENCH/'mcp_um.py',BENCH/'README.md',NOS/'um_absoluto_selo.json']+sorted((BENCH/'bancada').glob('*.py'))+sorted((BENCH/'tabelas').glob('*.json'))+sorted((BENCH/'estado').glob('validacao*.json'))
pins=[pin(p) for p in files]
validations=[]
for p in sorted((BENCH/'estado').glob('validacao*.json')):
 d=json.loads(p.read_text(encoding='utf-8'));validations.append(dict(path=str(p),keys=list(d),veredito=d.get('veredito'),resumo_curto_present='resumo_curto' in d))
prov=state.get('motor',{}).get('fontes',{}).get('alpha',{})
summary=dict(observed_at=datetime.now(timezone.utc).isoformat(),canonical=up,loaded_alpha_provenance=prov,loaded_um_hash_matches_current=prov.get('um_py_sha256')==up['sha256'],loaded_alpha_matches_current=state.get('motor',{}).get('alpha')==up['alpha'],state=statepin,pins=pins,validations=validations,scope='READ_ONLY_NO_MODEL_OR_OBSERVED_DATA_EXECUTION')
print(json.dumps(save('RUNTIME_COMPARISON_R1.json',summary),ensure_ascii=False))
print(json.dumps({k:summary[k] for k in ['canonical','loaded_alpha_provenance','loaded_um_hash_matches_current','loaded_alpha_matches_current','validations']},ensure_ascii=False,indent=2))
