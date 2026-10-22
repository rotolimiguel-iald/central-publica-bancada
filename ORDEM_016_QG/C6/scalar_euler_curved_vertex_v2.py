"""First-curvature scalar Euler graph, with actual mixed X/Y internal derivatives."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';D=ROOT/'C6/scalar_vertex_v2'
sys.path[:0]=[str(ROOT/'C6'),str(H)]
import sympy as s
import tensor_euler_zerojet as T
import balanced_log_pair_engine as E
from balanced_tensor_transport_engine import balanced_euler_line
from smooth_line_compatibility_check_v2 import multiply
from deliver_nonminimal_wick_and_mimo_audit import sha,put

import labelled_bilocal_jet_engine as L

def profile(order, word):
    return L.scalar(order,tuple((0 if side=='X' else 1,i) for side,i in word))

@lru_cache(None)
def contact(mu,nu,r,order):
    A0=profile(0,(('Y',mu),));B0=profile(0,(('X',r),('Y',nu)))
    flat=sum(L.pair(A0,((0,k),(0,k)),B0,()) for k in range(4))
    if order==0:return s.expand(flat)
    A1=profile(1,(('Y',mu),));B1=profile(1,(('X',r),('Y',nu)))
    val=sum(L.pair(A1,((0,k),(0,k)),B0,())+L.pair(A0,((0,k),(0,k)),B1,()) for k in range(4))
    for i,j in product(range(4),repeat=2):val+=multiply((T.xx*T.delta(i,j)-T.x[i]*T.x[j])/3,L.pair(A0,((0,i),(0,j)),B0,()))
    for i in range(4):val+=multiply(-2*T.x[i],L.pair(A0,((0,i),),B0,()))
    val+=multiply(-T.xx/2,flat)
    return s.expand(val)

def main():
    D.mkdir(exist_ok=False);t0=time.process_time();checks=0
    sources=[Path(__file__),ROOT/'C6/tensor_euler_zerojet.py',H/'balanced_scalar_euler_check_v2.py',H/'bilocal_scalar_euler_zerojet.py',H/'balanced_tensor_transport_engine.py']
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='Actual scalar graph (E_phi c.dphi)_X times metric-scalar cubic vertex atY, three flavors, to first curvature',
        first_line='nabla_Ymu Hscalar; X densitized scalar Euler',second_line='nabla_Xr nabla_Ynu Hscalar',
        prescription='Same partial R_bal plus smooth-line completion; scalar potential zero',
        cutoff='No integration by parts or external-jet covariant completion inferred',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
    kernels={}
    for mu,nu,r in product(range(4),repeat=3):
        v0=contact(mu,nu,r,0);v1=contact(mu,nu,r,1)
        assert s.expand(v0-balanced_euler_line((mu,),tuple(sorted((nu,r)))))==0
        assert not v1.free_symbols.difference(E.Q)
        assert all(sum(p)==3 for p,c in s.Poly(v1,*E.Q).terms() if c)
        checks+=3;kernels[str((mu,nu,r))]=[str(v0),str(v1)]
    labels=[(i,j) for i in range(4) for j in range(i,4)]
    matrices=[]
    for order in (0,1):
        rows=[]
        for a,b in labels:
            B=s.zeros(4);B[a,b]=B[b,a]=1;vertex=s.eye(4)*s.trace(B)/2-B
            rows.append([s.expand(3*sum(vertex[i,j]*contact(i,j,r,order) for i,j in product(range(4),repeat=2))) for r in range(4)])
        matrices.append(s.Matrix(rows))
    aa,bb,cc=s.symbols('aa bb cc');q2=sum(q*q for q in E.Q)
    def target(a,b,r):return aa*int(a==b)*E.Q[r]*q2+bb*(int(a==r)*E.Q[b]+int(b==r)*E.Q[a])*q2+cc*E.Q[a]*E.Q[b]*E.Q[r]
    expected=s.Matrix([[target(a,b,r)*(1 if a==b else 2) for r in range(4)] for a,b in labels])
    equations=[]
    for val in matrices[1]-expected:equations.extend(s.Poly(s.expand(val),*E.Q).coeffs())
    sol=s.solve(equations,(aa,bb,cc));assert set(sol)=={aa,bb,cc}
    for val in matrices[1]-expected.subs(sol):assert s.expand(val)==0;checks+=1
    # Recover the old principal coefficients independently from the newly bilocal calculation.
    old=json.loads((H/'balanced_scalar_euler_v2/results.json').read_bytes())['coefficients']
    old_expected=(expected*q2).subs({aa:s.Rational(old['aa']),bb:s.Rational(old['bb']),cc:s.Rational(old['cc'])})
    for val in matrices[0]-old_expected:assert s.expand(val)==0;checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-t0,
        first_curvature_coordinate_contact_coefficients={str(k):str(v) for k,v in sol.items()},
        invariant_polynomial_basis='aa delta_ab Qr Q²+bb(delta_ar Qb+delta_br Qa)Q²+cc QaQbQr',
        scope='Metric h at Y, contravariant c at X, coefficient of coordinate delta derivatives, K CE stripped',
        full_covariant_operator=False,external_metric_and_ghost_jets_not_transposed=True,
        full_Q2=False,gate_changed=False)
    put(D/'KERNELS.json',kernels);put(D/'MATRICES.json',[[[str(v) for v in row] for row in mat.tolist()] for mat in matrices]);put(D/'results.json',result)
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'KERNELS.json',D/'MATRICES.json',D/'results.json']]))
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
