"""Prepared E4/E5 deterministic diagnostics. CLI science requires principal E2 activation.

No campaign, random sampling, PE, waveform generator, network or test-strain reader.
The analytical damped-mode Fisher and archived-posterior diagnostics run only after
the CLI gate. Importing this file defines functions but does not run science.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import re
import time
from datetime import datetime, timezone

O = Path(__file__).resolve().parent
B = O.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite JSON: ' + value)
    result = json.loads(Path(path).read_text(encoding='utf-8-sig'),
                        object_pairs_hook=pairs, parse_constant=invalid)
    def finite(value):
        if isinstance(value, float):
            require(math.isfinite(value), 'Nonfinite JSON number')
        elif isinstance(value, dict):
            for entry in value.values():
                finite(entry)
        elif isinstance(value, list):
            for entry in value:
                finite(entry)
    finite(result)
    return result


def check_inputs(manifest):
    for item in manifest['files']:
        path = B / item['path']
        require(path.resolve().is_relative_to(B.parent.resolve()), 'Input outside task house')
        require(path.is_file(), 'Missing input: ' + str(path))
        require(path.stat().st_size == item['bytes'] and sha(path) == item['sha256'],
                'Changed input: ' + str(path))


def gate(authorization_path):
    """Before scipy/h5py import, HDF values, numerical predictions or mkdir."""
    auth = load(authorization_path)
    require(auth.get('status') == 'AUTHORIZED_BY_PRINCIPAL_AFTER_E2', 'No principal activation')
    require(auth.get('allowed_task') == 'E4_E5_DETERMINISTIC_ARCHIVED_CALIBRATION_ONLY', 'Scope')
    require(auth.get('new_test_data_allowed') is False, 'Test-data permission must remain false')
    for name in ['PLAN.json', 'INPUT_MANIFEST.json', 'SCHEMA.json', 'deterministic_e4_e5.py']:
        require(auth.get('package_sha256', {}).get(name) == sha(O / name), 'Package pin: ' + name)
    registration = Path(auth['E2_registration_path']).resolve()
    witness = Path(auth['E2_tunnel_witness_path']).resolve()
    require(registration.is_relative_to(B.resolve()) and not registration.is_relative_to(O), 'E2 path')
    tunnel = (B.parent / 'TUNEL/DO_CHATGPT').resolve()
    require(witness.is_relative_to(tunnel), 'Witness outside outgoing tunnel')
    require(sha(registration) == auth['E2_registration_sha256'], 'E2 hash')
    require(sha(witness) == auth['E2_tunnel_witness_sha256'], 'Witness hash')
    reg = load(registration)
    require(reg.get('e4_e5_preparation_pins') == auth['package_sha256'], 'E2 must pin exact preparation')
    require(auth['E2_registration_sha256'] in witness.read_text(encoding='utf-8-sig'), 'Witness omits E2 pin')
    require(auth.get('run_id') and re.fullmatch(r'[a-z][a-z0-9_]{0,47}', auth['run_id']), 'Run name')
    plan = load(O / 'PLAN.json')
    manifest = load(O / 'INPUT_MANIFEST.json')
    require(plan['input_manifest_sha256'] == sha(O / 'INPUT_MANIFEST.json'), 'Plan/input pin')
    check_inputs(manifest)
    budget = load(B / 'bis/PART_B_BUDGET_START.json')
    require(datetime.now(timezone.utc) < datetime.fromisoformat(budget['hard_deadline_utc']), 'Budget expired')
    target = O / 'runs' / auth['run_id']
    require(target.resolve().is_relative_to(O.resolve()), 'Output escaped through symlink')
    require(not target.exists(), 'Existing run; no overwrite')
    return auth, plan, manifest, target


def load_prediction():
    import importlib.util
    spec = importlib.util.spec_from_file_location('pinned_e4_prediction', B / 'tgl_ringdown_prediction.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def qnm_functions():
    import numpy as np
    from scipy.interpolate import CubicSpline
    grid = load(B / 'QNM_GRID.json')
    return {m: CubicSpline(grid['spins'], np.asarray(grid['modes'][m]['real']) +
                           1j * np.asarray(grid['modes'][m]['imag']), extrapolate=False)
            for m in ['220', '440']}


def forecast(plan, prediction, qnms):
    """GR local Fisher; isolated mode SNR, not transported IMR/network SNR."""
    import numpy as np
    cfg = plan['E4']['fisher']
    ref = cfg['reference_source']
    q = prediction.kerr_mode(ref['mass_detector_Msun'], ref['spin'], mode=(4, 4, 0),
                            qnm_dimensionless=complex(qnms['440'](ref['spin'])))
    f = np.arange(cfg['f_min_Hz'], cfg['f_max_Hz'] + cfg['df_Hz'] / 2, cfg['df_Hz'])
    d, fr = 1 / q['tau_gr_s'], q['f_gr_hz']
    zm, zp = d + 2j * np.pi * (f - fr), d + 2j * np.pi * (f + fr)
    h = .5 * (1 / zm + 1 / zp)
    deriv = [h, .5j * (1 / zm - 1 / zp),
             .5 * (2j * np.pi * fr / zm**2 - 2j * np.pi * fr / zp**2),
             +.5 * d * (1 / zm**2 + 1 / zp**2)]  # dH/d(delta_tau) at GR
    predictions = {}
    for reading in plan['readings']:
        if reading in ['R-PROP', 'R-RAIZ-COHERENT']:
            predictions[reading] = None
        else:
            predictions[reading] = prediction.prediction(ref['mass_detector_Msun'], ref['spin'], reading,
                redshift=ref['redshift'], mode=(4, 4, 0),
                qnm_dimensionless=complex(qnms['440'](ref['spin'])))
    rows, noise_configs = [], []
    for psd in load(B / 'FISHER_INPUTS.json')['psds']:
        raw = np.loadtxt(B / 'cache/psd' / psd['filename'])
        require(raw.ndim == 2 and raw.shape[1] >= 2 and np.isfinite(raw[:, :2]).all(), 'PSD array')
        require(np.all(np.diff(raw[:, 0]) > 0), 'PSD frequencies')
        positive = raw[(raw[:, 0] > 0) & (raw[:, 1] > 0)]
        require(positive[0, 0] <= f[0] and positive[-1, 0] >= f[-1], 'PSD extrapolation forbidden')
        require(psd['kind'] in ['ASD', 'PSD'], 'PSD convention')
        sn = positive[:, 1] ** (2 if psd['kind'] == 'ASD' else 1)
        curve = np.exp(np.interp(np.log(f), np.log(positive[:, 0]), np.log(sn)))
        norm = math.sqrt(float(4 * np.trapezoid(abs(h)**2 / curve, f)))
        noise_configs.append((psd, curve, norm))
    norm_o4 = next(norm for psd, curve, norm in noise_configs if psd['key'] == 'O4')
    for psd, curve, norm in noise_configs:
        def inner(a, b):
            return float(4 * np.trapezoid((a * b.conj()).real / curve, f))
        derivatives = [a / norm for a in deriv]
        gram = np.array([[inner(a, b) for b in derivatives] for a in derivatives])
        for profile, indices in [('FIXED_SOURCE_FREQUENCY', [0, 1]), ('FREE_FREQUENCY_FIXED_TAU_GR', [0, 1, 2])]:
            nuisance = gram[np.ix_(indices, indices)]
            require(np.linalg.cond(nuisance) < 1e12, 'Singular nuisance Gram')
            information = float(gram[3, 3] - gram[3, indices] @ np.linalg.solve(nuisance, gram[indices, 3]))
            require(math.isfinite(information) and information > 0, 'Nonpositive Fisher information')
            for reading in plan['readings']:
                for variant in plan['variants']:
                    pred = predictions[reading]
                    delta = None if pred is None else (0.0 if variant == 'ONLY_220_DEFORMED' else pred['delta_tau'])
                    for route in ['ISOLATED_440_GRID', 'AMPLITUDE_FIXA_INPUT']:
                        for anchor in cfg['isolated_440_snr_grid']:
                            gain = norm / norm_o4
                            rho = anchor if route == 'ISOLATED_440_GRID' else anchor * gain
                            sigma = 1 / (rho * math.sqrt(information))
                            z = None if delta is None else abs(delta) / sigma
                            zlog = None if delta is None else abs(math.log1p(delta)) / sigma
                            resolved = delta is not None and abs(delta) >= cfg['operational_delta_min'] and z > 0
                            rows.append(dict(reading=reading, variant=variant, psd=psd['key'], profile=profile,
                                snr_route=route, rho_440_used=rho,
                                rho_440_equal_per_PSD_INPUT=anchor if route == 'ISOLATED_440_GRID' else None,
                                rho_440_O4_anchor_INPUT=anchor if route == 'AMPLITUDE_FIXA_INPUT' else None,
                                common_Fourier_amplitude_INPUT=anchor / norm_o4 if route == 'AMPLITUDE_FIXA_INPUT' else None,
                                reference_mode_norm=norm, rho_gain_at_fixed_amplitude_vs_O4=gain,
                                snr_kind='ISOLATED_440_IN_SINGLE_REFERENCE_PSD_NOT_IMR_NETWORK',
                                delta_tau_440=delta, sigma_delta_tau_local_GR=sigma,
                                expected_local_z=z, log_coordinate_z_sensitivity_only=zlog,
                                N_expected_local_z5_proxy=25 / z**2 if resolved else None,
                                N_expected_local_z5_interpretation='N50_INPUT_E_z_EQUALS_5_KNOWN_GAUSSIAN_UNIT_VARIANCE',
                                N90_conditional=(5 + cfg['normal_90_quantile'])**2 / z**2 if resolved else None,
                                power_scope='INPUT one-sided Gaussian Z~N(sqrt(N)*z,1), known covariance, identical independent sources, no systematics; not calibrated null significance',
                                target_status='DERIVED_CONDITIONAL_GAUSSIAN' if resolved else 'OPEN_ZERO_SUBRESOLUTION_OR_NO_EXPONENTIAL',
                                calibrated_significance=None,
                                status='OPEN_NO_UNIQUE_EXPONENTIAL' if delta is None else
                                       ('ZERO_440_EFFECT_BY_CONSTRUCTION' if delta == 0 else 'DERIVED_CONDITIONAL_LOCAL_FISHER'),
                                reference_prediction=pred,
                                assumptions='Fixed source and GR spectral shape. Equal-rho route compares PSD shapes only; amplitude route transports INPUT O4 normalization, not measured GW250114 mode amplitude.'))
    require(len(rows) == len(plan['readings']) * len(plan['variants']) * 4 * 2 * 2 * len(cfg['isolated_440_snr_grid']), 'Forecast coverage')
    return rows


def support_at_zero(data, covariance):
    import numpy as np
    z = np.linalg.solve(np.linalg.cholesky(covariance), data)
    dist = np.sum(z * z, axis=0)
    weights = np.exp(-.5 * (dist - np.min(dist)))
    return {'kernel_effective_samples': float(weights.sum()**2 / (weights @ weights)),
            'within_two_kernel_sd': int(np.sum(dist <= 4))}


def gaussian_logzero(data):
    import numpy as np
    covariance = np.cov(data, ddof=1)
    mean = np.mean(data, axis=1)
    chol = np.linalg.cholesky(covariance)
    standardized = np.linalg.solve(chol, mean)
    return float(-len(mean) / 2 * math.log(2 * math.pi) - np.log(np.diag(chol)).sum() - .5 * (standardized @ standardized))


def archived_440(plan, prediction, qnms):
    """Paired residual density diagnostics, no 4D density or evidence promotion."""
    import numpy as np
    import h5py
    from scipy.stats import gaussian_kde
    from scipy.special import ndtr
    cfg = plan['E4']['posterior']
    with h5py.File(B / cfg['path'], 'r') as h:
        samples = h[cfg['label'] + '/posterior_samples'][()]
        for field, prior in cfg['prior_strings'].items():
            actual = h[cfg['label'] + '/priors/analytic/' + field][()]
            text = actual.flat[0].decode() if hasattr(actual, 'flat') else actual.decode()
            require(text == prior, 'Archived prior changed: ' + field)
    require(len(samples) == cfg['N'], 'Sample count')
    fields = ['domega220', 'dtau220', 'domega440', 'dtau440',
              'final_mass_non_evolved', 'final_spin_non_evolved', 'redshift']
    require(set(fields).issubset(samples.dtype.names), 'Required paired fields')
    require(all(np.isfinite(samples[n]).all() for n in fields), 'Nonfinite posterior')
    spin = samples['final_spin_non_evolved']
    require(np.all((spin >= 0) & (spin < .98)), 'Spin outside audited interpolation domain')
    rows, marginal_diagnostics = [], {}
    for mode in ['220', '440']:
        names = ['domega' + mode, 'dtau' + mode]
        data = np.vstack([samples[n] for n in names])
        base = gaussian_kde(data)
        edges = []
        for axis, name in enumerate(names):
            lo, hi = cfg['bounds'][name]
            require(np.all((data[axis] >= lo) & (data[axis] <= hi)), 'Posterior outside prior')
            h = math.sqrt(base.covariance[axis, axis])
            edges.append({'field': name, 'bounds': [lo, hi],
                'quantiles_05_50_95': np.quantile(data[axis], [.05, .5, .95]).tolist(),
                'sample_fraction_within_one_kernel_sd_of_edge': float(np.mean((data[axis] - lo < h) | (hi - data[axis] < h))),
                'marginal_KDE_mass_outside_original_prior': float(np.mean(ndtr((lo-data[axis])/h) + ndtr((data[axis]-hi)/h))),
                'boundary_correction_applied': False})
        marginal_diagnostics[mode] = edges
        base_gaussian = gaussian_logzero(data)
        base_kdes = {mult: gaussian_kde(data, bw_method=base.scotts_factor() * mult) for mult in cfg['bandwidth_multipliers']}
        for reading in plan['readings']:
            if reading in ['R-PROP', 'R-RAIZ-COHERENT']:
                rows.append(dict(mode=mode, reading=reading, status='OPEN_NO_UNIQUE_EXPONENTIAL', estimators=None, lnB=None))
                continue
            dimless = qnms[mode](spin)
            shifts = np.array([prediction.prediction(float(m), float(s), reading, redshift=float(z),
                mode=tuple(int(c) for c in mode), qnm_dimensionless=complex(w))['delta_tau']
                for m, s, z, w in zip(samples['final_mass_non_evolved'], spin, samples['redshift'], dimless)])
            lo, hi = cfg['bounds']['dtau' + mode]
            require(np.all((shifts > lo) & (shifts < hi)), 'Curve outside marginal prior')
            residual = data.copy()
            residual[1] -= shifts
            estimators = []
            for mult, original in base_kdes.items():
                fitted = gaussian_kde(residual, bw_method=original.factor)
                score = float(fitted.logpdf(np.zeros((2, 1)))[0] - original.logpdf(np.zeros((2, 1)))[0])
                estimators.append({'method': 'PAIRED_RESIDUAL_KDE2D', 'bandwidth_multiplier': mult,
                    'log_density_ratio_diagnostic': score, 'null_support': support_at_zero(data, original.covariance),
                    'curve_support': support_at_zero(residual, fitted.covariance)})
            estimators.append({'method': 'INDEPENDENT_FULL_MOMENT_GAUSSIAN2D_NO_KDE_BANDWIDTH',
                               'log_density_ratio_diagnostic': gaussian_logzero(residual) - base_gaussian})
            scores = [item['log_density_ratio_diagnostic'] for item in estimators]
            supported = all(e['null_support']['kernel_effective_samples'] >= cfg['ESS_min'] and
                            e['curve_support']['kernel_effective_samples'] >= cfg['ESS_min']
                            for e in estimators if 'null_support' in e)
            rows.append(dict(mode=mode, reading=reading,
                status='NONBLIND_CONDITIONAL_DENSITY_DIAGNOSTIC' if supported else 'OPEN_LOCAL_SUPPORT',
                estimators=estimators, estimator_range=[min(scores), max(scores)],
                sign_stable_across_estimators=(min(scores) > 0 or max(scores) < 0),
                predicted_shift_quantiles_05_50_95=np.quantile(shifts, [.05, .5, .95]).tolist(),
                lnB=None, calibrated_evidence=False, prior_density_ratio_for_deviation_coordinates_only=1.0,
                global_nuisance_prior_contract='OPEN',
                physical_scope='Marginal sector with other mode kept as identically free nuisance; not joint 220+440 evidence'))
    require(len(rows) == 2 * len(plan['readings']), 'Posterior table coverage')
    return {'rows': rows, 'prior_boundary_diagnostics': marginal_diagnostics,
        'joint_220_440_lnB': None, 'joint_status': 'OPEN_NO_4D_KDE_EVIDENCE_NO_PRODUCT_OF_DEPENDENT_MARGINALS',
        'fixed_440_vs_free_440_robustness': plan['E4']['fixed_free_robustness'],
        'uncertainty': 'Estimator/bandwidth range is not a confidence interval; posterior correlations and prior edges remain; no bootstrap or chain-ESS certification'}


def information_table(plan):
    """Reexpress archived sample standard deviations; no posterior refitting."""
    source = load(B / 'bis/e0_core/DATASET.json')
    by_id = {r['product_id']: r for r in source['rows']}
    anchor = by_id['GWTC5:GW250114_082203']['stats']['df']['std_ddof1']
    outputs = []
    for population in plan['E5']['archived_information_populations']:
        ids = source['sets'][population]
        require(len(ids) == len(set(ids)), 'Duplicate product')
        rows = []
        for key in ids:
            r = by_id[key]
            sigma = r['stats']['df']['std_ddof1']
            require(math.isfinite(sigma) and sigma > 0, 'Sigma')
            rows.append({'product_id': key, 'event': r['event'], 'sigma_df_archived_ddof1': sigma,
                         'relative_information_to_GW250114': (anchor / sigma)**4,
                         'source_posterior_sha256_declared_in_dataset': r['source_sha256']})
        total = sum(r['relative_information_to_GW250114'] for r in rows)
        for r in rows:
            r['information_fraction'] = r['relative_information_to_GW250114'] / total
        outputs.append({'population': population, 'rows': rows, 'N_GW250114_equivalent': total,
                        'statute': 'DERIVED_GAUSSIAN_LOCAL_VARIANCE_INFORMATION_PROXY_NONBLIND_CALIBRATION',
                        'new_test_population': False, 'sigma_sys': None, 'jitter_transfer': None})
    return outputs


def gaussian_profile_loglike(q, y, sigma, sigma_sys):
    """Exact heteroscedastic Gaussian INPUT model at q>=0; NOT population KDE."""
    import numpy as np
    y, sigma = np.asarray(y, float), np.asarray(sigma, float)
    require(y.ndim == 1 and sigma.shape == y.shape and len(y) >= 2, 'Shape')
    require(np.isfinite(y).all() and np.isfinite(sigma).all() and np.all(sigma > 0), 'Data')
    require(type(q) in (int, float) and math.isfinite(q) and q >= 0, 'q')
    require(type(sigma_sys) in (int, float) and math.isfinite(sigma_sys) and sigma_sys >= 0, 'sigma_sys')
    variance = sigma**2 + sigma_sys**2 + q
    mu = float(np.sum(y / variance) / np.sum(1 / variance))
    ll = float(-.5 * np.sum(np.log(2 * np.pi * variance) + (y-mu)**2 / variance))
    return ll, mu


def posterior_population_logscore(mu, sigma_total, paired_df_draws, uniform_prior_bounds):
    """Full-draw importance identity under an OPEN global likelihood/selection contract.

    Positive widths only: no fake finite-width substitution for the delta-function
    null. Does not fit nuisance, select events, infer evidence or calibrate p-values.
    """
    import numpy as np
    from scipy.special import logsumexp
    require(type(mu) in (int, float) and math.isfinite(mu), 'mu')
    require(type(sigma_total) in (int, float) and math.isfinite(sigma_total) and sigma_total > 0, 'Positive sigma_total')
    require(len(paired_df_draws) == len(uniform_prior_bounds) > 0, 'Prior coverage')
    terms = []
    for draws, bounds in zip(paired_df_draws, uniform_prior_bounds):
        draws = np.asarray(draws, float)
        lo, hi = bounds
        require(math.isfinite(lo) and math.isfinite(hi) and lo < hi, 'Uniform support')
        require(draws.ndim == 1 and len(draws) >= 2 and np.isfinite(draws).all(), 'Full posterior draws')
        require(np.all((draws >= lo) & (draws <= hi)), 'Draw outside prior')
        logpdf = -.5 * ((draws-mu)/sigma_total)**2 - math.log(sigma_total * math.sqrt(2*math.pi))
        terms.append(float(logsumexp(logpdf) - math.log(len(draws)) + math.log(hi-lo)))
    return {'conditional_logscore': sum(terms), 'event_terms': terms, 'statute': 'OPEN_UNCALIBRATED_POPULATION_CONTRACT',
            'selection_normalization': None, 'lnB': None, 'tail_support_certified': False}


def main():
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--authorization', type=Path)
    args = parser.parse_args()
    require(args.execute and args.authorization is not None, 'AWAITING_E2_AND_PRINCIPAL_ACTIVATION; no science run')
    auth, plan, manifest, target = gate(args.authorization)
    for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        os.environ[variable] = '1'
    import numpy as np
    import scipy
    import h5py
    prediction, qnms = load_prediction(), qnm_functions()
    result = {'schema_version': 1, 'status': 'NONBLIND_CONDITIONAL_DETERMINISTIC_DIAGNOSTICS',
        'utc': datetime.now(timezone.utc).isoformat(), 'authorization_sha256': sha(args.authorization),
        'E2_registration_sha256': auth['E2_registration_sha256'], 'plan_sha256': sha(O / 'PLAN.json'),
        'input_manifest_sha256': sha(O / 'INPUT_MANIFEST.json'), 'scientific_reading_selected': False,
        'versions': {'numpy': np.__version__, 'scipy': scipy.__version__, 'h5py': h5py.__version__},
        'thread_request': 1, 'E4_fisher': forecast(plan, prediction, qnms),
        'E4_archived_marginals': archived_440(plan, prediction, qnms),
        'E5_information': information_table(plan), 'E5_contract': plan['E5'],
        'new_PE': False, 'new_waveforms': False, 'new_test_data': False,
        'population_fit_executed': False, 'null_calibration_executed': False}
    result['performance'] = {'wall_seconds_through_computation': time.perf_counter() - start_wall,
                             'process_CPU_seconds_through_computation': time.process_time() - start_cpu,
                             'scope': 'Includes authorization/hash checks and imports; one process; thread count requested, not measured'}
    payload = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    check_inputs(manifest)
    require(datetime.now(timezone.utc) < datetime.fromisoformat(load(B / 'bis/PART_B_BUDGET_START.json')['hard_deadline_utc']), 'Budget expired')
    target.mkdir(parents=True, exist_ok=False)
    with (target / 'DETERMINISTIC_DIAGNOSTICS.json').open('xb') as stream:
        stream.write(payload)
    output_hash = sha(target / 'DETERMINISTIC_DIAGNOSTICS.json')
    receipt = {'status': 'COMPLETED_DETERMINISTIC_ARCHIVED_DIAGNOSTICS',
               'result_sha256': output_hash, 'plan_sha256': sha(O / 'PLAN.json'),
               'executor_sha256': sha(Path(__file__)), 'authorization_sha256': sha(args.authorization),
               'input_bytes_unchanged': True, 'wall_seconds_through_result_hash': time.perf_counter() - start_wall,
               'process_CPU_seconds_through_result_hash': time.process_time() - start_cpu,
               'clock_scope': 'Whole process from main entry through result write/hash, excludes final receipt write',
               'new_PE': False, 'new_MC': False, 'new_waveforms': False, 'new_test_data': False}
    with (target / 'RESULT_RECEIPT.json').open('xb') as stream:
        stream.write((json.dumps(receipt, indent=2, allow_nan=False) + '\n').encode('utf-8'))
    print(json.dumps({'path': str(target), 'sha256': output_hash}))


if __name__ == '__main__':
    main()
