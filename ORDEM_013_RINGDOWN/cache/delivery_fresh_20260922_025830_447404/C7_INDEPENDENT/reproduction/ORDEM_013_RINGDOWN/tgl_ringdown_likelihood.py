"""Finite-interval Gaussian likelihood with explicit linear amplitude priors.

All inputs are already whitened by a data-independent, truncated-interval map.
Independent complex mode amplitudes in each detector define a phenomenological
ringdown model, not a polarization-coherent network GR/TGL likelihood.
Profile likelihoods and properly marginalized likelihoods are kept distinct.
"""
import numpy as np

def linear_statistics(basis, targets, amplitude_prior_sd):
    """Return log L/L(no signal), profiling or integrating real amplitudes.

    basis: (grid, time, coefficients), targets: (draws, time).
    The proper prior is isotropic Normal(0, amplitude_prior_sd**2) on each
    coefficient of the UNNORMALIZED physical basis, in the declared units.
    Omitting the determinant would turn the integral into a profile fit.
    """
    basis=np.asarray(basis,dtype=float); targets=np.asarray(targets,dtype=float)
    if basis.ndim==2:basis=basis[None,:,:]
    if targets.ndim==1:targets=targets[None,:]
    if amplitude_prior_sd<=0 or not np.isfinite(amplitude_prior_sd):
        raise ValueError('Finite proper Gaussian amplitude prior required')
    gram=np.einsum('gti,gtj->gij',basis,basis,optimize=True)
    rhs=np.einsum('gti,dt->gdi',basis,targets,optimize=True)
    coeff=np.linalg.solve(gram,rhs.transpose(0,2,1)).transpose(0,2,1)
    profile=.5*np.einsum('gdi,gdi->gd',rhs,coeff)
    p=gram.shape[-1]
    regularized=gram+np.eye(p)[None,:,:]/amplitude_prior_sd**2
    mean=np.linalg.solve(regularized,rhs.transpose(0,2,1)).transpose(0,2,1)
    sign,logdet=np.linalg.slogdet(regularized*amplitude_prior_sd**2)
    if np.any(sign<=0):raise ValueError('Amplitude covariance not positive')
    marginal=.5*np.einsum('gdi,gdi->gd',rhs,mean)-.5*logdet[:,None]
    return profile,marginal

def profile_intervals(grid, log_likelihood, delta_chisquare=2.705543454095404):
    """Unconstrained diagnostic MLE and 90% profile interval, no Bayes label.

    Negative dephasing amplitudes, if passed on the grid, are diagnostics only;
    the physical point hypotheses remain a=0 and a=1. Multiple islands are
    reported and enveloped conservatively. Boundary truncation remains visible.
    """
    grid=np.asarray(grid); log_likelihood=np.asarray(log_likelihood)
    out=[]
    for col in log_likelihood.T:
        k=int(np.argmax(col)); center=float(grid[k]);maximum=float(col[k])
        if 0<k<len(grid)-1:
            x=grid[k-1:k+2]-grid[k]
            c=np.polyfit(x,col[k-1:k+2]-col[k],2)
            if c[0]<0:
                offset=-c[1]/(2*c[0])
                if x[0]<=offset<=x[-1]:
                    center+=float(offset);maximum+=float(np.polyval(c,offset))
        level=maximum-delta_chisquare/2
        good=np.flatnonzero(col>=level)
        if not len(good):raise ValueError('Profile grid misses peak')
        lo=int(good[0]);hi=int(good[-1])
        left=float(grid[lo]);right=float(grid[hi])
        if lo>0:left=float(np.interp(level,[col[lo-1],col[lo]],[grid[lo-1],grid[lo]]))
        if hi<len(grid)-1:right=float(np.interp(level,[col[hi+1],col[hi]],[grid[hi+1],grid[hi]]))
        out.append(dict(MLE=center,CI90=[left,right],boundary=lo==0 or hi==len(grid)-1,
                        islands=int(1+np.count_nonzero(np.diff(good)>1))))
    return out
