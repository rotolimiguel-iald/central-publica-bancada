"""Explicit aligned-spin pSEOBNRv4HM_PA source for the registered pilot.

Source preparation only. No waveform is computed on import. Masses are detector
frame solar masses; distance Mpc; deformation parameters are fractional QNM
frequency/damping-time changes in LAL's pSEOB convention.
"""
import numpy as np

def pseob_frequency_domain(frequency_array, mass_1, mass_2,
        luminosity_distance, chi_1, chi_2, theta_jn, phase,
        dtau220, dtau440, domega220=0., domega440=0., **kwargs):
    import lal
    import lalsimulation as ls
    from bilby.gw.source import lal_binary_black_hole
    values=[mass_1,mass_2,luminosity_distance,chi_1,chi_2,theta_jn,
            phase,dtau220,dtau440,domega220,domega440]
    if not np.isfinite(values).all():raise ValueError('Nonfinite waveform parameters')
    if mass_1<=0 or mass_2<=0 or luminosity_distance<=0:raise ValueError('Invalid physical scale')
    if abs(chi_1)>=1 or abs(chi_2)>=1:raise ValueError('Spin outside supported Kerr range')
    if dtau220<=-1 or dtau440<=-1 or domega220<=-1 or domega440<=-1:raise ValueError('Invalid fractional QNM parameter')
    if kwargs.get('waveform_approximant','pSEOBNRv4HM_PA')!='pSEOBNRv4HM_PA':raise ValueError('Unregistered approximant')
    # A fresh dictionary per evaluation prevents parameter leakage between calls.
    if 'lal_waveform_dictionary' in kwargs:raise ValueError('Caller must not override deformation dictionary')
    dictionary=lal.CreateDict()
    for name,value in [('DTau220',dtau220),('DTau440',dtau440),
                       ('DOmega220',domega220),('DOmega440',domega440)]:
        getattr(ls,'SimInspiralWaveformParamsInsert'+name)(dictionary,float(value))
    options=dict(kwargs,waveform_approximant='pSEOBNRv4HM_PA',lal_waveform_dictionary=dictionary)
    return lal_binary_black_hole(frequency_array,mass_1,mass_2,
        luminosity_distance,abs(chi_1),0. if chi_1>=0 else np.pi,0.,
        abs(chi_2),0. if chi_2>=0 else np.pi,0.,theta_jn,phase,**options)

def parameter_conversion(parameters):
    """Preserve source parameters; add only the mass-order constraint coordinate."""
    out=dict(parameters)
    if 'mass_1' in out and 'mass_2' in out:
        out['mass_ratio']=out['mass_2']/out['mass_1']
    return out, ['mass_ratio'] if 'mass_ratio' not in parameters else []
