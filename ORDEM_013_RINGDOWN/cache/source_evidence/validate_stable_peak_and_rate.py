"""Validate the copied phase-zero peak model; diagnose remaining rate errors.

The tangent projection is only a selected-source diagnostic. It neither changes
the source prior nor counts as an integrated-evidence or coverage test.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import continuous_phase_source as cp
import peak_phase_coordinates as pc
import stable_peak_imr_model as stable
from diagnose_generator_alignment import targets_for_source

FOLDER = se.ROOT/"stable_peak_validation"


def main():
    pm.check()
    FOLDER.mkdir(exist_ok=False)
    provenance = json.loads((se.ROOT/"STABLE_PEAK_MODEL_PROVENANCE.json").read_bytes())
    for key in ("source", "copy"):
        if se.sha(se.ROOT/provenance[key]) != provenance[key+"_sha256"]:
            raise ValueError("Model changed after copied refinement")
    names = ["validate_stable_peak_and_rate.py", "stable_peak_imr_model.py", "STABLE_PEAK_MODEL_PROVENANCE.json",
             "generator_alignment_diagnostic/RESULT.json", "coherent_imr_model.py", "INJECTIONS.npz"]
    se.write(FOLDER/"REGISTRATION.json", dict(date_utc=datetime.now(timezone.utc).isoformat(),
             status="REGISTERED_NUMERICAL_COPY_VALIDATION_AND_RATE_DIAGNOSTIC",
             hypothesis="The one-line copied correction reproduces phase-zero alignment; a separate time/phase tangent diagnostic distinguishes geometric alignment from remaining waveform-shape error.",
             physical_prior_changed=False, evidence_acceptance=False, C6_changed=False,
             hashes={n:se.sha(se.ROOT/n) for n in names}))
    state = se.load_state()
    source = next(s for s in se.SOURCES if s["name"] == "source_90")
    x = se.source_vector(source)
    targets = targets_for_source(state, source["name"])
    validations, rate_rows = [], []
    rates = (32768, 65536, 131072)
    for family in se.FAMILIES:
        mf, spin = stable.remnant(family, source["mass"]*source["q"]/(1+source["q"]),
                                  source["mass"]/(1+source["q"]), source["s1"], source["s2"])
        for rate in rates:
            with np.load(se.ROOT/f"generator_alignment_diagnostic/{family}_{rate}.npz") as data:
                raw = dict(samples=data["common_phase_zero_peak_raw"].copy(), times=state["times"],
                           remnant_mass=mf, remnant_spin=spin, n=16, family=family)
            for psd in ("O4", "O5"):
                white = state[psd+"_white"]
                bank = cp.make_bank(raw, "R-B", [0., 1.], white)
                for phase in (.173, .619, 1.413):
                    y = x.copy(); y[5] = phase
                    for a in (0, 1):
                        original, meta = stable.network_basis(family, y, state["times"], "R-B", a, white, rate)
                        approx = pc.evaluate_bank(bank, [phase], a)[0]
                        _, logl = se.linear_statistics(original, targets[psd], 3.)
                        error = float(np.max(np.abs(logl-pc.bank_loglikes(bank, [phase], targets[psd], a))))
                        relative = float(np.linalg.norm(original-approx)/np.linalg.norm(original))
                        validations.append(dict(family=family, rate=rate, psd=psd, phase=phase, a=a,
                                                relative_error=relative, max_logL_error=error,
                                                passes=bool(relative <= 1e-6 and error <= .001)))
        # A rate comparison after fitting only the already-existing nuisance
        # directions. A small projected error is not evidence convergence.
        for low, high in zip(rates[:-1], rates[1:]):
            for a in (0., 1.):
                for psd in ("O4", "O5"):
                    white = state[psd+"_white"]
                    def basis(z, rate):
                        return stable.network_basis(family, z, state["times"], "R-B", a, white, rate)[0]
                    bh, bl = basis(x, high), basis(x, low)
                    orientation = np.array([np.cos(2*source["psi"]), np.sin(2*source["psi"])])
                    amplitude = 600./np.linalg.norm(bh@orientation)
                    target = bh@orientation*amplitude
                    coefficients = np.linalg.lstsq(bl, target, rcond=None)[0]
                    residual = target-bl@coefficients
                    derivatives, convergence = [], []
                    for index, step in ((5, 1e-5), (6, 1e-4)):
                        estimates = []
                        for h in (step, step/2):
                            up, down = x.copy(), x.copy()
                            up[index] += h; down[index] -= h
                            estimates.append(((basis(up, low)-basis(down, low))/(2*h))@coefficients)
                        convergence.append(float(np.linalg.norm(estimates[1]-estimates[0])/np.linalg.norm(estimates[1])))
                        derivatives.append(estimates[1])
                    design = np.column_stack([bl]+derivatives)
                    # Normalize columns before least squares because time is ms.
                    norms = np.linalg.norm(design, axis=0)
                    coefficient = np.linalg.lstsq(design/norms, residual, rcond=None)[0]/norms
                    projected = residual-design@coefficient
                    shifted = x.copy(); shifted[5] += coefficient[2]; shifted[6] += coefficient[3]
                    moved = basis(shifted, low)
                    exact_coefficients = np.linalg.lstsq(moved, target, rcond=None)[0]
                    exact_residual = target-moved@exact_coefficients
                    rate_rows.append(dict(family=family, psd=psd, a=a, low_rate=low, high_rate=high, snr=600.,
                        source=source["name"], phase=source["phase"],
                        common_amplitude_residual_norm=float(np.linalg.norm(residual)),
                        tangent_residual_norm=float(np.linalg.norm(projected)),
                        direct_shifted_residual_norm=float(np.linalg.norm(exact_residual)),
                        delta_orbital_phase=float(coefficient[2]), delta_peak_ms=float(coefficient[3]),
                        derivative_relative_convergence=convergence,
                        scope="Noiseless selected-source profile diagnostic; no prior marginalization or posterior calibration"))
            print(json.dumps(dict(family=family, low_rate=low, high_rate=high, done=True)), flush=True)
    result = dict(status="PASS_COPIED_PHASE_ALIGNMENT" if all(r["passes"] for r in validations) else "FAIL_COPIED_PHASE_ALIGNMENT",
                  checks=validations, count=len(validations), max_waveform_error=max(r["relative_error"] for r in validations),
                  max_logL_error=max(r["max_logL_error"] for r in validations), rate_diagnostics=rate_rows,
                  scientific_acceptance=False, registered_running_model_unchanged=True,
                  scope="Phase copy validated for source90, two families, three rates, two hypotheses, two PSDs, three held-out phases up toSNR600; not full source-prior validation",
                  registration_sha256=se.sha(FOLDER/"REGISTRATION.json"))
    se.write(FOLDER/"RESULT.json", result)
    print(json.dumps({k:result[k] for k in ("status", "count", "max_waveform_error", "max_logL_error")}), flush=True)


if __name__ == "__main__":
    main()
