"""Worker: one process per case, so native SIGSEGV/abort become return codes.

Modes:
  direct : lalsimulation.SimInspiralChooseTDWaveform with an explicit LALDict (DTau/DOmega)
  bilby  : bilby.gw.source.lal_binary_black_hole exactly as the pilot's pseob_source.py does
Input : JSON on argv[1] = {"mode":..., "cases":[{...}, ...], "progress": path}
Each case is written to the progress file BEFORE the native call (so a crash identifies the case).
"""
import json, sys, time, os
import numpy as np

MSUN = 1.98892e30  # only for direct mode masses; lal.MSUN_SI used when available

def direct_case(c, ls, lal):
    d = lal.CreateDict()
    for k, v in (("DTau220", c.get("dtau220", 0.)), ("DTau440", c.get("dtau440", 0.)),
                 ("DOmega220", c.get("domega220", 0.)), ("DOmega440", c.get("domega440", 0.))):
        getattr(ls, "SimInspiralWaveformParamsInsert" + k)(d, float(v))
    approx = ls.GetApproximantFromString(c.get("approximant", "pSEOBNRv4HM_PA"))
    dt = 1.0 / float(c["fs"])
    t0 = time.perf_counter()
    hp, hc = ls.SimInspiralChooseTDWaveform(
        c["m1"] * lal.MSUN_SI, c["m2"] * lal.MSUN_SI,
        0., 0., c.get("chi1", 0.), 0., 0., c.get("chi2", 0.),
        c.get("dist_Mpc", 403.) * 1e6 * lal.PC_SI, c.get("iota", 0.6), c.get("phase", 0.37), 0., 0., 0.,
        dt, c.get("f_low", 20.), c.get("f_ref", 20.), d, approx)
    wall = time.perf_counter() - t0
    h = hp.data.data + 1j * hc.data.data
    return dict(status="FINITE" if np.isfinite(h).all() else "NONFINITE", n=len(h), dt=dt,
                duration_s=len(h) * dt, wall_s=wall, peak_abs=float(np.max(np.abs(h))),
                epoch=float(hp.epoch))

def bilby_case(c):
    import lal, lalsimulation as ls
    from bilby.gw.source import lal_binary_black_hole
    duration = c.get("duration", 16); fs = c.get("fs", 4096)
    f = np.arange(0, fs / 2 + 1.0 / duration, 1.0 / duration)
    d = lal.CreateDict()
    for k, v in (("DTau220", c.get("dtau220", 0.)), ("DTau440", c.get("dtau440", 0.)),
                 ("DOmega220", c.get("domega220", 0.)), ("DOmega440", c.get("domega440", 0.))):
        getattr(ls, "SimInspiralWaveformParamsInsert" + k)(d, float(v))
    chi1 = c.get("chi1", 0.); chi2 = c.get("chi2", 0.)
    t0 = time.perf_counter()
    r = lal_binary_black_hole(f, c["m1"], c["m2"], c.get("dist_Mpc", 403.),
                              abs(chi1), 0. if chi1 >= 0 else np.pi, 0.,
                              abs(chi2), 0. if chi2 >= 0 else np.pi, 0.,
                              c.get("iota", 0.6), c.get("phase", 0.37),
                              waveform_approximant=c.get("approximant", "pSEOBNRv4HM_PA"),
                              minimum_frequency=20., maximum_frequency=c.get("fmax", 1024.),
                              reference_frequency=20., catch_waveform_errors=True,
                              lal_waveform_dictionary=d)
    wall = time.perf_counter() - t0
    if r is None:
        return dict(status="DOMAIN_RETURNED_NONE", wall_s=wall)
    hp = np.asarray(r["plus"]); m = (f >= 20) & (f <= 1024)
    return dict(status="FINITE" if np.isfinite(hp).all() else "NONFINITE",
                band_norm2=float(np.sum(np.abs(hp[m]) ** 2)), wall_s=wall, n=len(hp))

def main():
    spec = json.load(open(sys.argv[1]))
    prog = open(spec["progress"], "a")
    import lal, lalsimulation as ls
    for i, c in enumerate(spec["cases"]):
        prog.write(json.dumps(dict(begin=i, case=c)) + "\n"); prog.flush(); os.fsync(prog.fileno())
        try:
            out = direct_case(c, ls, lal) if spec["mode"] == "direct" else bilby_case(c)
        except Exception as e:
            out = dict(status="PY_EXCEPTION", error=type(e).__name__ + ": " + str(e)[:200])
        prog.write(json.dumps(dict(end=i, result=out)) + "\n"); prog.flush(); os.fsync(prog.fileno())
    prog.write(json.dumps(dict(done=True, n=len(spec["cases"]))) + "\n"); prog.flush()

if __name__ == "__main__":
    main()
