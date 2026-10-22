"""Measure second-K Ward coefficients with fifth-order covariant ghost jets."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
from fractions import Fraction as F
import hashlib,json
import sympy as s
from oneform_second_curvature_engine_v2 import *
H=Path(__file__).resolve().parent;D=H/'second_curvature_ward_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'oneform_second_curvature_engine_v2.py'),
    target='K2 Hloop G and E R; calibrate differentiated classical Ward and firstK; linear tadpole to be computed independently',full_Q2=False))
cpu=process_time();checks=0
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
def read(f):return json.loads((H/f).read_bytes())
flat=list(map(F,read('metric_bubble_v2/results.json')['combined_Hessian_coefficients_over_hbar_A0']))
first=list(map(F,read('first_curvature_total_hessian/results.json')['total']))
second=list(map(F,read('position_metric_ordered_second/results.json')['total']))
cases=[];rows=[];left=[];right=[]
for p,v in [((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0)),((1,2,-1,1),(2,-1,1,2))]:
    jet,gauge,sym=oneform_second(v,p);p2=sum(x*x for x in p);pv=sum(x*y for x,y in zip(p,v))
    first_actual=loop_gauge(sym,flat,first,second,1)
    for a in range(4):
        for b in range(4):
            G=p[a]*v[b]+p[b]*v[a]
            check(first_actual[a][b],-F(1,2)*p2*G-2*p[a]*p[b]*pv+F(3,2)*int(a==b)*p2*pv)
            for i in range(4):
                for j in range(4):check(einstein_gauge(gauge,(i,j),a,b,2))
    actual=loop_gauge(sym,flat,first,second,2);source=[]
    for a in range(4):
        rr=[]
        for b in range(4):
            e=-4*sum(jet((a,b,i),i,1) for i in range(4))
            if a==b:
                e+=4*sum(jet((j,j,i),i,1) for i in range(4) for j in range(4))
                e+=12*sum(jet((i,),i,0) for i in range(4))
            rr.append(e);rows.append([p[a]*v[b]+p[b]*v[a],int(a==b)*pv]);left.append(actual[a][b]);right.append(e)
        source.append(rr)
    cases.append(dict(p=p,v=v,HloopG=[[str(t) for t in row] for row in actual],ER=[[str(t) for t in row] for row in source]))
    print(json.dumps(dict(case=len(cases),checks=checks,cpu=process_time()-cpu)),flush=True)
M=s.Matrix(rows);hl,pa=M.gauss_jordan_solve(s.Matrix(left));er,pb=M.gauss_jordan_solve(s.Matrix(right))
check(len(pa),0);check(len(pb),0)
fresh(D/'results.json',dict(statute='MEASURE_SECOND_K_LOG_WARD_BEFORE_LINEAR_TADPOLE',checks=checks,cases=cases,
    basis=['K²(pv^t+vp^t)','K²g(p.v)'],HloopG=list(map(str,hl)),ER=list(map(str,er)),sum=list(map(str,hl+er)),
    cpu_seconds=process_time()-cpu,full_Q2=False))
files=[Path(__file__),H/'oneform_second_curvature_engine_v2.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,HloopG=list(map(str,hl)),ER=list(map(str,er)),sum=list(map(str,hl+er)),cpu=process_time()-cpu)))
