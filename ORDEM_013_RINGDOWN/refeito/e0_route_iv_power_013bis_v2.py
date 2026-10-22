"""Nonblind Gaussian-population lower-bound power, using released measurement widths."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,argparse,math
import numpy as np,h5py
from scipy.optimize import minimize_scalar,brentq
from scipy.stats import chi2
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
def budget():
    d=json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes())
    if datetime.now(timezone.utc)>=datetime.fromisoformat(d['hard_deadline_utc']):raise RuntimeError('40h deadline reached')
    return d
def widths():
    schema=json.loads((B/'C4_CATALOG_SCHEMA.json').read_bytes());rows=[]
    for r in schema['rows']:
        p=B/'cache/public/21454847/extracted/pSEOB/metafiles'/r['filename']
        if sha(p)!=r['sha256']:raise ValueError('Input changed '+r['event'])
        with h5py.File(p,'r') as h:
            s=h[r['label']+'/posterior_samples'][()]
            x=s['domega220'];y=s['dtau220']
        if not np.isfinite(x).all() or len(x)<2:raise ValueError('Invalid data')
        rows.append(dict(event=r['event'],N=len(x),sigma_df=float(np.std(x,ddof=1)),sigma_tau=float(np.std(y,ddof=1)),mean_df=float(np.mean(x)),median_df=float(np.median(x)),sha256=r['sha256']))
    selected=json.loads((B/'C4_CATALOG_COMBINATION.json').read_bytes())['selected_events']
    if len(selected)!=31 or len(rows)!=33:raise ValueError('Unexpected coverage')
    return rows,selected
def sufficient(N,variances,jitter,draws,seed):
    rng=np.random.default_rng(seed);K=len(variances)
    counts=rng.multinomial(N,np.full(K,1/K),size=draws)
    total=np.asarray(variances)[None,:]+jitter*jitter
    sy=rng.normal(size=counts.shape)*np.sqrt(counts*total)
    # Conditional centered sums of squares are independent chi-square(n-1).
    df=np.maximum(counts-1,1)
    centered=rng.chisquare(df)*total*(counts>1)
    sq=centered+np.divide(sy*sy,counts,out=np.zeros_like(sy),where=counts>0)
    return counts,sy,sq
def ll(q,n,s,ss,v,free_mean=True):
    q=np.asarray(q)
    if q.ndim==0:q=np.full(len(n),q)
    w=v[None,:]+q[:,None]
    quad=np.sum(ss/w,axis=1)
    if free_mean:
        quad-=np.sum(s/w,axis=1)**2/np.sum(n/w,axis=1)
    return -.5*(np.sum(n*np.log(w),axis=1)+quad)
def lrt(n,s,ss,v,free_mean=True):
    if len(v)==1:
        N=n[:,0];rss=ss[:,0]-(s[:,0]**2/N if free_mean else 0)
        ratio=rss/(N*v[0]);ratio=np.maximum(ratio,1.)
        return N*(ratio-1-np.log(ratio)),np.maximum(0,rss/N-v[0])
    hi=max(1.,10*float(np.max(ss.sum(axis=1)/n.sum(axis=1))))
    grid=np.r_[0,np.geomspace(float(min(v))*1e-7,hi,81)]
    values=np.stack([ll(q,n,s,ss,v,free_mean) for q in grid],axis=1)
    ids=np.argmax(values,axis=1)
    if np.any(ids==len(grid)-1):raise ValueError('Variance search boundary')
    low=grid[np.maximum(ids-1,0)];high=grid[np.minimum(ids+1,len(grid)-1)]
    for _ in range(34):
        a=low+(high-low)/3;b=high-(high-low)/3
        choose=ll(a,n,s,ss,v,free_mean)>ll(b,n,s,ss,v,free_mean)
        high=np.where(choose,b,high);low=np.where(choose,low,a)
    q=(low+high)/2;value=ll(q,n,s,ss,v,free_mean);null=values[:,0]
    q=np.where(value>null,q,0.)
    return np.maximum(0,2*(value-null)),q
def wilson(k,n):
    z=1.959963984540054;p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [c-h,c+h]
def power(N,sig,jit,draws,seed):
    n,s,ss=sufficient(N,sig*sig,jit,draws,seed+N)
    t,q=lrt(n,s,ss,sig*sig)
    count=int(np.sum(t>25.))
    return dict(N=N,power=count/draws,successes=count,draws=draws,binomial_95=wilson(count,draws),seed=seed+N)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draws',type=int,default=4000);parser.add_argument('--smoke',action='store_true');args=parser.parse_args()
    started=time.perf_counter();stamp=datetime.now(timezone.utc).isoformat();bud=budget()
    target=B/('bis/E0_ROUTE_IV_SMOKE_v2.json' if args.smoke else 'bis/E0_ROUTE_IV_POWER_v2.json')
    if target.exists():raise FileExistsError(target)
    rows,selected=widths();anchor=next(r for r in rows if r['event']=='GW250114_082203')['sigma_df']
    pops={'GW250114_actual_width':np.array([anchor]),'GWTC5_31_quality_mixture':np.array([r['sigma_df'] for r in rows if r['event'] in selected]),'GWTC5_33_quality_mixture':np.array([r['sigma_df'] for r in rows])}
    # Independent direct scalar optimization checks of grouped sufficient statistics.
    sig=pops['GWTC5_31_quality_mixture'];n,s,ss=sufficient(38,sig*sig,.0228,16,13220901);t,q=lrt(n,s,ss,sig*sig);errors=[]
    for i in range(len(n)):
        f=lambda x:-float(ll(x,n[i:i+1],s[i:i+1],ss[i:i+1],sig*sig)[0])
        opt=minimize_scalar(f,bounds=(0,.1),method='bounded',options={'xatol':1e-12})
        best=min(f(0),opt.fun);errors.append(abs(t[i]-max(0,2*(f(0)-best))))
    if max(errors)>1e-5:raise ValueError('Variance optimizer disagreement')
    # Exact homogeneous null/alternative analytic tail checks use the same free-mean estimator.
    controls=[]
    for N in [20,38,59]:
        ratio=brentq(lambda x:N*(x-1-math.log(x))-25,1.000001,100.)
        expected=float(chi2.sf(N*ratio*anchor**2/(anchor**2+.0228**2),N-1))
        measured=power(N,np.array([anchor]),.0228,max(4000,args.draws),13220902)
        se=math.sqrt(expected*(1-expected)/measured['draws'])
        if abs(measured['power']-expected)>5*se+.002:raise ValueError('Homogeneous MC control failed')
        controls.append(dict(**measured,analytic_power=expected))
    results=[]
    for pi,(name,sig) in enumerate(pops.items()):
        for ji,jitter in enumerate([.019,.0228,.030]):
            seed=13221000+1000*pi+100*ji;trials={}
            def evaluate(N):
                budget()
                if N not in trials:trials[N]=power(N,sig,jitter,args.draws,seed)
                return trials[N]
            if args.smoke:
                evaluate(38);evaluate(100)
                result=dict(population=name,sigma_jit=jitter,smoke_only=True,trials=list(trials.values()))
            else:
                endpoints={}
                for goal in [.5,.9]:
                    lo,hi=2,16
                    while (evaluate(hi)['binomial_95'][0] if goal==.9 else evaluate(hi)['power'])<goal:
                        lo=hi;hi*=2
                        if hi>2000000:raise ValueError('Power target beyond declared search ceiling')
                    while hi-lo>max(1,int(.005*hi)):
                        mid=(lo+hi)//2
                        if (evaluate(mid)['binomial_95'][0] if goal==.9 else evaluate(mid)['power'])>=goal:hi=mid
                        else:lo=mid
                    endpoints[str(goal)]=dict(below=evaluate(lo),at_or_above=evaluate(hi),meaning='Monte Carlo bracket, not exact minimal integer; N50 uses point power, N90 requires Wilson95 lower bound >=0.90; uncertainty and mean profiling make it differ from simple reference counts')
                result=dict(population=name,sigma_jit=jitter,targets=endpoints,trials=sorted(trials.values(),key=lambda x:x['N']))
            results.append(result);print(json.dumps({k:v for k,v in result.items() if k!='trials'}),flush=True)
    equivalent={name:float(np.sum((anchor/sig)**4)) for name,sig in pops.items()}
    out=dict(status='NONBLIND_GAUSSIAN_POPULATION_POWER_LOWER_BOUND__NOT_CALIBRATED_5SIGMA',started_utc=stamp,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.perf_counter()-started,code_sha256=sha(Path(__file__)),budget_sha256=sha(B/'bis/PART_B_BUDGET_START.json'),sigma_convention='Full existing posterior standard deviation ddof=1; proxy measurement Gaussian variance only for this prospective calculation',statistic='Profile Gaussian heteroscedastic log-likelihood ratio, intrinsic variance >=0, common mean profiled under both hypotheses',threshold=25.,population_sampling='Prospective multinomial mixture of released measurement widths, equal event-class probabilities; grouped exact Gaussian sufficient-statistic simulation',selection_warning='Widths define calibration scenarios only; no posterior-width selection of test events',sigma_sys_assumed=0.,lower_bound_until_transfer_and_systematics=True,per_event=rows,information_df_fourth_power_equivalents=equivalent,controls=dict(max_scalar_optimization_error=max(errors),homogeneous=controls),results=results,not_done=['Physical jitter transfer into IMR estimator','Two-family delta-f systematic floor','5sigma null-tail calibration; E2 separate','Full-posterior population inference; E5 separate'])
    new(target,out);print('SAVED',target,sha(target),'seconds',out['elapsed_seconds'])
if __name__=='__main__':main()
