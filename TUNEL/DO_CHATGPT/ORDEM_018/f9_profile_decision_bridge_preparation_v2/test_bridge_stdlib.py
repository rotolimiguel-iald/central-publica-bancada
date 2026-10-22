"""Prepared stdlib integration tests. NOT RUN in the preparation.

The semantic verifier below is a test double, never a scientific verifier.
It uses SYNTHETIC_CONTROL_ONLY and never publishes a scientific decision.
"""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import profile_decision_bridge as bridge
from frozen_contract import SOURCE_PINS, SCENARIOS, MODELS, TESTS, DOMAIN, MODEL_SHA256


def load_pinned(name):
    source = SOURCE_PINS[name]
    path = Path(source["path"])
    raw = path.read_bytes()
    assert len(raw) == source["bytes"] and hashlib.sha256(raw).hexdigest() == source["sha256"]
    spec = importlib.util.spec_from_file_location("bridge_test_" + name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# Importing this TEST MODULE is future test execution. Preparation only AST-parses it.
MODULES = {name: load_pinned(name) for name in ("theta", "tail", "reducer")}
profile_meta = SOURCE_PINS["profile"]
profile_raw = Path(profile_meta["path"]).read_bytes()
assert len(profile_raw) == profile_meta["bytes"] and hashlib.sha256(profile_raw).hexdigest() == profile_meta["sha256"]
profile_values = {}
for node in ast.parse(profile_raw).body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ("MODELS", "SOURCE_PINS"):
                profile_values[target.id] = ast.literal_eval(node.value)
MODULES["profile"] = SimpleNamespace(**profile_values)


def unavailable_certificates():
    return {"conditional_minimum": {"status":"UNAVAILABLE", "lower":None, "upper":None,
                                    "certificate":None, "verified":False},
            "global_theta_minimum": {"status":"NOT_SEARCHED", "estimate":None,
                                    "lower":None, "upper":None, "certificate":None, "verified":False}}
PIN = hashlib.sha256(b"LOCAL_SYNTHETIC_DOUBLE_NOT_SCIENTIFIC_PROOF").hexdigest()
RAW = b"LOCAL_SYNTHETIC_DOUBLE_NOT_SCIENTIFIC_PROOF"
CTX = {key: PIN for key in bridge.CONTEXT_FIELDS}


def object_verifier(modules, pins):
    assert all(modules[name] is MODULES[name] for name in MODULES)
    assert pins == {name: SOURCE_PINS[name] for name in MODULES}
    return bridge.Receipt("LOADED_OBJECTS", bridge.digest(pins),
                          tuple(sorted(p["sha256"] for p in pins.values())), PIN, "LOADED_OBJECTS_ONLY")


class FixtureVerifier:
    """A double for integration wiring; explicitly incapable of scientific approval."""
    def __init__(self):
        self.calls = []
        self.unavailable_role = None

    def __call__(self, role, payload, materials):
        self.calls.append(role)
        assert materials == {PIN: RAW}
        if role == "REDUCER_THRESHOLD_AND_OUTPUT" or role == self.unavailable_role:
            return None
        assert role in ("MINIMUM_BOUNDS", "STATISTICAL_HYPOTHESES", "OPENING_AND_ADMISSIONS")
        return bridge.Receipt(role, bridge.digest(payload), (PIN,), PIN,
                              "SYNTHETIC_CONTROL_ONLY")


def make(verifier=None, clock=lambda: 0.0):
    return bridge.Bridge(modules=MODULES, object_verifier=object_verifier,
                         object_verifier_sha256=PIN, semantic_verifier=verifier,
                         semantic_verifier_sha256=PIN if verifier else None,
                         semantic_scope="SYNTHETIC_CONTROL_ONLY", deadline=100.0, clock=clock)


def contexts():
    return {sid: dict(CTX) for sid in SCENARIOS}


def rational(n, d=1):
    from fractions import Fraction
    return bridge.encoded(Fraction(n, d))


def opening(b, ctxs):
    return {"binding": {"family_sha256": bridge.FAMILY_SHA256,
                        "model_contract_sha256": MODEL_SHA256,
                        "domain_sha256": bridge.DOMAIN_SHA256,
                        "contexts_sha256": bridge.digest(ctxs)},
            "readiness": dict(data_released=True, v1_ratified=True,
                              integrity_valid=True, common_support_valid=True),
            "proof": PIN}


def empty_bundles():
    return {sid: {"models": dict.fromkeys(MODELS), "hypotheses": dict.fromkeys(TESTS)}
            for sid in SCENARIOS}


def populated(b, ctxs, *, lower=0, upper=0):
    result = {}
    for sid in SCENARIOS:
        result[sid] = {
            "models": {m: {"binding": b.binding(sid, ctxs[sid], model=m),
                           "lower": rational(lower), "upper": rational(upper),
                           "error_status": "BOUNDED", "proof": PIN} for m in MODELS},
            "hypotheses": {t: {"binding": b.binding(sid, ctxs[sid], test=t),
                               "degree": 0, "support": PIN, "domination": PIN,
                               "degree_proof": PIN,
                               "inclusion": PIN if t == "LAW_H1_VS_FREE" else None}
                           for t in TESTS}}
    return result


def reduce(b, bundles, ctxs=None):
    ctxs = contexts() if ctxs is None else ctxs
    return b.reduce_certificates(contexts=ctxs, certificates=bundles,
        materials_by_scenario={sid: {PIN: RAW} for sid in SCENARIOS},
        opening=opening(b, ctxs), opening_materials={PIN: RAW})


def profile_rows():
    for sid in SCENARIOS:
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    key = MODULES["theta"]._node_key((a, b, c), 2)
                    theta = list(MODULES["theta"]._theta(key))
                    records = {}
                    for index, model in enumerate(MODELS):
                        params = dict(zip(DOMAIN["theta_names"], theta))
                        if model == "H3_beta_free":
                            params["beta"] = 0.0
                        elif model == "H4_Cepheid":
                            params["s"] = 0.0
                        elif model == "H5_rd_free":
                            params["rd_Mpc"] = 145.0
                        records[model] = {"q_feasible_estimate": float(a+b+c+index),
                            "physical_parameters": params, "log_profile_deta": -0.5*float(a+b+c+index), "status": ("FINITE_LOG_FLAT_INTEGRAL" if index < 2 else "CONDITIONAL_FEASIBLE_PROFILE_ESTIMATE"),
                            "certificates": unavailable_certificates()}
                    p = {"schema": "F9_CONDITIONAL_AFFINE_PROFILE_RESULT_V1",
                         "request_id": bridge.PROFILE_REQUEST_ID, "status": "ENGINEERING_ONLY",
                         "theta": theta, "models": records, "physical_extra_priors_applied": False,
                         "base_theta_prior": {"density_exact":"50/3", "applied":False, "integrated":False},
                         "MM_status": "CONDITIONAL_UNRATIFIED",
                         "measure": MODULES["theta"].MEASURE, "output_measure": MODULES["theta"].OUTPUT_MEASURE,
                         "global_theta_search_performed": False,
                         **dict.fromkeys(("global_minima", "relative_evidence", "lnB", "p", "sigma", "verdict")),
                         "provenance": {"assembly_sha256": PIN, "background_sha256": PIN,
                                        "consumer_admission_sha256": PIN,
                                        "source_pins": MODULES["profile"].SOURCE_PINS}}
                    raw = bridge.canonical(p)
                    yield sid, key, raw, hashlib.sha256(raw).hexdigest(), PIN, PIN


class Integration(unittest.TestCase):
    def test_all_600_five_models_and_entire_finite_plan_remain_estimates(self):
        out = make().estimate_family(profile_rows(), contexts=contexts(), level=1, max_records=16200)
        self.assertEqual(tuple(out["scenarios"]), SCENARIOS)
        self.assertEqual(out["records"], 16200)
        self.assertFalse(out["global_minimum_proved"])
        self.assertIsNone(out["certified_bounds"])
        for rec in out["scenarios"].values():
            self.assertFalse(rec["continuous_domain_covered"])
            self.assertEqual(set(rec["models"]), set(MODELS))
            self.assertEqual(rec["models"]["H1_TGL"]["q_estimate"], 0.0)

    def test_missing_first_record_fails(self):
        rows = profile_rows(); next(rows)
        with self.assertRaisesRegex(bridge.BridgeError, "ORDER"):
            make().estimate_family(rows, contexts=contexts(), level=1, max_records=16200)

    def test_duplicate_record_fails(self):
        rows = profile_rows(); first = next(rows)
        def bad():
            yield first; yield first
        with self.assertRaisesRegex(bridge.BridgeError, "ORDER"):
            make().estimate_family(bad(), contexts=contexts(), level=1, max_records=16200)

    def test_closed_path_has_no_semantic_calls_or_records(self):
        v = FixtureVerifier(); b = make(v)
        out = b.reduce_certificates(contexts=contexts(), certificates=None, materials_by_scenario=None)
        self.assertEqual(v.calls, [])
        self.assertIsNone(out["scientific_decision"])

    def test_closed_rejects_supplied_records(self):
        with self.assertRaisesRegex(bridge.BridgeError, "CLOSED"):
            make().reduce_certificates(contexts=contexts(), certificates={}, materials_by_scenario=None)

    def test_no_semantic_verifier_cannot_open(self):
        b = make(); out = reduce(b, empty_bundles())
        self.assertEqual(out["status"], "ADMISSION_UNAVAILABLE")

    def test_forged_boolean_receipt_fails(self):
        b = make(lambda *args: True)
        with self.assertRaisesRegex(bridge.BridgeError, "NOT_FLAG"):
            reduce(b, empty_bundles())

    def test_missing_certificate_not_artificial_p1(self):
        out = reduce(make(FixtureVerifier()), empty_bundles())
        for test in TESTS:
            self.assertFalse(out["logical_proposal"]["tests"][test]["complete"])
            self.assertTrue(all(r["log_p_upper"] is None for r in out["records"][test].values()))

    def test_valid_atom_wiring_exact_audit_remains_synthetic(self):
        b = make(FixtureVerifier()); out = reduce(b, populated(b, contexts()))
        self.assertIsNone(out["scientific_decision"])
        self.assertEqual(out["status"], "SYNTHETIC_CONTROL_ONLY")
        self.assertIsNotNone(out["synthetic_decision"])
        self.assertEqual(out["logical_proposal"]["multiplicity"], 5)
        self.assertEqual(out["logical_proposal"]["tests"]["COMPAT_H1"]["adjusted_bound"]["p_upper"], 1.0)

    def test_degree_zero_positive_is_invalid_not_rejection(self):
        b = make(FixtureVerifier()); out = reduce(b, populated(b, contexts(), lower=1, upper=1))
        self.assertEqual(out["diagnostics"][SCENARIOS[0]]["COMPAT_H1"]["status"], "INVALID")
        self.assertFalse(out["logical_proposal"]["tests"]["COMPAT_H1"]["complete"])

    def test_cross_scenario_minimum_fails(self):
        b = make(FixtureVerifier()); bundles = populated(b, contexts())
        bundles[SCENARIOS[0]]["models"]["H1_TGL"]["binding"]["scenario_id"] = SCENARIOS[1]
        with self.assertRaisesRegex(bridge.BridgeError, "MINIMUM_IDENTITY"):
            reduce(b, bundles)

    def test_historical_inverted_model_label_fails(self):
        b = make(FixtureVerifier()); bundles = populated(b, contexts())
        bundles[SCENARIOS[0]]["models"]["H1_TGL"]["binding"]["model_id"] = "H1_LCDM"
        with self.assertRaisesRegex(bridge.BridgeError, "MINIMUM_IDENTITY"):
            reduce(b, bundles)

    def test_family_order_cannot_change(self):
        ctxs = contexts(); first = SCENARIOS[0]; val = ctxs.pop(first); ctxs[first] = val
        with self.assertRaisesRegex(bridge.BridgeError, "ORDERED_CONTEXTS"):
            make().contexts(ctxs)

    def test_missing_inclusion_keeps_law_unavailable(self):
        b = make(FixtureVerifier()); bundles = populated(b, contexts())
        for row in bundles.values():
            row["hypotheses"]["LAW_H1_VS_FREE"]["inclusion"] = hashlib.sha256(b"missing").hexdigest()
        out = reduce(b, bundles)
        self.assertFalse(out["logical_proposal"]["tests"]["LAW_H1_VS_FREE"]["complete"])
        self.assertTrue(out["logical_proposal"]["tests"]["COMPAT_H1"]["complete"])

    def test_unbounded_error_not_promoted(self):
        b = make(FixtureVerifier()); bundles = populated(b, contexts())
        for row in bundles.values():
            row["models"]["H1_TGL"]["error_status"] = "UNAVAILABLE"
        out = reduce(b, bundles)
        self.assertFalse(out["logical_proposal"]["tests"]["COMPAT_H1"]["complete"])

    def test_wrong_proof_bytes_fails(self):
        b = make(FixtureVerifier()); ctxs = contexts()
        with self.assertRaisesRegex(bridge.BridgeError, "PROOF_BYTES_PIN"):
            b.verify("MINIMUM_BOUNDS", {}, {PIN: b"tampered"})

    def test_estimate_cannot_be_used_as_minimum_certificate(self):
        b = make(FixtureVerifier()); bundles = empty_bundles()
        bundles[SCENARIOS[0]]["models"]["H1_TGL"] = {"q_feasible_estimate": 0.0}
        with self.assertRaisesRegex(bridge.BridgeError, "MINIMUM_SCHEMA"):
            reduce(b, bundles)

    def test_analytical_zero_does_not_certify_upper(self):
        b = make(FixtureVerifier()); ctxs = contexts()
        cert = populated(b, ctxs)[SCENARIOS[0]]["models"]["H1_TGL"]
        cert["error_status"] = "ANALYTIC_NONNEGATIVITY"
        with self.assertRaisesRegex(bridge.BridgeError, "NOT_NUMERICAL_WITNESS"):
            b._minimum(cert, b.binding(SCENARIOS[0], CTX, model="H1_TGL"), {PIN: RAW})

    def test_cooperative_deadline_fails(self):
        with self.assertRaisesRegex(bridge.BridgeError, "DEADLINE"):
            make(clock=lambda: 100.0)

    def test_log_transport_exact_dyadic_and_outward(self):
        from fractions import Fraction
        for k in (0, 1, 24, 25, 100):
            out = bridge.conservative_log_bound(rational(1, 2**k))
            self.assertEqual(out["dyadic_k_diagnostic"], k)
            exact = Fraction(int(out["log_upper_rational"]["numerator"]),
                             int(out["log_upper_rational"]["denominator"]))
            self.assertGreaterEqual(Fraction(*out["log_p_upper"].as_integer_ratio()), exact)

    def test_non_power_probability_coarsening(self):
        out = bridge.conservative_log_bound(rational(3, 8))
        self.assertEqual(out["dyadic_k_diagnostic"], 1)
        self.assertFalse(out["threshold_certified"])

    def test_no_double_fwer_through_real_tail_and_reducer(self):
        b = make(FixtureVerifier()); bundles = populated(b, contexts())
        row = bundles[SCENARIOS[0]]
        row["models"]["H1_TGL"].update(lower=rational(100), upper=rational(100))
        row["hypotheses"]["COMPAT_H1"]["degree"] = 1
        out = reduce(b, bundles)
        test = out["logical_proposal"]["tests"]["COMPAT_H1"]
        one = out["records"]["COMPAT_H1"][SCENARIOS[0]]["log_p_upper"]
        import math
        self.assertEqual(test["scenarios"][SCENARIOS[0]]["log_p_FWER"], min(0.0, one+math.log(5)))
        self.assertIsNone(out["scientific_decision"])

    def threshold_inputs(self, probability):
        from fractions import Fraction
        log = bridge.conservative_log_bound(bridge.encoded(probability))
        records, bindings = {}, {}
        for test in TESTS:
            records[test] = {}
            for sid in SCENARIOS:
                direction = test in TESTS[2:]
                records[test][sid] = {
                    "statistic": 1.0, "statistic_available": True, "statistic_valid": True,
                    "calibration_status": "VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND",
                    "calibration_scope": "SYNTHETIC_TEST_ONLY", "log_p_upper": log["log_p_upper"],
                    "numerical_certificate": {"id": "fixture", "sha256": PIN},
                    "calibration_reference": {"id": "fixture", "sha256": PIN},
                    "direction_positive_certified": direction,
                    "direction_reference": {"id":"fixture", "sha256":PIN} if direction else None}
                bindings[test+":"+sid] = {"log": log, "lower": Fraction(1)}
        proposed = MODULES["reducer"].evaluate_decisions(records, scenario_ids=SCENARIOS,
            readiness=dict(data_released=True,v1_ratified=True,integrity_valid=True,common_support_valid=True),
            contract_sha256=MODEL_SHA256)
        return records, bindings, proposed

    def test_rational_alpha_interval_and_both_threshold_sides(self):
        from fractions import Fraction
        audit = bridge.threshold_audit
        lo, hi = audit.alpha_interval()
        self.assertLess(hi-lo, Fraction(1,10**69))
        self.assertLess(Fraction(5,2**25),lo)
        self.assertLess(hi,Fraction(5,2**24))
        # Separation 1e-18 in raw p: near the decision threshold but well
        # outside both enclosure width and float-transport uncertainty.
        scale = 10**18
        k = (lo*scale/5).numerator // (lo*scale/5).denominator
        for p, expected in ((Fraction(k-1,scale),True),(Fraction(k+2,scale),False)):
            records, bindings, proposal = self.threshold_inputs(p)
            exact = audit.audit(records, bindings, proposal)
            self.assertIs(exact["tests"]["COMPAT_H1"]["reject"], expected)

    def test_alpha_crossing_is_explicit_unavailable(self):
        from fractions import Fraction
        audit = bridge.threshold_audit
        lo, hi = audit.alpha_interval()
        with self.assertRaisesRegex(audit.AuditUnavailable, "INTERVAL_CROSSED"):
            audit.rejection((lo+hi)/2,(lo,hi))

    def test_deliberate_reducer_boolean_mismatch_is_rejected(self):
        from fractions import Fraction
        records, bindings, proposed = self.threshold_inputs(Fraction(1,10**9))
        proposed["tests"]["COMPAT_H1"]["reject"] = False
        with self.assertRaisesRegex(bridge.threshold_audit.AuditUnavailable, "ROBUST"):
            bridge.threshold_audit.audit(records,bindings,proposed)

    def test_finite_q_with_failure_status_or_log_is_rejected(self):
        for field, value in (("status","COMPUTATIONAL_FAILURE"),("log_profile_deta",{"$float":"-inf"})):
            first = next(profile_rows())
            payload = json.loads(first[2])
            payload["models"]["H1_TGL"][field] = value
            raw = bridge.canonical(payload)
            row = (*first[:2],raw,hashlib.sha256(raw).hexdigest(),*first[4:])
            with self.assertRaises(bridge.BridgeError):
                make().estimate_family(iter([row]),contexts=contexts(),level=1,max_records=16200)


    def test_object_verifier_valid_receipt_after_deadline_is_rejected(self):
        current = [0.0]
        calls = [0]
        def late_object_verifier(modules, pins):
            receipt = object_verifier(modules, pins)
            calls[0] += 1
            if calls[0] == 2:
                current[0] = 100.0
            return receipt
        b = bridge.Bridge(modules=MODULES, object_verifier=late_object_verifier,
            object_verifier_sha256=PIN, deadline=100.0, clock=lambda: current[0])
        # The same _objects path guards final estimate_family publication.
        # No sleep, full profile rerun, solver or real deadline consumption.
        with self.assertRaisesRegex(bridge.BridgeError, "COOPERATIVE_DEADLINE"):
            b._objects()
        self.assertEqual(calls[0], 2)


if __name__ == "__main__":
    unittest.main()
