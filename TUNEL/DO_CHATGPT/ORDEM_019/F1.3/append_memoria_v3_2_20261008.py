"""Append the F1.3 v3.2 receipt to Central memory with immediate byte backups."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

UNIT = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes")
RESULT = UNIT / "RESULTADO_V3_2_ENUNCIADO_D1A3_20261008.json"
RECEIPT = UNIT / "MEMORY_V3_2_RECEIPT_20261008.json"
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    UNIT.parent / "AVISO_GERENCIA.md",
]
MARKER = b"<!-- F13_V32_TYPED_D1A3_20261008 -->"


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


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
    if result["unit"] != "F1.3" or result["status"] != "ENTREGUE_PARA_REAUDITORIA_C1":
        raise ValueError("unexpected F1.3 evidence")
    result_hash = digest(RESULT.read_bytes())
    entry = f"""

## 08/10/2026 — F1.3 v3.2, saída D1a.3 tipada para reauditoria

<!-- F13_V32_TYPED_D1A3_20261008 -->

[REAL documental] Antes de produzir, o Nós Vivo registrava a v3.1 e a reauditoria c1. A v3.1 já atende a tabela do mathlib pinado, a ausência de Fubini L² vetorial, Tomita genérico em H1, Eckmann–Osterwalder/Leyland–Roberts–Testard e a família curva até a linha 75. A c1 marcou seus pedidos 1/4/5/6 atendidos, 3 parcial e 2 faltante. A F1.1 já está FECHADA com terceira camada e erratas em suas memórias; nenhuma edição F1.1 foi repetida neste ciclo.

[REAL tipagem; OPEN habitante] A v3.2 acrescenta `F1.3/COMPLEMENTO_V3_2_ENUNCIADO_D1A3_20261008.md` e cópias byte a byte da sonda Lean e do log de build da c1. `D1a3OutputBGL` tipa Fub, J_W, T, σ, condições de S_W, Δ caracterizado unicamente por grafo S†S e multiplicadores após Fourier. `K(W_R)` é construído condicionalmente por `closedAntilinearStandardSubspace`; `exists_nonzero` é consequência, não campo. `LightNetStandardWedgeDataBGL` propõe a colagem da cunha direita para decisão do operador. O build da c1 saiu EXIT 0, zero sorry e só `propext`, `Classical.choice`, `Quot.sound`.

[OPEN] Não foi construído habitante físico, Fubini L² vetorial, J_W, T positivo, nem cálculo funcional ilimitado `Δ_K^{{it}}=B0(−2πt)`. O campo `ModularGroupIsBoost` só expressa o contrato multiplicativo para B0 após Fourier. Tipagem condicional não instala tipo no kernel nem fecha a realização.

[CUSTÓDIA] `F1.3/RESULTADO_V3_2_ENUNCIADO_D1A3_20261008.json` SHA-256 {result_hash}; mapa seq 838; quadro evento 305, F1.3 ENTREGUE para reauditoria c1. Sem novo MiMo ou outro provedor, sem alteração de `um.py`, kernel ou gate. `NOT_FALSIFIED` não é creditação.
""".encode("utf-8")
    rows = [append_one(path, entry) for path in PATHS]
    receipt = {"schema": "iald.f1_3.memory_v3_2.v1", "unit": "F1.3", "result_sha256": result_hash,
               "map_seq": 838, "board_event": 305, "rows": rows}
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECEIPT.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"receipt": str(RECEIPT), "sha256": digest(encoded), "surfaces": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
