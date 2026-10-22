"""Full100 independent integer contraction audit of the adjoint correction."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from position_metric_adjoint_engine import *
H=Path(__file__).resolve().parent;D=H/'position_metric_adjoint_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),
    predecessor_sha256=sha(H/'position_metric_adjoint/results.json'),
    target='Full100 pairs via integer contraction, distinct evaluation order; nonaxis and scalar box² controls',
    normalization='Raw bubble/A0; K coefficient of integration-by-parts correction only',full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
ref=list(map(F,json.loads((H/'position_metric_adjoint/results.json').read_bytes())['coefficients']))
def iv(A,B,p):
    a=s.Matrix(4,4,A);b=s.Matrix(4,4,B);q=s.Matrix(p);p2=(q.T*q)[0]
    return list(map(F,[p2*s.trace(a*b),p2*s.trace(a)*s.trace(b),(q.T*a*q)[0]*s.trace(b),(q.T*b*q)[0]*s.trace(a),(q.T*a*b*q)[0]]))
def integer_jets(A,p):
    out={}
    for key,vector in jet_data(A,p).items():
        v=[18*t for t in vector];assert all(t.denominator==1 for t in v)
        out[key]=[t.numerator for t in v]
    return out
p=(1,0,0,0);jets=[integer_jets(A,p) for A in BASIS]
total=[[F() for _ in range(10)] for _ in range(10)]
for node_index,node in enumerate(nodes):
    x=tuple(node['vector']);z=sum(t*t for t in x);G,_,_,d0,_=green_integer(x)
    v2=[vertex_data(A)[0] for A in BASIS]
    v1=[vertex_data(A)[1] for A in BASIS]
    c2=[sandwich(G,W) for W in v2]
    c1=[[sandwich(G,W) for W in V] for V in v1]
    t2=[[[frob(c2[e],v1[b][j]) for j in range(4)] for b in range(10)] for e in range(10)]
    t1=[[[[frob(c1[e][i],v1[b][j]) for j in range(4)] for b in range(10)] for e in range(10)] for i in range(4)]
    factor=-F(node['weight'])*F(z*z,108*16*d0*d0)
    x3={w:mono(w,x) for w in TRIPLES};x2={w:mono(w,x) for w in PAIRS}
    for a,J in enumerate(jets):
        accum=[0]*10
        for j in range(4):
            vec=[sum(v*J[j,w][e] for w,v in x3.items()) for e in range(10)]
            for e,v in enumerate(vec):
                if v:
                    for b in range(10):accum[b]+=v*t2[e][b][j]
            for i in range(4):
                vec=[sum(v*J[j,tuple(sorted((i,)+w))][e] for w,v in x2.items()) for e in range(10)]
                for e,v in enumerate(vec):
                    if v:
                        for b in range(10):accum[b]+=3*v*t1[i][e][b][j]
        for b in range(10):total[a][b]+=factor*accum[b]
    if node_index%16==0:print(json.dumps(dict(node=node_index,cpu=process_time()-cpu)),flush=True)
for a in range(10):
    for b in range(10):check(f'integer_full100_{a}_{b}',total[a][b],sum(c*v for c,v in zip(ref,iv(BASIS[a],BASIS[b],p))))
for a,b,p in [(0,4,(1,2,-1,1)),(5,5,(1,-1,0,2)),(4,0,(1,2,-1,1))]:
    actual=sum((F(n['weight'])*adjoint_node(BASIS[a],BASIS[b],p,tuple(n['vector'])) for n in nodes),F())
    check(f'nonaxis_{a}_{b}',actual,sum(c*v for c,v in zip(ref,iv(BASIS[a],BASIS[b],p))))
    print(json.dumps(dict(nonaxis=[a,b],value=str(actual),cpu=process_time()-cpu)),flush=True)
# Independent scalar calibration: on constant-curvature normal chart,
# Box = partial²+K(z delta-xx)partialpartial/3 -2K x.partial.
# Therefore (Box² exp(ipx))_K at0 =2p².
from radial_covariant_jet_engine import radial_jets
g=[[int(i==j) for j in range(4)] for i in range(4)]
p=(1,2,-1,1);v,_,_=radial_jets(g,p)
check('scalar_trace_box_squared',sum(v((i,i,j,j),a,a) for i in range(4) for j in range(4) for a in range(4)),8*sum(t*t for t in p))
prior=list(map(F,json.loads((H/'position_metric_curvature_v2/results.json').read_bytes())['curvature_coefficients']))
combined=[a+b for a,b in zip(prior,ref)]
check('mixed_symmetry_without_tuning',combined[2],combined[3])
check('delete_adjoint_breaks_symmetry',prior[2]!=prior[3],True)
fresh(D/'results.json',dict(statute='REAL_FULL_FIBER_ADJOINT_CORRECTION',checks=len(checks),check_names=checks,
    coefficients=list(map(str,ref)),combined=list(map(str,combined)),values=[[str(v) for v in row] for row in total],
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu=process_time()-cpu)))
