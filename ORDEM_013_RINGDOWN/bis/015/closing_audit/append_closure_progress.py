"""Append the two final reports to the mission ledger with byte backup."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
TUNNEL = ROOT / "TUNEL" / "DO_CHATGPT"
PROGRESS = TUNNEL / "ENTREGA_016_PROGRESSO.md"
HERE = Path(__file__).resolve().parent


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    at = datetime.now(timezone.utc)
    tag = at.strftime("%Y%m%d_%H%M%S_%f")
    a = TUNNEL / "ENTREGA_016_RELATORIO_FINAL.md"
    b = TUNNEL / "ENTREGA_015_RELATORIO_FINAL.md"
    budget = ROOT / "ORDEM_013_RINGDOWN" / "ORCAMENTO_015_v13.json"
    forms = sorted(TUNNEL.glob("REAPROVEITAMENTO_T??.md"))
    if len(forms) != 19:
        raise ValueError(f"Need 19 reuse forms, found {len(forms)}")
    pre = PROGRESS.read_bytes()
    if b"ORDEM016_PARTE_A_E_015_PARTE_B_FINAL_20260927" in pre:
        raise FileExistsError("final progress already appended")
    backup = PROGRESS.with_name(PROGRESS.name + ".bak_" + tag)
    shutil.copyfile(PROGRESS, backup)
    if sha(backup.read_bytes()) != sha(pre):
        raise IOError("byte backup differs")
    line = (
        f"\n\n{at.isoformat()} | ORDEM016_PARTE_A_E_015_PARTE_B_FINAL_20260927 | "
        f"A={sha(a.read_bytes())} | B={sha(b.read_bytes())} | "
        f"budget_v13={sha(budget.read_bytes())} | "
        f"reaproveitamento={len(forms)}/19 | "
        "A0-A8 MEDIDA; B T01-T19 prestacao documental final, T14 API paga, T15 nao pago; "
        "sigma(c)=null, nenhum z conjunto 5sigma, gate intacto; T19 strain publico, censo aberto.\n"
    ).encode("utf-8")
    new = pre + line
    fd, tmp_name = tempfile.mkstemp(prefix="progress_", suffix=".tmp", dir=PROGRESS.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(new)
            handle.flush()
            os.fsync(handle.fileno())
        if tmp.stat().st_size != len(new):
            raise IOError("short temporary write")
        os.replace(tmp, PROGRESS)
        if PROGRESS.stat().st_size <= len(pre) or not PROGRESS.read_bytes().startswith(pre):
            os.replace(backup, PROGRESS)
            raise IOError("progress append invalid; restored backup")
    finally:
        if tmp.exists():
            tmp.unlink()
    receipt = {
        "status": "FINAL_PROGRESS_APPEND_VERIFIED",
        "backup_name": backup.name,
        "backup_sha256": sha(pre),
        "progress_sha256_after": sha(PROGRESS.read_bytes()),
        "A_final_sha256": sha(a.read_bytes()),
        "B_final_sha256": sha(b.read_bytes()),
        "budget_v13_sha256": sha(budget.read_bytes()),
        "reuse_form_count": len(forms),
    }
    out = HERE / "PROGRESS_APPEND_RECEIPT_20260927.json"
    if out.exists():
        raise FileExistsError(out)
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt))
