"""Analytic and independent repeated-sampling controls of family combination."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
from source_family_mixture import mix_statistics, source_precision_mask

FOLDER = se.ROOT/'source_family_mixture_validation'


def check_close(got, expected, atol=1e-11):
    error = float(np.max(np.abs(np.asarray(got)-expected)))
    if error > atol:
        raise ValueError(f'Analytic mixture control failed: {error}')
    return error


def main():
    FOLDER.mkdir(exist_ok=False)
    se.write(FOLDER/'REGISTRATION.json', dict(
        status='REGISTERED_FAMILY_MIXTURE_IMPLEMENTATION_CONTROL',
        date_utc=datetime.now(timezone.utc).isoformat(), seed=130910,
        repetitions=4000, draws_per_family=512,
        variance_ratio_interval=[.9, 1.1], standardized_mean_limit=.08,
        hypotheses='Positive lognormal toy integrands with known exact means; not gravitational-wave data',
        hashes={n: se.sha(se.ROOT/n) for n in
                ('source_family_mixture.py', 'validate_source_family_mixture.py')}))
    prior = np.array([.5, .5])
    evidences = np.array([[1., 4.], [9., 1.]])
    uniform = [np.ones((17, 2))/17, np.ones((23, 2))/23]
    constant = mix_statistics(np.log(evidences), uniform, prior)
    constant_error = check_close(constant['lnB'], np.log(2.5/5.))
    check_close(constant['lnB_MC_sd'], 0., 1e-15)
    # The uncentered formula gives spurious uncertainty for EXACT constants.
    naive = sum(len(p)/(len(p)-1)*np.sum(
        (r[1]*p[:, 1]-r[0]*p[:, 0])**2)
        for p, r in zip(uniform, constant['family_responsibility']))
    if naive <= .01:
        raise ValueError('Constant-family control failed to expose centering error')
    shift = mix_statistics(np.log(evidences)+10000., uniform, prior)
    shift_error = check_close(shift['lnB'], constant['lnB'])
    wrong_log_average = float(np.mean(np.log(evidences[:, 1]/evidences[:, 0])))
    if abs(wrong_log_average-constant['lnB'][0]) < .1:
        raise ValueError('Control did not distinguish evidence mixing from log averaging')
    # Opposite paired hypotheses share the same weights, so covariance cancels.
    p = np.array([.1, .3, .6])
    shared = [np.column_stack([p, p]), np.column_stack([p[::-1], p[::-1]])]
    paired = mix_statistics(np.log([[2., 6.], [4., 12.]]), shared, prior)
    check_close(paired['lnB'], np.log(3.))
    check_close(paired['lnB_MC_sd'], 0., 1e-15)
    # A low-ESS component must stay rejected even if the ratio cancels exactly.
    low = dict(ESS=np.array([2., 2.]), max_weight=np.array([.6, .6]), lnB_MC_sd=np.array([0.]))
    if source_precision_mask(low).any():
        raise ValueError('Low ESS was hidden by cancellation')
    invalid = []
    cases = [(np.log(evidences), uniform, [.4, .4]),
             (np.log(evidences), [uniform[0]*.9, uniform[1]], prior),
             (np.array([[np.nan, 0.], [0., 0.]]), uniform, prior),
             (np.log(evidences), uniform, [1., 0.])]
    for i, args in enumerate(cases):
        try:
            mix_statistics(*args)
        except ValueError:
            invalid.append(i)
        else:
            raise ValueError('Invalid mixture input was accepted')
    # Both hypotheses have correlated lognormal integrands within a family;
    # family draws are independent. This oracle checks the covariance term.
    mu = np.array([[.2, -.1], [1., .6]])
    matrices = np.array([[[.55, 0.], [.3, .4]], [[.3, -.2], [-.1, .65]]])
    exact_z = mu+.5*np.sum(matrices**2, axis=2)
    exact = logsumexp(exact_z[:, 1]+np.log(prior))-logsumexp(exact_z[:, 0]+np.log(prior))
    rng = np.random.default_rng(130910)
    records = []
    for _ in range(4000):
        values = [rng.normal(size=(512, 2))@a.T+m for a, m in zip(matrices, mu)]
        totals = [logsumexp(v, axis=0) for v in values]
        logs = np.array(totals)-np.log(512)
        weights = [np.exp(v-s[None, :]) for v, s in zip(values, totals)]
        got = mix_statistics(logs, weights, prior)
        records.append([got['lnB'][0], got['lnB_MC_sd'][0]])
    records = np.asarray(records)
    residual = records[:, 0]-exact
    ratio = float(residual.var(ddof=1)/np.mean(records[:, 1]**2))
    standardized_mean = float(np.mean(residual/records[:, 1]))
    passed = .9 <= ratio <= 1.1 and abs(standardized_mean) <= .08
    output = dict(status='PASS_FAMILY_MIXTURE_ARITHMETIC' if passed else 'FAIL_FAMILY_MIXTURE_ARITHMETIC',
        exact_toy_lnB=float(exact), toy_empirical_mean=float(records[:, 0].mean()),
        empirical_over_predicted_variance=ratio, standardized_mean=standardized_mean,
        constant_evidence_lnB_error=constant_error, centering_shift_error=shift_error,
        constant_likelihood_correct_MC_sd=float(constant['lnB_MC_sd'][0]),
        constant_likelihood_spurious_uncentered_MC_sd=float(np.sqrt(naive)),
        improper_mean_logB=wrong_log_average, proper_constant_mixture_lnB=float(constant['lnB'][0]),
        invalid_inputs_refused=len(invalid), low_ESS_refused=True,
        scientific_acceptance=False, registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.save_arrays(FOLDER/'TOY_REPETITIONS.npz', lnB=records[:, 0], MC_sd=records[:, 1])
    se.write(FOLDER/'RESULT.json', output)
    print(json.dumps(output), flush=True)
    if not passed:
        raise ValueError('Repeated-sampling mixture oracle failed')


if __name__ == '__main__':
    main()
