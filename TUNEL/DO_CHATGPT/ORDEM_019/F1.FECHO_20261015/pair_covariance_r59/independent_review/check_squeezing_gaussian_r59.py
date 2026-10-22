"""Independent covariance derivation from the Schrödinger Gaussian pullback."""
from pathlib import Path
import datetime
import hashlib
import json
import sympy as s

u=s.symbols('u', positive=True)  # u=exp(rho)
theta=s.symbols('theta',real=True)  # phi=2 theta
c=(u+1/u)/2
d=(u-1/u)/2
M=s.Matrix([[c,d],[d,c]])
A=s.simplify(M.inv().T*M.inv())
# |psi|² has precision A. Coordinate covariance is A^-1/2;
# momentum covariance follows by differentiating the real Gaussian: A/2.
Q=s.simplify(A.inv()/2)
P=s.simplify(A/2)
V0=s.Matrix([[Q[0,0],0,Q[0,1],0], [0,P[0,0],0,P[0,1]],
             [Q[1,0],0,Q[1,1],0], [0,P[1,0],0,P[1,1]]])
R=s.diag(s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]]),
         s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]]))
V=(R*V0*R.T).applyfunc(s.trigsimp)
h=(u**2+u**-2)/2
g=(u**2-u**-2)/2
target=s.Matrix([[h,0,g*s.cos(2*theta),g*s.sin(2*theta)],
                 [0,h,g*s.sin(2*theta),-g*s.cos(2*theta)],
                 [g*s.cos(2*theta),g*s.sin(2*theta),h,0],
                 [g*s.sin(2*theta),-g*s.cos(2*theta),0,h]])/2
checks=[]
def check(name,expr):
    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    residuals=[s.simplify(s.trigsimp(s.expand_trig(x))) for x in values]
    assert all(x==0 for x in residuals),(name,residuals)
    checks.append({'name':name,'scalar_equalities':len(values),'pass':True})

omega=s.diag(s.Matrix([[0,1],[-1,0]]),s.Matrix([[0,1],[-1,0]]))
check('pullback_determinant_one',M.det()-1)
check('gaussian_phase_rotated_covariance',V-target)
check('Gaussian_number',(V[0,0]+V[1,1]-1)/2-d**2)
pair=(V[0,2]-V[1,3]+s.I*(V[0,3]+V[1,2]))/2
check('Gaussian_anomalous_pair',pair-c*d*(s.cos(2*theta)+s.I*s.sin(2*theta)))
check('pure_gaussian_covariance',target*omega*target-omega/4)
e=s.Matrix([1,0,-1,0])
check('difference_variance_from_Gaussian',(e.T*target*e)[0]-h+g*s.cos(2*theta))
check('aligned_variance',((e.T*target*e)[0]).subs(theta,0)-u**-2)
check('vacuum_phase_degeneracy',target.subs(u,1)-s.eye(4)/2)
# The pair phase Jacobian is m_amplitude*m_amplitude', rho derivative=u*d/du.
amp=c*d
check('phase_jacobian',amp*u*s.diff(amp,u)-(u**4-u**-4)/8)

result={'status':'PASS_INDEPENDENT_GAUSSIAN_IDENTITIES','reviewer':'codex-mission-memory-review',
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'method':'Gaussian pullback precision A=M^-T M^-1, position/momentum covariance, then common phase rotation. No author code imported or executed.',
        'checks':checks,'count':len(checks),'scalar_equalities':sum(x['scalar_equalities'] for x in checks),
        'script':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'limits':'Finite-mode covariance identities; functional domain reasoning is separate and written in the review. No GKLS, device or spatial realization inferred.'}
p=Path(__file__).with_name('SQUEEZING_GAUSSIAN_CHECKS_R59.json')
with p.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':len(checks),'scalar_equalities':result['scalar_equalities']}))
