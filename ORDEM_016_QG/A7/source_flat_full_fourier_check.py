"""Validate the flat source functional, keeping its opposite Fourier orientation."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from source_full_fourier_engine import source_node
from curved_source_jet_engine import kernel
from finite_harmonic_extension_engine_v2 import represent,Q
from flat_reference_weight_engine import scalar_reference_local
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'source_flat_full_fourier';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'source_full_fourier_engine.py',H/'curved_harmonic_fourier_engine.py',
 H/'first_curvature_gauge_generating_engine.py',H/'flat_reference_ward/results.json',H/'angular_cubature_degree12/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Flat full source Fourier functional, finite part against harmonic reference+contact and logarithmic Einstein image',
 orientation='Tensor test exp(-ipX), ghost exp(+ipY); A phase +i and B explicit ghost derivative gives -i',
 scope='Flat only; curved source code remains candidate, not used',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();nodes=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())['nodes'];checks=[];rows=[]
def scalar_reference(T,p,v):
    a,b=kernel(T,s.Matrix(v),s.Matrix(p),0);ar,ac=represent(a);br,bc=represent(b)
    return s.expand(-(scalar_reference_local(ar)+scalar_reference_local(br)+ac+bc).subs(dict(zip(Q,p))))
def einstein(T,p):
    p=s.Matrix(p);p2=p.dot(p)
    return p2*T-p*(T*p).T-(T*p)*p.T+p*p.T*s.trace(T)+s.eye(4)*((p.T*T*p)[0]-p2*s.trace(T))
def run(T,p,v,label):
    T=s.Matrix(T);out=[F(),F(),F()]
    for node in nodes:
        value=source_node(tuple(T),p,v,tuple(node['vector']),0)
        for j in range(3):out[j]+=F(node['weight'])*value[j]
    expected=scalar_reference(T,p,v)
    assert s.Rational(out[0])==expected,(label,out,expected)
    assert out[2]==0
    checks.extend([label+'_finite_against_differential_reference',label+'_no_log_squared'])
    row=dict(label=label,T=list(map(str,T)),p=p,v=v,full=list(map(str,out)),reference=str(expected))
    rows.append(row);print(json.dumps(dict(label=label,out=list(map(str,out)),cpu=time.process_time()-cpu)),flush=True)
    return out
p=(1,0,0,0)
for ti,v in [(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))]:
    T=s.Matrix(4,4,BASIS[ti]);r=run(T,p,v,'raw_'+str(ti))
    e=run(einstein(T,p),p,v,'Einstein_'+str(ti))
    assert e[1]==0;checks.append('Einstein_common_log_'+str(ti))
p=(1,2,-1,1);v=(2,-1,1,3);T=s.Matrix(4,4,BASIS[4])
r=run(einstein(T,p),p,v,'nonaxis_Einstein');assert r[1]==0;checks.append('nonaxis_Einstein_common_log')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FLAT_SOURCE_FULL_FOURIER_CALIBRATED',
 checks=len(checks),check_names=checks,values=rows,cpu_seconds=time.process_time()-cpu,
 full_Q2=False,curved_source_validated=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')}))
