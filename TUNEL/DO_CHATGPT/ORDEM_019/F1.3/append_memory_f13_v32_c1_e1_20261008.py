"""Append the signed F1.3.E1 audit errata to four memory surfaces."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile


UNIT = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes")
ERRATA = UNIT / "ERRATA_F13_V32_C1_E1_20261008.md"
RECEIPT = UNIT / "MEMORY_F13_V32_C1_E1_RECEIPT_20261008.json"
PATHS = [
    ROOT / "memory" / "TGL_ATLAS.md",
    ROOT / "memory" / "TGL_INDICE_VIVO.md",
    ROOT / "memory" / "TGL_CORE_MEMORY.md",
    UNIT.parent / "AVISO_GERENCIA.md",
]
MARKER = b"<!-- F13_V32_C1_E1_MEMORY_ERRATA_20261008 -->"
PREVIOUS = b"<!-- F13_V32_TYPED_D1A3_20261008 -->"


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def main() -> None:
    if RECEIPT.exists():
        raise FileExistsError(RECEIPT)
    errata_hash = digest(ERRATA.read_bytes())
    paragraph = f"""

## 08/10/2026 — F1.3.E1: errata c1 ao lado da v3.1 e v3.2

<!-- F13_V32_C1_E1_MEMORY_ERRATA_20261008 -->

[REAL — codex-gerente-tgl, unidade reivindicada F1.3.E1] A v3.2 já adotou `D1a3OutputBGL` como saída tipada do D1a.3 e `LightNetStandardWedgeDataBGL` como interface proposta ao operador. A c1 recompilou a sonda em sandbox (EXIT 0, 19 declarações só em `propext`, `Classical.choice`, `Quot.sound`, zero sorry). A frase da v3.1 «só pode ser tipada após construir» está corrigida: Fub, J_W, T, σ e as condições modulares são campos tipados [OPEN]; não foi exibido habitante. A forma dos três campos da interface é a que compila; fortalecer `LightNetData` no kernel é decisão do operador, não escolha de forma pela c1. O pedido 2 da v3.1 ficou sem enunciado Lean e foi omitido na anotação do mapa seq 830; registrar ANOTACAO ao lado, preservando a v3.1.

[REAL documental — correções menores] `H1_nontrivial` está em `F13v3_H1_nontrivial.lean:16`. O caminho completo é `Mathlib/Analysis/VonNeumannAlgebra/Basic.lean:23`. A tabela explicita Stone para grupos unitários fortemente contínuos [FALTA], o TODO de Tomita/KMS em `Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean:42` e `eigenvectorBasis` em dimensão finita em `Mathlib/Analysis/InnerProductSpace/Spectrum.lean:34`; estes três itens tinham ficado só por remissão. Crismale–Fidaleo–Lu (2017) é a bibliografia que cita o preprint LRT 1978. A checagem de 35 referências da v3.1 verificou existência de arquivos e intervalo das linhas; não certificou todo o conteúdo. A proposta tipada é [DERIVED]; a construção D1a.1, começando por Fubini L² vetorial e depois Fourier parcial, permanece [OPEN] em unidade própria e espera o levantamento. A F1.3 principal está FECHADA por ato posterior da c1; esta E1 não a reabre. Nenhum kernel, `um.py` ou gate foi alterado nesta errata.

[EVIDÊNCIA] `F1.3/ERRATA_F13_V32_C1_E1_20261008.md` SHA-256 {errata_hash}; auditorias c1 `AUDITORIA_F1_3_C1_ad949e97.md` e `AUDITORIA_F1_3_C1_a20c3246.md` em `C:\\IALD\\PROGRAMA_IALD\\auditorias\\F1.3`.
""".encode("utf-8")

    before = {}
    for path in PATHS:
        data = path.read_bytes()
        if not data or PREVIOUS not in data or MARKER in data:
            raise ValueError(f"memory preflight failed: {path}")
        before[path] = data

    rows = []
    for path in PATHS:
        data = before[path]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f_UTC")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if backup.read_bytes() != data:
            raise OSError(f"backup mismatch: {path}")

        updated = data + paragraph
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False
        ) as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
            temporary = Path(stream.name)
        if temporary.stat().st_size != len(updated) or path.read_bytes() != data:
            raise OSError(f"temporary or source drift: {path}")
        os.replace(temporary, path)
        after = path.read_bytes()
        if after != updated or not after.startswith(data):
            raise OSError(f"append verification failed: {path}")
        rows.append(
            {
                "path": str(path),
                "backup": str(backup),
                "before_sha256": digest(data),
                "backup_sha256": digest(backup.read_bytes()),
                "after_sha256": digest(after),
                "before_bytes": len(data),
                "after_bytes": len(after),
                "append_bytes": len(paragraph),
            }
        )

    receipt = {
        "schema": "iald.f1_3.e1.memory_errata.v1",
        "unit": "F1.3.E1",
        "author": "codex-gerente-tgl",
        "errata_path": str(ERRATA),
        "errata_sha256": errata_hash,
        "marker": MARKER.decode("ascii"),
        "rows": rows,
    }
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECEIPT.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    print(
        json.dumps(
            {"receipt": str(RECEIPT), "sha256": digest(encoded), "surfaces": len(rows)},
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
