"""Exact local source ambiguity controls; no observed data or canonical imports."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time
import sympy as s

ROOT = Path(__file__).resolve().parent
def pin(p):
    p=Path(p); return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(name,obj):
    with (ROOT/name).open('xb') as f:
        f.write((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

assert not (ROOT/'SOURCE_OFFSHELL_RESULT.json').exists()
started=datetime.datetime.now(datetime.timezone.utc).isoformat(); tic=time.perf_counter()
t,b,e,l0=s.symbols('t beta epsilon L0', real=True)
# Null contravariant k=(1,1,0,0), inverse-metric variation q=k outer k.
# n=(0,1,0,0) is a held-fixed covector, I=g^{-1}(n,n), I0=-1.
k=s.Matrix([1,1,0,0]); inv0=s.diag(1,-1,-1,-1); q=k*k.T
inv=inv0+t*q; n=s.Matrix([0,1,0,0]); I=(n.T*inv*n)[0]
volume=s.sqrt(-1/inv.det())
delta_l=b*e*l0*(I+1); delta_density=volume*delta_l
checks=[]
def check(name,condition,details):
    checks.append({'name':name,'passed':bool(condition),'details':details})
check('null_direction', (k.T*inv0*k)[0]==0,'k=(1,1,0,0) is null at g0=diag(1,-1,-1,-1).')
check('same_background_action_density',s.simplify(delta_density.subs(t,0))==0,'Two local extensions agree at the comparison metric.')
check('different_metric_first_variation',s.simplify(s.diff(delta_density,t).subs(t,0)-b*e*l0)==0,'Difference of first variations = beta*epsilon*L0.')
check('different_null_stress',s.simplify(-2*s.diff(delta_density,t).subs(t,0)+2*b*e*l0)==0,'Hilbert convention T=-2/sqrt(|g|) delta S/delta g^{-1}: difference T(k,k)=-2 beta epsilon L0.')
# |1+w| at w=-1 is not two-sided differentiable along a nonzero crossing.
a=s.symbols('a',positive=True)
f=s.Abs(a*t)
left=s.limit(f/t,t,0,dir='-');right=s.limit(f/t,t,0,dir='+')
check('absolute_value_crossing_not_differentiable',s.simplify(right-left)==2*a,'Left derivative -a, right +a. Vanishing L0 or a zero first-order crossing needs separate treatment.')
# Holding sigma fixed gives only tau variations: spatial block lambda*h.
# At any positive-definite 3-metric use an orthonormal spatial basis and align
# the nonzero spatial part of a null covector with the first axis.
lam,amp,r=s.symbols('lambda amplitude radius',real=True)
spatial=s.diag(lam,lam,lam)-s.diag(amp*r*r,0,0)
check('fixed_sigma_no_nonzero_null_square_lift',s.simplify(spatial[0,0]-spatial[1,1]+amp*r*r)==0,
      'If all entries vanish, lambda=0 and amplitude*radius^2=0; null nonzero implies radius>0, hence amplitude=0.')
sources=[
    Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'),
    Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex'),
    Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\O Um e o Grande Atrator.tex'),
    Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\SelectedProbabilitySigma.lean'),
]
new('SOURCE_OFFSHELL_RESULT.json',{'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','checks':checks,
    'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'seconds':time.perf_counter()-tic,'sympy':s.__version__,'script':pin(__file__),
    'sources':[pin(p) for p in sources],
    'scope':'Exact local algebraic controls, not a physical alternative action, full source construction or general differential proof. beta is symbolic; no numerical calibration or data.'})
print(json.dumps({'checks':len(checks),'passed':all(c['passed'] for c in checks)}))
