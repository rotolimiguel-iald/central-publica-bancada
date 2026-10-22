# R80 — identificação material: o elo ficou localizado

19/10/2026, codex-gerente-tgl, F1.FECHO_20261015, claim985. Continuidade R79, sem reabrir resultados ou repetir trajetórias.

## O que foi reaproveitado
[REAL documental] A patente já contém níveis OH F=1/F=2 e desdobramento Λ, bomba RF, portas ópticas780nm, modulação EOM e o salto J. O artigo Graviton já tem banho nomeado e saltos correlacionados de outro modelo. R66 realiza o gerador por colisões; R74 transporta fases; R79 liga drive/leitura e controla o corte contínuo. A atribuição espectroscópica dos labels da patente fica DECLARADO; não foi validada externamente. SOURCE_PINS_R80 registra cinco textos pesquisados e referências formais reaproveitadas. Não há alegação de ausência em todo o computador.

## O avanço desta etapa
[DERIVED analítico, não Lean] BATH_IDENTIFICATION_R80 torna executável a condição material: mesmo banho exige as duas linhas de acoplamento iguais, com intensidades λ>0 e fase correta. Posto1 sozinho aceita também F1−F2, que é outro salto. A redução OH ao modo brilhante exige bomba alinhada e ausência de mistura por detunings, além do tratamento dos demais canais e das excitações múltiplas.

A condição de frequência não é nova descoberta: a obstrução estacionária já estava na R65/R66. Agora foi ligada às portas e aos níveis efetivamente especificados. No quadro livre usado para esse diagnóstico, o cruzamento contém δ=ωi+ωo−2ωOH. Uma média em janela τ multiplica-o por exp(iδτ/2)sinc(δτ/2). Uma troca de referencial que transporta tudo não elimina essa diferença física. Banhos dirigidos/engenheirados continuam possíveis; seus recursos precisam ser identificados, como na R66.

## Verificação executável
[REAL — sintético] PREREG_TESTS_R80 foi fixado antes da execução:29/29 casos passaram. Um exemplo alinhado/comum/ressonante passa; bomba escura, detunings diferentes, banho independente, fase oposta e janela de fase incompatível são detectados. Entradas ausentes, booleanas, não finitas, banho nulo e matriz não positiva são recusados. β foi calculado em runtime a partir da constante pinada. São testes de álgebra e contrato, não trajetórias, dados do aparelho ou significância experimental. As tolerâncias1e−12 pertencem aos exemplos e não foram escolhidas como tolerâncias físicas.

## A pendência concreta
A pergunta física agora é: **os operadores a_in/a_out do gerador representam diretamente os portos ópticos, modos RF ressonantes ou envelopes obtidos por conversão?**
- Se forem os dois portos ópticos780nm com a transição OH RF, a identificação estacionária/secular nua usada no diagnóstico não satisfaz o bloco comum.
- Se forem modos RF ressonantes, resta ligar esses modos aos portos ópticos.
- Se forem envelopes convertidos ou um banho dirigido, deve entrar a transformação física completa: níveis/tons, amplitudes, fases, correlações e energia fornecida. EOM e Λ-doubling já escritos não bastam, por si, para determinar esse mapa.

Não é pedido para o operador redefinir reconhecimento, Verbo ou espelhamento. É uma distinção de componentes do aparelho, a resolver pelo projeto e sua derivação. MATERIAL_DATA_STATUS_R80 permanece OPEN: nenhum exemplo sintético foi adotado como calibração. Cópias candidatas somente; R4/R5 integrais abertos, R3/R10 aguardam revalidação final. O próximo passo é localizar ou construir esse conversor explícito a partir dos componentes nomeados, com suas hipóteses, sem ajustar β. Nenhum um.py, kernel, produção, dado observado ou gate foi alterado.

