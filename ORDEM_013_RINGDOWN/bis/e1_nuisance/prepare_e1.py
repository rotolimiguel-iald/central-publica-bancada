"""E1 design implementation. UNEXECUTED; explicit later authorization required.

Outputs conditional posterior-density diagnostics, never calibrated tests/Bayes
factors. No pickle, waveform, PE, posterior downloads or producer imports.
"""
import argparse
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
READINGS = ('GR', 'R-A', 'R-B', 'R-MOD', 'R-RAIZ-0', 'R-RAIZ-EP4',
            'R-RAIZ-REST', 'R-LIN', 'R-GLOBAL')
OPEN_READINGS = {'R-RAIZ-COHERENT': 'Occupation and fitted window missing; no universal dtau',
                 'R-PROP': 'Propagation is not a local ringdown dtau'}
START = None
LIMIT_SECONDS = 900
DEADLINE = None


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def within_root(name):
    path = Path(name)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Path outside authorized Chatgpt root')
    return path


def check_pin(path, expected):
    actual = sha(path)
    if actual != expected:
        raise ValueError(f'Hash mismatch: {path}')
    return actual


def clock_guard():
    if DEADLINE is not None and dt.datetime.now(dt.timezone.utc) >= DEADLINE:
        raise TimeoutError('Authorization/Part B deadline reached')
    if START is not None and time.monotonic() - START > LIMIT_SECONDS:
        raise TimeoutError('Bounded E1 allowance exceeded; no automatic continuation')


def publish_new(path, value):
    """Publish complete bytes exclusively; never replace an existing artifact."""
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    temp = path.with_name(path.name + '.pending')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(raw):
        raise OSError('Incomplete temporary output retained')
    os.link(temp, path)  # Atomic no-overwrite. Failure preserves .pending.
    temp.unlink()


def authorize(args):
    global DEADLINE
    if not args.execute or not args.authorization:
        raise PermissionError('DESIGN ONLY: later E0-sealed authorization is required')
    manifest_path = HERE / 'DESIGN_MANIFEST.json'
    manifest = read_json(manifest_path)
    auth_path = within_root(args.authorization)
    auth = read_json(auth_path)
    required = {'status': 'E0_SEALED_E1_AUTHORIZED', 'approved_by_role': 'principal_agent',
                'design_manifest_sha256': sha(manifest_path)}
    for key, value in required.items():
        if auth.get(key) != value:
            raise PermissionError(f'Authorization field not satisfied: {key}')
    seal = within_root(auth['sealed_E0_path'])
    check_pin(seal, auth['sealed_E0_sha256'])
    for row in manifest['files']:
        check_pin(within_root(row['path']), row['sha256'])
    budget = read_json(BASE / 'bis/PART_B_BUDGET_START.json')
    # The date is part of this design, not an inferred renewal of the budget.
    deadline = dt.datetime.fromisoformat(auth['expires_utc'].replace('Z', '+00:00'))
    hard = dt.datetime.fromisoformat(budget['hard_deadline_utc'])
    now = dt.datetime.now(dt.timezone.utc)
    if deadline.tzinfo is None or now >= min(deadline, hard):
        raise PermissionError('Authorization or Part B budget expired')
    DEADLINE = min(deadline, hard)
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', args.tag):
        raise ValueError('Unsafe output tag')
    destination = HERE / 'runs' / args.tag
    if destination.exists():
        raise FileExistsError(destination)
    return manifest, auth_path, budget, destination


def uniform_literal(text):
    """Parse only the two numerical bounds; never evaluate a prior expression."""
    node = ast.parse(text.strip(), mode='eval').body
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != 'Uniform':
        raise ValueError('Expected a literal Uniform declaration')
    if node.args or any(k.arg is None for k in node.keywords):
        raise ValueError('Positional/dynamic prior arguments are unsupported')
    values = {}
    for keyword in node.keywords:
        if keyword.arg in values:
            raise ValueError('Duplicate prior argument')
        values[keyword.arg] = ast.literal_eval(keyword.value)
    low, high = float(values['minimum']), float(values['maximum'])
    if not (math.isfinite(low) and math.isfinite(high) and low < high):
        raise ValueError('Invalid Uniform bounds')
    return low, high


