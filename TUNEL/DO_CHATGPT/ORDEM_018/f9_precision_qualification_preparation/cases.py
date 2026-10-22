"""Q01 finite independent references and behavior checks; not run at preparation."""
import math
import sys
import time

CASE_IDS = ("W01", "W02", "W03", "W04", "W05", "P01", "P02", "N01", "N02")


class CheckFailure(ValueError):
    pass


class CallbackSentinel(Exception):
    pass


def need(condition, detail):
    if not condition:
        raise CheckFailure(detail)


def tick(deadline):
    if time.monotonic() >= deadline:
        raise CheckFailure("COOPERATIVE_DEADLINE")


def value(spec):
    if type(spec) is dict:
        need(set(spec) == {"power_of_two", "sign"}, "invalid exact input descriptor")
        need(type(spec["power_of_two"]) is int and spec["sign"] in (-1, 1), "invalid power")
        return math.ldexp(float(spec["sign"]), spec["power_of_two"])
    need(type(spec) in (int, float) and math.isfinite(spec), "invalid numerical input")
    return float(spec)


def window_reference(name):
    # Explicit erf/erfc arguments, with representable tails only; no adaptive rule or candidate helper.
    if name in ("symmetric_unit_gaussian",
                "scaled_unit_gaussian_minus500", "scaled_unit_gaussian_plus500"):
        base = 0.5 * math.log(math.pi) + math.log(math.erf(1.0))
        shift = {"symmetric_unit_gaussian": 0,
                 "scaled_unit_gaussian_minus500": -500,
                 "scaled_unit_gaussian_plus500": 500}[name]
        ref = math.fsum((base, shift * math.log(2.0)))
        return {"reference_log": ref, "analytic_approximation_bound": 0.0,
                "formula": "shift*ln(2)+ln(sqrt(pi)*erf(1))",
                "reference_rounding": "stdlib float, not an interval certificate"}
    if name == "boundary_erfc_difference":
        difference = math.erfc(1.0) - math.erfc(17.0)
        need(difference > 0, "reference erfc difference")
        ref = math.fsum((1.0, 0.5 * math.log(math.pi), -math.log(2.0),
                         math.log(difference)))
        return {"reference_log": ref, "analytic_approximation_bound": 0.0,
                "formula": "1+ln(sqrt(pi)/2)+ln(erfc(1)-erfc(17))",
                "reference_rounding": "moderate erfc arguments; stdlib float"}
    if name == "short_window_inequality":
        # For d=2^-40, exp(-d^2) <= average exp(-z^2) <= 1.
        # Hence ln(d)-d^2 <= ln(W) <= ln(d); no CDF subtraction.
        return {"reference_log": -40.0 * math.log(2.0),
                "analytic_approximation_bound": math.ldexp(1.0, -80),
                "formula": "ln(d)-d^2 <= ln(W) <= ln(d), d=2^-40",
                "reference_rounding": "log reference float; comparison allowance explicit"}
    raise CheckFailure("unknown reference")


def check_receipt(record, field, service_id, count, cap):
    need(type(record) is dict and set(record) == {
        "service_id", "status", field, "error_estimate", "error_kind",
        "converged", "evaluations", "method"}, "receipt shape")
    need(record["service_id"] == service_id and record["status"] == "ENGINEERING_ESTIMATE",
         "receipt identity")
    need(type(record[field]) in (int, float) and math.isfinite(record[field]), "receipt value")
    need(type(record["evaluations"]) is int and record["evaluations"] == count <= cap,
         "reported count differs from observed calls or cap")
    need(type(record["converged"]) is bool and type(record["method"]) is str
         and bool(record["method"]), "receipt diagnostics")
    need(record["error_kind"] == "ESTIMATED_NOT_CERTIFIED"
         and type(record["error_estimate"]) in (int, float)
         and math.isfinite(record["error_estimate"]) and record["error_estimate"] >= 0,
         "finite local estimate required by these qualification cases")


