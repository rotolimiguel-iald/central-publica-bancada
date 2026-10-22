"""Continuous-strength source curves with original full-wave held-out checks.

No changed prior, clock or dynamics. SEOB uses its previously validated native
phase bank; Phenom uses the original complete waveform. Every new strength is
checked at all three held-out phases before its phase integral is accepted.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import numpy as np
import source_evidence as se
from phase_marginal_source import six_to_physical
import real_continuous_phase_source as api
import real_fourier_phase as real
import native_seob_phase_source as native


def evaluate(family, u, state, strengths, reading='R-B', sample_rate=8192):
    strengths = np.asarray(strengths, dtype=float)
    if strengths.ndim != 1 or not len(strengths) or not np.all(np.isfinite(strengths)):
        raise ValueError('Finite diagnostic strengths required')
    x = six_to_physical(u)
    raw_reader = native.raw_phase_samples if family == 'SEOBNRv4HM' else api.raw_phase_samples
    raw = raw_reader(family, x, state['times'], sample_rate=sample_rate)
    direct = {}
    for phase in (.173, .619, 1.413):
        y = x.copy(); y[5] = phase
        direct[phase] = []
        for a in strengths:
            hp, hc, _ = se.model.polarizations(family, y, state['times'], reading, float(a), sample_rate)
            direct[phase].append(np.array([hp, hc]))
    values, controls = [], []
    for psd in ('O4', 'O5'):
        white, targets = state[psd + '_white'], state[psd + '_targets']
        bank = api.make_bank(raw, reading, strengths, white)
        max_wave = max_logl = 0.
        for phase, polarizations in direct.items():
            for k, pair in enumerate(polarizations):
                original = se.basis_from_polarizations(pair, white)
                approx = real.evaluate_bank(bank, [phase], k)[0]
                relative = float(np.linalg.norm(original - approx) / np.linalg.norm(original))
                _, exact = se.linear_statistics(original, targets, 3.)
                error = float(np.max(np.abs(exact - real.bank_loglikes(bank, [phase], targets, k))))
                max_wave, max_logl = max(max_wave, relative), max(max_logl, error)
                if relative > 1e-6 or error > .001:
                    raise ValueError(f'Continuous full-wave control failed:{family},{phase},{strengths[k]},{relative},{error}')
        integrated, quadrature = api.marginal_loglikes(bank, targets)
        values.append(integrated - state[psd + '_centers'][None, :])
        controls.append(dict(psd=psd, max_relative_wave_error=max_wave, max_logL_error=max_logl,
            full_wave_checks=len(strengths)*len(direct), phase_quadrature=quadrature))
    result = np.concatenate(values, axis=1)
    if not np.all(np.isfinite(result)):
        raise ValueError('Nonfinite complete continuous source curve')
    return result, dict(controls=controls, reading=reading, sample_rate=sample_rate,
        native_seob=family == 'SEOBNRv4HM', physical_prior_changed=False)
