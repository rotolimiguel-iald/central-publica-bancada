"""Cross-check radial tensor propagator jets against coordinate parametrices."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time,perf_counter
import hashlib,json
import sympy as s
from curved_source_jet_engine import x,z,L,hjet
from metric_radial_bitensor_engine import metric_radial_jet
from metric_coincident_jet_engine_v2 import metric_fiber
H=Path(__file__).resolve().parent;D=H/'metric_radial_bitensor';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'metric_radial_bitensor_engine.py'),
    coordinate_source_sha256=sha(H/'curved_source_jet_engine.py'),
    target='Full first-K spin-two bitensor and first/mixed endpoint covariant derivatives',
    comparison='Transform coordinate jets with coframe and Christoffel symbols',
    no_loop_computed=True,full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,e):assert s.expand(e)==0,(n,e);checks.append(n)
f=metric_fiber();labels=f['labels']
N=s.Matrix(4,4,lambda a,b:(int(a==b)*z-x[a]*x[b])/6)
def gamma(r,i,a):return -(int(r==i)*x[a]+int(r==a)*x[i]-2*int(i==a)*x[r])/3
def coord(a,b,c,d,xi,yi):
    ans=hjet(1,a,b,c,d,yi,xi)
    for r in range(4):
        # Convert both covariant field slots at X to the radial orthonormal frame.
        ans+=N[r,a]*hjet(0,r,b,c,d,yi,xi)+N[r,b]*hjet(0,a,r,c,d,yi,xi)
        if xi>=0:
            # Derivative index and Christoffel action on the two field indices.
            ans+=N[r,xi]*hjet(0,a,b,c,d,yi,r)
            ans-=gamma(r,xi,a)*hjet(0,r,b,c,d,yi,-1)
            ans-=gamma(r,xi,b)*hjet(0,a,r,c,d,yi,-1)
    return s.expand(ans)
for xi in [-1,0,1,2,3]:
    for yi in [-1,0,1,2,3]:
        radial=metric_radial_jet(1,xi,yi)
        for a,(i,j) in enumerate(labels):
            for b,(k,l) in enumerate(labels):
                check(f'jet_{xi}_{yi}_{a}_{b}',coord(i,j,k,l,xi,yi)-radial[a,b])
# A nonzero derivative of parallel transport must survive outside radial direction.
test=s.expand(metric_radial_jet(1,1,-1)[0,1])
assert test!=0
fresh(D/'results.json',dict(statute='REAL_EXACT_COVARIANT_RADIAL_BITENSOR_JETS',
    checks=len(checks),check_names=checks,
    retained=['Tensor parallel transport','Christoffel field terms','Derivative coframe conversion',
              'Van Vleck term','Modular-independent curvature endomorphism log term'],
    negative_control_nonzero_transport=str(test),
    no_loop_computed=True,full_Q2=False,gate_changed=False,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in
    [Path(__file__),H/'metric_radial_bitensor_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu_seconds=process_time()-cpu)))
