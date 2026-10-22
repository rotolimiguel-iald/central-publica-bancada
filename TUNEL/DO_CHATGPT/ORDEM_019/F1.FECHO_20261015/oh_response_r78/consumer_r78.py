"""Finite-cut OH/light first variation; all settings are synthetic INPUTs."""
from pathlib import Path
import ast, json, math, hashlib


def calculate(plan):
    import numpy as np
    import scipy
    from scipy import sparse as sp
    from scipy.sparse.linalg import expm_multiply
    src = {x['role']: Path(x['path']) for x in plan['sources']}
    for x in plan['sources']:
        if hashlib.sha256(Path(x['path']).read_bytes()).hexdigest() != x['sha256']:
            raise ValueError('Source pin mismatch: ' + x['role'])
    prior = json.loads(src['r62_plan'].read_text(encoding='utf-8'))
    params = dict(prior['model']['parameters'])
    constants = {}
    for n in ast.parse(src['alpha'].read_text(encoding='utf-8')).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ['ALPHA_FINE_CODATA_2018', '_SEALED_ALPHA_CODATA_2018']:
            constants[n.targets[0].id] = ast.literal_eval(n.value)
    if constants['ALPHA_FINE_CODATA_2018'] != constants['_SEALED_ALPHA_CODATA_2018']:
        raise ValueError('Alpha seal mismatch')
    beta = constants['ALPHA_FINE_CODATA_2018'] * math.sqrt(math.e)
    gamma = prior['model']['gamma_Lambda']; lam = beta * gamma
    nodes = [n for n in ast.walk(ast.parse(src['r66_helpers'].read_text(encoding='utf-8'))) if isinstance(n, ast.FunctionDef) and n.name in ['liou', 'model']]
    if len(nodes) != 2:
        raise ValueError('Pure helper selection mismatch')
    code = compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), str(src['r66_helpers']), 'exec')
    times = plan['times']; tol = plan['tolerances']; checks = []
    def check(name, value, bound, negative=False):
        value = float(value); bound = float(bound)
        checks.append({'name': name, 'value': value, 'bound': bound, 'relation': 'gt' if negative else 'le', 'passed': bool(math.isfinite(value) and math.isfinite(bound) and (value > bound if negative else value <= bound))})
    def vec(x): return x.reshape(-1, order='F')
    def mat(x, d): return x.reshape((d, d), order='F')
    def zjson(a):
        a = np.asarray(a)
        if not np.all(np.isfinite(a)): raise ValueError('Nonfinite complex result')
        return {'real': a.real.tolist(), 'imag': a.imag.tolist()}
    if len(times) != 4 or times[0] != 0 or any(abs(t-j*times[-1]/3) > 1e-15 for j, t in enumerate(times)):
        raise ValueError('Time grid differs from preregistered equal grid')
    branches = {}
    for branch in plan['branches']:
        p = dict(params); local_lam = lam
        if branch['blocked_transfer']:
            p['g_JC'] = 0.; local_lam = 0.
        env = {'np': np, 'sp': sp, 'math': math, 'p': p, 'lam': local_lam}
        exec(code, env)
        mod = env['model'](plan['cut']); d = len(mod['basis']); dd = d*d
        ket = np.zeros(d, complex)
        for term in plan['initial_states'][branch['state']]:
            ket[mod['index'][tuple(term['basis'])]] = complex(*term['amplitude'])
        ket /= np.linalg.norm(ket); rho0 = np.outer(ket, ket.conj()); r0 = vec(rho0)
        ai = mod['ai']; ao = np.zeros((d, d), complex)
        for col, (i, o, e) in enumerate(mod['basis']):
            if o: ao[mod['index'][(i, o-1, e)], col] = math.sqrt(o)
        g = mod['g']; eye = sp.eye(d, format='csr')
        # The physical mapping from this Hamiltonian probe to RF/laser voltage remains OPEN.
        scale = plan['input_gain'] * math.sqrt(p['kappa_in'])
        hprobes = [scale*(ai+ai.conj().T)/math.sqrt(2), scale*(ai-ai.conj().T)/(1j*math.sqrt(2))]
        perturb = [-1j*(sp.kron(eye, sp.csr_matrix(h))-sp.kron(sp.csr_matrix(h.T), eye)) for h in hprobes]
        # Input and output reservoirs are distinct in this model: no added coherent feedthrough at output.
        lout = mod['jumps'][1]
        def receptors(phi):
            return [plan['output_gain']*(np.exp(-1j*(theta+phi))*lout+np.exp(1j*(theta+phi))*lout.conj().T)/math.sqrt(2) for theta in [0., math.pi/2]]
        qs = receptors(0.); badqs = receptors(plan['wrong_LO_offset'])
        def measure(states, operators):
            values = np.array([[np.trace(q@mat(r, d)) for q in operators] for r in states])
            check(branch['name']+'_observable_imag', np.max(np.abs(values.imag)), tol['algebra'])
            return values.real
        baseline = expm_multiply(g, r0, start=0., stop=times[-1], num=4, endpoint=True)
        obs = measure(baseline, qs); badobs = measure(baseline, badqs)
        z = (obs[:, 0]+1j*obs[:, 1])/math.sqrt(2)
        badz = (badobs[:, 0]+1j*badobs[:, 1])/math.sqrt(2)
        check(branch['name']+'_LO_rotation_law', np.max(abs(badz-np.exp(-1j*plan['wrong_LO_offset'])*z)), tol['algebra'])
        trace_error = max(abs(np.trace(mat(r, d))-1) for r in baseline)
        min_eigenvalue = min(np.linalg.eigvalsh((mat(r, d)+mat(r, d).conj().T)/2).min() for r in baseline)
        check(branch['name']+'_baseline_trace', trace_error, tol['algebra'])
        check(branch['name']+'_baseline_positivity', max(0., -float(min_eigenvalue)), tol['algebra'])
        intracavity_ops = [ao.conj().T@ao, ai.conj().T@ao]
        def intracavity(states):
            return np.array([[np.trace(o@mat(r, d)) for o in intracavity_ops] for r in states])
        diagnostic_baseline = intracavity(baseline)
        response = []; rho_errors = []; fd_rows = []; badresponse = []; diagnostic_response = []
        for j, v in enumerate(perturb):
            # Exact finite-dimensional Duhamel equation encoded in one block exponential.
            aug = sp.bmat([[g, None], [v, g]], format='csr')
            y0 = np.r_[r0, np.zeros(dd, complex)]
            both = expm_multiply(aug, y0, start=0., stop=times[-1], num=4, endpoint=True)
            check(branch['name']+f'_baseline_block_{j}', np.max(abs(both[:, :dd]-baseline)), tol['algebra'])
            drho = both[:, dd:]; r = measure(drho, qs); rb = measure(drho, badqs)
            response.append(r); badresponse.append(rb)
            diagnostic_response.append(intracavity(drho))
            check(branch['name']+f'_variation_trace_{j}', max(abs(np.trace(mat(x, d))) for x in drho), tol['algebra'])
            for eps in plan['epsilons']:
                plus = expm_multiply(g+eps*v, r0, start=0., stop=times[-1], num=4, endpoint=True)
                minus = expm_multiply(g-eps*v, r0, start=0., stop=times[-1], num=4, endpoint=True)
                central = (plus-minus)/(2*eps)
                err = float(np.max(abs(central-drho)))
                out_error = float(np.max(abs(measure(central, qs)-r)))
                diagnostic_error = float(np.max(abs(intracavity(central)-intracavity(drho))))
                check(branch['name']+f'_Duhamel_vs_central_state_{j}_{eps}', err, tol['finite_difference_state'])
                check(branch['name']+f'_Duhamel_vs_central_output_{j}_{eps}', out_error, tol['finite_difference_output'])
                check(branch['name']+f'_Duhamel_vs_central_intracavity_{j}_{eps}', diagnostic_error, tol['finite_difference_state'])
                fd_rows.append({'input_quadrature': ['X','P'][j], 'epsilon': eps, 'state_max_error': err, 'output_max_error': out_error, 'intracavity_max_error':diagnostic_error})
                rho_errors.append(err)
        response = np.asarray(response).transpose(1,2,0)
        badresponse = np.asarray(badresponse).transpose(1,2,0)
        h = (response[:, 0, :]+1j*response[:, 1, :])/math.sqrt(2)
        badh = (badresponse[:, 0, :]+1j*badresponse[:, 1, :])/math.sqrt(2)
        check(branch['name']+'_sensitivity_LO_rotation_law', np.max(abs(badh-np.exp(-1j*plan['wrong_LO_offset'])*h)), tol['algebra'])
        response_norm = float(np.max(abs(response)))
        if branch['blocked_transfer']:
            check(branch['name']+'_blocked_first_variation', response_norm, tol['blocked_zero'])
        if branch['state'] == 'unseeded_output':
            check(branch['name']+'_unseeded_baseline_mean_zero', np.max(abs(z)), tol['algebra'])
            # Zero output means are admissible and expected for this seed-free branch, not a physical failure.
            check(branch['name']+'_unseeded_variation_mean_zero', response_norm, tol['blocked_zero'])
        if branch['name'] == 'seeded_full':
            check('wrong_LO_changes_seeded_baseline', np.max(abs(badz-z)), tol['negative_LO_baseline'], True)
        branches[branch['name']] = {
            'state': branch['state'], 'dimension': d, 'parameters_INPUT': p, 'lambda_INPUT': local_lam,
            'baseline_quadratures': obs.tolist(), 'baseline_complex_signal': zjson(z),
            'response_real_2x2_by_time': response.tolist(), 'response_complex_by_input_XP': zjson(h),
            'response_max': response_norm, 'finite_difference_checks': fd_rows,
            'intracavity_diagnostics':{'operators':['n_out','a_in_dagger_a_out'], 'baseline':zjson(diagnostic_baseline), 'first_variation_input_time_operator':zjson(np.asarray(diagnostic_response)), 'not_temporal_detector_correlation':True},
            'complex_linearity_defect_hP_minus_i_hX': zjson(h[:,1]-1j*h[:,0]),
            'wrong_LO': {'offset':plan['wrong_LO_offset'], 'baseline_difference_max':float(np.max(abs(badz-z))), 'response_difference_max':float(np.max(abs(badh-h))), 'response_distinguishable_at_floor':bool(np.max(abs(badh-h)) > tol['response_floor'])},
            'shot_noise': {'instantaneous':'white-noise distribution, not a finite pointwise variance', 'unit_boxcar_integral_duration':times[-1], 'diagonal_contact_variance':plan['output_gain']**2*times[-1]/2, 'not_total_variance':True},
            'zero_response_admissible':True,
        }
    checks.append({'name':'all_branches_finite_json','value':0.,'bound':0.,'relation':'le','passed':True})
    report = {'status':'SYNTHETIC_FINITE_CUT_RESPONSE', 'passed':all(x['passed'] for x in checks), 'checks':checks, 'branches':branches,
              'beta_runtime_INPUT':beta, 'Gamma_INPUT':gamma, 'times':times, 'cut':plan['cut'],
              'full_minus_blocked_seeded_response_max':float(np.max(abs(np.asarray(branches['seeded_full']['response_real_2x2_by_time'])-np.asarray(branches['seeded_blocked']['response_real_2x2_by_time'])))),
              'versions':{'numpy':np.__version__,'scipy':scipy.__version__}, 'limits':plan['limits']}
    json.dumps(report, allow_nan=False)
    return report
