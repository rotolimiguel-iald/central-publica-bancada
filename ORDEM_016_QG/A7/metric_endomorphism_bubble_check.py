"""Explicit E insertions in the metric bubble, not a scalar replacement.

This is only one decomposition of the curved problem: all tensor projectors,
trace reversal, vertices and Wick pairings are retained; geometric transport
corrections remain separate. Repeated denominators and exact sector masses
provide independent checks of this particular subset.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
from functools import lru_cache
import hashlib,json
import sympy as s
from metric_principal_vertices import basis,eh_cubic_16k,clear_caches
from metric_curvature_vertices import eh_cubic_potential_16k_over_K
from metric_coincident_jet_engine_v2 import metric_fiber
from one_loop_scale_engine import q,ANGULAR_FACTOR,log_coefficient
H=Path(__file__).resolve().parent;D=H/'metric_endomorphism_bubble';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),principal_sha256=sha(H/'metric_principal_vertices.py'),
    potential_sha256=sha(H/'metric_curvature_vertices.py'),
    radial_sha256=sha(H/'one_loop_scale_engine.py'),
    convention='D=q²-E; inverse expanded +E/q4+E²/q6; E/K=-2P_TL+6P_tr',
    target=['Principal vertices with one E insertion','Principal vertices with two E insertions',
            'One potential vertex and one E insertion'],
    comparison='Exact two-sector denominator masses -e*K, independent radial recurrence',
    omissions=['Parallel transport','Metric and measure terms','Connection derivative corrections',
               'Finite causal part','Full Q2'],
    no_scalar_substitution=True,gate_changed=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,e):assert s.expand(e)==0,(n,e);checks.append(n)
f=metric_fiber();S=f['S0'];E=f['E'];bs=[basis(i,j) for i,j in f['labels']]
zero=(0,0,0,0);p=(1,0,0,0)
axes=[tuple(int(i==j) for j in range(4)) for i in range(4)]
mons=[s.S.One]+list(q)+[a*a for a in q]+[q[i]*q[j] for i in range(4) for j in range(i+1,4)]
def W(A,k):
    r=tuple(-p[i]-k[i] for i in range(4))
    return s.Matrix(10,10,lambda a,b:eh_cubic_16k(A,p,bs[a],k,bs[b],r))
def coefficients(A):
    c=W(A,zero);pl=[W(A,e) for e in axes];mi=[W(A,tuple(-v for v in e)) for e in axes]
    cs=[c]+[(pl[i]-mi[i])/2 for i in range(4)]+[(pl[i]+mi[i])/2-c for i in range(4)]
    cs += [W(A,tuple(axes[i][k]+axes[j][k] for k in range(4)))-pl[i]-pl[j]+c
           for i in range(4) for j in range(i+1,4)]
    node=(2,-1,1,3)
    check('cubic_offnode_'+str(len(checks)),
          sum((m.subs(dict(zip(q,node)))*c for m,c in zip(mons,cs)),s.zeros(10))-W(A,node))
    clear_caches();return cs
# Matrix form of the exact-zero condition above, deliberately explicit.
oldcheck=check
def check(n,e):
    if isinstance(e,s.MatrixBase):
        assert all(s.expand(v)==0 for v in e),(n,e);checks.append(n)
    else:oldcheck(n,e)
cs=[coefficients(A) for A in bs]
pot=[s.Matrix(10,10,lambda a,b:eh_cubic_potential_16k_over_K(A,bs[a],bs[b])) for A in bs]
props=[S,E*S,E*E*S]
@lru_cache(None)
def weights(left,right):
    shifts=[zero]*left+[p]*right
    return {(i,j):s.cancel(log_coefficient(a*b,shifts,[0]*(left+right))/ANGULAR_FACTOR)
            for i,a in enumerate(mons) for j,b in enumerate(mons)}
def frob(A,B):return sum(a*b for a,b in zip(A,B))
@lru_cache(None)
def left_cache(a,u,v):return [props[u]*C*props[v] for C in cs[a]]
def pp(a,b,u,v):
    w=weights(1+u,1+v);left=left_cache(a,u,v)
    return sum(val*frob(left[i],cs[b][j]) for (i,j),val in w.items() if val)/16
def pv(a,b,u,v):
    w=weights(1+u,1+v)
    return sum(w[i,0]*frob(props[u]*C*props[v],pot[b])
               +w[0,i]*frob(props[u]*pot[a]*props[v],cs[b][i])
               for i,C in enumerate(cs[a]) if w[i,0] or w[0,i])/16
def pieces(a,b):
    return [pp(a,b,1,0)+pp(a,b,0,1),
            pp(a,b,2,0)+pp(a,b,1,1)+pp(a,b,0,2),
            pv(a,b,1,0)+pv(a,b,0,1)]
def invariants(a,b):
    A=s.Matrix(4,4,bs[a]);B=s.Matrix(4,4,bs[b]);P=s.Matrix(p)
    return [s.trace(A*B),s.trace(A)*s.trace(B),
        (P.T*A*P)[0]*s.trace(B)+(P.T*B*P)[0]*s.trace(A),(P.T*A*B*P)[0]]
lookup={v:i for i,v in enumerate(f['labels'])}
fit=[(lookup[a],lookup[b]) for a,b in [((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1))]]
cache={pair:pieces(*pair) for pair in fit}
M=s.Matrix([invariants(*pair) for pair in fit])
c1=M.inv()*s.Matrix([cache[pair][0] for pair in fit])
c2=s.Matrix([invariants(*pair)[:2] for pair in fit[:2]]).inv()*s.Matrix([cache[pair][1] for pair in fit[:2]])
c3=s.Matrix([invariants(*pair)[:2] for pair in fit[:2]]).inv()*s.Matrix([cache[pair][2] for pair in fit[:2]])
for a in range(10):
    for b in range(a,10):
        pair=a,b
        if pair not in cache:cache[pair]=pieces(a,b)
        for n,coeff in enumerate([c1,c2,c3]):
            check(f'basis_{a}_{b}_piece_{n}',cache[pair][n]-sum(x*y for x,y in zip(coeff,invariants(a,b))))
# Independent denominator check in exact fiber sectors, including potential.
K=s.symbols('K');sector=[(-2,f['tl']*S),(6,f['ptr']*S)]
cross_prior=list(map(s.Rational,json.loads((H/'metric_curvature_vertices/results.json').read_bytes())['K_bubble_cross_coefficients']))
pot_prior=list(map(s.Rational,json.loads((H/'metric_curvature_vertices/results.json').read_bytes())['K2_potential_bubble_coefficients']))
for a,b in [fit[0],fit[2]]:
    WA=sum((m*C for m,C in zip(mons,cs[a])),s.zeros(10))+K*pot[a]
    WB=sum((m*C for m,C in zip(mons,cs[b])),s.zeros(10))+K*pot[b]
    exact=0
    for e,PS in sector:
        for ee,QS in sector:
            numerator=s.expand(s.trace(PS*WA*QS*WB.T)/16)
            exact+=log_coefficient(numerator,[zero,p],[-e*K,-ee*K])/ANGULAR_FACTOR
    exact=s.Poly(s.expand(exact),K)
    check(f'exact_mass_K_{a}_{b}',exact.nth(1)-cache[a,b][0]-sum(x*y for x,y in zip(cross_prior,invariants(a,b))))
    check(f'exact_mass_K2_{a}_{b}',exact.nth(2)-cache[a,b][1]-cache[a,b][2]
          -sum(x*y for x,y in zip(pot_prior,invariants(a,b)[:2])))
neg=dict(omit_E_first_order=str(cache[fit[0]][0]),omit_E_second_order=str(cache[fit[0]][1]),
         omit_mixed_potential_E=str(cache[fit[0]][2]))
assert all(s.Rational(v)!=0 for v in neg.values()),neg
fresh(D/'results.json',dict(statute='DERIVED_TENSOR_ENDOMORPHISM_INSERTIONS_ONLY',
    checks=len(checks),check_names=checks,negative_controls=neg,
    K_principal_one_E_coefficients=list(map(str,c1)),
    K2_principal_two_E_coefficients=list(map(str,c2)),
    K2_mixed_potential_one_E_coefficients=list(map(str,c3)),
    K_invariants=['p²trAB','p²trA trB','pAp trB+pBp trA','pABp'],K2_invariants=['trAB','trA trB'],
    normalization='Raw metric bubble /A0, effective Hessian weight -1/2 not yet applied',
    remaining='Connection, derivative and parallel-transport terms; finite and BV sum',
    full_curved_metric_bubble=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),K1=list(map(str,c1)),K2=list(map(str,c2)),
    K2mix=list(map(str,c3)),cpu_seconds=process_time()-cpu)))
