"""Check variance-optimal multi-target training against arithmetic pooling.

For normalized target densities p_j, q proportional to sqrt(mean(p_j**2))
minimizes the mean importance second moment, by Cauchy-Schwarz. Here target
normalizations are estimated from a low-ESS pilot, so this is a proposal
hypothesis only. Held-out data and ultimately fresh draws must test it.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import json
import numpy as np
import source_evidence as se
from audit_phase_source import load_run
from adapt_phase_source import weighted_fit
from diagnose_proposal_efficiency import PILOT,posterior_weights,logq_for

FOLDER=se.ROOT/'balanced_proposal_diagnostic'


def fit_proposal(y,weights,count,seed):
    components,history=weighted_fit(y,weights,count=count,floor=1e-5,seed=seed)
    for c in components:
        c['weight']*=.9/.7
    return dict(kind='full6D',components=components,defensive_weight=.1,df=30.,
                covariance_inflation=2.,count=count,fit_history=history)


def main():
    result,u,logq,inside,logl,stats=load_run(PILOT)
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y,jac=(f[n].copy() for n in ('transport_y','forward_Jacobian'))
    prior=json.loads((se.ROOT/'proposal_efficiency_diagnostic/REGISTRATION.json').read_bytes())
    folds=[np.array(v) for v in prior['fold_indices']]
    FOLDER.mkdir(exist_ok=False)
    names=['diagnose_balanced_proposal.py','diagnose_proposal_efficiency.py',
           'proposal_efficiency_diagnostic/RESULT.json',
           'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT.json']
    se.write(FOLDER/'REGISTRATION.json',dict(status='REGISTERED_MULTI_TARGET_VARIANCE_PROPOSAL_CHECK',
        date_utc=datetime.now(timezone.utc).isoformat(),selection='Maximize minimum-fold 10th percentile efficiency gain; median as secondary diagnostic',
        formula='q_opt proportional sqrt(mean_j p_j^2) minimizes average relative variance at fixed normalized targets; pilot target estimates may be unreliable',
        alternatives=['mean','rms'],components=[3,6,12],df=30.,inflation=2.,
        physical_prior_changed=False,scientific_acceptance=False,
        hashes={n:se.sha(se.ROOT/n) for n in names}))
    all_rows=[]
    for fold,test_ids in enumerate(folds):
        train_ids=folds[1-fold]; p=posterior_weights(logl[train_ids],logq[train_ids])
        ep=posterior_weights(logl[test_ids],logq[test_ids]); good=inside[test_ids]
        yy,jj=y[test_ids][good],jac[test_ids][good]; oldq=logq[test_ids][good]; pp=ep[good]
        baseline=1/(len(test_ids)*np.sum(pp*pp,axis=0)); rows=[]; models=[]
        for method in ('mean','rms'):
            w=p.mean(axis=1) if method=='mean' else np.sqrt((p*p).mean(axis=1))
            w/=w.sum(); tg=inside[train_ids]
            for count in (3,6,12):
                model=fit_proposal(y[train_ids][tg],w[tg],count,130882+100*fold+count)
                model.update(id=f'{method}_K{count}',method=method)
                newq=logq_for(model,yy,jj)
                terms=pp*pp*np.exp(oldq-newq)[:,None]
                estimate=1/(len(test_ids)*terms.sum(axis=0)); gain=estimate/baseline
                row=dict(id=model['id'],fold=fold,gain_quantiles=np.quantile(gain,[0,.1,.5,.9,1]).tolist(),
                    efficiency_quantiles=np.quantile(estimate,[0,.1,.5,.9,1]).tolist(),
                    training_ESS=float(1/np.sum(w*w)),
                    second_moment_max_contribution_quantiles=np.quantile(terms.max(axis=0)/terms.sum(axis=0),[.5,.9,1]).tolist())
                rows.append(row); models.append(model)
        all_rows.extend(rows)
        se.write(FOLDER/f'fold_{fold}.json',dict(rows=rows,proposals=models))
    ranking=[]
    for name in sorted({r['id'] for r in all_rows}):
        rows=[r for r in all_rows if r['id']==name]
        ranking.append(dict(id=name,min_fold_gain10=min(r['gain_quantiles'][1] for r in rows),
            min_fold_median_gain=min(r['gain_quantiles'][2] for r in rows),rows=rows))
    ranking.sort(key=lambda r:r['min_fold_gain10'],reverse=True)
    summary=dict(status='VARIANCE_BALANCED_PROPOSAL_DIAGNOSTIC_ONLY',ranking=ranking,
        scientific_acceptance=False,physical_prior_changed=False,
        caution='Not a new evidence estimate or convergence result; denominator uncertainty and unsampled tails remain',
        registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json',summary)
    print(json.dumps(dict(status=summary['status'],ranking=[{k:v for k,v in r.items() if k!='rows'} for r in ranking])),flush=True)


if __name__=='__main__':
    main()
