# R72 — testemunha de preparo nos modos locais da cavidade

Em nome de codex-gerente-tgl, 18/10/2026. [DERIVED — demonstração analítica, NOT_LEAN]. Reaproveita a fatorização local R71 e o contrato de quadraturas/portas R63–R64; não postula uma nova leitura de beta nem presume aparelho realizado.

## Objeto e normalização

Os dois pares q_r,p_r são os mesmos pares canônicos da realização R71, com [q_r,p_s]=i delta_rs, b_r=(q_r+i p_r)/sqrt(2). Quadraturas adimensionais; domínio de forma de N_b; rho positivo de traço1 com segundos momentos finitos. O espectador e o OH permanecem no estado conjunto, inclusive se entrelaçados. Não se assume estado gaussiano, pureza ou produto inicial.

Com X=(q_i,p_i,q_o,p_o), d_a=Tr rho X_a e V_aa=Tr rho (X_a-d_a)^2,

    epsilon_field = Tr rho N_b = (Tr V + ||d||² - 2)/2 >= 0.

São necessárias quatro medidas de segundo momento e suas médias, em configurações separadas no MESMO preparo. A soma dos momentos brutos também serve. Correlações cruzadas não são necessárias para esta testemunha, mas continuam necessárias para reconstruir a forma simplética/identificar os modos. Remover médias subestima a ocupação de estados deslocados. Preservar ganho, fase, bandas e normalização de comutador; não ajustar estes parâmetros para obter epsilon pequeno.

## Prova do certificado sem hipótese gaussiana

Seja P0=|00><00| no fator dos dois osciladores, tensor identidade no resto. Pelo espectro inteiro não negativo de N_b, I-P0 <= N_b como formas. Logo

    p0=Tr rho P0 >= 1-epsilon_field.

Para a REDUÇÃO rho_b dos dois modos,

    ||rho_b - |00><00|||_1 <= 2 sqrt(1-p0) <= 2 sqrt(epsilon_field).

A prova da primeira desigualdade pode ser dada por purificação: projete uma purificação de rho em P0 e normalize. O módulo do produto interno é sqrt(p0), e a distância-traço dos projetores puros é 2sqrt(1-p0). A contração da norma-traço sob traço parcial conclui. Para p0>0, o mesmo argumento ANTES de descartar o espectador mostra

    ||rho - |00><00| tensor sigma_rest,conditional||_1 <= 2 sqrt(1-p0).

A preparação assim certificada não determina sigma_rest,conditional, nem o identifica com Omega_spec. Portanto não certifica o vetor global particular Omega_b de R71. Certifica a redução local e proximidade a um produto com o restante condicionado. Essa distinção é necessária à referência física.

Para incluir OH no fundamental, defina epsilon_joint=<N_b+n_e>. O mesmo gap1 vale para P00g tensor I_spec. Inclui-se a medida independente de <n_e>; não se deduz estado OH das quadraturas ópticas. Se epsilon>=1, use apenas a cota trivial de distância2; não se declara p0>0. Se epsilon=0 exatamente, rho está no suporte do projetor do vácuo local (e do OH se incluído), mas o espectador continua livre.

## Preparação e dinâmica: quando usar

Aplicar antes da etapa cuja condição inicial exige o vácuo local. Com bomba ligada, esse vácuo não é em geral estacionário. Esperar um múltiplo de tempo térmico, como no protocolo M1, não fornece sozinho a cota epsilon: precisa do espectro/estado/ruído pertinente. A testemunha aqui dá critério quantitativo para testar esse preparo. Não afirma que se consiga epsilon arbitrariamente pequeno nem que perdas/banho correspondam aos parâmetros da patente.

## Erro de leitura e cobertura estatística

Se quatro limites superiores simultâneos U_a para <X_a²> têm cobertura conjunta1-alpha_stat, então

    epsilon_upper=(sum U_a - 2)/2

é um limite superior com a mesma cobertura, desde que as calibrações/modos/normalizações sejam válidos. Para o certificado conjunto, acrescentar o limite superior da ocupação OH com cobertura conjunta. Não confundir alpha_stat com a constante da estrutura fina. Um limite negativo é incompatível com as hipóteses de normalização/cobertura desta realização: recusar o certificado, não zerar silenciosamente. Se forem usados limites de variâncias/médias separados, propagar os erros das médias quadradas; somar somente variâncias é incorreto. O orçamento estatístico, ganho, ruído de detector, eficiência e deriva de preparo ainda devem ser fixados no rito real. Nenhum sigma foi calculado aqui.

## Porta e cavidade: a ponte ainda exigida

O R64 fornece momentos de modos TEMPORAIS de saída filtrados, não de b_r instantâneo da cavidade. A mesma testemunha pode certificar o vácuo desses modos de saída, mas não transporta o certificado à cavidade sem inversão/estimativa de observabilidade do instrumento. Contraexemplo simples: uma porta desacoplada (kappa_ext=0) tem saída de vácuo com cavidade ocupada. Ganho conhecido sozinho não elimina a diferença temporal. Mesmo kappa_ext>0 requer o mapa temporal completo e os outros canais, sem desligar termos do gerador para fabricar a identificação.

Este critério usa o espectro de número e quadraturas, sem beta de entrada. Isso evita circularidade no preparo; não mede beta e não fornece Gamma independente.

## Verificação sintética proposta, não experimento

O script adjunto avaliará estados de suporte finito no Fock infinito, com espaço ampliado suficiente para aplicar uma quadratura antes de tirar sua norma. Testará a identidade de segundos momentos, a desigualdade de gap, as distâncias da redução e do produto condicionado, a necessidade das médias e o ramo sem certificado (epsilon>=1). Estados com espectador entrelaçado serão incluídos. O pré-registro e a revisão precedem qualquer execução; não se repetem os controles R71.
