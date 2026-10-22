"""Independent conformal EH contraction, Wick bookkeeping and cutoff Euler term."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,time
import sympy as s
from metric_principal_vertices import I,clear_caches
from metric_quartic_vertices import eh_quartic_32k
H=Path(__file__).resolve().parent;D=H/'finite_smooth_wick_trace';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[Path(__file__),H/'metric_quartic_vertices.py',H/'metric_principal_vertices.py',
 H/'linear_normalization_v2/DERIVACAO_CONTATO.md',H/'finite_smooth_tadpole_derivative_jets/DERIVACAO.md',
 H/'smooth_reference_transport_audit/results.json']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Actual conformal EH Wick contraction through quartic and derivative-cutoff completion',
 scope='h=u*delta, Euclidean contractions; restriction of metric action, not a scalar substitute',
 fixed='V3=3/(4k)*u*(du)^2, V4=-3/(4k)*u^2*(du)^2 from existing conformal action',
 covariance='W00=a, W0i=b_i, Wij=c_ij; symmetric smooth jet, no bisolution assumed',
 method='Independent functional second derivative vs polarized tensor vertex; symbolic Euler variation with cutoff',
 T1='Conjugation transports an existing T1; no new prescription fixed',
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1
u=s.Symbol('u');v=s.symbols('v0:4');k=s.Symbol('k',nonzero=True);a=s.Symbol('a');b=s.symbols('b0:4')
cs=s.symbols('c0:10');labels=[(i,j) for i in range(4) for j in range(i,4)]
c=s.Matrix(4,4,lambda i,j:cs[labels.index(tuple(sorted((i,j))))]);trc=s.trace(c)
z=(u,)+v;W=s.zeros(5);W[0,0]=a
for i in range(4):
 W[0,i+1]=W[i+1,0]=b[i]
 for j in range(4):W[i+1,j+1]=c[i,j]
def contract(f):return s.expand(sum(W[i,j]*s.diff(f,z[i],z[j])/2 for i in range(5) for j in range(5)))
v2=sum(vi**2 for vi in v);V3=3*u*v2/(4*k);V4=-3*u**2*v2/(4*k)
linear=3*(2*sum(b[i]*v[i] for i in range(4))+trc*u)/(4*k)
quadratic=-3*(a*v2+4*u*sum(b[i]*v[i] for i in range(4))+trc*u**2)/(4*k)
eq(contract(V3),linear);eq(contract(V4),quadratic)
# Fully symbolic four-profile Hessian of the independent density.
f,g=s.symbols('f g');df=s.symbols('f0:4');dg=s.symbols('g0:4');t,r=s.symbols('t r')
hessian=s.diff(quadratic.subs(dict(zip(z,(t*f+r*g,)+tuple(t*df[i]+r*dg[i] for i in range(4))))),t,r)
expected=-3*(2*a*sum(df[i]*dg[i] for i in range(4))+
             4*sum(b[i]*(f*dg[i]+g*df[i]) for i in range(4))+2*trc*f*g)/(4*k)
eq(hessian,expected)
# Fourier polarized tensor vertex versus conformal formula, all six pair placements.
fixtures=[((1,2,-1,1),(-2,-3,2,-1),(0,1,0,0),(1,0,-1,0)),
          ((2,-1,0,3),(1,2,0,-1),(1,0,0,0),(0,1,1,0)),
          ((1,0,0,0),(-1,0,0,0),(0,0,0,0),(0,0,0,0))]
fourier=[]
for momenta in fixtures:
 raw=eh_quartic_32k(*[(I,p) for p in momenta])
 total=sum(sum(momenta[i][j]*momenta[l][j] for j in range(4)) for i in range(4) for l in range(i+1,4))
 eq(raw,96*total)
 # W=(U tensor V + V tensor U)/2, U=e^(irx),V=e^(isx).
 p,q,rp,sp=momenta
 replace={a:1,f:1,g:1,k:1}
 replace.update({df[i]:s.I*p[i] for i in range(4)});replace.update({dg[i]:s.I*q[i] for i in range(4)})
 replace.update({b[i]:s.I*(rp[i]+sp[i])/2 for i in range(4)})
 replace.update({cs[n]:-(rp[i]*sp[j]+sp[i]*rp[j])/2 for n,(i,j) in enumerate(labels)})
 # Multiply by 4k from the propagator; retain common hbar/(4pi^2).
 value=s.expand(4*hessian.subs(replace));eq(value,s.Rational(raw,16))
 fourier.append(dict(momenta=momenta,contracted_tensor=str(s.Rational(raw,16)),conformal_Wick_hessian=str(value)))
clear_caches()
# All4 coordinates and arbitrary smooth coefficient fields, not just an axial profile.
x=s.symbols('x0:4');uf=s.Function('u')(*x);af=s.Function('a')(*x);ch=s.Function('chi')(*x)
bf=[s.Function('b'+str(i))(*x) for i in range(4)];cf=s.Function('c')(*x)
grad=[s.diff(uf,xi) for xi in x]
lag=ch*(af*sum(vi**2 for vi in grad)+4*uf*sum(bf[i]*grad[i] for i in range(4))+cf*uf**2)
euler=s.diff(lag,uf)-sum(s.diff(s.diff(lag,grad[i]),x[i]) for i in range(4))
correct=-2*sum(s.diff(ch*af*grad[i],x[i]) for i in range(4))-4*uf*sum(s.diff(ch*bf[i],x[i]) for i in range(4))+2*ch*cf*uf
eq(euler,correct)
constant_cutoff=s.expand(correct.subs(ch,1).doit())
defect=s.expand(correct-ch*constant_cutoff)
boundary=-2*sum(s.diff(ch,x[i])*(af*grad[i]+2*bf[i]*uf) for i in range(4))
eq(defect,boundary)
negative=s.expand(boundary.subs({ch:1+x[0],af:1+x[0],uf:x[0]**2,bf[0]:s.Rational(1,2),bf[1]:0,bf[2]:0,bf[3]:0},simultaneous=True).doit())
eq(negative,-6*x[0]**2-4*x[0]);assert negative!=0;checks+=1
# Symmetry of W gives b=da/2 on diagonal. It does not fix c=tr W11.
diagonal=s.expand(correct.subs({bf[i]:s.diff(af,x[i])/2 for i in range(4)}).doit())
eq(diagonal,-2*sum(s.diff(ch*af*grad[i],x[i]) for i in range(4))-
   2*uf*sum(s.diff(ch*s.diff(af,x[i]),x[i]) for i in range(4))+2*ch*cf*uf)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 contracted_V3=str(linear),contracted_V4=str(quadratic),hessian=str(expected),fourier_controls=fourier,
 euler='For density chi[a(du)^2+4u b.du+c u^2]: -2div(chi a du)-4u div(chi b)+2chi c u',
 omitted_cutoff_control=str(negative),common_physical_factor='Contracted V3/V4 times hbar*4k/(4pi^2)',
 T1_selected=False,full_Q2=False,gate_changed=False)
save('results.json',result);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
