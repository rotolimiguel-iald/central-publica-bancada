"""Seven-dimensional analytic oracle for the actual nested-mixture interface."""
import source_evidence as se
import dynesty
from dynesty.utils import resample_run
import numpy as np
from scipy.special import ndtr, logsumexp

MEANS = np.array([[-1.]*7, [1.]*7])
WIDTHS = np.array([.65, 1.])
OFFSETS = np.array([0., .7])


def prior(u):
    return -5.+10.*np.asarray(u)


def likelihood(x):
    blobs = -.5*np.sum((np.asarray(x)[None, :]-MEANS)**2, axis=1)/WIDTHS**2+OFFSETS
    return se.log_mixture(blobs), blobs


def main():
    expected = []
    for mu, sd, offset in zip(MEANS, WIDTHS, OFFSETS):
        expected.append(float(offset+np.sum(np.log(sd*np.sqrt(2*np.pi)/10*
                               (ndtr((5-mu)/sd)-ndtr((-5-mu)/sd))))))
    expected = np.array(expected)
    rows = []
    for seed in (130524, 130525):
        sampler = dynesty.NestedSampler(likelihood, prior, 7, nlive=256, bound="multi", sample="rwalk",
                                       walks=20, blob=True, rstate=np.random.default_rng(seed))
        sampler.run_nested(dlogz=.15, print_progress=False)
        result = sampler.results
        estimate, ess, maximum = se.component_integrals(result.logwt, result.logl, np.stack(result.blob))
        repeat = []
        for k in range(64):
            boot = resample_run(result, rstate=np.random.default_rng(seed+k+100))
            got, _, _ = se.component_integrals(boot.logwt, boot.logl, np.stack(boot.blob))
            repeat.append(got)
        sigma = np.std(repeat, axis=0, ddof=1)
        errors = estimate-expected
        # A stochastic sampler is not an exact integrator. Compare with independent
        # analytic integrals and explicitly retain the MC uncertainty.
        passed = bool(np.all(np.abs(errors) < 5*np.maximum(sigma, .03)))
        rows.append(dict(seed=seed, expected=expected.tolist(), measured=estimate.tolist(),
                         errors=errors.tolist(), bootstrap_sd=sigma.tolist(), ESS=ess.tolist(),
                         max_weights=maximum.tolist(), ncall=int(np.sum(result.ncall)), passed=passed))
        print(rows[-1], flush=True)
    out = dict(status="PASS_ANALYTIC_7D_SAMPLER_ORACLE" if all(r["passed"] for r in rows) else "FAIL",
               runs=rows, bootstrap_per_run=64, scope="Actual dynesty blobs/reweight/bootstrap tested against analytic integrals. Does not prove convergence of astrophysical runs",
               source_sha256=se.sha(se.ROOT/se.Path(__file__).name))
    se.write(se.ROOT/"NESTED_ORACLE.json", out)
    if out["status"] == "FAIL":
        raise ValueError("Analytic oracle failed")


if __name__ == "__main__":
    main()