def run_case(candidate, case, source_filename, deadline):
    """One service invocation only; no retries or fallback, even on a failed check."""
    tick(deadline)
    cid, kind = case["id"], case["kind"]
    need(cid in CASE_IDS, "unknown case")
    observed = {"calls": 0, "duplicate_nodes": 0}
    seen = set()
    cap = case["max_evaluations"]
    diagnostics = {"case_id": cid, "kind": kind, "observed": observed,
                   "service_invocations": 0}
    try:
        if kind == "window":
            reference = window_reference(case["reference"])
            diagnostics["reference"] = reference
            args = [value(x) for x in case["input"]]
            need(sys.getprofile() is None, "unexpected profiler")
            def profile(frame, event, arg):
                if (event == "call" and frame.f_code.co_filename == source_filename
                        and frame.f_code.co_name == "integrand"):
                    observed["calls"] += 1
                    need(observed["calls"] <= cap, "observed window cap")
                    tick(deadline)
            sys.setprofile(profile)
            try:
                diagnostics["service_invocations"] = 1
                result = candidate.log_exp_quad_interval(
                    *args, absolute_log_error_target=case["log_target"],
                    max_evaluations=cap)
            finally:
                sys.setprofile(None)
            diagnostics["receipt"] = result
            check_receipt(result, "log_value", candidate.LOG_SERVICE_ID,
                          observed["calls"], cap)
            if case["expected_evaluations"] is not None:
                need(observed["calls"] == case["expected_evaluations"], "exact window count")
            need(result["converged"] is case["require_converged"], "window convergence")
            difference = abs(result["log_value"] - reference["reference_log"])
            tolerance = (case["comparison_absolute_tolerance"]
                         + reference["analytic_approximation_bound"])
            diagnostics.update(absolute_log_difference=difference,
                               accepted_absolute_difference=tolerance)
            need(difference <= tolerance, "independent log reference disagreement")
        else:
            sentinel = CallbackSentinel("Q01 fixed callback sentinel")
            def callback(u):
                tick(deadline)
                need(type(u) in (int, float) and math.isfinite(u) and 0 <= u <= 1,
                     "callback coordinate")
                observed["calls"] += 1
                need(observed["calls"] <= cap, "observed positive callback cap")
                if u in seen:
                    observed["duplicate_nodes"] += 1
                seen.add(u)
                if kind == "callback_exception" and observed["calls"] == case["raise_on_call"]:
                    raise sentinel
                return math.exp(u) if kind == "positive_exp_nonconverged" else 1.0 + u*u*u
            result, captured = None, None
            diagnostics["service_invocations"] = 1
            try:
                result = candidate.positive_quad_1d(
                    callback, 0.0, 1.0, absolute_error_target=case["absolute_target"],
                    relative_error_target=case["relative_target"], max_evaluations=cap)
            except Exception as exc:
                captured = exc
            tick(deadline)
            need(observed["calls"] == case["expected_evaluations"], "exact callback count")
            need(observed["duplicate_nodes"] == 0, "duplicate callback invocation")
            if kind == "insufficient_budget":
                need(isinstance(captured, candidate.PrecisionServiceError)
                     and captured.code == case["expected_exception_code"], "budget refusal")
                need(result is None and observed["calls"] == 0, "callback before refusal")
                diagnostics["expected_exception"] = {"type": type(captured).__name__,
                                                     "code": captured.code}
            elif kind == "callback_exception":
                need(captured is sentinel and result is None, "callback exception replaced or swallowed")
                diagnostics["expected_exception"] = {"same_object": True, "type": type(sentinel).__name__}
            else:
                if captured is not None:
                    raise captured
                diagnostics["receipt"] = result
                check_receipt(result, "value", candidate.QUAD_SERVICE_ID, observed["calls"], cap)
                need(result["converged"] is case["require_converged"], "quadrature convergence")
                if kind == "positive_cubic":
                    reference, tolerance = 1.25, case["comparison_absolute_tolerance"]
                    formula = "integral_0^1 (1+u^3)du = 5/4"
                elif kind == "positive_exp_nonconverged":
                    reference = math.expm1(1.0)
                    # Composite Simpson on 16 equal elementary intervals:
                    # absolute remainder <= sup exp(u) /(180*16^4).
                    tolerance = math.e / (180 * 16**4) + case["comparison_rounding_allowance"]
                    formula = "expm1(1); classical Simpson error <= e/(180*16^4)"
                else:
                    raise CheckFailure("unknown positive case")
                difference = abs(result["value"] - reference)
                diagnostics.update(reference_value=reference, reference_formula=formula,
                                   absolute_difference=difference,
                                   accepted_absolute_difference=tolerance)
                need(difference <= tolerance, "independent positive reference disagreement")
        tick(deadline)
        diagnostics["status"] = "PASS"
        return diagnostics
    except BaseException as exc:
        diagnostics.update(status="FAIL", exception_type=type(exc).__name__,
                           exception_code=getattr(exc, "code", None), detail=str(exc)[:2000])
        # An unexpected failure is a terminal case result; caller must stop the unit.
        return diagnostics
