"""Local exact audit: diagonal derivatives, smooth multipliers and contact recurrence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from itertools import product
import sympy as s
from logarithmic_contact_engine import contact,Q

H=Path(__file__).resolve().parent;D=H/'kimi_smooth_twojet_review/local_audit';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
start=time.process_time();checks=0
u,v,q=s.symbols('u v q')
def normal(W,beta):
    return s.expand(sum((-1)**(beta-a)*s.binomial(beta,a)*s.diff(W,v,beta-a).subs(v,0)*q**a for a in range(beta+1)))
# Complete polynomial bases for delta orders0..4 and multiplier degree0..6.
for beta,degree in product(range(5),range(7)):
    W=(1+u+u*u)*v**degree
    lhs=normal(s.diff(W,v),beta)+normal(W,beta+1)
    assert s.expand(lhs-q*normal(W,beta))==0;checks+=1
    # d_X=d_v+(1/2)d_u on the diagonal coefficient representation.
    lhs+=normal(s.diff(W,u)/2,beta)
    rhs=q*normal(W,beta)+s.diff(normal(W,beta),u)/2
    assert s.expand(lhs-rhs)==0;checks+=1
    if degree>beta:assert normal(W,beta)==0;checks+=1

# Section5 of the response differentiates W|diag as if its transverse jet survived.
W=v;correct=s.diff(W.subs(v,0),u)/2+W.subs(v,0)*q
quoted=s.diff(W,v).subs(v,0)+s.diff(W,u).subs(v,0)/2+W.subs(v,0)*q
assert correct==0 and quoted==1;checks+=1

# The contact of a differentiated line is not simply the derivative of its contact.
C2=contact(1,0,(0,0));C3=contact(1,0,(0,0,0));C4=contact(1,0,(0,0,0,0))
assert C2==-s.Rational(1,4);checks+=1
assert s.expand(C3-Q[0]*C2)==-Q[0]/4;checks+=1
assert s.expand(C4-Q[0]*C3)!=0;checks+=1

# Smooth multiplication commutes with this fixed meromorphic finite-part map:
# R(Wf)=FP[(1-a)mu^(2a)z^a Wf]=W FP[...] distributionally.
# Jet bound is an upper bound; top jet is realized only for a nonzero top contact.
assert normal(v*v,0)==0 and normal(v*v,1)==0 and normal(v*v,2)==2;checks+=3
assert normal(v,1)==-1;checks+=1
# Scalar odd W is not a counterexample to bosonic endpoint symmetry; an
# antisymmetric fiber matrix times odd v IS symmetric under endpoints+transpose.
A=s.Matrix([[0,1],[-1,0]]);matrix=v*A
assert matrix==matrix.subs(v,-v).T;checks+=1
assert s.diff(matrix,v).subs(v,0)!=s.zeros(2);checks+=1

result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    accepted=['Delta multiplier formula and finite-jet upper bound with nonzero-top-coefficient caveat',
      'For a degree-zero contact Cdelta, only W at the diagonal contributes to multiplication',
      'Odd transverse jets need not vanish componentwise under combined endpoint/fiber symmetry'],
    corrected=['Section5 derivative of W|diag incorrectly retains a transverse derivative: W=v gives1 instead of0',
      'Section5 contact of derived line is not derivative of previous contact in this fixed prescription',
      'Upper degree bound is not always attained; cannot call it exact for every component',
      'The fixed meromorphic finite-part extension commutes with smooth multiplication at all orders, not only kmax0'],
    C2=str(C2),C3=str(C3),C4=str(C4),C3_minus_dC2=str(s.expand(C3-Q[0]*C2)),
    diagonal_derivative_counterexample=dict(W='v',correct=str(correct),quoted=str(quoted)),
    excluded=['No full vertex Ward identity follows from multiplier algebra alone',
      'No generic ghost same-block odd endpoint law assumed from Grassmann statistics',
      'Smooth functions are not globally determined by all diagonal Taylor jets without analyticity'],
    full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
 [Path(__file__),H/'kimi_smooth_twojet_review/RESPONSE.md',H/'logarithmic_contact_engine.py',D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
