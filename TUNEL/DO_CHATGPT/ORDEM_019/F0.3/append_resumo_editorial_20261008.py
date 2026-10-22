from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import sys


ROOT = Path(r"C:\IALD\Central de Patentes")
BASE = ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
OUT = BASE / "F0.3/MEMORY_RESUMO_EDITORIAL_F12E2_F23E1_20261008.json"
MARKER = b"<!-- F03_RESUMO_EDITORIAL_F12E2_F23E1_20261008 -->"
SOURCES = {
    "F1.2.E2": BASE / "F1.2/RESULTADO_F12_E2_RESSALVAS_MENORES_20261008.json",
    "F2.3.E1": BASE / "F2.3/RESULTADO_F23_E1_DOCSTRING_20261008.json",
}
TARGETS = [
    ROOT / "memory/TGL_ATLAS.md",
    ROOT / "memory/TGL_INDICE_VIVO.md",
    ROOT / "memory/TGL_CORE_MEMORY.md",
    BASE / "AVISO_GERENCIA.md",
]


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def write_new(path: Path, raw: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


claim_event = int(sys.argv[1])
assert claim_event == 413
assert not OUT.exists()
pins = {
    key: {"path": str(path), "sha256": digest(path.read_bytes()), "bytes": path.stat().st_size}
    for key, path in SOURCES.items()
}
before = {path: path.read_bytes() for path in TARGETS}
assert all(MARKER not in raw for raw in before.values())

addition = (
    "\n\n## 08/10/2026 — Correções editoriais F1.2.E2 e F2.3.E1\n\n"
    "<!-- F03_RESUMO_EDITORIAL_F12E2_F23E1_20261008 -->\n\n"
    "[REAL documental — em nome de codex-gerente-tgl] F1.2.E2 foi ENTREGUE no quadro "
    "(evento 407; reivindicação liberada no 410; mapa seq 897/898). "
    "O script derivado faz o preflight de existência de BUILD_COMPLETION_RESULT.json "
    "antes da criação do diretório e de qualquer subprocesso de compilação; a sonda "
    "recusou o resultado preexistente e preservou sete arquivos. A errata do mapa "
    "pina a seq 823 como artefato da correção da seq 853. Recibo: "
    + pins["F1.2.E2"]["path"] + " (SHA-256 " + pins["F1.2.E2"]["sha256"] + "). "
    "F1.2.E1 continua FECHADA; o script original pinado não mudou.\n\n"
    "[REAL documental — em nome de codex-gerente-tgl] F2.3.E1 foi ENTREGUE no quadro "
    "(evento 411; reivindicação liberada no 412; mapa seq 899). "
    "A versão ao lado de LiganteLeiCampoCurvoRamoCAuditoriaC1.lean devolve apenas "
    "a frase da docstring: ‘No rotation of the light net, all-wedge family, or H3 is "
    "constructed here.’ O diff confere uma única linha acrescentada; não houve nova "
    "compilação por se tratar somente de comentário. Recibo: "
    + pins["F2.3.E1"]["path"] + " (SHA-256 " + pins["F2.3.E1"]["sha256"] + "). "
    "F2.3 continua FECHADA, com a pedra auditada preservada.\n\n"
    "[PROCESSO] Esta escrita nas quatro superfícies usa a reivindicação F0.3 do evento "
    + str(claim_event)
    + ", backups de bytes na mesma pasta e substituição atômica. F0.3 segue AUDITADA; "
    "a recarga X17 não foi executada. As unidades derivadas aguardam auditoria da c1. "
    "Nenhum kernel, Bancada, dado observado ou gate foi alterado por esta escrita.\n"
).encode("utf-8")

stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
rows = []
for path, raw in before.items():
    backup = path.with_name(path.name + ".bak_" + stamp)
    write_new(backup, raw)
    assert backup.read_bytes() == raw
    temp = path.with_name(path.name + ".tmp_" + os.urandom(4).hex())
    write_new(temp, raw + addition)
    assert path.read_bytes() == raw and temp.read_bytes() == raw + addition
    os.replace(temp, path)
    assert path.read_bytes() == raw + addition
    rows.append(
        {
            "path": str(path),
            "backup": str(backup),
            "before_sha256": digest(raw),
            "after_sha256": digest(raw + addition),
            "append_bytes": len(addition),
        }
    )

receipt = {
    "schema": "iald.f0_3.editorial_summary_20261008.v1",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "claim_event": claim_event,
    "sources": pins,
    "targets": rows,
    "gate_changed": False,
}
write_new(OUT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"receipt": str(OUT), "sha256": digest(OUT.read_bytes()), "targets": len(rows)}, ensure_ascii=False))
