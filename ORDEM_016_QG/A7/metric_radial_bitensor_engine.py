"""First-curvature metric propagator jets in radial orthonormal frames.

All matrices use the ten symmetric tensor component coordinates and include
the inverse Gram matrix. Strip 4*kappa/(4*pi²); return coefficient of K^order.
The derivative labels are orthonormal tangent labels, one at either endpoint.
"""
from functools import lru_cache
import sympy as s
from metric_coincident_jet_engine_v2 import metric_fiber
from curved_source_jet_engine import x,z,L

@lru_cache(None)
def frame_data():
    f=metric_fiber();S=f['S0'];g=f['g'];omega=f['omega']
    A=[sum((x[j]*omega[j,i]/2 for j in range(4)),s.zeros(10)) for i in range(4)]
    return S,g*g.T/2,omega,A

@lru_cache(None)
def metric_radial_jet(order,xi=-1,yi=-1):
    S,V,omega,A=frame_data()
    if order==0:
        if xi<0 and yi<0:return S/z
        if xi<0:return 2*x[yi]*S/z**2
        if yi<0:return -2*x[xi]*S/z**2
        return S*(2*int(xi==yi)/z**2-8*x[xi]*x[yi]/z**3)
    assert order==1
    if xi<0 and yi<0:return S/4+V*L
    if xi<0:return A[yi]*S/z-2*x[yi]*V/z
    if yi<0:return A[xi]*S/z+2*x[xi]*V/z
    i,j=xi,yi
    Nij=z*int(i==j)-x[i]*x[j]
    return (S*Nij/(3*z**2)+omega[i,j]*S/(2*z)
            -2*x[i]*A[j]*S/z**2+2*x[j]*A[i]*S/z**2
            +V*(-2*int(i==j)/z+4*x[i]*x[j]/z**2))
