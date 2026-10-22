"""Build the live ORDEM 018 summary and index existing receipts.

This tool does not move or delete custody artifacts. Existing files are backed
up byte-for-byte before an atomic replacement. A receipt-chain mismatch fails.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ORDER = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
CLI = Path(r"C:\IALD\PROGRAMA_IALD\iald.py")
PYTHON = Path(r"C:\Python314\python.exe")
BOOK = ORDER / "recibos.jsonl"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def atomic_replace(path: Path, data: bytes) -> None:
    old = path.read_bytes() if path.exists() else None
    if old == data:
        return
    if old is not None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as handle:
            handle.write(old)
            handle.flush()
            os.fsync(handle.fileno())
        if backup.read_bytes() != old:
            raise RuntimeError(f"backup mismatch: {backup}")
    temp = path.with_name(path.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(data):
        raise RuntimeError(f"temporary size mismatch: {temp}")
    os.replace(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError(f"replacement mismatch: {path}")


def verify_book(raw: bytes) -> tuple[list[dict], dict[str, str], str]:
    records = []
    by_path = {}
    previous = "0" * 64
    for line_number, line in enumerate(raw.splitlines(), 1):
        item = json.loads(line)
        digest = item.pop("record_sha256")
        if item["previous_sha256"] != previous or sha(canonical(item)) != digest:
            raise RuntimeError(f"receipt chain broken at line {line_number}")
        item["record_sha256"] = digest
        if item["path"] in by_path:
            raise RuntimeError(f"duplicate receipt: {item['path']}")
        by_path[item["path"]] = item["file_sha256"]
        previous = digest
        records.append(item)
    return records, by_path, previous


def main() -> None:
    if not ORDER.is_dir():
        raise RuntimeError("ORDEM 018 missing")
    raw = BOOK.read_bytes() if BOOK.exists() else b""
    records, known, previous = verify_book(raw)
    added = 0
    for path in sorted(ORDER.glob("RECIBO_*.json"), key=lambda p: p.name.casefold()):
        data = path.read_bytes()
        digest = sha(data)
        name = path.name
        if name in known:
            if known[name] != digest:
                raise RuntimeError(f"indexed receipt changed: {name}")
            continue
        item = {
            "path": name,
            "file_sha256": digest,
            "bytes": len(data),
            "previous_sha256": previous,
            "statute": "INDEXED_EXISTING_RECEIPT_NOT_REVALIDATED",
        }
        item["record_sha256"] = sha(canonical(item))
        previous = item["record_sha256"]
        records.append(item)
        known[name] = digest
        added += 1
    new_book = b"".join(canonical(item) + b"\n" for item in records)
    if raw and not new_book.startswith(raw):
        raise RuntimeError("append-only receipt book would be rewritten")
    atomic_replace(BOOK, new_book)
    verify_book(BOOK.read_bytes())

    state = json.loads(subprocess.check_output([str(PYTHON), str(CLI), "estado"], text=True, encoding="utf-8"))
    board = state["quadro"]
    statuses = board["por_status"]
    pending = ", ".join(board["aguardam_operador"])
    archive_path = ORDER.parent / "ORDEM_019" / "F9.5" / "BACKUP_ARCHIVE_RESULT.json"
    archived = json.loads(archive_path.read_text(encoding="utf-8"))["count"] if archive_path.exists() else 0
    status_lines = "\n".join(f"| {name} | {count} |" for name, count in sorted(statuses.items()))
    text_state = (
        "# ORDEM 018 — estado vivo\n\n"
        f"Gerado em {state['quando']} por `ORDEM_019/F9.5/build_order18_state.py`. "
        "[REAL] Retrato do quadro, sem alterar o relatório histórico nem os gates.\n\n"
        "| Estado do quadro | Unidades |\n|---|---:|\n"
        f"{status_lines}\n\n"
        f"[REAL] Pendências do operador no quadro: {pending}. "
        "A resposta do operador continua necessária antes das execuções correspondentes.\n\n"
        f"[REAL] Livro `recibos.jsonl`: {len(records)} recibos legados indexados; "
        f"cabeça SHA-256 `{previous}`. O índice registra integridade dos bytes, "
        "não valida automaticamente o conteúdo científico de cada recibo.\n\n"
        f"[REAL] Backups históricos do guia de transporte arquivados por data: {archived}; "
        "manifesto com SHA-256 antes/depois em `ORDEM_019/F9.5/BACKUP_ARCHIVE_RESULT.json`.\n\n"
        "[OPEN] F3.5/d72, F4.1/P3 A02, F4.2/conjunto D e F5.1/BBN "
        "seguem seus gates individuais. Ver o quadro e `INDICE.md` para a origem.\n"
    )
    atomic_replace(ORDER / "ESTADO.md", text_state.encode("utf-8"))
    index_lines = [
        "# ORDEM 018 — índice de artefatos",
        "",
        f"Gerado em {state['quando']}. [REAL] O livro tem {len(records)} recibos indexados por SHA-256.",
        "",
        "- [Estado vivo](ESTADO.md)",
        "- [Relatório histórico](ENTREGA_018_RELATORIO_FINAL.md)",
        "- [Livro encadeado](recibos.jsonl)",
        "- [Manifesto do arquivo morto](../ORDEM_019/F9.5/BACKUP_ARCHIVE_RESULT.json)",
        "",
        "## Recibos legados na raiz",
        "",
        "| Recibo | SHA-256 dos bytes |",
        "|---|---|",
    ]
    for item in records:
        index_lines.append(f"| [{item['path']}]({item['path']}) | `{item['file_sha256']}` |")
    index_lines.extend(["", "As subpastas preservam seus próprios artefatos; nenhum recibo legado foi movido ou apagado.", ""])
    atomic_replace(ORDER / "INDICE.md", "\n".join(index_lines).encode("utf-8"))
    print(json.dumps({"indexed": len(records), "new": added, "head": previous,
                      "state_sha256": sha((ORDER / "ESTADO.md").read_bytes()),
                      "index_sha256": sha((ORDER / "INDICE.md").read_bytes())}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL_CLOSED: {exc}", file=sys.stderr)
        raise
