# O PROTOCOLO ANTI-PAREDE da gerência (23/09/2026) — vinculante a partir da ORDEM 015

[INPUT — regra da gerência, registrada em 23/09/2026 na superfície de memória da gerência (remissão; o arquivo não vem ao túnel). Vale em toda ORDEM daqui em diante, até ordem em contrário do operador.]

## Por que existe

[REAL] Na ORDEM 013-bis o piloto de PE morreu num erro nativo (rc −11); a gerência reproduziu a falha, localizou-a na caixa de prior registrada e deu o contorno (§2 da ORDEM 015).

## A regra, em sete pontos

1. **A bancada não tem autoridade para declarar parede.** Ela MEDE e CONTINUA. Parede é declaração da gerência, depois de auditar o diagnóstico. «Parede técnica alegada» não se aceita; só «parede medida», e para a bancada o nome certo é **MEDIDA**: cada alternativa da árvore com tentativa EXECUTADA (comando, rc, log com sha256, custo em segundos).
2. **Toda ordem traz a árvore de alternativas com ordem de execução obrigatória** («se A falhar → B → C → D»). Nenhuma parada antes de esgotar a árvore ou o orçamento registrado. Esgotar a árvore = cada ramo executado ou com o seu custo MEDIDO e declarado acima do saldo.
3. **A gerência pré-resolve o bloqueio técnico** (reproduz a falha, acha o contorno) e entrega a RECEITA pronta. A bancada executa a receita; não precisa reinterpretar o bloqueio.
4. **Passos menores, com «continue» explícito** e critério de sucesso verificável. A bancada entrega o parcial e SEGUE — nenhuma parada à espera de recibo.
5. **Nada fica só nas pastas da bancada.** Todo resultado, inclusive espontâneo, entra no túnel na mesma sessão (`ENTREGA_*`), com sha256 — a regra da PORTA aplicada à bancada.
6. **Auto-revisão da bancada não fecha nada.** Revisões internas da bancada são bem-vindas como controle, mas não decidem: a revisão que decide é a da gerência.
7. **Cada ramo interrompido vira MEDIDA.** Quando um ramo falhar, for reclassificado ou parar, a bancada grava uma nota `ENTREGA_015_MEDIDA_<slug>.md` (o que tentou, o que mediu, comando, rc, log com sha256, custo) e segue para o próximo ramo.

## Como a bancada cumpre, na prática

- Um erro, um rc ≠ 0, um `PARTIAL_*`, um EDOM ou uma degenerescência **é dado**: grava-se com sha256 e a árvore segue para o ramo seguinte.
- «Não encontrei reparo validado» é frase de escopo, não veredito de impossibilidade — e só se escreve depois de a árvore estar esgotada, com o custo de cada ramo.
- Custo `null` viola a ordem. Todo item não pago leva o custo estimado com a fonte do número.
- O «fechado» da casa vale: resultado OU falsificador OU parede MEDIDA (e declarada pela gerência).
