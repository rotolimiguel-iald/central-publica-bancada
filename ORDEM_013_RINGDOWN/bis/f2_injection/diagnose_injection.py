"""Independent bounded posterior diagnostics. No PE, strain or production imports.

Equal-weight posterior rows are treated as the released empirical measure, not
independent repeated injections. KDE contours describe that posterior only.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import hashlib, json, math, time, platform, re
import h5py
import numpy as np
import scipy
from scipy.stats import gaussian_kde

OUT=Path(__file__).resolve().parent
B=OUT.parents[1]
START=time.perf_counter()
SEED=1302212026
FIELDS=['domega220','dtau220','domega440','dtau440','final_spin_non_evolved',
        'final_mass_non_evolved','redshift','network_optimal_snr']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()
def new(name,obj):
    p=OUT/name
    if p.exists(): raise FileExistsError(p)
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw
    t.replace(p)
def shortest_interval(x,level):
    s=np.sort(x); width=int(math.ceil(level*len(s)))-1
    i=int(np.argmin(s[width:]-s[:len(s)-width]))
    return [float(s[i]),float(s[i+width])]
def summary(x):
    assert x.ndim==1 and np.all(np.isfinite(x))
    q=np.quantile(x,[.005,.025,.05,.25,.5,.75,.95,.975,.995],method='linear')
    central={}
    shortest={}
    for level in [.5,.9,.95,.99]:
        a,b=np.quantile(x,[(1-level)/2,(1+level)/2],method='linear')
        central[str(level)]={'interval':[float(a),float(b)],'contains_zero':bool(a<=0<=b)}
        a,b=shortest_interval(x,level)
        shortest[str(level)]={'interval':[a,b],'contains_zero':bool(a<=0<=b)}
    return {'n':len(x),'mean':float(np.mean(x)),'sd_ddof1':float(np.std(x,ddof=1)),
            'median':float(q[4]),'quantile_probabilities':[.005,.025,.05,.25,.5,.75,.95,.975,.995],
            'quantiles':q.tolist(),'min':float(np.min(x)),'max':float(np.max(x)),
            'n_positive':int(np.sum(x>0)),'n_zero':int(np.sum(x==0)),
            'p_positive':float(np.mean(x>0)),'cdf_at_zero':float(np.mean(x<=0)),
            'central_intervals':central,'shortest_contiguous_intervals':shortest}
def prior_bounds(text):
    # Parse literal numbers only; never evaluate archived prior expressions.
    assert text.startswith('Uniform(') and 'condition' not in text.lower()
    return [float(re.search(r'\b'+key+r'=([-+\d.eE]+)',text)[1]) for key in ['minimum','maximum']]
def hpd_content(data):
    # Single deterministic split; no fit on held-out query points. 64M kernel
    # terms/bandwidth, in batches of 256; two datasets and three bandwidths.
    rng=np.random.default_rng(SEED)
    perm=rng.permutation(data.shape[1]); train=perm[:16000]; test=perm[16000:]
    out=[]
    for mult in [.7,1.,1.4]:
        kde=gaussian_kde(data[:,train],bw_method=lambda k:k.scotts_factor()*mult)
        log0=float(kde.logpdf(np.zeros(2))[0]); count=0
        for start in range(0,len(test),256):
            logq=kde.logpdf(data[:,test[start:start+256]])
            count+=int(np.sum(logq>=log0))
        content=count/len(test)
        full=gaussian_kde(data,bw_method=lambda k:k.scotts_factor()*mult)
        d2=np.einsum('in,ij,jn->n',data,full.inv_cov,data)
        weights=np.exp(-d2/2)
        out.append({'bandwidth_multiplier':mult,'train_n':len(train),'query_n':len(test),
            'train_scott_factor':kde.factor,'content_at_GR':content,
            'inside_joint_90':content<=.9,'inside_joint_95':content<=.95,
            'query_binomial_scale_if_iid_only':math.sqrt(content*(1-content)/len(test)),
            'full_sample_log_density_at_GR':float(full.logpdf([0.,0.])[0]),
            'kernel_weight_effective_count_not_chain_ESS':float(weights.sum()**2/(weights@weights)),
            'rows_within_two_kernel_sd':int(np.sum(d2<=4))})
    return out

meta=json.loads((OUT/'METADATA.json').read_bytes())
src=B/meta['source']; source_hash=sha(src)
assert source_hash==meta['sha256']
schema=json.loads((B/'bis/F2_CONTROL_SCHEMAS.json').read_bytes())
assert next(x for x in schema if x['path'].replace('\\','/')==meta['source'])['sha256']==source_hash
receipt=json.loads((B/'bis/F2_CONTROL_EXTRACTION.json').read_bytes())
matches=[x for a in receipt['archives'] for x in a['files'] if x.get('path','').replace('\\','/')==meta['source']]
# Receipts may use an extraction-path key; preserve explicit match status.
result={'status':'NONBLIND_DESCRIPTIVE_PUBLIC_POSTERIOR_DIAGNOSTIC__AWAITING_OTHER_AGENT_REVIEW',
 'source':meta['source'],'source_sha256':source_hash,'extraction_path_matches':matches,
 'seed':SEED,'weighting':'equal weight released posterior rows; no weight column; chain ESS unknown',
 'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'h5py':h5py.__version__,'threads':1},'groups':{},'source_field_sha256':{},
 'method':{'quantiles':'numpy linear','sd':'ddof=1','shortest_interval':'shortest single contiguous sample interval, not multimodal HPD',
 'joint_hpd':'posterior mass above estimated density at (0,0), 16000 training and 4000 held-out rows, one fixed split',
 'hpd_warning':'bandwidth and finite-sample diagnostic, not a calibrated coverage probability or significance',
 'coverage':'membership of the GR reference in this posterior, not repeated-injection frequentist coverage'}}
prior_comparison={}
with h5py.File(src,'r') as f:
    for label in ['NR_with_44','NR_without_44']:
        g=f[label]; ds=g['posterior_samples']
        assert ds.shape==(20000,)
        assert not any('weight' in x.lower() for x in ds.dtype.names)
        a=ds.fields(FIELDS)[:]
        assert all(np.all(np.isfinite(a[k])) for k in FIELDS)
        result['source_field_sha256'][label]={k:hashlib.sha256(np.asarray(a[k],dtype='<f8').tobytes()).hexdigest() for k in FIELDS}
        stats={k:summary(a[k]) for k in FIELDS}
        data=np.vstack([a['domega220'],a['dtau220']])
        prior={}; ps=[]
        for field in ['domega220','dtau220','domega440','dtau440']:
            txt=g['priors/analytic/'+field][0].decode()
            lo,hi=prior_bounds(txt); v=a[field]
            assert np.all((v>=lo)&(v<=hi))
            pv=g['priors/samples/'+field][:]
            assert np.all(np.isfinite(pv)) and np.all((pv>=lo)&(pv<=hi))
            prior[field]={'analytic':txt,'bounds':[lo,hi],'density':1/(hi-lo),
                'analytic_p_positive':hi/(hi-lo),'posterior_minus_prior_p_positive':float(np.mean(v>0)-hi/(hi-lo)),
                'prior_samples_n':len(pv),'sample_p_positive':float(np.mean(pv>0)),
                'posterior_within_1percent_prior_width_lower':float(np.mean(v<lo+.01*(hi-lo))),
                'posterior_within_1percent_prior_width_upper':float(np.mean(v>hi-.01*(hi-lo)))}
            ps.append(pv)
        prior_comparison[label]=meta['groups'][label]['priors_analytic']
        finite_truth={k:float(g['injection_data'][0][k]) for k in g['injection_data'].dtype.names
                      if np.isfinite(g['injection_data'][0][k])}
        result['groups'][label]={'summaries':stats,'prior_diagnostics':prior,
            'posterior_correlation_220':float(np.corrcoef(data)[0,1]),
            'prior_sample_correlation_4fields':np.corrcoef(ps).tolist(),
            'posterior_quadrants_220':{f'df_{sx}_dtau_{sy}':int(np.sum((data[0]>0 if sx=='positive' else data[0]<=0)&(data[1]>0 if sy=='positive' else data[1]<=0)))/data.shape[1]
                for sx in ['positive','nonpositive'] for sy in ['positive','nonpositive']},
            'posterior_joint_unique_rows_220':int(len(np.unique(data.T,axis=0))),
            'truth_finite_fields':finite_truth,'hpd_GR_220':hpd_content(data)}
        print(json.dumps({'group':label,'summary':{k:{z:stats[k][z] for z in ['median','p_positive','central_intervals']} for k in ['domega220','dtau220']},
            'hpd':result['groups'][label]['hpd_GR_220']}),flush=True)
result['analytic_prior_dictionaries_identical']=prior_comparison['NR_with_44']==prior_comparison['NR_without_44']
result['differences_with_minus_without']={}
for k in FIELDS:
    s1=result['groups']['NR_with_44']['summaries'][k];s0=result['groups']['NR_without_44']['summaries'][k]
    result['differences_with_minus_without'][k]={'median_difference':s1['median']-s0['median'],
      'mean_difference':s1['mean']-s0['mean'],'p_positive_difference':s1['p_positive']-s0['p_positive'],
      'sd_ratio':s1['sd_ddof1']/s0['sd_ddof1'],
      'warning':'difference between two posterior summaries; not paired samples, not significance of an injection bias'}
assert sha(src)==source_hash
result['source_unchanged_after']=True
result['elapsed_s']=time.perf_counter()-START
result['dependencies_sha256']={str(p.relative_to(B)):sha(p) for p in [Path(__file__),OUT/'inspect_injection.py',OUT/'METADATA.json',B/'bis/F2_CONTROL_EXTRACTION.json',B/'bis/F2_CONTROL_SCHEMAS.json',B/'REGISTRO_C4.json',B/'posterior_220_readout.py',B/'catalog_220_readout.py']}
new('DESCRIPTIVE_RESULT.json',result)
print(json.dumps({'elapsed_s':result['elapsed_s'],'priors_identical':result['analytic_prior_dictionaries_identical'],'written':'DESCRIPTIVE_RESULT.json'}))
