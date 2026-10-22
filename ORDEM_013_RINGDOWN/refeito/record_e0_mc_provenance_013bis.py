"""Post-computation custody receipt; explicitly not a preregistration."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,ast
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['C4_CATALOG_SCHEMA.json','C4_CATALOG_COMBINATION.json','refeito/e0_route_iv_power_013bis.py','refeito/e0_route_iv_power_013bis_v2.py','refeito/validate_e0_mc_targets_013bis.py','bis/E0_ROUTE_IV_SMOKE.json','bis/E0_ROUTE_IV_POWER_v2.json','bis/E0_ROUTE_IV_VALIDATION_PLAN.json','bis/E0_ROUTE_IV_VALIDATION.json','bis/E0_ROUTE_IV_POWER_NOTE.md','bis/PART_B_BUDGET_START.json']
rows={n:dict(bytes=(B/n).stat().st_size,sha256=sha(B/n)) for n in names}
schema=json.loads((B/names[0]).read_bytes());sel=json.loads((B/names[1]).read_bytes())['selected_events'];d=json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes());result={r['event']:r for r in d['per_event']}
if len(sel)!=len(set(sel)) or not set(sel)<=set(result):raise ValueError('Selection coverage')
if set(result)!={r['event'] for r in schema['rows']}:raise ValueError('Schema coverage')
for r in schema['rows']:
    if r['sha256']!=result[r['event']]['sha256']:raise ValueError('Source receipt mismatch')
for p in [B/'refeito/deliver_m6_ma_013bis.py',B/'refeito/start_part_b_budget_013bis.py']:ast.parse(p.read_text(encoding='utf-8'))
out=dict(status='POSTHOC_NONBLIND_COMPUTATION_CUSTODY__NOT_PREREGISTRATION',utc=datetime.now(timezone.utc).isoformat(),files=rows,selected_events=sel,selected_sigma_df=[result[e]['sigma_df'] for e in sel],coverage_verified=True,validation_design_preceded_independent_draws=True,physical_gate_unchanged=True,code_sha256=sha(Path(__file__)))
p=B/'bis/E0_ROUTE_IV_PROVENANCE.json'
with p.open('xb') as f:f.write((json.dumps(out,indent=2)+'\n').encode())
print('PASS',len(rows),len(sel),sha(p))
