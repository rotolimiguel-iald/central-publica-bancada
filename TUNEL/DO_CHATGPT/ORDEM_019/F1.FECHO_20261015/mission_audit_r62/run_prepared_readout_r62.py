"""One frozen synthetic run. Reuse the existing full joint Liouvillian only."""
from pathlib import Path
import argparse
import ast
import datetime
import hashlib
import importlib.util
import json
import math
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    path = Path(path)
    return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}

def write_new(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf8')
    with Path(path).open('xb') as handle:
        handle.write(data)

def verify_pin(row):
    if sha(row['path']) != row['sha256']:
        raise ValueError('Changed frozen file: ' + row['path'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', required=True)
    args = parser.parse_args()
    freeze_path = Path(args.freeze).resolve()
    freeze = json.loads(freeze_path.read_text(encoding='utf8'))
    if freeze['status'] != 'FROZEN_AFTER_PREEXEC_REVIEW_AND_ROOT_PREFLIGHT':
        raise ValueError('Freeze not authorized')
    for row in freeze['files']:
        verify_pin(row)
    required = {str(BASE / name) for name in ['PREPARED_READOUT_PLAN_R62.json',
                 'finite_device_functions_r62.py', 'run_prepared_readout_r62.py',
                 'PREEXEC_REVIEW_R62.json']}
    if not required.issubset({r['path'] for r in freeze['files']}):
        raise ValueError('Missing execution pin')
    if not freeze.get('root_preflight_verified') or not freeze.get('root_execution_order_received'):
        raise ValueError('Root preflight/order not recorded')
    started = datetime.datetime.now(datetime.timezone.utc)
    if datetime.datetime.fromisoformat(freeze['created_utc']) >= started:
        raise ValueError('Freeze must precede start')
    plan = json.loads((BASE / 'PREPARED_READOUT_PLAN_R62.json').read_text(encoding='utf8'))
    for row in plan['source_pins']:
        verify_pin(row)
    review = json.loads((BASE / 'PREEXEC_REVIEW_R62.json').read_text(encoding='utf8'))
    if not str(review.get('status', review.get('verdict', ''))).startswith('PASS'):
        raise ValueError('Independent pre-execution review did not pass')
    run = BASE / 'run_r62'
    run.mkdir(exist_ok=False)
    start = {'status': 'RUNNING', 'started_utc': started.isoformat(),
             'freeze': pin(freeze_path), 'runner': pin(__file__),
             'scope': 'Synthetic 8-dimensional readout; no observed data or physical calibration.'}
    write_new(run / 'START_R62.json', start)
    timer = time.perf_counter()
    try:
        result = calculate(plan)
        result.update({'started_utc': started.isoformat(),
                       'ended_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       'seconds': time.perf_counter() - timer,
                       'freeze': pin(freeze_path)})
        write_new(run / 'RESULT_R62.json', result)
        print(json.dumps({'status': result['status'], 'checks': len(result['checks']),
                          'failed': [c['name'] for c in result['checks'] if not c['passed']],
                          'seconds': result['seconds'], 'result': pin(run / 'RESULT_R62.json')}))
        return 0 if result['status'] == 'PASS_FINITE_SYNTHETIC_READOUT' else 1
    except Exception:
        result = {'status': 'NUMERICAL_OR_EXECUTION_FAILURE', 'started_utc': started.isoformat(),
                  'ended_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'seconds': time.perf_counter() - timer, 'traceback': traceback.format_exc(),
                  'retry_automatic': False}
        write_new(run / 'FAILURE_R62.json', result)
        print(json.dumps(result))
        return 1

def calculate(plan):
    import numpy as np
    import scipy
    from scipy.linalg import expm
    spec = importlib.util.spec_from_file_location('frozen_finite_device_r62', BASE / 'finite_device_functions_r62.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    checks = []
    def check(name, metric, bound, relation='le'):
        value = float(metric)
        passed = math.isfinite(value) and (value <= bound if relation == 'le' else value > bound)
        checks.append({'name': name, 'value': value, 'relation': relation, 'bound': bound, 'passed': bool(passed)})
    def expect(rho, op):
        value = complex(np.trace(rho @ op))
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise ValueError('Nonfinite expectation')
        return value
    def complex_json(value):
        return {'re': float(value.real), 'im': float(value.imag)}
    def phase(value):
        if abs(value) <= 1e-8:
            return {'status': 'PHASE_UNDEFINED_LOW_MODULUS', 'value': None}
        return {'status': 'DEFINED_SYNTHETIC_PHASE', 'value': float(np.angle(value))}
    model = plan['model']
    m = model['parameters']
    for key, value in m.items():
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
            raise ValueError('Invalid strictly positive model parameter: ' + key)
    alpha_path = next(row['path'] for row in plan['source_pins'] if 'ALPHA_FINE_CODATA_2018' in row['role'])
    constants = {}
    for node in ast.parse(Path(alpha_path).read_text(encoding='utf8')).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in {'ALPHA_FINE_CODATA_2018', '_SEALED_ALPHA_CODATA_2018'}:
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    alpha = constants['ALPHA_FINE_CODATA_2018']
    if alpha != constants['_SEALED_ALPHA_CODATA_2018'] or not math.isfinite(alpha):
        raise ValueError('Canonical alpha pin/constant mismatch')
    beta = alpha * math.sqrt(math.e)
    lam = beta * model['gamma_Lambda']
    if not 0 < beta < .5 or not lam > 0:
        raise ValueError('Invalid holographic rate')
    dims = tuple(model['dims'])
    if dims != (2, 2, 2):
        raise ValueError('Unexpected cutoff')
    lower = np.array([[0, 1], [0, 0]], dtype=complex)
    z = np.diag([1., -1.]).astype(complex)
    ai = old.embed(lower, (0,), dims); ao = old.embed(lower, (1,), dims)
    sm = old.embed(lower, (2,), dims); sp = sm.conj().T
    Zi = old.embed(z, (0,), dims); Zoh = old.embed(z, (2,), dims)
    h = m['omega_c'] * (ai.conj().T @ ai + ao.conj().T @ ao) + m['omega_OH'] * (sp @ sm)
    h += m['g_JC'] * (ai.conj().T @ sm + sp @ ai) + m['Omega'] * (sp + sm)
    jump = ao.conj().T @ sm + sp @ ai
    jumps = [(m['kappa_in'], ai), (m['kappa_out'], ao), (m['gamma_OH'], sm),
             (m['gamma_dephasing'], Zoh), (lam, jump)]
    gen = old.liouvillian(h, jumps)
    C = ai @ ao; B = ai.conj().T @ ao
    Xi = (ai + ai.conj().T) / math.sqrt(2); Xo = (ao + ao.conj().T) / math.sqrt(2)
    Pi = 1j * (ai.conj().T - ai) / math.sqrt(2); Po = 1j * (ao.conj().T - ao) / math.sqrt(2)
    quadratures = [('XX', Xi, Xo), ('PP', Pi, Po), ('XP', Xi, Po), ('PX', Pi, Xo)]
    for label, u, v in quadratures:
        check('operator_quadratic_' + label, old.residual((u+v)@(u+v) - (u-v)@(u-v) - 4*u@v), 1e-12)
    states = []
    q = .5
    for label, phi in [('0', 0.), ('Pi2', math.pi / 2)]:
        pair = np.array([1., 0., 0., q*np.exp(1j*phi)], complex) / math.sqrt(1+q*q)
        relative = np.array([0., np.exp(1j*phi), 1., 0.], complex) / math.sqrt(2)
        states.append(('pair_phi'+label, np.kron(old.projector(pair), np.eye(2)/2)))
        states.append(('relative_phi'+label, np.kron(old.projector(relative), np.eye(2)/2)))
    epsilon = .5
    D = Zi @ (ao + ao.conj().T) @ (sm + sp)
    states += [('rho_plus', (np.eye(8)+epsilon*D)/8), ('rho_minus', (np.eye(8)-epsilon*D)/8)]
    initial = {}
    for name, rho in states:
        old.validate_density(rho, 1e-10)
        drho = old.direct_generator(h, jumps, rho)
        check('generator_' + name, old.residual(old.unvec(gen @ old.vec(rho), 8) - drho), 1e-12)
        initial[name] = {'C': expect(rho, C), 'B': expect(rho, B), 'dC': expect(drho, C), 'dB': expect(drho, B)}
    for name, sign in [('rho_plus', 1), ('rho_minus', -1)]:
        check('initial_dC_' + name, abs(initial[name]['dC'] + sign*1j*epsilon*m['g_JC']/4), 1e-12)
        check('initial_dB_' + name, abs(initial[name]['dB'] - sign*1j*epsilon*m['g_JC']/4), 1e-12)
    check('initial_nonclosure_difference', abs(initial['rho_plus']['dC']-initial['rho_minus']['dC']), 1e-6, 'gt')
    rows = []
    mutations = {'wrong_imaginary_sign': [], 'missing_LO_normalization': []}
    for t in model['times']:
        if isinstance(t, bool) or not isinstance(t, (float, int)) or not math.isfinite(t) or t < 0:
            raise ValueError('Invalid frozen time')
        channel = expm(t*gen)
        for name, rho0 in states:
            rho = old.unvec(channel @ old.vec(rho0), 8)
            if not np.isfinite(rho).all(): raise ValueError('Nonfinite evolved density')
            tag = name + '_t' + str(t)
            check('hermitian_' + tag, old.residual(rho-rho.conj().T), 1e-10)
            check('trace_' + tag, abs(np.trace(rho)-1), 1e-10)
            check('positive_' + tag, max(0., -float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())), 1e-10)
            Q = {}; M = {}
            for label, u, v in quadratures:
                val = expect(rho, u@v)
                check('real_moment_' + label + '_' + tag, abs(val.imag), 1e-10)
                Q[label] = val.real
                M[label] = val.real - expect(rho,u).real * expect(rho,v).real
                norm_readout = (expect(rho,(u+v)@(u+v))-expect(rho,(u-v)@(u-v)))/4
                check('norm_readout_' + label + '_' + tag, abs(norm_readout-val), 1e-10)
            c = (Q['XX']-Q['PP']+1j*(Q['XP']+Q['PX']))/2
            b = (Q['XX']+Q['PP']+1j*(Q['XP']-Q['PX']))/2
            direct_c = expect(rho,C); direct_b = expect(rho,B)
            check('C_read_' + tag, abs(c-direct_c), 1e-10)
            check('B_read_' + tag, abs(b-direct_b), 1e-10)
            check('C_modulus_' + tag, abs(abs(c)**2-((Q['XX']-Q['PP'])**2+(Q['XP']+Q['PX'])**2)/4), 1e-10)
            check('B_modulus_' + tag, abs(abs(b)**2-((Q['XX']+Q['PP'])**2+(Q['XP']-Q['PX'])**2)/4), 1e-10)
            mean_i = expect(rho,ai); mean_o = expect(rho,ao)
            ccov = (M['XX']-M['PP']+1j*(M['XP']+M['PX']))/2
            bcov = (M['XX']+M['PP']+1j*(M['XP']-M['PX']))/2
            check('C_centered_' + tag, abs(ccov-(direct_c-mean_i*mean_o)), 1e-10)
            check('B_centered_' + tag, abs(bcov-(direct_b-mean_i.conjugate()*mean_o)), 1e-10)
            pc = phase(direct_c); pb = phase(direct_b)
            for obs, read, direct, ph in [('C',c,direct_c,pc), ('B',b,direct_b,pb)]:
                if ph['value'] is not None:
                    check('phase_' + obs + '_' + tag, abs(np.angle(read/direct)), 1e-8)
                elif t == 0 and name in {'rho_plus','rho_minus'}:
                    check('undefined_phase_' + obs + '_' + tag, float(phase(read)['value'] is not None), 0.)
            if t == 0:
                if name in {'pair_phiPi2','relative_phiPi2'}:
                    mutations['wrong_imaginary_sign'] += [abs(c.conjugate()-direct_c), abs(b.conjugate()-direct_b)]
                mutations['missing_LO_normalization'] += [abs(2*c-direct_c), abs(2*b-direct_b)]
            rows.append({'state':name,'time':t,'quadrature_moments':Q,'centered_quadratures':M,
                         'mean_in':complex_json(mean_i),'mean_out':complex_json(mean_o),
                         'C_direct':complex_json(direct_c),'C_read':complex_json(c),
                         'B_direct':complex_json(direct_b),'B_read':complex_json(b),
                         'C_covariance':complex_json(ccov),'B_covariance':complex_json(bcov),
                         'phase_C':pc,'phase_B':pb})
    for name, values in mutations.items():
        check('negative_' + name, max(values), 1e-6, 'gt')
    loss_error = abs(initial['pair_phi0']['dC'] + 2j*m['omega_c']*initial['pair_phi0']['C'])
    check('negative_drop_loss_reading', loss_error, 1e-6, 'gt')
    check('negative_drop_OH_correlations', abs(initial['rho_plus']['dC']), 1e-6, 'gt')
    return {'status':'PASS_FINITE_SYNTHETIC_READOUT' if all(c['passed'] for c in checks) else 'FAIL_FINITE_READOUT',
            'versions':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
            'parameters':m,'gamma_Lambda':model['gamma_Lambda'],'alpha_runtime':alpha,'beta_runtime':beta,'lambda_runtime':lam,
            'model_scope':'Existing 2x2x2 full GKLS; parameters/times dimensionless INPUT. No measurement of beta.',
            'states':len(states),'times':model['times'],'rows':rows,'checks':checks,
            'initial_values':{name:{key:complex_json(value) for key,value in values.items()} for name,values in initial.items()},
            'limits':['No physical homodyne POVM or shot data.','No OH clock waveform derived.',
                      'No transfer to infinite bosonic CCR.','No R4/R5 acceptance or gate change.',
                      'No renormalization, factorization, positivity clipping or state replacement.']}

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
