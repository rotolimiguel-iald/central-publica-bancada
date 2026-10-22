"""Optional, explicitly chosen effective readouts; NumPy-only public API.

These functions do not change the frozen C6 analysis. They supplement the
ensemble/Brownian template with Cauchy phase noise and a finite-occupation
root-generator coherent field. A GKSL generator does not select a classical
strain unraveling. Exact finite-N sums are never silently extrapolated to a
macroscopic occupation. A separate oscillator model is an INPUT assumption.
"""
import math
import numpy as np
from tgl_ringdown_prediction import beta_tgl, kerr_mode, prediction
from tgl_ringdown_template import ringdown

def _elapsed(time):
    t=np.asarray(time,dtype=float)
    if t.ndim!=1 or not np.all(np.isfinite(t)) or np.any(t<0) or np.any(np.diff(t)<=0):
        raise ValueError('Finite nonnegative strictly increasing elapsed times required')
    return t

def phase_factor(elapsed, gamma_per_s, *, process, seed=None):
    """One unit-modulus realization, or its exponential ensemble mean.

    E exp(i phi_t)=exp(-Gamma*t). Brownian increments have variance 2*Gamma*dt;
    Cauchy increments have scale Gamma*dt and NO finite phase variance. The
    identical one-coherence mean does not identify their full generators.
    """
    t=_elapsed(elapsed)
    if not math.isfinite(gamma_per_s) or gamma_per_s<0:raise ValueError('Finite nonnegative rate required')
    if process=='ensemble':return np.exp(-gamma_per_s*t).astype(complex)
    if process not in ('brownian','cauchy'):raise ValueError('Explicit ensemble, brownian or cauchy process required')
    if seed is None:raise ValueError('Explicit seed required for stochastic readout')
    dt=np.diff(np.r_[0.,t]);rng=np.random.default_rng(seed)
    increments=(rng.normal(size=len(t))*np.sqrt(2*gamma_per_s*dt) if process=='brownian'
                else rng.standard_cauchy(size=len(t))*gamma_per_s*dt)
    return np.exp(1j*np.cumsum(increments))

def poisson_support(occupation, *, tail_bound=1e-13):
    """Centered recurrence, Chernoff/Bernstein support, no SciPy dependency.

    Normalization is checked, not repaired by renormalizing a truncated tail.
    Roundoff is reported separately from the analytic omitted-mass bound.
    Exact support is limited to N<=4096, explicitly; larger N needs a separate
    approximation and cannot be treated as an exact sum by this interface.
    """
    if not math.isfinite(occupation) or not 0<occupation<=4096:
        raise ValueError('Exact coherent sum requires 0 < occupation <= 4096')
    if not 1e-15<=tail_bound<=1e-6:raise ValueError('Unsupported tail tolerance')
    logbound=math.log(2/tail_bound)
    low=max(0,int(math.floor(occupation-math.sqrt(2*occupation*logbound))))
    high=int(math.ceil(occupation+math.sqrt(2*occupation*logbound)+(2/3)*logbound))
    indices=np.arange(low,high+1);weights=np.zeros(len(indices));mode=int(math.floor(occupation))
    center=mode-low
    weights[center]=math.exp(-occupation+mode*math.log(occupation)-math.lgamma(mode+1))
    for j in range(center+1,len(weights)):weights[j]=weights[j-1]*occupation/indices[j]
    for j in range(center-1,-1,-1):weights[j]=weights[j+1]*(indices[j]+1)/occupation
    normalization=float(weights.sum())
    if abs(1-normalization)>5e-11:raise ArithmeticError('Poisson normalization unresolved')
    return indices,weights,dict(occupation=occupation,support=[low,high],
        analytic_omitted_mass_bound=tail_bound,measured_probability_sum=normalization,
        normalization_roundoff_allowance=5e-11,renormalized=False)

