"""Independent arithmetic, custody and waveform-rate audit of importance draws."""
import argparse
import json
import time
import numpy as np
import source_evidence as se


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_name")
    args = parser.parse_args()
    folder = se.ROOT/"importance_runs"/args.run_name
    result = json.loads((folder/"RESULT.json").read_bytes())
    for name, value in result["hashes"].items():
        if se.sha(folder/name) != value:
            raise ValueError("Result arrays changed")
    if result["registration_sha256"] != se.sha(se.REG):
        raise ValueError("Registered inputs changed")
    with np.load(folder/"PROPOSALS.npz") as f:
        u, logq, inside = f["unit_cube"].copy(), f["logq"].copy(), f["inside"].copy()
    with np.load(folder/"RESULT_ARRAYS.npz") as f:
        scientific = {k:f[k].copy() for k in f.files}
    count = len(scientific["logz"])
    values = np.full((len(u), count), -np.inf)
    seen = np.zeros(len(u), dtype=bool)
    for path in sorted(folder.glob("chunk_*.npz")):
        with np.load(path) as f:
            ii = f["indices"]
            if np.any(seen[ii]) or not np.all(inside[ii]):
                raise ValueError("Duplicate or outside-support evaluation")
            values[ii] = f["components"]
            seen[ii] = True
    if not np.array_equal(inside, seen):
        raise ValueError("Unaccounted proposal points")
    if not np.array_equal(inside, np.all((u >= 0)&(u <= 1), axis=1)):
        raise ValueError("Prior support flag is incorrect")
    maxima = np.zeros(count, dtype=int)
    logz, ess, maxw = [], [], []
    posterior_weights = np.empty_like(values)
    # Long-double shifted direct sums, separate from scipy.logsumexp production.
    for k in range(count):
        z = np.asarray(values[:, k]-logq, dtype=np.longdouble)
        shift = np.max(z)
        w = np.exp(z-shift)
        total = np.sum(w, dtype=np.longdouble)
        normalized = w/total
        logz.append(float(shift+np.log(total)-np.log(np.longdouble(len(u)))))
        ess.append(float(total*total/np.sum(w*w, dtype=np.longdouble)))
        maxw.append(float(np.max(normalized)))
        maxima[k] = np.argmax(normalized)
        posterior_weights[:, k] = normalized
    logz, ess, maxw = np.array(logz), np.array(ess), np.array(maxw)
    n = count//2
    error = dict(logz=float(np.max(np.abs(logz-scientific["logz"]))),
                 ESS_relative=float(np.max(np.abs(ess-scientific["ESS"])/ess)),
                 maximum_weight=float(np.max(np.abs(maxw-scientific["max_weight"]))),
                 lnB=float(np.max(np.abs(logz[n:]-logz[:n]-scientific["lnB"]))))
    if max(error.values()) > 1e-10:
        raise ValueError("Independent integral arithmetic differs")
    state = se.load_state()
    checks = []
    selected = np.unique(maxima)
    for iteration, index in enumerate(selected):
        x = se.prior_transform(u[index])
        got = se.component_loglikes(result["family"], x, state)
        original_error = float(np.max(np.abs(got-values[index])))
        if original_error > 1e-7:
            raise ValueError("Waveform reevaluation differs")
        refined = se.component_loglikes(result["family"], x, state, sample_rate=16384)
        active = posterior_weights[index] >= .01
        error_active = float(np.max(np.abs(refined[active]-got[active]))) if active.any() else 0.
        checks.append(dict(index=int(index), components_above_one_percent=int(active.sum()),
                           original_evaluation_error=original_error, max_logL_change_active=error_active,
                           max_logL_change_all=float(np.max(np.abs(refined-got)))))
        if iteration%10 == 0:
            print(json.dumps(dict(rate_checks_done=iteration+1, total=len(selected))), flush=True)
    out = dict(status="PASS_ARITHMETIC_AND_RATE" if all(c["max_logL_change_active"] <= .1 for c in checks) else "RATE_CONTROL_FAILED",
               arithmetic_errors=error, waveform_checks=checks,
               max_active_logL_rate_change=max(c["max_logL_change_active"] for c in checks),
               unique_dominant_samples=len(selected), all_prior_draws_in_denominator=len(u), outside_prior_zero=int((~inside).sum()),
               precision_pass=result["all_draws_pass_precision"], independent_repeat=False,
               scientific_acceptance=False, scope="Arithmetic/rate controls do not replace ESS, repeats or source-model adequacy",
               hashes={"RESULT.json":se.sha(folder/"RESULT.json"), "source":se.sha(se.ROOT/se.Path(__file__).name)})
    se.write(folder/"AUDIT.json", out)
    print(json.dumps({k:out[k] for k in ("status", "precision_pass", "unique_dominant_samples", "max_active_logL_rate_change")}), flush=True)


if __name__ == "__main__":
    main()
