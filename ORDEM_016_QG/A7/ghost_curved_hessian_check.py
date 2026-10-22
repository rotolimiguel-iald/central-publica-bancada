"""Fit and verify the complete integrated quadratic ghost residue on a spaceform.

Coefficients were explored before this run; this is a recorded verification,
not a blind preregistration. It never substitutes for the analytic heat assumptions.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
from itertools import product
from functools import lru_cache
import hashlib,json
import sympy as s
from ghost_covariant_word_engine import *
from spaceform_covariant_jet_engine import first_curvature_recursive,second_curvature_constant,connection
HOM=Path(__file__).resolve().parent;DEST=HOM/'ghost_curved_hessian';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(DEST/'VERIFICATION_PLAN.json',dict(at=datetime.now(timezone.utc).isoformat(),
 script_sha256=sha(Path(__file__)),word_engine_sha256=sha(HOM/'ghost_covariant_word_engine.py'),
 jet_engine_sha256=sha(HOM/'spaceform_covariant_jet_engine.py'),
 parent_sha256=sha(HOM/'ghost_minimal_heat/DERIVACAO.md'),
 earlier_exploration_disclosed=True,
 target='Full ghost integrated quadratic heat coefficient, K^0,K^1,K^2, fixed background',
 acceptance=['Gamma through K² from exact normal spaceform metric',
 'Two independent first-K covariant word evaluators',
 'Recover flat coefficients; fit four K and two K² invariant coefficients',
 '55 bilinear basis pairs at each order plus dense nonaxial control',
 'Recover independent conformal result; detect omitted connections'],
 analytic_heat_assumptions_inherited=True,finite_causal_part=False,full_Q2=False))
start,cpu=perf_counter(),process_time();checks=[];negative=[]
def check(n,e):
 assert s.expand(e)==0,(n,e);checks.append(n)
def reject(n,e):
 assert s.expand(e)!=0,(n,e);negative.append(dict(name=n,value=str(e)))

# Independent derivation of the cubic connection from the metric/inverse.
xx=s.symbols('x0:4');z=sum(t*t for t in xx);Id=s.eye(4);X=s.Matrix(xx)
g1=-(z*Id-X*X.T)/3;g2=2*(z*z*Id-z*X*X.T)/45;inv1=-g1
def pp(poly):return sum(s.Rational(c.numerator,c.denominator)*s.prod(xx[i]**e[i] for i in range(4)) for e,c in poly.items())
for a,b,c in product(range(4),repeat=3):
 direct1=(s.diff(g1[a,c],xx[b])+s.diff(g1[a,b],xx[c])-s.diff(g1[b,c],xx[a]))/2
 direct2=(s.diff(g2[a,c],xx[b])+s.diff(g2[a,b],xx[c])-s.diff(g2[b,c],xx[a]))/2
 direct2+=sum(inv1[a,d]*(s.diff(g1[d,c],xx[b])+s.diff(g1[d,b],xx[c])-s.diff(g1[b,c],xx[d]))/2 for d in range(4))
 check(f'Gamma1_from_metric_{a}_{b}_{c}',direct1-pp(connection(1,a,b,c)))
 check(f'Gamma2_from_metric_{a}_{b}_{c}',direct2-pp(connection(2,a,b,c)))

Hdense=[[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]];pd=(1,2,-1,3)
independent=first_curvature_recursive(Hdense,pd)
labels=[(i,j) for i in range(4) for j in range(i,4)]
for w in product(range(4),repeat=4):
 for a,b in labels:check('firstK_word_'+str(w)+str((a,b)),jet(w,a,b,Hdense,pd,1)-independent(w,a,b))
op=hessian_terms();ref=hessian_terms(True);corr=curvature_gradient_terms()
p0=(1,0,0,0)
def invK(T,H,p):
 T,H,p=s.Matrix(T),s.Matrix(H),s.Matrix(p);p2=p.dot(p)
 return [p2*s.trace(T*H),p2*s.trace(T)*s.trace(H),
 (p.T*T*p)[0]*s.trace(H)+(p.T*H*p)[0]*s.trace(T),(p.T*T*H*p)[0]]
fit=[((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1))]
mat=[];vals=[]
for l,r in fit:
 T,H=matrix_unit(*l),matrix_unit(*r);mat.append(invK(T,H,p0))
 vals.append(evaluate(op,T,H,p0,1)-evaluate(ref,T,H,p0,1))
c1=s.Matrix(mat).inv()*s.Matrix(vals)

@lru_cache(None)
def jj_for(Hkey):return second_curvature_constant([list(t) for t in Hkey])
def ev2(oo,T,H):
 jj=jj_for(tuple(tuple(t) for t in H))
 return sum((c*T[a][b]*jj(w,u,v,2-ko) for (ko,a,b,u,v,w),c in oo.items() if T[a][b]),Q(0))
v2=[];m2=[]
for l,r in fit[:2]:
 T,H=matrix_unit(*l),matrix_unit(*r)
 v2.append(ev2(op,T,H)-ev2(ref,T,H)-ev2(corr,T,H))
 m2.append([s.trace(s.Matrix(T)*s.Matrix(H)),s.trace(s.Matrix(T))*s.trace(s.Matrix(H))])
c2=s.Matrix(m2).inv()*s.Matrix(v2)
old=json.loads((HOM/'ghost_bubble/results.json').read_bytes());c0=list(map(s.Rational,old['coefficients_over_angular_factor']))
def flat_expected(T,H,p):
 T,H,p=s.Matrix(T),s.Matrix(H),s.Matrix(p);p2=p.dot(p);tp=(p.T*T*p)[0];hp=(p.T*H*p)[0]
 inv=[s.trace(T*H)*p2*p2,s.trace(T)*s.trace(H)*p2*p2,
 (tp*s.trace(H)+hp*s.trace(T))*p2,(p.T*T*H*p)[0]*p2,tp*hp]
 return sum(a*b for a,b in zip(c0,inv))
for i,l in enumerate(labels):
 for r in labels[i:]:
  T,H=matrix_unit(*l),matrix_unit(*r)
  check('flat_'+str((l,r)),evaluate(op,T,H,p0,0)-flat_expected(T,H,p0))
  check('firstK_'+str((l,r)),evaluate(op,T,H,p0,1)-evaluate(ref,T,H,p0,1)-sum(a*b for a,b in zip(c1,invK(T,H,p0))))
  check('firstK_gradient_form_'+str((l,r)),evaluate(corr,T,H,p0,1)-sum(a*b for a,b in zip(c1,invK(T,H,p0))))
  tm,hm=s.Matrix(T),s.Matrix(H)
  check('secondK_'+str((l,r)),ev2(op,T,H)-ev2(ref,T,H)-ev2(corr,T,H)-c2[0]*s.trace(tm*hm)-c2[1]*s.trace(tm)*s.trace(hm))
Tdense=[[2,-1,1,0],[-1,0,2,1],[1,2,3,-2],[0,1,-2,1]]
check('dense_nonaxial_flat',evaluate(op,Tdense,Hdense,pd,0)-flat_expected(Tdense,Hdense,pd))
check('dense_nonaxial_firstK',evaluate(op,Tdense,Hdense,pd,1)-evaluate(ref,Tdense,Hdense,pd,1)-evaluate(corr,Tdense,Hdense,pd,1))
check('dense_secondK',ev2(op,Tdense,Hdense)-ev2(ref,Tdense,Hdense)-ev2(corr,Tdense,Hdense)-
 c2[0]*s.trace(s.Matrix(Tdense)*s.Matrix(Hdense))-c2[1]*s.trace(s.Matrix(Tdense))*s.trace(s.Matrix(Hdense)))
grad=[c1[0]/2,c1[1]/2,c1[2],c1[3]/2];potential=[c2[0]/2,c2[1]/2]
check('conformal_firstK_with_reference_Bochner',4*grad[0]+16*grad[1]+4*grad[2]+grad[3]+s.Rational(1,8)+s.Rational(19,2))
check('parallel_conformal_constant_potential_zero',4*potential[0]+16*potential[1])
T=matrix_unit(1,2);H=matrix_unit(1,2)
massonly=sum(c*T[a][b]*jet(w,u,v,H,p0,0) for (ko,a,b,u,v,w),c in op.items() if ko==1 and T[a][b])
reject('ignore_derivative_commutators_at_firstK',evaluate(op,T,H,p0,1)-massonly)
reject('omit_secondK_potential',c2[0]*2)
result=dict(statute='DERIVED_CONDITIONAL_COMPLETE_INTEGRATED_QUADRATIC_GHOST_LOG_WITH_EXACT_CAS',
 checks=len(checks),check_names=checks,negative_controls=negative,
 firstK_bilinear_coefficients=list(map(str,c1)),firstK_gradient_density_coefficients=list(map(str,grad)),
 secondK_bilinear_coefficients=list(map(str,c2)),secondK_potential_density_coefficients=list(map(str,potential)),
 density_reference='(box h)^2/24+7(box t)^2/96-(div u)(box t)/8-(nabla u)^2/24+(div u)^2/12',
 density_firstK='K[7(nabla h)^2/12-17(nabla t)^2/12+7u.nabla t/2-79u²/24]',
 density_secondK='13K²(4h²-t²)/6',t='tr h',u='div h',
 operator_terms=len(op),reference_terms=len(ref),gradient_correction_terms=len(corr),
 coefficient_matching_scope='O(4)-covariant local fourth-order operator on spaceform; flat/firstK/secondK exhaustive homogeneous orders',
 analytic_conditions=['Fixed-background ghost operator and Laplace-type heat residue of parent report',
 'Trace cyclicity at logarithmic symbol residue, not finite determinant equality',
 'Compact support or quotient by divergences; no variable-cutoff contact conclusion'],
 finite_causal_part_computed=False,full_metric_sector=False,full_Q2=False,gate_changed=False,
 wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
files=[Path(__file__),HOM/'ghost_covariant_word_engine.py',HOM/'spaceform_covariant_jet_engine.py',
 DEST/'VERIFICATION_PLAN.json',DEST/'results.json']
new(DEST/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
