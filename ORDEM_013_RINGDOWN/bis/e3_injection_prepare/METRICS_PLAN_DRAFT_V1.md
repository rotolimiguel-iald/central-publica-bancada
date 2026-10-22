# E3 — plano candidato de métricas, antes da alocação

[INPUT — plano para revisão/alocação; nenhuma campanha calculada ou executada]

**Uma ou duas recuperações podem produzir medidas válidas de recuperação; não validam viés por repetição do ruído, cobertura ou sigma_sys. Com N=1 ou2, o gate de calibração permanece OPEN/vermelho.** Este plano acrescenta critérios ao desenho candidato, sem modificar E2, produtores, templates, campanhas encerradas ou resultados anteriores. Não constitui alocação.

## 1. Unidade experimental e estimador fixado

Uma célula é `(fonte de verdade, bin/alvo de SNR, família injetora, hipótese/convenção)`. As famílias são pSEOBNRv4HM_PA e IMRPhenomXPHM; a recuperação é pSEOBNRv4HM_PA em ambas. O vetor avaliado, sempre completo, é

`theta = (dtau220, dtau440, domega220, domega440)`.

Na convenção fracional correspondente, `domega = δω/ω = δf/f`; não converter isso em deslocamento absoluto em Hz. A verdade vem do recibo final da injeção, inclusive distância reescalada e convenção dos modos; não vem do posterior recuperado. Para GR, os quatro valores verdadeiros são zero. TGL a=1 só possui métricas de recuperação onde a verdade e o gerador forem implementáveis conforme o desenho preservado.

Proposta a congelar na alocação: estimador pontual primário = **mediana marginal do posterior** de cada coordenada. Para réplica r, família f, bin b e coordenada j:

`e[f,b,r,j] = mediana(theta_rec[j]) − theta_truth[f,b,r,j]`.

Não substituir mediana por média, MAP ou estimador mais favorável depois de ler resultados. Registrar também IC/intervalos credíveis equal-tailed de90% e95%, média e covariância posterior4×4, sempre dos mesmos índices/amostras pareadas e com a convenção de pesos explicitada. Esses últimos são descritores da distribuição posterior, não novas réplicas de ruído. Nenhuma aproximação gaussiana substitui silenciosamente posterior não gaussiano.

Uma réplica de ruído = uma janela independente planejada; os dois jobs de famílias que usam a mesma janela formam **um par**, não duas réplicas independentes. Fontes diferentes são estratos distintos até existir regra populacional prévia. PSD compartilhada e dependência entre janelas devem ficar explícitas: inferências podem ser apenas condicionais à PSD/época. Não multiplicar N por quatro coordenadas, duas famílias ou número de amostras do posterior.

## 2. c(SNR), resíduo e incerteza

Para cada família/bin/coordenada, publicar N_planejado, N_tentado, N_válido e a lista completa de resíduos. Estimar, com peso igual por réplica válida:

`c_hat[f,b,j] = soma_r e[f,b,r,j] / N_válido`.

Esse c estima o viés do **estimador mediana** no desenho condicionado a fonte, ruído, PSD, prior e família. Não é uma curva universal de eventos. Não ponderar réplicas pelo inverso da largura recuperada: isso faria o próprio resultado escolher seu peso.

Para N≥2, fornecer a covariância empírica4×4 dos vetores e, com divisor N−1, e o espalhamento por coordenada. Apenas sob hipótese explicitada de réplicas independentes e comparáveis, `Cov(c_hat)=S_e/N` e `SE(c_hat[j])=sqrt(S_e[j,j]/N)`. Com correlação entre janelas/PSD, essa expressão não é automaticamente válida; sem modelo ou desenho que a justifique, a incerteza calibrada de c fica OPEN.

IC candidato para N suficiente e hipótese de resíduos aproximadamente normais: Student t com N−1 graus de liberdade, `c_hat ± t_(1−alpha/2,N−1) SE`. Rotular **IC condicional ao modelo de repetições**; não chamar de exato para mediana posterior, ruído real ou pequenas amostras. A alocação deve definir, antes da execução, N mínimo para seu uso inferencial e a evidência de adequação/independência. Este plano não fixa um N que torne a normalidade verdadeira. Sem esses requisitos, apresentar apenas diagnóstico descritivo e OPEN.

A incerteza dentro do posterior de uma recuperação não é SE(c_hat), nem mede o erro entre repetições. Não substituir uma pela outra. Tampouco o intervalo credível de theta é IC frequentista do viés.

Publicar primeiro os pontos por bin. Ajuste c(SNR) contínuo exige forma funcional, pesos/covariância, tratamento de bins vazios e domínio de aplicação congelados antes da execução; sem isso, não ajustar/interpolar/extrapolar. O eixo da injeção é SNR **ótimo IMR de rede**, distinto do SNR de detecção GWOSC e de SNR_RD.

