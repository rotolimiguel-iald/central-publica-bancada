"""Conditional TGL single-mode waveform; numpy only, default 220.

CONVENTION: Gamma damps ensemble AMPLITUDE, coherent power by 2*Gamma.
It does not remove oscillator energy. A single stochastic phase realization
has the GR envelope; the generator alone does not select this unraveling.

Units: seconds, Hz, dimensionless strain, detector-frame mass and clock.
h_plus = A (1+cos(iota)^2)/2 exp(-t/tau) cos(omega*t+phase).
h_cross = A cos(iota) exp(-t/tau) sin(omega*t+phase).
Thus h_plus-i*h_cross has exp(-i*omega*t) for face-on orientation,
matching the right-circular convention of LVK arXiv:2509.08099 eq. (1).
phase is the mode phase, not the orbital phase; onset is fixed explicitly.
Higher modes require an exact QNM and explicit (plus, cross) angular factors
in this cosine/sine convention. The 220 inclination factors are never reused
silently for 440 or for another mode. Combine modes by summing polarizations.
The output dict has the plus/cross keys used by Bilby time-domain sources.
For Bilby WaveformGenerator, include the fixed `reading` string and all
positional fit parameters in `parameters`; use an identity conversion.
Keep source options (qnm_dimensionless, observable, profile) in waveform_arguments.
PyCBC users may wrap these arrays with TimeSeries(delta_t=..., epoch=...).
Not a drop-in modification of an IMR merger, nor a pyRing likelihood.
"""
import math
import numpy as np
from tgl_ringdown_prediction import prediction

def ringdown(time_array, mass_detector_solar, spin, reading, strain_amplitude,
             t_start=0., phase=0., inclination=0., deformation=1., redshift=0.,
             *,
             qnm_dimensionless=None, observable='ensemble', seed=None, occupation=None,mode=(2,2,0),
             polarization_factors=None,
             profile='CODATA2018_IAU2015'):
    time=np.asarray(time_array,dtype=float)
    if time.ndim!=1 or len(time)<2 or not np.all(np.isfinite(time)) or not np.all(np.diff(time)>0):
        raise ValueError('Finite strictly increasing one-dimensional times required')
    if not all(math.isfinite(x) for x in (strain_amplitude,t_start,phase,inclination,deformation)):
        raise ValueError('Finite parameters required')
    if strain_amplitude<0 or deformation<0:
        raise ValueError('Negative amplitude or anti-dephasing is not admissible')
    if polarization_factors is None:
        if tuple(mode)!=(2,2,0):
            raise ValueError('Higher mode requires explicit angular projection factors; do not reuse the 220 inclination pattern')
        ci=math.cos(inclination)
        factors=((1+ci*ci)/2,ci)
    else:
        if len(polarization_factors)!=2 or not all(math.isfinite(x) for x in polarization_factors):
            raise ValueError('Two finite angular projection factors required')
        factors=polarization_factors
    if observable not in ('ensemble','brownian_phase'):
        raise ValueError('Choose ensemble or explicit brownian_phase unraveling')
    if reading=='R-RAIZ-COHERENT':
        raise ValueError('Root coherent field is generally nonexponential; use its Poisson sum')
    if observable=='brownian_phase' and reading not in ('R-A','R-B','R-MOD','R-GLOBAL'):
        raise ValueError('Brownian time noise is only the explicit quadratic-gap unraveling')
    pred=prediction(mass_detector_solar,spin,reading,redshift=redshift,
                    qnm_dimensionless=qnm_dimensionless,occupation=occupation,profile=profile,mode=mode)
    gamma=deformation*pred['gamma_per_s']
    active=time>=t_start
    elapsed=time[active]-t_start
    angle=pred['omega_rad_s']*elapsed+phase
    decay=1/pred['tau_gr_s']
    if observable=='ensemble':
        decay+=gamma
    else:
        if seed is None:
            raise ValueError('Explicit random seed required for a reproducible realization')
        increments=np.diff(np.r_[0.,elapsed])
        angle+=np.cumsum(np.random.default_rng(seed).normal(size=len(elapsed))*np.sqrt(2*gamma*increments))
    envelope=strain_amplitude*np.exp(-decay*elapsed)
    plus=np.zeros_like(time); cross=np.zeros_like(time)
    plus[active]=envelope*factors[0]*np.cos(angle)
    cross[active]=envelope*factors[1]*np.sin(angle)
    return {'plus':plus,'cross':cross}

def damped_cosine_fourier(frequency_array, amplitude, frequency_hz, decay_per_s, phase=0.):
    """Integral from 0 to infinity, Fourier exp(-2*pi*i*f*t), a real cosine."""
    freq=np.asarray(frequency_array,dtype=float)
    if decay_per_s<=0 or frequency_hz<=0:
        raise ValueError('Positive frequency and damping rate required')
    return amplitude/2*(np.exp(1j*phase)/(decay_per_s+2j*np.pi*(freq-frequency_hz))+
                        np.exp(-1j*phase)/(decay_per_s+2j*np.pi*(freq+frequency_hz)))
