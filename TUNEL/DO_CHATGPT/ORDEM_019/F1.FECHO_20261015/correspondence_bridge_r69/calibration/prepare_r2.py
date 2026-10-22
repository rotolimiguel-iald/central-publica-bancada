"""Create additive guarded candidate and frozen regression runner; do not execute tests."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def exclusive(name,text):
    with (ROOT/name).open('xb') as f:f.write(text.encode('utf8'))
source=(ROOT/'bridge_r69.py').read_text(encoding='utf8')
source=source.replace('import math\n','import math\nimport functools\n')
guard='''
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

'''
source=source.replace('J0 = ',guard+'J0 = ',1)
source=source.replace("return rotation(c['lo_i_radians']).T @ raw @ rotation(c['lo_o_radians'])/(c['gain_i']*c['gain_o'])", "denominator=np.multiply(np.float64(c['gain_i']),np.float64(c['gain_o']))\n    number(denominator,positive=True)\n    left=checked_result(rotation(c['lo_i_radians']).T @ raw)\n    numerator=checked_result(left @ rotation(c['lo_o_radians']))\n    return np.divide(numerator,denominator)")
source=source.replace('    def decode(q):','    @numeric_guard\n    def decode(q):')
source=source.replace("'beta':lam/gam", "'beta':float(np.divide(np.float64(lam),np.float64(gam)))")
source=source.replace('float(np.linalg.norm(array(observed,(2,2))-array(target,(2,2))))','stable_norm(array(observed,(2,2))-array(target,(2,2)))')
source=source.replace('float(np.linalg.norm(p@x-a))','stable_norm(p@x-a)').replace('float(np.linalg.norm(q@x))','stable_norm(q@x)').replace('float(np.linalg.norm(x-a))','stable_norm(x-a)')
old="""    if np.linalg.cond(C)>1e10: raise BridgeError("Singular/ill-conditioned calibration")
    inv=np.linalg.inv(C); G=inv.conj().T@inv
    d=C@(x-a)
    return float(math.sqrt(max(0,float(np.vdot(d,G@d).real))))
"""
replacement="""    condition=number(np.linalg.cond(C))
    if condition>1e10: raise BridgeError("Singular/ill-conditioned calibration")
    delta=checked_result(x-a)
    d=checked_result(C@delta)
    pulled_back=checked_result(np.linalg.solve(C,d))
    return stable_norm(pulled_back)
"""
assert old in source
source=source.replace(old,replacement)
for name in ('recover_moments','observable_correspondence','synthetic_ratio','finite_vector_residual','transported_residual'):
    source=source.replace('def '+name+'(', '@numeric_guard\ndef '+name+'(')
exclusive('bridge_r69_r2.py',source)
test=(ROOT/'test_r69.py').read_text(encoding='utf8').replace('import bridge_r69 as b','import bridge_r69_r2 as b')
for old,new in [('PRE_REGISTRO_R69.json','PRE_REGISTRO_R69_R2.json'),('FREEZE_R69.json','FREEZE_R69_R2.json'),('START_R69.json','START_R69_R2.json'),('RESULT_R69.json','RESULT_R69_R2.json')]:test=test.replace(old,new)
attacks='''        # R2 additive numerical-integrity attacks, fixed before this execution.
        extreme={**c,'gain_i':1e154,'gain_o':1e155,'lo_i_radians':0.,'lo_o_radians':0.}
        refuse('R2_overflow_product_cannot_fake_zero',lambda:b.recover_moments([[1e308,0],[0,0]],extreme))
        refuse('R2_both_gains_1e308_refused',lambda:b.recover_moments([[1.,0],[0,0]],{**extreme,'gain_i':1e308,'gain_o':1e308}))
        refuse('R2_underflow_product_refused',lambda:b.recover_moments([[1.,0],[0,0]],{**extreme,'gain_i':1e-308,'gain_o':1e-308}))
        refuse('R2_ratio_overflow_refused',lambda:b.synthetic_ratio(1e308,1e-308,independent=True,calibration=c))
        refuse('R2_ratio_underflow_refused',lambda:b.synthetic_ratio(1e-308,1e308,independent=True,calibration=c))
        refuse('R2_subnormal_divisor_refused',lambda:b.synthetic_ratio(1.,5e-324,independent=True,calibration=c))
        refuse('R2_subnormal_gains_refused',lambda:b.recover_moments([[1.,0],[0,0]],{**extreme,'gain_i':5e-324,'gain_o':5e-324}))
        huge=np.eye(2,dtype=complex)*1e200
        check('R2_large_C_no_false_zero',abs(b.transported_residual(np.array([1.,1.]),np.array([1.,0.]),huge)-1.)<tol)
        refuse('R2_transport_overflow_refused',lambda:b.transported_residual(np.array([1.,1e200]),np.array([1.,0.]),huge))
        refuse('R2_decoder_overflow_refused',lambda:decode([[1e308,0],[0,-1e308]]))
        refuse('R2_observable_difference_overflow_refused',lambda:b.observable_correspondence([[1e308,0],[0,0]],[[-1e308,0],[0,0]],tol))
        check('R2_large_norm_is_finite_nonzero',math.isfinite(b.observable_correspondence([[1e200,0],[0,0]],[[0,0],[0,0]],tol)['residual']) and not b.observable_correspondence([[1e200,0],[0,0]],[[0,0],[0,0]],tol)['matches'])
'''
needle="        status='PASS_SYNTHETIC_CONTRACTS'"
assert needle in test
test=test.replace(needle,attacks+needle)
exclusive('test_r69_r2.py',test)
wrapper=(ROOT/'execute_r69.py').read_text(encoding='utf8')
for old,new in [('test_r69.py','test_r69_r2.py'),('COMMAND_RESULT_R69.json','COMMAND_RESULT_R69_R2.json'),('STDOUT_R69.txt','STDOUT_R69_R2.txt'),('STDERR_R69.txt','STDERR_R69_R2.txt'),('START_R69.json','START_R69_R2.json'),('FREEZE_R69.json','FREEZE_R69_R2.json'),('RESULT_R69.json','RESULT_R69_R2.json')]:wrapper=wrapper.replace(old,new)
exclusive('execute_r69_r2.py',wrapper)
