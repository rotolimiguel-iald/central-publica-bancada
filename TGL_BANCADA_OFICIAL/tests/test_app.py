import math
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import app


class BenchTests(unittest.TestCase):
    def test_historical_d9_report_keeps_uncalibrated_sigma_out(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            source = Path(directory) / "model.py"
            source.write_text("# source fixture\n", encoding="utf-8")
            body = {"name": "D9_DESI_DR2_BAO", "N_measurements": 13, "DOF": 11,
                    "LCDM_bestfit": {"Om0": 0.3, "rd_Mpc": 147.0, "chi2": 10.0, "chi2_reduced": 10 / 11},
                    "TGL_bestfit": {"Om0": 0.31, "rd_Mpc": 146.0, "chi2": 10.2, "chi2_reduced": 10.2 / 11},
                    "delta_chi2_TGL_minus_LCDM": 0.2,
                    "effective_tension_sigma": 0.4, "verdict": "PASS"}
            report.write_text(json.dumps({"main_body": {"D9": body}}), encoding="utf-8")
            with patch.object(app, "BAO_D9_REPORT", report), patch.object(app, "BAO_D9_SOURCE", source):
                result = app.read_bao_report()
                self.assertEqual(result["status"], "HISTORICAL_REPORT_NOT_REEXECUTED")
                self.assertEqual(result["delta_chi2_tgl_minus_lcdm"], 0.2)
                self.assertNotIn("effective_tension_sigma", result)
                self.assertNotIn("verdict", result)
                body["delta_chi2_TGL_minus_LCDM"] = 9.0
                report.write_text(json.dumps({"main_body": {"D9": body}}), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "does not match"):
                    app.read_bao_report()

    def test_index_has_traceable_modules(self):
        index = app.load_index()
        self.assertEqual(index["release"], "v368")
        self.assertIn("modules", index)
        self.assertGreater(len(index["modules"]), 0)

    def test_prior_protocols_are_indexed_without_replay_claim(self):
        records = app.list_protocols()
        self.assertEqual(len(records), 28)
        self.assertEqual({r["target"] for r in records},
                         {f"A{i}" for i in range(9)} | {f"T{i:02d}" for i in range(1, 20)})
        self.assertTrue(all(r["replay_status"] == "NOT_CONNECTED_TO_THIS_BENCH" for r in records))

    def test_chain_uses_input_constant(self):
        values = app.calculate({"operation": "identity_chain"})["values"]
        self.assertAlmostEqual(values["beta"], app.ALPHA_FINE_CODATA_2018 * math.sqrt(math.e))
        self.assertAlmostEqual(values["reflection_probability"] + values["transmission_probability"], 1)

    def test_dephasing_is_conditional_and_monotone(self):
        result = app.calculate({"operation": "dephasing", "omega_rad_s": 2.0, "tau_s": 0.3, "duration_s": 4.0})
        self.assertEqual(result["status"], "CONDITIONAL_MODEL_CALCULATION")
        curve = result["values"]["curve"]
        self.assertEqual(curve[0], 1.0)
        self.assertTrue(all(a >= b for a, b in zip(curve, curve[1:])))

    def test_invalid_and_unlisted_execution_refused(self):
        with self.assertRaises(ValueError):
            app.calculate({"operation": "dephasing", "omega_rad_s": -1, "tau_s": 1, "duration_s": 1})
        with self.assertRaises(ValueError):
            app.calculate({"operation": "shell", "command": "anything"})
        with self.assertRaises(ValueError):
            app.calculate({"operation": "dephasing", "omega_rad_s": float("nan"), "tau_s": 1, "duration_s": 1})

    def test_run_ledger_is_append_only(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(app, "DB", Path(directory) / "runs.db"):
            app.initialize_db()
            with closing(sqlite3.connect(app.DB)) as conn, conn:
                conn.execute("INSERT INTO runs(created_utc, operation, parameters_json, result_json, source_sha256, status) VALUES (?,?,?,?,?,?)",
                             (app.utc_now(), "identity_chain", "{}", "{}", "hash", "DERIVED_WITH_INPUT"))
                with self.assertRaises(sqlite3.IntegrityError):
                    conn.execute("UPDATE runs SET status='CONFIRMED' WHERE id=1")

    def test_inquiry_links_existing_catalogs_without_promoting_proof(self):
        result = app.investigate(app.load_index(), {
            "question": "Ward e GWOSC: onde encontro a relação?",
            "hypothesis": "A rota tem um observável definido",
            "falsifier": "A rota não define observável",
            "alternative": "A relação é apenas uma identidade formal",
            "instrumental": "O catálogo pode não conter dados compatíveis",
            "discriminator": "Conferir a previsão quantitativa e a sensibilidade do dado",
        })
        self.assertEqual(result["status"], "EXPLORATORY_SOURCE_MAP")
        self.assertGreater(result["formal_total"], 0)
        self.assertTrue(any("GWOSC" in item["label"] for item in result["datasets"]))
        self.assertTrue(all(item["status"] == "SOURCE_LOCATOR_NOT_RECOMPILED" for item in result["formal"]))
        self.assertEqual(result["open_items"], [])
        self.assertEqual(result["analysis_stage"], "EXPLORATORY_NOT_PREREGISTERED")

    def test_inquiry_requires_specific_question_and_immutable_ledger(self):
        with self.assertRaises(ValueError):
            app.investigate(app.load_index(), {"question": "o?"})
        with tempfile.TemporaryDirectory() as directory, patch.object(app, "DB", Path(directory) / "runs.db"):
            app.initialize_db()
            with closing(sqlite3.connect(app.DB)) as conn, conn:
                conn.execute("INSERT INTO inquiries(created_utc, question, hypothesis, falsifier, result_json, source_sha256, status) VALUES (?,?,?,?,?,?,?)",
                             (app.utc_now(), "Ward e GWOSC", "", "", "{}", "hash", "EXPLORATORY_SOURCE_MAP"))
                with self.assertRaises(sqlite3.IntegrityError):
                    conn.execute("UPDATE inquiries SET status='PHYSICALLY_CONFIRMED' WHERE id=1")
                conn.execute("INSERT INTO inquiry_events(created_utc, inquiry_id, event_type, note) VALUES (?,?,?,?)",
                             (app.utc_now(), 1, "ERRATUM", "Correção ao lado"))
                with self.assertRaises(sqlite3.IntegrityError):
                    conn.execute("DELETE FROM inquiry_events WHERE id=1")

    def test_namespace_word_does_not_match_entire_tower(self):
        index = app.load_index()
        result = app.investigate(index, {"question": "Ringdown GWTC3 na TGL: qual dado?"})
        self.assertLess(result["formal_total"], len(index["modules"]) // 2)
        self.assertTrue(any("GWTC-3" in item["label"] for item in result["datasets"]))


if __name__ == "__main__":
    unittest.main()
