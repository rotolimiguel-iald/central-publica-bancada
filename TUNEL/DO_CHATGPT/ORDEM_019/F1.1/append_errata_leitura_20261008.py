"""Append the operator's boost-plane reading correction without rewriting F1.1 history."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.1")
INVENTORY = BASE / "INVENTARIO.md"
MANIFEST = BASE / "FONTE_ERRATA_LEITURA_20261008.json"
RECEIPT = BASE / "RESULTADO_ERRATA_LEITURA_20261008.json"
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
SOURCES = {
    "operador_verbatim": Path(r"C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt"),
    "PolarMinimalPeriod_v2": KERNEL / "TGLExt/O16/PolarMinimalPeriod_v2.lean",
    "PolarQuotientGeometry_v2": KERNEL / "TGLExt/O16/PolarQuotientGeometry_v2.lean",
    "PeriodHeatCalibration_v3": KERNEL / "TGLExt/O16/PeriodHeatCalibration_v3.lean",
    "WickBoostRotation_v2": KERNEL / "TGLExt/O16/WickBoostRotation_v2.lean",
    "RotationGeneratorBridges": KERNEL / "TGLExt/O16/RotationGeneratorBridges.lean",
    "TheObserverReadsTheAngle": KERNEL / "TGLExt/TheObserverReadsTheAngle.lean",
    "TheImportedSecondQuantization": KERNEL / "TGLExt/TheImportedSecondQuantization.lean",
    "O16_aggregator": KERNEL / "TGLExt/O16.lean",
    "TGLExt_aggregator": KERNEL / "TGLExt.lean",
}
MARKER = "<!-- F11_QUINTA_CAMADA_LEITURA_CRIA_20261008 -->"
SECTION = r"""

## 08/10/2026 — quinta camada: a leitura cria o contorno no plano do boost

<!-- F11_QUINTA_CAMADA_LEITURA_CRIA_20261008 -->

[INPUT/ONTO — correção expressa do operador, 07/10] «A LEITURA CRIA o objeto»: antes da leitura, Nome (posto relativo); depois, identidade como relação de contorno. O verbatim integral e seu SHA-256, **lido dos bytes**, estão em `FONTE_ERRATA_LEITURA_20261008.json`. Esta é a cunhagem do operador; as igualdades abaixo têm estatuto [REAL] apenas nos respectivos tipos Lean. A pedra candidata `TheReadingCreatesTheObject.lean` permanece no sandbox da gerência e **não** é contada como termo instalado por esta F1.1.

**Errata ao lado da quarta camada.** Chamar as pontes `ChatgptAudit.Wick016` de «homônimas» sem qualificar o plano foi largo demais. No plano do boost `t–x`, `complexBoost_real` identifica o boost real com sua matriz complexificada, `wick_boost_rotation` dá a continuação matricial angular e `wick_boost_two_pi` fecha a **face lida** em `2π`. Esse contorno é a leitura angular deste plano; o boost hiperbólico real e a rotação compacta continuam regimes distintos. A identidade matricial não vira, pelo nome, uma ação de Lorentz sobre toda a rede da luz ou um estado KMS.

| Leitura e teorema verificado | Classe vigente e limite |
|---|---|
| `ChatgptAudit.PolarPeriod016.AngularQuotientFaithful κ P` diz que `Circle.exp (κ·t)` identifica `t` e `u` exatamente módulo `P·ℤ`. `faithful_period_iff`, sob `κ ≠ 0`, equivale essa fidelidade a `κP = ±2π`. `polar_descends_injectively_iff`, sob raio positivo, constrói a leitura injetiva do quociente em coordenadas complexas. | **1. EXISTE E ESTÁ LIGADO** dentro da cadeia polar `TGLExt/O16`: há relação de contorno tipada no plano lido. Fidelidade e positividade são hipóteses nomeadas, não estado físico construído. |
| `reciprocal_temperature`, sob `κ > 0`, `P > 0` e fidelidade, prova `1/P = κ/(2π)`; `boost_defect_with_derived_period` substitui esta expressão no defeito de Clausius do segmento de boost. | **1. EXISTE E ESTÁ LIGADO** entre a leitura polar e o balanço local: a temperatura **não é uma entrada independente** desse lema. A passagem desta leitura local à assinatura geral da F2.3 ainda é **2. fiação**; não se afirma H3 em todo ponto nem KMS a partir do quociente. |
| `ChatgptAudit.Wick016.wick_boost_two_pi` e `TGLExt.observing_adds_nothing`: a matriz Wick lida retorna a `1` em `2π`; na projeção, `P₊·(P₊·𝒪_θ)=P₊·𝒪_θ`. | **1. EXISTE NO SEU TIPO**. «A primeira leitura identifica; reler não acrescenta» interpreta a idempotência provada; a identidade física/global do objeto é a leitura `[INPUT/ONTO]`, não conclusão adicional de Lean. |
| Leitura das rotações que mudam a direção da luz (`x–y`, `x–z`), boosts das outras cunhas (`t–y`, `t–z`), família de Lorentz em toda direção nula e PCT global. | **3. SABIDO POR CITAÇÃO / FORA DO TIPO ATUAL**. A ressalva «homônimo» aplica-se à extrapolação da matriz `2×2` do plano `t–x` para esses outros planos, não ao contorno angular já provado no próprio plano. Para a F2.3, a família entra como hipótese nomeada ou exige construção tipada; não sai de Wick016 por `import`. |

