# Fase9 — montagem comum proposta para as cinco hipóteses

[DERIVED condicional / PROPOSTA NÃO RATIFICADA] Este desenho conecta as peças já revistas. Não abre médias observadas, não monta a covariância numérica, não calcula ajuste/evidência e não substitui o V1. A reprodução histórica E45 usa outro contrato e permanece separada.

## Um vetor de dados por comparação

A proposta é usar o bloco de fundo Planck comprimido + DESI DR2 e a rede local H0DN V01, com fontes, seleção e normalizações comuns. A validade da compressão e a fatoração entre blocos precisam ser explicitadas; ausência de uma covariância cruzada não prova independência. O H0 publicado pelo H0DN, seus ramos SH0ES/CCHP, as mesmas SNe Pantheon+ e N4258 não entram novamente como dados adicionais. Sirenes/lentes/escada inversa são extensões separadas até terem mapa observável e dependências qualificados.

No recorte R-A, theta descreve o fundo nu. Defina I(theta)=(2/3)ln E_LCDM(z_star;theta), beta_TGL=ALPHA_FINE_CODATA_2018*sqrt(e) em runtime, e h=log10(H_local). O desenho mantém o fator beta somente na resposta local desta comparação. Não é uma implementação de todos os setores cosmológicos da TGL e não pode herdar sem exame uma compressão validada para outro modelo.

Escreva o bloco da rede como y=X eta+a_h h+c_C delta_C+epsilon. Aqui X contém os nuisance compartilhados (distâncias/interceptos que restarem após escolher h), a_h é a coluna de h efetivamente derivada das equações e c_C é a resposta diferencial proposta nas linhas elementares Cefeida. Essa notação não autoriza criar respostas nas equações redundantes: todas devem ser transportadas pela mesma transformação B usada nas medidas, com suporte coerente.

| Hipótese | Resposta local h | Desvio diferencial | Bloco BAO |
|---|---|---|---|
| TGL fixa no mapa R-A | log10(H0_bg)+I beta_TGL/ln10 | zero | régua padrão do fundo especificado |
| Referência LCDM | log10(H0_bg) | zero | padrão |
| beta livre diagnóstico | log10(H0_bg)+I beta/ln10 | zero | padrão |
| Cefeidas diferencial | log10(H0_bg) | delta_C livre por c_C | padrão |
| H5 opção A, se escolhida | log10(H0_bg) | zero | rd livre em DM/rd,DH/rd,DV/rd; CMB rstar padrão |

A última linha é a alternativa fenomenológica A da nota H5, não uma escolha adotada nem um modelo EDE. B exige outro motor e qualificação CMB; C replica o espaço de respostas do beta livre nas condições explicitadas e não cria uma quinta assinatura. A previsão universal local é hipótese de correspondência da rota, a justificar para os indicadores admitidos antes da abertura.

## Medida, suporte e nuisance

Para covariância C fixa, rank r e suporte afim comum, a densidade gaussiana tem fator (2pi)^(-r/2) pdet(C)^(-1/2) e expoente −residual^T C+ residual/2, além da condição N^T residual=0. Não somar covariância já marginalizada e o mesmo nuisance com prior. Escalas de unidades, tolerâncias e transformação B ficam congeladas antes de rank/contraste.

Alternativa1: priors próprios comuns para eta e marginalização com normalizações; os limites físicos e sensibilidade das caudas precisam constar do contrato, sem escolher a partir de um melhor ajuste. Alternativa2: razão relativa com a mesma medida plana nuisance, apenas se seu fator arbitrário comum cancelar exatamente em todos os modelos e parâmetros comparados. Não chamá-la de evidência absoluta.

No caso restrito em que X está inteiramente no suporte comum de C, G=X^T C+ X é invertível, a condição do núcleo é satisfeita e o domínio eta é todo R^p com a mesma medida, a integral em eta multiplica a likelihood perfilada por (2pi)^(p/2)/sqrt(det G). Só nesse caso esse determinante cancela se X e C forem os mesmos e independentes de theta/modelo. Priors finitos acrescentam probabilidades de truncamento dependentes dos parâmetros. Se N^T X não for zero, há restrições determinísticas sobre eta e a fórmula acima não se aplica diretamente; deve-se parametrizar o subespaço admissível e sua medida. A implementação não poderá tratar a pseudoinversa como licença para ignorar isso.

A informação sobre delta_C após nuisance depende do projeto e covariância reais. A coluna candidata binária não transforma uma rede mista em uma única escada Cefeida, nem permite aplicar ±0,2delta_C a seu H0 agregado sem derivação. O coeficiente matricial ainda não foi computado. Um deslocamento universal é absorvido por h livre na rede isolada; o bloco de fundo fornece o vínculo que distingue as hipóteses.

## Priors candidatos e decisões restantes

O rascunho anterior propõe beta diagnóstico uniforme em[−0,05,0,05], s uniforme em[−0,15,0,15] e rd uniforme em[130,160]Mpc; nenhum desses priors é prior da beta_TGL. Preservar a proposta s via delta_C=−5log10(1+s) fixa uma densidade não uniforme em magnitude. Essa transformação parametriza um prior motivado pelo caso puro; não deve ser usada como lei de resposta de H0 para a rede mista. Escolher uniforme em delta_C ou q_d define outros priors e precisa aparecer como tal, com sensibilidades previstas antes do composto.

Faltam para congelar um V1 executável: escolha científica de H5 e fundo; fontes/seleção e resposta física final; covariância residual justificada ou família PSD pré-especificada; suporte/rank/normalização com unidades; priors nuisance completos; política de margens/caudas e custo; função única de veredito com seus diagnósticos. O dossiê de JAGB localizou as dependências concretas e a nova unidade documental busca quantificá-las. Não há exigência de provar independência de toda sistemática imaginável.

O contrato deve emitir separadamente separação esperada, resíduos observados e evidência relativa, sem somá-los como provas independentes. A ordem de vereditos vem da ORDEM018; o ramo sem poder conserva os diagnósticos residuais, sem os esconder. Nenhuma saída automática dirá CONFIRMED. A gerência recebe o V1 concreto para a decisão de abertura prevista no §6; isso não é permissão pendente para controles sintéticos ou reprodução histórica já autorizados.
