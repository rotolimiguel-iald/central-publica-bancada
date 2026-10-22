"""Explicit reduced-model material compatibility; no physical certification."""
import math
from fractions import Fraction

class ContractError(ValueError):
    pass

def number(value, name):
    if type(value) not in (float, int) or not math.isfinite(value):
        raise ContractError(name + ': finite real, non-boolean required')
    return float(value)

def complex_number(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise ContractError(name + ': [real, imaginary] required')
    return complex(number(value[0], name), number(value[1], name))

def evaluate(data):
    try:
        if data['schema'] != 'iald-material-reduced/v1':
            raise ContractError('unsupported schema')
        if data['units'] != 'angular_frequency_s^-1;C_s^-1':
            raise ContractError('explicit units required')
        if data['origin_kind'] not in ('synthetic', 'documented_input') or not isinstance(data['source_refs'],list) or not data['source_refs'] or not all(isinstance(x,str) and x.strip() for x in data['source_refs']):
            raise ContractError('origin and source references required')
        alpha = number(data['alpha_fine'], 'alpha')
        gamma = number(data['gamma_lambda'], 'gamma_lambda')
        if alpha <= 0 or gamma <= 0:
            raise ContractError('positive alpha and active bath required')
        beta = alpha * math.sqrt(math.e)
        lam = beta * gamma
        g = [complex_number(x, 'g') for x in data['g']]
        pump = [complex_number(x, 'pump') for x in data['pump']]
        detuning = [number(x, 'detuning') for x in data['detunings']]
        if not g or len(g) != len(pump) or len(g) != len(detuning):
            raise ContractError('same nonempty ensemble required')
        norm = math.sqrt(sum(abs(x)**2 for x in g))
        if norm <= 0:
            raise ContractError('nonzero bright mode required')
        b = [x/norm for x in g]
        bright = sum(x.conjugate()*y for x,y in zip(b,pump))
        dark = math.sqrt(sum(abs(y-x*bright)**2 for x,y in zip(b,pump)))
        mean = sum(abs(x)**2*y for x,y in zip(b,detuning))
        mixing = math.sqrt(sum(abs(x*(y-mean))**2 for x,y in zip(b,detuning)))
        c11 = number(data['C11'], 'C11'); c22 = number(data['C22'], 'C22')
        c12 = complex_number(data['C12'], 'C12')
        # Exact arithmetic on the supplied binary floats: no underflow or PSD tolerance.
        determinant = Fraction(c11)*Fraction(c22) - Fraction(c12.real)**2 - Fraction(c12.imag)**2
        if c11 < 0 or c22 < 0 or determinant < 0:
            raise ContractError('C must be positive semidefinite; no physical tolerance repairs it')
        tolerances = data['tolerances']
        limits = {k:number(tolerances[k],k) for k in ('pump_dark','bright_mixing','bath_relative','phase_defect')}
        if any(v < 0 for v in limits.values()):
            raise ContractError('nonnegative tolerances required')
        delta = number(data['delta_reduced'], 'delta_reduced')
        window = number(data['window_s'], 'window_s')
        if window <= 0:
            raise ContractError('positive time window required')
        x = delta*window/2
        if not math.isfinite(x):
            raise ContractError('nonfinite phase product')
        sinc = math.sin(x)/x if x else 1.0
        factor = complex(math.cos(x),math.sin(x))*sinc
        bath_error = max(abs(c11/lam-1),abs(c22/lam-1),abs(c12/lam-1))
        residuals = {'pump_dark':dark,'bright_mixing':mixing,'bath_relative':bath_error,'phase_defect':abs(factor-1)}
        if not all(math.isfinite(v) for v in [beta,lam,norm,*residuals.values()]):
            raise ContractError('nonfinite intermediate result')
        passed = {k:v<=limits[k] for k,v in residuals.items()}
        return {'status':'MODEL_MATCH_WITHIN_INPUT_TOLERANCES' if all(passed.values()) else 'MODEL_MISMATCH',
                'origin_kind':data['origin_kind'],'physical_certification':False,
                'beta_runtime':beta,'lambda':lam,'residuals':residuals,'checks':passed,
                'cross_window_factor':[factor.real,factor.imag],
                'scope':'One-excitation coherent bright subspace and fixed two-channel bath; additional dynamics and device identity unchecked.'}
    except KeyError as e:
        raise ContractError('missing field: '+str(e)) from e
    except (OverflowError, ZeroDivisionError, TypeError) as e:
        raise ContractError('invalid numerical record: '+str(e)) from e

