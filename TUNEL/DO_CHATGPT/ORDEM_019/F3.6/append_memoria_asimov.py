"""Append the F3.6 Lambda power result with immediate byte backups."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HELPER = Path(__file__).resolve().parents[1] / "F7.2" / "append_memoria_v2.py"
spec = importlib.util.spec_from_file_location("iald_memory_append", HELPER)
assert spec and spec.loader
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

helper.MARKER = b"<!-- F36_ASIMOV_LAMBDA_ENTREGUE_20261008 -->"
helper.ENTRY = """

## 08/10/2026 — F3.6: portão C16 aferido no tangente Λ

<!-- F36_ASIMOV_LAMBDA_ENTREGUE_20261008 -->

[REAL numérico local] CAMB 2.0.4 no WSL e Fisher de 15 observáveis sintéticos/6 parâmetros livres, sob fundo nu V3 e covariâncias corrigidas DESI D_M–D_H/Planck, deram σβ=0,01804348 para β=ALPHA_FINE_CODATA_2018×√e=0,012031300400803142 em runtime. As composições A e B′ coincidem na Jacobiana do ponto Λ (β=0,w0=−1,wa=0). Nos passos testados σβ variou de 0,01790070 a 0,01836213, mínimo 1,4878β: `UNDERPOWERED_DO_NOT_OPEN_DATA`. Fontes primárias de covariância: https://arxiv.org/html/2404.03002v3 e https://arxiv.org/html/1808.05724 .

[REAL/OPEN — limites] O teste exigente de precisão a 0,5% falhou (variação até 1,77%); o negativo vale sob a especificação local declarada. D1F-04 na convenção l_A, likelihood CMB completa, CPL fora de Λ, cruzamento phantom, âncora futura e injeção com ruído não foram aferidos. Médias observadas publicadas apareceram incidentalmente ao ler código/artigo, mas nenhuma entrou na conta nem foi ajustada. O dado observado não foi aberto para o controle 2, e o portão ordena não abri-lo.

[EVIDÊNCIA] F3.6/ENTREGA_ASIMOV_LAMBDA.md SHA-256 d5a6f0dd25cb88f6682510038746e815f913d157667e8336e5f6898d348cfe97; ASIMOV_LAMBDA_SANDBOX/RESULTADO_ASIMOV_LAMBDA.json SHA-256 d6fe92487ac667d0e59288df0aa6e7cc594fb0e6c9e257031741ef065af16912; VALIDACAO_GATE.json SHA-256 075ee78e8f717cd88dc031dcae886eeac77e701854945d7cf7ba4eff07c5999f. Mapa seq 808, quadro F3.6 ENTREGUE evento 268. A gerência c1 decide FECHADA após reauditoria; nenhum gate, um.py ou original científico mudou.
""".encode("utf-8")


if __name__ == "__main__":
    for target in helper.PATHS:
        print(helper.append_one(target))
