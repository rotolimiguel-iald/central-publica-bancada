"""Conditional ensemble ringdown: complete SEOB41 waveform, modified22/44.

No clock/readout is selected implicitly. All input masses are detector-frame.
Distance and polarization are physical common network parameters, never
independent fitted amplitudes per harmonic or detector.
"""
import math
import numpy as np
import native_seob_phase_source as native
import stable_peak_imr_model as model


def prepare_ringdown(coordinates,times,*,sample_rate=8192):
    """Coordinates: log(Mtot/Msun),log(q),chi1z,chi2z,iota,phase,t0_ms.

    times are seconds relative to the intrinsic phase-zero complex22 peak.
    The entire trial interval must be after that peak. No normalization to a
    chosen SNR is performed. This function retains the unchanged other modes.
    """
    x=np.asarray(coordinates,dtype=float)
    t=np.asarray(times,dtype=float)
    if t.ndim!=1 or len(t)<2 or not np.all(np.isfinite(t)) or np.any(np.diff(t)<=0):
        raise ValueError('Expected a finite, strictly increasing time grid')
    if not math.isfinite(sample_rate) or sample_rate<=0:
        raise ValueError('Positive finite generator rate required')
    raw=native.raw_phase_samples('SEOBNRv4HM',x,t,sample_rate=sample_rate)
    raw['coefficients']=np.fft.fft(raw['samples'],axis=0)/raw['n']
    raw['orders']=np.fft.fftfreq(raw['n'])*raw['n']
    return raw


def polarizations(prepared,*,reading,strength,distance_mpc,polarization_rad=0.,phase=None,redshift=0.):
    """Return h_plus,h_cross as dimensionless strain and conditional metadata.

    This is the effective ENSEMBLE envelope of the whole22/44 harmonics, not
    a unique stochastic trajectory or a quantization of Kerr quasinormal modes.
    A coherent-state initial slope is not treated as an exact exponential.
    """
    if reading=='R-RAIZ-COHERENT':
        raise ValueError('An initial coherent-state slope is not a full exponential waveform')
    if not math.isfinite(strength) or strength<0:
        raise ValueError('Nonnegative finite physical dephasing strength required')
    if not math.isfinite(distance_mpc) or distance_mpc<=0 or not math.isfinite(polarization_rad):
        raise ValueError('Positive finite distance and finite polarization required')
    phase=float(prepared['coordinates'][5] if phase is None else phase)
    if not math.isfinite(phase):
        raise ValueError('Finite orbital phase required')
    c=prepared['coefficients']; orders=prepared['orders']
    value=np.einsum('k,kjpt->jpt',np.exp(1j*phase*orders),c,optimize=True)
    if np.max(np.abs(value.imag))>1e-10*max(1.,np.max(np.abs(value.real))):
        raise ValueError('Nonreal finite-mode reconstruction')
    parts=value.real; h=parts[0].copy(); predictions=[]
    for j,ell in enumerate((2,4)):
        spin=prepared['remnant_spin']; spline=model.qnm_splines()[ell]
        if not spline.x[0]<=spin<=spline.x[-1]:
            raise ValueError('Remnant outside the supplied QNM grid')
        p=model.prediction(prepared['remnant_mass'],spin,reading,mode=(ell,ell,0),
                           qnm_dimensionless=complex(spline(spin)),redshift=redshift)
        h+=np.expm1(-strength*p['gamma_per_s']*prepared['times'])[None,:]*parts[j+1]
        predictions.append(p)
    cp,sp=math.cos(2*polarization_rad),math.sin(2*polarization_rad)
    # Matches common-network coefficients (cos2psi,sin2psi) in the reference API.
    hp,hc=cp*h[0]-sp*h[1],sp*h[0]+cp*h[1]
    amplitude=403./distance_mpc*1e-21
    return amplitude*hp,amplitude*hc,dict(family='SEOBNRv4HM',reading=reading,strength=strength,
        predictions=predictions,distance_mpc=distance_mpc,polarization_rad=polarization_rad,
        remnant_mass=prepared['remnant_mass'],remnant_spin=prepared['remnant_spin'],
        peak_generator_s=prepared['peak_generator_s'],native_dynamics=prepared['native_dynamics'],
        physical_clock_selected=False,scope='CONDITIONAL_WHOLE_HARMONIC_ENSEMBLE_ENVELOPE_NOT_CONFIRMED_PHYSICS')

# Deliberate corruption of a disposable verification copy only.
