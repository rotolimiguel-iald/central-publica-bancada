"""Diagnostic of the assembled logarithmic Hessian against the gauge map.

Uses odd covariant jets of a one-form in a parallel radial frame.
The phase i is removed. Does not claim full causal Ward or choose a counterterm.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations,permutations,combinations_with_replacement
from functools import lru_cache
from fractions import Fraction as F
from time import process_time,perf_counter
import hashlib,json
from ghost_covariant_word_engine import gamma
H=Path(__file__).resolve().parent;D=H/'first_curvature_ward_probe';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),
    inputs=[dict(path=str(H/r),sha256=sha(H/r)) for r in ['first_curvature_total_hessian/results.json','covariant_source_operator/DERIVACAO.md','metric_bubble_v2/results.json','ghost_bubble/results.json']],
    question='What is the firstK local logarithmic coefficient of Hloop K_gauge, compared with E0R1?',
    forbidden='No fit to zero, no ad hoc change of weights, no full Q2 conclusion'))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
def oneform(v,p):
    @lru_cache(None)
    def jet(w,a,order):
        n=len(w);assert n in (1,3,5)
        if order==0:
            out=F(v[a])*(-1)**((n-1)//2)
            for i in w:out*=p[i]
            return out
        if n==1:return F()
        out=F()
        # Differentiate exactly one Christoffel, including derivative slots.
        for k in range(1,n):
            for j in range(k):
                for slot in range(k+1,n+1):
                    target=w[slot] if slot<n else a
                    for c in range(4):
                        value=-gamma(c,w[k],target,w[j])*(-1)**((n-3)//2)
                        if not value:continue
                        ww=list(w);aa=a
                        if slot<n:ww[slot]=c
                        else:aa=c
                        value*=v[aa]
                        for t,i in enumerate(ww):
                            if t not in (j,k):value*=p[i]
                        out+=value
        # h_coordinate=e h_radial with e=I-K(zI-xx)/6.
        for i,j in combinations(range(n),2):
            a1,a2=w[i],w[j]
            c2=-F(1,3)*int(a1==a2)*v[a]+F(1,6)*(int(a==a1)*v[a2]+int(a==a2)*v[a1])
            value=c2*(-1)**((n-3)//2)
            for t,b in enumerate(w):
                if t not in (i,j):value*=p[b]
            out+=value
        return out
    @lru_cache(None)
    def h(w,a,b,order):return jet(w+(a,),b,order)+jet(w+(b,),a,order)
    @lru_cache(None)
    def hs(w,a,b,order):
        words=set(permutations(w))
        return sum((h(t,a,b,order) for t in words),F())/len(words)
    return jet,hs
flat=list(map(F,['-61/120','-23/120','23/120','61/60','-7/10']))
curved=list(map(F,json.loads((H/'first_curvature_total_hessian/results.json').read_bytes())['total']))
assert curved[2]==curved[3]
c1,c2,c3,c4,c5=flat;d1,d2,d3,_,d4=curved
def gauge_hessian(v,p,order):
    jet,j=oneform(tuple(v),tuple(p));out=[]
    for a in range(4):
        row=[]
        for b in range(4):
            value=c1*sum(j((i,i,k,k),a,b,order) for i in range(4) for k in range(4))
            if a==b:value+=c2*sum(j((i,i,k,k),m,m,order) for i in range(4) for k in range(4) for m in range(4))
            value+=c3*sum(j((a,b,i,i),m,m,order) for i in range(4) for m in range(4))
            if a==b:value+=c3*sum(j((i,k,m,m),i,k,order) for i in range(4) for k in range(4) for m in range(4))
            value+=c4/2*sum(j((a,i,k,k),i,b,order)+j((b,i,k,k),i,a,order) for i in range(4) for k in range(4))
            value+=c5*sum(j((a,b,i,k),i,k,order) for i in range(4) for k in range(4))
            if order:
                value-=d1*sum(j((i,i),a,b,0) for i in range(4))
                if a==b:value-=d2*sum(j((i,i),m,m,0) for i in range(4) for m in range(4))
                value-=d3*sum(j((a,b),m,m,0) for m in range(4))
                if a==b:value-=d3*sum(j((i,k),i,k,0) for i in range(4) for k in range(4))
                value-=d4/2*sum(j((a,i),i,b,0)+j((b,i),i,a,0) for i in range(4))
            row.append(value)
        out.append(row)
    return out
cases=[]
for p,v in [((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0)),((1,2,-1,1),(2,0,1,-1))]:
    j,_=oneform(v,p)
    for n in (3,5):
        for w in combinations_with_replacement(range(4),n):
            words=set(permutations(w))
            for a in range(4):check(f'sym_oneform_{p}_{w}_{a}',sum((j(t,a,1) for t in words),F()),0)
    flatvalue=gauge_hessian(v,p,0)
    for a in range(4):
        for b in range(4):check(f'flat_Ward_{p}_{a}_{b}',flatvalue[a][b],0)
    actual=gauge_hessian(v,p,1);p2=sum(t*t for t in p);pv=sum(a*b for a,b in zip(p,v))
    source=[[F(4*(p[a]*p[b]-int(a==b)*p2)*pv) for b in range(4)] for a in range(4)]
    cases.append(dict(p=p,v=v,Hloop_G=[[str(t) for t in row] for row in actual],E_R=[[str(t) for t in row] for row in source],
        sum=[[str(actual[a][b]+source[a][b]) for b in range(4)] for a in range(4)],
        difference=[[str(actual[a][b]-source[a][b]) for b in range(4)] for a in range(4)]))
    print(json.dumps(cases[-1]),flush=True)
fresh(D/'results.json',dict(statute='REAL_DIAGNOSTIC_FIRST_K_LOG_WARD_ONLY',checks=len(checks),cases=cases,
    cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),cpu=process_time()-cpu)))
