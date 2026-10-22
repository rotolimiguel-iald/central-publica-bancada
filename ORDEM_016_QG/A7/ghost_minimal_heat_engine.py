"""Pure algebra for the fixed-background ghost operator and heat residue.

No files, remote calls or executions on import. Lorentz tensors may be restored
after the Euclidean auxiliary contractions; no causal finite part is inferred.
"""
import sympy as s

def first_order(H, p):
    p=s.Matrix(p); C=H*p-p*s.trace(H)/2
    return [s.Matrix(4,4,lambda nu,rho:s.I*(
        p[rho]*H[lam,nu]+p[lam]*H[rho,nu]-p[nu]*H[lam,rho]
        +int(lam==nu)*C[rho])) for lam in range(4)]

def zeroth_order(H,p):
    p=s.Matrix(p);C=H*p-p*s.trace(H)/2
    return -C*p.T

def vertex_reduced(H,p,k):
    k=s.Matrix(k);A=first_order(H,p)
    return s.expand(-H*k.dot(k)+sum((s.I*k[j]*A[j] for j in range(4)),s.zeros(4))+zeroth_order(H,p))

def vertex_direct(H,p,k):
    p,k=s.Matrix(p),s.Matrix(k);r=p+k
    return s.Matrix(4,4,lambda nu,rho:s.expand(-(
        p[rho]*(H*r)[nu]+r.dot(k)*H[rho,nu]+k[nu]*(H*r)[rho]
        -r[nu]*p[rho]*s.trace(H)/2-r[nu]*(H*k)[rho])))

def flat_heat_cross(H,J,p):
    """Coefficient of ab, h=a H exp(ipx)+b J exp(-ipx), in tr a4."""
    p=s.Matrix(p);AH=first_order(H,p);AJ=first_order(J,-p)
    EH=(zeroth_order(H,p)+p.dot(p)*H)/2
    EJ=(zeroth_order(J,-p)+p.dot(p)*J)/2
    result=s.trace(EH*EJ)
    for mu in range(4):
      for nu in range(4):
        OH=s.I*(p[mu]*AH[nu]-p[nu]*AH[mu])/2
        OJ=-s.I*(p[mu]*AJ[nu]-p[nu]*AJ[mu])/2
        result+=s.trace(OH*OJ)/6
    return s.factor(result)

def invariants(H,J,p):
    p=s.Matrix(p);p2=p.dot(p);hp=(p.T*H*p)[0];jp=(p.T*J*p)[0]
    return [s.trace(H*J)*p2**2,s.trace(H)*s.trace(J)*p2**2,
        (hp*s.trace(J)+jp*s.trace(H))*p2,(p.T*H*J*p)[0]*p2,hp*jp]

def basis(i,j):
    H=s.zeros(4);H[i,j]=1;H[j,i]=1;return H
