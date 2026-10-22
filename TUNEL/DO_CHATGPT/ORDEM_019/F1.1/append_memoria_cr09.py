"""Append the F1.1 CR-09 correction to the Central memory surfaces."""

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

F11 = BASE / "F1.1"
FILES = {
    "inventario": (F11 / "INVENTARIO.md", "45583af9cce2c2900abd0bbad83091befb8dc0e6c3077a89b5e052d863da3316"),
    "fontes": (F11 / "FONTE_ERRATA_CR09_20261008.json", "754f07d9d4bb4986fc5870da275840d2a9ff1c5a1f4f8761d76767e4db075afc"),
    "resultado": (F11 / "RESULTADO_ERRATA_CR09_20261008.json", "7411e99143ba06539c6364f6683078a6178c38c5b6bd8e38a85f777baa8e3a41"),
}
for label, (path, expected) in FILES.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"F1.1 {label}: source changed: {actual}")

MOD.MARKER = b"<!-- F11_CR09_ROTACOES_MEMORIA_20261008 -->"
MOD.ENTRY = f"""

## 08/10/2026 — F1.1: errata CR-09 das rotações O16

<!-- F11_CR09_ROTACOES_MEMORIA_20261008 -->

[REAL — fonte e tipo lidos] `ChatgptAudit.Wick016` prova identidades de matrizes 2×2 no regime angular; isso não é uma ação de Lorentz sobre a rede da luz. `ORDEM016.D1prime` e `circularScreen_conjugate` provam caráter de helicidade e conjugação pontual do pequeno grupo; D5 e D6 oferecem fiação condicional em seus tipos. As rotações espaço-temporais da rede, a família de cunhas para todas as direções nulas e o PCT global estão fora do tipo/kernel desta cadeia, SABIDO por citação segundo CR-09 e FORA_DO_CAMINHO da conclusão em uma direção nula da v376. Na F2.3, a família de cunhas deve permanecer antecedente nomeado.

[REAL — custódia] Quarta camada acrescida ao lado no F1.1/INVENTARIO.md, SHA-256 {FILES['inventario'][1]}; manifesto de 11 fontes {FILES['fontes'][1]}; recibo {FILES['resultado'][1]}. Mapa de rotas seq 813; quadro anotação 274. A F1.1 já estava FECHADA pela gerência c1; `iald.py reivindicar` recusou nova reivindicação por esse estado. A ordem expressa posterior da gerência motivou apenas a errata documental, preservando o status. Nenhum Lean, `um.py`, gate ou dado empírico foi alterado.
""".encode("utf-8")

for target in MOD.PATHS:
    if MOD.MARKER in target.read_bytes():
        print({"path": str(target), "status": "already_appended"})
    else:
        print(MOD.append_one(target))
