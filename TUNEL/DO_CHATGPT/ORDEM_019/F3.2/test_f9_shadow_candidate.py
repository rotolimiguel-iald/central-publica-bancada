"""Synthetic-only adversarial tests for the proposed V1.x gate and runner."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path

from f9_reader_gate_v1x_candidate import (
    BINDING_SCHEMA,
    FROZEN_SCHEMA,
    HISTORICAL_V1_SHA256,
    ReaderGateError,
    verify_v1x_binding,
)
from f9_shadow_runner_candidate import (
    DECLARED_EXECUTOR_SEMANTICS,
    MU_DO_RITO,
    SHADOW_SCHEMA,
    run_synthetic_shadow,
)


IDS = ("L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo")
COMPONENTS = ((1.04,), (1.22, 1.33, 0.7), (0.7, 2.3), (3.1, 3.0), (3.9, 3.3))
TRANSFORMS = ("identity", "quadrature", "quadrature", "arithmetic_mean", "arithmetic_mean")


def _save(path: Path, data: bytes) -> dict:
    path.write_bytes(data)
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def _json(path: Path, value: dict) -> dict:
    return _save(path, json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8"))


class CandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records = []
        frozen_readers = {}
        for i, reader_id in enumerate(IDS):
            h0 = float(10 + i)
            parts = list(COMPONENTS[i])
            transform = TRANSFORMS[i]
            source = "\n".join(
                [f"synthetic H0={h0}"]
                + [f"synthetic sigma_component={part}" for part in parts]
            ).encode("utf-8")
            source_pin = _save(self.root / f"source_{i}.txt", source)
            sigma = (
                parts[0]
                if transform == "identity"
                else math.sqrt(sum(x * x for x in parts))
                if transform == "quadrature"
                else sum(parts) / 2
            )
            metadata = {"H0": h0, "sigma": sigma, "tipo": "synthetic"}
            frozen_readers[reader_id] = metadata
            record = {
                "reader_id": reader_id,
                "source": source_pin,
                "H0_published": h0,
                "sigma_published_components": parts,
                "local_transform": transform,
                "frozen_metadata": metadata,
                "numeric_windows": {
                    "H0": {"literal": f"synthetic H0={h0}", "numeric_literal": str(h0)},
                    "sigma_components": [
                        {"literal": f"synthetic sigma_component={part}", "numeric_literal": str(part)}
                        for part in parts
                    ],
                },
            }
            if transform == "arithmetic_mean":
                record["asymmetric_sigma"] = {"plus": parts[0], "minus": parts[1]}
            self.records.append(record)
        self.frozen = {"schema": FROZEN_SCHEMA, "synthetic_fixture": True, "spec": {"leitores": frozen_readers}}
        self.frozen_pin = _json(self.root / "frozen.json", self.frozen)
        self.binding = {
            "schema": BINDING_SCHEMA,
            "synthetic_fixture": True,
            "statistical_admission_decided": False,
            "frozen_v1x": self.frozen_pin,
            "readers": self.records,
        }
        self.binding_pin = _json(self.root / "binding.json", self.binding)
        self.case = {
            "schema": SHADOW_SCHEMA,
            "mode": "SYNTHETIC_SHADOW_ONLY",
            "synthetic_fixture": True,
            "mu_do_rito": MU_DO_RITO,
            "declared_executor_semantics": DECLARED_EXECUTOR_SEMANTICS,
            "binding": self.binding_pin,
            "synthetic_power": {
                "K": 1.08,
                "H0_background": 10.0,
                "sigma_background": 0.3,
                "sigma_comb_min": 0.8,
                "sigma_comb_max": 1.0,
            },
        }
        self.case_pin = _json(self.root / "case.json", self.case)

    def _verify(self) -> dict:
        return verify_v1x_binding(
            self.root / "binding.json",
            expected_binding_sha256=self.binding_pin["sha256"],
            allowed_source_root=self.root,
        )

    def _run(self) -> dict:
        return run_synthetic_shadow(
            self.root / "case.json",
            expected_case_sha256=self.case_pin["sha256"],
            fixture_root=self.root,
        )

    def _replace_binding(self, change) -> None:
        value = copy.deepcopy(self.binding)
        change(value)
        self.binding_pin = _json(self.root / "binding.json", value)
        self.case["binding"] = self.binding_pin
        self.case_pin = _json(self.root / "case.json", self.case)

    def _replace_case(self, change) -> None:
        value = copy.deepcopy(self.case)
        change(value)
        self.case_pin = _json(self.root / "case.json", value)

    def test_valid_synthetic_case_reports_no_verdict_or_admission(self) -> None:
        before = sorted(p.name for p in self.root.iterdir())
        result = self._run()
        self.assertEqual(result["verified_reader_count"], 5)
        self.assertEqual(result["statistical_admission"], "OPEN")
        self.assertEqual(result["verdict"], "NONE_SYNTHETIC_PREFLIGHT")
        self.assertFalse(result["executor_semantics_executed"])
        self.assertGreater(result["power_at_min_sigma"], result["power_at_max_sigma"])
        self.assertEqual(before, sorted(p.name for p in self.root.iterdir()))

    def test_generic_anchor_is_rejected_even_when_in_source(self) -> None:
        def change(value):
            value["readers"][0]["numeric_windows"]["H0"] = {
                "literal": "synthetic", "numeric_literal": "10.0"
            }
        self._replace_binding(change)
        with self.assertRaisesRegex(ReaderGateError, "does not contain"):
            self._verify()

    def test_numeric_component_window_cannot_be_omitted(self) -> None:
        def change(value):
            value["readers"][1]["numeric_windows"]["sigma_components"].pop()
        self._replace_binding(change)
        with self.assertRaisesRegex(ReaderGateError, "windows incomplete"):
            self._verify()

    def test_real_or_unknown_mode_refused(self) -> None:
        self._replace_case(lambda value: value.update(mode="REAL"))
        with self.assertRaisesRegex(ReaderGateError, "mode refused"):
            self._run()

    def test_missing_mu_do_rito_refused(self) -> None:
        self._replace_case(lambda value: value.pop("mu_do_rito"))
        with self.assertRaisesRegex(ReaderGateError, "mu_do_rito"):
            self._run()

    def test_old_executor_semantics_refused(self) -> None:
        self._replace_case(lambda value: value["declared_executor_semantics"].update(background="profiled"))
        with self.assertRaisesRegex(ReaderGateError, "executor semantics"):
            self._run()

    def test_real_binding_refused_before_documentary_gate(self) -> None:
        self._replace_binding(lambda value: value.update(synthetic_fixture=False))
        with self.assertRaisesRegex(ReaderGateError, "not a synthetic fixture"):
            self._run()

    def test_old_v1_pin_refused(self) -> None:
        self._replace_binding(lambda value: value["frozen_v1x"].update(sha256=HISTORICAL_V1_SHA256))
        with self.assertRaisesRegex(ReaderGateError, "historical V1"):
            self._verify()

    def test_missing_schema_is_typed_refusal(self) -> None:
        def change(value):
            del value["readers"][0]["sigma_published_components"]
        self._replace_binding(change)
        with self.assertRaises(ReaderGateError):
            self._verify()

    def test_asymmetric_sides_preserved(self) -> None:
        def change(value):
            value["readers"][3]["asymmetric_sigma"] = {"plus": 3.0, "minus": 3.1}
        self._replace_binding(change)
        with self.assertRaisesRegex(ReaderGateError, "asymmetric sigma sides changed"):
            self._verify()

    def test_source_outside_fixture_root_refused(self) -> None:
        outside = self.root.parent / "outside_synthetic_f9.txt"
        outside.write_text("synthetic", encoding="utf-8")
        self.addCleanup(outside.unlink)
        self._replace_binding(lambda value: value["readers"][0]["source"].update(path=str(outside)))
        with self.assertRaisesRegex(ReaderGateError, "outside synthetic fixture root"):
            self._run()

    def test_source_bytes_mismatch_refused(self) -> None:
        (self.root / "source_0.txt").write_bytes(b"tampered")
        with self.assertRaisesRegex(ReaderGateError, "bytes/hash mismatch"):
            self._verify()


if __name__ == "__main__":
    unittest.main()
