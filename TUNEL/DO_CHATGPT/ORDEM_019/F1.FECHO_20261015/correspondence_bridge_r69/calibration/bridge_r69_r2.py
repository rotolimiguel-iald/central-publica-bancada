"""Synthetic calibration contracts. No physical receipt, inference or tomography."""
from pathlib import Path
import ast
import hashlib
import math
import functools
import numpy as np

class BridgeError(ValueError):
    pass


def checked_result(value):
    if isinstance(value, dict):
        for x in value.values(): checked_result(x)
    elif isinstance(value, (list, tuple)):
        for x in value: checked_result(x)
    elif isinstance(value, np.ndarray):
        if not np.isfinite(value).all(): raise BridgeError("Nonfinite array result")
    elif isinstance(value, (int, float, complex, np.number)) and not isinstance(value, (bool,np.bool_)):
        if not np.isfinite(value): raise BridgeError("Nonfinite scalar result")
    return value

def numeric_guard(fn):
    @functools.wraps(fn)
    def guarded(*args, **kwargs):
        try:
            with np.errstate(over='raise', under='raise', divide='raise', invalid='raise'):
                return checked_result(fn(*args, **kwargs))
        except (ArithmeticError, np.linalg.LinAlgError) as exc:
            raise BridgeError("Unsafe finite-precision operation: " + str(exc)) from exc
    return guarded

def stable_norm(value):
    a=array(value,complex_ok=True)
    # hypot scales before squaring; no quadratic form is clamped to zero.
    n=math.hypot(*(float(v) for z in a.ravel() for v in (z.real,z.imag)))
    return number(n)

J0 = "a_o_dag*sigma_minus + sigma_plus*a_i; ordered=(i,o,OH); unit_coefficients"

def number(x, *, positive=False):
    if isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, float, np.integer, np.floating)):
        raise BridgeError("Expected real non-boolean number")
    if not math.isfinite(float(x)) or (positive and x <= 0):
        raise BridgeError("Expected finite number (positive when required)")
    return float(x)

def array(x, shape=None, *, complex_ok=False):
    def reject_bool(value):
        if isinstance(value, (bool, np.bool_)): raise BridgeError("Boolean is not a measurement")
        if isinstance(value, (list,tuple)):
            for item in value: reject_bool(item)
    reject_bool(x)
    a = np.asarray(x)
    if a.dtype.kind not in ('i', 'u', 'f', 'c') or (a.dtype.kind == 'c' and not complex_ok):
        raise BridgeError("Expected numeric non-boolean array")
    if shape is not None and a.shape != shape:
        raise BridgeError("Shape mismatch")
    if not np.isfinite(a).all():
        raise BridgeError("Nonfinite array")
    return a.astype(complex if complex_ok else float)

def validate_calibration(c):
    required = {'kind','J0','time_unit','rate_unit','quadrature_unit','t0_seconds',
                'gain_i','gain_o','lo_i_radians','lo_o_radians','filter_l2_norm',
                'port_model','same_preparation_four_runs'}
    if not isinstance(c, dict) or not required.issubset(c):
        raise BridgeError("Missing calibration keys")
    if c['kind'] != 'SYNTHETIC_INPUT':
        raise BridgeError("Physical evidence admission is not implemented")
    if c['J0'] != J0 or c['time_unit'] != 's' or c['rate_unit'] != 's^-1' or c['quadrature_unit'] != 'dimensionless':
        raise BridgeError("Normalization/unit mismatch")
    if c['port_model'] != 'H_MARKOV_VACUUM_PORTS' or c['same_preparation_four_runs'] is not True:
        raise BridgeError("Port/preparation contract missing")
    for k in ('t0_seconds','gain_i','gain_o','filter_l2_norm'):
        number(c[k], positive=True)
    if abs(c['filter_l2_norm']-1) > 1e-12:
        raise BridgeError("Filter not normalized")
    for k in ('lo_i_radians','lo_o_radians'):
        number(c[k])
    return {'status':'VALIDATED_SYNTHETIC_SCHEMA', 'measurement_verified':False}

def rotation(t):
    number(t)
    return np.array([[math.cos(t), math.sin(t)],[-math.sin(t), math.cos(t)]])

