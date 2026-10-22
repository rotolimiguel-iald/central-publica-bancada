"""Check that the reduced computational proposal is the actual Student-t marginal."""
import json
import numpy as np
from scipy.integrate import quad
from scipy.stats import multivariate_t
import source_evidence as se
from phase_marginal_source import check, INDICES, DIRECTORY
from importance_source_evidence import proposal_logpdf


def main():
    check()
    original = json.loads((se.ROOT/"runs/IMRPhenomXPHM_adapted_130701/IMPORTANCE_PROPOSAL.json").read_bytes())
    marginal = json.loads((DIRECTORY/"PROPOSAL.json").read_bytes())
    examples = [np.array(original["components"][i]["mean"])[INDICES] for i in (0, 5, 12)]
    examples.append(np.array([.4, .3, .5, .5, .75, .5]))
    checks = []
    for point in examples:
        numerical = original["defensive_weight"] if np.all((point >= 0)&(point <= 1)) else 0.
        component_errors = []
        for before, after in zip(original["components"], marginal["components"]):
            loc = np.array(before["mean"])
            shape = np.array(before["shape"])
            marginal_value = multivariate_t.pdf(point, loc=after["mean"], shape=after["shape"], df=original["df"])
            sxx = shape[np.ix_(INDICES, INDICES)]
            cross = shape[5, INDICES]
            delta = point-loc[INDICES]
            mean = loc[5]+cross@np.linalg.solve(sxx, delta)
            scale = np.sqrt((shape[5, 5]-cross@np.linalg.solve(sxx, cross))*
                            (original["df"]+delta@np.linalg.solve(sxx, delta))/(original["df"]+6))
            def integrand(v):
                x = np.insert(point, 5, mean+scale*v)
                return multivariate_t.pdf(x, loc=loc, shape=shape, df=original["df"])*scale/marginal_value
            ratio, error = quad(integrand, -np.inf, np.inf, epsabs=1e-10, epsrel=1e-10)
            component_errors.append(abs(ratio-1))
            numerical += before["weight"]*ratio*marginal_value
        explicit = float(np.exp(proposal_logpdf(point, marginal)[0]))
        relative = abs(numerical-explicit)/explicit
        checks.append(dict(point=point.tolist(), component_max_relative_error=max(component_errors), mixture_relative_error=relative))
    maximum = max(max(c["component_max_relative_error"], c["mixture_relative_error"]) for c in checks)
    result = dict(status="PASS_EXACT_PROPOSAL_MARGINAL" if maximum < 1e-8 else "FAIL", checks=checks,
                  max_relative_error=maximum, scope="Computational proposal normalized by integrating the removed coordinate over its full real domain; physical phase prior is independently integrated on0..2pi",
                  source_sha256=se.sha(se.ROOT/se.Path(__file__).name), proposal_sha256=se.sha(DIRECTORY/"PROPOSAL.json"))
    se.write(DIRECTORY/"PROPOSAL_VALIDATION.json", result)
    print(json.dumps(dict(status=result["status"], max_relative_error=maximum)), flush=True)
    if result["status"] == "FAIL":
        raise ValueError("Proposal marginal check failed")


if __name__ == "__main__":
    main()
