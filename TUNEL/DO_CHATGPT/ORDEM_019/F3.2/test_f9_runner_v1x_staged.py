"""Synthetic-only checks of the staged Fase 9 V1.x statistical runner."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import f9_runner_v1x_staged as runner


HERE = Path(__file__).resolve().parent
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R2_20261008.json"
RECEIPT = HERE / "RESULTADO_GATE_V1X_R2_20261008.json"


class StagedRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        cls.binding_pin = receipt["artifacts"][BINDING.name]["sha256"]
        cls.spec_pin = receipt["spec_sha256"]

    def run_stage(self, *, mode="synthetic_only", fixture=FIXTURE, fixture_pin=None):
        return runner.run_synthetic(
            BINDING, self.binding_pin, SOURCE_ROOT, self.spec_pin,
            fixture, fixture_pin or runner.PINNED_FIXTURE_SHA256, mode=mode)

    def test_reviewed_fixture_bytes_are_hard_pinned(self):
        self.assertEqual(hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
                         runner.PINNED_FIXTURE_SHA256)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(fixture["center"], 50.0)
        self.assertEqual(fixture["primary_offsets"], [0.7, -0.4, 0.2, -0.1, 1.0])

    def test_synthetic_stage_and_covariance_adverse_endpoints(self):
        result = self.run_stage()
        self.assertEqual(result["stage"], "SYNTHETIC_STATISTICAL_REHEARSAL_ONLY")
        self.assertIsNone(result["verdict"])
        self.assertFalse(result["v2_frozen"])
        self.assertFalse(result["data_opened"])
        self.assertEqual(result["n_alvos_declarados_primary"], 0)
        self.assertEqual(result["n_alvos_declarados_inventory"], 2)
        self.assertIn("um.py not reread", result["scale"]["alpha_provenance"])
        primary = result["covariance_boxes"]["P_primaria"]
        self.assertEqual(primary["accepted"], 441)
        self.assertAlmostEqual(primary["minimum"]["sigma_comb"], 0.8034568044326528, places=11)
        self.assertAlmostEqual(primary["maximum"]["sigma_comb"], 0.9492872124413783, places=11)
        self.assertEqual(primary["maximum"]["negative_weights"], ["L3_sbf"])
        self.assertAlmostEqual(primary["maximum"]["power_only_sigma"]["BG1"], 5.721774587340219, places=10)
        self.assertGreater(primary["minimum"]["power_only_sigma"]["BG1"],
                           primary["maximum"]["power_only_sigma"]["BG1"])
        self.assertNotIn("L4_masers_6", primary["minimum"]["gls_weights"])
        self.assertGreaterEqual(result["synthetic_statistics"]["minimum"]["p_dispersion"], 0)
        self.assertLessEqual(result["synthetic_statistics"]["minimum"]["p_dispersion"], 1)
        self.assertGreaterEqual(result["synthetic_statistics"]["maximum"]["p_dispersion"], 0)
        self.assertLessEqual(result["synthetic_statistics"]["maximum"]["p_dispersion"], 1)
        self.assertEqual(result["synthetic_statistics"]["maximum"]["lnB_TGL_free_background"],
                         "NOT_IMPLEMENTED_REQUIRES_BANCADA_MOTOR")

    def test_synthetic_profile_and_quadrature(self):
        result = self.run_stage()
        for side in ("minimum", "maximum"):
            stats = result["synthetic_statistics"][side]
            self.assertIsNotNone(stats["z_delta_profile_logdet"])
            self.assertGreater(stats["beta_profile_minus"], 0)
            self.assertGreater(stats["beta_profile_plus"], 0)
            self.assertLess(stats["lnB_beta_quadrature_abs_diff"], 1e-9)
            self.assertLess(stats["lnB_shift_quadrature_abs_diff"], 1e-9)
            self.assertEqual(stats["gls"]["mean"], stats["gls"]["mean"])
        self.assertAlmostEqual(runner._ln_evidence_uniform(lambda _: 0.0, -1, 1, 100), 0.0, places=12)
        with self.assertRaises(runner.ReaderGateError):
            runner._ln_evidence_uniform(lambda _: 0.0, -1, 1, 25)

    def test_real_mode_refused_before_gate(self):
        with patch.object(runner, "verify_v1x_binding", side_effect=AssertionError("gate must not run")):
            with self.assertRaisesRegex(runner.ReaderGateError, "real or unknown mode"):
                self.run_stage(mode="real")

    def test_substituted_fixture_refused_even_with_caller_hash(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "synthetic.json"
            modified = json.loads(FIXTURE.read_text(encoding="utf-8"))
            modified["center"] = 73.04
            raw = json.dumps(modified).encode("utf-8")
            path.write_bytes(raw)
            with self.assertRaisesRegex(runner.ReaderGateError, "reviewed fixture"):
                self.run_stage(fixture=path, fixture_pin=hashlib.sha256(raw).hexdigest())

    def test_binding_hash_refusal(self):
        with self.assertRaises(runner.ReaderGateError):
            runner.run_synthetic(BINDING, "0" * 64, SOURCE_ROOT, self.spec_pin,
                                 FIXTURE, runner.PINNED_FIXTURE_SHA256)

    def test_spec_snapshot_once_and_no_reader_centers_in_statistics(self):
        real_gate = runner.verify_v1x_binding
        calls = []
        def once(*args, **kwargs):
            calls.append(1)
            return real_gate(*args, **kwargs)
        with patch.object(runner, "verify_v1x_binding", side_effect=once):
            baseline = self.run_stage()
        self.assertEqual(len(calls), 1)
        altered_gate = real_gate(BINDING, expected_binding_sha256=self.binding_pin,
                                 allowed_source_root=SOURCE_ROOT,
                                 expected_spec_sha256=self.spec_pin)
        altered_gate = copy.deepcopy(altered_gate)
        for reader in altered_gate["spec_snapshot"]["leitores"].values():
            reader["H0"] = -999.0
        with patch.object(runner, "verify_v1x_binding", return_value=altered_gate):
            altered = self.run_stage()
        self.assertEqual(baseline["synthetic_statistics"], altered["synthetic_statistics"])
        self.assertFalse(altered["observed_H0_use_this_fixture"]["used"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
