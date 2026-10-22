"""F7.2 read-only channel: published-model and interferometry provenance.

The module checks frozen script, document and primary-PDF bytes. It never imports
the June scripts, runs external programs, contacts a provider, or computes a TGL
tau-star bound. Published values belong to the cited articles' own models.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re

MANIFEST = Path(__file__).with_name("neutrino_fontes_f72.json")
MANIFEST_SHA256 = "abc36292630087de410cbb7300507fbed3d3320d6cd4ae5c3d4887af2b850a33"  # reviewed frozen manifest bytes
SOURCE_ROOT = Path(r"C:\IALD\Artigo\Haja_Luz")
UNIT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F7.2")
PDF_ROOT = UNIT / "fontes_primarias"
SCRIPT_NAMES = frozenset({
    "tgl_neutrino_decoherence.py", "tgl_neutrino_exponent_test.py",
    "tgl_dephasing_falsifier.py", "tgl_decoherence_contour.py",
    "tgl_dephasing_systems.py", "tgl_paper_unified.py",
})
DOC_PATHS = {
    "local_review_note": UNIT / "REAPROVEITAMENTO_E_ERRATA.md",
    "local_confronted_review": UNIT / "PARECER_KIMI_CONFERIDO.md",
    "channel_power_table": UNIT / "TABELA_DE_PODER_POR_CANAL.md",
    "matter_validation": UNIT / "MATTER_SOURCE_CUSTODY_VALIDATION.json",
    "neutrino_custody": PDF_ROOT / "SOURCE_CUSTODY.json",
    "matter_custody": PDF_ROOT / "MATTER_SOURCE_CUSTODY.json",
    "clock_v369_result": Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\v369_um_absoluto.json"),
}
PDF_CHANNELS = {
    "Fogli_2007_arxiv_0704.2568.pdf": "NEUTRINO",
    "DeRomeri_2023_arxiv_2306.14699.pdf": "NEUTRINO",
    "ORCA6_2025_arxiv_2410.01388.pdf": "NEUTRINO",
    "IceCube_2024_arxiv_2308.00105.pdf": "NEUTRINO",
    "Coloma_2018_arxiv_1803.04438.pdf": "NEUTRINO_CONTEXT",
    "Chapman_1995_author.pdf": "ATOM_INTERFEROMETRY",
    "Hackermueller_2004_arxiv_quant-ph_0402146.pdf": "MOLECULE_INTERFEROMETRY",
    "Pedalino_2025_preprint_arxiv_2507.21211v1.pdf": "NANOPARTICLE_INTERFEROMETRY",
    "Pedalino_2026_published_author.pdf": "NANOPARTICLE_INTERFEROMETRY",
}
MATTER_PDF_NAMES = frozenset({
    "Chapman_1995_author.pdf",
    "Hackermueller_2004_arxiv_quant-ph_0402146.pdf",
    "Pedalino_2025_preprint_arxiv_2507.21211v1.pdf",
    "Pedalino_2026_published_author.pdf",
})
REJECTED_HTML = frozenset({
    "Kovachy_2015_Nature_abstract.html",
    "Fein_2019_NaturePhysics_abstract.html",
})
SHA256 = re.compile(r"^[0-9a-f]{64}$")

class FonteRecusada(ValueError):
    """A pinned local input failed closed."""

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _verify_source(path: Path, pin: str, *, python_source: bool = True) -> dict:
    """Hash and optionally AST-parse local bytes, without importing a script."""
    if not isinstance(pin, str) or not SHA256.fullmatch(pin):
        raise FonteRecusada(f"invalid SHA-256 pin for {path}")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FonteRecusada(f"source unavailable: {path}: {exc}") from exc
    actual = _sha256(raw)
    if actual != pin:
        raise FonteRecusada(f"source hash differs: {path}: actual={actual} pin={pin}")
    if python_source:
        try:
            ast.parse(raw.decode("utf-8-sig"), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            raise FonteRecusada(f"source cannot be parsed: {path}: {exc}") from exc
    return {"path": str(path), "sha256": actual, "bytes": len(raw), "ast_parsed": python_source}

def _verify_pdf(path: Path, pin: str, expected_bytes: int) -> dict:
    """Stream and verify one substantive local PDF; no PDF code is executed."""
    if not isinstance(pin, str) or not SHA256.fullmatch(pin):
        raise FonteRecusada(f"invalid PDF SHA-256 pin for {path}")
    if not isinstance(expected_bytes, int) or expected_bytes < 1000:
        raise FonteRecusada(f"invalid PDF byte count for {path}")
    digest = hashlib.sha256()
    count = 0
    try:
        with path.open("rb") as stream:
            header = stream.read(5)
            if header != b"%PDF-":
                raise FonteRecusada(f"PDF header invalid: {path}")
            digest.update(header)
            count += len(header)
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
                count += len(block)
    except OSError as exc:
        raise FonteRecusada(f"PDF unavailable: {path}: {exc}") from exc
    actual = digest.hexdigest()
    if actual != pin or count != expected_bytes:
        raise FonteRecusada(f"PDF drift: {path}: actual={actual}/{count} pin={pin}/{expected_bytes}")
    return {"path": str(path), "sha256": actual, "bytes": count, "pdf_header_valid": True}

def _load_sources(manifest_path: Path) -> tuple[dict[str, dict], dict[str, dict], dict[str, dict], dict, str]:
    try:
        manifest_raw = manifest_path.read_bytes()
    except OSError as exc:
        raise FonteRecusada(f"manifest unavailable: {manifest_path}: {exc}") from exc
    manifest_hash = _sha256(manifest_raw)
    if manifest_hash != MANIFEST_SHA256:
        raise FonteRecusada(f"manifest hash differs: actual={manifest_hash} pin={MANIFEST_SHA256}")
    try:
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise FonteRecusada(f"manifest invalid: {exc}") from exc
    if manifest.get("schema") != "iald.f7_2.channel_sources.v2" or manifest.get("unit") != "F7.2":
        raise FonteRecusada("manifest schema/unit mismatch")
    if (manifest.get("primary_article_pdfs_custodied") is not True
            or manifest.get("raw_experimental_data_custodied") is not False):
        raise FonteRecusada("manifest article/raw-data custody mismatch")
    if Path(manifest.get("source_root", "")).resolve() != SOURCE_ROOT.resolve():
        raise FonteRecusada("script root mismatch")
    if Path(manifest.get("primary_pdf_root", "")).resolve() != PDF_ROOT.resolve():
        raise FonteRecusada("PDF root mismatch")
    if frozenset(manifest.get("rejected_publisher_html", [])) != REJECTED_HTML:
        raise FonteRecusada("publisher HTML exclusion mismatch")
    script_entries = manifest.get("scripts")
    if not isinstance(script_entries, list) or len(script_entries) != len(SCRIPT_NAMES):
        raise FonteRecusada("script count mismatch")
    if frozenset(entry.get("name") for entry in script_entries) != SCRIPT_NAMES:
        raise FonteRecusada("script allowlist mismatch")
    scripts = {}
    for entry in script_entries:
        name = entry["name"]
        path = Path(entry.get("path", ""))
        if path.resolve() != (SOURCE_ROOT / name).resolve() or name in scripts:
            raise FonteRecusada(f"script path/duplicate mismatch: {name}")
        result = _verify_source(path, entry.get("sha256"))
        if result["bytes"] != entry.get("bytes"):
            raise FonteRecusada(f"script byte count mismatch: {name}")
        scripts[name] = result
    doc_entries = manifest.get("documents")
    if not isinstance(doc_entries, dict) or set(doc_entries) != set(DOC_PATHS):
        raise FonteRecusada("document allowlist mismatch")
    docs = {}
    for name, expected_path in DOC_PATHS.items():
        entry = doc_entries[name]
        path = Path(entry.get("path", ""))
        if path.resolve() != expected_path.resolve():
            raise FonteRecusada(f"document path mismatch: {name}")
        result = _verify_source(path, entry.get("sha256"), python_source=False)
        if result["bytes"] != entry.get("bytes"):
            raise FonteRecusada(f"document byte count mismatch: {name}")
        docs[name] = result
    pdf_entries = manifest.get("primary_pdfs")
    if not isinstance(pdf_entries, list) or len(pdf_entries) != len(PDF_CHANNELS):
        raise FonteRecusada("PDF count mismatch")
    if frozenset(entry.get("name") for entry in pdf_entries) != frozenset(PDF_CHANNELS):
        raise FonteRecusada("PDF allowlist mismatch")
    pdfs = {}
    for entry in pdf_entries:
        name = entry["name"]
        path = Path(entry.get("path", ""))
        if path.resolve() != (PDF_ROOT / name).resolve() or name in pdfs:
            raise FonteRecusada(f"PDF path/duplicate mismatch: {name}")
        if (entry.get("kind") != "PDF_FULL_TEXT"
                or entry.get("channel") != PDF_CHANNELS[name]
                or entry.get("validated_matter") is not (name in MATTER_PDF_NAMES)):
            raise FonteRecusada(f"PDF metadata mismatch: {name}")
        url = entry.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            raise FonteRecusada(f"PDF URL invalid: {name}")
        pdfs[name] = {**_verify_pdf(path, entry.get("sha256"), entry.get("bytes")),
                      "name": name, "channel": PDF_CHANNELS[name], "url": url,
                      "matter_validation": name in MATTER_PDF_NAMES}
    projection = manifest.get("clock_v369_projection")
    if (not isinstance(projection, dict)
            or projection.get("json_path") != "core.clock_test_result_v369.five_sigma_requirement"
            or projection.get("kind") != "CONDITIONAL_5SIGMA_PROJECTION"
            or projection.get("platform") != "sr87_kim2025"):
        raise FonteRecusada("v369 projection metadata mismatch")
    clock_path = DOC_PATHS["clock_v369_result"]
    try:
        clock_raw = clock_path.read_bytes()
        if (_sha256(clock_raw) != docs["clock_v369_result"]["sha256"]
                or len(clock_raw) != docs["clock_v369_result"]["bytes"]):
            raise FonteRecusada("v369 result changed between verification and parse")
        clock_data = json.loads(clock_raw.decode("utf-8"))
        requirement = clock_data["core"]["clock_test_result_v369"]["five_sigma_requirement"]
        n_exact = requirement["ghz_N_needed"]
        energy_exact = requirement["hbar_omega_needed_eV_at_todays_sigma"]
        platform = requirement["platform"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise FonteRecusada(f"v369 projection path unreadable: {exc}") from exc
    if (type(n_exact) not in (int, float) or type(energy_exact) not in (int, float)
            or n_exact <= 0 or energy_exact <= 0
            or projection.get("ghz_N_needed") != n_exact
            or projection.get("hbar_omega_needed_eV_at_todays_sigma") != energy_exact
            or platform != "sr87_kim2025"):
        raise FonteRecusada("v369 projection values mismatch")
    return scripts, docs, pdfs, projection, manifest_hash

def canal(manifest_path: str | Path = MANIFEST) -> dict:
    """Return a read-only, source-pinned table; never infer a TGL limit."""
    scripts, docs, pdfs, clock_projection, manifest_hash = _load_sources(Path(manifest_path))
    table = docs["channel_power_table"]
    def model_row(identifier: str, exponent: int, value: float, unit: str,
                  relation: str, pivot_gev: float, cl_percent: int,
                  gamma_channel: str, ordering: str | None, pdf_name: str,
                  anchor: str, scenario: str) -> dict:
        source = pdfs[pdf_name]
        return {
            "channel": identifier,
            "energy_exponent_n": exponent,
            "published_model_limit": {
                "value": value, "unit": unit, "relation": relation,
                "pivot_energy_GeV": pivot_gev, "confidence_level_percent": cl_percent,
                "gamma_channel": gamma_channel, "mass_ordering": ordering,
            },
            "published_observation": None,
            "model_scenario": scenario,
            "external_reference": source["url"],
            "source_basis": source,
            "citation_anchor": anchor,
            "local_table_basis": table,
            "statute": "[DECLARADO]",
            "primary_bytes_custodied": True,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        }
    def matter_row(identifier: str, pdf_name: str, anchor: str, observation: dict,
                   scenario: str, prior_version: str | None = None) -> dict:
        source = pdfs[pdf_name]
        return {
            "channel": identifier,
            "energy_exponent_n": None,
            "published_model_limit": None,
            "published_observation": observation,
            "model_scenario": scenario,
            "external_reference": source["url"],
            "source_basis": source,
            "citation_anchor": anchor,
            "local_table_basis": table,
            "supporting_previous_version": pdfs[prior_version] if prior_version else None,
            "statute": "[DECLARADO]",
            "primary_bytes_custodied": True,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        }
    rows = [
        {
            "channel": "JUNE_TGL_SIGNATURE",
            "energy_exponent_n": -2,
            "published_model_limit": None,
            "published_observation": None,
            "model_scenario": "Vacuum scaling conditional on constant mass gap, tau_star and Kfac.",
            "external_reference": None,
            "source_basis": scripts["tgl_neutrino_decoherence.py"],
            "citation_anchor": "local June script, model formula",
            "local_table_basis": table,
            "statute": "[DERIVED]",
            "primary_bytes_custodied": False,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        },
        model_row("FOGLI_2007", -2, 8.1e-29, "GeV", "<", 1.0, 95,
                  "gamma_0", None, "Fogli_2007_arxiv_0704.2568.pdf", "Eq. 3; Table I",
                  "Solar+KamLAND with Fogli's solar matter dissipator; not pure dephasing."),
        model_row("DE_ROMERI_2023_A", -2, 7.8e-27, "GeV", "<", 1.0, 90,
                  "Gamma_21=Gamma_31=Gamma_32", None, "DeRomeri_2023_arxiv_2306.14699.pdf",
                  "Table 3; section V", "Current KamLAND bound in model A."),
        model_row("DE_ROMERI_2023_E", -2, 7.9e-27, "GeV", "<", 1.0, 90,
                  "Gamma_21 only", None, "DeRomeri_2023_arxiv_2306.14699.pdf",
                  "Table 3", "Current KamLAND bound in model E."),
        model_row("ORCA6_GAMMA21_NO", -2, 2.8e-21, "GeV", "<", 1.0, 90,
                  "Gamma_21 profiled", "NO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eq. 10", "ORCA6 normal ordering."),
        model_row("ORCA6_GAMMA21_IO", -2, 4.6e-21, "GeV", "<", 1.0, 90,
                  "Gamma_21 profiled", "IO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eq. 10", "ORCA6 inverted ordering."),
        model_row("ORCA6_GAMMA31_NO", -2, 8.4e-21, "GeV", "<", 1.0, 90,
                  "Gamma_31 profiled", "NO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eq. 10", "ORCA6 normal ordering."),
        model_row("ORCA6_GAMMA31_IO", -2, 2.2e-21, "GeV", "<", 1.0, 90,
                  "Gamma_31 profiled", "IO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eq. 10", "ORCA6 inverted ordering."),
        model_row("ICECUBE_2024_STATE_SELECTION", 0, 1.17e-15, "eV", "<=", 1000.0, 90,
                  "Gamma_0 state selection", None, "IceCube_2024_arxiv_2308.00105.pdf",
                  "Table 1", "IceCube n=0, not a direct n=-2 test."),
        matter_row("ATOM_INTERFEROMETRY_CHAPMAN_1995", "Chapman_1995_author.pdf",
                   "p. 3, Figs. 2-3",
                   {"contrast_near_half_scattered_photon_wavelength": "approximately_zero",
                    "recovered_lost_contrast_fraction_greater_than": 0.60},
                   "Photon scattering and angular selection, not a gravitational dephasing bound."),
        matter_row("MOLECULE_INTERFEROMETRY_C70_2004",
                   "Hackermueller_2004_arxiv_quant-ph_0402146.pdf", "p. 2, Fig. 2",
                   {"material": "C70", "speed_m_per_s": 190,
                    "visibility_by_heating": [
                        {"power_W": 0.0, "visibility_percent": 47},
                        {"power_W": 3.0, "visibility_percent": 29},
                        {"power_W": 6.0, "visibility_percent": 7},
                        {"power_W": 10.5, "visibility_percent": 0},
                    ]},
                   "Thermal-emission decoherence in the article's apparatus."),
        matter_row("NANOPARTICLE_INTERFEROMETRY_PEDALINO_2026",
                   "Pedalino_2026_published_author.pdf", "pp. 1-3, Fig. 2",
                   {"atom_count_greater_than": 7000, "mass_kDa_range": [143, 197],
                    "visibility_runs": [
                        {"mean_mass_kDa": 172, "visibility": 0.10, "uncertainty": 0.01},
                        {"mean_mass_kDa": 172, "visibility": 0.08, "uncertainty": 0.01},
                    ]},
                   "Published nanoparticle interferometry; visibility limited in part by photodepletion.",
                   prior_version="Pedalino_2025_preprint_arxiv_2507.21211v1.pdf"),
    ]
    return {
        "ok": True, "unit": "F7.2", "mode": "READ_ONLY_SOURCE_PROVENANCE",
        "manifest_sha256": manifest_hash, "local_sources": scripts,
        "local_documents": docs, "primary_pdfs": pdfs,
        "primary_article_pdfs_custodied": True,
        "raw_experimental_data_custodied": False,
        "rejected_publisher_html": sorted(REJECTED_HTML),
        "clock_v369_context": {
            "statute": "[DERIVED]",
            "qualification": "projeção condicional da v369",
            "kind": "CONDITIONAL_5SIGMA_PROJECTION",
            "source_json_path": clock_projection["json_path"],
            "platform": clock_projection["platform"],
            "ghz_N_needed_exact": clock_projection["ghz_N_needed"],
            "hbar_omega_needed_eV_exact": clock_projection["hbar_omega_needed_eV_at_todays_sigma"],
            "comparison_symbol": "≳",
            "GHZ_N_approx": 1690000,
            "hbar_omega_MeV_approx": 3.0,
            "rounded_thresholds_not_exact_bounds": True,
            "matter_interferometry_measurement": False,
            "observed_measurement": False,
            "source_basis": docs["clock_v369_result"],
            "interpretation_basis": table,
        },
        "preregistration_required_before_nature_verdict": True,
        "rows": rows, "overall_verdict": "SEM_LIMITE_TGL",
        "gate_effect": "NONE", "not_falsified_is_not_confirmed": True,
    }
