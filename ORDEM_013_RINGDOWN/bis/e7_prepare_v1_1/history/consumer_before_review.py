"""E7 fail-closed consumer. Scientific dependency: NumPy only.

No physical likelihood is implemented: normalized restricted model, selection,
physical nuisance and blind-release policy remain OPEN. Never promote a local
Hessian covariance to a physical calibration. Hash reads do not parse HDF5.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import numpy as np

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
READINGS = ('R-A', 'R-B', 'R-MOD', 'R-RAIZ-0', 'R-RAIZ-EP4',
            'R-RAIZ-REST', 'R-RAIZ-COHERENT', 'R-LIN', 'R-GLOBAL', 'R-PROP')
FIELDS = ('df220', 'dtau220', 'Mfdet', 'af', 'z')
READING_STATUTES = {r: ('CONJECTURE' if r in ('R-MOD', 'R-RAIZ-REST', 'R-RAIZ-COHERENT', 'R-LIN', 'R-PROP')
                        else 'INPUT') for r in READINGS}
VERDICTS = ('NOT_FALSIFIED_UNDERPOWERED', 'NOT_FALSIFIED_POWERED',
            'INCONCLUSIVE_SYSTEMATICS', 'EXCLUDED_IN_READING',
            'FALSIFIED_IN_READING', 'AWAITING_DATA')


def beta_runtime():
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require_pin(path, wanted):
    if not isinstance(wanted, str) or not re.fullmatch('[0-9a-f]{64}', wanted):
        raise ValueError('Missing/invalid SHA256: ' + str(path))
    if sha(path) != wanted:
        raise ValueError('SHA256 mismatch: ' + str(path))


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('Duplicate JSON key: ' + key)
        out[key] = value
    return out


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=unique_object,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def contained(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('Expected relative custody path')
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Path escapes custody root')
    return path


def publish_new(path, value):
    """No overwrite; stage bytes and atomically create a hard link on same volume."""
    path = Path(path)
    payload = (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + '\n').encode('utf-8')
    if len(payload) > 25 * 1024 * 1024 and 'cache' not in path.parts:
        raise ValueError('Output >25 MiB requires registered first-level cache destination')
    fd, tmp = tempfile.mkstemp(prefix='.e7-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(tmp).stat().st_size != len(payload):
            raise IOError('Short staged write')
        os.link(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


def checked_context(root, registration, registration_sha256):
    require_pin(registration, registration_sha256)
    raise ValueError("Legacy extraction context disabled; use the embedded run_rite reader")


def validate_design(reg):
    if reg.get('status') != 'REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST':
        raise ValueError('Draft is not a registration')
    if set(reg['readings']) != set(READINGS) or len(reg['readings']) != len(READINGS):
        raise ValueError('E2 reading matrix differs')
    if set(reg['permitted_verdicts']) != set(VERDICTS) or len(reg['permitted_verdicts']) != len(VERDICTS):
        raise ValueError('E2 permitted verdicts differ')
    stats, gate = reg['statistics'], reg['systematic_gate']
    if (stats['offset_fixed_zero'] != 'PROIBIDA_COMO_TESTE' or
            stats['LRT_IV_threshold_strict_greater'] != 25.0 or
            gate['floor_divisor_primary_INPUT'] != 5 or gate['floor_divisor_sensitivity_only'] != 15 or
            gate['admit_event_only_after_green'] is not True or gate['physical_z_when_red'] is not None):
        raise ValueError('E2 scientific guard contract differs')
    cap = stats['maximum_information_weight_INPUT']
    if isinstance(cap, bool) or not isinstance(cap, (int, float)) or not math.isfinite(cap) or not 0 < cap <= 1:
        raise ValueError('Invalid registered event weight cap')
    if type(stats['split_null_seed']) is not int or stats['split_null_seed'] < 0:
        raise ValueError('Invalid split seed')


def validate_events(events):
    seen, seen_source = set(), set()
    for event in events:
        identity = event['event_id']
        if not isinstance(identity, str) or not identity or identity in seen:
            raise ValueError('Duplicate/empty canonical event identity')
        seen.add(identity)
        source = (event['source_sha256'], event['dataset'])
        if source in seen_source:
            raise ValueError('Same posterior product counted twice')
        seen_source.add(source)
        if event['role'] not in ('calibration', 'blind_test'):
            raise ValueError('Unknown role')
        if set(event['samples']) != set(FIELDS) or set(event['priors']) != set(FIELDS):
            raise ValueError('Five paired sample columns and prior records required')
        n = event['N']
        if type(n) is not int or n < 2:
            raise ValueError('At least two samples required')
        for field in FIELDS:
            values = np.asarray(event['samples'][field], dtype=float)
            if values.shape != (n,) or not np.isfinite(values).all():
                raise ValueError('Unpaired/nonfinite posterior column: ' + field)
            prior = event['priors'][field]
            if not prior.get('status') or 'declarations' not in prior:
                raise ValueError('Prior provenance/status missing')
        samples = event['samples']
        if (np.any(np.asarray(samples['Mfdet']) <= 0) or
                np.any(np.abs(samples['af']) >= 1) or np.any(np.asarray(samples['z']) < 0)):
            raise ValueError('Invalid remnant frame/spin/redshift')
        thin = event['thinning']
        if thin != {'factor': 1, 'seed': None, 'method': 'none'} or event['N_source'] != n:
            raise ValueError('This version only supports full samples, no thinning')
        if event['sample_weights'] != 'equal_as_stored':
            raise ValueError('Weighted posterior unsupported')
    return events


def checked_authorization(reg, guard, registration_sha256, authorization, authorization_sha256):
    """Check the principal receipt supplied independently of the payload.

    The caller must obtain its path/hash from the principal after E2. A hash
    asserted inside a posterior is not an authorization or a signature.
    """
    if authorization is None or authorization_sha256 is None:
        raise ValueError('Principal post-E2 authorization path and SHA256 required')
    require_pin(authorization, authorization_sha256)
    auth = read_json(authorization)
    spec = reg['e7']
    if (auth.get('status') != 'AUTHORIZED_BY_PRINCIPAL_AFTER_E2' or
            auth.get('registration_sha256') != registration_sha256 or
            auth.get('plan_sha256') != spec['plan_sha256'] or
            auth.get('producer_tree_sha256') != spec['producer_tree_sha256']):
        raise ValueError('Missing/mismatched principal post-E2 authorization')
    if not all(isinstance(value, str) and value.strip() for value in
               (auth.get('registered_utc'), reg.get('registered_utc'))):
        raise ValueError('Explicit authorization and E2 UTC timestamps required')
    authorized = guard.utc(auth['registered_utc'])
    registered = guard.utc(reg['registered_utc'])
    if authorized.utcoffset() is None or registered.utcoffset() is None:
        raise ValueError('Timezone required for authorization and E2')
    if authorized < registered:
        raise ValueError('Principal authorization predates E2')
    if authorized > datetime.now(timezone.utc):
        raise ValueError('Principal authorization is future-dated')
    return auth


def validate_payload_contract(payload, plan, spec, registration_sha256, authorization_sha256):
    """Reject transport-authenticated bytes that do not satisfy the frozen plan."""
    if (payload.get('schema') != 'POSTERIORES_PSEOB_V1' or
            payload.get('catalogue') != plan['catalogue'] or
            payload.get('registration_sha256') != registration_sha256 or
            payload.get('plan_sha256') != spec['plan_sha256'] or
            payload.get('producer_tree_sha256') != spec['producer_tree_sha256'] or
            payload.get('authorization_sha256') != authorization_sha256):
        raise ValueError('Posterior schema/production/authorization contract differs')
    if plan.get('status') != 'READY_FOR_REGISTERED_CALIBRATION_EXTRACTION':
        raise ValueError('Extraction plan is not complete/reviewed')
    events = validate_events(payload['events'])
    if not events or [e['event_id'] for e in events] != [e['event_id'] for e in plan['events']]:
        raise ValueError('Changed membership/order, including cross-release duplicates')
    for event, planned in zip(events, plan['events']):
        for key in ('event_id', 'role', 'source_path', 'source_sha256', 'tar_path',
                    'tar_sha256', 'dataset', 'model', 'mass_frame', 'mass_unit'):
            if event[key] != planned[key]:
                raise ValueError('Posterior source not registered: ' + key)
        if (type(planned['N_source']) is not int or type(event['N_source']) is not int or
                event['N'] != planned['N_source'] or event['N_source'] != planned['N_source']):
            raise ValueError('Full sample count differs from registered plan')
        if (event['source_field_mapping'] != planned['fields'] or
                set(planned['fields']) != set(FIELDS) or
                event['mass_frame'] != 'detector' or event['mass_unit'] != 'solar_mass'):
            raise ValueError('Registered mapping or detector mass units differ')
        if set(planned['prior_paths']) != set(FIELDS):
            raise ValueError('Incomplete registered prior paths')
        for field in FIELDS:
            prior = event['priors'][field]
            declarations = prior['declarations']
            paths = planned['prior_paths'][field]
            if not isinstance(paths, list) or not isinstance(declarations, list):
                raise ValueError('Prior declarations/paths must be lists')
            if not all(isinstance(d, dict) and set(d) == {'path', 'text'} for d in declarations):
                raise ValueError('Malformed prior declaration')
            if [d['path'] for d in declarations] != paths or len(paths) != len(set(paths)):
                raise ValueError('Prior paths differ from registered plan')
            expected = 'DECLARADO_TEXT_NOT_NORMALIZED' if paths else 'OPEN_DERIVED_PRIOR_NOT_DECLARED'
            if (prior.get('status') != expected or prior.get('joint_factorization') != 'OPEN' or
                    'density' not in prior or prior['density'] is not None):
                raise ValueError('Prior status/density is not the declared OPEN contract')
            if field in ('df220', 'dtau220') and not paths:
                raise ValueError('Deformation prior declaration is required')
            for declaration in declarations:
                texts = declaration['text']
                if (not isinstance(texts, list) or not 1 <= len(texts) <= 256 or
                        not all(isinstance(t, str) and t.strip() for t in texts) or
                        sum(map(len, texts)) > 100000):
                    raise ValueError('Prior declaration must contain bounded nonempty text')
    return events


def conditional_projection(delta, sigma, design):
    """INPUT Gaussian planning geometry after projecting free nuisance columns.

    No observations, Bayes factors, physical z, covariance calibration or MC.
    A constant correction projects to zero when the design has an intercept.
    """
    d, s, x = np.asarray(delta, float), np.asarray(sigma, float), np.asarray(design, float)
    if d.ndim != 1 or s.shape != d.shape or x.ndim != 2 or x.shape[0] != d.size:
        raise ValueError('Projection shape mismatch')
    if d.size <= x.shape[1] or not all(np.isfinite(v).all() for v in (d, s, x)) or np.any(s <= 0):
        raise ValueError('Invalid projection input')
    weighted = x / s[:, None]
    q, singular, _ = np.linalg.svd(weighted, full_matrices=False)
    if singular[-1] <= singular[0] * max(weighted.shape) * np.finfo(float).eps:
        raise ValueError('Rank-deficient nuisance design')
    whitened = d / s
    residual = whitened - q @ (q.T @ whitened)
    information = float(residual @ residual)
    if information <= 1e-24 * float(whitened @ whitened):
        information = 0.
    return {'status': 'INPUT_CONDITIONAL_GAUSSIAN_PROJECTION_NOT_PHYSICAL_SIGNIFICANCE',
            'projected_information': information,
            'expected_amplitude_uncertainty_conditional': 1 / math.sqrt(information) if information else None,
            'z_physical': None, 'lnB': None}


def prediction_draws(mass_detector, spin, redshift, reading, qnm_dimensionless=None):
    """Vector form of pinned tgl_ringdown_prediction.prediction, CODATA/IAU.

    Ensemble-220 only. Returned arrays preserve original joint sample rows.
    Exact QNM input is a conditional numerical input, not certified by this
    function. The five-column extractor does not supply it; R-MOD stays OPEN.
    """
    if reading not in READINGS:
        raise ValueError('Unknown C1 reading')
    m, a, z = (np.asarray(v, dtype=float) for v in (mass_detector, spin, redshift))
    if m.ndim != 1 or m.size < 2 or a.shape != m.shape or z.shape != m.shape:
        raise ValueError('Unpaired remnant draws')
    if not all(np.isfinite(v).all() for v in (m,a,z)) or np.any(m <= 0) or np.any(np.abs(a) >= 1) or np.any(z < 0):
        raise ValueError('Invalid remnant draws')
    result = {'reading': reading, 'statute': READING_STATUTES[reading],
              'status': 'OPEN', 'delta_tau': None, 'delta_f': None,
              'scope': 'CONDITIONAL_ENSEMBLE_220_NOT_SINGLE_REALIZATION'}
    if reading in ('R-PROP','R-RAIZ-COHERENT'):
        result['reason'] = ('Propagation exponent is not a local damping rate' if reading == 'R-PROP'
                            else 'Occupation and fitting window required; initial slope is not delta_tau')
        return result
    if reading == 'R-MOD' and qnm_dimensionless is None:
        result['reason'] = 'EXACT_PAIRED_QNM_REQUIRED_NO_BCW_SUBSTITUTION'
        return result
    c=299792458.0; gravity=6.67430e-11; gm_sun=1.3271244e20
    hbar=6.62607015e-34/(2*math.pi)
    tm=m*gm_sun/c**3; tp=math.sqrt(hbar*gravity/c**5); z1=1+z
    if qnm_dimensionless is None:
        if np.any(a < 0):
            result['reason']='NEGATIVE_SPIN_REQUIRES_EXACT_QNM_NO_BCW_EXTRAPOLATION'
            return result
        wr=1.5251-1.1568*(1-a)**0.1292
        quality=.7000+1.4187*(1-a)**(-.4990)
        damping=wr/(2*quality)
        result['qnm_method']='BERTI_CARDOSO_WILL_FIT_2006_CONDITIONAL'
    else:
        q=np.asarray(qnm_dimensionless,complex)
        if q.shape != m.shape or not np.isfinite(q).all() or np.any(q.real <= 0) or np.any(q.imag >= 0):
            raise ValueError('QNM must be paired omega_R - i/tau with positive real frequency')
        wr=q.real; damping=-q.imag
        result['qnm_method']='EXTERNALLY_SUPPLIED_QNM_INPUT_PROVENANCE_REQUIRED'
    omega=wr/tm; tau=tm/damping; b=beta_runtime()
    if reading=='R-A': gamma=b*z1*tp*omega**2/2
    elif reading=='R-B': gamma=b*tm*omega**2/2
    elif reading=='R-RAIZ-0': gamma=b*omega/2
    elif reading=='R-RAIZ-EP4':
        w0=1/(4*tp*z1); gamma=b*omega**2/(2*(np.sqrt(w0+omega)+np.sqrt(w0))**2)
    elif reading=='R-RAIZ-REST':
        mass_source_kg=(tm/z1)*c**3/gravity
        w0=mass_source_kg*c*c/(hbar*z1)
        gamma=b*omega**2/(2*(np.sqrt(w0+omega)+np.sqrt(w0))**2)
    elif reading=='R-LIN': gamma=b*omega
    elif reading=='R-GLOBAL': gamma=np.zeros_like(m)
    elif reading=='R-MOD':
        root=np.sqrt(1-a*a); horizon=a/(2*tm*(1+root)); kappa=root/(2*tm*(1+root))
        effective=omega-2*horizon
        if np.any(effective <= 0):
            raise ValueError('Nonpositive restricted corotating gap')
        gamma=b*math.pi*effective**2/kappa
    x=gamma*tau
    delta=-x/(1+x)
    if not np.isfinite(delta).all():
        raise ValueError('Nonfinite conditional prediction')
    result.update(status='CONDITIONAL_PAIRED_ENSEMBLE_PREDICTION',delta_tau=delta,
                  delta_f=np.zeros_like(m),reason=None)
    return result


def reading_diagnostics(events):
    """All C1 readings side-by-side; full paired corrections and geometry only."""
    output={}
    for reading in READINGS:
        rows=[]; deltas=[]; widths=[]
        for event in events:
            s=event['samples']
            prediction=prediction_draws(s['Mfdet'],s['af'],s['z'],reading)
            row={k:v for k,v in prediction.items() if k not in ('delta_tau','delta_f')}
            row['event_id']=event['event_id']; row['N']=event['N']
            if prediction['delta_tau'] is not None:
                d=prediction['delta_tau']; measured=np.asarray(s['dtau220'],float)
                sigma=float(np.std(measured,ddof=1))
                if sigma <= 0: raise ValueError('Zero posterior width')
                residual=measured-d
                row.update(delta_tau_mean=float(np.mean(d)),delta_tau_q05_q95=np.quantile(d,[.05,.95]).tolist(),
                           delta_tau_std_ddof1=float(np.std(d,ddof=1)),
                           conditional_abs_correction_over_sigma=float(abs(np.mean(d))/sigma),
                           correction_over_sigma_scope='CONDITIONAL_EFFECT_SIZE_NOT_PHYSICAL_Z',
                           residual_mean=float(np.mean(residual)), residual_std_ddof1=float(np.std(residual,ddof=1)),
                           cov_dtau_prediction=float(np.cov(measured,d,ddof=1)[0,1]),
                           residual_numerically_identical_to_GR=bool(np.array_equal(residual,measured)),
                           systematic_floor_abs_delta_over5=float(abs(np.mean(d))/5),
                           systematic_floor_sensitivity_over15=float(abs(np.mean(d))/15),
                           delta_f_ensemble=0.,lnB=None,z_physical=None)
                deltas.append(float(np.mean(d))); widths.append(sigma)
            rows.append(row)
        geometry={'status':'OPEN_INSUFFICIENT_EVENTS_OR_PREDICTION','projected_information':None,
                  'z_physical':None,'lnB':None}
        if len(deltas)==len(events) and len(deltas)>1:
            geometry=conditional_projection(deltas,widths,np.ones((len(deltas),1)))
            geometry['design']='FREE_INTERCEPT_ONLY_CONDITIONAL_EVENT_MEAN_TEMPLATE'
            geometry['mean_template_scope']='MEAN_OF_PAIRED_PREDICTIONS_NOT_MEDIAN_REMNANT_PLUG_IN'
            if len(deltas)>2:
                design=np.column_stack((np.ones(len(deltas)),widths))
                try:
                    geometry['intercept_plus_sigma_slope']=conditional_projection(deltas,widths,design)
                except ValueError as exc:
                    geometry['intercept_plus_sigma_slope']={'status':'OPEN_DEGENERATE_DESIGN','reason':str(exc)}
        output[reading]={'statute':READING_STATUTES[reading],'events':rows,
                         'geometric_free_intercept_information':geometry,
                         'mode_440':{'status':'OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM',
                                     'reason':'Five-column extractor carries 220 only; 220+440 is not evaluated'},
                         'physical_likelihood_status':'OPEN','lnB':None,'z_physical':None}
    return output


def fullsample_diagnostics(events, statistics):
    """Descriptive calibration diagnostics from ALL paired draws, not PE evidence.

    Inverse-width weights are reported, never used to remove an event. Event
    means and split/jackknife summaries below are conditional descriptive
    summaries, not a hierarchical fit, corrected null, LRT or Bayes factor.
    """
    validate_events(events)
    if any(e['role'] != 'calibration' for e in events):
        raise ValueError('Descriptive diagnostics accept nonblind calibration only')
    report = {'status': 'NONBLIND_FULLSAMPLE_CONDITIONAL_DESCRIPTIVE_ONLY',
              'events': [], 'z_physical': None, 'lnB': None, 'LRT_IV': None,
              'sigma_pop_calibrated': None, 'split_null_p': None,
              'covariance_scope': 'EMPIRICAL_WITHIN_EVENT_SAMPLES_NOT_CALIBRATED_SYSTEMATICS'}
    if not events:
        return report
    for event in events:
        values = np.column_stack([event['samples'][key] for key in FIELDS])
        covariance = np.cov(values, rowvar=False, ddof=1)
        std = np.std(values, axis=0, ddof=1)
        if not np.isfinite(covariance).all() or np.any(std[:2] <= 0):
            raise ValueError('Degenerate posterior width; do not fabricate information')
        report['events'].append({'event_id': event['event_id'], 'N': event['N'],
                                'field_order': FIELDS, 'mean': values.mean(axis=0).tolist(),
                                'std_ddof1': std.tolist(), 'paired_covariance': covariance.tolist()})
    s_tau = np.array([r['std_ddof1'][1] for r in report['events']])
    s_df = np.array([r['std_ddof1'][0] for r in report['events']])
    weights = {}
    for label, widths, exponent in [('tau_inverse_variance', s_tau, 2), ('IV_inverse_fourth', s_df, 4)]:
        logs = -exponent * np.log(widths)
        w = np.exp(logs - logs.max()); w /= w.sum()
        weights[label] = w
        report[label] = {'shares': w.tolist(), 'max_share': float(w.max()),
                         'cap_INPUT': statistics['maximum_information_weight_INPUT'],
                         'dominates_cap': bool(w.max() > statistics['maximum_information_weight_INPUT']),
                         'events_dropped': 0}
    means = np.array([r['mean'][1] for r in report['events']])
    w = weights['tau_inverse_variance']
    report['descriptive_uncorrected_dtau_weighted_mean'] = float(w @ means)
    report['leave_one_out_descriptive_means'] = []
    if len(events) > 1:
        for i, event in enumerate(events):
            keep = np.arange(len(events)) != i
            local = 1 / (s_tau[keep] / s_tau[keep].min())**2
            report['leave_one_out_descriptive_means'].append(
                {'omitted': event['event_id'], 'mean': float(local @ means[keep] / local.sum())})
    permutation = np.random.default_rng(statistics['split_null_seed']).permutation(len(events))
    report['split_seed'] = statistics['split_null_seed']
    report['split_membership_only'] = [[events[i]['event_id'] for i in permutation[offset::2]] for offset in (0, 1)]
    report['unpaid'] = ['nuisance-corrected split null with shared covariance', 'calibrated jackknife verdicts',
                        'paired reading-dependent restricted likelihood', 'selection', 'physical covariance',
                        'population-width LRT calibration', '440 posterior extraction']
    return report


def verdict_matrix(registration, nuisance, test_count=0):
    if type(test_count) is not int or test_count < 0:
        raise ValueError('Invalid test count')
    gate = nuisance['gate']
    red = (gate.get('systematic_calibration_paid') is not True or
           gate.get('physical_likelihood_paid') is not True or
           gate.get('sigma_c_physically_calibrated') is None or
           gate.get('selection_efficiency') is None or
           gate.get('global_restricted_prior_normalization') is None)
    # A declared green gate cannot create an unimplemented restricted model.
    rows = []
    for reading in READINGS:
        target = registration['e7']['readings'][reading]
        for mode in ('220_only', '220_plus_440_INPUT'):
            rows.append({'reading': reading, 'mode_variant': mode,
                         'statute': READING_STATUTES[reading],
                         'mode_data_status': ('OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM' if mode != '220_only'
                                              else 'CONDITIONAL_220_ONLY'),
                         'verdict': 'AWAITING_DATA' if test_count == 0 else 'INCONCLUSIVE_SYSTEMATICS',
                         'N_target_information': target['N_target_information'],
                         'target_status': target['status'], 'systematic_gate': 'red' if red else 'UNVERIFIED',
                         'lnB': None, 'z_physical': None, 'correction_over_sigma_physical': None,
                         'reason': 'OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE',
                         'fixed_offset_zero': 'PROIBIDA_COMO_TESTE'})
    return rows


def run(root, registration, registration_sha256, posterior=None, posterior_sha256=None,
        authorization=None, authorization_sha256=None):
    reg, guard = checked_context(root, registration, registration_sha256)
    spec = reg['e7']
    nuisance = read_json(contained(root, spec['nuisance_path']))
    plan = read_json(contained(root, spec['plan_path']))
    events = []
    if posterior is not None:
        if any(e['role'] != 'calibration' for e in plan['events']):
            raise ValueError('Blind-release adapter OPEN; refuse before opening posterior JSON')
        checked_authorization(reg, guard, registration_sha256, authorization, authorization_sha256)
        require_pin(posterior, posterior_sha256)
        payload = read_json(posterior)
        events = validate_payload_contract(payload, plan, spec, registration_sha256, authorization_sha256)
        for event in events:
            for stem in ('source', 'tar'):
                require_pin(contained(root, event[stem + '_path']), event[stem + '_sha256'])
            guard.authorize_event(reg, event['event_id'], event['role'])
            if event['role'] == 'blind_test':
                raise ValueError('Blind-release adapter not implemented; refuse test sample inspection')
    result = {'status': 'PREPARED_FAIL_CLOSED_NO_PHYSICAL_TEST',
              'registration_sha256': registration_sha256, 'posterior_sha256': posterior_sha256,
              'authorization_sha256': authorization_sha256,
              'nuisance_sha256': spec['nuisance_sha256'], 'plan_sha256': spec['plan_sha256'],
              'beta_runtime': beta_runtime(), 'test_events_added': 0,
              'calibration_events': len(events), 'matrix': verdict_matrix(reg, nuisance),
              'lnB': None, 'z_physical': None,
              'local_covariance_scope': 'INPUT_SYNTHETIC_NULL_ONLY_NOT_PHYSICAL_COVARIANCE',
              'does_not_gate_core': True}
    result['fullsample_diagnostics'] = fullsample_diagnostics(events, reg['statistics'])
    result['conditional_readings'] = reading_diagnostics(events)
    result['prediction_source_sha256'] = spec['prediction_source_sha256']
    return result


# T12: portable, calibration-only reader. No import of a guard or comparison
# against the running module's directory. The numerical functions above are
# byte-derived from V1 and their ASTs are audited independently.
STATISTICAL_FIELDS = ('observables', 'statistics', 'systematic_gate', 'nulls',
    'route_IV', 'conventions', 'planning_targets', 'permitted_verdicts',
    'forbidden_verdicts', 'stopping', 'calibration_event_ids')


def utc(value):
    if not isinstance(value, str):
        raise ValueError('Timestamp must be text')
    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise ValueError('Timezone required')
    return value.astimezone(timezone.utc)


def statistical_subobject(reg):
    obj = {k: reg[k] for k in STATISTICAL_FIELDS}
    obj['blinding'] = {k: reg['blinding'][k] for k in ('seed_commitment_sha256', 'offset_half_range')}
    return obj


def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def witnessed(root, reg, digest, expected_name):
    note = contained(root, reg['witness_relative_to_Chatgpt'])
    if note != Path(root).resolve()/'TUNEL/DO_CHATGPT'/expected_name:
        raise ValueError('Wrong witness path')
    text = note.read_text('utf-8-sig')
    hashes = re.findall(r'^registro_sha256: ([0-9a-f]{64})\s*$', text, re.M)
    stamps = re.findall(r'^registered_utc: (\S+)\s*$', text, re.M)
    if hashes != [digest] or len(stamps) != 1:
        raise ValueError('Missing or ambiguous witness')
    stamp = utc(stamps[0]); current = datetime.now(timezone.utc)
    if not utc(reg['registered_utc']) <= stamp <= current:
        raise ValueError('Invalid witness chronology')
    if not stamp.timestamp()-2 <= note.stat().st_mtime <= current.timestamp()+2:
        raise ValueError('Invalid witness file chronology')
    return stamp, sha(note)


def embedded_context(root, registration, registration_sha256, nuisance, nuisance_sha256):
    """Replay a witnessed calibration design; never authorize PE or blind I/O.

    The caller must obtain the registration SHA independently, as with V1.
    Calendar/heavy-runtime guards belong to new jobs, not this read-only replay.
    No self-asserted green gate can activate a missing physical likelihood.
    """
    root = Path(root).resolve(); base = root/'ORDEM_013_RINGDOWN'
    registration = Path(registration).resolve()
    require_pin(registration, registration_sha256)
    match = re.fullmatch(r'RINGDOWN_5SIGMA_V1_1_([1-9][0-9]*)\.json', registration.name)
    if registration.parent != base or match is None:
        raise ValueError('T12 requires a witnessed V1.1.n producer amendment')
    ordinal = int(match[1])
    later = [p for p in base.glob('RINGDOWN_5SIGMA_V1_1_*.json')
             if re.fullmatch(r'RINGDOWN_5SIGMA_V1_1_[1-9][0-9]*\.json',p.name)
             and int(p.stem.rsplit('_',1)[1]) > ordinal]
    if later: raise ValueError('Stale registration; later amendment exists')
    current = read_json(registration)
    spec = current['e7_rite_v1_1']
    require_pin(__file__, current['e7']['producer_tree_sha256']['tgl_ringdown_ampliacao.py'])
    original_path = contained(root, spec['legacy_registration_path'])
    require_pin(original_path, spec['legacy_registration_sha256'])
    original = read_json(original_path)
    if original_path != base/'RINGDOWN_5SIGMA_V1.json':
        raise ValueError('Wrong legacy registration')
    previous_time, witness_sha = witnessed(root, original, spec['legacy_registration_sha256'],
                                          'ENTREGA_013BIS_E2_REGISTRO_V1.md')
    parent = spec['legacy_registration_sha256']; previous = original
    frozen = statistical_subobject(original)
    paths = [base/'RINGDOWN_5SIGMA_V1_1.json'] + [base/f'RINGDOWN_5SIGMA_V1_1_{n}.json' for n in range(1, ordinal+1)]
    for n, path in enumerate(paths):
        reg = read_json(path); digest = sha(path)
        validate_design(reg)
        if reg['parent_registration_sha256'] != parent or reg['v1_witness_sha256'] != witness_sha:
            raise ValueError('Amendment parent or V1 witness differs')
        if statistical_subobject(reg) != frozen or reg['statistical_subobject_sha256'] != canonical_sha(frozen):
            raise ValueError('Frozen statistical subobject differs')
        if set(reg['nulls']['cells']) & set(reg['nulls_v1_1']['cells']):
            raise ValueError('V1 null identity reused')
        if utc(reg['registered_utc']) < previous_time:
            raise ValueError('Registration chronology reversed')
        note_name = 'ENTREGA_015_E2_REGISTRO_V1_1' + (f'_{n}' if n else '') + '.md'
        stamp, _ = witnessed(root, reg, digest, note_name)
        if n and any(k not in reg['pe_jobs'] or reg['pe_jobs'][k] != v for k,v in previous['pe_jobs'].items()):
            raise ValueError('Existing job replaced')
        if set(reg['pe_jobs']) & set(original['pe_jobs']):
            raise ValueError('V1 job reused')
        previous_time, parent, previous = stamp, digest, reg
    if parent != registration_sha256 or previous != current:
        raise ValueError('Registration changed during read')
    require_pin(nuisance, nuisance_sha256)
    if nuisance_sha256 != current['e7']['nuisance_sha256']:
        raise ValueError('Nuisance differs from registration')
    for key in ('plan_path','plan_sha256','prediction_source_path','prediction_source_sha256'):
        if current['e7'][key] != original['e7'][key]:
            raise ValueError('Historical calibration plan/prediction changed')
    for reading in READINGS:
        target = current['e7']['readings'][reading]
        expected = [v for v in current['planning_targets'] if v['reading'] == reading]
        if target.get('conditional_E0_targets') != expected or target['N_target_information'] is not None:
            raise ValueError('Conditional targets changed or promoted to operational')
    return current, original, read_json(nuisance)


def verify_source_pins(root, events):
    records = []; cache = {}
    for e in events:
        for stem in ('source', 'tar'):
            name, pin = e[stem+'_path'], e[stem+'_sha256']
            if not isinstance(pin,str) or re.fullmatch('[0-9a-f]{64}',pin) is None:
                raise ValueError('Missing source/tar pin')
            path = contained(root,name)
            if not path.exists():
                status = 'DECLARADO_NOT_VERIFIED_HERE'
            else:
                if path not in cache: cache[path] = sha(path)
                if cache[path] != pin: raise ValueError('Source/tar SHA256 mismatch')
                status = 'FILE_HASH_VERIFIED_HERE'
            records.append(dict(event=e['event_id'],kind=stem,path=name,sha256=pin,status=status))
    return records


def matrix_rite(reg, nuisance, events, source_pins):
    counts = {role:sum(e['role']==role for e in events) for role in ('calibration','blind_test')}
    if counts['blind_test']:
        raise ValueError('Blind adapter absent')
    rows = verdict_matrix(reg,nuisance,counts['blind_test'])
    g = nuisance['gate']
    reasons = ['OPEN_NORMALIZED_RESTRICTED_MODEL_IMPLEMENTATION','OPEN_BLIND_RELEASE_ADAPTER']
    for key in ('systematic_calibration_paid','physical_likelihood_paid'):
        if g.get(key) is not True: reasons.append(key)
    for key in ('sigma_c_physically_calibrated','selection_efficiency','global_restricted_prior_normalization'):
        if g.get(key) is None: reasons.append(key)
    if any(v['status'] != 'FILE_HASH_VERIFIED_HERE' for v in source_pins):
        reasons.append('SOURCE_OR_TAR_PINS_NOT_VERIFIED_HERE')
    for row in rows:
        targets = json.loads(json.dumps(reg['e7']['readings'][row['reading']]['conditional_E0_targets']))
        for target in targets:
            val=target['N90_mixture_illustration_not_selection']
            target['N90_ceiling'] = math.ceil(val) if val is not None else None
            target['scope_label']='CONDITIONAL_PLANNING_ONLY'
            target['limitation']='limite inferior até σ_jit,rec'
        row.update(conditional_E0_targets=targets,systematic_gate='red',gate_reasons=list(reasons),
                   test_count=counts['blind_test'],N_target_information=None)
    return rows, counts


def spline_qnm(spins, coefficients, mode):
    """Evaluate pinned not-a-knot cubic coefficients; never extrapolate.

    The table is derived from the registered qnm grid in a separate producer
    preparation. It is interpolation of a grid, not an exact analytic QNM.
    """
    data=coefficients['modes'][mode]
    x=np.asarray(data['x'],float); c=np.asarray(data['c_real'],float)+1j*np.asarray(data['c_imag'],float)
    a=np.asarray(spins,float)
    if x.ndim!=1 or len(x)<4 or np.any(np.diff(x)<=0) or c.shape!=(4,len(x)-1) or not np.isfinite(c).all():
        raise ValueError('Invalid pinned spline')
    if not np.isfinite(a).all():raise ValueError('Nonfinite spin')
    if np.any(a<x[0]) or np.any(a>x[-1]):return None
    ix=np.clip(np.searchsorted(x,a,side='right')-1,0,len(x)-2);dx=a-x[ix]
    return ((c[0,ix]*dx+c[1,ix])*dx+c[2,ix])*dx+c[3,ix]


def paired_qnm_diagnostics(root, reg, events):
    spec=reg['e7_rite_v1_1'];path=contained(root,spec['qnm_coefficients_path'])
    require_pin(path,spec['qnm_coefficients_sha256']);coefficients=read_json(path)
    grid_path=contained(root,spec['qnm_grid_path']);require_pin(grid_path,spec['qnm_grid_sha256'])
    if coefficients['grid_sha256']!=spec['qnm_grid_sha256']:raise ValueError('QNM grid provenance differs')
    rows=[]
    for e in events:
        s=e['samples'];q=spline_qnm(s['af'],coefficients,'220')
        for reading in READINGS:
            if q is None:
                rows.append(dict(event=e['event_id'],reading=reading,mode='220',status='OPEN_SPIN_OUTSIDE_GRID',N=e['N']))
                continue
            pred=prediction_draws(s['Mfdet'],s['af'],s['z'],reading,qnm_dimensionless=q)
            d=pred['delta_tau']
            rows.append(dict(event=e['event_id'],reading=reading,mode='220',N=e['N'],status=pred['status'],
                statute=pred['statute'],delta_tau_05_50_95=None if d is None else np.quantile(d,[.05,.5,.95]).tolist(),
                qnm_scope='PAIRED_INTERPOLATION_OF_PINNED_QNM_GRID_NO_EXTRAPOLATION',lnB=None,z_physical=None))
    # 440 was evaluated on paired draws by T05. Preserve its receipt and label;
    # no need to re-read HDF5 or silently rewrite the four legacy formulas.
    t05_path=contained(root,spec['t05_receipt_path']);require_pin(t05_path,spec['t05_receipt_sha256'])
    t05=read_json(t05_path)
    mode440=[v for v in t05['paired_predictions'] if v['mode']=='440']
    return dict(rows220=rows,mode440=dict(status='OPEN_440_SINGLE_EVENT_NONBLIND',
        source='T05_PREVIOUSLY_MEASURED_PAIRED_CALIBRATION',receipt_sha256=spec['t05_receipt_sha256'],
        rows=mode440),physical_N=None,z_physical=None)


def run_rite(root, registration, registration_sha256, nuisance, nuisance_sha256,
             posterior=None, posterior_sha256=None):
    reg, old, noise = embedded_context(root,registration,registration_sha256,nuisance,nuisance_sha256)
    spec = reg['e7_rite_v1_1']; events=[]; source_pins=[]
    plan_path=contained(root,old['e7']['plan_path']);require_pin(plan_path,old['e7']['plan_sha256'])
    plan=read_json(plan_path)
    # Reject a blind plan BEFORE opening posterior bytes.
    if any(e['role']!='calibration' or e['event_id'] not in old['calibration_event_ids'] for e in plan['events']):
        raise ValueError('Blind adapter absent; calibration-only plan required')
    receipt_path=contained(root,spec['execution_receipt_path']);require_pin(receipt_path,spec['execution_receipt_sha256'])
    receipt=read_json(receipt_path)
    if receipt['status']!='E7_EXECUTED_NO_PHYSICAL_TEST' or receipt.get('failure') is not None:
        raise ValueError('Historical E7 execution failed')
    if posterior is not None:
        expected=receipt['products'][spec['posterior_product_name']]['sha256']
        if posterior_sha256!=expected:raise ValueError('Only witnessed historical calibration product admitted')
        require_pin(posterior,posterior_sha256)
        auth_path=contained(root,spec['legacy_authorization_path'])
        auth_pin=receipt['authorization_sha256']
        # This proves historical authorization, not a new blind authorization.
        guard=type('HistoricalClock',(),{'utc':staticmethod(utc)})
        checked_authorization(old,guard,spec['legacy_registration_sha256'],auth_path,auth_pin)
        payload=read_json(posterior)
        events=validate_payload_contract(payload,plan,old['e7'],spec['legacy_registration_sha256'],auth_pin)
        if any(e['role']!='calibration' or e['event_id'] not in reg['calibration_event_ids'] for e in events):
            raise ValueError('Only registered calibration events admitted')
        source_pins=verify_source_pins(root,events)
    matrix,counts=matrix_rite(reg,noise,events,source_pins)
    missing=any(v['status']!='FILE_HASH_VERIFIED_HERE' for v in source_pins)
    notice=('pins transportados do recibo E7_FINAL_EXECUTION_V1 ('+spec['execution_receipt_sha256'][:16]+
            '), não conferidos aqui [DECLARADO]') if missing else None
    if notice:print(notice)
    paired=paired_qnm_diagnostics(root,reg,events)
    for row in matrix:
        if row['mode_variant']=='220_plus_440_INPUT':row['mode_data_status']=paired['mode440']['status']
    return dict(status='AWAITING_DATA',scope='NONBLIND_HISTORICAL_CALIBRATION_REPLAY_NOT_A_PHYSICAL_TEST',
        registration_sha256=registration_sha256,posterior_sha256=posterior_sha256,nuisance_sha256=nuisance_sha256,
        historical_registration_sha256=spec['legacy_registration_sha256'],source_pins=source_pins,pin_notice=notice,
        beta_runtime=beta_runtime(),test_count=counts['blind_test'],role_counts=counts,matrix=matrix,
        fullsample_diagnostics=fullsample_diagnostics(events,reg['statistics']),
        conditional_readings=reading_diagnostics(events),paired_qnm_diagnostics=paired,gate_changed=False,lnB=None,z_physical=None,
        heavy_job_authorized=False,blind_data_authorized=False)


def main():
    ap=argparse.ArgumentParser(description='T12 calibration-only portable rite; no external guard import')
    for key in ('root','registration','registration-sha256','nuisance','nuisance-sha256','output'):
        ap.add_argument('--'+key,required=True)
    ap.add_argument('--posterior');ap.add_argument('--posterior-sha256')
    a=ap.parse_args()
    result=run_rite(a.root,a.registration,a.registration_sha256,a.nuisance,a.nuisance_sha256,a.posterior,a.posterior_sha256)
    publish_new(a.output,result)


if __name__=='__main__':main()
