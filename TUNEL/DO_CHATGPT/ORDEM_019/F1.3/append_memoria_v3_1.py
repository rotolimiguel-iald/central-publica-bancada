"""Append the F1.3 v3.1 addendum with byte backups to Central memory."""

from __future__ import annotations

import importlib.util
from pathlib import Path


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
HELPER = BASE / "F7.2" / "append_memoria_v2.py"
spec = importlib.util.spec_from_file_location("append_memoria_v2", HELPER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

module.MARKER = b"<!-- F13_V31_FACTIBILIDADE_20261008 -->"
module.ENTRY = """

## 08/10/2026 — F1.3 v3.1: tabela de factibilidade ao lado da v3 auditada

<!-- F13_V31_FACTIBILIDADE_20261008 -->

[REAL — estado] A F1.3 já foi entregue como v3 (quadro evento 238) e reauditorada pela c1 como AUDITADA/APROVA_COM_RESSALVAS (evento 249; custódia corrigida ao lado no evento 281). O relatório real é C:\\IALD\\PROGRAMA_IALD\\auditorias\\F1.3\\AUDITORIA_F1_3_V3_C1_ab8cb3e7.md, SHA-256 89979aec3ec3b624a13e6fd3ce0e6853d413079b2d777f79b86a1124cb4393b8. A v3 registrada, SHA-256 599f7bcccc2a3804aa6420427b00b492783671f0b83a15b0f9ff7f524b60f457, permanece intacta. Seis pedidos foram atendidos; a tabela Mathlib estava parcial.

[REAL documental] O complemento F1.3/COMPLEMENTO_V3_1_FACTIBILIDADE_20261008.md, SHA-256 3b4986c319f77bc15f0bc344af4e63fbe4376aeccc02cfae458b53924fe5fd6e, anexa por D0.5–D7 as referências arquivo:linha no pin Lean v4.31.0/Mathlib fabf563a7c95a166b8d7b6efca11c8b4dc9d911f. Foram conferidas 35 referências de arquivo e intervalo, zero inválidas. D1a.1 declara [OPEN] a isometria de Fubini L² vetorial sobre produto, não localizada pela c1 no pin; `MemLp.comp_fst/comp_snd` e Fubini de integrais não são essa equivalência. A nota nomeia as hipóteses 61–66, propõe só ao operador uma interface antinula colada a `D.K` e conserva Araki/EO/LRT/BGL como atalhos [KNOWN] condicionais, com divergência bibliográfica explícita para os preprints LRT.

[EVIDÊNCIA] F1.3/RESULTADO_V3_1_FACTIBILIDADE_20261008.json SHA-256 5263f4aac4063173f688a372fbe803c8fab51a8adda8f36fad73a18167445bdc. Mapa seq 830; quadro anotação evento 294. A c1 deve ler o complemento, sem promover esta anotação a reauditoria. D1a.1–D7 físicos continuam [OPEN]. Nenhum Lean novo compilado, MiMo chamado, dado real aberto, kernel/um.py alterado ou gate movido.
""".encode("utf-8")

if __name__ == "__main__":
    for target in module.PATHS:
        print(module.append_one(target))
