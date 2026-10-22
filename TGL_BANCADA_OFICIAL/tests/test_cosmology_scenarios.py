"""Persistence tests with synthetic backend receipts and temporary databases."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import types
import unittest
from unittest import mock
import uuid


ROOT = Path(__file__).resolve().parents[1]


def load_store():
    spec = importlib.util.spec_from_file_location("_scenario_store_test", ROOT / "cosmology_scenarios.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CosmologyScenarioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / "state" / "scenarios.sqlite3"
        self.store = load_store()
        self.runtime = types.ModuleType("cosmology_runtime")
        engine = self.root / "fixture_runtime.py"
        engine.write_bytes(b"# Synthetic fixture: never executed.\n")
        self.runtime.__file__ = str(engine)
        self.runtime.ENGINE_SHA256 = hashlib.sha256(engine.read_bytes()).hexdigest()
        self.runtime.MEAN_FILE, self.runtime.COV_FILE = "mean.txt", "cov.txt"
        self.runtime.EXPECTED_SHA256 = {}
        for name, content in (("mean.txt", b"synthetic mean\n"), ("cov.txt", b"synthetic covariance\n")):
            path = self.root / name
            path.write_bytes(content)
            self.runtime.EXPECTED_SHA256[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        model = {"id": "TEST_BACKGROUND", "status": "TEST_ONLY_NOT_SCIENCE"}
        points = [{"z": z, "type": "DM_over_rd", "observed": 10.0, "sigma": 1.0} for z in (0.5, 1.0)]
        self.overview = {
            "schema_version": "cosmology_background_v1", "status": "ok", "model": model,
            "engine_sha256": self.runtime.ENGINE_SHA256,
            "parameters": {"H0": {"min": 40, "max": 100, "default": 67.4, "unit": "km/s/Mpc"},
                           "redshift": {"min": 0.001, "max": 3, "default": 0.5, "unit": "dimensionless"}},
            "memory": {"load_id": "fixture-load", "source_reads_since_load": 0},
            "dataset": {"id": "SYNTHETIC_FIXTURE", "n_points": 2, "points": points,
                        "covariance": [[1, 0], [0, 1]], "release_commit_verified": False,
                        "mean_sha256": self.runtime.EXPECTED_SHA256["mean.txt"],
                        "covariance_sha256": self.runtime.EXPECTED_SHA256["cov.txt"]},
            "evaluation_status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA",
        }
        self.evaluation = {
            "schema_version": "cosmology_background_v1", "status": "ok", "model": model,
            "engine_sha256": self.runtime.ENGINE_SHA256,
            "parameters": {"H0": 67.4, "redshift": 0.5}, "memory": self.overview["memory"],
            "dataset_id": "SYNTHETIC_FIXTURE", "cursor": {"z": 0.5, "dm_over_rd": 11.0},
            "series": [{"z": 0, "dm_over_rd": 0}, {"z": 0.5, "dm_over_rd": 11.0}],
            "observations": [{**p, "predicted": 11.0, "residual": 1.0} for p in points],
            "residual_definition": "predicted_minus_observed", "quadrature": {"method": "SYNTHETIC"},
            "chi2": {"value": 2.0, "n_points": 2, "method": "SYNTHETIC",
                     "status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA"}, "elapsed_ms": 0.1,
        }
        self.runtime.overview = mock.Mock(side_effect=lambda: copy.deepcopy(self.overview))
        self.runtime.evaluate = mock.Mock(side_effect=AssertionError("Do not recompute science"))
        patcher = mock.patch.dict(sys.modules, {"cosmology_runtime": self.runtime, "resident_bridge": None})
        patcher.start()
        self.addCleanup(patcher.stop)

    def save(self, label="Referência", evaluation=None):
        return self.store.save_scenario(label, self.evaluation if evaluation is None else evaluation, db_path=self.db)

    def install_components(self, missing_last=False):
        names = [Path(self.runtime.__file__).name, "cosmology_v3_bridge.py",
                 "workers/cosmology_v3_worker.py", "scientific_models/tgl_camb_worker_v3.py"]
        for name in names[1:]:
            path = self.root / name
            if missing_last and name == names[-1]:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(("# Synthetic component: " + name + "\n").encode())
        self.runtime.ENGINE_COMPONENTS = {
            name: hashlib.sha256((self.root / name).read_bytes()).hexdigest()
            if (self.root / name).is_file() else "MISSING" for name in names}
        self.sync_component_receipts()
        return names

    def sync_component_receipts(self):
        components = self.runtime.ENGINE_COMPONENTS
        self.runtime.ENGINE_GENERATION = hashlib.sha256("\n".join(
            f"{name}:{pin}" for name, pin in sorted(components.items())).encode()).hexdigest()
        for receipt in (self.overview, self.evaluation):
            receipt["engine_components"] = dict(components)
            receipt["engine_generation"] = self.runtime.ENGINE_GENERATION

    def test_restart_roundtrip_export_and_future_model(self):
        original = copy.deepcopy(self.evaluation)
        summary = self.save()
        future = copy.deepcopy(self.evaluation)
        future["model"] = {"id": "FUTURE_ENGINE", "status": "TEST_ONLY_NOT_SCIENCE", "version": "fixture-v2"}
        future["additional_outputs"] = {"preserved": [1, 2, 3]}
        second = self.save(evaluation=future)
        restarted = load_store()
        # Historical reads must not load the runtime or depend on current data.
        with mock.patch.dict(sys.modules, {"cosmology_runtime": None}):
            rows = restarted.list_scenarios(db_path=self.db)
            full = restarted.get_scenario(summary["id"], db_path=self.db)
            self.assertEqual(rows, [second, summary])
            self.assertEqual(restarted.get_scenario(second["id"], db_path=self.db)["evaluation"], future)
        self.assertEqual(full["evaluation"], original)
        self.assertEqual(self.evaluation, original)
        self.assertEqual(full["overview"], self.overview)
        self.assertEqual(full["inputs"], original["parameters"])
        self.assertTrue(full["created_at_utc"].endswith("Z"))
        digest = full.pop("sha256")
        encoded = json.dumps(full, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), digest)
        self.assertEqual(full["provenance"]["engine"]["sha256"],
                         hashlib.sha256(Path(self.runtime.__file__).read_bytes()).hexdigest())
        self.assertEqual(full["provenance"]["engine"]["sha256"], full["evaluation"]["engine_sha256"])
        self.assertEqual(full["provenance"]["engine"]["hash_scope"], "INSTALLED_SOURCE_MATCHES_IMPORT_TIME_PIN")
        self.runtime.evaluate.assert_not_called()

    def test_invalid_labels_and_ids_and_missing_store(self):
        self.assertEqual(self.store.list_scenarios(db_path=self.db), [])
        self.assertFalse(self.db.exists())
        for label in (None, "", " ", "x" * 121, "x\ny", "x\x00y", "x\u202ey"):
            with self.subTest(label=label), self.assertRaises(self.store.ScenarioValidationError):
                self.save(label)
        for identifier in (None, "../cosmology_runtime.py", "C:\\file", "x' OR 1=1", str(uuid.uuid4()).upper()):
            with self.subTest(id=identifier), self.assertRaises(self.store.ScenarioValidationError):
                self.store.get_scenario(identifier, db_path=self.db)
        with self.assertRaises(self.store.ScenarioNotFoundError):
            self.store.get_scenario(str(uuid.uuid4()), db_path=self.db)
        self.assertFalse(self.db.exists())
        self.runtime.overview.assert_not_called()

    def test_reject_invalid_evaluation_without_creating_database(self):
        mutations = [
            lambda e: e.update(status="error"),
            lambda e: e.update(schema_version="other"),
            lambda e: e.pop("engine_sha256"),
            lambda e: e.update(engine_sha256=hashlib.sha256(b"different engine").hexdigest()),
            lambda e: e["parameters"].update(H0=True),
            lambda e: e["parameters"].update(H0=101),
            lambda e: e["parameters"].update(extra=1),
            lambda e: e["chi2"].update(value=-1),
            lambda e: e["chi2"].update(value=float("nan")),
            lambda e: e["chi2"].update(status="CONFIRMED"),
            lambda e: e.update(dataset_id="wrong"),
            lambda e: e["memory"].update(load_id="another-load"),
            lambda e: e["observations"][0].update(observed=99),
            lambda e: e["observations"][0].update(residual=-1),
            lambda e: e.pop("series"),
            lambda e: e["cursor"].update(z=2),
        ]
        for index, mutate in enumerate(mutations):
            evaluation = copy.deepcopy(self.evaluation)
            mutate(evaluation)
            with self.subTest(index=index), self.assertRaises(self.store.ScenarioValidationError):
                self.save(evaluation=evaluation)
        self.assertFalse(self.db.exists())

    def test_reject_mismatched_backend_pin(self):
        self.overview["dataset"]["mean_sha256"] = hashlib.sha256(b"changed fixture").hexdigest()
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "source pin mismatch"):
            self.save()
        self.assertFalse(self.db.exists())

    def test_reject_source_changed_after_import(self):
        Path(self.runtime.__file__).write_bytes(b"# Changed after import.\n")
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "differs from import-time"):
            self.save()
        self.runtime.overview.assert_not_called()
        self.assertFalse(self.db.exists())

    def test_reject_missing_invalid_or_mismatched_engine_pins(self):
        for pin in (None, "not-a-sha256", hashlib.sha256(b"other source").hexdigest()):
            with self.subTest(pin=pin), mock.patch.object(self.runtime, "ENGINE_SHA256", pin):
                with self.assertRaises(self.store.ScenarioValidationError):
                    self.save()
        del self.runtime.ENGINE_SHA256
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "missing or invalid"):
            self.save()
        self.runtime.ENGINE_SHA256 = hashlib.sha256(Path(self.runtime.__file__).read_bytes()).hexdigest()
        for pin in (None, hashlib.sha256(b"old overview").hexdigest()):
            self.overview["engine_sha256"] = pin
            with self.subTest(overview_pin=pin), self.assertRaisesRegex(
                    self.store.ScenarioValidationError, "overview engine pin mismatch"):
                self.save()
        self.assertFalse(self.db.exists())

    def test_reject_source_changed_during_snapshot(self):
        def changed_overview():
            Path(self.runtime.__file__).write_bytes(b"# Changed during overview.\n")
            return copy.deepcopy(self.overview)
        self.runtime.overview.side_effect = changed_overview
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "changed during snapshot"):
            self.save()
        self.assertFalse(self.db.exists())

    def test_component_generation_snapshot_and_missing_component(self):
        self.install_components(missing_last=True)
        summary = self.save()
        record = self.store.get_scenario(summary["id"], db_path=self.db)
        engine = record["provenance"]["engine"]
        self.assertEqual(engine["components"], self.runtime.ENGINE_COMPONENTS)
        self.assertEqual(engine["generation"], self.runtime.ENGINE_GENERATION)
        self.assertEqual(engine["hash_scope"], "INSTALLED_COMPONENTS_MATCH_IMPORT_TIME_PINS")
        self.runtime.evaluate.assert_not_called()

    def test_dependency_changed_before_or_during_context(self):
        names = self.install_components()
        dependency = self.root / names[2]
        original = dependency.read_bytes()
        dependency.write_bytes(b"# Hot edit before context\n")
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "engine component changed"):
            self.save()
        self.runtime.overview.assert_not_called()
        dependency.write_bytes(original)

        def changed_overview():
            dependency.write_bytes(b"# Hot edit during context\n")
            return copy.deepcopy(self.overview)
        self.runtime.overview.side_effect = changed_overview
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "engine component changed"):
            self.save()
        self.assertFalse(self.db.exists())

    def test_missing_dependency_appearing_is_refused(self):
        names = self.install_components(missing_last=True)
        dependency = self.root / names[-1]
        dependency.parent.mkdir(parents=True)
        dependency.write_bytes(b"# Appeared after import\n")
        with self.assertRaisesRegex(self.store.ScenarioValidationError, "MISSING engine component appeared"):
            self.save()
        self.assertFalse(self.db.exists())

    def test_component_path_escape_is_refused(self):
        self.install_components()
        original = dict(self.runtime.ENGINE_COMPONENTS)
        for name in ("../outside.py", "/outside.py", "C:/outside.py", "workers/../outside.py",
                     "workers\\outside.py", "workers//outside.py"):
            self.runtime.ENGINE_COMPONENTS = {**original, name: "MISSING"}
            self.sync_component_receipts()
            with self.subTest(name=name), self.assertRaisesRegex(
                    self.store.ScenarioValidationError, "unsafe engine component path"):
                self.save()
        self.assertFalse(self.db.exists())

    def test_generation_and_component_receipt_mismatches_are_refused(self):
        self.install_components()
        wrong = hashlib.sha256(b"other generation").hexdigest()
        with mock.patch.object(self.runtime, "ENGINE_GENERATION", wrong):
            with self.assertRaisesRegex(self.store.ScenarioValidationError, "runtime engine generation mismatch"):
                self.save()
        for receipt_name in ("overview", "evaluation"):
            receipt = getattr(self, receipt_name)
            for key, value in (("engine_generation", None), ("engine_generation", wrong),
                               ("engine_components", {})):
                original = receipt[key]
                receipt[key] = value
                with self.subTest(receipt=receipt_name, key=key), self.assertRaises(
                        self.store.ScenarioValidationError):
                    self.save()
                receipt[key] = original
        self.assertFalse(self.db.exists())

    def test_append_only_and_corruption_refused_for_get_and_list(self):
        summary = self.save()
        connection = sqlite3.connect(self.db)
        try:
            for query in ("UPDATE scenarios SET record_json='{}'", "DELETE FROM scenarios"):
                with self.assertRaisesRegex(sqlite3.IntegrityError, "append-only"):
                    connection.execute(query)
                connection.rollback()
            # Simulate corruption outside the API by explicitly removing the guard.
            connection.execute("DROP TRIGGER scenarios_no_update")
            connection.execute("UPDATE scenarios SET record_json='{}'")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaises(self.store.ScenarioIntegrityError):
            self.store.get_scenario(summary["id"], db_path=self.db)
        with self.assertRaises(self.store.ScenarioIntegrityError):
            self.store.list_scenarios(db_path=self.db)

    def test_concurrent_saves_do_not_overwrite_identical_labels(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            summaries = list(pool.map(lambda _: self.save("Mesmo rótulo"), range(8)))
        self.assertEqual(len({row["id"] for row in summaries}), 8)
        self.assertEqual(len(self.store.list_scenarios(db_path=self.db)), 8)


if __name__ == "__main__":
    unittest.main()