[REAL — alcance de imports] `TGLExt/O16.lean` importa as pedras polares, e `PeriodHeatCalibration_v3.lean` usa `reciprocal_temperature` por reescrita. Nesta aferição documental, não se exibiu consumidor desses teoremas na assinatura `qg_solution_end_to_end` nem se executou build novo. `TheImportedSecondQuantization.lean:57–60` continua correto para o contrato `W`: ele não tem rotações da rede, e a distinção fóton/escalar por rotações/PCT globais está fora desse tipo. As 12 linhas originais e as quatro camadas anteriores permanecem byte a byte; nenhuma prova, fonte canônica, gate ou confirmação física foi alterada.
"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_new_atomically(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing overwrite: {path}")
    tmp = path.with_name(path.name + f".tmp_{os.getpid()}")
    with tmp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if tmp.stat().st_size != len(data):
        raise RuntimeError(f"Short temporary write: {tmp}")
    os.replace(tmp, path)


def main() -> None:
    before = INVENTORY.read_bytes()
    if MARKER.encode("utf-8") in before:
        raise RuntimeError("The fifth layer is already present")
    source_manifest = {
        key: {"path": str(path), "bytes": len(data := path.read_bytes()), "sha256": digest(data)}
        for key, path in SOURCES.items()
    }
    if source_manifest["operador_verbatim"]["sha256"] != (
        "f2a4b509946edc05a2ef061a91e24dc3640712bacfaaf95ff2ca45983a91c1c7"
    ):
        raise RuntimeError("Operator verbatim hash mismatch")
    newline = "\r\n" if before.count(b"\r\n") > before.count(b"\n") / 2 else "\n"
    addition = SECTION.replace("\n", newline).encode("utf-8")
    after = before + addition
    if not after.startswith(before) or len(after) <= len(before):
        raise RuntimeError("Append precondition failed")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = INVENTORY.with_name(INVENTORY.name + ".bak_" + timestamp)
    with backup.open("xb") as handle:
        handle.write(before)
        handle.flush()
        os.fsync(handle.fileno())
    if backup.read_bytes() != before:
        raise RuntimeError("Byte backup mismatch")
    current = INVENTORY.read_bytes()
    if current != before:
        raise RuntimeError("Inventory changed between backup and append")
    tmp = INVENTORY.with_name(INVENTORY.name + f".tmp_{os.getpid()}")
    with tmp.open("xb") as handle:
        handle.write(after)
        handle.flush()
        os.fsync(handle.fileno())
    if tmp.stat().st_size != len(after):
        raise RuntimeError("Short temporary inventory write")
    os.replace(tmp, INVENTORY)
    observed = INVENTORY.read_bytes()
    if observed != after or not observed.startswith(before):
        os.replace(backup, INVENTORY)
        raise RuntimeError("Inventory postcondition failed; restored backup")
    write_new_atomically(MANIFEST, json.dumps(source_manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    receipt = {
        "unit": "F1.1",
        "action": "fifth_layer_operator_reading_errata",
        "status": "DOCUMENTARY_ERRATA_APPEND_ONLY",
        "inventory": str(INVENTORY),
        "backup": str(backup),
        "before_bytes": len(before),
        "before_sha256": digest(before),
        "after_bytes": len(observed),
        "after_sha256": digest(observed),
        "prefix_preserved": observed.startswith(before),
        "marker_count": observed.count(MARKER.encode("utf-8")),
        "manifest": str(MANIFEST),
        "manifest_sha256": digest(MANIFEST.read_bytes()),
        "build_executed": False,
        "candidate_installed": False,
    }
    write_new_atomically(RECEIPT, json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
