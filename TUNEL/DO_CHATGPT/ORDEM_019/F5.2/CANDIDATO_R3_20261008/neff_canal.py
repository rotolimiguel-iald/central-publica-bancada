# -*- coding: utf-8 -*-
"""Uninstalled F5.2 R3 candidate: extract CMB-SPA Table 5 cells from pinned v1/v2."""
from __future__ import annotations

import hashlib
import importlib.util
import math
from pathlib import Path
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
R2 = HERE.parent / "CANDIDATO_R2_20261008" / "neff_canal.py"
R2_SHA256 = "ec15f89dbce1ae72041d4e971b0f4182a2997557321790556dc19f6e5a0353d5"
PAGES = {
    "v1": (Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\web\2506.20707v1.html"),
           "e43ce11f6bd9737ea93d284a9201d142dcb132c67b88dd38d532f0140aa429f7"),
    "v2": (Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2\web\2506.20707v2.html"),
           "be14d2e40592e55b0becd6cb332709e708dc094d8d46cc3c1cf8963b897d93d9"),
}
HEADERS = ("", "SPT-3G D1", "SPT+ACT", "CMB-SPA", "SPT-3G D1 + DESI")
TABLE_ID = "S7.T5.2"

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def pinned_bytes(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    actual = sha(raw)
    if actual != expected:
        raise ValueError(f"SHA-256 divergente: {path}; {actual}")
    return raw

def _r2():
    pinned_bytes(R2, R2_SHA256)
    info = importlib.util.spec_from_file_location("f52_neff_r2_pin", R2)
    if info is None or info.loader is None:
        raise ValueError("R2 candidate unavailable")
    module = importlib.util.module_from_spec(info)
    info.loader.exec_module(module)
    return module

def _math_numbers(cell) -> tuple[float, ...]:
    math_node = cell.find("math")
    if math_node is None:
        raise ValueError("CMB-SPA cell lacks MathML")
    values = tuple(float(node.get_text("", strip=True)) for node in math_node.find_all("mn"))
    if len(values) not in (2, 3) or any(not math.isfinite(v) or v <= 0 for v in values):
        raise ValueError("CMB-SPA numeric form invalid")
    return values

def extract_table5(version: str, page: Path | None = None) -> list[dict]:
    if version not in PAGES:
        raise ValueError("Only pinned v1/v2 source versions are accepted")
    canonical, expected = PAGES[version]
    page = canonical if page is None else Path(page)
    raw = pinned_bytes(page, expected)
    soup = BeautifulSoup(raw, "html.parser")
    table = soup.find("table", id=TABLE_ID)
    if table is None or table.parent is None:
        raise ValueError("Table 5 structural anchor absent")
    caption = table.parent.find(class_="ltx_caption")
    if caption is None or not caption.get_text(" ", strip=True).startswith("Table 5:"):
        raise ValueError("Table 5 caption absent")
    rows = table.find_all("tr", recursive=False)
    if len(rows) != 5:
        raise ValueError("Table 5 must contain header and four body rows")
    cells = [row.find_all(["td", "th"], recursive=False) for row in rows]
    if any(len(row) != 5 for row in cells):
        raise ValueError("Table 5 column count differs")
    headers = tuple(cell.get_text(" ", strip=True) for cell in cells[0])
    if headers != HEADERS:
        raise ValueError(f"Table 5 reader order differs: {headers}")
    if any("N eff" not in cells[i][0].get_text(" ", strip=True) for i in (1, 3)):
        raise ValueError("N_eff row labels differ")
    if any("Y P" not in cells[i][0].get_text(" ", strip=True) for i in (2, 4)):
        raise ValueError("Y_P row labels differ")
    bbn = _math_numbers(cells[1][3])
    free = _math_numbers(cells[3][3])
    if len(bbn) != 2 or len(free) != 3:
        raise ValueError("Expected symmetric BBN and asymmetric free-Yp cells")
    common = {
        "conjunto": "CMB-SPA (SPT-3G D1 + Planck + ACT)",
        "fonte": f"arXiv:2506.20707{version}, Table 5, CMB-SPA column",
        "version": version,
        "source_path": str(page),
        "source_sha256": expected,
        "table_id": TABLE_ID,
        "estatuto": "[REAL documental: valores extraídos de MathML com fonte pinada; admissão D8 e escolha X16 OPEN]",
    }
    return [
        {**common, "yp": "BBN_CONSISTENCY", "N_eff_obs": bbn[0],
         "sigma": bbn[1], "sigma_plus": bbn[1], "sigma_minus": bbn[1],
         "cell_id": cells[1][3].get("id")},
        {**common, "yp": "FREE", "N_eff_obs": free[0],
         "sigma": None, "sigma_plus": free[2], "sigma_minus": free[1],
         "cell_id": cells[3][3].get("id"),
         "nota": "assimetria publicada preservada; nenhuma compressão decisória"},
    ]

def opcoes_yp_v1_v2() -> list[dict]:
    return extract_table5("v1") + extract_table5("v2")

def canal(N_base=None, sigmas_extra=(), frozen=None, um=None) -> dict:
    """R2 computation with its candidate pinned; replace only source options by extracted cells."""
    r2 = _r2()
    kwargs = {"N_base": N_base, "sigmas_extra": sigmas_extra}
    if frozen is not None:
        kwargs["frozen"] = frozen
    if um is not None:
        kwargs["um"] = um
    r2_out = r2.canal(**kwargs)
    options = opcoes_yp_v1_v2()
    v2_options = [row for row in options if row["version"] == "v2"]
    old = r2_out["opcoes_CMB_SPA_Yp"]
    for historical, extracted in zip(old, v2_options, strict=True):
        for key in ("yp", "N_eff_obs", "sigma", "sigma_plus", "sigma_minus"):
            if historical[key] != extracted[key]:
                raise ValueError(f"R2 literal differs from extracted v2 source: {key}")
    r2_out["opcoes_CMB_SPA_Yp"] = v2_options
    r2_out["opcoes_CMB_SPA_Yp_v1_v2"] = options
    r2_out["opcoes_origem"] = "EXTRACTED_FROM_PINNED_TABLE5_MATHML_V1_AND_V2"
    r2_out["escolha_Yp"] = "[OPEN — operador X16; nenhuma linha decisória selecionada]"
    r2_out["source_admission"] = "D8_PENDING"
    r2_out["candidate_state"] = "SANDBOX_ONLY_NOT_INSTALLED"
    return r2_out