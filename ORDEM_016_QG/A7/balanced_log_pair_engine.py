"""Balanced extension of labelled radial/logarithmic line profiles, divided by CE."""
from functools import lru_cache
from itertools import product
import sympy as s
from logarithmic_contact_engine import contact as radial_contact,Q

x=s.symbols('x0:4');z,L=s.symbols('z L')

def dx(expr,i):
    return s.expand(s.diff(expr,x[i])+2*x[i]*(s.diff(expr,z)+s.diff(expr,L)/z))

@lru_cache(None)
def line(n,ell,word):
    if not word:return z**(-n)*L**ell
    return dx(line(n,ell,word[:-1]),word[-1])

@lru_cache(None)
def monomial_contact(n,ell,powers,word):
    out=0
    for mask in product((0,1),repeat=len(word)):
        remaining=list(powers);coef=s.Integer(1);rest=[]
        for i,on_monomial in zip(word,mask):
            if on_monomial:
                coef*=remaining[i];remaining[i]-=1
                if not coef:break
            else:rest.append(i)
        if not coef or not rest:continue
        v=radial_contact(n,ell,tuple(rest))
        for i,p in enumerate(remaining):v=(-1)**p*s.diff(v,Q[i],p)
        out+=coef*v
    return s.expand(out)

@lru_cache(None)
def contact(expr,word):
    out=0
    for term in s.Add.make_args(s.expand(expr)):
        if not term:continue
        powers=term.as_powers_dict();n=-powers.get(z,0);ell=powers.get(L,0)
        assert int(n)==n and n>=0 and int(ell)==ell and ell>=0,(term,n,ell)
        for xp,c in s.Poly(term*z**n/L**ell,*x).terms():
            assert c.is_Rational,(term,c)
            out+=c*monomial_contact(int(n),int(ell),xp,word)
    return s.expand(out)

@lru_cache(None)
def balanced(left_profile,right_profile,word):
    out=0
    for mask in product((0,1),repeat=len(word)):
        u=tuple(i for i,b in zip(word,mask) if not b);v=tuple(i for i,b in zip(word,mask) if b)
        out+=(-1)**len(v)*line(*left_profile,u)*line(*right_profile,v)/s.Integer(2)**len(word)
    return s.expand(out)

@lru_cache(None)
def correction(left_profile,right_profile,left_word,right_word):
    slots=tuple((0,i) for i in left_word)+tuple((1,i) for i in right_word);out=0
    for mask in product((0,1),repeat=len(slots)):
        total=[];bal=[];coef=s.Integer(1)
        for (side,i),is_bal in zip(slots,mask):
            if is_bal:bal.append(i);coef*=(-1)**side
            else:total.append(i);coef/=2
        if total:out-=coef*contact(balanced(left_profile,right_profile,tuple(sorted(bal))),tuple(sorted(total)))
    return s.expand(out)

def euler_correction(left_profile,right_profile,left_word=(),right_word=()):
    return s.expand(sum(correction(left_profile,right_profile,tuple(sorted(left_word+(i,i))),right_word) for i in range(4)))
