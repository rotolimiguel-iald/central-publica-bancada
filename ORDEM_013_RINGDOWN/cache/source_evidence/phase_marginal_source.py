"""Integrate the full orbital phase before six-dimensional source sampling.

This is the same seven-dimensional source prior. Both orbital branches and all
waveform harmonics are retained. Conditional phase quadrature is checked on each
source point; failed interpolation or quadrature is a visible execution failure.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import multiprocessing as mp
import time
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_t
import source_evidence as se
import peak_phase_coordinates as pc
from importance_source_evidence import proposal_logpdf, importance_statistics

DIRECTORY = se.ROOT/"phase_runs"
REG = DIRECTORY/"REGISTRATION.json"
INDICES = [0, 1, 2, 3, 4, 6]


def six_to_physical(u):
    u = np.asarray(u)
    if u.shape != (6,):
        raise ValueError("Six independent prior coordinates required")
    original = np.insert(u, 5, .5)
    return se.prior_transform(original)


def phase_marginal_loglikes(family, u, state, sample_rate=8192):
    x = six_to_physical(u)
    values = [[], []]
    maximum_interpolation = 0.
    maximum_waveform = 0.
    maximum_quadrature = 0.
    highest_grid = 0
    for psd in ("O4", "O5"):
        white = state[psd+"_white"]
        targets = state[psd+"_targets"]
        bank = pc.phase_bank(family, x, state["times"], white, sample_rate=sample_rate)
        # Each bank is checked at non-grid phases against the original full-wave
        # generator. This is not a Taylor surrogate in the source parameters.
        for phase in (.173, .619, 1.413):
            y = x.copy()
            y[5] = phase
            pair, meta = se.paired_polarizations(family, y, state["times"], sample_rate)
            for a in (0, 1):
                original = se.basis_from_polarizations(pair[a], white)
                interpolated = pc.evaluate_bank(bank, [phase], a)[0]
                error = float(np.linalg.norm(original-interpolated)/np.linalg.norm(original))
                _, direct = se.linear_statistics(original, targets, 3.)
                approximate = pc.bank_loglikes(bank, [phase], targets, a)
                ll_error = float(np.max(np.abs(direct-approximate)))
                maximum_waveform = max(maximum_waveform, error)
                maximum_interpolation = max(maximum_interpolation, ll_error)
                if error > 1e-6 or ll_error > .001:
                    raise ValueError(f"Full-wave phase interpolation failed: relative={error}, logL={ll_error}, coordinates={x.tolist()}")
        for a in (0, 1):
            n = 512
            while True:
                phases = 2*np.pi*np.arange(n)/n
                logvalues = pc.bank_loglikes(bank, phases, targets, a)
                fine = logsumexp(logvalues, axis=0)-np.log(n)
                coarse = logsumexp(logvalues[::2], axis=0)-np.log(n//2)
                error = float(np.max(np.abs(fine-coarse)))
                if error <= 1e-5:
                    maximum_quadrature = max(maximum_quadrature, error)
                    highest_grid = max(highest_grid, n)
                    break
                if n >= 8192:
                    raise ValueError(f"Phase quadrature did not converge: {error}")
                n *= 2
            values[a].extend((fine-state[psd+"_centers"]).tolist())
    result = np.array(values).ravel()
    if not np.all(np.isfinite(result)):
        raise ValueError("Nonfinite phase integral")
    return result, dict(max_logL_interpolation_error=maximum_interpolation,
                        max_relative_waveform_interpolation_error=maximum_waveform,
                        max_phase_quadrature_error=maximum_quadrature, largest_phase_grid=highest_grid)


def register():
    DIRECTORY.mkdir(exist_ok=False)
    validation = json.loads((se.ROOT/"PEAK_PHASE_COORDINATES_VALIDATION.json").read_bytes())
    if validation["status"] != "PASS_PRIOR_PRESERVING_PHASE_COORDINATES":
        raise ValueError("Phase coordinates have not passed validation")
    source = se.ROOT/"runs/IMRPhenomXPHM_adapted_130701/IMPORTANCE_PROPOSAL.json"
    proposal = json.loads(source.read_bytes())
    for component in proposal["components"]:
        component["mean"] = np.array(component["mean"])[INDICES].tolist()
        component["shape"] = np.array(component["shape"])[np.ix_(INDICES, INDICES)].tolist()
    proposal.update(status="SIX_DIMENSIONAL_COMPUTATIONAL_PROPOSAL", source_7D_proposal_sha256=se.sha(source),
                    marginalization="Exact Student-t marginal on coordinates0,1,2,3,4,6; uniform component retains volume1", physical_prior_changed=False)
    se.write(DIRECTORY/"PROPOSAL.json", proposal)
    names = ["phase_marginal_source.py", "peak_phase_coordinates.py", "PEAK_PHASE_COORDINATES_VALIDATION.json",
             "importance_source_evidence.py", "source_evidence.py", "coherent_imr_model.py", "tgl_ringdown_prediction.py",
             "tgl_ringdown_likelihood.py", "REGISTRATION.json", "INJECTIONS.json", "INJECTIONS.npz", "phase_runs/PROPOSAL.json"]
    reg = dict(status="REGISTERED_EXACT_PHASE_MARGINALIZATION_NONBLIND", date_utc=datetime.now(timezone.utc).isoformat(),
               physical_prior="Exactly inherited from REGISTRATION.json; orbital phase uniform on0..2pi integrated, six remaining variables sampled",
               families=se.FAMILIES, datasets=1200, original_noise_indices=[50, 100], original_SNR=40.,
               phase_representation="Complete-wave 16-point Fourier bank, with three held-out phase controls at each source point",
               phase_quadrature="Periodic trapezoid512, doubled to8192 if necessary; compare full and half grids each point",
               accuracy=dict(max_waveform_interpolation_relative=1e-6, max_logL_interpolation_error=.001, max_phase_quadrature_log_error=1e-5),
               source_MC="Independent draws with exact six-dimensional Student-t marginal proposal and10% original-prior draws; outside cube integrand zero",
               physical_clock_or_partition_selected=False, original_C6_changed=False, on_source_strain_read=False,
               acceptance="Original component ESS, maximum-weight, MC-error, independent-repeat and waveform-rate criteria retained; source model and continuous-a calibration remain open",
               hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(REG, reg)
    print(json.dumps(dict(status=reg["status"], sha256=se.sha(REG))), flush=True)


def check():
    reg = json.loads(REG.read_bytes())
    for name, expected in reg["hashes"].items():
        if se.sha(se.ROOT/name) != expected:
            raise ValueError("Phase integration input changed: "+name)
    se.check()
    return reg


def draw(proposal, count, seed):
    rng = np.random.default_rng(seed)
    weights = [proposal["defensive_weight"]]+[c["weight"] for c in proposal["components"]]
    if abs(sum(weights)-1.) > 1e-12:
        raise ValueError("Proposal is not normalized")
    groups = rng.choice(len(weights), size=count, p=weights)
    u = np.empty((count, 6))
    for k in range(len(weights)):
        ids = np.flatnonzero(groups == k)
        if not len(ids):
            continue
        if k == 0:
            u[ids] = rng.uniform(size=(len(ids), 6))
        else:
            component = proposal["components"][k-1]
            v = rng.normal(size=(len(ids), 6))@np.linalg.cholesky(component["shape"]).T
            v /= np.sqrt(rng.chisquare(proposal["df"], size=len(ids))/proposal["df"])[:, None]
            u[ids] = v+np.array(component["mean"])
    return u, proposal_logpdf(u, proposal)


def evaluate(item):
    index, u = item
    value, meta = phase_marginal_loglikes(se._FAMILY, u, se._STATE)
    return index, value, meta


def run(args):
    check()
    proposal = json.loads((DIRECTORY/"PROPOSAL.json").read_bytes())
    folder = DIRECTORY/f"{args.family}_seed{args.seed}_N{args.draws}"
    folder.mkdir(exist_ok=False)
    se.initialize(args.family)
    u, logq = draw(proposal, args.draws, args.seed)
    inside = np.all((u >= 0)&(u <= 1), axis=1)
    se.save_arrays(folder/"PROPOSALS.npz", unit_cube=u, logq=logq, inside=inside)
    se.write(folder/"START.json", dict(status="REGISTERED_RUN", family=args.family, seed=args.seed, draws=args.draws,
             registration_sha256=se.sha(REG), known_parameters="same physical priors, phase fully integrated", processes=args.processes,
             proposal_sha256=se.sha(DIRECTORY/"PROPOSAL.json"), date_utc=datetime.now(timezone.utc).isoformat()))
    values = np.full((args.draws, 2400), -np.inf)
    jobs = [(int(i), u[i]) for i in np.flatnonzero(inside)]
    start, done, number = time.monotonic(), 0, 0
    chunk, metadata = [], []
    with mp.get_context("fork").Pool(args.processes, initializer=se.initialize, initargs=(args.family,)) as pool:
        for index, value, meta in pool.imap_unordered(evaluate, jobs, chunksize=1):
            values[index] = value
            chunk.append((index, value))
            metadata.append(dict(index=index, **meta))
            done += 1
            if len(chunk) == 16 or done == len(jobs):
                se.save_arrays(folder/f"chunk_{number:05d}.npz", indices=np.array([c[0] for c in chunk]), components=np.stack([c[1] for c in chunk]))
                chunk = []
                number += 1
                progress = dict(done=done, valid_draws=len(jobs), seconds=time.monotonic()-start, date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder/"PROGRESS.json", progress, replace=True)
                print(json.dumps(progress), flush=True)
    stats = importance_statistics(values, logq)
    se.save_arrays(folder/"RESULT_ARRAYS.npz", **stats)
    n = 1200
    pass_precision = (np.minimum(stats["ESS"][:n], stats["ESS"][n:]) >= 100)&(
        np.maximum(stats["max_weight"][:n], stats["max_weight"][n:]) <= .05)&(stats["lnB_MC_sd"] <= .2)
    rows = []
    for label in se._STATE["labels"]:
        cell = {k:label[k] for k in ("psd", "source", "injection_family", "injection_a", "snr")}
        if any(row["cell"] == cell for row in rows):
            continue
        ii = np.array([i for i, other in enumerate(se._STATE["labels"]) if all(other[k] == v for k, v in cell.items())])
        both = np.r_[ii, n+ii]
        ll = stats["lnB"][ii]
        rows.append(dict(cell=cell, N=len(ii), lnB_mean=float(ll.mean()), lnB_sd_noise=float(ll.std(ddof=1)),
                         lnB_quantiles=np.quantile(ll, [.05, .5, .95]).tolist(), min_component_ESS=float(stats["ESS"][both].min()),
                         max_weight=float(stats["max_weight"][both].max()), max_lnB_MC_sd=float(stats["lnB_MC_sd"][ii].max()),
                         draws_passing_precision=int(pass_precision[ii].sum())))
    result = dict(status="PHASE_MARGINAL_SOURCE_PILOT_NOT_ACCEPTED", family=args.family, seed=args.seed, draws=args.draws,
                  evaluations=done, rows=rows, integration_controls=metadata, source_parameters_integrated=7,
                  source_parameters_sampled=6, phase_integrated_numerically=True, both_phase_branches_kept=True,
                  all_precision_pass=bool(pass_precision.all()), draws_passing_precision=int(pass_precision.sum()),
                  ESS_range=[float(stats["ESS"].min()), float(stats["ESS"].max())], no_C6_change=True,
                  independent_repeat=False, rate_control=False, registration_sha256=se.sha(REG),
                  hashes={p.name:se.sha(p) for p in folder.glob("*.npz")})
    se.write(folder/"RESULT.json", result)
    print(json.dumps({k:result[k] for k in ("status", "draws", "evaluations", "draws_passing_precision", "ESS_range")}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["register", "run", "benchmark"])
    parser.add_argument("--family", choices=se.FAMILIES, default="IMRPhenomXPHM")
    parser.add_argument("--seed", type=int, default=130801)
    parser.add_argument("--draws", type=int, default=1024)
    parser.add_argument("--processes", type=int, default=6)
    args = parser.parse_args()
    if args.command == "register":
        register()
    elif args.command == "benchmark":
        state = se.load_state()
        begin = time.monotonic()
        value, meta = phase_marginal_loglikes(args.family, np.array([22/60, (39/33-1)/2, .45/.8, .37/.8, (np.cos(.6)+.95)/1.9, .5]), state)
        print(json.dumps(dict(seconds=time.monotonic()-begin, components=len(value), **meta)), flush=True)
    else:
        run(args)
