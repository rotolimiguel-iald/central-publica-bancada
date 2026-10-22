"""Exact finite counterexamples for the received DeepSeek WZ review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,time,uuid
import sympy as s
HERE=Path(__file__).resolve().parent; DEST=HERE/'odd_bracket_review';DEST.mkdir(exist_ok=True)
def new(p,obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(data)
    assert q.read_bytes()==data;q.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Odd antibracket signs and a counterexample to the claimed arbitrary-S Jacobi identity',
    even_pair_coordinate='x',odd_pair_coordinate='theta',odd_spectators=['c','d'],
    controls=['wrong even Poisson antisymmetry','S0 in place of full S in Jacobi','antighost sign'],
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
start=time.process_time();wall=time.perf_counter();x,b=s.symbols('x b')
def clean(a):return {m:s.expand(v) for m,v in a.items() if s.expand(v)!=0}
def add(a,b):
    r=dict(a)
    for k,v in b.items():r[k]=r.get(k,0)+v
    return clean(r)
def scale(a,c):return clean({m:c*v for m,v in a.items()})
def mul(a,b):
    r={}
    for m,v in a.items():
        for n,w in b.items():
            if m&n:continue
            swaps=sum((n&((1<<i)-1)).bit_count() for i in range(3) if m&(1<<i))
            r[m|n]=r.get(m|n,0)+(-1)**swaps*v*w
    return clean(r)
def dx(a):return clean({m:s.diff(v,x) for m,v in a.items()})
def odd_derivative(a,index,right=False):
    bit=1<<index;r={}
    for m,v in a.items():
        if not m&bit:continue
        n=((m>>(index+1)) if right else (m&(bit-1))).bit_count()
        r[m^bit]=(-1)**n*v
    return clean(r)
def bracket(a,b):return add(mul(dx(a),odd_derivative(b,0)),
    scale(mul(odd_derivative(a,0,right=True),dx(b)),-1))
def parity(a):
    p={m.bit_count()%2 for m in a};assert len(p)==1
    return next(iter(p))
one={0:s.Integer(1)};X={0:x};theta={1:s.Integer(1)};c={2:s.Integer(1)};d={4:s.Integer(1)}
basis=[one,X,theta,c,d,mul(theta,c),mul(X,mul(theta,c)),mul(theta,d)]
assert bracket(X,theta)==one and bracket(theta,X)==scale(one,-1)
count=2
for f in basis:
    for g in basis:
        sign=-(-1)**((parity(f)+1)*(parity(g)+1))
        assert bracket(f,g)==scale(bracket(g,f),sign)
        count+=1
        for h in basis:
            rhs=add(bracket(f,bracket(g,h)),scale(bracket(g,bracket(f,h)),
                -(-1)**((parity(f)+1)*(parity(g)+1))))
            assert bracket(bracket(f,g),h)==rhs
            count+=1
S=mul(theta,add(mul(X,c),d));S0=X
ss=bracket(S,S)
assert ss==scale(mul(theta,mul(c,d)),2)
assert bracket(S,ss)=={}
assert bracket(S0,S0)=={}
assert bracket(S0,ss)==scale(mul(c,d),2)
count+=4
# The provider's unshifted parity rule would force (S,S)=0 for this even S.
assert ss!=scale(ss,-1)
# Pair (barc,B) with barc odd, B even, canonical (barc,B)=1 is
# minus the bracket for coordinates (x=B,theta=barc).
ghost_action={0:-x*b}
ghost_generated=scale(bracket(ghost_action,theta),-1)
assert ghost_generated=={0:b} and ghost_generated!={0:-b}
count+=1
new(DEST/'results.json',dict(at=datetime.now(timezone.utc).isoformat(),
    status='EXACT_ODD_BRACKET_REVIEW_PASSED',checks=count,negative_controls=3,
    S='theta*(x*c+d)',S0='x',self_bracket='2 theta c d',
    full_Jacobi='(S,(S,S))=0',false_provider_identity='(S0,(S,S))=2 c d != 0',
    antighost_with_provider_convention='(-B*b,barc)=+b, not -b',
    quantum_anomaly_computed=False,cpu_seconds=time.process_time()-start,
    wall_seconds=time.perf_counter()-wall))
print(json.dumps(dict(checks=count,negative_controls=3,cpu_seconds=time.process_time()-start)))
