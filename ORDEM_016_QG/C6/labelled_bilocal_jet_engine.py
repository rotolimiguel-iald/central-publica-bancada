"""Preserve radial line derivative labels while differentiating coefficient jets.

Each term is (polynomial coefficient, radial base profile, radial derivative word).
Covariant words are kept ordered; only radial partial words commute.
"""
from functools import lru_cache
from collections import defaultdict
import sympy as s
import tensor_euler_zerojet as T
import balanced_log_pair_engine as E
from bilocal_scalar_euler_zerojet import jet
from smooth_line_compatibility_check_v2 import multiply,correction as smooth

def clean(terms):
    grouped=defaultdict(lambda:s.S.Zero)
    for c,p,w in terms:grouped[(p,tuple(sorted(w)))]+=c
    return tuple((s.expand(c),p,w) for (p,w),c in sorted(grouped.items()) if s.expand(c)!=0)

def partial(terms,side,i):
    coords=T.x if side==0 else T.y;sign=1 if side==0 else -1
    return clean([t for c,p,w in terms for t in [(s.diff(c,coords[i]),p,w),(sign*c,p,w+(i,))]])

@lru_cache(None)
def metric(order,ind,word):
    if not word:return tuple((c,p,()) for c,p in T.prop(order,ind))
    j,*tail=word;tail=tuple(tail)
    terms=list(partial(metric(order,ind,tail),1,j))
    if order:
        for pos,b in enumerate(tail):
            for c in range(4):
                new=tail[:pos]+(c,)+tail[pos+1:]
                g=-T.gamma(T.y,c,j,b)
                terms.extend((g*a,p,w) for a,p,w in metric(0,ind,new))
        for pos in (2,3):
            b=ind[pos]
            for c in range(4):
                ids=ind[:pos]+(c,)+ind[pos+1:];g=-T.gamma(T.y,c,j,b)
                terms.extend((g*a,p,w) for a,p,w in metric(0,ids,tail))
    return clean(terms)

@lru_cache(None)
def scalar(order,word):
    base=(((s.S.One,T.F,()),) if order==0 else
        (((T.xx*T.yy-T.xy**2)/3,(2,0),()),(s.Rational(1,4),T.ONE,()),(-s.Rational(1,2),T.LG,())))
    for side,i in word:base=partial(base,side,i)
    return base

@lru_cache(None)
def pair(a,ua,b,ub):
    out=0
    for ca,pa,wa in a:
        for cb,pb,wb in b:
            for c,p,u in jet(ca,pa,ua):
                for d,q,v in jet(cb,pb,ub):
                    u=tuple(sorted(u+wa));v=tuple(sorted(v+wb))
                    if q==T.ONE:value=0 if v else smooth(p,s.S.One,u,())
                    elif p==T.ONE:value=0 if u else smooth(q,s.S.One,v,())
                    else:value=E.correction(p,q,u,v)
                    out+=multiply(c*d,value)
    return s.expand(out)

@lru_cache(None)
def unit(word):return tuple((2*c,p,w) for c,p,w in metric(0,(0,1,0,1),word))

def realize(terms):
    repl={E.z:T.B.w,E.L:T.B.L,**{E.x[i]:T.x[i]-T.y[i] for i in range(4)}}
    return s.expand(sum(c*E.line(*p,w).subs(repl,simultaneous=True) for c,p,w in terms))
