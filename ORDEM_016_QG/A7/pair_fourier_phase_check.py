"""Check phase bookkeeping for the plus-sign plane on the moving pair leg."""
from pathlib import Path
from datetime import datetime,timezone
import json,uuid,hashlib,time
import sympy as s
H=Path(__file__).resolve().parent;D=H/'pair_fourier_phase';D.mkdir(exist_ok=True)
def put(n,o):
    p=D/n;assert not p.exists();b=json.dumps(o,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[Path(__file__),H/'curved_pair_fourier_engine.py',H/'fourier_phase_convention/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    scope='Phase of anchored pair Taylor input exp(+ipx); not source orientation or full Wick weights',
    proof='Fourier plus gives i^(m-j), covariant derivative polynomial gives i^(n-2o+j); n+m-2o=5-2order.',
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
specs=[(2,-1,0)]+[(1,i,0) for i in range(4)]+[(0,-1,1)]
for order in (0,1):
    for nx,xi,ex in specs:
        for ny,yj,ey in specs:
            if ex+ey>order:continue
            for r in range(order-ex-ey+1):
                o=order-ex-ey-r;m=nx+ny-2*r
                n=1+int(xi>=0)+int(yj>=0)
                assert n+m-2*o==5-2*order
                for j in range(3 if o else 1):
                    if m-j<0 or n-2*o+j<0:continue
                    actual=s.I**(m-j)*s.I**(n-2*o+j)/s.I
                    actual*=(-1 if ny==1 else 1)*(-1)**(ex+ey)
                    used=(-1 if ny==1 else 1)*(-1)**(ex+ey+order)
                    assert s.simplify(actual-used)==0
                    checks.append([order,nx,xi,ny,yj,r,o,j])
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),check_rows=checks,
    status='PAIR_PLUS_PLANE_PHASE_CONSISTENT',cpu_seconds=time.process_time()-cpu,
    conclusion='No rational multiplier or pair sign change: i^m is plus-plane convention. For minus-plane standalone transform use (-i)^m.',
    source_orientation='NOT_TESTED',full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_rows'}))
