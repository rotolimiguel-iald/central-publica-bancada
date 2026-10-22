"""Add the c1 O16 caveat to F1.1 without changing its historical text."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


UNIT = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
O16 = KERNEL / "O16"
INVENTORY = UNIT / "INVENTARIO.md"
ORIGINAL_RESULT = UNIT / "RESULTADO.json"
PINS = UNIT / "O16_AFERICAO_F11.json"
RESULT = UNIT / "RESULTADO_RESSALVA_O16.json"
MARKER = "<!-- F11_O16_CLASSE2_FIACAO_20261008 -->"

SOURCES = [
    ("RecognitionGraph_v2.lean", "theorem recognition_tomita_graph", (18, 47, 74)),
    ("DilationModularRecognition_v2.lean", "theorem dilation_recognizes_modular_content", (13, 33)),
    ("PhotonScreenCharacters_v3.lean", "theorem conjugation_exchanges_wave_sections", (54, 83)),
    ("BoostScreenPolarizations_v2.lean", "theorem circularScreen_conjugate", (23, 41, 47)),
    ("RotationGeneratorBridges.lean", "theorem genK_eq_Grot", (11, 18, 23)),
    ("WickBoostRotation_v2.lean", "theorem wick_boost_rotation", (31, 41, 47)),
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}


def new_atomic(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"FAIL_CLOSED: target already exists: {path}")
    with NamedTemporaryFile(dir=path.parent, prefix=".f11_o16_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        tmp = Path(temp.name)
    if tmp.stat().st_size != len(payload):
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"FAIL_CLOSED: incomplete temp: {path}")
    os.replace(tmp, path)
    if path.read_bytes() != payload:
        raise RuntimeError(f"FAIL_CLOSED: post-write mismatch: {path}")


def append_inventory(addition: str) -> dict[str, object]:
    original = INVENTORY.read_bytes()
    if MARKER.encode("ascii") in original:
        raise RuntimeError("FAIL_CLOSED: caveat already present")
    historical = json.loads(ORIGINAL_RESULT.read_text(encoding="utf-8"))
    expected = next(x["sha256"] for x in historical["hashes_lidos"] if Path(x["path"]).name == "INVENTARIO.md")
    if digest(original) != expected:
        raise RuntimeError("FAIL_CLOSED: historical inventory pin differs before append")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = INVENTORY.with_name(INVENTORY.name + f".bak_{stamp}")
    with backup.open("xb") as out:
        out.write(original)
        out.flush()
        os.fsync(out.fileno())
    if backup.read_bytes() != original:
        raise RuntimeError("FAIL_CLOSED: backup byte mismatch")
    payload = original + addition.encode("utf-8")
    with NamedTemporaryFile(dir=UNIT, prefix=".f11_inventory_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        tmp = Path(temp.name)
    if tmp.stat().st_size != len(payload):
        tmp.unlink(missing_ok=True)
        raise RuntimeError("FAIL_CLOSED: incomplete inventory temp")
    if INVENTORY.read_bytes() != original:
        tmp.unlink(missing_ok=True)
        raise RuntimeError("FAIL_CLOSED: concurrent inventory change")
    os.replace(tmp, INVENTORY)
    written = INVENTORY.read_bytes()
    if written != payload or len(written) <= len(original):
        with NamedTemporaryFile(dir=UNIT, prefix=".f11_restore_", suffix=".tmp", delete=False) as temp:
            temp.write(backup.read_bytes())
            temp.flush()
            os.fsync(temp.fileno())
            restore = Path(temp.name)
        os.replace(restore, INVENTORY)
        raise RuntimeError("FAIL_CLOSED: inventory write mismatch; restored")
    return {
        "path": str(INVENTORY),
        "backup": str(backup),
        "before_bytes": len(original),
        "before_sha256": digest(original),
        "after_bytes": len(written),
        "after_sha256": digest(written),
        "backup_matches_original": True,
    }


def main() -> None:
    if PINS.exists() or RESULT.exists():
        raise RuntimeError("FAIL_CLOSED: O16 output exists; do not overwrite")
    source_rows = []
    for name, needle, anchors in SOURCES:
        path = O16 / name
        raw = path.read_bytes()
        lines = raw.decode("utf-8-sig").splitlines()
        if needle not in "\n".join(lines):
            raise RuntimeError(f"FAIL_CLOSED: expected declaration missing: {name}")
        row = file_record(path)
        row["needle"] = needle
        row["anchors"] = [{"line": n, "text": lines[n - 1]} for n in anchors]
        source_rows.append(row)
    anchors = [file_record(KERNEL / "QGSolutionComplete.lean"), file_record(KERNEL / "TheImportedSecondQuantization.lean")]
    pin_doc = {
        "unit": "F1.1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "classification_target": "EXISTS_IN_KERNEL_NOT_LINKED_TO_QG_SOLUTION_END_TO_END_SIGNATURE",
        "sources": source_rows,
        "signature_anchors": anchors,
        "scope_note": "D6 selfRecognition is already connected to lightImport with U=id; the cross-pair projection/core bridge is not",
        "new_lean_compilation": False,
        "gate_changed": False,
    }
    new_atomic(PINS, (json.dumps(pin_doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    s = {Path(row["path"]).name: row["sha256"] for row in source_rows}
    addition = f"""

