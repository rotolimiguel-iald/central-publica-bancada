"""Graded local identity for a quadratic-antifield Koszul-Tate primitive.

Convention delta(u)=E, delta(c)=0 is explicit. This does not identify E with
the fully gauge-fixed BV derivative, which also contains the b sector.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'antifield_quadratic_primitive';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    b=json.dumps(o,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='delta(1/2 u_i B_ij c du_j)+1/2 d(u_i B_ij c E_j)=u_i B_ij(c dE_j+1/2 dc E_j)',
    assumptions='B constant symmetric, u and c odd, E even, delta u=E, delta c=delta E=0',
    scope='Local jet algebra modulo displayed divergence; compact support removes integral boundary term only'))
start,cpu=perf_counter(),process_time()
E=s.symbols('E0:2');dE=s.symbols('dE0:2');b00,b01,b11=s.symbols('b00 b01 b11')
# Odd variables u0,u1,du0,du1,c,dc.
def clean(a):return {k:s.expand(v) for k,v in a.items() if s.expand(v)!=0}
def add(*args):
    out={}
    for a in args:
        for k,v in a.items():out[k]=out.get(k,0)+v
    return clean(out)
def scale(a,v):return clean({k:c*v for k,c in a.items()})
def mul(a,b):
    out={}
    for ka,va in a.items():
        for kb,vb in b.items():
            k=ka+kb
            if len(set(k))!=len(k):continue
            sign=(-1)**sum(k[i]>k[j] for i in range(len(k)) for j in range(i+1,len(k)))
            key=tuple(sorted(k));out[key]=out.get(key,0)+sign*va*vb
    return clean(out)
def atom(i):return {(i,):s.S.One}
def delta(a):
    out={}
    vals={0:E[0],1:E[1],2:dE[0],3:dE[1]}
    for k,v in a.items():
        for j,x in enumerate(k):
            if x in vals:out=add(out,{k[:j]+k[j+1:]:v*(-1)**j*vals[x]})
    return out
def deriv(a):
    out={};oddmap={0:2,1:3,4:5}
    for k,v in a.items():
        dv=sum(s.diff(v,E[i])*dE[i] for i in range(2))
        out=add(out,{k:dv})
        for j,x in enumerate(k):
            if x in oddmap:
                term={():v}
                for z in k[:j]+(oddmap[x],)+k[j+1:]:term=mul(term,atom(z))
                out=add(out,term)
    return out
def expressions(B):
    psi={};current={};target={}
    for i in range(2):
        for j in range(2):
            uc=mul(atom(i),atom(4))
            psi=add(psi,scale(mul(uc,atom(2+j)),B[i,j]/2))
            current=add(current,scale(uc,B[i,j]*E[j]))
            target=add(target,scale(uc,B[i,j]*dE[j]),scale(mul(atom(i),atom(5)),B[i,j]*E[j]/2))
    return psi,current,target
B=s.Matrix([[b00,b01],[b01,b11]])
psi,current,target=expressions(B)
assert not add(delta(psi),scale(deriv(current),s.Rational(1,2)),scale(target,-1))
assert add(delta(psi),scale(target,-1)), 'Divergence is nonzero before quotient'
assert not delta(delta(psi))
assert add(delta(psi),scale(deriv(current),-s.Rational(1,2)),scale(target,-1)), 'Wrong divergence sign must fail'
_,_,wrong=expressions(s.Matrix([[b00,0],[0,b11]]))
assert add(target,scale(wrong,-1)), 'Off-diagonal fiber terms matter'
bad=s.Matrix([[0,1],[-1,0]]);f,j,t=expressions(bad)
assert add(delta(f),scale(deriv(j),s.Rational(1,2)),scale(t,-1)), 'Symmetry is a necessary hypothesis for this identity'
ghost={0:-1,1:-1,2:-1,3:-1,4:1,5:1}
assert all(sum(ghost[i] for i in mon)==-1 and len(mon)%2==1 for mon in psi)
assert all(sum(ghost[i] for i in mon)==0 and len(mon)%2==0 for mon in target)
res=dict(statute='DERIVED_GRADED_JET_PRIMITIVE_MODULO_EXPLICIT_DIVERGENCE',
    checks_passed=5,negative_controls=3,convention='delta u=E',
    identity='delta Psi + (1/2)dJ = u B[c dE+(1/2)(dc)E]',
    physical_candidate='B(A)=-A/6-I trA/12 matches previously measured transverse constant ghost sector after Fourier/normalization identification',
    unresolved=['Gauge-fixed delta h* includes C* b','BV sign and 4kappa normalization','Other ghost momenta and full h*hc','Cutoff derivative terms','Curvature and finite causal anomaly'],
    full_Q2=False,gate_changed=False,source_sha256=sha(Path(__file__)),
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-start)
new(DEST/'results.json',res)
print(json.dumps(res,ensure_ascii=False))
