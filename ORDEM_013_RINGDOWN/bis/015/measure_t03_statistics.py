"""Light-stage T03 calibration diagnostics using only already published posteriors."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,resource,time
import numpy as np,h5py
from scipy.stats import kurtosis
B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03/statistics_001'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def save(p,obj):
    with p.open('xb') as f:f.write((json.dumps(obj,indent=2,allow_nan=False)+'\n').encode())
def excess(a):
    a=np.asarray(a,float)
    if len(a)<4 or not np.isfinite(a).all() or np.var(a)==0:raise ValueError('Insufficient finite kurtosis data')
    return float(kurtosis(a,fisher=True,bias=False))
def main():
    resource.setrlimit(resource.RLIMIT_CPU,(899,900));resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
    wall=time.perf_counter();cpu=time.process_time();D.mkdir(exist_ok=False)
    dp=B/'bis/e0_core/DATASET.json';npth=B/'bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json'
    data=json.loads(dp.read_bytes());nu=json.loads(npth.read_bytes());lookup={r['product_id']:r for r in data['rows']}
    seed=15260310;draws=2000
    inputs=dict(status='NONBLIND_DIAGNOSTIC_DESIGN_FROZEN_BEFORE_BOOTSTRAP',at=datetime.now(timezone.utc).isoformat(),
        inputs={str(p.relative_to(ROOT)):sha(p) for p in (dp,npth)},seed=seed,bootstrap_draws=draws,
        bootstrap_unit='31 events with replacement, same indices for each reading; never posterior draws as independent events',
        bootstrap_estimator='WLS of event posterior means against [1,posterior std]; weights inverse posterior variance; DIAGNOSTIC, not a KDE-covariance replacement',
        kurtosis='Unbiased Fisher excess; stored equal-weight full marginal dtau posterior per published event',
        residuals='Across events: posterior mean minus mean prediction minus KDE fitted c0+k*sigma, at bandwidth1, sigma covariate',
        scale_hypothesis='INPUT: elliptical t5 has one shared measurement scale per synthetic catalog; independent scales are a different model',
        expected_total_samples=sum(v['N'] for v in nu['events'].values()))
    save(D/'INPUTS.json',inputs);events=[]
    for pid,item in nu['events'].items():
        row=lookup[pid];p=(ROOT/row['source_path']).resolve()
        if not p.is_relative_to((B/'cache/public').resolve()):raise ValueError('Only public calibration archive paths allowed')
        pin=sha(p)
        if pin!=row['source_sha256'] or pin!=item['source_sha256']:raise ValueError('Published posterior changed')
        with h5py.File(p,'r') as f:
            ds=f[row['dataset']]
            if any('weight' in x.lower() for x in ds.dtype.names):raise ValueError('Weighted posterior requires separate estimator')
            values=np.asarray(ds.fields(row['field_mapping']['dtau'])[:],float)
        if len(values)!=item['N'] or not np.isfinite(values).all():raise ValueError('Sample count/finiteness changed')
        if not np.isclose(np.std(values,ddof=1),item['sigma_dtau_ddof1'],rtol=1e-12,atol=1e-14):raise ValueError('Published marginal differs')
        k=excess(values);center=values-values.mean();m2=float(np.mean(center**2));m4=float(np.mean(center**4));n=len(values)
        independent=((n-1)/((n-2)*(n-3)))*((n+1)*(m4/m2**2-3)+6)
        if not np.isclose(k,independent,rtol=1e-10,atol=1e-10):raise ValueError('Independent kurtosis formula disagrees')
        events.append(dict(product_id=pid,event=item['event'],N=n,source_sha256=pin,excess_kurtosis=k,
            caveat='Bounded posterior, correlated MCMC draws with unknown ESS; no frequentist tail or physical p inferred'))
    assert sum(x['N'] for x in events)==inputs['expected_total_samples']
    residuals=[];o4b=[]
    for fit in nu['fits']:
        if fit['covariate']!='sigma' or fit['bandwidth_factor']!=1.0:continue
        if fit['group'] not in ('GWTC5_31','GWTC5_33'):
            if fit['result'].get('n')==14:o4b.append(dict(group=fit['group'],reading=fit['reading'],c0=fit['result']['c0'],stderr_c0=fit['result']['stderr'][0],n=14))
            continue
        ids=fit['product_ids'];r=fit['result'];values=[]
        for pid in ids:
            e=nu['events'][pid];delta=e['predictions'][fit['reading']]['mean']
            values.append(e['mean_dtau']-delta-r['c0']-r['k']*e['sigma_dtau_ddof1'])
        residuals.append(dict(group=fit['group'],reading=fit['reading'],n=len(values),excess_kurtosis=excess(values),
            gaussian_large_n_SE_illustration=float(np.sqrt(24/len(values))),
            SE_scope='Asymptotic Gaussian independent-event illustration, not a calibrated error after nuisance fitting',
            residual_definition=inputs['residuals']))
    ids=data['sets']['GWTC5_31'];assert len(ids)==31 and len({nu['events'][pid]['event'] for pid in ids})==31
    sigma=np.array([nu['events'][pid]['sigma_dtau_ddof1'] for pid in ids]);X=np.column_stack([np.ones(31),sigma]);weights=1/sigma**2
    readings=[f['reading'] for f in nu['fits'] if f['group']=='GWTC5_31' and f['bandwidth_factor']==1.0 and f['covariate']=='sigma']
    assert len(readings)==len(set(readings))
    y=np.array([[nu['events'][pid]['mean_dtau']-nu['events'][pid]['predictions'][rd]['mean'] for rd in readings] for pid in ids])
    rng=np.random.default_rng(seed);coeff=[]
    for _ in range(draws):
        index=rng.integers(0,len(ids),size=len(ids));xx=X[index];ww=weights[index];yy=y[index]
        if np.linalg.matrix_rank(xx)<2:raise ValueError('Bootstrap rank failure, no silent rejection of draw')
        coeff.append(np.linalg.solve(xx.T@(ww[:,None]*xx),xx.T@(ww[:,None]*yy)))
    coeff=np.asarray(coeff);bootstrap=[]
    for j,rd in enumerate(readings):
        boot=coeff[:,:,j];bootstrap.append(dict(reading=rd,draws=draws,event_count=31,
            coefficient_mean=boot.mean(axis=0).tolist(),covariance=np.cov(boot,rowvar=False,ddof=1).tolist(),
            coefficient_quantiles_025_50_975=np.quantile(boot,[.025,.5,.975],axis=0).tolist(),
            scope='EVENT_BOOTSTRAP_WLS_DIAGNOSTIC_NOT_KDE_CURVATURE_OR_PHYSICAL_SYSTEMATICS'))
    result=dict(status='T03_NONBLIND_MOMENTS_AND_EVENT_BOOTSTRAP_MEASURED',input_manifest_sha256=sha(D/'INPUTS.json'),events=events,
        total_published_samples=sum(x['N'] for x in events),between_event_residuals=residuals,bootstrap=bootstrap,
        O4b_only_bandwidth1=o4b,groups_in_nuisance=sorted(set(f['group'] for f in nu['fits'])),
        sigma_sys_calibrated=False,physical_p_emitted=False,draws_per_event_as_independent=False,
        wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,heavy_machine_hours=0,
        source_sha256=sha(Path(__file__)))
    save(D/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','total_published_samples','wall_seconds','cpu_seconds','physical_p_emitted')}|{'events':len(events),'bootstrap_readings':len(bootstrap),'O4b_rows':len(o4b)}))
if __name__=='__main__':main()
