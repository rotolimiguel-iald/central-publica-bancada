"""Verify curvature potential and compute two explicit metric bubble pieces."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
from itertools import permutations
import hashlib,json
import sympy as s
import metric_curvature_vertices as cv
from metric_principal_vertices import basis,eh_cubic_16k,clear_caches
from one_loop_scale_engine import q,ANGULAR_FACTOR,log_coefficient
HOM=Path(__file__).resolve().parent;DEST=HOM/'metric_curvature_vertices';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),script_sha256=sha(Path(__file__)),
 engine_sha256=sha(HOM/'metric_curvature_vertices.py'),principal_sha256=sha(HOM/'metric_principal_vertices.py'),
 action='-(2kappa)^-1 integral sqrt(g+h)[R(g+h)-6K], gauge fixing C_g(h) linear',
 relative_connection='R(g+h) integrated = (g+h)^-1 Ric(g) + covariant Gamma-Gamma modulo divergence',
 potential='-3K/(2kappa)*sqrt(det(I+h))*(tr((I+h)^-1)-2)',
 contractions='Same S0 and transposed Wick contraction as metric_bubble_v2',
 compute=['Cubic/quartic zero-derivative curvature vertices','One potential and one principal cubic in bubble with leading propagators',
 'Two potential cubic vertices with leading propagators','Potential-quartic tadpole local log trace contraction only'],
 excluded=['Derivative-vertex bitensor corrections','All derivative quartic tadpoles','Cutoff divergences and finite causal contacts','Full Q2']))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(n,e):assert s.expand(e)==0,(n,e);checks.append(n)
def reject(n,e):assert s.expand(e)!=0,(n,e);neg.append(dict(name=n,value=str(e)))

# Independent eigenvalue expansion: invariant polynomials of a real symmetric h.
lam=s.symbols('l0:4');eps=s.symbols('eps')
det=s.prod(1+eps*x for x in lam)
sqrt=s.series(s.sqrt(det),eps,0,5).removeO()
invtr=sum(sum((-eps*x)**j for j in range(5)) for x in lam)
series=s.Poly(s.expand(sqrt*(invtr-2)),eps)
M=tuple(lam[a] if a==b else s.Integer(0) for a in range(4) for b in range(4))
check('potential_stationary',series.nth(1))
for n in (2,3,4):check(f'determinant_inverse_series_{n}',series.nth(n)-cv.potential_polynomial(M,n))
t,a2,a3,a4=s.symbols('t a2 a3 a4')
P3=-t**3/12+t*a2/2-2*a3/3
P4=-t**4/64+3*t*t*a2/16-3*a2*a2/16-t*a3/2+3*a4/4
check('cubic_identity_direction',4*s.diff(P3,t)+2*t*s.diff(P3,a2)+3*a2*s.diff(P3,a3))
check('quartic_identity_direction',4*s.diff(P4,t)+2*t*s.diff(P4,a2)+3*a2*s.diff(P4,a3)+4*a3*s.diff(P4,a4)+s.Rational(3,2)*P3)
check('pure_conformal_cubic',P3.subs({t:4,a2:4,a3:4}))
check('pure_conformal_quartic',P4.subs({t:4,a2:4,a3:4,a4:4}))
bs=[basis(i,j) for i in range(4) for j in range(i,4)];labels=[(i,j) for i in range(4) for j in range(i,4)]
for i,A in enumerate(bs):
 for j in range(i,10):
  B=bs[j]
  check(f'cubic_trace_leg_{i}_{j}',cv.polarized([cv.I,A,B]))
  check(f'quartic_trace_pair_tadpole_{i}_{j}',cv.polarized([cv.I,cv.I,A,B]))
for i,j,k in [(0,1,1),(4,4,0),(7,5,5),(9,1,6),(1,5,8)]:
 A,B,C=bs[i],bs[j],bs[k]
 check(f'cubic_polarization_{i}_{j}_{k}',cv.eh_cubic_potential_16k_over_K(A,B,C)+24*cv.polarized([A,B,C]))
 for perm in permutations((A,B,C)):check(f'cubic_Bose_{i}_{j}_{k}_{len(checks)}',cv.eh_cubic_potential_16k_over_K(*perm)-cv.eh_cubic_potential_16k_over_K(A,B,C))

S=s.zeros(10)
for a,(i,j) in enumerate(labels):
 for b,(k,l) in enumerate(labels):
  if i==j and k==l:S[a,b]=s.Integer(i==k)-s.Rational(1,2)
  elif a==b:S[a,b]=s.Rational(1,2)
p=(1,0,0,0);zero=(0,0,0,0);axes=[tuple(int(i==j) for j in range(4)) for i in range(4)]
mons=[s.S.One]+list(q)+[x*x for x in q]+[q[i]*q[j] for i in range(4) for j in range(i+1,4)]
weights=[s.cancel(log_coefficient(m,[zero,p],[0,0])/ANGULAR_FACTOR) for m in mons]
def W(H,k):
 r=tuple(-p[i]-k[i] for i in range(4))
 return s.Matrix(10,10,lambda a,b:eh_cubic_16k(H,p,bs[a],k,bs[b],r))
def coefficients(H):
 c=W(H,zero);pl=[W(H,e) for e in axes];mi=[W(H,tuple(-x for x in e)) for e in axes]
 cc=[c]+[(pl[i]-mi[i])/2 for i in range(4)]+[(pl[i]+mi[i])/2-c for i in range(4)]
 cc += [W(H,tuple(axes[i][k]+axes[j][k] for k in range(4)))-pl[i]-pl[j]+c for i in range(4) for j in range(i+1,4)]
 k=(2,-1,1,3);interp=sum((m.subs(dict(zip(q,k)))*c for m,c in zip(mons,cc)),s.zeros(10))
 assert interp==W(H,k);checks.append('principal_interpolation_offnodes_'+str(len(checks)));clear_caches()
 return sum((w*c for w,c in zip(weights,cc)),s.zeros(10))
# Varying curvature vertex only: the leading propagators are intentionally fixed.
principal=[coefficients(H) for H in bs]
potential=[s.Matrix(10,10,lambda i,j:cv.eh_cubic_potential_16k_over_K(H,bs[i],bs[j])) for H in bs]
def cross(a,b):return s.trace(S*principal[a]*S*potential[b].T+S*potential[a]*S*principal[b].T)/16
def twice(a,b):return s.trace(S*potential[a]*S*potential[b].T)/16
def inv(a,b):
 A,B,P=s.Matrix(4,4,bs[a]),s.Matrix(4,4,bs[b]),s.Matrix(p)
 return [s.trace(A*B),s.trace(A)*s.trace(B),(P.T*A*P)[0]*s.trace(B)+(P.T*B*P)[0]*s.trace(A),(P.T*A*B*P)[0]]
lookup={l:i for i,l in enumerate(labels)}
fit=[(lookup[a],lookup[b]) for a,b in [((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1))]]
c1=s.Matrix([inv(a,b) for a,b in fit]).inv()*s.Matrix([cross(a,b) for a,b in fit])
c2=s.Matrix([inv(a,b)[:2] for a,b in fit[:2]]).inv()*s.Matrix([twice(a,b) for a,b in fit[:2]])
for a in range(10):
 for b in range(a,10):
  check(f'cross_tensor_{a}_{b}',cross(a,b)-sum(x*y for x,y in zip(c1,inv(a,b))))
  check(f'potential_squared_tensor_{a}_{b}',twice(a,b)-sum(x*y for x,y in zip(c2,inv(a,b)[:2])))
reject('potential_squared_cannot_be_discarded',twice(lookup[(1,2)],lookup[(1,2)]))
reject('potential_cross_cannot_be_discarded',cross(lookup[(1,2)],lookup[(1,2)]))
result=dict(statute='DERIVED_CURVATURE_POTENTIAL_VERTICES_AND_PARTIAL_METRIC_LOG_WITH_EXACT_CAS',
 checks=len(checks),check_names=checks,negative_controls=neg,
 P2='trh²/2-(trh)^2/4',P3='-(trh)^3/12+(trh)trh²/2-2trh³/3',
 P4='-(trh)^4/64+3(trh)^2trh²/16-3(trh²)^2/16-(trh)trh³/2+3trh⁴/4',
 cubic_traceless='P3=-2tr(h0³)/3;16kappa V3pot/K=96tr(A0 B0 C0)',
 K_bubble_cross_coefficients=list(map(str,c1)),K2_potential_bubble_coefficients=list(map(str,c2)),
 invariant_cross_order=['p²trAB','p²trA trB','pAp trB+pBp trA','pABp'],
 invariant_potential_order=['trAB','trA trB'],
 potential_quartic_tadpole_log='Zero for universal coincident logarithmic metric coefficient (K/2)g_ab g_cd:V4pot(g,g,A,B)=0',
 normalization='Unweighted numerator bubble /A0 as metric_bubble_v2; Hessian weight -1/2 NOT applied',
 missing=['Curvature in transport/derivatives/propagators for all other pieces','Derivative quartic tadpoles','Cutoff/finite contacts','Full BV sum'],
 full_metric_curved=False,full_Q2=False,gate_changed=False,
 wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
files=[Path(__file__),HOM/'metric_curvature_vertices.py',DEST/'PRE_REGISTER.json',DEST/'results.json']
new(DEST/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
