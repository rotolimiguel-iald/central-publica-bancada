"""Kerr 220 two-branch model specified from local pyRing 2.7.0 source.

Preparation only: importing this module evaluates no waveform or likelihood.
Mf is detector-frame solar mass. h = h_plus + i h_cross, pyRing convention.
"""
import numpy as np
from scipy.linalg import solve_triangular

PARAMETERS=('psi','Mf','af','cosiota','A2220_1','A2220_2','phi2220_1','phi2220_2','dtau220')


def frequency_tau(mass,spin,coefficients,mass_time_s):
    if not np.isfinite([mass,spin]).all() or mass<=0 or not 0<=spin<1:
        raise ValueError('Invalid detector remnant')
    f1,f2,f3,q1,q2,q3=coefficients
    frequency=(f1+f2*(1-spin)**f3)/(2*np.pi*mass_time_s*mass)
    quality=q1+q2*(1-spin)**q3
    tau=quality/(np.pi*frequency)
    if not np.isfinite([frequency,tau]).all() or min(frequency,tau)<=0:
        raise ValueError('Invalid QNM fit')
    return frequency,tau


def polarizations(relative_time,parameters,config,mass_time_s):
    """Do not absorb inclination harmonics into uniform-radius amplitudes."""
    x=parameters
    if not all(np.isfinite(x[k]) for k in PARAMETERS):raise ValueError('Nonfinite parameters')
    if not -1<=x['cosiota']<=1:raise ValueError('Invalid inclination')
    f,tau=frequency_tau(x['Mf'],x['af'],config['qnm_coefficients'],mass_time_s)
    if not x['dtau220']>-1:raise ValueError('Invalid dtau220: tau must remain positive')
    tau*=1+x['dtau220']
    t=np.asarray(relative_time,dtype=float)-config['start_offset_s']
    if t.ndim!=1 or not np.isfinite(t).all() or np.any(t<0):raise ValueError('Invalid truncated times')
    # Spin -2, l=2, m=+/-2 spherical harmonics at azimuth phi=0.
    norm=np.sqrt(5/(64*np.pi))
    yp=norm*(1+x['cosiota'])**2
    ym=norm*(1-x['cosiota'])**2
    plus_branch=x['A2220_1']*np.exp(1j*x['phi2220_1'])
    minus_branch=x['A2220_2']*np.exp(1j*x['phi2220_2'])
    h=config['reference_amplitude']*np.exp(-t/tau)*(yp*plus_branch*np.exp(2j*np.pi*f*t)+ym*minus_branch*np.exp(-2j*np.pi*f*t))
    if not np.isfinite(h).all():raise ValueError('Invalid model')
    return h.real,h.imag


def geometry(detector,config):
    import lal
    obj=lal.cached_detector_by_prefix[detector]
    ref=lal.cached_detector_by_prefix[config['reference_detector']]
    trigger=lal.LIGOTimeGPS(config['trigger_GPS'])
    delay=float(lal.ArrivalTimeDiff(obj.location,ref.location,config['ra'],config['dec'],trigger))
    response_time=lal.LIGOTimeGPS(config['trigger_GPS']+config['start_offset_s']+delay)
    gmst=lal.GreenwichMeanSiderealTime(response_time)
    return obj,delay,gmst


def make_likelihood(blocks,config,guard):
    import bilby,lal
    class KerrLikelihood(bilby.Likelihood):
        def __init__(self):
            super().__init__(parameters={k:None for k in PARAMETERS})
            self.calls=0
        def log_likelihood(self,parameters=None):
            guard();self.calls+=1
            values=self.parameters if parameters is None else parameters
            total=0.
            # Use same physical branches in both detectors, not detector amplitudes.
            for block in blocks:
                hp,hc=polarizations(block['relative_times'],values,config,lal.G_SI*lal.MSUN_SI/lal.C_SI**3)
                fp,fc=lal.ComputeDetAMResponse(block['response'],config['ra'],config['dec'],values['psi'],block['gmst'])
                residual=(block['data']-fp*hp-fc*hc)/config['reference_amplitude']
                whitened=solve_triangular(block['cholesky_scaled'],residual,lower=True,check_finite=False)
                total+=block['log_normalization']-.5*float(whitened@whitened)
            if not np.isfinite(total):raise ValueError('Nonfinite likelihood, no silent rejection')
            return total
        def noise_log_likelihood(self):
            total=0.
            for b in blocks:
                y=solve_triangular(b['cholesky_scaled'],b['data']/config['reference_amplitude'],lower=True)
                total+=b['log_normalization']-.5*float(y@y)
            return total
    return KerrLikelihood()
