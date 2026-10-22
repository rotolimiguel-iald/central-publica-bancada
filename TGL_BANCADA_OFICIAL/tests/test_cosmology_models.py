"""Model-selector regression tests; V3 is mocked, never started or imported.

The local 13-component BAO vector and full covariance are read-only inputs.
All V3 distances below are deliberately synthetic protocol fixtures, not
scientific predictions. Each V3 evaluation must dispatch exactly once.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
V3_MODELS = (("TGL_V3_TOTAL_FIXED_BETA", "fixed"), ("V3_TOTAL_BETA_ZERO", "zero"))
FIELDS = {"DM_over_rd": "dm_over_rd", "DH_over_rd": "dh_over_rd", "DV_over_rd": "dv_over_rd"}


def quadratic_form(covariance, residual):
    """Independent pivoted Gaussian solve; do not reuse runtime Cholesky."""
    n = len(residual)
    augmented = [list(row) + [residual[i]] for i, row in enumerate(covariance)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(augmented[i][col]))
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        if divisor == 0:
            raise AssertionError("singular fixture covariance")
        augmented[col] = [v / divisor for v in augmented[col]]
        for row in range(n):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [a - factor * b for a, b in zip(augmented[row], augmented[col])]
    return sum(r * augmented[i][-1] for i, r in enumerate(residual))


class CosmologyModelTests(unittest.TestCase):
    def setUp(self):
        # Isolate import-time pins and cache from other test suites. Installing
        # this inert bridge stub prevents any real WSL/process dispatch.
        self.bridge = types.ModuleType("cosmology_v3_bridge")
        self.bridge.evaluate_background = mock.Mock(name="synthetic_v3")
        name = "_cosmology_model_selector_test"
        spec = importlib.util.spec_from_file_location(name, ROOT / "cosmology_runtime.py")
        self.runtime = importlib.util.module_from_spec(spec)
        modules = mock.patch.dict(sys.modules, {
            name: self.runtime, "cosmology_v3_bridge": self.bridge, "resident_bridge": None})
        modules.start()
        self.addCleanup(modules.stop)
        spec.loader.exec_module(self.runtime)
        self.data = self.runtime._load_dataset()
        self.parameters = {key: rule[2] for key, rule in self.runtime.PARAMETERS.items()}
        self.redshifts = sorted({row[0] for row in self.data.points})
        self.assertEqual(len(self.data.points), 13)
        self.assertEqual(len(self.redshifts), 7)

    def point(self, z, dm=None, dh=None):
        """Synthetic positive distances with consistent Mpc, rd and D_V units."""
        horizon = self.runtime.C_KM_S / self.parameters["H0"]
        dm = horizon * math.log1p(z) * 1.1 if dm is None else dm
        dh = horizon / (1 + z) if dh is None else dh
        dv = (z * dm * dm * dh) ** (1 / 3) if z else 0.0
        return {"z": z, "dm_mpc": dm, "dh_mpc": dh, "dv_mpc": dv,
                "dm_over_rd": dm / self.parameters["rd_mpc"],
                "dh_over_rd": dh / self.parameters["rd_mpc"],
                "dv_over_rd": dv / self.parameters["rd_mpc"]}

    def fixture(self, model_id=V3_MODELS[0][0]):
        exact = {}
        for i, (z, kind, observed, sigma) in enumerate(self.data.points):
            row = exact.setdefault(z, self.point(z))
            mpc = (observed + sigma * (1.0 + (i % 3) * 0.2)) * self.parameters["rd_mpc"]
            if kind == "DV_over_rd":
                row["dm_mpc"] = math.sqrt(mpc ** 3 / (z * row["dh_mpc"]))
            else:
                row[{"DM_over_rd": "dm_mpc", "DH_over_rd": "dh_mpc"}[kind]] = mpc
        exact = [self.point(z, row["dm_mpc"], row["dh_mpc"]) for z, row in exact.items()]
        # Deliberately different from the exact observations, so using visual
        # interpolation in chi2 cannot accidentally pass this regression test.
        series = [self.point(i * 3.0 / 120) for i in range(121)]
        mode = "fixed" if model_id == V3_MODELS[0][0] else "zero"
        return {"status": "ok", "series": series,
                "cursor": self.point(self.parameters["redshift"]), "distances": exact,
                "quadrature": {"method": "SYNTHETIC_EXACT_Z_FIXTURE", "ngrid_pinned": 121,
                               "local_refined_points": 241, "distance_intervals_pinned": 200,
                               "cursor_refined_intervals": 400, "local_z_range": [0.0, 3.0],
                               "max_relative_e_refinement": 0.0,
                               "max_relative_second_friedmann_residual": 0.0,
                               "e0_residual": 0.0, "cursor_dm_relative_delta": 0.0,
                               "min_e2_z0_to_3": 1.0},
                "details": {"fixture_only": True, "model_id": model_id, "beta_mode": mode,
                            "status": "CONDITIONAL_V3_TOTAL_FLUID_BACKGROUND_ONLY",
                            "beta": 7.2973525693e-3 * math.sqrt(math.e) if mode == "fixed" else 0.0,
                            "omega_r": 0.00009, "omega_m_effective": self.parameters["omega_m"],
                            "omega_lambda_closed": 0.68, "c": 0.0,
                            "mapping": {"ombh2": 0.0, "omch2": self.parameters["omega_m"]
                                        * (self.parameters["H0"] / 100) ** 2,
                                        "mnu_ev": 0.0, "TCMB_K": 2.7255, "Neff": 3.046,
                                        "note": "Synthetic fixture, not a prediction"},
                            "assumptions": ["Synthetic fixture only"], "background_cache_hit": False,
                            "background_builds": 1, "background_build_ms": 0.1},
                "source_hashes": {key: self.runtime.ENGINE_COMPONENTS[path] for key, path in (
                    ("scientific_model_sha256", "scientific_models/tgl_camb_worker_v3.py"),
                    ("adapter_worker_sha256", "workers/cosmology_v3_worker.py"),
                    ("bridge_sha256", "cosmology_v3_bridge.py"))}, "elapsed_ms": 0.1}

    def evaluate_v3(self, receipt, model_id=V3_MODELS[0][0], parameters=None):
        self.bridge.evaluate_background.reset_mock(return_value=True, side_effect=True)
        self.bridge.evaluate_background.return_value = copy.deepcopy(receipt)
        payload = dict(self.parameters if parameters is None else parameters, model_id=model_id)
        with mock.patch.object(self.runtime, "_distances", side_effect=AssertionError("CPL fallback")) as cpl:
            result = self.runtime.evaluate(payload)
        cpl.assert_not_called()
        return result

    def test_exact_observed_redshifts_and_full_covariance_for_both_v3_modes(self):
        for model_id, mode in V3_MODELS:
            with self.subTest(model=model_id):
                receipt = self.fixture(model_id)
                result = self.evaluate_v3(receipt, model_id)
                self.assertEqual(result["status"], "ok", result)
                self.bridge.evaluate_background.assert_called_once_with(
                    self.parameters, mode, redshifts=self.redshifts)
                self.assertEqual(result["series"], receipt["series"])
                self.assertEqual(result["cursor"], receipt["cursor"])
                self.assertEqual(result["model"]["id"], model_id)
                self.assertEqual(result["model"]["beta_mode"], mode)
                self.assertEqual(result["parameters"], self.parameters)
                self.assertNotIn("model_id", result["parameters"])
                by_z = {row["z"]: row for row in receipt["distances"]}
                residual = []
                for actual, (z, kind, observed, sigma) in zip(result["observations"], self.data.points):
                    prediction = by_z[z][FIELDS[kind]]
                    self.assertEqual(actual, {"z": z, "type": kind, "observed": observed,
                                              "sigma": sigma, "predicted": prediction,
                                              "residual": prediction - observed})
                    residual.append(prediction - observed)
                expected = quadratic_form(self.data.covariance, residual)
                diagonal = sum(r * r / self.data.covariance[i][i] for i, r in enumerate(residual))
                self.assertTrue(math.isclose(result["chi2"]["value"], expected, rel_tol=1e-12))
                self.assertFalse(math.isclose(expected, diagonal, rel_tol=1e-3))
                self.assertEqual(result["chi2"]["n_points"], 13)
                self.assertEqual(result["chi2"]["method"], "CHOLESKY_FULL_COVARIANCE")

    def test_changing_visual_curve_and_cursor_does_not_change_chi2(self):
        receipt = self.fixture()
        first = self.evaluate_v3(receipt)
        self.assertEqual(first["status"], "ok", first)
        self.bridge.evaluate_background.assert_called_once()
        changed = copy.deepcopy(receipt)
        changed["series"] = [self.point(row["z"], row["dm_mpc"] * 1.3, row["dh_mpc"])
                             for row in changed["series"]]
        changed["cursor"] = self.point(self.parameters["redshift"], 2000.0, 3000.0)
        second = self.evaluate_v3(changed)
        self.assertEqual(second["status"], "ok", second)
        self.bridge.evaluate_background.assert_called_once()
        self.assertEqual(first["chi2"], second["chi2"])
        self.assertEqual(first["observations"], second["observations"])
        self.assertNotEqual(first["series"], second["series"])

    def test_worker_errors_and_exceptions_never_fall_back_to_cpl(self):
        failures = [{"status": "error", "error": {"message": "synthetic worker failure"}},
                    {"status": "error", "error": "synthetic protocol failure"}, None,
                    {"status": "ok"}]
        for model_id, _ in V3_MODELS:
            for failure in failures:
                with self.subTest(model=model_id, failure=failure):
                    result = self.evaluate_v3(failure, model_id)
                    self.assertEqual(result["status"], "error")
                    self.assertEqual(result["error"]["code"], "V3_UNAVAILABLE")
                    self.assertNotIn("chi2", result)
                    self.bridge.evaluate_background.assert_called_once()
            for failure in (TimeoutError("synthetic timeout"), RuntimeError("synthetic crash")):
                with self.subTest(model=model_id, exception=type(failure).__name__):
                    self.bridge.evaluate_background.reset_mock()
                    self.bridge.evaluate_background.side_effect = failure
                    with mock.patch.object(self.runtime, "_distances") as cpl:
                        result = self.runtime.evaluate({**self.parameters, "model_id": model_id})
                    cpl.assert_not_called()
                    self.bridge.evaluate_background.assert_called_once()
                    self.assertEqual(result["error"]["code"], "V3_UNAVAILABLE")
                    self.bridge.evaluate_background.side_effect = None

    def test_missing_exact_z_is_never_repaired_from_visual_series(self):
        for model_id, _ in V3_MODELS:
            for near_match in (False, True):
                with self.subTest(model=model_id, near_match=near_match):
                    receipt = self.fixture(model_id)
                    lost = receipt["distances"][0]
                    missing_z = lost["z"]
                    if near_match:
                        lost["z"] = math.nextafter(missing_z, math.inf)
                    else:
                        receipt["distances"].pop(0)
                    result = self.evaluate_v3(receipt, model_id)
                    self.bridge.evaluate_background.assert_called_once()
                    self.assertEqual(result["error"]["code"], "V3_UNAVAILABLE")
                    self.assertIn("Missing exact observation redshift", result["error"]["message"])
                    self.assertNotIn("observations", result)

    def test_unknown_models_and_beta_mode_inputs_fail_before_dispatch(self):
        bad = [{"model_id": value} for value in ("unknown", "fixed", "zero", "", None, False, [], {})]
        bad += [{"model_id": V3_MODELS[0][0], "beta_mode": "zero"},
                {"model_id": V3_MODELS[0][0], "beta": 0.0}]
        with mock.patch.object(self.runtime, "_load_dataset") as load:
            for payload in bad:
                with self.subTest(payload=payload):
                    result = self.runtime.evaluate({**self.parameters, **payload})
                    self.assertEqual(result["error"]["code"], "INVALID_INPUT")
            load.assert_not_called()
        self.bridge.evaluate_background.assert_not_called()

    def test_v3_requires_lambda_values_and_supplies_all_six_numeric_parameters(self):
        invalid = ({"w0": -0.9}, {"wa": 0.01}, {"w0": None}, {"wa": False},
                   {"w0": "-1"}, {"wa": math.nan})
        for model_id, mode in V3_MODELS:
            for changed in invalid:
                with self.subTest(model=model_id, changed=changed):
                    self.bridge.evaluate_background.reset_mock()
                    result = self.runtime.evaluate({**self.parameters, **changed, "model_id": model_id})
                    self.assertEqual(result["error"]["code"], "INVALID_INPUT")
                    self.bridge.evaluate_background.assert_not_called()
            # Existing evaluate contract supplies defaults when keys are omitted.
            result = self.evaluate_v3(self.fixture(model_id), model_id, parameters={})
            self.assertEqual(result["status"], "ok")
            self.bridge.evaluate_background.assert_called_once_with(
                self.parameters, mode, redshifts=self.redshifts)
            self.assertEqual(result["parameters"]["w0"], -1)
            self.assertEqual(result["parameters"]["wa"], 0)

    def test_beta_zero_stays_on_v3_radiation_branch_not_cpl(self):
        result = self.evaluate_v3(self.fixture("V3_TOTAL_BETA_ZERO"), "V3_TOTAL_BETA_ZERO")
        model = result["model"]
        self.assertEqual(model["id"], "V3_TOTAL_BETA_ZERO")
        self.assertEqual(model["beta_mode"], "zero")
        self.assertIn("radiation+matter+Lambda", model["domain"])
        self.assertEqual(model["scope"], "BACKGROUND_ONLY_NOT_FULL_CMB_PREDICTION")
        self.assertNotEqual(model["status"], self.runtime.MODEL_STATUS)
        self.bridge.evaluate_background.assert_called_once_with(self.parameters, "zero", redshifts=self.redshifts)

    def test_cpl_remains_available_without_v3_dispatch(self):
        result = self.runtime.evaluate({**self.parameters, "model_id": "FLAT_MATTER_CPL_BACKGROUND",
                                        "w0": -0.9, "wa": 0.1})
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["model"]["id"], "FLAT_MATTER_CPL_BACKGROUND")
        self.assertEqual(result["model"]["status"], self.runtime.MODEL_STATUS)
        self.bridge.evaluate_background.assert_not_called()

    def test_engine_receipt_matches_overview_for_accepted_v3_result(self):
        overview = self.runtime.overview()
        result = self.evaluate_v3(self.fixture())
        for key in ("engine_sha256", "engine_generation", "engine_components"):
            self.assertEqual(result[key], overview[key])
        self.assertEqual(result["data_hashes"], {key: overview["dataset"][key]
                                               for key in ("mean_sha256", "covariance_sha256")})

    def assert_rejected_before_chi2(self, receipt, model_id=V3_MODELS[0][0]):
        with mock.patch.object(self.runtime, "_chi2", side_effect=AssertionError("chi2 reached")) as chi2:
            result = self.evaluate_v3(receipt, model_id)
        chi2.assert_not_called()
        self.bridge.evaluate_background.assert_called_once()
        self.assertEqual(result["status"], "error", result)
        self.assertEqual(result["error"]["code"], "V3_UNAVAILABLE", result)
        self.assertNotIn("chi2", result)
        self.assertNotIn("observations", result)
        json.dumps(result, allow_nan=False)
        return result

    def test_incomplete_success_is_rejected_before_chi2(self):
        for key in ("series", "cursor", "distances", "quadrature", "details", "source_hashes", "elapsed_ms"):
            for value in ("omit", None, []):
                with self.subTest(key=key, value=value):
                    receipt = self.fixture()
                    if value == "omit":
                        receipt.pop(key)
                    else:
                        receipt[key] = value
                    self.assert_rejected_before_chi2(receipt)
        receipt = self.fixture()
        receipt["error"] = "worker contradicted success"
        self.assert_rejected_before_chi2(receipt)

    def test_all_distance_fields_must_be_present_numeric_and_finite(self):
        keys = ("z", "dm_mpc", "dh_mpc", "dv_mpc", "dm_over_rd", "dh_over_rd", "dv_over_rd")
        for section in ("series", "cursor", "distances"):
            for key in keys:
                for value in ("omit", math.nan, math.inf, -math.inf, None, True, "1.0", 10**400):
                    with self.subTest(section=section, key=key, value=str(value)[:30]):
                        receipt = self.fixture()
                        row = receipt[section] if section == "cursor" else receipt[section][1]
                        if value == "omit":
                            row.pop(key)
                        else:
                            row[key] = value
                        self.assert_rejected_before_chi2(receipt)

    def test_grid_cursor_and_exact_redshift_identity(self):
        mutations = [
            lambda r: r["series"].pop(),
            lambda r: r["series"].append(copy.deepcopy(r["series"][-1])),
            lambda r: r["series"].reverse(),
            lambda r: r["series"][1].update(z=0.03),
            lambda r: r["cursor"].update(z=math.nextafter(self.parameters["redshift"], math.inf)),
            lambda r: r["distances"].append(copy.deepcopy(r["distances"][0])),
            lambda r: r["distances"].append(self.point(0.123)),
            lambda r: r["distances"][0].update(z=-0.1),
            lambda r: r["distances"][0].update(z=3.1),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                receipt = self.fixture()
                mutate(receipt)
                self.assert_rejected_before_chi2(receipt)
        # np.linspace and Python arithmetic can differ by a few ULPs.
        receipt = self.fixture()
        receipt["series"][3]["z"] = math.nextafter(receipt["series"][3]["z"], math.inf)
        result = self.evaluate_v3(receipt)
        self.assertEqual(result["status"], "ok", result)

    def test_distance_units_signs_and_overflow_guard(self):
        mutations = [
            lambda r: r["distances"][0].update(dm_mpc=-1),
            lambda r: r["cursor"].update(dh_mpc=0, dh_over_rd=0),
            lambda r: r["cursor"].update(dm_over_rd=r["cursor"]["dm_over_rd"] * 1000),
            lambda r: r["cursor"].update(dv_mpc=1, dv_over_rd=1 / self.parameters["rd_mpc"]),
            lambda r: r["series"][0].update(dm_mpc=1, dm_over_rd=1 / self.parameters["rd_mpc"]),
            lambda r: r["distances"][0].update(dm_mpc=1e200, dm_over_rd=1e200 / self.parameters["rd_mpc"]),
            lambda r: r["series"][0].update(dh_mpc=r["series"][0]["dh_mpc"] * 1000,
                                             dh_over_rd=r["series"][0]["dh_over_rd"] * 1000),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                receipt = self.fixture()
                mutate(receipt)
                self.assert_rejected_before_chi2(receipt)

    def test_source_hashes_must_match_each_imported_component(self):
        keys = ("scientific_model_sha256", "adapter_worker_sha256", "bridge_sha256")
        mismatch = hashlib.sha256(b"synthetic mismatched component bytes").hexdigest()
        for key in keys:
            for value in (None, "omit", "MISSING", mismatch):
                with self.subTest(key=key, value=value):
                    receipt = self.fixture()
                    if value == "omit":
                        receipt["source_hashes"].pop(key)
                    else:
                        receipt["source_hashes"][key] = value
                    result = self.assert_rejected_before_chi2(receipt)
                    self.assertIn(key, result["error"]["message"])
        receipt = self.fixture()
        path = "scientific_models/tgl_camb_worker_v3.py"
        with mock.patch.dict(self.runtime.ENGINE_COMPONENTS, {path: "MISSING"}):
            receipt["source_hashes"]["scientific_model_sha256"] = "MISSING"
            self.assert_rejected_before_chi2(receipt)

    def test_execution_metadata_complete_and_finite(self):
        for section in ("details", "quadrature"):
            for key in self.fixture()[section]:
                if key == "fixture_only":
                    continue
                with self.subTest(section=section, missing=key):
                    receipt = self.fixture()
                    receipt[section].pop(key)
                    self.assert_rejected_before_chi2(receipt)
        mutations = [
            lambda r: r["details"].update(model_id="FLAT_MATTER_CPL_BACKGROUND"),
            lambda r: r["details"].update(beta_mode="zero"),
            lambda r: r["details"].update(beta=0),
            lambda r: r["details"].update(omega_m_effective=0.49),
            lambda r: r["details"].update(background_cache_hit=1),
            lambda r: r["details"]["mapping"].update(TCMB_K=math.nan),
            lambda r: r["quadrature"].update(cursor_dm_relative_delta=math.inf),
            lambda r: r["quadrature"].update(ngrid_pinned=True),
            lambda r: r.update(elapsed_ms=-1),
            lambda r: r.update(additive_field={"nested": [math.nan]}),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                receipt = self.fixture()
                mutate(receipt)
                self.assert_rejected_before_chi2(receipt)
        receipt = self.fixture("V3_TOTAL_BETA_ZERO")
        receipt["details"]["beta"] = self.fixture()["details"]["beta"]
        self.assert_rejected_before_chi2(receipt, "V3_TOTAL_BETA_ZERO")


if __name__ == "__main__":
    unittest.main()
