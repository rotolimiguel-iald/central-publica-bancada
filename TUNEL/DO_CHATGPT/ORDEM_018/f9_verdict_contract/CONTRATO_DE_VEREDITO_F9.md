# F9 — contrato concreto de veredito, candidato para decisão

Unidade **18dced03-6d38-4a2e-a2c8-a44ab39ed171**, 06/10/2026. [INPUT] pedido delimitado da coordenação; [DERIVED] definições e regras condicionais de teste; [REAL] custódia documental e leitura dos resultados error-only existentes; [OPEN] ratificação e calibração. **Não é V1 adotado nem autorização de abertura.** Zero fit, centro composto, vetor y, S/g, H0, evidência, simulação científica, CAMB, um.py, upstream, rede ou provedor executado.

**Recomendação:** adotar como candidato a alternativa A abaixo: cinco perguntas frequentistas explicitamente calibradas, acompanhadas das razões bayesianas relativas como outra leitura. Remover os símbolos indefinidos z_TGL/z_LCDM e o retorno antecipado “underpowered”. Até a calibração existir, a saída diz **CALIBRATION_UNAVAILABLE**, sem fabricar sigma. A regra admite residuais extremos mesmo num desenho previamente considerado pouco potente.

## 1. Objeto da decisão e dados comuns

A decisão diz respeito à **rota observável R-A da TGL, aos cinco modelos aqui especificados e ao contrato de dados/erros admitido**. Uma rejeição dessa rota não é rejeição automática de toda a teoria; uma preferência por ela não é confirmação ontológica ou mudança do gate.

Use uma única montagem: fundo padrão plano proposto, Planck comprimido + DESI DR2, e rede local V01 aumentada para JAGB. Mesmas observações, seleção, unidades, suporte e transformações nos cinco modelos. Não adicionar os H0 agregados dos mesmos dados, repetir SNe/âncoras, multiplicar diagnósticos históricos ou tratar Planck-only e Planck+BAO como experimentos independentes.

A proposta corrente mantém **267 linhas locais e 63 nuisance η**. O preflight262 é controle parcial por erros, excluindo cinco megamasers por falta de erro relativo autorizado; não substitui silenciosamente o conjunto267. Fatoração entre blocos, compressões com q0/j0 fixos, universalidade do mapa local e partição dos erros são hipóteses explícitas, não resultados dos postos matriciais.

No bloco local:

\[
 y=X\eta+a_hh_i(\xi_i)+c_C\delta_i+\varepsilon.
\]

O contraste/fluxo cosmológico integra-se ao bloco de fundo na **mesma** função de amostragem. Defina θ=(H0,wb,wc), h_bg=log10[H0/(km s⁻¹ Mpc⁻¹)], I(θ)=(2/3)ln E_padrão(1089,95;θ). A escolha z★_lei fixo é INPUT, distinta de zstar de recombinação.

| Modelo | Resposta local | Cefeidas | BAO e CMB |
|---|---|---|---|
| H1 TGL fixa | h_bg+I β_TGL/ln10 | δ=0 | escalas padrão |
| H2 ΛCDM | h_bg | δ=0 | padrão |
| H3 β livre, diagnóstico | h_bg+I β/ln10 | δ=0 | padrão |
| H4 diferencial Cefeida | h_bg | c_C δ nas linhas elementares | padrão |
| H5 régua BAO livre | h_bg | δ=0 | BAO usa rd livre; CMB conserva rstar padrão |

β_TGL=α_CODATA2018√e em runtime; não é parâmetro ajustado. H3 contém H1 e H2 quando o intervalo declarado os inclui. **Logo não se pode rejeitar toda H3 em favor de H1:** a preferência pela restrição fixa pode aparecer no fator de Bayes, enquanto o contraste H1 versus H3 testa se a restrição fixa é incompatível. H5 aqui é fenomenológico, não EDE.

## 2. Likelihood, perfil frequentista e integral plana não são o mesmo objeto

Para cada variante sistemática s, a função de amostragem gaussiana completa, com covariância fixa C_s e suporte afim comum, é

