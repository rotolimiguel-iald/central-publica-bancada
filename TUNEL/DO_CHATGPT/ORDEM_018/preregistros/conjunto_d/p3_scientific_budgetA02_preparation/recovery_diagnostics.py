"""Proposed weak, realization-specific summaries; never a science PASS."""
import math


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def numerical_criteria(result, *, max_calls, dlogz=0.1, ess_min=100):
    delta = result.get("delta_logz_before_live_addition")
    ess = result.get("weighted_ESS")
    span = result.get("live_logl_span_before_addition")
    calls = result.get("likelihood_calls")
    return (finite_number(delta) and 0 <= delta < dlogz
            and finite_number(ess) and ess >= ess_min
            and finite_number(span) and span > 0
            and result.get("final_live_points_added") is True
            and type(calls) is int and 0 < calls < max_calls
            and result.get("error") is None)


def summarize(values, weights, truth, *, numerical_eligible):
    if type(numerical_eligible) is not bool:
        raise TypeError("Explicit numerical eligibility required")
    if (not isinstance(values, (list, tuple)) or not isinstance(weights, (list, tuple))
            or not values or len(values) != len(weights)):
        raise ValueError("Equal nonempty value/weight vectors required")
    if not finite_number(truth) or not -0.8 <= truth <= 2.0:
        raise ValueError("Truth outside frozen synthetic prior")
    if any(not finite_number(x) or not -0.8 <= x <= 2.0 for x in values):
        raise ValueError("Nonfinite/out-of-prior posterior value")
    if any(not finite_number(x) or x < 0 for x in weights):
        raise ValueError("Nonnegative finite weights required")
    total = math.fsum(weights)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("Positive finite total weight required")
    pairs = sorted((float(x), float(weight / total))
                   for x, weight in zip(values, weights) if weight > 0)
    norm = math.fsum(weight for _, weight in pairs)
    pairs = [(x, weight / norm) for x, weight in pairs]
    # Discrete inverse CDF, no interpolation or random resampling.
    def quantile(p):
        running = 0.0
        correction = 0.0
        for x, weight in pairs:
            add = weight - correction
            updated = running + add
            correction = (updated - running) - add
            running = updated
            if running >= p:
                return x
        return pairs[-1][0]
    q05, q50, q95 = (quantile(p) for p in (0.05, 0.5, 0.95))
    width = q95 - q05
    favorable = q05 <= truth <= q95 and width < 2.52
    return {
        "schema": "P3_WEAK_RECOVERY_DIAGNOSTIC_V1",
        "q05": q05, "q50": q50, "q95": q95,
        "q95_minus_q05": width, "q50_minus_truth": q50 - truth,
        "F_w_truth": math.fsum(weight for x, weight in pairs if x <= truth),
        "mass_lower_prior_edge": math.fsum(weight for x, weight in pairs if -0.8 <= x <= -0.66),
        "mass_upper_prior_edge": math.fsum(weight for x, weight in pairs if 1.86 <= x <= 2.0),
        "W90_divided_by_2p52": width / 2.52,
        "weighted_ESS_from_summary": 1 / math.fsum(weight * weight for _, weight in pairs),
        "numerical_eligible": numerical_eligible,
        "proposed_favorable_condition": favorable if numerical_eligible else None,
        "interpretation": ("WEAK_COMPATIBILITY_AND_CONTRACTION_REQUIRES_INDEPENDENT_REVIEW"
                           if numerical_eligible and favorable else
                           "RECOVERY_NOT_ESTABLISHED_FOR_THIS_REALIZATION"
                           if numerical_eligible else "NUMERICALLY_INCOMPLETE_DESCRIPTIVE_ONLY"),
        "independent_interpretation_required": True,
        "scientific_qualification": False, "coverage_claim": False, "D_ready": False,
    }
