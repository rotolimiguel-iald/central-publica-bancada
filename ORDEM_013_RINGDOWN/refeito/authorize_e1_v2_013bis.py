"""Issue v2 receipt after full v1 review plus verified environment-only diff."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,hashlib
B=Path(__file__).resolve().parents[1];R=B.parent;D=B/'bis/e1_nuisance_v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'DESIGN_MANIFEST.json').read_bytes())
for r in manifest['files']:
    p=(R/r['path']).resolve()
    if not p.is_relative_to(R) or sha(p)!=r['sha256']:raise ValueError('Design input changed')
budget=json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes());now=datetime.now(timezone.utc)
auth={'status':'E0_SEALED_E1_AUTHORIZED','approved_by_role':'principal_agent',
 'design_manifest_sha256':sha(D/'DESIGN_MANIFEST.json'),'sealed_E0_path':'ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json',
 'sealed_E0_sha256':sha(B/'PORTAO_DA_AMPLIACAO_V1.json'),'issued_utc':now.isoformat(),
 'expires_utc':min(now+timedelta(minutes=30),datetime.fromisoformat(budget['hard_deadline_utc'])).isoformat(),
 'review':'Full v1 source/plan reviewed; v2 diff removes absent optional threadpoolctl and records environment-only thread caps. Science AST unchanged. Conditional nuisance only, no calibrated significance.',
 'limits':{'runtime_s':900,'threads_requested':1,'new_posterior_downloads':False,'new_PE':False},'code_sha256':sha(Path(__file__))}
with (D/'AUTHORIZATION.json').open('x',encoding='utf-8') as f:json.dump(auth,f,ensure_ascii=False,indent=2)
print(json.dumps({'authorization_sha256':sha(D/'AUTHORIZATION.json'),'expires_utc':auth['expires_utc']}))
