"""Light deterministic review: binomial inversion, sufficient-statistic algebra and receipts.
Never execute either builder, never open HDF5, never run a Monte Carlo campaign.
"""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import ast,copy,hashlib,json,math,time,warnings
import numpy as np
B=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((B/p).read_bytes())
def req(x,m):
    if not x:raise ValueError(m)

# Independent CP inversion using a finite binomial sum (no scipy/beta.ppf).
def binomial_upper(k,n,p):
    if k==0:return 1.
    if p==0:return 0.
    if p==1:return 1.
    term=math.exp(math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p))
    terms=[term]
    for j in range(k,n):
        term*=((n-j)/(j+1))*(p/(1-p));terms.append(term)
    return math.fsum(terms)
def lower_bound(k,n,alpha):
    if k==0:return 0.
    lo,hi=0.,k/n
    for _ in range(48):
        m=(lo+hi)/2
        if binomial_upper(k,n,m)<alpha:lo=m
        else:hi=m
    return (lo+hi)/2
def chi2_upper(x,df):
    z=x/2
    if df%2:a=.5;q=math.erfc(math.sqrt(z))
    else:a=1.;q=math.exp(-z)
    while a<df/2:
        q+=math.exp(a*math.log(z)-z-math.lgamma(a+1));a+=1
    return q
def homogeneous_power(N,v,j):
    lo,hi=1.,100.
    for _ in range(60):
        m=(lo+hi)/2
        if N*(m-1-math.log(m))<25:lo=m
        else:hi=m
    return chi2_upper(N*((lo+hi)/2)*v/(v+j*j),N-1)

def validate(plan,val):
    req(len(plan['cells'])==len(val['cells'])==27,'27 cells')
    req(plan['draws_per_cell']==20000 and plan['alpha_per_cell']==.05/27 and val['alpha_family']==.05,'Family alpha/draws')
    req(len({c['seed'] for c in plan['cells']})==27,'Duplicate seed')
    for p,c in zip(plan['cells'],val['cells']):
        req(all(c[k]==v for k,v in p.items()),'Cell differs from plan')
        k,n=c['successes'],c['draws'];req(type(k)is int and n==20000 and 0<=k<=n,'Invalid binomial counts')
        req(c['power']==k/n,'Power fraction')
        req(c['meets_90_percent']==(c['simultaneous_lower']>=.9),'Decision flag')
    for s in val['selected']:
        passed=[c['N'] for c in val['cells'] if c['population']==s['population'] and c['sigma_jit']==s['sigma_jit'] and c['meets_90_percent']]
        req(s['N90_validated']==(min(passed) if passed else None),'Selected target')

