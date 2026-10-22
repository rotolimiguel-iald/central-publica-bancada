# R80 — leitura vigente após revisão
[REAL documental] Níveis OH, bomba RF, portas ópticas, EOM e banho engenheirado já existem; ver MATERIAL_AUDIT_R80. Ainda falta a identificação entre modos RF/ópticos/efetivos e a textura correlacionada do mesmo banho. A análise de frequência reaproveita R65/R66, sem nova alegação de impossibilidade geral.
[DERIVED analítico, NOT_LEAN] Critério Gram e teste de fase da janela, mais controle de mistura do modo brilhante, em BATH_IDENTIFICATION_R80. Sob as hipóteses nomeadas, distinguem acoplamentos que têm o mesmo módulo, mas não a mesma fase/dinâmica.
[REAL sintético] Vigente: material_contract_r80_r2.py e RESULT_TESTS_R80_R2.json:31/31 verificações, com os dois ataques que invalidaram a aceitação PSD da R1. O determinante racional verifica os valores binários fornecidos, não incertezas físicas. ERRATA_VALIDATOR_R80 preserva o defeito e o resultado histórico29/29. Os testes não executam trajetória e não estabelecem5sigma.
[OPEN] MATERIAL_DATA_STATUS_R80 não contém calibração fabricada. O resíduo operacional é explicitar o conversor RF–óptico/definição dos modos, ou identificar o banho dirigido que realiza as fases/correlações do salto. R4/R5 integrais continuam abertos; R3/R10 exigem revalidação final. Sem mudança de produção, kernel, um.py ou gate.


## Correção final de não vacuidade
O parágrafo acima que chama R2 de vigente fica superado: final R3,33/33 verificações, exige C11>0 e C22>0 independentemente da tolerância. R2 podia admitir C=0 com tolerância larga apesar de gammaLambda>0. Ver ERRATA_NONVACUITY_R80_R3. Os recibos REVIEW_R80.json/MEMORY_REVIEW_R80.json anteriores não foram aplicados; aceite atual somente REVIEW_R80_R3.json/MEMORY_REVIEW_R80_R3.json.

