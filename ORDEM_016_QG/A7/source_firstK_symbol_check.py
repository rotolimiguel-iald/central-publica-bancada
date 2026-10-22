"""Measure candidate source symbol; compare its log with the paid local log.

An invariant fit is not a proof of curved adjunction or Einstein composition.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from source_full_fourier_engine import source_node
from position_metric_bubble_engine import BASIS
from oneform_second_curvature_engine_v2 import oneform_second
H=Path(__file__).resolve().parent;D=H/'source_firstK_symbol';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'source_full_fourier_engine.py',H/'source_flat_full_fourier/results.json',H/'covariant_source_operator/results.json',H/'angular_cubature_degree12/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Candidate firstK source Fourier symbol, including potentially nonlocal longitudinal structure',
 basis=['Tpv','pTp pv/p2','trT pv'],log_basis=['1','FourierLog','FourierLog^2'],
 checks='Three axial fits, independent nonaxis holdout; compare log to -1/4 paid covariant UV log without imposing equality',
 exclusions=['curved adjunction not established','Einstein composition','full Ward','Q2'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();nodes=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())['nodes'];data=[]
def uv(T,p,v):
    jet,_,_=oneform_second(v,p);out=F()
    for a in range(4):
        for b in range(4):
            if not T[4*a+b]:continue
            y=F(3,8)*sum(jet((a,i,i),b,1)+jet((b,i,i),a,1) for i in range(4))
            y-=F(1,2)*sum(jet((a,b,i),i,1) for i in range(4))
            y-=F(37,8)*(jet((a,),b,0)+jet((b,),a,0))
            if a==b:y+=2*sum(jet((i,),i,0) for i in range(4))
            out+=T[4*a+b]*y
    return out
def basis(ti,p,v):
    T=s.Matrix(4,4,BASIS[ti]);p=s.Matrix(p);v=s.Matrix(v)
    return [(p.T*T*v)[0],(p.T*T*p)[0]*p.dot(v)/p.dot(p),s.trace(T)*p.dot(v)]
def run(ti,p,v):
    T=BASIS[ti];out=[F(),F(),F()]
    for node in nodes:
        val=source_node(T,p,v,tuple(node['vector']),1)
        for j in range(3):out[j]+=F(node['weight'])*val[j]
    local=-uv(T,p,v)/4
    row=dict(T=ti,p=p,v=v,full=list(map(str,out)),local_UV_Log=str(local),
        difference_Log=str(out[1]-local))
    data.append(row);print(json.dumps(dict(**row,cpu=time.process_time()-cpu)),flush=True)
    return out
p=(1,0,0,0);fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))]
fit=s.Matrix([basis(ti,p,v) for ti,v in fixtures]).inv()*s.Matrix([list(map(s.Rational,run(ti,p,v))) for ti,v in fixtures])
p=(1,2,-1,1);v=(2,-1,1,3);got=run(4,p,v);expected=s.Matrix([basis(4,p,v)])*fit
for j in range(3):assert s.Rational(got[j])==expected[j],(j,got[j],expected[j])
result=dict(at=datetime.now(timezone.utc).isoformat(),status='CANDIDATE_SOURCE_SYMBOL_MEASURED',
 coefficients=[[str(fit[i,j]) for j in range(3)] for i in range(3)],values=data,independent_checks=3,
 cpu_seconds=time.process_time()-cpu,curved_adjunction_validated=False,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'}))
