"""Read source-marginal likelihood curves without choosing a strength prior.

The existing paired importance estimator and interval geometry are reused.
These are likelihood-ratio diagnostic intervals of a nuisance-marginal curve,
not Bayesian credible intervals or a theorem of frequentist coverage. Coverage
must be measured using the registered injections. No curve is a new event.
"""
import numpy as np
from importance_source_evidence import importance_statistics
from tgl_ringdown_likelihood import profile_intervals


def checked_grid(strengths):
    grid = np.asarray(strengths, dtype=float)
    if (grid.ndim != 1 or len(grid) < 5 or not np.all(np.isfinite(grid)) or
            np.any(np.diff(grid) <= 0) or np.count_nonzero(grid == 0.) != 1 or
            np.count_nonzero(grid == 1.) != 1):
        raise ValueError('Ordered finite strength grid including zero and one required')
    return grid


def curve_statistics(strengths, log_values, logq, target_batch=32):
    """Integrate all source draws; retain outside-support zero integrands.

    Input shape is (source draw, strength, mock target). Each curve difference
    uses the SAME source draws at a and zero. This accepts a memory map and
    only materializes a pair of strengths for a small batch of targets.
    """
    grid = checked_grid(strengths)
    values = np.asanyarray(log_values)
    q = np.asarray(logq, dtype=float)
    if (values.ndim != 3 or values.shape[0] < 2 or values.shape[1] != len(grid)
            or values.shape[2] < 1 or q.shape != (len(values),)
            or not np.all(np.isfinite(q)) or target_batch < 1):
        raise ValueError('Complete source draws and proposal densities required')
    reference = int(np.flatnonzero(grid == 0.)[0])
    shape = values.shape[1:]
    result = {key: np.empty(shape) for key in
              ('logz', 'ESS', 'max_weight', 'relative_logz', 'relative_MC_sd')}
    for start in range(0, shape[1], target_batch):
        stop = min(start + target_batch, shape[1])
        base = np.asarray(values[:, reference, start:stop])
        for k in range(len(grid)):
            pair = np.concatenate((base, values[:, k, start:stop]), axis=1)
            if (np.any(np.isnan(pair)) or np.any(np.isposinf(pair)) or
                    np.any(~np.any(np.isfinite(pair), axis=0))):
                raise ValueError('Nonfinite or empty likelihood component')
            statistics = importance_statistics(pair, q)
            width = stop - start
            for key in ('logz', 'ESS', 'max_weight'):
                result[key][k, start:stop] = statistics[key][width:]
            result['relative_logz'][k, start:stop] = statistics['lnB']
            result['relative_MC_sd'][k, start:stop] = statistics['lnB_MC_sd']
    result['local_precision'] = ((result['ESS'] >= 100.) &
        (result['max_weight'] <= .05) & (result['relative_MC_sd'] <= .2))
    return result


def read_curves(strengths, statistics, labels, grid_tolerance=.05):
    """Use existing interval geometry, with explicit non-identification flags.

    Comparing every other grid point is a necessary numerical diagnostic,
    never proof of resolution. Boundary and disconnected intervals are kept
    visible. No finite uncertainty or power is invented for them. No failed
    mock is dropped from a cell's denominator.
    """
    grid = checked_grid(strengths)
    logz = np.asarray(statistics['relative_logz'], dtype=float)
    precision = np.asarray(statistics['local_precision'], dtype=bool)
    if (len(grid) % 2 != 1 or logz.shape != (len(grid), len(labels)) or
            precision.shape != logz.shape or not np.all(np.isfinite(logz)) or
            not np.isfinite(grid_tolerance) or grid_tolerance <= 0):
        raise ValueError('Matched finite curves, precision flags and nested grid required')
    fine = profile_intervals(grid, logz)
    coarse = profile_intervals(grid[::2], logz[::2])
    curves = []
    for i, (full, half) in enumerate(zip(fine, coarse)):
        errors = []
        if not bool(precision[:, i].all()):
            errors.append('SOURCE_PRECISION_FAILED')
        if float(np.ptp(logz[:, i])) <= 1e-10:
            errors.append('UNIDENTIFIED_FLAT_CURVE')
        if full['boundary'] or half['boundary']:
            errors.append('INTERVAL_TRUNCATED_BY_GRID')
        if full['islands'] != 1 or half['islands'] != 1:
            errors.append('DISCONNECTED_INTERVAL')
        shift = float(max(abs(full['MLE'] - half['MLE']),
            np.max(np.abs(np.asarray(full['CI90']) - np.asarray(half['CI90'])))))
        if shift > grid_tolerance:
            errors.append('STRENGTH_GRID_UNRESOLVED')
        truth = float(labels[i]['injection_a'])
        if not np.isfinite(truth):
            raise ValueError('Finite injected diagnostic strength required')
        curves.append(dict(label=labels[i], diagnostic=full, coarse_diagnostic=half,
            grid_change=shift, diagnostic_contains_truth=full['CI90'][0] <= truth <= full['CI90'][1],
            numerically_usable=not errors, failures=errors))
    cells = []
    for i, label in enumerate(labels):
        cell = {key: label[key] for key in ('psd', 'source', 'injection_family', 'injection_a', 'snr')}
        if any(row['cell'] == cell for row in cells):
            continue
        selected = [row for row in curves if all(row['label'][k] == v for k, v in cell.items())]
        noises = [row['label']['noise_index'] for row in selected]
        if len(set(noises)) != len(noises):
            raise ValueError('Duplicate noise realization within one calibration cell')
        usable = all(row['numerically_usable'] for row in selected)
        bias = abs(float(np.median([row['diagnostic']['MLE'] for row in selected])) - float(cell['injection_a']))
        coverage = float(np.mean([row['diagnostic_contains_truth'] for row in selected]))
        enough = len(selected) >= 50
        cells.append(dict(cell=cell, N=len(selected), all_curves_usable=usable,
            diagnostic_bias=bias, diagnostic_coverage=coverage,
            calibrated_bias=bias if usable and enough else None,
            calibrated_coverage=coverage if usable and enough else None,
            numerical_and_local_calibration_pass=usable and enough and bias <= .2 and .80 <= coverage <= .97,
            failed_curves=sum(not row['numerically_usable'] for row in selected)))
    return dict(curves=curves, cells=cells, strength_prior_selected=False,
        interval_kind='Likelihood-ratio diagnostic of source-marginal curve; empirical coverage required',
        scientific_acceptance=False, independent_repeat_verified=False,
        waveform_rate_verified=False, all_source_and_strength_checks_complete=False)
