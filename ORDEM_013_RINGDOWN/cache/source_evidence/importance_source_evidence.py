"""Independent importance integration with a defensive, normalized proposal.

The physical prior remains uniform in the registered seven-dimensional cube.
A completed nested pilot only trains the computational proposal. At least 10%
of samples come from the original prior, so support is never truncated to fits.
Student-t draws outside the cube have exactly zero integrand; they still count
in the Monte Carlo denominator. No rejection-renormalization is hidden.
"""
import argparse
from datetime import datetime, timezone
import json
import multiprocessing as mp
import time
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_normal, multivariate_t
import source_evidence as se


def proposal_logpdf(u, proposal):
    u = np.atleast_2d(u)
    inside = np.all((u >= 0)&(u <= 1), axis=1)
    terms = [np.where(inside, np.log(proposal["defensive_weight"]), -np.inf)]
    for component in proposal["components"]:
        terms.append(np.log(component["weight"])+multivariate_t.logpdf(
            u, loc=component["mean"], shape=component["shape"], df=proposal["df"]))
    return logsumexp(np.column_stack(terms), axis=1)


def draw_proposal(proposal, count, seed):
    rng = np.random.default_rng(seed)
    weights = [proposal["defensive_weight"]]+[c["weight"] for c in proposal["components"]]
    if not np.isclose(sum(weights), 1., atol=1e-12):
        raise ValueError("Proposal weights are not normalized")
    selected = rng.choice(len(weights), size=count, p=weights)
    u = np.empty((count, 7))
    for k in range(len(weights)):
        indices = np.flatnonzero(selected == k)
        if not len(indices):
            continue
        if k == 0:
            u[indices] = rng.uniform(size=(len(indices), 7))
        else:
            c = proposal["components"][k-1]
            lower = np.linalg.cholesky(c["shape"])
            g = rng.normal(size=(len(indices), 7))@lower.T
            g /= np.sqrt(rng.chisquare(proposal["df"], size=len(indices))/proposal["df"])[:, None]
            u[indices] = g+np.array(c["mean"])
    return u, proposal_logpdf(u, proposal)


def fit_gaussians(u, weights, count=16, seed=130700):
    """Weighted Gaussian EM used only to place heavy-tailed proposal components."""
    weights = np.asarray(weights)/np.sum(weights)
    rng = np.random.default_rng(seed)
    centers = u[rng.choice(len(u), count, replace=False, p=weights)]
    mean = np.sum(weights[:, None]*u, axis=0)
    covariance = np.einsum("n,ni,nj->ij", weights, u-mean, u-mean)+np.eye(7)*1e-4
    shapes = np.repeat(covariance[None, :, :], count, axis=0)
    mixture = np.ones(count)/count
    history = []
    for iteration in range(60):
        logits = np.column_stack([np.log(mixture[k])+multivariate_normal.logpdf(u, centers[k], shapes[k]) for k in range(count)])
        normalizer = logsumexp(logits, axis=1)
        responsibilities = np.exp(logits-normalizer[:, None])*weights[:, None]
        amounts = responsibilities.sum(axis=0)
        for k in range(count):
            if amounts[k] < 1e-8:
                centers[k] = u[rng.choice(len(u), p=weights)]
                shapes[k] = covariance.copy()
                continue
            centers[k] = np.sum(responsibilities[:, k, None]*u, axis=0)/amounts[k]
            delta = u-centers[k]
            shapes[k] = np.einsum("n,ni,nj->ij", responsibilities[:, k]/amounts[k], delta, delta)+np.eye(7)*1e-4
        mixture = np.maximum(amounts, 1e-5)
        mixture /= mixture.sum()
        history.append(float(weights@normalizer))
    # Inflate and use heavier tails than the fitted Gaussian density. The
    # fitted mode weights do not alter the source prior or model probabilities.
    mixture = .9*(.9*mixture+.1/count)
    components = [dict(weight=float(mixture[k]), mean=centers[k].tolist(), shape=(2*shapes[k]).tolist()) for k in range(count)]
    return dict(defensive_weight=.1, df=5., components=components, fit_history=history)


