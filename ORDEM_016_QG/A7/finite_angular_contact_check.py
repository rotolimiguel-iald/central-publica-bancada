"""Exact scalar-contact table and independent spherical Laurent audit."""
from pathlib import Path
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import time
import uuid
import sympy as s
from finite_angular_contact_engine import coefficient, projector_polynomial, node_weights
from finite_harmonic_extension_engine_v2 import radial_inverse
from logarithmic_contact_engine import A, Q, differentiated
from curved_source_jet_engine import x, z

H = Path(__file__).resolve().parent
D = H/'finite_angular_contact'
D.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name, obj):
    p=D/name
    assert not p.exists(), p
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b)
    assert t.read_bytes()==b
    t.replace(p)

sources=[Path(__file__),H/'finite_angular_contact_engine.py',
         H/'finite_harmonic_extension_engine_v2.py',H/'logarithmic_contact_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='m0..4, l<=m same parity, ell0..2 harmonic-reference contact table',
    independent_route='S3 Taylor moments and explicit Laurent finite part, not x-delta multiplication',
    exclusions=['full graph Ward identity','smooth W omitted as zero','change of extension'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
started=time.process_time()
checks=[]
def ck(name, value):
    assert s.expand(value)==0,(name,value)
    checks.append(name)

def compositions(n, d=4):
    if d==1:
        yield(n,)
        return
    for k in range(n+1):
        for rest in compositions(n-k,d-1): yield(k,)+rest

@lru_cache(None)
def moment(powers):
    if any(n%2 for n in powers):return s.Integer(0)
    h=sum(powers)//2
    return s.prod(s.factorial2(n-1) for n in powers)/(2**h*s.factorial(h+1))

def average(poly):
    return s.expand(sum(c*moment(p) for p,c in s.Poly(s.expand(poly),*x).terms()))

@lru_cache(None)
def sphere_residue(n, powers):
    degree=2*n-4-sum(powers)
    if degree<0:return s.Integer(0)
    return s.expand(-s.Rational(1,4)*sum(
        (-1)**degree*moment(tuple(a+b for a,b in zip(powers,k)))
        *s.prod(Q[i]**k[i]/s.factorial(k[i]) for i in range(4))
        for k in compositions(degree)))

def direct_contact(base, ell, word):
    out=0
    for (n,powers),c in differentiated(base,word,(1,1,1,1)).items():
        res=sphere_residue(n,powers)
        for t in range(ell+1):
            k=ell-t
            difference=s.diff(c,A,k).subs(A,0)-s.diff(c,A,k)
            expr=(1-A)*s.binomial(ell,t)*difference*s.diff(res/A,A,t)
            out+=s.expand(expr).coeff(A,0)
    return s.expand(out)

table=[]
q2=sum(q*q for q in Q)
for m in range(5):
    for l in range(m%2,m+1,2):
        b=(m+4-l)//2
        harmonic=s.expand((x[0]+s.I*x[1])**l)
        for ell in range(3):
            value=coefficient(m,l,ell)
            inv=radial_inverse(l,b,ell)
            direct=0
            for powers,c in s.Poly(harmonic,*x).terms():
                word=tuple(i for i,n in enumerate(powers) for _ in range(n))
                direct+=c*sum(v*direct_contact(b,r,word) for r,v in enumerate(inv))
            target=value*q2**((m-l)//2)*(Q[0]+s.I*Q[1])**l
            ck(f'spherical_Laurent_{m}_{l}_{ell}',direct-target)
            table.append(dict(m=m,l=l,ell=ell,coefficient=str(value)))
    for ell in range(3):
        polynomial=projector_polynomial(m,ell)
        sphere=polynomial.subs(z,1)
        for l in range(m%2,7,2):
            # Two harmonic families ensure axes and imaginary/offdiagonal terms.
            for pair in [(0,1),(1,3)]:
                h=s.expand((x[pair[0]]+s.I*x[pair[1]])**l)
                expected=(coefficient(m,l,ell)*q2**((m-l)//2)
                          *(Q[pair[0]]+s.I*Q[pair[1]])**l if l<=m else 0)
                ck(f'zonal_{m}_{ell}_{l}_{pair}',average(sphere*h)-expected)
        for node in [(1,0,0,0),(1,2,-1,1),(2,-3,1,2)]:
            weights=node_weights(m,ell,node)
            from_weights=sum(v.numerator*s.prod(Q[i] for i in w)/s.Integer(v.denominator)
                             for w,v in weights.items())
            expected=polynomial.subs({z:sum(a*a for a in node),**dict(zip(x,node))})
            ck(f'nonunit_node_{m}_{ell}_{node}',from_weights-expected)

ck('degree_minus5',coefficient(1,1,0)-s.Rational(1,32))
ck('degree_minus5_log',coefficient(1,1,1)-s.Rational(3,64))
ck('degree_minus6',coefficient(2,2,0)+s.Rational(5,576))
ck('degree_minus6_log',coefficient(2,2,1)+s.Rational(49,3456))
# Explicit negative controls for logs and odd-distribution orientation.
assert coefficient(1,1,1)!=coefficient(1,1,0)
assert -coefficient(1,1,0)!=coefficient(1,1,0)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='EXACT_COMPONENT_VERIFIED',
    checks=len(checks),check_names=checks,negative_controls=2,table=table,
    normalization='local difference / C, not graph normalization',
    cpu_seconds=time.process_time()-started,full_Q2=False,gate_changed=False,
    use='multiply angular kernel by z² projector polynomial, average, then ordered test jets with (-1)^m; no repeated Taylor factorial')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('check_names',)},ensure_ascii=False))
