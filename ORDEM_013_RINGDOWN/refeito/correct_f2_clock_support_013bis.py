"""Retain raw clock curves and expose their unsupported tails, without truncation."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json,hashlib,sys
import numpy as np,h5py
from scipy.integrate import trapezoid
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tgl_ringdown_prediction import prediction
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=ROOT/'bis/F2_FREE_CLOCK_EXTENDED.json';doc=json.loads(old.read_bytes())
    path=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    if sha(path)!=doc['source_sha256']:raise ValueError('Source mismatch')
    with h5py.File(path,'r') as f:s=f['pSEOBNRv5PHM/posterior_samples'][()]
    x=np.vstack([s['domega220'],s['dtau220']])
    xb=np.array([prediction(float(m),float(a),'R-B')['x'] for m,a in zip(s['final_mass_non_evolved'],s['final_spin_non_evolved'])])
    def ess(q,bw):
        moved=x.copy();moved[1]+=q*xb/(1+q*xb)
        cov=np.cov(moved)*len(s)**(-1/3)*bw*bw;inv=np.linalg.inv(cov)
        t=-.5*np.einsum('in,ij,jn->n',moved,inv,moved)
        w=np.exp(t-t.max());return float(w.sum()**2/(w@w))
    for c in doc['curves']:
        bw=c['bandwidth_multiplier'];null=ess(0,bw)
        def point(q):
            value=ess(q,bw)
            return dict(q=float(q),ESS_GR=null,ESS_restricted=value,ESS_threshold=100,
              status='SUPPORTED_LOCAL_KERNEL_COUNT' if min(null,value)>=100 else 'INCONCLUSIVE_DENSITY_SUPPORT')
        c['support_reported_points']=[point(float(q)) for q in c['reported_points']]
        cut=c['first_lnB_minus_log100_crossing_q']
        c['raw_KDE_diagnostic_crossing']=None if cut is None else point(cut)
        c['data_supported_cut']=None
        c['crossing_scope']='Raw KDE approximation only; no supported cut while local ESS fails. No physical exclusion.'
        q=np.array(c['q']);support=np.array([ess(v,bw) for v in q])
        c['ESS_restricted_grid']=support.tolist()
        c['support_interval_rule']='Grid of pointwise kernel ESS; not MCMC effective sample size or calibrated error bars'
        for post in c['conditional_posteriors']:
            post['quantile_support']={quantile:point(v) for quantile,v in post['q_quantiles'].items()}
            keep=q<=post['ceiling_in_tM'];qq=q[keep];w=np.exp(np.array(c['lnB'])[keep])
            unsupported=(support[keep]<100).astype(float)
            post['raw_KDE_posterior_mass_in_low_support_grid']=float(trapezoid(w*unsupported,qq)/trapezoid(w,qq))
            post['quadrature_converged']=post['converged']
            post['density_validation_status']='INCONCLUSIVE_DENSITY_SUPPORT_IN_NORMALIZATION_TAIL'
            post['interpretation']='Numerical conditional prior result only; stable quadrature does not establish density-tail validity. Tail and ceiling retained unchanged.'
        print(bw,c['raw_KDE_diagnostic_crossing'],flush=True)
    doc.update(supersedes='bis/F2_FREE_CLOCK_EXTENDED.json',supersedes_sha256=sha(old),
      support_correction=dict(builder_sha256=sha(Path(__file__)),review_path='bis/F2_DENSITY_CLOCK_REVIEW.md',review_sha256=sha(ROOT/'bis/F2_DENSITY_CLOCK_REVIEW.md'),finding='F2-R1'),
      status='NONBLIND_RAW_CLOCK_DENSITY__INCONCLUSIVE_DENSITY_SUPPORT_FOR_CUT')
    p=ROOT/'bis/F2_FREE_CLOCK_EXTENDED_v2.json'
    if p.exists():raise FileExistsError(p)
    raw=(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p);print(p,sha(p))
if __name__=='__main__':main()