def stored_text(dataset):
    raw = dataset[()]
    values = raw.ravel().tolist() if hasattr(raw, 'ravel') else [raw]
    return '\n'.join(v.decode('utf-8') if isinstance(v, bytes) else str(v) for v in values)


def verify_uniform(group, name):
    declarations = []
    analytic = f'priors/analytic/{name}'
    if analytic in group:
        declarations.append((analytic, stored_text(group[analytic])))
    for key in ('config_file/config/prior-dict', 'config_file/config/prior_dict'):
        if key in group:
            text = stored_text(group[key])
            for match in re.finditer(r'\b' + re.escape(name) + r'\s*=\s*(Uniform\([^)]*\))', text):
                declarations.append((key, match.group(1)))
    if not declarations:
        raise ValueError(f'Uniform declaration missing: {name}')
    bounds = [uniform_literal(text) for _, text in declarations]
    if len(set(bounds)) != 1:
        raise ValueError(f'Conflicting priors: {name}')
    return dict(bounds=list(bounds[0]), declarations=[dict(path=p, text=t) for p, t in declarations],
                status='UNIFORM_MARGINAL_DECLARATION_VERIFIED__JOINT_FACTORIZATION_OPEN')


class Density:
    """Fullsample Gaussian KDE: linear binning/FFT, checked against direct sums."""
    def __init__(self, samples, bandwidth_factor, support):
        self.u = samples
        self.h = float(np.std(samples, ddof=1) * len(samples)**(-0.2) * bandwidth_factor)
        if not math.isfinite(self.h) or self.h <= 0:
            raise ValueError('Degenerate KDE bandwidth')
        self.support = support
        self.mean = float(np.mean(samples))
        self.variance = float(np.var(samples, ddof=1))
        controls = np.quantile(samples, np.linspace(.01, .99, 17))
        direct = np.array([self.direct(float(q))[0] for q in controls])
        for resolution in (16, 32, 64):
            clock_guard()
            lower, upper = float(np.min(samples) - 8*self.h), float(np.max(samples) + 8*self.h)
            count = int(math.ceil((upper-lower)/(self.h/resolution))) + 1
            if count > 131072:
                raise ValueError('KDE grid cap exceeded; no silent coarsening')
            self.grid = np.linspace(lower, upper, count)
            dx = float(self.grid[1]-self.grid[0])
            pos = (samples-lower)/dx
            left = np.floor(pos).astype(int)
            frac = pos-left
            mass = np.bincount(left, weights=1-frac, minlength=count)
            mass += np.bincount(left+1, weights=frac, minlength=count)
            radius = int(math.ceil(8*self.h/dx))
            offset = np.arange(-radius, radius+1)*dx
            kernel = np.exp(-.5*(offset/self.h)**2)/(self.h*math.sqrt(2*math.pi))
            pdf = fftconvolve(mass/len(samples), kernel, mode='same')
            self.integral = float(np.sum(pdf)*dx)
            if abs(self.integral-1) > 1e-6:
                raise ValueError('KDE normalization failure')
            self.interpolator = PchipInterpolator(self.grid, pdf, extrapolate=False)
            approx = np.array([self.logpdf(float(q)) for q in controls])
            self.max_control_log_error = float(np.max(np.abs(approx-direct)))
            self.resolution = resolution
            if self.max_control_log_error <= .002:
                break
        else:
            raise ValueError('FFT versus direct KDE control failed')

    def logpdf(self, point):
        value = float(self.interpolator(point))
        if not math.isfinite(value) or value <= 0:
            return -math.inf
        return math.log(value)

    def direct(self, point):
        clock_guard()
        scaled = (self.u-point)/self.h
        exponents = -.5*scaled**2
        shift = float(np.max(exponents))
        weights = np.exp(exponents-shift)
        total = float(np.sum(weights))
        weights /= total
        first = float(np.dot(weights, scaled))
        second = float(np.dot(weights, scaled*scaled))
        logpdf = shift+math.log(total)-math.log(len(self.u)*self.h*math.sqrt(2*math.pi))
        return logpdf, first/self.h, (second-first*first-1)/(self.h*self.h)


