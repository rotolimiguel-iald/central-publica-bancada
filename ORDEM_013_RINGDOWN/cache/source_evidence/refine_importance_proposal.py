"""Learn a new proposal from a completed independent pilot, keep prior fixed."""
import argparse
import json
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
from importance_source_evidence import fit_gaussians


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_name")
    parser.add_argument("proposal_name")
    args = parser.parse_args()
    folder = se.ROOT/"importance_runs"/args.run_name
    report = json.loads((folder/"RESULT.json").read_bytes())
    for name, expected in report["hashes"].items():
        if se.sha(folder/name) != expected:
            raise ValueError("Training run changed")
    with np.load(folder/"PROPOSALS.npz") as f:
        u, logq, inside = f["unit_cube"].copy(), f["logq"].copy(), f["inside"].copy()
    with np.load(folder/"RESULT_ARRAYS.npz") as f:
        logz = f["logz"].copy()
    values = np.full((len(u), len(logz)), -np.inf)
    seen = np.zeros(len(u), dtype=bool)
    for path in sorted(folder.glob("chunk_*.npz")):
        with np.load(path) as f:
            indices = f["indices"]
            if np.any(seen[indices]):
                raise ValueError("Repeated training points")
            values[indices] = f["components"]
            seen[indices] = True
    if not np.array_equal(inside, seen):
        raise ValueError("Missing inside-prior evaluation")
    logw = values[inside]-logq[inside, None]-logz[None, :]-np.log(len(u))
    if np.max(np.abs(logsumexp(logw, axis=0))) > 1e-10:
        raise ValueError("Per-component training weights are not normalized")
    weights = np.exp(logsumexp(logw, axis=1)-np.log(len(logz)))
    # Rescale only computational coordinates during fitting: the preexisting
    # covariance floor 1e-4 becomes 6.25e-6 in unit-prior coordinates. No physical
    # prior narrows, and heavy tails plus 10% original-prior draws are retained.
    fitted = fit_gaussians(4*u[inside], weights, count=24, seed=130706)
    for component in fitted["components"]:
        component["mean"] = (np.array(component["mean"])/4).tolist()
        component["shape"] = (np.array(component["shape"])/16).tolist()
    fitted.update(status="COMPUTATIONAL_PROPOSAL_NOT_PHYSICAL_PRIOR", family=report["family"],
                  registration_sha256=se.sha(se.REG), training_run=args.run_name,
                  training_result_sha256=se.sha(folder/"RESULT.json"), training_convergence_assumed=False,
                  all_components_in_training=True, likelihood_or_prior_changed=False,
                  covariance_floor_unit_cube=6.25e-6, fitting_coordinate_scale=4.,
                  source_sha256=se.sha(se.ROOT/se.Path(__file__).name),
                  scope="Adaptive proposal learned from all 2400 weighted targets. Final integrals use new independent draws; training data are not reused as independent validation")
    target = se.ROOT/"runs"/args.proposal_name
    target.mkdir(exist_ok=False)
    se.write(target/"IMPORTANCE_PROPOSAL.json", fitted)
    print(json.dumps(dict(status="REFINED_PROPOSAL_READY", name=args.proposal_name, components=24,
                          training_points=int(inside.sum()), physical_prior_unchanged=True)), flush=True)


if __name__ == "__main__":
    main()