\[
 \ell_{i,s}(Y;\xi_i,\eta)
 =-\frac{r_s}{2}\ln(2\pi)-\frac12\ln\operatorname{pdet}C_s
 -\frac12 R_i^T C_s^+R_i,
 \quad N_s^T R_i=0.
\]

Y representa simbolicamente todos os blocos; nenhuma realização foi aberta nesta unidade. O mesmo jacobiano de dados acompanha qualquer transformação. O loglikelihood dos blocos não gaussianos, se admitidos, precisa ser definido antes de substituir esta fórmula.

**Perfil:** \(\widehat\ell_{i,s}=\sup_{\xi_i,\eta}\ell_{i,s}\), sobre os domínios físicos congelados e η∈R^63. Não se multiplicam priors para produzir esse perfil. Limites físicos coincidentes com a caixa bayesiana são uma escolha explícita do domínio de calibração, não garantia sobre parâmetros fora dela.

**Integral plana relativa:** usa a fórmula já qualificada, com F_s=XᵀC_s⁺X, P_s=C_s⁺−C_s⁺XF_s⁻¹XᵀC_s⁺:

\[
 L_{\mathrm{flat},s}\propto
 (2\pi)^{-(r_s-63)/2}
 [\operatorname{pdet} C_s\det F_s]^{-1/2}
 \exp(-b^TP_sb/2).
\]

A constante arbitrária κ da medida κdη cancela somente sob as condições comuns já documentadas. Isso **não cria um prior amostrável uniforme em R^63**. Perfil não contém o fator det(F_s)^−1/2 da integração. Se C, X ou o domínio dependerem de parâmetros, preservar os determinantes/jacobianos correspondentes; não trocar os dois objetivos por nome.

O guard existente verifica dados, suporte, posto e finitude. Violação comum dos vínculos determinísticos por arredondamento/transformação é falha do modelo de dados a resolver, não evidência específica contra H1. Não reparar por jitter ou ocultar o resíduo no núcleo. Erro numérico ou tabela ausente dentro do prior não é likelihood zero. Se variâncias forem calculadas de centros estimados, o protocolo de calibração precisa ou condicionar explicitamente nos erros reportados como INPUT, ou reproduzir a estimação/transformação a partir de um modelo primitivo; congelá-las após olhar o resultado sem declarar isso não constitui calibração exata.

## 3. Cinco perguntas primárias com estatísticas definidas

Esta família contém **m=5 testes**, numa única rota conjunta R-A. O bloco de compatibilidade é subdividido para não confundir uma falha geral de ajuste com a lei fixa de β.

| ID | Estatística exata definida | Hipótese nula e interpretação |
|---|---|---|
| COMPAT_H1 | G_1,s = inf_(ξ1,η) R_1ᵀ C_s⁺ R_1 | H1: inadequação absoluta do ajuste completo |
| LAW_H1_VS_FREE | Q_1,s = 2(ℓ̂_3,s−ℓ̂_1,s) | H1: perda ao impor β fixo frente a β livre |
| H2_TO_H1 | T_21,s = 2(ℓ̂_1,s−ℓ̂_2,s) | H2: dados favorecem H1 contra ΛCDM |
| H4_TO_H1 | T_41,s = 2(ℓ̂_1,s−ℓ̂_4,s) | H4: favorecem H1 contra viés diferencial Cefeida |
| H5_TO_H1 | T_51,s = 2(ℓ̂_1,s−ℓ̂_5,s) | H5: favorecem H1 contra régua BAO livre |

As caudas são superiores. G é a deviance contra a média saturada no caso gaussiano de C fixo. Q≥0 apenas se os ajustes aninhados convergirem corretamente e compartilharem exatamente o modelo/dados. T pode ser negativo; preferência por H1 requer T>0, além do teste calibrado. Não recortar T em zero para fabricar uma lei χ².

Reter os cinco perfis, os residuais por bloco, todos os cenários e, como diagnósticos, as demais diferenças de perfil. Os dez pares possíveis são dependentes. Não atribuir sigma inferencial a pares adicionais depois de escolher os mais favoráveis: ampliar a família primeiro ou mantê-los descritivos. Para G não usar automaticamente χ²_(n−p); para Q não presumir Wilks; para T não usar √Δχ² como sigma. Linearidade parcial e grandes postos não provam as distribuições de cauda do problema não linear composto.

