"""Check geometric construction and actual scalar Euler graph at second curvature."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'scalar_second_curvature'
sys.path[:0]=[str(C),str(H)]
import scalar_second_curvature_engine as E
import balanced_log_pair_engine as R
import labelled_bilocal_jet_engine as L
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    # Cosine law fixes distance2, independently of the pair-extension implementation.
    K,A,B,C0=s.symbols('K A B C');d0=A+B-2*C0;d1=-(A*B-C0**2)/3;d2=-(A+B-4*C0)*(A*B-C0**2)/45
    cos=lambda v:1-v/2+v**2/24-v**3/720
    sinc=lambda v:1-v/6+v**2/120
    residual=s.series(cos(K*(d0+K*d1+K**2*d2))-cos(K*A)*cos(K*B)-K*C0*sinc(K*A)*sinc(K*B),K,0,4).removeO()
    for n in range(4):eq(residual.expand().coeff(K,n),0)
    # Independent radial ODE: no K² log term; smooth Euler defect agrees with existing heat coefficient.
    r=s.symbols('r',positive=True)
    H=1/r**2+K*(s.Rational(1,4)-s.log(r**2)/2)+K**2*s.Rational(19,480)*r**2
    radial=s.diff(H,r,2)+(3/r-K*r-K**2*r**3/15)*s.diff(H,r)
    for n,expected in [(0,0),(1,0),(2,s.Rational(29,20))]:eq(s.expand(radial).coeff(K,n),expected)
    eq(s.diff(s.expand(radial).coeff(K,2),r),0)
    # Density/inverse metric produce the independently stated scalar drift.
    x=E.x;xx=E.xx;I=s.eye(4);X=s.Matrix(x)
    a1=(xx*I-X*X.T)/3;a2=xx*(xx*I-X*X.T)/15
    dens1=-xx/2;dens2=s.Rational(13,120)*xx**2
    for j in range(4):
        drift1=sum(s.diff(a1[i,j]+dens1*I[i,j],x[i]) for i in range(4))
        drift2=sum(s.diff(a2[i,j]+dens1*a1[i,j]+dens2*I[i,j],x[i]) for i in range(4))-dens1*drift1
        eq(drift1,-2*x[j]);eq(drift2,-s.Rational(4,15)*xx*x[j])
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        scope='Same partial labelled R_bal scalar Euler graph; singular local Hadamard jet without added state term, to K²',
        scalar_radial_H2='19 r²/480',smooth_Euler_defect='29K²/20; derivative of this constant vanishes at this order',
        distance2=str(E.distance2),unknown_coefficients=True,full_Q2=False))
    old=json.loads((C/'scalar_vertex_v2/KERNELS.json').read_bytes());kernels={}
    for mu,nu,r0 in product(range(4),repeat=3):
        for o in (0,1):eq(E.contact(mu,nu,r0,o),s.sympify(old[str((mu,nu,r0))][o]))
        val=E.contact(mu,nu,r0,2)
        assert not val.free_symbols.difference(R.Q)
        assert all(sum(p)==1 for p,c in s.Poly(val,*R.Q).terms() if c)
        checks+=2;kernels[str((mu,nu,r0))]=str(val)
        if nu==3 and r0==3:print(json.dumps(dict(mu=mu,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    labels=[(a,b) for a in range(4) for b in range(a,4)]
    M=s.zeros(10,4)
    for n,(a,b) in enumerate(labels):
        Bm=s.zeros(4);Bm[a,b]=Bm[b,a]=1;vertex=s.eye(4)*s.trace(Bm)/2-Bm
        for r0 in range(4):M[n,r0]=s.expand(3*sum(vertex[i,j]*E.contact(i,j,r0,2) for i,j in product(range(4),repeat=2)))
    aa,bb=s.symbols('aa bb')
    target=s.Matrix([[(1 if a==b else 2)*(aa*int(a==b)*R.Q[r0]+bb*(int(a==r0)*R.Q[b]+int(b==r0)*R.Q[a])) for r0 in range(4)] for a,b in labels])
    equations=[]
    for val in M-target:equations.extend(s.Poly(s.expand(val),*R.Q).coeffs())
    sol=s.solve(equations,(aa,bb));assert set(sol)=={aa,bb}
    for val in M-target.subs(sol):eq(val,0)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        coefficients={str(k):str(v) for k,v in sol.items()},basis='aa delta_ab Qr+bb(delta_ar Qb+delta_br Qa)',
        coordinate_contact=True,parallel_readout_pending=True,full_Q2=False,gate_changed=False)
    put(D/'KERNELS.json',kernels);put(D/'MATRIX.json',[[str(v) for v in row] for row in M.tolist()]);put(D/'results.json',result)
    paths=[Path(__file__),C/'scalar_second_curvature_engine.py',C/'labelled_bilocal_jet_engine.py',C/'scalar_vertex_v2/KERNELS.json',D/'PRE_REGISTER.json',D/'KERNELS.json',D/'MATRIX.json',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
