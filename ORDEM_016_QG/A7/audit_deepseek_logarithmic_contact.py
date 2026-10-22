"""Test the full Leibniz sum, including the terms the review incorrectly drops."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'deepseek_logarithmic_contact_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    b=json.dumps(v,indent=2,ensure_ascii=False).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('AUDIT_PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 targets=['All Leibniz terms for log degrees0..6 and coefficient powers0..8',
 'Analytic regular part drops from contact','Minimal ell2,c=a3 counterexample to t<=1 truncation',
 'Profile arithmetic only; no bitensor amplitude'],
 sources=[dict(path=str(p),sha256=sha(p)) for p in (Path(__file__),D/'ANSWER.md',D/'RECEIPT.json')]))
cpu=time.process_time();a=s.Symbol('a');rho=s.Symbol('rho');count=0
def pieces(c,ell,T):
    out=[]
    for t in range(ell+1):
        diff=s.diff(c,a,ell-t).subs(a,0)-s.diff(c,a,ell-t)
        value=(1-a)*s.binomial(ell,t)*diff*s.diff(T,a,t)
        out.append(s.expand(value).coeff(a,0))
    return out
for ell in range(7):
    for m in range(9):
        c=a**m
        exact=sum(pieces(c,ell,rho/a))
        closed=-rho*(s.diff(c,a,ell+1).subs(a,0)/(ell+1)
                     +(s.diff(c,a,ell).subs(a,0) if ell else 0))
        assert s.expand(exact-closed)==0,(ell,m,exact,closed)
        assert s.expand(sum(pieces(c,ell,rho/a+1+2*a+3*a*a))-closed)==0
        count+=2
example=pieces(a**3,2,rho/a)
assert example==[-6*rho,6*rho,-2*rho]
assert sum(example[:2])!=sum(example);count+=1
assert sum(pieces(1,0,rho/a))==0;count+=1
K=s.Symbol('K')
profiles=[K/2*(-s.Rational(1,12))-5*K/4*s.Rational(1,24),
          K/2*(-s.Rational(1,16))-5*K/4*s.Rational(5,96),
          K/2*s.Rational(1,384)-5*K/4*s.Rational(1,768)]
targets=[-3*K/32,-37*K/384,-K/3072]
for got,want in zip(profiles,targets):assert s.expand(got-want)==0;count+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FORMULA_ACCEPTED_TRUNCATED_LEIBNIZ_ARGUMENT_REJECTED',
 checks=count,example_terms=list(map(str,example)),example_sum=str(sum(example)),
 t_le1_only=str(sum(example[:2])),monomial_exception='ell=0,m=0 gives0, not -rho',
 proof='For m=ell+1 sum binom(ell,t)(-1)^t/(t+1)=1/(ell+1); for m=ell>=1 sum t>=1 binom(ell,t)(-1)^t=-1; regular terms vanish',
 profile_coefficients=list(map(str,profiles)),cpu_seconds=time.process_time()-cpu,full_Q2=False,
 scope='Algebraic finite-part identity conditional on simple-pole meromorphic base; not distributional existence or full curved amplitude')
put('audit_results.json',result)
print(json.dumps(result,ensure_ascii=False))
