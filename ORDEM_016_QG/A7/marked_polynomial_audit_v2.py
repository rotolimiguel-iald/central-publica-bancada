"""Audit the symbolic proof's classical reduction and all UV monomials."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
from itertools import product
from math import comb,factorial
import hashlib,json
from sympy.polys.rings import ring
from marked_polynomial_engine import *
from metric_principal_vertices import eh_cubic_16k,clear_caches
HERE=Path(__file__).resolve().parent;DEST=HERE/'marked_polynomial_audit_v2';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_polynomial_engine.py'),
    predecessor_sha256=sha(HERE/'marked_polynomial/results.json'),
    targets=['all400 classical cubic Ward polarizations with k=a e0 and q arbitrary',
             'all126 loop monomials of degree<=5 in each of three denominator families vs independent simplex',
             'source and ghost duals vs indices; symmetric fiber contraction',
             'negative mutations of measured symbolic BV relation'],
    full_Q2=False,gate_changed=False))
start,cpu=perf_counter(),process_time();checks=[];neg=[];classical_nonzero=0
def check(name,e):
    assert e==ZERO,(name,str(e));checks.append(name)
def reject(name,e):
    assert e!=ZERO,name;neg.append(name)
bs=[]
for i in range(4):
    for j in range(i,4):
        bs.append([[ONE if (x,y) in [(i,j),(j,i)] else ZERO for y in range(4)] for x in range(4)])
def flat(H):return tuple(x for row in H for x in row)
pa=scale(q,-1);pb=add(q,scale(P,-1))
for j,A in enumerate(bs):
    for k,B in enumerate(bs):
        for m,v in enumerate(axes):
            derived=cubic_gauge(A,pa,B,pb,P,v)
            direct=eh_cubic_16k(flat(gauge(P,v)),tuple(P),flat(A),tuple(pa),flat(B),tuple(pb))
            check(f'full_classical_Ward_{j}_{k}_{m}',derived-direct)
            if derived:classical_nonzero+=1
            clear_caches()
    print(json.dumps(dict(classical_rows=j+1,checks=len(checks),elapsed=perf_counter()-start)),flush=True)
assert classical_nonzero

# Independent direct-index ghost and source definitions, no dual contraction.
k=q;l=add(P,Q);rr=add(k,l)
for i,H in enumerate(bs):
    for m,v in enumerate(axes):
        kv=dot(k,v);rl=dot(rr,l);Hr=mv(H,rr);Hv=mv(H,v);Hl=mv(H,l)
        direct=add(add(scale(Hr,-kv),scale(Hv,-rl)),
                   add(scale(l,-dot(v,Hr)),scale(rr,kv*trace(H)/2+dot(v,Hl))))
        derived=[inner(B,H) for B in ghost_duals(k,l,v)]
        for n in range(4):check(f'ghost_dual_{i}_{m}_{n}',derived[n]-direct[n])
    for ti,T in enumerate(bs):
        du=source_duals(T,k,l);HTl=mv(H,mv(T,l))
        for n in range(4):check(f'source_dual_{i}_{ti}_{n}',inner(du[n],H)-k[n]*inner(T,H)-2*HTl[n])

# Pairing inverse is checked algebraically using its ten-coordinate entries.
labels=[(i,j) for i in range(4) for j in range(i,4)]
ss=[[QQ(int(i==k))-QQ(1,2) if i==j and k==l else
     (QQ(1,2) if a==b else QQ.zero) for b,(k,l) in enumerate(labels)] for a,(i,j) in enumerate(labels)]
for i,A in enumerate(bs):
    for j,B in enumerate(bs):
        left=sum((inner(A,bs[m])*ss[m][n]*inner(bs[n],B) for m in range(10) for n in range(10)),ZERO)
        check(f'fiber_completeness_{i}_{j}',left-inner(A,itr(B)))

# Independent symbolic Feynman simplex integration for every loop monomial.
# This algorithm uses no radial recurrence and no q -> n asymptotics.
S,aa,bb,cc,x,y=ring('a,b,c,x,y',QQ)
def lift(poly):
    assert all(not any(e[:4]) for e in poly)
    return S.from_dict({e[4:]+(0,0):v for e,v in poly.items()})
def integrate_simplex(poly):
    out={}
    for e,v in poly.items():
        coeff=v*QQ(factorial(e[3])*factorial(e[4]),factorial(e[3]+e[4]+2))
        k=(0,0,0,0)+e[:3];out[k]=out.get(k,QQ.zero)+coeff
    return R.from_dict({k:v for k,v in out.items() if v})
def simplex_monomial(alpha,s1,s2):
    p=[lift(z) for z in s1];r=[lift(z) for z in s2]
    shift=[x*u+y*v for u,v in zip(p,r)]
    delta=x*sum((u*u for u in p),S.zero)+y*sum((v*v for v in r),S.zero)-sum((z*z for z in shift),S.zero)
    acc=S.zero
    for even in product(*(range(0,e+1,2) for e in alpha)):
        n=sum(even)//2
        if n<1:continue
        coef=2*(-1)**(n-1)*comb(n+1,2)*angular(even)
        term=S.one*coef*delta**(n-1)
        for i in range(4):
            exponent=alpha[i]-even[i]
            term*=comb(alpha[i],even[i])
            if exponent:term*=(-shift[i])**exponent
        acc+=term
    return integrate_simplex(acc)
alphas=[e for e in product(range(6),repeat=4) if sum(e)<=5]
assert len(alphas)==126
families=[(scale(P,-1),scale(add(P,Q),-1)),(scale(Q,-1),scale(add(P,Q),-1)),(P,scale(Q,-1))]
for fi,(s1,s2) in enumerate(families):
    uv=UV([ZERO4,s1,s2])
    for index,alpha in enumerate(alphas):
        numerator=R.from_dict({alpha+(0,0,0):QQ.one})
        check(f'UV_monomial_{fi}_{index}',uv.extract(numerator)-simplex_monomial(alpha,s1,s2))
    print(json.dumps(dict(simplex_family=fi,checks=len(checks),elapsed=perf_counter()-start)),flush=True)

res,pieces=ward(bs[0],axes[0],axes[1]);tri,free,lg,lm,rg,rm=pieces
check('symbolic_reference_component',res)
reject('erase_triangle',free-lg+lm/4+rg-rm/4)
reject('erase_metric_insertions',tri+free-lg+rg)
reject('reverse_triangle_sign',-tri+free-lg+lm/4+rg-rm/4)
reject('metric_relative_factor_two',tri+free-lg+lm/2+rg-rm/2)
# A second component is needed: ghosts cancel in the first one.
res,pieces=ward(bs[4],axes[1],axes[0]);tri,free,lg,lm,rg,rm=pieces
reject('erase_ghost_insertions',tri+free+lm/4-rm/4)
reject('forget_logLambda_vs_logLambdaSquared',simplex_monomial((2,0,0,0),*families[0])/2-simplex_monomial((2,0,0,0),*families[0]))
result=dict(statute='REAL_POLYNOMIAL_WARD_COMPLETENESS_AUDIT',checks_passed=len(checks),
    classical_basis_checks=400,classical_nonzero=classical_nonzero,UV_monomial_checks=378,
    negative_controls=neg,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    full_Q2=False,gate_changed=False,source_sha256=sha(Path(__file__)),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'))
new(DEST/'results.json',result);print(json.dumps(result),flush=True)
