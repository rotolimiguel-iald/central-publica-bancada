# CÉTICO 1 — achado da lente regua_hashes_casa sobre a L143 (§4.0, «Estatuto de tudo acima»)

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.**

## O que a ordem diz (lida com numeração)

- L143: «R-RAIZ-0 e R-LIN EXCLUDED_IF_UNIVERSAL (só sobrevivem com partição não universal, do operador)».
- L31 (C1, PAGO_FALSO): «bandeira EXCLUÍDA_SE_UNIVERSAL da R-MOD = null (a própria linha diz que a v369 exclui o análogo terrestre, Unruh-g)».
- L63 (F1): «R-MOD `excluded_if_universal` explícita (true, escopo “se o período KMS do horizonte local vale para relógios de laboratório — Unruh-g; sobrevive só com regra de NÃO universalidade, que é partição do operador”); R-A e R-RAIZ-EP4 com a bandeira em dois campos (P1-matéria: false para ambas; P2-luz nos braços: true para ambas …)».
- L137: «R-LIN … é EXCLUDED_IF_UNIVERSAL na C1» (coerente com a bancada).
- ORDEM 013 (`PARA_CHATGPT/ORDEM_013_confrontacao_do_ringdown.md`): L54 «se a lei for universal, estão excluídas também Unruh-g»; L111 «o mesmo relógio … aplicado a um relógio de laboratório é a alternativa Unruh-g, EXCLUÍDA pelos relógios v369 se a lei for universal. A R-MOD só sobrevive com uma regra explícita de NÃO universalidade».

## Medição na bancada (só leitura) — `ORDEM_013_RINGDOWN\C1_LEITURAS.json`, lido por script

`rows[*].excluded_if_universal`: R-A None · R-B None · **R-MOD None** · **R-RAIZ-0 True** · R-RAIZ-EP4 False · **R-RAIZ-REST True** · R-RAIZ-COHERENT None · **R-LIN True** · R-GLOBAL None · R-PROP None. Idêntico na cópia `cache/delivery_v2_fresh_20260922_032436_194092/C1_C6_ADDENDUM/C1_LEITURAS.json` e na cópia auditada `auditoria/C3_C7_codigo_pacote/bv2/.../C1_LEITURAS.json`. Auditor 1 (aud_1.txt:51,71), auditor 3 (aud_3.txt:45-46,66,155) e auditor 5 (aud_5.txt:85) marcam o null do R-MOD como PAGO_FALSO/CORRIGIR.

## Por que o achado se sustenta

1. A L143 lista dois nomes como se fosse a lista fechada, mas a própria ordem (L31, L63) manda a bancada gravar `true` no R-MOD, e a ORDEM 013 L111 já dizia isso. A frase-resumo contradiz a ordem que a contém: a bancada pode citar a L143 para manter o null (ou gravar false) no R-MOD e dizer que cumpriu o «Estatuto».
2. Omissão adicional, medida: **R-RAIZ-REST = True** na C1 da bancada (nenhum auditor a contestou; aud_3.txt:45 a lista explicitamente: «R-RAIZ-0, R-RAIZ-REST e R-LIN = True»). A L143 a deixa fora sem dizer por quê. E R-A/R-RAIZ-EP4 ficam `true` no campo P2-luz pela L63. Uma lista «fechada» com só dois nomes está errada contra três fontes internas da própria ordem.
3. Não é gosto: é inconsistência interna entre §1 (recibo), F1 (correção ordenada) e §4.0 (estatuto), no ponto exato — a partição — que a régua reserva ao operador. Uma lista incompleta aqui deixa a bancada decidir sozinha quais leituras carregam a condição.

## Gravidade

IMPORTANTE, mantida (inconsistência interna explorável; não induz erro de física nem fabrica número; não decide partição — só deixa de repetir o que já foi decidido em L63).

## Correção FINAL (substituir na L143 o trecho entre «relógio [INPUT]; » e «; todo N é valor esperado»)

**De:** `R-RAIZ-0 e R-LIN EXCLUDED_IF_UNIVERSAL (só sobrevivem com partição não universal, do operador)`

**Para:** `R-MOD (true pela correção de F1, L63; escopo Unruh-g/v369), R-RAIZ-0, R-RAIZ-REST e R-LIN EXCLUDED_IF_UNIVERSAL na C1 (R-A e R-RAIZ-EP4: true só no campo P2-luz, false em P1-matéria, conforme F1) — só sobrevivem com regra explícita de NÃO universalidade, que é partição do operador`
