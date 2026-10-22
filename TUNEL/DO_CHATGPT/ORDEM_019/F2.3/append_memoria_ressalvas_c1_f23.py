"""Append the F2.3 c1 audit errata to four memory surfaces with byte backups."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(r"C:\IALD\Central de Patentes")
UNIT = Path(__file__).resolve().parent
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3\AUDITORIA_F2_3_C1_20261007.md")
RECEIPT = UNIT / "MEMORIA_RESSALVAS_C1_F23_20261008.json"
MARKER = b"<!-- F23_C1_AUDIT_ERRATA_20261008 -->"
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
]


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def append_one(path: Path, addition: bytes) -> dict:
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
        raise OSError(f"backup mismatch: {path}")
    updated = before + addition
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(updated) or path.read_bytes() != before:
        raise OSError(f"source or temporary drift: {path}")
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
    audit_hash = digest(AUDIT.read_bytes())
    if audit_hash != "f718620ec89c61d408ba9bf03ac0cfc1b53f31aa6486f57fae41d183e3a86624":
        raise ValueError("unexpected c1 audit hash")
    addition = f"""

## 08/10/2026 — F2.3: errata ao lado da auditoria c1, seq 804

<!-- F23_C1_AUDIT_ERRATA_20261008 -->

[REAL documental] O trecho F2.3 anterior continua como história. Sua frase «revisão independente de tipos e log» tinha estatuto [DECLARADO] naquele momento, pois não trouxe artefato dessa revisão. A auditoria cética posterior da c1 é [REAL] por seu relatório `C:\\IALD\\PROGRAMA_IALD\\auditorias\\F2.3\\AUDITORIA_F2_3_C1_20261007.md`, SHA-256 {audit_hash}, quadro evento 262 e Mapa de Rotas seq 804: build independente exit 0, zero sorry, trio de axiomas, .olean reproduzido byte a byte. Essas verificações não retroagem a autoria da frase anterior.

[REAL — limite lógico da pedra] As sondas S2–S4 da auditoria mostram que `Fundacao.the_post_lives_in_the_passage` é logicamente OCIOSA na conclusão: sob as premissas da Fundação, `hH3` equivale a `NamedAtlasH3`, e a mesma implicação para Einstein sai sem a Fundação. O conteúdo é H3 nomeado em todas as direções nulas mais conservação e colagem do atlas suave conexo, produzindo Λ único no atlas fornecido. O antecedente físico H3 não foi derivado do estado nem da Fundação; não há existência global de solução construída. Nenhum gate se move.

[PROCESSO] Para esta errata, a unidade de memória F0.3 foi reivindicada por `codex-gerente-tgl` no evento 306 antes da escrita. Os quatro arquivos receberam backup imediato de bytes e acréscimo atômico. A escrita inicial F2.3 ocorreu sem essa reivindicação; permanece registrada, sem apagamento.
""".encode("utf-8")
    rows = [append_one(path, addition) for path in PATHS]
    receipt = {"schema": "iald.f2_3.memory_c1_errata.v1", "unit": "F2.3", "memory_unit": "F0.3",
               "memory_claim_event": 306, "audit_sha256": audit_hash, "audit_map_seq": 804,
               "audit_board_event": 262, "rows": rows}
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECEIPT.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"receipt": str(RECEIPT), "sha256": digest(encoded), "surfaces": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