def main():
    start=time.perf_counter()
    paths=['refeito/e0_route_iv_power_013bis_v2.py','refeito/validate_e0_mc_targets_013bis.py','bis/E0_ROUTE_IV_POWER_v2.json',
        'bis/E0_ROUTE_IV_VALIDATION_PLAN.json','bis/E0_ROUTE_IV_VALIDATION.json','C4_CATALOG_COMBINATION.json','C4_CATALOG_SCHEMA.json',
        'bis/e0_core/DATASET.json','bis/PART_B_BUDGET_START.json','bis/E0_ROUTE_IV_POWER_NOTE.md']
    d,p,v=map(read,paths[2:5]);dataset=read('bis/e0_core/DATASET.json');sel=read('C4_CATALOG_COMBINATION.json')['selected_events']
    req(d['code_sha256']==p['simulation_code_sha256']==sha(B/paths[0]),'Simulation source hash')
    req(p['code_sha256']==sha(B/paths[1]),'Validation source hash')
    req(p['exploration_sha256']==v['source_result_sha256']==sha(B/paths[2]),'Exploration hash')
    req(v['plan_sha256']==sha(B/paths[3]),'Plan hash')
    req(d['budget_sha256']==sha(B/'bis/PART_B_BUDGET_START.json'),'Budget hash')
    req(d['finished_utc']<p['utc']<v['finished_utc'],'Chronology')
    validate(p,v)
    intervals=[]
    for cell in v['cells']:
        independent=lower_bound(cell['successes'],cell['draws'],p['alpha_per_cell'])
        err=abs(independent-cell['simultaneous_lower']);req(err<2e-10,'CP inversion discrepancy')
        intervals.append(dict(population=cell['population'],sigma_jit=cell['sigma_jit'],N=cell['N'],lower_independent=independent,abs_error=err))
    negatives=[]
    for kind in ['alpha','successes','decision','seed']:
        pp,vv=copy.deepcopy(p),copy.deepcopy(v)
        if kind=='alpha':pp['alpha_per_cell']=.05
        elif kind=='successes':vv['cells'][0]['successes']=20001
        elif kind=='decision':vv['cells'][-1]['meets_90_percent']=False
        else:vv['cells'][0]['seed']+=1
        try:validate(pp,vv)
        except ValueError as e:negatives.append(dict(mutation=kind,rejected=True,reason=str(e)))
        else:raise ValueError('Audit guard accepted '+kind)
    rows=d['per_event'];core={r['event']:r for r in dataset['rows'] if r['release']=='GWTC5'}
    req(len(rows)==33 and len({r['event'] for r in rows})==33,'Rows')
    req(len(sel)==len(set(sel))==31 and set(sel)<=set(core),'Current selected set')
    req(set('GWTC5:'+n for n in sel)==set(dataset['sets']['GWTC5_31']),'A selection differs')
    for r in rows:
        a=core[r['event']]
        req(r['N']==a['N'] and r['sha256']==a['source_sha256'],'A input provenance')
        req(r['sigma_df']==a['stddf'] and r['sigma_tau']==a['stdtau'],'A width differs')
        req(math.isfinite(r['sigma_df']) and r['sigma_df']>0,'Invalid actual width')
    anchor=next(r['sigma_df'] for r in rows if r['event']=='GW250114_082203')
    analytic=[]
    for c in v['cells']:
        if c['population']=='GW250114_actual_width':
            analytic.append(dict(N=c['N'],sigma_jit=c['sigma_jit'],exact_power=homogeneous_power(c['N'],anchor*anchor,c['sigma_jit']),power_MC=c['power']))
    for r in d['controls']['homogeneous']:
        req(abs(homogeneous_power(r['N'],anchor*anchor,.0228)-r['analytic_power'])<1e-11,'Analytic source control')
    explored_seeds={t['seed'] for r in d['results'] for t in r['trials']}|{c['seed'] for c in d['controls']['homogeneous']}
    req(not explored_seeds & {c['seed'] for c in p['cells']},'Reused validation seed')
    for i,r in enumerate(d['results']):
        initial=r['targets']['0.9']['at_or_above']['N']
        for j,scale in enumerate([1.,1.10,1.21]):
            cell=p['cells'][3*i+j]
            req(cell['population']==r['population'] and cell['sigma_jit']==r['sigma_jit'] and cell['N']==math.ceil(initial*scale),'Plan reconstruction')

    # Evaluate only pure ll/lrt definitions extracted by AST. No main/import/output path executes.
    tree=ast.parse((B/paths[0]).read_text())
    pure=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['ll','lrt']],type_ignores=[])
    ns={'np':np};exec(compile(pure,'audited_pure_definitions','exec',optimize=1),ns)
    data=[np.array([-.1,.2,.05]),np.array([]),np.array([.5,-.3])];variances=np.array([.01,.04,.1])
    n=np.array([[len(a) for a in data]]);s=np.array([[sum(a) for a in data]]);ss=np.array([[sum(a*a) for a in data]])
    yy=np.concatenate(data);vv=np.repeat(variances,n[0])
    def direct(q):
        w=1/(vv+q);mu=sum(w*yy)/sum(w)
        return -.5*sum(np.log(vv+q)+(yy-mu)**2/(vv+q))
    diffs=[abs(float(ns['ll'](q,n,s,ss,variances)[0])-direct(q)) for q in [0,.01,.2]]
    req(max(diffs)<1e-12,'Expanded Gaussian likelihood')
    grid=np.r_[0,np.geomspace(1e-9,10,1500)]
    j=max(range(len(grid)),key=lambda j:direct(grid[j]));lo=grid[max(j-1,0)];hi=grid[min(j+1,len(grid)-1)]
    golden=(math.sqrt(5)-1)/2
    for _ in range(90):
        a=hi-golden*(hi-lo);bb=lo+golden*(hi-lo)
        if direct(a)>direct(bb):hi=bb
        else:lo=a
    independent_lrt=max(0,2*(max(direct(0),direct((lo+hi)/2))-direct(0)))
    actual=float(ns['lrt'](n,s,ss,variances)[0][0]);req(abs(actual-independent_lrt)<1e-9,'Profile maximizer')
    shift=1.7;shifted=float(ns['lrt'](n,s+shift*n,ss+2*shift*s+shift*shift*n,variances)[0][0])
    req(abs(shifted-actual)<1e-9,'Free common mean translation')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        bad=ns['lrt'](np.array([[10]]),np.array([[0.]]),np.array([[float('nan')]]),np.array([.01]))[0]
    # Isolate an actual missing-selection guard: same list size, one unknown member.
    mutated=sel[:-1]+['UNKNOWN_EVENT'];bad_population=[r for r in rows if r['event'] in mutated]
    guard_accepts=(len(mutated)==31 and len(rows)==33)
    manifest={p:sha(B/p) for p in paths}
    out=dict(status='ARITHMETIC_AND_SCENARIO_CHECKS_PASS_WITH_PROVENANCE_GUARD_FINDING',utc=datetime.now(timezone.utc).isoformat(),
        source_hashes=manifest,code_sha256=sha(Path(__file__)),threads=1,full_MC_rerun=False,new_PE=False,HDF5_opened=False,
        CP_independent=intervals,CP_max_error=max(r['abs_error'] for r in intervals),own_audit_negatives=negatives,
        homogeneous_analytic=analytic,selection_width_crosscheck_A=dict(rows=33,df_tau_equal=66,selected31_equal=True,A_status='Independent existing dataset read, not recomputed here'),
        algebra=dict(direct_observation_ll_max_error=max(diffs),profile_lrt=actual,independent_lrt=independent_lrt,mean_shift_error=abs(shifted-actual),zero_count_class_included=True),
        production_negatives=dict(unknown_selection_same_length_guard_accepts=guard_accepts,actual_population_size_after_filter=len(bad_population),
            nan_lrt_raises=False,nan_lrt_result_nonfinite=bool(np.any(~np.isfinite(bad))),nan_comparison_counted_as_success=bool(np.any(bad>25))),
        validation_selected=v['selected'],failed_cells=[c for c in v['cells'] if not c['meets_90_percent']],
        chronology=dict(exploration_finished=d['finished_utc'],plan=p['utc'],validation_finished=v['finished_utc'],
            strength='Consistent file contents, hashes, source order and mtimes; local record, not trusted external timestamp'),
        elapsed_s=time.perf_counter()-start)
    target=Path(__file__).with_name('e0_mc_independent_results.json')
    with target.open('xb') as f:f.write((json.dumps(out,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps({k:out[k] for k in ['status','CP_max_error','algebra','production_negatives','elapsed_s']}))
if __name__=='__main__':main()
