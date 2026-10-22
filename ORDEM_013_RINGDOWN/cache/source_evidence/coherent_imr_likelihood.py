"""Nonlinear source likelihood with exact coherent distance/polarization integral.

The two common coefficients have an isotropic Normal(0,s**2) prior. Equivalently,
psi is uniform modulo pi and distance D>0 has the normalized input prior
p(D)=D_ref**2/(s**2*D**3)*exp(-D_ref**2/(2*s**2*D**2)), D_ref=403 Mpc.
This is not a uniform-volume prior. Source parameters still require sampling.
No normalization of the waveform to a chosen SNR occurs in this likelihood.
"""
import math
import numpy as np
from coherent_imr_model import network_basis,remnant,qnm_splines
from tgl_ringdown_likelihood import linear_statistics


def distance_prior_density(distance_mpc,amplitude_prior_sd):
    if not math.isfinite(amplitude_prior_sd) or amplitude_prior_sd<=0:
        raise ValueError("A finite positive common amplitude prior is required")
    d=np.asarray(distance_mpc,dtype=float)
    if np.any(~np.isfinite(d)) or np.any(d<=0):raise ValueError("Distance must be positive and finite")
    ref=403.;s=amplitude_prior_sd
    return ref**2/(s*s*d**3)*np.exp(-ref**2/(2*s*s*d*d))


def marginalized_source_log_likelihood(*,family,coordinates,times,white,targets,reading,a,
                                      amplitude_prior_sd,sample_rate=8192):
    x=np.asarray(coordinates,dtype=float)
    if x.shape!=(7,) or np.any(~np.isfinite(x)):raise ValueError("Seven finite source coordinates required")
    total=np.exp(x[0]);q=np.exp(x[1]);m1=total*q/(1+q);m2=total/(1+q)
    _,spin=remnant(family,m1,m2,x[2],x[3])
    if a!=0 and any(spin<s.x[0] or spin>s.x[-1] for s in qnm_splines().values()):
        raise ValueError("Source remnant is outside the verified signed-axis QNM grid; no extrapolation")
    if not math.isfinite(a) or a<0:raise ValueError("Nonnegative physical dephasing amplitude required")
    basis,metadata=network_basis(family,x,times,reading,a,white,sample_rate)
    targets=np.atleast_2d(np.asarray(targets,dtype=float))
    if targets.shape[1]!=basis.shape[0] or not np.all(np.isfinite(targets)):
        raise ValueError("Whitened network target has incompatible dimensions or nonfinite entries")
    _,logz=linear_statistics(basis,targets,amplitude_prior_sd)
    return logz[0],dict(**metadata,distance_prior="INPUT_INVERSE_RAYLEIGH_DISTANCE",distance_reference_mpc=403.,
                       amplitude_prior_sd=float(amplitude_prior_sd),polarization="uniform_mod_pi",
                       source_parameters_marginalized=False,noise_constant="logL(data|noise) omitted consistently",
                       scope="Exact two-coefficient integral for the nonlinear source at supplied coordinates; not full source evidence")
