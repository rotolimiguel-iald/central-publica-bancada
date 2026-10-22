"""Adapt the computational proposal to the completed phase-integrated pilot.

All 2400 normalized posterior targets enter with equal weight. The original
physical prior, phase quadrature, model and rejection criteria are unchanged.
New estimates use fresh independent draws, never fitted samples as a validation.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
import argparse
from datetime import datetime, timezone
import json
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_normal
import source_evidence as se
import phase_marginal_source as pm
from audit_phase_source import load_run, direct_statistics


def weighted_fit(u, weights, count=12, floor=1e-4, seed=130810):
    """Regularized EM for a proposal, with no change of physical prior."""
    d = u.shape[1]
    weights = weights/weights.sum()
    rng = np.random.default_rng(seed)
    centers = u[rng.choice(len(u), count, replace=False, p=weights)].copy()
    mean = np.sum(weights[:, None]*u, axis=0)
    covariance = np.einsum("n,ni,nj->ij", weights, u-mean, u-mean)+np.eye(d)*floor
    shapes = np.repeat(covariance[None], count, axis=0)
    mixture = np.ones(count)/count
    history = []
    for iteration in range(100):
        logits = np.column_stack([np.log(mixture[k])+multivariate_normal.logpdf(u, centers[k], shapes[k]) for k in range(count)])
        norm = logsumexp(logits, axis=1)
        resp = np.exp(logits-norm[:, None])*weights[:, None]
        amounts = resp.sum(axis=0)
        for k in range(count):
            if amounts[k] < 1e-8:
                centers[k] = u[rng.choice(len(u), p=weights)]
                shapes[k] = covariance.copy()
                continue
            centers[k] = np.sum(resp[:, k, None]*u, axis=0)/amounts[k]
            delta = u-centers[k]
            shapes[k] = np.einsum("n,ni,nj->ij", resp[:, k]/amounts[k], delta, delta)+np.eye(d)*floor
        mixture = np.maximum(amounts, 1e-5)
        mixture /= mixture.sum()
        history.append(float(weights@norm))
    components = [dict(weight=float(.7*(.9*mixture[k]+.1/count)), mean=centers[k].tolist(),
                       shape=(2*shapes[k]).tolist()) for k in range(count)]
    return components, history


def fit(args):
    folder = pm.DIRECTORY/args.training
    result, u, logq, inside, values, stats = load_run(folder)
    independent, posterior_weights = direct_statistics(values, logq)
    if max(float(np.max(np.abs(independent[k]-stats[k]))) for k in independent)>1e-9:
        raise ValueError("Training arithmetic not verified")
    weights = posterior_weights.mean(axis=1)
    components, history = weighted_fit(u[inside], weights[inside])
    previous = json.loads((pm.DIRECTORY/"PROPOSAL.json").read_bytes())
    previous_total = sum(c["weight"] for c in previous["components"])
    for c in previous["components"]:
        components.append(dict(mean=c["mean"], shape=c["shape"], weight=.2*c["weight"]/previous_total))
    if abs(sum(c["weight"] for c in components)+.1-1)>1e-12:
        raise ValueError("Incorrect mixture normalization")
    for c in components:
        np.linalg.cholesky(c["shape"])
    stage = se.ROOT/args.stage
    stage.mkdir(exist_ok=False)
    proposal = dict(status="ADAPTED_PHASE_PROPOSAL_NOT_PHYSICAL_PRIOR", defensive_weight=.1, df=5.,
        components=components, fit_history=history, floor=1e-4, inflation=2.,
        fitting_seed=130810, fitted_mixture_mass=.7, previous_mixture_mass=.2,
        training_pooled_ESS=float(1/np.sum(weights**2)), training_accepted_as_science=False,
        training_result_sha256=se.sha(folder/"RESULT.json"), all_targets_equal_in_training=True,
        physical_prior_changed=False)
    se.write(stage/"PROPOSAL.json", proposal)
    files = [se.Path(__file__), se.ROOT/"audit_phase_source.py", pm.REG, folder/"RESULT.json", stage/"PROPOSAL.json"]
    reg = dict(status="REGISTERED_ADAPTIVE_COMPUTATIONAL_PROPOSAL", date_utc=datetime.now(timezone.utc).isoformat(),
        training=args.training, likelihood_registration_sha256=se.sha(pm.REG),
        scientific_acceptance=False, prior_changed=False, C6_changed=False,
        scope="70% phase-trained Student-t mixture,20% previous mixture,10% full original prior. Same2400 targets, fresh independent draws required.",
        acceptance="Original ESS>=100,maxweight<=.05,MCsdlnB<=.2; independent repeats and rate/source checks remain mandatory",
        hashes={str(p.relative_to(se.ROOT)):se.sha(p) for p in files})
    se.write(stage/"ADAPTATION.json", reg)
    print(json.dumps(dict(status=reg["status"], stage=args.stage, components=len(components),
        training_pooled_ESS=proposal["training_pooled_ESS"], prior_changed=False)), flush=True)


def run(args):
    stage = se.ROOT/args.stage
    reg = json.loads((stage/"ADAPTATION.json").read_bytes())
    for name, expected in reg["hashes"].items():
        if se.sha(se.ROOT/name) != expected:
            raise ValueError("Adaptive registration changed: "+name)
    # Only the proposal and result directory change. pm.REG and all checked
    # physical-model inputs remain those of the original phase registration.
    pm.DIRECTORY = stage
    pm.run(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["fit", "run"])
    parser.add_argument("--training", default="IMRPhenomXPHM_seed130801_N1024")
    parser.add_argument("--stage", default="phase_adapted_130801")
    parser.add_argument("--family", choices=se.FAMILIES, default="IMRPhenomXPHM")
    parser.add_argument("--seed", type=int, default=130811)
    parser.add_argument("--draws", type=int, default=2048)
    parser.add_argument("--processes", type=int, default=6)
    args = parser.parse_args()
    if args.command == "fit":
        fit(args)
    else:
        run(args)
