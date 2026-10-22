"""Prepared synthetic controls only. Not executed during preparation."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE))
import argparse
import copy
import hashlib
import json
import math
import os
import time
from fractions import Fraction
import tail_envelope as te

DEADLINE = None
VERIFIER_REFERENCE = None
ALGORITHM_CONTRACT_REFERENCE = None
AUDIT_DENIED = []


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def budget():
    if AUDIT_DENIED:
        raise RuntimeError("AUDIT_DENIAL_LATCHED")
    if time.monotonic() >= DEADLINE:
        raise RuntimeError("WORKER_COOPERATIVE_23S_DEADLINE")


def ref(label):
    return hashlib.sha256(("SYNTHETIC_ONLY:" + label).encode("ascii")).hexdigest()


def domain(scenarios=("a",)):
    return te.Domain("COMPAT_H1", "H1_TGL", scenarios,
                     ref("family:" + ",".join(scenarios)), ref("model"), ALGORITHM_CONTRACT_REFERENCE)


def request(d, x, scenario="a", dom=None, source_kind="GLOBAL_LOWER_SYNTHETIC"):
    dom = dom or domain()
    if type(x) is Fraction:
        encoded = {"numerator": str(x.numerator), "denominator": str(x.denominator)}
    else:
        encoded = {"numerator": str(x), "denominator": "1"}
    identity = {
        "test_id": dom.test_id, "null_model_id": dom.null_model_id,
        "scenario_id": scenario, "frozen_scenario_family_sha256": dom.family_sha256,
        "model_contract_sha256": dom.model_sha256,
        "algorithm_contract_sha256": dom.algorithm_sha256,
        "lower_statistic_certificate_sha256": ref(source_kind + ":" + json.dumps(encoded, sort_keys=True)),
        "support_certificate_sha256": ref("synthetic-support"),
        "domination_certificate_sha256": ref("synthetic-domination"),
        "degree_certificate_sha256": ref("synthetic-degree:" + str(d)),
    }
    return {"identity": identity, "d": d, "x_lower": encoded}


class FixtureVerifier:
    """Exact fixture registry, not a verifier of physical F9 certificates."""
    def __init__(self):
        self.entries = {}

    def admit(self, payload, role, source_kind="GLOBAL_LOWER_SYNTHETIC"):
        if source_kind not in {"GLOBAL_LOWER_SYNTHETIC", "EXACT_SYNTHETIC_BOUND"}:
            return
        refs = tuple(payload["identity"][k] for k in te.HASH_KEYS)
        if role == "BOUND_RECORD":
            refs += (payload["bound_certificate_sha256"],)
        self.entries[(te.digest(payload), role)] = refs

    def __call__(self, payload, role):
        key = (te.digest(payload), role)
        if key not in self.entries:
            return None
        return te.VerificationReceipt(key[0], role, "SYNTHETIC_CONTROL_ONLY",
                                      self.entries[key], VERIFIER_REFERENCE)


def evaluate(d, x, *, dom=None, scenario="a", clock=time.monotonic,
             deadline=None, source_kind="GLOBAL_LOWER_SYNTHETIC"):
    dom = dom or domain()
    payload = request(d, x, scenario, dom, source_kind)
    verifier = FixtureVerifier()
    verifier.admit(payload, "STATISTIC_SEMANTICS", source_kind)
    budget()
    result = te.tail_upper(payload, dom, verifier,
                           DEADLINE if deadline is None else deadline, clock)
    budget()
    return result


def p_value(result):
    value = result["p_upper"]
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def exact_certificate(result, d, x):
    require(result["status"] == "VALID_CERTIFIED_ENVELOPE", "expected completed envelope")
    certificate = result["certificate"]
    for key in ("R_numerator_hex", "R_denominator_hex"):
        value = certificate[key]
        require(type(value) is str and 1 <= len(value) <= (te.MAX_SCRATCH_BITS + 3) // 4,
                "bounded hex certificate")
        require(value[0] != "0" and all(c in "0123456789abcdef" for c in value),
                "canonical positive hex")
    a = int(certificate["R_numerator_hex"], 16)
    b = int(certificate["R_denominator_hex"], 16)
    u = int(certificate["root_index"])
    require(a.bit_length() <= te.MAX_SCRATCH_BITS and b.bit_length() <= te.MAX_SCRATCH_BITS,
            "certificate bit bounds")
    require(0 < a <= b and 1 <= u <= te.Q, "positive unit bound")
    require((u - 1) ** 2 * b < a * te.Q ** 2 <= u ** 2 * b, "integer root certificate")
    x = Fraction(x)
    # Independent algebraic expression, solely on fixed synthetic values.
    expected_R = (x / d) ** d / (1 + (x - d) / 512) ** 512
    require(Fraction(a, b) == expected_R, "exact R reconstruction")
    require(p_value(result) == Fraction(u, te.Q), "root and returned fraction agree")
    return {"status": result["status"], "certificate_sha256": te.digest(certificate),
            "p_upper": result["p_upper"]}


def T01_ATOM():
    values = [evaluate(0, x) for x in (-1, 0, 1)]
    require([v["status"] for v in values] == ["VALID_ATOM_TAIL", "VALID_ATOM_TAIL", "INVALID"],
            "F9 atom statuses")
    require(p_value(values[0]) == 1 and p_value(values[1]) == 1, "nonpositive atom upper")
    require(values[2]["p_upper"] is None and
            values[2]["reason"] == "CONTRACT_INCOHERENCE_NOT_REJECTION",
            "positive lower at zero degree must never reject")
    return {"F9_statuses": [v["status"] for v in values], "positive_p": None,
            "abstract_tail_not_used_as_API_output": True}


def T02_THRESHOLD_AND_DOMAIN():
    values = [evaluate(17, x) for x in (16, 17, 18)]
    require(p_value(values[0]) == 1 and p_value(values[1]) == 1, "threshold bounds")
    exact_certificate(values[2], 17, 18)
    for d in (-1, 149, True):
        require(evaluate(d, 18)["status"] == "UNAVAILABLE", "invalid degree")
    require(evaluate(17, 18.5)["status"] == "UNAVAILABLE", "uncertified float")
    return {"threshold_cases": 3, "invalid_degree_or_float_cases": 4}


def T03_EVEN():
    result = evaluate(2, 4)
    summary = exact_certificate(result, 2, 4)
    exact_B = 2 * Fraction(256, 257) ** 256
    scaled = exact_B * te.Q
    ceiling = (scaled.numerator + scaled.denominator - 1) // scaled.denominator
    require(p_value(result) == Fraction(ceiling, te.Q), "independent even-degree ceiling")
    return summary


def T04_ODD():
    result = evaluate(3, 6)
    summary = exact_certificate(result, 3, 6)
    a = int(result["certificate"]["R_numerator_hex"], 16)
    b = int(result["certificate"]["R_denominator_hex"], 16)
    require(Fraction(a, b) == 8 * Fraction(512, 515) ** 512, "odd rational R")
    return summary


def T05_MONOTONE_D148():
    values = [evaluate(148, x) for x in (148, 296, 592)]
    exact_certificate(values[1], 148, 296)
    exact_certificate(values[2], 148, 592)
    require(Fraction(1, te.Q) <= p_value(values[2]) <= p_value(values[1]) <= p_value(values[0]) == 1,
            "completed branch monotone on fixed inputs")
    return {"p_upper": [v["p_upper"] for v in values], "scope": "three fixed inputs only"}


def T06_NO_FALSE_UNDERFLOW():
    x = 10 ** 100
    result = evaluate(148, x)
    summary = exact_certificate(result, 148, x)
    require(p_value(result) == Fraction(1, te.Q), "positive grid floor, never numerical zero")
    return summary


def T07_LOWER_ENDPOINT():
    left = evaluate(148, 150)
    right = evaluate(148, 160)
    require(p_value(left) >= p_value(right), "lower endpoint direction")
    require(p_value(evaluate(148, 147)) == 1, "interval lower endpoint below mean")
    bad = evaluate(148, 150, source_kind="LOCAL_FEASIBLE_UPPER_ONLY")
    require(bad["status"] == "UNAVAILABLE" and bad["p_upper"] is None,
            "feasible upper is not lower certificate")
    dom = domain()
    lower = request(148, 150, dom=dom)
    verifier = FixtureVerifier()
    verifier.admit(lower, "STATISTIC_SEMANTICS")
    tampered = copy.deepcopy(lower)
    tampered["x_lower"]["numerator"] = "160"
    require(te.tail_upper(tampered, dom, verifier, DEADLINE)["status"] == "UNAVAILABLE",
            "endpoint mutation invalidates registered lower certificate")
    return {"lower_endpoint_preserved": True, "local_upper_rejected": True,
            "mutated_endpoint_rejected": True}


def bound_records():
    dom = domain(("a", "b", "c"))
    verifier = FixtureVerifier()
    records = []
    for scenario, denominator in zip(dom.scenarios, (1000, 500, 4000)):
        row = {
            "identity": request(17, 18, scenario, dom)["identity"],
            "status": "VALID_CERTIFIED_ENVELOPE",
            "p_upper": {"numerator": "1", "denominator": str(denominator)},
            "bound_certificate_sha256": ref("synthetic-certified-bound:" + scenario),
        }
        # These are synthetic probability upper-bound fixtures, not evaluated tails.
        verifier.admit(row, "BOUND_RECORD", "EXACT_SYNTHETIC_BOUND")
        records.append(row)
    return dom, verifier, records


def T08_AGGREGATION_AND_FAILURE():
    dom, verifier, rows = bound_records()
    full = te.aggregate_bounds(rows, dom, verifier)
    require(full["status"] == "COMPLETE_CONDITIONAL_BOUND", "complete family")
    require(full["p_robust"] == {"numerator": "1", "denominator": "500"}, "max all")
    require(full["p_FWER_upper"] == {"numerator": "1", "denominator": "100"}, "Bonferroni5")
    require(te.aggregate_bounds(rows[:2], dom, verifier)["status"] == "UNAVAILABLE",
            "missing scenario unavailable")
    trivial = copy.deepcopy(rows)
    trivial[2]["status"] = "VALID_TRIVIAL_BOUND_RESOURCE_LIMIT"
    trivial[2]["p_upper"] = {"numerator": "1", "denominator": "1"}
    trivial[2]["bound_certificate_sha256"] = ref("synthetic-trivial-after-validation")
    verifier.admit(trivial[2], "BOUND_RECORD", "EXACT_SYNTHETIC_BOUND")
    require(te.aggregate_bounds(trivial, dom, verifier)["p_FWER_upper"] ==
            {"numerator": "1", "denominator": "1"}, "explicit resource trivial is visible")
    invalid = copy.deepcopy(rows)
    invalid[2]["status"] = "INVALID"
    invalid[2]["p_upper"] = None
    require(te.aggregate_bounds(invalid, dom, verifier)["p_FWER_upper"] is None,
            "invalid model not converted to1")
    return {"complete": full, "missing_and_invalid_unavailable": True}


def N01_IDENTITY_AND_BINDING():
    dom = domain()
    good = request(17, 18, dom=dom)
    verifier = FixtureVerifier()
    verifier.admit(good, "STATISTIC_SEMANTICS")
    count = 0
    for key, value in (("algorithm_contract_sha256", ref("wrong-algorithm")),
                       ("model_contract_sha256", ref("wrong-model")),
                       ("frozen_scenario_family_sha256", ref("wrong-family")),
                       ("scenario_id", "other"),
                       ("support_certificate_sha256", ref("unregistered-support"))):
        bad = copy.deepcopy(good)
        bad["identity"][key] = value
        require(te.tail_upper(bad, dom, verifier, DEADLINE)["status"] == "UNAVAILABLE",
                "identity or payload binding failure")
        count += 1
    return {"negative_inputs": count}


def N02_CERTIFICATION_NOT_FLAGS():
    dom = domain()
    good = request(17, 18, dom=dom)
    for verifier in (None, lambda payload, role: True,
                     lambda payload, role: {"valid": True},
                     lambda payload, role: te.VerificationReceipt(
                         ref("different-payload"), role, "SYNTHETIC_CONTROL_ONLY",
                         tuple(good["identity"][k] for k in te.HASH_KEYS), VERIFIER_REFERENCE)):
        result = te.tail_upper(good, dom, verifier, DEADLINE)
        require(result["p_upper"] is None, "no flags, missing or mismatched receipt")
    return {"negative_verifiers": 4, "physical_certificates_created": 0}


def N03_CANONICAL_AND_SIZE():
    dom = domain()
    bad_values = [
        {"numerator": "+1", "denominator": "1"},
        {"numerator": "-0", "denominator": "1"},
        {"numerator": "01", "denominator": "1"},
        {"numerator": "2", "denominator": "2"},
        {"numerator": "0", "denominator": "2"},
        {"numerator": "1", "denominator": "0"},
        {"numerator": "1", "denominator": "-1"},
        {"numerator": True, "denominator": "1"},
        {"numerator": "1.0", "denominator": "1"},
        {"numerator": "9" * 156, "denominator": "1"},
        {"numerator": str(1 << 512), "denominator": "1"},
    ]
    calls = []
    def forbidden_verifier(payload, role):
        calls.append("unexpected")
        raise AssertionError("invalid encoding reached verifier")
    for rational in bad_values:
        bad = request(17, 18, dom=dom)
        bad["x_lower"] = rational
        require(te.tail_upper(bad, dom, forbidden_verifier, DEADLINE)["status"] == "UNAVAILABLE",
                "noncanonical or oversized rational")
    require(not calls, "guard before expensive parsing and verifier")
    return {"negative_encodings": len(bad_values), "verifier_calls": 0}


def N04_RESOURCE_AFTER_SEMANTICS():
    # An already expired synthetic clock triggers the declared branch after semantics.
    result = evaluate(17, 18, clock=lambda: 2.0, deadline=1.0)
    require(result["status"] == "VALID_TRIVIAL_BOUND_RESOURCE_LIMIT" and p_value(result) == 1,
            "declared resource bound")
    dom = domain()
    good = request(17, 18, dom=dom)
    unverified = te.tail_upper(good, dom, None, 1.0, lambda: 2.0)
    require(unverified["status"] == "UNAVAILABLE" and unverified["p_upper"] is None,
            "resource cannot hide missing semantics")
    calls = []
    def forbidden_clock():
        calls.append("called")
        raise AssertionError("d0 guard must precede budget")
    invalid_atom = evaluate(0, 1, clock=forbidden_clock, deadline=1.0)
    require(invalid_atom["status"] == "INVALID" and not calls, "d0 before any fallback")
    return {"resource_upper": result["p_upper"], "missing_semantics_not_hidden": True,
            "positive_d0_clock_calls": 0}


def N05_SCRATCH_PREFLIGHT():
    small_clock = lambda: 0.0
    arithmetic = te.Budget(1.0, small_clock)
    left = 1 << (te.MAX_SCRATCH_BITS - 1)
    try:
        arithmetic.multiply(left, 2)
    except te.ResourceLimit as error:
        require(str(error) == "PREDICTED_PRODUCT_524288_BITS", "pre-product size reason")
    else:
        raise AssertionError("oversized product not blocked")
    return {"scratch_cap": te.MAX_SCRATCH_BITS, "blocked_before_product": True}


def N06_FAMILY_DUPLICATES_AND_TAMPERING():
    dom, verifier, rows = bound_records()
    duplicate = [rows[0], rows[0], rows[2]]
    require(te.aggregate_bounds(duplicate, dom, verifier)["status"] == "UNAVAILABLE",
            "duplicate scenario never hides missing")
    extra = rows + [rows[0]]
    require(te.aggregate_bounds(extra, dom, verifier)["status"] == "UNAVAILABLE", "extra scenario")
    tampered = copy.deepcopy(rows)
    tampered[0]["p_upper"] = {"numerator": "1", "denominator": "100000"}
    require(te.aggregate_bounds(tampered, dom, verifier)["status"] == "UNAVAILABLE",
            "unverified bound mutation rejected")
    zero = copy.deepcopy(rows)
    zero[0]["p_upper"] = {"numerator": "0", "denominator": "1"}
    verifier.admit(zero[0], "BOUND_RECORD", "EXACT_SYNTHETIC_BOUND")
    require(te.aggregate_bounds(zero, dom, verifier)["status"] == "UNAVAILABLE",
            "no numeric zero F9 bound")
    bad_family = te.Domain(dom.test_id, dom.null_model_id, ("a", "a", "c"),
                           dom.family_sha256, dom.model_sha256, dom.algorithm_sha256)
    require(te.aggregate_bounds(rows, bad_family, verifier)["status"] == "UNAVAILABLE",
            "duplicate frozen labels")
    return {"negative_family_or_record_inputs": 5}


def N07_ROOT_CERTIFICATE_BOUNDARIES():
    arithmetic = te.Budget(DEADLINE)
    u, certificate = te.ceil_root_certificate(1, 4, arithmetic)
    require(u == te.Q // 2, "perfect square uses exact root without increment")
    u2, certificate2 = te.ceil_root_certificate(1, te.Q * te.Q, arithmetic)
    require(u2 == 1, "exact positive grid boundary")
    u3, certificate3 = te.ceil_root_certificate(1, 3, arithmetic)
    require((u3 - 1) ** 2 * 3 < te.Q ** 2 <= u3 ** 2 * 3, "non-square rounds upward")
    for a, b in ((0, 1), (-1, 1), (1, 0), (2, 1)):
        try:
            te.ceil_root_certificate(a, b, arithmetic)
        except te.InvalidCertificate:
            pass
        else:
            raise AssertionError("invalid root domain not rejected")
    return {"perfect_square": True, "grid_boundary": True, "non_square_upper": True,
            "invalid_domains": 4}


PRIMARY = (T01_ATOM, T02_THRESHOLD_AND_DOMAIN, T03_EVEN, T04_ODD,
           T05_MONOTONE_D148, T06_NO_FALSE_UNDERFLOW, T07_LOWER_ENDPOINT,
           T08_AGGREGATION_AND_FAILURE)
NEGATIVE = (N01_IDENTITY_AND_BINDING, N02_CERTIFICATION_NOT_FLAGS,
            N03_CANONICAL_AND_SIZE, N04_RESOURCE_AFTER_SEMANTICS,
            N05_SCRATCH_PREFLIGHT, N06_FAMILY_DUPLICATES_AND_TAMPERING,
            N07_ROOT_CERTIFICATE_BOUNDARIES)


def install_audit():
    def hook(event, args):
        if (event == "open" or event.startswith(("socket.", "subprocess.", "ctypes.")) or
                event in {"os.system", "os.spawn", "os.exec", "os.fork", "os.remove",
                          "os.rename", "os.mkdir", "sys.addaudithook"} or
                (event == "import" and args[0] not in sys.modules)):
            AUDIT_DENIED.append(event)
            raise RuntimeError("SYNTHETIC_WORKER_FORBIDDEN_EVENT:" + event)
    sys.addaudithook(hook)


def main():
    global DEADLINE, VERIFIER_REFERENCE, ALGORITHM_CONTRACT_REFERENCE
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--claim-token", required=True)
    parser.add_argument("--deadline-monotonic", required=True, type=float)
    args = parser.parse_args()
    identity = json.loads((PACKAGE / "IDENTITY.json").read_bytes())
    claim = json.loads((PACKAGE / "CLAIM.json").read_bytes())
    authorization_bytes = (PACKAGE / "AUTORIZACAO_ROOT.json").read_bytes()
    contract_bytes = (PACKAGE / "CONTROL_CONTRACT.json").read_bytes()
    require(args.request_id == identity["request_id"] == claim["request_id"], "request identity")
    require(args.claim_token == claim["claim_token"], "claim token")
    require(claim["authorization_sha256"] == hashlib.sha256(authorization_bytes).hexdigest(),
            "authorization pin")
    require(claim["contract_sha256"] == hashlib.sha256(contract_bytes).hexdigest(), "contract pin")
    require(claim["supervisor_pid"] == os.getppid(), "official supervisor parent")
    authorization = json.loads(authorization_bytes)
    require(authorization["authorized"] is True and authorization["request_id"] == args.request_id,
            "explicit authorization")
    DEADLINE = args.deadline_monotonic
    require(math.isfinite(DEADLINE) and 0 < DEADLINE - time.monotonic() <= 23.0,
            "single cooperative deadline")
    VERIFIER_REFERENCE = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    ALGORITHM_CONTRACT_REFERENCE = hashlib.sha256(contract_bytes).hexdigest()
    started = time.monotonic()
    install_audit()
    results = []
    status = "FAILED"
    error = None
    try:
        for function in PRIMARY + NEGATIVE:
            budget()
            value = function()
            budget()
            results.append({"id": function.__name__, "status": "PASS", "result": value})
        require(not AUDIT_DENIED, "audit latch clear")
        status = "PASS"
    except Exception as exc:
        error = {"type": type(exc).__name__, "message": str(exc)[:2000]}
    output = {
        "request_id": args.request_id, "status": status, "worker_pid": os.getpid(),
        "supervisor_pid": os.getppid(), "results": results,
        "primary_count_expected": 8, "negative_group_count_expected": 7,
        "error": error, "audit_denied": AUDIT_DENIED,
        "wall_s": time.monotonic() - started, "synthetic_only": True,
        "physical_certification": False, "observed_data": False,
        "remote_calls": 0, "MC": 0, "CAMB": 0,
    }
    print(json.dumps(output, ensure_ascii=True, separators=(",", ":")))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