## 4. Calibração e significado de 5σ

Para cada teste j e cenário s, a quantidade exigida é

\[
 p_{j,s}=\sup_{\xi\in\Theta_{H_j},\,\eta\in\mathbb R^{63}}
 \Pr_{H_j,\xi,s}\{T_j(Y^*)\ge T_j(Y_{obs})\}.
\]

Para COMPAT e LAW, H_j é H1; nos três contrastes dirigidos é respectivamente H2, H4 e H5. A probabilidade usa a **mesma rotina completa**: transformação de dados, suporte, otimização, seleção previamente autorizada e estatística. Um bootstrap no melhor ajuste, sem controle do supremo sobre o nulo composto, é calibração pontual aproximada; deve ser nomeado assim. Uma grade finita de parâmetros não garante o supremo contínuo sem limite de interpolação/cobertura ou argumento adicional.

Há uma redução possível a provar sem gerar dados: quando a rotina inteira é invariante a Y_local→Y_local+Xv, o supremo em η desaparece. De fato, substituir η por η+v preserva a coleção de resíduos de cada perfil e a média saturada; logo G/Q/T não mudam. Isto requer X comum fixo, domínio η todo R^63, suporte preservado e nenhuma seleção dependente do deslocamento. Só então η=0 é representante para calibração; não é amostra de um prior impróprio. Se uma etapa viola a invariância, η continua no problema.

A normalização dos parâmetros físicos proposta é comum: H0[50,90], wb[.015,.03], wc[.08,.18] com densidade 50/3; H3 tem β uniforme[−.05,.05], densidade10. H4 preserva s uniforme[−.15,.15], transformado para δ=−5log10(1+s), densidade (ln10/1.5)10^(−δ/5), sem aplicar o fator de escada pura ao H0 misto. H5 tem rd uniforme[130,160] Mpc, densidade1/30; em q=rd/rd_CAMB o suporte e a densidade são condicionais a θ. Priors entram na integração bayesiana; o supremo frequentista percorre o domínio, sem ponderação por eles.

**Convenção proposta:** α5=1−Φ(5)=erfc(5/√2)/2. Sigma equivalente é \(Z_{eq}=\Phi^{-1}(1-p_{FWER})\), somente uma maneira de nomear a probabilidade de cauda global calibrada. Não afirma que um resíduo seja gaussiano. A cauda bilateral de |z|≥5 é 2α5 e não deve ser confundida com esta convenção unilateral equivalente. Não emitimos Z positivo significativo se p≥1/2; sempre exibir p junto da convenção.

No nulo simples, réplicas independentes e intercambiáveis da rotina integral permitem p_MC=(b+1)/(N+1), b sendo o número de estatísticas pelo menos tão extremas. Empates são conservadores; p=0 não é permitido. Para apenas resolver o limiar α5/5 seriam necessários N≥ceil(5/α5)−1 sob esse esquema, mesmo com zero excedências. Isso é limitação aritmética da resolução, **não ordem para lançar esse lote** nem garantia de calibração composta.

Uma avaliação analítica demonstrada ou método de eventos raros pode reduzir o custo. Exige demonstração/controles dos pesos e limites de erro, não extrapolação gaussiana da cauda central. Se limites de confiança Monte Carlo forem usados como certificado de cauda, sua probabilidade de falha entra no orçamento global de erro; um certificado de 99% não se torna sozinho evidência frequentista de 5σ. Erros de integração, otimização e qualificação do supremo devem ser propagados conservadoramente. Sem isso, **CALIBRATION_UNAVAILABLE** ou calibração condicional delimitada, sem o rótulo global pedido.

## 5. Variantes sistemáticas e multiplicidade sem escolher o cenário favorável

Proposta finita revisável: todas as 300 etiquetas da família estelar interior já preparada, cruzadas com as duas receitas SBF do preflight (erro m110; acréscimo independente e(M110), esta última estritamente condicional). São **600 etiquetas candidatas**, não 600 matrizes completas já qualificadas. O número283 de desenhos primitivos estelares distintos não autoriza afirmar quantas covariâncias completas são distintas. Deduplicar apenas por identidade da covariância completa, mapa de média e normalização, preservando etiquetas/proveniência.

