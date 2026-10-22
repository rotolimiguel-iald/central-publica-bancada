"""Synthetic-only checks for byte-re-read lineage and fully relocated F3.2 bundle."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import f9_reader_gate_v1x_e1_bytes as gate
import f9_runner_v1x_preflight_e1_bytes as pre
import f9_runner_v1x_staged_e1_bytes as stage

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parents[1]
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json"
BINDING_SHA = "f6e7840e28071a524035c49196c989b0fe871ac27685e0f26bac1a7aa24376b6"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
FIXTURE_SHA = "d9c07fd536ee4ca93956ccc06a3e8217719e1d028cd00350cd5ddb43ec2f08ff"
SPEC_SHA = gate.E1_SPEC_SHA256
PINS = json.loads(BINDING.read_bytes())


def verify(binding: Path, archive: Path) -> dict:
    return gate.verify_v1x_binding(
        binding, expected_binding_sha256=BINDING_SHA,
        allowed_source_root=archive / "ORDEM_018",
        expected_spec_sha256=SPEC_SHA,
    )


def relocated_copy() -> Path:
    root = Path(tempfile.mkdtemp(prefix="f32_e1_bytes_")).resolve()
    assert root.is_relative_to(Path(tempfile.gettempdir()).resolve())
    destination = root / "bundle"
    (destination / "ORDEM_019" / "F3.1").mkdir(parents=True)
    (destination / "ORDEM_019" / "F3.2").mkdir(parents=True)
    (destination / "ORDEM_018").mkdir(parents=True)
    for pin in PINS["r52_ancestor_files"]:
        source = Path(pin["path"])
        target = destination / source.relative_to(ARCHIVE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for record in PINS["readers"]:
        for key in ("source", "text_projection", "projection_receipt"):
            pin = record.get(key)
            if not pin:
                continue
            source = Path(pin["path"])
            target = destination / source.relative_to(ARCHIVE)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    shutil.copyfile(BINDING, destination / "ORDEM_019" / "F3.2" / BINDING.name)
    shutil.copyfile(FIXTURE, destination / "ORDEM_019" / "F3.2" / FIXTURE.name)
    return destination


def remove_copy(destination: Path) -> None:
    target = destination.parent.resolve()
    if not target.is_relative_to(Path(tempfile.gettempdir()).resolve()) or not target.name.startswith("f32_e1_bytes_"):
        raise AssertionError("refusing recursive cleanup outside designated test directory")
    shutil.rmtree(target)


class ByteLineageTests(unittest.TestCase):
    def test_original_receipt(self) -> None:
        self.assertEqual(hashlib.sha256(BINDING.read_bytes()).hexdigest(), BINDING_SHA)
        record = verify(BINDING, ARCHIVE)
        self.assertEqual([x["role"] for x in record["ancestor_bytes_rechecked"]],
                         ["F3.4", "R5", "R5.1", "R5.2", "F3.1.E1"])
        self.assertEqual(record["source_admission"], "OPEN")
        self.assertEqual(record["spec_sha256"], gate.E1_SPEC_SHA256)
        self.assertEqual(record["projection"], "F3.1.E1")
        self.assertFalse(record["v2_frozen"])

    def test_full_relocation_and_synthetic_runner(self) -> None:
        moved = relocated_copy()
        try:
            binding = moved / "ORDEM_019" / "F3.2" / BINDING.name
            fixture = moved / "ORDEM_019" / "F3.2" / FIXTURE.name
            self.assertNotEqual(moved, ARCHIVE)
            record = verify(binding, moved)
            self.assertEqual(record["spec_sha256"], SPEC_SHA)
            ready = pre.prepare_v1x(
                binding, expected_binding_sha256=BINDING_SHA,
                allowed_source_root=moved / "ORDEM_018",
                expected_spec_sha256=SPEC_SHA)
            self.assertFalse(ready["data_opened"])
            result = stage.run_synthetic(
                binding, BINDING_SHA, moved / "ORDEM_018", SPEC_SHA,
                fixture, FIXTURE_SHA, mode="synthetic_only")
            self.assertFalse(result["data_opened"])
            self.assertFalse(result["v2_frozen"])
            self.assertIsNone(result["verdict"])
            self.assertEqual(result["synthetic_proposed_rule_output"]["function_sha256"],
                             gate.R52_FUNCTION_SHA256)
        finally:
            remove_copy(moved)

    def test_each_ancestor_mutation_refused(self) -> None:
        moved = relocated_copy()
        try:
            binding = moved / "ORDEM_019" / "F3.2" / BINDING.name
            for pin in PINS["r52_ancestor_files"]:
                target = moved / Path(pin["path"]).relative_to(ARCHIVE)
                original = target.read_bytes()
                try:
                    target.write_bytes(original + b" ")
                    with self.subTest(role=pin["role"]):
                        with self.assertRaises(gate.ReaderGateError):
                            verify(binding, moved)
                finally:
                    target.write_bytes(original)
            self.assertEqual(len(verify(binding, moved)["ancestor_bytes_rechecked"]), 5)
        finally:
            remove_copy(moved)

    def test_partial_relocation_refused(self) -> None:
        moved = relocated_copy()
        try:
            source = moved / "ORDEM_018" / "fontes_publicas" / "sh0es_2022.html"
            source.unlink()
            with self.assertRaises(gate.ReaderGateError):
                verify(moved / "ORDEM_019" / "F3.2" / BINDING.name, moved)
            with self.assertRaisesRegex(gate.ReaderGateError, "source root differs"):
                gate.verify_v1x_binding(
                    moved / "ORDEM_019" / "F3.2" / BINDING.name,
                    expected_binding_sha256=BINDING_SHA,
                    allowed_source_root=ARCHIVE / "ORDEM_018",
                    expected_spec_sha256=SPEC_SHA)
        finally:
            remove_copy(moved)

    def test_wrong_hash_and_real_mode_refused_before_read(self) -> None:
        with self.assertRaisesRegex(gate.ReaderGateError, "binding hash mismatch"):
            gate.verify_v1x_binding(
                BINDING, expected_binding_sha256="0" * 64,
                allowed_source_root=ARCHIVE / "ORDEM_018",
                expected_spec_sha256=SPEC_SHA)
        absent = HERE / "NO_REAL_INPUT_EXISTS.json"
        self.assertFalse(absent.exists())
        with self.assertRaisesRegex(gate.ReaderGateError, "refused before documentary reading"):
            stage.run_synthetic(
                absent, "0" * 64, absent, SPEC_SHA,
                absent, "0" * 64, mode="real")


if __name__ == "__main__":
    unittest.main(verbosity=2)