def fit(densities, x, widths):
    """Free intercept/slope only. Gaussian comparator does not replace KDE."""
    if len(x) < 5 or float(np.std(x)) < 1e-12:
        return dict(status='NAO_PAGO_NOT_IDENTIFIABLE', n=len(x))
    center, scale = float(np.mean(x)), float(np.std(x))
    design = np.column_stack((np.ones(len(x)), (x-center)/scale))
    transform = np.array([[1, -center/scale], [0, 1/scale]])
    y = np.array([d.mean for d in densities])
    variances = np.array([d.variance for d in densities])
    information = design.T @ (design/variances[:, None])
    if np.linalg.cond(information) > 1e10:
        return dict(status='NAO_PAGO_ILL_CONDITIONED', n=len(x))
    gcov = np.linalg.inv(information)
    seed = gcov @ (design.T @ (y/variances))
    lows = np.array([max(d.support[0], d.grid[0]+d.h) for d in densities])
    highs = np.array([min(d.support[1], d.grid[-1]-d.h) for d in densities])
    if np.any(lows >= highs):
        return dict(status='NAO_PAGO_EMPTY_EMPIRICAL_SUPPORT', n=len(x))

    def objective(theta):
        clock_guard()
        query = design @ theta
        if np.any(query <= lows) or np.any(query >= highs):
            return 1e100
        values = [d.logpdf(float(q)) for d, q in zip(densities, query)]
        return -float(np.sum(values)) if np.all(np.isfinite(values)) else 1e100

    constraints = LinearConstraint(design, lows+1e-9, highs-1e-9)
    results = []
    for shift in (np.zeros(2), np.array([.5, 0.]), np.array([-.5, 0.]),
                  np.array([0., .5]), np.array([0., -.5])):
        initial = seed + shift*np.sqrt(np.diag(gcov))
        result = minimize(objective, initial, method='SLSQP', constraints=constraints,
                          options={'ftol': 1e-9, 'maxiter': 150})
        if result.success and math.isfinite(result.fun) and result.fun < 1e99:
            results.append(result)
    if not results:
        return dict(status='NAO_PAGO_OPTIMIZATION', n=len(x))
    optimum = min(results, key=lambda r: r.fun)
    theta = optimum.x
    query = design @ theta
    boundary_h = min(float(min(q-low, high-q)/d.h)
                     for d, q, low, high in zip(densities, query, lows, highs))
    if boundary_h < 3:
        return dict(status='NAO_PAGO_PRIOR_OR_GRID_BOUNDARY', n=len(x), boundary_distance_h=boundary_h)
    exact = np.array([d.direct(float(q)) for d, q in zip(densities, query)])
    errors = np.abs(exact[:, 0]-[d.logpdf(float(q)) for d, q in zip(densities, query)])
    hessian = -(design.T @ (design*exact[:, 2, None]))
    gradient = design.T @ exact[:, 1]
    if float(np.max(errors)) > .002 or np.min(np.linalg.eigvalsh(hessian)) <= 0:
        return dict(status='NAO_PAGO_DIRECT_CONTROL_OR_NONCONCAVE', n=len(x),
                    max_direct_log_error=float(np.max(errors)))
    covariance = np.linalg.inv(hessian)
    newton_distance = float(math.sqrt(max(0, gradient @ covariance @ gradient)))
    if newton_distance > .05:
        return dict(status='NAO_PAGO_DIRECT_STATIONARITY', n=len(x), newton_distance=newton_distance)
    parameters = transform @ theta
    localcov = transform @ covariance @ transform.T
    gaussian = transform @ seed
    gaussian_cov = transform @ gcov @ transform.T
    stderr = np.sqrt(np.diag(localcov))
    return dict(status='CONDITIONAL_DENSITY_DIAGNOSTIC_NOT_CALIBRATED_TEST', n=len(x),
                c0=float(parameters[0]), k=float(parameters[1]), covariance=localcov.tolist(),
                covariance_status='LOCAL_CURVATURE_NOT_CALIBRATED_POSTERIOR', stderr=stderr.tolist(),
                c0_local_wald_to_zero=float(parameters[0]/stderr[0]),
                c0_local_interval_95=(parameters[0]+np.array([-1, 1])*1.959963984540054*stderr[0]).tolist(),
                local_wald_status='DESCRIPTIVE_ONLY_NO_FREQUENTIST_SIGMA_CLAIM',
                conditional_log_density=float(np.sum(exact[:, 0])),
                uniform_width_log_constant=float(np.sum(np.log(widths))),
                log_evidence=None, z_vs_GR_calibrated=None, z_vs_reading_calibrated=None,
                max_direct_log_error=float(np.max(errors)), newton_distance=newton_distance,
                support_distance_h=boundary_h, multistart_successes=len(results),
                multistart_spread=float(max(r.fun for r in results)-optimum.fun),
                gaussian_moment=dict(c0=float(gaussian[0]), k=float(gaussian[1]),
                                     covariance=gaussian_cov.tolist(), sigma_definition='std(u), ddof=1'),
                fixed_offset_zero_status='PROIBIDA_COMO_TESTE')


