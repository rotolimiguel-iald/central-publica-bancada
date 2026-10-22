"""Combine metric bubble, tadpole and ghost in one symmetric radial symbol.

First K only, local logarithmic Hessian. No finite causal Ward conclusion.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
from fractions import Fraction as F
from itertools import combinations_with_replacement
import hashlib,json
import sympy as s
from ghost_covariant_word_engine import hessian_terms,matrix_unit
from radial_covariant_jet_engine import radial_jets
H=Path(__file__).resolve().parent;D=H/'first_curvature_total_hessian';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),
    inputs=[dict(path=str(H/r),sha256=sha(H/r)) for r in ['ghost_covariant_word_engine.py','position_metric_adjoint/results.json','metric_curvature_vertices/results.json','metric_derivative_tadpole/results.json']],
    target='Put ghost covariant Hessian and adjoint-corrected metric bubble in the same radial symmetric symbol; add already computed tadpole',
    no_full_Q2=True))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
labels=list(combinations_with_replacement(range(4),2));basis=[matrix_unit(*t) for t in labels]
operator=hessian_terms()
def inv(A,B,p):
    a=s.Matrix(A);b=s.Matrix(B);q=s.Matrix(p);p2=(q.T*q)[0]
    pa=(q.T*a*q)[0];pb=(q.T*b*q)[0]
    return list(map(F,[p2*s.trace(a*b),p2*s.trace(a)*s.trace(b),pa*s.trace(b),pb*s.trace(a),(q.T*a*b*q)[0]]))
def evaluate(A,B,p,order):
    value,_,_=radial_jets(A,p)
    return sum((c*B[a][b]*value(w,u,v,order-k)
        for (k,a,b,u,v,w),c in operator.items() if k<=order and B[a][b]),F())
p=(1,0,0,0);matrix=[];values=[]
for a,A in enumerate(basis):
    for b,B in enumerate(basis):
        iv=inv(A,B,p);actual=evaluate(A,B,p,1)
        matrix.append(iv);values.append(actual)
M=s.Matrix(matrix);fit,params=M.gauss_jordan_solve(s.Matrix(values));check('unique_ghost_symbol',len(params),0)
for i,(iv,actual) in enumerate(zip(matrix,values)):check('ghost_pair_'+str(i),actual,sum(F(c)*v for c,v in zip(fit,iv)))
check('ghost_mixed_symmetry',fit[2],fit[3])
for a,b in [(0,4),(5,5),(4,0)]:
    p=(1,2,-1,1)
    check(f'ghost_nonaxis_{a}_{b}',evaluate(basis[a],basis[b],p,1),sum(F(c)*v for c,v in zip(fit,inv(basis[a],basis[b],p))))
principal=list(map(F,json.loads((H/'position_metric_adjoint/results.json').read_bytes())['combined']))
potential=list(map(F,json.loads((H/'metric_curvature_vertices/results.json').read_bytes())['K_bubble_cross_coefficients']))
potential=[potential[0],potential[1],potential[2],potential[2],potential[3]]
tadpole=[F(-2),F(2),F(-2),F(-2),F(4)]
metric_bubble=[a+b for a,b in zip(principal,potential)]
metric=[-v/2+t for v,t in zip(metric_bubble,tadpole)]
total=[a+F(b) for a,b in zip(metric,fit)]
check('total_mixed_symmetry',total[2],total[3])
fresh(D/'results.json',dict(statute='DERIVED_FIRST_K_LOG_HESSIAN_RADIAL_SYMBOL',checks=len(checks),check_names=checks,
    ghost=list(map(str,fit)),metric_raw_bubble=list(map(str,metric_bubble)),metric_with_tadpole=list(map(str,metric)),
    total=list(map(str,total)),basis=['p²trAB','p²trA trB','pAp trB','pBp trA','pABp'],
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False,K2_complete=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),ghost=list(map(str,fit)),metric=list(map(str,metric)),total=list(map(str,total)),cpu=process_time()-cpu)))
