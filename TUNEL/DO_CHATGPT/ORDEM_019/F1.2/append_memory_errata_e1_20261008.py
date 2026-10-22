"""Append signed F1.2 bookkeeping errata to four claimed memory surfaces."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
F12 = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "F1.2"
MARKER = b"<!-- F12_E1_SIGNED_MEMORY_ERRATA_20261008 -->"
TARGETS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
]
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F1.2\AUDITORIA_F1_2_C1_a5aa4480.md")


def pin(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main() -> None:
    if pin(AUDIT)["sha256"] != "ec1040a05d51cde22f3cb6cd6ffe3674049084eae0208397aa2ff36096bcffb5":
        raise RuntimeError("c1 audit changed")
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f_UTC")
    addition = """

## 08/10/2026 — F1.2: errata assinada da escrituração, ao lado

<!-- F12_E1_SIGNED_MEMORY_ERRATA_20261008 -->

[REAL — auditoria c1 `AUDITORIA_F1_2_C1_a5aa4480.md`, §3/S6 e cético anterior C9] Onde o parágrafo F1.2 acima põe «a unidade de `positiveUnit P` tem traço infinito» sob `[OPEN — alcance]`, leia-se **[REAL]**: o traço da unidade é infinito no core regular v351. A testemunha positiva de traço finito da não vacuidade é outro elemento. Continua [OPEN] somente a construção de `M_n ⋊_σ ℝ` com L², fecho de von Neumann e equivalência de entrelaçamento; isso não reabre a F1.2, FECHADA pela c1 no evento 287.

[REAL — assinatura da errata] O parágrafo anterior identificado como `[REAL — errata ao lado]` foi produzido **por codex-gerente-tgl**, na entrega F1.2 sob a reivindicação então vigente. Esta correção adicional é feita **em nome de codex-gerente-tgl**, por ordem da gerência c1 de 08/10/2026, sob a unidade derivada F1.2.E1 reivindicada no evento 344. O Mapa seq 853 corrige o alvo: a seq 823 usou `corrige: 716`, mas as frases «2 declarações» e «Fundacao externa» pertencem à seq 728. Nenhuma sequência antiga foi alterada. Nenhum kernel, `um.py` ou gate mudou por esta escrituração.
""".encode("utf-8")
    records = []
    for path in TARGETS:
        original = path.read_bytes()
        if MARKER in original:
            raise RuntimeError(f"marker already exists: {path}")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as stream:
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != original:
            raise RuntimeError(f"backup mismatch: {path}")
        temp = path.with_name(path.name + ".tmp_" + os.urandom(4).hex())
        with temp.open("xb") as stream:
            stream.write(original + addition)
            stream.flush()
            os.fsync(stream.fileno())
        if path.read_bytes() != original or temp.read_bytes() != original + addition:
            raise RuntimeError(f"concurrent change or short write: {path}")
        os.replace(temp, path)
        if path.read_bytes() != original + addition:
            raise RuntimeError(f"post-write mismatch: {path}")
        records.append({"before": {"path": str(backup), "sha256": hashlib.sha256(original).hexdigest(), "bytes": len(original)}, "after": pin(path)})
    receipt = {
        "schema": "iald.f1_2.e1.memory_signed_errata.v1",
        "created_utc": now.isoformat(),
        "unit": "F1.2.E1",
        "claim_event": 344,
        "source_unit_status": "FECHADA",
        "map_errata_seq": 853,
        "signed_by": "codex-gerente-tgl",
        "audit": pin(AUDIT),
        "targets": records,
        "gate_effect": "NONE",
    }
    out = F12 / "MEMORY_ERRATA_E1_RECEIPT_20261008.json"
    with out.open("xb") as stream:
        stream.write((json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(pin(out), ensure_ascii=False))


if __name__ == "__main__":
    main()
