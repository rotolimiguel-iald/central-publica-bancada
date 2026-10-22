[INPUT — insumos do ADENDO 001 à ORDEM 015 (alvo T-20), montados por script pela gerência em 23/09/2026; nada move o gate]

# ORDEM 015 — ADENDO 001 — INSUMOS (por onde começar)

1. Leia primeiro o ADENDO: `PARA_CHATGPT\ORDEM_015_ADENDO_001_a_equacao_da_verdade.md`. Leia também, inteira, a ORDEM 015 (`c903681d01eec5ed`), que continua em vigor por inteiro.
2. Confira por script o sha16 de cada arquivo desta pasta contra `MANIFESTO_INSUMOS.json`. O sha16 são os 16 primeiros hex do sha256 dos bytes. Confira ali também o sha16 do adendo, na chave `ordem_arquivo`.
3. `VERBATIM\` guarda o texto que o operador colou, cópia de BYTES. A primeira linha é dele; o resto é [DECLARADO pelo canal ChatGPT]. Leia-o inteiro.
4. `V1_verificacao_independente\` é a verificação matemática da gerência (sympy exato, 51/51 e 9/9). O relatório é transcrição do retorno da frente, com os ids dos checks corrigidos pelo log.
5. `V2_ancoras\` é o que já está no kernel e o que é novo. É cópia saneada; ver `SANEADOS.json`.
6. `V3_pre_resolucao_lean\` é a pedra `TheEquationOfTruth.lean` (46 teoremas, trio), com os logs de todas as compilações da frente.
7. `MEDIDAS_DO_REDATOR\` guarda as reproduções da gerência: a V1 byte-idêntica, a pedra de novo, a variante só-Mathlib e os axiomas de `TheContourOfTruth`. Também as ferramentas: `auditar_axiomas.py` **v2** (recebe PARES fonte + log; confere trio, erros, sorry, COBERTURA e tokens proibidos), o seu autoteste (`autoteste_auditor_v2\`), a v1 preservada com o defeito no nome (`auditor_v1_fail_open\`), `derivar_variante_so_mathlib.py` e a pré-resolução do C2 (`mutantes_C2\`: as 8 mutações geradas e compiladas pela gerência, com os logs).
8. Nada se executa DENTRO de `PARA_CHATGPT`. Copie para `Chatgpt\ORDEM_015_T20_EQUACAO_DA_VERDADE\<ramo>\` só os `.py`/`.lean` e as entradas que eles leem, e rode as cópias lá. Os resultados da gerência se leem aqui, só leitura, para comparação. Nunca se copia o número.
9. `NAO_COPIADOS.json` lista o que não veio, e por quê.
