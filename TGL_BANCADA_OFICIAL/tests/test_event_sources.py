"""Temporary C6 fixtures only; never execute the scientific source programs."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock
import zipfile

SPEC = importlib.util.spec_from_file_location(
    "event_sources_under_test", Path(__file__).resolve().parents[1] / "event_sources.py")
sources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sources)

try:
    import h5py
except ImportError:
    h5py = None

DQ_NAMES = ["DATA", "CBC_CAT1", "CBC_CAT2", "CBC_CAT3", "BURST_CAT1",
            "BURST_CAT2", "BURST_CAT3", "STOCH_CAT1", "CW_CAT1"]
INJ_NAMES = ["NO_CBC_HW_INJ", "NO_BURST_HW_INJ", "NO_DETCHAR_HW_INJ",
             "NO_CW_HW_INJ", "NO_STOCH_HW_INJ"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, allow_nan=False), encoding="utf-8")


def write_npz(path, whitener=(407, 410)):
    """Generate valid NPY headers/payloads without NumPy."""
    shapes = {"frequency_hz": (8193,), "median_psd_strain": (8193,),
              "covariance_scaled": (410, 410), "projected_covariance_scaled": (407, 407),
              "whitener_scaled": whitener}
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, shape in shapes.items():
            header = repr({"descr": "<f8", "fortran_order": False, "shape": shape}).encode("ascii")
            header += b" " * ((-10 - len(header) - 1) % 64) + b"\n"
            payload = b"\x93NUMPY\x01\x00" + struct.pack("<H", len(header)) + header
            archive.writestr(name + ".npy", payload + bytes(math.prod(shape) * 8))


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("cache/gwosc/on_source", "cache/gwosc/offsource", "cache/empirical_noise"):
            (self.root / folder).mkdir(parents=True)
        self.reg = {
            "event": "GW250114_082203",
            "reference_peak_GPS": {"H1": 1420878141.2189023, "L1": 1420878141.2164068},
            "reference_source": "Synthetic fixture of the C6 interface",
            "reference_redshift": .086,
            "reference_mass_for_start_solar": 68.40897469707073,
            "reference_tM_seconds": .0003369477856078424,
            "interval_samples": 410, "analysis_sample_rate_hz": 2048, "sample_stride": 2,
            "start_times_tM": [6., 8., 10., 10.5, 12.], "primary_start_tM": 10.,
            "time_selection": "First original sample at/after start, every second sample",
            "noise": "Offsource finite interval degree-2 quotient",
            "quality_required": DQ_NAMES[:4],
            "injection_flags_required": [n for n in INJ_NAMES if n != "NO_CW_HW_INJ"],
            "likelihood": "Synthetic C6 220+440 likelihood description",
            "scope": "Independent detector quadratures, not coherent polarization",
            "computed_readings": ["R-GLOBAL"], "subresolution_readings": {},
            "omitted_nonexponential": "Fixture omitted model", "mass_detector_prior_solar": [40, 100],
            "spin_prior": [0, .95], "amplitude_prior": {"primary": 10},
            "physical_gate": "INCONCLUSIVE_SYSTEMATICS", "target_downloads": [],
            "code_and_input_hashes": {},
        }
        self.noise = {"status": "MEASURED_OFF_SOURCE_ONLY", "detectors": []}
        self.downloads = {"files": []}
        self.results = {"status": "INCONCLUSIVE_SYSTEMATICS", "reason": "Synthetic failed calibration",
                        "scope": "Conditional", "do_not_combine": "Overlapping windows"}
        (self.root / "c6_engine.py").write_text("raise RuntimeError('MUST NEVER EXECUTE')\n", encoding="utf-8")
        for detector in ("H1", "L1"):
            on_name = f"cache/gwosc/on_source/{detector}-target.hdf5"
            off_name = f"cache/gwosc/offsource/{detector}-noise.hdf5"
            (self.root / on_name).write_bytes(b"Synthetic hash-only target " + detector.encode())
            (self.root / off_name).write_bytes(b"Synthetic hash-only offsource " + detector.encode())
            write_npz(self.root / f"cache/empirical_noise/{detector}_noise.npz")
            url = "https://example.invalid/" + Path(on_name).name
            self.reg["target_downloads"].append({"detector": detector, "gps_start": 1420877824,
                                                  "hdf5_url": url, "sample_rate_kHz": 4})
            self.downloads["files"].append({"detector": detector, "path": on_name, "url": url})
            self.noise["detectors"].append({
                "detector": detector, "input_path": off_name, "GPSstart": 1420873728,
                "training_seconds": [0, 2048], "sample_selection": "Every second sample; no filter",
                "method": "Synthetic median Welch", "nuisance": "Degree 2 polynomial quotient",
                "whitened_dof": 407, "interval_samples": 410, "sample_rate_hz": 2048,
                "original_sample_rate_hz": 4096, "no_filter": True, "no_PSD_floor": True,
                "CW_scope": "CW hardware injections are not vetoed for CBC",
            })
        self.refresh_pins()

    def refresh_pins(self):
        pins = {"c6_engine.py": digest(self.root / "c6_engine.py")}
        for n in self.noise["detectors"]:
            n["input_sha256"] = digest(self.root / n["input_path"])
            name = f"cache/empirical_noise/{n['detector']}_noise.npz"
            n["cache_sha256"] = pins[name] = digest(self.root / name)
        write_json(self.root / "C5_EMPIRICAL_NOISE.json", self.noise)
        pins["C5_EMPIRICAL_NOISE.json"] = digest(self.root / "C5_EMPIRICAL_NOISE.json")
        self.reg["code_and_input_hashes"] = pins
        write_json(self.root / "REGISTRO_C6.json", self.reg)
        reg_hash = digest(self.root / "REGISTRO_C6.json")
        self.downloads["registration_sha256"] = self.results["registration_sha256"] = reg_hash
        for d in self.downloads["files"]:
            d["registration_sha256"] = reg_hash
            d["sha256"] = digest(self.root / d["path"])
        write_json(self.root / "C6_DOWNLOADS.json", self.downloads)
        write_json(self.root / "C6_RESULTS.json", self.results)

    def build(self, **kwargs):
        return sources.build_event_manifest(root=self.root, **kwargs)

    def assert_blocked(self, result, code):
        self.assertFalse(result["ready_for_source_use"])
        self.assertIn(code, [e["code"] for e in result["errors"]], result["errors"])

    def test_infers_event_compact_schema_and_preserves_originals(self):
        before = {str(p): digest(p) for p in self.root.rglob("*") if p.is_file()}
        result = self.build()
        self.assertTrue(result["ready_for_source_use"], result["errors"])
        self.assertEqual(result["event"], self.reg["event"])
        self.assertEqual(result["reference_peak_gps"], self.reg["reference_peak_GPS"])
        self.assertIsNone(result["event_gps"])
        self.assertEqual(result["scientific_status"], "INCONCLUSIVE_SYSTEMATICS")
        self.assertTrue(result["scientific_result"]["registration_matches"])
        self.assertFalse(result["model"]["physical_exclusion_allowed"])
        self.assertEqual(result["dq_status"], "PENDING_RESIDENT_VALIDATION")
        analysis = result["analysis"]
        self.assertEqual(analysis["reference_mass_detector_solar_for_start"], self.reg["reference_mass_for_start_solar"])
        for key in ("quality_required", "injection_flags_required", "start_times_tM"):
            self.assertEqual(analysis[key], self.reg[key])
        arrays = result["detectors"]["H1"]["noise"]["arrays"]
        self.assertEqual(arrays["whitener_scaled"]["shape"], [407, 410])
        self.assertEqual(arrays["frequency_hz"]["shape"], [8193])
        self.assertLess(len(json.dumps(result, allow_nan=False)), 40000)
        self.assertEqual(before, {str(p): digest(p) for p in self.root.rglob("*") if p.is_file()})

    def test_default_does_not_import_h5py(self):
        original = __import__
        def guarded(name, *args, **kwargs):
            if name == "h5py":
                raise AssertionError("Default must not import h5py")
            return original(name, *args, **kwargs)
        with mock.patch("builtins.__import__", side_effect=guarded):
            self.assertTrue(self.build()["ready_for_source_use"])

    def test_default_root_is_absolute_and_independent_of_installation(self):
        self.assertTrue(sources.DEFAULT_ROOT.is_absolute())
        expected = ("C:/IALD" if os.name == "nt" else "/mnt/c/IALD") + "/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN"
        self.assertEqual(sources.DEFAULT_ROOT.as_posix(), expected)

    def test_explicit_event_mismatch_is_not_relabelled(self):
        result = self.build(event="OTHER_EVENT")
        self.assert_blocked(result, "EVENT_MISMATCH")
        self.assertEqual(result["event"], self.reg["event"])

    def test_hash_mismatch_keeps_expected_and_measured_digests(self):
        target = self.downloads["files"][0]
        (self.root / target["path"]).write_bytes(b"Altered fixture")
        result = self.build()
        self.assert_blocked(result, "HASH_MISMATCH")
        entry = result["sources"][target["path"]]
        self.assertEqual(entry["expected_sha256"], target["sha256"])
        self.assertEqual(entry["sha256"], digest(self.root / target["path"]))
        self.assertEqual(entry["integrity"], "MISMATCH")

    def test_missing_source_fails(self):
        (self.root / self.downloads["files"][0]["path"]).unlink()
        self.assert_blocked(self.build(), "SOURCE_UNREADABLE")

    def test_modified_scientific_code_is_hashed_not_executed(self):
        (self.root / "c6_engine.py").write_bytes(b"Not executed")
        self.assert_blocked(self.build(), "HASH_MISMATCH")

    def test_results_must_bind_to_registration(self):
        self.results["registration_sha256"] = "0" * 64
        write_json(self.root / "C6_RESULTS.json", self.results)
        self.assert_blocked(self.build(), "REGISTRATION_HASH_MISMATCH")

    def test_status_cannot_be_promoted(self):
        self.results["status"] = "CONFIRMED"
        write_json(self.root / "C6_RESULTS.json", self.results)
        self.assert_blocked(self.build(), "SCIENTIFIC_STATUS_CHANGED")

    def test_square_whitener_is_rejected_even_with_matching_digest(self):
        write_npz(self.root / "cache/empirical_noise/H1_noise.npz", whitener=(410, 410))
        self.refresh_pins()
        self.assert_blocked(self.build(), "NPZ_SCHEMA_ERROR")

    def test_source_traversal_is_rejected(self):
        self.reg["code_and_input_hashes"]["../outside.py"] = "0" * 64
        write_json(self.root / "REGISTRO_C6.json", self.reg)
        result = self.build()
        self.assert_blocked(result, "SOURCE_UNREADABLE")
        self.assertIsNone(result["sources"]["../outside.py"]["sha256"])

    def test_null_pin_is_not_unpinned_success(self):
        self.reg["code_and_input_hashes"]["c6_engine.py"] = None
        write_json(self.root / "REGISTRO_C6.json", self.reg)
        self.assert_blocked(self.build(), "REGISTRATION_SCHEMA_ERROR")

    def test_invalid_json_fails_closed(self):
        (self.root / "REGISTRO_C6.json").write_text('{"event":NaN}', encoding="utf-8")
        self.assert_blocked(self.build(), "INVALID_JSON")

    def make_hdf(self, *, mask_offset=0., mask_spacing=1., reorder=False):
        for role in ("on_source", "offsource"):
            gps = 1420877824 if role == "on_source" else 1420873728
            for detector in ("H1", "L1"):
                name = detector + ("-target.hdf5" if role == "on_source" else "-noise.hdf5")
                path = self.root / "cache/gwosc" / role / name
                with h5py.File(path, "w") as f:
                    f["meta/GPSstart"] = gps
                    f["meta/Duration"] = 4096
                    f["meta/Detector"] = detector.encode()
                    strain = f.create_dataset("strain/Strain", shape=(4096 * 4096,), dtype="f8", fillvalue=0.)
                    strain.attrs.update(Xstart=gps, Xspacing=1 / 4096, Xunits="second")
                    for parent, prefix, names in (("quality/simple", "DQ", DQ_NAMES),
                                                  ("quality/injections", "Inj", INJ_NAMES)):
                        names = list(reversed(names)) if reorder else names
                        required = self.reg["quality_required" if prefix == "DQ" else "injection_flags_required"]
                        value = sum(1 << names.index(n) for n in required)
                        ds = f.create_dataset(f"{parent}/{prefix}mask", shape=(4096,), dtype="u4", fillvalue=value)
                        ds.attrs.update(Xstart=gps + mask_offset, Xspacing=mask_spacing,
                                        Xunits="second", Bits=len(names))
                        f.create_dataset(f"{parent}/{prefix}Shortnames", data=[n.encode() for n in names])
                        f.create_dataset(f"{parent}/{prefix}Descriptions", data=[n.encode() for n in names])
        self.refresh_pins()

    @unittest.skipIf(h5py is None, "Optional h5py unavailable; default is tested without it")
    def test_hdf_masks_whitener_and_cw_policy(self):
        self.make_hdf()
        result = self.build(inspect_hdf5=True)
        self.assertTrue(result["ready_for_source_use"], result["errors"])
        self.assertEqual(result["dq_status"], "REGISTERED_WINDOWS_PASS")
        metadata = result["detectors"]["H1"]["strain"]["metadata"]
        self.assertEqual(metadata["masks"]["dq"]["required_mask"], 15)
        self.assertEqual(metadata["masks"]["injection"]["required_mask"], 23)
        self.assertTrue(metadata["masks"]["injection"]["cw_not_vetoed"])
        self.assertEqual(metadata["masks"]["injection"]["cw_present_seconds"], 4096)
        self.assertTrue(all(w["dq_injection_pass"] for w in metadata["registered_windows"]))

    @unittest.skipIf(h5py is None, "Optional h5py unavailable")
    def test_mask_uses_own_epoch_cadence_and_named_bit_order(self):
        self.make_hdf(mask_offset=-2., mask_spacing=.5, reorder=True)
        result = self.build(inspect_hdf5=True)
        self.assertTrue(result["ready_for_source_use"], result["errors"])
        metadata = result["detectors"]["H1"]["strain"]["metadata"]
        self.assertEqual(metadata["masks"]["dq"]["required_mask"], sum(1 << i for i in (5, 6, 7, 8)))
        w = metadata["registered_windows"][0]
        self.assertEqual(w["mask_intervals"]["dq"]["first"], math.floor((w["first_sample_gps"] - (1420877824 - 2)) / .5))

    @unittest.skipIf(h5py is None, "Optional h5py unavailable")
    def test_bad_required_injection_bit_rejects_window(self):
        self.make_hdf()
        with h5py.File(self.root / self.downloads["files"][0]["path"], "r+") as f:
            f["quality/injections/Injmask"][317] = 22
        self.refresh_pins()
        self.assert_blocked(self.build(inspect_hdf5=True), "DQ_WINDOW_REJECTED")

    @unittest.skipIf(h5py is None, "Optional h5py unavailable")
    def test_uncovered_mask_time_is_rejected(self):
        self.make_hdf(mask_offset=1000)
        self.assert_blocked(self.build(inspect_hdf5=True), "HDF5_SCHEMA_ERROR")

    @unittest.skipIf(h5py is None, "Optional h5py unavailable")
    def test_external_hdf_link_is_not_followed(self):
        self.make_hdf()
        with h5py.File(self.root / self.downloads["files"][0]["path"], "r+") as f:
            del f["strain/Strain"]
            f["strain/Strain"] = h5py.ExternalLink("never-read.hdf5", "strain/Strain")
        self.refresh_pins()
        result = self.build(inspect_hdf5=True)
        self.assert_blocked(result, "HDF5_SCHEMA_ERROR")
        self.assertTrue(any("Nonlocal HDF5 link" in e["detail"] for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
