"""Prepared scalar-prior join qualification. No numerical work on import.

Gaussian fixtures replace only the projected matrix geometry, explicitly.
The original df482 scalar operators/vertex and f820 services are exercised.
"""
import math
import sys
import time

REQUEST_ID = '4f5a24b4-594d-4c6d-84f6-cd06dc4c6064'
CASE_IDS = ('B01','B02','S01','R01','F01','F02','F03','Z01','N01','N02','N03')


def need(ok, message):
    if not ok:
        raise AssertionError(message)


class AffineGaussianFixture:
    """log L(x)=offset-a(x-center)^2/2, realizable in a residual line.

Not a PreparedJoint or an execution of _Curve.__init__; no matrix claim.
The vertex is computed by the ORIGINAL _Curve.peak implementation.
"""
    def __init__(self, prior, spec, deadline):
        self.prior, self.deadline = prior, deadline
        self.a, self.center, self.offset = spec['a'], spec['center'], spec['offset']
        self.reference, self.lower, self.upper = spec['reference'], spec['lower'], spec['upper']
        self.b = self.a*(self.center-self.reference)
        self.flat_in_float_geometry = self.a == 0
        self.zero_density = spec.get('zero_density',False)
        self.base_point = {'status':'ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT' if self.zero_density
                           else 'FINITE_LOG_FLAT_INTEGRAL',
                           'log_integral_deta':float('-inf') if self.zero_density else self.offset-0.5*self.a*(self.reference-self.center)**2}
        self.log_calls, self.peak_calls = 0, 0
        self.cap = spec['maximum_log_calls']

    def peak(self, prior_linear=0.0):
        self.peak_calls += 1
        need(self.peak_calls<=1,'UNEXPECTED_VERTEX_REPEAT')
        return self.prior._Curve.peak(self,prior_linear)

    def log_likelihood(self,x):
        need(time.monotonic()<self.deadline,'CURVE_DEADLINE')
        self.log_calls += 1
        need(self.log_calls<=self.cap,'CURVE_EVALUATION_CAP')
        need(self.lower<=x<=self.upper and math.isfinite(x),'CURVE_DOMAIN')
        return self.offset-0.5*self.a*(x-self.center)**2


def erf_reference(a,center,lower,upper,offset=0.0,linear=0.0,log_density=0.0):
    """Independent completion of square and finite Gaussian primitive."""
    tilted=center+linear/a
    scale=math.sqrt(a/2)
    difference=math.erf(scale*(upper-tilted))-math.erf(scale*(lower-tilted))
    need(difference>0,'REFERENCE_ERF_DIFFERENCE')
    return math.fsum((offset,linear*center,linear*linear/(2*a),log_density,
                     0.5*math.log(math.pi/(2*a)),math.log(difference)))


def original_rd_reference(a,center,deadline):
    """Fixed256-panel Simpson in ORIGINAL rd; no candidate helper/service.

Classical quadrature remainder bounded symbolically via fourth derivative.
Floating point/library allowance remains separately declared, not certified.
"""
    low,high,n=130.0,160.0,256
    h=(high-low)/n
    values=[]
    for i in range(n+1):
        need(time.monotonic()<deadline,'REFERENCE_DEADLINE')
        r=low if i==0 else high if i==n else low+h*i
        f=math.exp(-0.5*a*(1/r-center)**2)
        weight=1 if i in (0,n) else 4 if i%2 else 2
        values.append(weight*f)
    average=(h/3)*math.fsum(values)/(high-low)
    z=max(abs(1/low-center),abs(1/high-center))
    u1=a*z/low**2
    u2=a/low**4+2*a*z/low**3
    u3=6*a/low**5+6*a*z/low**4
    u4=36*a/low**6+24*a*z/low**5
    fourth_bound=u4+4*u1*u3+3*u2*u2+6*u1*u1*u2+u1**4
    remainder=h**4*fourth_bound/180
    need(0<remainder<average,'REFERENCE_POSITIVE_BRACKET')
    return {'reference_log':math.log(average),'evaluations':n+1,
            'simpson_absolute_remainder_bound_formula_value':remainder,
            'simpson_log_remainder_allowance':-math.log1p(-remainder/average),
            'fourth_derivative_bound_formula_value':fourth_bound,
            'floating_roundoff_allowance':5e-12,
            'reference_is_interval_arithmetic':False}


