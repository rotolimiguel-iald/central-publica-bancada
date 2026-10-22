"""Conditional F9 extra-parameter profiles; prepared, not numerically executed.

The trusted caller injects the pinned a987 consumer and df482 curve geometry.
No data access, new Gaussian solver, optimizer, prior integration or certificate.
"""
import math

REQUEST_ID = '4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3'
# BEGIN SOURCE PINS
SOURCE_PINS = {'dependency_board': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\preregistros\\f9_completion_dependencies\\QUADRO_F9_ATE_V1.md', 'bytes': 36718, 'sha256': 'c965992156debd0508eaf2f4afeb937ecca1ceb96b5aba7577881d35d5813d56'}, 'physical_prior': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\physical_prior.py', 'bytes': 21629, 'sha256': '4fbae1160282875c4ed61c242361c14db9434416a1886d41905c79f0a4f7a3f6'}, 'prior_derivation': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\DERIVACAO.md', 'bytes': 12288, 'sha256': '1dd3d81dc735799050d3cf055342ab498e2a37f0932a6044e3e2e785265367ad'}, 'prior_api': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\API_CONTRATO.md', 'bytes': 10781, 'sha256': '9cb26ecd71dcdf54c7d8989cb21c03e1a92c0fb76e8026886862906bbd4b87b7'}, 'consumer': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\likelihood_consumer.py', 'bytes': 24982, 'sha256': '6776bb660f6b8565c7282f937ecdc5239d5b941cce3e257aa6155379c9ccd6a5'}, 'consumer_api': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\API_CONTRATO.md', 'bytes': 14238, 'sha256': '449e4ffb95a4af757384db4e1277741d37ffc1a7ab8d47d980910e6a5baabc77'}, 'prior_review': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\derivacoes\\revisao_f9_physical_prior\\PARECER_PRIORS_FISICOS_F9.md', 'bytes': 8641, 'sha256': '9bc6d2b8b94ddd46e966f8eaa63a1f90394923225c327be9890b229c0da70f6b'}, 'certificate_interface': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_numerical_certification_preparation\\INTERFACE_CERTIFICADOS_F9.json', 'bytes': 11018, 'sha256': 'df431bf0919b87dcbd9620f8852fac8192591f16efe23d51a7b7b12644cbd9ba'}, 'linear_gaussian': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\linear_gaussian.py', 'bytes': 3772, 'sha256': '7dc486b5568876385f4b2e6647e0f449accfea0862c3b0d46ce90d657fba2736'}, 'singular_gaussian': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\singular_gaussian_v2.py', 'bytes': 4953, 'sha256': '98264bdd57aaad0904bd342631fd3c147fa19f90e8922f0ad6b15ac1b3b93374'}}
# END SOURCE PINS
MODELS = ('H1_TGL', 'H2_LCDM', 'H3_beta_free', 'H4_Cepheid', 'H5_rd_free')
THETA_NAMES = ('H0', 'ombh2', 'omch2')
THETA_BOUNDS = ((50.0, 90.0), (0.015, 0.030), (0.08, 0.18))


def _unavailable_certificates():
    return {
        'conditional_minimum': {'status': 'UNAVAILABLE', 'lower': None, 'upper': None,
                                'certificate': None, 'verified': False},
        'global_theta_minimum': {'status': 'NOT_SEARCHED', 'estimate': None,
                                 'lower': None, 'upper': None, 'certificate': None,
                                 'verified': False}}


def _q_at_mean(joint, mean, consumer):
    """Evaluate only the norm of the residual projected by the existing backend."""
    residual = joint._y - mean
    check = joint._engine.support.evaluate(residual)
    consumer._require(check['support_ok'] and math.isfinite(check['null_residual_norm']),
                      'PROFILE_SUPPORT_INCONSISTENCY', 'feasible profile residual')
    projected = joint._engine.residualize(residual[:, None])[:, 0]
    consumer._require(bool(joint._np.isfinite(projected).all()),
                      'PROFILE_NONFINITE_RESIDUAL', 'existing residualize output')
    value = float(projected @ projected)
    consumer._require(math.isfinite(value) and value >= 0,
                      'PROFILE_QUADRATIC_RANGE', 'finite nonnegative norm required')
    consumer._require(value != 0 or bool((projected == 0).all()),
                      'PROFILE_NORM_UNDERFLOW', 'nonzero vector must not yield zero norm')
    return value, consumer._diagnostic(check)


