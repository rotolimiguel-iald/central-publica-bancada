"""Exact rational synthetic interfaces. Not a physical calibration admission API."""
from fractions import Fraction

class CalibrationError(ValueError): pass

J0='a_o_dag*sigma_minus + sigma_plus*a_i; ordered=(i,o,OH); unit_coefficients'

def rational(value, unit, *, positive=False):
    if not isinstance(value,dict) or set(value)!= {'numerator','denominator','unit'}:
        raise CalibrationError('Explicit rational quantity required')
    n,d=value['numerator'],value['denominator']
    if type(n) is not int or type(d) is not int or d<=0 or value['unit']!=unit:
        raise CalibrationError('Invalid exact quantity or units')
    q=Fraction(n,d)
    if q<0 or (positive and q<=0): raise CalibrationError('Invalid sign')
    return q

def quantity(value,unit):
    return {'numerator':value.numerator,'denominator':value.denominator,'unit':unit}

def check_scope(kind,normalization):
    if kind!='SYNTHETIC_INPUT' or normalization!=J0:
        raise CalibrationError('Physical receipt not admitted or J0 mismatch')

def collision_coefficients(*,kind,normalization,frequency,angle,p_excited):
    """Leading weak-collision coefficients; not an exact finite-angle generator."""
    check_scope(kind,normalization)
    nu=rational(frequency,'s^-1',positive=True)
    theta=rational(angle,'rad')
    p=rational(p_excited,'dimensionless')
    if p>1: raise CalibrationError('Population outside [0,1]')
    rate=nu*theta**2
    return {'status':'SYNTHETIC_LEADING_WEAK_COLLISION_COEFFICIENTS',
            'lambda_eff':quantity(rate,'s^-1'),
            'J_rate':quantity((1-p)*rate,'s^-1'),
            'J_dagger_rate':quantity(p*rate,'s^-1'),
            'vacuum_target_compatible':p==0,'physical_measurement':False,
            'Gamma':None,'beta':None}

def reference_coefficient(*,kind,normalization,frequency,reference_angle,bridge_hypothesis):
    check_scope(kind,normalization)
    nu=rational(frequency,'s^-1',positive=True)
    if reference_angle is None or bridge_hypothesis!='theta_eff_squared = beta * theta_ref_squared':
        return {'status':'OPEN_INDEPENDENT_REFERENCE','Gamma':None,'physical_measurement':False}
    theta=rational(reference_angle,'rad',positive=True)
    return {'status':'CONDITIONAL_SYNTHETIC_REFERENCE','Gamma':quantity(nu*theta**2,'s^-1'),
            'bridge_verified':False,'independence_verified':False,'physical_measurement':False}

def control_identifiability(controls):
    if not isinstance(controls,list) or not controls: raise CalibrationError('Control contracts required')
    for c in controls:
        if not isinstance(c,dict) or set(c)!= {'label','parameter_dependence'} or not isinstance(c['label'],str):
            raise CalibrationError('Malformed control contract')
    if all(c['parameter_dependence']=='lambda_only' for c in controls):
        return {'status':'OPEN_BETA_GAMMA_DEGENERACY','identifies_beta':False,'proof_scope':'Conditional on generator, preparation and instrument factoring through lambda'}
    return {'status':'OPEN_VERIFY_NEW_PARAMETER_DEPENDENCE','identifies_beta':False}
