"""Independent checks on archived posteriors only; no PE, strain, builder imports or writes."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,io,json,math,re,time
import h5py
import numpy as np
B=Path(__file__).resolve().parents[2];A=B/'bis/f2_injection'
START=time.perf_counter()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def get(p):return json.loads(p.read_bytes())
def close(a,b,label):
    need(np.allclose(a,b,rtol=2e-12,atol=2e-13,equal_nan=False),label)
def plain(v):
    if isinstance(v,bytes):return v.decode()
    if isinstance(v,np.ndarray):
        if v.dtype.names:return [{n:plain(row[n]) for n in v.dtype.names} for row in v]
        return [plain(x) for x in v]
    if isinstance(v,np.generic):return plain(v.item())
    if isinstance(v,float) and not math.isfinite(v):return None
    return v
receipt=get(A/'RECEIPT.json');d=get(A/'DESCRIPTIVE_RESULT.json');meta=get(A/'METADATA.json');contract=get(A/'PRIOR_CONTRACT.json')
pins={}
for row in receipt['inputs']+receipt['files_written']:
    p=B/row['path'].replace('\\','/');actual=sha(p)
    need(actual==row['sha256'] and p.stat().st_size==row['bytes'],'Receipt pin '+row['path']);pins[row['path']]=actual
need(receipt['lnB'] is None and contract['lnB'] is None,'Invented Bayes factor')
for n,h in d['dependencies_sha256'].items():need(sha(B/n.replace('\\','/'))==h,'Dependency '+n)
src=B/d['source'];before=sha(src)
need(before==d['source_sha256']==meta['sha256']==contract['source_sha256']==receipt['unchanged_source_sha256_after_reporting'],'Cross source hashes')
matches=[r for a in get(B/'bis/F2_CONTROL_EXTRACTION.json')['archives'] for r in a['files'] if r.get('path','').replace('\\','/')==d['source']]
need(len(matches)==1 and matches[0]['sha256']==before and matches==d['extraction_path_matches'],'Extraction identity')
schema=[r for r in get(B/'bis/F2_CONTROL_SCHEMAS.json') if r['path'].replace('\\','/')==d['source']]
need(len(schema)==1 and schema[0]['sha256']==before,'Schema identity')
need(meta['schema_receipt_sha256']==sha(B/'bis/F2_CONTROL_SCHEMAS.json'),'Metadata schema pin')
fields=['domega220','dtau220','domega440','dtau440','final_spin_non_evolved','final_mass_non_evolved','redshift','network_optimal_snr']

def independent_stats(x,expected):
    n=len(x);s=np.sort(x);positions=np.arange(n,dtype=float)
    # Order-statistic interpolation, not the builder's np.quantile call.
    quant=lambda ps:np.interp(np.asarray(ps)*(n-1),positions,s)
    mean=math.fsum(map(float,x))/n
    sd=math.sqrt(math.fsum((float(v)-mean)**2 for v in x)/(n-1))
    close([mean,sd,float(quant([.5])[0]),s[0],s[-1]],[expected[k] for k in ['mean','sd_ddof1','median','min','max']],'Moment mismatch')
    close(quant(expected['quantile_probabilities']),expected['quantiles'],'Quantile mismatch')
    pos=int(np.count_nonzero(x>0));zero=int(np.count_nonzero(x==0))
    need(n==expected['n'] and pos==expected['n_positive'] and zero==expected['n_zero'],'Sign/count mismatch')
    close([pos/n,1-pos/n],[expected['p_positive'],expected['cdf_at_zero']],'Sign mass mismatch')
    for level in [.5,.9,.95,.99]:
        bounds=quant([(1-level)/2,(1+level)/2]);r=expected['central_intervals'][str(level)]
        close(bounds,r['interval'],'Central interval');need(bool(bounds[0]<=0<=bounds[1])==r['contains_zero'],'Central membership')
        included=math.ceil(level*n);widths=s[included-1:]-s[:n-included+1];i=int(np.argmin(widths))
        shortest=[s[i],s[i+included-1]];r=expected['shortest_contiguous_intervals'][str(level)]
        close(shortest,r['interval'],'Shortest interval');need(bool(shortest[0]<=0<=shortest[1])==r['contains_zero'],'Shortest membership')

def independent_kde_checks(data,rows):
    # Direct NumPy Gaussian sums with covariance whitening; no scipy.stats.gaussian_kde.
    ix=np.random.default_rng(d['seed']).permutation(len(data));train=data[ix[:16000]];queries=data[ix[16000:]]
    mean=train.mean(axis=0);cov=np.cov(train,rowvar=False,ddof=1);chol=np.linalg.cholesky(cov)
    white=np.linalg.solve(chol,(train-mean).T).T
    whiteq=np.linalg.solve(chol,(queries-mean).T).T
    zero=np.linalg.solve(chol,-mean)
    distances0=np.sum((white-zero)**2,axis=1)
    factors=np.array([16000**(-1/6)*r['bandwidth_multiplier'] for r in rows]);scales=2*factors**2
    zero_sums=np.array([np.exp(-distances0/s).sum() for s in scales]);counts=np.zeros(len(rows),dtype=int)
    norms=np.sum(white*white,axis=1)
    for start in range(0,len(whiteq),128):
        q=whiteq[start:start+128]
        distance=np.maximum(np.sum(q*q,axis=1)[:,None]+norms[None,:]-2*q@white.T,0)
        for k,scale in enumerate(scales):counts[k]+=np.count_nonzero(np.exp(-distance/scale).sum(axis=1)>=zero_sums[k])
    fullcov=np.cov(data,rowvar=False,ddof=1);inv=np.linalg.inv(fullcov)
    fulldistance=np.einsum('ni,ij,nj->n',data,inv,data)
    result=[]
    for k,r in enumerate(rows):
        content=float(counts[k]/len(queries));factor=len(data)**(-1/6)*r['bandwidth_multiplier']
        weights=np.exp(-fulldistance/(2*factor**2));support=float(weights.sum()**2/np.sum(weights**2))
        logdensity=math.log(weights.mean())-math.log(2*math.pi*math.sqrt(np.linalg.det(fullcov))*factor**2)
        scale=math.sqrt(content*(1-content)/len(queries));within=int(np.count_nonzero(fulldistance/factor**2<=4))
        close([content,factors[k],support,logdensity,scale],[r['content_at_GR'],r['train_scott_factor'],r['kernel_weight_effective_count_not_chain_ESS'],r['full_sample_log_density_at_GR'],r['query_binomial_scale_if_iid_only']],'Independent KDE differs')
        need(within==r['rows_within_two_kernel_sd'] and (content<=.9)==r['inside_joint_90'] and (content<=.95)==r['inside_joint_95'],'KDE discrete check')
        result.append(dict(bandwidth=r['bandwidth_multiplier'],query_count=int(counts[k]),content=content,kernel_support=support,binomial_scale_if_iid=scale))
    return result

groups={};analytic_groups={}
with h5py.File(src,'r') as f:
    for label in ['NR_with_44','NR_without_44']:
        g=f[label];ds=g['posterior_samples'];need(ds.shape==(20000,) and not any('weight' in n.lower() for n in ds.dtype.names),'Shape/weight field')
        a=ds.fields(fields)[:];saved=d['groups'][label]
        for field in fields:
            x=np.asarray(a[field],dtype='<f8');need(np.isfinite(x).all(),'Nonfinite posterior')
            need(hashlib.sha256(x.tobytes()).hexdigest()==d['source_field_sha256'][label][field],'Field hash mismatch')
            independent_stats(x,saved['summaries'][field])
        analytic={n:plain(g['priors/analytic/'+n][()]) for n in g['priors/analytic']}
        need(analytic==meta['groups'][label]['priors_analytic'],'Archived prior declarations mismatch');analytic_groups[label]=analytic
        priorarrays=[]
        for field in fields[:4]:
            declaration=g['priors/analytic/'+field][0].decode()
            need(declaration.startswith('Uniform('),'Unexpected analytic class')
            lo,hi=[float(re.search(r'\b'+key+r'=([-+\d.eE]+)',declaration)[1]) for key in ['minimum','maximum']]
            need([lo,hi]==([-0.8,2.0] if field.endswith('220') else [-0.8,0.8]),'Different prior limits')
            prior=g['priors/samples/'+field][:];priorarrays.append(prior)
            need(len(prior)==5000 and np.isfinite(prior).all() and np.all((prior>=lo)&(prior<=hi)),'Prior samples')
            need(np.all((a[field]>=lo)&(a[field]<=hi)) and np.ptp(a[field])>0,'Posterior support/free parameter')
            p=saved['prior_diagnostics'][field]
            close([1/(hi-lo),hi/(hi-lo),np.mean(prior>0),np.mean(a[field]>0)-hi/(hi-lo)],
                  [p['density'],p['analytic_p_positive'],p['sample_p_positive'],p['posterior_minus_prior_p_positive']],'Prior diagnostics')
        close(np.corrcoef(priorarrays),saved['prior_sample_correlation_4fields'],'Prior sample correlation')
        data=np.column_stack([a['domega220'],a['dtau220']])
        corr=np.cov(data,rowvar=False)[0,1]/(np.std(data[:,0],ddof=1)*np.std(data[:,1],ddof=1))
        close(corr,saved['posterior_correlation_220'],'Correlation')
        unique=len(set(map(tuple,data)));need(unique==saved['posterior_joint_unique_rows_220'],'Unique pair count')
        for sx in ['positive','nonpositive']:
            for sy in ['positive','nonpositive']:
                maskx=data[:,0]>0 if sx=='positive' else data[:,0]<=0
                masky=data[:,1]>0 if sy=='positive' else data[:,1]<=0
                close(np.count_nonzero(maskx&masky)/len(data),saved['posterior_quadrants_220'][f'df_{sx}_dtau_{sy}'],'Quadrants')
        truth=g['injection_data'][0];need(all(not np.isfinite(truth[n]) for n in truth.dtype.names),'Finite truth not reported')
        need(plain(g['injection_data'][()])==meta['groups'][label]['metadata']['injection_data'],'NaN to null representation')
        for key in ['prior_file','prior_dict','default_prior']:
            need(g['config_file/config/'+key][0].decode()==contract['groups'][label][key],'Contract config')
        for field in ['final_spin_non_evolved','final_mass_non_evolved']:
            arr=g['priors/samples/'+field][:];savedprior=contract['groups'][label]['prior_remnant_sample_check'][field]
            close([len(arr),np.isfinite(arr).sum(),np.nanmin(arr),np.nanmax(arr)],[savedprior[n] for n in ['n','finite','min','max']],'Prior remnant sample support')
        kde=independent_kde_checks(data,saved['hpd_GR_220'])
        groups[label]=dict(rows=20000,fields_verified=fields,unique_220_pairs=unique,kde=kde,
            median_df=float(np.median(data[:,0])),median_dtau=float(np.median(data[:,1])),
            prior_220_positive_mass=2/2.8,all_440_deviations_free=True,injection_truth_nonfinite=True)
        print(json.dumps(dict(group=label,kde=kde)),flush=True)
need(analytic_groups['NR_with_44']==analytic_groups['NR_without_44'] and d['analytic_prior_dictionaries_identical'],'Prior dictionary difference')
for field,r in d['differences_with_minus_without'].items():
    s1=d['groups']['NR_with_44']['summaries'][field];s0=d['groups']['NR_without_44']['summaries'][field]
    close([s1['median']-s0['median'],s1['mean']-s0['mean'],s1['p_positive']-s0['p_positive'],s1['sd_ddof1']/s0['sd_ddof1']],
          [r[n] for n in ['median_difference','mean_difference','p_positive_difference','sd_ratio']],'Differences')

# Reproduce only overwrite guarding in memory, never running the builder/file writes.
tree=ast.parse((A/'check_contract.py').read_text(encoding='utf-8'))
start=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='p' for t in n.targets))
end=next(i for i in range(start,len(tree.body)) if isinstance(tree.body[i],ast.Expr) and isinstance(tree.body[i].value,ast.Call) and isinstance(tree.body[i].value.func,ast.Attribute) and tree.body[i].value.func.attr=='replace')
nodes=tree.body[start:end+1];guard_probes=[]
for optimize in [0,1]:
    events=[];raw_store={}
    class Stream(io.BytesIO):
        def close(self):
            if not self.closed:raw_store['bytes']=self.getvalue()
            super().close()
    class FakePath:
        def __truediv__(self,n):return self
        def exists(self):return True
        def with_suffix(self,s):return self
        def open(self,mode):events.append('open_mock_tmp');return Stream()
        def read_bytes(self):return raw_store['bytes']
        def replace(self,p):events.append('replace_existing_mock_result')
    env=dict(OUT=FakePath(),res={'lnB':None},json=json)
    error=None
    try:exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'overwrite_guard_mock','exec',optimize=optimize),env)
    except AssertionError:error='AssertionError'
    need((error=='AssertionError' and not events) if optimize==0 else 'replace_existing_mock_result' in events,'Guard probe differs')
    guard_probes.append(dict(optimize=optimize,error=error,events=events))
need(sha(src)==before,'HDF5 source changed')
for n,h in pins.items():need(sha(B/n.replace('\\','/'))==h,'Input/artifact changed during review')
result=dict(status='DESCRIPTIVE_NUMBERS_AND_SCOPE_VALIDATED_WITH_OPTIMIZED_GUARD_FINDING',utc=datetime.now(timezone.utc).isoformat(),
    method='Independent NumPy moments/order-statistics/direct Gaussian kernel sums; h5py read-only; no scipy KDE/builder imports',
    source_sha256=before,source_bytes=src.stat().st_size,receipt_sha256=sha(A/'RECEIPT.json'),artifact_input_pins=pins,
    prior_contract_lnB_is_null=True,frequentist_coverage_not_estimated=True,groups=groups,overwrite_guard_probes=guard_probes,
    source_and_artifacts_unchanged=True,script_sha256=sha(Path(__file__)),elapsed_s=time.perf_counter()-START,
    runtime=dict(numpy=np.__version__,h5py=h5py.__version__))
out=Path(__file__).with_name('f2_injection_independent_results.json');need(not out.exists(),'Own result exists')
raw=(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();tmp=out.with_suffix('.json.tmp')
with tmp.open('xb') as f:f.write(raw)
need(tmp.read_bytes()==raw,'Own write mismatch');tmp.rename(out)
print(json.dumps(dict(status=result['status'],elapsed_s=result['elapsed_s'],overwrite_guard_probes=guard_probes)),flush=True)
