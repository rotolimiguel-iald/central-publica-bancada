"""Append the F7.2 c1 re-audit correction under the claimed F0.3 unit."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
F72 = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "F7.2"
F03 = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "F0.3"
MARKER = b"<!-- F72_C1_REAUDIT_ERRATA_20261008 -->"
TARGETS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
]


def pin(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main() -> None:
    result = F72 / "RESULTADO_ERRATAS_C1_F72_20261008_V4.json"
    if pin(result)["sha256"] != "ffc79f931654eecfd3a582577a1e0c4abc66de3c9bfbeb8685d30b4d2612c485":
        raise RuntimeError("F7.2 result changed")
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f_UTC")
    addition = """

## 08/10/2026 — F7.2: errata da reauditoria c1 ao lado

<!-- F72_C1_REAUDIT_ERRATA_20261008 -->

[REAL operacional] A frase anterior «as 26 fontes foram copiadas e conferidas» omitiu a autorização: a cópia para `Bancada_Um/fontes_externas/F7.2` ocorreu **sem ato da c1**, conforme mapa seq 841. A auditoria achou a cópia aditiva e inerte, mas a gerência ainda decide ratificar ou retirar esses arquivos. A ratificação `08541b69…` cobre somente o deploy V2 anterior; não autoriza a cópia R8 nem novos `--apply`. Esta camada não escreveu na Bancada e não recarregou o MCP.

[REAL documental / KNOWN fonte primária] `F7.2/RESULTADO_ERRATAS_C1_F72_20261008_V4.json` (SHA-256 ffc79f931654eecfd3a582577a1e0c4abc66de3c9bfbeb8685d30b4d2612c485) fixa as erratas ao lado do README/recibo/tabela V2 e da tabela V3; o README V2 tem backup de bytes. A Eq. (6) de Beccaria–Ternes fica na §III.B do PDF; a Eq. (13), na §IV.B. `arXiv:2605.13955` é ν-loss anterior a junho, distinto do dephasing JUNO. Os 26 arquivos congelados foram conferidos por hash; nenhum limite de τ★ da TGL foi derivado. Mapa seq 850–851, quadro evento 336. A errata correspondente na cópia da tabela V3 dentro da Bancada aguarda ato específico da c1; módulo V3 ainda é staging. Gate intacto.
""".encode("utf-8")
    records = []
    for path in TARGETS:
        original = path.read_bytes()
        if MARKER in original:
            raise RuntimeError(f"marker already in {path}")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as stream:
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != original:
            raise RuntimeError(f"backup mismatch: {path}")
        tmp = path.with_name(path.name + ".tmp_" + os.urandom(4).hex())
        with tmp.open("xb") as stream:
            stream.write(original + addition)
            stream.flush()
            os.fsync(stream.fileno())
        if path.read_bytes() != original or tmp.read_bytes() != original + addition:
            raise RuntimeError(f"concurrent change or short write: {path}")
        os.replace(tmp, path)
        if path.read_bytes() != original + addition:
            raise RuntimeError(f"post-write mismatch: {path}")
        records.append({"before": {"path": str(backup), "sha256": hashlib.sha256(original).hexdigest(), "bytes": len(original)}, "after": pin(path)})
    receipt = {
        "schema": "iald.f0_3.f7_2_c1_reaudit_memory_errata.v1",
        "created_utc": now.isoformat(),
        "memory_unit": "F0.3",
        "claim_event": 337,
        "source_unit": "F7.2",
        "source_result": pin(result),
        "map_seq": [850, 851],
        "board_event": 336,
        "targets": records,
    }
    out = F03 / "MEMORY_ERRATA_F72_REAUDIT_C1_20261008.json"
    with out.open("xb") as stream:
        stream.write((json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(pin(out), ensure_ascii=False))


if __name__ == "__main__":
    main()
