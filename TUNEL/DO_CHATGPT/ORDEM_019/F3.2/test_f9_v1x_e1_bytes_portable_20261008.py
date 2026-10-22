"""Portable, leak-free synthetic-only harness for the pinned F3.1.E1 documentary gate."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PureWindowsPath
import shutil
import subprocess
import sys
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
TEMP_PREFIX = "f32_e1_bytes_portable_"
LOCAL_MODULES = (
    "f9_reader_gate.py",
    "f9_reader_gate_v1x_e1_bytes.py",
    "f9_runner_v1x_preflight_e1_bytes.py",
    "f9_runner_v1x_staged_e1_bytes.py",
)


class InjectedCopyFailure(RuntimeError):
    pass


def archive_suffix(documentary_path: str) -> Path:
    """Extract the ORDEM subtree, independent of the absolute origin path."""
    parts = PureWindowsPath(documentary_path).parts
    markers = [index for index, part in enumerate(parts)
               if part.casefold() in {"ordem_018", "ordem_019"}]
    if len(markers) != 1:
        raise AssertionError("documentary path lacks one unique ORDEM root")
    suffix = Path(*parts[markers[0]:])
    if suffix.parts[0].casefold() == "ordem_019" and (
            len(suffix.parts) < 3 or suffix.parts[1].casefold() != "f3.1"):
        raise AssertionError("unexpected ORDEM_019 source subtree")
    return suffix


def source_in_current_archive(documentary_path: str) -> Path:
    return ARCHIVE / archive_suffix(documentary_path)


def verify(binding: Path, archive: Path) -> dict:
    return gate.verify_v1x_binding(
        binding, expected_binding_sha256=BINDING_SHA,
        allowed_source_root=archive / "ORDEM_018",
        expected_spec_sha256=SPEC_SHA,
    )


def temp_snapshot() -> set[str]:
    temp_root = Path(tempfile.gettempdir()).resolve()
    return {child.name for child in temp_root.iterdir()
            if child.is_dir() and child.name.startswith(TEMP_PREFIX)}


@contextmanager
def relocated_bundle(*, fail_at: str | None = None, include_harness: bool = False):
    """Construct and clean a moved bundle, including failures before the yield."""
    temp_root = Path(tempfile.gettempdir()).resolve()
    root: Path | None = None
    try:
        if fail_at == "before_mkdtemp":
            raise InjectedCopyFailure("before_mkdtemp")
        root = Path(tempfile.mkdtemp(prefix=TEMP_PREFIX, dir=temp_root)).resolve()
        if root.parent != temp_root or not root.name.startswith(TEMP_PREFIX):
            raise AssertionError("test root escaped its dedicated temp directory")
        if fail_at == "after_mkdtemp":
            raise InjectedCopyFailure("after_mkdtemp")
        destination = root / "bundle"
        (destination / "ORDEM_019" / "F3.1").mkdir(parents=True)
        (destination / "ORDEM_019" / "F3.2").mkdir(parents=True)
        (destination / "ORDEM_018").mkdir(parents=True)
        copied: set[Path] = set()
        for pin in PINS["r52_ancestor_files"]:
            suffix = archive_suffix(pin["path"])
            target = destination / suffix
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_in_current_archive(pin["path"]), target)
            copied.add(suffix)
            if fail_at == "during_copy":
                raise InjectedCopyFailure("during_copy")
        for record in PINS["readers"]:
            for key in ("source", "text_projection", "projection_receipt"):
                pin = record.get(key)
                if not pin:
                    continue
                suffix = archive_suffix(pin["path"])
                if suffix in copied:
                    continue
                target = destination / suffix
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_in_current_archive(pin["path"]), target)
                copied.add(suffix)
        target_dir = destination / "ORDEM_019" / "F3.2"
        shutil.copyfile(BINDING, target_dir / BINDING.name)
        shutil.copyfile(FIXTURE, target_dir / FIXTURE.name)
        if include_harness:
            for name in LOCAL_MODULES + (Path(__file__).name,):
                shutil.copyfile(HERE / name, target_dir / name)
        yield destination
    finally:
        if root is not None:
            target = root.resolve()
            if target.parent != temp_root or not target.name.startswith(TEMP_PREFIX):
                raise AssertionError("refusing recursive cleanup outside designated temp root")
            shutil.rmtree(target)


class PortableHarnessTests(unittest.TestCase):
    def test_original_receipt(self) -> None:
        self.assertEqual(hashlib.sha256(BINDING.read_bytes()).hexdigest(), BINDING_SHA)
        receipt = verify(BINDING, ARCHIVE)
        self.assertEqual([row["role"] for row in receipt["ancestor_bytes_rechecked"]],
                         ["F3.4", "R5", "R5.1", "R5.2", "F3.1.E1"])
        self.assertEqual(receipt["spec_sha256"], SPEC_SHA)
        self.assertEqual(receipt["projection"], "F3.1.E1")
        self.assertFalse(receipt["v2_frozen"])

    def test_full_relocation_and_synthetic_runner(self) -> None:
        with relocated_bundle() as moved:
            binding = moved / "ORDEM_019" / "F3.2" / BINDING.name
            fixture = moved / "ORDEM_019" / "F3.2" / FIXTURE.name
            receipt = verify(binding, moved)
            self.assertEqual(receipt["spec_sha256"], SPEC_SHA)
            preflight = pre.prepare_v1x(
                binding, expected_binding_sha256=BINDING_SHA,
                allowed_source_root=moved / "ORDEM_018",
                expected_spec_sha256=SPEC_SHA)
            self.assertFalse(preflight["data_opened"])
            result = stage.run_synthetic(
                binding, BINDING_SHA, moved / "ORDEM_018", SPEC_SHA,
                fixture, FIXTURE_SHA, mode="synthetic_only")
            self.assertFalse(result["data_opened"])
            self.assertFalse(result["v2_frozen"])
            self.assertIsNone(result["verdict"])
            self.assertEqual(result["synthetic_proposed_rule_output"]["function_sha256"],
                             gate.R52_FUNCTION_SHA256)

    def test_harness_itself_runs_from_relocated_package(self) -> None:
        with relocated_bundle(include_harness=True) as moved:
            harness = moved / "ORDEM_019" / "F3.2" / Path(__file__).name
            run = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(harness),
                 "PortableHarnessTests.test_original_receipt"],
                cwd=Path(tempfile.gettempdir()), capture_output=True,
                text=True, encoding="utf-8")
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertIn("Ran 1 test", run.stderr)

    def test_each_lineage_mutation_refused(self) -> None:
        with relocated_bundle() as moved:
            binding = moved / "ORDEM_019" / "F3.2" / BINDING.name
            for pin in PINS["r52_ancestor_files"]:
                target = moved / archive_suffix(pin["path"])
                original = target.read_bytes()
                mutant = bytearray(original)
                mutant[-1] = 32 if mutant[-1] != 32 else 10
                self.assertNotEqual(mutant, original)
                try:
                    target.write_bytes(mutant)
                    with self.subTest(role=pin["role"]):
                        with self.assertRaises(gate.ReaderGateError):
                            verify(binding, moved)
                finally:
                    target.write_bytes(original)
            self.assertEqual(len(verify(binding, moved)["ancestor_bytes_rechecked"]), 5)

    def test_partial_relocation_refused(self) -> None:
        with relocated_bundle() as moved:
            source = moved / "ORDEM_018" / "fontes_publicas" / "sh0es_2022.html"
            source.unlink()
            with self.assertRaises(gate.ReaderGateError):
                verify(moved / "ORDEM_019" / "F3.2" / BINDING.name, moved)

    def test_cleanup_before_after_and_during_copy_failure(self) -> None:
        before = temp_snapshot()
        for point in ("before_mkdtemp", "after_mkdtemp", "during_copy"):
            with self.subTest(point=point):
                with self.assertRaisesRegex(InjectedCopyFailure, point):
                    with relocated_bundle(fail_at=point):
                        self.fail("injected failure should prevent yield")
                self.assertEqual(temp_snapshot(), before, "temporary bundle leaked")

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
