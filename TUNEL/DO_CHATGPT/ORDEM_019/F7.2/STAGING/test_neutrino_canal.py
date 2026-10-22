"""Offline checks for the frozen F7.2 source channel and its fail-closed pins."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
MODULE = HERE / "bancada" / "neutrino_canal.py"
spec = importlib.util.spec_from_file_location("neutrino_canal_staged", MODULE)
assert spec and spec.loader
channel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(channel)

class NeutrinoChannelTests(unittest.TestCase):
    def test_real_sources_typed_bounds_and_no_tgl_limit(self) -> None:
        result = channel.canal()
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["local_sources"]), 6)
        self.assertEqual(len(result["primary_pdfs"]), 9)
        self.assertEqual(len(result["rows"]), 12)
        self.assertEqual(result["overall_verdict"], "SEM_LIMITE_TGL")
        self.assertEqual(result["gate_effect"], "NONE")
        self.assertTrue(result["primary_article_pdfs_custodied"])
        self.assertFalse(result["raw_experimental_data_custodied"])
        self.assertEqual(result["manifest_sha256"], channel.MANIFEST_SHA256)
        clock = result["clock_v369_context"]
        self.assertEqual(clock["statute"], "[DERIVED]")
        self.assertEqual(clock["qualification"], "projeção condicional da v369")
        self.assertEqual(clock["kind"], "CONDITIONAL_5SIGMA_PROJECTION")
        self.assertEqual(clock["source_json_path"], "core.clock_test_result_v369.five_sigma_requirement")
        source = clock["source_basis"]
        self.assertEqual(source["sha256"], "456f0ab149bb13f6997972dbfaf9c72a2891d744c22f04241eefa619e4953a95")
        self.assertEqual(source["bytes"], 4131975)
        v369 = json.loads(Path(source["path"]).read_text(encoding="utf-8"))
        requirement = v369["core"]["clock_test_result_v369"]["five_sigma_requirement"]
        self.assertEqual(clock["ghz_N_needed_exact"], requirement["ghz_N_needed"])
        self.assertEqual(clock["hbar_omega_needed_eV_exact"],
                         requirement["hbar_omega_needed_eV_at_todays_sigma"])
        self.assertEqual(clock["comparison_symbol"], "≳")
        self.assertTrue(clock["rounded_thresholds_not_exact_bounds"])
        self.assertFalse(clock["matter_interferometry_measurement"])
        self.assertFalse(clock["observed_measurement"])
        self.assertTrue(result["preregistration_required_before_nature_verdict"])
        receipt = json.loads((HERE / "STAGING_RECEIPT.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["manifest_sha256_locked"], channel.MANIFEST_SHA256)
        self.assertEqual(receipt["files"]["bancada/neutrino_fontes_f72.json"], channel.MANIFEST_SHA256)
        self.assertEqual({row["statute"] for row in result["rows"]}, {"[DECLARADO]", "[DERIVED]"})
        self.assertTrue(all(row["tau_star_limit_s"] is None and row["verdict"] == "SEM_LIMITE_TGL"
                            and row["conditional"] is True and row["exponent_measured"] is False
                            and row["raw_data_reanalysed"] is False
                            for row in result["rows"]))
        self.assertNotIn("7.780735588e-10", json.dumps(result))
        docs = result["local_documents"]
        self.assertEqual(docs["channel_power_table"]["sha256"],
                         "e848eeba67900a5812d4045c68b3005dd71a7119af2ac8e0ae4d31a0e13a6ae0")
        self.assertEqual(docs["matter_validation"]["sha256"],
                         "32f6c46a4d15b651b2b5e7d58b5c2d2d53861c092c3d1e094a4cb53c6db28b39")
        published = {row["channel"]: row for row in result["rows"]
                     if row["published_model_limit"] is not None}
        expected = {
            "FOGLI_2007": (8.1e-29, "GeV", 1.0, 95, "gamma_0", None, -2),
            "DE_ROMERI_2023_A": (7.8e-27, "GeV", 1.0, 90, "Gamma_21=Gamma_31=Gamma_32", None, -2),
            "DE_ROMERI_2023_E": (7.9e-27, "GeV", 1.0, 90, "Gamma_21 only", None, -2),
            "ORCA6_GAMMA21_NO": (2.8e-21, "GeV", 1.0, 90, "Gamma_21 profiled", "NO", -2),
            "ORCA6_GAMMA21_IO": (4.6e-21, "GeV", 1.0, 90, "Gamma_21 profiled", "IO", -2),
            "ORCA6_GAMMA31_NO": (8.4e-21, "GeV", 1.0, 90, "Gamma_31 profiled", "NO", -2),
            "ORCA6_GAMMA31_IO": (2.2e-21, "GeV", 1.0, 90, "Gamma_31 profiled", "IO", -2),
            "ICECUBE_2024_STATE_SELECTION": (1.17e-15, "eV", 1000.0, 90, "Gamma_0 state selection", None, 0),
        }
        self.assertEqual(set(published), set(expected))
        for name, wanted in expected.items():
            row = published[name]
            bound = row["published_model_limit"]
            got = (bound["value"], bound["unit"], bound["pivot_energy_GeV"],
                   bound["confidence_level_percent"], bound["gamma_channel"],
                   bound["mass_ordering"], row["energy_exponent_n"])
            self.assertEqual(got, wanted)
            self.assertTrue(row["primary_bytes_custodied"])
            self.assertTrue(row["source_basis"]["pdf_header_valid"])
            self.assertEqual(row["statute"], "[DECLARADO]")
        local = next(row for row in result["rows"] if row["channel"] == "JUNE_TGL_SIGNATURE")
        self.assertEqual(local["statute"], "[DERIVED]")
        self.assertFalse(local["primary_bytes_custodied"])

    def test_matter_channels_observables_and_prior_version(self) -> None:
        rows = {row["channel"]: row for row in channel.canal()["rows"]}
        atom = rows["ATOM_INTERFEROMETRY_CHAPMAN_1995"]
        self.assertEqual(atom["published_observation"]["recovered_lost_contrast_fraction_greater_than"], 0.60)
        self.assertEqual(atom["citation_anchor"], "p. 3, Figs. 2-3")
        molecule = rows["MOLECULE_INTERFEROMETRY_C70_2004"]
        self.assertEqual(molecule["published_observation"]["speed_m_per_s"], 190)
        self.assertEqual(molecule["published_observation"]["visibility_by_heating"],
                         [{"power_W": 0.0, "visibility_percent": 47},
                          {"power_W": 3.0, "visibility_percent": 29},
                          {"power_W": 6.0, "visibility_percent": 7},
                          {"power_W": 10.5, "visibility_percent": 0}])
        nano = rows["NANOPARTICLE_INTERFEROMETRY_PEDALINO_2026"]
        self.assertEqual(nano["published_observation"]["mass_kDa_range"], [143, 197])
        self.assertEqual(nano["published_observation"]["atom_count_greater_than"], 7000)
        self.assertEqual(nano["published_observation"]["visibility_runs"],
                         [{"mean_mass_kDa": 172, "visibility": 0.10, "uncertainty": 0.01},
                          {"mean_mass_kDa": 172, "visibility": 0.08, "uncertainty": 0.01}])
        self.assertEqual(nano["supporting_previous_version"]["name"],
                         "Pedalino_2025_preprint_arxiv_2507.21211v1.pdf")
        self.assertTrue(all(row["primary_bytes_custodied"] and row["published_model_limit"] is None
                            and row["tau_star_limit_s"] is None
                            for row in (atom, molecule, nano)))

    def test_manifest_adulteration_fails_closed(self) -> None:
        altered = json.loads(channel.MANIFEST.read_text(encoding="utf-8"))
        altered["documents"]["channel_power_table"]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "tampered.json"
            manifest.write_text(json.dumps(altered), encoding="utf-8")
            with self.assertRaisesRegex(channel.FonteRecusada, "manifest hash differs"):
                channel.canal(manifest)

    def test_regenerated_manifest_same_source_pins_fails_closed(self) -> None:
        altered = json.loads(channel.MANIFEST.read_text(encoding="utf-8"))
        altered["scope"] = "regenerated with the same pins"
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "regenerated.json"
            manifest.write_text(json.dumps(altered), encoding="utf-8")
            with self.assertRaisesRegex(channel.FonteRecusada, "manifest hash differs"):
                channel.canal(manifest)

    def test_pdf_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "source.pdf"
            original = b"%PDF-" + b"x" * 1000
            pdf.write_bytes(original)
            pin = hashlib.sha256(original).hexdigest()
            report = channel._verify_pdf(pdf, pin, len(original))
            self.assertEqual(report["sha256"], pin)
            pdf.write_bytes(original + b"changed")
            with self.assertRaisesRegex(channel.FonteRecusada, "PDF drift"):
                channel._verify_pdf(pdf, pin, len(original))

    def test_rejected_publisher_html_never_enters_primary_pdf_set(self) -> None:
        result = channel.canal()
        self.assertEqual(set(result["rejected_publisher_html"]),
                         {"Kovachy_2015_Nature_abstract.html", "Fein_2019_NaturePhysics_abstract.html"})
        self.assertTrue(all(name.endswith(".pdf") for name in result["primary_pdfs"]))
        self.assertFalse(set(result["rejected_publisher_html"]) & set(result["primary_pdfs"]))

    def test_source_ast_is_never_executed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "trap.py"
            raw = b'raise RuntimeError("EXECUTED")\n'
            source.write_bytes(raw)
            report = channel._verify_source(source, hashlib.sha256(raw).hexdigest())
            self.assertTrue(report["ast_parsed"])
            self.assertEqual(report["bytes"], len(raw))
            source.write_bytes(raw + b"# drift")
            with self.assertRaisesRegex(channel.FonteRecusada, "source hash differs"):
                channel._verify_source(source, hashlib.sha256(raw).hexdigest())

    def test_staged_mcp_tool_is_syntactically_present(self) -> None:
        import ast
        tree = ast.parse((HERE / "mcp_um.py").read_text(encoding="utf-8"))
        functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
        self.assertIn("neutrino_canal_f72", functions)

if __name__ == "__main__":
    unittest.main()