def management_controls(events, groups):
    """Diagnostic median WLS, independently recomputed from fullsample quantiles."""
    reference_path = ROOT / ('TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/'
                             'C_piso_sistematico/C_piso_sinais_catalogo.json')
    reference = read_json(reference_path)
    results = {}
    for group in ('GWTC5_31', 'GWTC5_33'):
        ids = groups[group]
        results[group] = {}
        for convention in ('median_q90_1.6449', 'median_std_ddof1', 'mean_std_ddof1'):
            sigma = np.array([events[i]['sigma_q90_management_1_6449'] if convention == 'median_q90_1.6449'
                              else events[i]['sigma_dtau_ddof1'] for i in ids])
            y = np.array([events[i]['mean_dtau'] if convention == 'mean_std_ddof1'
                          else events[i]['median_dtau'] for i in ids])
            design = np.column_stack((np.ones(len(ids)), sigma))
            weights = 1/sigma**2
            covariance = np.linalg.inv(design.T @ (weights[:, None]*design))
            parameters = covariance @ (design.T @ (weights*y))
            result = dict(c0=float(parameters[0]), k=float(parameters[1]), covariance=covariance.tolist(),
                          stderr=np.sqrt(np.diag(covariance)).tolist(), n=len(ids),
                          status='DIAGNOSTIC_ONLY_NOT_PRIMARY; absolute WLS covariance, no chi2 rescaling')
            if convention == 'median_q90_1.6449':
                old = reference['b_F_catalogo_' + group]
                old_values = [old['wls_intercept_sigma0'], old['wls_slope_per_sigma'],
                              old['wls_intercept_se'], old['wls_slope_se']]
                new_values = [result['c0'], result['k'], *result['stderr']]
                result['difference_from_archived_management'] = [a-b for a, b in zip(new_values, old_values)]
                result['reference_source'] = str(reference_path.relative_to(ROOT))
                result['reference_sha256'] = sha(reference_path)
                result['reference_field_order'] = ['c0', 'k', 'SE_c0', 'SE_k']
            results[group][convention] = result
    return results


