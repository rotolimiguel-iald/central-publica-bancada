"""Copied original source integral; same physical source and tolerances.

Only the even-DFT Nyquist convention is corrected. This does not change the
real part returned by the previous interpolant. Full-wave held-out controls
and phase-integral accuracy checks are retained verbatim.
"""
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import peak_phase_coordinates as pc
import real_fourier_phase as real
from phase_marginal_source import six_to_physical

def phase_marginal_loglikes(family, u, state, sample_rate=8192):
    x = six_to_physical(u)
    values = [[], []]
    maximum_interpolation = 0.
    maximum_waveform = 0.
    maximum_quadrature = 0.
    highest_grid = 0
    for psd in ("O4", "O5"):
        white = state[psd+"_white"]
        targets = state[psd+"_targets"]
        bank = pc.phase_bank(family, x, state["times"], white, sample_rate=sample_rate)
        # Each bank is checked at non-grid phases against the original full-wave
        # generator. This is not a Taylor surrogate in the source parameters.
        for phase in (.173, .619, 1.413):
            y = x.copy()
            y[5] = phase
            pair, meta = se.paired_polarizations(family, y, state["times"], sample_rate)
            for a in (0, 1):
                original = se.basis_from_polarizations(pair[a], white)
                interpolated = real.evaluate_bank(bank, [phase], a)[0]
                error = float(np.linalg.norm(original-interpolated)/np.linalg.norm(original))
                _, direct = se.linear_statistics(original, targets, 3.)
                approximate = real.bank_loglikes(bank, [phase], targets, a)
                ll_error = float(np.max(np.abs(direct-approximate)))
                maximum_waveform = max(maximum_waveform, error)
                maximum_interpolation = max(maximum_interpolation, ll_error)
                if error > 1e-6 or ll_error > .001:
                    raise ValueError(f"Full-wave phase interpolation failed: relative={error}, logL={ll_error}, coordinates={x.tolist()}")
        for a in (0, 1):
            n = 512
            while True:
                phases = 2*np.pi*np.arange(n)/n
                logvalues = real.bank_loglikes(bank, phases, targets, a)
                fine = logsumexp(logvalues, axis=0)-np.log(n)
                coarse = logsumexp(logvalues[::2], axis=0)-np.log(n//2)
                error = float(np.max(np.abs(fine-coarse)))
                if error <= 1e-5:
                    maximum_quadrature = max(maximum_quadrature, error)
                    highest_grid = max(highest_grid, n)
                    break
                if n >= 8192:
                    raise ValueError(f"Phase quadrature did not converge: {error}")
                n *= 2
            values[a].extend((fine-state[psd+"_centers"]).tolist())
    result = np.array(values).ravel()
    if not np.all(np.isfinite(result)):
        raise ValueError("Nonfinite phase integral")
    return result, dict(max_logL_interpolation_error=maximum_interpolation,
                        max_relative_waveform_interpolation_error=maximum_waveform,
                        max_phase_quadrature_error=maximum_quadrature, largest_phase_grid=highest_grid)
