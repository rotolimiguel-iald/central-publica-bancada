"""Existing continuous-strength integral with the validated real phase reader.

This API selects no strength prior or physical interpretation. Negative strength
is a numerical estimator control only. No new physical dynamics are introduced.
"""
import numpy as np
from scipy.special import logsumexp
from continuous_phase_source import raw_phase_samples, make_bank
import real_fourier_phase as real


def marginal_loglikes(bank, targets, amplitude_sd=3.0, tolerance=1e-05, maximum_grid=8192):
    """One independent phase integral per strength and target, no target product."""
    values, controls = ([], [])
    for i, a in enumerate(bank['strengths']):
        n = 512
        while True:
            phases = 2 * np.pi * np.arange(n) / n
            logl = real.bank_loglikes(bank, phases, targets, i, amplitude_sd)
            fine = logsumexp(logl, axis=0) - np.log(n)
            coarse = logsumexp(logl[::2], axis=0) - np.log(n // 2)
            error = float(np.max(np.abs(fine - coarse)))
            if error <= tolerance:
                values.append(fine)
                controls.append(dict(strength=float(a), phase_grid=n, error=error))
                break
            if n >= maximum_grid:
                raise ValueError(f'Continuous-strength phase quadrature failed: {a},{error}')
            n *= 2
    return (np.array(values), controls)