def inspect_event(row, metadata, module, interpolators):
    clock_guard()
    path = within_root(row['source_path'])
    check_pin(path, row['source_sha256'])
    fields = row['field_mapping']
    with h5py.File(path, 'r') as source:
        group = source[row['dataset'].rsplit('/', 1)[0]]
        posterior = source[row['dataset']]
        if any('weight' in name.lower() for name in posterior.dtype.names):
            raise ValueError('Weights require an explicitly reviewed implementation')
        # Compound-field selection; preserve row order and fullsample pairing.
        array = posterior.fields(list(fields.values()))[:]
        priors = {key: verify_uniform(group, fields[key]) for key in ('df', 'dtau')}
    values = {key: np.asarray(array[name], dtype=float) for key, name in fields.items()}
    if len(array) != row['N'] or not all(np.all(np.isfinite(v)) for v in values.values()):
        raise ValueError('Nonfinite samples or changed fullsample count')
    for key in ('df', 'dtau'):
        low, high = priors[key]['bounds']
        if np.any(values[key] < low) or np.any(values[key] > high):
            raise ValueError('Posterior outside declared Uniform prior')
    sigma = float(np.std(values['dtau'], ddof=1))
    q05, median, q95 = np.quantile(values['dtau'], [.05, .5, .95])
    if not math.isclose(sigma, row['stdtau'], rel_tol=1e-12, abs_tol=1e-14):
        raise ValueError('Independent fullsample sigma differs from E0')
    spins = values['spin']
    frequencies = interpolators[0](spins) + 1j*interpolators[1](spins)
    if not np.all(np.isfinite(frequencies)):
        raise ValueError('Spin outside pinned QNM grid: no clipping/dropping')
    predictions = {'GR': np.zeros(len(array))}
    scopes = {'GR': 'REFERENCE_DTAU_ZERO_WITH_FREE_DF'}
    for reading in READINGS[1:]:
        predictions[reading] = np.empty(len(array))
        for j, (mass, spin, z, omega) in enumerate(zip(values['mass_detector'], spins,
                                                       values['redshift'], frequencies)):
            if j % 2048 == 0:
                clock_guard()
            kwargs = {'qnm_dimensionless': complex(omega)} if reading == 'R-MOD' else {}
            prediction = module.prediction(float(mass), float(spin), reading, redshift=float(z),
                                           observable='ensemble', profile='CODATA2018_IAU2015', **kwargs)
            predictions[reading][j] = prediction['delta_tau']
            scopes[reading] = prediction['scope']
        if not np.all(np.isfinite(predictions[reading])):
            raise ValueError('Nonfinite prediction; population may not be silently reduced')
    low, high = priors['dtau']['bounds']
    residuals = {key: values['dtau']-delta for key, delta in predictions.items()}
    prediction_summary = {}
    for reading, delta in predictions.items():
        u = residuals[reading]
        prediction_summary[reading] = dict(scope=scopes[reading], mean=float(np.mean(delta)),
            median=float(np.median(delta)), std_ddof1=float(np.std(delta, ddof=1)),
            min=float(np.min(delta)), max=float(np.max(delta)),
            u_mean=float(np.mean(u)), u_std_ddof1=float(np.std(u, ddof=1)),
            cov_dtau_delta=float(np.cov(values['dtau'], delta, ddof=1)[0, 1]),
            numerically_identical_residual_to_GR=bool(np.array_equal(u, values['dtau'])))
    summary = dict(event=row['event'], N=len(array), source_sha256=row['source_sha256'],
                   dataset=row['dataset'], priors=priors, sigma_dtau_ddof1=sigma, metadata=metadata,
                   mean_dtau=float(np.mean(values['dtau'])), median_dtau=float(median),
                   sigma_q90_management_1_6449=float((q95-q05)/(2*1.6449)),
                   paired_covariance_fields=list(fields),
                   paired_covariance=np.cov(np.vstack(list(values.values())), ddof=1).tolist(),
                   predictions=prediction_summary, ESS=None, sample_weights='Equal as stored; no weight field',
                   prediction_convention='BCW except R-MOD pinned complex QNM spline; matches E0 convention')
    supports = {key: (low-float(np.min(delta)), high-float(np.max(delta)))
                for key, delta in predictions.items()}
    return summary, residuals, supports