def importance_statistics(log_values, logq):
    """Independent-draw integral, with covariance retained in each log Bayes ratio."""
    log_weights = log_values-logq[:, None]
    total = logsumexp(log_weights, axis=0)
    p = np.exp(log_weights-total[None, :])
    n = len(log_values)
    logz = total-np.log(n)
    ess = 1/np.sum(p*p, axis=0)
    maxweight = p.max(axis=0)
    count = log_values.shape[1]//2
    lnB = logz[count:]-logz[:count]
    mc = np.sqrt(n/(n-1)*np.sum((p[:, count:]-p[:, :count])**2, axis=0))
    return dict(logz=logz, ESS=ess, max_weight=maxweight, lnB=lnB, lnB_MC_sd=mc)


def fit(pilot_name):
    folder = se.ROOT/"runs"/pilot_name
    result = json.loads((folder/"RESULT.json").read_bytes())
    if se.sha(folder/"samples.npz") != result["arrays_sha256"]:
        raise ValueError("Pilot arrays changed")
    with np.load(folder/"samples.npz") as f:
        u = f["samples_u"].copy()
        logw = f["logwt"][:, None]+f["components"]-f["logl"][:, None]-f["component_logz"][None, :]
    # Average normalized component posterior weights, not their evidences.
    weights = np.exp(logsumexp(logw, axis=1)-np.log(logw.shape[1]))
    proposal = fit_gaussians(u, weights)
    proposal.update(status="COMPUTATIONAL_PROPOSAL_NOT_PHYSICAL_PRIOR", family=result["family"],
                    pilot=pilot_name, pilot_sha256=se.sha(folder/"samples.npz"), registration_sha256=se.sha(se.REG),
                    source_sha256=se.sha(se.ROOT/se.Path(__file__).name), pilot_convergence_not_assumed=True,
                    full_prior_support=True, null_integrand_outside_cube=True,
                    scope="Train from all components without selecting favorable Bayes factors; independent future draws measure the integral")
    se.write(folder/"IMPORTANCE_PROPOSAL.json", proposal)
    print(json.dumps(dict(status="PROPOSAL_FITTED", components=len(proposal["components"]), family=result["family"])), flush=True)


def evaluate_one(item):
    index, u = item
    values = se.component_loglikes(se._FAMILY, se.prior_transform(u), se._STATE)
    return index, values


