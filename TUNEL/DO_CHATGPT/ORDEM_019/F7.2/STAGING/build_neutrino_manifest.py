"""Build a frozen F7.2 source manifest from validated local bytes only.

No scientific original is imported or executed. The builder checks custody
receipts, the matter-validation report and PDF signatures before writing.
Rebuilding changes the manifest SHA and requires a separate review and update
of MANIFEST_SHA256 in neutrino_canal.py.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
SOURCE_ROOT = Path(r"C:\IALD\Artigo\Haja_Luz")
PDF_ROOT = UNIT / "fontes_primarias"
CLOCK_RESULT = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\project_fisica\v369_um_absoluto.json")
OUT = HERE / "bancada" / "neutrino_fontes_f72.json"

JUNE_NAMES = (
    "tgl_neutrino_decoherence.py",
    "tgl_neutrino_exponent_test.py",
    "tgl_dephasing_falsifier.py",
    "tgl_decoherence_contour.py",
    "tgl_dephasing_systems.py",
    "tgl_paper_unified.py",
)
NEUTRINO_PDFS = {
    "Fogli_2007_arxiv_0704.2568.pdf": "NEUTRINO",
    "DeRomeri_2023_arxiv_2306.14699.pdf": "NEUTRINO",
    "ORCA6_2025_arxiv_2410.01388.pdf": "NEUTRINO",
    "IceCube_2024_arxiv_2308.00105.pdf": "NEUTRINO",
    "Coloma_2018_arxiv_1803.04438.pdf": "NEUTRINO_CONTEXT",
}
MATTER_PDFS = {
    "Chapman_1995_author.pdf": "ATOM_INTERFEROMETRY",
    "Hackermueller_2004_arxiv_quant-ph_0402146.pdf": "MOLECULE_INTERFEROMETRY",
    "Pedalino_2025_preprint_arxiv_2507.21211v1.pdf": "NANOPARTICLE_INTERFEROMETRY",
    "Pedalino_2026_published_author.pdf": "NANOPARTICLE_INTERFEROMETRY",
}
DOCS = {
    "local_review_note": UNIT / "REAPROVEITAMENTO_E_ERRATA.md",
    "local_confronted_review": UNIT / "PARECER_KIMI_CONFERIDO.md",
    "channel_power_table": UNIT / "TABELA_DE_PODER_POR_CANAL.md",
    "matter_validation": UNIT / "MATTER_SOURCE_CUSTODY_VALIDATION.json",
    "neutrino_custody": PDF_ROOT / "SOURCE_CUSTODY.json",
    "matter_custody": PDF_ROOT / "MATTER_SOURCE_CUSTODY.json",
    "clock_v369_result": CLOCK_RESULT,
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_document(path: Path) -> tuple[bytes, dict]:
    data = path.read_bytes()
    if not data:
        raise ValueError(f"empty source: {path}")
    return data, {"path": str(path), "sha256": sha256(data), "bytes": len(data)}

def json_document(path: Path) -> tuple[dict, dict]:
    data, pin = read_document(path)
    value = json.loads(data.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value, pin

def checked_pdf(name: str, receipt: dict, channel: str, validation: dict | None) -> dict:
    path = PDF_ROOT / name
    if Path(receipt.get("file", "")).resolve() != path.resolve():
        raise ValueError(f"PDF path mismatch: {name}")
    data, info = read_document(path)
    if not data.startswith(b"%PDF-") or len(data) < 1000:
        raise ValueError(f"not a substantive PDF: {name}")
    if receipt.get("sha256") != info["sha256"] or receipt.get("bytes") != info["bytes"]:
        raise ValueError(f"PDF custody mismatch: {name}")
    if receipt.get("status") != "downloaded":
        raise ValueError(f"PDF custody status not downloaded: {name}")
    if validation is not None:
        if (validation.get("content_status") != "PDF_FULL_TEXT_PARSED"
                or validation.get("receipt_kind") != "PDF_FULL_TEXT"
                or validation.get("pdf_header_valid") is not True
                or validation.get("first_page_title_verified") is not True
                or validation.get("receipt_sha256_match") is not True
                or validation.get("receipt_bytes_match") is not True
                or validation.get("sha256") != info["sha256"]
                or validation.get("bytes") != info["bytes"]
                or validation.get("channel") != channel
                or Path(validation.get("file", "")).resolve() != path.resolve()):
            raise ValueError(f"PDF matter validation mismatch: {name}")
    return {**info, "name": name, "channel": channel, "url": receipt.get("url"),
            "kind": "PDF_FULL_TEXT", "validated_matter": validation is not None}

def backup_and_replace(path: Path, encoded: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as stream:
            stream.write(old)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != old:
            raise OSError("manifest byte backup mismatch")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(encoded):
        raise OSError("manifest temporary size mismatch")
    os.replace(temporary, path)

def main() -> None:
    neutrino_receipt, _ = json_document(DOCS["neutrino_custody"])
    matter_receipt, _ = json_document(DOCS["matter_custody"])
    validation, _ = json_document(DOCS["matter_validation"])
    clock_result, clock_pin = json_document(DOCS["clock_v369_result"])
    try:
        clock_requirement = clock_result["core"]["clock_test_result_v369"]["five_sigma_requirement"]
        clock_n = clock_requirement["ghz_N_needed"]
        clock_energy = clock_requirement["hbar_omega_needed_eV_at_todays_sigma"]
        clock_platform = clock_requirement["platform"]
    except (KeyError, TypeError) as exc:
        raise ValueError("v369 clock projection path missing") from exc
    if (not isinstance(clock_n, (int, float)) or isinstance(clock_n, bool)
            or not isinstance(clock_energy, (int, float)) or isinstance(clock_energy, bool)
            or not math.isfinite(clock_n) or not math.isfinite(clock_energy)
            or clock_n <= 0 or clock_energy <= 0 or clock_platform != "sr87_kim2025"):
        raise ValueError("v369 clock projection values/platform invalid")
    clock_projection = {
        "json_path": "core.clock_test_result_v369.five_sigma_requirement",
        "ghz_N_needed": clock_n,
        "hbar_omega_needed_eV_at_todays_sigma": clock_energy,
        "platform": clock_platform,
        "kind": "CONDITIONAL_5SIGMA_PROJECTION",
    }
    if neutrino_receipt.get("schema") != "iald.f7_2.primary_source_custody.v1":
        raise ValueError("neutrino custody schema mismatch")
    if matter_receipt.get("schema") != "iald.f7_2.matter_source_custody.v1":
        raise ValueError("matter custody schema mismatch")
    if validation.get("schema") != "iald.f7_2.matter_source_custody_validation.v1":
        raise ValueError("matter validation schema mismatch")
    if validation.get("overall_verdict") != "PARTIAL_PRIMARY_CUSTODY_NO_TGL_LIMIT" or validation.get("gate_effect") != "NONE":
        raise ValueError("matter validation verdict/gate mismatch")
    if validation.get("counts", {}).get("pdf_full_text_validated") != 4 or validation.get("counts", {}).get("distinct_pdf_studies") != 3:
        raise ValueError("matter PDF count/studies mismatch")
    n_rows = {Path(row["file"]).name: row for row in neutrino_receipt["sources"] if row.get("file")}
    m_rows = {Path(row["file"]).name: row for row in matter_receipt["sources"] if row.get("file") and row.get("kind") == "PDF_FULL_TEXT"}
    v_rows = {Path(row["file"]).name: row for row in validation["sources"] if row.get("file") and row.get("content_status") == "PDF_FULL_TEXT_PARSED"}
    if set(n_rows) != set(NEUTRINO_PDFS) or set(m_rows) != set(MATTER_PDFS) or set(v_rows) != set(MATTER_PDFS):
        raise ValueError("custodied PDF allowlist mismatch")
    if not all(row.get("content_status") == "CLIENT_CHALLENGE_NOT_ARTICLE"
               for row in validation["sources"] if row.get("receipt_kind") == "PUBLISHER_ABSTRACT_HTML"):
        raise ValueError("publisher HTML status not safely rejected")
    pdfs = [checked_pdf(name, n_rows[name], channel, None) for name, channel in NEUTRINO_PDFS.items()]
    pdfs += [checked_pdf(name, m_rows[name], channel, v_rows[name]) for name, channel in MATTER_PDFS.items()]
    scripts = [{"name": name, **read_document(SOURCE_ROOT / name)[1]} for name in JUNE_NAMES]
    docs = {name: (clock_pin if name == "clock_v369_result" else read_document(path)[1])
            for name, path in DOCS.items()}
    manifest = {
        "schema": "iald.f7_2.channel_sources.v2",
        "unit": "F7.2",
        "source_root": str(SOURCE_ROOT),
        "primary_pdf_root": str(PDF_ROOT),
        "scripts": scripts,
        "documents": docs,
        "primary_pdfs": pdfs,
        "primary_article_pdfs_custodied": True,
        "raw_experimental_data_custodied": False,
        "clock_v369_projection": clock_projection,
        "rejected_publisher_html": ["Kovachy_2015_Nature_abstract.html", "Fein_2019_NaturePhysics_abstract.html"],
        "scope": "Published article bytes and local review/table; no raw-data reanalysis or TGL tau-star limit.",
    }
    encoded = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    backup_and_replace(OUT, encoded)
    print(f"{OUT} sha256={sha256(encoded)} scripts={len(scripts)} pdfs={len(pdfs)}")

if __name__ == "__main__":
    main()
