"""Append one auditable F0.3 layer to the four shared memory surfaces."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"C:\IALD\Central de Patentes")
ORDER = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019"
IALD = Path(r"C:\IALD\PROGRAMA_IALD")
MARKER = "<!-- iald_ordem019_a39a1758_a7aff55e_f34_08out -->"
TARGETS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ORDER / "AVISO_GERENCIA.md",
]
SOURCES = {
    "F0.3.E2": ORDER / "F0.3" / "RESULTADO_F03_E2_A39A1758_20261008.json",
    "F1.2.E3": ORDER / "F1.2" / "RESULTADO_F12_E3_PREFLIGHT_COMPLETO_20261008.json",
    "F2.3.E3": ORDER / "F2.3" / "RESULTADO_F23_E3_CUSTODIA_SEQ899_20261008.json",
    "F2.3.E4": ORDER / "F2.3" / "RESULTADO_F23_E4_APPEND_IN_LOCO_20261008.json",
    "F3.6.E3": ORDER / "F3.6" / "RESULTADO_F36_E3_DIGITO_V3_20261008.json",
    "F3.1.F34": ORDER / "F3.1" / "RESULTADO_F31_F34_DUAS_TESTEMUNHAS_20261008.json",
    "F3.2.F34": ORDER / "F3.2" / "RESULTADO_F32_F34_VINCULO_20261008.json",
    "F4.3.R5": ORDER / "F4.3" / "RESULTADO_F43_R5_20261008.json",
    "F4.3.R5.1": ORDER / "F4.3" / "RESULTADO_F43_R5_1_20261008.json",
    "F3.4.operador": ROOT / "work" / "f9_pergunta_08out" / "OPERADOR_08out_resposta_verbatim.txt",
}
RECEIPT = ORDER / "F0.3" / "MEMORY_A39A1758_F34_F43_20261008.json"


def hash_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main() -> None:
    if RECEIPT.exists():
        raise FileExistsError(RECEIPT)
    state = json.loads(subprocess.check_output(
        [sys.executable, "-X", "utf8", str(IALD / "iald.py"), "ver", "F0.3"],
        text=True,
    ))
    claim = state.get("reivindicacao") or {}
    if state["status"] != "AUDITADA" or claim.get("quem") != "codex-coordenadora":
        raise RuntimeError("F0.3 must be AUDITADA and claimed by codex-coordenadora")
    note = claim.get("nota", "")
    if not all(name in note for name in (
        "TGL_ATLAS.md", "TGL_INDICE_VIVO.md", "TGL_CORE_MEMORY.md", "AVISO_GERENCIA.md"
    )):
        raise RuntimeError("The claim does not name all four memory surfaces")

    source_rows = {}
    for label, path in SOURCES.items():
        data = path.read_bytes()
        source_rows[label] = {
            "path": str(path), "sha256": hash_bytes(data), "bytes": len(data)
        }
    original = {}
    for path in TARGETS:
        data = path.read_bytes()
        if MARKER.encode("utf-8") in data:
            raise FileExistsError(f"Memory layer already present: {path}")
        original[path] = data

    pin_line = "; ".join(
        f"{label} {row['sha256'][:16]}"
        for label, row in source_rows.items()
    )
    lines = [
        "",
        "",
        "### 08/10/2026 — ORDEM 019: auditorias a39a1758/a7aff55e e decisão F3.4 [codex-coordenadora]",
        MARKER,
        "",
        "[INPUT — operador] A F3.4 foi FECHADA no evento 462: a V2 escalar e a ROOT90da são duas testemunhas do mesmo fato. β_TGL = ALPHA_FINE_CODATA_2018 × √e fica fixo em runtime, sem ajuste. Cada testemunha depõe pela própria função pinada antes do composto; não se julgam, não se somam e não transferem poder ou admissão.",
        "",
        "[REAL documental; ainda sem reauditoria c1] F3.1 recebeu projeção nova da V2 R4 e adendo ROOT90da; F3.2 recebeu vínculo, gate e runner novos que pinam essa projeção. Seis testes sintéticos passaram e o modo real foi recusado antes da leitura. Nada foi congelado ou aberto; X13, D-H, d72 e a abertura continuam atos do operador.",
        "",
        "[REAL documental e sintético; OPEN poder] A F4.3 R5 fixa 13 campos de desenho, usa PSD de projeto C7 e explicita a precedência e o limiar unilateral de oposição. A R5.1 exige recibos de calibração e FWER para usar p-valores em produção; sem eles, recusa. As injeções exatas não foram rodadas, o adaptador full IMR executável falta, e o pedido ao operador segue SUSPENSO.",
        "",
        "[REAL documental] F1.2.E3 recusa resultado, BUILD_*.log e .olean antigos antes de compilar; F2.3.E3 trouxe a fonte de %TEMP% ao túnel e corrigiu a ref da seq 899; F2.3.E4 documentou o append in loco de 651 B ao artefato já pinado, sem nova edição; F3.6.E3 devolveu o último dígito do valor V3 da base nua.",
        "",
        "[REAL — custódia e processo] F0.3.E2 recustodiou no evento 486 os três recibos dos eventos 400/414/433, com origem e cópia iguais por hash e tamanho; a errata da seq 900 está ao lado na seq 927. A menção das 14:32 a F7.2.E1/F1.3.E4 era antecipação e só ganhou registro depois. A reivindicação F1.3 nº 301 foi limpa automaticamente pelo fechamento 312; o quadro hoje mostra null. F0.3 permanece AUDITADA aguardando X17.",
        "",
        "[PINS LIDOS DO ARQUIVO — sha16] " + pin_line + ".",
        "[REAL — escopo] Este append usa a reivindicação F0.3 nº 497, backup imediato de bytes e substituição atômica nas quatro superfícies. Nenhuma Bancada, MCP, dado observado ou gate foi alterado.",
        "",
    ]
    append = "\r\n".join(lines).encode("utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
    receipts = []
    changed = []
    try:
        for path, before in original.items():
            backup = path.with_name(path.name + f".bak_{stamp}")
            temp = path.with_name(path.name + f".tmp_{stamp}")
            if backup.exists() or temp.exists():
                raise FileExistsError(f"Backup/temp collision for {path}")
            write_new(backup, before)
            after = before + append
            write_new(temp, after)
            if temp.stat().st_size != len(after):
                raise RuntimeError(f"Temporary size mismatch: {path}")
            os.replace(temp, path)
            changed.append((path, backup))
            actual = path.read_bytes()
            if actual != after or not actual.startswith(before):
                raise RuntimeError(f"Append verification failed: {path}")
            receipts.append({
                "path": str(path), "backup": str(backup),
                "before_sha256": hash_bytes(before),
                "after_sha256": hash_bytes(actual),
                "append_bytes": len(append),
            })
    except Exception:
        for path, backup in reversed(changed):
            restore = path.with_name(path.name + f".restore_{stamp}")
            write_new(restore, backup.read_bytes())
            os.replace(restore, path)
        raise

    receipt = {
        "schema": "iald.f0_3.memory_a39a1758_f34_f43.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_event": 497,
        "parent_status": "AUDITADA",
        "pending": "X17",
        "gate_changed": False,
        "sources": source_rows,
        "targets": receipts,
        "script_sha256": hash_bytes(Path(__file__).read_bytes()),
    }
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = RECEIPT.with_name(RECEIPT.name + f".tmp_{stamp}")
    write_new(temp, encoded)
    os.replace(temp, RECEIPT)
    print(json.dumps({
        "receipt": str(RECEIPT), "sha256": hash_bytes(encoded),
        "targets": len(receipts), "append_bytes_each": len(append),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()