## 08/10/2026 — ressalva da gerência c1: pedras O16 existentes, fiação da assinatura pendente

{MARKER}

[REAL — cético aferidor] Classificação antes de dizer «falta»: **1. EXISTE E ESTÁ LIGADO** — `TheImportedSecondQuantization.lean:565–582` já usa `ReconhecimentoPeloConteudo` em `lightImport` como `selfRecognition`, com `U=id` no mesmo par da luz. **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** — as seis pedras O16 abaixo têm termos, mas a ponte entre pares/projeções e a ação física de rotação/PCT não aparecem entre as entradas nem na conclusão de `QGSolutionComplete.qg_solution_end_to_end:79–91`. **3. SABIDO** — a identificação espectral no core permanece uma referência sob suas hipóteses; isso não é o termo de ligação. **4. AUSENTE** qualifica apenas o habitante/teorema de colagem tipada e a realização física global, não as pedras que já existem.

| Resultado existente a aproveitar | Pedra e enunciado provado neste escopo | Classe para o elo solicitado | Estimativa do trabalho restante |
|---|---|---|---|
| Reconhecimento modular por conteúdo, dilatação da cunha, caracteres/telas circulares e pontes de rotação/Wick já no `TGLExt/O16`; o alvo novo é ligá-los ao mesmo par de `qg_solution_end_to_end`. | D6 transporta grafos Tomita sob `U`/álgebra/vácuo; D5 reconhece a dilatação sob `D`, covariância, vácuo e realização analítica; D1prime e `circularScreen_conjugate` provam caracteres e conjugação pontual; `RotationGeneratorBridges` liga os três geradores matriciais; `WickBoostRotation` identifica boost complexo e rotação 2×2. Detalhes e hashes abaixo. | **2 — EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** para a identificação entre pares e o PCT físico. O subcaso D6 `selfRecognition` já usado por `lightImport` é classe 1, sem pagar a ponte para `P_F`. | `[INPUT — engenharia, não medição]` Ver estimativa por pedra abaixo. As faixas se sobrepõem e supõem as testemunhas nomeadas; construir rede/Fock físicos é trabalho distinto. |

**Pinos e fiação, por pedra (SHA-256 integral lido dos bytes):**