def _physical_point(model, coordinate, curve, reference, prior, consumer):
    """Return a feasible physical extra AND its actual float forward coordinate."""
    need, finite = consumer._require, consumer._number
    if model == 'H3_beta_free':
        name, physical, realized = 'beta', coordinate, coordinate
        bounds = prior.BETA_LIMITS
    elif model == 'H4_Cepheid':
        name, bounds = 's', prior.S_LIMITS
        if coordinate == curve.lower:
            physical = bounds[1]
        elif coordinate == curve.upper:
            physical = bounds[0]
        elif coordinate == curve.reference:
            physical = reference
        else:
            physical = math.expm1(-(math.log(10) / 5) * coordinate)
        # Endpoints are evaluated as the same transformed endpoints as df482.
        if physical == bounds[1]:
            realized = curve.lower
        elif physical == bounds[0]:
            realized = curve.upper
        elif physical == reference:
            realized = curve.reference
        else:
            realized = -5 * math.log1p(physical) / math.log(10)
    elif model == 'H5_rd_free':
        name, bounds = 'rd_Mpc', prior.RD_LIMITS
        if coordinate == curve.lower:
            physical = bounds[1]
        elif coordinate == curve.upper:
            physical = bounds[0]
        elif coordinate == curve.reference:
            physical = reference
        else:
            physical = 1 / coordinate
        realized = 1 / physical
    else:
        raise ValueError('unknown affine extra model')
    physical, realized = finite(physical, 'physical profile point'), finite(realized, 'forward coordinate')
    need(bounds[0] <= physical <= bounds[1] and curve.lower <= realized <= curve.upper,
         'PROFILE_MAPPING_OUTSIDE_DOMAIN', 'no silent clipping of inverse mapping')
    return name, physical, realized, list(bounds)


def _extra_profile(model, curve, reference, parameters, prior, consumer):
    geometry = {'A': curve.a, 'B': curve.b, 'reference': curve.reference,
                'affine_interval': [curve.lower, curve.upper],
                'endpoint_support': curve.endpoint_support,
                'flat_status_is_not_exact_scientific_certificate': True}
    output = {'geometry': geometry, 'certificates': _unavailable_certificates(),
              'q_feasible_estimate': None, 'log_profile_deta': None,
              'physical_parameters': None, 'affine_candidate': None,
              'affine_evaluated': None, 'roundtrip_shift': None,
              'residual_support': None, 'argmin_description': None}
    if curve.zero_density:
        output.update(status='ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT',
                      log_profile_deta=float('-inf'),
                      residual_support=curve.base_point['residual_support'],
                      argmin_description='No finite feasible q witness returned; support diagnosis is not a numerical failure surrogate.')
        return output
    # A=0 was admitted only when every projected component is float-exact zero.
    # The default prior_linear=0 is essential: B-lambda belongs to integration.
    coordinate = curve.reference if curve.flat_in_float_geometry else curve.peak()
    name, physical, realized, bounds = _physical_point(model, coordinate, curve,
                                                       reference, prior, consumer)
    point = dict(parameters)
    point[name] = physical
    mean = curve.mean(realized)
    q_value, support = _q_at_mean(curve.joint, mean, consumer)
    if curve.flat_in_float_geometry:
        log_value = curve.base_point['log_integral_deta']
        status = 'FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY'
        argmin = {'kind': 'ENTIRE_EXTRA_DOMAIN_IN_PROJECTED_FLOAT_GEOMETRY',
                  'physical_interval': bounds, 'representative': 'original reference',
                  'scientific_identifiability_claim': False}
    else:
        log_value = curve.log_likelihood(realized)
        status = 'CONDITIONAL_FEASIBLE_PROFILE_ESTIMATE'
        argmin = {'kind': 'RESTRICTED_QUADRATIC_VERTEX_IN_FLOAT_GEOMETRY',
                  'formula': 'xref+clip(B/A,[lo-xref,hi-xref])',
                  'active_affine_boundary': 'lower' if coordinate == curve.lower else
                                            'upper' if coordinate == curve.upper else 'interior',
                  'roundtrip_evaluated': True, 'certified_minimizer': False}
    consumer._number(log_value, 'finite profile log-integral')
    output.update(status=status, q_feasible_estimate=q_value, log_profile_deta=log_value,
                  physical_parameters=point, affine_candidate=coordinate,
                  affine_evaluated=realized, roundtrip_shift=realized-coordinate,
                  residual_support=support, argmin_description=argmin)
    return output


