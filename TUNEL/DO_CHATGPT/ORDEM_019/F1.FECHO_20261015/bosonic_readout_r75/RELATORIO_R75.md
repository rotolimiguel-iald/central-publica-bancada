# R75 — ligação do leitor ao gerador bosônico completo

Em nome de codex-gerente-tgl. Unidade F1.FECHO_20261015, reivindicação967, escopo975. Execução única congelada após revisão independente; resultados em RESULT_R75.json.

## Avanço material

[DERIVED — demonstração analítica, não Lean] Reutilizamos o semigrupo bosônico completo R66 e o instrumento R64/R74. Para uma preparação com suporte N≤m0 e observação em tempo finito T, demonstramos limites únicos dos primeiros e segundos momentos filtrados, covariâncias e decoder, com cotas explícitas do erro de corte. O reconhecimento/releitura R57 permanece disponível como operação linear. A nota BOSONIC_FILTERED_MOMENTS_R75.md contém a demonstração e as hipóteses.

A norma-traço convergente dos estados, sozinha, não controlaria observáveis ilimitados. A ponte adicional controla cada inserção de leitura pela ocupação e soma as caudas ponderadas da expansão Dyson: peso sqrt(m0+n) para uma inserção, m0+n para duas, multiplicados por (2|Omega|T)^n/n!. O multinômio dos intervalos dá T^n/n!, sem fator combinatório extra. O contato de ruído é igual entre os cortes. As fases R74 comutam com N e conservam as cotas.

## Verificação sintética

[INPUT] Cortes totais N≤2,3,4 (dimensões9,16,25), suporte inicial N≤1, T=.75; mesmo gerador com cinco saltos, JC e bomba. Parâmetros adimensionais, Gamma sintético e beta em runtime; quatro configurações de quadratura separadas por corte e um quadro girante no corte3. Plano e tolerâncias pinados antes de START.

[REAL sintético] 181/181 critérios PASSA, exit 0, 1.353316s. Maior resíduo nas identidades de transporte de quadro: 5.8351366594e-12, tolerância ODE3e-8. As diferenças máximas entre médias dos cortes2 e4 foram 4.01275368489e-08; entre seus segundos momentos, 2.7364677857e-08. As diferenças3→4 são menores que a tolerância ODE e não certificam precisão de14casas. Nenhum corte foi tratado como solução infinita exata.

Cota analítica por corte4 para médias: [6.375796982324104e-06, 4.534053982986321e-06]; para C/B reconstruídos sem ganhos: 5.37309555789e-06; para C/B centrados: 1.09721801285e-05. São cotas superiores conservadoras do modelo, não intervalos estatísticos nem erros empíricos medidos. A comparação numérica agrega tolerância de integração3e-8, sem certificação por aritmética intervalar.

Os quatro controles algébricos previstos detectaram: coeficiente Pauli em lugar de sqrt(2) (0.414213562373); quadrado após projeção em lugar da projeção do quadrado (1.5); omissão dos contatos de ruído (0.845 e 0.32). São controles da implementação/normalização, não quatro experimentos físicos.

O campo legado max_equality_residual do wrapper inclui diferenças entre cortes; seu nome não transforma essas diferenças em identidades. Os valores discriminados em checks/cut_comparisons são os referentes válidos.

## Acervo e alcance

[REAL — busca focal] Foram consultados69 arquivos de extraçãoR67, com2414parágrafos, pelos padrões registrados. Não houve hit; isso não cobre o acervo integral, equaçõesOMML ou imagens e não demonstra inexistência de calibração. R65/R72 já delimitam normalizações e requisitos físicos; não foram reconstruídos. Ver FOCAL_ACERVO_SCOPE_R75.txt.

[OPEN] R75 obtém um funcional de momentos como limite dos instrumentos finitos. Não constrói a unitária HP ilimitada, a distribuição completa de trajetórias nem o campo de saída global. Não estende a prova a estados iniciais arbitrários ou T infinito. A identificação física do aparelho e Gamma independente continuam com o alcance documental anterior; R4/R5 integrais permanecem abertos. Sem provedor, novo Lean, produção, dado observado ou alteração de gate.

Próxima ação: reaproveitar a ponte demonstrada para os contratos de preparo/canais e a realização restante da rede. Não pedir novamente a definição de realização/satisfação ao operador nem reconstruir R57/R64/R66/R74/R75.

