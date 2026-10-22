"""Cross-fit numerical proposals on existing pilot likelihoods.

No waveform evaluations, no new evidence estimates, no physical-prior change.
Held-out second-moment estimates diagnose inefficiency but are unreliable in
unsampled tails; the winner must face fresh draws and all original criteria.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import copy
import json
import time
import numpy as np
from scipy.special import logsumexp, betaln
from scipy.optimize import minimize
from scipy.stats import multivariate_t
import source_evidence as se
from audit_phase_source import load_run
from adapt_phase_source import weighted_fit

FOLDER=se.ROOT/'proposal_efficiency_diagnostic'
PILOT=se.ROOT/'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192'


def posterior_weights(logl,logq):
    logw=logl-logq[:,None]
    return np.exp(logw-logsumexp(logw,axis=0))


def beta_fit(x,w):
    if np.any(x<=0) or np.any(x>=1):
        raise ValueError('Open unit interval required for beta fit')
    logx,log1x=float(w@np.log(x)),float(w@np.log1p(-x))
    def cost(z):
        a,b=np.exp(z)
        return -(a-1)*logx-(b-1)*log1x+betaln(a,b)
    result=minimize(cost,np.log([2.,2.]),method='L-BFGS-B',bounds=[(np.log(.2),np.log(100))]*2)
    if not result.success:
        raise ValueError('Weighted beta fit failed')
    return np.exp(result.x).tolist()


def logq_for(proposal,y,jac):
    coords=y[:,:2] if proposal['kind']=='spectral_product' else y
    logs=[]
    for c in proposal['components']:
        logs.append(np.log(c['weight'])+multivariate_t.logpdf(coords,loc=c['mean'],shape=c['shape'],df=proposal['df']))
    value=logsumexp(np.column_stack(logs),axis=1)
    if proposal['kind']=='spectral_product':
        a,b=proposal['beta_cosi']
        value+=(a-1)*np.log(y[:,4])+(b-1)*np.log1p(-y[:,4])-betaln(a,b)
        # The other three unchanged unit-prior coordinates have density one.
    return np.logaddexp(np.log(proposal['defensive_weight'])-np.log(jac),value)+np.log(jac)


def candidates(y,weights,seed):
    answer=[]
    for kind in ('full6D','spectral_product'):
        coords=y if kind=='full6D' else y[:,:2]
        beta=beta_fit(y[:,4],weights) if kind=='spectral_product' else None
        for count in (3,6,12):
            components,history=weighted_fit(coords,weights,count=count,floor=1e-5,seed=seed+count)
            for inflation in (.5,1.,2.):
                for df in (5.,30.):
                    cs=copy.deepcopy(components)
                    for c in cs:
                        c['weight']*=.9/.7
                        c['shape']=(np.array(c['shape'])*(inflation/2)).tolist()
                    answer.append(dict(id=f'{kind}_K{count}_scale{inflation}_df{int(df)}',kind=kind,
                         components=cs,beta_cosi=beta,defensive_weight=.1,df=df,
                         covariance_inflation=inflation,count=count,fit_history=history))
    return answer


def main():
    started=time.monotonic()
    result,u,logq,inside,logl,stats=load_run(PILOT)
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y,jac=(f[n].copy() for n in ('transport_y','forward_Jacobian'))
    FOLDER.mkdir(exist_ok=False)
    ids=np.random.default_rng(130881).permutation(len(u))
    folds=np.array_split(ids,2)
    names=['diagnose_proposal_efficiency.py','adapt_phase_source.py','audit_phase_source.py',
           'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT.json',
           'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/PROPOSALS.npz']
    se.write(FOLDER/'REGISTRATION.json',dict(status='REGISTERED_CROSS_FIT_PROPOSAL_DIAGNOSTIC',
        date_utc=datetime.now(timezone.utc).isoformat(),split_seed=130881,fold_indices=[v.tolist() for v in folds],
        hypotheses=['Six-dimensional inflated Student-t tails and unnecessary nuisance-coordinate correlations may waste samples',
                    'A spectral2D mixture times an independently fitted beta(cosi) and uniform q,spin2,time may sample more efficiently'],
        warning='Same-pilot cross-fitting is only numerical training diagnostics, not independent scientific evidence; lowESS and unseen tails can invalidate predicted efficiency',
        physical_prior_changed=False,scientific_acceptance=False,
        hashes={n:se.sha(se.ROOT/n) for n in names}))
    all_rows=[]
    for fold,test_ids in enumerate(folds):
        train_ids=folds[1-fold]
        tw=posterior_weights(logl[train_ids],logq[train_ids]).mean(axis=1)
        train_good=inside[train_ids]
        trained=candidates(y[train_ids][train_good],tw[train_good]/tw.sum(),130882+100*fold)
        ep=posterior_weights(logl[test_ids],logq[test_ids])
        good=inside[test_ids]; yy,jj=y[test_ids][good],jac[test_ids][good]
        oldq=logq[test_ids][good]; pp=ep[good]
        baseline=1/(len(test_ids)*np.sum(pp*pp,axis=0))
        second_weight=pp*pp
        rows=[]
        for proposal in trained:
            newq=logq_for(proposal,yy,jj)
            terms=second_weight*np.exp(oldq-newq)[:,None]
            estimate=1/(len(test_ids)*terms.sum(axis=0))
            gain=estimate/baseline
            concentration=np.max(terms,axis=0)/np.sum(terms,axis=0)
            rows.append(dict(id=proposal['id'],fold=fold,
                median_efficiency=float(np.median(estimate)),efficiency_quantiles=np.quantile(estimate,[0,.1,.5,.9,1]).tolist(),
                median_gain=float(np.median(gain)),gain_quantiles=np.quantile(gain,[0,.1,.5,.9,1]).tolist(),
                second_moment_max_contribution_quantiles=np.quantile(concentration,[0,.5,.9,1]).tolist(),
                scope='Held-out approximate variance prediction, not measured efficiency on new draws'))
        rows.sort(key=lambda r:r['median_efficiency'],reverse=True)
        baseline_data=dict(median_efficiency=float(np.median(baseline)),
            training_pooled_ESS=float(1/np.sum(tw**2)),test_component_ESS_quantiles=np.quantile(1/np.sum(ep*ep,axis=0),[0,.5,1]).tolist())
        se.write(FOLDER/f'fold_{fold}.json',dict(rows=rows,baseline=baseline_data,proposals=trained))
        all_rows.extend(rows)
        print(json.dumps(dict(fold=fold,baseline=baseline_data,top=rows[:3])),flush=True)
    ids=sorted({r['id'] for r in all_rows})
    ranking=[]
    for name in ids:
        rows=[r for r in all_rows if r['id']==name]
        ranking.append(dict(id=name,minimum_fold_median_gain=min(r['median_gain'] for r in rows),
                            median_gains=[r['median_gain'] for r in rows],efficiencies=[r['median_efficiency'] for r in rows]))
    ranking.sort(key=lambda r:r['minimum_fold_median_gain'],reverse=True)
    summary=dict(status='CROSS_FIT_DIAGNOSTIC_ONLY',ranking=ranking,scientific_acceptance=False,
        elapsed_seconds=time.monotonic()-started,number_of_candidates=len(ids),registration_sha256=se.sha(FOLDER/'REGISTRATION.json'),
        action='Fresh independently generated points, support/density validation and numerical/original precision checks are mandatory before adopting any proposal')
    se.write(FOLDER/'RESULT.json',summary)
    print(json.dumps(dict(status=summary['status'],top=ranking[:6],elapsed_seconds=summary['elapsed_seconds'])),flush=True)


if __name__=='__main__':
    main()
