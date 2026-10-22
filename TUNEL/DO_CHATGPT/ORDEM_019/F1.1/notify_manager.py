"""Append an atomic, byte-backed correction notice for the manager."""

from __future__ import annotations

import hashlib
import os
from datetime import datetime
from pathlib import Path


NOTICE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\AVISO_GERENCIA.md")
MARKER = "F1.1 — correção de estado após auditoria concorrente"
SECTION = """

## 07/10/2026 20:30 — F1.1 — correção de estado após auditoria concorrente

[REAL] A gerência marcou F1.1 `AUDITADA` no evento 73. O Codex, ao anexar um recibo complementar, usou inadvertidamente `avancar --status ENTREGUE` no evento 153; a CLI aceitou o retrocesso. O erro foi registrado nos eventos 154 e 156. O `F1.1/RESULTADO.json` foi restaurado byte a byte ao SHA-256 da evidência auditada do evento 73; o complemento com `LightOneParticleByTerm.lean` está separado em `F1.1/RESULTADO_ADENDO_LIGHT_TERM.json`.

[INPUT para gerência] Conferir o complemento e restaurar `AUDITADA` se o parecer do evento 73 permanece válido. O Codex não assumiu a auditoria. F1.2 segue `EM_CURSO` com dois lemas algébricos compilados no sandbox e a ponte analítica `M_n⋊ℝ` aberta; F4.2/F5.1 permanecem `AGUARDA_OPERADOR`; F9.5 foi entregue com 117 recibos encadeados e 130 backups históricos arquivados por hash.
"""


def main() -> None:
    old = NOTICE.read_bytes()
    if MARKER.encode("utf-8") in old:
        raise RuntimeError("notice already present")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = NOTICE.with_name(NOTICE.name + ".bak_" + stamp)
    with backup.open("xb") as handle:
        handle.write(old)
    if backup.read_bytes() != old:
        raise RuntimeError("byte backup mismatch")
    new = old + SECTION.encode("utf-8")
    temp = NOTICE.with_name(NOTICE.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(new)
        handle.flush()
        os.fsync(handle.fileno())
    if NOTICE.read_bytes() != old or temp.stat().st_size != len(new):
        raise RuntimeError("concurrent edit or temporary size mismatch")
    os.replace(temp, NOTICE)
    if NOTICE.read_bytes() != new:
        raise RuntimeError("replacement mismatch")
    print(hashlib.sha256(new).hexdigest())


if __name__ == "__main__":
    main()
