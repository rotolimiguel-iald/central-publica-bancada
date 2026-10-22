"""Independent arithmetic checks of archived C5 conversions; no science rerun."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import json, hashlib, math, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

B=Path(__file__).resolve().parents[1]
def read(n): return json.loads((B/n).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    start=time.perf_counter(); checks=[]; errors=[]
    a=read('bis/e0_core/SYSTEMATICS_ADENDO.json'); old=read('C5_IMR_RECOVERY.json')
    for n,h in a['sources'].items():
        if sha(B/n)!=h['sha256']: raise ValueError('Changed input '+n)
    arrays={}; gps={}
    for f in old['draws']:
        p=B/f['path']
        if sha(p)!=f['sha256']: raise ValueError('Changed draws')
        with np.load(p,allow_pickle=False) as z:
            key=p.name.split('_')[0];arrays[key]=z['draws'].copy()
            gps[key]=list(zip(z['H1_original_GPS'].tolist(),z['L1_original_GPS'].tolist()))
    def compare(got,want,label):
        err=abs(got-want)/max(abs(want),1e-12);errors.append(err)
        if not math.isclose(got,want,rel_tol=1e-9,abs_tol=1e-13): raise ValueError((label,got,want))
    def stats(v,groups,st,label):
        n=len(v); m=math.fsum(v)/n; variance=math.fsum((q-m)**2 for q in v)/(n-1); sd=math.sqrt(variance)
        sums={};isums={}
        for q,g in zip(v,groups):
            sums[g]=sums.get(g,0)+(q-m)
            influence=((q-m)**2-variance*(n-1)/n)*n/(n-1)/(2*sd) if sd else 0
            isums[g]=isums.get(g,0)+influence
        G=len(sums);se=math.sqrt(G/(G-1)*math.fsum(q*q for q in sums.values()))/n
        sse=math.sqrt(G/(G-1)*math.fsum(q*q for q in isums.values()))/n
        for k,w in [('mean',m),('sigma_ddof1',sd),('SE_mean_grouped_conditional',se),('SE_sigma_influence_grouped_conditional',sse)]: compare(st[k],w,label+':'+k)
    for i,r in enumerate(a['full_IMR_family_recovery']):
        orig=old['results'][i]
        if r.get('dtau_statistics') is None: continue
        x=r['x220_recovery']; raw=arrays[r['psd']][orig['draws_index']][:,1]
        values=[-float(v)*x/(1+float(v)*x) for v in raw]
        stats(values,gps[r['psd']],r['dtau_statistics'],str(i))
        compare(r['noiseless_dtau'],-orig['noiseless_a_hat']*x/(1+orig['noiseless_a_hat']*x),'noiseless')
        checks.append('IMR:'+str(i))
    emp=read('C5_EMPIRICAL_IMR_STARTS.json')
    for i,r in enumerate(a['empirical_QNM_recovery_by_window']):
        if r.get('dtau_statistics') is None: continue
        orig=emp['results'][i]; x=orig['dimensionless_extra_damping'][0]
        compare(r['x220'],x,'stored x')
        values=[-f['MLE']*x/(1+f['MLE']*x) for f in orig['profile_intervals']]
        stats(values,emp['noise_indices'],r['dtau_statistics'],'emp'+str(i));checks.append('EMP:'+str(i))
    for r in a['noiseless_ablations']:
        compare(r['dtau_hat'],-r['a_hat']*r['x220']/(1+r['a_hat']*r['x220']),'ablations')
        if r['SE_mean'] is not None:raise ValueError('One noiseless estimate is not sampling error')
    result={'status':'PASS_ARITHMETIC_AND_SCOPE_NOT_OPERATIONAL_CALIBRATION','utc':datetime.now(timezone.utc).isoformat(),
      'source_sha256':sha(B/'bis/e0_core/SYSTEMATICS_ADENDO.json'),'code_sha256':sha(Path(__file__)),
      'cells_recomputed':len(checks),'scalar_comparisons':len(errors),'max_relative_error_scaled_1e12':max(errors),
      'wall_seconds':time.perf_counter()-start,
      'scope':['No generator imported; no waveform, PE, strain or new injection','Moment arithmetic independently recomputed from archived estimates','Recovery x checked against stored exact-QNM x for empirical cells; main scalar physics review separate','Grouped influence errors conditional on finite noise library, not independent event replication','Missing mixture family branch remains null; no systematic gate paid','Correction: report phrase operador communicated prior scalar review means principal agent, not human operator','25 MiB writer guard in producer is weaker than task decimal 25 MB; actual outputs below both; future packaging uses decimal'],
      'gate':'INCONCLUSIVE_SYSTEMATICS'}
    p=B/'bis/E0_SYSTEMATICS_REVIEW.json'
    with p.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
