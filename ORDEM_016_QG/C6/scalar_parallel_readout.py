"""Parallel contravariant ghost readout of the measured scalar contact."""
from pathlib import Path
from datetime import datetime, timezone
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1]; H=ROOT/'A7'; D=ROOT/'C6/scalar_parallel'
sys.path[:0]=[str(ROOT/'C6'),str(H)]
import balanced_log_pair_engine as E
from smooth_line_compatibility_check_v2 import multiply
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    source=ROOT/'C6/scalar_vertex_v2/MATRICES.json'
    data=json.loads(source.read_bytes());flat,curved=[s.Matrix(a) for a in data]
    x,Q=E.x,E.Q;xx=sum(t*t for t in x);q2=sum(t*t for t in Q)
    P=s.Matrix(4,4,lambda r,j:(xx*int(r==j)-x[r]*x[j])/6)
    # Radial parallel equation for a contravariant vector: x.dP+Gamma_rad=0.
    gamma_rad=-2*P
    for r in range(4):
        for j in range(4):
            radial=sum(x[i]*s.diff(P[r,j],x[i]) for i in range(4))
            assert s.expand(radial+gamma_rad[r,j])==0;checks+=1
    assert any(s.expand(-sum(x[i]*s.diff(P[r,j],x[i]) for i in range(4))+gamma_rad[r,j])!=0 for r in range(4) for j in range(4))
    checks+=1
    corrected=curved.copy()
    for row in range(10):
        for j in range(4):
            corrected[row,j]=s.expand(curved[row,j]+sum(multiply(P[r,j],flat[row,r]) for r in range(4)))
    # Independent definition on test polynomials: (P d^alpha delta)(f)=d^alpha delta(P f).
    def action(local,test):
        result=0
        for powers,c in s.Poly(local,*Q).terms():
            v=test
            for i,n in enumerate(powers):v=s.diff(v,x[i],n)
            result+=c*(-1)**sum(powers)*v.subs(dict.fromkeys(x,0))
        return s.expand(result)
    tests=[x[0]**3,x[0]*x[1]**2,x[0]*x[1]*x[2],(x[0]+2*x[1]-x[2]+x[3])**3]
    for row in range(10):
        for j in range(4):
            for f in tests:
                assert s.expand(action(corrected[row,j],f)-action(curved[row,j],f)-sum(action(flat[row,r],s.expand(P[r,j]*f)) for r in range(4)))==0
                checks+=1
    aa,bb,cc=s.symbols('aa bb cc');labels=[(a,b) for a in range(4) for b in range(a,4)]
    target=s.Matrix([[(1 if a==b else 2)*(aa*int(a==b)*Q[j]*q2+bb*(int(a==j)*Q[b]+int(b==j)*Q[a])*q2+cc*Q[a]*Q[b]*Q[j]) for j in range(4)] for a,b in labels])
    equations=[]
    for v in corrected-target:equations.extend(s.Poly(s.expand(v),*Q).coeffs())
    sol=s.solve(equations,(aa,bb,cc));assert set(sol)=={aa,bb,cc}
    for v in corrected-target.subs(sol):assert s.expand(v)==0;checks+=1
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        coefficients={str(k):str(v) for k,v in sol.items()},
        statement='Scalar hc graph: coordinate derivative-of-delta contact evaluated on contravariant ghost parallel transported from Y to X',
        density_already_in_Euler=True,metric_external_at_Y=True,
        full_covariant_operator_proved=False,full_Q2=False,gate_changed=False)
    put(D/'MATRICES.json',[[str(v) for v in row] for row in corrected.tolist()]);put(D/'results.json',result)
    files=[Path(__file__),source,H/'smooth_line_compatibility_check_v2.py',D/'MATRICES.json',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
