"""Append the audited-scope F2.3 branch C update to Central memory."""

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
    "lean": (F23 / "LiganteLeiCampoCurvoRamoC.lean", "56a186a39bf5dc44f3e0e9065bbb384f558afaf61b855672a57a412dd1b4c033"),
    "result": (F23 / "RESULTADO_RAMOC.json", "b773379c02d63bc1bf0d55921644fa16d94dfb8052da70ed49c6eb922ef3174d"),
    "hashes": (F23 / "HASHES_RAMOC.json", "b22aa09ed1121cfd252fc164d89cc0bc1fee9a60e3125b9c95d09db4704dcfcb"),
    "diagnostic": (F23 / "ADENDO_RAMOC_DIAGNOSTICO.md", "f88d2b21a0f82820aa15ed33309969f052ed970ad74b88f197ee542a7a20e0a5"),
}
for label, (path, expected) in FILES.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"F2.3 {label}: source changed: {actual}")

MOD.MARKER = b"<!-- F23_CURVED_FIELD_BRANCH_C_20261008 -->"
MOD.ENTRY = f"""

## 08/10/2026 — F2.3: ramo C com cunhas e tensor nomeados

<!-- F23_CURVED_FIELD_BRANCH_C_20261008 -->

[REAL — kernel em cópia] A pedra `LiganteLeiCampoCurvoRamoC.lean` (SHA-256 {FILES['lean'][1]}) compilou na cópia do kernel do Nós com Lean 4.31.0, exit 0, sem erro/aviso/sorry; `#print axioms` reportou apenas propext, Classical.choice e Quot.sound. O teorema `passage_with_light_lorentz_wedges_all_null_h3_to_einstein_atlas` aplica a implicação v338 ao atlas fornecido e conclui Λ único e coeficiente 8πG com η=(4G)⁻¹. Recibo {FILES['result'][1]}, hashes {FILES['hashes'][1]}, diagnóstico {FILES['diagnostic'][1]}. Mapa seq 814; quadro anotação 275; F2.3 permanece AUDITADA até reauditoria c1 deste adendo.

[INPUT/OPEN — limites] A família de cunhas é hipótese pontual por carta/ponto/direção nula, sem representação global coerente de Lorentz/Poincaré. H3 de todas as telas, a identificação `recordSource = M.T.T ψ` e a conservação covariante curvada entram como hipóteses nomeadas. A tela do registro não é derivada da cunha, `ψ` não é ligado ao domínio regular de `lightH3`, e H3 não é derivado do estado. A passagem finita permanece logicamente ociosa ante a hipótese H3, como mostrou a auditoria c1 anterior; este ramo explicita a fiação, sem ganho de conteúdo físico frente à implicação v338. Nenhum `um.py`, kernel original, gate ou dado da natureza foi alterado; a integração v392 pertence à gerência.
""".encode("utf-8")

for target in MOD.PATHS:
    if MOD.MARKER in target.read_bytes():
        print({"path": str(target), "status": "already_appended"})
    else:
        print(MOD.append_one(target))
