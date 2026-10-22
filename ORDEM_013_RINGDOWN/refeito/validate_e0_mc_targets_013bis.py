"""Independent draws at a finite, recorded target grid; no adaptive-CI claim."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,hashlib,time,math
import numpy as np
from scipy.stats import beta
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,d):
    with p.open('xb') as f:f.write((json.dumps(d,indent=2,allow_nan=False)+'\n').encode())
source=B/'refeito/e0_route_iv_power_013bis_v2.py';result=B/'bis/E0_ROUTE_IV_POWER_v2.json'
d=json.loads(result.read_bytes())
if sha(source)!=d['code_sha256']:raise ValueError('Source changed')
spec=importlib.util.spec_from_file_location('mc',source);mc=importlib.util.module_from_spec(spec);spec.loader.exec_module(mc)
mc.budget();p=B/'bis/E0_ROUTE_IV_VALIDATION_PLAN.json';out=B/'bis/E0_ROUTE_IV_VALIDATION.json'
if p.exists() or out.exists():raise FileExistsError('Immutable validation outputs already exist')
plan=dict(status='NONBLIND_POWER_MC_VALIDATION_DESIGN',utc=datetime.now(timezone.utc).isoformat(),exploration_sha256=sha(result),simulation_code_sha256=sha(source),code_sha256=sha(Path(__file__)),draws_per_cell=20000,confidence='One-sided Clopper-Pearson with alpha=0.05/27 for all 27 prespecified validation cells; independent from exploration',alpha_per_cell=.05/27,cells=[])
for i,r in enumerate(d['results']):
    n=r['targets']['0.9']['at_or_above']['N']
    for j,scale in enumerate([1.,1.10,1.21]):
        plan['cells'].append(dict(population=r['population'],sigma_jit=r['sigma_jit'],N=math.ceil(n*scale),seed=14000000+i*10000+j*1000,scale_from_exploration=scale))
new(p,plan) # This receipt precedes every independent validation draw.
rows=d['per_event'];sel=json.loads((B/'C4_CATALOG_COMBINATION.json').read_bytes())['selected_events'];anchor=next(r for r in rows if r['event']=='GW250114_082203')['sigma_df']
pops={'GW250114_actual_width':np.array([anchor]),'GWTC5_31_quality_mixture':np.array([r['sigma_df'] for r in rows if r['event'] in sel]),'GWTC5_33_quality_mixture':np.array([r['sigma_df'] for r in rows])}
start=time.perf_counter();results=[]
for c in plan['cells']:
    mc.budget();s=pops[c['population']];n,y,yy=mc.sufficient(c['N'],s*s,c['sigma_jit'],plan['draws_per_cell'],c['seed']);t,_=mc.lrt(n,y,yy,s*s)
    k=int(np.sum(t>25));lower=float(beta.ppf(plan['alpha_per_cell'],k,len(t)-k+1)) if k else 0.
    results.append(dict(**c,successes=k,draws=len(t),power=k/len(t),simultaneous_lower=lower,meets_90_percent=lower>=.9))
    print(c['population'],c['sigma_jit'],c['N'],k/len(t),lower,flush=True)
selected=[]
for r in d['results']:
    cells=[c for c in results if c['population']==r['population'] and c['sigma_jit']==r['sigma_jit']]
    passed=[c for c in cells if c['meets_90_percent']]
    selected.append(dict(population=r['population'],sigma_jit=r['sigma_jit'],N90_validated=min(c['N'] for c in passed) if passed else None,status='POWER_90_CONFIRMED_WITHIN_GAUSSIAN_SCENARIO' if passed else 'POWER_90_NOT_ESTABLISHED_IN_GRID'))
# No physical-confirmation token: the result is explicitly scenario-only.
for r in selected:
    if r['N90_validated'] is not None:r['status']='GAUSSIAN_SCENARIO_POWER_LOWER_BOUND_GE_90_PERCENT'
new(out,dict(status='NONBLIND_MC_POWER_VALIDATION__PHYSICAL_TRANSFER_AND_NULL_TAIL_OPEN',plan_sha256=sha(p),source_result_sha256=sha(result),elapsed_seconds=time.perf_counter()-start,finished_utc=datetime.now(timezone.utc).isoformat(),cells=results,selected=selected,alpha_family=.05,not_calibrated=['5sigma false-positive tail','Physical transfer to pSEOB estimator','Nonzero systematic intrinsic variance']))
print('SAVED',out,sha(out))
