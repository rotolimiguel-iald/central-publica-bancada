"""Separate GWTC-3 common-deformation control; never pool repeated events.

NONBLIND diagnostic under the released independent uniform deformation-prior
interpretation. The original sampler version is unavailable. A product of KDEs
is a conditional credible-region diagnostic, not an injection calibration.
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
from pathlib import Path
import hashlib
import json
import math
import h5py
import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import logsumexp
from combine_catalog import weighted_quantile
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def main():
    target = ROOT / 'C4_GWTC3_PUBLISHED_COMBINATION.json'
    if target.exists():
        raise FileExistsError('Preserve existing diagnostic; use a fresh reproduction directory')
    catalog = json.loads((ROOT / 'C4_GWTC3_220.json').read_bytes())
    selection = json.loads((ROOT / 'C4_GWTC3_SELECTION.json').read_bytes())
    if hashlib.sha256((ROOT/selection['source_path']).read_bytes()).hexdigest() != selection['source_sha256']:
        raise ValueError('Published selection source changed')
    catalog['rows'] = [r for r in catalog['rows'] if r['event'] in selection['selected_events']]
    if len(catalog['rows']) != len(selection['selected_events']):
        raise ValueError('Selected event missing from release')
    schema = json.loads((ROOT / 'C4_GWTC3_SCHEMA.json').read_bytes())
    data, bounds = {}, {}
    for row in catalog['rows']:
        source = next(s for s in schema['rows'] if s['member'] == row['legacy_member'])
        path = ROOT / source['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['source_sha256']:
            raise ValueError('Changed source posterior')
        with h5py.File(path, 'r') as h:
            samples = h[row['label'] + '/posterior_samples'][()]
        data[row['event']] = np.vstack([samples['domega220'], samples['dtau220']])
        bounds[row['event']] = np.array([row['prior_bounds'][k] for k in ['domega220', 'dtau220']])
    events = list(data)
    support = np.array([np.max([bounds[k][:, 0] for k in events], axis=0),
                        np.min([bounds[k][:, 1] for k in events], axis=0)])
    if not np.all((support[0] < 0) & (support[1] > 0)):
        raise ValueError('Null is outside common prior support')
    controls = []
    for bw, count, seed in [(1.,4096,130435), (1.,8192,130436), (.7,4096,130437), (1.4,4096,130438)]:
        densities = {k: gaussian_kde(v, bw_method=lambda kde: kde.scotts_factor()*bw) for k,v in data.items()}
        proposal = densities['GW150914_095045']
        points = proposal.resample(count, seed=seed)
        logs = np.zeros(count)
        null = 0.
        for kde in densities.values():
            logs += kde.logpdf(points)
            null += float(kde.logpdf([0.,0.])[0])
        valid = np.all((points > support[0, :, None]) & (points < support[1, :, None]), axis=0)
        logs[~valid] = -np.inf
        weights = np.exp(logs-proposal.logpdf(points)-logsumexp(logs-proposal.logpdf(points)))
        ess = float(1/np.sum(weights**2))
        indicators = (logs >= null).astype(float)
        content = float(weights @ indicators)
        se = float(np.sqrt(np.sum(weights**2*(indicators-content)**2)))
        row = dict(bandwidth=bw, draws=count, seed=seed, N_events=len(events),
            proposal='GW150914_095045 posterior KDE', importance_ESS=ess,
            prior_support=support.tolist(), points_outside_support=int(np.sum(~valid)),
            GR_HPD_content=content, MC_standard_error=se,
            GR_inside_95=bool(content+3*se < .95), GR_outside_95=bool(content-3*se > .95),
            posterior_quantiles={name:weighted_quantile(points[i],weights) for i,name in enumerate(['df220','dtau220'])})
        controls.append(row)
        print(json.dumps(row), flush=True)
    gr_safe = all(c['GR_inside_95'] and c['importance_ESS'] > 500 for c in controls)
    gr_out = any(c['GR_outside_95'] and c['importance_ESS'] > 500 for c in controls)
    results = []
    for original in catalog['catalog']:
        reading = original['reading']
        lines = [next(r for r in event['rows'] if r['reading'] == reading) for event in catalog['rows']]
        robust = np.sum([r['lnB_bandwidth'] for r in lines], axis=0)
        resolved = all(min(r['support']['kernel_effective_samples'], event['GR_support']['kernel_effective_samples']) >= 100
                       for event,r in zip(catalog['rows'],lines))
        if gr_out:
            verdict = 'INCONCLUSIVE_SYSTEMATICS'
        elif not gr_safe:
            verdict = 'INCONCLUSIVE_GR_REGION_OR_MC'
        elif not resolved:
            verdict = 'INCONCLUSIVE_DENSITY_SUPPORT'
        elif np.all(robust <= -math.log(100)):
            verdict = 'EXCLUDED_IN_READING__CONDITIONAL_SECTOR_ONLY'
        else:
            verdict = 'NOT_EXCLUDED'
        results.append(dict(reading=reading, lnB=sum(r['lnB_conditional_uniform_prior'] for r in lines),
            lnB_bandwidth=robust.tolist(), lnB_tau_marginal=sum(r['lnB_tau_marginal'] for r in lines),
            individual_event_density_support=resolved, verdict=verdict))
    hashes = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
              ['combine_gwtc3.py','combine_catalog.py','C4_GWTC3_220.json','C4_GWTC3_SCHEMA.json','C4_GWTC3_SELECTION.json']}
    atomic_json(target,dict(status='NONBLIND_SEPARATE_GWTC3_CONDITIONAL_220_SECTOR',
        selected_events=events, N_events=len(events), selection=selection,
        input_sha256=hashes, common_deformation_GR_diagnostics=controls, catalog=results,
        duplicate_reconciliation=catalog['duplicate_reconciliation'],
        combined_with_current_release=False,
        limitations=['Uniform prior convention conditional on released configuration and inspected later source; original executable version missing',
                     'KDE smoothing and waveform systematics; MC intervals do not include those systematics',
                     'This is not a Bayes factor for a uniquely specified full TGL theory',
                     'No frequentist significance follows from this diagnostic']))
    print(json.dumps(dict(catalog=results)), flush=True)


if __name__ == '__main__':
    main()
