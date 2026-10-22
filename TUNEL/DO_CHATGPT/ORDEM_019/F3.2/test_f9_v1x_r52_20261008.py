"""Synthetic-only tests for the additive F3.1 R5.2 / F3.2 binding."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import f9_reader_gate_v1x_r52 as gate
import f9_runner_v1x_preflight_r52 as pre
import f9_runner_v1x_staged_r52 as stage
import f9_runner_v1x_staged_f34 as previous_stage


HERE = Path(__file__).resolve().parent
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R52_20261008.json"
BASE_BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_F34_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
BINDING_SHA = "a0c098763d305308e47b40196263416b63d6b7893d555bd9618072915c3f6316"
BASE_BINDING_SHA = "19d03542ae8839d4856a44eb2291397a4c26f7760881345762d1de5e7c0854cc"
DRAFT_SHA = "6b6769da821b03dd96728202b478d3c0920b51f68cb6ca013916899390c517cd"
SPEC_SHA = "9c7f05a1821ccb88936c0190934db524f4dca1de20ab2c98c5206a4c157cbb7c"
BASE_SPEC_SHA = "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"
FUNCTION_SHA = "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5"
FIXTURE_SHA = "d9c07fd536ee4ca93956ccc06a3e8217719e1d028cd00350cd5ddb43ec2f08ff"
_record = json.loads(BINDING.read_bytes())
SOURCE_ROOT = Path(_record["draft_v2"]["path"]).parents[2] / "ORDEM_018"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(path: Path, digest: str, spec: str) -> dict:
    return gate.verify_v1x_binding(
        path, expected_binding_sha256=digest,
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=spec,
    )


def mutated_path(payload: dict) -> Path:
    with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as stream:
        stream.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        return Path(stream.name)


class R52BindingTests(unittest.TestCase):
    def test_base_pins_and_lineage(self) -> None:
        self.assertEqual(sha(BINDING), BINDING_SHA)
        self.assertEqual(sha(BASE_BINDING), BASE_BINDING_SHA)
        record = check(BINDING, BINDING_SHA, SPEC_SHA)
        self.assertEqual(record["draft_v2_sha256"], DRAFT_SHA)
        self.assertEqual(record["spec_sha256"], SPEC_SHA)
        self.assertEqual(
            hashlib.sha256(
                record["spec_snapshot"]["funcao_de_veredito"]["fonte"].encode("utf-8")
            ).hexdigest(),
            FUNCTION_SHA,
        )
        self.assertEqual(
            _record["r52_lineage"]["r51_sha256"],
            "f73bee1d8b45c43575e73bea8f4adf10724d039f1b96a50542cd7e70ae100c60",
        )
        self.assertFalse(record["v2_frozen"])
        self.assertEqual(record["source_admission"], "OPEN")

    def test_reader_bytes_and_f34_decision_unchanged(self) -> None:
        base = json.loads(BASE_BINDING.read_bytes())
        self.assertEqual(_record["readers"], base["readers"])
        self.assertEqual(_record["f34_decision"], base["f34_decision"])

    def test_independent_binding_hash_refusal(self) -> None:
        with self.assertRaisesRegex(gate.ReaderGateError, "binding hash mismatch"):
            check(BINDING, "0" * 64, SPEC_SHA)

    def test_wrong_draft_hash_refusal(self) -> None:
        payload = copy.deepcopy(_record)
        payload["draft_v2"]["sha256"] = "0" * 64
        path = mutated_path(payload)
        try:
            with self.assertRaisesRegex(gate.ReaderGateError, "V2 draft bytes/hash mismatch"):
                check(path, sha(path), SPEC_SHA)
        finally:
            path.unlink()

    def test_wrong_lineage_refusal(self) -> None:
        payload = copy.deepcopy(_record)
        payload["r52_lineage"]["r52_function_sha256"] = "0" * 64
        path = mutated_path(payload)
        try:
            with self.assertRaisesRegex(gate.ReaderGateError, "R5.2 lineage binding differs"):
                check(path, sha(path), SPEC_SHA)
        finally:
            path.unlink()

    def test_preflight_has_no_admission(self) -> None:
        record = pre.prepare_v1x(
            BINDING, expected_binding_sha256=BINDING_SHA,
            allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
        )
        self.assertFalse(record["data_opened"])
        self.assertIsNone(record["verdict"])
        self.assertEqual(record["operator_admission"], "PENDING_D_H")

    def test_synthetic_stats_and_new_verdict_pin(self) -> None:
        fresh = stage.run_synthetic(
            BINDING, BINDING_SHA, SOURCE_ROOT, SPEC_SHA,
            FIXTURE, FIXTURE_SHA, mode="synthetic_only",
        )
        historical = previous_stage.run_synthetic(
            BASE_BINDING, BASE_BINDING_SHA, SOURCE_ROOT, BASE_SPEC_SHA,
            FIXTURE, FIXTURE_SHA, mode="synthetic_only",
        )
        for field in ("scale", "covariance_boxes", "primary_rule1_if_applied"):
            self.assertEqual(fresh[field], historical[field], field)
        for family, sides in fresh["synthetic_statistics"].items():
            for side, record in sides.items():
                current = {k: v for k, v in record.items()
                           if k != "dispersion_rule_evaluation"}
                previous = {k: v for k, v in historical["synthetic_statistics"][family][side].items()
                            if k != "dispersion_rule_evaluation"}
                self.assertEqual(current, previous, (family, side))
        self.assertEqual(
            fresh["synthetic_proposed_rule_output"]["function_sha256"], FUNCTION_SHA
        )
        self.assertTrue(
            fresh["synthetic_proposed_rule_output"]["draft_token_synthetic_only"].startswith(
                "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__"
            )
        )
        self.assertFalse(fresh["data_opened"])
        self.assertFalse(fresh["v2_frozen"])
        self.assertIsNone(fresh["verdict"])

    def test_real_mode_refused_before_read(self) -> None:
        missing = HERE / "NAO_EXISTE_R52_REAL.json"
        self.assertFalse(missing.exists())
        with self.assertRaisesRegex(
            gate.ReaderGateError, "mode refused before documentary reading"
        ):
            stage.run_synthetic(
                missing, "0" * 64, missing, SPEC_SHA,
                missing, "0" * 64, mode="real",
            )


if __name__ == "__main__":
    unittest.main()
