"""Prepared I05->I06 adapter. No I/O, solver, discovery, retry or execution CLI.

Loaded objects and external semantic verifiers remain a trusted caller boundary.
Do not confuse matching hashes/typed receipts with proof of their statements.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import hashlib
import json
import math
import time
import threshold_audit

from frozen_contract import (SOURCE_PINS, SCENARIOS, MODELS, TESTS, TEST_MODELS,
                             DOMAIN, DOMAIN_SHA256, FAMILY_SHA256,
                             MODEL_SHA256, NUMERICAL_SHA256, PROFILE_REQUEST_ID)


class BridgeError(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise BridgeError(reason)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def raw_sha(raw):
    need(type(raw) is bytes, "BYTES_REQUIRED")
    return hashlib.sha256(raw).hexdigest()


def is_hash(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def decode(raw):
    need(type(raw) is bytes and len(raw) <= 262144, "PROFILE_SIZE_OR_TYPE")
    def bad(_):
        raise BridgeError("NONFINITE_JSON")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def finite(value):
    need(type(value) in (int, float), "NUMBER_NOT_BOOL")
    value = float(value)
    need(math.isfinite(value), "NONFINITE_NUMBER")
    return value


def rational(value):
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "RATIONAL_SCHEMA")
    for name in value:
        text = value[name]
        need(type(text) is str and 1 <= len(text) <= 156, "RATIONAL_TEXT_BOUND")
        unsigned = text[1:] if text.startswith("-") else text
        need(unsigned.isascii() and unsigned.isdigit(), "RATIONAL_GRAMMAR")
        need(str(int(text)) == text, "RATIONAL_CANONICAL")
    a, b = int(value["numerator"]), int(value["denominator"])
    need(b > 0 and max(abs(a).bit_length(), b.bit_length()) <= 512, "RATIONAL_512_BIT_BOUND")
    need(math.gcd(abs(a), b) == 1, "RATIONAL_REDUCED")
    return Fraction(a, b)


def encoded(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def outward_float(value, upward):
    candidate = float(value)
    need(math.isfinite(candidate), "FLOAT_RANGE")
    exact = Fraction(*candidate.as_integer_ratio())
    if (upward and exact < value) or (not upward and exact > value):
        candidate = math.nextafter(candidate, math.inf if upward else -math.inf)
    need((Fraction(*candidate.as_integer_ratio()) >= value) if upward
         else (Fraction(*candidate.as_integer_ratio()) <= value), "OUTWARD_CONVERSION_FAILED")
    return candidate


def conservative_log_bound(probability, checkpoint=lambda: None):
    """Refined upper log via exact negative atanh series, not libm.

    Normalize p=m*2^-k, 1/2<m<=1. The truncated negative atanh series
    is ABOVE ln(m), and -k*Lln2 is ABOVE -k*ln2. Compress the exact
    upper to a decimal rational rounded UP before any decimal serialization.
    """
    p = rational(probability)
    need(0 < p <= 1, "POSITIVE_PROBABILITY_REQUIRED")
    checkpoint()
    if p == 1:
        return {"method": "NORMALIZED_ATANH64_DECIMAL80_UPWARD_FLOAT_V1",
                "probability_upper": encoded(p), "dyadic_k_diagnostic": 0,
                "log_upper_rational": encoded(Fraction(0)),
                "series_plus_compression_error_upper": encoded(Fraction(0)),
                "decimal_scale": 80, "log_p_upper": 0.0, "threshold_certified": False}
    k = 0
    while p.numerator * (1 << (k + 1)) <= p.denominator:
        k += 1
    m = p * (1 << k)
    z = (m - 1) / (m + 1)
    need(Fraction(-1, 3) <= z <= 0, "LOG_NORMALIZATION")
    lower_ln2 = Fraction(0)
    upper_lnm = Fraction(0)
    for j in range(64):
        checkpoint()
        lower_ln2 += Fraction(2, (2*j+1) * 3**(2*j+1))
        upper_lnm += 2 * z**(2*j+1) / (2*j+1)
    exact_upper = upper_lnm - k * lower_ln2
    scale = 10**80
    # Exact ceil of signed rational; no global integer-string limit change.
    scaled = exact_upper * scale
    numerator = -(-scaled.numerator // scaled.denominator)
    compressed_upper = Fraction(numerator, scale)
    need(compressed_upper >= exact_upper and compressed_upper <= 0, "LOG_ENCLOSURE")
    remainder = Fraction(9, 4*129*3**129)
    return {"method": "NORMALIZED_ATANH64_DECIMAL80_UPWARD_FLOAT_V1",
            "probability_upper": encoded(p), "dyadic_k_diagnostic": k,
            "log_upper_rational": encoded(compressed_upper),
            "series_plus_compression_error_upper": encoded((k+1)*remainder + Fraction(1, scale)),
            "decimal_scale": 80,
            "log_p_upper": outward_float(compressed_upper, True),
            "threshold_certified": False}


@dataclass(frozen=True)
class Receipt:
    role: str
    payload_sha256: str
    evidence_sha256: tuple
    verifier_sha256: str
    scope: str


def accept_receipt(result, role, payload, evidence, verifier_sha256, scope):
    need(type(result) is Receipt, "TYPED_RECEIPT_REQUIRED_NOT_FLAG")
    need(result.role == role and result.payload_sha256 == digest(payload)
         and result.evidence_sha256 == tuple(sorted(evidence))
         and result.verifier_sha256 == verifier_sha256
         and result.scope == scope, "EXTERNAL_RECEIPT_BINDING")
    return result


CONTEXT_FIELDS = ("data_sha256", "covariance_sha256", "X_response_sha256",
                  "support_sha256", "engine_config_sha256", "consumer_admission_sha256")
CERT_FIELDS = {"binding", "lower", "upper", "error_status", "proof"}
HYP_FIELDS = {"binding", "degree", "support", "domination", "degree_proof", "inclusion"}


class Bridge:
    """Pure composition over previously admitted bytes and exact certificate material.

    object_verifier must inspect actual loaded objects independently, not just pins.
    semantic_verifier must validate proof content, source lineage, hypotheses and
    release evidence. Neither implementation is supplied as a fake scientific verifier.
    """
    def __init__(self, *, modules, object_verifier, object_verifier_sha256,
                 semantic_verifier=None, semantic_verifier_sha256=None,
                 semantic_scope="EXTERNAL_SCIENTIFIC_CONDITIONAL", deadline, clock=time.monotonic):
        need(set(modules) == {"profile", "theta", "tail", "reducer"}, "LOADED_MODULE_SET")
        need(callable(object_verifier) and is_hash(object_verifier_sha256), "OBJECT_VERIFIER_REQUIRED")
        need(semantic_verifier is None or (callable(semantic_verifier)
             and is_hash(semantic_verifier_sha256)), "SEMANTIC_VERIFIER_IDENTITY")
        self.modules = dict(modules)
        self.object_verifier = object_verifier
        self.object_verifier_sha256 = object_verifier_sha256
        self.semantic_verifier = semantic_verifier
        self.semantic_verifier_sha256 = semantic_verifier_sha256
        need(semantic_scope in ("EXTERNAL_SCIENTIFIC_CONDITIONAL", "SYNTHETIC_CONTROL_ONLY"), "SEMANTIC_SCOPE")
        self.semantic_scope = semantic_scope
        self.deadline, self.clock = finite(deadline), clock
        self.calls = 0
        self._objects()

    def checkpoint(self):
        need(finite(self.clock()) < self.deadline, "COOPERATIVE_DEADLINE")

    def _objects(self):
        self.checkpoint()
        pins = {key: SOURCE_PINS[key] for key in self.modules}
        result = self.object_verifier(self.modules, json.loads(canonical(pins)))
        self.checkpoint()
        accept_receipt(result, "LOADED_OBJECTS", pins,
                       [p["sha256"] for p in pins.values()],
                       self.object_verifier_sha256, "LOADED_OBJECTS_ONLY")
        need(tuple(self.modules["profile"].MODELS) == MODELS
             and tuple(self.modules["theta"].MODELS) == MODELS
             and tuple(self.modules["reducer"].TESTS) == TESTS
             and self.modules["reducer"].CONTRACT_SHA256 == MODEL_SHA256,
             "MODEL_OR_CONTRACT_IDENTITY")

    def verify(self, role, payload, materials):
        """None means unavailable. Malformed/cross-bound/stale receipts fail closed."""
        self.checkpoint()
        need(type(materials) is dict and len(materials) <= 32, "MATERIAL_COUNT")
        total = 0
        for pin, raw in materials.items():
            need(is_hash(pin) and type(raw) is bytes and raw_sha(raw) == pin, "PROOF_BYTES_PIN")
            total += len(raw)
        need(total <= 8388608, "MATERIAL_BYTES_CAP")
        if self.semantic_verifier is None:
            return None
        self.calls += 1
        need(self.calls <= 6002, "SEMANTIC_CALL_CAP")
        result = self.semantic_verifier(role, json.loads(canonical(payload)), dict(materials))
        self.checkpoint()
        if result is None:
            return None
        return accept_receipt(result, role, payload, materials,
                              self.semantic_verifier_sha256, self.semantic_scope)

    def contexts(self, supplied):
        need(type(supplied) is dict and tuple(supplied) == SCENARIOS, "EXACT_600_ORDERED_CONTEXTS")
        result = {}
        for sid, ctx in supplied.items():
            need(type(ctx) is dict and set(ctx) == set(CONTEXT_FIELDS), "CONTEXT_FIELDS")
            need(all(is_hash(v) for v in ctx.values()), "CONTEXT_PINS")
            result[sid] = dict(ctx)
        return result

    def binding(self, sid, ctx, *, model=None, test=None):
        result = {"scenario_id": sid, "family_sha256": FAMILY_SHA256,
                  "model_contract_sha256": MODEL_SHA256, "domain_sha256": DOMAIN_SHA256,
                  "numerical_contract_sha256": NUMERICAL_SHA256, **ctx}
        if model is not None:
            result["model_id"] = model
        if test is not None:
            result.update(test_id=test, null_model_id=TEST_MODELS[test][0],
                          competitor_model_id=TEST_MODELS[test][1])
        return result

    def estimate_family(self, records, *, contexts, level, max_records):
        """Stream every existing profile artifact in scenario/node order; no callbacks.

        Records: (scenario_id, canonical_node_key, profile_json_bytes,
                  expected_profile_sha256, expected_assembly_sha256, expected_background_sha256).
        Keys/theta are reused from the pinned theta module. Continuous coverage is
        never inferred from the finite plan.
        """
        self._objects()
        ctxs = self.contexts(contexts)
        need(type(level) is int and 1 <= level <= self.modules["theta"].MAX_LEVEL, "LEVEL")
        n = 2**level
        required = len(SCENARIOS) * (n+1)**3
        need(type(max_records) is int and max_records >= required, "FULL_PLAN_BUDGET")
        iterator, count, output = iter(records), 0, {}
        theta = self.modules["theta"]
        for sid in SCENARIOS:
            best = {m: None for m in MODELS}
            missing = {m: 0 for m in MODELS}
            chain = hashlib.sha256()
            for indices in product(range(n+1), repeat=3):
                self.checkpoint()
                key = theta._node_key(indices, n)
                expected_theta = list(theta._theta(key))
                row = next(iterator, None)
                need(type(row) in (tuple, list) and len(row) == 6, "MISSING_PROFILE_RECORD")
                got_sid, got_key, raw, profile_pin, assembly_pin, background_pin = row
                need(got_sid == sid and tuple(got_key) == key, "PROFILE_ORDER_OR_DUPLICATE")
                need(is_hash(profile_pin) and raw_sha(raw) == profile_pin
                     and is_hash(assembly_pin) and is_hash(background_pin), "PROFILE_INPUT_PINS")
                prof = decode(raw)
                need(prof["schema"] == "F9_CONDITIONAL_AFFINE_PROFILE_RESULT_V1"
                     and prof["request_id"] == PROFILE_REQUEST_ID
                     and prof["status"] == "ENGINEERING_ONLY"
                     and prof["base_theta_prior"] == {"density_exact": "50/3", "applied": False, "integrated": False}
                     and prof["MM_status"] == "CONDITIONAL_UNRATIFIED"
                     and prof["measure"] == self.modules["theta"].MEASURE
                     and prof["output_measure"] == self.modules["theta"].OUTPUT_MEASURE
                     and prof["theta"] == expected_theta
                     and set(prof["models"]) == set(MODELS)
                     and prof["physical_extra_priors_applied"] is False
                     and prof["global_theta_search_performed"] is False
                     and all(prof[k] is None for k in
                             ("global_minima", "relative_evidence", "lnB", "p", "sigma", "verdict")),
                     "PROFILE_SCHEMA_SCOPE_OR_DOMAIN")
                provenance = prof["provenance"]
                need(provenance["assembly_sha256"] == assembly_pin
                     and provenance["background_sha256"] == background_pin
                     and provenance["consumer_admission_sha256"] == ctxs[sid]["consumer_admission_sha256"]
                     and provenance["source_pins"] == self.modules["profile"].SOURCE_PINS,
                     "PROFILE_PROVENANCE")
                pin = raw_sha(raw)
                chain.update(canonical([sid, key, pin, assembly_pin, background_pin]))
                for model in MODELS:
                    rec = prof["models"][model]
                    certs = rec["certificates"]
                    need(certs["conditional_minimum"] == {
                            "status": "UNAVAILABLE", "lower": None, "upper": None,
                            "certificate": None, "verified": False}
                         and certs["global_theta_minimum"] == {
                            "status": "NOT_SEARCHED", "estimate": None, "lower": None,
                            "upper": None, "certificate": None, "verified": False},
                         "PROFILE_CERTIFICATE_PROMOTION")
                    q = rec["q_feasible_estimate"]
                    if q is None:
                        need(rec["status"] in (
                            "ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT",
                            "ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT"),
                            "UNKNOWN_PROFILE_FAILURE_NOT_SUPPORT_ZERO")
                        need(rec["log_profile_deta"] == {"$float": "-inf"}, "SUPPORT_ZERO_LOG_TAG")
                        missing[model] += 1
                        continue
                    need(rec["status"] in ("FINITE_LOG_FLAT_INTEGRAL",
                         "FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY",
                         "CONDITIONAL_FEASIBLE_PROFILE_ESTIMATE"), "UNKNOWN_FINITE_PROFILE_STATUS")
                    q = finite(q)
                    finite(rec["log_profile_deta"])
                    need(q >= 0, "NEGATIVE_Q")
                    params = rec["physical_parameters"]
                    need(type(params) is dict and
                         [params[k] for k in DOMAIN["theta_names"]] == expected_theta,
                         "WITNESS_THETA")
                    extras = {"H3_beta_free": "beta", "H4_Cepheid": "s", "H5_rd_free": "rd_Mpc"}
                    names = set(DOMAIN["theta_names"]) | ({extras[model]} if model in extras else set())
                    need(set(params) == names, "WITNESS_COORDINATES")
                    if model in extras:
                        lo, hi = map(Fraction, DOMAIN["extra_bounds"][model])
                        val = Fraction(*finite(params[extras[model]]).as_integer_ratio())
                        # Source physical endpoints are binary64 versions of the exact endpoints.
                        need(float(lo) <= float(val) <= float(hi), "WITNESS_EXTRA_DOMAIN")
                    if best[model] is None or q < best[model]["q_estimate"]:
                        best[model] = {"q_estimate": q, "physical_parameters": dict(params),
                                       "profile_sha256": pin, "node_key": list(key)}
                count += 1
            output[sid] = {"models": best, "support_zero_counts": missing,
                           "profile_chain_sha256": chain.hexdigest(),
                           "status": "FINITE_PLAN_ESTIMATE_ONLY",
                           "minimum_interval": None, "continuous_domain_covered": False}
        need(next(iterator, None) is None and count == required, "EXTRA_PROFILE_OR_COUNT")
        self._objects()
        return {"schema": "F9_PROFILE_FAMILY_ESTIMATES_V1", "status": "ENGINEERING_ONLY",
                "scenarios": output, "domain": DOMAIN, "family_sha256": FAMILY_SHA256,
                "domain_sha256": DOMAIN_SHA256, "level": level, "records": count,
                "all_planned_nodes_present": True, "global_minimum_proved": False,
                "continuous_search_performed": False, "certified_bounds": None,
                "p": None, "verdict": None, "callbacks_executed": 0}

    def _minimum(self, cert, expected, materials):
        if cert is None:
            return None
        need(type(cert) is dict and set(cert) == CERT_FIELDS, "MINIMUM_SCHEMA")
        need(cert["binding"] == expected and is_hash(cert["proof"]), "MINIMUM_IDENTITY")
        if cert["proof"] not in materials:
            return None
        need(cert["error_status"] in ("BOUNDED", "UNAVAILABLE",
                                     "ANALYTIC_NONNEGATIVITY"), "MINIMUM_ERROR_STATUS")
        if cert["error_status"] == "UNAVAILABLE":
            return None
        lower = rational(cert["lower"]) if cert["lower"] is not None else None
        upper = rational(cert["upper"]) if cert["upper"] is not None else None
        need(lower is None or lower >= 0, "NEGATIVE_MINIMUM_LOWER")
        need(upper is None or upper >= 0, "NEGATIVE_MINIMUM_UPPER")
        need(lower is None or upper is None or lower <= upper, "INVERTED_INTERVAL")
        if cert["error_status"] == "ANALYTIC_NONNEGATIVITY":
            need(lower == 0 and upper is None, "ANALYTIC_NOT_NUMERICAL_WITNESS")
        receipt = self.verify("MINIMUM_BOUNDS", cert, materials)
        if receipt is None:
            return None
        return {"lower": lower, "upper": upper, "certificate_sha256": digest(cert)}

    def reduce_certificates(self, *, contexts, certificates, materials_by_scenario,
                            opening=None, opening_materials=None):
        """One tail per scenario/test, then one reducer call and independent exact audit.

        No estimate is accepted as a certificate. Threshold ambiguity/disagreement
        retains calibration evidence but publishes no scientific decision.
        """
        self._objects()
        ctxs = self.contexts(contexts)
        reducer, tail = self.modules["reducer"], self.modules["tail"]
        closed = dict(data_released=False, v1_ratified=False,
                      integrity_valid=False, common_support_valid=False)
        if opening is None:
            need(certificates is None and materials_by_scenario is None, "CLOSED_NO_CERTIFICATE_INPUT")
            return {"status": "AWAITING_EXTERNAL_OPENING", "scientific_decision": None,
                    "logical_proposal": reducer.evaluate_decisions(None, scenario_ids=SCENARIOS,
                                      readiness=closed, contract_sha256=MODEL_SHA256)}
        need(type(opening) is dict and set(opening) == {"binding", "readiness", "proof"}, "OPENING_SCHEMA")
        expected_open = {"family_sha256": FAMILY_SHA256, "model_contract_sha256": MODEL_SHA256,
                         "domain_sha256": DOMAIN_SHA256, "contexts_sha256": digest(ctxs)}
        need(opening["binding"] == expected_open and is_hash(opening["proof"]), "OPENING_BINDING")
        readiness = opening["readiness"]
        need(type(readiness) is dict and set(readiness) == set(closed)
             and all(type(x) is bool for x in readiness.values()), "READINESS_SCHEMA")
        need(type(opening_materials) is dict, "OPENING_MATERIALS")
        opened = (opening["proof"] in opening_materials and
                  self.verify("OPENING_AND_ADMISSIONS", opening, opening_materials) is not None)
        if not opened or not all(readiness.values()):
            return {"status": "ADMISSION_UNAVAILABLE", "scientific_decision": None,
                    "logical_proposal": None}
        need(type(certificates) is dict and tuple(certificates) == SCENARIOS, "CERTIFICATE_FAMILY_ORDER")
        need(type(materials_by_scenario) is dict and tuple(materials_by_scenario) == SCENARIOS,
             "MATERIAL_FAMILY_ORDER")
        records = {test: {} for test in TESTS}
        diagnostics, valid_payloads = {}, {}
        for sid in SCENARIOS:
            self.checkpoint()
            bundle = certificates[sid]
            mats = materials_by_scenario[sid]
            need(type(bundle) is dict and set(bundle) == {"models", "hypotheses"}, "BUNDLE_SCHEMA")
            need(type(bundle["models"]) is dict and set(bundle["models"]) == set(MODELS), "FIVE_MINIMA_REQUIRED")
            need(type(bundle["hypotheses"]) is dict and set(bundle["hypotheses"]) == set(TESTS), "FIVE_TESTS_REQUIRED")
            minima = {m: self._minimum(bundle["models"][m], self.binding(sid, ctxs[sid], model=m), mats)
                      for m in MODELS}
            diagnostics[sid] = {}
            for test in TESTS:
                null, competitor = TEST_MODELS[test]
                first, second = minima[null], minima[competitor] if competitor else None
                hyp = bundle["hypotheses"][test]
                lower = first["lower"] if first is not None else None
                if competitor is not None:
                    lower = (lower - second["upper"] if lower is not None and second is not None
                             and second["upper"] is not None else None)
                record = {"statistic": None, "statistic_available": False, "statistic_valid": False,
                          "calibration_status": "UNAVAILABLE", "calibration_scope": "",
                          "log_p_upper": None, "numerical_certificate": None,
                          "calibration_reference": None, "direction_positive_certified": False,
                          "direction_reference": None}
                records[test][sid] = record
                diagnostics[sid][test] = {"status": "UNAVAILABLE", "reason": "MISSING_BOUND_OR_HYPOTHESIS"}
                if lower is None or hyp is None:
                    continue
                need(type(hyp) is dict and set(hyp) == HYP_FIELDS, "HYPOTHESIS_SCHEMA")
                need(hyp["binding"] == self.binding(sid, ctxs[sid], test=test), "HYPOTHESIS_BINDING")
                need(type(hyp["degree"]) is int and 0 <= hyp["degree"] <= 148, "DEGREE")
                required = ("support", "domination", "degree_proof") + (("inclusion",) if test == "LAW_H1_VS_FREE" else ())
                need(all(is_hash(hyp[k]) for k in required), "HYPOTHESIS_PINS")
                need(test == "LAW_H1_VS_FREE" or hyp["inclusion"] is None, "UNUSED_INCLUSION")
                if any(hyp[k] not in mats for k in required):
                    continue
                if self.verify("STATISTICAL_HYPOTHESES", hyp, mats) is None:
                    continue
                if test in TESTS[:2]:
                    lower = max(Fraction(0), lower)
                # Result may exceed the existing tail input size after subtraction.
                try:
                    lower = rational(encoded(lower))
                except BridgeError:
                    diagnostics[sid][test]["reason"] = "TAIL_RATIONAL_INPUT_LIMIT"
                    continue
                statement = {"binding": hyp["binding"], "lower": encoded(lower),
                             "minimum_certificates": [first["certificate_sha256"]] +
                             ([second["certificate_sha256"]] if second is not None else []),
                             "inclusion": hyp["inclusion"], "derivation": test}
                identity = {"test_id": test, "null_model_id": null, "scenario_id": sid,
                            "frozen_scenario_family_sha256": FAMILY_SHA256,
                            "model_contract_sha256": MODEL_SHA256,
                            "lower_statistic_certificate_sha256": digest(statement),
                            "support_certificate_sha256": hyp["support"],
                            "domination_certificate_sha256": hyp["domination"],
                            "degree_certificate_sha256": hyp["degree_proof"],
                            "algorithm_contract_sha256": SOURCE_PINS["tail"]["sha256"]}
                domain = tail.Domain(test, null, SCENARIOS, FAMILY_SHA256, MODEL_SHA256,
                                     SOURCE_PINS["tail"]["sha256"])
                request = {"identity": identity, "d": hyp["degree"], "x_lower": encoded(lower)}
                family = tail.family_payload(domain)
                def verified(payload, role):
                    # Exact scoped wrapper over already externally validated material.
                    need((role == "FROZEN_DOMAIN_FAMILY" and payload == family) or
                         (role == "STATISTIC_SEMANTICS" and payload == request), "TAIL_CALLBACK_PAYLOAD")
                    refs = ((domain.family_sha256, domain.model_sha256, domain.algorithm_sha256)
                            if role == "FROZEN_DOMAIN_FAMILY" else
                            tuple(identity[k] for k in tail.HASH_KEYS))
                    return tail.VerificationReceipt(tail.digest(payload), role,
                            ( "SYNTHETIC_CONTROL_ONLY" if self.semantic_scope == "SYNTHETIC_CONTROL_ONLY"
                              else "EXTERNAL_VERIFIER_CONDITIONAL"), refs, self.semantic_verifier_sha256)
                self.checkpoint()
                bound = tail.tail_upper(request, domain, verified, self.deadline, self.clock)
                self.checkpoint()
                diagnostics[sid][test] = {"status": bound["status"], "reason": bound.get("reason"),
                                         "lower_statement": statement, "tail_result": bound}
                if bound["status"] not in tail.VALID_STATUSES:
                    record["calibration_status"] = "INVALID" if bound["status"] == "INVALID" else "UNAVAILABLE"
                    continue
                need(bound["identity"] == identity and bound["input"] == request, "TAIL_OUTPUT_BINDING")
                log = conservative_log_bound(bound["p_upper"], self.checkpoint)
                bound_pin = digest(bound)
                record.update(statistic=outward_float(lower, False), statistic_available=True,
                              statistic_valid=True, calibration_status="VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND",
                              calibration_scope="EXTERNAL_HYPOTHESES_AND_MINIMUM_PROOFS_CONDITIONAL",
                              log_p_upper=log["log_p_upper"],
                              numerical_certificate={"id": "lower-statistic", "sha256": digest(statement)},
                              calibration_reference={"id": "tail-bound", "sha256": bound_pin})
                if test in TESTS[2:] and lower > 0 and record["statistic"] > 0:
                    record.update(direction_positive_certified=True,
                                  direction_reference={"id": "positive-certified-lower", "sha256": digest(statement)})
                diagnostics[sid][test]["log_conversion"] = log
                valid_payloads[test + ":" + sid] = {"tail_sha256": bound_pin, "log": log, "lower": lower}
        proposal = reducer.evaluate_decisions(records, scenario_ids=SCENARIOS,
                         readiness=dict(readiness), contract_sha256=MODEL_SHA256)
        self._objects()
        try:
            exact = threshold_audit.audit(records, valid_payloads, proposal)
            audit_reason = None
        except threshold_audit.AuditUnavailable as error:
            exact, audit_reason = None, str(error)
        self.checkpoint()
        synthetic = self.semantic_scope == "SYNTHETIC_CONTROL_ONLY"
        return {"schema": "F9_PROFILE_DECISION_BRIDGE_RESULT_V1",
                "status": ("SYNTHETIC_CONTROL_ONLY" if synthetic else "EXTERNAL_VERIFIER_CONDITIONAL")
                          if exact is not None else "DECISION_UNAVAILABLE_THRESHOLD_AUDIT",
                "threshold_audit_reason": audit_reason,
                "records": records, "diagnostics": diagnostics,
                "logical_proposal": proposal,
                "logical_proposal_float_fields": "DIAGNOSTIC_NOT_CERTIFIED",
                "scientific_decision": exact if exact is not None and not synthetic else None,
                "synthetic_decision": exact if synthetic else None,
                "physical_confirmation": False, "authorization_granted": False,
                "gate_changed": False, "new_solver_calls": 0,
                "semantic_verifier_scope": self.semantic_scope,
                "trust_boundary": "EXTERNAL_PROOF_VALIDATOR_NOT_SUPPLIED_HERE"}



if __name__ == "__main__":
    raise SystemExit("PREPARATION_ONLY_NO_EXECUTION_AUTHORITY")
