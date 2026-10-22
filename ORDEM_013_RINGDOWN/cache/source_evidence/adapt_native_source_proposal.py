"""Train on SEOB's own pilot with held-out diagnostics, preserving the prior."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import argparse
import copy
import json
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_t
import source_evidence as se
import transport_phase_source as tp
import run_native_seob_source as runner
from audit_phase_source import load_run
from adapt_phase_source import weighted_fit
from diagnose_proposal_efficiency import posterior_weights, logq_for

PILOT = se.ROOT/'phase_native_seob/SEOBNRv4HM_seed130901_N2048'
DIAGNOSTIC = se.ROOT/'native_proposal_crossfit'
STAGE = se.ROOT/'phase_native_adapted'


def candidate(y, weights, old, count, seed):
    components, history = weighted_fit(y, weights, count=count, floor=1e-5, seed=seed)
    inherited = copy.deepcopy(old['components'])
    for c in inherited:
        c['weight'] *= .2/sum(v['weight'] for v in old['components'])
    return dict(kind='full6D', family='SEOBNRv4HM', defensive_weight=.1,
        df=old['df'], components=components+inherited, fit_history=history,
        trained_weight=.7, inherited_weight=.2, covariance_inflation=2.,
        physical_prior_changed=False, training_accepted_as_science=False)


def diagnostic():
    runner.check()
    result, u, logq, inside, values, stats = load_run(PILOT)
    density = json.loads((PILOT/'DENSITY_AUDIT.json').read_bytes())
    if density['hashes']['RESULT.json'] != se.sha(PILOT/'RESULT.json'):
        raise ValueError('Unmatched source-density audit')
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y, jac = (f[k].copy() for k in ('transport_y', 'forward_Jacobian'))
    old = json.loads((PILOT.parent/'PROPOSAL.json').read_bytes())
    folds = np.array_split(np.random.default_rng(130911).permutation(len(u)), 2)
    DIAGNOSTIC.mkdir(exist_ok=False)
    names = ['adapt_native_source_proposal.py', 'adapt_phase_source.py', 'diagnose_proposal_efficiency.py',
             'phase_native_seob/PROPOSAL.json', 'phase_native_seob/REGISTRATION.json',
             'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json',
             'phase_native_seob/SEOBNRv4HM_seed130901_N2048/DENSITY_AUDIT.json']
    se.write(DIAGNOSTIC/'REGISTRATION.json', dict(
        status='REGISTERED_NATIVE_PROPOSAL_CROSS_FIT', date_utc=datetime.now(timezone.utc).isoformat(),
        seed=130911, folds=[v.tolist() for v in folds], alternatives=['mean_K3', 'mean_K6', 'rms_K3', 'rms_K6'],
        selection='Maximize minimum-fold10th-percentile predicted efficiency gain; require >1 before fitting a production proposal. No selection on evidence sign.',
        proposal_mass={'original_prior': .1, 'inherited': .2, 'SEOB_trained': .7},
        caution='Pilot ESS is low. Cross-fit second moments do not prove future efficiency or cover unsampled tails.',
        physical_prior_changed=False, hashes={n: se.sha(se.ROOT/n) for n in names}))
    rows = []
    for fold, held in enumerate(folds):
        train = folds[1-fold]
        pt = posterior_weights(values[train], logq[train])
        pe = posterior_weights(values[held], logq[held])
        good = inside[held]
        yy, jj, oq, pp = y[held][good], jac[held][good], logq[held][good], pe[good]
        for method in ('mean', 'rms'):
            weights = pt.mean(axis=1) if method == 'mean' else np.sqrt((pt*pt).mean(axis=1))
            weights /= weights.sum()
            for count in (3, 6):
                model = candidate(y[train][inside[train]], weights[inside[train]], old, count, 130912+100*fold+count)
                terms = pp*pp*np.exp(oq-logq_for(model, yy, jj))[:, None]
                gain = (pp*pp).sum(axis=0)/terms.sum(axis=0)
                rows.append(dict(id=f'{method}_K{count}', fold=fold,
                    gain_quantiles=np.quantile(gain, [0, .1, .5, .9, 1]).tolist(),
                    training_ESS=float(1/np.sum(weights*weights)),
                    second_moment_max_contribution_quantiles=np.quantile(terms.max(axis=0)/terms.sum(axis=0), [.5, .9, 1]).tolist()))
    ranking = []
    for name in sorted({r['id'] for r in rows}):
        group = [r for r in rows if r['id'] == name]
        ranking.append(dict(id=name, min_fold_gain10=min(r['gain_quantiles'][1] for r in group),
            min_fold_median_gain=min(r['gain_quantiles'][2] for r in group), rows=group))
    ranking.sort(key=lambda r: r['min_fold_gain10'], reverse=True)
    output = dict(status='NATIVE_PROPOSAL_DIAGNOSTIC_ONLY', ranking=ranking,
        prospective_refinement_allowed=bool(ranking[0]['min_fold_gain10'] > 1),
        scientific_acceptance=False, physical_prior_changed=False,
        registration_sha256=se.sha(DIAGNOSTIC/'REGISTRATION.json'))
    se.write(DIAGNOSTIC/'RESULT.json', output)
    print(json.dumps({**output, 'ranking': [{k: v for k, v in r.items() if k != 'rows'} for r in ranking]}), flush=True)


def fit():
    previous = runner.check()
    diagnosis = json.loads((DIAGNOSTIC/'RESULT.json').read_bytes())
    if not diagnosis['prospective_refinement_allowed']:
        raise ValueError('No lower-tail improvement in held-out diagnostic; no new production run authorized by this rule')
    selected = diagnosis['ranking'][0]
    method, count = selected['id'].split('_K')
    result, u, logq, inside, values, stats = load_run(PILOT)
    p = posterior_weights(values, logq)
    w = p.mean(axis=1) if method == 'mean' else np.sqrt((p*p).mean(axis=1))
    w /= w.sum()
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y = f['transport_y'].copy()
    proposal = candidate(y[inside], w[inside], previous, int(count), 130920)
    proposal.update(training_weight_ESS=float(1/np.sum(w*w)), selected_candidate=selected,
        training_result_sha256=se.sha(PILOT/'RESULT.json'))
    STAGE.mkdir(exist_ok=False)
    se.write(STAGE/'PROPOSAL.json', proposal)
    names = ['adapt_native_source_proposal.py', 'adapt_phase_source.py', 'diagnose_proposal_efficiency.py',
             'native_proposal_crossfit/REGISTRATION.json', 'native_proposal_crossfit/RESULT.json',
             'phase_native_adapted/PROPOSAL.json', 'run_native_seob_source.py',
             'native_seob_source_likelihood.py', 'native_seob_phase_source.py', 'direct_seob_modes.py',
             'stable_peak_imr_model.py', 'stable_peak_phase_source.py', 'source_evidence.py',
             'phase_marginal_source.py', 'importance_source_evidence.py', 'transport_phase_source.py',
             'ringdown_source_coordinates.py', 'phase_runs/REGISTRATION.json', 'INJECTIONS.npz',
             'phase_native_seob/REGISTRATION.json', 'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json']
    se.write(STAGE/'REGISTRATION.json', dict(status='REGISTERED_NATIVE_ADAPTIVE_PROPOSAL',
        date_utc=datetime.now(timezone.utc).isoformat(), family='SEOBNRv4HM', seed=130922, draws=16384,
        selected=selected, source_parameters_integrated=7, source_parameters_sampled=6,
        physical_prior_changed=False, likelihood_changed=False, C6_changed=False,
        acceptance='Unchanged ESS100/maxweight.05/MCsd.2, independent repeat, waveform rate and continuous-strength calibration',
        caution='Estimated cross-fit gains are not convergence. Pilot target normalizations are uncertain.',
        hashes={n: se.sha(se.ROOT/n) for n in names}))
    print(json.dumps(dict(status='FITTED_NATIVE_SOURCE_PROPOSAL', selected=selected['id'],
        training_weight_ESS=proposal['training_weight_ESS'])), flush=True)


def oracle():
    runner.STAGE = STAGE
    proposal = runner.check()
    s = tp.draw(proposal, 32768, 130921)
    good, u, jac, y, logq = (s[k] for k in ('inside', 'unit_cube', 'forward_Jacobian', 'transport_y', 'logq'))
    w = np.zeros(len(good)); w[good] = np.exp(-logq[good])
    values = np.column_stack([w]+[w*u[:, i] for i in range(6)]+[w*u[:, i]**2 for i in range(6)])
    expected = np.array([1.]+[.5]*6+[1/3]*6)
    means = values.mean(axis=0); errors = values.std(axis=0, ddof=1)/np.sqrt(len(w))
    z = np.abs(means-expected)/errors
    terms = [np.full(int(good.sum()), np.log(proposal['defensive_weight']))]
    for c in proposal['components']:
        terms.append(np.log(c['weight'])+multivariate_t.logpdf(y[good], loc=c['mean'], shape=c['shape'], df=proposal['df'])+np.log(jac[good]))
    density_error = float(np.max(np.abs(logsumexp(np.column_stack(terms), axis=1)-logq[good])))
    passed = bool(z.max() < 5 and density_error <= 1e-12)
    output = dict(status='PASS_TRANSPORT_PROPOSAL_MOMENTS' if passed else 'PROPOSAL_MOMENTS_FAILED',
        N=len(w), seed=130921, inside=int(good.sum()), means=means.tolist(), MC_standard_errors=errors.tolist(),
        expected=expected.tolist(), max_standardized_error=float(z.max()), direct_density_error=density_error,
        scientific_acceptance=False, registration_sha256=se.sha(STAGE/'REGISTRATION.json'))
    se.write(STAGE/'PROPOSAL_ORACLE.json', output)
    print(json.dumps(output), flush=True)
    if not passed:
        raise ValueError('Native proposal normalization oracle failed')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('command', choices=['diagnostic', 'fit', 'oracle', 'run'])
    p.add_argument('--draws', type=int, default=16384); p.add_argument('--seed', type=int, default=130922)
    p.add_argument('--processes', type=int, default=4)
    args = p.parse_args()
    if args.command == 'diagnostic': diagnostic()
    elif args.command == 'fit': fit()
    elif args.command == 'oracle': oracle()
    else:
        runner.STAGE = STAGE
        runner.run(args)