Se já existir correção c_ref fixada com fonte/hash independente, registrar o resíduo `r_c=c_hat−c_ref` e sua incerteza, incluindo Cov(c_hat,c_ref) quando compartilharem dados. Se c_ref não existir, `r_c` fica null e o viés e é o produto disponível. Não ajustar c nos mesmos jobs e declarar a cobertura corrigida deles como validação: isso requer avaliação separada/holdout predefinido.

## 3. Diferença pareada entre famílias e covariância

Somente pares com ambas as recuperações válidas entram no contraste pareado:

`d[r] = e[XPHM,r] − e[pSEOB,r]`, `Delta_hat = media_r d[r]`.

Guardar N_pares e IDs; jobs isolados continuam na tabela individual, sem completar pares por imputação. Para N_pares≥2, publicar S_A, S_B, covariância cruzada S_AB e S_d. A identidade de controle é `S_d = S_A + S_B − S_AB − S_AB^T`, calculada no **mesmo conjunto de pares**. Sob independência entre pares, `Cov(Delta_hat)=S_d/N_pares`; caso contrário, essa inferência permanece OPEN. Preservar as correlações entre os quatro desvios, sem exigir inversão de matriz singular.

Delta_hat mede contraste de famílias sob essa fonte, janela, banda e normalização. À mesma meta de SNR, as distâncias reescaladas das famílias podem diferir; não declarar simultaneamente mesma distância e mesmo SNR se o recibo não mostrar isso. Não converter automaticamente `|Delta|`, `|Delta|/2` ou `|Delta|/sqrt(2)` em sigma_sys conhecido. Duas famílias não são uma amostra representativa de todas as discrepâncias de modelagem.

## 4. Canal df e sistemática

Para domega220 **e** domega440, publicar separadamente: média dos resíduos, espalhamento entre repetições dentro de cada família/bin, covariâncias com dtau e contraste pareado. O termo comum de frequência é livre: não forçar média zero para transformar deslocamento em largura.

O espalhamento de recuperações contém ruído de medida, efeitos do prior/estimador, possível não estacionariedade e modelagem. Não é, sozinho, sigma_sys físico. Não usar `max(0, variância_dos_resíduos − média(variância_posterior))` como uma decomposição calibrada: a variância posterior não é automaticamente a variância de erro do estimador em repetições.

Uma inferência de sigma_sys precisa de modelo de separação de componentes, likelihood/normalizações, quantidade suficiente de repetições/fontes e validação independente registrados antes. Na ausência disso: `sigma_sys_calibrado = null`, estatuto OPEN; fornecer os descritores medidos e limites de alcance. O contraste de duas famílias é um diagnóstico adicional, não fecha essa lacuna. Estes jobs GR também não medem transferência de desenrolamento browniano à pipeline nem calibram a cauda física5σ.

## 5. Cobertura e falhas

Para cada família/bin/coordenada e nível nominal q∈{0,90;0,95}, contar `k = número de intervalos credíveis que incluem a verdade` entre n recuperações válidas. Convenção: inclusão dos endpoints. Publicar k/n e IC binomial Clopper–Pearson central95%:

- limite inferior:0 se k=0; caso contrário, quantil Beta(alpha/2;k,n−k+1);
- limite superior:1 se k=n; caso contrário, quantil Beta(1−alpha/2;k+1,n−k);
- aqui alpha=0,05. Para n=0, estimativa e IC são null.

A interpretação binomial exige tentativas independentes com cobertura comparável dentro da célula; com dependência, rotular o IC como condicional/não validado. Esses IC são pontuais, não simultâneos entre bins, famílias, quatro coordenadas e dois níveis. Não multiplicar coberturas marginais para fabricar cobertura conjunta4D. Qualquer decisão simultânea exige correção/plano próprio previamente fixado, sem escolher a coordenada favorável.

Mostrar também `k/N_tentado` como **taxa operacional de tentativa com recuperação válida e cobertura**, contando falhas como insucessos operacionais; isso não se chama cobertura estatística do posterior. Publicar taxa de falha e razões: dados/DQ, PSD, janela, geração, suporte/distância, orçamento, maxcall, ESS, convergência e revisão. N_planejado não tentado por orçamento é categoria separada, não uma falha de PE executada. Jobs rejeitados pelos critérios congelados não entram como posteriores válidos; não os apagar nem refazer até passar. Pares incompletos e dados ausentes podem causar seleção; a cobertura condicional aos válidos não demonstra cobertura de todas as tentativas.

## 6. Regras explícitas para N pequeno

| Situação | Produto permitido | Produto não estabelecido / gate |
|---|---|---|
| N=0 | Estado e motivo; contagens0; métricas null. | Nenhuma recuperação/calibração. OPEN/vermelho. |
| N=1 por célula | Estimador recuperado, resíduo individual e incerteza **posterior**; indicadores de cobertura0/1. | Sem variância de repetição, SE de c ou IC de viés empiricamente validado. Não usar zero como substituto. OPEN/vermelho. |
| Dois jobs totais, um por família | Um contraste pareado4D e dois resultados individuais, se ambos válidos. | N_pares=1; nenhuma covariância empírica entre pares ou sigma_sys conhecido. OPEN/vermelho. |
| N=2 por célula/par | Média e covariância amostral descritivas quando definidas; cobertura k/2 com IC amplo e suas hipóteses. | Covariância4×4 tem posto≤1; sem inversão/certeza multivariada. SE/t calculáveis sob hipótese não validam viés de ruído. OPEN/vermelho mesmo se os dois resíduos coincidirem. |

