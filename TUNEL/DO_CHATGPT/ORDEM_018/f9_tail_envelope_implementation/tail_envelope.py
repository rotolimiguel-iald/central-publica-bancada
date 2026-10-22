"""Conditional rational tail bounds. No I/O, models, data access or physical certificates.

The mandatory verifier is a trust boundary, not a proof engine. This package's
controls provide only an exact synthetic-fixture verifier. No physical F9
certificate is created, inferred from flags or shipped by this module.
"""
from dataclasses import dataclass
import hashlib
import json
import math
import time

N = 256
Q = 10 ** 30
MAX_INPUT_BITS = 512
MAX_SCRATCH_BITS = 524288
MAX_DECIMAL = str((1 << MAX_INPUT_BITS) - 1)
MAX_SCENARIOS = 4096
VALID_STATUSES = frozenset({
    "VALID_CERTIFIED_ENVELOPE", "VALID_ATOM_TAIL",
    "VALID_TRIVIAL_BOUND_MATHEMATICAL", "VALID_TRIVIAL_BOUND_RESOURCE_LIMIT",
})
TEST_IDS = frozenset({
    "COMPAT_H1", "LAW_H1_VS_FREE", "H2_TO_H1", "H4_TO_H1", "H5_TO_H1",
})
HASH_KEYS = (
    "frozen_scenario_family_sha256", "model_contract_sha256",
    "lower_statistic_certificate_sha256", "support_certificate_sha256",
    "domination_certificate_sha256", "degree_certificate_sha256",
    "algorithm_contract_sha256",
)
ID_KEYS = ("test_id", "null_model_id", "scenario_id") + HASH_KEYS


@dataclass(frozen=True)
class Domain:
    test_id: str
    null_model_id: str
    scenarios: tuple
    family_sha256: str
    model_sha256: str
    algorithm_sha256: str


@dataclass(frozen=True)
class VerificationReceipt:
    payload_sha256: str
    role: str
    scope: str
    evidence_references: tuple
    verifier_reference_sha256: str


class InvalidInput(Exception):
    pass


class ResourceLimit(Exception):
    pass


class InvalidCertificate(Exception):
    pass


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _hash(value):
    return (type(value) is str and len(value) == 64 and
            all(c in "0123456789abcdef" for c in value))


def _label(value):
    return (type(value) is str and 1 <= len(value) <= 64 and
            all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for c in value))


def _domain(domain):
    if type(domain) is not Domain:
        raise InvalidInput("DOMAIN_TYPE")
    if domain.test_id not in TEST_IDS or not _label(domain.null_model_id):
        raise InvalidInput("DOMAIN_TEST_OR_NULL")
    if (type(domain.scenarios) is not tuple or
            not 1 <= len(domain.scenarios) <= MAX_SCENARIOS or
            any(not _label(x) for x in domain.scenarios) or
            len(set(domain.scenarios)) != len(domain.scenarios)):
        raise InvalidInput("FAMILY_MALFORMED_OR_DUPLICATED")
    if not all(_hash(x) for x in (
            domain.family_sha256, domain.model_sha256, domain.algorithm_sha256)):
        raise InvalidInput("DOMAIN_PINS")


def _integer_text(value, signed):
    # Type, length, grammar and the exact 512-bit lexical ceiling precede int().
    if type(value) is not str or not 1 <= len(value) <= len(MAX_DECIMAL) + int(signed):
        raise InvalidInput("INTEGER_TEXT_TYPE_OR_LENGTH")
    negative = value.startswith("-")
    if negative and not signed:
        raise InvalidInput("NEGATIVE_DENOMINATOR")
    digits = value[1:] if negative else value
    if (not digits or any(c not in "0123456789" for c in digits) or
            (len(digits) > 1 and digits[0] == "0") or
            (negative and digits == "0")):
        raise InvalidInput("NONCANONICAL_INTEGER")
    if len(digits) > len(MAX_DECIMAL) or (
            len(digits) == len(MAX_DECIMAL) and digits > MAX_DECIMAL):
        raise InvalidInput("INPUT_EXCEEDS_512_BITS")
    return int(value)


