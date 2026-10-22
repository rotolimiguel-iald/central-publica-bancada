"""Isolate orbital-phase peak jitter from waveform-rate errors.

Diagnostic only: the registered inference and frozen injections are unchanged.
Every alignment uses the same intrinsic complex-22 peak, either recomputed for
each phase or computed once at phase zero. It is not a new physical clock.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import argparse
import json
import multiprocessing as mp
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import continuous_phase_source as cp

FOLDER = se.ROOT / "generator_alignment_diagnostic"
RATES = (32768, 65536, 131072)
PHASES = (.173, .619, 1.413)
SNRS = (40., 200., 600.)


def targets_for_source(state, source):
    output = {}
    for psd in ("O4", "O5"):
        labels = [l for l in state["labels"] if l["psd"] == psd]
        ids = [i for i, l in enumerate(labels) if l["source"] == source]
        with np.load(se.ROOT / f"cache/recolored_noise/{psd}_noise.npz") as data:
            noise = np.hstack([data[d+"_strain_scaled"][50:100] @ state[psd+"_white"].T for d in ("H1", "L1")])
        ns = noise[[labels[i]["noise_index"]-50 for i in ids]]
        signal = state[psd+"_targets"][ids]-ns
        if np.max(np.abs(np.linalg.norm(signal, axis=1)-40.)) > 1e-10:
            raise ValueError("Frozen injection normalization differs")
        output[psd] = np.vstack([signal*(s/40.)+ns for s in SNRS])
    return output


def raw_at_phase(family, coordinates, times, rate, phase, reference_peak):
    x = coordinates.copy()
    x[5] = phase
    curves, mf, spin, peak = se.model.source_curves(family, tuple(x[:6]), rate, True)
    t = times-x[6]*1e-3
    outputs = {}
    for alignment, shift in (("per_phase_peak", 0.), ("common_phase_zero_peak", reference_peak-peak)):
        samples = []
        for name in ("all", "22", "44"):
            p, c, start, end, ratio = curves[name]
            position = t+shift
            if position.min() < start or (position.max() > end and ratio > 1e-5):
                raise ValueError("Missing diagnostic waveform interval")
            hp, hc = np.array(p(position)), np.array(c(position))
            hp[position > end], hc[position > end] = 0., 0.
            if not np.all(np.isfinite(hp)) or not np.all(np.isfinite(hc)):
                raise ValueError("Nonfinite diagnostic curve")
            samples.append(np.array([hp, hc]))
        outputs[alignment] = np.array(samples)
    return outputs, float(peak), float(mf), float(spin)


def task(job):
    family, rate = job
    state = se.load_state()
    source = next(s for s in se.SOURCES if s["name"] == "source_90")
    x = se.source_vector(source)
    x[5] = 0.
    _, _, _, peak_zero = se.model.source_curves(family, tuple(x[:6]), rate, True)
    targets = targets_for_source(state, source["name"])
    samples = {k: [] for k in ("per_phase_peak", "common_phase_zero_peak")}
    peaks = []
    for phase in 2*np.pi*np.arange(16)/16:
        evaluated, peak, mf, spin = raw_at_phase(family, x, state["times"], rate, phase, peak_zero)
        peaks.append(peak)
        for name in samples:
            samples[name].append(evaluated[name])
    direct = {}
    for phase in PHASES:
        direct[phase] = raw_at_phase(family, x, state["times"], rate, phase, peak_zero)[0]
    rows, arrays = [], {}
    t = state["times"]-x[6]*1e-3
    for alignment, values in samples.items():
        raw = dict(samples=np.array(values), times=t, remnant_mass=mf, remnant_spin=spin,
                   n=16, sample_rate=rate, family=family, coordinates=x.copy())
        arrays[alignment+"_raw"] = raw["samples"]
        for psd in ("O4", "O5"):
            white, data = state[psd+"_white"], targets[psd]
            bank = cp.make_bank(raw, "R-B", [0., 1.], white)
            integrals, quadrature = cp.marginal_loglikes(bank, data)
            arrays[alignment+"_"+psd+"_log_integrals"] = integrals
            controls = []
            for phase in PHASES:
                direct_raw = dict(raw, samples=direct[phase][alignment][None, :], n=1)
                direct_bank = cp.make_bank(direct_raw, "R-B", [0., 1.], white)
                for j, a in enumerate((0., 1.)):
                    original = direct_bank["samples"][j, 0]
                    reconstructed = pc.evaluate_bank(bank, [phase], j)[0]
                    _, full_logl = se.linear_statistics(original, data, 3.)
                    interp_logl = pc.bank_loglikes(bank, [phase], data, j)
                    errors = np.abs(full_logl-interp_logl).reshape(3, 200).max(axis=1)
                    relative = float(np.linalg.norm(original-reconstructed)/np.linalg.norm(original))
                    controls.append(dict(phase=phase, strength=a, relative_waveform_error=relative,
                                         max_logL_error_by_SNR=errors.tolist(),
                                         passes=bool(relative <= 1e-6 and errors.max() <= .001)))
            rows.append(dict(alignment=alignment, psd=psd, quadrature=quadrature, controls=controls))
    arrays["phase_grid_peaks"] = np.array(peaks)
    se.save_arrays(FOLDER/f"{family}_{rate}.npz", **arrays)
    result = dict(family=family, rate=rate, source=source["name"], peak_zero_s=peak_zero,
                  phase_peak_span_s=float(np.ptp(peaks)), rows=rows)
    se.write(FOLDER/f"{family}_{rate}.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processes", type=int, default=2)
    args = parser.parse_args()
    pm.check()
    FOLDER.mkdir(exist_ok=False)
    names = ["diagnose_generator_alignment.py", "coherent_imr_model.py", "source_evidence.py",
             "continuous_phase_source.py", "peak_phase_coordinates.py", "INJECTIONS.npz"]
    registration = dict(status="REGISTERED_DISCOVERY_NUMERICAL_CONTROL", date_utc=datetime.now(timezone.utc).isoformat(),
                        source="source_90", families=se.FAMILIES, rates=RATES, snrs=SNRS,
                        phases=PHASES, strengths=[0., 1.], reading="R-B",
                        hypothesis="Phase-dependent minimization noise can spoil the finite Fourier representation; a common phase-zero intrinsic peak should remove that error. Rate errors may have a different cause.",
                        unchanged=["physical source", "clock reading", "source priors", "injections", "C6", "running integration"],
                        scope="Selected-source diagnostic, not posterior calibration; frozen8192Hz injections scaled to each SNR",
                        hashes={n: se.sha(se.ROOT/n) for n in names})
    se.write(FOLDER/"REGISTRATION.json", registration)
    jobs = [(family, rate) for family in se.FAMILIES for rate in RATES]
    results = []
    with mp.get_context("fork").Pool(args.processes) as pool:
        for result in pool.imap_unordered(task, jobs, chunksize=1):
            results.append(result)
            print(json.dumps(dict(family=result["family"], rate=result["rate"], peak_span_s=result["phase_peak_span_s"])), flush=True)
    comparisons = []
    for family in se.FAMILIES:
        for alignment in ("per_phase_peak", "common_phase_zero_peak"):
            for psd in ("O4", "O5"):
                loaded = []
                for rate in RATES:
                    with np.load(FOLDER/f"{family}_{rate}.npz") as data:
                        loaded.append(data[alignment+"_"+psd+"_log_integrals"].reshape(2, 3, 200))
                changes = [np.max(np.abs(b-a), axis=(0, 2)).tolist() for a, b in zip(loaded[:-1], loaded[1:])]
                comparisons.append(dict(family=family, alignment=alignment, psd=psd, max_rate_logL_changes_by_SNR=changes))
    summary = []
    for alignment in ("per_phase_peak", "common_phase_zero_peak"):
        controls = [c for r in results for row in r["rows"] if row["alignment"] == alignment for c in row["controls"]]
        summary.append(dict(alignment=alignment, controls=len(controls), failures=sum(not c["passes"] for c in controls),
                            max_logL_error_by_SNR=np.max([c["max_logL_error_by_SNR"] for c in controls], axis=0).tolist(),
                            max_waveform_error=max(c["relative_waveform_error"] for c in controls)))
    output = dict(status="GENERATOR_ALIGNMENT_DIAGNOSTIC_NOT_SCIENTIFIC_ACCEPTANCE", results=results,
                  interpolation_summary=summary, rate_comparisons=comparisons,
                  registration_sha256=se.sha(FOLDER/"REGISTRATION.json"),
                  hashes={p.name: se.sha(p) for p in FOLDER.glob("*.npz")})
    se.write(FOLDER/"RESULT.json", output)
    print(json.dumps(dict(status=output["status"], interpolation_summary=summary)), flush=True)


if __name__ == "__main__":
    main()
