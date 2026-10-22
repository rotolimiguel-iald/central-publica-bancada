"""One-loop linear local logarithm from actual cubic metric/ghost vertices."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
from fractions import Fraction as F
import hashlib,json
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber
from position_metric_bubble_engine import BASIS,vertex_data
from position_metric_second_curvature_engine_v2 import potential
from ghost_direct_position_engine import vertex as ghost_vertex
H=Path(__file__).resolve().parent;D=H/'linear_curvature_tadpole';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='Cubic metric and ghost trace; coefficient of K²trh in Gamma1; no Ward tuning',
    normalization='Metric -W2*mixed*S/8 + Wpot*a1*S/8; ghost +W2*mixed, Dghost=-Q',full_Q2=False))
cpu=process_time();checks=0
def check(a,b=0):
    global checks
    assert a==b,(a,b);checks+=1
fm=metric_fiber();mc={k:M*fm['S0'] for k,M in fm['mixed'].items()};m0=fm['a1']*fm['S0']
I=s.eye(4);E=3*I;om={}
for i in range(4):
    for j in range(4):
        M=s.zeros(4)
        if i!=j:M[i,j]=1;M[j,i]=-1
        om[i,j]=M
a1=5*I;om2=sum((v*v for v in om.values()),s.zeros(4));a2=E*E/2+2*E+s.Rational(29,15)*I+om2/12
xx={};gc={}
for i in range(4):
    for j in range(4):
        xx[i,j]=(E/2+s.Rational(29,30)*I)*int(i==j)+om[i,j]*a1/2
        xx[i,j]+=sum((om[i,k]*om[j,k]+om[j,k]*om[i,k] for k in range(4)),s.zeros(4))/12
for i in range(4):
    for j in range(4):gc[i,j]=a2*int(i==j)/2-xx[j,i]
check(sum((gc[i,i] for i in range(4)),s.zeros(4)),E*a1)
values=[]
for ai,A in enumerate(BASIS):
    W2,_,_=vertex_data(A);W0=potential(A);V2,_=ghost_vertex(A)
    md=s.S.Zero;mp=s.S.Zero;gg=s.S.Zero
    for r,row in enumerate(W2):
        for c,v in row.items():md-=s.Rational(v)*mc[(r//10-1,c//10-1)][r%10,c%10]/8
    for r,row in enumerate(W0):
        for c,v in row.items():mp+=s.Rational(v)*m0[r,c]/8
    for r,row in enumerate(V2):
        for c,v in row.items():gg+=s.Rational(v)*gc[(r//4-1,c//4-1)][r%4,c%4]
    values.append(dict(a=ai,trace=sum(A[4*i+i] for i in range(4)),metric_derivative=str(md),metric_potential=str(mp),ghost=str(gg),total=str(md+mp+gg)))
coeff=s.Rational(values[0]['total']);metric=s.Rational(values[0]['metric_derivative'])+s.Rational(values[0]['metric_potential']);ghost=s.Rational(values[0]['ghost'])
for v in values:
    check(s.Rational(v['total']),coeff*v['trace'])
    check(s.Rational(v['metric_derivative'])+s.Rational(v['metric_potential']),metric*v['trace'])
    check(s.Rational(v['ghost']),ghost*v['trace'])
before=list(map(s.Rational,json.loads((H/'second_curvature_ward_v2/results.json').read_bytes())['sum']))
after=[before[0]+coeff,before[1]-coeff]
fresh(D/'results.json',dict(statute='MEASURE_LINEAR_LOG_TADPOLE_AND_QUADRATIC_WARD',checks=checks,values=values,
    metric_coefficient=str(metric),ghost_coefficient=str(ghost),total_coefficient=str(coeff),
    density='hbar*A0*K²*coefficient*trh',gauge_action='coefficient*K²*(Gv-g divv)',
    ward_before=list(map(str,before)),ward_after=list(map(str,after)),cpu_seconds=process_time()-cpu,full_Q2=False))
files=[Path(__file__),H/'metric_coincident_jet_engine_v2.py',H/'ghost_direct_position_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,metric=str(metric),ghost=str(ghost),total=str(coeff),ward_after=list(map(str,after)),cpu=process_time()-cpu)))
