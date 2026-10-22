"""Append the R2 Fase 9 delivery to the four Central memory surfaces."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes")
BASE = ROOT / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019"
F31 = BASE / "F3.1"
F32 = BASE / "F3.2"
HELPER = BASE / "F7.2" / "append_memoria_v2.py"
spec = importlib.util.spec_from_file_location("append_memoria_v2", HELPER)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


marker = "<!-- FASE9_F31_F32_V2_R2_20261008 -->"
module.MARKER = marker.encode("utf-8")
result = F31 / "RESULTADO_V2_R2_F31_F32_20261008.json"
draft = F31 / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json"
exam = F31 / "EXAME_MAPA_TGL_H0_R2_20261008.md"
binding = F32 / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json"
synthetic = F32 / "RESULTADO_RUNNER_V1X_SINTETICO_R2_20261008.json"
module.ENTRY = f"""

## 08/10/2026 — F3.1/F3.2 V2 R2 entregue para reauditoria, sem congelamento

{marker}

[REAL documental] O gerador R7 novo produziu JSON/Markdown V2 R2 e diff por script contra V1 histórico. Rascunho `{draft.name}` SHA-256 {sha(draft)}; recibo novo `{result.name}` SHA-256 {sha(result)}. A c1 decidiu cinco masers sem NGC 4258 como leitor decisório e seis como diagnóstico separado. A grade fixa, só com σ e sem correlação primária central, encontrou σ_comb de 0,8034568 a 0,9492872 nos cinco; a ponta de máximo pode ser interior e tem peso GLS negativo, registrado. Falsificação/tensão usam σ mínimo; discriminação/poder, σ máximo; dispersão falha se qualquer ponta falhar. `mu_do_rito: q→0 (Thomson; Teorema da Escala)` e β₀ = ALPHA_FINE_CODATA_2018 × √e entram no gerador em runtime; K foi recalculado e conferido com o V1. É desenho condicional de poder, não composto observado.

[REAL documental/OPEN mapa] `{exam.name}` SHA-256 {sha(exam)} examina AO LADO as oito conversões de H₀ publicado à likelihood TGL. A Eq. 1 de Pesce+2020 usa ΛCDM plano Ωm=0,315; sua cota de ≲1% para Ωm∈[0;0,5] não foi promovida a cota TGL. O transporte quantitativo de todos os oito leitores permanece [OPEN]. L1b e L6 seguem [DECLARADO_UNVERIFIED] sem fonte pinada; seus centros não foram usados em cálculos desta entrega.

[REAL documental e sintético] F3.2 vinculou o PDF Pesce e sua Tabela 2, inclusive 73,6 +3,1/−3,0, em `{binding.name}` SHA-256 {sha(binding)}. O novo gate lê o draft uma vez, recusa âncora genérica, chave ausente, pin alterado, V1 histórico, assimetria trocada e alegação indevida de admissão. Seis leitores têm conferência documental por hash; L1b/L6 permanecem declarados. A suíte do gate passou 12/12, preflight 3/3 e runner V1.x em estágio sintético 7/7. O ensaio pinado `{synthetic.name}` SHA-256 {sha(synthetic)} exercita covariância/poder, perfil, log-det, quadratura n=100/200 e dispersão do caso sintético, com `verdict=null` e `data_opened=false`; fundo livre do motor e execução real não foram implementados. `n_alvos_declarados` aplica a conjunção de não verificado E não admitido; falta de admissão D-H bloqueia abertura por guarda separada.

[REAL operacional] Mapa seq 832–833; quadro F3.1 evento 297 (`ENTREGUE` para reauditoria), F3.2 evento 298 (anotação complementar, estado anterior `AUDITADA` preservado). O gate antigo `f9_reader_gate.py` ficou intacto, `__pycache__` residual foi removido, `ALVOS_FASE9_LIDOS.json` não foi criado, nenhum dado real foi aberto e nenhum gate foi movido.

[AGUARDA_OPERADOR] F3.4 (especificação governante) e X13/NAT-22 (desvios do executor) precedem o congelamento V2; D-H admite fontes antes de abrir; D-J nomeia o token. F3.3 segue fechada até V2 congelada e AUDITADA pela c1. O rascunho entregue não reivindica completude do runner real nem validação da TGL pela natureza. Referência: «achados D1 a D6 da seq 696». `NOT_FALSIFIED` nunca é `CONFIRMED`.
""".encode("utf-8")


if __name__ == "__main__":
    for target in module.PATHS:
        print(module.append_one(target))
