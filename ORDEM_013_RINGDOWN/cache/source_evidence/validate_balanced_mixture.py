"""Verify computational balancing using a previous pilot, not oracle truth.

Offsets affect the nested proposal only. The integrals of the original Gaussian
likelihood components, their priors and evidence ratios remain unchanged.
"""
import json
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import dynesty
from dynesty.utils import resample_run
from validate_nested_mixture import prior, likelihood

PILOT = json.loads((se.ROOT/"NESTED_ORACLE.json").read_bytes())
OFFSETS = np.array(PILOT["runs"][0]["measured"])


def balanced_likelihood(x):
    _, components = likelihood(x)
    return float(logsumexp(components-OFFSETS)-np.log(len(components))), components


def main():
    expected = np.array(PILOT["runs"][0]["expected"])
    rows = []
    for seed in (130626, 130627):
        sampler = dynesty.NestedSampler(balanced_likelihood, prior, 7, nlive=512, bound="multi", sample="rwalk",
                                       walks=20, blob=True, rstate=np.random.default_rng(seed))
        sampler.run_nested(dlogz=.1, print_progress=False)
        result = sampler.results
        estimate, ess, maximum = se.component_integrals(result.logwt, result.logl, np.stack(result.blob))
        bootstraps = []
        for k in range(64):
            boot = resample_run(result, rstate=np.random.default_rng(seed+100+k))
            value, _, _ = se.component_integrals(boot.logwt, boot.logl, np.stack(boot.blob))
            bootstraps.append(value)
        sigma = np.std(bootstraps, axis=0, ddof=1)
        ratio_sd = float(np.std(np.array(bootstraps)[:, 1]-np.array(bootstraps)[:, 0], ddof=1))
        row = dict(seed=seed, nlive=512, ncall=int(np.sum(result.ncall)), expected=expected.tolist(),
                   measured=estimate.tolist(), errors=(estimate-expected).tolist(), ESS=ess.tolist(),
                   max_weights=maximum.tolist(), logZ_bootstrap_sd=sigma.tolist(), lnB_bootstrap_sd=ratio_sd,
                   lnB_measured=float(estimate[1]-estimate[0]), lnB_expected=float(expected[1]-expected[0]),
                   component_weights_pass=bool(np.all(ess >= 100)&np.all(maximum <= .05)),
                   consistency_pass=bool(np.all(np.abs(estimate-expected) < 5*np.maximum(sigma, .03))))
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = dict(status="MEASURED_BALANCED_ORACLE", learned_offsets=OFFSETS.tolist(), runs=rows,
                  difference_between_seed_lnB=float(abs(rows[0]["lnB_measured"]-rows[1]["lnB_measured"])),
                  prior_unchanged=True, original_likelihood_components_unchanged=True,
                  scientific_astrophysical_acceptance=False,
                  scope="Computational balancing learned from previous toy pilot only; does not choose a physical TGL model or prove an astrophysical integral",
                  hashes={n:se.sha(se.ROOT/n) for n in ("NESTED_ORACLE.json", "validate_nested_mixture.py", "validate_balanced_mixture.py")})
    se.write(se.ROOT/"BALANCED_ORACLE.json", report)
    if not all(r["consistency_pass"] for r in rows):
        raise ValueError("Balanced oracle consistency check failed; result preserved")


if __name__ == "__main__":
    main()