A família exclui fronteiras singulares, correlações gerais MAS–HMS entre níveis e dependências físicas ainda não modeladas. Ela não é uma distribuição estatística medida das sistemáticas. Não selecionar melhor cenário depois de ver os centros, nem fazer média ou marginalização sem pesos próprios congelados.

Regra recomendada para uma afirmação robusta dentro dessa família:

\[
 p_j^{rob}=\max_{s\in\mathcal S}p_{j,s},\qquad
 p_j^{FWER}=\min(1,5p_j^{rob}).
\]

[DERIVED] Se o cenário verdadeiro admitido é s₀, p_rob≥p_s₀. Portanto a rejeição por p_rob≤a está contida na rejeição por p_s₀≤a e sua probabilidade é ≤a quando p_s₀ é válido. A união das cinco possibilidades de falso alarme tem probabilidade ≤5a pela soma das probabilidades, sem hipótese de independência. Assim, máximo entre sistemáticas seguido de Bonferroni entre cinco testes controla essa família, **sob suas hipóteses**. Não multiplicar novamente por600 quando a afirmação exige passar em todos os cenários: essa interseção é conservadora. Em contraste, selecionar o menor p entre cenários exigiria calibrar a busca ou ajustar sua multiplicidade.

A palavra “global” fica restrita a **estes cinco testes da rota R-A e à família sistemática declarada**. Se D9/D10, Planck-only, outros fundos, cortes, fórmulas ou rotas entrarem na escolha de um vencedor, seus ensaios precisam constar do livro de seleção e da calibração conjunta, ou de um ajuste conservador finito previamente definido. Fontes compartilhadas nunca geram independência por terem nomes diferentes. A história exploratória já conhecida é declarada; congelar este contrato não apaga consultas anteriores. Isso não desqualifica retrodição sem ajuste, mas delimita o alcance de um p global.

**Completude sistemática é campo próprio.** Uma família limitada pode sustentar resultado condicional rigoroso dentro dela; não recebe selo de cobertura de toda física instrumental. Se a conclusão varia com s, relatar SYSTEMATICS_SENSITIVE_RESULT e todos os extremos. Se uma dependência necessária impede definir sequer a distribuição de amostragem, ainda não há p válido, mesmo que um resíduo bruto seja grande. Esse resíduo continua exposto com unidade, cenário e limitação.

## 6. Cinco integrais relativas e fatores de Bayes

Para cada modelo i e cenário s, definir

\[
 J_{i,s}=\int L_{bg,i}(d_{bg}|\xi_i)
 L_{local,flat,s}(y|h_i,\delta_i)
 \pi_i(\xi_i)\,d\xi_i,
 \qquad \ln B_{ij,s}=\ln J_{i,s}-\ln J_{j,s}.
\]

Requer integrais finitas/não nulas, suporte/medida η comuns, priors físicos normalizados, todos os jacobianos e cobertura do prior inteiro. A constante κ comum cancela nas razões; os J isolados não são evidências absolutas normalizadas. Usar o código de integração plana já qualificado; nenhuma nova camada de física é requerida por este documento.

Entregar cinco log-integrais até constante comum e dez diferenças coerentes, erros numéricos e intervalos sobre s. Não somar lnB de estudos sobrepostos, multiplicá-los como evidências independentes ou converter lnB em sigma. lnB pode favorecer H1 contra H3 mesmo que um teste de compatibilidade não rejeite H1; são perguntas distintas. Se todos os modelos forem ruins, o “menos ruim” pode ter lnB elevado: G1 é indispensável.

Os cortes antigos lnB12≥5 e lnB13≥−1 podem permanecer como **sinalizadores bayesianos separados**, propostos para todos os cenários via mínimo. Não definem 5σ e não devem ocultar uma rejeição calibrada. Se erro numérico permite atravessar o corte, sinalizador indeterminado. Nenhum limiar de evidência é adotado por esta entrega.

## 7. Informação/poder, aproveitando o preflight sem centros

