"""Trace-channel restriction of the new covariant ghost residue."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HOM=Path(__file__).resolve().parent;D=HOM/'ghost_conformal_curvature';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
 parent_sha256=sha(HOM/'ghost_minimal_heat/DERIVACAO.md'),
 target='Restriction h=f*g of integrated ghost residue; exact Hessian and curvature, not full hh tensor',
 conventions='Same fixed background; compact f; formal Euclidean auxiliary heat residue',
 assumptions_inherited=True,gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[]
def check(n,e):
 assert all(s.expand(v)==0 for v in e) if isinstance(e,s.MatrixBase) else s.expand(e)==0,(n,e)
 checks.append(n)
K,f=s.symbols('K f');v=s.Matrix(s.symbols('v0:4'));ss=s.symbols('u0:10');S=s.zeros(4)
for a,(i,j) in enumerate((i,j) for i in range(4) for j in range(i,4)):S[i,j]=S[j,i]=ss[a]
I=s.eye(4);e=[I[:,i] for i in range(4)]
A=[v[m]*I-v*e[m].T for m in range(4)];B=-S;box=s.trace(S);DD=B-box*I
F={(m,n):-S[:,m]*e[n].T+S[:,n]*e[m].T for m in range(4) for n in range(4)}
Omega={(m,n):K*(e[m]*e[n].T-e[n]*e[m].T) for m in range(4) for n in range(4)}
AA=sum(s.trace(a*a) for a in A)
FF=sum(s.trace(a*a) for a in F.values())
OC=sum(s.trace(Omega[m,n]*(A[m]*A[n]-A[n]*A[m])) for m in range(4) for n in range(4))
check('connection_norm',AA-3*v.dot(v))
check('endomorphism_square',s.trace(DD*DD)-s.trace(S*S)-6*box**2)
check('connection_curl_square',FF-2*s.trace(S*S)+2*box**2)
check('background_curvature_commutator',OC+6*K*v.dot(v))
local=s.expand(5*K*(-s.trace(f*I*B)-AA/4)+s.trace(DD*DD)/8+FF/48+OC/24)
check('pointwise_trace_restriction',local-(s.trace(S*S)/6+s.Rational(17,24)*box**2+5*K*f*box-4*K*v.dot(v)))

# Integrated identities, proved in the written companion: integral f box f
# = -integral |df|²; integral |Hess f|²=integral(box f)²-3K integral|df|².
bb,vv,hh,fb=s.symbols('bb vv hh fb')
formal=hh/6+s.Rational(17,24)*bb+5*K*fb-4*K*vv
integrated=s.expand(formal.subs({hh:bb-3*K*vv,fb:-vv}))
check('integrated_Bochner_reduction',integrated-s.Rational(7,8)*bb+s.Rational(19,2)*K*vv)
dd=lambda a,b:s.Integer(a==b)
R=lambda a,b,m,n:K*(dd(a,m)*dd(b,n)-dd(a,n)*dd(b,m))
for a in range(4):
 for b in range(4):
  check(f'Bochner_Ricci_{a}_{b}',sum(R(m,a,m,b) for m in range(4))-3*K*dd(a,b))
old=json.loads((HOM/'ghost_bubble/results.json').read_bytes())
c=list(map(s.Rational,old['coefficients_over_angular_factor']))
check('flat_trace_bilinear_matches_prior_bubble',sum(a*b for a,b in zip(c,[4,16,8,1,1]))-s.Rational(7,4))
negative={'drop_connection_Omega0_commutator':str(-K*vv/4),
 'drop_Bochner_commutator':str(-K*vv/2),
 'assume_ghost_trace_channel_zero':str(s.Rational(7,4))}
assert all(s.sympify(v)!=0 for v in negative.values())
result=dict(statute='DERIVED_CONDITIONAL_GHOST_LOG_TRACE_CHANNEL_WITH_EXACT_CAS',checks=len(checks),check_names=checks,
 pointwise='tr a4_2=(Hess f)^2/6+17(box f)^2/24+5K f box f-4K(df)^2',
 integrated='integral[7(box f)^2/8-19K(df)^2/2]',
 trace_Hessian='(7/4)box^2+19K box',
 K2_trace_constant_term=0,negative_controls=negative,
 assumptions=['Parent local heat residue/minimalization conditions',
 'Compact support/integrated divergences; Bochner identity on Ric=3Kg'],
 finite_causal_Ward=False,full_metric_tensor=False,full_Q2=False,gate_changed=False,
 wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(D/'results.json',result)
files=[Path(__file__),D/'PRE_REGISTER.json',D/'results.json']
new(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
