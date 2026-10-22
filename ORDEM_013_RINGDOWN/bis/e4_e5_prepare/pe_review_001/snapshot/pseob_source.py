"""Explicit aligned-spin pSEOBNRv4HM_PA source for the registered pilot.

Source preparation only. No waveform is computed on import. Masses are detector
frame solar masses; distance Mpc; deformation parameters are fractional QNM
frequency/damping-time changes in LAL's pSEOB convention.
"""
import numpy as np
import time

STOP_UTC_TIMESTAMP = None
COST_COUNTER = None

def set_deadline(timestamp):
    global STOP_UTC_TIMESTAMP
    if not np.isfinite(timestamp) or timestamp<=time.time():raise ValueError('Invalid source deadline')
    STOP_UTC_TIMESTAMP=float(timestamp)

def set_cost_counter(counter):
    global COST_COUNTER
    COST_COUNTER=counter

def validate_polarizations(result,frequencies,minimum,maximum):
    if result is None:return None
    f=np.asarray(frequencies,dtype=float)
    if f.ndim!=1 or len(f)<2 or not np.isfinite(f).all() or not np.all(np.diff(f)>0):raise ValueError('Invalid frequency grid')
    if not isinstance(result,dict) or not {'plus','cross'}<=set(result):raise RuntimeError('Malformed waveform response')
    arrays=[np.asarray(result[k]) for k in ('plus','cross')]
    if any(a.shape!=f.shape or not np.isfinite(a).all() for a in arrays):raise RuntimeError('Nonfinite/wrong-shape waveform')
    mask=(f>=minimum)&(f<=maximum)
    if not mask.any() or not any(np.any(a[mask]!=0) for a in arrays):raise RuntimeError('Jointly zero active-band waveform')
    return result

def pseob_frequency_domain(frequency_array, mass_1, mass_2,
        luminosity_distance, chi_1, chi_2, theta_jn, phase,
        dtau220, dtau440, domega220=0., domega440=0., geocent_time=None, **kwargs):
    if STOP_UTC_TIMESTAMP is not None and time.time()>=STOP_UTC_TIMESTAMP:raise TimeoutError('Source deadline reached')
    import lal
    import lalsimulation as ls
    from bilby.gw.source import lal_binary_black_hole
    values=[mass_1,mass_2,luminosity_distance,chi_1,chi_2,theta_jn,
            phase,dtau220,dtau440,domega220,domega440]
    if not np.isfinite(values).all():raise ValueError('Nonfinite waveform parameters')
    if mass_1<=0 or mass_2<=0 or luminosity_distance<=0:raise ValueError('Invalid physical scale')
    if abs(chi_1)>=1 or abs(chi_2)>=1:raise ValueError('Spin outside supported Kerr range')
    if dtau220<=-1 or dtau440<=-1 or domega220<=-1 or domega440<=-1:raise ValueError('Invalid fractional QNM parameter')
    # Conservative LAL temporal bounds; failure aborts PE, never trims the prior.
    timing=kwargs.pop('analysis_time_contract',None)
    if timing is None or geocent_time is None or not np.isfinite(geocent_time):raise ValueError('Analysis time contract required')
    m1=mass_1*lal.MSUN_SI;m2=mass_2*lal.MSUN_SI
    inspiral=ls.SimInspiralChirpTimeBound(kwargs['minimum_frequency'],m1,m2,chi_1,chi_2)
    merger=ls.SimInspiralMergeTimeBound(m1,m2)
    spin_bound=ls.SimInspiralFinalBlackHoleSpinBound(chi_1,chi_2)
    tail=ls.SimInspiralRingdownTimeBound(m1+m2,spin_bound)*max(1.,1+dtau220,1+dtau440)
    if not np.isfinite([inspiral,merger,tail]).all() or min(inspiral,merger,tail)<0:raise RuntimeError('Invalid LAL duration bounds')
    lower=timing['start_GPS']+timing['roll_off_s'];upper=timing['start_GPS']+timing['duration_s']-timing['roll_off_s']
    if geocent_time-inspiral-merger<lower or geocent_time+tail>upper:
        raise RuntimeError('WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION; widen registered segment')
    if kwargs.get('waveform_approximant','pSEOBNRv4HM_PA')!='pSEOBNRv4HM_PA':raise ValueError('Unregistered approximant')
    # A fresh dictionary per evaluation prevents parameter leakage between calls.
    if 'lal_waveform_dictionary' in kwargs:raise ValueError('Caller must not override deformation dictionary')
    if any(k in kwargs for k in ('DTau220','DTau440','DOmega220','DOmega440')):raise ValueError('Duplicate deformation override')
    dictionary=lal.CreateDict()
    for name,value in [('DTau220',dtau220),('DTau440',dtau440),
                       ('DOmega220',domega220),('DOmega440',domega440)]:
        getattr(ls,'SimInspiralWaveformParamsInsert'+name)(dictionary,float(value))
    options=dict(kwargs,waveform_approximant='pSEOBNRv4HM_PA',lal_waveform_dictionary=dictionary)
    started=time.perf_counter()
    try:
        result=lal_binary_black_hole(frequency_array,mass_1,mass_2,
            luminosity_distance,abs(chi_1),0. if chi_1>=0 else np.pi,0.,
            abs(chi_2),0. if chi_2>=0 else np.pi,0.,theta_jn,phase,**options)
    finally:
        if COST_COUNTER is not None:
            with COST_COUNTER.get_lock():
                COST_COUNTER[0]+=1;COST_COUNTER[1]+=time.perf_counter()-started
    return validate_polarizations(result,frequency_array,kwargs['minimum_frequency'],kwargs['maximum_frequency'])

def parameter_conversion(parameters):
    """Preserve source parameters; add only the mass-order constraint coordinate."""
    out=dict(parameters)
    if 'mass_1' in out and 'mass_2' in out:
        out['mass_ratio']=out['mass_2']/out['mass_1']
    return out, ['mass_ratio'] if 'mass_ratio' not in parameters else []