def calculate():
    dataset = read_json(BASE / 'bis/e0_core/DATASET.json')
    join = read_json(BASE / 'bis/e0_metadata/SNR_JOIN_FOR_A.json')
    names = [e['event'] for e in join['events']]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate metadata join keys')
    metadata = {e['event']: e for e in join['events']}
    aliases = {'GW150914_095045': 'GW150914', 'GW170104_101158': 'GW170104'}
    selected = dataset['sets']['GWTC5_33']
    if len(selected) != 33 or len(set(selected)) != 33:
        raise ValueError('Expected 33 distinct product IDs')
    rows = [row for row in dataset['rows'] if row['product_id'] in selected]
    if len(rows) != 33:
        raise ValueError('Missing or duplicate posterior product')
    spec = importlib.util.spec_from_file_location('e1_pinned_prediction', BASE / 'tgl_ringdown_prediction.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Sole reviewed runtime import, never um.py.
    qnm = read_json(BASE / 'QNM_GRID.json')
    mode = qnm['modes']['220']
    if not (len(mode['spins']) == len(mode['real']) == len(mode['imag'])):
        raise ValueError('Mode-specific QNM grid shape mismatch')
    interpolators = [CubicSpline(mode['spins'], mode[key], extrapolate=False)
                     for key in ('real', 'imag')]
    events, residuals, supports = {}, {}, {}
    processed_samples = 0
    projection_start = time.monotonic()
    total_samples = sum(row['N'] for row in rows)
    for index, row in enumerate(rows):
        key = row['product_id']
        meta = metadata[aliases.get(row['event'], row['event'])]
        if meta['run'] not in ('O1', 'O2', 'O3', 'O3a', 'O3b', 'O4a', 'O4b'):
            raise ValueError('Unknown run; no inferred grouping')
        if not isinstance(meta['network_matched_filter_snr'], (float, int)) or meta['network_matched_filter_snr'] <= 0:
            raise ValueError('Missing/nonpositive SNR; no imputation')
        events[key], residuals[key], supports[key] = inspect_event(row, meta, module, interpolators)
        processed_samples += row['N']
        if index == 2:
            estimate = (time.monotonic()-projection_start)*total_samples/processed_samples
            print(json.dumps(dict(stage='early_cost_guard', prediction_seconds_estimated=estimate,
                                  cutoff_prediction_seconds=LIMIT_SECONDS*.55)), flush=True)
            if estimate > LIMIT_SECONDS*.55:
                raise TimeoutError('Early prediction cost exceeds allowance; no campaign extension')
        print(json.dumps(dict(stage='event_complete', event=row['event'], n=row['N'])), flush=True)
    groups = {}
    for name in ('GWTC5_31', 'GWTC5_33'):
        ids = dataset['sets'][name]
        if len(ids) != int(name[-2:]) or len(set(ids)) != len(ids) or not set(ids) <= set(events):
            raise ValueError('Population membership contract failed')
        groups[name] = ids
        for cut in (.15, .20, .25):
            groups[f'{name}/sigma_lt_{cut:.2f}'] = [i for i in ids if events[i]['sigma_dtau_ddof1'] < cut]
        for run in ('O1-O3', 'O4a', 'O4b'):
            allowed = ('O1', 'O2', 'O3', 'O3a', 'O3b') if run == 'O1-O3' else (run,)
            groups[f'{name}/{run}'] = [i for i in ids if events[i]['metadata']['run'] in allowed]
    fits, controls = [], []
    for reading in READINGS:
        print(json.dumps(dict(stage='density_fits', reading=reading)), flush=True)
        for factor in (.7, 1., 1.4):
            densities = {i: Density(residuals[i][reading], factor, supports[i][reading]) for i in events}
            for i, density in densities.items():
                controls.append(dict(product_id=i, reading=reading, bandwidth_factor=factor,
                                     bandwidth=density.h, integral=density.integral,
                                     grid_size=len(density.grid), resolution=density.resolution,
                                     max_direct_log_error=density.max_control_log_error))
            for group, ids in groups.items():
                # Bandwidth sensitivity on full populations; all splits at nominal bandwidth.
                if '/' in group and factor != 1.:
                    continue
                for covariate in ('sigma', 'inverse_SNR'):
                    x = np.array([events[i]['sigma_dtau_ddof1'] if covariate == 'sigma'
                                  else 40/events[i]['metadata']['network_matched_filter_snr'] for i in ids])
                    widths = np.array([np.diff(events[i]['priors']['dtau']['bounds'])[0] for i in ids])
                    result = fit([densities[i] for i in ids], x, widths)
                    if 'c0_local_wald_to_zero' in result:
                        field = 'c0_GR_over_SE_descriptive' if reading == 'GR' else 'c0_residual_L_over_SE_descriptive'
                        result[field] = result['c0_local_wald_to_zero']
                    fits.append(dict(reading=reading, bandwidth_factor=factor, group=group,
                                     product_ids=ids, covariate=covariate, result=result))
    comparisons = []
    for reading in READINGS[1:]:
        for group in ('GWTC5_31', 'GWTC5_33'):
            for covariate in ('sigma', 'inverse_SNR'):
                selected = [f for f in fits if f['reading'] == reading and f['group'] == group
                            and f['covariate'] == covariate]
                gr = [f for f in fits if f['reading'] == 'GR' and f['group'] == group
                      and f['covariate'] == covariate]
                comparisons.append(dict(reading=reading, group=group, covariate=covariate,
                    bandwidth_comparison=[dict(factor=f['bandwidth_factor'],
                       status=f['result']['status'], c0_residual_L_over_SE=f['result'].get('c0_local_wald_to_zero'),
                       c0_GR_over_SE=next(g['result'].get('c0_local_wald_to_zero') for g in gr
                                         if g['bandwidth_factor'] == f['bandwidth_factor'])) for f in selected],
                    status='DESCRIPTIVE_LOCAL_ONLY_NOT_LR_OR_BAYES_FACTOR', z_calibrated=None))
    return dict(status='NAO_CEGO_CONDITIONAL_CALIBRATION_ONLY_NOT_LR_OR_BAYES_FACTOR', events=events, fits=fits,
                descriptive_comparisons=comparisons, management_WLS_controls=management_controls(events, groups),
                kde_controls=controls, open_readings=OPEN_READINGS, beta_runtime=module.beta_tgl(),
                all_readings=list(READINGS[1:])+list(OPEN_READINGS),
                df_handling='Integrated with original posterior, NOT fixed to zero',
                selection='UNKNOWN_NORMALIZATION; network SNR is not the two selection thresholds',
                prior='Uniform marginals checked; joint factorization/global restricted support OPEN',
                reference_management_method='s02_measure.py:177-180; s03_sinais_e_catalogo.py:20-27; '
                    'median y, sigma=(q95-q05)/(2*1.6449), weights=sigma^-2, absolute covariance',
                covariance_scope='LOCAL_ONLY; sigma endogenous; no calibrated posterior or hypothesis test',
                E1_2='NAO_PAGO_BY_THIS_SCRIPT_FULL_TEXT_READING_REQUIRED',
                E1_3='NO_NEW_INJECTIONS; existing LVK single-point review, no bias curve',
                E1_4='NAO_PAGO_BY_THIS_SCRIPT_C2_AND_C5_REQUIRE_SEPARATE_ESTIMATOR_COMPARISON',
                E1_5='LOCAL_DESCRIPTIVE_DISTANCES_ONLY; calibrated separation remains OPEN',
                fixed_offset_zero='PROIBIDA_COMO_TESTE', axioms='N/A', theorems=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--authorization')
    parser.add_argument('--tag', default='authorized_001')
    args = parser.parse_args()
    manifest, authorization, budget, destination = authorize(args)
    # Set thread caps BEFORE scientific imports. Runtime invoked with -B.
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[key] = '1'
    global np, h5py, fftconvolve, PchipInterpolator, CubicSpline, minimize, LinearConstraint, START
    import numpy as np
    import h5py
    import scipy
    from scipy.signal import fftconvolve
    from scipy.interpolate import PchipInterpolator, CubicSpline
    from scipy.optimize import minimize, LinearConstraint
    from threadpoolctl import threadpool_limits
    destination.mkdir(parents=True, exist_ok=False)
    START = time.monotonic()
    cpu_start = time.process_time()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    result = None
    try:
        with threadpool_limits(limits=1):
            result = calculate()
        # Recheck all inputs, including raw HDF5 pins, before publishing results.
        for source in manifest['files']:
            check_pin(within_root(source['path']), source['sha256'])
        data = read_json(BASE / 'bis/e0_core/DATASET.json')
        for row in data['rows']:
            if row['product_id'] in data['sets']['GWTC5_33']:
                check_pin(within_root(row['source_path']), row['source_sha256'])
        publish_new(destination / 'NUISANCE_DIAGNOSTIC.json', result)
    except Exception as error:
        publish_new(destination / 'FAILED.json', dict(status='FAILED_NOT_SUCCESS',
                    error_type=type(error).__name__, message=str(error), started_utc=started,
                    wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-cpu_start))
        raise
    receipt = dict(status='COMPUTATION_REQUIRES_INDEPENDENT_REVIEW', started_utc=started,
                   wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-cpu_start,
                   processes=1, thread_limit=1, command=sys.argv, script_sha256=sha(Path(__file__)),
                   manifest_sha256=sha(HERE/'DESIGN_MANIFEST.json'), authorization_sha256=sha(authorization),
                   result_sha256=sha(destination/'NUISANCE_DIAGNOSTIC.json'),
                   versions=dict(numpy=np.__version__, scipy=scipy.__version__, h5py=h5py.__version__),
                   budget_source_sha256=sha(BASE/'bis/PART_B_BUDGET_START.json'),
                   open_cells=sum(not f['result']['status'].startswith('CONDITIONAL') for f in result['fits']))
    publish_new(destination / 'RECEIPT.json', receipt)


if __name__ == '__main__':
    main()
