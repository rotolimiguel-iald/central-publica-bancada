"""Independent integral/interval oracles and fail-closed controls, no strain fit."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import numpy as np
from scipy.special import logsumexp, ndtri
import source_evidence as se
from continuous_source_calibration import curve_statistics, read_curves

STAGE = se.ROOT / 'continuous_calibration_validation'


def labels(count, injection=0.):
    return [dict(psd='ORACLE', source='analytic', injection_family='analytic',
        injection_a=injection, snr=0., noise_index=i) for i in range(count)]


def fake_statistics(curves):
    return dict(relative_logz=curves, local_precision=np.ones(curves.shape, dtype=bool))


def main():
    se.check()
    STAGE.mkdir(exist_ok=False)
    names = ['validate_continuous_calibration.py', 'continuous_source_calibration.py',
        'importance_source_evidence.py', 'tgl_ringdown_likelihood.py']
    se.write(STAGE / 'REGISTRATION.json', dict(date_utc=datetime.now(timezone.utc).isoformat(),
        seed=131002, source_draws=32768, finite_integral_oracle='192-point Gauss-Legendre',
        hashes={n: se.sha(se.ROOT / n) for n in names}, scientific_acceptance=False))
    grid = np.linspace(-4., 4., 81)
    # Zero/one are exact endpoints of the arithmetic progression in NumPy here.
    if np.count_nonzero(grid == 1.) != 1:
        raise ValueError('Unexpected floating grid representation')
    u = np.random.default_rng(131002).uniform(size=32768)
    centers = np.array([-.3, 0., .7])
    values = -.5*((grid[None, :, None]-centers[None, None, :]-.4*(u[:, None, None]-.5))/.6)**2
    statistics = curve_statistics(grid, values, np.zeros(len(u)), target_batch=2)
    nodes, weights = np.polynomial.legendre.leggauss(192)
    quadrature = -.5*((grid[None, :, None]-centers[None, None, :]-.2*nodes[:, None, None])/.6)**2
    exact = logsumexp(quadrature + np.log(weights/2.)[:, None, None], axis=0)
    ref = int(np.flatnonzero(grid == 0.)[0])
    exact -= exact[ref]
    standardized = np.abs(statistics['relative_logz'] - exact) / np.maximum(statistics['relative_MC_sd'], 1e-12)
    if standardized.max() > 5.:
        raise ValueError('Continuous integral differs from independent quadrature')
    # Independent long-double sums, including covariance, not a second call
    # to the implementation under test.
    weights_ld = np.exp(values.astype(np.longdouble)-np.max(values, axis=0))
    normalized = weights_ld / weights_ld.sum(axis=0)
    n = np.longdouble(len(values))
    mc = np.sqrt(n/(n-1)*np.sum((normalized-normalized[:, ref:ref+1])**2, axis=0))
    covariance_error = float(np.max(np.abs(mc-statistics['relative_MC_sd'])))
    if covariance_error > 1e-12:
        raise ValueError('Paired covariance arithmetic differs')
    # Zero-integrand cemetery draws must remain in N, affecting absolute Z.
    padded = np.concatenate((values, np.full((23, len(grid), 3), -np.inf)), axis=0)
    cemetery = curve_statistics(grid, padded, np.zeros(len(padded)))
    cemetery_error = float(np.max(np.abs(cemetery['logz']-statistics['logz']-
        np.log(len(values)/len(padded)))))
    if cemetery_error > 1e-12:
        raise ValueError('Outside-support draws lost from denominator')
    # A Gaussian location experiment has independently known MLE and LR limits.
    # Deterministic normal quantiles are an oracle, not experimental coverage.
    sigma = .5
    estimates = sigma * ndtri((np.arange(50)+.5)/50.)
    curves = -.5*((grid[:, None]-estimates[None, :])/sigma)**2
    result = read_curves(grid, fake_statistics(curves), labels(50))
    expected_half = np.sqrt(2.705543454095404)*sigma
    interval_error = max(max(abs(row['diagnostic']['CI90'][0]-(m-expected_half)),
        abs(row['diagnostic']['CI90'][1]-(m+expected_half))) for row, m in zip(result['curves'], estimates))
    mle_error = max(abs(row['diagnostic']['MLE']-m) for row, m in zip(result['curves'], estimates))
    if interval_error > .01 or mle_error > 1e-12 or not result['cells'][0]['numerical_and_local_calibration_pass']:
        raise ValueError('Analytic interval/bias/coverage oracle failed')
    refused = []
    def require_flag(name, curve, flag, precision=None):
        stats = fake_statistics(curve)
        if precision is not None:
            stats['local_precision'] = precision
        report = read_curves(grid, stats, labels(curve.shape[1]))
        if (flag not in report['curves'][0]['failures'] or
                report['cells'][0]['calibrated_coverage'] is not None or
                report['cells'][0]['numerical_and_local_calibration_pass']):
            raise ValueError('Invalid curve accepted: ' + name)
        refused.append(name)
    require_flag('flat', np.zeros((len(grid), 50)), 'UNIDENTIFIED_FLAT_CURVE')
    require_flag('boundary', np.tile((-.5*(grid-4.)**2)[:, None], (1, 50)), 'INTERVAL_TRUNCATED_BY_GRID')
    bimodal = logsumexp(np.stack((-.5*((grid-2.)/.2)**2, -.5*((grid+2.)/.2)**2)), axis=0)
    require_flag('disconnected', np.tile(bimodal[:, None], (1, 50)), 'DISCONNECTED_INTERVAL')
    precision = np.ones_like(curves, dtype=bool); precision[ref, 0] = False
    require_flag('one_failed_mock_not_dropped', curves, 'SOURCE_PRECISION_FAILED', precision)
    low_weight = values.copy(); low_weight[0] += 80.
    bad = curve_statistics(grid, low_weight, np.zeros(len(u)))
    if bad['local_precision'].any():
        raise ValueError('Dominant single source draw accepted')
    refused.append('single_dominant_source_draw')
    for name, action in (
        ('nan', lambda: curve_statistics(grid, np.full_like(values[:2], np.nan), np.zeros(2))),
        ('empty_integral', lambda: curve_statistics(grid, np.full_like(values[:2], -np.inf), np.zeros(2))),
        ('duplicate_strength', lambda: curve_statistics(np.zeros_like(grid), values, np.zeros(len(u)))),
        ('duplicate_noise', lambda: read_curves(grid, fake_statistics(curves), labels(1)*50))):
        try:
            action()
        except ValueError:
            refused.append(name)
        else:
            raise ValueError('Malformed data accepted: ' + name)
    output = dict(status='PASS_CONTINUOUS_CALIBRATION_ARITHMETIC',
        max_integral_error_in_MC_sd=float(standardized.max()),
        paired_covariance_absolute_error=covariance_error, cemetery_logz_error=cemetery_error,
        gaussian_MLE_error=float(mle_error), gaussian_interval_error=float(interval_error),
        gaussian_oracle_cell=result['cells'][0], refused_controls=refused,
        physical_injections_calibrated=False, strength_prior_selected=False, scientific_acceptance=False,
        registration_sha256=se.sha(STAGE / 'REGISTRATION.json'))
    se.write(STAGE / 'RESULT.json', output)
    print(json.dumps(output), flush=True)


if __name__ == '__main__':
    main()