O recibo262 já mediu, nas duas receitas SBF baseline, posto C=190, nulidade72 e posto whitened X=63. As incertezas conjuntas ideais de h são 0.00639243108635 e 0.00641018106161 dex; de δ_C, 0.0277838016608 e 0.0278127974879 mag. São leituras do recibo custodiado, não novo cálculo nesta unidade. Usam h e δ_C livres simultaneamente e não incluem os cinco MM; não valem como erro de β, erro de H0 ajustado ou poder do experimento completo.

Para alternativas **simples previamente fixadas**, ruído gaussiano conhecido e contraste linear adequado, a separação ideal pode ser escrita D²=ΔμᵀPΔμ após nuisance. O teste ótimo unidirecional tem poder

\[
 1-\Phi\bigl(\Phi^{-1}(1-\alpha)-D\bigr).
\]

Isso é fórmula condicional, não cálculo do poder da F9 não linear. No caso simples, D=5 e limiar não corrigido5σ dão poder50%, não detecção garantida. Multiplicidade altera o limiar. Desenho/rank e erros, sozinhos, não fornecem Δμ completo nem o poder marginal sobre todos os rivais. Não calculamos um vetor de separação nesta unidade.

**Consequência para a função de veredito:** underpowered não é veto de análise nem critério de veracidade. Um resultado raro pode ser extremo num teste de baixo poder esperado; calcular/exibir o resíduo e sua cauda quando válidos precede a anotação de poder. Ausência de rejeição num teste pouco potente permanece pouco informativa.

## 8. Saída e ordem de decisão

A saída é estruturada, não uma única cadeia de `if` que apaga diagnósticos:

1. **availability/integrity/support:** entradas, autorização de abertura, hashes, suporte e normalização. Ausência vira AWAITING_DATA_OR_RATIFICATION; campos observados permanecem null. Falha instrumental/computacional é nomeada, não rejeição física.
2. **per_scenario_residuals/calibration:** conservar G,Q,T, resíduos por bloco e falhas, se calculáveis legitimamente. Sem cauda calibrada, não rotular sigma. No estado atual todos estes campos permanecem null.
3. **compatibility:** se COMPAT_H1 ou LAW rejeitar robustamente após ajuste familiar, ROUTE_H1_REJECTED_AT_5SIGMA_CONDITIONAL_CONTRACT. Vale mesmo com baixo poder prévio. Explicar se a inadequação é global ou especificamente da lei fixa.
4. **comparisons:** quando cada contraste dirigido for positivo em todos os cenários e seu p_FWER cruzar α5, informar H1_DISCRIMINATES_FROM_Hj_AT_CALIBRATED_LEVEL_CONDITIONAL_CONTRACT, separadamente para j=2,4,5, desde que H1 não seja rejeitado nos controles primários. “Não rejeitado” não significa validado; isso acompanha a frase.
5. **relative_evidence/use_novelty:** lnB e proveniência separados, com dependências e limites. Significância não é inferida deles. Não rejeitar H3 em favor do submodelo H1.
6. **systematics_coverage:** campo sempre visível. Variação de conclusão em cenários gera SYSTEMATICS_SENSITIVE_RESULT. Cobertura incompleta recebe SYSTEMATICS_COVERAGE_LIMITED, inclusive quando a significância condicional for extrema.
7. **information_power:** último campo independente. Se não houve rejeição válida, NOT_FALSIFIED_IN_THIS_CONTRACT acompanhado de POWER_NOT_EVALUATED ou classificação condicional apropriada. Poder insuficiente nunca retorna antes dos campos2–6.

Falta de calibração não vira NOT_FALSIFIED por padrão: é ausência de teste calibrado. Falta de dados não é resultado nulo. Nenhuma saída automática diz CONFIRMED ou move o gate. Falha comum aos modelos no suporte é primeiro questão do instrumento/contrato, não seleção do vencedor.

## 9. Novidade de uso, alternativas e decisão revisável

Reutilizamos a auditoria local de proveniência, incluindo seu adendo: antecedente holográfico em novembro, ramo inverso de dezembro separado e incompatível com o valor teórico, relação/fatoração em janeiro/março, D1a em maio e D1b em junho. São marcos com os estatutos e limites da auditoria; não reabrimos suas fontes originais nem transferimos números do ramo ajustado à predição fixa.

