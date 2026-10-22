"""Match a free local Hessian family to the ACTUAL scalar parallel readout through K."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from fractions import Fraction as F
import sys,json,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'scalar_measured_primitive'
sys.path.insert(0,str(H))
from oneform_second_curvature_engine_v2 import oneform_second,loop_gauge
from deliver_nonminimal_wick_and_mimo_audit import sha,put

def main():
    D.mkdir(exist_ok=False);start=time.process_time();checks=0
    principal=H/'balanced_scalar_euler_v2/results.json';curved=C/'scalar_parallel/results.json'
    p0=json.loads(principal.read_bytes())['coefficients'];p1=json.loads(curved.read_bytes())['coefficients']
    u,v,w=[s.Rational(p0[k]) for k in ('aa','bb','cc')]
    U,V,W=[s.Rational(p1[k]) for k in ('aa','bb','cc')]
    b,c,t=s.symbols('b c t',real=True)
    flat=[v-c/2,u/2-b,b,c,w/2-b-c/2]
    zero=[F(0)]*5
    def measured(p,e,o):
        p2=sum(k*k for k in p);pe=sum(k*l for k,l in zip(p,e))
        a0,a1,a2=(u,v,w) if o==0 else (-U,-V,-W)
        return s.Matrix(4,4,lambda i,j:s.expand((p2 if o==0 else 1)*(a0*int(i==j)*p2*pe+a1*(p[i]*e[j]+p[j]*e[i])*p2+a2*p[i]*p[j]*pe)))
    def evaluate(p,e,first,o):
        _,_,sym=oneform_second(e,p)
        return s.Matrix(loop_gauge(sym,flat,first,[F(0)]*2,o))
    # Identify the invariant residual using simple data, then verify symbolically below.
    rows=[];rhs=[]
    samples=[((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0)),((1,2,-1,1),(2,-1,1,2))]
    for p,e in samples:
        diff=measured(p,e,1)-evaluate(p,e,zero,1);p2=sum(k*k for k in p);pe=sum(k*l for k,l in zip(p,e))
        for i in range(4):
            for j in range(4):
                rows.append([p2*(p[i]*e[j]+p[j]*e[i]),p[i]*p[j]*pe,int(i==j)*p2*pe]);rhs.append(diff[i,j])
    fit,free=s.Matrix(rows).gauss_jordan_solve(s.Matrix(rhs));assert len(free)==0
    d1=fit[0]-t/2;d3=(fit[1]-t)/2;d2=fit[2]/2-d3
    first=list(map(s.expand,[d1,d2,d3,d3,t]))
    p=s.symbols('p0:4')
    for r in range(4):
        e=tuple(int(i==r) for i in range(4))
        for o in (0,1):
            for val in evaluate(p,e,first,o)-measured(p,e,o):
                assert s.expand(val)==0,(r,o,val);checks+=1
        print(json.dumps(dict(stage='symbolic_polarization',r=r,checks=checks,cpu_seconds=time.process_time()-start)),flush=True)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        flat_coefficients=list(map(str,flat)),first_curvature_coefficients=list(map(str,first)),parameters=['b','c','t'],parameters_chosen=False,
        comparison='N G(c) on covector parallel-wave jets matches R(p)=Aflat(p)-K Aparallel(p); the measured distribution applied to exp(ipx) has common factor -i CE',
        advance='Target is actual scalar graph readout, not unproved replacement of partial derivatives by covariant derivatives',
        scope='Local normal-jet matching through K, scalar hc sector, constant cutoff; no naturality theorem for the full prescription',
        full_Q2=False,causal_normalization_constructed=False,gate_changed=False)
    put(D/'results.json',result)
    files=[Path(__file__),principal,curved,C/'scalar_parallel_readout.py',H/'oneform_second_curvature_engine_v2.py',H/'spaceform_covariant_jet_engine.py',D/'results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