def run_case(prior, case, prior_filename, deadline, precision_module):
    cid=case['id']; need(cid in CASE_IDS,'UNKNOWN_CASE')
    need(prior._analytic.__code__.co_filename==prior_filename and
         prior._rd_quadrature.__code__.co_filename==prior_filename,'PINNED_SCALAR_FUNCTIONS')
    precision_filename=precision_module.log_exp_quad_interval.__code__.co_filename
    state={'calls':0,'duplicate_nodes':0,'service_invocations':0,'real_service_invocations':0,
           'synthetic_service_invocations':0,'swallowed':None}
    rd=case['route']=='rd'
    lam=math.log(10)/5
    lower=-5*math.log1p(0.15)/math.log(10) if case['route']=='s' else 1/160 if rd else -0.05
    upper=-5*math.log1p(-0.15)/math.log(10) if case['route']=='s' else 1/130 if rd else 0.05
    center=1/145 if rd else case['center']
    reference=1/140 if rd else 0.0
    spec={'a':case['a'],'center':center,'reference':reference,'lower':lower,'upper':upper,
          'offset':case['offset'],'zero_density':cid=='Z01','maximum_log_calls':case['maximum_log_calls']}
    curve=AffineGaussianFixture(prior,spec,deadline)
    linear=-lam if case['route']=='s' else 0.0
    log_density=math.log(lam/0.30) if case['route']=='s' else -math.log(0.10)
    p={'absolute_log_error_target':1e-10,'absolute_scaled_error_target':1e-10,
       'relative_scaled_error_target':1e-10,'max_window_evaluations':4098,
       'max_quadrature_evaluations':4097,
       'services':{'log_exp_quad_interval':{'id':precision_module.LOG_SERVICE_ID},
                   'positive_quad_1d':{'id':precision_module.QUAD_SERVICE_ID}}}

    def fake_receipt(service_id,key,value,count):
        return {'service_id':service_id,'status':'ENGINEERING_ESTIMATE',key:value,
                'error_kind':'UNASSESSED','error_estimate':None,'converged':False,
                'evaluations':count,'method':'INTENTIONAL_NEGATIVE_SERVICE_FIXTURE'}

    def window(*args,**kwargs):
        state['service_invocations']+=1
        if cid=='N01':
            state['synthetic_service_invocations']+=1
            return fake_receipt('INTENTIONALLY_WRONG_SERVICE','log_value',0.0,0)
        state['real_service_invocations']+=1
        need(sys.getprofile() is None,'NO_PREEXISTING_PROFILER')
        def profile(frame,event,arg):
            if event=='call' and frame.f_code.co_filename==precision_filename and frame.f_code.co_name=='integrand':
                state['calls']+=1
                need(state['calls']<=case['maximum_evaluations'],'WINDOW_CAP')
                need(time.monotonic()<deadline,'WINDOW_DEADLINE')
        sys.setprofile(profile)
        try:
            result=precision_module.log_exp_quad_interval(*args,**kwargs)
        finally:
            sys.setprofile(None)
        need(result['evaluations']==state['calls'],'INDEPENDENT_WINDOW_COUNT')
        return result

    def quadrature(callback,*args,**kwargs):
        state['service_invocations']+=1
        seen=set()
        def counted(u):
            state['calls']+=1
            need(state['calls']<=case['maximum_evaluations'],'QUADRATURE_CAP')
            need(u not in seen,'DUPLICATE_RD_NODE')
            seen.add(u)
            need(time.monotonic()<deadline,'QUADRATURE_DEADLINE')
            return callback(u)
        if cid=='N02':
            state['synthetic_service_invocations']+=1
            try:counted(-0.125)
            except prior.PriorError as exc:state['swallowed']=exc
            return fake_receipt(precision_module.QUAD_SERVICE_ID,'value',1.0,1)
        if cid=='N03':
            state['synthetic_service_invocations']+=1
            counted(0.5)
            return fake_receipt(precision_module.QUAD_SERVICE_ID,'value',0.0,1)
        state['real_service_invocations']+=1
        result=precision_module.positive_quad_1d(counted,*args,**kwargs)
        need(result['evaluations']==state['calls'],'INDEPENDENT_RD_COUNT')
        return result

    result=None;caught=None
    try:
        services={'log_exp_quad_interval':window,'positive_quad_1d':quadrature}
        result=prior._rd_quadrature(curve,p,services) if rd else prior._analytic(curve,linear,log_density,p,services)
    except BaseException as exc:
        caught=exc
    ref=None;comparison=None
    if cid.startswith('N'):
        need(isinstance(caught,prior.PriorError) and caught.code==case['expected_exception_code'],
             'EXPECTED_TYPED_SERVICE_REFUSAL')
        need(result is None,'FAILED_SERVICE_RETURNED_SUCCESS')
        if cid=='N02':
            need(caught.__cause__ is state['swallowed'] and state['swallowed'].code=='DOMAIN_ERROR',
                 'SWALLOWED_CALLBACK_NOT_LATCHED')
        need(state['calls']==case['expected_evaluations'],'NEGATIVE_CALLBACK_COUNT')
    else:
        need(caught is None and type(result) is dict,'UNEXPECTED_CANDIDATE_FAILURE:'+repr(caught))
        if cid=='Z01':
            need(result['log_conditional_integral']==float('-inf') and
                 result['status']=='ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT','LEGITIMATE_ZERO')
        elif cid.startswith('F'):
            need(result['log_conditional_integral']==case['offset'] and
                 result['status']=='FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY','NORMALIZED_FLAT_PRIOR')
        else:
            if rd:
                ref=original_rd_reference(case['a'],center,deadline)
                expected_peak=center
            else:
                value=erf_reference(case['a'],center,lower,upper,case['offset'],linear,log_density)
                ref={'reference_log':value,'evaluations':0,'simpson_log_remainder_allowance':0.0,
                     'floating_roundoff_allowance':5e-12,'formula':'completed square and erf in original prior measure'}
                expected_peak=min(upper,max(lower,center+linear/case['a']))
            tolerance=case['comparison_absolute_log_tolerance']+ref['simpson_log_remainder_allowance']+ref['floating_roundoff_allowance']
            difference=abs(result['log_conditional_integral']-ref['reference_log'])
            need(difference<=tolerance,'PRIOR_MEASURE_OR_JACOBIAN_MISMATCH')
            need(abs(result['anchor_coordinate']-expected_peak)<=1e-13,'WRONG_RESTRICTED_VERTEX')
            need(result['precision']['converged'] is True and
                 result['precision']['error_kind']=='ESTIMATED_NOT_CERTIFIED','SERVICE_PRECISION_SCOPE')
            comparison={'absolute_log_difference':difference,'allowed_absolute_log_difference':tolerance,
                        'expected_vertex':expected_peak}
    need(state['service_invocations']==case['expected_service_invocations'],'SERVICE_INVOCATION_COUNT')
    need(state['calls']<=case['maximum_evaluations'],'TOTAL_CASE_WORK')
    need(curve.peak_calls==case['expected_peak_calls'],'VERTEX_CALLS')
    if cid.startswith('F') or cid=='Z01':
        need(state['calls']==0 and curve.log_calls==0,'CONSTANT_CASE_CALLED_A_SERVICE')
    encoded=None if result is None else dict(result)
    if encoded is not None and encoded.get('log_conditional_integral')==float('-inf'):
        encoded['log_conditional_integral']={'$float':'-inf'}
    need(time.monotonic()<deadline,'CASE_DEADLINE')
    return {'case_id':cid,'status':'PASS','scope':'SCALAR_PRIOR_MEASURE_JOIN_ON_EXPLICIT_GAUSSIAN_FIXTURE',
            'observed':{'calls':state['calls'],'duplicate_nodes':0 if rd or not state['calls'] else None},
            'service_invocations':state['service_invocations'],
            'real_service_invocations':state['real_service_invocations'],
            'synthetic_service_invocations':state['synthetic_service_invocations'],
            'candidate_invocations':1,'curve_log_calls':curve.log_calls,'vertex_calls':curve.peak_calls,
            'reference':ref,'comparison':comparison,'candidate_result':encoded,
            'expected_exception_code':case.get('expected_exception_code'),
            'swallowed_callback_cause_preserved':cid=='N02' and caught.__cause__ is state['swallowed'],
            'matrix_backend_executed':False,'full_integrate_at_fixed_theta_executed':False,
            'solver_calls':0,'observed_data':False,'uniform_certificate':False}