def run(args):
    proposal_path = se.ROOT/"runs"/args.pilot/"IMPORTANCE_PROPOSAL.json"
    proposal = json.loads(proposal_path.read_bytes())
    if proposal["registration_sha256"] != se.sha(se.REG):
        raise ValueError("Proposal registration changed")
    folder = se.ROOT/"importance_runs"/f"{args.pilot}_seed{args.seed}_N{args.draws}"
    if folder.exists():
        raise FileExistsError("Preserve previous or incomplete importance run")
    folder.mkdir(parents=True)
    se.initialize(proposal["family"])
    state = se._STATE
    u, logq = draw_proposal(proposal, args.draws, args.seed)
    inside = np.all((u >= 0)&(u <= 1), axis=1)
    se.save_arrays(folder/"PROPOSALS.npz", unit_cube=u, logq=logq, inside=inside)
    se.write(folder/"START.json", dict(status="REGISTERED_INDEPENDENT_IMPORTANCE_RUN", date_utc=datetime.now(timezone.utc).isoformat(),
             family=proposal["family"], seed=args.seed, draws=args.draws, valid_draws=int(inside.sum()),
             physical_prior_unchanged=True, proposal_sha256=se.sha(proposal_path), registration_sha256=se.sha(se.REG),
             source_sha256=se.sha(se.ROOT/se.Path(__file__).name),
             precision="Each component ESS>=100, maxweight<=.05, paired MC lnB sd<=.2, independent repeats and rate checks required"))
    components = np.full((args.draws, 2*len(state["labels"])), -np.inf)
    jobs = [(int(i), u[i]) for i in np.flatnonzero(inside)]
    chunk = []
    done = 0
    counter = 0
    start = time.monotonic()
    with mp.get_context("fork").Pool(args.processes, initializer=se.initialize, initargs=(proposal["family"],)) as pool:
        for index, values in pool.imap_unordered(evaluate_one, jobs, chunksize=1):
            components[index] = values
            chunk.append((index, values))
            done += 1
            if len(chunk) >= 128 or done == len(jobs):
                se.save_arrays(folder/f"chunk_{counter:05d}.npz", indices=np.array([v[0] for v in chunk]), components=np.stack([v[1] for v in chunk]))
                chunk = []
                counter += 1
                progress = dict(completed=done, valid_draws=len(jobs), seconds=time.monotonic()-start,
                                date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder/"PROGRESS.json", progress, replace=True)
                print(json.dumps(progress), flush=True)
    statistics = importance_statistics(components, logq)
    se.save_arrays(folder/"RESULT_ARRAYS.npz", **statistics)
    n = len(state["labels"])
    enough = (np.minimum(statistics["ESS"][:n], statistics["ESS"][n:]) >= 100)&(
               np.maximum(statistics["max_weight"][:n], statistics["max_weight"][n:]) <= .05)&(statistics["lnB_MC_sd"] <= .2)
    rows = []
    for label in state["labels"]:
        cell = {k:label[k] for k in ("psd", "source", "injection_family", "injection_a", "snr")}
        if any(r["cell"] == cell for r in rows):
            continue
        ii = np.array([i for i, other in enumerate(state["labels"]) if all(other[k] == v for k, v in cell.items())])
        ids = np.r_[ii, n+ii]
        values = statistics["lnB"][ii]
        rows.append(dict(cell=cell, N=len(ii), lnB_mean=float(values.mean()), lnB_sd_noise=float(values.std(ddof=1)),
                         lnB_quantiles=np.quantile(values, [.05, .5, .95]).tolist(),
                         min_component_ESS=float(statistics["ESS"][ids].min()), max_component_weight=float(statistics["max_weight"][ids].max()),
                         MC_lnB_sd_max=float(statistics["lnB_MC_sd"][ii].max()), draws_passing_precision=int(enough[ii].sum())))
    report = dict(status="INDEPENDENT_IMPORTANCE_PILOT_NOT_ACCEPTED", rows=rows, family=proposal["family"],
                  seed=args.seed, draws=args.draws, evaluated_draws=done, source_parameters_integrated=7,
                  all_draws_pass_precision=bool(enough.all()), draws_passing_precision=int(enough.sum()),
                  independent_repeat=False, rate_control=False, physical_prior_unchanged=True, no_C6_change=True,
                  seconds=time.monotonic()-start, proposal_sha256=se.sha(proposal_path), registration_sha256=se.sha(se.REG),
                  hashes={p.name:se.sha(p) for p in folder.glob("*.npz")},
                  scope="Independent samples under a full-support computational proposal. Finite-sample ratio bias/tails and waveform error still require validation; no lnB-to-sigma conversion")
    se.write(folder/"RESULT.json", report)
    print(json.dumps({k:report[k] for k in ("status", "draws_passing_precision", "draws", "seconds")}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["fit", "run"])
    parser.add_argument("--pilot", default="IMRPhenomXPHM_seed130522_nlive256")
    parser.add_argument("--seed", type=int, default=130701)
    parser.add_argument("--draws", type=int, default=4096)
    parser.add_argument("--processes", type=int, default=6)
    args = parser.parse_args()
    if args.command == "fit":
        fit(args.pilot)
    else:
        run(args)
