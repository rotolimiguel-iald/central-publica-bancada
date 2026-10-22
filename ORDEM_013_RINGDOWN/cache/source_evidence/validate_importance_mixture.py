"""Independent 7D known integrals, normalized proposal and covariance controls."""
import json
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_t
import source_evidence as se
from importance_source_evidence import draw_proposal, proposal_logpdf, importance_statistics
from validate_nested_mixture import MEANS, WIDTHS, OFFSETS, prior


def main():
    # Deliberately imperfect heavy-tailed proposal, not equal to either target.
    proposal = dict(defensive_weight=.1, df=5., components=[
        dict(weight=.45, mean=((MEANS[k]+5)/10+.015*(-1)**k).tolist(),
             shape=(np.eye(7)*(1.4*WIDTHS[k]/10)**2).tolist()) for k in range(2)])
    expected = np.array(json.loads((se.ROOT/"NESTED_ORACLE.json").read_bytes())["runs"][0]["expected"])
    rows = []
    for seed in (130702, 130703, 130704, 130705):
        u, logq = draw_proposal(proposal, 32768, seed)
        inside = np.all((u >= 0)&(u <= 1), axis=1)
        values = np.full((len(u), 2), -np.inf)
        x = -5+10*u[inside]
        values[inside] = -.5*np.sum((x[:, None, :]-MEANS[None, :, :])**2, axis=2)/WIDTHS[None, :]**2+OFFSETS
        stat = importance_statistics(values, logq)
        error = float(stat["lnB"][0]-(expected[1]-expected[0]))
        rows.append(dict(seed=seed, draws=len(u), outside_cube=int((~inside).sum()),
                         logZ=stat["logz"].tolist(), logZ_error=(stat["logz"]-expected).tolist(),
                         lnB_error=error, lnB_MC_sd=float(stat["lnB_MC_sd"][0]), ESS=stat["ESS"].tolist(),
                         max_weights=stat["max_weight"].tolist(), consistency=bool(abs(error)<5*stat["lnB_MC_sd"][0])))
    # Independent density evaluation of every mixture term, with a nonzero
    # defensive cube component exactly where the physical prior has support.
    points = np.array([[.5]*7, [1.5]*7, [.2]*7])
    q = np.zeros(3)
    for i, u in enumerate(points):
        q[i] = .1 if np.all((u >= 0)&(u <= 1)) else 0.
        for c in proposal["components"]:
            q[i] += c["weight"]*multivariate_t.pdf(u, loc=c["mean"], shape=c["shape"], df=5.)
    density_error = float(np.max(np.abs(np.log(q)-proposal_logpdf(points, proposal))))
    output = dict(status="PASS_INDEPENDENT_IMPORTANCE_ORACLE" if all(r["consistency"] for r in rows) and density_error<1e-12 else "FAIL",
                  rows=rows, independent_density_log_error=density_error,
                  all_draws_in_denominator=True, prior_unchanged=True,
                  scope="Analytic test validates normalized proposal, zero outside-prior integrand and covariance of evidence ratio; does not validate astrophysical posterior coverage",
                  source_sha256=se.sha(se.ROOT/se.Path(__file__).name))
    se.write(se.ROOT/"IMPORTANCE_ORACLE.json", output)
    print(json.dumps(output), flush=True)
    if output["status"] == "FAIL":
        raise ValueError("Importance oracle failed")


if __name__ == "__main__":
    main()
