"""Numerical checks for the local Lambda Fisher diagnostic."""
import json
from pathlib import Path
import numpy as np
from asimov_lambda import (
    FIDUCIAL, BETA_TGL, beta_observables, camb_observables, compute, covariance,
)

base = json.loads(Path(__file__).with_name("RESULTADO_ASIMOV_LAMBDA.json").read_text(encoding="utf-8"))
main = next(r for r in base["runs"] if r["mnu_eV"] == 0.06)
checks = {}
checks["beta_is_runtime_alpha_sqrt_e"] = BETA_TGL == 0.0072973525693 * np.sqrt(np.e)
checks["A_Bprime_same_beta_derivative"] = main["A_Bprime_beta_jacobian_max_abs"] < 1e-12
checks["closure_E0"] = abs(main["check"]["A"]["K_at_0"]) < 1e-12
checks["fisher_full_rank"] = all(v["rank"] == 6 for v in main["cases"].values())
checks["covariances_positive_definite"] = all(np.min(np.linalg.eigvalsh(covariance(c))) > 0 for c in (False, True))
checks["all_gate_variants_underpowered"] = all(v["gate"] == "UNDERPOWERED_DO_NOT_OPEN_DATA" for v in main["cases"].values())
checks["beta0_exact_camb_baseline"] = main["check"]["A"]["baseline_max_abs"] < 1e-10

steps = {}
ref = main["cases"]["A_bare_corrected"]["sigma_beta"]
for step in (0.005, 0.02):
    r = compute(0.06, step=step)
    sigma = r["cases"]["A_bare_corrected"]["sigma_beta"]
    steps[str(step)] = {"sigma_beta": sigma, "fractional_from_step_0p01": sigma / ref - 1,
                        "gate": r["cases"]["A_bare_corrected"]["gate"]}
checks["parameter_step_convergence"] = all(abs(v["fractional_from_step_0p01"]) < 0.005 for v in steps.values())

beta_steps = {}
deriv_ref = None
for h in (5e-5, 1e-4, 2e-4):
    yp, _ = beta_observables(FIDUCIAL, 0.06, "A", "bare", +h)
    ym, _ = beta_observables(FIDUCIAL, 0.06, "A", "bare", -h)
    deriv = (yp - ym) / (2*h)
    if deriv_ref is None:
        deriv_ref = deriv
    beta_steps[str(h)] = {"max_abs_difference_from_5e_minus5": float(np.max(np.abs(deriv - deriv_ref))),
                          "derivative_planck_R": float(deriv[0]),
                          "derivative_planck_lA": float(deriv[1])}
checks["beta_step_convergence"] = all(v["max_abs_difference_from_5e_minus5"] < 0.02 for v in beta_steps.values())

result = {"checks": {k: bool(v) for k, v in checks.items()}, "passed": bool(all(checks.values())),
          "parameter_step_sensitivity": steps, "beta_step_sensitivity": beta_steps,
          "observed_means_used": False}
p = Path(__file__).with_name("SELFTEST_ASIMOV_LAMBDA.json")
t = p.with_suffix(".json.tmp")
t.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
t.replace(p)
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["passed"] else 1)
