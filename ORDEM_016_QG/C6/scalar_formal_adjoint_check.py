"""Formal-adjoint check in the basis of completely symmetrized covariant words.

Commuting Q variables encode multisets of SYMMETRIZED words; this does not
assert commutation of unsymmetrized covariant derivatives.
"""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'scalar_formal_adjoint'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    Q=s.symbols('q0:4');q=s.Matrix(Q);q2=q.dot(q);I=s.eye(4)
    labels=[(i,j) for i in range(4) for j in range(i,4)];basis=[]
    for i,j in labels:
        B=s.zeros(4);B[i,j]=B[j,i]=1;basis.append(B)
    weight=s.diag(*[1 if a==b else 2 for a,b in labels])
    def matrix(co,degree):
        cols=[]
        for B in basis:
            tr=s.trace(B);div=B*q;dd=(q.T*B*q)[0]
            if degree==0:V=co[0]*B+co[1]*I*tr
            else:
                a,b,c,d,e=co
                V=a*q2*B+b*I*q2*tr+c*q*q.T*tr+d*I*dd+e*(q*div.T+div*q.T)/2
                if degree==4:
                    # At order4 co is c1..c5; the third coefficient occurs in both transposed slots.
                    V=a*q2**2*B+b*I*q2**2*tr+c*q2*(q*q.T*tr+I*dd)+d*q2*(q*div.T+div*q.T)/2+e*q*q.T*dd
            cols.append(s.Matrix([s.expand(V[i,j]) for i,j in labels]))
        return s.Matrix.hstack(*cols)
    a,b,c,d,e=s.symbols('a b c d e')
    forms=[matrix([a,b,c,d,e],4),matrix([a,b,c,c,e],2),matrix([a,b],0)]
    for M in forms:
        for val in weight*M-M.T*weight:
            assert s.expand(val)==0;checks+=1
    # Dropping the transposed Hessian term is rejected; the test is not automatic symmetrization.
    bad=matrix([a,b,c,d,e],2);defect=(weight*bad-bad.T*weight).applyfunc(s.expand)
    witness=next((i,j,v) for i in range(10) for j in range(10) if (v:=defect[i,j])!=0)
    assert witness[2].has(c,d);checks+=1
    data=json.loads((C/'scalar_second_parallel_primitive/results.json').read_bytes())
    params=s.symbols('b c t',real=True);loc=dict(zip(('b','c','t'),params))
    nf=[s.sympify(v,locals=loc) for v in data['N4']];n1=[s.sympify(v,locals=loc) for v in data['N2']];n0=[s.sympify(v,locals=loc) for v in data['N0']]
    K=s.symbols('K');actual=matrix(nf,4)+K*matrix(n1,2)+K**2*matrix(n0,0)
    for val in weight*actual-actual.T*weight:
        assert s.expand(val)==0;checks+=1
    # Bosonic h has no graded product minus: s(1/2 h.Nh)=1/2(Gc.Nh+h.NGc).
    # Formal adjunction identifies the two summands. The contact sign is fixed
    # independently by (-i)^5=-i, (-i)^3=+i, (-i)^1=-i.
    for n,sign in [(5,1),(3,-1),(1,1)]:
        assert s.simplify((-s.I)**n/(-s.I)-sign)==0;checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        weighted_fiber_transpose=True,negative_control=dict(row=witness[0],column=witness[1],difference=str(witness[2])),
        formal_assumptions=['Levi-Civita metric connection','parallel coefficient tensors made of metric and constant K','complete symmetrization of every derivative word','compactly supported fields or vanishing boundary contribution'],
        proof='Integration by parts reverses even words with sign+; full symmetrization is invariant under reversal; fiber transpose matches the paired coefficient tensors',
        local_primitive='For the matched contact representative A_scalar=-CE integral h.NG(c), B_scalar=-CE/2 integral h.Nh satisfies s0 B_scalar=A_scalar',
        cancellation_counterterm='Opposite sign +CE/2 integral h.Nh cancels this representative at linearized constant-cutoff level',
        not_claimed=['No temporal combinatorial prefactor selected','No nonlinear completion','No full metric/ghost sector','No field-dependent cutoff completion','No full Q2','No Lean compilation'],
        gate_changed=False)
    put(D/'results.json',result)
    files=[Path(__file__),C/'scalar_second_parallel_primitive/results.json',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
