import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import data_lab
import treatment
import treatment_coverage


def item(identifier, fmt, size, *, name=None):
    return {"id": identifier, "name": name or f"{identifier}{fmt}",
            "path": f"C:/allowlisted/{identifier}{fmt}", "group": "fixture",
            "bytes": size, "format": fmt}


class CoverageReportTests(unittest.TestCase):
    def test_totals_routes_and_schema_statutes(self):
        catalog = [item("a", ".fits", 10), item("b", ".npz", 20),
                   item("c", ".txt", 30),
                   item("d", ".txt", 40, name=data_lab.BAO_COV)]
        with patch.object(data_lab, "catalog", return_value=catalog), \
             patch.object(treatment, "record", side_effect=AssertionError("schema read")), \
             patch.object(treatment, "edge_fingerprint", side_effect=AssertionError("unique size")):
            report = treatment_coverage.coverage_report()

        self.assertEqual(report["catalog"]["files"], 4)
        self.assertEqual(report["catalog"]["bytes"], 100)
        self.assertEqual(sum(row["files"] for row in report["formats"].values()), 4)
        self.assertEqual(sum(row["bytes"] for row in report["formats"].values()), 100)
        self.assertEqual(sum(row["files"] for row in report["reader_routes"].values()), 4)
        self.assertEqual(sum(row["bytes"] for row in report["reader_routes"].values()), 100)
        self.assertEqual(report["reader_routes"]["READY"]["files"], 2)
        self.assertEqual(report["reader_routes"]["PENDING"]["files"], 2)
        self.assertEqual(report["formats"][".txt"]["reader_route"], "MIXED")
        self.assertEqual(report["schema_validation_status"], "NOT_CHECKED_PER_FILE")
        self.assertEqual(report["statistical_independence_status"], "NOT_ESTABLISHED")
        self.assertEqual(report["possible_duplicates"]["groups"], [])

    def test_only_equal_size_files_are_fingerprinted_as_candidates(self):
        catalog = [item("a", ".csv", 10), item("b", ".fits", 10),
                   item("c", ".h5", 10), item("d", ".npz", 99)]
        digests = {"a": "same", "b": "same", "c": "different"}

        def fingerprint(path):
            return {"sha256": digests[path.stem]}

        with patch.object(data_lab, "catalog", return_value=catalog), \
             patch.object(Path, "stat", return_value=SimpleNamespace(st_size=10)), \
             patch.object(treatment, "edge_fingerprint", side_effect=fingerprint) as mocked:
            report = treatment_coverage.coverage_report()

        self.assertEqual(mocked.call_count, 3)
        duplicates = report["possible_duplicates"]
        self.assertEqual(duplicates["same_size_candidate_files"], 3)
        self.assertEqual(duplicates["fingerprinted_files"], 3)
        self.assertEqual(len(duplicates["groups"]), 1)
        self.assertEqual({entry["id"] for entry in duplicates["groups"][0]["files"]}, {"a", "b"})
        self.assertEqual(duplicates["groups"][0]["bytes_each"], 10)
        self.assertIn("CANDIDATES_ONLY", duplicates["status"])
        self.assertIn("NOT_FULL_FILE_HASH", duplicates["method"])

    def test_limit_and_changed_file_remain_visible(self):
        catalog = [item(str(index), ".hdf5", 12) for index in range(5)]
        def stat(path):
            return SimpleNamespace(st_size=13 if path.stem == "0" else 12)

        with patch.object(data_lab, "catalog", return_value=catalog), \
             patch.object(treatment_coverage, "MAX_FINGERPRINT_FILES", 3), \
             patch.object(Path, "stat", autospec=True, side_effect=stat), \
             patch.object(treatment, "edge_fingerprint", return_value={"sha256": "same"}) as mocked:
            report = treatment_coverage.coverage_report()

        duplicates = report["possible_duplicates"]
        self.assertEqual(duplicates["same_size_candidate_files"], 5)
        self.assertEqual(duplicates["fingerprint_attempted_files"], 3)
        self.assertEqual(duplicates["fingerprinted_files"], 2)
        self.assertEqual(duplicates["limit_skipped_files"], 2)
        self.assertEqual(duplicates["changed_or_unreadable"], [{"id": "0", "reason": "SIZE_CHANGED"}])
        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(report["schema_validation_status"], "NOT_CHECKED_PER_FILE")


if __name__ == "__main__":
    unittest.main()