**Retrodição sem ajuste é evidência de pleno direito.** A existência anterior dos dados e o uso de IA não a desqualificam. Para o selo USE_NOVEL, rastrear o parâmetro fixo, a lei, os chamadores e o que foi aprendido/escolhido a partir dos dados, usando fontes/hash e preservando ramos contrários. Isto é distinto de afirmar ignorância histórica de todos os dados. O pré-registro é do teste: função de veredito, dados, covariâncias, variantes, modelos/priors, método de calibração e livro de seleção, antes do composto. Conhecimento anterior não autoriza duplicar dados ou ocultar seleção.

| Alternativa concreta | O que entrega | Limite | Recomendação |
|---|---|---|---|
| A. Família frequentista calibrada + lnB separado | Compatibilidade, rejeição de rivais definidos e sigma equivalente com escopo controlado | Requer calibração do nulo composto/cauda; não foi realizada | **Escolher para a meta5σ**, sem prometer que o resultado será5σ |
| B. Comparação bayesiana relativa + checagem preditiva própria | Preferência e adequação preditiva, sem rotular sigma global | Medida plana imprópria não gera prior-preditivo; usar prior próprio ou distribuição justificada em coordenadas livres de η. Cauda posterior-preditiva não é p frequentista uniforme | Viável como entrega bayesiana se não se adotar a calibração de A; nunca renomear lnB como sigma |

Decisões propostas ao operador/ROOT, que não foram tomadas por este documento: (a) A para significância ou B sem sigma; (b) os cinco mapas e dados comuns, fundo/prior e compressões; (c) família finita600etiquetas e limites; (d) cinco testes, cauda superior equivalente e alcance da multiplicidade; (e) medida η comum e priors transportados; (f) critérios/recursos de certificação numérica em unidade posterior, antes de abertura observada.

Não é necessário provar ausência de toda sistemática imaginável. É necessário dizer precisamente qual experimento/modelo de erro foi testado e limitar a conclusão a ele. O contrato não exige novos dados nesta unidade, não cria missão para executores indisponíveis e não ordena simulações. Ele torna a escolha científica revisável.

## 10. Custódia e alcance desta entrega

`SOURCES.json` contém14snapshots byte a byte e hashes efetivamente lidos, incluindo o candidato F9 solicitado pela coordenação, projeto linear, medida plana, controles existentes, preflight262, notaH5 e proveniência. `F9_VERDICT_CONTRACT_CANDIDATE.json` expressa a decisão em campos de máquina. Campos fit/y/S/g/H0/lnB/sigma/global_power são null; `opening_authorized=false`.

São definições de estatísticas e regras condicionais, não valores observados ou calibração executada. A seleção de modelos, pressupostos de erro, novidade de uso e abertura permanecem separados. A função antiga com z_TGL/z_LCDM indefinidos não pode ser usada como atalho por cima deste contrato candidato.

<!-- F9_VERDICT_ROOT_THEORY_CONTROL_READONLY_20261006 -->
## 11. Atualização de prontidão — lote teórico da ROOT, sem ampliar escopo

[REAL — recibos consultados, não rerun] Depois da preparação deste contrato, a coordenação executou sua unidade autorizada com o motor corrigido. Dez unidades / cinco pares baseline-referência passaram; maior diferença relativa 5.41048670841e-07 (zdrag/corner_LLL), abaixo do limiar1e−5. Controlador 7.263976766s; solvers somados 0.200314653s; RSSmáximo 95932KiB. O custo dominante desta pequena rodada foi processo/bootstrap. Nenhuma tabela/grade ampliada, ajuste ou dado observado foi aberto por esse controle.

Esta unidade leu somente os dois recibos e conferiu seus hashes e os pins do motor/protocolo; não releu as previsões brutas nem repetiu pontos. `BACKGROUND_CONTROL_REFERENCE.json` e dois snapshots adicionais registram a fonte. O resultado qualifica apenas os5pontos, não o prior contínuo, a compatibilidade de compressõesPlanck, a integral bayesiana ou a cauda de5σ. Os campos observados/calibrados do contrato permanecem null. Motor e protocolo consumidos não foram alterados após a execução da ROOT.