Zero diferença entre duas recuperações não prova ausência de viés. Dois casos cobertos não demonstram cobertura nominal90/95%. Nenhum número de amostras internas do sampler altera essas contagens de repetições.

## 7. Pisos por leitura, precisão e parada

Quando houver predição aplicável, obter delta_j da **fonte de predição pinada** e registrar hash, leitura, modo, verdade física/remanescente, clock, redshift, QNM, observável e convenção. Não computar nada nesta preparação. O nome “kernel prediction” não transfere estatuto de prova formal a uma injeção física. Beta continua calculado em runtime como `ALPHA_FINE_CODATA_2018 × sqrt(e)`.

Para |delta_j| finito e resolvido: `piso_primario=|delta_j|/5`; `piso_sensibilidade=|delta_j|/15`. Mostrar por leitura/bin/família:

- `|c_hat|/piso` e, se definido, `|r_c|/piso`: tamanho do viés/resíduo, não incerteza;
- `sigma_c_calibrado/piso`: somente se a incerteza de calibração estiver estabelecida; nunca substituir por largura posterior;
- `H_IC(c)/piso`: meia-largura do IC, com nível/hipóteses explícitos, distinta de sigma;
- `|Delta_hat|/piso` e incerteza do contraste: diagnóstico de sensibilidade entre famílias, não sigma_sys.

Predição zero, sub-resolução, não exponencial, não implementada ou sem modo/mapeamento válido: razões null com motivo, nunca divisão por zero ou N astronômico apresentado como resultado implementável. No ensemble, delta_f=0: **não** criar piso positivo de frequência a partir de |delta_f|/5. A rota IV exige desenho próprio de sigma_sys e transferência, com os alvos registrados pertinentes; até então OPEN. dtau440 só recebe piso de uma hipótese440 declarada, não herdado automaticamente do220.

A alocação deve fixar N_planejado/N_máximo por célula, mínimo de pares/repetições para inferência, conjunto de leituras/modos avaliáveis, precisão-alvo, método de IC e critérios simultâneos. Proposta simples: **decisão de precisão apenas no endpoint N registrado**; verificações intermediárias servem a custo, integridade e segurança, sem parar ao primeiro IC favorável. Se quiser parada sequencial por precisão, registrar antes método com validade sequencial e contabilização de todas as inspeções; IC de tamanho fixo não fornece isso por si só.

No endpoint, reportar precisão alcançada e lacunas. Uma meta de meia-largura de IC pode ser escolhida para planejamento, mas não muda o gate E2, que exige a condição estrita de sigma(c_calibrado)<|delta|/5 e os demais requisitos. `/15` segue somente sensibilidade. Nenhuma passagem verde é automática por SE pequeno, N grande ou contraste de família pequeno. N=1/2, incerteza não validada, seleção de válidos não controlada ou modelo sistemático não pago mantêm OPEN/vermelho.

Parada por orçamento/deadline, impossibilidade técnica ou gate vermelho sem rota prevista preserva todas as tentativas e produz `PRECISION_NOT_ESTABLISHED`/`INCONCLUSIVE_SYSTEMATICS`, com motivo. Não estender N, trocar fonte/bin/prior/família ou ressuscitar campanha encerrada para obter aprovação. O orçamento total continua o da ordem; este plano não o aloca nem renova.

## 8. Entrega mínima futura e decisões que faltam

Uma tabela por tentativa deve ligar configuração/verdade/ruído/PSD/resultado por hashes e registrar família, bin, fonte, réplica/par, estado, custo e exclusão justificada de métricas. Uma tabela por célula conserva os quatro desvios, viés e sua incerteza separada, cobertura/IC, falhas, dependências e estatutos. Uma tabela por leitura expõe predição/pisos/razões ou null motivado; a matriz de gates mantém as lacunas visíveis.

Antes da execução, completar: N e orçamento; definição de independência/pareamento; N mínimo e modelo inferencial; precision target e multiplicidade; eventual c_ref independente; regras de correção/holdout; modelo e critérios de sigma_sys; origens das predições aplicáveis. Não fabricar esses pagamentos a partir de um ou dois jobs.

Uma recuperação aceita pode ser reportada `[REAL — recuperação medida no desenho]`, enquanto a calibração permanece `[OPEN]`. O estado máximo não se promove a significância física. **NOT_FALSIFIED nunca CONFIRMED.** Nenhum waveform, draw, PE, strain ou posterior foi calculado/lido para redigir este plano.
