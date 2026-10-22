"""T06 archived population-width diagnostic, never a calibrated hypothesis test."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,math
import numpy as np
from scipy.special import logsumexp
from scipy.optimize import minimize_scalar,brentq
from scipy.stats import chi2
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t06'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
    raw=(json.dumps(x,indent=2,allow_nan=False)+'\n').encode();t=p.with_name(p.name+'.pending');assert not p.exists()
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;os.link(t,p);t.unlink()
def main():
    wall=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    p=B/'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json';receipt=json.loads((B/'bis/E7_FINAL_EXECUTION_V1.json').read_bytes());assert sha(p)==receipt['products'][p.name]['sha256']
    payload=json.loads(p.read_bytes());events=payload['events'];assert len(events)==33 and all(e['role']=='calibration' for e in events)
    data=[np.asarray(e['samples']['df220'],float) for e in events];means=np.array([x.mean() for x in data]);sd=np.array([x.std(ddof=1) for x in data]);h=sd*np.array([len(x)**(-.2) for x in data]);var=sd**2
    assert all(np.isfinite(x).all() for x in data) and np.all(sd>0)
    # Posterior-as-likelihood only on the archived uniform deformation-prior support.
    prior_contract=[]
    for e in events:
        prior_contract.append(dict(event=e['event_id'],df220_prior=e['priors'].get('df220')))
    mu_grid=np.linspace(float(means.min()-2*sd.min()),float(means.max()+2*sd.min()),81)
    def compress(bins):
        nodes=np.zeros((33,bins));weights=np.zeros_like(nodes)
        for i,x in enumerate(data):
            count,edges=np.histogram(x,bins=bins);inds=np.minimum(np.searchsorted(edges,x,side='right')-1,bins-1);sums=np.bincount(inds,weights=x,minlength=bins)
            nodes[i]=np.divide(sums,count,out=(edges[:-1]+edges[1:])/2,where=count>0);weights[i]=count/len(x)
        with np.errstate(divide='ignore'):lw=np.log(weights)
        return nodes,lw
    nodes,lw=compress(512)
    def llvec(mu,sigma,kind='kde',resolution=None):
        if time.process_time()-cpu>850:raise TimeoutError('T06 light command CPU ceiling reached before900s')
        if kind=='gaussian':return -.5*((means-mu)**2/(var+sigma*sigma)+np.log(2*np.pi*(var+sigma*sigma)))
        nn,ww=(nodes,lw) if resolution is None else resolution
        vv=h*h+sigma*sigma
        return logsumexp(ww-(nn-mu)**2/(2*vv[:,None]),axis=1)-.5*np.log(2*np.pi*vv)
    def profile(sigma,kind,keep,resolution=None):
        if kind=='gaussian':
            vv=var[keep]+sigma*sigma;mu=float(np.sum(means[keep]/vv)/np.sum(1/vv));return float(llvec(mu,sigma,kind)[keep].sum()),mu
        vals=np.array([llvec(m,sigma,kind,resolution)[keep].sum() for m in mu_grid]);best=int(vals.argmax());lo=mu_grid[max(0,best-1)];hi=mu_grid[min(len(mu_grid)-1,best+1)]
        assert 0<best<len(mu_grid)-1,'Mean scan boundary'
        opt=minimize_scalar(lambda m:-float(llvec(m,sigma,kind,resolution)[keep].sum()),bounds=(lo,hi),method='bounded',options={'xatol':1e-9})
        assert opt.success;return -float(opt.fun),float(opt.x)
    sig_grid=np.r_[0,np.geomspace(1e-5,.5,49),1.]
    def fit(kind,keep,resolution=None,curve=False):
        scanned=[profile(float(s),kind,keep,resolution) for s in sig_grid];v=np.array([x[0] for x in scanned]);i=int(v.argmax());assert i<len(sig_grid)-1,'Width scan boundary'
        opt=minimize_scalar(lambda s:-profile(s,kind,keep,resolution)[0],bounds=(sig_grid[max(0,i-1)],sig_grid[i+1]),method='bounded',options={'xatol':1e-8});assert opt.success
        sigma=float(opt.x);peak,mu=profile(sigma,kind,keep,resolution)
        if v[0]>=peak:sigma=0.;peak,mu=scanned[0]
        threshold=float(chi2.ppf(.9,1));root=brentq(lambda s:2*(peak-profile(s,kind,keep,resolution)[0])-threshold,max(sigma,1e-9),1.,xtol=1e-8)
        out=dict(LRT=max(0.,2*(peak-v[0])),sigma_pop_MLE=sigma,mu_MLE=mu,mu_null=scanned[0][1],sigma_upper_nominal_profile90=root,
            level=threshold,limit_scope='Nominal profile-likelihood level only; boundary, posterior smoothing and selection not coverage-calibrated. Not physical jitter bound.')
        if curve:out['profile_grid']=[dict(sigma=float(s),logL_relative=float(a-peak),mu=float(b)) for s,(a,b) in zip(sig_grid,scanned)]
        return out
    keep=np.arange(33);results={kind:fit(kind,keep,curve=True) for kind in ['gaussian','kde']};print('FITS',json.dumps({k:{n:v for n,v in x.items() if n!='profile_grid'} for k,x in results.items()}),flush=True)
    finer=compress(2048);fine=fit('kde',keep,resolution=finer);assert abs(fine['LRT']-results['kde']['LRT'])<.01 and abs(fine['sigma_upper_nominal_profile90']-results['kde']['sigma_upper_nominal_profile90'])<1e-4
    # Full uncompressed mixture checks at fitted null/maximum/upper limit.
    exact=[]
    for s in [0.,results['kde']['sigma_pop_MLE'],results['kde']['sigma_upper_nominal_profile90']]:
        approx,mu=profile(s,'kde',keep);val=0.
        for x,hh in zip(data,h):
            v=hh*hh+s*s;val+=float(logsumexp(-(x-mu)**2/(2*v))-math.log(len(x))-.5*math.log(2*np.pi*v))
        exact.append(dict(sigma=s,mu=mu,logL_compression_error=approx-val));assert abs(approx-val)<.01
    jack=[]
    for i,e in enumerate(events):
        k=np.delete(keep,i);jack.append(dict(omitted=e['event_id'],gaussian=fit('gaussian',k),kde=fit('kde',k)))
    weights=sd**-4;weights/=weights.sum();jump=[]
    for e,x,m,s,w in zip(events,data,means,sd,weights):jump.append(dict(event=e['event_id'],N=len(x),mean=float(m),sd=float(s),information_weight_sigma_minus4=float(w),posterior_fraction_abs_df_gt_3sigma=float(np.mean(np.abs(x)>3*s)),center_abs_df_gt_3sigma=bool(abs(m)>3*s)))
    r=dict(status='T06_NONBLIND_PROFILE_DIAGNOSTIC_NOT_PHYSICAL_TEST',at=datetime.now(timezone.utc).isoformat(),results=results,jackknife=jack,per_event=jump,
        empirical_method='Event KDE with Scott bandwidth sd*N^(-1/5); integrate against Normal(mu,sigma_pop). Histogram-centroid compression512 checked against2048 and exact full-sample mixture. Mean profiled; sigma>=0.',
        Gaussian_method='Registered heteroscedastic Gaussian profile with full posterior mean/sd, free common mean; information weights proportional1/sigma_i^4 reported but never exponentiate event likelihoods.',
        prior_contract=prior_contract,prior_scope='Marginal posterior used as measurement-likelihood proxy under its archived uniform deviation prior, after other parameters marginalized under release priors. Not a full selection-corrected hierarchical likelihood.',
        resolution_control=fine,exact_mixture_controls=exact,archived_00243_comparison={k:dict(nominal_profile90=v['sigma_upper_nominal_profile90'],difference_from_declared_00243=v['sigma_upper_nominal_profile90']-.0243) for k,v in results.items()},
        observed_center_jump_fraction=float(np.mean([r['center_abs_df_gt_3sigma'] for r in jump])),posterior_mean_jump_fraction=float(np.mean([r['posterior_fraction_abs_df_gt_3sigma'] for r in jump])),
        physical_sigma_jitter=None,physical_p=None,significance=None,calibrated_coverage=False,scientific_reading_selected=False,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,heavy_machine_hours=0,seed_read=False,gate_changed=False,
        sources_sha256={str(p.relative_to(B)):sha(p),'bis/E7_FINAL_EXECUTION_V1.json':sha(B/'bis/E7_FINAL_EXECUTION_V1.json')},script_sha256=sha(Path(__file__)))
    put(D/'RESULT.json',r);print(json.dumps(dict(status=r['status'],cpu_seconds=r['cpu_seconds'],wall_seconds=r['wall_seconds'],jackknife=len(jack))))
if __name__=='__main__':main()
