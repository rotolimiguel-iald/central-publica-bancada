"""Focused contract and optional local WSL integration tests for V3."""

from __future__ import annotations

import hashlib
import math
import os
from pathlib import Path
import queue
import sys
import unittest
from unittest.mock import patch


BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
import cosmology_v3_bridge as bridge


PARAMETERS = {"H0": 67.4, "omega_m": 0.315, "rd_mpc": 147.09,
              "w0": -1.0, "wa": 0.0, "redshift": 0.5}


class ContractTests(unittest.TestCase):
    def test_pinned_scientific_copy_and_loaded_hashes(self):
        self.assertEqual(hashlib.sha256(bridge.SOURCE.read_bytes()).hexdigest(), bridge.SOURCE_SHA256)
        self.assertEqual(bridge._LOADED_WORKER_SHA256,
                         hashlib.sha256(bridge.WORKER.read_bytes()).hexdigest())
        self.assertEqual(bridge._LOADED_BRIDGE_SHA256,
                         hashlib.sha256(Path(bridge.__file__).read_bytes()).hexdigest())

    def test_nonfinite_invalid_and_unsupported_inputs_fail_before_dispatch(self):
        cases = [({**PARAMETERS, "H0": float("nan")}, "zero", None),
                 ({**PARAMETERS, "omega_m": float("inf")}, "zero", None),
                 ({**PARAMETERS, "w0": -0.9}, "fixed", None),
                 ({**PARAMETERS, "wa": 0.01}, "fixed", None),
                 ({**PARAMETERS, "redshift": 0.0}, "fixed", None),
                 (PARAMETERS, "other", None),
                 (PARAMETERS, "zero", [0.1, float("nan")]),
                 (PARAMETERS, "zero", [3.01])]
        with patch.object(bridge._SESSION, "exchange", side_effect=AssertionError("dispatched")):
            for params, mode, zs in cases:
                result = bridge.evaluate_background(params, mode, zs)
                self.assertEqual(result["status"], "error")
                self.assertEqual(result["error"]["code"], "ValueError")

    def test_beta_formula_and_exact_redshift_order_sent_to_worker(self):
        captured = []
        def fake_exchange(request):
            captured.append(request)
            return {"status": "ok", "series": [], "cursor": {}, "distances": [],
                    "quadrature": {}, "details": {}, "source_hashes": {}}
        with patch.object(bridge._SESSION, "exchange", side_effect=fake_exchange):
            result = bridge.evaluate_background(PARAMETERS, "fixed", [0.0, 1.5, 0.5, 1.5, 3.0])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(captured[0]["redshifts"], [0.0, 1.5, 0.5, 1.5, 3.0])
        self.assertEqual(captured[0]["model_id"], "TGL_V3_TOTAL_FIXED_BETA")
        self.assertEqual(captured[0]["beta"], bridge.ALPHA_FINE_CODATA_2018 * math.sqrt(math.e))
        self.assertEqual(result["source_hashes"]["bridge_sha256"], bridge._LOADED_BRIDGE_SHA256)

    def test_source_change_rejected_before_worker_start(self):
        session = bridge._Session()
        real_sha = bridge._sha
        def altered(path):
            return "0" * 64 if path == bridge.SOURCE else real_sha(path)
        with patch.object(bridge, "_sha", side_effect=altered):
            with self.assertRaisesRegex(RuntimeError, "source changed"):
                session._start()

    def test_timeout_marks_delivery_uncertain_without_replay(self):
        session = bridge._Session()
        class FakeInput:
            writes = 0
            def write(self, line):
                self.writes += 1
            def flush(self):
                pass
        class FakeProcess:
            stdin = FakeInput()
            def kill(self):
                pass
            def wait(self, timeout):
                return 0
        fake = FakeProcess()
        session.process = fake
        session.replies = queue.Queue()
        request = {"parameters": PARAMETERS, "beta_mode": "zero", "redshifts": [0.5]}
        with patch.object(session, "_start"), patch.object(bridge, "TIMEOUT_SECONDS", 0.001):
            with self.assertRaises(TimeoutError):
                session.exchange(request)
            with self.assertRaisesRegex(RuntimeError, "no automatic retry"):
                session.exchange(request)
        self.assertEqual(fake.stdin.writes, 1)


@unittest.skipUnless(os.environ.get("RUN_COSMOLOGY_V3_WSL") == "1",
                     "set RUN_COSMOLOGY_V3_WSL=1 for local WSL integration")
class WslIntegrationTests(unittest.TestCase):
    def test_zero_matches_independent_radiation_lcdm_quadrature(self):
        z = 1.2
        result = bridge.evaluate_background(PARAMETERS, "zero", [z, 0.0])
        self.assertEqual(result["status"], "ok", result.get("error"))
        point = result["distances"][0]
        omega_r = result["details"]["omega_r"]
        omega_m = PARAMETERS["omega_m"]
        omega_l = 1.0 - omega_m - omega_r
        def e(zz):
            return math.sqrt(omega_r * (1 + zz)**4 + omega_m * (1 + zz)**3 + omega_l)
        n = 8192
        h = z / n
        integ = (1 / e(0.0) + 1 / e(z) +
                 4 * sum(1 / e(i*h) for i in range(1, n, 2)) +
                 2 * sum(1 / e(i*h) for i in range(2, n, 2))) * h / 3
        dm = 299792.458 / PARAMETERS["H0"] * integ
        dh = 299792.458 / (PARAMETERS["H0"] * e(z))
        self.assertLess(abs(point["dm_mpc"] / dm - 1), 2e-6)
        self.assertLess(abs(point["dh_mpc"] / dh - 1), 2e-6)
        self.assertAlmostEqual(point["dm_over_rd"], point["dm_mpc"] / PARAMETERS["rd_mpc"])
        self.assertEqual(result["distances"][1]["dm_mpc"], 0.0)
        self.assertEqual(len(result["series"]), 121)
        self.assertEqual(result["series"][0]["z"], 0.0)
        self.assertEqual(result["series"][-1]["z"], 3.0)
        self.assertLess(result["quadrature"]["cursor_dm_relative_delta"], 1e-7)
        self.assertLess(result["quadrature"]["e0_residual"], 5e-6)
        self.assertLess(result["quadrature"]["max_relative_second_friedmann_residual"], 1e-3)

    def test_fixed_differs_from_zero_and_cursor_move_hits_last_cache(self):
        zs = [0.20, 0.51, 0.706, 0.93, 1.32, 1.49, 2.33]
        zero = bridge.evaluate_background(PARAMETERS, "zero", zs)
        fixed = bridge.evaluate_background(PARAMETERS, "fixed", zs)
        moved = bridge.evaluate_background({**PARAMETERS, "redshift": 1.0}, "fixed", zs)
        self.assertEqual(zero["status"], fixed["status"])
        self.assertEqual(fixed["status"], moved["status"])
        self.assertEqual(fixed["details"]["model_id"], "TGL_V3_TOTAL_FIXED_BETA")
        self.assertGreater(abs(fixed["distances"][3]["dm_mpc"] -
                               zero["distances"][3]["dm_mpc"]), 1.0)
        self.assertEqual([v["z"] for v in moved["distances"]], zs)
        self.assertTrue(moved["details"]["background_cache_hit"])
        self.assertEqual(fixed["details"]["background_builds"],
                         moved["details"]["background_builds"])
        self.assertEqual(fixed["source_hashes"], moved["source_hashes"])
        self.assertLess(moved["elapsed_ms"], 60000)


if __name__ == "__main__":
    unittest.main()
