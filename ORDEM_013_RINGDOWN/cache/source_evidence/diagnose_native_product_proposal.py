"""Test lower-dimensional proposals after SEOB's full6D adaptation failed.

Only proposal densities are compared on held-out, already computed source
likelihoods. This is not fresh evidence or a change of the physical source prior.
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
from diagnose_proposal_efficiency import posterior_weights, beta_fit, logq_for
from adapt_native_source_proposal import PILOT, DIAGNOSTIC

FOLDER = se.ROOT/'native_product_proposal_diagnostic'


def main():
    previous = json.loads((DIAGNOSTIC/'RESULT.json').read_bytes())
    if previous['prospective_refinement_allowed']:
        raise ValueError('This follow-up is conditioned on failure of the registered full6D diagnostic')
    result, u, logq, inside, values, stats = load_run(PILOT)
    registration = json.loads((DIAGNOSTIC/'REGISTRATION.json').read_bytes())
    folds = [np.array(v) for v in registration['folds']]
    with np.load(PILOT/'PROPOSALS.npz') as f:
        y, jac = (f[k].copy() for k in ('transport_y', 'forward_Jacobian'))
    FOLDER.mkdir(exist_ok=False)
    names = ['diagnose_native_product_proposal.py', 'diagnose_proposal_efficiency.py',
             'adapt_phase_source.py', 'native_proposal_crossfit/REGISTRATION.json',
             'native_proposal_crossfit/RESULT.json',
             'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json']
    se.write(FOLDER/'REGISTRATION.json', dict(status='REGISTERED_NATIVE_SPECTRAL_PRODUCT_DIAGNOSTIC',
        date_utc=datetime.now(timezone.utc).isoformat(), seed=130930,
        hypothesis='Pilot cannot learn six-dimensional nuisance correlations reliably; spectral2D times beta(cosi) times uniform other coordinates may generalize better',
        pooling=['mean', 'rms'], counts=[3, 6], inflation=[.5, 1., 2.], df=[5., 30.],
        retain_old_proposal=[False, True], selection='Maximum worst-fold10th-percentile gain, require >1 to propose production adaptation',
        warning='Adaptive diagnostic after previous failure, not an unbiased validation sample; fresh source evaluations and frozen tests still required',
        physical_prior_changed=False, hashes={n: se.sha(se.ROOT/n) for n in names}))
    rows = []
    for fold, held in enumerate(folds):
        train = folds[1-fold]
        pt = posterior_weights(values[train], logq[train])
        pe = posterior_weights(values[held], logq[held])
        good = inside[held]
        yy, jj, oq, pp = y[held][good], jac[held][good], logq[held][good], pe[good]
        models = []
        for method in ('mean', 'rms'):
            w = pt.mean(axis=1) if method == 'mean' else np.sqrt((pt*pt).mean(axis=1))
            w /= w.sum()
            yy_train, ww = y[train][inside[train]], w[inside[train]]
            beta = beta_fit(yy_train[:, 4], ww)
            for count in (3, 6):
                cs, history = weighted_fit(yy_train[:, :2], ww, count=count, floor=1e-5, seed=130930+100*fold+count)
                for inflation in (.5, 1., 2.):
                    for df in (5., 30.):
                        components = copy.deepcopy(cs)
                        for c in components:
                            c['weight'] *= .9/.7
                            c['shape'] = (np.array(c['shape'])*(inflation/2)).tolist()
                        model = dict(kind='spectral_product', family='SEOBNRv4HM', components=components,
                            beta_cosi=beta, defensive_weight=.1, df=df, inflation=inflation, method=method, count=count)
                        qnew = logq_for(model, yy, jj)
                        for retain in (False, True):
                            # Convex combination preserves 10% physical-prior
                            # defense: 7/9*(.1+.9new)+2/9*(.1+.9old).
                            density = np.logaddexp(np.log(7/9)+qnew, np.log(2/9)+oq) if retain else qnew
                            terms = pp*pp*np.exp(oq-density)[:, None]
                            gain = (pp*pp).sum(axis=0)/terms.sum(axis=0)
                            name = f'{method}_K{count}_inflate{inflation}_df{df}_retain{retain}'
                            rows.append(dict(id=name, fold=fold, gain_quantiles=np.quantile(gain, [0, .1, .5, .9, 1]).tolist(),
                                second_moment_max_contribution_quantiles=np.quantile(terms.max(axis=0)/terms.sum(axis=0), [.5, .9, 1]).tolist()))
                            models.append(dict(id=name, retain=retain, proposal=model))
        se.write(FOLDER/f'fold_{fold}.json', dict(proposals=models, rows=[r for r in rows if r['fold'] == fold]))
    ranking = []
    for name in sorted({r['id'] for r in rows}):
        group = [r for r in rows if r['id'] == name]
        ranking.append(dict(id=name, min_fold_gain10=min(r['gain_quantiles'][1] for r in group),
            min_fold_median_gain=min(r['gain_quantiles'][2] for r in group), rows=group))
    ranking.sort(key=lambda r: r['min_fold_gain10'], reverse=True)
    output = dict(status='NATIVE_PRODUCT_PROPOSAL_DIAGNOSTIC_ONLY', ranking=ranking,
        prospective_refinement_allowed=bool(ranking[0]['min_fold_gain10'] > 1),
        scientific_acceptance=False, physical_prior_changed=False,
        registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json', output)
    print(json.dumps(dict(status=output['status'], prospective_refinement_allowed=output['prospective_refinement_allowed'],
        candidates=len(ranking), top=[{k: v for k, v in r.items() if k != 'rows'} for r in ranking[:5]])), flush=True)


if __name__ == '__main__':
    main()
