"""Fit and check the constant-field K² radial bubble, retaining log terms."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
from position_metric_second_curvature_engine_v2 import *
H=Path(__file__).resolve().parent;D=H/'position_metric_second_curvature_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'position_metric_second_curvature_engine_v2.py'),
    supersedes_sha256='79eb9d1f71cdd91e48336e3bd180881bf1331c418d39d31e3a8b8dea138b78cc',
    correction='Keep denominator z cubed before imposing z=x²; v1 conversion failed locally',
    target='Full55 raw radial K² bubble pairs, all propagator/volume/connection/potential pieces',
    excludes=['Anchored-leg adjoints','smooth W','finite causal extension'],full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
# Sparse polynomial conversion preserves all rational coefficients.
point=(1,2,0,-1);zv=sum(t*t for t in point);G,GL,den=second_integer(point)
subs=dict(zip(sx,point));subs[sz]=zv;subs[sL]=0
for i in range(4):
    for j in range(4):
        M=green_jet(2,i,j);N=M.subs(subs);NL=M.diff(sL).subs(subs)
        for a in range(10):
            for b in range(10):
                check(f'sparse2_{i}{j}_{a}_{b}',F(G[10*(i+1)+a].get(10*(j+1)+b,0),den),F(N[a,b]))
                check(f'sparse2log_{i}{j}_{a}_{b}',F(GL[10*(i+1)+a].get(10*(j+1)+b,0),den),F(NL[a,b]))
values=[];matrix=[]
for a in range(10):
    for b in range(a,10):
        A,B=BASIS[a],BASIS[b];val=[F() for _ in range(5)]
        for n in nodes:
            piece=second_node(A,B,tuple(n['vector']))
            for k in range(5):val[k]+=F(n['weight'])*piece[k]
        am=s.Matrix(4,4,A);bm=s.Matrix(4,4,B)
        matrix.append([s.trace(am*bm),s.trace(am)*s.trace(bm)])
        values.append(dict(a=a,b=b,pieces=list(map(str,val)),total=str(sum(val[:4]))))
    print(json.dumps(dict(row=a,cpu=process_time()-cpu)),flush=True)
fresh(D/'raw_values.json',dict(values=values,cpu_seconds=process_time()-cpu))
M=s.Matrix(matrix);fits=[]
for piece in range(5):
    coeff,params=M.gauss_jordan_solve(s.Matrix([v['pieces'][piece] for v in values]));check(f'unique_fit_{piece}',len(params),0)
    fits.append(list(map(str,coeff)))
for a,b in [(0,4),(5,5)]:
    first=second_node(BASIS[a],BASIS[b],(1,2,1,-1));scaled=second_node(BASIS[a],BASIS[b],(2,4,2,-2))
    check(f'scaling_{a}_{b}',first,scaled)
total=[sum(F(fits[k][j]) for k in range(4)) for j in range(2)]
fresh(D/'results.json',dict(statute='DERIVED_RAW_K2_RADIAL_PROFILE_NOT_INTEGRATED_HESSIAN',checks=len(checks),values=values,
    pieces=['derivative_propagators_volume','external_connection','potential_cross','potential_squared','log_coefficient'],
    coefficients=fits,total=list(map(str,total)),cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'position_metric_second_curvature_engine_v2.py',D/'PRE_REGISTER.json',D/'raw_values.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),coefficients=fits,total=list(map(str,total)),cpu=process_time()-cpu)))