def profile_at_fixed_theta(joint, assembly_json, *, assembly_sha256, background_json,
                           consumer_module, physical_prior_module,
                           caller_verification_reference):
    """Five conditional profile estimates at a single fixed admitted theta.

Caller verifies loaded modules externally. Receipts are not authorization.
No physical prior density/Jacobian is applied to this likelihood profile.
"""
    c, p = consumer_module, physical_prior_module
    c._require(getattr(c, 'REQUEST_ID', None) == 'a9874f79-9d71-48f5-824c-d51d6d819534'
               and getattr(p, 'REQUEST_ID', None) == 'df482198-56c4-4169-ae5e-3908f5d12f2c'
               and isinstance(joint, c.PreparedJoint),
               'PROFILE_DEPENDENCY_IDENTITY', 'pinned consumer and curve provider')
    c._reference(caller_verification_reference, 'externally verified loaded profile dependencies')
    c._require(c.MODELS == MODELS and p.MODELS == MODELS
               and p.SOURCE_PINS['f9_likelihood_consumer_preparation/likelihood_consumer.py'] == SOURCE_PINS['consumer']
               and c.SOURCE_PINS['linear_gaussian'] == SOURCE_PINS['linear_gaussian']
               and c.SOURCE_PINS['support'] == SOURCE_PINS['singular_gaussian'],
               'PROFILE_DEPENDENCY_PINS', 'exact source lineage; caller verifies actual objects')
    c._require(p.BETA_LIMITS == (-0.05, 0.05) and p.S_LIMITS == (-0.15, 0.15)
               and p.RD_LIMITS == (130.0, 160.0), 'PROFILE_DOMAIN_CHANGED', 'frozen physical domains')
    packet = c._json(assembly_json, assembly_sha256, 'fixed-theta profile assembly')
    pointwise = joint.evaluate_five(assembly_json, assembly_sha256=assembly_sha256)
    background_sha = packet['identity']['background_packet_sha256']
    bg = c._json(background_json, background_sha, 'same computed background')
    c._require(bg.get('schema') == 'F9_BACKGROUND_PACKET_V1' and
               bg.get('status') == 'ENGINEERING_RESULT' and bg.get('error') is None and
               bg['identity'] == packet['identity']['background_identity'],
               'PROFILE_BACKGROUND_IDENTITY', 'frozen shared background')
    theta = tuple(c._number(packet['models']['H2_LCDM']['parameters'][n], n) for n in THETA_NAMES)
    c._require(tuple(bg['result']['theta']) == theta and tuple(bg['identity']['theta']) == theta
               and all(lo <= value <= hi for value, (lo, hi) in zip(theta, THETA_BOUNDS)),
               'PROFILE_THETA_MISMATCH', 'one theta within original domain')
    extras = {'H1_TGL': (), 'H2_LCDM': (), 'H3_beta_free': ('beta',),
              'H4_Cepheid': ('s',), 'H5_rd_free': ('rd_Mpc',)}
    densities = {'H1_TGL': '1', 'H2_LCDM': '1', 'H3_beta_free': '10',
                 'H4_Cepheid': '10/3', 'H5_rd_free': '1/30'}
    for model in MODELS:
        record = packet['models'][model]
        names = (*THETA_NAMES, *extras[model])
        c._keys(record['parameters'], names, model + ' parameters')
        c._require(tuple(c._number(record['parameters'][n], n) for n in THETA_NAMES) == theta,
                   'PROFILE_THETA_MISMATCH', model)
        c._require(record['prior'] == {'coordinates': list(names),
                   'common_theta_density_exact': '50/3', 'extra_density_exact': densities[model],
                   'measure': 'uniform_in_listed_coordinates'}, 'PROFILE_PRIOR_CHANGED', model)
    np = joint._np
    vectors = {m: np.array(packet['models'][m]['mean_without_nuisance'], dtype='<f8') for m in MODELS}
    responses = joint._structure['response_columns']
    ah = np.array([float(c._fraction(v, 'a_h')) for v in responses['a_h']], dtype='<f8')
    cc = np.array([float(c._fraction(v, 'c_C')) for v in responses['c_C']], dtype='<f8')
    I, E = c._number(bg['result']['I_law'], 'I_law'), c._number(bg['result']['E_law'], 'E_law')
    c._require(E > 0 and math.isclose(I, (2 / 3) * math.log(E), rel_tol=1e-12, abs_tol=1e-14),
               'PROFILE_BACKGROUND_LAW', 'same engineering I/E check as df482')
    beta_ref = c._number(packet['models']['H3_beta_free']['parameters']['beta'], 'beta reference')
    s_ref = c._number(packet['models']['H4_Cepheid']['parameters']['s'], 's reference')
    rd_ref = c._number(packet['models']['H5_rd_free']['parameters']['rd_Mpc'], 'rd reference')
    c._require(p.BETA_LIMITS[0] <= beta_ref <= p.BETA_LIMITS[1]
               and p.S_LIMITS[0] <= s_ref <= p.S_LIMITS[1]
               and p.RD_LIMITS[0] <= rd_ref <= p.RD_LIMITS[1],
               'PROFILE_REFERENCE_OUTSIDE_DOMAIN', 'original extra domains')
    # Same affine construction as df482, whose internal curves have no export API.
    # Reuse _Curve itself rather than integrate priors just to retrieve geometry.
    dlo = -5 * math.log1p(p.S_LIMITS[1]) / math.log(10)
    dhi = -5 * math.log1p(p.S_LIMITS[0]) / math.log(10)
    dref = -5 * math.log1p(s_ref) / math.log(10)
    v5 = np.zeros(283, dtype='<f8')
    v5[3:16] = vectors['H5_rd_free'][3:16] * rd_ref
    curves = {
        'H3_beta_free': p._Curve(joint, vectors['H3_beta_free'], (I / math.log(10)) * ah,
                                beta_ref, *p.BETA_LIMITS, pointwise['models']['H3_beta_free']),
        'H4_Cepheid': p._Curve(joint, vectors['H4_Cepheid'], cc, dref, dlo, dhi,
                              pointwise['models']['H4_Cepheid']),
        'H5_rd_free': p._Curve(joint, vectors['H5_rd_free'], v5, 1 / rd_ref,
                              1 / p.RD_LIMITS[1], 1 / p.RD_LIMITS[0],
                              pointwise['models']['H5_rd_free'])}
    outputs = {}
    for model in ('H1_TGL', 'H2_LCDM'):
        base = pointwise['models'][model]
        outside = base['status'] == 'ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT'
        q_value, diagnostic = (None, base['residual_support']) if outside else _q_at_mean(joint, vectors[model], c)
        outputs[model] = {'status': base['status'], 'q_feasible_estimate': q_value,
                          'log_profile_deta': base['log_integral_deta'],
                          'physical_parameters': dict(base['parameters']) if not outside else None,
                          'residual_support': diagnostic, 'extra': None,
                          'certificates': _unavailable_certificates()}
    references = {'H3_beta_free': beta_ref, 'H4_Cepheid': s_ref, 'H5_rd_free': rd_ref}
    for model, curve in curves.items():
        outputs[model] = _extra_profile(model, curve, references[model],
                                        packet['models'][model]['parameters'], p, c)
    return {'schema': 'F9_CONDITIONAL_AFFINE_PROFILE_RESULT_V1', 'request_id': REQUEST_ID,
            'status': 'ENGINEERING_ONLY', 'theta': list(theta), 'models': outputs,
            'scope': 'FEASIBLE_CONDITIONAL_PROFILE_ESTIMATES_AT_FIXED_THETA',
            'base_theta_prior': {'density_exact': '50/3', 'applied': False, 'integrated': False},
            'physical_extra_priors_applied': False, 'global_theta_search_performed': False,
            'measure': pointwise['measure'], 'output_measure': pointwise['output_measure'],
            'common_measure_id': pointwise['common_measure_id'],
            'normalization': pointwise['normalization'],
            'MM_status': 'CONDITIONAL_UNRATIFIED', 'certification': pointwise['certification'],
            'error_scope': 'Coefficient, support, inverse-map, backend and theory errors unbounded; no numerical estimate is a certified upper/lower.',
            'provenance': {'source_pins': SOURCE_PINS, 'assembly_sha256': assembly_sha256,
                           'background_sha256': background_sha,
                           'consumer_admission_sha256': joint._admission_sha256,
                           'caller_verification_reference': dict(caller_verification_reference)},
            'global_minima': None, 'relative_evidence': None,
            'lnB': None, 'p': None, 'sigma': None, 'verdict': None}
