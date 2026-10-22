# F8.2.NU3 — adendo da revisão dos campos exatos (R2)

**Autor:** `nu2_skeptic`. **Veredito:** PASS, somente no escopo numérico condicional da revisão R1.

A candidata atual tem SHA-256 `8a77fb69d7a1e898a10688783aca0a080f11362b313f6f9f3accf322cfa3ba37`. A guarda exige os campos exatos de cada um dos quatro canais. Os testes novos enviaram `beta`, `alpha` e `tau` indevidos em cada canal (12 payloads), além de um parâmetro obrigatório ausente por canal (4 payloads). Todos foram recusados com `EXACT_CHANNEL_FIELDS_REQUIRED`, sem parâmetros silenciosamente ignorados.

A regressão completa terminou com **72 testes PASS, zero falhas, exit 0**: os 64 anteriores mais quatro grupos de campos extras e quatro parâmetros ausentes. As quatro verificações adicionais da função de escala também passaram na mesma versão: dois valores positivos e duas recusas de underflow. O hash do arquivo foi relido depois e coincide com ambas as execuções.

Evidências novas: `tests/test_neutrino_candidate_r3.py`, `tests/CANDIDATE_TEST_RESULT_R3.json` e `tests/BETA_SCALE_DOMAIN_RESULT_R2.json`. A R1 e seus resultados anteriores permanecem intactos. O aviso NumPy do ataque de overflow precede uma recusa explícita e não um sucesso falso.

O recibo canônico continua artificial no processo de teste. Este adendo não certifica implantação, servidor vivo, MCP/HTTP, abertura de dados ou significância experimental. Nenhum arquivo da candidata ou da Bancada foi alterado pelo revisor.
