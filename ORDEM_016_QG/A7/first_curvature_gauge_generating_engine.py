"""Exact first-K covariant Taylor generator for a radial-frame one-form.

Uses real formal momenta. Restore i^(derivative_order-2*K_order) only
after combining a homogeneous kernel. No infinite numerical Taylor sum.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import factorial
from functools import lru_cache

AXES=tuple(tuple(int(i==j) for i in range(4)) for j in range(4))
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())
def product(xs):
    value=F(1)
    for x in xs:value*=x
    return value
def gamma_contraction(output,b,c,j):
    """output_c d_j Gamma^c_(b,c), same spaceform RNC sign as predecessor."""
    return -(dot(output,c)*dot(b,j)+dot(output,b)*dot(c,j)-2*dot(b,c)*dot(output,j))/3
def frame_second(a,b,c,v):
    return -dot(b,c)*dot(a,v)/3+(dot(a,b)*dot(v,c)+dot(a,c)*dot(v,b))/6

def word_value(word,a,p,v,order):
    """Ordered derivative word at origin, K0 or K1; no Fourier phase."""
    word=tuple(word);n=len(word)
    if order==0:return dot(a,v)*product(dot(p,w) for w in word)
    assert order==1
    total=F()
    for i in range(n):
        for j in range(i+1,n):
            other=product(dot(p,w) for t,w in enumerate(word) if t not in (i,j))
            total+=(frame_second(a,word[i],word[j],v)
                    -gamma_contraction(v,word[j],a,word[i]))*other
            for k in range(j+1,n):
                remaining=product(dot(p,w) for t,w in enumerate(word) if t not in (i,j,k))
                total-=dot(a,v)*gamma_contraction(p,word[j],word[k],word[i])*remaining
    return total

def _selections(groups,radial,n):
    for selected in combinations_with_replacement(range(len(groups)),n):
        if any(selected.count(i)>1 for i in set(selected) if i!=radial):continue
        yield selected

def oneform_generator(prefix,suffix,a,p,v,x,order):
    """e^(-p.x) sum_n (D_prefix D_x^n D_suffix v)_a/n!.

    Returned entries are homogeneous x-degrees0..3. Triples all drawn
    from the radial group vanish since d_x Gamma(x,x)=0, hence degree3=0.
    The binomial multiplicity of selecting k radial slots becomes 1/k!.
    """
    if order==0:return (dot(a,v)*product(dot(p,w) for w in prefix+suffix),F(),F(),F())
    assert order==1
    groups=tuple(prefix)+(tuple(x),)+tuple(suffix);radial=len(prefix)
    out=[F() for _ in range(4)]
    for selected in _selections(groups,radial,2):
        i,j=selected;k=selected.count(radial)
        remaining=product(dot(p,w) for t,w in enumerate(groups) if t!=radial and t not in selected)
        out[k]+=(frame_second(a,groups[i],groups[j],v)
                 -gamma_contraction(v,groups[j],a,groups[i]))*remaining/factorial(k)
    for selected in _selections(groups,radial,3):
        i,j,k=selected;degree=selected.count(radial)
        remaining=product(dot(p,w) for t,w in enumerate(groups) if t!=radial and t not in selected)
        out[degree]-=dot(a,v)*gamma_contraction(p,groups[j],groups[k],groups[i])*remaining/factorial(degree)
    assert out[3]==0,out
    return tuple(out)

@lru_cache(None)
def gauge_generator(p,v,x,xi,yj,order):
    prefix=(AXES[yj],) if yj>=0 else ()
    suffix=(AXES[xi],) if xi>=0 else ()
    result=[]
    for a in range(4):
        for b in range(a,4):
            first=oneform_generator(prefix,suffix+(AXES[a],),AXES[b],p,v,x,order)
            second=oneform_generator(prefix,suffix+(AXES[b],),AXES[a],p,v,x,order)
            result.append(tuple(c+d for c,d in zip(first,second)))
    return tuple(tuple(result[a][j] for a in range(10)) for j in range(3))
