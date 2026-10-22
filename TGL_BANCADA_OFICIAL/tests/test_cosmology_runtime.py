"""Quantitative checks for the read-only cosmology explorer (stdlib runner)."""

from __future__ import annotations

import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cosmology_runtime as runtime


class CosmologyRuntimeTests(unittest.TestCase):
    def test_official_pair_and_schema(self):
        result = runtime.overview()
        self.assertEqual(result["status"], "ok")
        data = result["dataset"]
        self.assertEqual(data["n_points"], 13)
        self.assertEqual(data["n_distinct_redshifts"], 7)
        self.assertEqual(len(data["covariance"]), 13)
        self.assertTrue(all(len(row) == 13 for row in data["covariance"]))
        self.assertEqual(data["points"][0], {
            "z": 0.295, "type": "DV_over_rd", "observed": 7.94167639,
            "sigma": math.sqrt(data["covariance"][0][0]),
        })
        self.assertEqual(data["mean_sha256"], runtime.EXPECTED_SHA256[runtime.MEAN_FILE])
        self.assertEqual(data["covariance_sha256"], runtime.EXPECTED_SHA256[runtime.COV_FILE])
        self.assertIs(data["release_commit_verified"], False)
        self.assertEqual(result["memory"]["loaded_source_bytes"], 3019)
        self.assertEqual(result["memory"]["matrix_numeric_elements"], 169)
        self.assertEqual(result["memory"]["matrix_numeric_payload_bytes"], 169 * 8)
        self.assertEqual(result["memory"]["source_reads_for_load"], 2)
        self.assertEqual(result["memory"]["source_reads_since_load"], 0)
        self.assertGreaterEqual(result["elapsed_ms"], 0)

    def test_quadrature_refinement_and_analytic_matter_limit(self):
        params = runtime._parameters({"w0": -0.83, "wa": 0.37})
        params["omega_m"] = 1.0  # analytic internal check, outside UI domain
        z = 2.4
        exact = 2 * runtime.C_KM_S / params["H0"] * (1 - 1 / math.sqrt(1 + z))
        coarse = runtime._comoving_distance_mpc(z, params, intervals=64)
        refined = runtime._comoving_distance_mpc(z, params, intervals=1024)
        self.assertLess(abs(refined - exact), abs(coarse - exact))
        self.assertLess(abs(refined - exact) / exact, 1e-10)
        params["omega_m"] = 0.315
        default = runtime._comoving_distance_mpc(3.0, params, intervals=256)
        refined_cpl = runtime._comoving_distance_mpc(3.0, params, intervals=2048)
        self.assertLess(abs(default - refined_cpl) / refined_cpl, 2e-8)

    def test_full_covariance_chi2(self):
        lower = ((1.0, 0.0), (0.5, math.sqrt(0.75)))
        self.assertTrue(math.isclose(runtime._chi2([1.0, 1.0], lower), 4 / 3,
                                      rel_tol=1e-14))
        data = runtime._load_dataset()
        result = runtime.evaluate({})
        self.assertEqual(result["status"], "ok")
        residual = [row["residual"] for row in result["observations"]]
        diagonal = sum(r * r / data.covariance[i][i] for i, r in enumerate(residual))
        self.assertFalse(math.isclose(result["chi2"]["value"], diagonal, rel_tol=1e-3))
        self.assertEqual(result["chi2"]["method"], "CHOLESKY_FULL_COVARIANCE")
        self.assertEqual(result["chi2"]["status"], "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA")
        self.assertEqual(result["memory"]["source_reads_since_load"], 0)

    def test_series_cursor_and_all_observations(self):
        result = runtime.evaluate({"redshift": 0.934})
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["model"]["status"],
                         "EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION")
        self.assertEqual(len(result["series"]), 121)
        self.assertEqual(result["series"][0]["z"], 0.0)
        self.assertEqual(result["series"][-1]["z"], 3.0)
        self.assertEqual(result["cursor"]["z"], 0.934)
        self.assertLess(result["quadrature"]["cursor_dm_relative_delta"], 2e-8)
        self.assertGreaterEqual(result["elapsed_ms"], 0)
        self.assertEqual(result["residual_definition"], "predicted_minus_observed")
        self.assertTrue(math.isclose(result["cursor"]["dm_over_rd"],
                                      result["cursor"]["dm_mpc"] / result["parameters"]["rd_mpc"]))
        self.assertEqual(len(result["observations"]), 13)
        for row in result["observations"]:
            self.assertTrue(math.isclose(row["residual"], row["predicted"] - row["observed"]))
            self.assertGreater(row["sigma"], 0)

    def test_tampered_data_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name in (runtime.MEAN_FILE, runtime.COV_FILE):
                (path / name).write_bytes((runtime.DATA_DIR / name).read_bytes())
            tampered = path / runtime.COV_FILE
            tampered.write_bytes(tampered.read_bytes() + b"\n0\n")
            runtime._cached_load_dataset.cache_clear()
            try:
                with patch.object(runtime, "DATA_DIR", path):
                    result = runtime.overview()
                self.assertEqual(result["status"], "error")
                self.assertEqual(result["error"]["code"], "DATA_INTEGRITY")
                self.assertIn("SHA-256 mismatch", result["error"]["message"])
            finally:
                runtime._cached_load_dataset.cache_clear()

    def test_warm_cache_survives_removal_of_temporary_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for name in (runtime.MEAN_FILE, runtime.COV_FILE):
                (path / name).write_bytes((runtime.DATA_DIR / name).read_bytes())
            runtime._cached_load_dataset.cache_clear()
            try:
                with patch.object(runtime, "DATA_DIR", path):
                    first = runtime.evaluate({"redshift": 1.321})
                    self.assertEqual(first["status"], "ok")
                    self.assertEqual(first["memory"]["source_reads_for_load"], 2)
                    before = first["memory"]["source_reads_total"]
                    (path / runtime.MEAN_FILE).unlink()
                    (path / runtime.COV_FILE).unlink()
                    second = runtime.evaluate({"redshift": 1.321})
                self.assertEqual(second["status"], "ok")
                self.assertEqual(second["memory"]["load_id"], first["memory"]["load_id"])
                self.assertEqual(second["memory"]["source_reads_total"], before)
                self.assertEqual(second["memory"]["source_reads_since_load"], 0)
                self.assertEqual(second["chi2"]["value"], first["chi2"]["value"])
            finally:
                runtime._cached_load_dataset.cache_clear()

    def test_nonfinite_and_out_of_range_input(self):
        for payload in ({"H0": math.nan}, {"omega_m": math.inf},
                        {"rd_mpc": -math.inf}, {"H0": 10**400}, {"redshift": 0.0},
                        {"omega_m": 0.7}, {"w0": True}, {"bad_key": 1.0}, []):
            with self.subTest(payload=payload):
                result = runtime.evaluate(payload)
                self.assertEqual(result["status"], "error")
                self.assertEqual(result["error"]["code"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
