"""Independent arithmetic and rate audit of the frozen phase-marginal pilot."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
import argparse
import json
import multiprocessing as mp
import numpy as np
import source_evidence as se
import phase_marginal_source as pm


def load_run(folder):
    result = json.loads((folder/"RESULT.json").read_bytes())
    for name, expected in result["hashes"].items():
        if se.sha(folder/name) != expected:
            raise ValueError("Result input changed: "+name)
    if result["registration_sha256"] != se.sha(pm.REG):
        raise ValueError("Phase registration changed")
    pm.check()
    with np.load(folder/"PROPOSALS.npz") as f:
        u, logq, inside = (f[k].copy() for k in ("unit_cube", "logq", "inside"))
    with np.load(folder/"RESULT_ARRAYS.npz") as f:
        stats = {k:f[k].copy() for k in f.files}
    values = np.full((len(u), len(stats["logz"])), -np.inf)
    seen = np.zeros(len(u), dtype=bool)
    for path in sorted(folder.glob("chunk_*.npz")):
        with np.load(path) as f:
            ids = f["indices"]
            if np.any(seen[ids]) or not np.all(inside[ids]):
                raise ValueError("Duplicate or invalid evaluation")
            values[ids] = f["components"]
            seen[ids] = True
    if not np.array_equal(seen, inside) or not np.array_equal(inside, np.all((u>=0)&(u<=1), axis=1)):
        raise ValueError("Unaccounted prior sample")
    return result, u, logq, inside, values, stats


def direct_statistics(values, logq):
    z = np.asarray(values-logq[:, None], dtype=np.longdouble)
    shift = z.max(axis=0)
    w = np.exp(z-shift)
    total = w.sum(axis=0)
    p = w/total
    n, nc = values.shape
    half = nc//2
    logz = shift+np.log(total)-np.log(np.longdouble(n))
    stats = dict(logz=logz, ESS=1/(p*p).sum(axis=0), max_weight=p.max(axis=0),
                 lnB=logz[half:]-logz[:half],
                 lnB_MC_sd=np.sqrt(np.longdouble(n)/(n-1)*((p[:, half:]-p[:, :half])**2).sum(axis=0)))
    return {k:np.asarray(v, dtype=float) for k,v in stats.items()}, np.asarray(p, dtype=float)


def rate_check(item):
    index, u, original, active = item
    got, meta = pm.phase_marginal_loglikes(se._FAMILY, u, se._STATE, sample_rate=16384)
    difference = got-original
    return dict(index=int(index), components_above_one_percent=int(active.sum()),
                max_active_logL_change=float(np.max(np.abs(difference[active]))),
                max_all_logL_change=float(np.max(np.abs(difference))), controls=meta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_name")
    parser.add_argument("--rate", action="store_true")
    parser.add_argument("--processes", type=int, default=6)
    args = parser.parse_args()
    folder = pm.DIRECTORY/args.run_name
    result, u, logq, inside, values, stats = load_run(folder)
    independent, weights = direct_statistics(values, logq)
    errors = {k:float(np.max(np.abs(stats[k]-v))) for k,v in independent.items()}
    if max(errors.values()) > 1e-9:
        raise ValueError("Independent summation differs")
    pool_weights = weights.mean(axis=1)
    average = np.sum(pool_weights[:, None]*u, axis=0)
    covariance = np.einsum("n,ni,nj->ij", pool_weights, u-average, u-average)
    selected = np.unique(np.argmax(weights, axis=0))
    labels = se.load_state()["labels"]
    half = len(labels)
    controls = result["integration_controls"]
    audit = dict(status="PASS_ARITHMETIC_NOT_PRECISION", scientific_acceptance=False,
        draws=len(u), inside=int(inside.sum()), outside=int((~inside).sum()),
        independent_arithmetic_errors=errors,
        ESS_quantiles=np.quantile(stats["ESS"], [0,.25,.5,.75,1]).tolist(),
        max_weight_quantiles=np.quantile(stats["max_weight"], [0,.25,.5,.75,1]).tolist(),
        passed_precision=result["draws_passing_precision"],
        pooled_target_sample_ESS=float(1/np.sum(pool_weights**2)),
        pooled_prior_coordinate_mean=average.tolist(), pooled_covariance=covariance.tolist(),
        pooled_covariance_eigenvalues=np.linalg.eigvalsh(covariance).tolist(),
        unique_dominant_samples=selected.tolist(),
        phase_controls={key:max(c[key] for c in controls) for key in controls[0] if key!="index"},
        diagnostic_points=[dict(index=int(i), pooled_weight=float(pool_weights[i]),
             coordinates=u[i].tolist(), dominant_components=int(np.sum(np.argmax(weights,axis=0)==i)))
             for i in selected],
        hashes={"RESULT.json":se.sha(folder/"RESULT.json"), "source":se.sha(se.Path(__file__))})
    if args.rate:
        jobs = [(int(i), u[i], values[i], weights[i]>=.01) for i in selected]
        checks = []
        with mp.get_context("fork").Pool(args.processes, initializer=se.initialize, initargs=(result["family"],)) as pool:
            for row in pool.imap_unordered(rate_check, jobs):
                checks.append(row)
                print(json.dumps(dict(rate_done=len(checks), total=len(jobs))), flush=True)
        audit["rate_checks"] = sorted(checks, key=lambda v:v["index"])
        audit["max_active_rate_difference"] = max(c["max_active_logL_change"] for c in checks)
        audit["rate_control_pass"] = bool(audit["max_active_rate_difference"]<=.1)
    se.write(folder/("AUDIT_RATE.json" if args.rate else "AUDIT.json"), audit)
    print(json.dumps({k:v for k,v in audit.items() if k not in ("diagnostic_points", "rate_checks", "pooled_covariance", "hashes")}), flush=True)


if __name__ == "__main__":
    main()
