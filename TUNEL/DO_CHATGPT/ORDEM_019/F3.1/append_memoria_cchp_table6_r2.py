"""Append the CCHP Table 6 side correction to Central memory."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
BASE = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019"
HELPER = BASE / "F7.2" / "append_memoria_v2.py"
spec = importlib.util.spec_from_file_location("append_memoria_v2", HELPER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


adendo = BASE / "F3.1" / "ADENDO_R2_CCHP_TABELA6_NOTA_A_20261008.md"
source = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_018" / "h0dn_documentary_review" / "jagb_extension" / "residual_systematics" / "sources" / "cchp_overview.txt"
marker = "<!-- F31_R2_CCHP_TABLE6_NOTE_A_20261008 -->"
module.MARKER = marker.encode("utf-8")
module.ENTRY = f"""

## 08/10/2026 — F3.1 R2: âncora CCHP Tabela 6 nota a ao lado

{marker}

[REAL documental] Após a entrega R2, a conferência da fonte integral `cchp_overview.txt` (SHA-256 {sha(source)}, linhas 205, 272 e 928–938) localizou a Tabela 6, nota a: o sistemático comum do TRGB inclui 1,5% da distância de NGC 4258 e a incerteza da medida TRGB. O H₀ publicado tem `70,39 ±1,22(stat) ±1,33(sys) ±0,70(SN)`; 0,024 ⊕ 0,022 mag da distância geométrica e 0,025 mag do TRGB são componentes da decomposição. A V2 R2 já usava `a₂N=1,0548837955` e `a₂T=0,8100124555` como tetos de sensibilidade, cuja quadratura recompõe o 1,33; não se soma 1,33 novamente à diagonal. A citação literal da nota a faltava no JSON/Markdown R2 e foi acrescentada **ao lado**, sem sobrescrever evidência, em `{adendo.name}` (SHA-256 {sha(adendo)}). Mapa seq 834; quadro evento 299. A covariância conjunta continua [OPEN], e o adendo não admite fontes, não abre dados nem move gate.
""".encode("utf-8")


if __name__ == "__main__":
    for target in module.PATHS:
        print(module.append_one(target))
