"""Exact graded derivation of an antifield-linear local redefinition generator.

No full QME assertion. The formal jet identity assumes s h=g, s u=E,
s E=s g=0. Its physical use needs the independently checked free Noether
identity E G=0 and the shifted-antifield convention.
"""
from pathlib import Path
from datetime import datetime, timezone
from time import process_time
import hashlib, json
import sympy as s
import quadratic_metric_engine as qm
import marked_polynomial_engine as p

H=Path(__file__).resolve().parent
D=H/'metric_A2_generator';D.mkdir(exist_ok=True)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def fresh(f,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not f.exists()
    t=f.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(f)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='s(u A(h,h)) = E A(h,h) - 2u A(h,g); locality/symmetry of the actual 57-term representative',
    assumptions='Free graded differential, symmetric bilinear local A, constant coefficients; no Helmholtz requirement',
    full_Q2=False))
cpu=process_time();checks=0;negative=0
def check(value):
    global checks
    assert value;checks+=1
def clean(a):return {k:s.expand(v) for k,v in a.items() if s.expand(v)!=0}
def plus(*args):
    out={}
    for a in args:
        for k,v in a.items():out[k]=out.get(k,0)+v
    return clean(out)
def scale(a,c):return clean({k:c*v for k,v in a.items()})
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
h=s.symbols('h0:3');E=s.symbols('E0:3')
# Exterior variables u0,u1,u2,g0,g1,g2. h and E commute.
def differential(a):
    out={}
    for k,v in a.items():
        for i in range(3):out=plus(out,mul(scale(atom(3+i),s.diff(v,h[i])),{k:s.S.One}))
        for j,x in enumerate(k):
            if x<3:out=plus(out,{k[:j]+k[j+1:]:v*(-1)**j*E[x]})
    return clean(out)
A={};F={};target={};companion={};minus_term={}
for i in range(3):
    for j in range(3):
        for k in range(j,3):
            a=s.Symbol(f'A{i}_{j}{k}')
            A[i,j,k]=A[i,k,j]=a
for i in range(3):
    polynomial=sum(A[i,j,k]*h[j]*h[k] for j in range(3) for k in range(3))
    F=plus(F,scale(atom(i),polynomial))
    companion=plus(companion,{():E[i]*polynomial})
    for j in range(3):
        for k in range(3):minus_term=plus(minus_term,scale(mul(atom(i),atom(3+k)),-2*A[i,j,k]*h[j]))
target=plus(companion,minus_term)
check(not plus(differential(F),scale(target,-1)))
check(not differential(differential(F)))
check(not differential(target))
for wrong in [plus(companion,scale(minus_term,-1)),plus(companion,scale(minus_term,s.Rational(1,2))),minus_term]:
    check(bool(plus(differential(F),scale(wrong,-1))));negative+=1
# Point field redefinition need not be the gradient of a scalar action.
# A0=h1^2, A1=A2=0 violates Helmholtz, yet has the displayed BV generator.
non_gradient=scale(atom(0),h[1]**2)
check(s.diff(h[1]**2,h[1])!=s.diff(s.S.Zero,h[0]))
check(not plus(differential(non_gradient),{():-E[0]*h[1]**2},scale(mul(atom(0),atom(4)),2*h[1])))
ghost={0:-1,1:-1,2:-1,3:1,4:1,5:1}
check(all(sum(ghost[x] for x in mon)==-1 for mon in F))
check(all(sum(ghost[x] for x in mon)==0 for mon in target))

fit=json.loads((H/'bv_gradient_fit/results.json').read_bytes())
coef=list(map(p.QQ,fit['A2_coefficients']));check(len(coef)==57)
check(fit['columns']-fit['rank']==31)
# Ten symmetric fiber basis elements, polynomial momenta on two independent
# directions. The map's full bilinear symmetry additionally follows directly
# from the explicit symmetrization of raw(H,k,J,l) in quadratic_metric_engine.
basis=[]
for i in range(4):
    for j in range(i,4):
        B=[[p.ZERO for _ in range(4)] for _ in range(4)]
        B[i][j]=B[j][i]=p.ONE;basis.append(B)
nonzero=0
for bi,Hh in enumerate(basis):
    for bj,Jj in enumerate(basis):
        aa,names=qm.terms(Hh,p.P,Jj,p.Q)
        bb,_=qm.terms(Jj,p.Q,Hh,p.P)
        check(names==fit['basis_names'])
        for i in range(4):
            for j in range(4):
                v=sum((c*T[i][j] for c,T in zip(coef,aa)),p.ZERO)
                w=sum((c*T[i][j] for c,T in zip(coef,bb)),p.ZERO)
                check(v==w)
                check(v==sum((c*T[j][i] for c,T in zip(coef,aa)),p.ZERO))
                check(all(sum(exponents)==2 for exponents in v.keys()))
                nonzero+=bool(v)
result=dict(statute='DERIVED_EXACT_GRADED_LOCAL_GENERATOR_WITH_COMPANION',checks=checks,negative_controls=negative,
    identity='s0 integral u.A2(h,h) = integral (Eh).A2(h,h) - 2u.A2(h,Gc)',
    shifted_antifield='u=4*kappa*(hstar+Cstar*barc), s0 u=Eh in the already checked convention',
    nonzero_actual_components=nonzero,rank=fit['rank'],parameters=fit['columns']-fit['rank'],
    no_helmholtz_required='Generator linear in antifield; not a claimed Euler-Lagrange gradient on fields alone',
    scope='Free local jet differential and flat degree-two representative; covariant/finite/cutoff hierarchy still separate',
    full_Q2=False,gate_changed=False,cpu_seconds=process_time()-cpu)
fresh(D/'results.json',result)
files=[Path(__file__),H/'quadratic_metric_engine.py',H/'marked_polynomial_engine.py',H/'bv_gradient_fit/results.json',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(f),sha256=sha(f)) for f in files]))
print(json.dumps(result,ensure_ascii=False))
