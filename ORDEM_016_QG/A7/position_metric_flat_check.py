"""Validate the position contraction against the previously computed flat loop."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from position_metric_bubble_engine import *
from metric_radial_bitensor_engine import metric_radial_jet
from curved_source_jet_engine import x as xx,z as zz,L
H=Path(__file__).resolve().parent;D=H/'position_metric_flat';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'position_metric_bubble_engine.py'),
    reference_sha256=sha(H/'metric_bubble_v2/results.json'),
    target='Derivative-expanded off-diagonal position bubble must reproduce full planar UV log before curvature',
    normalization='4k/(4pi²) propagator and16k vertex; angular mean /16',
    degree_bound='Flat angular degree<=8 from <=4 internal derivatives and Taylor degree<=4',
    no_new_model_calls=True,full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
point=(1,2,0,-1);norm=sum(v*v for v in point)
G0,G1,GL,d0,d1=green_integer(point)
subs=dict(zip(xx,point));subs[zz]=norm;subs[L]=0
for i in range(5):
    for j in range(5):
        M0=metric_radial_jet(0,i-1,j-1).subs(subs)
        M1=metric_radial_jet(1,i-1,j-1).subs(subs)
        ML=metric_radial_jet(1,i-1,j-1).diff(L).subs(subs)
        for a in range(10):
            for b in range(10):
                check(f'G0_{i}_{j}_{a}_{b}',F(G0[10*i+a].get(10*j+b,0),d0),F(M0[a,b]))
                check(f'G1_{i}_{j}_{a}_{b}',F(G1[10*i+a].get(10*j+b,0),d1),F(M1[a,b]))
                check(f'GL_{i}_{j}_{a}_{b}',F(GL[10*i+a].get(10*j+b,0),d1),F(ML[a,b]))
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
cc=list(map(F,json.loads((H/'metric_bubble_v2/results.json').read_bytes())['metric_coefficients_over_A0']))
p=(1,0,0,0)
def inv(A,B):
    am=s.Matrix(4,4,A);bm=s.Matrix(4,4,B);pv=s.Matrix(p)
    pa=(pv.T*am*pv)[0];pb=(pv.T*bm*pv)[0]
    return [F(s.trace(am*bm)),F(s.trace(am)*s.trace(bm)),
            F(pa*s.trace(bm)+pb*s.trace(am)),F((pv.T*am*bm*pv)[0]),F(pa*pb)]
lookup={p:i for i,p in enumerate(LABELS)}
pairs=[(lookup[a],lookup[b]) for a,b in [((1,2),(1,2)),((1,1),(2,2)),
    ((0,0),(1,1)),((0,1),(0,1)),((0,0),(0,0))]]
values=[]
for a,b in pairs:
    A,B=BASIS[a],BASIS[b]
    actual=sum((F(node['weight'])*contracted_node(A,B,p,tuple(node['vector']),curved=False)[0]
                for node in nodes),F())
    expected=sum(c*v for c,v in zip(cc,inv(A,B)))
    check(f'flat_loop_{a}_{b}',actual,expected)
    values.append(dict(a=a,b=b,actual=str(actual),expected=str(expected)))
    print(json.dumps(dict(pair=[a,b],actual=str(actual),expected=str(expected),elapsed=perf_counter()-wall)),flush=True)
fresh(D/'results.json',dict(statute='REAL_POSITION_VS_MOMENTUM_PRINCIPAL_METRIC_LOG',checks=len(checks),
    check_names=checks,values=values,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'position_metric_bubble_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu_seconds=process_time()-cpu)))
