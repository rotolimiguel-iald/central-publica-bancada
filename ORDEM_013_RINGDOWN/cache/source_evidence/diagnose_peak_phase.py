"""Measure phase winding in the unchanged waveform coordinates; no inference."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
import source_evidence as se


def measure(mass, phase=0., s1=.05, s2=-.03, q=39/33):
    m1 = mass*q/(1+q)
    hp, hc = se.model.get_td_waveform(approximant="IMRPhenomXPHM", mass1=m1, mass2=mass-m1,
         spin1x=0., spin1y=0., spin1z=s1, spin2x=0., spin2y=0., spin2z=s2,
         inclination=0., coa_phase=phase, distance=403., delta_t=1/8192, f_lower=20., f_ref=20., mode_array=[(2, 2)])
    t = np.asarray(hp.sample_times)
    p, c = np.asarray(hp)*1e21, np.asarray(hc)*1e21
    i = int(np.argmax(p*p+c*c))
    ps, cs = CubicSpline(t, p), CubicSpline(t, c)
    peak = minimize_scalar(lambda x:-(ps(x)**2+cs(x)**2)/(p[i]**2+c[i]**2),
                           bounds=(t[i-2], t[i+2]), method="bounded", options={"xatol":1e-13})
    return float(np.angle(ps(peak.x)-1j*cs(peak.x))), float(peak.x)


def main():
    rows = []
    for mass in np.linspace(60., 100., 81):
        angle, peak = measure(mass)
        rows.append(dict(mass=float(mass), phase_22_at_peak=angle, peak_generator_s=peak))
    unwrapped = np.unwrap([r["phase_22_at_peak"] for r in rows])
    phases = np.array([0., .1, .2, .4, .8, 1.2])
    phase_values = np.unwrap([measure(72., phase=float(p))[0] for p in phases])
    fit = np.polyfit(phases, phase_values, 1)
    nonlinearity = float(np.max(np.abs(phase_values-np.polyval(fit, phases))))
    spin_rows = []
    for s in np.linspace(-.25, .25, 41):
        angle, peak = measure(72., s1=float(s), s2=float(s))
        spin_rows.append(dict(common_spin=float(s), phase_22_at_peak=angle))
    spin_unwrapped = np.unwrap([r["phase_22_at_peak"] for r in spin_rows])
    report = dict(status="COORDINATE_DIAGNOSTIC_NOT_NEW_MODEL", mass_scan=rows, spin_scan=spin_rows,
                  mass_phase_range_rad=float(np.ptp(unwrapped)), common_spin_phase_range_rad=float(np.ptp(spin_unwrapped)),
                  phase_response_slope=float(fit[0]), phase_response_residual_rad=nonlinearity,
                  conditional_reparameterization="If the orbital phase at peak is reference phase plus an intrinsic-dependent shift modulo2pi, its conditional uniform prior is unchanged; branch consistency and all harmonics need verification before use",
                  interpretation="Large winding can make Gaussian proposals inefficient; this diagnostic does not establish it is the only reason for poor effective sampling",
                  original_likelihood_unchanged=True, source_sha256=se.sha(se.ROOT/se.Path(__file__).name))
    se.write(se.ROOT/"PEAK_PHASE_DIAGNOSTIC.json", report)
    print(json.dumps({k:report[k] for k in ("status", "mass_phase_range_rad", "common_spin_phase_range_rad", "phase_response_slope", "phase_response_residual_rad")}), flush=True)


if __name__ == "__main__":
    main()
