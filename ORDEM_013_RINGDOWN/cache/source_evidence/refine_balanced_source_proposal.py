"""Fit and test a variance-balanced proposal; never alter the physical prior."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import argparse
import json
import numpy as np
from scipy.stats import multivariate_t
from scipy.special import logsumexp
import source_evidence as se
import phase_marginal_source as pm
import transport_phase_source as tp
from audit_phase_source import load_run
from diagnose_proposal_efficiency import PILOT,posterior_weights
from diagnose_balanced_proposal import fit_proposal

STAGE=se.ROOT/'phase_ringdown_balanced'


def fit():
    diagnostic=json.loads((se.ROOT/'balanced_proposal_diagnostic/RESULT.json').read_bytes())
    selected=diagnostic['ranking'][0]
    method,count_text=selected['id'].split('_K'); count=int(count_text)
    result,u,logq,inside,logl,stats=load_run(PILOT)
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y=f['transport_y'].copy()
    p=posterior_weights(logl,logq)
    w=p.mean(axis=1) if method=='mean' else np.sqrt((p*p).mean(axis=1))
    w/=w.sum()
    proposal=fit_proposal(y[inside],w[inside],count,130890)
    proposal.update(family=result['family'],method=method,training_weight_ESS=float(1/np.sum(w*w)),
        physical_prior_changed=False,training_accepted_as_science=False,
        selected_by='Largest minimum-fold10th percentile predicted efficiency gain, no lnB values used for selection',
        selected_candidate=selected)
    STAGE.mkdir(exist_ok=False); se.write(STAGE/'PROPOSAL.json',proposal)
    names=['refine_balanced_source_proposal.py','diagnose_balanced_proposal.py','diagnose_proposal_efficiency.py',
        'balanced_proposal_diagnostic/RESULT.json','balanced_proposal_diagnostic/REGISTRATION.json',
        'transport_phase_source.py','ringdown_source_coordinates.py','adapt_phase_source.py',
        'phase_marginal_source.py','phase_runs/REGISTRATION.json','phase_ringdown_balanced/PROPOSAL.json',
        'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192/RESULT.json']
    se.write(STAGE/'REGISTRATION.json',dict(status='REGISTERED_VARIANCE_BALANCED_NUMERICAL_PROPOSAL',
        date_utc=datetime.now(timezone.utc).isoformat(),selected=selected,seed=130892,draws=16384,
        caution='Cross-fit lower-tail gains remain below one. Fresh draws are required; no expected precision is asserted.',
        source_parameters_integrated=7,source_parameters_sampled=6,physical_prior_changed=False,
        likelihood_changed=False,scientific_acceptance=False,C6_changed=False,
        acceptance='Unchanged ESS>=100,maxweight<=.05,MCsdlnB<=.2, independent repeats, rate and posterior calibration',
        hashes={n:se.sha(se.ROOT/n) for n in names}))
    print(json.dumps(dict(status='FITTED_VARIANCE_BALANCED_PROPOSAL',selected=selected['id'],count=count,
        training_weight_ESS=proposal['training_weight_ESS'])),flush=True)


def oracle():
    proposal=tp.check(); draws=tp.draw(proposal,32768,130891)
    good=draws['inside']; u=draws['unit_cube']; logq=draws['logq']; y=draws['transport_y']
    jac=draws['forward_Jacobian']; w=np.zeros(len(good)); w[good]=np.exp(-logq[good])
    values=np.column_stack([w]+[w*u[:,i] for i in range(6)]+[w*u[:,i]**2 for i in range(6)])
    expected=np.array([1.]+[.5]*6+[1/3]*6)
    means=values.mean(axis=0); errors=values.std(axis=0,ddof=1)/np.sqrt(len(w))
    standardized=np.abs(means-expected)/errors
    # Independent density formula in physical unit-prior coordinates.
    terms=[np.full(int(good.sum()),np.log(proposal['defensive_weight']))]
    for c in proposal['components']:
        terms.append(np.log(c['weight'])+multivariate_t.logpdf(y[good],loc=c['mean'],shape=c['shape'],df=proposal['df'])+np.log(jac[good]))
    density_error=float(np.max(np.abs(logsumexp(np.column_stack(terms),axis=1)-logq[good])))
    ok=bool(standardized.max()<5 and density_error<=1e-12)
    output=dict(status='PASS_TRANSPORT_PROPOSAL_MOMENTS' if ok else 'PROPOSAL_MOMENTS_FAILED',
        N=len(w),seed=130891,inside=int(good.sum()),outside=int((~good).sum()),
        means=means.tolist(),expected=expected.tolist(),MC_standard_errors=errors.tolist(),
        max_standardized_error=float(standardized.max()),direct_density_error=density_error,
        scientific_acceptance=False,physical_prior_changed=False,
        registration_sha256=se.sha(STAGE/'REGISTRATION.json'))
    se.write(STAGE/'PROPOSAL_ORACLE.json',output); print(json.dumps(output),flush=True)
    if not ok:
        raise ValueError('Proposal normalization/density check failed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['fit','oracle','run'])
    parser.add_argument('--draws',type=int,default=16384);parser.add_argument('--seed',type=int,default=130892)
    parser.add_argument('--processes',type=int,default=6)
    args=parser.parse_args(); tp.STAGE=STAGE
    if args.command=='fit': fit()
    elif args.command=='oracle': oracle()
    else: tp.run(args)
