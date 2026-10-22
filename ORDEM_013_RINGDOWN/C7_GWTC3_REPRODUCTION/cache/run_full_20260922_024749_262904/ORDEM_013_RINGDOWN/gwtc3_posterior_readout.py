"""GWTC-3 pSEOB220 comparison and GPS-based cross-release reconciliation.

Each release is a model/analysis alternative for overlapping events. Do not
multiply old and current likelihoods for the same strain. The legacy uniform
deformation-prior interpretation is explicit and tied to released configuration
and inspected LAL source documentation; original executable versions are absent.
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
from pathlib import Path
from datetime import datetime
import hashlib
import json
import math
import h5py
import lal
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from posterior_220_readout import ratio_pair
from catalog_220_readout import local_support, READINGS
from tgl_ringdown_prediction import prediction

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def event_gps(name):
    t = datetime.strptime(name, 'GW%y%m%d_%H%M%S')
    return float(lal.UTCToGPS(t.timetuple()))


def main():
    reg = json.loads((ROOT / 'REGISTRO_C4.json').read_bytes())
    regsha = sha(ROOT / 'REGISTRO_C4.json')
    if regsha not in (ROOT.parent / 'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md').read_text():
        raise ValueError('C4 registration changed')
    schema = json.loads((ROOT / 'C4_GWTC3_SCHEMA.json').read_bytes())
    current = json.loads((ROOT / 'C4_CATALOG_220.json').read_bytes())['rows']
    timestamps = {r['event']: event_gps(r['event']) for r in current}
    q = json.loads((ROOT / 'QNM_GRID.json').read_bytes())['modes']['220']
    interp = CubicSpline(q['spins'], np.array(q['real'])+1j*np.array(q['imag']), extrapolate=False)
    out = ROOT / 'cache/gwtc3_220'
    out.mkdir(exist_ok=True)
    deps = {name: sha(ROOT / name) for name in ['tgl_ringdown_prediction.py', 'QNM_GRID.json',
        'posterior_220_readout.py', 'catalog_220_readout.py', 'C4_GWTC3_SCHEMA.json']}
    rows = []
    for index, source in enumerate(schema['rows']):
        label, = source['labels']
        path = ROOT / source['path']
        if sha(path) != source['sha256']:
            raise ValueError('GWTC-3 source changed')
        cache = out / (Path(source['member']).stem + '.json')
        if cache.exists():
            old = json.loads(cache.read_bytes())
            if old['code_sha256'] != sha(Path(__file__)) or old['dependencies'] != deps:
                raise ValueError('Keep old calculation and inspect code/dependency changes')
            rows.append(old)
            continue
        text = label['source_text']
        if text['config_file/engine/qnmtest-parameters'] != ['domega220,dtau220']:
            raise ValueError('Legacy product does not jointly vary only the 220 deformation')
        bounds = {name: [float(text[f'config_file/engine/{name}-min'][0]),
                        float(text[f'config_file/engine/{name}-max'][0])] for name in ['domega220', 'dtau220']}
        with h5py.File(path, 'r') as h:
            s = h[label['label'] + '/posterior_samples'][()]
        spin_name = 'final_spin_non_evolved' if 'final_spin_non_evolved' in s.dtype.names else 'final_spin'
        mass_name = 'final_mass_non_evolved' if 'final_mass_non_evolved' in s.dtype.names else 'final_mass'
        spin, mass, redshift = s[spin_name], s[mass_name], s['redshift']
        data = np.vstack([s['domega220'], s['dtau220']])
        exact = interp(spin)
        if not np.all(np.isfinite(data)) or not np.all(np.isfinite(exact)):
            raise ValueError('Nonfinite posterior or uncovered QNM spin')
        time = float(np.median(s['geocent_time']))
        matched = [event for event, gps in timestamps.items() if abs(time-gps) < 1.]
        if len(matched) > 1:
            raise ValueError('Ambiguous cross-release GPS identity')
        utc = lal.GPSToUTC(int(time))
        timestamp_name = datetime(*utc[:6]).strftime('GW%y%m%d_%H%M%S')
        event = matched[0] if matched else timestamp_name
        rng = np.random.default_rng(13043400 + index)
        test = rng.choice(len(s), min(5000, len(s)//5), replace=False)
        train = np.setdiff1d(np.arange(len(s)), test)
        kd = gaussian_kde(data[:, train])
        hpd = float(np.mean(kd.logpdf(data[:, test]) >= kd.logpdf([0., 0.])[0]))
        hpd_se = math.sqrt(hpd*(1-hpd)/len(test))
        null_support = local_support(data)
        results = []
        for reading in READINGS:
            predictions = [prediction(float(m), float(a), reading, redshift=float(z),
                qnm_dimensionless=complex(w) if reading == 'R-MOD' else None)
                for m, a, z, w in zip(mass, spin, redshift, exact)]
            shift = np.array([p['delta_tau_ensemble_exact'] for p in predictions])
            if not bounds['domega220'][0] < 0 < bounds['domega220'][1] or np.any(
                    (shift <= bounds['dtau220'][0]) | (shift >= bounds['dtau220'][1])):
                raise ValueError('Constrained curve leaves the broad-prior support')
            central, marginal = ratio_pair(data, shift)
            moved = data.copy()
            moved[1] -= shift
            support = local_support(moved)
            robust = [ratio_pair(data, shift, bw)[0] for bw in reg['KDE']['bandwidth_robustness_multipliers']]
            boot = []
            if np.max(abs(shift)) > 1e-12:
                for _ in range(reg['KDE']['bootstrap_replicates']):
                    ix = rng.integers(0, len(s), len(s))
                    boot.append(ratio_pair(data[:, ix], shift[ix])[0])
            else:
                boot = [0.] * reg['KDE']['bootstrap_replicates']
            median = prediction(float(np.median(mass)), float(np.median(spin)), reading,
                redshift=float(np.median(redshift)),
                qnm_dimensionless=complex(interp(np.median(spin))) if reading == 'R-MOD' else None)
            gr_inside = hpd + 3*hpd_se < .95
            resolved = min(null_support['kernel_effective_samples'], support['kernel_effective_samples']) >= 100
            verdict = 'NOT_EXCLUDED'
            if all(x <= -math.log(100) for x in robust) and gr_inside and resolved:
                verdict = 'EXCLUDED_IN_READING'
            if not gr_inside:
                verdict = 'INCONCLUSIVE_SYSTEMATICS'
            if not resolved:
                verdict = 'INCONCLUSIVE_DENSITY_SUPPORT'
            comparison = None
            if matched:
                prior_result = next(r for r in current if r['event'] == event)
                newer = next(r for r in prior_result['rows'] if r['reading'] == reading)
                comparison = dict(current_lnB=newer['lnB'], old_minus_current_lnB=central-newer['lnB'],
                    same_data_alternative_models=True, do_not_multiply=True)
            results.append(dict(reading=reading, lnB_conditional_uniform_prior=central,
                lnB_tau_marginal=marginal, lnB_bandwidth=robust,
                bootstrap_N=len(boot), lnB_bootstrap_025_50_975=np.quantile(boot,[.025,.5,.975]).tolist(),
                median_prediction=median, shift_05_50_95=np.quantile(shift,[.05,.5,.95]).tolist(),
                gamma_over_omega_05_50_95=np.quantile([p['gamma_over_omega'] for p in predictions],[.05,.5,.95]).tolist(),
                correction_over_sigma=abs(median['delta_tau'])/float(np.std(data[1],ddof=1)),
                z_tau_gaussian_diagnostic=(float(np.median(data[1]))-median['delta_tau'])/float(np.std(data[1],ddof=1)),
                support=support, verdict=verdict, current_comparison=comparison))
        row = dict(event=event, legacy_member=source['member'], label=label['label'], N=len(s),
            source_sha256=source['sha256'], code_sha256=sha(Path(__file__)), dependencies=deps,
            median_GPS=time, mapped_current_event=matched[0] if matched else None,
            mapping='Unique current event within 1 s of released geocenter posterior median; otherwise UTC-derived label',
            timestamp_only_label=not bool(matched), prior_bounds=bounds, prior_density_ratio=1.,
            prior_scope='Conditional on independent uniform deformation priors, matched nuisance priors; bounds read from release; LAL uniform registration inspected in source documentation',
            original_executable_version=text.get('version'),
            remnant_fields=dict(mass=mass_name,spin=spin_name), remnant_scope='Released derived remnant; original postprocessing fit version unavailable',
            GR_HPD_content=hpd, GR_HPD_MC_se=hpd_se, GR_support=null_support,
            quantiles={k:np.quantile(v,[.05,.5,.95]).tolist() for k,v in
                [('df220',data[0]),('dtau220',data[1]),('spin',spin),('mass_detector',mass),('redshift',redshift)]}, rows=results)
        atomic_json(cache,row)
        rows.append(row)
        print(json.dumps(dict(event=event,overlap=bool(matched),N=len(s),GR_HPD=hpd,
            lnB={r['reading']:r['lnB_conditional_uniform_prior'] for r in results})),flush=True)
    if len({r['event'] for r in rows}) != len(rows):
        raise ValueError('Duplicate event inside older release')
    overlap=[r['event'] for r in rows if r['mapped_current_event']]
    unique=[r['event'] for r in rows if not r['mapped_current_event']]
    combined=[dict(reading=reading,lnB_separate_GWTC3_18_event_sum=sum(
        next(x for x in r['rows'] if x['reading']==reading)['lnB_conditional_uniform_prior'] for r in rows),
        verdict='PENDING_SEPARATE_CATALOG_GR_HPD',not_combined_with_current=True) for reading in READINGS]
    atomic_json(ROOT/'C4_GWTC3_220.json',dict(status='NONBLIND_LEGACY_220_POSTERIOR_COMPARISON',
        registration_sha256=regsha,source_archive_sha256=schema['archive_sha256'],N_events=len(rows),
        duplicate_reconciliation=dict(current_events=len(current),overlap=overlap,older_only=unique,
            union_distinct_events=len(current)+len(unique),strategy='Current analysis preferred on overlap; no heterogeneous union evidence calculated; release-selection differences remain explicit'),
        prior_semantics_source='https://lscsoft.docs.ligo.org/lalsuite/lalinference/_l_a_l_inference_init_c_b_c_8c_source.html',
        damping_convention_source='https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c.html',
        limitation='Source documentation establishes uniform registration and fractional damping-time interpretation; legacy HDF5 lacks executable version. Ratios explicitly conditional on that convention. No new PE or physical model selection.',
        rows=rows,catalog=combined))


if __name__ == '__main__':
    main()
