"""Generate the same SEOB41 phase bank with one native modes call.

This is a numerical adapter, not a new family or a change to the source prior.
Peak location still uses the unchanged PyCBC face-on, phase-zero 22 waveform.
The public make_bank function applies 22/44 damping before whitening.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from pycbc.waveform import get_td_waveform
from direct_seob_modes import direct_modes, sum_modes
import stable_peak_imr_model as stable


def phase_zero_peak(mass, q, s1, s2, rate):
    pars=dict(mass1=mass*q/(1+q), mass2=mass/(1+q), spin1z=s1, spin2z=s2,
              spin1x=0.,spin1y=0.,spin2x=0.,spin2y=0.,inclination=0.,coa_phase=0.,
              distance=403.,delta_t=1/rate,f_lower=20.,f_ref=20.,
              approximant='SEOBNRv4HM',mode_array=[(2,2)])
    hp,hc=get_td_waveform(**pars)
    t=np.asarray(hp.sample_times); p=np.asarray(hp)*1e21; c=np.asarray(hc)*1e21
    index=int(np.argmax(p*p+c*c)); amplitude=p[index]**2+c[index]**2
    sp,sc=CubicSpline(t,p),CubicSpline(t,c)
    peak=minimize_scalar(lambda x:-(float(sp(x))**2+float(sc(x))**2)/amplitude,
                         bounds=(t[index-2],t[index+2]),method='bounded',options={'xatol':1e-13})
    if not peak.success:
        raise ValueError('Phase-zero peak alignment failed')
    return float(peak.x)


def raw_phase_samples(family, coordinates, times, n=16, sample_rate=8192):
    if family!='SEOBNRv4HM':
        raise ValueError('This separately validated adapter is for native SEOB41 only')
    x=np.asarray(coordinates,dtype=float)
    if x.shape!=(7,) or not np.all(np.isfinite(x)):
        raise ValueError('Expected seven finite physical source coordinates')
    mass,q=np.exp(x[0]),np.exp(x[1]); s1,s2=x[2:4]
    if not 1<=q<=4 or max(abs(s1),abs(s2))>.8 or not 0<x[4]<np.pi:
        raise ValueError('Unphysical source')
    t=np.asarray(times)-x[6]*1e-3
    if t.min()<0:
        raise ValueError('Entire interval must lie after trial peak')
    peak=phase_zero_peak(mass,q,s1,s2,sample_rate)
    modes,timestamps,dynamics=direct_modes(mass,q,s1,s2,sample_rate)
    expected={(2,2),(2,1),(3,3),(4,4),(5,5)}
    if set(modes)!=expected:
        raise ValueError('Registered SEOB mode set changed')
    tref=timestamps[(2,2)]
    for tm in timestamps.values():
        if len(tm)!=len(tref) or not np.array_equal(tm,tref):
            raise ValueError('Native mode time grids differ')
    start,end=float(tref[0]-peak),float(tref[-1]-peak)
    if t.min()<start:
        raise ValueError('Missing early waveform interval')
    sampled={}
    for label,h in modes.items():
        sampled[label]=np.asarray(CubicSpline(tref-peak,h,extrapolate=False)(t))
        sampled[label][t>end]=0.
        if not np.all(np.isfinite(sampled[label])):
            raise ValueError('Nonfinite interpolated native mode')
    rows=[]
    for phase in 2*np.pi*np.arange(n)/n:
        parts=[]
        for selection in (None,[(2,2)],[(4,4)]):
            if t.max()>end:
                p,c=sum_modes(modes,x[4],phase,selection)
                ratio=np.hypot(p[-1],c[-1])/max(np.hypot(p,c))
                if ratio>1e-5:
                    raise ValueError('Missing non-negligible late waveform')
            parts.append(np.array(sum_modes(sampled,x[4],phase,selection)))
        rows.append(parts)
    mf,spin=stable.remnant(family,mass*q/(1+q),mass/(1+q),s1,s2)
    return dict(samples=np.array(rows), times=t, remnant_mass=mf, remnant_spin=spin,
                n=n,sample_rate=sample_rate,family=family,coordinates=x.copy(),
                peak_generator_s=peak,native_dynamics=dynamics,
                scope='All five native SEOB41 positive modes plus their negative-m partners; unchanged source prior')
