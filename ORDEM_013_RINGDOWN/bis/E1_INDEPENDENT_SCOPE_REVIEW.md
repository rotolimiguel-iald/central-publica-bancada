# E1 — revisão independente de escopo e preservação

[REAL — leitura de código, custódia documental e consistência de JSON; não refit científico]

**Sem bloqueante novo encontrado para publicar este produto como diagnóstico condicional NÃO-CEGO. Não é likelihood populacional hierárquica calibrada, Bayes factor ou teste físico.** Resultado examinado: `bis/e1_nuisance_v2/runs/authorized_001/NUISANCE_DIAGNOSTIC.json`. A execução de 41.58470s é do agente principal autorizado; não foi repetida aqui.

## Cobertura e preservação

Conferidos os 20 arquivos do manifesto por tamanho/SHA256, os vínculos do recibo com código, manifesto, autorização, resultado e orçamento, além da cronologia plano→autorização→execução. A AST dos métodos científicos é idêntica entre v1 e v2; apenas main mudou. A versão antiga, seu plano/manifesto e o registro de falha de dependência permanecem. O status UNEXECUTED do plano é histórico; o recibo posterior comprova a etapa executada.

O conjunto tem 33 eventos/608.681 linhas declaradas, com N, dataset e hash de cada produto iguais ao DATASET congelado. Esta revisão **não reabriu nem rehasheou HDF5**: conferiu a cadeia documental e o código que verifica esses arquivos antes/depois. A conferência científica GR/R-B independente conduzida pelo principal é distinta deste parecer.

Grade completa: nove referências calculáveis (GR marginal + oito leituras), 14 grupos, dois covariáveis; três bandas nas populações31/33 e banda nominal nos recortes. São **324 células =288 ajustes condicionais +36 NÃO PAGO**, estes exclusivamente nos dois recortes σ<0,15, com três eventos cada. Não são 36 falhas descartadas ou substituídas por zero. R-PROP e R-RAIZ-COHERENT são duas leituras físicas adicionais OPEN, fora dessa grade calculável; não confundí-las com as 36 células pequenas. As dez leituras estão conservadas.

Os 891 controles KDE registrados cobrem 33×9×3 sem duplicatas. As flags salvas respeitam limites de integral, erro direto, estacionariedade e distância de suporte. Maior erro de logdensidade no ótimo: 4.2102749e-05; distância de Newton máxima 0.002069712; margem mínima 7.2287185 h. Isso é conferência de resultados/limiares registrados, **não nova execução das somas KDE**, certificação de ótimo global ou cobertura estatística.

## Objeto efetivamente ajustado

O código preserva linhas conjuntas e calcula u=δτ−δ_L(Mf_det,chi_f,z) amostra por amostra. Não substitui os parâmetros por medianas nem corta δf. A marginalização sobre δf e parâmetros auxiliares mantém suas correlações na distribuição de u, mas **remove a restrição δf=0**. A referência GR aqui é δτ=0 com δf marginalizado/livre, diferente do ponto GR conjunto (δf,δτ)=(0,0) e do lnB da curva anterior. É indispensável conservar esse qualificador ao exportar tabelas; rótulo isolado “GR” seria ambíguo.

Conferidas 297 identidades a partir dos momentos publicados: E[u]=E[δτ]−E[δ_L] e Var(u)=Var(δτ)+Var(δ_L)−2Cov(δτ,δ_L). A matriz pareada é simétrica e sua entrada δτ coincide com σ². Isso apoia a preservação das correlações no produto, sem provar novamente a extração científica das amostras. R-GLOBAL e ramos abaixo da resolução podem ser idênticos numericamente ao controle marginal, sem virarem medições independentes nem efeito analítico literalmente nulo.

## Priors e constantes

