"""Validation of diagnostic fit summaries; no model or observed data is executed."""
import math
from numbers import Real

def finite_number(value, label, *, positive=False, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(label + ": expected a real number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(label + ": non-finite value")
    if positive and value <= 0:
        raise ValueError(label + ": expected a positive value")
    if nonnegative and value < 0:
        raise ValueError(label + ": expected a nonnegative value")
    return value

def validate_fit(fit, parameter_names):
    if not isinstance(fit, dict) or fit.get("sucesso") is not True:
        raise ValueError("fit did not report successful optimization")
    finite_number(fit.get("chi2"), "chi2", nonnegative=True)
    theta = fit.get("theta")
    if not isinstance(theta, dict):
        raise ValueError("fit parameters are missing")
    for name in parameter_names:
        finite_number(theta.get(name), "theta." + name)
    sigma = fit.get("sigma_JtJ")
    if not isinstance(sigma, dict):
        raise ValueError("fit uncertainty mapping is missing")
    for name, value in sigma.items():
        finite_number(value, "sigma_JtJ." + str(name), positive=True)
    return fit

def nested_deltas(lcdm, fixed, free):
    # No objective-error bound is supplied by the legacy solver.
    # Optimizer stopping thresholds do not supply a clipping tolerance.
    fixed_delta = fixed["chi2"] - free["chi2"]
    lcdm_delta = lcdm["chi2"] - free["chi2"]
    finite_number(fixed_delta, "fixed minus free", nonnegative=True)
    finite_number(lcdm_delta, "LCDM minus free", nonnegative=True)
    return fixed_delta, lcdm_delta
