"""Audit received Fourier reasoning against Schwinger formula and exact controls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time
import sympy as s
from curved_harmonic_fourier_engine import coefficients,L
H=Path(__file__).resolve().parent; D=H/'fourier_review_audit';D.mkdir(exist_ok=True)
source=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/6c210ea9-cc1e-4c09-a039-3d469ae4f090_delivery.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v):
 p=D/name;assert not p.exists(),p
 b=v.encode() if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2).encode()
 t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(source),
 tests=['Even/odd phase against Schwinger Gamma formula','Angular multiplication with both reexpanded harmonics',
        'Literal table entries against formula','Double-counted momentum regulator and cubic Gamma sign'],
 no_new_remote_call=True,no_original_edits=True))
t=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.simplify(a-b)==0,(a,b)
 checks+=1
a=s.Symbol('a'); q=s.symbols('q0:4',real=True);Q=sum(v*v for v in q)
phase=[]
# Schwinger formula: (-i)^l*pi²*2^-m * e^(aL) * Gamma(a-k)/Gamma(N-a).
# Cubic Gamma quotient is irrelevant to finite parts at log orders0,1.
for m in range(5):
 for l in range(m%2,7,2):
  k=(m-l)//2;N=(m+l+4)//2
  ratio=(1/(a*s.prod(a-j for j in range(1,k+1))) if k>=0 else s.prod(j+a for j in range(1,-k)))/s.prod(j-a for j in range(1,N))
  series=s.series(s.exp(a*L)*ratio,a,0,2).removeO()
  for ell in (0,1):
   fp=s.expand((1-a)*(s.diff(series,a) if ell else series)).coeff(a,0)
   true_over_C_i_m=s.expand(-(-s.I)**l/s.I**m*s.Rational(1,2**(m+2))*fp)
   c=coefficients(m,l,ell);code=sum(s.Rational(v.numerator,v.denominator)*L**j for j,v in enumerate(c))
   eq(true_over_C_i_m,(-1)**l*code)
   phase.append(dict(m=m,l=l,ell=ell,ratio=(-1)**l))
# Nonradial x0 multiplication, all involved Gamma factors nonsingular.
# Product decomposition x0 Hl = Hplus + z*l/(2(l+1))*H(l-1).
angular=[]
def transform(m,l,polynomial):
 k=s.Rational(m-l,2);N=s.Rational(m+l+4,2)
 return (-s.I)**l*s.pi**2*2**(-s.Integer(m))*s.gamma(-k)/s.gamma(N)*Q**k*polynomial
for m in range(1,5):
 for l in (m+2,m+4):
  hl=(q[0]+s.I*q[1])**l;lower=(q[0]+s.I*q[1])**(l-1)
  hp=q[0]*hl-Q*s.Rational(l,2*(l+1))*lower
  eq(sum(s.diff(hp,v,2) for v in q))
  lhs=s.I*s.diff(transform(m,l,hl),q[0])
  rhs=transform(m-1,l+1,hp)+s.Rational(l,2*(l+1))*transform(m-1,l-1,lower)
  eq(lhs,rhs)
  angular.append(dict(m=m,l=l,new_m_both_components=m-1))
literal={(0,4,0):s.Rational(-1,384),(0,6,0):s.Rational(1,23040),(1,1,1):s.Rational(-11,128)}
table=[]
for key,claimed in literal.items():
 c=coefficients(*key)[0];measured=s.Rational(c.numerator,c.denominator)
 assert measured!=claimed;checks+=1
 table.append(dict(m=key[0],l=key[1],ell=key[2],claimed=str(claimed),measured=str(measured)))
# The review's intermediate line uses exp(a log(4mu²/p²)) AND (p²)^(k-a).
# Momentum scaling p->t*p would then be t^(m-4a), rather than t^(m-2a).
eq(s.diff(-a*s.log(Q),q[0]),-2*a*q[0]/Q)
gamma_cubic=(s.polygamma(2,1)-(-1)**3*s.polygamma(2,1))/s.factorial(3)
eq(gamma_cubic,-s.Rational(2,3)*s.zeta(3))
reply=json.loads(source.read_bytes())
save('KIMI_RESPONSE.md',reply['result']['text'])
save('RECEIPT.json',dict(source=str(source),source_sha256=sha(source),job_id=reply['job_id'],
 execution_task_id=reply['execution_task_id'],request_id='1610f043-fce4-4d6d-b05d-d23c0080a635',
 usage=reply['result']['usage'],model=reply['result']['model'],response_sha256=sha(D/'KIMI_RESPONSE.md'),
 elapsed_seconds=reply['result']['elapsed_seconds'],cost_estimate_usd=None,new_call=False))
results=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-t,
 phase_audit=phase,angular_controls=angular,incorrect_literal_table=table,
 gamma_log_cubic=str(gamma_cubic),
 scope='Standard e^-ipx with solid harmonics: odd code phase differs; no change to engine or assembled amplitudes. Reassembly phase impact remains open.',
 nonradial_shift='m-j holds for every harmonic after reexpansion, not only radial multipliers',
 p_origin='A polynomial in p is visible for p²>0; local-in-x is not supported only at p=0',
 double_count='Intermediate review formula includes p^-2a twice; final master formula removes duplication',
 full_Q2=False,gate_changed=False)
save('results.json',results)
files=[Path(__file__),H/'curved_harmonic_fourier_engine.py',source]+list(D.iterdir())
save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in files if p.is_file()]))
print(json.dumps({k:v for k,v in results.items() if k!='phase_audit'}))