def coherent_root_factor(elapsed, omega_rad_s, occupation, *, deformation=1.,
                         observable='ensemble', seed=None):
    """Normalized <a> factor for f(n)=sqrt(beta*omega*n), finite occupation.

    Ensemble: sum Pois(N;n) exp[-a*beta*omega*t/(2(sqrt(n+1)+sqrt(n))^2)].
    Conditional quantum trajectory: same weights, one shared Wiener process,
    exp[i sqrt(a*beta*omega)*W_t/(sqrt(n+1)+sqrt(n))]. Its |<a>|^2 need not be
    constant although oscillator number is conserved. It is not a phase-only
    classical realization, nor a unique waveform implied by the generator.
    """
    t=_elapsed(elapsed)
    if not math.isfinite(omega_rad_s) or omega_rad_s<=0:raise ValueError('Positive finite omega required')
    if not math.isfinite(deformation) or deformation<0:raise ValueError('Nonnegative finite deformation required')
    n,weights,meta=poisson_support(occupation)
    gaps=np.sqrt(deformation*beta_tgl()*omega_rad_s)/(np.sqrt(n+1)+np.sqrt(n))
    if observable=='ensemble':
        factors=np.exp(-.5*t[:,None]*gaps[None,:]**2)@weights
    elif observable=='quantum_wiener':
        if seed is None:raise ValueError('Explicit seed required for quantum trajectory')
        wt=np.cumsum(np.random.default_rng(seed).normal(size=len(t))*np.sqrt(np.diff(np.r_[0.,t])))
        factors=np.exp(1j*wt[:,None]*gaps[None,:])@weights
    else:raise ValueError('Explicit ensemble or quantum_wiener readout required')
    meta.update(initial_rate_per_s=float(weights@(.5*gaps**2)),
        rate_scope='Poisson-weighted initial slope, not one exponential damping time',
        readout=observable)
    return np.asarray(factors,dtype=complex),meta

def conditional_ringdown(time_array,mass_detector_solar,spin,reading,strain_amplitude,
                         t_start=0.,phase=0.,inclination=0.,deformation=1.,redshift=0.,*,
                         observable='ensemble',seed=None,occupation=None,
                         qnm_dimensionless=None,mode=(2,2,0),polarization_factors=None,
                         profile='CODATA2018_IAU2015'):
    """Bilby-compatible plus/cross arrays with additional explicit readouts.

    Existing ensemble/Brownian calls delegate unchanged. R-LIN can use
    cauchy_phase; R-RAIZ-COHERENT requires an exact finite occupation and either
    ensemble or quantum_wiener. The coherent carrier uses the same exact QNM
    and detector-frame seconds as its root coefficients. Amplitude is free;
    no distance-to-occupation/excitation law is invented here.
    """
    base=dict(t_start=t_start,phase=phase,inclination=inclination,deformation=deformation,
        redshift=redshift,seed=seed,occupation=occupation,qnm_dimensionless=qnm_dimensionless,
        mode=mode,polarization_factors=polarization_factors,profile=profile)
    if reading!='R-RAIZ-COHERENT' and observable!='cauchy_phase':
        return ringdown(time_array,mass_detector_solar,spin,reading,strain_amplitude,observable=observable,**base)
    if reading!='R-RAIZ-COHERENT' and reading!='R-LIN':
        raise ValueError('Cauchy readout is provided only for the explicit R-LIN hypothesis')
    # Reuse all physical parameter, time, mode and angular validation in the base.
    carrier=ringdown(time_array,mass_detector_solar,spin,'R-GLOBAL',strain_amplitude,
                     observable='ensemble',**base)
    time=np.asarray(time_array,dtype=float);active=time>=t_start;t=time[active]-t_start
    q=kerr_mode(mass_detector_solar,spin,profile=profile,qnm_dimensionless=qnm_dimensionless,mode=mode)
    if reading=='R-RAIZ-COHERENT':
        if occupation is None:raise ValueError('Explicit occupation required')
        factor,_=coherent_root_factor(t,q['omega_rad_s'],occupation,deformation=deformation,observable=observable,seed=seed)
    else:
        p=prediction(mass_detector_solar,spin,reading,redshift=redshift,profile=profile,qnm_dimensionless=qnm_dimensionless,mode=mode)
        factor=phase_factor(t,deformation*p['gamma_per_s'],process='cauchy',seed=seed)
    factors=((1+math.cos(inclination)**2)/2,math.cos(inclination)) if polarization_factors is None else polarization_factors
    z=strain_amplitude*np.exp(-t/q['tau_gr_s']+1j*(q['omega_rad_s']*t+phase))*factor
    carrier['plus'][active]=factors[0]*z.real;carrier['cross'][active]=factors[1]*z.imag
    return carrier
