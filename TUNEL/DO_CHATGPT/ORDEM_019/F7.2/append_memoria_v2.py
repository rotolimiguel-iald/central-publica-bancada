"""Append the audited F7.2 V2 state to the four Central memory surfaces."""

from __future__ import annotations

from datetime import datetime
import hashlib
import os
from pathlib import Path
import tempfile


ROOT = Path(r"C:\IALD\Central de Patentes")
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
]
MARKER = b"<!-- F72_JUNO_V2_INSTALADO_20261008 -->"
ENTRY = """

## 08/10/2026 — F7.2: fonte JUNO de 2026 e canal V2 instalado em disco

<!-- F72_JUNO_V2_INSTALADO_20261008 -->

[REAL documental/KNOWN fonte] A análise fenomenológica de Beccaria–Ternes dos primeiros dados JUNO (arXiv:2606.13362v1, PDF local SHA-256 9212cd391d88846ee8065ac3ebf8ccb17be297417a86a22482fca858ed3be107) publicou, no cenário Γ21=Γ31, Γ32=0, n=−2 e E0=1 GeV, Γ<4,1×10⁻²⁷ GeV a 90% CL. É limite do modelo das autoras, não resultado oficial da Colaboração JUNO nem cota TGL. Fonte: https://arxiv.org/html/2606.13362 . A tabela V1 permanece intacta; a errata ao lado está em F7.2/ERRATA_JUNO_2026.md.

[REAL operacional] A V2 foi instalada somente em disco na Bancada após prévia, backup byte a byte do MCP, CAS de bytes e 11/11 testes offline. A consulta local instalada devolveu 13 linhas e 10 PDFs pinados, `tau_star_limit_s=null` em todas, `SEM_LIMITE_TGL`, gate `NONE`. F7.2/RESULTADO_V2.json SHA-256 284c22359ef71a89758a033def0b9d6cfa1af1798e511364af561dbf025f3ab0; V2_STAGING/STAGING_RECEIPT_V2.json SHA-256 10fc874e65a8cc64fb7cdc28dedd96e927dae0f57a06a683c3a382b75799f183. Mapa seq 807, quadro anotação evento 267; F7.2 segue AUDITADA até reauditoria c1.

[OPEN] Não existe tradução demonstrada do dissipador em matéria/likelihood para τ★. O processo MCP antigo não foi recarregado e a nova função não foi declarada ativa; a ligação ao `um.py` v392 e a migração das fontes pinadas para fora do túnel seguem pendentes. Nenhum dado bruto, gate ou confirmação da natureza foi produzido por esta atualização.
""".encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def append_one(path: Path) -> dict:
    before = path.read_bytes()
    if MARKER in before:
        raise ValueError(f"already appended: {path}")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = path.with_name(path.name + ".bak_" + stamp)
    with backup.open("xb") as stream:
        stream.write(before)
        stream.flush()
        os.fsync(stream.fileno())
    if backup.read_bytes() != before:
        raise OSError(f"byte backup mismatch: {path}")
    updated = before + ENTRY
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(updated):
        raise OSError(f"temporary truncated: {path}")
    if path.read_bytes() != before:
        raise OSError(f"concurrent edit before replace: {path}")
    os.replace(temporary, path)
    after = path.read_bytes()
    if after != updated or len(after) <= len(before):
        os.replace(backup, path)
        raise OSError(f"post-append mismatch: {path}")
    return {"path": str(path), "backup": str(backup), "before": digest(before), "after": digest(after)}


if __name__ == "__main__":
    for target in PATHS:
        print(append_one(target))
