"""Complete parallel readout and local normal-jet matching of the scalar graph through K²."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'scalar_second_parallel_primitive'
sys.path.insert(0,str(H))
import balanced_log_pair_engine as E
from smooth_line_compatibility_check_v2 import multiply
from oneform_second_curvature_engine_v2 import oneform_second,loop_gauge
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    x,Q=E.x,E.Q;X=s.Matrix(x);xx=X.dot(X);N=xx*s.eye(4)-X*X.T
    P1=N/6;P2=7*xx*N/360;g1=-N/3;g2=2*xx*N/45
    for v in g2+g1*P1+P2-xx*N/120:eq(v,0)
    for v in P2+P2.T+P1.T*P1+P1.T*g1+g1*P1+g2:eq(v,0)
    flat,first=[s.Matrix(m) for m in json.loads((C/'scalar_vertex_v2/MATRICES.json').read_bytes())]
    second=s.Matrix(json.loads((C/'scalar_second_curvature_v2/MATRIX.json').read_bytes()))
    par=second.copy()
    for row in range(10):
        for j in range(4):par[row,j]=s.expand(second[row,j]+sum(multiply(P1[r,j],first[row,r])+multiply(P2[r,j],flat[row,r]) for r in range(4)))
    # Direct distribution action gives an independent check of all first-degree test jets.
    def act(poly,test):
        out=0
        for powers,c in s.Poly(poly,*Q).terms():
            value=test
            for i,n in enumerate(powers):value=s.diff(value,x[i],n)
            out+=c*(-1)**sum(powers)*value.subs(dict.fromkeys(x,0))
        return s.expand(out)
    for row in range(10):
        for j in range(4):
            for test in x:eq(act(par[row,j],test),act(second[row,j],test)+sum(act(first[row,r],P1[r,j]*test)+act(flat[row,r],P2[r,j]*test) for r in range(4)))
    labels=[(a,b) for a in range(4) for b in range(a,4)];aa,bb=s.symbols('aa bb')
    target=s.Matrix([[(1 if a==b else 2)*(aa*int(a==b)*Q[j]+bb*(int(a==j)*Q[b]+int(b==j)*Q[a])) for j in range(4)] for a,b in labels])
    equations=[]
    for v in par-target:equations.extend(s.Poly(v,*Q).coeffs())
    sol=s.solve(equations,(aa,bb));assert set(sol)=={aa,bb}
    for v in par-target.subs(sol):eq(v,0)
    # Match the O(K²) readout to the same previously verified N4+K N2 family.
    old=json.loads((C/'scalar_measured_primitive/results.json').read_bytes());b,c,t=s.symbols('b c t',real=True)
    loc={'b':b,'c':c,'t':t};nf=[s.sympify(v,locals=loc) for v in old['flat_coefficients']];n1=[s.sympify(v,locals=loc) for v in old['first_curvature_coefficients']]
    p=s.symbols('p0:4');rows=[];rhs=[];data=[]
    for r in range(4):
        e=tuple(int(i==r) for i in range(4));_,_,sym=oneform_second(e,p)
        before=s.Matrix(loop_gauge(sym,nf,n1,[F(0)]*2,2))
        wanted=s.Matrix(4,4,lambda i,j:sol[aa]*int(i==j)*p[r]+sol[bb]*(p[i]*e[j]+p[j]*e[i]))
        data.append((r,sym,wanted))
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    rows.append([s.expand(p[i]*e[j]+p[j]*e[i]).coeff(p[k]),s.expand(2*int(i==j)*p[r]).coeff(p[k])]);rhs.append(s.expand(wanted[i,j]-before[i,j]).coeff(p[k]))
    n2,free=s.Matrix(rows).gauss_jordan_solve(s.Matrix(rhs));assert len(free)==0
    for r,sym,wanted in data:
        after=s.Matrix(loop_gauge(sym,nf,n1,n2,2))
        for v in after-wanted:eq(v,0)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        K2_parallel_coefficients={str(k):str(v) for k,v in sol.items()},N4=list(map(str,nf)),N2=list(map(str,n1)),N0=list(map(str,n2)),
        free_parameters=['b','c','t'],parameters_chosen=False,
        matching='Local normal parallel-wave jets: N4+K N2+K² N0 acting on G(c) matches actual scalar contact readout at all derivative degrees5,3,1',
        distribution_factor='Actual integrated contact = -i CE times the matched polynomial on exp(i p.x)',
        limited_to='Three massless scalar flavors, fixed local Hadamard singular jet, constant cutoff, auxiliary Euclidean spaceform',
        full_Q2=False,full_causal_family=False,global_naturality_proved=False,gate_changed=False)
    put(D/'MATRIX.json',[[str(v) for v in row] for row in par.tolist()]);put(D/'results.json',result)
    paths=[Path(__file__),C/'scalar_vertex_v2/MATRICES.json',C/'scalar_second_curvature_v2/MATRIX.json',C/'scalar_measured_primitive/results.json',H/'oneform_second_curvature_engine_v2.py',D/'MATRIX.json',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths]));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
