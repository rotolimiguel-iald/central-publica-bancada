"""Held-out phase tests at source points spanning the unchanged physical prior."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import argparse
import json
import multiprocessing as mp
import numpy as np
from scipy.stats import qmc
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import stable_peak_imr_model as model
import stable_peak_phase_source as phase_model

FOLDER = se.ROOT/"stable_phase_prior_controls"
_STATE = None
_TARGETS = None


def initialize():
    global _STATE, _TARGETS
    _STATE = se.load_state()
    _TARGETS = {}
    for psd in ("O4", "O5"):
        labels = [l for l in _STATE["labels"] if l["psd"] == psd]
        with np.load(se.ROOT/f"cache/recolored_noise/{psd}_noise.npz") as data:
            noise = np.hstack([data[d+"_strain_scaled"][50:100]@_STATE[psd+"_white"].T for d in ("H1", "L1")])
        ns = noise[[l["noise_index"]-50 for l in labels]]
        signals = _STATE[psd+"_targets"]-ns
        _TARGETS[psd] = np.vstack([signals*(snr/40.)+ns for snr in (40., 600.)])


def evaluate(job):
    name, x, family, rate = job
    x = np.array(x)
    rows = []
    raw = phase_model.raw_phase_samples(family, x, _STATE["times"], sample_rate=rate)
    for psd in ("O4", "O5"):
        white = _STATE[psd+"_white"]
        bank = phase_model.make_bank(raw, "R-B", [0., .37, 1.], white)
        for phase in (.173, .619, 1.413):
            y = x.copy(); y[5] = phase
            for index, strength in enumerate((0., .37, 1.)):
                direct, meta = model.network_basis(family, y, _STATE["times"], "R-B", strength, white, rate)
                approx = pc.evaluate_bank(bank, [phase], index)[0]
                relative = float(np.linalg.norm(direct-approx)/np.linalg.norm(direct))
                _, logl = se.linear_statistics(direct, _TARGETS[psd], 3.)
                interpolation = pc.bank_loglikes(bank, [phase], _TARGETS[psd], index)
                errors = np.abs(logl-interpolation).reshape(2, 600).max(axis=1)
                rows.append(dict(psd=psd, phase=phase, strength=strength, relative_waveform_error=relative,
                                 max_logL_errors_SNR40_600=errors.tolist(),
                                 passes=bool(relative <= 1e-6 and errors.max() <= .001)))
    result = dict(source=name, family=family, rate=rate, coordinates=x.tolist(), controls=rows,
                  max_error=max(max(r["max_logL_errors_SNR40_600"]) for r in rows),
                  passes=all(r["passes"] for r in rows))
    se.write(FOLDER/f"{name}_{family}_{rate}.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--processes", type=int, default=2)
    args = parser.parse_args()
    pm.check()
    FOLDER.mkdir(exist_ok=False)
    provenance = json.loads((se.ROOT/"STABLE_PHASE_API_PROVENANCE.json").read_bytes())
    for key in ("source", "copy"):
        if se.sha(se.ROOT/provenance[key]) != provenance[key+"_sha256"]:
            raise ValueError("Phase API custody differs")
    unit = qmc.LatinHypercube(7, seed=130872).random(4)
    points = [(s["name"], se.source_vector(s).tolist()) for s in se.SOURCES]
    points += [(f"prior_{i}", se.prior_transform(u).tolist()) for i,u in enumerate(unit)]
    jobs = [(name, x, family, rate) for name,x in points for family in se.FAMILIES for rate in (8192, 16384)]
    names = ["validate_stable_phase_prior.py", "stable_peak_imr_model.py", "stable_peak_phase_source.py",
             "STABLE_PHASE_API_PROVENANCE.json", "INJECTIONS.npz", "phase_runs/REGISTRATION.json"]
    registration = dict(status="REGISTERED_NUMERICAL_PRIOR_POINT_CONTROLS", date_utc=datetime.now(timezone.utc).isoformat(),
                        seed=130872, new_points_unit_cube=unit.tolist(), all_points=points, rates=[8192,16384],
                        phases=[.173,.619,1.413], strengths=[0.,.37,1.], snrs=[40.,600.], reading="R-B",
                        scope="Three reference sources plus four stratified prior points, not a bound over every prior point or posterior calibration",
                        unchanged=["running integral", "C6", "physical prior", "frozen8192Hz injections"],
                        hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(FOLDER/"REGISTRATION.json", registration)
    results = []
    with mp.get_context("fork").Pool(args.processes, initializer=initialize) as pool:
        for result in pool.imap_unordered(evaluate, jobs, chunksize=1):
            results.append(result)
            print(json.dumps({k:result[k] for k in ("source","family","rate","max_error","passes")}), flush=True)
    controls = [c for result in results for c in result["controls"]]
    summary = dict(status="PASS_PRIOR_POINT_PHASE_CONTROLS" if all(c["passes"] for c in controls) else "FAIL_PRIOR_POINT_PHASE_CONTROLS",
                   count=len(controls), failures=sum(not c["passes"] for c in controls),
                   max_logL_errors_SNR40_600=np.max([c["max_logL_errors_SNR40_600"] for c in controls],axis=0).tolist(),
                   max_relative_waveform_error=max(c["relative_waveform_error"] for c in controls),
                   results=results, scientific_acceptance=False, global_uniform_prior_bound=False,
                   registration_sha256=se.sha(FOLDER/"REGISTRATION.json"))
    se.write(FOLDER/"RESULT.json",summary)
    print(json.dumps({k:v for k,v in summary.items() if k != "results"}),flush=True)


if __name__=="__main__":
    main()
