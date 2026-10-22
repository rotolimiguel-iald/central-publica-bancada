"""Verbatim native-mode helpers; task-only validator omitted."""
import lal
import lalsimulation as ls
import numpy as np
from pycbc import pnutils

def direct_modes(mass, q, s1, s2, rate):
    m1, m2 = mass*q/(1+q), mass/(1+q)
    nqc = lal.CreateREAL8Vector(10)
    nqc.data[:] = 0.
    pa, tgr = lal.CreateDict(), lal.CreateDict()
    for mode in (220,210,330,440,550):
        getattr(ls, f"SimInspiralWaveformParamsInsertDOmega{mode}")(tgr, 0.)
        getattr(ls, f"SimInspiralWaveformParamsInsertDTau{mode}")(tgr, 0.)
    lal.DictInsertUINT2Value(tgr, "TGRflag", 0)
    result = ls.SimIMRSpinAlignedEOBModes(1./rate, pnutils.solar_mass_to_kg(m1), pnutils.solar_mass_to_kg(m2),
         20., pnutils.megaparsecs_to_meters(403.), s1, s2, 41, *([0.]*8), 1., 1., nqc, 0, pa, tgr)
    modes, low, high = result
    native = modes
    output, timestamps = {}, {}
    while native:
        label = (int(native.l), int(native.m))
        output[label] = np.array(native.mode.data.data)*1e21
        timestamps[label] = float(native.mode.epoch)+np.arange(len(output[label]))*native.mode.deltaT
        native = native.next
    # Dynamics vectors have five contiguous rows: time,r,phase,pr,pphi.
    dt = np.array(high.data)
    if len(dt)%5:
        raise ValueError("Unexpected high-rate dynamics layout")
    time = dt.reshape(5,-1)[0]
    return output, timestamps, dict(high_time_step_M=float(np.median(np.diff(time))),
                                   high_time_step_spread_M=float(np.ptp(np.diff(time))),
                                   high_grid_points=len(time))

def sum_modes(modes, inclination, phase, selection=None):
    output = None
    for (ell,m), h in modes.items():
        if selection is not None and (ell,m) not in selection:
            continue
        phi = np.pi/2-phase
        term = lal.SpinWeightedSphericalHarmonic(inclination,phi,-2,ell,m)*h
        term += (-1)**ell*lal.SpinWeightedSphericalHarmonic(inclination,phi,-2,ell,-m)*h.conj()
        output = term if output is None else output+term
    if output is None:
        raise ValueError("Empty mode selection")
    # Match the explicit -pi/2 EOB-to-LAL polarization rotation in
    # LALSimInspiralGeneratorLegacy.c lines868 and1267-1277.
    p, c = output.real, -output.imag
    cp, sp = np.cos(-np.pi), np.sin(-np.pi)
    return cp*p+sp*c, cp*c-sp*p
