"""One preregistered exact-arithmetic contract test; no observed data or ODE."""
from pathlib import Path
from fractions import Fraction
import datetime,hashlib,json,sys,time
import reservoir_calibration_r70 as b
ROOT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,obj):
    with Path(p).open('xb') as f:f.write((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
def q(n,d=1,unit='s^-1'):return {'numerator':n,'denominator':d,'unit':unit}
def main():
    started=datetime.datetime.now(datetime.timezone.utc); timer=time.perf_counter()
    freeze=json.loads((ROOT/'FREEZE_CALIBRATION_R70.json').read_text(encoding='utf8'))
    for row in freeze['files']:
        if pin(row['path'])['sha256']!=row['sha256']:raise RuntimeError('Changed execution pin')
    if datetime.datetime.fromisoformat(freeze['created_utc'])>=started:raise RuntimeError('Freeze does not precede run')
    if any((ROOT/n).exists() for n in ['START_CALIBRATION_R70.json','RESULT_CALIBRATION_R70.json']):raise RuntimeError('No overwrite')
    new(ROOT/'START_CALIBRATION_R70.json',{'started_utc':started.isoformat(),'freeze':pin(ROOT/'FREEZE_CALIBRATION_R70.json')})
    tests=[]
    def check(n,p):tests.append({'name':n,'passed':bool(p)})
    def refuse(n,fn):
        try:fn()
        except b.CalibrationError:check(n,True);return
        check(n,False)
    args=dict(kind='SYNTHETIC_INPUT',normalization=b.J0,frequency=q(100),angle=q(1,10,'rad'),p_excited=q(0,1,'dimensionless'))
    z=b.collision_coefficients(**args)
    check('vacuum_coefficient_exact',z['J_rate']==q(1) and z['J_dagger_rate']==q(0))
    check('coefficient_is_not_Gamma',z['Gamma'] is None and z['beta'] is None and not z['physical_measurement'])
    hot=b.collision_coefficients(**{**args,'p_excited':q(1,4,'dimensionless')})
    check('nonvacuum_reverse_jump_required',hot['J_rate']==q(3,4) and hot['J_dagger_rate']==q(1,4) and not hot['vacuum_target_compatible'])
    ref=dict(kind='SYNTHETIC_INPUT',normalization=b.J0,frequency=q(100),reference_angle=None,bridge_hypothesis=None)
    check('missing_reference_stays_open',b.reference_coefficient(**ref)['Gamma'] is None)
    check('measured_effective_angle_not_reference',b.reference_coefficient(**{**ref,'reference_angle':q(1,10,'rad')})['Gamma'] is None)
    r=b.reference_coefficient(**{**ref,'reference_angle':q(1,5,'rad'),'bridge_hypothesis':'theta_eff_squared = beta * theta_ref_squared'})
    check('conditional_reference_not_measurement',r['Gamma']==q(4) and not r['bridge_verified'] and not r['independence_verified'] and not r['physical_measurement'])
    c=b.control_identifiability([{'label':x,'parameter_dependence':'lambda_only'} for x in ['drive_on','drive_off','bath_count','four_correlations']])
    check('on_off_same_product_not_identifiable',not c['identifies_beta'] and c['status']=='OPEN_BETA_GAMMA_DEGENERACY')
    check('new_dependence_not_automatically_proof',not b.control_identifiability([{'label':'reference','parameter_dependence':'Gamma_only_declared'}])['identifies_beta'])
    # beta here is a free symbolic rational, not betaTGL.
    beta=Fraction(2,7);Gamma=Fraction(3,2);scale=Fraction(5,3)
    check('product_invariance_exact',beta*Gamma==(scale*beta)*(Gamma/scale))
    I=Fraction(11,9)
    A=Gamma**2*I;B=beta*Gamma*I;D=beta**2*I
    check('score_information_rank_one_exact',A*D-B*B==0)
    check('independent_information_adds_rank_exact',A*(D+Fraction(4,3))-B*B==Gamma**2*I*Fraction(4,3))
    refuse('bool_quantity_rejected',lambda:b.collision_coefficients(**{**args,'frequency':q(True)}))
    refuse('zero_denominator_rejected',lambda:b.collision_coefficients(**{**args,'frequency':q(1,0)}))
    refuse('wrong_units_rejected',lambda:b.collision_coefficients(**{**args,'frequency':q(100,1,'Hz_label_without_convention')}))
    refuse('invalid_population_rejected',lambda:b.collision_coefficients(**{**args,'p_excited':q(5,4,'dimensionless')}))
    refuse('physical_receipt_rejected',lambda:b.collision_coefficients(**{**args,'kind':'MEASURED'}))
    refuse('changed_jump_rejected',lambda:b.collision_coefficients(**{**args,'normalization':'sqrt_beta_J0'}))
    refuse('NaN_float_rejected',lambda:b.collision_coefficients(**{**args,'frequency':q(float('nan'))}))
    result={'status':'PASS_EXACT_SYNTHETIC_INTERFACES' if all(t['passed'] for t in tests) else 'FAIL_EXACT_SYNTHETIC_INTERFACES','checks':tests,'started_utc':started.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-timer,'freeze':pin(ROOT/'FREEZE_CALIBRATION_R70.json'),'physical_measurement':False,'betaTGL_used_or_estimated':False,'scientific_scope':'Interfaces and exact finite algebra; general controlled-protocol proof is documentary.'}
    new(ROOT/'RESULT_CALIBRATION_R70.json',result)
    print(json.dumps({'status':result['status'],'checks':len(tests),'failed':[t['name'] for t in tests if not t['passed']],'result':pin(ROOT/'RESULT_CALIBRATION_R70.json')}))
    return 0 if result['status'].startswith('PASS') else 1
if __name__=='__main__':sys.exit(main())
