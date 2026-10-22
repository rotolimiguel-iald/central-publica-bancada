import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import data_lab
import treatment


class DataLabTests(unittest.TestCase):
    def test_live_memory_and_installed_catalog(self):
        memory = data_lab.memory_status()
        self.assertGreater(memory["total_bytes"], 0)
        self.assertLessEqual(memory["interactive_budget_bytes"], memory["available_bytes"])
        items = data_lab.catalog()
        self.assertTrue(any("DESIVAST" in item["name"] for item in items))
        self.assertTrue(any("KiDS_DR4.1" in item["name"] for item in items))

    def test_actual_desi_fits_bounded_preview(self):
        item = next(item for item in data_lab.catalog() if item["name"] == "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits")
        path = data_lab.selected(item["id"])
        info = data_lab.describe(path)
        self.assertGreater(info["rows"], 1000)
        self.assertIn("RADIUS", {column["name"] for column in info["columns"]})
        sample = data_lab.preview(path, "X", "Y", 40)
        self.assertLessEqual(len(sample["points"]), 40)
        self.assertEqual(sample["status"], "DATA_PREVIEW_NOT_MODEL_FIT")

    def test_17_gb_kids_header_without_loading_file(self):
        item = next(item for item in data_lab.catalog() if item["name"].startswith("KiDS_DR4.1"))
        info = data_lab.describe(data_lab.selected(item["id"]))
        self.assertGreater(info["rows"], 10_000_000)
        self.assertGreater(len(info["columns"]), 100)

    def test_complex_npy_quantum_array_can_be_sampled_without_numpy(self):
        item = next(item for item in data_lab.catalog() if item["format"] == ".npy")
        path = data_lab.selected(item["id"])
        info = data_lab.describe(path)
        names = {column["name"] for column in info["columns"]}
        self.assertIn("col_0_real", names)
        self.assertIn("col_0_imag", names)
        result = data_lab.preview(path, "col_0_real", "col_0_imag", 25)
        self.assertLessEqual(len(result["points"]), 25)
        self.assertEqual(result["sample_method"], "UNIFORM_ROW_STRIDE")

    def test_bao_mean_uses_matching_covariance_and_rejects_asymmetry(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(data_lab, "BAO_ROOT", Path(folder)):
            mean = Path(folder) / data_lab.BAO_MEAN
            cov = Path(folder) / data_lab.BAO_COV
            mean.write_text("# z value observable\n" + "".join(f"{i/10} {i+3} DM_over_rs\n" for i in range(13)), encoding="utf-8")
            matrix = [[0.04 if i == j else 0.01 for j in range(13)] for i in range(13)]
            cov.write_text("".join(" ".join(str(v) for v in row) + "\n" for row in matrix), encoding="utf-8")
            result = data_lab.preview(mean, "z", "value", 800)
            self.assertEqual(len(result["points"]), 13)
            self.assertAlmostEqual(result["observations"][0]["sigma"], 0.2)
            self.assertEqual(result["covariance"], matrix)
            self.assertEqual(result["mean_sha256"], data_lab.hashlib.sha256(mean.read_bytes()).hexdigest())
            self.assertEqual(result["covariance_sha256"], data_lab.hashlib.sha256(cov.read_bytes()).hexdigest())
            self.assertEqual(result["sample_method"], "FULL_13_POINT_BAO_SUMMARY")
            matrix[1][0] = 0.02
            cov.write_text("".join(" ".join(str(v) for v in row) + "\n" for row in matrix), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not symmetric"):
                data_lab.preview(mean, "z", "value", 800)

    def test_text_preview_is_bounded_and_rejects_bad_column(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "mock.csv"
            with path.open("w", encoding="utf-8") as output:
                output.write("z,value\n")
                for n in range(5000):
                    output.write(f"{n/1000},{n*n}\n")
            result = data_lab.preview(path, "z", "value", 37)
            self.assertEqual(result["sampled_rows"], 5000)
            self.assertEqual(len(result["points"]), 37)
            with self.assertRaises(ValueError):
                data_lab.preview(path, "z", "missing", 37)

    def test_unlisted_path_cannot_be_requested_by_browser(self):
        with self.assertRaises(ValueError):
            data_lab.selected("../other")
        with self.assertRaises(ValueError):
            data_lab.selected("0" * 24)

    def test_treatment_distinguishes_partial_fingerprint_and_statistical_custody(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "data.csv"
            source.write_text("distance,flux\n1,2\n3,4\n", encoding="utf-8")
            record = treatment.record(source)
            self.assertEqual(record["treatment"]["status"], "SCHEMA_READABLE")
            self.assertTrue(all(c["unit"] == "UNKNOWN" for c in record["treatment"]["columns"]))
            self.assertEqual(record["statistics"]["independence"], "NOT_ESTABLISHED")
            self.assertIn("NOT_FULL_FILE_HASH", record["source"]["edge_fingerprint"]["method"])
            source.write_text("distance,flux\n1,2\n3,5\n", encoding="utf-8")
            self.assertNotEqual(record["source"]["edge_fingerprint"]["sha256"],
                                treatment.record(source)["source"]["edge_fingerprint"]["sha256"])

    def test_treatment_refuses_to_call_unknown_format_readable(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "strain.npz"
            source.write_bytes(b"not a validated NPZ dataset")
            record = treatment.record(source)
            self.assertEqual(record["treatment"]["status"], "ADAPTER_PENDING")
            self.assertEqual(record["statistics"]["status"], "NOT_FIT")

    def test_actual_bao_treatment_keeps_pair_and_correlation_status(self):
        source = data_lab.BAO_ROOT / data_lab.BAO_MEAN
        record = treatment.record(source)
        self.assertEqual(record["treatment"]["rows"], 13)
        self.assertEqual(record["statistics"]["independence"], "CORRELATED_WITHIN_THIS_VECTOR")
        self.assertEqual(record["statistics"]["covariance"],
                         "FULL_13X13_VALIDATED_DIMENSIONS_SYMMETRY_DIAGONAL")
        self.assertNotEqual(record["statistics"]["mean_sha256"], record["statistics"]["covariance_sha256"])

    def test_hdf5_preview_calls_bounded_adapter_without_promoting_a_fit(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "strain.hdf5"
            source.write_bytes(b"fixture")
            def adapter(_path, operation, **kwargs):
                if operation == "describe":
                    return {"format": "HDF5_NUMERIC", "rows": 1000000,
                            "columns": [{"name": "index", "unit": "sample_index"},
                                        {"name": "/strain/Strain", "unit": ""}]}
                self.assertEqual(kwargs["limit"], 12)
                return {"points": [[0.0, 1.0], [2.0, 3.0]], "sampled_rows": 12,
                        "dropped_nonfinite_pairs": 10, "coverage": "STRIDED_PREVIEW_NOT_ANALYSIS",
                        "frequency_inference": "FORBIDDEN_WITHOUT_ANTIALIAS_AND_TIME_METADATA",
                        "sample_index": "SYNTHETIC_INDEX_NOT_PHYSICAL_TIME"}
            with patch.object(data_lab.hdf5_bridge, "call", side_effect=adapter) as mocked:
                result = data_lab.preview(source, "index", "/strain/Strain", 12)
            self.assertEqual(mocked.call_count, 2)
            self.assertEqual(result["sample_method"], "HDF5_STRIDED_HYPERSLAB_MAX_1200")
            self.assertEqual(result["status"], "DATA_PREVIEW_NOT_MODEL_FIT")
            self.assertEqual(len(result["points"]), 2)
            self.assertEqual(result["dropped_nonfinite_pairs"], 10)


if __name__ == "__main__":
    unittest.main()
