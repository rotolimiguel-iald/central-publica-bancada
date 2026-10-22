"""Direct GammaGamma density versus stored Fourier vertices, including cutoff flux."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
from metric_boundary_current_engine import metric_series,boundary_current,submasks
from metric_principal_vertices import gamma2,upper_product,contraction,eh_quadratic_8k,eh_cubic_16k,basis
from localized_eh_cubic_engine import localized_vertex_data,evaluate

H=Path(__file__).resolve().parent;D=H/'real_density_fourier_vertex';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    action='S=-integral chi sqrt(g)R/(2kappa), R=GammaGamma+divB',
    method='Compute actual Christoffel and metric/density coefficient series, no Fourier i inserted',
    target='Stored localized cubic is -16kappa times direct real-derivative action',
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),H/'metric_principal_vertices.py',H/'metric_boundary_current_engine.py',H/'localized_eh_cubic_engine.py']]))
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert a==b,(a,b);checks+=1
def real_gamma_gamma(fields):
    inverse,density=metric_series([A for A,p in fields]);full=(1<<len(fields))-1
    gammas={}
    for mask in range(1,full+1):
        terms=[]
        for leg,(A,p) in enumerate(fields):
            if mask&(1<<leg):terms.append(upper_product(inverse[mask^(1<<leg)],gamma2(A,tuple(p))))
        gammas[mask]=tuple(sum(t[i] for t in terms)*F(1,2) for i in range(64))
    total=F()
    for denmask in submasks(full):
        remain=full^denmask
        for outer in submasks(remain):
            left=remain^outer
            for first in submasks(left):
                second=left^first
                if first and second:total+=density[denmask]*contraction(inverse[outer],gammas[first],gammas[second])
    return total
rows=[];p=(1,2,-1,1);q=(2,-1,1,0);r=(-1,1,0,2);eta=(1,-1,0,1)
for ij,kl,mn in [((0,0),(1,1),(2,2)),((0,1),(0,2),(1,3)),((1,1),(0,1),(0,1)),((0,0),(0,0),(0,0)),((0,2),(1,2),(0,3))]:
    A,B,C=basis(*ij),basis(*kl),basis(*mn)
    density2=real_gamma_gamma(((A,p),(B,q)))
    eq(eh_quadratic_8k(A,p,B,q),4*density2)
    density3=real_gamma_gamma(((A,p),(B,q),(C,r)))
    eq(eh_cubic_16k(A,p,B,q,C,r),8*density3)
    b=boundary_current((A,p),(B,q),(C,r))
    physical=-density3/2+sum(t*v for t,v in zip(eta,b))/2
    stored=evaluate(localized_vertex_data(A,1,eta),p,B,q,C,r)
    eq(stored,-16*physical)
    rows.append(dict(fields=[ij,kl,mn],physical_real_kappa1=str(physical),stored_fourier=str(stored)))
assert any(F(v['physical_real_kappa1']) for v in rows);checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    rows=rows,conversion='V3real=-stored/(16kappa), V2real=-stored/(8kappa); both contain two derivatives including cutoff derivatives',
    consequence='One raw EH vertex with direct b.Zbar requires +1/4, not -1/4; two EH-derived vertices keep product sign',
    no_full_Q2=True)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
