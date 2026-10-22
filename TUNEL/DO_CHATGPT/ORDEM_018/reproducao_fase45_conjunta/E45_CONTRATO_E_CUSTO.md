# E45 — contrato histórico e piloto de custo

[REAL] Piloto completo; nenhuma grade observacional iniciada. Dentro de F1(b), foram preparados código e contrato de evidências relativas históricas P/F4 e P/F5. Nenhum ajuste T4, P45 ou SN-only foi repetido. O operador/coordenação deve receber este custo antes de qualquer lote.

Protocolo congelado em 2026-10-06T01:47:21.202040+00:00, mapa pré-execução seq415 confirmado. SHA-256 do protocolo: 35bd6815dc9c8e7b8768136a6d33a740bc08abe6a47c49f4c06612893457df8c; código: 31042ef8b8d37eb5f310c7307d4c0056c53997cb3db10f6022af43a8eccef479.

## Medida de custo

Foram feitas 369 avaliações nos mesmos theta já usados na reprodução P45, sem pontos observacionais novos. Houve cinco rodadas de oito ciclos dos três modelos por configuração, mais verificações iniciais. Custo: 2.5633s wall, 2.4062s CPU, pico 165.172MiB, uma thread. Diferenças dos valores repetidos ficaram abaixo de1e-10 em chi2.

| Configuração | ms/avaliação | Minutos para grades25+35 | Margem 2x máxima taxa medida (min) |
|---|---:|---:|---:|
| P4_d1b | 0.1623 | 5.43 | 11.32 |
| P5_sombra | 4.6449 | 155.47 | 317.73 |
| P5_acumulada | 5.2767 | 171.47 | 345.95 |

Total projetado: 5966250 nós e 5.540 horas. Extrapolação linear CPU, não duração medida; sem descontar recusas de suporte. LCDM P5 é comum às leituras e conta uma vez por n. Os tempos GPU antigos não são transferíveis para este processo.

## Contrato preservado

As funções históricas _grade, _lnL_grade, evidencia, comparar_evidencias, _ajuste e máscaras foram lidas; E45_FONTES_HISTORICAS.json guarda funções/linhas/hashes. Nenhum original foi importado/executado. Matrizes, likelihoods e M são os mesmos de P45: SH0ES escalar somente P4; Pantheon+SH0ES completo P5; CC ausente; covariâncias cruzadas entre blocos ausentes, fatoração histórica INPUT.

Modelos LCDM beta=0, TGL beta=ALPHA_FINE_CODATA_2018*sqrt(e) em runtime, livre beta uniforme em(−0,05,0,05); c=0. Priors: H0(50,90), omega_b(0,015,0,030), omega_c(0,08,0,18). O volume do modelo livre inclui largura beta0,1; modelos fixos usam delta normalizado, sem essa largura.

Centros/sigmas são reutilizados do recibo P45 verificado. A rotina original refazia ajuste a cada n a partir do ponto padrão; o JSON resumido não conserva todos esses centros/sigmas. Trata-se de reconstrução independente da grade, sem alegação de identidade byte a byte. Não repetir fits para preencher essa lacuna.

Grade inclusive linspace n25/n35, fundo entre max(limite,theta−6sigma) e min(limite,theta+6sigma); beta livre cobre todo prior. Fallback histórico de sigma ausente/zero é0,05largura; os sigmas atuais estão presentes. LogZ=logsumexp(−chi2/2)+sum(logDelta)−logVprior. Pesos constantes em endpoints, não trapézio. Motor histórico rejeita endpoints estritos do prior (inclusive beta), embora constem no linspace. CAMB aceita posições1≤pos≤n_eixo−2, sem extrapolar.

Likelihood zero fora do suporte, contagem de recusas preservada. Não renormalizar pelo suporte CAMB menor nem pela caixa de integração. Alvo publicado logZ25; refinado logZ35 e diferença aparecem ao lado. Marginal beta usa soma*dBeta, interpolação linear para Savage–Dickey e CDF de nós para quantis; reproduzir e identificar essas discretizações.

## Validade e normalização

[DERIVED] A integral (1/Vprior)∫exp(−chi2/2)dtheta define alvo finito para a likelihood indicada. A rotina retangular o aproxima apenas dentro da caixa de fundo dependente do ajuste. Comparar n25/n35 não controla caudas omitidas por ±6sigma nem o efeito da máscara computacional. Isso não certifica a evidência no prior completo.

