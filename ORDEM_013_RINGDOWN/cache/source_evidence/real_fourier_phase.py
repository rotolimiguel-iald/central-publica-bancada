"""Real trigonometric interpolation of a complete-wave phase bank.

An even DFT's Nyquist coefficient represents a cosine for real interpolation,
not one unpaired complex exponential. Original real outputs are preserved;
coefficient/sample consistency and conjugate symmetry remain checked.
"""
import numpy as np


def phase_matrix(bank, phases, hypothesis):
    phases = np.atleast_1d(np.asarray(phases, dtype=float))
    n = bank['n']
    if (not isinstance(n, (int, np.integer)) or n < 3 or phases.ndim != 1 or
            phases.size == 0 or not np.all(np.isfinite(phases))):
        raise ValueError('Finite phases and a valid phase-bank size required')
    samples = np.asarray(bank['samples'][hypothesis])
    c = np.asarray(bank['coefficients'][hypothesis])
    orders = np.fft.fftfreq(n)*n
    if (samples.ndim != 3 or samples.shape[0] != n or samples.shape[-1] != 2 or
            np.iscomplexobj(samples) or samples.shape != c.shape or
            not np.all(np.isfinite(samples)) or not np.all(np.isfinite(c)) or
            not np.array_equal(np.asarray(bank['orders']), orders)):
        raise ValueError('Invalid real complete-wave phase bank')
    expected = np.fft.fft(samples, axis=0)/n
    tolerance = 64*np.finfo(float).eps*max(1., float(np.max(np.abs(expected))))
    if np.max(np.abs(c-expected)) > tolerance:
        raise ValueError('Phase coefficients do not match recorded real samples')
    if np.max(np.abs(c-np.conj(c[(-np.arange(n)) % n]))) > tolerance:
        raise ValueError('Phase coefficients violate real conjugate symmetry')
    matrix = np.exp(1j*np.outer(phases, orders))
    if n % 2 == 0:
        matrix[:, n//2] = np.cos((n//2)*phases)
    return matrix, c


def evaluate_bank(bank, phases, hypothesis):
    matrix, c = phase_matrix(bank, phases, hypothesis)
    value = np.einsum('pk,ktj->ptj', matrix, c, optimize=True)
    bound = 128*np.finfo(float).eps*max(1., float(np.max(np.sum(np.abs(c), axis=0))))
    if np.max(np.abs(value.imag)) > bound:
        raise ValueError('Real Fourier interpolant has residual imaginary leakage')
    return value.real


def bank_loglikes(bank, phases, targets, hypothesis, amplitude_sd=3.):
    if not np.isfinite(amplitude_sd) or amplitude_sd <= 0:
        raise ValueError('Positive amplitude prior width required')
    matrix, c = phase_matrix(bank, phases, hypothesis)
    basis = evaluate_bank(bank, phases, hypothesis)
    targets = np.atleast_2d(np.asarray(targets, dtype=float))
    if not np.all(np.isfinite(targets)):
        raise ValueError('Nonfinite target')
    gram = np.einsum('pti,ptj->pij', basis, basis, optimize=True)
    rhs_c = np.einsum('kti,dt->kdi', c, targets, optimize=True)
    rhs = np.einsum('pk,kdi->pdi', matrix, rhs_c, optimize=True).real
    aa, bb, cc = gram[:, 0, 0]+1/amplitude_sd**2, gram[:, 0, 1], gram[:, 1, 1]+1/amplitude_sd**2
    det = aa*cc-bb*bb
    if np.any(det <= 0) or not np.all(np.isfinite(det)):
        raise ValueError('Invalid common-amplitude covariance')
    quadratic = (cc[:, None]*rhs[:, :, 0]**2-2*bb[:, None]*rhs[:, :, 0]*rhs[:, :, 1]+aa[:, None]*rhs[:, :, 1]**2)/det[:, None]
    result = .5*quadratic-.5*np.log(det*amplitude_sd**4)[:, None]
    if not np.all(np.isfinite(result)):
        raise ValueError('Nonfinite phase likelihood')
    return result
