"""Audit the nonzero residual; exhibit, but do not adopt, a local correction."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
from fractions import Fraction as F
import hashlib,json
from first_curvature_ward_engine import gauge_hessian
H=Path(__file__).resolve().parent;D=H/'first_curvature_ward_audit';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),
    hessian_sha256=sha(H/'first_curvature_total_hessian/results.json'),
    target='Test measured residual at independent momenta and polarizations; algebraic counterterm family is not adopted or a finite Ward proof'))
cpu=process_time();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
flat=list(map(F,['-61/120','-23/120','23/120','61/60','-7/10']))
curved=list(map(F,json.loads((H/'first_curvature_total_hessian/results.json').read_bytes())['total']))
cases=[]
for p in [(1,0,0,0),(1,2,-1,1),(2,-1,3,1)]:
    for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(2,-1,1,2)]:
        actual=gauge_hessian(v,p,1,flat,curved);p2=sum(t*t for t in p);pv=sum(a*b for a,b in zip(p,v))
        for a in range(4):
            for b in range(4):
                G=p[a]*v[b]+p[b]*v[a]
                expected=-F(1,2)*p2*G-2*p[a]*p[b]*pv+F(3,2)*int(a==b)*p2*pv
                check(f'residual_{p}_{v}_{a}_{b}',actual[a][b],expected)
        cases.append(dict(p=p,v=v,coefficient_verified=True))
# At this homogeneous order only, adding delta D to the local Hessian
# changes the gauge symbol by (d1+d4/2)p²G+(2d3+d4)pp(p.v)+2(d2+d3)gp²(p.v).
# The residual of Hloop G + E R has coefficients (-1/2,2,-5/2).
for t in [F(0),F(1),F(-2),F(1,3)]:
    d1=F(1,2)-t/2;d2=F(9,4)+t/2;d3=-1-t/2;d4=t
    check(f'family_G_{t}',d1+d4/2,F(1,2))
    check(f'family_pp_{t}',2*d3+d4,-2)
    check(f'family_g_{t}',2*(d2+d3),F(5,2))
fresh(D/'results.json',dict(statute='REAL_NONZERO_FIRST_K_LOG_RESIDUAL_AND_ALGEBRAIC_LOCAL_FAMILY',checks=len(checks),cases=cases,
    Hloop_G_coefficients=['-1/2','-2','3/2'],
    basis=['K p²(pv^t+vp^t)','K pp^t(p.v)','K g p²(p.v)'],
    E_R_coefficients=['0','4','-4'],sum_coefficients=['-1/2','2','-5/2'],
    local_family=['d1=1/2-t/2','d2=9/4+t/2','d3=-1-t/2','d4=t'],
    counterterm_adopted=False,full_Q2=False,complete_BRST_class=False,cpu_seconds=process_time()-cpu))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'first_curvature_ward_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu=process_time()-cpu)))