- `RecognitionGraph_v2.lean` — `{s['RecognitionGraph_v2.lean']}`. `ReconhecimentoPeloConteudo` pede unitário `U`, preservação do vetor e equivalência das álgebras; os teoremas transportam grafo Tomita/fecho e operadores fechados sob hipóteses de realização. `selfRecognition` usa `U=id` no import v3.2, mas não identifica a projeção da torre `P_ker K` com `C.PF` do core da luz. **Fiação:** construir/fornecer o reconhecimento entre os pares efetivamente distintos, os mapas entre cores/cantos de tipos diferentes e um consumidor tipado na cadeia QG. **Esforço `[INPUT]`:** 2–5 dias só para a interface depois de fornecidos os certificados; semanas–meses para a identificação entre pares, cores e projeções.
- `DilationModularRecognition_v2.lean` — `{s['DilationModularRecognition_v2.lean']}`. `dilation_recognizes_modular_content` conserva `J` e fluxo no mesmo par da cunha para dilatação positiva, **sob** `D`, `hVac`, `hNet` e `PairTomitaAnalyticRealizationMeasured`; rejeita dilatação zero. **Fiação:** adaptar o contrato O16, uma cópia retipada de `TGL.SpecificAQFT`, ao certificado da cadeia; instanciar `D`, `hVac`, `hNet` e ligar o teorema à assinatura. A pedra não constrói `D` físico. **Esforço `[INPUT]`:** 2–5 dias para interface e conversão tipada com testemunhas fornecidas; a dilatação física é trabalho adicional.
- `PhotonScreenCharacters_v3.lean` — `{s['PhotonScreenCharacters_v3.lean']}`. Prova métrica transversal, coeficientes O(2), fase/caracteres compostos e troca **pontual** das seções circulares por conjugação; orientação `det=+1` é hipótese adicional. O próprio arquivo nega inferência automática de PCT da rede. **Fiação:** representação global induzida de helicidade ±1, orientação, ação no `H1`/Fock e covariância da rede `D.K` no mesmo par. **Esforço `[INPUT]`:** semanas para integração tipada; meses se a representação física não estiver disponível.
- `BoostScreenPolarizations_v2.lean` — `{s['BoostScreenPolarizations_v2.lean']}`. `complex_boost_circular` transporta vetores de tela; `circularScreen_conjugate` troca `h↔−h` componente a componente e as telas diferem na carta regular. **Fiação:** promover a identidade pontual a antiunitário global e PCT da rede/Fock com domínio e covariância, não apenas trocar um rótulo. **Esforço `[INPUT]`:** dias para o transporte local sob representação pronta; semanas–meses para PCT físico.
- `RotationGeneratorBridges.lean` — `{s['RotationGeneratorBridges.lean']}`. Liga `genK=Grot` e `rotGen.map=Grot`, suas exponenciais a `Smat`, e o boost Wick a esses geradores **matriciais**. **Fiação:** representar essa rotação no `H1`/Fock da assinatura e provar o entrelaçamento com o mesmo `D.K`; a identidade 2×2 não faz isso. **Esforço `[INPUT]`:** dias para a ponte matricial já tipada; semanas para a ação física.
- `WickBoostRotation_v2.lean` — `{s['WickBoostRotation_v2.lean']}`. Prova continuação complexa matricial exata boost→`Smat` e a identidade em `2π`; o arquivo declara que isso **não** afirma estado KMS. **Fiação:** ação unitária/antiunitária sobre o par físico e faixa analítica KMS quando requerida, sem confundir a rotação compacta com o boost hiperbólico. **Esforço `[INPUT]`:** dias para consumir a identidade de matrizes; semanas–meses para a ponte modular/KMS física.

[ERRATA AO LADO] O parágrafo histórico acima que diz «não há ... identificação»/«sem rotação/PCT construída» deve ser lido no escopo da **assinatura e do par físico completo**. As pedras de reconhecimento, tela e rotação **existem no kernel**. O que não está demonstrado por elas é `U P_kerK U⁻¹ = C.PF` (ou a correspondência espectral tipada pertinente), nem o operador PCT global no `H1`/Fock/rede da assinatura. `P_ker K = ρ*_IALD` na luz e `ρ* ↔ P_F` por saber externo têm estatutos distintos; nenhum hash ou nome os funde. A tabela original de 12 linhas permanece intacta, Jones segue sem consumidor, e nenhum gate se move.

[EVIDÊNCIA] `O16_AFERICAO_F11.json` registra os seis caminhos, hashes integrais, bytes, âncoras e os dois arquivos da assinatura por hash. Nenhum `um.py` ou original Lean foi alterado; nenhuma compilação nova foi executada para esta classificação.
"""
    change = append_inventory(addition)
    result_doc = {
        "unit": "F1.1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "CAVEAT_APPENDED_FOR_C1_CLOSURE_REVIEW",
        "statute": "REAL_SOURCE_AUDIT_AND_INPUT_EFFORT_ESTIMATES",
        "classification": "EXISTS_IN_KERNEL_NOT_LINKED_TO_QG_SOLUTION_END_TO_END_SIGNATURE",
        "class_one_exception": "D6 selfRecognition U=id in lightImport is already linked for the same light pair",
        "inventory": change,
        "o16_pins": file_record(PINS),
        "historical_result": file_record(ORIGINAL_RESULT),
        "source_count": len(source_rows),
        "sources": source_rows,
        "signature_anchors": anchors,
        "source_files_modified": False,
        "new_lean_compilation": False,
        "gate_changed": False,
        "next_action": "advance F1.1 with new evidence; c1 alone decides FECHADA",
    }
    new_atomic(RESULT, (json.dumps(result_doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"inventory": change, "pins": file_record(PINS), "result": file_record(RESULT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
