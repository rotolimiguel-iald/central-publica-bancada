"""Combine complete source curves with the existing evidence-mixture reader.

The discrete family prior is identical at every strength. No strength prior
is introduced. Individual numerical failures survive model averaging.
"""
import numpy as np
from continuous_source_calibration import checked_grid
from source_family_mixture import mix_statistics


def mix_curves(strengths, family_values, family_logq, family_statistics,
               family_prior, target_batch=32):
    grid = checked_grid(strengths)
    nf = len(family_values)
    prior = np.asarray(family_prior, dtype=float)
    if (nf < 1 or len(family_logq) != nf or len(family_statistics) != nf or
            prior.shape != (nf,) or not np.isfinite(prior).all() or
            np.any(prior <= 0.) or abs(prior.sum()-1.) > 1e-12 or target_batch < 1):
        raise ValueError('Matching family inputs and normalized positive prior required')
    nc = np.asanyarray(family_values[0]).shape[-1]
    for values, q, statistics in zip(family_values, family_logq, family_statistics):
        if (values.ndim != 3 or len(values) < 2 or values.shape[1:] != (len(grid), nc)
                or np.shape(q) != (len(values),) or not np.isfinite(q).all()):
            raise ValueError('Family source dimensions or density differ')
        for key in ('logz', 'ESS', 'max_weight', 'relative_MC_sd', 'local_precision'):
            if np.shape(statistics[key]) != (len(grid), nc):
                raise ValueError('Family statistics have wrong shape')
        # The mask is derived again, so an optimistic stored flag cannot hide
        # a failing family component in an otherwise dominant mixture.
        expected = ((statistics['ESS'] >= 100.) & (statistics['max_weight'] <= .05)
                    & (statistics['relative_MC_sd'] <= .2))
        if not np.array_equal(expected, statistics['local_precision']):
            raise ValueError('Family precision mask contradicts its diagnostics')
    reference = int(np.flatnonzero(grid == 0.)[0])
    mixed = {k: np.empty((len(grid), nc)) for k in ('logz', 'relative_logz', 'relative_MC_sd')}
    responsibility = np.empty((nf, len(grid), nc))
    contributions = np.empty_like(responsibility)
    family_masks = np.stack([s['local_precision'] for s in family_statistics])
    for first in range(0, nc, target_batch):
        last = min(first+target_batch, nc)
        width = last-first
        for a in range(len(grid)):
            logs, weights = [], []
            for values, q, statistics in zip(family_values, family_logq, family_statistics):
                paired = np.concatenate((values[:, reference, first:last], values[:, a, first:last]), axis=1)
                logz = np.concatenate((statistics['logz'][reference, first:last], statistics['logz'][a, first:last]))
                if np.isnan(paired).any() or np.isposinf(paired).any() or not np.isfinite(logz).all():
                    raise ValueError('Nonfinite family likelihood')
                normalized = np.exp(paired-np.asarray(q)[:, None]-logz[None, :]-np.log(len(values)))
                logs.append(logz); weights.append(normalized)
            result = mix_statistics(np.asarray(logs), weights, prior)
            mixed['logz'][a, first:last] = result['logz'][width:]
            mixed['relative_logz'][a, first:last] = result['lnB']
            mixed['relative_MC_sd'][a, first:last] = result['lnB_MC_sd']
            responsibility[:, a, first:last] = result['family_responsibility'][:, width:]
            contributions[:, a, first:last] = result['family_variance_contributions']
    mixed.update(family_responsibility=responsibility, family_variance_contributions=contributions,
        individual_family_precision=family_masks,
        local_precision=family_masks.all(axis=0) & (mixed['relative_MC_sd'] <= .2))
    return mixed
