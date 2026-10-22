"""Independent geometric jets and non-fit polarizations for the curved source."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time
import sympy as s
import curved_source_jet_engine as e
H=Path(__file__).resolve().parent;O=H/'curved_source_jet_audit';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=O/n;assert not p.exists(),p
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(H/'curved_source_jet_engine.py'),
    targets=['derive parallel transport by integrating the normal-coordinate connection',
             'metric compatibility and reversal', 'first Y jets before endpoint specialization',
             'all 40 axial polarizations plus dense nonaxis outside fit',
             'negative control omitting transverse transport derivatives'],
    restriction='First order K in Euclidean normal chart, geometric singular kernel only'))
t=time.process_time();checks=[];neg=[]
def ck(n,v):
    assert s.expand(v)==0,(n,v);checks.append(n)
x=e.x;y=s.symbols('y0:4');u=s.symbols('u');delta=e.d
X=s.Matrix(x);Y=s.Matrix(y);D=X-Y;S=X+Y;I=s.eye(4)
gX=-(I*X.dot(X)-X*X.T)/3;gY=-(I*Y.dot(Y)-Y*Y.T)/3
def conn(a,m,b,Z):return -(delta(a,b)*Z[m]+delta(a,m)*Z[b]-2*delta(m,b)*Z[a])/3
P=s.Matrix(4,4,lambda a,b:s.expand(-s.integrate(sum(conn(a,m,b,Y+u*D)*D[m] for m in range(4)),(u,0,1))))
Pclaim=(I*(X.dot(X)-Y.dot(Y))+D*S.T-2*S*D.T)/6
for a in range(4):
 for b in range(4):
    ck(f'P_from_connection_{a}_{b}',P[a,b]-Pclaim[a,b])
    ck(f'metric_transport_{a}_{b}',(P.T+P+gX-gY)[a,b])
    reverse=P[b,a].xreplace(dict(zip(x,y))|dict(zip(y,x)))
    # Inverse is a matrix, not transpose, between coordinate frames.
    rev=P[a,b].xreplace(dict(zip(x,y))|dict(zip(y,x)))
    ck(f'inverse_transport_{a}_{b}',P[a,b]+rev)
    for m in range(4):
     for n in range(4):
      R=s.diff(conn(a,n,b,X),x[m])-s.diff(conn(a,m,b,X),x[n])
      ck(f'curvature_{a}_{b}_{m}_{n}',R-(delta(a,m)*delta(b,n)-delta(a,n)*delta(b,m)))
zeroY=dict.fromkeys(y,0); cross=gX+P
z0=X.dot(X)
for a in range(4):
 for c in range(4):
    ck(f'lower_cross_{a}_{c}',cross[a,c].subs(zeroY)-e.lower_cross(a,c).subs(e.z,z0))
    for j in range(4):
        ck(f'cross_y_{a}_{c}_{j}',s.diff(cross[a,c],y[j]).subs(zeroY)-e.lower_cross_y(a,c,j))
for a in range(4):
 for b in range(a,4):
  for c in range(4):
   for d in range(c,4):
    full=(cross[a,c]*delta(b,d)+delta(a,c)*cross[b,d]+cross[a,d]*delta(b,c)+delta(a,d)*cross[b,c]
          -gX[a,b]*delta(c,d)-delta(a,b)*gY[c,d])/2
    ck(f'spin_value_{a}{b}{c}{d}',full.subs(zeroY)-e.spin1(a,b,c,d).subs(e.z,z0))
    for j in range(4):ck(f'spin_y_{a}{b}{c}{d}_{j}',s.diff(full,y[j]).subs(zeroY)-e.spin1_y(a,b,c,d,j))
# First Y and mixed X/Y jets of the quartic distance correction vanish at Y=0.
distance4=-(X.dot(X)*Y.dot(Y)-X.dot(Y)**2)/3
for j in range(4):
    ck(f'distance_firstY_{j}',s.diff(distance4,y[j]).subs(zeroY))
    for i in range(4):ck(f'distance_mixedXY_{i}_{j}',s.diff(distance4,y[j],x[i]).subs(zeroY))
axes=[I[:,i] for i in range(4)];p=axes[0]
for a in range(4):
 for b in range(a,4):
  T=s.zeros(4);T[a,b]=T[b,a]=1
  for j,v in enumerate(axes):
    expected=-s.Rational(20,3)*(v.T*T*p)[0]+s.Rational(5,3)*s.trace(T)*p.dot(v)
    ck(f'curved_basis_{a}_{b}_{j}',e.local_log_profile(T,v,p,1)-expected)
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
p=s.Matrix([1,2,-1,1]);v=s.Matrix([2,-1,1,3])
expected=-s.Rational(20,3)*(v.T*T*p)[0]+s.Rational(5,3)*s.trace(T)*p.dot(v)
ck('dense_nonaxis',e.local_log_profile(T,v,p,1)-expected)
ck('dense_flat',e.local_log_profile(T,v,p,0)+s.Rational(3,4)*p.dot(p)*(v.T*T*p)[0]
   -s.Rational(1,2)*(p.T*T*p)[0]*p.dot(v))
# Mutation is local to this process. Excluding both endpoint connection jets
# would silently replace the bitensor by a radial scalar profile.
oldg=e.gjet;oldcross=e.lower_cross_y
e.lower_cross_y=lambda *args:s.Integer(0)
e.hjet.cache_clear()
def nog(order,m,n,yi,xi=-1):
    val=oldg(order,m,n,yi,xi)
    if order:
        corr=oldcross(m,n,yi)/e.z
        val-=corr if xi<0 else e.dx(corr,xi)
    return s.expand(val)
e.gjet=nog
T=s.zeros(4);T[0,1]=T[1,0]=1;p=axes[0];v=axes[1]
mut=s.expand(e.local_log_profile(T,v,p,1)+s.Rational(20,3))
assert mut!=0;neg.append(dict(name='transverse_transport_omitted',defect=str(mut)))
result=dict(status='PASS_GEOMETRIC_JETS_AND_NONFIT_CONTROLS',checks=len(checks),
 check_names=checks,negative_controls=neg,cpu_seconds=time.process_time()-t,
 statement='The singular first-K angular profile is -10K/3 times the trace-reversed gauge tensor',
 full_renormalized_amplitude=False,curved_Ward_anomaly=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
 [Path(__file__),H/'curved_source_jet_engine.py',O/'PRE_REGISTER.json',O/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False),flush=True)
