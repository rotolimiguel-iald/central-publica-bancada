"""Polarized Einstein-Hilbert divergence current in a flat coordinate frame.

Only a finite square-free jet in the supplied legs is built. The variables
commute; the coefficient matrices do not. The returned B has its Fourier i
removed. No integration by parts or zero total momentum is imposed.
"""
from fractions import Fraction as F
from metric_principal_vertices import I, gamma2, upper_product, trace
from metric_quartic_vertices import mm

ZERO=(0,)*16
def submasks(mask):
    part=mask
    while True:
        yield part
        if part==0:break
        part=(part-1)&mask

def matrix_add(*terms):
    return tuple(sum(x) for x in zip(*terms)) if terms else ZERO

def metric_series(matrices):
    """Coefficients of g^-1 and sqrt(det g); coefficient equals polarization."""
    size=1<<len(matrices)
    powers={0:I}
    for mask in range(1,size):
        powers[mask]=matrix_add(*[mm(matrices[i],powers[mask^(1<<i)])
                                 for i in range(len(matrices)) if mask&(1<<i)])
    inverse={mask:tuple((-1)**mask.bit_count()*v for v in powers[mask]) for mask in range(size)}
    log={mask:F((-1)**(mask.bit_count()+1),2*mask.bit_count())*trace(powers[mask])
         for mask in range(1,size)}
    density={0:F(1)}
    for mask in range(1,size):
        first=mask&-mask
        density[mask]=sum((log[part]*density[mask^part] for part in submasks(mask) if part&first),F())
    return inverse,density

def current_contraction(outer,inner,gamma):
    raised=upper_product(inner,gamma)
    contracted_trace=[sum(raised[16*b+4*a+b] for b in range(4)) for a in range(4)]
    return tuple(sum(outer[4*a+b]*raised[16*mu+4*a+b] for a in range(4) for b in range(4))
                 -sum(outer[4*mu+a]*contracted_trace[a] for a in range(4)) for mu in range(4))

def boundary_current(*fields):
    """Coefficient of sqrt(g)(g^ab Gamma^mu_ab - g^mu,a Gamma^b_ab)."""
    matrices=[field[0] for field in fields]
    inverse,density=metric_series(matrices)
    full=(1<<len(fields))-1;answer=[F()]*4
    for leg,(matrix,momentum) in enumerate(fields):
        rest=full^(1<<leg);gamma=gamma2(matrix,tuple(momentum))
        for outer_mask in submasks(rest):
            remaining=rest^outer_mask
            for inner_mask in submasks(remaining):
                weight=density[remaining^inner_mask]/2
                if not weight:continue
                vector=current_contraction(inverse[outer_mask],inverse[inner_mask],gamma)
                for mu in range(4):answer[mu]+=weight*vector[mu]
    return tuple(answer)

def eh_boundary_vertex_raw(*fields):
    """2^(n+1) kappa times the action vertex from -div B/(2kappa)."""
    momentum=tuple(sum(p[i] for _,p in fields) for i in range(4))
    current=boundary_current(*fields)
    return 2**len(fields)*sum(p*b for p,b in zip(momentum,current))
