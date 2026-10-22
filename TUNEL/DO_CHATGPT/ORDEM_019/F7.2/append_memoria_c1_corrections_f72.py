"""Append the F7.2 c1 corrections to four Central memory surfaces safely."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

UNIT = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes")
RESULT = UNIT / "RESULTADO_CORRECOES_C1_F72_20261008.json"
RECEIPT = UNIT / "MEMORY_CORRECTIONS_RECEIPT_F72_20261008.json"
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    UNIT.parent / "AVISO_GERENCIA.md",
]
MARKER = b"<!-- F72_C1_CORRECTIONS_20261008 -->"


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def append_one(path: Path, entry: bytes) -> dict:
    before = path.read_bytes()
    if not before or MARKER in before:
        raise ValueError(f"empty or already appended: {path}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
    backup = path.with_name(path.name + ".bak_" + stamp)
    with backup.open("xb") as stream:
        stream.write(before)
        stream.flush()
        os.fsync(stream.fileno())
    if backup.read_bytes() != before:
        raise OSError(f"backup differs: {path}")
    updated = before + entry
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(updated) or path.read_bytes() != before:
        raise OSError(f"temporary or source drift: {path}")
    os.replace(temporary, path)
    after = path.read_bytes()
    if after != updated or len(after) <= len(before):
        os.replace(backup, path)
        raise OSError(f"post-append mismatch: {path}")
    return {"path": str(path), "backup": str(backup), "before_sha256": digest(before),
            "after_sha256": digest(after), "before_bytes": len(before), "after_bytes": len(after)}


def main() -> None:
    if RECEIPT.exists():
        raise ValueError(f"receipt already exists: {RECEIPT}")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    if result["unit"] != "F7.2" or result["R8"]["source_files_copied"] != 26:
        raise ValueError("unexpected F7.2 result")
    result_hash = digest(RESULT.read_bytes())
    entry = f"""

## 08/10/2026 — F7.2: ressalvas c1 R1–R6/R8/R9 entregues para reauditoria

<!-- F72_C1_CORRECTIONS_20261008 -->

[REAL documental] O Nós vivo foi consultado. A V2 já continha o limite publicado de Beccaria–Ternes (JUNO, n=−2, Γ₂₁=Γ₃₁<4,1×10⁻²⁷ GeV, E₀=1 GeV, 90% CL), as âncoras R4 e os estatutos R5. A c1 ratificou a instalação V2 em disco depois de registrar o desvio de processo. A busca nova `F7.2/LITERATURA_POS_JUNHO_F7_2_20261008.md` custodiou SN1987A, mas sua cota de 10⁻⁴¹ GeV é de um modelo com perda de fluxo, distinto do dephasing JUNO [KNOWN]; nenhuma cota τ★ TGL resulta daí [OPEN].

[DERIVED condicional] A leitura completa da v369 está em `F7.2/EVIDENCIA_R2_R3_V369_ORDENS_20261008_V2.md`: Sr precisa fechar 12,46 ordens na projeção 5σ; Mössbauer ⁶⁷Zn tem cota apenas NOMINAL a 9,27 ordens; neutrinos ficam 38,07–45,82 ordens acima da taxa TGL sob τ★=tₚ, Kfac=1 e vácuo (JUNO Γ₂₁ a 39,77). P3_NO_LOCAL_OBSERVABLE, kbar_rest_mass_excluded e MODULAR_LAB_BRIDGE_OPEN permanecem tipados; ω efetivo, operador→visibilidade e σ de franjas seguem [OPEN].

[REAL operacional] O literal `'tau_star_bound_neutrino_s': 7.8e-10` na linha 18393 de `tgl_paper_unified.py` foi corrigido **ao lado**, sem editar o original, em `F7.2/ERRATA_LITERAL_J4B_F72_20261008.md`. As 26 fontes da F7.2 foram copiadas e conferidas por SHA-256 em `C:\\IALD\\Bancada_Um\\fontes_externas\\F7.2`; `F7.2/SOURCE_MIGRATION_RECEIPT_V3.json` prova que MCP, canais e manifestos existentes mantiveram os bytes. Módulo/manifesto V3 têm pino novo e validação fail-closed no staging; aguardam ato da c1 para instalar. `STAGING/README_DEPLOY.md` teve o único byte 0x0b corrigido para `\\v`, com backup byte a byte. O arquivo nomeado `AUDITORIA_F7_2_C1_20261007.md` contém um script Python; o relatório Markdown real está em `AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md`.

[CUSTÓDIA] `F7.2/RESULTADO_CORRECOES_C1_F72_20261008.json` SHA-256 {result_hash}; mapa seq 835; quadro evento 300, F7.2 ENTREGUE para reauditoria c1. Nenhum processo MCP recarregado, nenhum `um.py` editado, nenhum dado bruto aberto e nenhum gate movido. `NOT_FALSIFIED` não é creditação.
""".encode("utf-8")
    rows = [append_one(path, entry) for path in PATHS]
    receipt = {"schema": "iald.f7_2.memory_c1_corrections.v1", "unit": "F7.2",
               "result_sha256": result_hash, "map_seq": 835, "board_event": 300, "rows": rows}
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECEIPT.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"receipt": str(RECEIPT), "sha256": digest(encoded), "surfaces": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
