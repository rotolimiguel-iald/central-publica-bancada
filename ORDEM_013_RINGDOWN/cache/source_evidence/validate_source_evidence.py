"""Independent integration identity and adapter checks before source sampling."""
from pathlib import Path
import time
import numpy as np
from scipy.special import logsumexp
from scipy.integrate import quad
import source_evidence as se


def main():
    se.check()
    state = se.load_state()
    rows = []
    # Independent analytic one-dimensional Gaussian integrals on a finite prior.
    nodes, weights = np.polynomial.legendre.leggauss(256)
    x = 5*nodes
    blobs = np.column_stack([-.5*((x-mu)/sd)**2 for mu, sd in ((-2., .3), (0., .8), (1.5, .5))])
    mixes = logsumexp(blobs, axis=1)-np.log(3)
    logwt = np.log(weights/2)+mixes
    got, ess, maximum = se.component_integrals(logwt, mixes, blobs)
    expected = np.log([quad(lambda v:np.exp(-.5*((v-mu)/sd)**2)/10, -5, 5, epsabs=1e-12)[0]
                       for mu, sd in ((-2., .3), (0., .8), (1.5, .5))])
    error = float(np.max(np.abs(got-expected)))
    if error > 1e-10:
        raise ValueError("Component evidence identity failed")
    rng = np.random.default_rng(130523)
    samples = np.array([se.prior_transform(u) for u in rng.uniform(size=(20000, 7))])
    physical = np.column_stack([np.exp(samples[:, 0]), np.exp(samples[:, 1]), samples[:, 2:4],
                                np.cos(samples[:, 4]), samples[:, 5], samples[:, 6]])
    expected_mean = np.array([80., 2., 0., 0., 0., np.pi, 0.])
    widths = np.array([60., 2., .8, .8, 1.9, 2*np.pi, 2.])
    prior_mean_z = (physical.mean(axis=0)-expected_mean)/(widths/np.sqrt(12*len(physical)))
    if np.max(np.abs(prior_mean_z)) > 5:
        raise ValueError("Prior transform control failed")
    for family in se.FAMILIES:
        for source in (se.SOURCES[0], se.SOURCES[2]):
            coordinates = se.source_vector(source)
            started = time.perf_counter()
            values = se.component_loglikes(family, coordinates, state)
            adapter_error = 0.
            count = len(state["labels"])
            offset = 0
            for a in (0., 1.):
                for psd in ("O4", "O5"):
                    # A separate original API generates each hypothesis again.
                    reference, metadata = se.marginalized_source_log_likelihood(
                        family=family, coordinates=coordinates, times=state["times"],
                        white=state[psd+"_white"], targets=state[psd+"_targets"], reading="R-B", a=a,
                        amplitude_prior_sd=3., sample_rate=8192)
                    n = len(reference)
                    adapter_error = max(adapter_error, float(np.max(np.abs(values[offset:offset+n]-reference+state[psd+"_centers"]))))
                    offset += n
            if offset != 2*count or adapter_error > 1e-7:
                raise ValueError("Nonlinear adapter differs from original likelihood")
            rows.append(dict(family=family, source=source["name"], components=len(values),
                             adapter_error=adapter_error, seconds=time.perf_counter()-started))
    result = dict(status="PASS_ADAPTER_AND_INTEGRAL_IDENTITY_NOT_SAMPLER_CONVERGENCE",
                  component_integral_max_error=error, prior_transform_mean_z=prior_mean_z.tolist(), checks=rows,
                  likelihood_components_per_call=2*len(state["labels"]),
                  no_C6_change=se.sha(se.ROOT/"REGISTRO_C6.json")==se.sha(se.ROOT.parent.parent/"REGISTRO_C6.json"),
                  registration_sha256=se.sha(se.REG))
    se.write(se.ROOT/"VALIDATION.json", result)
    print(result, flush=True)


if __name__ == "__main__":
    main()
