"""Export regressions using existing synthetic scenario fixtures, never science."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest import mock
import uuid

from tests import test_cosmology_scenarios as fixtures


class CosmologyExportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.CosmologyScenarioTests(methodName="runTest")
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.store = self.fixture.store
        self.runtime = self.fixture.runtime
        self.store.DB_PATH = self.fixture.db
        for key, value, low, high in (("omega_m", 0.315, 0.1, 0.5), ("rd_mpc", 147.09, 120, 170),
                                      ("w0", -1.0, -1.5, -0.5), ("wa", 0.0, -1, 1)):
            self.fixture.evaluation["parameters"][key] = value
            self.fixture.overview["parameters"][key] = {"min": low, "max": high, "default": value}
        self.fixture.install_components()
        self.fixture.evaluation["data_hashes"] = {
            key: self.fixture.overview["dataset"][key] for key in ("mean_sha256", "covariance_sha256")}
        self.params = copy.deepcopy(self.fixture.evaluation["parameters"])
        modules = mock.patch.dict(sys.modules, {"cosmology_scenarios": self.store})
        modules.start()
        self.addCleanup(modules.stop)
        spec = importlib.util.spec_from_file_location("_exports_test", fixtures.ROOT / "cosmology_exports.py")
        self.exports = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.exports)
        self.exports.EXPORT_DIR = self.fixture.root / "exports"
        self.runtime.evaluate.side_effect = self.calculation

    def calculation(self, payload):
        result = copy.deepcopy(self.fixture.evaluation)
        result["parameters"] = {key: value for key, value in payload.items() if key != "model_id"}
        result["cursor"]["z"] = payload["redshift"]
        result["model"]["id"] = payload.get("model_id", self.fixture.overview["model"]["id"])
        result["chi2"]["value"] = payload["H0"]  # Synthetic output, not a cosmology calculation.
        return result

    def assert_no_export(self):
        directory = self.exports.EXPORT_DIR
        self.assertFalse(directory.exists() and any(directory.iterdir()))

    def test_scenario_roundtrip_is_historical_and_get_is_read_only(self):
        saved = self.fixture.save()
        with mock.patch.dict(sys.modules, {"cosmology_runtime": None}):
            summary = self.exports.export_scenario(saved["id"])
            file = Path(summary["path"])
            before = file.read_bytes(), file.stat().st_mtime_ns
            full = self.exports.get_export(summary["id"])
            self.assertEqual((file.read_bytes(), file.stat().st_mtime_ns), before)
        self.assertEqual(full["payload"]["scenario"]["id"], saved["id"])
        self.assertEqual(full["payload"]["scenario"]["sha256"], saved["sha256"])
        self.assertEqual(full["status"], "exploratory")
        self.assertTrue(full["created_at_utc"].endswith("Z"))
        self.assertEqual(summary["download_url"], "/api/cosmology/exports/" + summary["id"])
        self.assertEqual(file.parent, self.exports.EXPORT_DIR)
        self.assertEqual(uuid.UUID(summary["id"]).version, 4)
        digest = full.pop("sha256")
        canonical = json.dumps(full, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), digest)
        self.runtime.evaluate.assert_not_called()

    def test_comparison_recalculates_both_models_and_delta(self):
        reference = {**self.params, "model_id": "TEST_BACKGROUND"}
        current = {**self.params, "H0": 73.0, "model_id": "TEST_OTHER_MODEL"}
        summary = self.exports.export_comparison(reference, current)
        full = self.exports.get_export(summary["id"])
        self.assertEqual(self.runtime.evaluate.call_args_list, [mock.call(reference), mock.call(current)])
        payload = full["payload"]
        self.assertAlmostEqual(payload["delta_chi2"], 5.6)
        self.assertEqual(payload["delta_chi2_definition"], "current_minus_reference")
        self.assertEqual(payload["current"]["evaluation"]["model"]["id"], "TEST_OTHER_MODEL")
        self.assertNotIn("model_id", payload["current"]["evaluation"]["parameters"])
        self.assertEqual(full["engine"]["generation"], self.runtime.ENGINE_GENERATION)
        self.assertEqual(full["data_hashes"], self.fixture.evaluation["data_hashes"])
        self.assertEqual(reference["H0"], self.params["H0"])

    def test_corrupt_export_and_corrupt_scenario_are_refused(self):
        saved = self.fixture.save()
        summary = self.exports.export_scenario(saved["id"])
        path = Path(summary["path"])
        altered = json.loads(path.read_bytes())
        altered["payload"]["scenario"]["label"] = "Changed label"
        path.write_text(self.store._canonical(altered), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            self.exports.get_export(summary["id"])
        with mock.patch.object(self.store, "get_scenario", side_effect=self.store.ScenarioIntegrityError("corrupt scenario")):
            with self.assertRaisesRegex(ValueError, "corrupt scenario"):
                self.exports.export_scenario(saved["id"])
        self.assertEqual(len(list(self.exports.EXPORT_DIR.iterdir())), 1)

    def test_uuid_traversal_and_missing_get_never_write(self):
        for identifier in ("../secret", "C:/secret", "x.json", str(uuid.uuid4()).upper(), None):
            for action in (self.exports.get_export, self.exports.export_scenario):
                with self.subTest(id=identifier, action=action.__name__), self.assertRaises(ValueError):
                    action(identifier)
        with self.assertRaises(ValueError):
            self.exports.get_export(str(uuid.uuid4()))
        self.assertFalse(self.exports.EXPORT_DIR.exists())

    def test_input_evaluations_unknown_fields_and_nonfinite_are_rejected(self):
        bad = [self.fixture.evaluation, {}, {**self.params, "path": "../outside"},
               {**self.params, "H0": True}, {**self.params, "H0": float("nan")},
               {**self.params, "model_id": {}}, {**self.params, "model_id": ""}]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.exports.export_comparison(self.params, value)
        self.runtime.evaluate.assert_not_called()
        self.assert_no_export()

    def test_failed_or_mismatched_calculation_never_publishes(self):
        wrong_hash = hashlib.sha256(b"wrong pin").hexdigest()
        mutations = [
            lambda r: r.update(status="error"),
            lambda r: r["chi2"].update(value=float("nan")),
            lambda r: r["parameters"].update(H0=70.0),
            lambda r: r["model"].update(id="WRONG_MODEL"),
            lambda r: r["data_hashes"].update(mean_sha256=wrong_hash),
            lambda r: r.update(engine_generation=wrong_hash),
        ]
        for index, mutate in enumerate(mutations):
            count = 0

            def evaluate(payload):
                nonlocal count
                count += 1
                result = self.calculation(payload)
                if count == 2:
                    mutate(result)
                return result
            self.runtime.evaluate.side_effect = evaluate
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.exports.export_comparison(self.params, self.params)
            self.assert_no_export()

    def test_engine_hotchange_during_second_calculation_is_refused(self):
        count = 0

        def evaluate(payload):
            nonlocal count
            count += 1
            if count == 2:
                (self.fixture.root / "workers/cosmology_v3_worker.py").write_bytes(b"# Hot edit\n")
            return self.calculation(payload)
        self.runtime.evaluate.side_effect = evaluate
        with self.assertRaisesRegex(ValueError, "engine component changed"):
            self.exports.export_comparison(self.params, self.params)
        self.assert_no_export()

    def test_atomic_publish_failure_cleans_temporary_file(self):
        with mock.patch.object(self.exports.os, "replace", side_effect=OSError("simulated publication failure")):
            with self.assertRaisesRegex(ValueError, "publication failure"):
                self.exports.export_comparison(self.params, self.params)
        self.assert_no_export()


if __name__ == "__main__":
    unittest.main()
