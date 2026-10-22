"""Guarded reuse of measured MC algebra; no campaign runs at import."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import json,hashlib,importlib.util
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frozen_populations():
    receipt=json.loads((B/'bis/E0_ROUTE_IV_PROVENANCE.json').read_bytes())
    for n,h in receipt['files'].items():
        if sha(B/n)!=h['sha256']:raise ValueError('Changed frozen input '+n)
    d=json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes())
    rows=d['per_event'];selected=receipt['selected_events'];validate_population(rows,selected)
    lookup={r['event']:r for r in rows}
    pops={'GW250114_actual_width':[lookup['GW250114_082203']],
      'GWTC5_31_quality_mixture':[lookup[e] for e in selected], 'GWTC5_33_quality_mixture':rows}
    return {k:{'events':[r['event'] for r in v],'sigma_df':[r['sigma_df'] for r in v],
      'probabilities':[1/len(v)]*len(v)} for k,v in pops.items()}
def validate_population(rows,selected):
    names=[r['event'] for r in rows]
    if len(names)!=33 or len(set(names))!=33 or len(selected)!=31 or len(set(selected))!=31 or not set(selected)<=set(names):raise ValueError('Invalid population membership')
    sig=np.asarray([r['sigma_df'] for r in rows])
    if not np.isfinite(sig).all() or np.any(sig<=0):raise ValueError('Invalid widths')
def implementation():
    p=B/'refeito/e0_route_iv_power_013bis_v2.py'
    d=json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes())
    if sha(p)!=d['code_sha256']:raise ValueError('Changed algebra source')
    spec=importlib.util.spec_from_file_location('frozen_mc_algebra',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
def sufficient(N,variances,jitter,draws,seed):
    v=np.asarray(variances,dtype=float)
    if not isinstance(N,int) or N<2 or not isinstance(draws,int) or draws<1:raise ValueError('Invalid draw dimensions')
    if v.ndim!=1 or len(v)<1 or not np.isfinite(v).all() or np.any(v<=0):raise ValueError('Invalid variance')
    if not np.isfinite(jitter) or jitter<0:raise ValueError('Invalid jitter')
    return implementation().sufficient(N,v,jitter,draws,seed)
def lrt(n,s,ss,v,free_mean=True):
    n,s,ss,v=[np.asarray(q,dtype=float) for q in [n,s,ss,v]]
    if n.ndim!=2 or s.shape!=n.shape or ss.shape!=n.shape or v.shape!=(n.shape[1],):raise ValueError('Invalid shape')
    if not all(np.isfinite(q).all() for q in [n,s,ss,v]):raise ValueError('Nonfinite sufficient statistic')
    if np.any(n<0) or np.any(n!=np.floor(n)) or np.any(n.sum(axis=1)<2) or np.any(v<=0) or np.any(ss<0):raise ValueError('Invalid sufficient statistic')
    if np.any((n==0)&((s!=0)|(ss!=0))) or np.any(s*s>n*ss+1e-10*np.maximum(1,n*ss)):raise ValueError('Inconsistent sums of squares')
    t,q=implementation().lrt(n,s,ss,v,free_mean)
    if not np.isfinite(t).all() or not np.isfinite(q).all():raise ValueError('Nonfinite LRT result')
    return t,q
def count_above(t,threshold=25.):
    a=np.asarray(t)
    if not np.isfinite(a).all() or a.ndim!=1 or len(a)==0:raise ValueError('Invalid values before boolean conversion')
    return int(np.sum(a>threshold))
