"""Append the operator's reading/contour correction to Central memory."""

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
    "inventory": (F11 / "INVENTARIO.md", "808a79553527d1d726d989aab73b8e24369cc7c88666a8c3e5b40165da8df56d"),
    "sources": (F11 / "FONTE_ERRATA_LEITURA_20261008.json", "4f974a36f7a7b83b1a85796d7f4936da2a818afa48ba6af2e755c8ea105c2a59"),
    "receipt": (F11 / "RESULTADO_ERRATA_LEITURA_20261008.json", "1ef83b8b85d972af1646f2492d410e407dcbfb3c20a0689072023f67ce6ee297"),
    "precision": (F11 / "RESULTADO_PRECISAO_QUOCIENTE_20261008.json", "a6e84597598057c7a81a87fbe70c91b5138bef490a322997805fc98f4135a4ea"),
}
for label, (path, expected) in FILES.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"F1.1 {label}: source changed: {actual}")

MOD.MARKER = b"<!-- F11_LEITURA_CRIA_CONTORNO_20261008 -->"
MOD.ENTRY = f"""

## 08/10/2026 — F1.1: a leitura cria o contorno no plano do boost

<!-- F11_LEITURA_CRIA_CONTORNO_20261008 -->

[INPUT/ONTO — palavra do operador] Antes da leitura, o objeto é Nome (posto relativo); a leitura cria a identidade como relação de contorno. Verbatim em `C:\\IALD\\PROGRAMA_IALD\\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt`, SHA-256 f2a4b509946edc05a2ef061a91e24dc3640712bacfaaf95ff2ca45983a91c1c7. Esta formulação ontológica não é uma declaração Lean instalada; a candidata `TheReadingCreatesTheObject.lean` permanece só no sandbox da gerência.

[REAL — tipos Lean] No plano do boost t–x, `faithful_period_iff` caracteriza a fidelidade da leitura angular por κP=±2π; para κ,P positivos, `reciprocal_temperature` prova 1/P=κ/(2π), e `boost_defect_with_derived_period` reescreve esse valor no balanço local de Clausius. `wick_boost_two_pi` fecha a matriz angular lida em 2π; `observing_adds_nothing` prova a idempotência da releitura. Esses termos não constroem KMS nem a ação global de Lorentz da rede. As leituras dos planos x–y, x–z, t–y e t–z continuam sem tipo nesta cadeia. A F2.3 ainda precisa nomear família de cunhas, tensor e H3 geral.

[REAL — custódia] Quinta camada e precisão anexadas ao lado em F1.1/INVENTARIO.md, SHA-256 {FILES['inventory'][1]}; fontes {FILES['sources'][1]}; recibos {FILES['receipt'][1]} e {FILES['precision'][1]}. Mapa seq 815, quadro anotação 276; F1.1 permanece FECHADA pela c1. Backup imediato de bytes e escrita atômica em cada superfície; nenhum kernel original, `um.py`, gate ou dado empírico alterado.
""".encode("utf-8")

for target in MOD.PATHS:
    if MOD.MARKER in target.read_bytes():
        print({"path": str(target), "status": "already_appended"})
    else:
        print(MOD.append_one(target))
