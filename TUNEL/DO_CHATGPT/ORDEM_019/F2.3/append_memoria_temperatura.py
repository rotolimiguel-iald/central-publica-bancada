"""Append the F2.3 faithful-reading temperature result to Central memory."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
HELPER = BASE / "F7.2" / "append_memoria_v2.py"
SPEC = importlib.util.spec_from_file_location("append_memoria_v2", HELPER)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

F23 = BASE / "F2.3"
FILES = {
    "lean": (F23 / "LiganteLeiCampoCurvoTemperaturaStandalone.lean", "3acf88c76189e69ae100fcd328cf43dc6b1767568c0857d8266baad7796fc62f"),
    "result": (F23 / "RESULTADO_TEMPERATURA.json", "abfd5fda38d39a08c5c420e0cd0037dceb46f6a6b27fa10304a51640cb699950"),
    "hashes": (F23 / "HASHES_TEMPERATURA.json", "8711411312c236885166ecc5bbc74eceb4b9cf44b90a05c89e0b38da303f6da4"),
    "diagnostic": (F23 / "ADENDO_TEMPERATURA_DIAGNOSTICO.md", "da2513df5051ef9d5f2bb1f6783e8dd1a3f5bd3c1c9ee5bd1461c4814748d715"),
    "map": (F23 / "MAPA_TEMPERATURA_20261008.json", None),
}
for label, (path, expected) in FILES.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected and actual != expected:
        raise RuntimeError(f"F2.3 {label}: source changed: {actual}")
    print({"source": label, "sha256": actual})

MOD.MARKER = b"<!-- F23_TEMPERATURA_LEITURA_FIEL_20261008 -->"
MOD.ENTRY = f"""

## 08/10/2026 — F2.3: temperatura da leitura fiel no ligante condicional

<!-- F23_TEMPERATURA_LEITURA_FIEL_20261008 -->

[REAL — kernel em cópia] `LiganteLeiCampoCurvoTemperaturaStandalone.lean` (SHA-256 {FILES['lean'][1]}) compilou em sandbox com Lean 4.31.0, exit 0, sem erro/aviso/sorry; dez `#print axioms` reportaram somente propext, Classical.choice e Quot.sound. Para cada cunha nomeada, `faithful_period_iff` com taxa κ>0 e período P>0 prova κP=2π, `reciprocal_temperature` prova 1/P=κ/(2π), e `boost_defect_with_derived_period` reescreve a identidade de defeito com esse inverso de período. O termo passa as três igualdades à ponte H3 nomeada e conclui Λ único e Gμν+Λgμν=8πG Tμν no atlas suave fornecido sob η=(4G)⁻¹. Recibo {FILES['result'][1]}, manifesto {FILES['hashes'][1]}, diagnóstico {FILES['diagnostic'][1]}. Mapa seq 817; quadro anotação 278; F2.3 permanece AUDITADA até decisão da gerência c1.

[INPUT/OPEN — alcance] A temperatura não é parâmetro numérico independente, mas 1/P permanece relativo à taxa κ livre da leitura. O contrato não identifica κ com `ContratoH2.kappa`/KillingNormalization, nem liga `Circle.exp` à ação do estado ou demonstra KMS. A identidade do defeito já contém κ/(2π) na definição plana e não prova defeito nulo, calor Maxwell ou H3. A ponte H3 exige a lei de Clausius em todas as telas e é logicamente equivalente a essa hipótese, pois as três provas térmicas já seguem do contrato de leitura. Família de cunhas em todas as direções nulas, tensor/fonte Maxwell, conservação curvada e H3 global seguem hipóteses nomeadas. A passagem finita permanece logicamente ociosa ante H3. O ramo C anterior foi reproduzido no standalone por limitação de import do sandbox. Nenhum `um.py`, Nós original, gate, dado da natureza ou candidata gerencial `TheReadingCreatesTheObject.lean` foi alterado.
""".encode("utf-8")

for target in MOD.PATHS:
    if MOD.MARKER in target.read_bytes():
        print({"path": str(target), "status": "already_appended"})
    else:
        print(MOD.append_one(target))
