"""Held-out precision diagnostics on the newly completed Phenom draw set.

Training compares mean, RMS and envelope of normalized component densities.
An envelope is a numerical coverage candidate, not a physics assumption or
claimed optimum. No choice depends on the sign of a Bayes factor.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import copy
import json
import numpy as np
import source_evidence as se
from audit_phase_source import load_run
from adapt_phase_source import weighted_fit
from diagnose_proposal_efficiency import posterior_weights, logq_for
from continue_real_phase_source import FOLDER as PILOT, STAGE as OLD_STAGE, check

FOLDER = se.ROOT/'continuation_proposal_crossfit'


def training_weights(p, method):
    if method == 'mean':
        value = p.mean(axis=1)
    elif method == 'rms':
        value = np.sqrt((p*p).mean(axis=1))
    elif method == 'envelope':
        value = p.max(axis=1)
    else:
        raise ValueError('Unknown training objective')
    return value/value.sum()


def candidate(y, w, old, count, seed, inflation):
    components, history = weighted_fit(y, w, count=count, floor=1e-5, seed=seed)
    for component in components:
        component['shape'] = (np.asarray(component['shape'])*(inflation/2.)).tolist()
    inherited = copy.deepcopy(old['components'])
    norm = sum(c['weight'] for c in inherited)
    for component in inherited:
        component['weight'] *= .2/norm
    return dict(kind='full6D', family='IMRPhenomXPHM', df=old['df'],
        defensive_weight=.1, components=components+inherited,
        fit_history=history, covariance_inflation=inflation,
        mixture_mass=dict(fitted=.7, inherited=.2, full_prior=.1),
        physical_prior_changed=False, training_accepted_as_science=False)


def main():
    check()
    result, u, logq, inside, values, stats = load_run(PILOT)
    density = json.loads((PILOT/'DENSITY_AUDIT.json').read_bytes())
    if density['hashes']['RESULT.json'] != se.sha(PILOT/'RESULT.json'):
        raise ValueError('Unmatched completed-draw audit')
    with np.load(PILOT/'PROPOSALS.npz') as archive:
        y, jac = archive['transport_y'].copy(), archive['forward_Jacobian'].copy()
    old = json.loads((OLD_STAGE/'PROPOSAL.json').read_bytes())
    folds = np.array_split(np.random.default_rng(130960).permutation(len(u)), 2)
    FOLDER.mkdir(exist_ok=False)
    names = ['diagnose_continuation_proposal.py','adapt_phase_source.py','diagnose_proposal_efficiency.py',
        str((PILOT/'RESULT.json').relative_to(se.ROOT)),str((PILOT/'DENSITY_AUDIT.json').relative_to(se.ROOT)),
        str((PILOT/'PROPOSALS.npz').relative_to(se.ROOT)),str((OLD_STAGE/'PROPOSAL.json').relative_to(se.ROOT))]
    registration = dict(status='REGISTERED_CONTINUATION_PROPOSAL_CROSS_FIT',
        date_utc=datetime.now(timezone.utc).isoformat(), seed=130960,
        folds=[ids.tolist() for ids in folds], methods=['mean','rms','envelope'],
        fitted_counts=[6,12], covariance_inflations=[1.,2.], df=old['df'],
        selection='Largest minimum-fold10th-percentile predicted gain. Require strictly >1 and minimum-foldmedian >=1 before prospective refinement.',
        purpose='Improve all component integrals, including difficult cross-family/noise targets; never select favorable evidence.',
        scientific_acceptance=False, physical_prior_changed=False,
        caveat='Cross-fit second moments miss unsampled tails and use estimated normalizations; not achieved ESS or a new evidence estimate.',
        hashes={name:se.sha(se.ROOT/name) for name in names})
    se.write(FOLDER/'REGISTRATION.json', registration)
    all_rows = []
    for fold, held in enumerate(folds):
        train = folds[1-fold]
        pt = posterior_weights(values[train], logq[train])
        pe = posterior_weights(values[held], logq[held])
        good = inside[held]
        yy, jj, oq, pp = y[held][good], jac[held][good], logq[held][good], pe[good]
        squares = pp*pp
        baseline = squares.sum(axis=0)
        models, rows = [], []
        for method in registration['methods']:
            w = training_weights(pt, method)
            for count in registration['fitted_counts']:
                # One EM fit shared by the two specified covariance scales.
                model = candidate(y[train][inside[train]], w[inside[train]], old, count, 130961+100*fold+count, 2.)
                for inflation in registration['covariance_inflations']:
                    scaled = copy.deepcopy(model)
                    for component in scaled['components'][:count]:
                        component['shape'] = (np.asarray(component['shape'])*(inflation/2.)).tolist()
                    scaled['covariance_inflation'] = inflation
                    name = f'{method}_K{count}_scale{inflation:g}'
                    terms = squares*np.exp(oq-logq_for(scaled, yy, jj))[:,None]
                    total = terms.sum(axis=0)
                    gain = baseline/total
                    row = dict(id=name, fold=fold, method=method, count=count, inflation=inflation,
                        gain_quantiles=np.quantile(gain,[0,.1,.5,.9,1]).tolist(),
                        predicted_efficiency_quantiles=np.quantile(1/(len(held)*total),[0,.1,.5,.9,1]).tolist(),
                        training_ESS=float(1/(w*w).sum()),
                        largest_second_moment_contribution_quantiles=np.quantile(terms.max(axis=0)/total,[.5,.9,1]).tolist())
                    rows.append(row); models.append(dict(id=name, proposal=scaled))
        all_rows += rows
        se.write(FOLDER/f'fold_{fold}.json',dict(rows=rows,proposals=models))
        print(json.dumps(dict(fold=fold,candidates=len(rows))),flush=True)
        del pt, pe, pp, squares, terms
    ranking = []
    for name in sorted({row['id'] for row in all_rows}):
        rows = [row for row in all_rows if row['id'] == name]
        ranking.append(dict(id=name,min_fold_gain10=min(row['gain_quantiles'][1] for row in rows),
            min_fold_median_gain=min(row['gain_quantiles'][2] for row in rows),rows=rows))
    ranking.sort(key=lambda row:row['min_fold_gain10'],reverse=True)
    best = ranking[0]
    output = dict(status='CONTINUATION_PROPOSAL_DIAGNOSTIC_ONLY',ranking=ranking,
        prospective_refinement_allowed=bool(best['min_fold_gain10']>1 and best['min_fold_median_gain']>=1),
        candidate_count=len(ranking),scientific_acceptance=False,physical_prior_changed=False,
        registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json',output)
    print(json.dumps({**output,'ranking':[{k:v for k,v in row.items() if k!='rows'} for row in ranking]}),flush=True)


if __name__ == '__main__':
    main()
