"""Algebraic curvature contribution of the measured antifield primitive.

Checks both Euclidean and Lorentz fiber metrics. This is not a curved loop
calculation and does not commute covariant derivatives silently.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'curved_primitive_mass';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    inputs_sha256=sha(HERE/'model_inputs/DERIVACAO_OPERADORES.md'),
    principal_sha256=sha(HERE/'bv_gradient_fit/DERIVACAO_COMPLETA_PRINCIPAL.md'),
    target='Curvature mass M(H)=2K H+K g trH inside B[c.nabla E+divc E/2]-D1(E)/3',
    hypotheses='constant K,metric-compatible Levi-Civita; fixed derivative ordering in E',
    excluded='No assertion that these are all curved loop terms or all commutator terms'))
start,cpu=perf_counter(),process_time();K=s.Symbol('K',real=True)
ps=s.Matrix(s.symbols('p0:4'));rs=s.Matrix(s.symbols('r0:4'));basis=[]
for i in range(4):
    for j in range(i,4):
        H=s.zeros(4);H[i,j]=H[j,i]=1;basis.append(H)
def sym(a,b):return (a*b.T+b*a.T)/2
def zero(A):return all(s.expand(x)==0 for x in A)
checks=0;nonzero=0;neg=set()
for label,g in [('Euclidean',s.eye(4)),('Lorentz',s.diag(1,-1,-1,-1))]:
    inv=g.inv()
    for hi,H in enumerate(basis):
        tr=s.trace(inv*H);M=2*K*H+K*g*tr
        B=-M/6-g*s.trace(inv*M)/12
        assert zero(B+K*(H/3+2*g*tr/3));checks+=1
        for vi in range(4):
            v=s.eye(4)[:,vi];vf=g*v;rsharp=inv*rs
            D=(sym(rs,M*v)-sym(vf,M*rsharp))/2
            targetD=K*(sym(rs,H*v)-sym(vf,H*rsharp))
            assert zero(D-targetD);checks+=1
            scalar=(ps+rs/2).dot(v);actual=scalar*B-D/3
            expected=-K*(scalar*(H/3+2*g*tr/3)+(sym(rs,H*v)-sym(vf,H*rsharp))/3)
            assert zero(actual-expected);checks+=1
            nonzero+=int(not zero(actual))
            if not zero(D):
                assert not zero(actual-(scalar*B));neg.add(label+'_omit_gradient')
            wrongM=2*K*H;wrongB=-wrongM/6-g*s.trace(inv*wrongM)/12
            wrongD=(sym(rs,wrongM*v)-sym(vf,wrongM*rsharp))/2
            if tr:
                assert not zero(actual-(scalar*wrongB-wrongD/3));neg.add(label+'_omit_trace_mass')
            # The curvature term is a lower derivative term of degree1 in momenta.
            for x in actual:
                for exps,c in s.Poly(s.expand(x),*(list(ps)+list(rs))).terms():
                    if c:assert sum(exps)==1
            checks+=1
result=dict(statute='DERIVED_CURVATURE_MASS_PART_OF_FREE_BV_PRIMITIVE',
    checks_passed=checks,nonzero_polarizations=nonzero,negative_controls=sorted(neg),
    physical_operator='E=4kappa H=-box Itr+Itr K_gauge C+2K id+K g trace',
    formula='-K{[(p+r/2).v](H/3+2g trH/3)+[sym(r,Hv)-sym(vflat,H rsharp)]/3}',
    common_factor='4 i kappa A0 for marked vertex, Fourier+i',
    derivative_order='No commuting of box,nabla or C; lower commutator terms remain separately',
    curved_loop_coefficient=False,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',result);print(json.dumps(result,ensure_ascii=False))
