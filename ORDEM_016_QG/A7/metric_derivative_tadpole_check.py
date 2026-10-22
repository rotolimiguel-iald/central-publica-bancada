"""Contract the quartic derivative vertex with coincident tensor Green jets."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
from fractions import Fraction
import hashlib,json
from metric_coincident_jet_engine_v2 import metric_fiber
from metric_principal_vertices import I,basis,gamma2,trace,inner,clear_caches
from metric_quartic_vertices import second_coefficient_4,eh_quartic_32k
H=Path(__file__).resolve().parent;D=H/'metric_derivative_tadpole';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),quartic_sha256=sha(H/'metric_quartic_vertices.py'),
    jets_sha256=sha(H/'metric_coincident_jet_engine_v2.py'),
    target='K² internal-derivative quartic tadpole; no fitting to Ward cancellation',
    normalization='Hessian Gamma1 tadpole: (1/2)*(1/(32k))*(4k)*A0= A0/16',
    full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,a,b);checks.append(n)
f=metric_fiber();bs=[basis(i,j) for i,j in f['labels']]
es=[tuple(int(i==j) for i in range(4)) for j in range(4)];zero=(0,0,0,0)
cov={key:M*f['S0'] for key,M in f['mixed'].items()}
entries=[]
for i in range(4):
    for a in range(10):
        for j in range(4):
            for b in range(10):
                if (j,b)<(i,a):continue
                w=cov[i,j][a,b]
                if w:
                    entries.append((gamma2(bs[a],es[i]),gamma2(bs[b],es[j]),
                        Fraction(w)*(1 if (i,a)==(j,b) else 2)))
def tad(A,B):
    # Two internally differentiated fields have opposite Fourier momenta.
    # External zero momenta imply only A,B can fill undifferentiated slots.
    return -sum((w*(second_coefficient_4(A,B,G,T)+second_coefficient_4(A,B,T,G))
                for G,T,w in entries),Fraction())/16
diag=tad(bs[0],bs[0]);cross=tad(bs[0],bs[4])
coeff=(diag-cross,cross)
for a,A in enumerate(bs):
    for b,B in enumerate(bs[a:],a):
        check(f'bilinear_{a}_{b}',tad(A,B),coeff[0]*inner(A,B)+coeff[1]*trace(A)*trace(B))
    clear_caches()
# Dense non-diagonal matrices add a linearity/covariance check off fitting points.
A=tuple([2,1,-1,3,1,0,2,-2,-1,2,1,0,3,-2,0,-1])
B=tuple([0,2,0,-1,2,1,3,0,0,3,-2,1,-1,0,1,4])
check('dense_bilinear',tad(A,B),coeff[0]*inner(A,B)+coeff[1]*trace(A)*trace(B))
clear_caches()
# Independent contraction using evaluation of the full four-leg vertex and
# extraction of q_i q_j coefficients rather than gamma derivative slots.
def full_momentum_contraction(A,B):
    total=Fraction()
    for a,Ea in enumerate(bs):
        for b,Eb in enumerate(bs):
            def V(q):return eh_quartic_32k((A,zero),(B,zero),(Ea,q),(Eb,tuple(-v for v in q)))
            diag=[V(e) for e in es]
            for i in range(4):
                total+=Fraction(cov[i,i][a,b])*diag[i]
                for j in range(i+1,4):
                    if cov[i,j][a,b]:
                        q=tuple(u+v for u,v in zip(es[i],es[j]))
                        total+=Fraction(cov[i,j][a,b])*(V(q)-diag[i]-diag[j])
    return total/16
for a,b in [(0,0),(0,4),(1,1)]:
    check(f'independent_momentum_contraction_{a}_{b}',full_momentum_contraction(bs[a],bs[b]),tad(bs[a],bs[b]))
    clear_caches()
assert any(c!=0 for c in coeff),'unexpected zero: inspect before declaring'
fresh(D/'results.json',dict(statute='DERIVED_QUARTIC_DERIVATIVE_TADPOLE_LOCAL_LOG',
    checks=len(checks),check_names=checks,sparse_covariance_entries=len(entries),
    internal_derivative_coefficients_over_hbar_A0_K2=list(map(str,coeff)),
    internal_invariants=['trAB','trA trB'],
    external_derivative_coefficients_over_hbar_A0_K=['-2','2','-2','4'],
    external_invariants=['p²trAB','p²trA trB','pAp trB+pBp trA','pABp'],
    internal_gradient_trace_trace=str(tad(I,I)),
    potential_quartic_log='0 previously established',
    odd_internal_derivative_log='0 in invariant reference',
    finite_state_part=False,full_curved_metric_bubble=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'metric_quartic_vertices.py',H/'metric_coincident_jet_engine_v2.py',
     D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),coefficients=list(map(str,coeff)),
    entries=len(entries),cpu_seconds=process_time()-cpu)))
