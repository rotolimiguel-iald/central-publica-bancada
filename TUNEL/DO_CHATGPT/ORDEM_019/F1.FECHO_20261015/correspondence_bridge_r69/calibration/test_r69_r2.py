"""Frozen finite synthetic tests. No acquisition, ODE or physical measurement."""
from pathlib import Path
import datetime, hashlib, json, math, sys, time, traceback
import numpy as np
import bridge_r69_r2 as b

ROOT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p); return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,obj):
    with Path(p).open('xb') as f: f.write((json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())

def main():
    started=datetime.datetime.now(datetime.timezone.utc); timer=time.perf_counter()
    plan=json.loads((ROOT/'PRE_REGISTRO_R69_R2.json').read_text(encoding='utf8'))
    freeze=json.loads((ROOT/'FREEZE_R69_R2.json').read_text(encoding='utf8'))
    for row in freeze['files']+plan['source_pins']:
        if pin(row['path'])['sha256']!=row['sha256']: raise RuntimeError('Changed pin: '+row['path'])
    if datetime.datetime.fromisoformat(freeze['created_utc'])>=started: raise RuntimeError('Freeze not before run')
    if (ROOT/'RESULT_R69_R2.json').exists() or (ROOT/'START_R69_R2.json').exists(): raise RuntimeError('No overwrite/rerun')
    new(ROOT/'START_R69_R2.json',{'started_utc':started.isoformat(),'freeze':pin(ROOT/'FREEZE_R69_R2.json')})
    checks=[]; metrics={}
    def check(name,passed,value=None):
        checks.append({'name':name,'passed':bool(passed),'value':value})
    def refuse(name,fn):
        try: fn()
        except b.BridgeError: check(name,True); return
        check(name,False)
    try:
        tol=plan['tolerance']; c=plan['calibration']; decode=b.load_existing_decoder(plan['decoder_source'])
        check('schema_is_not_measurement',b.validate_calibration(c)['measurement_verified'] is False)
        q=np.array([[.2,.11],[-.07,-.1]])
        raw=c['gain_i']*c['gain_o']*(b.rotation(c['lo_i_radians'])@q@b.rotation(c['lo_o_radians']).T)
        recovered=b.recover_moments(raw,c)
        check('gain_and_LO_inverse',np.linalg.norm(recovered-q)<tol,float(np.linalg.norm(recovered-q)))
        C,B=decode(recovered)
        check('R62_decoder_C',abs(C-(.15+.02j))<tol)
        check('R62_decoder_B',abs(B-(.05+.09j))<tol)
        c2={**c,'gain_i':7.,'gain_o':.2,'lo_i_radians':-.7,'lo_o_radians':1.3}
        raw2=c2['gain_i']*c2['gain_o']*(b.rotation(c2['lo_i_radians'])@q@b.rotation(c2['lo_o_radians']).T)
        check('known_gain_change_preserves_decoded',np.linalg.norm(b.recover_moments(raw2,c2)-q)<tol)
        check('uncorrected_gain_rejected_by_residual',not b.observable_correspondence(raw,q,tol)['matches'])
        # Same filtered quadrature under time-unit changes: exponential matched filter.
        kap=2.; T=3.; timegrid=np.linspace(0,T,1001); p=1-math.exp(-kap*T)
        physical=np.sqrt(kap)*np.exp(-kap*timegrid/2)/math.sqrt(p)
        for t0 in (.2,4.):
            tau=timegrid/t0; kd=t0*kap
            dimless=np.sqrt(kd)*np.exp(-kd*tau/2)/math.sqrt(p)
            check('filter_transport_'+str(t0),np.max(abs(dimless-math.sqrt(t0)*physical))<tol)
            check('rate_ratio_time_invariant_'+str(t0),abs((t0*.3)/(t0*2.5)-.3/2.5)<tol)
        # Non-injective four-cross-moment observation on two finite modes.
        lower=np.array([[0,1],[0,0]],complex); eye=np.eye(2)
        ai=np.kron(lower,eye); ao=np.kron(eye,lower)
        Xi=(ai+ai.conj().T)/math.sqrt(2); Pi=(ai-ai.conj().T)/(1j*math.sqrt(2))
        Xo=(ao+ao.conj().T)/math.sqrt(2); Po=(ao-ao.conj().T)/(1j*math.sqrt(2))
        r0=np.diag([1.,0,0,0]); r1=np.diag([0.,0,1,0])
        def moments(r): return np.array([[np.trace(r@A@D).real for D in (Xo,Po)] for A in (Xi,Pi)])
        q0=moments(r0); q1=moments(r1)
        check('different_density_same_four_correlations',np.linalg.norm(q0-q1)<tol and np.linalg.norm(r0-r1)>1)
        check('selected_match_never_promotes_full_state',not b.observable_correspondence(q0,q1,tol)['full_state_certified'])
        refuse('full_state_request_refused',lambda:b.observable_correspondence(q0,q1,tol,requested='full_state'))
        metrics['noninjective_counterexample']={'basis':['00','01','10','11'],'rho0_diagonal':r0.diagonal().tolist(),'rho1_diagonal':r1.diagonal().tolist(),'four_moments':q0.tolist(),'density_distance_frobenius':float(np.linalg.norm(r0-r1))}
        a=np.array([1.,0.],complex); x=np.array([1.,.3j]); rr=b.finite_vector_residual(x,a)
        check('projection_match_has_unread_residual',rr['parallel']<tol and rr['outside']>.29)
        check('wrong_coefficient_not_repaired',b.finite_vector_residual(2*a,a)['parallel']>.99)
        xn=x/np.linalg.norm(x)
        check('normalized_nonzero_residual_breaks_exact_projection',b.finite_vector_residual(xn,a)['parallel']>1e-3)
        for label,coord in [('unitary',np.array([[0,1j],[1,0]])),('gain',np.diag([2.,.5]))]:
            check('transported_residual_'+label,abs(b.transported_residual(x,a,coord)-rr['total'])<tol)
        check('raw_euclidean_gain_not_invariant',abs(np.linalg.norm(np.diag([2.,.5])@(x-a))-rr['total'])>.1)
        refuse('singular_calibration_refused',lambda:b.transported_residual(x,a,np.diag([1.,0.])))
        for gam in (None,0.):
            z=b.synthetic_ratio(.3,gam,independent=True,calibration=c)
            check('missing_positive_Gamma_'+str(gam),z['beta'] is None and z['status'].startswith('OPEN'))
        check('dependent_Gamma_no_beta',b.synthetic_ratio(.3,2.5,independent=False,calibration=c)['beta'] is None)
        z=b.synthetic_ratio(.3,2.5,independent=True,calibration=c)
        check('conditional_ratio_is_not_measurement',abs(z['beta']-.12)<tol and not z['measurement_verified'])
        check('product_degeneracy_preserved',abs((.12*3)*(2.5/3)-.12*2.5)<tol)
        for key,val in [('gain_i',True),('gain_o',float('nan')),('lo_i_radians',float('inf')),('t0_seconds',False),('rate_unit','Hz'),('J0','rescaled_unspecified'),('filter_l2_norm',.5),('kind','REAL')]:
            refuse('schema_refuses_'+key,lambda key=key,val=val:b.validate_calibration({**c,key:val}))
        refuse('missing_key_refused',lambda:b.validate_calibration({k:v for k,v in c.items() if k!='J0'}))
        refuse('NaN_moment_refused',lambda:b.recover_moments([[float('nan'),0],[0,0]],c))
        refuse('boolean_moment_refused',lambda:b.recover_moments([[True,0],[0,0]],c))
        refuse('boolean_Gamma_refused',lambda:b.synthetic_ratio(.3,True,independent=True,calibration=c))
        refuse('NaN_lambda_refused',lambda:b.synthetic_ratio(float('nan'),2.5,independent=True,calibration=c))
        # R2 additive numerical-integrity attacks, fixed before this execution.
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
        status='PASS_SYNTHETIC_CONTRACTS' if all(z['passed'] for z in checks) else 'FAIL_SYNTHETIC_CONTRACTS'
        result={'status':status,'checks':checks,'metrics':metrics,'physical_measurement':False,'beta_TGL_estimated':False,'full_state_tomography':False}
    except Exception:
        result={'status':'EXECUTION_FAILURE','checks':checks,'error':traceback.format_exc()}
    result.update({'started_utc':started.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-timer,'python':sys.version,'numpy':np.__version__,'preregistration':pin(ROOT/'PRE_REGISTRO_R69_R2.json'),'freeze':pin(ROOT/'FREEZE_R69_R2.json')})
    new(ROOT/'RESULT_R69_R2.json',result)
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c['name'] for c in checks if not c['passed']],'result':pin(ROOT/'RESULT_R69_R2.json')}))
    return 0 if result['status']=='PASS_SYNTHETIC_CONTRACTS' else 1

if __name__=='__main__': sys.exit(main())
