"""Exact principal metric bubble, with normalization fixed before computation."""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import hashlib, json
import sympy as s
from metric_principal_vertices import basis, eh_cubic_16k, clear_caches
from one_loop_scale_engine import q, ANGULAR_FACTOR, log_coefficient

HERE=Path(__file__).resolve().parent
DEST=HERE/'metric_bubble'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    raw=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists(), str(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw;tmp.replace(p)

new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),vertices_sha256=sha(HERE/'metric_principal_vertices.py'),
    engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    ghost_manifest_sha256=sha(HERE/'ghost_bubble/manifest.json'),
    prescription='Euclidean principal logLambda radial expansion; massless two denominators',
    numerator='Tr(S0 W_A S0 W_B)/16; W=16*kappa*V3',
    effective_Hessian='hbar*(-metric/2+ghost), before Lorentz phase',
    controls='Full symmetric fiber, exact polynomial interpolation checked off nodes; 55 pairs; double gauge contraction measured, not imposed',
    omission='curvature, quartic curvature tadpoles, finite terms, cutoff, BV marked insertions; NOT full Q2'))
start,cpu=perf_counter(),process_time()
bs=[basis(i,j) for i in range(4) for j in range(i,4)]
labels=[(i,j) for i in range(4) for j in range(i,4)]
S=s.zeros(10)
for a,(i,j) in enumerate(labels):
    for b,(k,l) in enumerate(labels):
        if i==j and k==l:S[a,b]=s.Integer(i==k)-s.Rational(1,2)
        elif a==b:S[a,b]=s.Rational(1,2)
zero=(0,0,0,0)
axes=[tuple(int(i==j) for j in range(4)) for i in range(4)]
p=(1,0,0,0)
mons=[s.S.One]+list(q)+[x*x for x in q]+[q[i]*q[j] for i in range(4) for j in range(i+1,4)]
checks=[]
def check(name, actual, expected=0):
    assert s.expand(actual-expected)==0,(name,actual,expected)
    checks.append(name)

def W(H,k):
    r=tuple(-p[i]-k[i] for i in range(4))
    return s.Matrix(10,10,lambda i,j:eh_cubic_16k(H,p,bs[i],k,bs[j],r))

def coefficients(H):
    c=W(H,zero);plus=[W(H,e) for e in axes]
    minus=[W(H,tuple(-x for x in e)) for e in axes]
    cs=[c]+[(plus[i]-minus[i])/2 for i in range(4)]
    cs += [(plus[i]+minus[i])/2-c for i in range(4)]
    cs += [W(H,tuple(axes[i][k]+axes[j][k] for k in range(4)))-plus[i]-plus[j]+c
           for i in range(4) for j in range(i+1,4)]
    k=(2,-1,1,3)
    interp=s.zeros(10)
    for m,C in zip(mons,cs):interp+=m.subs(dict(zip(q,k)))*C
    assert interp==W(H,k), 'off-node cubic polynomial check'
    checks.append('vertex_polynomial_off_nodes_'+str(len(checks)))
    clear_caches()
    return [S*C for C in cs]

cache=[coefficients(H) for H in bs]
def bubble(a,b):
    numerator=0
    for m,A in zip(mons,cache[a]):
        for n,B in zip(mons,cache[b]):
            val=sum(A[i,j]*B[j,i] for i in range(10) for j in range(10))
            numerator+=val*m*n/16
    return s.cancel(log_coefficient(s.expand(numerator),[zero,p],[0,0])/ANGULAR_FACTOR)

def invariants(a,b):
    A=s.Matrix(4,4,bs[a]);B=s.Matrix(4,4,bs[b]);P=s.Matrix(p)
    pa=(P.T*A*P)[0];pb=(P.T*B*P)[0];p2=(P.T*P)[0]
    return [s.trace(A*B)*p2**2,s.trace(A)*s.trace(B)*p2**2,
        (pa*s.trace(B)+pb*s.trace(A))*p2,(P.T*A*B*P)[0]*p2,pa*pb]

lookup={label:i for i,label in enumerate(labels)}
fit_labels=[((1,2),(1,2)),((1,1),(2,2)),((0,0),(1,1)),((0,1),(0,1)),((0,0),(0,0))]
fit=[(lookup[a],lookup[b]) for a,b in fit_labels]
values={pair:bubble(*pair) for pair in fit}
M=s.Matrix([invariants(*pair) for pair in fit])
assert M.det()!=0
coef=M.inv()*s.Matrix([values[pair] for pair in fit])
for a in range(10):
    for b in range(a,10):
        pair=(a,b)
        val=values.setdefault(pair,bubble(a,b)) if pair not in values else values[pair]
        check(f'tensor_basis_{a}_{b}',val,sum(x*y for x,y in zip(coef,invariants(a,b))))

ghost=s.Matrix([s.Rational(1,12),s.Rational(7,48),-s.Rational(1,8),-s.Rational(1,12),s.Rational(1,6)])
combined=-coef/2+ghost
longitudinal={}
for nu in range(4):
    for rho in range(nu,4):
        a=lookup[(0,nu)];b=lookup[(0,rho)]
        # K(e_nu) has twice E00 when nu=0; otherwise E0nu.
        factor=(2 if nu==0 else 1)*(2 if rho==0 else 1)
        longitudinal[f'{nu}_{rho}']=str(s.expand(factor*sum(x*y for x,y in zip(combined,invariants(a,b)))))
neg=[]
assert values[fit[-1]]!=0;neg.append('metric_longitudinal_piece_discarded')
wrong=coef/2+ghost
assert sum(x*y for x,y in zip(wrong,invariants(*fit[-1])))!=0
neg.append('wrong_relative_determinant_sign')
result=dict(statute='REAL_EXACT_PRINCIPAL_METRIC_BUBBLE',
    at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    metric_coefficients_over_A0=list(map(str,coef)),
    ghost_coefficients_over_A0=list(map(str,ghost)),
    combined_Hessian_coefficients_over_hbar_A0=list(map(str,combined)),
    metric_e00_e00=str(values[fit[-1]]),
    double_gauge_contractions_over_hbar_A0=longitudinal,
    double_gauge_zero=all(s.sympify(v)==0 for v in longitudinal.values()),
    checks_passed=len(checks),checks=checks,negative_controls=neg,
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    full_ward_coefficient_computed=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False),flush=True)
