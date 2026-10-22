"""Synthetic checks of the new F3.4 binding; observed data remain closed."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import f9_reader_gate_v1x_f34 as gate
import f9_runner_v1x_preflight_f34 as pre
import f9_runner_v1x_staged_f34 as run
import f9_runner_v1x_staged_r4 as old_run


HERE = Path(__file__).resolve().parent
F31 = HERE.parent / "F3.1"
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_F34_20261008.json"
OLD_BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R4_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
SOURCE_ROOT = HERE.parents[1] / "ORDEM_018"
SCALAR = F31 / "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json"
SPEC_SHA = "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"
OLD_SPEC_SHA = "d6b6486b8a761028ec6f839ff6cd04fea49693eb5d0c2d39c62feb9ca345ea31"
FUNCTION_SHA = "98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(path: Path = BINDING) -> dict:
    return gate.verify_v1x_binding(
        path, expected_binding_sha256=sha(path),
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
    )


class F34BindingTests(unittest.TestCase):
    def test_projection_and_function_pins(self) -> None:
        record = verify()
        self.assertEqual(record["draft_v2_sha256"], sha(SCALAR))
        self.assertEqual(record["spec_sha256"], SPEC_SHA)
        spec = record["spec_snapshot"]
        self.assertEqual(spec["f34_duas_testemunhas"]["quadro_f34"],
                         {"status": "FECHADA", "evento": 462})
        self.assertEqual(hashlib.sha256(spec["funcao_de_veredito"]["fonte"].encode()).hexdigest(),
                         FUNCTION_SHA)
        self.assertFalse(record["v2_frozen"])
        self.assertEqual(record["source_admission"], "OPEN")

    def test_old_r4_binding_refused(self) -> None:
        with self.assertRaisesRegex(gate.ReaderGateError, "F3.4 projection pin differs"):
            gate.verify_v1x_binding(
                OLD_BINDING, expected_binding_sha256=sha(OLD_BINDING),
                allowed_source_root=SOURCE_ROOT,
                expected_spec_sha256=OLD_SPEC_SHA,
            )

    def test_false_no_pooling_decision_refused(self) -> None:
        binding = json.loads(BINDING.read_bytes())
        binding["f34_decision"]["no_pooling"] = False
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tampered_binding.json"
            path.write_text(json.dumps(binding, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(gate.ReaderGateError, "F3.4 decision binding differs"):
                verify(path)

    def test_documentary_preflight_has_no_admission(self) -> None:
        record = pre.prepare_v1x(
            BINDING, expected_binding_sha256=sha(BINDING),
            allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
        )
        self.assertEqual(record["spec_governance"], "F3_4_RESOLVED_TWO_WITNESSES")
        self.assertEqual(record["n_alvos_declarados"], 2)
        self.assertEqual(record["operator_admission"], "PENDING_D_H")
        self.assertFalse(record["data_opened"])
        self.assertIsNone(record["verdict"])

    def test_synthetic_statistics_equal_r4_and_no_real_verdict(self) -> None:
        fresh = run.run_synthetic(
            BINDING, sha(BINDING), SOURCE_ROOT, SPEC_SHA,
            FIXTURE, sha(FIXTURE), mode="synthetic_only",
        )
        old = old_run.run_synthetic(
            OLD_BINDING, sha(OLD_BINDING), SOURCE_ROOT, OLD_SPEC_SHA,
            FIXTURE, sha(FIXTURE), mode="synthetic_only",
        )
        for field in ("scale", "covariance_boxes", "synthetic_statistics",
                      "synthetic_proposed_rule_output", "primary_rule1_if_applied"):
            self.assertEqual(fresh[field], old[field], field)
        self.assertEqual(fresh["spec_governance"], "F3_4_RESOLVED_TWO_WITNESSES")
        self.assertEqual(fresh["synthetic_proposed_rule_output"]["function_sha256"], FUNCTION_SHA)
        self.assertFalse(fresh["data_opened"])
        self.assertFalse(fresh["v2_frozen"])
        self.assertIsNone(fresh["verdict"])

    def test_real_mode_refused_before_documentary_read(self) -> None:
        missing = HERE / "NAO_EXISTE_F34_real.json"
        self.assertFalse(missing.exists())
        with self.assertRaisesRegex(gate.ReaderGateError, "mode refused before documentary reading"):
            run.run_synthetic(
                missing, "0" * 64, missing, SPEC_SHA,
                missing, "0" * 64, mode="real",
            )


if __name__ == "__main__":
    unittest.main()
