# Revisão independente do contrato de veredito F9

[REAL — revisão documental] O contrato fornece cinco estatísticas e interpretações coerentes, separa perfil frequentista de integração bayesiana, preserva a novidade de uso e impede que poder baixo esconda um resíduo. Não encontrei erro matemático na regra max entre cenários seguida de Bonferroni5 sob as hipóteses declaradas. Há uma ambiguidade material na regra terminal do JSON, a corrigir antes de convertê-la em código: ausência de rejeição não pode representar ausência de calibração.

Request18dced03-6d38-4a2e-a2c8-a44ab39ed171, mapa consultado seq474. Revisão por chatgpt-codex/ordem-018/derivacoes. Nenhum centro, composto, solver, simulação, ajuste, integral ou cauda numérica foi aberto/calculado; nenhum controle anterior foi repetido.

## VC-01 — estado de calibração precisa entrar no predicado de decisão

[REAL — localização] F9_VERDICT_CONTRACT_CANDIDATE.json:170 preserva estatísticas sem calibração; a linha175 diz “If no rejection: NOT_FALSIFIED...”, sem exigir calibração válida. A linha174 pede “H1 not rejected” para anunciar discriminação, também sem distinguir teste válido não rejeitado de teste ausente. Como a saída é de campos separados e não uma cadeia de retorno antecipado, a primeira condição não impede sozinha a última.

O documento textual, §8/linha160, já determina corretamente que falta de calibração não vira NOT_FALSIFIED. Portanto o reparo é alinhar as regras de máquina à distinção existente, não criar outra exigência científica.

Recomendação concreta:
- cada teste e cenário deve informar separadamente disponibilidade/validade da calibração, estatística, p ou limite certificado, e decisão;
- não rejeição de H1 exige que COMPAT_H1 e LAW_H1_VS_FREE estejam válidos/calibrados e não rejeitem; indisponibilidade de comparações rivais continua em seus próprios campos;
- uma rejeição robusta e válida de um teste de H1 pode continuar exposta mesmo se o outro estiver indisponível;
- o rótulo combinado “H1 discrimina Hj” exige os controles de H1 válidos e não rejeitados, além do contraste dirigido válido/positivo e corrigido; mera ausência de rejeição registrada não basta;
- p_rob exige toda a família admitida ou um limite certificado para cada caso; omitir cenários indisponíveis ao tomar o máximo não satisfaz o contrato;
- CALIBRATION_UNAVAILABLE/PARTIAL permanece visível e nunca é completado com sigma, p fictício ou rótulo de não rejeição.

Isso não suprime a estatística/resíduo válido, uma rejeição válida ou a preferência bayesiana separada. Também não exige calibração dos três rivais como pré-requisito matemático para dizer que os dois testes próprios de H1 não a rejeitaram; o alcance de cada campo deve ficar explícito.

## Cinco perguntas e modelos

[DERIVED — sob a função de amostragem declarada] G1 testa adequação absoluta; Q1=2(ellhat3−ellhat1) testa a restrição fixa de beta; T21/T41/T51 comparam em direção a H1 sob seus respectivos nulos. Q é não negativo para máximos globais aninhados no mesmo suporte; T pode ser negativo. Exigir T positivo em todos os cenários acrescenta uma condição à rejeição calibrada, sem inflar sua taxa de falso alarme.

Não é correto usar automaticamente graus de liberdade n−p, Wilks, sqrt(delta chi2) ou lnB como sigma; o contrato recusa esses atalhos. O teste de adequação evita interpretar o melhor entre modelos ruins como modelo adequado. Mesmo quando H1 não é rejeitada, isso não a valida: a discriminação é relativa aos rivais definidos e ao contrato.

H3 contém H1 e H2. O teste LAW pode rejeitar a restrição fixa em favor da extensão, mas não pode rejeitar a classe inteira H3 em favor de um membro contido nela. A preferência bayesiana por H1 sobre H3 é pergunta diferente, dependente dos priors normalizados. Não há potência uniforme para separar H1 de toda H3 que inclui H1.

H4 usa a resposta diferencial c_C na rede elementar, não um deslocamento uniforme de todo H0. H5 altera somente a régua BAO e conserva rstar da CMB; não é EDE. A identificabilidade local de h e delta_C observada no preflight262 é condicional e parcial: não demonstra identificabilidade de todos os parâmetros físicos nas267 linhas ou nas600 sensibilidades. Uma interseção observacional entre hipóteses limita poder; não invalida, por si, um teste composto conservador.

## Perfil, integração e nuisance

[DERIVED] Com C_s e X fixos e comuns, o perfil em eta minimiza o resíduo quadrático e a integral plana acrescenta o fator (2pi)^(63/2)/sqrt(det F_s). Como esse fator é comum aos modelos no mesmo cenário, ele pode cancelar em diferenças de perfil/log-integral condicionais; isso não torna os objetos intercambiáveis para normalização absoluta, comparação entre cenários ou modelos com outro X/C/domínio.

A fórmula com pdet C, det F e P está correta sob as condições já qualificadas. Kappa d eta é uma medida comum para razões relativas, não um prior próprio nem uma distribuição geradora. Os priors físicos transportados estão coerentes: s uniforme em[-.15,.15] induz pi_delta=(ln10/1.5)10^(−delta/5); rd uniforme induz pi(q|theta)=rd_CAMB/30 em extremos dependentes de theta. Não se altera a medida por escolher uma parametrização conveniente.

Se toda a rotina respeita Y_local→Y_local+Xv, a coleção de resíduos perfilados é preservada por eta→eta+v. Então a distribuição das estatísticas independe de eta e eta=0 é representante, não sorteio de um prior impróprio. Essa conclusão depende de domínio irrestrito, suporte e seleção invariantes, como o contrato explicita. Posto/whitening por si não prova a invariância de etapas posteriores.

