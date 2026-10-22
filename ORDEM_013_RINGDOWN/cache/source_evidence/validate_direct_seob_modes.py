"""Verify direct SEOB41 modes against the unchanged PyCBC polarization API."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import json
import lal
import lalsimulation as ls
import numpy as np
from pycbc.waveform import get_td_waveform
import source_evidence as se


def direct_modes(mass, q, s1, s2, rate):
    m1, m2 = mass*q/(1+q), mass/(1+q)
    nqc = lal.CreateREAL8Vector(10)
    nqc.data[:] = 0.
    pa, tgr = lal.CreateDict(), lal.CreateDict()
    for mode in (220,210,330,440,550):
        getattr(ls, f"SimInspiralWaveformParamsInsertDOmega{mode}")(tgr, 0.)
        getattr(ls, f"SimInspiralWaveformParamsInsertDTau{mode}")(tgr, 0.)
    lal.DictInsertUINT2Value(tgr, "TGRflag", 0)
    result = ls.SimIMRSpinAlignedEOBModes(1./rate, m1*lal.MSUN_SI, m2*lal.MSUN_SI,
         20., 403.e6*lal.PC_SI, s1, s2, 41, *([0.]*8), 1., 1., nqc, 0, pa, tgr)
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
    return output.real, -output.imag


def main():
    se.check()
    source = next(s for s in se.SOURCES if s["name"]=="source_90")
    x = se.source_vector(source)
    mass, q = np.exp(x[0]), np.exp(x[1])
    rate = 8192
    modes, times, dynamics = direct_modes(mass, q, x[2], x[3], rate)
    rows = []
    for phase in (0., .173, 1.2):
        for inclination in (0., source["inclination"]):
            for selection in (None, [(2,2)], [(4,4)]):
                pars = dict(approximant="SEOBNRv4HM", mass1=mass*q/(1+q), mass2=mass/(1+q),
                            spin1x=0.,spin1y=0.,spin1z=x[2],spin2x=0.,spin2y=0.,spin2z=x[3],
                            distance=403.,delta_t=1./rate,f_lower=20.,f_ref=20.,coa_phase=phase,inclination=inclination)
                if selection is not None:
                    pars["mode_array"] = selection
                hp,hc = get_td_waveform(**pars)
                p,c = sum_modes(modes,inclination,phase,selection)
                tref = times[(2,2)]
                if len(p)!=len(hp) or np.max(np.abs(np.asarray(hp.sample_times)-tref))>1e-12:
                    raise ValueError("Time convention differs")
                direct = np.array([np.asarray(hp),np.asarray(hc)])*1e21
                norm = float(np.linalg.norm(direct))
                error = float(np.linalg.norm(np.array([p,c])-direct)/max(norm,1e-30))
                rows.append(dict(phase=phase,inclination=inclination,selection=selection,relative_error=error,
                                 zero_signal=bool(norm==0.),passes=bool(error<=1e-10)))
    output = dict(status="PASS_DIRECT_SEOB_MODES" if all(r["passes"] for r in rows) else "FAIL_DIRECT_SEOB_MODES",
                  date_utc=datetime.now(timezone.utc).isoformat(),checks=rows,modes=[list(m) for m in modes],
                  count=len(rows),max_relative_error=max(r["relative_error"] for r in rows),dynamics=dynamics,
                  scientific_acceptance=False,scope="Source90 at8192Hz, all registered SEOB modes, three phases and two inclinations; unchanged GR generator, no PA model substitution",
                  source_sha256=se.sha(se.Path(__file__)),lal_commit=ls.SimulationVCSInfo.vcsId)
    se.write(se.ROOT/"DIRECT_SEOB_MODES_VALIDATION.json",output)
    print(json.dumps({k:v for k,v in output.items() if k!="checks"}),flush=True)


if __name__=="__main__":
    main()
