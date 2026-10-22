"""Exact finite-matrix exploration. No numerical trajectories or rate fitting."""
from pathlib import Path
import itertools, json
import sympy as s

I=s.I
e=s.eye(2); a=s.Matrix([[0,1],[0,0]]); z=s.diag(1,-1)
k=s.kronecker_product
ai=k(a,e,e); ao=k(e,a,e); sm=k(e,e,a); sp=sm.H
Zi=k(z,e,e); Zo=k(e,z,e); Z=k(e,e,z)
ni=ai.H*ai; no=ao.H*ao; ne=sp*sm
wc,w,g,Om=s.symbols('wc w g Om',positive=True)
ki,ko,gam,gp,lam=s.symbols('ki ko gam gp lam',positive=True)
h=wc*(ni+no)+w*ne+g*(ai.H*sm+sp*ai)+Om*(sp+sm)
J=ao.H*sm+sp*ai
jumps=[(ki,ai),(ko,ao),(gam,sm),(gp,Z),(lam,J)]
def dd(j,A): return j.H*A*j-(j.H*j*A+A*j.H*j)/2
def L(A): return (I*(h*A-A*h)+sum((r*dd(j,A) for r,j in jumps),s.zeros(8))).applyfunc(s.expand)
def dec(A):
    basis={'I':e,'Z':z,'a':a,'ad':a.H}; rows=[]
    for ns in itertools.product(basis,repeat=3):
        B=k(*(basis[n] for n in ns))
        c=s.simplify(s.trace(B.H*A)/s.trace(B.H*B))
        if c: rows.append({'basis':list(ns),'coefficient':str(c)})
    return rows
def ev(r,A): return s.simplify(s.trace(r*A))
def main():
    out={}
    C=ai*ao; B=ai.H*ao
    for name,A in [('C',C),('B',B)]:
        out[name]={'L':dec(L(A)),'holo':dec(dd(J,A))}
    t=s.symbols('q',positive=True)
    vp=s.Matrix([1,0,0,t])/s.sqrt(1+t*t)
    vm=s.Matrix([1,0,0,-t])/s.sqrt(1+t*t)
    rv=vp*vp.H
    states={'ground':s.diag(1,0),'excited':s.diag(0,1),'plus':s.Matrix([[1,1],[1,1]])/2,'plus_i':s.Matrix([[1,-I],[I,1]])/2,'mixed':e/2}
    out['states']={}
    for name,rh in states.items():
        r=k(rv,rh)
        out['states'][name]={n:str(ev(r,A)) for n,A in [('C',C),('dC',L(C)),('ddC',L(L(C))),('B',B),('dB',L(B)),('ai',ai),('ao',ao)]}
    # A maximally mixed base plus a Hermitian term invisible to pair first moments.
    out['correction_candidates']=[]
    for ns in itertools.product(['I','Z','X','Y'],repeat=3):
        bas={'I':e,'Z':z,'X':a+a.H,'Y':I*(a.H-a)}
        D=k(*(bas[n] for n in ns))
        if ev(D,C)==0 and ev(D,B)==0 and ev(D,ai)==0 and ev(D,ao)==0:
            dc=ev(D,L(C)); db=ev(D,L(B))
            if dc or db: out['correction_candidates'].append({'basis':ns,'dC':str(dc),'dB':str(db)})
    p=Path(__file__).with_name('EXPLORATION_R59.json')
    with p.open('x',encoding='utf8') as f: json.dump(out,f,indent=2,ensure_ascii=False)
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