## Supremo composto, sistemáticas e cauda

[DERIVED] Para um cenário verdadeiro s0 admitido, p_rob=max_s p_s≥p_s0. O evento p_rob≤a está contido no evento p_s0≤a. Bonferroni nos cinco testes controla a união dos falsos alarmes por soma de probabilidades, mesmo dependentes e sob nulos diferentes. Portanto não é necessário multiplicar novamente por600 quando a rejeição exige todos os cenários. Selecionar o menor p seria outro procedimento.

A validade exige p_s válido uniformemente no nulo correspondente. Priors físicos não ponderam esse supremo; bootstrap no estimador e grade finita não certificam o contínuo sem argumento adicional. Correlação/deduplicação de etiquetas não substitui covariâncias completas e respostas normalizadas; o contrato preserva isso.

O uso de cinco testes correlacionados não torna Bonferroni errado, apenas potencialmente conservador. O fator5 controla a família declarada, não todas as explorações históricas ou futuras. Fonte comum não cria independência, e declarar seleção anterior não a apaga. A família finita de sistemáticas sustenta conclusão condicional dentro dela, não uma distribuição medida ou exaustão de toda física instrumental. SYSTEMATICS_COVERAGE_LIMITED continua apropriado, sem demandar prova de ausência de toda sistemática imaginável.

[DERIVED — calibração] No nulo simples, a regra de postos (b+1)/(N+1) evita p=0 e tem a interpretação de Monte Carlo indicada. A resolução mínima expressa por ceil(5/alpha5)−1 não é ordem para executar nem certificado de supremo composto. Cota de confiança Monte Carlo com falha de1% não certifica automaticamente uma alegação de5sigma; o orçamento de falha e erros numéricos deve entrar conservadoramente. A distinção entre cauda superior equivalente e cauda bilateral também está correta.

## Opção analítica localizada, sem mudar este candidato

[DERIVED condicional — apenas para a estatística COMPAT_H1 já definida] Seja r_s=rank C_s e p_eta=63. Com erro gaussiano, covariância fixa, X no suporte e parâmetros verdadeiros no domínio de H1:

G1 = min_(theta,eta) RSS ≤ min_eta RSS(theta_verdadeiro,eta)
   = epsilon^T P_s epsilon ~ chi2_(r_s−63).

Logo a sobrevivência dessa chi2 em G1 observado fornece um limite superior conservador para o p composto. Não se trata de Wilks nem de subtrair todos os parâmetros físicos: apenas a projeção linear exata de eta foi usada. Isso pode viabilizar COMPAT_H1 sem uma grade de supremo/Monte Carlo volumoso sob aquele modelo de amostragem.

Nenhuma CDF, estatística observada ou número de poder foi avaliado. Um mínimo local numérico de RSS é um limite superior do mínimo verdadeiro, podendo inflar G; não basta substituí-lo sem certificação conservadora. Erros estimados dos próprios centros e escolhas posteriores continuam exigindo a distribuição/condicionamento declarado. A ROOT já encaminhou uma unidade separada para examinar essa via e suas extensões/certificados; não repetimos essa prova ampliada nem adotamos o método aqui.

## Poder e novidade de uso

[DERIVED] A fórmula simples 1−Phi(Phi^-1(1−alpha)−D) é válida no experimento gaussiano simples declarado, após nuisance. A separação D=5 dá50% de poder no limiar unilateral não corrigido5sigma, não uma garantia. Isso não transforma os sigmas do preflight262 em erro de beta ou potência global do experimento completo. Nenhum delta_mu foi reconstruído nesta revisão.

A prioridade correta é conservar dados/resíduos/estatísticas e decisões válidas antes do campo de poder. Baixo poder esperado não impede ocorrência de uma rejeição válida rara; ausência de rejeição em teste pouco potente não é evidência forte de compatibilidade. Falta de calibração é outra categoria e exige o reparo VC-01.

A regra de novidade de uso está preservada: derivação posterior à existência de dados, estudo de hipóteses e auxílio de IA não desqualificam retrodição sem ajuste. A auditoria de coeficiente, lei e chamadores é distinta de seleção de dados/modelos ou multiplicidade. O contrato remete à proveniência com seus ramos e limites, sem reaproveitar parâmetros de ajuste inverso como previsão fixa. Não reabrimos os originais históricos nem fizemos nova busca de acervo.

## Custódia e encaminhamento

[REAL] Os26 arquivos do manifesto e os16 snapshots conferem. Quinze snapshots ainda coincidem com suas origens atuais. O snapshot F9_MANAGER_REQUEST representa o estado SENT; sua origem foi depois atualizada pela ROOT para RESPONDED, mantendo identidade/escopo e acrescentando recebimento/mapa/manifesto. O backup imediato desse arquivo coincide com o snapshot, preservando a cadeia. Isso é atualização operacional posterior, não corrupção.

A validação documental anterior pinava a nota antes do adendo sobre o piloto da ROOT; o backup correspondente confere e o FINAL_CHECK/manifesto final pinam a nota completa atual. Não há erro de custódia nessa distinção. Os controles teóricos já consumidos foram apenas referenciados, não repetidos; cinco pares de precisão não certificam o prior inteiro ou a cauda estatística.

Encaminhamento: esclarecer VC-01 no candidato ao lado e congelar os predicados antes da implementação. A alternativa A é conceitualmente coerente para uma significância calibrada; a B continua opção de comparação bayesiana sem renomeá-la sigma. A escolha, a calibração e a abertura não são autorizadas por este parecer. Não se emite veredito científico, CONFIRMED ou mudança de gate.