@numeric_guard
def recover_moments(raw, calibration):
    """Correct a 2x2 cross-moment matrix, rows Xi/Pi and columns Xo/Po."""
    validate_calibration(calibration)
    raw=array(raw,(2,2))
    c=calibration
    denominator=np.multiply(np.float64(c['gain_i']),np.float64(c['gain_o']))
    number(denominator,positive=True)
    left=checked_result(rotation(c['lo_i_radians']).T @ raw)
    numerator=checked_result(left @ rotation(c['lo_o_radians']))
    return np.divide(numerator,denominator)

def load_existing_decoder(source_pin):
    """Reuse the two actual AST expressions of R62, without importing its runner."""
    p=Path(source_pin['path']); raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=source_pin['sha256']:
        raise BridgeError("R62 source pin mismatch")
    tree=ast.parse(raw.decode('utf-8-sig'))
    found={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in ('c','b') and isinstance(node.value,ast.BinOp):
                segment=ast.get_source_segment(raw.decode('utf-8-sig'),node.value)
                if "Q['XX']" in segment and "Q['PX']" in segment:
                    if name in found: raise BridgeError("Ambiguous decoder expression")
                    found[name]=compile(ast.Expression(node.value),str(p),'eval')
    if set(found)!= {'c','b'}: raise BridgeError("R62 decoder missing")
    @numeric_guard
    def decode(q):
        q=array(q,(2,2))
        Q={'XX':q[0,0],'PP':q[1,1],'XP':q[0,1],'PX':q[1,0]}
        return tuple(complex(eval(found[k],{'__builtins__':{}},{'Q':Q})) for k in ('c','b'))
    return decode

@numeric_guard
def observable_correspondence(observed, target, tolerance, *, requested='selected_moments'):
    if requested != 'selected_moments':
        raise BridgeError("Four correlations cannot certify a complete state")
    tol=number(tolerance,positive=True)
    residual=stable_norm(array(observed,(2,2))-array(target,(2,2)))
    return {'status':'SYNTHETIC_SELECTED_MOMENT_CHECK','matches':residual<=tol,
            'residual':residual,'full_state_certified':False,'measurement_verified':False}

@numeric_guard
def synthetic_ratio(lambda_phys, gamma_phys, *, independent, calibration):
    """Conditional algebra only; never fills Gamma with betaTGL or claims measurement."""
    validate_calibration(calibration)
    lam=number(lambda_phys)
    if lam<0: raise BridgeError("Negative dissipative coefficient")
    if not isinstance(independent,bool): raise BridgeError("Independent flag is not boolean")
    if gamma_phys is None:
        return {'status':'OPEN_INDEPENDENT_GAMMA','beta':None,'measurement_verified':False}
    gam=number(gamma_phys)
    if gam<0: raise BridgeError("Negative Gamma")
    if gam==0 or not independent:
        return {'status':'OPEN_INDEPENDENT_GAMMA','beta':None,'measurement_verified':False}
    return {'status':'CONDITIONAL_SYNTHETIC_RATIO','beta':float(np.divide(np.float64(lam),np.float64(gam))),'measurement_verified':False}

@numeric_guard
def finite_vector_residual(x,a):
    """Full-coordinate diagnostic, not reachable from four selected correlations."""
    a=array(a,complex_ok=True); x=array(x,a.shape,complex_ok=True)
    if a.ndim!=1 or abs(np.vdot(a,a)-1)>1e-12: raise BridgeError("Reference must be a unit vector")
    p=np.outer(a,a.conj()); q=np.eye(len(a))-p
    return {'parallel':stable_norm(p@x-a), 'outside':stable_norm(q@x),
            'total':stable_norm(x-a)}

@numeric_guard
def transported_residual(x,a,C):
    """Invertible coordinate calibration uses pullback metric, not raw Euclidean gain."""
    a=array(a,complex_ok=True); x=array(x,a.shape,complex_ok=True)
    C=array(C,(len(a),len(a)),complex_ok=True)
    condition=number(np.linalg.cond(C))
    if condition>1e10: raise BridgeError("Singular/ill-conditioned calibration")
    delta=checked_result(x-a)
    d=checked_result(C@delta)
    pulled_back=checked_result(np.linalg.solve(C,d))
    return stable_norm(pulled_back)
