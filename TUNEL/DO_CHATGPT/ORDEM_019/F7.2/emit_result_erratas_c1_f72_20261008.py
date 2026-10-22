"""Seal the F7.2 sidecar corrections without changing pinned sources."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V2 = ROOT / "V2_STAGING"
V3 = ROOT / "V3_STAGING"
OUT = ROOT / "RESULTADO_ERRATAS_C1_F72_20261008_V4.json"


def pin(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main() -> None:
    if OUT.exists():
        raise FileExistsError(OUT)
    receipt = json.loads((V2 / "STAGING_RECEIPT_V2.json").read_text(encoding="utf-8"))
    frozen = json.loads((ROOT / "FREEZE_DEPENDENCIAS_V2_F72_20261008.json").read_text(encoding="utf-8"))
    if receipt["status"] != "STAGED_NOT_DEPLOYED":
        raise RuntimeError("historical receipt was changed")
    for item in frozen["files"]:
        current = pin(Path(item["path"]))
        if current["sha256"] != item["sha256"] or current["bytes"] != item["bytes"]:
            raise RuntimeError(f"frozen dependency drift: {item['path']}")
    if len(frozen["files"]) != 26:
        raise RuntimeError("unexpected frozen set")

    new_paths = [
        V2 / "README_V2_STAGING.md",
        sorted(V2.glob("README_V2_STAGING.md.bak_20261008_*"))[-1],
        V2 / "STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json",
        V2 / "ERRATA_CABECALHO_TABELA_V2_20261008.md",
        ROOT / "ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md",
        V3 / "ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md",
        ROOT / "FREEZE_DEPENDENCIAS_V2_F72_20261008.json",
        ROOT / "fechar_erratas_curta_f72_20261008.py",
        ROOT / "ERRATA_LITERAL_J4B_F72_20261008.md",
    ]
    old_paths = [
        V2 / "STAGING_RECEIPT_V2.json",
        V2 / "TABELA_DE_PODER_POR_CANAL_V2.md",
        V2 / "JUNO_SOURCE_CUSTODY.json",
        V2 / "fontes_primarias" / "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf",
        ROOT / "LITERATURA_POS_JUNHO_F7_2_20261008.md",
        ROOT / "EVIDENCIA_R2_R3_V369_ORDENS_20261008_V2.md",
        ROOT / "SOURCE_MIGRATION_RECEIPT_V3.json",
        Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2\RECIBO_RATIFICACAO_DEPLOY_V2_C1_20261008.json"),
    ]
    data = {
        "schema": "iald.f7_2.c1_short_errata.v4",
        "unit": "F7.2",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "already_present": "JUNO V2, SN1987A literature, R2/R3 orders, J.4b literal, R9 VT fix and 26 copied sources were in the earlier result; not recomputed or recopied here.",
        "new_work": [
            "README V2 has additive errata and byte-identical backup of historical version",
            "V2 receipt and V2 table have adjacent sidecar errata; registered originals untouched",
            "Eq. (6) anchored to PDF III.B; Eq. (13) to IV.B; HTML IV.2 distinguished",
            "arXiv:2605.13955 classified as pre-June neutrino-loss, distinct from JUNO dephasing",
            "V3 pinned table corrected by sidecar only; copy in Bancada awaits c1 act",
            "26 protected dependencies recorded and rechecked by SHA-256",
        ],
        "process": {
            "v2_disk_deploy": "ratified after the fact by c1",
            "source_copy_26_files": "occurred without c1 act; decision pending, no further write here",
            "mcp_reloaded": False,
            "v3_channel_installed": False,
            "bancada_touched_by_this_layer": False,
            "gate_effect": "NONE",
        },
        "limits": "Published model limits are KNOWN; mapping to TGL tau-star is OPEN. Search does not prove absence of other results.",
        "frozen_dependencies": len(frozen["files"]),
        "new_artifacts": [pin(p) for p in new_paths],
        "reused_artifacts": [pin(p) for p in old_paths],
    }
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with OUT.open("xb") as stream:
        stream.write(raw)
    print(json.dumps(pin(OUT), ensure_ascii=False))


if __name__ == "__main__":
    main()
