# CÉTICO 2 — achado L143 (§4.0) «R-RAIZ-0 e R-LIN EXCLUDED_IF_UNIVERSAL» omite a R-MOD

**Veredito: refutado = false (achado CONFIRMADO e ampliado). Gravidade mantida: IMPORTANTE.**

## Medição (por script, 22/09/2026)

1. `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C1_LEITURAS.json` (só-leitura), campo `rows[*].excluded_if_universal`:
   R-A null · R-B null · **R-MOD null** · **R-RAIZ-0 true** · R-RAIZ-EP4 false · **R-RAIZ-REST true** · R-RAIZ-COHERENT null · **R-LIN true** · R-GLOBAL null · R-PROP null.
   Idêntico na cópia `cache/delivery_v2_fresh_20260922_032436_194092/C1_C6_ADDENDUM/C1_LEITURAS.json`.
2. ORDEM 013-bis L31 (C1, coluna PAGO_FALSO): «bandeira EXCLUÍDA_SE_UNIVERSAL da R-MOD = null (a própria linha diz que a v369 exclui o análogo terrestre, Unruh-g)». L63 (F1): «R-MOD `excluded_if_universal` explícita (**true**, escopo "se o período KMS do horizonte local vale para relógios de laboratório — Unruh-g; sobrevive só com regra de NÃO universalidade, que é partição do operador")». L137 (g): «R-LIN … é EXCLUDED_IF_UNIVERSAL na C1».
3. ORDEM 013 (`TUNEL\PARA_CHATGPT\ORDEM_013_confrontacao_do_ringdown.md`) L53: se universal, excluídas «lei-raiz com k̄ = 0» e «k̄ = massa de repouso»; L54: Unruh-g e GM_⊕/c³; L111: «A R-MOD só sobrevive com uma regra explícita de NÃO universalidade, e essa regra é partição, do operador».
4. Auditorias: aud_1.txt:51,71 e aud_3.txt:63,66,155 e aud_5.txt:85 pedem exatamente `R-MOD.excluded_if_universal` → true/condicional.
5. `grep -c "R-RAIZ-REST"` na ORDEM 013-bis = **0**.

## Conclusão

- A L143 se apresenta como «Estatuto de tudo acima» e lista a bandeira EXCLUDED_IF_UNIVERSAL como par fechado {R-RAIZ-0, R-LIN}. A própria ordem, em L31 e L63, MANDA a bancada gravar `true` na R-MOD. A frase-resumo contradiz a correção que a ordem exige — inconsistência interna, e a bancada pode ler L143 como a lista autoritativa (é a linha de estatuto) e deixar a R-MOD em null «porque o resumo não a nomeia». Não é gosto: é número (a bandeira) contra frase.
- Ampliação: R-RAIZ-REST está `true` no arquivo da bancada e na ORDEM 013 L53 («k̄ = massa de repouso»), e a ordem-bis nunca a nomeia. Efeito nulo no ringdown (SINTESE.md:55, z ~ 1e-41), logo não muda N nem portão — mas um resumo de estatuto que se diz completo e omite uma bandeira `true` lida do artefato fere «o número corrige a frase». Cabe na mesma emenda, com custo zero.
- Não é BLOQUEANTE: não induz erro de física nem decide partição (a frase preserva «do operador»); é omissão que a bancada pode explorar. IMPORTANTE mantido.

## Correção FINAL (substituir na L143 o trecho exato)

DE:
`R-RAIZ-0 e R-LIN EXCLUDED_IF_UNIVERSAL (só sobrevivem com partição não universal, do operador)`

PARA:
`R-MOD (true pela correção da F1, L63), R-RAIZ-0, R-RAIZ-REST e R-LIN EXCLUDED_IF_UNIVERSAL — as três últimas `true` lidas de `C1_LEITURAS.json` [REAL] — (só sobrevivem com regra explícita de NÃO universalidade, que é partição, do operador; ORDEM 013 L53–54, L111)`