O parser lê declarações Uniform via AST de literais; não executa texto de prior. Os recibos registram **29 priors δτ em [−0,8;2] e quatro em [−0,8;4]**. Reobtida Σlog W individual para cada um dos288 ajustes: não há substituição universal por largura2,8. A constante está registrada separadamente; `conditional_log_density` é soma de log p_u, e não evidência normalizada.

A identidade W p_u(c) só representa integral restrita proporcional à likelihood sob prior τ fatorizado constante, prior auxiliar comum/normalizado e suporte global compatível. A transformação u=τ−δ_L(η) não torna o prior de u uniforme. Declarações marginais e draws dentro dos limites não provam essas hipóteses. Código/plano mantêm **fatorização, suporte global e normalização restrita OPEN**. A interseção empírica [τmin−minδ,τmax−maxδ] e a margem3h são guardas conservadoras; não são prior exato nem correção de borda. Seu cumprimento não fecha essas lacunas.

## σ, covariância e interpretação

c(σ)=c0+kσ usa σ=DP posterior de δτ, ddof1, comum às leituras. A KDE usa a dispersão própria de u; o comparador gaussiano usa Var(u). São papéis diferentes, corretamente separados. σ é estimado do mesmo posterior: há endogeneidade, erro no covariável e possível efeito de prior/seleção. Não foram resolvidos por tratar σ como fixo. A variante c(ρ)=c∞+kρ·40/ρ é INPUT, não lei deduzida; sua SNR total GWOSC não substitui as duas SNRs da seleção pSEOB.

A Hessiana usa derivadas da soma gaussiana direta e a transformação de coordenadas devolve covariância local de(c0,k). Diagonais/EP, razões c0/EP e intervalos Wald salvos são coerentes aritmeticamente. Isso não calibra a distribuição amostral ou um posterior dos hiperparâmetros: ESS é desconhecida, banda varia, grupos se sobrepõem, não há lei de seleção/população normalizada nem validação de cobertura. Os z físicos, evidências e comparações calibradas continuam **null**. Diferenças entre escores de leituras com intercepto livre não são LR ou sigma; deslocamento quase constante é degenerado com c0.

O controle da gerência usa mediana/q90/1,6449 e covariância WLS absoluta, sem reescalaχ²; o KDE fullsample é outro estimador. Diferença entre seus erros não é ganho de precisão física demonstrado. Não reajustei nem repeti esse controle científico.

## Seleção, preservação operacional e conclusão de escopo

Eficiência α(Λ) segue UNKNOWN_NORMALIZATION. A norma escolhida de seleção, os vieses possíveis, a injeção LVK de ponto único e os dois estimadores C2/C5 estão no parecer lateral `bis/e1_selection/SELECTION_AND_CONTROLS.md`; não transformam o ajuste em inferência hierárquica calibrada. A expressão FULL_TEXT_READING_REQUIRED no JSON descreve pendência daquele script: o parecer lateral documenta passagens primárias efetivamente lidas, **não leitura integral dos PDFs**.

Guardas usam exceções explícitas, não assert. Caminhos resolvidos ficam na raiz autorizada, tag é restrita, destino preexistente é recusado; publicação por hard link de temporário completo não substitui saída existente. Falha deixa registro/temporário, sem apagar ciência antiga. Limite temporal é cooperativo. Uma thread foi solicitada por variáveis de ambiente, não medida; o recibo diz isso corretamente. Nenhum desses controles é autorização automática para nova execução.

**Aprovação limitada ao estatuto documental/condicional e à preservação conferida.** Curva de calibração pSEOB, eficiência de seleção, prior restrito global e significância/likelihood populacional calibrada continuam NÃO PAGOS/OPEN. Nenhuma produção alterada, nenhum gate movido, nenhuma leitura escolhida.

Controle: `bis/e1_selection/review_nuisance_scope.py`; recibo `NUISANCE_SCOPE_CONTROLS.json` (hashes completos). SHA256 do resultado examinado: `4fec657346f96153488b872190484e3c4bee3800111f16193d844ce20decae00`. Axiomas N/A; teoremas0.
