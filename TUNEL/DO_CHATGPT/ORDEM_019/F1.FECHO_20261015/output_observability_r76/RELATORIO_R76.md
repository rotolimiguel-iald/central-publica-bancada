# R76 — leitura de saída ligada ao preparo intracavidade

Em nome de codex-gerente-tgl. F1.FECHO_20261015, reivindicação967, escopo977. [DERIVED] Demonstração analítica revisada, não Lean. [REAL sintético] Uma campanha pré-registrada, sem dados observados.

## O que foi ligado

A R72 estabeleceu uma testemunha de vácuo/ocupação da cavidade, mas advertiu que quadraturas temporais de saída não são as quadraturas internas. A R76 faz essa passagem pelo instrumento R64/R75 e pelo gerador completo R66. Cada média ou segundo momento bruto é um funcional linear do estado inicial; sua propagação adjunta fornece um operador no suporte inicial admitido. O contato de ruído é mantido. Covariâncias centradas não são usadas como efeitos lineares.

Para o observável A, a aproximação A≈aI+sum(w_l E_l) tem resíduo de norma eta. A leitura v=a+sum(w_l y_l) fornece o intervalo v±Delta, onde Delta=eta+sum(|w_l|*(erro_corte+erro_numerico+erro_modelo+erro_medicao)). A identidade de traço não recebe ruído. O intervalo precisa ser consistente com o espectro; a testemunha R72 só é informativa quando seu limite superior U<1.

A nota OUTPUT_TO_INITIAL_OCCUPATION_R76.md prova o critério de identificabilidade e constrói pares de estados indistinguíveis quando o alvo não pertence ao espaço gerado pelas leituras. O limite é da classe de leituras e preparos nomeados, não uma proibição universal de medir.

## Campanha congelada

[INPUT] Estado inicial desconhecido no suporte total N≤1 (dimensão4); gerador cortado em N≤3 (dimensão16), com todos os termos R66. 61features: identidade exata e60 momentos brutos de quatro configurações de LO em três janelas (.25,.5,.75). Sete estados sintéticos de validação, fixados antes. Pesos por pseudoinversa calculados a partir do instrumento/alvo, sem ajuste aos resultados dos estados.

As taxas, o relógio e os ganhos são INPUTs do modelo, inclusive Gamma; beta é calculado em runtime da constante pinada. Não se extrai uma calibração independente do modelo que a recebeu como entrada. Orçamentos de erro estatístico e de diferença de modelo foram postos em zero SOMENTE para o caso sintético de mesma equação. As margens numéricas são INPUT, sem aritmética intervalar validada. No aparelho real esses campos precisam de limites justificados e cobertura simultânea.

## Resultado discriminado

[REAL sintético] 1050/1050 controles PASSA, exit0, 1.115029s. Maior discrepância adjunto/primal: 3.33066975926e-16. Posto numérico do desenho normal: 16/16; no controle de portas desacopladas: 1/16. Posto numérico não é prova de precisão experimental nem tomografia física realizada.

| Alvo inicial | Resíduo no corte | Amplificação L1 de erros das leituras | Cauda R75 amplificada | Erro total condicional |
|---|---:|---:|---:|---:|
| N_b: dois modos de luz | 8.7150974e-14 | 1267.5451 | 0.02548946 | 0.025490729 |
| N_total: luz + OH | 3.2399777e-12 | 89174.912 | 3.6981769 | 3.6982661 |

**Dois modos de luz:** no caso sintético preparado no vácuo, o intervalo é [0; 0.0254907289]. Sob as hipóteses e margens declaradas, a testemunha dá p_vac≥0.9745092711. Isso limita a população do vácuo do estado no modelo; NÃO é nível de confiança experimental, probabilidade de a teoria ser verdadeira ou confirmação física. O espectador e o OH não são certificados por esse alvo. Os casos totalmente ocupados devolvem corretamente ausência de certificado de vácuo; não são falha da teoria.

**Luz + OH:** embora haja reconstrução algébrica no corte, o erro propagado excede todo o intervalo físico[0;1]. Todos os sete casos ficam INCONCLUSIVE para certificar o vácuo conjunto. A cauda de corte conservadora amplificada domina o orçamento; o resultado não mede ruído real nem prova impossibilidade de outro desenho ou pesos. Não foram trocadas janelas, cortes, pesos ou tolerâncias depois de ver o resultado.

**Controle sem portas:** a saída contém apenas ruído proporcional à identidade; os alvos não são reconhecíveis. Resíduos 0.5 e 0.75, intervalos triviais. O controle impede que saída de vácuo seja confundida com cavidade vazia.

Os dados de validação são gerados no corte finito. Os intervalos chamados conditional_continuum_interval são certificados condicionais ao orçamento declarado, apoiados pela transferência uniforme R75; não são leituras observadas de um aparelho ou execução direta do Fock infinito. O campo legado max_equality_residual inclui o resíduo esperado do controle negativo; não é erro global da integração.

## Atalho preservado e próximo passo

PHOTON_COUNTING_ALTERNATIVE_R76.md demonstra, no instrumento de contagem finito nomeado, m_j(T)=kappa_j integral<n_j(t)>dt e um erro de janela limitado por T||G†n_j||/2. É alternativa analítica NÃO executada nem já implementada nesta campanha; seu limite bosônico e sua calibração continuam explícitos. Não permite concluir que reduzirT gratuitamente aumentaria a precisão: a incerteza de contagem é dividida porT.

Próximo trabalho material: reaproveitar o diagnóstico para ligar a leitura/controle do setor OH já presente no acervo ou obter uma cota de propagação mais informativa, fixando qualquer novo desenho antes da execução. O resultado atual já fornece a ponte saída→testemunha dos dois modos no contrato estudado; ela não deve ser reconstruída.

[OPEN] Preparação geral fora deP1, parâmetros/calibração independentes do aparelho, realização global e critérios integraisR4/R5. Não houve provedor, novoLean, produção, dado observado ou gate.

