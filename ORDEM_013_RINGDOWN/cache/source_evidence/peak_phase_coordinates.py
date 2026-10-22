"""Prior-preserving orbital phase coordinates and complete-wave phase controls."""
from functools import lru_cache
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp
import source_evidence as se


@lru_cache(maxsize=32)
def peak_reference_phase(family, intrinsic, sample_rate=8192):
    lm, lq, s1, s2 = intrinsic
    mass, q = np.exp(lm), np.exp(lq)
    m1 = mass*q/(1+q)
    hp, hc = se.model.get_td_waveform(approximant=family, mass1=m1, mass2=mass-m1,
        spin1x=0., spin1y=0., spin1z=s1, spin2x=0., spin2y=0., spin2z=s2,
        inclination=0., coa_phase=0., distance=403., delta_t=1/sample_rate,
        f_lower=20., f_ref=20., mode_array=[(2, 2)])
    t, p, c = np.asarray(hp.sample_times), np.asarray(hp)*1e21, np.asarray(hc)*1e21
    i = int(np.argmax(p*p+c*c))
    ps, cs = CubicSpline(t, p), CubicSpline(t, c)
    peak = minimize_scalar(lambda x:-(ps(x)**2+cs(x)**2)/(p[i]**2+c[i]**2),
             bounds=(t[i-2], t[i+2]), method="bounded", options={"xatol":1e-13})
    if not peak.success:
        raise ValueError("Intrinsic phase reference failed")
    return float(np.angle(ps(peak.x)-1j*cs(peak.x)))


def prior_transform(u):
    x = se.prior_transform(u)
    x[5] *= .5  # zeta uniform on [0,pi); both preimages integrated below.
    return x


def reference_branches(family, peak_coordinates):
    x = np.array(peak_coordinates, dtype=float)
    if x.shape != (7,) or not 0 <= x[5] < np.pi:
        raise ValueError("Expected phase-at-peak coordinate in [0,pi)")
    # Coordinate chart is fixed at8192Hz even in a template-rate control.
    b = peak_reference_phase(family, tuple(x[:4]), 8192)
    out = []
    for j in (0, 1):
        y = x.copy()
        y[5] = (x[5]+b/2+j*np.pi)%(2*np.pi)
        out.append(y)
    return out


def loglikes(family, peak_coordinates, state, sample_rate=8192):
    values = [se.component_loglikes(family, branch, state, sample_rate) for branch in reference_branches(family, peak_coordinates)]
    return np.logaddexp(values[0], values[1])-np.log(2.)


def phase_bank(family, coordinates, times, white, n=16, sample_rate=8192):
    """Finite Fourier control built from COMPLETE original waveform evaluations.

    No harmonic is dropped. Interpolation must pass held-out phase controls.
    This representation accelerates only phase quadrature, not intrinsic physics.
    """
    phases = 2*np.pi*np.arange(n)/n
    arrays = [[], []]
    for phase in phases:
        x = np.array(coordinates, copy=True)
        x[5] = phase
        pair, meta = se.paired_polarizations(family, x, times, sample_rate)
        for a in (0, 1):
            arrays[a].append(se.basis_from_polarizations(pair[a], white))
    data = np.array(arrays)
    coefficients = np.fft.fft(data, axis=1)/n
    return dict(orders=np.fft.fftfreq(n)*n, coefficients=coefficients, n=n,
                samples=data, phase_reference=peak_reference_phase(family, tuple(coordinates[:4])), family=family)


def evaluate_bank(bank, phases, hypothesis):
    exponential = np.exp(1j*np.outer(np.atleast_1d(phases), bank["orders"]))
    c = bank["coefficients"][hypothesis]
    result = np.einsum("pk,ktj->ptj", exponential, c, optimize=True)
    if np.max(np.abs(result.imag)) > 1e-7*max(1., np.max(np.abs(result.real))):
        raise ValueError("Fourier phase control has a non-real reconstruction")
    return result.real


def bank_loglikes(bank, phases, targets, hypothesis, amplitude_sd=3.):
    """Exact two-coefficient Gaussian integral after phase interpolation."""
    exponential = np.exp(1j*np.outer(np.atleast_1d(phases), bank["orders"]))
    c = bank["coefficients"][hypothesis]
    basis = evaluate_bank(bank, phases, hypothesis)
    gram = np.einsum("pti,ptj->pij", basis, basis, optimize=True)
    rhs_c = np.einsum("kti,dt->kdi", c, np.atleast_2d(targets), optimize=True)
    rhs = np.einsum("pk,kdi->pdi", exponential, rhs_c, optimize=True).real
    aa, bb, cc = gram[:, 0, 0]+1/amplitude_sd**2, gram[:, 0, 1], gram[:, 1, 1]+1/amplitude_sd**2
    det = aa*cc-bb*bb
    if np.any(det <= 0):
        raise ValueError("Common-amplitude covariance is not positive")
    quadratic = (cc[:, None]*rhs[:, :, 0]**2-2*bb[:, None]*rhs[:, :, 0]*rhs[:, :, 1]+aa[:, None]*rhs[:, :, 1]**2)/det[:, None]
    return .5*quadratic-.5*np.log(det*amplitude_sd**4)[:, None]


def phase_integral(bank, targets, hypothesis, n=512, transformed=False):
    if transformed:
        zeta = np.pi*np.arange(n//2)/(n//2)
        b = bank["phase_reference"]
        zero = bank_loglikes(bank, zeta+b/2, targets, hypothesis)
        one = bank_loglikes(bank, zeta+b/2+np.pi, targets, hypothesis)
        return logsumexp(np.logaddexp(zero, one)-np.log(2.), axis=0)-np.log(n//2)
    phases = 2*np.pi*np.arange(n)/n
    return logsumexp(bank_loglikes(bank, phases, targets, hypothesis), axis=0)-np.log(n)
