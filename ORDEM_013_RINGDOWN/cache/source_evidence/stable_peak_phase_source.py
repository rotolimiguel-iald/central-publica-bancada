# Copied phase API with the separately validated phase-zero peak generator.
"""Checked full-phase likelihood for continuous dephasing strength.

Conditional whole-harmonic model, not a physical choice of clock/unraveling.
The source waveform, intrinsic peak, seven source priors and shared amplitude
integration are inherited. No prior for the continuous strength is selected here.
Negative strength is only a phenomenological calibration control, not GKLS.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import stable_peak_imr_model as stable
import peak_phase_coordinates as pc


def raw_phase_samples(family, coordinates, times, n=16, sample_rate=8192):
    """Keep full,22,44 polarizations before whitening or damping."""
    coordinates = np.asarray(coordinates)
    t = np.asarray(times)-coordinates[6]*1e-3
    if t.min()<0:
        raise ValueError("Entire window must lie after trial peak")
    rows = []
    remnants = []
    for phase in 2*np.pi*np.arange(n)/n:
        x = coordinates.copy()
        x[5] = phase
        curves, mf, spin, peak = stable.source_curves(family, tuple(x[:6]), sample_rate, True)
        signals = []
        for name in ("all", "22", "44"):
            p,c,start,end,ratio = curves[name]
            if t.min()<start or (t.max()>end and ratio>1e-5):
                raise ValueError("Incomplete waveform interval")
            hp, hc = np.asarray(p(t)), np.asarray(c(t))
            hp[t>end], hc[t>end] = 0., 0.
            if not np.all(np.isfinite(hp)) or not np.all(np.isfinite(hc)):
                raise ValueError("Nonfinite raw phase sample")
            signals.append(np.array([hp, hc]))
        rows.append(signals)
        remnants.append((mf,spin))
    remnants = np.asarray(remnants)
    if np.max(np.abs(remnants-remnants[0]))>1e-12:
        raise ValueError("Remnant depends on orbital phase")
    return dict(samples=np.array(rows), times=t, remnant_mass=float(remnants[0,0]),
                remnant_spin=float(remnants[0,1]), n=n, sample_rate=sample_rate,
                family=family, coordinates=coordinates.copy())


def make_bank(raw, reading, strengths, white):
    strengths = np.atleast_1d(np.asarray(strengths,dtype=float))
    if not np.all(np.isfinite(strengths)):
        raise ValueError("Nonfinite dephasing strength")
    spin = raw["remnant_spin"]
    rates = []
    for ell in (2,4):
        spline = stable.qnm_splines()[ell]
        if spin<spline.x[0] or spin>spline.x[-1]:
            raise ValueError("Remnant outside validated QNM grid")
        rates.append(stable.prediction(raw["remnant_mass"],spin,reading,mode=(ell,ell,0),
                     qnm_dimensionless=complex(spline(spin)))["gamma_per_s"])
    samples = raw["samples"]
    output = []
    for a in strengths:
        waveform = samples[:,0].copy()
        for j,rate in enumerate(rates):
            # Apply time-domain damping BEFORE the covariance whitener.
            waveform += np.expm1(-a*rate*raw["times"])[None,None,:]*samples[:,j+1]
        output.append([se.basis_from_polarizations(pair,white) for pair in waveform])
    output = np.array(output)
    if not np.all(np.isfinite(output)):
        raise ValueError("Nonfinite damped basis")
    return dict(samples=output, coefficients=np.fft.fft(output,axis=1)/raw["n"],
                orders=np.fft.fftfreq(raw["n"])*raw["n"], n=raw["n"], strengths=strengths,
                reading=reading, rates=np.array(rates), family=raw["family"])


def marginal_loglikes(bank, targets, amplitude_sd=3., tolerance=1e-5, maximum_grid=8192):
    """One independent phase integral per strength and target, no target product."""
    values, controls = [], []
    for i,a in enumerate(bank["strengths"]):
        n = 512
        while True:
            phases = 2*np.pi*np.arange(n)/n
            logl = pc.bank_loglikes(bank,phases,targets,i,amplitude_sd)
            fine = logsumexp(logl,axis=0)-np.log(n)
            coarse = logsumexp(logl[::2],axis=0)-np.log(n//2)
            error = float(np.max(np.abs(fine-coarse)))
            if error<=tolerance:
                values.append(fine)
                controls.append(dict(strength=float(a),phase_grid=n,error=error))
                break
            if n>=maximum_grid:
                raise ValueError(f"Continuous-strength phase quadrature failed: {a},{error}")
            n*=2
    return np.array(values), controls
