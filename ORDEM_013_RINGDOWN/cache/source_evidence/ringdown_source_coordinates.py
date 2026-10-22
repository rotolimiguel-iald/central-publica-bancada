"""Transport the SAME source prior into ringdown frequency/damping coordinates.

This changes numerical sampling coordinates only; it fixes neither source
parameters nor a physical dephasing reading. Inherited exact-QNM spline and
family-specific remnant fit. The Jacobian is mandatory in any integration.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
import numpy as np
from scipy.optimize import brentq
import source_evidence as se

FREF=250.
TREF=.004
TSUN=se.model.scales(1.,"CODATA2018_IAU2015")[0]
LOG_RATIO_REFERENCE=np.log(2*np.pi*FREF*TREF)


def remnant_at_unit_mass(family,q,s1,s2):
    mass,spin=se.model.remnant(family,80*q/(1+q),80/(1+q),s1,s2)
    return mass/80.,spin


def spectral(spin):
    spline=se.model.qnm_splines()[2]
    if not spline.x[0]<=spin<=spline.x[-1]:
        raise ValueError("Spin outside validated QNM spline")
    w=complex(spline(spin));d=complex(spline(spin,1))
    if w.real<=0 or w.imag>=0:raise ValueError("Invalid QNM convention")
    logratio=np.log(w.real/-w.imag)
    slope=d.real/w.real-d.imag/w.imag
    if slope<=0:raise ValueError("Nonmonotone QNM quality factor")
    return w,float(logratio),float(slope)


def spin_derivative(family,q,s1,s2):
    def chi(s):return remnant_at_unit_mass(family,q,s,s2)[1]
    def difference(h):return (chi(s1-2*h)-8*chi(s1-h)+8*chi(s1+h)-chi(s1+2*h))/(12*h)
    coarse,fine=difference(.001),difference(.0005)
    if fine<=0 or abs(coarse-fine)>1e-7*abs(fine):
        raise ValueError("Remnant-spin Jacobian did not converge or is not positive")
    return fine


def forward(family,u):
    u=np.asarray(u,dtype=float)
    if u.shape!=(6,) or np.any(~np.isfinite(u)) or np.any(u<0) or np.any(u>1):
        raise ValueError("Original unit-prior coordinates required")
    mass,q,s1,s2=50+60*u[0],1+2*u[1],-.4+.8*u[2],-.4+.8*u[3]
    fraction,spin=remnant_at_unit_mass(family,q,s1,s2)
    w,logratio,slope=spectral(spin)
    tm=mass*fraction*TSUN
    y=np.array([np.log(w.real/(2*np.pi*tm*FREF)),np.log(tm/(-w.imag*TREF)),u[1],u[3],u[4],u[5]])
    jacobian=48/mass*spin_derivative(family,q,s1,s2)*slope
    if not np.isfinite(jacobian) or jacobian<=0:raise ValueError("Singular prior transport")
    return y,float(jacobian)


def inverse(family,y):
    """Return (original unit coordinates,forward Jacobian), or None outside prior."""
    y=np.asarray(y,dtype=float)
    if y.shape!=(6,) or np.any(~np.isfinite(y)):
        raise ValueError("Finite six-dimensional transport coordinates required")
    if np.any(y[2:]<0) or np.any(y[2:]>1):return None
    q,s2=1+2*y[2],-.4+.8*y[3]
    target=LOG_RATIO_REFERENCE+y[0]+y[1]
    def ratio(s1):return spectral(remnant_at_unit_mass(family,q,s1,s2)[1])[1]
    lo,hi=ratio(-.4),ratio(.4)
    if not lo<hi:raise ValueError("Invalid spin-image bounds")
    if not lo<=target<=hi:return None
    s1=brentq(lambda s:ratio(s)-target,-.4,.4,xtol=1e-13,rtol=1e-14)
    fraction,spin=remnant_at_unit_mass(family,q,s1,s2)
    w,_,_=spectral(spin)
    mass=w.real/(2*np.pi*TSUN*fraction*FREF*np.exp(y[0]))
    if not 50<=mass<=110:return None
    u=np.array([(mass-50)/60,y[2],(s1+.4)/.8,y[3],y[4],y[5]])
    reconstructed,jacobian=forward(family,u)
    if np.max(np.abs(reconstructed-y))>1e-10:raise ValueError("Prior transport inverse mismatch")
    return u,jacobian
