"""Exact algebra only; no trajectories, sample data, dynamics or physical calibration."""
from pathlib import Path
import datetime, hashlib, json, time
import sympy as s
BASE=Path(__file__).resolve().parent
def pin(p):
    b=Path(p).read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write_new(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,ensure_ascii=False)
def main():
    plan=json.loads((BASE/'PLAN_R63.json').read_text(encoding='utf8'))
    if plan['runner']['sha256']!=pin(__file__)['sha256']:raise ValueError('Runner changed')
    started=datetime.datetime.now(datetime.timezone.utc)
    if datetime.datetime.fromisoformat(plan['created_utc'])>=started:raise ValueError('Plan must precede calculation')
    for row in plan['source_pins']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('Changed source')
    if (BASE/'RESULT_R63.json').exists() or (BASE/'START_R63.json').exists():raise FileExistsError('Execution already started')
    write_new(BASE/'START_R63.json',{'started_utc':started.isoformat(),'plan':pin(BASE/'PLAN_R63.json')})
    timer=time.perf_counter();checks=[]
    def check(name,A,B):
        diff=A-B
        values=list(diff) if isinstance(diff,s.MatrixBase) else [diff]
        residual=[s.simplify(v) for v in values]
        checks.append({'name':name,'passed':all(v==0 for v in residual),'nonzero_residuals':[str(v) for v in residual if v!=0]})
    x=s.symbols('x',real=True);p,q=s.symbols('p q',nonzero=True)
    e=s.eye(2);n=s.diag(0,1);a=s.Matrix([[0,1],[0,0]])
    # p=exp(i theta): inverse represents complex conjugate on the unit circle.
    E=s.Matrix([[1,s.sqrt(2)*x/p],[s.sqrt(2)*x*p,2*x*x]])
    gaussian={0:s.Integer(1),1:s.Integer(0),2:s.Rational(1,2),3:s.Integer(0),4:s.Rational(3,4)}
    def moment(k):
        return E.applyfunc(lambda f:sum(c*gaussian[j[0]] for j,c in s.Poly(s.expand(x**k*f),x).terms()))
    Q=lambda z:(a/z+a.T*z)/s.sqrt(2)
    M0=moment(0);M1=moment(1);M2=moment(2)
    check('POVM_integral_identity',M0,e)
    check('POVM_first_moment',M1,Q(p))
    check('POVM_second_moment',M2,e/2+n)
    check('compressed_operator_square',Q(p)**2,e/2)
    check('second_moment_defect',M2-Q(p)**2,n)
    w=s.Matrix([1,s.sqrt(2)*x*p]);wstar=s.Matrix([[1,s.sqrt(2)*x/p]])
    check('effect_positive_rank_one_factorization',E,w*wstar)
    # Three occupation levels suffice for the exact X^2 matrix elements on n=0,1.
    a3=s.Matrix([[0,1,0],[0,0,s.sqrt(2)],[0,0,0]])
    Q3=(a3/p+a3.T*p)/s.sqrt(2)
    check('bosonic_n012_first_compression',Q3[:2,:2],Q(p))
    check('bosonic_n012_second_compression',(Q3**2)[:2,:2],M2)
    k=s.kronecker_product
    U=k(Q(p),e);V=k(e,Q(q));cross=k(Q(p),Q(q))
    Ni=k(n,e);No=k(e,n)
    check('two_mode_cross_moment',k(M1,M1.subs(p,q)),U*V)
    plus=k(M2,e)+k(e,M2)+2*cross
    minus=k(M2,e)+k(e,M2)-2*cross
    check('plus_square_defect',plus-(U+V)**2,Ni+No)
    check('minus_square_defect',minus-(U-V)**2,Ni+No)
    check('physical_quadratic_difference', (plus-minus)/4,cross)
    check('compressed_quadratic_difference',((U+V)**2-(U-V)**2)/4,cross)
    XX=k(Q(1),Q(1));PP=k(Q(s.I),Q(s.I))
    XP=k(Q(1),Q(s.I));PX=k(Q(s.I),Q(1))
    check('C_decoder_from_physical_cross_moments',(XX-PP+s.I*(XP+PX))/2,k(a,a))
    check('B_decoder_from_physical_cross_moments',(XX+PP+s.I*(XP-PX))/2,k(a.T,a))
    v1=s.Matrix([0,1])
    check('one_photon_physical_second_moment',(v1.T*M2*v1)[0],s.Rational(3,2))
    check('one_photon_cutoff_square',(v1.T*Q(p)**2*v1)[0],s.Rational(1,2))
    check('one_photon_nonhomomorphism_witness',(v1.T*(M2-Q(p)**2)*v1)[0],s.Integer(1))
    result={'status':'PASS_EXACT_COMPRESSED_HOMODYNE' if all(c['passed'] for c in checks) else 'FAIL_EXACT_ALGEBRA',
      'started_utc':started.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'seconds':time.perf_counter()-timer,'sympy_version':s.__version__,'checks':checks,
      'moments':{'M0':str(M0),'M1':str(M1),'M2':str(M2),'defect':str(n)},
      'domains':'p,q on unit circle; exact Gaussian moments; finite input support n_i,n_o in {0,1}; OH identity.',
      'limits':['No new Liouvillian or time evolution.','No detector samples, calibration or observed data.',
                'Compression is a POVM, not Pauli spectral measurement.','No dynamic intertwiner or physical packet identification derived.'],
      'plan':pin(BASE/'PLAN_R63.json'),'runner':pin(__file__)}
    write_new(BASE/'RESULT_R63.json',result)
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c for c in checks if not c['passed']],
                      'result':pin(BASE/'RESULT_R63.json'),'seconds':result['seconds']}))
    return 0 if all(c['passed'] for c in checks) else 1
if __name__=='__main__':raise SystemExit(main())