LogZ histórico omite normalizações gaussianas dos dados. Elas cancelam nas razões da mesma família com mesma covariância, mas não justificam comparação absoluta entre conjuntos diferentes. Em P5, A=1ᵀC⁻¹1 e chi2(theta,M)=chi2_prof(theta)+A(M−Mhat)^2. Integrar uma medida plana comum de M multiplica exp(−chi2_prof/2) por sqrt(2pi/A), constante entre modelos/leituras. Esse fator comum cancela. Um prior impróprio não define evidência absoluta; o fator relativo pode ser interpretado com medida nuisance comum compatível ou limite de priors próprios iguais e amplos. Prior M finito introduz fatores erf dependentes de theta. Nenhum prior finito novo foi inventado aqui.

Alternativas: A reproduzir o fator relativo histórico explicitando cancelamentos, domínio e limites; B em etapa distinta definir M próprio e controle de caudas para evidência absoluta. B muda contrato e não entra silenciosamente. MEDIDA atual: leitura e álgebra; nenhuma integral observacional nova.

## Laplace e resolução

Laplace diagonal histórico: logLhat+d/2log(2pi)+sum(logsigma_j)−logVprior. Usa produto das variâncias marginais, não detSigma. Para Sigma positiva definida, diferença para Laplace completo é0,5log(prodSigma_jj/detSigma)≥0, mas diferenças entre modelos podem ter qualquer sinal. É diagnóstico grosseiro, não substituição da grade.

Tolerâncias congeladas para reprodução futura: ΔlogZ≤0,01; ΔlogB≤0,02; SD versus arquivo≤0,01; erro máximo arquivado versus reproduzido≤0,001. Diferença35−25 acima0,01 sinaliza não resolvido, sem extensão automática. A diferença entre duas grades não é limite rigoroso de erro; SD não será forçado a igualar Bayes direto.

O controle sintético usa gaussiana de média0,01, sigma0,0022, prior(−0,05,0,05); integral exata por erf. Não integra dados observacionais. Avaliação pontual em beta_TGL runtime.

| n | Erro logZ | Erro log densidade interpolada | Erro mediana CDF nós |
|---|---:|---:|---:|
| 25 | -0.00661472 | -0.16539413 | -0.00234910 |
| 35 | -0.00002586 | +0.02341367 | -0.00154520 |

Para L=1 constante, soma retangular inclusiva tem excesso1/(n−1); ao excluir os dois endpoints estritos, falta1/(n−1). Pequeno erro de logZ não certifica densidade pontual ou CDF. Alternativas: A preservar discretizações históricas como alvos; B melhoria numérica separada com outro protocolo. MEDIDA acima mostra o alcance do erro25/35, sem inferir novos valores científicos.

## Recursos e opções de aceleração

Runner preparado: streaming, uma thread,600s e512MiB por unidade; resultado parcial de falha não recebe logZ concluído e não é sobrescrito. Modo grade ainda não exercitado. Não lançar o lote P5 escalar de horas.

Alternativa A exata: P4 usa beta só em [H0exp(beta I*)−H_SH]^2/sigma_SH^2, permitindo vetor beta para cada fundo. Em P5 sombra r(beta)=r0+(5/ln10)beta I*q, q=1 nas não-calibradoras e0 nas calibradoras. Após whitening e projeção de M, chi2 é quadrática exata em beta. Calcular coeficientes uma vez por fundo preserva nós e pesos da grade. Requer validação contra escalares antes de usar.

Alternativa B: lotes pequenos de quadratura e soluções triangulares com múltiplos lados direitos, incluindo ramo acumulado cuja dependência não é quadrática em geral. MEDIDA futura: benchmark e erro versus escalar antes de nova integral. Ganhos não presumidos.

O arquivo E45_CUSTO_E_COMANDOS.json descreve16 unidades únicas e custos, não autorização de lote. Primeira unidade escalar pequena proposta para depois da decisão da coordenação:

~~~powershell
& 'C:\Python314\python.exe' -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\reproducao_fase45_conjunta\E45_piloto_e_grade.py' grid P4_d1b tgl 25 --max-seconds 600
~~~

Esta unidade tem15625 nós; não foi executada. O benchmark já concluído usou o argumento benchmark, sem grid. MCMC/F9 e vereditos novos permanecem fora. Uma ordem posterior da coordenação autorizou preparar e validar a alternativa algébrica exata antes de lote; essa continuação receberá protocolo próprio ao lado.
