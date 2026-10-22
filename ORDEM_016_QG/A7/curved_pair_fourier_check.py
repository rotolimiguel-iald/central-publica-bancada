"""Laurent checks, flat calibration and first-K raw-pair Ward symbol."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from curved_harmonic_fourier_engine import coefficients,direct_meromorphic,L
from curved_pair_fourier_engine import pair_node
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'curved_pair_fourier';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    b=json.dumps(v,indent=2,ensure_ascii=False).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'curved_pair_fourier_engine.py',H/'curved_harmonic_fourier_engine.py',
 H/'first_curvature_gauge_generating_engine.py',H/'first_curvature_gauge_generating/results.json',
 H/'angular_cubature_degree12/results.json',H/'flat_reference_ward/results.json',H/'finite_pair_ward/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Actual full Fourier/Laurent metric and ghost pair with ordered gauge input through K1',
 calibration='All three axial flat cases against previous contact plus independently computed reference',
 fit='Three firstK invariants; holdout nonaxis at T=e11',
 exclusions=['antifield source Einstein image','finite tadpole','smooth W','higher arities','full Q2'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
for m in range(5):
    for l in range(m%2,7,2):
        for ell in (0,1):
            expected=sum(s.Rational(c)*L**i for i,c in enumerate(coefficients(m,l,ell)))
            got=direct_meromorphic(m,l,ell)
            assert s.expand(expected-got)==0,(m,l,ell,expected,got)
            checks.append('Laurent_'+str((m,l,ell)))
nodes=json.loads((H/'angular_cubature_degree12/results.json').read_bytes())['nodes']
contact=json.loads((H/'finite_pair_ward/results.json').read_bytes())
reference=json.loads((H/'flat_reference_ward/results.json').read_bytes())
fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))];p=(1,0,0,0);data=[]
def run(ti,p,v,order):
    total=[[F() for _ in range(3)] for _ in range(2)]
    for ni,node in enumerate(nodes):
        out=pair_node(BASIS[ti],p,v,tuple(node['vector']),order);w=F(node['weight'])
        for a in range(2):
            for b in range(3):total[a][b]+=w*out[a][b]
        if ni%100==0:print(json.dumps(dict(order=order,T=ti,node=ni,cpu=time.process_time()-cpu)),flush=True)
    comb=[-total[0][i]/2+total[1][i] for i in range(3)]
    row=dict(order=order,T=ti,p=p,v=v,metric=list(map(str,total[0])),ghost=list(map(str,total[1])),
             combination=list(map(str,comb)))
    data.append(row);print(json.dumps(row),flush=True)
    return total,comb
for ti,v in fixtures:
    totals,comb=run(ti,p,v,0)
    old=next(row for row in contact['values'] if row['order']==0 and row['T']==ti)
    ref=next(row for row in reference['values'] if row['p']==list(p) and row['T']==ti)
    for i,kind in enumerate(('metric','ghost')):
        expected=sum(map(F,old[kind+'_pieces']))+F(ref[kind])
        assert totals[i][0]==expected,(ti,kind,totals[i][0],expected)
        assert totals[i][2]==0
        checks.append('flat_finite_'+str((ti,kind)))
    assert comb[1]==0 and comb[2]==0,(ti,comb)
    checks.append('flat_common_log_Ward_'+str(ti))
def basis(ti,p,v):
    T=s.Matrix(4,4,BASIS[ti]);p=s.Matrix(p);v=s.Matrix(v);p2=p.dot(p)
    return [p2*(p.T*T*v)[0],(p.T*T*p)[0]*p.dot(v),p2*s.trace(T)*p.dot(v)]
rows=[];values=[]
for ti,v in fixtures:
    _,comb=run(ti,p,v,1);rows.append(basis(ti,p,v));values.append(list(map(s.Rational,comb)))
fits=s.Matrix(rows).inv()*s.Matrix(values)
np=(1,2,-1,1);nv=(2,-1,1,3);_,holdout=run(4,np,nv,1)
pred=s.Matrix([basis(4,np,nv)])*fits
for j in range(3):
    assert s.Rational(holdout[j])==pred[j],(j,holdout[j],pred[j])
    checks.append('nonaxis_firstK_LogPower'+str(j))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='RAW_FIRST_K_FOURIER_PAIR_MEASURED',checks=len(checks),
 check_names=checks,values=data,first_K_coefficients_by_invariant=[[str(fits[i,j]) for j in range(3)] for i in range(3)],
 invariant_basis=['p2 Tpv','pTp pv','p2 trT pv'],log_basis=['1','FourierLog','FourierLog^2'],
 cpu_seconds=time.process_time()-cpu,full_Q2=False,
 scope='Metric and ghost raw pairs; source/tadpole/W/higher arities omitted explicitly; Euclidean formal symbol')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('values','check_names')}))