def _rational(value):
    if type(value) is not dict or set(value) != {"numerator", "denominator"}:
        raise InvalidInput("RATIONAL_SCHEMA")
    a = _integer_text(value["numerator"], True)
    b = _integer_text(value["denominator"], False)
    if b <= 0 or math.gcd(abs(a), b) != 1:
        raise InvalidInput("RATIONAL_NOT_REDUCED_OR_NONPOSITIVE_DENOMINATOR")
    return a, b


def _encoded(a, b):
    g = math.gcd(abs(a), b)
    return {"numerator": str(a // g), "denominator": str(b // g)}


def _identity(value, domain):
    if type(value) is not dict or set(value) != set(ID_KEYS):
        raise InvalidInput("IDENTITY_SCHEMA")
    if any(not _label(value[k]) for k in ID_KEYS[:3]):
        raise InvalidInput("IDENTITY_LABEL")
    if any(not _hash(value[k]) for k in HASH_KEYS):
        raise InvalidInput("IDENTITY_REFERENCE")
    if (value["test_id"] != domain.test_id or
            value["null_model_id"] != domain.null_model_id or
            value["scenario_id"] not in domain.scenarios or
            value["frozen_scenario_family_sha256"] != domain.family_sha256 or
            value["model_contract_sha256"] != domain.model_sha256 or
            value["algorithm_contract_sha256"] != domain.algorithm_sha256):
        raise InvalidInput("IDENTITY_MISMATCH")


def _semantic(payload, role, references, verifier):
    if not callable(verifier):
        raise InvalidInput("EXPLICIT_VERIFIER_REQUIRED")
    # The verifier receives a detached primitive payload, not live caller state.
    serialized = canonical_bytes(payload)
    result = verifier(json.loads(serialized), role)
    if type(result) is not VerificationReceipt:
        raise InvalidInput("VERIFIER_RECEIPT_REQUIRED_NOT_FLAGS")
    expected = hashlib.sha256(serialized).hexdigest()
    if (result.payload_sha256 != expected or result.role != role or
            result.scope not in {"SYNTHETIC_CONTROL_ONLY", "EXTERNAL_VERIFIER_CONDITIONAL"} or
            type(result.evidence_references) is not tuple or
            result.evidence_references != tuple(references) or
            not _hash(result.verifier_reference_sha256)):
        raise InvalidInput("VERIFIER_RECEIPT_BINDING_FAILED")
    return result


class Budget:
    """Cooperative arithmetic guard; supervisor supplies the hard process budget."""
    def __init__(self, deadline, clock=time.monotonic):
        if (type(deadline) not in (int, float) or not math.isfinite(deadline)
                or not callable(clock)):
            raise InvalidInput("DEADLINE_OR_CLOCK_INVALID")
        self.clock = clock
        current = clock()
        if type(current) not in (int, float) or not math.isfinite(current):
            raise InvalidInput("CLOCK_INVALID")
        self.deadline = min(deadline, current + 30.0)

    def checkpoint(self):
        current = self.clock()
        if type(current) not in (int, float) or not math.isfinite(current):
            raise InvalidCertificate("CLOCK_INVALID")
        if current >= self.deadline:
            raise ResourceLimit("NOMINAL_ARITHMETIC_DEADLINE")

    def integer(self, value):
        self.checkpoint()
        if type(value) is not int:
            raise InvalidCertificate("SCRATCH_INTEGER_TYPE")
        if value.bit_length() > MAX_SCRATCH_BITS:
            raise ResourceLimit("SCRATCH_524288_BITS")
        return value

    def multiply(self, a, b):
        self.integer(a)
        self.integer(b)
        # Conservative preflight upper bound; never allocate an over-budget product.
        if a and b and a.bit_length() + b.bit_length() > MAX_SCRATCH_BITS:
            raise ResourceLimit("PREDICTED_PRODUCT_524288_BITS")
        result = a * b
        return self.integer(result)

    def power(self, a, exponent):
        if type(exponent) is not int or not 0 <= exponent <= 512:
            raise InvalidCertificate("POWER_EXPONENT")
        self.integer(a)
        result = 1
        while exponent:
            self.checkpoint()
            if exponent & 1:
                result = self.multiply(result, a)
            exponent >>= 1
            if exponent:
                a = self.multiply(a, a)
        return result


def _failure(status, reason):
    return {"status": status, "reason": reason, "p_upper": None,
            "physical_certification": False, "automatic_rejection": False}


def _success(payload, receipt, status, numerator, denominator, certificate, reason=None):
    return {
        "status": status, "reason": reason, "p_upper": _encoded(numerator, denominator),
        "identity": dict(payload["identity"]), "input": json.loads(canonical_bytes(payload)),
        "semantic_scope": receipt.scope,
        "semantic_receipt": {
            "payload_sha256": receipt.payload_sha256, "role": receipt.role,
            "scope": receipt.scope, "evidence_references": list(receipt.evidence_references),
            "verifier_reference_sha256": receipt.verifier_reference_sha256,
        },
        "certificate": certificate, "exact_SF_claim": False,
        "physical_certification": False, "automatic_rejection": False,
    }


def ceil_root_certificate(numerator, denominator, budget):
    """Exact internal certificate helper; does not certify a statistical model."""
    budget.integer(numerator)
    budget.integer(denominator)
    if not 0 < numerator <= denominator:
        raise InvalidCertificate("R_OUTSIDE_POSITIVE_UNIT_INTERVAL")
    scaled = budget.multiply(numerator, Q * Q)
    budget.checkpoint()
    floor_ratio = scaled // denominator
    budget.checkpoint()
    k = math.isqrt(floor_ratio)
    budget.checkpoint()
    k_square_denominator = budget.multiply(k * k, denominator)
    u = k if k_square_denominator == scaled else k + 1
    lower_product = budget.multiply((u - 1) * (u - 1), denominator)
    upper_product = budget.multiply(u * u, denominator)
    if not (1 <= u <= Q and lower_product < scaled <= upper_product):
        raise InvalidCertificate("CEIL_ROOT_CERTIFICATE_FAILED")
    budget.checkpoint()
    certificate = {
        "kind": "EXACT_RATIONAL_AND_CEIL_ROOT",
        "R_numerator_hex": format(numerator, "x"),
        "R_denominator_hex": format(denominator, "x"),
        "root_index": str(u), "Q": str(Q), "N": N,
        "inequality": "(u-1)^2*B < A*Q^2 <= u^2*B; 1<=u<=Q; 0<A<=B",
        "numerical_evaluation_completed": True,
    }
    return u, certificate


def tail_upper(request, domain, verifier, deadline, clock=time.monotonic):
    """Compute only a conditional upper bound; semantic verification is external."""
    try:
        _domain(domain)
        if type(request) is not dict or set(request) != {"identity", "d", "x_lower"}:
            raise InvalidInput("REQUEST_SCHEMA")
        _identity(request["identity"], domain)
        if type(request["d"]) is not int or not 0 <= request["d"] <= 148:
            raise InvalidInput("DEGREE_TYPE_OR_RANGE")
        a, b = _rational(request["x_lower"])
        # All request fields are bounded primitive values before copying/hashing.
        payload = json.loads(canonical_bytes(request))
        receipt = _semantic(payload, "STATISTIC_SEMANTICS",
                            [payload["identity"][k] for k in HASH_KEYS], verifier)
    except InvalidInput as error:
        return _failure("UNAVAILABLE", str(error))
    except Exception as error:
        return _failure("INVALID", "SEMANTIC_VERIFIER_ERROR:" + type(error).__name__)

    d = payload["d"]
    # F9 coherence guard precedes all resource fallback, tail and aggregation.
    if d == 0 and a > 0:
        return _failure("INVALID", "CONTRACT_INCOHERENCE_NOT_REJECTION")
    if d == 0:
        return _success(payload, receipt, "VALID_ATOM_TAIL", 1, 1,
                        {"kind": "F9_NONPOSITIVE_ATOM_BOUND"})
    if a <= d * b:
        return _success(payload, receipt, "VALID_TRIVIAL_BOUND_MATHEMATICAL", 1, 1,
                        {"kind": "LOWER_STATISTIC_AT_OR_BELOW_DEGREE"})
    try:
        budget = Budget(deadline, clock)
        # R=(a/(b*d))^d * (512*b/(a+(512-d)*b))^512.
        bd = budget.multiply(b, d)
        denominator_base = a + budget.multiply(512 - d, b)
        budget.integer(denominator_base)
        numerator = budget.multiply(budget.power(a, d),
                                    budget.power(budget.multiply(512, b), 512))
        denominator = budget.multiply(budget.power(bd, d),
                                      budget.power(denominator_base, 512))
        budget.checkpoint()
        common = math.gcd(numerator, denominator)
        budget.checkpoint()
        numerator //= common
        denominator //= common
        if not 0 < numerator <= denominator:
            raise InvalidCertificate("R_OUTSIDE_POSITIVE_UNIT_INTERVAL")
        u, certificate = ceil_root_certificate(numerator, denominator, budget)
        return _success(payload, receipt, "VALID_CERTIFIED_ENVELOPE", u, Q, certificate)
    except ResourceLimit as error:
        return _success(payload, receipt, "VALID_TRIVIAL_BOUND_RESOURCE_LIMIT", 1, 1,
                        {"kind": "PREDECLARED_TRIVIAL_BOUND_AFTER_SEMANTIC_VALIDATION",
                         "numerical_evaluation_completed": False,
                         "monotonic_across_resource_states": False},
                        str(error))
    except Exception as error:
        return _failure("INVALID", "ARITHMETIC_OR_CERTIFICATE_ERROR:" + type(error).__name__)


def aggregate_bounds(records, domain, verifier):
    """max of every frozen scenario then Bonferroni5; no threshold evaluation.

    The record verifier must validate each bound/certificate, not merely its
    status. Test fixtures may be verified as synthetic rational bounds. A receipt
    proves only that this explicit verifier accepted the exact record.
    """
    try:
        _domain(domain)
        if type(records) is not list or len(records) != len(domain.scenarios):
            raise InvalidInput("MISSING_OR_EXTRA_SCENARIO")
        seen = set()
        best = (0, 1)
        verified = []
        for row in records:
            if type(row) is not dict or set(row) != {
                    "identity", "status", "p_upper", "bound_certificate_sha256"}:
                raise InvalidInput("BOUND_RECORD_SCHEMA")
            _identity(row["identity"], domain)
            scenario = row["identity"]["scenario_id"]
            if scenario in seen:
                raise InvalidInput("DUPLICATED_SCENARIO")
            seen.add(scenario)
            if row["status"] not in VALID_STATUSES:
                raise InvalidInput("SCENARIO_BOUND_UNAVAILABLE_OR_INVALID")
            if not _hash(row["bound_certificate_sha256"]):
                raise InvalidInput("BOUND_CERTIFICATE_REFERENCE")
            a, b = _rational(row["p_upper"])
            if not 0 < a <= b:
                raise InvalidInput("F9_BOUND_NOT_IN_POSITIVE_UNIT_INTERVAL")
            payload = json.loads(canonical_bytes(row))
            refs = [row["identity"][k] for k in HASH_KEYS]
            refs.append(row["bound_certificate_sha256"])
            receipt = _semantic(payload, "BOUND_RECORD", refs, verifier)
            if a * best[1] > best[0] * b:
                best = (a, b)
            verified.append({"scenario_id": scenario, "scope": receipt.scope,
                             "record_sha256": receipt.payload_sha256})
        if seen != set(domain.scenarios):
            raise InvalidInput("FAMILY_INCOMPLETE")
        a, b = best
        adjusted = _encoded(1, 1) if 5 * a >= b else _encoded(5 * a, b)
        return {"status": "COMPLETE_CONDITIONAL_BOUND", "p_robust": _encoded(a, b),
                "p_FWER_upper": adjusted, "family_factor": 5,
                "verified_records": verified, "alpha_evaluated": False,
                "physical_certification": False, "automatic_rejection": False}
    except InvalidInput as error:
        return {"status": "UNAVAILABLE", "reason": str(error),
                "p_robust": None, "p_FWER_upper": None, "automatic_rejection": False}
    except Exception as error:
        return {"status": "INVALID", "reason": "BOUND_VERIFIER_ERROR:" + type(error).__name__,
                "p_robust": None, "p_FWER_upper": None, "automatic_rejection": False}
