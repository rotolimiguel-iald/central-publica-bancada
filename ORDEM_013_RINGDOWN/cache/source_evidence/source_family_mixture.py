"""Two independent source-family integrals, never a product of mock data.

This module combines evidences, not log Bayes factors. The family prior must
be explicit and common to the two point hypotheses. Numerical uncertainty is
conditional on frozen proposals and independent draws between families.
"""
import numpy as np
from scipy.special import logsumexp


def mix_statistics(log_evidences, component_weights, family_prior):
    """Return evidence ratios and paired delta-method Monte Carlo errors.

    Columns are [a=0 targets, a=1 targets]. Within each family the two
    hypotheses use the SAME source draws. Different families use independent
    draws. Component weights include zero-integrand proposals in their rows.
    Low ESS invalidates the error approximation; this routine cannot accept
    a scientific result or override individual-family convergence criteria.
    """
    z = np.asarray(log_evidences, dtype=float)
    prior = np.asarray(family_prior, dtype=float)
    if (z.ndim != 2 or z.shape[1] % 2 or z.shape[1] == 0 or
            not np.all(np.isfinite(z)) or prior.shape != (z.shape[0],) or
            np.any(prior <= 0) or not np.all(np.isfinite(prior)) or
            abs(prior.sum()-1) > 1e-12 or len(component_weights) != len(prior)):
        raise ValueError('Finite paired evidences and normalized positive family prior required')
    logz = logsumexp(z+np.log(prior)[:, None], axis=0)
    responsibility = np.exp(z+np.log(prior)[:, None]-logz[None, :])
    half = z.shape[1]//2
    variance = np.zeros(half)
    contributions = []
    for r, weights in zip(responsibility, component_weights):
        p = np.asarray(weights, dtype=float)
        if (p.ndim != 2 or p.shape[0] < 2 or p.shape[1] != z.shape[1] or
                not np.all(np.isfinite(p)) or np.any(p < 0) or
                np.max(np.abs(p.sum(axis=0)-1)) > 1e-9):
            raise ValueError('Normalized per-component source weights required')
        # Family posterior probabilities can change between a=0 and a=1.
        # Thus each family's influence does NOT have zero sample mean.
        influence = p[:, half:]*r[half:]-p[:, :half]*r[:half]
        influence -= influence.mean(axis=0)
        n = len(p)
        part = (n/(n-1))*np.sum(influence*influence, axis=0)
        contributions.append(part)
        variance += part
    return dict(logz=logz, lnB=logz[half:]-logz[:half],
                family_responsibility=responsibility,
                lnB_MC_sd=np.sqrt(variance),
                family_variance_contributions=np.asarray(contributions))


def source_precision_mask(statistics):
    """Keep individual source components visible even when mixing families."""
    ess, largest = (np.asarray(statistics[k]) for k in ('ESS', 'max_weight'))
    half = len(ess)//2
    return ((np.minimum(ess[:half], ess[half:]) >= 100) &
            (np.maximum(largest[:half], largest[half:]) <= .05) &
            (np.asarray(statistics['lnB_MC_sd']) <= .2))
