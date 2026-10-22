# CÉTICO 2 — achado I5 (L129 / L159, «may favor» sem fonte e sha) — NÃO REFUTADO

Medido por script em 22/09/2026 (sha256sum | cut -c1-16; grep -c):
- `Chatgpt\ORDEM_013_RINGDOWN\cache\literature\gwtc5_tgr_abstract.html`: sha16 542a5b672c33e586, 348.283 B, `may favor` = 0 ocorrências.
- `medir\B_catalogos\gwtc5_tgr.txt` = `ORDEM_013BIS_INSUMOS\medicao_da_ampliacao\B_catalogos\gwtc5_tgr.txt`: sha16 d523ae94f23f40b5, 248.915 B; L4656–4657: «selection criteria may favor events with positive damping time / deviations, as these tend to have a larger ringdown SNR» (mesmo sha nas duas cópias).
- `arxiv_2607.19293_gwtc5_tgr.pdf` (medir e insumos): sha16 4ab5df879daa2f4a, 1.894.358 B.
- A mesma frase existe também no GWTC-4.0 (`gwtc4_tgr3.txt` L3546) — a atribuição «GWTC-5.0» na ordem está correta, não é erro.
- Na mesma frase da L129 a citação do GWTC-3 leva «fonte em cache, sha16 9c5271fba4aaa144» (conferido: gwtc3_article_v3.html, 1 ocorrência de «biased towards positive») — a assimetria é real: uma citação com sha, a outra sem.
- L152 (Aceitação da §4.0): «cada número com fonte e sha16» — a gerência exige da bancada o que não cumpriu na L129.
- L159 é verdadeira literalmente (o cache da bancada só tem o abstract) mas omite que o integral está nos insumos (sha acima) — induz redownload ou a resposta «não está em cache».

Gravidade mantida: IMPORTANTE (rastreabilidade/inconsistência interna; não é erro de física nem de estatística).
Correção final: ver StructuredOutput / abaixo.
